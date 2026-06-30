"""분포 비교 유틸리티 — SAMPLE.

SAMPLE — 실데이터에선 구조를 실시간 점검하고
도메인 맞춤 코드로 적응하라.
변수 스케일·분포 형태·이상치 처리 방식은
실제 모델/관측 데이터마다 다를 수 있다.

Distribution comparison utilities for model QC.
Functions
---------
quantiles(x, p)               : 분위수 벡터 계산
qq_points(obs, fct)           : Q-Q 비교점 (obs_q, fct_q)
perkins_skill_score(obs, fct)  : 공통면적 기반 유사도 [0, 1]
ks_distance(obs, fct)         : Kolmogorov-Smirnov 통계량 D
"""
from __future__ import annotations

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# 공개 API
# ---------------------------------------------------------------------------

def quantiles(x: np.ndarray, p: np.ndarray | list) -> np.ndarray:
    """배열 x 의 분위수를 반환한다.

    Parameters
    ----------
    x : array-like   — 1-D 또는 N-D (flatten 처리)
    p : array-like   — 분위수 확률값 [0, 1] 범위

    Returns
    -------
    np.ndarray, shape == len(p)

    SAMPLE — NaN 처리, 가중치 등은 실데이터에 맞춰 확장하라.
    """
    x = np.asarray(x, dtype=float).ravel()
    p = np.asarray(p, dtype=float)
    # NaN 제거 후 분위수 계산
    x_valid = x[np.isfinite(x)]
    if x_valid.size == 0:
        return np.full(p.shape, np.nan)
    return np.percentile(x_valid, p * 100.0)


def qq_points(
    obs: np.ndarray,
    fct: np.ndarray,
    n_quantiles: int = 50,
) -> tuple[np.ndarray, np.ndarray]:
    """관측(obs)·예측(fct) Q-Q 비교점 쌍을 반환한다.

    Parameters
    ----------
    obs, fct     : 1-D array-like (값 순서 무관, 크기 달라도 됨)
    n_quantiles  : Q-Q 점 개수 (기본 50)

    Returns
    -------
    (obs_q, fct_q) : 길이 n_quantiles 의 분위수 배열 쌍

    SAMPLE — 실데이터에서 이상치·결측 비율이 높으면
    n_quantiles 와 분위 범위를 조정하라.
    """
    p = np.linspace(0.0, 1.0, n_quantiles)
    return quantiles(obs, p), quantiles(fct, p)


def perkins_skill_score(
    obs: np.ndarray,
    fct: np.ndarray,
    bins: int | np.ndarray = 20,
) -> float:
    """Perkins Skill Score (PSS) — 분포 공통면적 척도.

    PSS = sum( min(obs_freq_i, fct_freq_i) ) ∈ [0, 1].
    1에 가까울수록 두 분포가 유사, 0에 가까울수록 다름.

    Parameters
    ----------
    obs, fct : 1-D array-like
    bins     : 히스토그램 빈 수(int) 또는 빈 경계 배열

    Returns
    -------
    float — PSS 값 [0, 1]

    SAMPLE — 빈 수·범위는 변수 스케일에 맞춰 조정하라.
    분포가 좁고 뾰족하면(첨도 높음) bins 를 늘려라.
    """
    obs = np.asarray(obs, dtype=float).ravel()
    fct = np.asarray(fct, dtype=float).ravel()
    obs = obs[np.isfinite(obs)]
    fct = fct[np.isfinite(fct)]
    if obs.size == 0 or fct.size == 0:
        return float("nan")

    # 공통 범위로 빈 결정 (SAMPLE — 실데이터에선 범위를 도메인 지식으로 고정 권장)
    lo = min(obs.min(), fct.min())
    hi = max(obs.max(), fct.max())
    if lo == hi:
        return 1.0  # 모든 값이 같음

    if isinstance(bins, int):
        bin_edges = np.linspace(lo, hi, bins + 1)
    else:
        bin_edges = np.asarray(bins, dtype=float)

    obs_freq, _ = np.histogram(obs, bins=bin_edges, density=False)
    fct_freq, _ = np.histogram(fct, bins=bin_edges, density=False)

    # 빈도 → 상대빈도(면적 합 = 1)
    obs_rel = obs_freq / obs_freq.sum() if obs_freq.sum() > 0 else obs_freq
    fct_rel = fct_freq / fct_freq.sum() if fct_freq.sum() > 0 else fct_freq

    return float(np.sum(np.minimum(obs_rel, fct_rel)))


def ks_distance(
    obs: np.ndarray,
    fct: np.ndarray,
) -> float:
    """Kolmogorov-Smirnov 통계량 D (최대 CDF 차이).

    D ∈ [0, 1]. 0에 가까울수록 두 분포가 유사.

    Parameters
    ----------
    obs, fct : 1-D array-like

    Returns
    -------
    float — KS statistic (D-value)

    SAMPLE — p-value 도 필요하면 scipy.stats.ks_2samp() 결과 전체를 반환하도록 수정하라.
    """
    obs = np.asarray(obs, dtype=float).ravel()
    fct = np.asarray(fct, dtype=float).ravel()
    obs = obs[np.isfinite(obs)]
    fct = fct[np.isfinite(fct)]
    if obs.size == 0 or fct.size == 0:
        return float("nan")
    result = stats.ks_2samp(obs, fct)
    return float(result.statistic)
