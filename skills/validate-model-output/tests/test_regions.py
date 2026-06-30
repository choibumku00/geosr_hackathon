"""tests/test_regions.py — regions.py 집중 테스트.

대상:
  NAMED_REGIONS          -- 한국 주요 해역 bbox 딕셔너리
  region_bbox(name)      -- 이름 → bbox | None
  crop_grid_mask(lon, lat, bbox)     -- 격자 bool 마스크 (1D/2D)
  crop_mesh_mask(node_lon, node_lat, bbox) -- mesh 노드 bool 마스크

실행:
  cd skills/validate-model-output
  python -m pytest tests/test_regions.py -q
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

# scripts/ 경로 주입 (conftest 보완)
HERE    = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from regions import (
    NAMED_REGIONS,
    crop_grid_mask,
    crop_mesh_mask,
    region_bbox,
)


# ===========================================================================
# 1. NAMED_REGIONS — 딕셔너리 기본 구조
# ===========================================================================

class TestNamedRegions:
    """NAMED_REGIONS 딕셔너리 검증."""

    def test_not_empty(self):
        """비어 있지 않아야 한다."""
        assert len(NAMED_REGIONS) > 0

    def test_bbox_length(self):
        """모든 bbox 는 길이 4 여야 한다."""
        for name, bbox in NAMED_REGIONS.items():
            assert len(bbox) == 4, f"{name!r} bbox 길이가 4 가 아님"

    def test_bbox_order(self):
        """lon_min < lon_max, lat_min < lat_max 여야 한다."""
        for name, (lon_min, lon_max, lat_min, lat_max) in NAMED_REGIONS.items():
            assert lon_min < lon_max, f"{name!r} lon_min >= lon_max"
            assert lat_min < lat_max, f"{name!r} lat_min >= lat_max"

    def test_has_east_sea_korean(self):
        """'동해' 키가 존재해야 한다."""
        assert "동해" in NAMED_REGIONS

    def test_has_east_sea_english(self):
        """'EastSea' 영문 키도 존재해야 한다."""
        assert "EastSea" in NAMED_REGIONS

    def test_east_sea_values_match(self):
        """'동해' 와 'EastSea' 의 bbox 값이 동일해야 한다."""
        assert NAMED_REGIONS["동해"] == NAMED_REGIONS["EastSea"]

    def test_has_yellow_sea(self):
        """서해(황해) 키 존재."""
        assert "서해" in NAMED_REGIONS or "YellowSea" in NAMED_REGIONS

    def test_has_south_sea(self):
        """남해 키 존재."""
        assert "남해" in NAMED_REGIONS or "SouthSea" in NAMED_REGIONS


# ===========================================================================
# 2. region_bbox — 이름 조회
# ===========================================================================

class TestRegionBbox:
    """region_bbox 함수 검증."""

    # ── 동해 / EastSea ────────────────────────────────────────────────────

    def test_east_sea_korean(self):
        """`region_bbox('동해')` 는 길이-4 list 를 반환해야 한다."""
        bbox = region_bbox("동해")
        assert bbox is not None, "region_bbox('동해') 가 None 을 반환했다"
        assert len(bbox) == 4

    def test_east_sea_english(self):
        """`region_bbox('EastSea')` 도 동일 bbox."""
        bbox = region_bbox("EastSea")
        assert bbox is not None
        assert len(bbox) == 4

    def test_east_sea_both_same(self):
        """한글·영문 bbox 값이 동일."""
        assert region_bbox("동해") == region_bbox("EastSea")

    def test_east_sea_longitude_range(self):
        """동해 bbox 의 경도 범위: 대략 129 ≤ lon_min < lon_max ≤ 133."""
        lon_min, lon_max, _, _ = region_bbox("동해")
        assert 125.0 <= lon_min < lon_max <= 135.0

    def test_east_sea_latitude_range(self):
        """동해 bbox 의 위도 범위: 대략 34 ≤ lat_min < lat_max ≤ 43."""
        _, _, lat_min, lat_max = region_bbox("동해")
        assert 30.0 <= lat_min < lat_max <= 45.0

    # ── 기타 해역 ─────────────────────────────────────────────────────────

    def test_south_sea(self):
        """'남해' 또는 'SouthSea' 중 하나 이상 인식."""
        assert region_bbox("남해") is not None or region_bbox("SouthSea") is not None

    def test_yellow_sea(self):
        """'서해' 또는 'YellowSea' 인식."""
        assert region_bbox("서해") is not None or region_bbox("YellowSea") is not None

    def test_unknown_name_returns_none(self):
        """알 수 없는 이름 → None."""
        assert region_bbox("없는해역_XYZ") is None

    def test_empty_string_returns_none(self):
        """빈 문자열 → None."""
        assert region_bbox("") is None

    def test_returns_new_list(self):
        """매 호출마다 독립적인 list 반환 (원본 오염 방지)."""
        b1 = region_bbox("동해")
        b2 = region_bbox("동해")
        b1[0] = -999.0
        assert region_bbox("동해")[0] != -999.0, "원본 NAMED_REGIONS 가 오염됐다"

    def test_case_insensitive_english(self):
        """영문 소문자 fallback — 'eastsea' 도 인식."""
        bbox = region_bbox("eastsea")
        assert bbox is not None


# ===========================================================================
# 3. crop_grid_mask — 격자 bool 마스크
# ===========================================================================

class TestCropGridMask:
    """crop_grid_mask 검증 (1D·2D 좌표)."""

    # ── 공통 bbox ─────────────────────────────────────────────────────────
    BBOX = [129.0, 132.0, 35.0, 42.0]   # 동해

    # ── 1-D 동일 길이 (비정형 점 집합) ────────────────────────────────────

    def test_1d_inside_point(self):
        """bbox 안 점 → True."""
        lon = np.array([130.0])
        lat = np.array([38.0])
        mask = crop_grid_mask(lon, lat, self.BBOX)
        assert bool(mask[0]) is True

    def test_1d_outside_point(self):
        """bbox 밖 점 → False."""
        lon = np.array([120.0])
        lat = np.array([38.0])
        mask = crop_grid_mask(lon, lat, self.BBOX)
        assert bool(mask[0]) is False

    def test_1d_boundary_included(self):
        """경계값(lon_min, lat_min) → True (포함 기준)."""
        lon = np.array([129.0])
        lat = np.array([35.0])
        mask = crop_grid_mask(lon, lat, self.BBOX)
        assert bool(mask[0]) is True

    def test_1d_mixed_points(self):
        """안/밖 혼재 — 개수 검증."""
        lons = np.array([130.0, 120.0, 131.0, 200.0])
        lats = np.array([ 38.0,  38.0,  40.0,  40.0])
        mask = crop_grid_mask(lons, lats, self.BBOX)
        assert mask.sum() == 2   # 130/38, 131/40 만 inside

    def test_1d_returns_bool_array(self):
        """반환값이 bool np.ndarray."""
        mask = crop_grid_mask(np.array([130.0]), np.array([38.0]), self.BBOX)
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == bool

    # ── 2-D meshgrid ──────────────────────────────────────────────────────

    def test_2d_meshgrid(self):
        """2-D meshgrid 입력 — bbox 안 원소가 True."""
        lon_vec = np.linspace(128.0, 133.0, 6)   # 128,129,...,133
        lat_vec = np.linspace(34.0,  43.0, 10)
        lon2d, lat2d = np.meshgrid(lon_vec, lat_vec)
        mask = crop_grid_mask(lon2d, lat2d, self.BBOX)
        # 경도 129~132, 위도 35~42 안에 있는 점만 True
        expected = (
            (lon2d >= 129.0) & (lon2d <= 132.0) &
            (lat2d >=  35.0) & (lat2d <=  42.0)
        )
        np.testing.assert_array_equal(mask, expected)

    def test_2d_returns_2d_mask(self):
        """2-D 입력 → 2-D 출력."""
        lon2d = np.array([[129.0, 131.0], [130.0, 133.0]])
        lat2d = np.array([[ 36.0,  37.0], [ 41.0,  43.0]])
        mask = crop_grid_mask(lon2d, lat2d, self.BBOX)
        assert mask.ndim == 2

    # ── 1-D 다른 길이 → meshgrid ──────────────────────────────────────────

    def test_1d_different_lengths_meshgrid(self):
        """len(lon) ≠ len(lat) → 내부에서 meshgrid 생성."""
        lon = np.array([129.0, 130.0, 132.0])   # 3 values
        lat = np.array([35.0, 40.0])             # 2 values
        mask = crop_grid_mask(lon, lat, self.BBOX)
        assert mask.shape == (2, 3)

    # ── 완전 밖 ───────────────────────────────────────────────────────────

    def test_all_outside(self):
        """모두 bbox 밖 → 전부 False."""
        lons = np.array([100.0, 105.0])
        lats = np.array([ 10.0,  15.0])
        mask = crop_grid_mask(lons, lats, self.BBOX)
        assert not mask.any()

    def test_all_inside(self):
        """모두 bbox 안 → 전부 True."""
        lons = np.array([130.0, 131.0])
        lats = np.array([ 37.0,  39.0])
        mask = crop_grid_mask(lons, lats, self.BBOX)
        assert mask.all()


# ===========================================================================
# 4. crop_mesh_mask — 비정형 mesh 노드 bool 마스크
# ===========================================================================

class TestCropMeshMask:
    """crop_mesh_mask 검증."""

    BBOX = [129.0, 132.0, 35.0, 42.0]   # 동해

    @pytest.fixture()
    def sample_nodes(self):
        """동해 안 3개, 밖 2개(총 5개) 테스트 노드."""
        node_lon = np.array([130.0, 131.0, 129.0,   120.0, 140.0])
        node_lat = np.array([ 38.0,  40.0,  35.0,    38.0,  38.0])
        # 인덱스 0,1,2 → inside / 3,4 → outside
        return node_lon, node_lat

    # ── 기본 동작 ─────────────────────────────────────────────────────────

    def test_inside_nodes_true(self, sample_nodes):
        """bbox 안 노드 → True."""
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, self.BBOX)
        assert bool(mask[0]) is True
        assert bool(mask[1]) is True
        assert bool(mask[2]) is True

    def test_outside_nodes_false(self, sample_nodes):
        """bbox 밖 노드 → False."""
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, self.BBOX)
        assert bool(mask[3]) is False
        assert bool(mask[4]) is False

    def test_count_inside(self, sample_nodes):
        """True 개수 = 3 (inside 노드)."""
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, self.BBOX)
        assert mask.sum() == 3

    # ── 경계 포함 ─────────────────────────────────────────────────────────

    def test_boundary_lon_min(self):
        """lon_min 경계 노드 → True."""
        mask = crop_mesh_mask(np.array([129.0]), np.array([38.0]), self.BBOX)
        assert bool(mask[0]) is True

    def test_boundary_lat_min(self):
        """lat_min 경계 노드 → True."""
        mask = crop_mesh_mask(np.array([130.0]), np.array([35.0]), self.BBOX)
        assert bool(mask[0]) is True

    def test_boundary_lon_max(self):
        """lon_max 경계 노드 → True."""
        mask = crop_mesh_mask(np.array([132.0]), np.array([38.0]), self.BBOX)
        assert bool(mask[0]) is True

    def test_boundary_lat_max(self):
        """lat_max 경계 노드 → True."""
        mask = crop_mesh_mask(np.array([130.0]), np.array([42.0]), self.BBOX)
        assert bool(mask[0]) is True

    # ── 반환 타입·형상 ────────────────────────────────────────────────────

    def test_returns_bool_ndarray(self, sample_nodes):
        """반환값은 bool np.ndarray."""
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, self.BBOX)
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == bool

    def test_shape_matches_nodes(self, sample_nodes):
        """마스크 형상 = 노드 수."""
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, self.BBOX)
        assert mask.shape == node_lon.shape

    # ── 극단 케이스 ───────────────────────────────────────────────────────

    def test_all_outside(self):
        """모두 bbox 밖 → 전부 False."""
        lons = np.array([100.0, 105.0, 110.0])
        lats = np.array([ 10.0,  15.0,  20.0])
        mask = crop_mesh_mask(lons, lats, self.BBOX)
        assert not mask.any()

    def test_all_inside(self):
        """모두 bbox 안 → 전부 True."""
        lons = np.array([130.0, 131.0, 129.5])
        lats = np.array([ 37.0,  39.0,  41.0])
        mask = crop_mesh_mask(lons, lats, self.BBOX)
        assert mask.all()

    def test_single_node_inside(self):
        """단일 노드, bbox 안 → [True]."""
        mask = crop_mesh_mask(np.array([130.0]), np.array([38.0]), self.BBOX)
        assert mask.shape == (1,)
        assert bool(mask[0]) is True

    def test_single_node_outside(self):
        """단일 노드, bbox 밖 → [False]."""
        mask = crop_mesh_mask(np.array([100.0]), np.array([10.0]), self.BBOX)
        assert bool(mask[0]) is False

    def test_shape_mismatch_raises(self):
        """node_lon / node_lat 길이 불일치 → ValueError."""
        with pytest.raises(ValueError):
            crop_mesh_mask(np.array([130.0, 131.0]), np.array([38.0]), self.BBOX)

    # ── NAMED_REGIONS 연동 ────────────────────────────────────────────────

    def test_with_region_bbox_east_sea(self, sample_nodes):
        """region_bbox('동해') 로 얻은 bbox 로 crop_mesh_mask 를 호출한다."""
        from regions import region_bbox
        bbox = region_bbox("동해")
        assert bbox is not None, "region_bbox('동해') 가 None 이다"
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, bbox)
        # 동해 bbox 안 노드(인덱스 0,1,2)가 True 여야 한다
        assert mask[0] and mask[1] and mask[2]
        # 밖 노드(인덱스 3,4)는 False 여야 한다
        assert not mask[3] and not mask[4]

    def test_with_region_bbox_eastsea_english(self, sample_nodes):
        """영문 'EastSea' bbox 로도 동일한 결과."""
        from regions import region_bbox
        bbox = region_bbox("EastSea")
        assert bbox is not None
        node_lon, node_lat = sample_nodes
        mask = crop_mesh_mask(node_lon, node_lat, bbox)
        assert mask.sum() == 3
