"""tests/test_mesh.py — R2 비정형 mesh 인식 테스트.

SAMPLE — 실데이터에서는 mesh 구조(변수명·차원명·토폴로지)를
실시간 점검하고 도메인 맞춤 코드로 적응하라.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import xarray as xr
import pytest

# scripts/ 경로 보장 (conftest.py 가 이미 추가하지만 명시적으로도 보장)
_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

# tests/ 경로 보장 (synth_waves import 용)
_TESTS = os.path.dirname(os.path.abspath(__file__))
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)

from dataset import Dataset
from synth_waves import ww3_mesh_like


# ── 보조 픽스처 ──────────────────────────────────────────────────────────

def _era5_like() -> xr.Dataset:
    """1D 정규 격자 (ERA5 모사) — 한국 근해 영역."""
    lat = np.linspace(33.0, 38.0, 5)
    lon = np.linspace(124.0, 132.0, 8)
    t2m = xr.DataArray(
        np.full((1, 5, 8), 280.0), dims=("time", "lat", "lon"),
        coords={"time": [np.datetime64("2024-01-01")], "lat": lat, "lon": lon},
        attrs={"units": "K", "standard_name": "air_temperature"},
    )
    return xr.Dataset({"t2m": t2m})


def _no_coord_ds() -> xr.Dataset:
    """lat/lon이 전혀 없는 Dataset — coord_kind()=='none' 확인용."""
    return xr.Dataset({"val": xr.DataArray(np.zeros((3, 4)), dims=("y", "x"))})


# ── mesh 인식 핵심 테스트 ─────────────────────────────────────────────────

class TestMeshDetection:
    """R2: ww3_mesh_like()가 mesh로 올바르게 인식되는지 검증."""

    def setup_method(self):
        self.ds = Dataset(ww3_mesh_like())

    def test_coord_kind_is_mesh(self):
        """coord_kind()는 'mesh'를 반환해야 한다."""
        assert self.ds.coord_kind() == "mesh", (
            f"expected 'mesh', got '{self.ds.coord_kind()}'"
        )

    def test_is_mesh_true(self):
        """is_mesh()는 True를 반환해야 한다."""
        assert self.ds.is_mesh() is True

    def test_grid_shape_is_n_nodes(self):
        """mesh grid_shape()는 (n_nodes,) == (40,)를 반환해야 한다."""
        shape = self.ds.grid_shape()
        assert shape == (40,), f"expected (40,), got {shape}"

    def test_latlon_returns_none_for_mesh(self):
        """mesh에서 latlon()은 None을 반환한다 — 정규 격자 좌표 없음."""
        assert self.ds.latlon() is None


# ── 정규 1D 격자 — 기존 동작 불변 ──────────────────────────────────────

class TestRegular1DUnchanged:
    """R2 추가 후에도 ERA5 1D 정규 격자 인식이 깨지지 않아야 한다."""

    def setup_method(self):
        self.ds = Dataset(_era5_like())

    def test_coord_kind_is_1d(self):
        assert self.ds.coord_kind() == "1d"

    def test_is_mesh_false(self):
        assert self.ds.is_mesh() is False

    def test_grid_shape_unchanged(self):
        """(n_lat, n_lon) 형태 유지."""
        assert self.ds.grid_shape() == (5, 8)

    def test_latlon_still_works(self):
        lat_name, lon_name, is_2d = self.ds.latlon()
        assert lat_name == "lat"
        assert lon_name == "lon"
        assert is_2d is False


# ── coord_kind()=='none' — 좌표 없음 케이스 ─────────────────────────────

def test_no_coord_kind_none():
    """lat/lon 좌표가 전혀 없으면 'none' 유지."""
    ds = Dataset(_no_coord_ds())
    assert ds.coord_kind() == "none"
    assert ds.is_mesh() is False
    assert ds.grid_shape() is None


# ── mesh 판별 세부 조건 ──────────────────────────────────────────────────

def test_mesh_requires_shared_dim():
    """lat/lon data var가 서로 다른 차원이면 mesh 아님."""
    ds_raw = xr.Dataset({
        "latitude":  xr.DataArray(np.linspace(33, 38, 5), dims=("node_lat",),
                                  attrs={"standard_name": "latitude"}),
        "longitude": xr.DataArray(np.linspace(124, 132, 8), dims=("node_lon",),
                                  attrs={"standard_name": "longitude"}),
    })
    ds = Dataset(ds_raw)
    assert ds.is_mesh() is False
    assert ds.coord_kind() == "none"


def test_mesh_requires_1d_vars():
    """lat/lon data var가 2D이면 mesh 조건 불충족."""
    lat2d = np.full((5, 8), 35.0)
    lon2d = np.full((5, 8), 128.0)
    ds_raw = xr.Dataset({
        "latitude":  xr.DataArray(lat2d, dims=("y", "x"),
                                  attrs={"standard_name": "latitude"}),
        "longitude": xr.DataArray(lon2d, dims=("y", "x"),
                                  attrs={"standard_name": "longitude"}),
    })
    ds = Dataset(ds_raw)
    assert ds.is_mesh() is False


def test_mesh_standard_name_detection():
    """standard_name 'latitude'/'longitude'로만 등록된 mesh 변수도 탐지."""
    rng = np.random.default_rng(0)
    n = 20
    ds_raw = xr.Dataset(
        {
            "lat_nodes": xr.DataArray(
                rng.uniform(33, 38, n), dims=("pt",),
                attrs={"standard_name": "latitude"},
            ),
            "lon_nodes": xr.DataArray(
                rng.uniform(124, 132, n), dims=("pt",),
                attrs={"standard_name": "longitude"},
            ),
            "hs": xr.DataArray(rng.uniform(0, 3, n), dims=("pt",)),
        }
    )
    ds = Dataset(ds_raw)
    assert ds.is_mesh() is True
    assert ds.coord_kind() == "mesh"
    assert ds.grid_shape() == (n,)
