"""전처리 브리지 — mesh→점 matchup(R3) + 단위 정규화 + 시간대/좌표 주입 SAMPLE.

SAMPLE — 격자/mesh/CRS/시간정합 데이터마다 다르니 실시간 적응하라;
일반 regrid 범위밖 케이스(구형 보간·CRS 변환·시간보간 등)는
이 코드 범위 밖이므로 실데이터 구조를 반드시 먼저 점검하고 도메인 맞춤 코드로 적응하라.

제공 함수:
  to_kelvin(values, units)           -- 온도 단위 → 켈빈 변환
  match_points_to_mesh(...)          -- cKDTree 최근접 노드 매칭 + 거리 필터
  build_pairs(...)                   -- station/time/model/obs 롱포맷 (선택)
  tz_to_utc(times, tz)              -- 시간대 변환 → UTC datetime64[ns]
  inject_point_coords(ids, mapping) -- 정점 ID → 위경도 배열 주입
  parse_points_list(path)           -- 관측점 파일 파싱 (에이전트/CLI 명시 호출)
  common_time_index(t1, t2)         -- 두 시계열 교집합 인덱스
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


# ---------------------------------------------------------------------------
# 4. 시간대 변환 — UTC 정규화
# ---------------------------------------------------------------------------

# KST(=UTC+9) 표기 변형 목록 (상단 정규화 후 비교)
_KST_ALIASES = {"KST", "+09:00", "+09", "+0900", "UTC+09:00", "UTC+9", "UTC+09"}


def tz_to_utc(times, tz=None):
    """시계열을 UTC datetime64[ns] 로 변환한다 (SAMPLE).

    Parameters
    ----------
    times : array-like
        datetime-like 배열 (np.datetime64·str·datetime 등).
    tz : str or None
        'UTC'            → 그대로 반환 (assumed=False).
        'KST'/'+09:00'   → -9h 적용하여 UTC 반환 (assumed=False).
        None             → UTC로 가정 (assumed=True).
        기타 알 수 없는 값 → UTC로 가정 + UserWarning (assumed=True).

    Returns
    -------
    times_utc : np.ndarray[datetime64[ns]]
        UTC 기준 시계열.
    assumed   : bool
        True 이면 TZ 미확인·가정(경고 필요). False 이면 명시 변환.

    SAMPLE — 실데이터에서 TZ 메타가 없으면 에이전트/사용자에게
    "부이 KST vs 모델 UTC 면 9 h 어긋남" 경고를 함께 전달하라.
    """
    # datetime64[ns] 로 안전 변환
    try:
        times_arr = np.asarray(times, dtype="datetime64[ns]")
    except (ValueError, TypeError):
        times_arr = np.array([np.datetime64(str(t), "ns") for t in times])

    if tz is None:
        return times_arr.copy(), True

    # 정규화: 공백 제거 + 대문자
    tz_norm = str(tz).strip().upper().replace(" ", "")

    if tz_norm == "UTC":
        return times_arr.copy(), False

    if tz_norm in _KST_ALIASES:
        # KST = UTC+9 → UTC = KST − 9 h
        offset = np.timedelta64(9, "h")
        return (times_arr - offset).astype("datetime64[ns]"), False

    # 알 수 없는 tz → UTC로 가정 + 경고
    warnings.warn(
        f"tz_to_utc: 알 수 없는 시간대 '{tz}' — UTC로 가정(assumed=True). "
        "KST 데이터라면 'KST' 또는 '+09:00' 을 명시하라.",
        UserWarning,
        stacklevel=2,
    )
    return times_arr.copy(), True


# ---------------------------------------------------------------------------
# 5. 정점 좌표 주입
# ---------------------------------------------------------------------------

def inject_point_coords(station_ids, mapping):
    """정점 ID 목록을 받아 위경도 배열을 반환한다 (SAMPLE).

    Parameters
    ----------
    station_ids : sequence[str]
        정점 ID 목록.
    mapping     : dict[str, tuple[float, float]]
        {정점ID: (lat, lon)} 형식 딕셔너리.
        에이전트/CLI 가 실데이터에서 구성해 주입한다.

    Returns
    -------
    lats : np.ndarray[float64]  — 위도 배열 (없는 ID 는 nan)
    lons : np.ndarray[float64]  — 경도 배열 (없는 ID 는 nan)

    SAMPLE — mapping 구성 방법(파일 파싱 등)은 호출 측에서 결정한다.
    parse_points_list() 를 활용하거나 실데이터 메타에서 직접 구성하라.
    """
    lats: list[float] = []
    lons: list[float] = []
    for sid in station_ids:
        if sid in mapping:
            lat, lon = mapping[sid]
            lats.append(float(lat))
            lons.append(float(lon))
        else:
            lats.append(float("nan"))
            lons.append(float("nan"))
    return np.array(lats, dtype=float), np.array(lons, dtype=float)


# ---------------------------------------------------------------------------
# 6. 관측점 목록 파일 파싱 (에이전트/CLI 명시 호출 전용)
# ---------------------------------------------------------------------------

def parse_points_list(path):
    """관측점 목록 파일을 읽어 {id: (lat, lon)} 딕셔너리를 반환한다 (SAMPLE).

    SAMPLE — 에이전트/CLI 가 명시 호출. 형식이 다르면 실시간 적응하라.
    코어 자동경로에 박지 말 것(자동 호출 금지) — 범용 주입구만 사용.

    지원 포맷 (best-effort 관용 파싱):
      'lon lat id'  — 공백/탭 구분 (기본 가정)
      '#' 로 시작하는 줄은 주석으로 건너뜀.
      파싱 불가한 줄은 경고 없이 건너뜀(no-crash).

    Parameters
    ----------
    path : str or Path
        관측점 목록 텍스트 파일 경로.

    Returns
    -------
    dict[str, tuple[float, float]]
        {정점ID: (lat, lon)}

    사용 예::
        mapping = parse_points_list('points.list')
        lats, lons = inject_point_coords(station_ids, mapping)
    """
    result: dict = {}
    try:
        with open(str(path), encoding="utf-8") as fh:
            lines = fh.readlines()
    except UnicodeDecodeError:
        # cp949 폴백 (한글 경로·내용 대비)
        with open(str(path), encoding="cp949") as fh:
            lines = fh.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            lon = float(parts[0])
            lat = float(parts[1])
            sid = parts[2]
            result[sid] = (lat, lon)
        except (ValueError, IndexError):
            # 파싱 불가 줄 → 건너뜀(no-crash)
            continue

    return result


# ---------------------------------------------------------------------------
# 7. 두 시계열 교집합 인덱스
# ---------------------------------------------------------------------------

def common_time_index(t1, t2):
    """두 datetime64 시계열의 교집합 인덱스를 반환한다 (SAMPLE).

    Parameters
    ----------
    t1, t2 : array-like of datetime64-like
        비교할 두 시계열 (np.datetime64·str·datetime 등).

    Returns
    -------
    idx1 : np.ndarray[int]
        t1 에서 교집합 원소의 인덱스 (오름차순 정렬).
    idx2 : np.ndarray[int]
        t2 에서 교집합 원소의 인덱스 (오름차순 정렬).

    사용 예::
        idx1, idx2 = common_time_index(obs_times, model_times)
        obs_common   = obs_vals[idx1]
        model_common = model_vals[idx2]

    SAMPLE — 중복 타임스탬프가 있으면 np.intersect1d 가 중복 제거한다.
    실데이터에서는 시간 해상도(초/분/시간)와 타임스탬프 정확도를 먼저 확인하라.
    """
    try:
        t1_arr = np.asarray(t1, dtype="datetime64[ns]")
    except (ValueError, TypeError):
        t1_arr = np.array([np.datetime64(str(x), "ns") for x in t1])

    try:
        t2_arr = np.asarray(t2, dtype="datetime64[ns]")
    except (ValueError, TypeError):
        t2_arr = np.array([np.datetime64(str(x), "ns") for x in t2])

    _, idx1, idx2 = np.intersect1d(t1_arr, t2_arr, return_indices=True)
    return idx1, idx2
