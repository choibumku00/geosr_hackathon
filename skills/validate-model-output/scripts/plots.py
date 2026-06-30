import matplotlib; matplotlib.use("Agg")  # noqa: E402 — 첫 줄 필수(백엔드 고정)
"""파랑 모델 검증용 그림 SAMPLE 모듈.

SAMPLE — 캡션 §G(reference≠truth·advisory·단일그림금지) 강제.
도메인별 그림은 카탈로그(project/research/figures)를 보고 실시간 작성하라.
이 파일은 대략적 구조 파악 + 적응의 출발점이 되는 SAMPLE/템플릿이다.
완비 금지 — 대표 샘플만 제공. 실데이터에선 구조를 실시간 점검하고
도메인 맞춤 코드로 적응하라.
"""

import os
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# 내부 유틸 — NaN 안전
# ---------------------------------------------------------------------------

def _finite_pair(o: np.ndarray, f: np.ndarray):
    """두 배열에서 둘 다 유한한 인덱스만 골라낸 (o_clean, f_clean) 반환."""
    o = np.asarray(o, dtype=float).ravel()
    f = np.asarray(f, dtype=float).ravel()
    mask = np.isfinite(o) & np.isfinite(f)
    return o[mask], f[mask]


def _scatter_index(o: np.ndarray, f: np.ndarray) -> float:
    """Scatter Index (SI) = RMSE / mean(|obs|) × 100 [%].

    배열이 비어 있거나 obs 평균이 0이면 NaN 반환.
    """
    if o.size == 0:
        return float("nan")
    rmse = float(np.sqrt(np.mean((f - o) ** 2)))
    mean_obs = float(np.mean(np.abs(o)))
    if mean_obs == 0.0:
        return float("nan")
    return rmse / mean_obs * 100.0


def _ols(o: np.ndarray, f: np.ndarray):
    """OLS 직선 계수 (slope, intercept) 반환. 점이 2개 미만이면 None."""
    if o.size < 2:
        return None
    coeffs = np.polyfit(o, f, 1)
    return float(coeffs[0]), float(coeffs[1])


# ---------------------------------------------------------------------------
# 공개 API
# ---------------------------------------------------------------------------

def scatter_si(
    o: Union[np.ndarray, list],
    f: Union[np.ndarray, list],
    out_png: Union[str, Path],
    units: str = "",
) -> str:
    """관측(o) vs 예보(f) 산점도: 1:1선 + OLS 직선 + SI 텍스트.

    Parameters
    ----------
    o        : 관측값 배열 (NaN 허용)
    f        : 예보/모델값 배열 (NaN 허용)
    out_png  : 저장할 PNG 경로
    units    : 축 레이블에 붙일 단위 문자열 (예: "m", "s")

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — 이 그림은 참고용 advisory 산점도다.
    관측값은 truth 가 아닌 reference 로 해석하라.
    단일 그림만으로 모델 성능을 결론짓지 마라.
    실데이터 적용 시 이상치·기기 오류·시공간 매칭 오차를 점검하라.
    """
    o_arr, f_arr = _finite_pair(o, f)
    out_png = str(out_png)

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.scatter(o_arr, f_arr, s=18, alpha=0.6, color="#2c7bb6", label="data")

    # 1:1 기준선
    if o_arr.size > 0:
        lims = [
            min(o_arr.min(), f_arr.min()),
            max(o_arr.max(), f_arr.max()),
        ]
        ax.plot(lims, lims, "k--", lw=1.0, label="1:1")

    # OLS 회귀선
    ols = _ols(o_arr, f_arr)
    if ols is not None:
        slope, intercept = ols
        x_fit = np.linspace(o_arr.min(), o_arr.max(), 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, "r-", lw=1.2,
                label=f"OLS  y={slope:.2f}x+{intercept:.2f}")

    # SI 텍스트
    si = _scatter_index(o_arr, f_arr)
    si_txt = f"SI={si:.1f}%" if np.isfinite(si) else "SI=N/A"
    n_txt = f"n={o_arr.size}"
    ax.text(0.05, 0.92, f"{si_txt}  {n_txt}",
            transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

    unit_label = f" [{units}]" if units else ""
    ax.set_xlabel(f"Observation{unit_label}")
    ax.set_ylabel(f"Forecast{unit_label}")
    ax.set_title("Scatter (advisory — reference≠truth)")
    ax.legend(fontsize=8)
    ax.set_aspect("equal", "box")

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
    return os.path.abspath(out_png)


def timeseries_overlay(
    t,
    o: Union[np.ndarray, list],
    f: Union[np.ndarray, list],
    out_png: Union[str, Path],
) -> str:
    """관측·예보 시계열 오버레이 그림.

    Parameters
    ----------
    t        : 시간 축 (datetime-like 또는 숫자 배열)
    o        : 관측값 배열 (NaN 허용)
    f        : 예보/모델값 배열 (NaN 허용)
    out_png  : 저장할 PNG 경로

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — advisory 시계열 비교다.
    관측값은 reference 로 해석하라(truth 아님).
    단일 변수·단일 지점 시계열만으로 모델 성능을 결론짓지 마라.
    """
    o_arr = np.asarray(o, dtype=float)
    f_arr = np.asarray(f, dtype=float)
    out_png = str(out_png)

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(t, o_arr, "o-", lw=1.2, ms=4, color="#d7191c", label="Observation")
    ax.plot(t, f_arr, "s--", lw=1.2, ms=4, color="#2c7bb6", label="Forecast")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title("Time-series overlay (advisory — reference≠truth)")
    ax.legend(fontsize=8)
    fig.autofmt_xdate()
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
    return os.path.abspath(out_png)


def diff_map(
    lat: Union[np.ndarray, list],
    lon: Union[np.ndarray, list],
    diff: Union[np.ndarray, list],
    out_png: Union[str, Path],
    units: str = "",
    title: str = "Forecast − Observation bias map",
) -> str:
    """격자 또는 점 위치에서의 (예보 − 관측) 편차 맵.

    산점도 기반(cartopy 없이 동작). 실데이터에선 배경지도·투영법을 추가하라.

    Parameters
    ----------
    lat      : 위도 배열
    lon      : 경도 배열
    diff     : 예보 − 관측 편차 배열 (NaN 허용)
    out_png  : 저장할 PNG 경로
    units    : 컬러바 레이블에 붙일 단위
    title    : 그림 제목

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — advisory 편차 분포 참고도다.
    배경 해안선 없음(실데이터 적용 시 cartopy 또는 basemap 추가 권장).
    관측 위치는 reference 이며 truth 아님.
    단일 그림만으로 모델 성능을 결론짓지 마라.
    """
    lat_arr = np.asarray(lat, dtype=float).ravel()
    lon_arr = np.asarray(lon, dtype=float).ravel()
    diff_arr = np.asarray(diff, dtype=float).ravel()
    out_png = str(out_png)

    mask = np.isfinite(lat_arr) & np.isfinite(lon_arr) & np.isfinite(diff_arr)
    lat_c, lon_c, dv = lat_arr[mask], lon_arr[mask], diff_arr[mask]

    fig, ax = plt.subplots(figsize=(6, 5))
    vmax = float(np.nanmax(np.abs(dv))) if dv.size > 0 else 1.0
    sc = ax.scatter(lon_c, lat_c, c=dv, cmap="RdBu_r",
                    vmin=-vmax, vmax=vmax, s=30, alpha=0.8)
    cbar = fig.colorbar(sc, ax=ax, pad=0.02)
    unit_label = f" [{units}]" if units else ""
    cbar.set_label(f"Bias (F−O){unit_label}", fontsize=9)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"{title}\n(advisory — reference≠truth, no basemap)")
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
    return os.path.abspath(out_png)
