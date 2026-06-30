"""원형 통계 지표 — 파향·풍향 검증용.

SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.

입력 규약
---------
- 각도 단위: **도(degree)**, 범위 [0, 360) 또는 임의.
- 오차 규약: **±180°** — 오차를 (-180, +180] 로 래핑한다.
- 배열 입력: float 또는 array-like (numpy broadcast 가능).
- NaN 포함 시 numpy nan-safe 함수(`np.nanmean` 등)를 쓰되,
  실데이터에선 결측 마스크를 먼저 확인하라.

사용 예
-------
>>> from scripts.metrics_circular import circular_mean_error, circular_rmse, circular_corr
>>> circular_mean_error(350.0, 10.0)   # 오차 ≈ -20°
-20.0
>>> circular_rmse([350.0, 10.0], [10.0, 350.0])  # ≈ 20°
20.0
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# 내부 헬퍼
# ---------------------------------------------------------------------------

def _wrap180(delta_deg: np.ndarray) -> np.ndarray:
    """각도 차를 (-180, +180] 구간으로 래핑한다.

    SAMPLE — 실데이터 단위(라디안 vs 도)를 반드시 확인하라.
    """
    return (delta_deg + 180.0) % 360.0 - 180.0


def _to_array(x) -> np.ndarray:
    return np.asarray(x, dtype=float)


# ---------------------------------------------------------------------------
# 공개 함수
# ---------------------------------------------------------------------------

def circular_mean_error(
    forecast_deg,
    observed_deg,
) -> float:
    """원형 평균 오차 (Circular Mean Error, CME).

    오차 = forecast − observed, ±180° 래핑 적용 후 평균.
    부호 있음(signed): 양수→ 예보가 시계방향 편향, 음수→ 반시계방향 편향.

    Parameters
    ----------
    forecast_deg : float or array-like
        예보 방향(도).
    observed_deg : float or array-like
        관측 방향(도).

    Returns
    -------
    float
        평균 오차 (도), 범위 (-180, +180].

    Examples
    --------
    SAMPLE — 스칼라 케이스:
    >>> circular_mean_error(350.0, 10.0)
    -20.0
    >>> circular_mean_error(10.0, 350.0)
    20.0

    SAMPLE — 동일 배열이면 0:
    >>> import numpy as np
    >>> a = np.array([45.0, 90.0, 315.0])
    >>> circular_mean_error(a, a)
    0.0
    """
    f = _to_array(forecast_deg)
    o = _to_array(observed_deg)
    diff = _wrap180(f - o)
    # 평균도 원형 래핑 (평균 자체가 ±180 넘을 일은 거의 없으나 안전하게)
    return float(_wrap180(np.nanmean(diff)))


def circular_rmse(
    forecast_deg,
    observed_deg,
) -> float:
    """원형 RMSE (Circular Root Mean Squared Error).

    ±180° 래핑된 오차의 RMS.  값은 항상 ≥ 0.

    Parameters
    ----------
    forecast_deg : float or array-like
        예보 방향(도).
    observed_deg : float or array-like
        관측 방향(도).

    Returns
    -------
    float
        RMSE (도), 범위 [0, 180].

    Examples
    --------
    SAMPLE:
    >>> circular_rmse(350.0, 10.0)
    20.0
    >>> import numpy as np
    >>> a = np.array([0.0, 90.0, 180.0])
    >>> circular_rmse(a, a)
    0.0
    """
    f = _to_array(forecast_deg)
    o = _to_array(observed_deg)
    diff = _wrap180(f - o)
    return float(np.sqrt(np.nanmean(diff ** 2)))


def circular_corr(
    forecast_deg,
    observed_deg,
) -> float:
    """원형 상관계수 (Circular–Circular Correlation).

    Jammalamadaka & SenGupta (2001) 공식 기반.
    sin 변환을 사용하므로 위상 차이에 민감하다.

    반환값 범위: [-1, 1].
    - 1 에 가까울수록 예보·관측 방향이 일치.
    - 0 에 가까우면 무상관.
    - -1 이면 방향이 반대 패턴.

    Parameters
    ----------
    forecast_deg : array-like, 길이 ≥ 2
        예보 방향(도).
    observed_deg : array-like, 길이 ≥ 2
        관측 방향(도).

    Returns
    -------
    float
        원형 상관계수. 분산 0·상수·빈 배열이면 nan (크래시·경고 없음).

    Notes
    -----
    SAMPLE — 모든 값이 동일한 **상수 배열**이면 평균 합성 벡터 길이 R = 1 →
    분산 0 → nan 반환.  변동이 있는 배열에서 f==o 이면 1.0 반환(완전 상관).
    실데이터에선 분산 확인 후 사용하라.

    구현 노트: ``denominator == 0`` 만으로는 py3.9/구버전 NumPy 에서
    arctan2 round-trip 부동소수 오차로 분모가 정확히 0 이 되지 않을 수 있다.
    이를 막기 위해 arctan2 계산 전에 평균 합성 벡터 길이 R 을 점검한다.
    상수 배열이면 sin²+cos²=1 에 의해 R = 1.0 이 정확하게 성립하므로
    Python/NumPy 버전에 무관하게 안전하게 NaN 을 반환한다.

    Examples
    --------
    SAMPLE — 동일(다변동) 배열 → 완전 상관 1.0:
    >>> import numpy as np
    >>> f = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    >>> circular_corr(f, f)
    1.0

    SAMPLE — 상수 배열 → R=1(분산 0) → nan:
    >>> g = np.array([45.0, 45.0, 45.0, 45.0])
    >>> import math; math.isnan(circular_corr(g, g))
    True

    SAMPLE — 의미 있는 변동이 있는 케이스:
    >>> f2 = np.array([0., 90., 180., 270., 10., 100.])
    >>> o2 = np.array([5., 95., 185., 275., 15., 105.])
    >>> 0.9 < circular_corr(f2, o2) <= 1.0
    True
    """
    f = _to_array(forecast_deg)
    o = _to_array(observed_deg)

    # 빈 배열 / 유효 쌍 부족 가드 (RuntimeWarning 방지)
    valid = ~(np.isnan(f) | np.isnan(o))
    if int(valid.sum()) < 2:
        return float("nan")

    # 각 배열의 원형 평균 (라디안 경유)
    f_rad = np.deg2rad(f)
    o_rad = np.deg2rad(o)

    sin_f_mean = np.nanmean(np.sin(f_rad))
    cos_f_mean = np.nanmean(np.cos(f_rad))
    sin_o_mean = np.nanmean(np.sin(o_rad))
    cos_o_mean = np.nanmean(np.cos(o_rad))

    # 상수 배열 / 분산 0 가드 ―― arctan2 계산 전에 수행.
    # 평균 합성 벡터 길이 R: 상수 배열이면 sin²+cos²=1 에 의해 R=1.0 이
    # Python/NumPy 버전에 무관하게 정확하게 성립한다.
    # R ≈ 1 이면 모든 값이 동일한 방향 → 원형 분산 0 → 상관 정의 불가 → NaN.
    # (denominator == 0 검사만으로는 py3.9 등에서 tiny nonzero 가 될 수 있다.)
    R_f = np.hypot(cos_f_mean, sin_f_mean)
    R_o = np.hypot(cos_o_mean, sin_o_mean)
    if not (R_f < 1.0 - 1e-9 and R_o < 1.0 - 1e-9):
        return float("nan")

    f_bar = np.arctan2(sin_f_mean, cos_f_mean)
    o_bar = np.arctan2(sin_o_mean, cos_o_mean)

    sin_f = np.sin(f_rad - f_bar)
    sin_o = np.sin(o_rad - o_bar)

    numerator = np.nansum(sin_f * sin_o)
    denominator = np.sqrt(np.nansum(sin_f ** 2) * np.nansum(sin_o ** 2))

    # 추가 안전망: R 검사를 통과했어도 부동소수 예외 케이스 대비
    if not (denominator > 0.0):
        return float("nan")

    return float(np.clip(numerator / denominator, -1.0, 1.0))
