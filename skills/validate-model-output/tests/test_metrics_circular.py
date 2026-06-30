"""tests/test_metrics_circular.py — 원형 통계 지표 단위 테스트.

소유: scripts/metrics_circular.py
"""
from __future__ import annotations

import math
import sys
import os

import numpy as np
import pytest

# conftest 가 scripts/ 를 sys.path 에 추가하지만, 직접 실행 안전망
_SKILL_ROOT = os.path.dirname(os.path.dirname(__file__))
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

from scripts.metrics_circular import (
    circular_mean_error,
    circular_rmse,
    circular_corr,
)


# ---------------------------------------------------------------------------
# circular_mean_error
# ---------------------------------------------------------------------------

class TestCircularMeanError:
    """circular_mean_error 검증."""

    def test_scalar_wrap_negative(self):
        """350° 예보, 10° 관측 → 오차 ≈ -20° (단거리 ±180 규약)."""
        result = circular_mean_error(350.0, 10.0)
        assert abs(result - (-20.0)) < 1e-6, f"expected -20.0, got {result}"

    def test_scalar_wrap_positive(self):
        """10° 예보, 350° 관측 → 오차 ≈ +20°."""
        result = circular_mean_error(10.0, 350.0)
        assert abs(result - 20.0) < 1e-6, f"expected +20.0, got {result}"

    def test_identical_scalar_zero(self):
        """동일값 → 오차 0."""
        assert circular_mean_error(45.0, 45.0) == pytest.approx(0.0, abs=1e-9)

    def test_identical_array_zero(self):
        """동일 배열 → 평균 오차 0."""
        a = np.array([0.0, 90.0, 180.0, 270.0, 350.0])
        result = circular_mean_error(a, a)
        assert abs(result) < 1e-9, f"expected 0, got {result}"

    def test_north_crossing(self):
        """북쪽(0°) 근방 교차 오차 — 거리는 작아야 한다.

        예: forecast=5°, observed=355° → 오차 +10° (not ±350°).
        """
        result = circular_mean_error(5.0, 355.0)
        assert abs(result - 10.0) < 1e-6, f"expected 10.0, got {result}"

    def test_array_mean_sign(self):
        """배열 평균: [350,350] vs [10,10] → 평균 오차 -20°."""
        f = np.array([350.0, 350.0])
        o = np.array([10.0, 10.0])
        result = circular_mean_error(f, o)
        assert abs(result - (-20.0)) < 1e-6

    def test_nan_safe(self):
        """NaN 포함 배열 → NaN 무시하고 유효값으로 계산."""
        f = np.array([350.0, np.nan])
        o = np.array([10.0, np.nan])
        result = circular_mean_error(f, o)
        assert math.isfinite(result), f"expected finite, got {result}"
        assert abs(result - (-20.0)) < 1e-6

    def test_opposite_directions(self):
        """정반대 방향: forecast=0°, observed=180° → 오차 ±180°."""
        result = circular_mean_error(0.0, 180.0)
        # _wrap180: (0-180+180)%360-180 = 180%360-180 = 0 → but 0-180=-180
        # (-180+180)%360-180 = 0-180 = -180
        # 규약상 -180 또는 +180 둘 다 허용
        assert abs(abs(result) - 180.0) < 1e-6, f"expected ±180, got {result}"


# ---------------------------------------------------------------------------
# circular_rmse
# ---------------------------------------------------------------------------

class TestCircularRmse:
    """circular_rmse 검증."""

    def test_scalar_20deg(self):
        """350° vs 10° → RMSE = 20°."""
        result = circular_rmse(350.0, 10.0)
        assert abs(result - 20.0) < 1e-6, f"expected 20.0, got {result}"

    def test_identical_scalar_zero(self):
        assert circular_rmse(90.0, 90.0) == pytest.approx(0.0, abs=1e-9)

    def test_identical_array_zero(self):
        a = np.array([0.0, 45.0, 90.0, 180.0, 270.0, 315.0])
        assert circular_rmse(a, a) == pytest.approx(0.0, abs=1e-9)

    def test_nonnegative(self):
        """RMSE 는 항상 ≥ 0."""
        rng = np.random.default_rng(7)
        f = rng.uniform(0, 360, 50)
        o = rng.uniform(0, 360, 50)
        assert circular_rmse(f, o) >= 0.0

    def test_symmetry(self):
        """RMSE 는 f와 o를 바꿔도 같다."""
        f = np.array([350.0, 5.0, 100.0])
        o = np.array([10.0, 355.0, 80.0])
        assert abs(circular_rmse(f, o) - circular_rmse(o, f)) < 1e-9

    def test_mixed_errors(self):
        """[350,10] vs [10,350] → 두 오차 모두 -20/+20 → RMSE = 20."""
        f = np.array([350.0, 10.0])
        o = np.array([10.0, 350.0])
        result = circular_rmse(f, o)
        assert abs(result - 20.0) < 1e-6


# ---------------------------------------------------------------------------
# circular_corr
# ---------------------------------------------------------------------------

class TestCircularCorr:
    """circular_corr 검증."""

    def test_near_perfect_corr(self):
        """거의 같은 배열(오프셋 5°) → 상관 ≈ 1."""
        f = np.array([0.0, 90.0, 180.0, 270.0, 10.0, 100.0])
        o = f + 5.0  # 동일 패턴, 5° 바이어스
        result = circular_corr(f, o)
        assert result > 0.99, f"expected >0.99, got {result}"

    def test_return_range(self):
        """반환값 ∈ [-1, 1]."""
        rng = np.random.default_rng(99)
        f = rng.uniform(0, 360, 30)
        o = rng.uniform(0, 360, 30)
        result = circular_corr(f, o)
        assert -1.0 <= result <= 1.0

    def test_identical_array_perfect_corr(self):
        """동일(다변동) 배열 → 완전 상관 1.0."""
        a = np.array([10.0, 20.0, 30.0, 40.0])
        result = circular_corr(a, a)
        assert abs(result - 1.0) < 1e-9, f"expected 1.0 for identical arrays, got {result}"

    def test_constant_array_nan(self):
        """상수 배열 → sin(f - f_bar)=0 → 분모 0 → nan (SAMPLE 주의사항 문서화)."""
        a = np.array([45.0, 45.0, 45.0, 45.0])
        result = circular_corr(a, a)
        assert math.isnan(result), f"expected nan for constant arrays, got {result}"

    def test_anticorrelated(self):
        """반대 패턴(sin 부호 반전) → 음의 상관."""
        base = np.linspace(0, 340, 18)
        f = base
        o = (base + 180.0) % 360.0  # 정반대 방향
        result = circular_corr(f, o)
        assert result < 0.0, f"expected negative corr, got {result}"
