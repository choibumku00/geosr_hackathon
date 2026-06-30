# Recipe: 파랑 검증 (Wave Model Validation)

> **SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.**
> 이 문서는 "대략적 흐름 + 출발점 템플릿"이다. 완비된 코드가 아니며,
> 실 데이터(WW3 출력·부이 CSV 등)의 변수명·단위·격자 위상에 따라
> 각 단계를 반드시 수정해서 사용한다.

---

## 빠른 참조 (Quick Reference)

| 단계 | 핵심 함수 | 주요 Figure |
|------|-----------|-------------|
| A. 전처리 | `open_nc`, `Dataset.latlon()`, `Dataset.coord_kind()` | — |
| B. 정확도 | `metrics_accuracy(obs, mdl)` | Fig 01 Scatter · Fig 02 Bias map |
| C. 분포 | `metrics_distribution(obs, mdl)` | Fig 03 QQ · Fig 04 Perkins Hist |
| D. 시계열 | `plot_timeseries(obs, mdl, t)` | Fig 05 Overlay · Fig 06 Lag-corr |
| E. 방향 | `metrics_directional(dir_obs, dir_mdl)` | Fig 07 Rose overlay |
| F. 종합 | `plot_taylor(stats)`, `plot_target(stats)` | Fig 08 Taylor · Fig 09 Target |
| G. 해역 crop | `crop_region(ds, bbox)` | Fig 10 Region mask |

---

## §A 전처리 (Preprocessing)

### A-1 부이 CSV 읽기 (cp949 + 한글 컬럼 alias)

```python
# SAMPLE — 실데이터 컬럼명·결측 기호를 반드시 점검하라.
import pandas as pd

# cp949(EUC-KR) 인코딩이 흔함; utf-8-sig 도 존재
df = pd.read_csv("buoy_obs.csv", encoding="cp949", na_values=["-", "999", "9999"])

# 한글 컬럼 → 영문 alias (실데이터 헤더에 맞춰 수정)
ALIAS = {
    "일시":       "datetime",
    "지점":       "station_id",
    "유의파고(m)": "hs_obs",   # 컬럼명에 단위가 붙는 경우
    "파주기(sec)": "tp_obs",   # ← §G 주의: T01·Tp·Te 정의 불일치
    "파향(deg)":   "mwd_obs",
    "수온(°C)":    "sst_obs",
    "풍속(m/s)":   "wspd_obs",
    "풍향(deg)":   "wdir_obs",
}
df = df.rename(columns={k: v for k, v in ALIAS.items() if k in df.columns})
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.set_index("datetime")
```

### A-2 모델 NetCDF 열기 (mesh 또는 격자)

```python
# scripts/dataset.py: open_nc() — 한글 경로 우회(h5netcdf/scipy 폴백) 내장
from dataset import open_nc, Dataset
from io_detect import open_dataset
from router import detect_domain

xr_ds = open_nc("ww3_output.nc")          # 한글 경로 안전
d = Dataset(xr_ds, source="ww3", fmt="netcdf4")

# 도메인 확인 (waves / meteorology / ...)
dom = detect_domain(d)  # {"domain": "waves", "confidence": 0.75, "matched": {...}}

# 좌표 위상 확인 — SAMPLE
kind = d.coord_kind()   # "1d" | "2d" | "none"
ll   = d.latlon()       # (lat_name, lon_name, is_2d) | None
shape = d.grid_shape()  # (ny, nx) or (nlat, nlon)
```

### A-3 비정형 Mesh → 점 매칭 (Nearest-node Matchup)

```python
# SAMPLE — mesh 위상은 모델마다 다름; latitude/longitude 가 coord가 아닌
# data variable 일 수 있음 (synth_waves.ww3_mesh_like() 참조).
import numpy as np

# 노드 좌표 (mesh 의 경우 xr.Dataset 안 data variable)
lon_node = xr_ds["longitude"].values   # shape (N_NODE,)
lat_node = xr_ds["latitude"].values    # shape (N_NODE,)

def nearest_node(lon_q, lat_q, lon_grid, lat_grid):
    """부이 위치(lon_q, lat_q)에 가장 가까운 노드 인덱스."""
    dist = (lon_grid - lon_q)**2 + (lat_grid - lat_q)**2
    return int(np.argmin(dist))

# 부이별 가장 가까운 노드 추출
buoy_lons = {"부산_B01": 129.04, "거제_B02": 128.69, "여수_B03": 127.76}
buoy_lats = {"부산_B01": 35.06, "거제_B02": 34.87, "여수_B03": 34.74}

nodes = {stn: nearest_node(buoy_lons[stn], buoy_lats[stn], lon_node, lat_node)
         for stn in buoy_lons}

# hs 시계열 추출 (time × node)
hs_model = xr_ds["hs"].values   # shape (N_TIME, N_NODE)
hs_at_buoy = {stn: hs_model[:, idx] for stn, idx in nodes.items()}
```

> **실데이터 점검 항목**
> - `latitude`·`longitude` 가 coord 인지 data_var 인지 확인
> - 노드 좌표 범위·단위(degrees vs radians) 확인
> - 최근접 거리가 허용 범위(예: 0.1°) 이내인지 확인
> - 시간 축 일치 여부(UTC vs KST 오프셋 +9h)

---

## §B 정확도 검증 (Accuracy Metrics)

Figure 카탈로그: **Fig 01 Scatter**, **Fig 02 Bias/RMSE Map**

```python
# SAMPLE metrics_accuracy — 실데이터에선 NaN 처리·단위 통일 먼저 점검
import numpy as np

def metrics_accuracy(obs: np.ndarray, mdl: np.ndarray) -> dict:
    """
    Hs 정확도 지표.
    obs, mdl : 동일 shape의 float 배열 (NaN 포함 가능)
    반환: bias, rmse, si(Scatter Index), r(Pearson), slope(회귀)
    """
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    n = len(o)
    if n < 2:
        return {"n": n, "bias": np.nan, "rmse": np.nan,
                "si": np.nan, "r": np.nan, "slope": np.nan}
    bias  = float(np.mean(m - o))
    rmse  = float(np.sqrt(np.mean((m - o)**2)))
    si    = rmse / float(np.mean(o)) if np.mean(o) > 0 else np.nan
    r     = float(np.corrcoef(o, m)[0, 1])
    # 최소제곱 회귀 기울기
    slope = float(np.polyfit(o, m, 1)[0])
    return {"n": n, "bias": bias, "rmse": rmse, "si": si, "r": r, "slope": slope}

# 사용 예
stats = metrics_accuracy(df["hs_obs"].values, hs_at_buoy["부산_B01"])
print(f"Bias={stats['bias']:.3f}m  RMSE={stats['rmse']:.3f}m  SI={stats['si']:.3f}  r={stats['r']:.3f}")
```

### 지표 해석 기준 (참고값 — 도메인마다 다름)

| 지표 | 양호 | 주의 | 불량 |
|------|------|------|------|
| Bias (m) | |·| < 0.1 | 0.1–0.3 | > 0.3 |
| RMSE (m) | < 0.3 | 0.3–0.6 | > 0.6 |
| SI | < 0.3 | 0.3–0.5 | > 0.5 |
| r | > 0.95 | 0.85–0.95 | < 0.85 |
| slope | 0.9–1.1 | 0.8–1.2 | < 0.8 or > 1.2 |

---

## §C 분포 검증 (Distribution Validation)

Figure 카탈로그: **Fig 03 QQ Plot**, **Fig 04 Perkins Skill Score Histogram**

```python
# SAMPLE metrics_distribution — 실데이터 분포 꼬리 처리 점검
import numpy as np

def metrics_distribution(obs: np.ndarray, mdl: np.ndarray,
                          bins: np.ndarray | None = None) -> dict:
    """
    QQ quantile 배열과 Perkins Skill Score 반환.
    Perkins SS = sum(min(obs_pdf_i, mdl_pdf_i)) * dbin
    """
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]

    # QQ (quantile-quantile)
    pcts = np.linspace(0, 100, 101)
    qq_obs = np.percentile(o, pcts)
    qq_mdl = np.percentile(m, pcts)

    # Perkins Skill Score
    if bins is None:
        lo, hi = min(o.min(), m.min()), max(o.max(), m.max())
        bins = np.linspace(lo, hi, 30)
    dbin = float(bins[1] - bins[0])
    hist_o, _ = np.histogram(o, bins=bins, density=True)
    hist_m, _ = np.histogram(m, bins=bins, density=True)
    pss = float(np.sum(np.minimum(hist_o, hist_m)) * dbin)

    return {"qq_obs": qq_obs, "qq_mdl": qq_mdl, "perkins_ss": pss}

def plot_qq(qq_obs, qq_mdl, title="QQ Plot: Model vs Obs Hs"):
    """Fig 03 QQ Plot — SAMPLE."""
    # matplotlib 필요; 실데이터에선 축 범위·단위 확인
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(qq_obs, qq_mdl, "o", ms=4, alpha=0.7)
        lim = (0, max(qq_obs.max(), qq_mdl.max()) * 1.05)
        ax.plot(lim, lim, "k--", lw=0.8, label="1:1")
        ax.set(xlabel="Obs quantile (m)", ylabel="Model quantile (m)", title=title,
               xlim=lim, ylim=lim)
        ax.legend(); ax.grid(True, alpha=0.3)
        return fig
    except ImportError:
        return None   # no-crash
```

---

## §D 시계열·시간 검증 (Temporal Validation)

Figure 카탈로그: **Fig 05 Time-series Overlay**, **Fig 06 Lag Correlation**

```python
# SAMPLE plot_timeseries — 실데이터 시간 인덱스 UTC/KST 확인 필수
def plot_timeseries(t_obs, hs_obs, t_mdl, hs_mdl,
                    station="", title=None):
    """
    Fig 05 — 관측(obs) vs 모델(mdl) 유의파고 시계열 중첩.
    t_obs·t_mdl: datetime-like array
    """
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(t_obs, hs_obs, "k-o", ms=4, label="Obs Hs")
        ax.plot(t_mdl, hs_mdl, "r--",       label="Model Hs")
        ax.set(ylabel="Hs (m)", title=title or f"Hs Time Series — {station}")
        ax.legend(); ax.grid(True, alpha=0.3)
        return fig
    except ImportError:
        return None

def lag_correlation(obs: np.ndarray, mdl: np.ndarray,
                    max_lag: int = 12) -> dict:
    """
    Fig 06 — lag 별 상관계수 (시간 지연 검출용).
    max_lag: 시간 단위 (3h 간격 데이터라면 max_lag=12 → ±36h)
    """
    import numpy as np
    lags, corrs = [], []
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            r = np.corrcoef(o[-lag:], m[:lag])[0, 1] if -lag < len(o) else np.nan
        elif lag > 0:
            r = np.corrcoef(o[:-lag], m[lag:])[0, 1] if lag < len(o) else np.nan
        else:
            r = np.corrcoef(o, m)[0, 1]
        lags.append(lag); corrs.append(float(r))
    best = lags[int(np.argmax(corrs))]
    return {"lags": lags, "corrs": corrs, "best_lag": best}
```

---

## §E 방향 원형통계 (Directional / Circular Statistics)

Figure 카탈로그: **Fig 07 MWD Rose Overlay**

```python
# SAMPLE metrics_directional — 방향은 0°=360° 순환 주의
import numpy as np

def metrics_directional(dir_obs: np.ndarray, dir_mdl: np.ndarray,
                         deg: bool = True) -> dict:
    """
    원형 통계(Circular Statistics) — 파향(MWD)·풍향 검증.
    반환: mean_dir_obs, mean_dir_mdl, circ_bias, circ_rmse
    """
    mask = np.isfinite(dir_obs) & np.isfinite(dir_mdl)
    o, m = dir_obs[mask], dir_mdl[mask]
    if deg:
        o, m = np.deg2rad(o), np.deg2rad(m)

    # 원형 평균
    mean_obs = float(np.arctan2(np.mean(np.sin(o)), np.mean(np.cos(o))))
    mean_mdl = float(np.arctan2(np.mean(np.sin(m)), np.mean(np.cos(m))))

    # 원형 편차 (−π, π] 로 래핑
    diff = m - o
    diff = (diff + np.pi) % (2 * np.pi) - np.pi
    circ_bias = float(np.mean(diff))
    circ_rmse = float(np.sqrt(np.mean(diff**2)))

    if deg:
        mean_obs  = np.rad2deg(mean_obs) % 360
        mean_mdl  = np.rad2deg(mean_mdl) % 360
        circ_bias = np.rad2deg(circ_bias)
        circ_rmse = np.rad2deg(circ_rmse)

    return {
        "mean_dir_obs": mean_obs, "mean_dir_mdl": mean_mdl,
        "circ_bias_deg": circ_bias, "circ_rmse_deg": circ_rmse,
    }
```

> **파향(MWD) 주의사항**
> - 기상학적 방향(바람이 오는 방향) vs 해양학적 방향(파가 나아가는 방향) 혼동 주의
> - 모델·관측이 같은 규약인지 반드시 확인 (→ §G 참조)

---

## §F 종합 검증 (Taylor Diagram & Target Diagram)

Figure 카탈로그: **Fig 08 Taylor Diagram**, **Fig 09 Target Diagram**

```python
# SAMPLE plot_taylor — 여러 지점/변수를 한 그래프에 비교
import numpy as np

def taylor_stats(obs: np.ndarray, mdl: np.ndarray) -> dict:
    """Taylor 통계량: σ_ref, σ_test, r, centered RMSE."""
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    sig_o  = float(np.std(o))
    sig_m  = float(np.std(m))
    r      = float(np.corrcoef(o, m)[0, 1])
    crmse  = float(np.sqrt(sig_o**2 + sig_m**2 - 2 * sig_o * sig_m * r))
    return {"sigma_ref": sig_o, "sigma_test": sig_m, "r": r, "crmse": crmse}

def target_stats(obs: np.ndarray, mdl: np.ndarray) -> dict:
    """Target Diagram 통계량: bias, uRMSE (signed)."""
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    bias   = float(np.mean(m - o))
    rmse   = float(np.sqrt(np.mean((m - o)**2)))
    urmse2 = max(rmse**2 - bias**2, 0.0)
    sign   = 1.0 if np.std(m) >= np.std(o) else -1.0
    urmse  = sign * float(np.sqrt(urmse2))
    return {"bias_norm": bias / np.std(o), "urmse_norm": urmse / np.std(o)}

# Taylor · Target 는 matplotlib polar axes 로 그리는 것이 일반적.
# 실데이터에서 여러 지점/시기를 한 그림에 겹쳐 도메인 특성 파악.
```

---

## §G 해역 Crop (Region Masking)

Figure 카탈로그: **Fig 10 Region Mask**

```python
# SAMPLE crop_region — mesh 자료는 MAPSTA 마스크도 함께 적용
import numpy as np

def crop_region(lon: np.ndarray, lat: np.ndarray,
                bbox: tuple) -> np.ndarray:
    """
    bbox = (lon_min, lon_max, lat_min, lat_max)
    반환: bool mask (True = 유효 노드 / 격자)
    """
    lon_min, lon_max, lat_min, lat_max = bbox
    mask = (
        (lon >= lon_min) & (lon <= lon_max) &
        (lat >= lat_min) & (lat <= lat_max)
    )
    return mask

# 사용 예 — 동해·남해·황해 분리 검증
BBOX_EAST_SEA  = (129.0, 132.0, 34.0, 38.5)
BBOX_SOUTH_SEA = (126.0, 130.5, 33.0, 35.5)
BBOX_YELLOW_SEA = (124.0, 127.5, 33.5, 38.5)

region_mask = crop_region(lon_node, lat_node, BBOX_EAST_SEA)
# MAPSTA 마스크 추가 (0=육지/제외)
if "MAPSTA" in xr_ds:
    mapsta_mask = xr_ds["MAPSTA"].values.astype(bool)
    region_mask = region_mask & mapsta_mask
```

---

## §H 함정 및 주의사항 (Pitfalls)

### H-1 파주기 정의 불일치 (Period Definition Mismatch)

> **가장 흔한 오류**: 모델 T01 ≠ 부이 Tp (Peak period)

| 기호 | 정의 | 출처 예 |
|------|------|---------|
| T01  | 0차·1차 모멘트 비 (m0/m1) | WW3 기본 출력 |
| Te   | 에너지 평균 주기 (m-1/m0) | ECWAM, ERA5 |
| Tp   | 피크 주기 (최대 에너지 주파수의 역수) | 부이 직접 계산 |
| Tm02 | 0차·2차 모멘트 비 (sqrt(m0/m2)) | NEMO 등 |

- 같은 해상 조건에서 T01 < Te < Tp 관계가 성립하는 경우가 많음
- 비교 전 양쪽 정의를 반드시 문서(NETCDF global attrs, 부이 메타) 로 확인
- 변환 공식(경험식)을 쓸 경우 그 가정과 한계를 명시

### H-2 대표성 오차 (Representativeness Error)

- 부이 점관측 vs 모델 격자 평균 → **스케일 불일치**
- 특히 천해·연안: 격자 해상도(~1–5 km)가 수심 변화를 평활화
- 최근접 노드 거리 > 0.1° 이면 비교 품질 저하 가능 → 로그에 거리 기록
- 해결책(참고): 복수 노드 보간, 격자 내 분산 보정, 관측 반경 평균

### H-3 시간 축 불일치

- 부이 CSV 시각: KST(+09:00) 가 많음 → UTC 변환 필수
- WW3 출력: 보통 UTC. 불확실하면 `global_attrs["time_zone"]` 확인
- 스텝 정렬: pd.merge_asof / xr.interp 사용 시 허용 오차(tolerance) 명시

### H-4 단위 오류

- 파향(dir): 일부 WW3 출력은 기상학 방향(coming-from), 일부는 going-to
- 풍속: 10m 기준인지 확인; 실측 센서 높이 보정 필요 시 멱함수(power law) 사용
- 주기: 단위 's' 가 맞는지 확인 (혼동 없지만 단위 속성 결측 주의)

---

## §I Figure 카탈로그 전체 (Figures Catalog)

| Fig # | 이름 | 축(X → Y) | 함수 | 비고 |
|--------|------|-----------|------|------|
| **01** | Scatter Hs | Obs → Model | `plot_scatter(obs, mdl)` | 1:1 선·컬러 밀도 |
| **02** | Bias Map | 위경도 → bias | `plot_map(lon, lat, bias)` | 공간 분포 |
| **03** | QQ Plot | Obs quantile → Model quantile | `plot_qq(qq_obs, qq_mdl)` | [§C] |
| **04** | Perkins Hist | Hs bin → PDF | `plot_hist_perkins(o, m)` | [§C] |
| **05** | Timeseries Overlay | Datetime → Hs | `plot_timeseries(...)` | [§D] |
| **06** | Lag Correlation | Lag (h) → r | `plot_lag_corr(lags, corrs)` | [§D] |
| **07** | MWD Rose Overlay | 방향 → 빈도 | `plot_rose_overlay(o, m)` | [§E] |
| **08** | Taylor Diagram | σ·r 극좌표 | `plot_taylor(stats_list)` | [§F] |
| **09** | Target Diagram | uRMSE → Bias | `plot_target(stats_list)` | [§F] |
| **10** | Region Mask | 위경도 지도 | `plot_map_mask(lon, lat, mask)` | [§G] |
| **11** | RMSE Map | 위경도 → RMSE | `plot_map(lon, lat, rmse)` | 공간 분포 |
| **12** | SI Map | 위경도 → SI | `plot_map(lon, lat, si)` | 공간 분포 |
| **13** | r Map | 위경도 → r | `plot_map(lon, lat, r)` | 공간 분포 |
| **14** | Hs PDF by Season | Hs bin → PDF | `plot_hist_season(o, m)` | 계절별 |
| **15** | Scatter by Direction | Dir sector → Hs | `plot_scatter_dir(...)` | 해역별 방향 분류 |
| **16** | Period Scatter | Obs Tp → Model T01 | `plot_scatter(tp_obs, t01_mdl)` | §H-1 불일치 |
| **17** | Wind Speed Scatter | Obs wspd → Model | `plot_scatter(ws_obs, ws_mdl)` | 바람 검증 |
| **18** | Multi-station Table | 지점 × 지표 | `render_table(stats_dict)` | 보고서 요약 |

> Fig 08 Taylor · Fig 18 Multi-station Table 은 최종 보고서에서 항상 포함 권장.

---

## 연관 모듈 참조

| 모듈 | 핵심 인터페이스 | 역할 |
|------|----------------|------|
| `scripts/dataset.py` | `open_nc`, `Dataset` | NetCDF 로딩·좌표 추상화 |
| `scripts/io_detect.py` | `open_dataset`, `detect_format` | 포맷 자동 판별(nc/csv/…) |
| `scripts/router.py` | `detect_domain` | 도메인 분류(waves/met/…) |
| `scripts/qc.py` | `run_qc`, `check_variable` | 층위1 QC(범위·결측·격자·시간) |
| `scripts/report.py` | `write_report`, `render_markdown` | QC 리포트 생성 |
| `tests/synth_waves.py` | `ww3_mesh_like`, `buoy_obs_like` | 합성 fixture (테스트·개발용) |
| `config/domains.yaml` | waves 도메인 규칙 | hs 표준명·이름 패턴 |

---

*SAMPLE — 도메인 맞춤 적응 없이 그대로 운용 금지. 실 데이터 구조 점검 후 수정.*
