"""tests/test_metrics_distribution.py — metrics_distribution SAMPLE 단위 테스트.

동일 분포: perkins_skill_score ≈ 1, ks_distance ≈ 0
이동 분포: perkins_skill_score < 1
"""
from __future__ import annotations

import numpy as np
import pytest

import metrics_distribution as md


RNG = np.random.default_rng(0)
N = 2000


# ---------------------------------------------------------------------------
# quantiles
# ---------------------------------------------------------------------------

class TestQuantiles:
    def test_basic(self):
        x = np.arange(101, dtype=float)
        q = md.quantiles(x, [0.0, 0.5, 1.0])
        assert q[0] == pytest.approx(0.0)
        assert q[1] == pytest.approx(50.0)
        assert q[2] == pytest.approx(100.0)

    def test_all_nan_returns_nan(self):
        x = np.array([float("nan")] * 10)
        q = md.quantiles(x, [0.5])
        assert np.isnan(q[0])

    def test_2d_input_flattened(self):
        x = np.ones((3, 4)) * 7.0
        q = md.quantiles(x, [0.5])
        assert q[0] == pytest.approx(7.0)


# ---------------------------------------------------------------------------
# qq_points
# ---------------------------------------------------------------------------

class TestQQPoints:
    def test_shapes(self):
        obs = RNG.normal(0, 1, 100)
        fct = RNG.normal(0, 1, 80)
        oq, fq = md.qq_points(obs, fct, n_quantiles=20)
        assert oq.shape == (20,)
        assert fq.shape == (20,)

    def test_same_dist_qq_diagonal(self):
        """동일 분포 Q-Q 점은 대각선에 가까워야 한다."""
        data = RNG.normal(5.0, 1.0, N)
        oq, fq = md.qq_points(data, data.copy(), n_quantiles=50)
        np.testing.assert_allclose(oq, fq, rtol=1e-6)


# ---------------------------------------------------------------------------
# perkins_skill_score
# ---------------------------------------------------------------------------

class TestPerkinsSkillScore:
    def test_identical_arrays_score_one(self):
        """완전히 동일한 배열 → PSS ≈ 1."""
        data = RNG.normal(3.0, 1.0, N)
        pss = md.perkins_skill_score(data, data.copy(), bins=30)
        assert pss == pytest.approx(1.0, abs=1e-9)

    def test_same_distribution_score_near_one(self):
        """동일 모수에서 독립 추출 → PSS 가 충분히 1에 가까워야 한다."""
        obs = RNG.normal(0.0, 1.0, N)
        fct = RNG.normal(0.0, 1.0, N)
        pss = md.perkins_skill_score(obs, fct, bins=30)
        assert pss >= 0.90, f"같은 분포인데 PSS={pss:.4f} < 0.90"

    def test_shifted_distribution_score_less_than_one(self):
        """평균이 크게 다른 분포 → PSS < 1."""
        obs = RNG.normal(0.0, 1.0, N)
        fct = RNG.normal(10.0, 1.0, N)   # 10σ 이동
        pss = md.perkins_skill_score(obs, fct, bins=30)
        assert pss < 0.5, f"이동 분포인데 PSS={pss:.4f} 가 너무 높음"

    def test_returns_float(self):
        obs = RNG.uniform(0, 1, 50)
        fct = RNG.uniform(0, 1, 50)
        pss = md.perkins_skill_score(obs, fct)
        assert isinstance(pss, float)

    def test_range_0_to_1(self):
        obs = RNG.exponential(2.0, N)
        fct = RNG.normal(5.0, 2.0, N)
        pss = md.perkins_skill_score(obs, fct, bins=20)
        assert 0.0 <= pss <= 1.0

    def test_custom_bin_edges(self):
        obs = RNG.normal(0.0, 1.0, N)
        fct = RNG.normal(0.0, 1.0, N)
        edges = np.linspace(-4, 4, 21)
        pss = md.perkins_skill_score(obs, fct, bins=edges)
        assert pss >= 0.85

    def test_all_nan_returns_nan(self):
        nan_arr = np.full(10, float("nan"))
        result = md.perkins_skill_score(nan_arr, np.ones(10))
        assert np.isnan(result)

    def test_constant_array_score_one(self):
        """모든 값이 동일할 때 lo==hi → 1.0 반환."""
        data = np.ones(20) * 5.0
        pss = md.perkins_skill_score(data, data.copy())
        assert pss == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# ks_distance
# ---------------------------------------------------------------------------

class TestKSDistance:
    def test_identical_arrays_zero(self):
        """완전히 동일한 배열 → KS-D ≈ 0."""
        data = RNG.normal(0.0, 1.0, N)
        d = md.ks_distance(data, data.copy())
        assert d == pytest.approx(0.0, abs=1e-9)

    def test_same_distribution_near_zero(self):
        """동일 모수 독립 추출 → KS-D 가 충분히 0에 가까워야 한다."""
        obs = RNG.normal(0.0, 1.0, N)
        fct = RNG.normal(0.0, 1.0, N)
        d = md.ks_distance(obs, fct)
        assert d <= 0.10, f"같은 분포인데 KS-D={d:.4f} > 0.10"

    def test_shifted_distribution_large_d(self):
        """크게 이동한 분포 → KS-D 가 커야 한다."""
        obs = RNG.normal(0.0, 1.0, N)
        fct = RNG.normal(10.0, 1.0, N)
        d = md.ks_distance(obs, fct)
        assert d > 0.8, f"이동 분포인데 KS-D={d:.4f} 가 너무 낮음"

    def test_range_0_to_1(self):
        obs = RNG.uniform(0, 5, N)
        fct = RNG.uniform(3, 8, N)
        d = md.ks_distance(obs, fct)
        assert 0.0 <= d <= 1.0

    def test_returns_float(self):
        d = md.ks_distance(RNG.normal(0, 1, 50), RNG.normal(1, 1, 50))
        assert isinstance(d, float)

    def test_all_nan_returns_nan(self):
        nan_arr = np.full(10, float("nan"))
        result = md.ks_distance(nan_arr, np.ones(10))
        assert np.isnan(result)
