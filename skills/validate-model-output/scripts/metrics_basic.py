# SAMPLE — 실데이터에선 면적가중·정의차(불편RMSE 분모 N vs N-1, SI 분모 |mean| vs range 등)를
# 실시간 점검하고 도메인 맞춤 코드로 적응하라.
# 이 모듈은 공통 NaN 마스크를 적용한 기본 오차 통계 SAMPLE 함수 집합이다.
# 패키지가 아닌 플랫 모듈 — conftest.py 가 scripts/ 를 sys.path 에 등록하므로
# tests 에서 `import metrics_basic` 으로 직접 사용 가능.
"""기본 오차 통계 함수 모음 (numpy, 공통 NaN 마스크).

Public API
----------
bias(f, o)         -> float
mae(f, o)          -> float
rmse(f, o)         -> float
nrmse(f, o)        -> float
si(f, o)           -> float   # 불편RMSE / mean(o)
pearson_r(f, o)    -> float
linregress(f, o)   -> (slope: float, intercept: float)
"""
from __future__ import annotations

from typing import Tuple

import numpy as np


# ---------------------------------------------------------------------------
# 내부 유틸 — 공통 NaN/Inf 마스크
# ---------------------------------------------------------------------------

def _mask(f: np.ndarray, o: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """두 배열에서 모두 유한한(finite) 값 쌍만 반환.

    Args:
        f: 예측(forecast) 배열
        o: 관측(observation) 배열

    Returns:
        (fv, ov): 동일 유한 인덱스만 추출된 1-D 배열 쌍
    """
    f = np.asarray(f, dtype=float).ravel()
    o = np.asarray(o, dtype=float).ravel()
    valid = np.isfinite(f) & np.isfinite(o)
    return f[valid], o[valid]


# ---------------------------------------------------------------------------
# 오차 통계 함수
# ---------------------------------------------------------------------------

def bias(f: np.ndarray, o: np.ndarray) -> float:
    """편차(Bias): mean(f - o). NaN/Inf 쌍 제외.

    양수 → 예측 과대(over-forecast), 음수 → 예측 과소.
    """
    fv, ov = _mask(f, o)
    if fv.size == 0:
        return float("nan")
    return float(np.mean(fv - ov))


def mae(f: np.ndarray, o: np.ndarray) -> float:
    """평균절대오차(MAE): mean(|f - o|). NaN/Inf 쌍 제외."""
    fv, ov = _mask(f, o)
    if fv.size == 0:
        return float("nan")
    return float(np.mean(np.abs(fv - ov)))


def rmse(f: np.ndarray, o: np.ndarray) -> float:
    """평균제곱근오차(RMSE): sqrt(mean((f - o)^2)). NaN/Inf 쌍 제외."""
    fv, ov = _mask(f, o)
    if fv.size == 0:
        return float("nan")
    return float(np.sqrt(np.mean((fv - ov) ** 2)))


def nrmse(f: np.ndarray, o: np.ndarray) -> float:
    """정규화 RMSE(NRMSE): RMSE / |mean(o)|. NaN/Inf 쌍 제외.

    SAMPLE 주의: 분모 정의는 도메인마다 다를 수 있다
    (range, std, max 사용 사례도 있음). 실데이터 적용 전 확인하라.
    mean(o) ≈ 0 이면 nan 반환.
    """
    fv, ov = _mask(f, o)
    if fv.size == 0:
        return float("nan")
    mean_o = float(np.mean(ov))
    if mean_o == 0.0:
        return float("nan")
    r = float(np.sqrt(np.mean((fv - ov) ** 2))) / abs(mean_o)
    return r


def si(f: np.ndarray, o: np.ndarray) -> float:
    """산란지수(Scatter Index, SI): 불편RMSE / |mean(o)|. NaN/Inf 쌍 제외.

    불편RMSE = sqrt(mean(((f - mean(f)) - (o - mean(o)))^2))
             = sqrt(RMSE^2 - Bias^2)

    SI ≥ 0. 값이 작을수록 무작위 오차(편향 제거 후) 가 작음을 의미.
    mean(o) ≈ 0 이면 nan 반환.
    """
    fv, ov = _mask(f, o)
    if fv.size == 0:
        return float("nan")
    mean_o = float(np.mean(ov))
    if mean_o == 0.0:
        return float("nan")
    diff = fv - ov
    b = float(np.mean(diff))
    unbiased_mse = float(np.mean((diff - b) ** 2))
    # 부동소수점 오차로 음수가 될 수 있으므로 max(0, ...) 보호
    unbiased_rmse = float(np.sqrt(max(0.0, unbiased_mse)))
    return unbiased_rmse / abs(mean_o)


def pearson_r(f: np.ndarray, o: np.ndarray) -> float:
    """피어슨 상관계수(r): -1 ~ 1. NaN/Inf 쌍 제외.

    유효 쌍이 2개 미만이거나 분산이 0이면 nan 반환.
    """
    fv, ov = _mask(f, o)
    if fv.size < 2:
        return float("nan")
    # np.corrcoef 는 분산이 0이면 nan 을 반환하므로 별도 처리 불필요
    return float(np.corrcoef(fv, ov)[0, 1])


def linregress(f: np.ndarray, o: np.ndarray) -> Tuple[float, float]:
    """단순 선형 회귀: f ~ slope * o + intercept. NaN/Inf 쌍 제외.

    SAMPLE — polyfit(최소제곱) 사용. 실데이터에서 가중치·로버스트 회귀가
    필요하면 도메인 맞춤 코드로 교체하라.

    Returns:
        (slope, intercept): o → f 방향 회귀 계수
        유효 쌍 2개 미만이면 (nan, nan) 반환.
    """
    fv, ov = _mask(f, o)
    if fv.size < 2:
        return float("nan"), float("nan")
    slope, intercept = np.polyfit(ov, fv, 1)
    return float(slope), float(intercept)
