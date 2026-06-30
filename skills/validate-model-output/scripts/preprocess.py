"""전처리 브리지 — mesh→점 matchup(R3) + 단위 정규화 SAMPLE.

SAMPLE — 격자/mesh/CRS/시간정합 데이터마다 다르니 실시간 적응하라;
일반 regrid 범위밖 케이스(구형 보간·CRS 변환·시간보간 등)는
이 코드 범위 밖이므로 실데이터 구조를 반드시 먼저 점검하고 도메인 맞춤 코드로 적응하라.

제공 함수:
  to_kelvin(values, units)           -- 온도 단위 → 켈빈 변환
  match_points_to_mesh(...)          -- cKDTree 최근접 노드 매칭 + 거리 필터
  build_pairs(...)                   -- station/time/model/obs 롱포맷 (선택)
"""
from __future__ import annotations

import warnings

import numpy as np


# ---------------------------------------------------------------------------
# 1. 단위 정규화
# ---------------------------------------------------------------------------

# 섭씨 표기 변형 목록 (소문자 trim 후 비교)
_CELSIUS_ALIASES = {"degc", "celsius", "°c", "c", "deg_c", "deg c"}
_KELVIN_ALIASES  = {"k", "kelvin", "kelvins"}


def to_kelvin(values, units: str) -> np.ndarray:
    """온도값을 켈빈(K)으로 변환한다.

    Parameters
    ----------
    values : array-like
        입력 온도값 (스칼라·리스트·ndarray 모두 가능).
    units  : str
        단위 문자열.
        * 'degC' / 'celsius' / '°C' / 'C' → +273.15
        * 'K' / 'kelvin'                  → 그대로
        * 그 외(알 수 없음)               → 그대로 반환 + UserWarning 표식

    Returns
    -------
    np.ndarray (float64)

    SAMPLE — 실데이터에서는 units 문자열 형식이 다를 수 있으니 _CELSIUS_ALIASES 를
    직접 확장하거나 cf_units/pint 라이브러리로 대체하라.
    """
    arr = np.asarray(values, dtype=float)
    u = units.strip().lower()

    if u in _CELSIUS_ALIASES:
        return arr + 273.15
    if u in _KELVIN_ALIASES:
        return arr.copy()

    # 알 수 없는 단위 — 변환 없이 원본 반환 + 경고(표식)
    warnings.warn(
        f"to_kelvin: 알 수 없는 단위 '{units}' — 변환 없이 원본 반환 (표식). "
        "_CELSIUS_ALIASES / _KELVIN_ALIASES 에 추가하거나 전문 라이브러리를 사용하라.",
        UserWarning,
        stacklevel=2,
    )
    return arr.copy()


# ---------------------------------------------------------------------------
# 2. mesh → 점 매칭
# ---------------------------------------------------------------------------

_KM_PER_DEG = 111.2   # 위도 1도 ≈ 111.2 km (SAMPLE 근사)


def match_points_to_mesh(
    mesh_lon,
    mesh_lat,
    pt_lon,
    pt_lat,
    max_km: float = 50.0,
):
    """비정형 mesh의 최근접 노드를 관측점에 매칭한다 (SAMPLE).

    scipy.spatial.cKDTree 로 최근접 노드 인덱스를 찾고,
    위경도 차이 기반 근사 km 거리를 계산한다.
    max_km 를 초과하는 관측점의 인덱스는 -1 로 표시(제외).

    Parameters
    ----------
    mesh_lon, mesh_lat : array-like, shape (N_node,)
        mesh 노드 좌표.
    pt_lon, pt_lat     : array-like, shape (N_pts,)
        관측(부이) 점 좌표.
    max_km             : float
        이 거리(km)를 초과하면 해당 관측점을 제외(-1).

    Returns
    -------
    indices  : np.ndarray[int],   shape (N_pts,)  — -1 = 임계초과/제외
    dists_km : np.ndarray[float], shape (N_pts,)  — 최근접 노드까지의 근사 거리(km)

    SAMPLE 주의:
    * 구면 거리 대신 평면 근사(cos 보정)를 사용 — 고위도·장거리는 오차 증가.
    * 실데이터에서는 CRS·데이텀·기준타원체를 확인하고 pyproj 등으로 대체하라.
    * mesh 노드 수가 수십만 이상이면 BallTree(Haversine 커널)가 더 정확·효율적.
    """
    try:
        from scipy.spatial import cKDTree  # lazy import — 설치 확인
    except ImportError as e:
        raise ImportError("match_points_to_mesh 은 scipy 를 필요로 합니다.") from e

    mesh_lon = np.asarray(mesh_lon, dtype=float).ravel()
    mesh_lat = np.asarray(mesh_lat, dtype=float).ravel()
    pt_lon   = np.asarray(pt_lon,   dtype=float).ravel()
    pt_lat   = np.asarray(pt_lat,   dtype=float).ravel()

    if mesh_lon.shape != mesh_lat.shape:
        raise ValueError("mesh_lon 과 mesh_lat 의 크기가 다릅니다.")
    if pt_lon.shape != pt_lat.shape:
        raise ValueError("pt_lon 과 pt_lat 의 크기가 다릅니다.")

    # KD 트리 생성 (위경도 2D, 도 단위 — 빠른 최근접 탐색)
    mesh_coords = np.column_stack([mesh_lon, mesh_lat])
    tree = cKDTree(mesh_coords)

    # 쿼리
    query_pts = np.column_stack([pt_lon, pt_lat])
    _, raw_idx = tree.query(query_pts)          # shape (N_pts,)

    # 근사 km 거리 계산 (cos 보정 평면 근사, SAMPLE)
    mean_lat_rad = np.deg2rad(0.5 * (mesh_lat[raw_idx] + pt_lat))
    dlat_km = (pt_lat - mesh_lat[raw_idx]) * _KM_PER_DEG
    dlon_km = (pt_lon - mesh_lon[raw_idx]) * _KM_PER_DEG * np.cos(mean_lat_rad)
    dists_km = np.sqrt(dlat_km ** 2 + dlon_km ** 2)

    # max_km 초과 → -1
    indices = raw_idx.astype(int).copy()
    indices[dists_km > max_km] = -1

    return indices, dists_km


# ---------------------------------------------------------------------------
# 3. 롱포맷 쌍 생성 (선택적 헬퍼)
# ---------------------------------------------------------------------------

def build_pairs(stations, times, model_vals, obs_vals, var_name: str = "value"):
    """모델-관측 쌍을 station/time/model/obs 롱포맷 DataFrame 으로 만든다 (SAMPLE).

    Parameters
    ----------
    stations   : sequence[str], length S
        관측 지점 이름 목록.
    times      : sequence, length T
        시간 스텝 목록 (문자열·datetime 모두 가능).
    model_vals : array-like, shape (T, S)
        모델 예측값.
    obs_vals   : array-like, shape (T, S)
        관측값.
    var_name   : str
        변수 이름 (현재는 메타 정보용; 확장 시 'variable' 컬럼 추가 가능).

    Returns
    -------
    pd.DataFrame  columns: ['station', 'time', 'model', 'obs']

    SAMPLE — 실데이터에서는 시간 인덱스 매칭·결측 처리·단위 통일을 먼저 수행하라.
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError("build_pairs 은 pandas 를 필요로 합니다.") from e

    stations_list = list(stations)
    times_list    = list(times)
    model_arr     = np.asarray(model_vals, dtype=float)
    obs_arr       = np.asarray(obs_vals,   dtype=float)

    if model_arr.shape != obs_arr.shape:
        raise ValueError(
            f"model_vals.shape {model_arr.shape} ≠ obs_vals.shape {obs_arr.shape}"
        )

    rows = []
    for ti, t in enumerate(times_list):
        for si, s in enumerate(stations_list):
            rows.append(
                {
                    "station": s,
                    "time":    t,
                    "model":   float(model_arr[ti, si]),
                    "obs":     float(obs_arr[ti, si]),
                }
            )
    return pd.DataFrame(rows, columns=["station", "time", "model", "obs"])
