"""Regression tests: coord_kind() with 2D lat/lon stored as data_vars.

Bug: After mesh refactor, latlon() was restricted to coords-only search.
Real GFS-like datasets store 2D lat/lon as data_vars (not coords) →
coord_kind() returned 'none' (regression).

Fix verifies:
  1. 2D lat/lon in data_vars  → coord_kind == '2d', is_mesh() == False
  2. ww3_mesh_like (1D data_var lat/lon sharing 'node' dim) → 'mesh' unchanged
  3. era5_like (1D lat/lon in coords) → '1d' unchanged

SAMPLE — 실데이터 실시간 점검·도메인 맞춤 코드로 적응.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import xarray as xr
import pytest

# scripts/ 경로 보장
_SCRIPTS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"
)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

# tests/ 경로 보장 (synth* import 용)
_TESTS = os.path.dirname(os.path.abspath(__file__))
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)

from dataset import Dataset
from synth import era5_like
from synth_waves import ww3_mesh_like


# ── 보조 픽스처 ──────────────────────────────────────────────────────────────

def _gfs_datavar_like() -> xr.Dataset:
    """2D lat/lon을 **data_vars** 에 저장한 GFS 유사 Dataset.

    assign_coords 를 사용하지 않아 lat/lon 이 xr.Dataset.coords 에 없다.
    이것이 회귀 버그를 재현하는 핵심 조건이다.
    """
    ny, nx = 6, 8
    lat2d = (
        np.linspace(30.0, 40.0, ny)[:, None] * np.ones((ny, nx))
    ).astype("float32")
    lon2d = (
        np.ones((ny, nx)) * np.linspace(120.0, 130.0, nx)[None, :]
    ).astype("float32")

    t2m = xr.DataArray(
        np.full((ny, nx), 280.0, dtype="float32"),
        dims=("y", "x"),
        attrs={"units": "K", "standard_name": "air_temperature"},
    )
    lat_da = xr.DataArray(
        lat2d, dims=("y", "x"),
        attrs={"units": "degrees_north", "standard_name": "latitude"},
    )
    lon_da = xr.DataArray(
        lon2d, dims=("y", "x"),
        attrs={"units": "degrees_east", "standard_name": "longitude"},
    )
    # lat/lon 을 의도적으로 data_vars 에 배치 (coords 아님)
    ds = xr.Dataset({"t2m": t2m, "lat": lat_da, "lon": lon_da})
    # coords 에 없음을 명시 확인
    assert "lat" not in ds.coords and "lon" not in ds.coords, (
        "픽스처 생성 오류: lat/lon 이 coords 에 올라가 있으면 회귀 재현 안 됨"
    )
    return ds


def _gfs_datavar_standard_name_like() -> xr.Dataset:
    """2D lat/lon을 'latitude'/'longitude' 이름으로 data_vars 에 저장한 변형."""
    ny, nx = 4, 5
    lat2d = (
        np.linspace(33.0, 38.0, ny)[:, None] * np.ones((ny, nx))
    ).astype("float32")
    lon2d = (
        np.ones((ny, nx)) * np.linspace(124.0, 132.0, nx)[None, :]
    ).astype("float32")

    ds = xr.Dataset({
        "TMP": xr.DataArray(
            np.full((ny, nx), 15.0, dtype="float32"), dims=("y", "x"),
            attrs={"units": "degC"},
        ),
        "latitude": xr.DataArray(
            lat2d, dims=("y", "x"),
            attrs={"units": "degrees_north", "standard_name": "latitude"},
        ),
        "longitude": xr.DataArray(
            lon2d, dims=("y", "x"),
            attrs={"units": "degrees_east", "standard_name": "longitude"},
        ),
    })
    return ds


# ── Case 1: 2D lat/lon in data_vars ──────────────────────────────────────────

class TestCoord2dDataVar:
    """2D lat/lon 이 data_vars 에 있을 때 coord_kind=='2d' 회귀 복구 확인."""

    def setup_method(self):
        self.ds = Dataset(_gfs_datavar_like())

    def test_coord_kind_is_2d(self):
        """핵심 회귀: 2D data_var lat/lon → coord_kind == '2d'."""
        kind = self.ds.coord_kind()
        assert kind == "2d", (
            f"회귀 버그: 2D data_var lat/lon 인데 coord_kind='{kind}' (expected '2d')"
        )

    def test_latlon_returns_tuple(self):
        """latlon()이 None 이 아닌 (lat_name, lon_name, True) 를 반환해야 한다."""
        ll = self.ds.latlon()
        assert ll is not None, "latlon() must find 2D data_var lat/lon"
        lat_name, lon_name, is_2d = ll
        assert is_2d is True, "is_2d must be True for 2D lat/lon"

    def test_latlon_var_names(self):
        """반환된 lat/lon 이름이 실제 Dataset 에 있어야 한다."""
        lat_name, lon_name, _ = self.ds.latlon()
        assert lat_name in self.ds.xr
        assert lon_name in self.ds.xr

    def test_grid_shape(self):
        """grid_shape()가 (ny, nx) == (6, 8)을 반환해야 한다."""
        shape = self.ds.grid_shape()
        assert shape == (6, 8), f"Expected (6,8), got {shape}"

    def test_is_mesh_false(self):
        """2D data_var lat/lon 은 mesh 가 아니다."""
        assert self.ds.is_mesh() is False, (
            "2D data_var lat/lon 을 mesh 로 오인해선 안 된다"
        )


class TestCoord2dDataVarStandardName:
    """'latitude'/'longitude' 이름으로 data_vars 에 2D 저장된 경우도 인식."""

    def setup_method(self):
        self.ds = Dataset(_gfs_datavar_standard_name_like())

    def test_coord_kind_is_2d(self):
        assert self.ds.coord_kind() == "2d"

    def test_is_mesh_false(self):
        assert self.ds.is_mesh() is False

    def test_grid_shape(self):
        assert self.ds.grid_shape() == (4, 5)


# ── Case 2: ww3_mesh_like — 기존 mesh 동작 불변 ──────────────────────────────

class TestMeshUnchanged:
    """ww3_mesh_like: 1D data_var lat/lon, 동일 'node' 차원 → 'mesh' 유지."""

    def setup_method(self):
        self.ds = Dataset(ww3_mesh_like())

    def test_coord_kind_is_mesh(self):
        assert self.ds.coord_kind() == "mesh", (
            f"ww3_mesh_like 는 'mesh' 여야 하는데 '{self.ds.coord_kind()}' 반환"
        )

    def test_is_mesh_true(self):
        assert self.ds.is_mesh() is True

    def test_latlon_none_for_mesh(self):
        """mesh에서 latlon()은 None이어야 한다 (정규 격자 없음)."""
        assert self.ds.latlon() is None, (
            "1D data_var lat/lon 을 2D 정규 격자로 오인하면 안 된다"
        )

    def test_grid_shape_nodes(self):
        assert self.ds.grid_shape() == (40,)


# ── Case 3: era5_like — 기존 1D coords 동작 불변 ─────────────────────────────

class TestEra5Unchanged:
    """era5_like: 1D lat/lon in coords → coord_kind == '1d' 유지."""

    def setup_method(self):
        self.ds = Dataset(era5_like())

    def test_coord_kind_is_1d(self):
        assert self.ds.coord_kind() == "1d"

    def test_is_mesh_false(self):
        assert self.ds.is_mesh() is False

    def test_latlon_1d(self):
        ll = self.ds.latlon()
        assert ll is not None
        lat_name, lon_name, is_2d = ll
        assert is_2d is False
        assert lat_name in ("lat", "latitude")
        assert lon_name in ("lon", "longitude")

    def test_grid_shape(self):
        shape = self.ds.grid_shape()
        assert shape is not None
        assert len(shape) == 2
