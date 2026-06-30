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

    # x축: matplotlib DatetimeConverter 가 numpy datetime64 를 받으면
    # 내부 _dt64_to_ordinalf 에서 np.datetime64('NaT').astype(np.int64) 를 호출해
    # DeprecationWarning(generic unit) 을 발생시킨다.
    # 이를 피하기 위해 수치 인덱스를 x축으로 쓰고 tick 레이블을 날짜 문자열로 지정한다.
    t_arr = np.asarray(t)
    t_is_dt64 = t_arr.dtype.kind == "M"
    x_vals = np.arange(len(t_arr))

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(x_vals, o_arr, "o-", lw=1.2, ms=4, color="#d7191c", label="Observation")
    ax.plot(x_vals, f_arr, "s--", lw=1.2, ms=4, color="#2c7bb6", label="Forecast")

    # tick 레이블: datetime64 이면 날짜 문자열, 아니면 원 값
    if t_is_dt64 and len(t_arr) > 0:
        step = max(1, len(t_arr) // 6)
        tick_pos = x_vals[::step]
        tick_lab = [str(t_arr[i])[:16].replace("T", " ") for i in range(0, len(t_arr), step)]
        ax.set_xticks(tick_pos)
        ax.set_xticklabels(tick_lab, rotation=30, ha="right", fontsize=8)
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
    """격자(2D) 또는 점(1D) 위치에서의 (예보 − 관측) 편차 발산 맵.

    2D 배열이면 pcolormesh 발산 맵, 1D·점 배열이면 scatter 맵.
    cartopy 없이 동작. 실데이터에선 배경지도·투영법을 추가하라.

    Parameters
    ----------
    lat      : 위도 배열 (2D 격자 또는 1D 점)
    lon      : 경도 배열 (2D 격자 또는 1D 점)
    diff     : 예보 − 관측 편차 배열 (NaN 허용; lat/lon 과 같은 형상)
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
    lat_arr = np.asarray(lat, dtype=float)
    lon_arr = np.asarray(lon, dtype=float)
    diff_arr = np.asarray(diff, dtype=float)
    out_png = str(out_png)
    unit_label = f" [{units}]" if units else ""

    fig, ax = plt.subplots(figsize=(6, 5))

    if lat_arr.ndim == 2 and lon_arr.ndim == 2 and diff_arr.ndim == 2:
        # pcolormesh — 2D 격자
        fin_vals = diff_arr[np.isfinite(diff_arr)]
        vmax = float(np.max(np.abs(fin_vals))) if fin_vals.size > 0 else 1.0
        diff_masked = np.ma.masked_invalid(diff_arr)
        sc = ax.pcolormesh(lon_arr, lat_arr, diff_masked, cmap="RdBu_r",
                           vmin=-vmax, vmax=vmax, shading="auto")
    else:
        # scatter — 1D 점
        lat_r = lat_arr.ravel()
        lon_r = lon_arr.ravel()
        diff_r = diff_arr.ravel()
        mask = np.isfinite(lat_r) & np.isfinite(lon_r) & np.isfinite(diff_r)
        lat_c, lon_c, dv = lat_r[mask], lon_r[mask], diff_r[mask]
        vmax = float(np.nanmax(np.abs(dv))) if dv.size > 0 else 1.0
        sc = ax.scatter(lon_c, lat_c, c=dv, cmap="RdBu_r",
                        vmin=-vmax, vmax=vmax, s=30, alpha=0.8)

    cbar = fig.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label(f"Bias (F−O){unit_label}", fontsize=9)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"{title}\n(advisory — reference≠truth, no basemap)")
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
    return os.path.abspath(out_png)


# ---------------------------------------------------------------------------
# Q-Q 그림
# ---------------------------------------------------------------------------

def qq_plot(
    o: Union[np.ndarray, list],
    f: Union[np.ndarray, list],
    out_png: Union[str, Path],
) -> str:
    """Q-Q 그림: 관측(o)·예보(f) 분위수 산점도 + 1:1선.

    두 배열의 유효값(NaN 제외)을 독립적으로 정렬하여 분위수를 비교한다.

    Parameters
    ----------
    o        : 관측값 배열 (NaN 허용)
    f        : 예보/모델값 배열 (NaN 허용)
    out_png  : 저장할 PNG 경로

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — advisory 분위수 비교도다.
    관측값은 reference 로 해석하라(truth 아님).
    표본 크기 차이가 크면 분위수 보간 오차가 생긴다. 실데이터에서 확인하라.
    단일 그림만으로 모델 분포 특성을 결론짓지 마라.
    """
    o_clean = np.asarray(o, dtype=float).ravel()
    f_clean = np.asarray(f, dtype=float).ravel()
    o_clean = o_clean[np.isfinite(o_clean)]
    f_clean = f_clean[np.isfinite(f_clean)]
    out_png = str(out_png)

    fig, ax = plt.subplots(figsize=(5, 5))

    if o_clean.size > 0 and f_clean.size > 0:
        n_q = min(o_clean.size, f_clean.size, 200)
        probs = np.linspace(0.0, 1.0, n_q)
        o_q = np.quantile(o_clean, probs)
        f_q = np.quantile(f_clean, probs)

        ax.scatter(o_q, f_q, s=18, alpha=0.7, color="#2c7bb6", label="Quantiles")

        lo = min(float(o_q.min()), float(f_q.min()))
        hi = max(float(o_q.max()), float(f_q.max()))
        ax.plot([lo, hi], [lo, hi], "k--", lw=1.0, label="1:1")

        ax.text(
            0.05, 0.93,
            f"n(obs)={o_clean.size}  n(fct)={f_clean.size}",
            transform=ax.transAxes, fontsize=8,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7),
        )
        ax.legend(fontsize=8)
    else:
        ax.text(0.5, 0.5, "No valid data", transform=ax.transAxes,
                ha="center", va="center", fontsize=10, color="gray")

    ax.set_xlabel("Observation quantiles")
    ax.set_ylabel("Forecast quantiles")
    ax.set_title("Q-Q Plot (advisory — reference≠truth)")
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
    return os.path.abspath(out_png)


# ---------------------------------------------------------------------------
# Taylor 다이어그램
# ---------------------------------------------------------------------------

def taylor_diagram(
    o: Union[np.ndarray, list],
    f: Union[np.ndarray, list],
    out_png: Union[str, Path],
) -> str:
    """Taylor 다이어그램: 표준편차 비·상관·CRMSD 한 점, 극좌표.

    극좌표: theta = arccos(R), r = sigma_f / sigma_o.
    참조점(관측)은 (theta=0, r=1).

    Parameters
    ----------
    o        : 관측값 배열 (NaN 허용)
    f        : 예보/모델값 배열 (NaN 허용)
    out_png  : 저장할 PNG 경로

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — advisory Taylor 다이어그램이다.
    표준편차 비(r)와 상관(theta)이 동시에 참조점에 가까울수록 패턴 일치가 좋음.
    CRMSD 점선은 참조점으로부터의 패턴 오차 크기다.
    단일 변수·단일 기간 결과만으로 모델 성능을 결론짓지 마라.
    """
    o_arr, f_arr = _finite_pair(o, f)
    out_png = str(out_png)

    n = o_arr.size
    std_ratio = corr = theta = crmsd = float("nan")
    if n >= 2:
        o_std = float(np.std(o_arr, ddof=0))
        f_std = float(np.std(f_arr, ddof=0))
        if o_std > 0.0:
            std_ratio = f_std / o_std
            corr = (
                float(np.corrcoef(o_arr, f_arr)[0, 1]) if f_std > 0.0 else 0.0
            )
            corr = float(np.clip(corr, -1.0, 1.0))
            theta = float(np.arccos(corr))          # [0, π]
            crmsd_sq = std_ratio**2 + 1.0 - 2.0 * std_ratio * corr
            crmsd = float(np.sqrt(max(crmsd_sq, 0.0)))

    r_max = max(2.0, (std_ratio * 1.3 if np.isfinite(std_ratio) else 2.0))

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="polar")

    # theta=0 East(오른쪽)=상관 1, theta=π/2 North(위)=상관 0
    # 음의 상관까지 보이도록 thetamax=180
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_rlim(0, r_max)
    ax.set_rlabel_position(90)

    # 상관 눈금 (theta 호)
    corr_ticks = [1.0, 0.99, 0.95, 0.9, 0.8, 0.7, 0.6, 0.4, 0.2, 0.0]
    theta_tick_deg = [float(np.degrees(np.arccos(c))) for c in corr_ticks]
    ax.set_thetagrids(
        theta_tick_deg,
        labels=[f"R={c:.2f}" for c in corr_ticks],
        fontsize=6,
    )

    # 표준편차 비 호선(배경 가이드)
    theta_arc = np.linspace(0.0, np.pi, 120)
    for r_std in [0.5, 1.0, 1.5, 2.0]:
        if r_std <= r_max:
            ax.plot(theta_arc, np.full_like(theta_arc, r_std),
                    "--", color="lightgray", lw=0.8)

    # CRMSD 원: Cartesian (1,0) 중심 → 극좌표 변환, 상반면만
    if np.isfinite(crmsd) and crmsd > 0.0:
        phi = np.linspace(0.0, np.pi, 300)
        cx = 1.0 + crmsd * np.cos(phi)
        cy = crmsd * np.sin(phi)
        r_circ = np.sqrt(cx**2 + cy**2)
        t_circ = np.arctan2(cy, cx)
        vis = (t_circ >= 0) & (t_circ <= np.pi) & (r_circ <= r_max * 1.05)
        if vis.any():
            ax.plot(t_circ[vis], r_circ[vis], ":", color="steelblue", lw=1.2,
                    label=f"CRMSD={crmsd:.3f}")

    # 참조점 (관측)
    ax.plot(0.0, 1.0, "k*", ms=14, zorder=6, label="Reference (obs)")

    # 모델점
    if np.isfinite(theta) and np.isfinite(std_ratio):
        ax.plot(theta, std_ratio, "ro", ms=10, zorder=6,
                label=f"Model  R={corr:.3f}  σ*={std_ratio:.3f}")

    ax.set_title(
        f"Taylor Diagram  n={n}\n(advisory — reference≠truth)",
        fontsize=9,
    )
    ax.legend(fontsize=7, loc="lower left", bbox_to_anchor=(0.0, -0.18))

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return os.path.abspath(out_png)


# ---------------------------------------------------------------------------
# 파향 로즈
# ---------------------------------------------------------------------------

def wave_rose(
    direction_deg: Union[np.ndarray, list],
    magnitude: Union[np.ndarray, list],
    out_png: Union[str, Path],
) -> str:
    """파향 로즈: 방향 히스토그램 극좌표(크기 4분위로 채색).

    Parameters
    ----------
    direction_deg : 방향 배열 [0, 360) 도 단위 (NaN 허용)
    magnitude     : 크기 배열 (파고·풍속 등; NaN 허용)
    out_png       : 저장할 PNG 경로

    Returns
    -------
    str
        저장된 PNG 파일의 절대 경로

    Notes — §G Advisory Caption
    ---------------------------
    SAMPLE — advisory 파향 로즈다.
    관측 기기 보정·방향 기준(기상학/항해학)을 실데이터에서 확인하라.
    단일 기간·단일 지점 로즈만으로 해당 지역 기후를 결론짓지 마라.
    """
    dirs = np.asarray(direction_deg, dtype=float).ravel()
    mags = np.asarray(magnitude, dtype=float).ravel()
    mask = np.isfinite(dirs) & np.isfinite(mags)
    dirs, mags = dirs[mask], mags[mask]
    out_png = str(out_png)

    N_SECTORS = 16
    bin_centers_deg = np.linspace(0.0, 360.0, N_SECTORS, endpoint=False)
    theta = np.radians(bin_centers_deg)
    width = 2.0 * np.pi / N_SECTORS

    # 크기 4분위 경계
    if mags.size > 1:
        mag_levels = np.quantile(mags, [0.0, 0.25, 0.50, 0.75, 1.0])
    elif mags.size == 1:
        mag_levels = np.array([mags[0], mags[0], mags[0], mags[0], mags[0]])
    else:
        mag_levels = np.array([0.0, 0.25, 0.50, 0.75, 1.0])

    colors = ["#ffffb2", "#fecc5c", "#fd8d3c", "#e31a1c"]
    lv_labels = [
        f"{mag_levels[0]:.2f}–{mag_levels[1]:.2f}",
        f"{mag_levels[1]:.2f}–{mag_levels[2]:.2f}",
        f"{mag_levels[2]:.2f}–{mag_levels[3]:.2f}",
        f"{mag_levels[3]:.2f}–{mag_levels[4]:.2f}",
    ]

    total = max(len(dirs), 1)
    sector_idx = (np.floor(dirs % 360.0 / (360.0 / N_SECTORS)).astype(int)) % N_SECTORS

    freq = np.zeros((N_SECTORS, 4))
    for lv in range(4):
        lo, hi = mag_levels[lv], mag_levels[lv + 1]
        lv_mask = (mags >= lo) & (mags <= hi) if lv == 3 else (mags >= lo) & (mags < hi)
        for s in range(N_SECTORS):
            freq[s, lv] = float(np.sum(lv_mask & (sector_idx == s))) / total * 100.0

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    bottom = np.zeros(N_SECTORS)
    for lv in range(4):
        ax.bar(theta, freq[:, lv], width=width, bottom=bottom,
               color=colors[lv], alpha=0.85, label=lv_labels[lv],
               edgecolor="white", linewidth=0.4)
        bottom += freq[:, lv]

    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"], fontsize=8)
    ax.set_ylabel("Frequency [%]", labelpad=28, fontsize=8)
    ax.set_title(
        f"Wave Rose  n={len(dirs)}\n(advisory — reference≠truth)",
        fontsize=9,
    )
    ax.legend(title="Magnitude", fontsize=7, loc="lower left",
              bbox_to_anchor=(1.05, 0.0))

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    fig.savefig(out_png, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return os.path.abspath(out_png)
