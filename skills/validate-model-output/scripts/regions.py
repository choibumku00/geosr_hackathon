"""해역 crop 헬퍼 — SAMPLE.

SAMPLE — 해역경계는 데이터·목적따라 조정.
여기 정의된 bbox 는 대표적인 한국 주요 해역의 근사 경계이며,
분석 목적·데이터 해상도에 따라 사용자가 직접 수정하라.

제공 객체:
  NAMED_REGIONS : dict[str, list[float]]
      이름 → [lon_min, lon_max, lat_min, lat_max]
      한글·영문 두 가지 키를 모두 지원한다.

제공 함수:
  region_bbox(name)                     -> list[float] | None
  crop_grid_mask(lon, lat, bbox)        -> np.ndarray[bool]  (1D·2D 모두 지원)
  crop_mesh_mask(node_lon, node_lat, bbox) -> np.ndarray[bool]
"""
from __future__ import annotations

from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# 1. 한국 주요 해역 bbox 정의  [lon_min, lon_max, lat_min, lat_max]
# ---------------------------------------------------------------------------
# SAMPLE — 아래 값은 근사 경계다. 실데이터·분석 목적에 맞게 조정하라.

NAMED_REGIONS: dict[str, list[float]] = {
    # ── 동해 / East Sea ────────────────────────────────────────────────────
    "동해":     [129.0, 132.0, 35.0, 42.0],
    "EastSea":  [129.0, 132.0, 35.0, 42.0],

    # ── 남해 / South Sea ──────────────────────────────────────────────────
    "남해":     [125.0, 130.0, 33.0, 35.0],
    "SouthSea": [125.0, 130.0, 33.0, 35.0],

    # ── 서해 (황해) / Yellow Sea ──────────────────────────────────────────
    "서해":      [124.0, 126.0, 34.0, 38.0],
    "황해":      [124.0, 126.0, 34.0, 38.0],
    "YellowSea": [124.0, 126.0, 34.0, 38.0],

    # ── 북서태평양 / NW Pacific ───────────────────────────────────────────
    "북서태평양": [120.0, 180.0, 0.0, 60.0],
    "NWPacific":  [120.0, 180.0, 0.0, 60.0],

    # ── 한반도 주변 전역 (South Korea Near-shore) ──────────────────────────
    "한국근해":   [122.0, 132.0, 32.0, 42.0],
    "KoreaNearshore": [122.0, 132.0, 32.0, 42.0],

    # ── 대한해협 / Korea Strait ───────────────────────────────────────────
    "대한해협":    [128.0, 132.0, 33.0, 35.5],
    "KoreaStrait": [128.0, 132.0, 33.0, 35.5],
}


# ---------------------------------------------------------------------------
# 2. region_bbox
# ---------------------------------------------------------------------------

def region_bbox(name: str) -> Optional[list[float]]:
    """해역 이름으로 bbox 를 반환한다.

    Parameters
    ----------
    name : str
        `NAMED_REGIONS` 의 키 (한글 또는 영문, 대소문자 정확히).
        정확히 일치하지 않으면 소문자 비교를 추가로 시도한다.

    Returns
    -------
    list[float] | None
        [lon_min, lon_max, lat_min, lat_max] 또는 None (인식 불가)

    Examples
    --------
    >>> region_bbox('동해')
    [129.0, 132.0, 35.0, 42.0]
    >>> region_bbox('EastSea')
    [129.0, 132.0, 35.0, 42.0]
    >>> region_bbox('없는해역') is None
    True
    """
    # 정확 일치 우선
    if name in NAMED_REGIONS:
        return list(NAMED_REGIONS[name])

    # 소문자 fallback (영문 입력의 대소문자 변형 허용)
    name_lower = name.lower()
    for key, bbox in NAMED_REGIONS.items():
        if key.lower() == name_lower:
            return list(bbox)

    return None


# ---------------------------------------------------------------------------
# 3. crop_grid_mask  (1-D 또는 2-D 좌표 배열)
# ---------------------------------------------------------------------------

def crop_grid_mask(
    lon,
    lat,
    bbox: list[float],
) -> np.ndarray:
    """bbox 안에 속하는 격자점의 bool 마스크를 반환한다.

    Parameters
    ----------
    lon  : array-like, shape (N,) or (M, N)
        경도 배열.  1-D (벡터) 또는 2-D (meshgrid 형태) 모두 지원.
    lat  : array-like, shape (M,) or (M, N)
        위도 배열.  lon 과 형상이 다른 경우(각각 1-D) meshgrid 를 내부 생성.
    bbox : list[float]
        [lon_min, lon_max, lat_min, lat_max]

    Returns
    -------
    np.ndarray[bool]
        True = bbox 안 포함. 형상은 2-D broadcast 결과와 같음.
        lon, lat 이 모두 1-D 이고 형상이 같으면 1-D bool 배열 반환.

    Notes
    -----
    * 경계 포함(≥, ≤) 처리.
    * SAMPLE — 날짜변경선(antimeridian) 걸쳐 있는 bbox 는 지원하지 않는다.
    """
    lon_arr = np.asarray(lon, dtype=float)
    lat_arr = np.asarray(lat, dtype=float)
    lon_min, lon_max, lat_min, lat_max = bbox

    if lon_arr.ndim == 1 and lat_arr.ndim == 1 and lon_arr.shape == lat_arr.shape:
        # 둘 다 1-D 이고 같은 길이 → 점-by-점 비교 (mesh/비정형 포함)
        mask = (
            (lon_arr >= lon_min) & (lon_arr <= lon_max) &
            (lat_arr >= lat_min) & (lat_arr <= lat_max)
        )
        return mask

    if lon_arr.ndim == 1 and lat_arr.ndim == 1:
        # 길이가 다른 1-D → meshgrid 생성 (정형격자용)
        lon2d, lat2d = np.meshgrid(lon_arr, lat_arr)
    elif lon_arr.ndim == 2 and lat_arr.ndim == 2:
        lon2d, lat2d = lon_arr, lat_arr
    else:
        raise ValueError(
            f"lon/lat 형상 불일치 또는 지원하지 않는 차원: "
            f"lon.shape={lon_arr.shape}, lat.shape={lat_arr.shape}"
        )

    mask = (
        (lon2d >= lon_min) & (lon2d <= lon_max) &
        (lat2d >= lat_min) & (lat2d <= lat_max)
    )
    return mask


# ---------------------------------------------------------------------------
# 4. crop_mesh_mask  (비정형 mesh 노드 — 1-D node 배열)
# ---------------------------------------------------------------------------

def crop_mesh_mask(
    node_lon,
    node_lat,
    bbox: list[float],
) -> np.ndarray:
    """비정형 mesh 노드 중 bbox 안에 속하는 노드의 bool 마스크를 반환한다.

    Parameters
    ----------
    node_lon : array-like, shape (N_node,)
        mesh 노드 경도.
    node_lat : array-like, shape (N_node,)
        mesh 노드 위도.
    bbox : list[float]
        [lon_min, lon_max, lat_min, lat_max]

    Returns
    -------
    np.ndarray[bool], shape (N_node,)
        True = bbox 안에 포함되는 노드.

    Notes
    -----
    경계 포함(≥, ≤) 처리.
    """
    nlon = np.asarray(node_lon, dtype=float).ravel()
    nlat = np.asarray(node_lat, dtype=float).ravel()

    if nlon.shape != nlat.shape:
        raise ValueError(
            f"node_lon.shape {nlon.shape} ≠ node_lat.shape {nlat.shape}"
        )

    lon_min, lon_max, lat_min, lat_max = bbox

    mask = (
        (nlon >= lon_min) & (nlon <= lon_max) &
        (nlat >= lat_min) & (nlat <= lat_max)
    )
    return mask
