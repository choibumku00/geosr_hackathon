"""tests/test_preprocess.py — preprocess.py 집중 테스트.

대상 함수:
  to_kelvin(values, units)
  match_points_to_mesh(mesh_lon, mesh_lat, pt_lon, pt_lat, max_km)
  build_pairs(stations, times, model_vals, obs_vals)

실행:
  cd skills/validate-model-output
  python -m pytest tests/test_preprocess.py -q
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

# scripts/ 를 sys.path 에 명시적으로 추가 (conftest 보완)
HERE    = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from preprocess import build_pairs, match_points_to_mesh, to_kelvin


# ===========================================================================
# 1. to_kelvin — 단위 변환
# ===========================================================================

class TestToKelvin:
    """온도 단위 변환 검증."""

    # ── 섭씨 변형 ──────────────────────────────────────────────────────────

    def test_degC_single(self):
        """`to_kelvin([10], 'degC')` 의 첫 번째 원소 ≈ 283.15."""
        result = to_kelvin([10], "degC")
        assert abs(result[0] - 283.15) < 1e-6

    def test_degC_array(self):
        """배열 입력 — 모든 원소에 +273.15 적용."""
        result = to_kelvin([0.0, 100.0, -273.15], "degC")
        np.testing.assert_allclose(result, [273.15, 373.15, 0.0], atol=1e-6)

    def test_celsius_alias(self):
        """`celsius` 는 `degC` 와 동일하게 처리."""
        result = to_kelvin([0.0], "celsius")
        assert abs(result[0] - 273.15) < 1e-6

    def test_degree_c_symbol(self):
        """`°C` 기호(유니코드) 도 인식."""
        result = to_kelvin([100.0], "°C")
        assert abs(result[0] - 373.15) < 1e-6

    def test_capital_c(self):
        """`C` 단독 표기 처리."""
        result = to_kelvin([25.0], "C")
        assert abs(result[0] - 298.15) < 1e-6

    # ── 켈빈 passthrough ────────────────────────────────────────────────────

    def test_kelvin_passthrough(self):
        """`K` 입력은 그대로 반환."""
        result = to_kelvin([300.0], "K")
        assert abs(result[0] - 300.0) < 1e-9

    def test_kelvin_lowercase(self):
        """`kelvin` 소문자도 인식."""
        result = to_kelvin([273.15], "kelvin")
        assert abs(result[0] - 273.15) < 1e-9

    # ── 알 수 없는 단위 → 원본 + 경고 ──────────────────────────────────────

    def test_unknown_unit_warns(self):
        """알 수 없는 단위는 UserWarning 을 발생시킨다."""
        with pytest.warns(UserWarning, match="알 수 없는 단위"):
            result = to_kelvin([25.0], "F")
        assert abs(result[0] - 25.0) < 1e-9   # 원본 그대로

    def test_unknown_unit_no_crash(self):
        """알 수 없는 단위여도 예외 없이 반환(no-crash)."""
        with pytest.warns(UserWarning):
            result = to_kelvin([0.0, 1.0], "psi")
        assert len(result) == 2

    # ── 반환 타입 ────────────────────────────────────────────────────────────

    def test_returns_ndarray(self):
        """반환값은 항상 np.ndarray."""
        result = to_kelvin([20.0], "degC")
        assert isinstance(result, np.ndarray)


# ===========================================================================
# 2. match_points_to_mesh — 최근접 노드 매칭
# ===========================================================================

class TestMatchPointsToMesh:
    """cKDTree 기반 mesh 매칭 검증."""

    # ── 테스트용 한국 근해 3×3 격자 (9 노드) ─────────────────────────────

    @pytest.fixture()
    def grid_9(self):
        """lon=[126,127,128] × lat=[34,35,36] 균일 격자."""
        lons = np.array([126., 127., 128., 126., 127., 128., 126., 127., 128.])
        lats = np.array([ 34.,  34.,  34.,  35.,  35.,  35.,  36.,  36.,  36.])
        return lons, lats

    # ── 정확한 노드 일치 ───────────────────────────────────────────────────

    def test_exact_node_index(self, grid_9):
        """쿼리점이 노드 위치와 정확히 일치 → 올바른 인덱스 반환."""
        mesh_lon, mesh_lat = grid_9
        # node 4 = (127, 35)
        idx, dist = match_points_to_mesh(mesh_lon, mesh_lat, [127.0], [35.0])
        assert idx[0] == 4

    def test_exact_node_distance_near_zero(self, grid_9):
        """정확한 노드 → 거리 ≈ 0 km."""
        mesh_lon, mesh_lat = grid_9
        _, dist = match_points_to_mesh(mesh_lon, mesh_lat, [126.0], [34.0])
        assert dist[0] < 1.0   # km

    def test_nearest_among_candidates(self, grid_9):
        """(126.1, 34.1) 은 node 0 (126, 34) 에 가장 가깝다."""
        mesh_lon, mesh_lat = grid_9
        idx, _ = match_points_to_mesh(mesh_lon, mesh_lat, [126.1], [34.1])
        assert idx[0] == 0

    def test_second_node(self, grid_9):
        """(127.4, 34.1) 은 node 1 (127, 34) 에 가장 가깝다."""
        mesh_lon, mesh_lat = grid_9
        idx, _ = match_points_to_mesh(mesh_lon, mesh_lat, [127.4], [34.1])
        assert idx[0] == 1

    # ── 임계초과 제외 ─────────────────────────────────────────────────────

    def test_threshold_exceeded_returns_minus1(self, grid_9):
        """mesh 범위 밖 관측점 → 인덱스 -1."""
        mesh_lon, mesh_lat = grid_9
        # (140, 35) — 최근접 node 까지 수백 km
        idx, _ = match_points_to_mesh(
            mesh_lon, mesh_lat, [140.0], [35.0], max_km=50.0
        )
        assert idx[0] == -1

    def test_threshold_zero_all_excluded(self, grid_9):
        """max_km=0 → 정확히 일치하지 않으면 모두 -1."""
        mesh_lon, mesh_lat = grid_9
        idx, _ = match_points_to_mesh(
            mesh_lon, mesh_lat, [126.01], [34.01], max_km=0.0
        )
        assert idx[0] == -1

    def test_mixed_within_and_beyond(self, grid_9):
        """복수 쿼리 — 범위 내 vs 범위 외 혼재."""
        mesh_lon, mesh_lat = grid_9
        pt_lon = [127.0, 155.0]
        pt_lat = [ 35.0,  35.0]
        idx, dist = match_points_to_mesh(
            mesh_lon, mesh_lat, pt_lon, pt_lat, max_km=50.0
        )
        assert idx[0] != -1    # (127, 35) 는 범위 내
        assert idx[1] == -1    # (155, 35) 는 범위 외

    def test_large_max_km_no_exclusion(self, grid_9):
        """max_km=9999 → 모든 점이 포함(인덱스 ≥ 0)."""
        mesh_lon, mesh_lat = grid_9
        idx, _ = match_points_to_mesh(
            mesh_lon, mesh_lat, [140.0, 150.0], [30.0, 40.0], max_km=9999.0
        )
        assert all(i >= 0 for i in idx)

    # ── 반환 타입 ─────────────────────────────────────────────────────────

    def test_returns_ndarray(self, grid_9):
        """반환값은 (ndarray, ndarray) 튜플."""
        mesh_lon, mesh_lat = grid_9
        idx, dist = match_points_to_mesh(mesh_lon, mesh_lat, [127.0], [35.0])
        assert isinstance(idx, np.ndarray)
        assert isinstance(dist, np.ndarray)


# ===========================================================================
# 3. build_pairs — 롱포맷 DataFrame 생성
# ===========================================================================

class TestBuildPairs:
    """station/time/model/obs 롱포맷 검증."""

    def test_row_count(self):
        """행 수 = N_time × N_station."""
        stations = ["A", "B"]
        times    = ["T1", "T2", "T3"]
        model    = np.zeros((3, 2))
        obs      = np.ones((3, 2))
        df = build_pairs(stations, times, model, obs)
        assert len(df) == 6

    def test_columns(self):
        """필수 컬럼 4개 존재."""
        df = build_pairs(["X"], ["T1"], [[1.0]], [[2.0]])
        assert list(df.columns) == ["station", "time", "model", "obs"]

    def test_values_correctness(self):
        """모델=2.5, 관측=3.7 이면 컬럼 값 일치."""
        df = build_pairs(["Busan"], ["2024-01-01"], [[2.5]], [[3.7]])
        assert df["model"].iloc[0] == pytest.approx(2.5)
        assert df["obs"].iloc[0]   == pytest.approx(3.7)

    def test_station_column_values(self):
        """station 컬럼에 올바른 지점 이름."""
        stations = ["부산", "거제"]
        times    = ["T1"]
        df = build_pairs(stations, times, [[1.0, 2.0]], [[3.0, 4.0]])
        assert set(df["station"]) == {"부산", "거제"}

    def test_shape_mismatch_raises(self):
        """model/obs 형상 불일치 → ValueError."""
        with pytest.raises(ValueError, match="shape"):
            build_pairs(["A"], ["T1"], [[1.0, 2.0]], [[3.0]])
