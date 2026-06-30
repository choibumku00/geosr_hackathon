"""tests/test_derive.py — derive 모듈 단위 테스트.

기상학적 풍향 규약(FROM direction, 0°=북 기준 시계방향):
  u=0,  v<0  → 0°   (북풍)
  u<0,  v=0  → 90°  (동풍)
  u=0,  v>0  → 180° (남풍)
  u>0,  v=0  → 270° (서풍)
"""
from __future__ import annotations

import math

import numpy as np
import pytest

import derive  # conftest.py 가 scripts/ 를 sys.path 에 추가


# ---------------------------------------------------------------------------
# windspeed
# ---------------------------------------------------------------------------

class TestWindspeed:
    def test_3_4_5(self):
        """피타고라스 3-4-5 케이스."""
        assert derive.windspeed(3, 4) == pytest.approx(5.0)

    def test_zero_zero(self):
        assert derive.windspeed(0, 0) == pytest.approx(0.0)

    def test_negative_components(self):
        """음수 성분도 절댓값 합산."""
        assert derive.windspeed(-3, -4) == pytest.approx(5.0)

    def test_scalar_float(self):
        assert derive.windspeed(1.0, 0.0) == pytest.approx(1.0)

    def test_array_input(self):
        u = np.array([0.0, 3.0])
        v = np.array([1.0, 4.0])
        result = derive.windspeed(u, v)
        np.testing.assert_allclose(result, [1.0, 5.0])

    def test_nan_propagates_u(self):
        result = derive.windspeed(float("nan"), 1.0)
        assert math.isnan(float(result))

    def test_nan_propagates_v(self):
        result = derive.windspeed(1.0, float("nan"))
        assert math.isnan(float(result))

    def test_returns_numpy_type(self):
        """스칼라 입력 시 numpy 스칼라(np.generic) 또는 ndarray 반환."""
        result = derive.windspeed(3, 4)
        assert isinstance(result, (np.ndarray, np.generic))


# ---------------------------------------------------------------------------
# wind_direction
# ---------------------------------------------------------------------------

class TestWindDirection:
    """기상학적 풍향 규약(FROM direction, 0°=북 기준 시계방향) 검증."""

    def test_north_wind(self):
        """u=0, v=-1 → 북쪽에서 오는 바람 → 0°."""
        result = float(derive.wind_direction(0, -1))
        assert result == pytest.approx(0.0)

    def test_south_wind(self):
        """u=0, v=1 → 남쪽에서 오는 바람 → 180°."""
        result = float(derive.wind_direction(0, 1))
        assert result == pytest.approx(180.0)

    def test_east_wind(self):
        """u=-1, v=0 → 동쪽에서 오는 바람 → 90°."""
        result = float(derive.wind_direction(-1, 0))
        assert result == pytest.approx(90.0)

    def test_west_wind(self):
        """u=1, v=0 → 서쪽에서 오는 바람 → 270°."""
        result = float(derive.wind_direction(1, 0))
        assert result == pytest.approx(270.0)

    def test_northeast_wind(self):
        """u=-1, v=-1 → 북동풍 → 45°."""
        result = float(derive.wind_direction(-1, -1))
        assert result == pytest.approx(45.0)

    def test_southwest_wind(self):
        """u=1, v=1 → 남서풍 → 225°."""
        result = float(derive.wind_direction(1, 1))
        assert result == pytest.approx(225.0)

    def test_calm(self):
        """u=0, v=0 (정온) → 방향 미정의; [0, 360) 범위 내 임의 값 허용.

        IEEE 754 에서 atan2(-0.0, -0.0) = -π 이므로 정확히 0° 가 아닐 수 있다.
        정온 시 풍향은 수학적으로 미정의이므로 범위만 검증한다.
        """
        result = float(derive.wind_direction(0, 0))
        assert 0.0 <= result < 360.0

    def test_range_0_to_360(self):
        """결과가 항상 [0, 360) 범위에 있어야 한다."""
        angles = np.linspace(0, 2 * math.pi, 360)
        u = np.cos(angles)
        v = np.sin(angles)
        dirs = derive.wind_direction(u, v)
        assert np.all(dirs >= 0.0)
        assert np.all(dirs < 360.0)

    def test_nan_propagates_u(self):
        result = derive.wind_direction(float("nan"), 1.0)
        assert math.isnan(float(result))

    def test_nan_propagates_v(self):
        result = derive.wind_direction(1.0, float("nan"))
        assert math.isnan(float(result))

    def test_array_cardinal_directions(self):
        """배열 입력으로 4방위 동시 검증."""
        u = np.array([0.0, 0.0, -1.0, 1.0])
        v = np.array([-1.0, 1.0, 0.0, 0.0])
        expected = np.array([0.0, 180.0, 90.0, 270.0])
        result = derive.wind_direction(u, v)
        np.testing.assert_allclose(result, expected, atol=1e-10)

    def test_returns_numpy_type(self):
        """스칼라 입력 시 numpy 스칼라(np.generic) 또는 ndarray 반환."""
        result = derive.wind_direction(1, -1)
        assert isinstance(result, (np.ndarray, np.generic))

    def test_strong_north_wind(self):
        """크기가 달라도 방향은 동일해야 한다 (u=0, v=-10 → 0°)."""
        result = float(derive.wind_direction(0, -10))
        assert result == pytest.approx(0.0)
