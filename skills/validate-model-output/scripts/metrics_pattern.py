"""패턴 통계 모듈 — Taylor·Target 다이어그램 지표 계산.

SAMPLE — 실데이터에서는 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
이 모듈은 '대략적 구조 파악 + 적응의 출발점'이다.
- 입력 배열 형상·결측 처리·마스킹은 실데이터에 맞게 검토할 것.
- 파랑(WW3)·부이 등 도메인에 따라 비교 격자 정합 전처리가 선행되어야 한다.

공개 API
--------
taylor_stats(o, f)      -> dict  # std_ratio, corr, crmsd
target_stats(o, f)      -> dict  # bias, urmsd
pattern_correlation(o, f) -> float  # 공간 패턴 상관
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# 내부 유틸
# ---------------------------------------------------------------------------

def _flatten_valid(o: np.ndarray, f: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """두 배열을 1-D로 평탄화하고 양쪽 모두 유한한 쌍만 반환.

    SAMPLE — 실데이터에서는 NaN/FillValue 처리, 마스크 배열, 단위 통일 여부를
    반드시 실시간 점검하고 여기에 적응하라.
    """
    o_flat = np.asarray(o, dtype="float64").ravel()
    f_flat = np.asarray(f, dtype="float64").ravel()
    if o_flat.shape != f_flat.shape:
        raise ValueError(
            f"관측(o)과 예측(f) 형상 불일치: {np.asarray(o).shape} vs {np.asarray(f).shape}"
        )
    valid = np.isfinite(o_flat) & np.isfinite(f_flat)
    return o_flat[valid], f_flat[valid]


# ---------------------------------------------------------------------------
# Taylor 다이어그램 지표
# ---------------------------------------------------------------------------

def taylor_stats(o: np.ndarray, f: np.ndarray) -> dict:
    """Taylor 다이어그램용 패턴 일치 지표.

    Parameters
    ----------
    o : array-like
        관측값(reference). 임의 형상 가능.
    f : array-like
        예측/모델값. o 와 같은 형상.

    Returns
    -------
    dict with keys
        std_ratio : float
            표준편차 비  σ_f / σ_o.  1에 가까울수록 분산 일치.
        corr : float
            Pearson 상관계수.  1에 가까울수록 패턴 일치.
        crmsd : float
            Centered RMSD (= unbiased RMSD).
            sqrt( mean( (f' - o')^2 ) )  where x' = x - mean(x).
            0에 가까울수록 패턴 오차 없음.

    SAMPLE — 실데이터에서 결측·격자 정합·단위 일치를 선행 확인하라.
    """
    o_v, f_v = _flatten_valid(o, f)
    n = len(o_v)
    if n < 2:
        nan = float("nan")
        return {"std_ratio": nan, "corr": nan, "crmsd": nan, "n": n}

    o_mean = float(np.mean(o_v))
    f_mean = float(np.mean(f_v))
    o_std = float(np.std(o_v, ddof=0))
    f_std = float(np.std(f_v, ddof=0))

    # 표준편차 비 (o_std=0 이면 정의 불가)
    if o_std == 0.0:
        std_ratio = float("nan")
        crmsd = float("nan")
        corr = float("nan")
    else:
        std_ratio = f_std / o_std

        # Pearson 상관계수 (f_std=0 이면 0)
        if f_std == 0.0:
            corr = 0.0
        else:
            corr = float(np.corrcoef(o_v, f_v)[0, 1])

        # CRMSD = sqrt( σ_f² + σ_o² - 2·σ_f·σ_o·R )
        # 수치 안정: 음수가 되지 않도록 clip
        crmsd_sq = f_std**2 + o_std**2 - 2.0 * f_std * o_std * corr
        crmsd = float(np.sqrt(max(crmsd_sq, 0.0)))

    return {
        "std_ratio": std_ratio,
        "corr": corr,
        "crmsd": crmsd,
        "n": n,
    }


# ---------------------------------------------------------------------------
# Target 다이어그램 지표
# ---------------------------------------------------------------------------

def target_stats(o: np.ndarray, f: np.ndarray) -> dict:
    """Target 다이어그램용 편차 분해 지표.

    Parameters
    ----------
    o : array-like
        관측값.
    f : array-like
        예측/모델값.

    Returns
    -------
    dict with keys
        bias : float
            평균 편차  mean(f) - mean(o).  양수=과대예측, 음수=과소예측.
        urmsd : float
            Unbiased RMSD = Centered RMSD.
            sqrt( mean( ((f - mean(f)) - (o - mean(o)))^2 ) ).
            0에 가까울수록 패턴 오차 없음.
        rmsd : float
            전체 RMSD = sqrt(bias² + urmsd²).

    SAMPLE — 실데이터에서 결측·격자 정합·단위 일치를 선행 확인하라.
    """
    o_v, f_v = _flatten_valid(o, f)
    n = len(o_v)
    if n < 1:
        nan = float("nan")
        return {"bias": nan, "urmsd": nan, "rmsd": nan, "n": n}

    bias = float(np.mean(f_v) - np.mean(o_v))

    # uRMSD = CRMSD
    o_anom = o_v - np.mean(o_v)
    f_anom = f_v - np.mean(f_v)
    urmsd = float(np.sqrt(np.mean((f_anom - o_anom) ** 2)))

    # 전체 RMSD
    rmsd = float(np.sqrt(np.mean((f_v - o_v) ** 2)))

    return {
        "bias": bias,
        "urmsd": urmsd,
        "rmsd": rmsd,
        "n": n,
    }


# ---------------------------------------------------------------------------
# 공간 패턴 상관
# ---------------------------------------------------------------------------

def pattern_correlation(o: np.ndarray, f: np.ndarray) -> float:
    """공간 패턴 상관계수 (Pearson).

    임의 형상의 2개 배열을 1-D로 평탄화한 뒤 유효 쌍만으로 상관 계산.
    Taylor 다이어그램의 corr 과 동일하지만, '공간 스냅샷' 비교에 특화한
    진입점으로 별도 제공한다.

    Parameters
    ----------
    o : array-like
        관측/참조 공간장.  (ny, nx) 또는 임의 N-D.
    f : array-like
        예측 공간장.  o 와 같은 형상.

    Returns
    -------
    float
        Pearson 상관계수.  유효 쌍이 2개 미만이면 NaN.

    SAMPLE — 실데이터에서는 격자 보간·육상 마스크 적용 후 호출하라.
    """
    o_v, f_v = _flatten_valid(o, f)
    if len(o_v) < 2:
        return float("nan")
    o_std = float(np.std(o_v, ddof=0))
    f_std = float(np.std(f_v, ddof=0))
    if o_std == 0.0 or f_std == 0.0:
        return float("nan")
    return float(np.corrcoef(o_v, f_v)[0, 1])
