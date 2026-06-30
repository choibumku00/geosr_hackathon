# SAMPLE — 실데이터 실시간 점검·도메인 맞춤 코드로 적응.
# 이 모듈은 u·v 바람 성분에서 파생변수를 계산하는 SAMPLE 함수 집합이다.
# 패키지가 아닌 플랫 모듈 — conftest.py 가 scripts/ 를 sys.path 에 등록하므로
# tests 에서 `import derive` 로 직접 사용 가능.
"""바람 성분 파생변수 모듈 (numpy, NaN 안전).

SAMPLE — 실데이터에선 u·v 의 좌표계(격자 상대 vs 지구 절대)·부호 규약·
단위(m/s vs knots 등)를 실시간 점검하고 도메인 맞춤 코드로 적응하라.

Public API (WIRE 인터페이스 계약)
----------------------------------
windspeed(u, v)       -> np.ndarray   풍속 [u·v 와 같은 단위]
wind_direction(u, v)  -> np.ndarray   기상학적 풍향 [°, 0–360)
                         풍향 규약: 바람이 불어오는 방향(FROM direction).
                         0°=북 기준 시계방향.
                         atan2(-u, -v) 기반 구현.
                         u=0, v<0  → 0° (북풍, 바람이 북쪽에서 옴)
                         u>0, v=0  → 270° (서풍, 바람이 서쪽에서 옴)
                         NaN 입력은 NaN 으로 전파.
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# 1. 풍속 (Wind Speed)
# ---------------------------------------------------------------------------

def windspeed(u, v) -> np.ndarray:
    """풍속 = sqrt(u² + v²).

    Parameters
    ----------
    u : array-like
        동서 바람 성분 (양수 = 동쪽으로 부는 방향).
    v : array-like
        남북 바람 성분 (양수 = 북쪽으로 부는 방향).

    Returns
    -------
    np.ndarray (float64)
        풍속. NaN 입력 시 NaN 전파.

    SAMPLE — 단위가 m/s 가 아니면 호출 전 변환하라.
    """
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return np.sqrt(u ** 2 + v ** 2)


# ---------------------------------------------------------------------------
# 2. 기상학적 풍향 (Meteorological Wind Direction)
# ---------------------------------------------------------------------------

def wind_direction(u, v) -> np.ndarray:
    """기상학적 풍향 = 바람이 불어오는 방향(FROM direction) [°, 0–360).

    구현: degrees(atan2(-u, -v)) % 360

    규약 요약
    ---------
    u=0,  v<0  → 0°   (북풍  — 바람이 북쪽에서 옴)
    u>0,  v=0  → 270° (서풍  — 바람이 서쪽에서 옴)
    u=0,  v>0  → 180° (남풍  — 바람이 남쪽에서 옴)
    u<0,  v=0  → 90°  (동풍  — 바람이 동쪽에서 옴)

    Parameters
    ----------
    u : array-like
        동서 바람 성분 (양수 = 동쪽으로 부는 방향).
    v : array-like
        남북 바람 성분 (양수 = 북쪽으로 부는 방향).

    Returns
    -------
    np.ndarray (float64)
        기상학적 풍향 [°]. 결과는 [0, 360) 범위.
        NaN 입력 시 NaN 전파.
        u=0, v=0 (정온) 인 경우 0° 반환 (수학적으로 미정의이나 0 으로 처리).

    SAMPLE — 격자 상대 바람(회전 필요)이거나 단위가 다를 때는 전처리 후 호출하라.
    """
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return np.degrees(np.arctan2(-u, -v)) % 360
