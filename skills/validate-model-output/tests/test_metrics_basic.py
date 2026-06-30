"""tests/test_metrics_basic.py — metrics_basic 모듈 단위 테스트.

conftest.py 가 scripts/ 를 sys.path 에 추가하므로 직접 import.
실행: python -m pytest tests/test_metrics_basic.py -q
"""
from __future__ import annotations

import math

import numpy as np
import pytest

import metrics_basic as mb


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def _pair(n: int = 100, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """관측 o ~ Uniform(1, 5), 예측 f = o + 1 (일정 bias = 1)."""
    rng = np.random.default_rng(seed)
    o = rng.uniform(1.0, 5.0, n)
    f = o + 1.0
    return f, o


# ---------------------------------------------------------------------------
# 기본 수치 검증 (f = o + 1)
# ---------------------------------------------------------------------------

class TestConstantOffset:
    """f = o + 1 일 때 해석적으로 알 수 있는 값 검증."""

    def test_bias_equals_one(self):
        f, o = _pair()
        assert abs(mb.bias(f, o) - 1.0) < 1e-10

    def test_mae_equals_one(self):
        f, o = _pair()
        assert abs(mb.mae(f, o) - 1.0) < 1e-10

    def test_rmse_equals_one(self):
        f, o = _pair()
        assert abs(mb.rmse(f, o) - 1.0) < 1e-10

    def test_nrmse_positive(self):
        f, o = _pair()
        result = mb.nrmse(f, o)
        assert math.isfinite(result) and result > 0.0

    def test_si_nonnegative(self):
        """SI >= 0; f=o+1 은 순수 편향이므로 불편RMSE=0 → SI=0."""
        f, o = _pair()
        result = mb.si(f, o)
        assert result >= 0.0

    def test_si_zero_for_pure_bias(self):
        """일정 offset 만 있으면 무작위 오차 없음 → SI = 0."""
        f, o = _pair()
        assert abs(mb.si(f, o)) < 1e-10

    def test_pearson_r_near_one(self):
        """일정 offset → 상관 1."""
        f, o = _pair()
        r = mb.pearson_r(f, o)
        assert abs(r - 1.0) < 1e-10

    def test_linregress_slope_and_intercept(self):
        """f = 1*o + 1 → slope=1, intercept=1."""
        f, o = _pair()
        slope, intercept = mb.linregress(f, o)
        assert abs(slope - 1.0) < 1e-10
        assert abs(intercept - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# NaN 마스크 동작 검증
# ---------------------------------------------------------------------------

class TestNanMask:

    def test_nan_in_f_excluded(self):
        """f 에 NaN 이 있는 인덱스는 제외하고 나머지로 계산."""
        rng = np.random.default_rng(0)
        o = rng.uniform(1.0, 5.0, 20)
        f = o + 1.0
        f[3] = np.nan
        f[7] = np.nan
        # 나머지 18개 요소는 여전히 bias=1
        assert abs(mb.bias(f, o) - 1.0) < 1e-10

    def test_nan_in_o_excluded(self):
        """o 에 NaN 이 있는 인덱스는 제외."""
        o = np.array([1.0, 2.0, np.nan, 4.0])
        f = o.copy()
        f = np.where(np.isfinite(o), o + 1.0, np.nan)
        assert abs(mb.bias(f, o) - 1.0) < 1e-10

    def test_inf_excluded(self):
        """Inf 도 마스크 대상."""
        o = np.array([1.0, 2.0, np.inf, 4.0])
        f = np.array([2.0, 3.0, np.inf, 5.0])
        # inf 인덱스 제외 후 3개 요소 → bias=1
        assert abs(mb.bias(f, o) - 1.0) < 1e-10

    def test_all_nan_returns_nan(self):
        """모든 값이 NaN 이면 nan 반환 (크래시 없음)."""
        o = np.full(5, np.nan)
        f = np.full(5, np.nan)
        assert math.isnan(mb.bias(f, o))
        assert math.isnan(mb.mae(f, o))
        assert math.isnan(mb.rmse(f, o))
        assert math.isnan(mb.nrmse(f, o))
        assert math.isnan(mb.si(f, o))
        assert math.isnan(mb.pearson_r(f, o))
        s, i_ = mb.linregress(f, o)
        assert math.isnan(s) and math.isnan(i_)

    def test_single_valid_pair(self):
        """유효 쌍이 1개이면 pearson_r·linregress 는 nan, 나머지는 계산 가능."""
        o = np.array([np.nan, 2.0])
        f = np.array([np.nan, 3.0])
        assert abs(mb.bias(f, o) - 1.0) < 1e-10
        assert math.isnan(mb.pearson_r(f, o))
        s, i_ = mb.linregress(f, o)
        assert math.isnan(s)


# ---------------------------------------------------------------------------
# 정의 일관성 검증
# ---------------------------------------------------------------------------

class TestDefinitionConsistency:

    def test_rmse_geq_bias_abs(self):
        """RMSE >= |Bias| (정의상 항상 성립)."""
        rng = np.random.default_rng(7)
        o = rng.uniform(0.5, 5.0, 200)
        f = o + rng.normal(0.5, 1.0, 200)
        assert mb.rmse(f, o) >= abs(mb.bias(f, o)) - 1e-12

    def test_si_from_rmse_bias(self):
        """SI = sqrt(RMSE^2 - Bias^2) / |mean(o)| 와 일치 확인."""
        rng = np.random.default_rng(9)
        o = rng.uniform(1.0, 5.0, 200)
        f = o + rng.normal(0.5, 0.8, 200)
        expected = math.sqrt(max(0.0, mb.rmse(f, o) ** 2 - mb.bias(f, o) ** 2)) / abs(np.mean(o))
        assert abs(mb.si(f, o) - expected) < 1e-10

    def test_mae_leq_rmse(self):
        """MAE <= RMSE (Cauchy-Schwarz, 일반적으로 성립)."""
        rng = np.random.default_rng(11)
        o = rng.uniform(0.5, 5.0, 200)
        f = o + rng.normal(0.0, 1.5, 200)
        assert mb.mae(f, o) <= mb.rmse(f, o) + 1e-12

    def test_pearson_r_range(self):
        """-1 <= pearson_r <= 1."""
        rng = np.random.default_rng(13)
        o = rng.uniform(0.5, 5.0, 200)
        f = rng.uniform(0.0, 6.0, 200)
        r = mb.pearson_r(f, o)
        assert -1.0 - 1e-12 <= r <= 1.0 + 1e-12

    def test_perfect_forecast_zero_rmse(self):
        """f = o 이면 RMSE=0, Bias=0, MAE=0, SI=0."""
        o = np.linspace(1.0, 5.0, 50)
        f = o.copy()
        assert abs(mb.bias(f, o)) < 1e-12
        assert abs(mb.mae(f, o)) < 1e-12
        assert abs(mb.rmse(f, o)) < 1e-12
        assert abs(mb.si(f, o)) < 1e-12
