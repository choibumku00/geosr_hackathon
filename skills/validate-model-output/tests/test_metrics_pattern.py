"""tests/test_metrics_pattern.py — metrics_pattern.py 단위 테스트.

검증 핵심:
  완벽 예측(f == o) → corr≈1, crmsd≈0, std_ratio≈1, bias≈0
  + 에러 경로(형상 불일치, 결측, 상수 배열) no-crash 확인.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

# conftest.py 가 scripts/ 를 sys.path 에 추가한다.
from metrics_pattern import taylor_stats, target_stats, pattern_correlation


# ---------------------------------------------------------------------------
# 도우미
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(0)


def _rand(shape=(50,)) -> np.ndarray:
    return RNG.standard_normal(shape).astype("float64")


# ---------------------------------------------------------------------------
# 완벽 예측: f == o
# ---------------------------------------------------------------------------

class TestPerfectForecast:
    """f == o 일 때 모든 지표가 이상적 값을 반환해야 한다."""

    def test_taylor_corr_perfect(self):
        o = _rand()
        stats = taylor_stats(o, o.copy())
        assert math.isclose(stats["corr"], 1.0, abs_tol=1e-9), stats

    def test_taylor_crmsd_zero(self):
        o = _rand()
        stats = taylor_stats(o, o.copy())
        assert math.isclose(stats["crmsd"], 0.0, abs_tol=1e-9), stats

    def test_taylor_std_ratio_one(self):
        o = _rand()
        stats = taylor_stats(o, o.copy())
        assert math.isclose(stats["std_ratio"], 1.0, abs_tol=1e-9), stats

    def test_target_bias_zero(self):
        o = _rand()
        stats = target_stats(o, o.copy())
        assert math.isclose(stats["bias"], 0.0, abs_tol=1e-9), stats

    def test_target_urmsd_zero(self):
        o = _rand()
        stats = target_stats(o, o.copy())
        assert math.isclose(stats["urmsd"], 0.0, abs_tol=1e-9), stats

    def test_target_rmsd_zero(self):
        o = _rand()
        stats = target_stats(o, o.copy())
        assert math.isclose(stats["rmsd"], 0.0, abs_tol=1e-9), stats

    def test_pattern_corr_perfect(self):
        o = _rand((10, 8))
        r = pattern_correlation(o, o.copy())
        assert math.isclose(r, 1.0, abs_tol=1e-9), r


# ---------------------------------------------------------------------------
# 알려진 값 검증 (analytic cases)
# ---------------------------------------------------------------------------

class TestKnownValues:
    """해석적으로 계산 가능한 케이스."""

    def test_taylor_constant_offset_no_crmsd(self):
        """f = o + c (상수 이동)이면 crmsd==0, corr==1, std_ratio==1."""
        o = _rand()
        f = o + 5.0
        stats = taylor_stats(o, f)
        assert math.isclose(stats["corr"], 1.0, abs_tol=1e-9)
        assert math.isclose(stats["crmsd"], 0.0, abs_tol=1e-9)
        assert math.isclose(stats["std_ratio"], 1.0, abs_tol=1e-9)

    def test_target_constant_offset_bias_only(self):
        """f = o + c 이면 bias==c, urmsd==0."""
        o = _rand()
        c = 3.7
        f = o + c
        stats = target_stats(o, f)
        assert math.isclose(stats["bias"], c, abs_tol=1e-9)
        assert math.isclose(stats["urmsd"], 0.0, abs_tol=1e-9)

    def test_taylor_scale_change(self):
        """f = 2*o 이면 std_ratio==2, corr==1."""
        o = _rand()
        # o 의 평균을 0으로 만들어야 corr=1이 정확히 나온다
        o = o - np.mean(o)
        f = 2.0 * o
        stats = taylor_stats(o, f)
        assert math.isclose(stats["std_ratio"], 2.0, abs_tol=1e-9)
        assert math.isclose(stats["corr"], 1.0, abs_tol=1e-9)

    def test_taylor_anticorrelated(self):
        """f = -o (평균 0인 경우) 이면 corr==-1."""
        o = _rand() - _rand().mean()
        f = -o
        stats = taylor_stats(o, f)
        assert math.isclose(stats["corr"], -1.0, abs_tol=1e-9)

    def test_rmsd_decomposition(self):
        """rmsd² = bias² + urmsd² (피타고라스 분해)."""
        o = _rand()
        f = _rand()
        stats = target_stats(o, f)
        lhs = stats["rmsd"] ** 2
        rhs = stats["bias"] ** 2 + stats["urmsd"] ** 2
        assert math.isclose(lhs, rhs, rel_tol=1e-9), (lhs, rhs)

    def test_crmsd_equals_urmsd(self):
        """taylor crmsd == target urmsd (정의가 동일)."""
        o = _rand()
        f = _rand()
        t = taylor_stats(o, f)
        tgt = target_stats(o, f)
        assert math.isclose(t["crmsd"], tgt["urmsd"], rel_tol=1e-9)

    def test_pattern_corr_2d(self):
        """2-D 공간장에 대해 pattern_correlation 이 올바른 값을 반환한다."""
        o = _rand((12, 15))
        f = _rand((12, 15))
        r = pattern_correlation(o, f)
        # numpy corrcoef 직접 계산과 비교
        expected = float(np.corrcoef(o.ravel(), f.ravel())[0, 1])
        assert math.isclose(r, expected, abs_tol=1e-12)


# ---------------------------------------------------------------------------
# No-crash 에러 경로
# ---------------------------------------------------------------------------

class TestErrorPaths:
    """잘못된 입력에서 크래시 없이 NaN/예외를 반환해야 한다."""

    def test_shape_mismatch_raises(self):
        """형상이 다르면 ValueError (크래시 아님)."""
        with pytest.raises(ValueError, match="형상 불일치"):
            taylor_stats(np.zeros(5), np.zeros(6))

    def test_nan_input_handled(self):
        """일부 NaN이 있어도 유효 쌍으로만 계산한다."""
        o = np.array([1.0, 2.0, 3.0, float("nan")])
        f = np.array([1.0, 2.0, 3.0, 99.0])
        stats = taylor_stats(o, f)
        # nan 쌍 제거 후 f==o 이므로 perfect
        assert math.isclose(stats["corr"], 1.0, abs_tol=1e-9)
        assert stats["n"] == 3

    def test_all_nan_returns_nan(self):
        o = np.full(5, float("nan"))
        f = np.full(5, float("nan"))
        stats = taylor_stats(o, f)
        assert math.isnan(stats["corr"])
        assert math.isnan(stats["crmsd"])

    def test_constant_o_returns_nan_ratio(self):
        """σ_o == 0 이면 std_ratio, corr, crmsd 모두 NaN (정의 불가)."""
        o = np.ones(10)
        f = np.ones(10) * 2.0
        stats = taylor_stats(o, f)
        assert math.isnan(stats["std_ratio"])

    def test_constant_f_corr_nan_or_zero(self):
        """σ_f == 0 이면 corr == 0 (분모 0)."""
        o = _rand()
        f = np.ones_like(o)
        stats = taylor_stats(o, f)
        assert stats["corr"] == 0.0

    def test_single_point_nan(self):
        """n < 2 이면 NaN 반환."""
        stats = taylor_stats(np.array([1.0]), np.array([1.0]))
        assert math.isnan(stats["corr"])

    def test_empty_after_nan_filter(self):
        """유효 쌍이 없어도 크래시 없이 NaN."""
        o = np.array([float("nan"), float("nan")])
        f = np.array([1.0, 2.0])
        stats = target_stats(o, f)
        assert math.isnan(stats["bias"])

    def test_pattern_corr_constant_returns_nan(self):
        """공간장이 상수이면 NaN 반환 (분산 0)."""
        o = np.ones((4, 4))
        f = np.ones((4, 4)) * 2.0
        r = pattern_correlation(o, f)
        assert math.isnan(r)

    def test_n_count_in_result(self):
        """n 필드는 유효 쌍의 수를 정확히 반환한다."""
        o = np.array([1.0, 2.0, float("nan"), 4.0])
        f = np.array([1.0, float("nan"), 3.0, 4.0])
        stats = taylor_stats(o, f)
        # 양쪽 유한: idx 0, 3 → n==2
        assert stats["n"] == 2
