"""plots.py SAMPLE 함수 기본 동작 테스트.

SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
"""
from __future__ import annotations

import sys
import os

import numpy as np
import pytest

# conftest.py 가 scripts/ 를 sys.path 에 추가하므로 직접 import 가능
import plots  # noqa: E402 (conftest 가 경로 세팅)


# ---------------------------------------------------------------------------
# scatter_si
# ---------------------------------------------------------------------------

def test_scatter_si_creates_png(tmp_path):
    """scatter_si: 합성 데이터로 PNG 파일이 생성되는지 확인."""
    rng = np.random.default_rng(0)
    o = rng.uniform(0.5, 4.0, 30)
    f = o + rng.normal(0, 0.3, 30)

    out = tmp_path / "scatter_test.png"
    result = plots.scatter_si(o, f, str(out), units="m")

    assert os.path.isfile(result), f"PNG 생성 실패: {result}"
    assert result.endswith(".png")


def test_scatter_si_with_nans(tmp_path):
    """scatter_si: NaN 포함 배열에서도 크래시 없이 PNG 생성."""
    o = np.array([1.0, 2.0, float("nan"), 4.0, 5.0])
    f = np.array([1.1, float("nan"), 3.0, 3.8, 5.2])

    out = tmp_path / "scatter_nan.png"
    result = plots.scatter_si(o, f, str(out))

    assert os.path.isfile(result)


def test_scatter_si_all_nan(tmp_path):
    """scatter_si: 전부 NaN 이면 크래시 없이 PNG 생성(n=0)."""
    o = np.full(5, float("nan"))
    f = np.full(5, float("nan"))

    out = tmp_path / "scatter_allnan.png"
    result = plots.scatter_si(o, f, str(out), units="s")

    assert os.path.isfile(result)


def test_scatter_si_returns_abspath(tmp_path):
    """scatter_si: 반환값이 절대 경로인지 확인."""
    o = np.array([1.0, 2.0, 3.0])
    f = np.array([1.1, 2.2, 2.9])

    out = tmp_path / "scatter_abs.png"
    result = plots.scatter_si(o, f, str(out))

    assert os.path.isabs(result)


# ---------------------------------------------------------------------------
# timeseries_overlay
# ---------------------------------------------------------------------------

def test_timeseries_overlay_creates_png(tmp_path):
    """timeseries_overlay: 숫자 시간 축으로 PNG 생성 확인."""
    t = np.arange(10)
    o = np.sin(t * 0.5)
    f = o + np.random.default_rng(1).normal(0, 0.1, 10)

    out = tmp_path / "ts_test.png"
    result = plots.timeseries_overlay(t, o, f, str(out))

    assert os.path.isfile(result)


def test_timeseries_overlay_with_nans(tmp_path):
    """timeseries_overlay: NaN 포함 시 크래시 없이 PNG 생성."""
    t = np.arange(6, dtype=float)
    o = np.array([1.0, float("nan"), 3.0, 4.0, float("nan"), 6.0])
    f = np.array([1.1, 2.0, float("nan"), 3.9, 5.0, 6.1])

    out = tmp_path / "ts_nan.png"
    result = plots.timeseries_overlay(t, o, f, str(out))

    assert os.path.isfile(result)


# ---------------------------------------------------------------------------
# diff_map
# ---------------------------------------------------------------------------

def test_diff_map_creates_png(tmp_path):
    """diff_map: 점 위치 + 편차 데이터로 PNG 생성 확인."""
    rng = np.random.default_rng(7)
    lat = rng.uniform(33.0, 38.0, 20)
    lon = rng.uniform(124.0, 132.0, 20)
    diff = rng.normal(0, 0.5, 20)

    out = tmp_path / "diffmap_test.png"
    result = plots.diff_map(lat, lon, diff, str(out), units="m")

    assert os.path.isfile(result)


def test_diff_map_with_nans(tmp_path):
    """diff_map: NaN 포함 시 크래시 없이 PNG 생성."""
    lat = np.array([35.0, float("nan"), 36.0, 37.0])
    lon = np.array([127.0, 128.0, float("nan"), 130.0])
    diff = np.array([0.1, -0.2, 0.3, float("nan")])

    out = tmp_path / "diffmap_nan.png"
    result = plots.diff_map(lat, lon, diff, str(out))

    assert os.path.isfile(result)
