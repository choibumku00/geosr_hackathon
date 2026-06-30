"""plots.py 신규 함수(qq_plot / taylor_diagram / wave_rose / diff_map 2D) 테스트.

SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
"""
from __future__ import annotations

import os

import numpy as np
import pytest

# conftest.py 가 scripts/ 를 sys.path 에 추가
import plots  # noqa: E402


# ---------------------------------------------------------------------------
# qq_plot
# ---------------------------------------------------------------------------

def test_qq_plot_creates_png(tmp_path):
    """qq_plot: 합성 데이터로 PNG 생성 확인."""
    rng = np.random.default_rng(42)
    o = rng.uniform(0.5, 4.0, 50)
    f = o + rng.normal(0.0, 0.4, 50)

    out = tmp_path / "qq_test.png"
    result = plots.qq_plot(o, f, str(out))

    assert os.path.isfile(result), f"PNG 생성 실패: {result}"
    assert result.endswith(".png")


def test_qq_plot_with_nans(tmp_path):
    """qq_plot: NaN 포함 배열에서 크래시 없이 PNG 생성."""
    o = np.array([1.0, 2.0, float("nan"), 4.0, 5.0, 6.0])
    f = np.array([1.1, float("nan"), 3.0, 3.9, float("nan"), 6.1])

    out = tmp_path / "qq_nan.png"
    result = plots.qq_plot(o, f, str(out))

    assert os.path.isfile(result)


def test_qq_plot_all_nan(tmp_path):
    """qq_plot: 전부 NaN → 크래시 없이 PNG 생성(no-valid-data 표시)."""
    o = np.full(6, float("nan"))
    f = np.full(6, float("nan"))

    out = tmp_path / "qq_allnan.png"
    result = plots.qq_plot(o, f, str(out))

    assert os.path.isfile(result)


def test_qq_plot_unequal_lengths(tmp_path):
    """qq_plot: 관측·예보 배열 크기가 달라도 크래시 없이 PNG 생성."""
    rng = np.random.default_rng(7)
    o = rng.normal(2.0, 0.5, 30)
    f = rng.normal(2.2, 0.6, 50)  # 다른 크기

    out = tmp_path / "qq_unequal.png"
    result = plots.qq_plot(o, f, str(out))

    assert os.path.isfile(result)


def test_qq_plot_returns_abspath(tmp_path):
    """qq_plot: 반환값이 절대 경로인지 확인."""
    o = np.array([1.0, 2.0, 3.0])
    f = np.array([1.2, 2.1, 3.0])

    out = tmp_path / "qq_abs.png"
    result = plots.qq_plot(o, f, str(out))

    assert os.path.isabs(result)


# ---------------------------------------------------------------------------
# taylor_diagram
# ---------------------------------------------------------------------------

def test_taylor_diagram_creates_png(tmp_path):
    """taylor_diagram: 합성 데이터로 PNG 생성 확인."""
    rng = np.random.default_rng(10)
    o = rng.uniform(1.0, 5.0, 40)
    f = 0.9 * o + rng.normal(0.0, 0.3, 40)

    out = tmp_path / "taylor_test.png"
    result = plots.taylor_diagram(o, f, str(out))

    assert os.path.isfile(result), f"PNG 생성 실패: {result}"
    assert result.endswith(".png")


def test_taylor_diagram_with_nans(tmp_path):
    """taylor_diagram: NaN 포함 배열에서 크래시 없이 PNG 생성."""
    o = np.array([1.0, 2.0, float("nan"), 4.0, 5.0])
    f = np.array([float("nan"), 2.1, 3.0, 3.9, 5.1])

    out = tmp_path / "taylor_nan.png"
    result = plots.taylor_diagram(o, f, str(out))

    assert os.path.isfile(result)


def test_taylor_diagram_all_nan(tmp_path):
    """taylor_diagram: 전부 NaN → 크래시 없이 PNG 생성."""
    o = np.full(5, float("nan"))
    f = np.full(5, float("nan"))

    out = tmp_path / "taylor_allnan.png"
    result = plots.taylor_diagram(o, f, str(out))

    assert os.path.isfile(result)


def test_taylor_diagram_low_corr(tmp_path):
    """taylor_diagram: 낮은 상관(음수 포함 가능) 시 크래시 없이 PNG 생성."""
    rng = np.random.default_rng(99)
    o = rng.uniform(0.0, 10.0, 50)
    f = rng.uniform(0.0, 10.0, 50)  # 무상관

    out = tmp_path / "taylor_lowcorr.png"
    result = plots.taylor_diagram(o, f, str(out))

    assert os.path.isfile(result)


def test_taylor_diagram_returns_abspath(tmp_path):
    """taylor_diagram: 반환값이 절대 경로인지 확인."""
    o = np.array([1.0, 2.0, 3.0, 4.0])
    f = np.array([1.1, 2.2, 2.9, 4.1])

    out = tmp_path / "taylor_abs.png"
    result = plots.taylor_diagram(o, f, str(out))

    assert os.path.isabs(result)


# ---------------------------------------------------------------------------
# wave_rose
# ---------------------------------------------------------------------------

def test_wave_rose_creates_png(tmp_path):
    """wave_rose: 합성 방향·파고 데이터로 PNG 생성 확인."""
    rng = np.random.default_rng(20)
    directions = rng.uniform(0.0, 360.0, 100)
    heights = rng.uniform(0.3, 4.0, 100)

    out = tmp_path / "rose_test.png"
    result = plots.wave_rose(directions, heights, str(out))

    assert os.path.isfile(result), f"PNG 생성 실패: {result}"
    assert result.endswith(".png")


def test_wave_rose_with_nans(tmp_path):
    """wave_rose: NaN 포함 시 크래시 없이 PNG 생성."""
    dirs = np.array([0.0, 90.0, float("nan"), 180.0, 270.0, float("nan")])
    mags = np.array([1.0, float("nan"), 2.0, 3.0, 0.5, 4.0])

    out = tmp_path / "rose_nan.png"
    result = plots.wave_rose(dirs, mags, str(out))

    assert os.path.isfile(result)


def test_wave_rose_all_nan(tmp_path):
    """wave_rose: 전부 NaN → 크래시 없이 PNG 생성."""
    dirs = np.full(5, float("nan"))
    mags = np.full(5, float("nan"))

    out = tmp_path / "rose_allnan.png"
    result = plots.wave_rose(dirs, mags, str(out))

    assert os.path.isfile(result)


def test_wave_rose_single_direction(tmp_path):
    """wave_rose: 단일 방향 집중 배열에서 크래시 없이 PNG 생성."""
    dirs = np.full(20, 45.0)   # 모두 NE
    mags = np.ones(20) * 2.0

    out = tmp_path / "rose_single.png"
    result = plots.wave_rose(dirs, mags, str(out))

    assert os.path.isfile(result)


def test_wave_rose_returns_abspath(tmp_path):
    """wave_rose: 반환값이 절대 경로인지 확인."""
    dirs = np.linspace(0.0, 350.0, 36)
    mags = np.ones(36)

    out = tmp_path / "rose_abs.png"
    result = plots.wave_rose(dirs, mags, str(out))

    assert os.path.isabs(result)


# ---------------------------------------------------------------------------
# diff_map — 2D pcolormesh 경로
# ---------------------------------------------------------------------------

def test_diff_map_2d_creates_png(tmp_path):
    """diff_map: 2D 격자 입력 시 pcolormesh PNG 생성 확인."""
    rng = np.random.default_rng(30)
    lat2d = np.tile(np.linspace(33.0, 38.0, 10), (12, 1)).T   # (10, 12)
    lon2d = np.tile(np.linspace(124.0, 132.0, 12), (10, 1))    # (10, 12)
    diff2d = rng.normal(0.0, 0.5, (10, 12))

    out = tmp_path / "diffmap_2d.png"
    result = plots.diff_map(lat2d, lon2d, diff2d, str(out), units="m")

    assert os.path.isfile(result), f"PNG 생성 실패: {result}"
    assert result.endswith(".png")


def test_diff_map_2d_with_nans(tmp_path):
    """diff_map: 2D NaN 포함 시 크래시 없이 PNG 생성(masked pcolormesh)."""
    rng = np.random.default_rng(31)
    lat2d = np.tile(np.linspace(34.0, 37.0, 5), (6, 1)).T
    lon2d = np.tile(np.linspace(125.0, 130.0, 6), (5, 1))
    diff2d = rng.normal(0.0, 1.0, (5, 6))
    diff2d[1, 2] = float("nan")
    diff2d[3, 0] = float("nan")

    out = tmp_path / "diffmap_2d_nan.png"
    result = plots.diff_map(lat2d, lon2d, diff2d, str(out))

    assert os.path.isfile(result)


def test_diff_map_2d_returns_abspath(tmp_path):
    """diff_map 2D: 반환값이 절대 경로인지 확인."""
    lat2d = np.tile(np.linspace(35.0, 37.0, 4), (5, 1)).T
    lon2d = np.tile(np.linspace(126.0, 130.0, 5), (4, 1))
    diff2d = np.zeros((4, 5))

    out = tmp_path / "diffmap_2d_abs.png"
    result = plots.diff_map(lat2d, lon2d, diff2d, str(out))

    assert os.path.isabs(result)
