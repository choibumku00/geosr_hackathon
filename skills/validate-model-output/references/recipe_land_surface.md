# Recipe: 육상(지표) 검증 (Land-Surface Model Validation)

> # ⚠️ SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> **이 스킬은 특정 분야 전용이 아니라 범용(generic)이다.** 이 파일은 그 범용 파이프라인을
> **육상(지표, land surface)** 이라는 *한 예시 도메인*에 적용해 본 worked SAMPLE일 뿐이다.
> 아래 코드는 "대략적 흐름 + 출발점 템플릿"이며, 완비된 프로덕션 코드가 아니다.
> 실제 데이터(ISMN 토양수분망 CSV·FLUXNET 타워·SMAP/SMOS L3·ERA5-Land/GLDAS NetCDF 등)의
> **변수명·단위·좌표 위상·시간대·품질플래그**에 따라 각 단계를 반드시 수정해서 쓴다.
>
> 대응 방법 카드: [`research/27_domain_land_surface.md`](research/27_domain_land_surface.md) ·
> 대응 그림 카드: [`research/figures/35_fig_land_surface.md`](research/figures/35_fig_land_surface.md)
>
> **§G 해석 원칙(항상 적용)**: ① 기준자료 ≠ 참값(ISMN·FLUXNET·위성·ERA5-Land 모두 reference이지 truth 아님) ·
> ② 점 관측 ≠ 격자 화소(대표성 오차 representativeness error) · ③ 해석 임계는 advisory(피복·계절·해상도 의존) ·
> ④ 단일 그림 금지(정확도+편향+분포/패턴 3축 최소) · ⑤ ★지도형 그림은 `add_basemap()`으로 해안선+위경도 필수.

---

## 대표 자료형 (Representative Data Forms)

이 레시피가 다루는 자료형은 **토양수분(soil moisture) 삼중대조(triple collocation)** 세팅이다:

| 축 | 자료 | 형태 | 예시 |
|----|------|------|------|
| in-situ [정점] | 관측망 점·시계열 | CSV/텍스트 | ISMN station θ (m³/m³), 심도 5·10·20 cm |
| 위성 [트랙/격자] | retrieval L3 | NetCDF 격자 | SMAP/SMOS/ASCAT 표층 θ |
| 모델/재분석 [격자] | 육상면 산출 | NetCDF 격자 | 우리 모델·ERA5-Land·GLDAS θ |

→ 열기 → 구조/메타 점검 → (정점이면) 매치업·시간대 정규화 → 다축 지표 → 그림 → 캡션(§G).
곁들여 **ET 에너지수지·SWE/SCA·LAI/GPP**를 도메인 특이 지표로 다룬다.

---

## 빠른 참조 (Quick Reference) — 단계 → 실제 스킬 함수 → 그림 카드

| 단계 | 실제 스킬 함수 (모듈.함수) | 대응 Figure 카드 (35_fig_land_surface) |
|------|--------------------------|----------------------------------------|
| A. 열기·포맷 판별 | `io_detect.open_dataset` · `io_detect.detect_format` · `dataset.open_nc` | — |
| A. 구조/메타/좌표 | `Dataset.latlon` · `Dataset.coord_kind` · `Dataset.grid_shape` · `Dataset.is_mesh` · `Dataset.variable` · `Dataset.time_info` | 카드14 관측소 위치 지도 |
| B. 정점 매치업·시간대 | `preprocess.match_points_to_mesh` · `preprocess.tz_to_utc` · `preprocess.common_time_index` · `preprocess.inject_point_coords` · `preprocess.build_pairs` | 카드14 station map |
| C. 정확도 지표 | `metrics_basic.bias` · `rmse` · `si` · `nrmse` · `mae` · `pearson_r` · `metrics_basic.linregress` | 카드1 시계열, [16 §A 산점] |
| D. 분포 | `metrics_distribution.qq_points` · `perkins_skill_score` · `ks_distance` · `quantiles` | 카드4 CDF, [16 QQ/PDF] |
| E. 종합(패턴) | `metrics_pattern.taylor_stats` · `target_stats` · `pattern_correlation` | [16 Taylor/Target] |
| F. 그림 | `plots.scatter_si` · `timeseries_overlay` · `qq_plot` · `taylor_diagram` · `diff_map` · **`plots.add_basemap`** | 카드1·3·6·9·13·14 |
| G. 지도 basemap (★) | `plots.add_basemap` · `plots._make_geo_axes` | 카드3·9·13·14 (해안선+위경도 필수) |
| H. 도메인 특이 지표 | numpy/scipy/xarray/pandas (+ 필요시 `pytesmo`·`xskillscore`, 실존만) | 카드2 TC · 카드6 EBR · 카드8 SWE · 카드9 SCA · 카드10 LAI |

> ⚠️ **인자 순서 주의(실제 시그니처)**: `metrics_basic.*`/`plots.scatter_si`/`plots.diff_map`은 **forecast 먼저, obs 나중** 규약이
> 함수마다 다르다 — `metrics_basic.bias(f, o)`는 `(f, o)`, `plots.scatter_si(o, f, ...)`는 `(o, f)`.
> 아래 코드에서 각 호출의 순서를 그대로 따르되, **네 데이터에 붙일 땐 docstring을 다시 확인**하라.

---

## §A 열기 · 구조/메타 점검 (Open & Inspect)

```python
# SAMPLE — scripts/ 를 import 경로에 넣고(플랫 모듈), 실데이터 경로로 바꿔라.
import sys, os
SKILL = os.environ.get("SKILL", os.getcwd())   # $SKILL = 스킬 설치 폴더(설치 위치/CLI 인자로 교체)
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import numpy as np
import pandas as pd
import xarray as xr

from io_detect import open_dataset, detect_format
from dataset import open_nc, Dataset

# --- 모델/재분석/위성 격자 열기 (한글 경로 안전: open_nc 내부 h5netcdf/scipy 폴백) ---
fmt = detect_format("era5land_swvl1.nc")      # 'netcdf4' | 'netcdf3' | 'csv' | 'unknown'
d   = open_dataset("era5land_swvl1.nc")        # -> Dataset 래퍼 (io_detect)

# --- 구조/좌표 위상 점검 (SAMPLE — 변수명은 데이터마다 다르다) ---
print(d.data_var_names())          # 예: ['swvl1'] (ERA5-Land 표층 토양수분) — 네 변수명 확인
kind  = d.coord_kind()             # '1d' | '2d' | 'mesh' | 'none'
ll    = d.latlon()                 # (lat_name, lon_name, is_2d) | None
shape = d.grid_shape()             # (nlat, nlon) 또는 (ny,nx) 또는 (n_nodes,)
tinfo = d.time_info()              # {'name','n_steps','start','end'} | None

# --- 변수 메타(단위·표준명) 점검: 토양수분 부피함수율 m³/m³ 인지 확인 ---
var = d.variable("swvl1")          # ← SAMPLE 변수명. Variable(name,dims,shape,units,standard_name,...)
print(var.units, var.standard_name)  # 예: 'm3 m-3', None  → 단위·표준명 결측이면 로그에 기록
# 이 줄은 SAMPLE — 네 데이터의 실제 토양수분 변수명/단위(m³/m³ vs %)·경도규약(0–360 vs −180…180)에 맞춰 바꿔라.
```

> **실데이터 점검 항목 (육상 특유)**
> - 토양수분 단위: 부피함수율 **m³/m³** 인가, %인가, kg/kg인가 → 통일 (→ 카드3 캡션)
> - **심도 정합**: 위성 표층(~0–5 cm) vs 관측 센서(5·10·20 cm) vs 모델 층 → 표층↔근권 혼용 금지 (27 토양층 정합 카드)
> - 경도 규약(0–360 → −180…180), 육지/해양/영구빙 마스크, 달력(gregorian/noleap)
> - 시간대: ISMN·타워 CSV는 현지시각(KST 등)일 수 있음 → UTC 정규화 필요 (§B)

---

## §B 정점 매치업 · 시간대 정규화 (Point Matchup & TZ)

ISMN 관측점을 모델/위성 격자(또는 mesh 노드)에 붙이고, 시각을 UTC로 맞춘다.

```python
# SAMPLE — ISMN CSV 컬럼명·인코딩·결측기호는 반드시 실데이터로 확인.
import preprocess as pp

# 1) 관측 CSV 읽기 (io_detect 가 utf-8→cp949→euc-kr→latin-1 폴백)
obs = open_dataset("ismn_station_ABC.csv").xr.to_dataframe()   # -> DataFrame
# 이 줄은 SAMPLE — ISMN 실헤더(예: 'soil_moisture','depth_from','network','station')에 맞춰 컬럼 rename 하라.

# 2) 시간대 → UTC (관측 현지시각 → UTC). 메타 없으면 assumed=True 경고.
t_utc, assumed = pp.tz_to_utc(obs["timestamp"].values, tz="UTC")   # ISMN 은 대개 UTC
if assumed:
    print("WARNING: TZ 미확인 — UTC 가정. ISMN 은 UTC지만 타워 CSV는 현지시각일 수 있음")

# 3) 정점 좌표 주입 → 격자/mesh 최근접 노드 매칭
#    격자면 lat/lon 을 meshgrid 로 펴서 cKDTree 최근접, mesh 면 그대로.
station_ids = ["ABC", "DEF"]
mapping = {"ABC": (37.5, 127.9), "DEF": (36.1, 128.2)}   # {id:(lat,lon)} — SAMPLE 좌표
lats, lons = pp.inject_point_coords(station_ids, mapping)

lat_g = d.xr[ll[0]].values; lon_g = d.xr[ll[1]].values   # 격자 좌표 (1D 가정)
LON, LAT = np.meshgrid(lon_g, lat_g)
idx, dist_km = pp.match_points_to_mesh(LON.ravel(), LAT.ravel(), lons, lats, max_km=25.0)
# idx==-1 은 max_km 초과(제외). 대표성 경고: dist_km 를 로그에 남겨라(§G-2).

# 4) 관측·모델 시각 교집합 (스텝 정렬)
mod_t = d.xr[tinfo["name"]].values
i_obs, i_mod = pp.common_time_index(t_utc, mod_t)

# 5) 롱포맷 쌍(선택) — station/time/model/obs
# pairs = pp.build_pairs(station_ids, mod_t[i_mod], model_TxS, obs_TxS, var_name="soil_moisture")
```

> **대표성 오차 경고 (육상 최대 함정, §G-2)**: 점 센서(수십 cm²) vs 격자(수 km) 지지면적 차이가 검증차의
> 상당부분일 수 있다. 최근접 거리가 크면(`dist_km`) "모델 나쁨"으로 단정 금지 — 로그에 거리·심도차를 남겨라.
> (온도 변수라면 `preprocess.to_kelvin(values, units)` 로 단위 정규화 — 토양수분엔 불필요.)

---

## §C 다축 정확도 지표 (Accuracy Metrics — 실제 함수)

토양수분은 **원자료 지표 + 이상(anomaly) 지표 + ubRMSD**를 병행한다(27 이상상관·ubRMSD 카드).

```python
# SAMPLE — 여기서부터 obs(관측), mdl(모델/위성) 은 정합된 동일길이 1D 배열이라 가정.
import metrics_basic as mb

obs = np.asarray(obs_matched, float)   # ISMN θ (m³/m³) — SAMPLE
mdl = np.asarray(mdl_matched, float)   # 모델/위성 θ — SAMPLE

# 실제 시그니처: metrics_basic 은 (forecast, obs) 순서!
stats = {
    "bias":  mb.bias(mdl, obs),        # mean(mdl - obs)  양수=모델 과습
    "rmse":  mb.rmse(mdl, obs),
    "mae":   mb.mae(mdl, obs),
    "si":    mb.si(mdl, obs),          # 불편RMSE / |mean(obs)|  (Scatter Index)
    "r":     mb.pearson_r(mdl, obs),
}
slope, intercept = mb.linregress(mdl, obs)   # obs → mdl 회귀
print({k: round(v, 4) for k, v in stats.items()}, "slope=", round(slope, 3))

# --- ubRMSD (토양수분 1차 표준) = bias·척도 제거 무작위오차 = CRMSD ---
# 실제 스킬 함수로: metrics_pattern.target_stats 의 'urmsd' 가 정확히 CRMSD(=ubRMSD).
import metrics_pattern as mp
tg = mp.target_stats(obs, mdl)          # (o, f) 순서! -> {'bias','urmsd','rmsd','n'}
ubrmsd = tg["urmsd"]                     # ≡ ubRMSD (m³/m³). RMSE² = bias² + ubRMSD²
print(f"ubRMSD={ubrmsd:.4f} m3/m3  (advisory 목표 ~0.04 는 미션요구값 — 절대기준 아님)")
```

### ★ 토양수분 이상상관 (Anomaly R) — 계절성 제거 후 단기 이벤트 재현력

원자료 R는 공통 계절성으로 과대해진다. 이동창 기후값을 빼 **이상 δθ**로 R를 다시 낸다(27 카드).

```python
# SAMPLE — 이동창 기후값 제거(±window). 실존 라이브러리 pytesmo 가 있으면 그걸 권장:
#   from pytesmo.time_series.anomaly import calc_anomaly     # 실존(선택)
#   an_obs = calc_anomaly(pd.Series(obs, index=idx), window_size=35)
# 없으면 numpy/pandas 로 직접(아래) — 창 길이·최소표본은 모델·관측 동일 규약!
def calc_anomaly_np(series: pd.Series, window_days: int = 35) -> pd.Series:
    """이동창 day-of-year 기후값 제거 (SAMPLE — 창 길이는 네 데이터에 맞춰라)."""
    clim = series.rolling(f"{window_days}D", center=True, min_periods=5).mean()
    return series - clim

s_obs = pd.Series(obs, index=pd.to_datetime(idx_utc))   # idx_utc: 매치업 시각 — SAMPLE
s_mdl = pd.Series(mdl, index=pd.to_datetime(idx_utc))
an_obs = calc_anomaly_np(s_obs); an_mdl = calc_anomaly_np(s_mdl)

# 실제 스킬 함수로 이상 상관: metrics_basic.pearson_r (forecast, obs) 순서
r_anom = mb.pearson_r(an_mdl.values, an_obs.values)
print(f"Anomaly R={r_anom:.3f}  (원자료 R={stats['r']:.3f}) — 이상 R가 진짜 스킬")
# 해석 advisory(27): 위성 표층 anomaly-R 0.3~0.7 흔함 — 밀림·동결·RFI 지역 급락. 값 하나로 단정 금지(§G-4).
```

### 분포 (Distribution) — QQ · Perkins · KS

```python
# SAMPLE — 실제 스킬 함수 metrics_distribution (obs, fct 순서)
import metrics_distribution as md
obs_q, mdl_q = md.qq_points(obs, mdl, n_quantiles=50)     # Q-Q 비교점
pss = md.perkins_skill_score(obs, mdl, bins=20)            # 분포 공통면적 [0,1]
ksd = md.ks_distance(obs, mdl)                             # KS 통계량 D
print(f"Perkins SS={pss:.3f}  KS D={ksd:.3f}")
```

---

## §D 종합 패턴 지표 (Taylor / Target)

```python
# SAMPLE — 실제 스킬 함수 metrics_pattern (o, f 순서)
import metrics_pattern as mp
ts = mp.taylor_stats(obs, mdl)     # {'std_ratio','corr','crmsd','n'}
tg = mp.target_stats(obs, mdl)     # {'bias','urmsd','rmsd','n'}
pc = mp.pattern_correlation(obs_map2d, mdl_map2d)   # 공간 스냅샷 상관 (2D 장, 육지마스크 후)
print(ts, tg, "pattern_corr=", round(pc, 3))
```

---

## §E 그림 (Figures — 실제 plots 함수, 지도는 add_basemap 필수)

```python
# SAMPLE — plots 는 PNG 경로를 반환. 지도형은 내부에서 add_basemap 호출(해안선+위경도).
import plots

# 카드1 시계열 overlay (obs, mdl) — 축=time×θ, 지도 아님
plots.timeseries_overlay(idx_utc, obs, mdl, "out/sm_timeseries.png")

# [16 §A] 산점 + SI + OLS  — 실제 시그니처는 (o, f, out_png, units)
plots.scatter_si(obs, mdl, "out/sm_scatter.png", units="m3/m3")

# QQ (분포) — (o, f, out_png)
plots.qq_plot(obs, mdl, "out/sm_qq.png")

# Taylor (종합) — (o, f, out_png)
plots.taylor_diagram(obs, mdl, "out/sm_taylor.png")

# ★ 카드3/13 공간 지도: (예보−관측) 편차 발산맵 — diff_map 내부에서 add_basemap 자동
#    1D 점(정점) 이면 scatter, 2D 격자면 pcolormesh. 해안선+위경도 자동.
plots.diff_map(lat=lats_pt, lon=lons_pt, diff=(mdl_pt - obs_pt),
               out_png="out/sm_bias_map.png", units="m3/m3",
               title="Soil moisture bias (model − ISMN)")   # SAMPLE 제목
```

### ★ 카드3: anomaly-R / ubRMSD 격자 지도 (직접 조립 + add_basemap 필수)

`diff_map`은 bias 발산맵 전용이므로, anomaly-R(0~1 순차맵)·ubRMSD 지도는 격자별 지표를
직접 계산해 `add_basemap`으로 해안선을 씌운다.

```python
# SAMPLE — 격자별 지표 지도. ★지도이므로 add_basemap 로 해안선/육지+위경도 라벨 필수.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from plots import add_basemap, _make_geo_axes

# 격자별 anomaly-R: 각 (y,x) 셀 시계열로 pearson_r. (여기선 mdl_grid, obs_grid: (t,y,x))
def gridwise_anomaly_r(obs_g, mdl_g):   # SAMPLE — 실데이터는 xr.apply_ufunc 로 벡터화 권장
    ny, nx = obs_g.shape[1:]
    R = np.full((ny, nx), np.nan)
    for j in range(ny):
        for i in range(nx):
            R[j, i] = mb.pearson_r(mdl_g[:, j, i], obs_g[:, j, i])   # (f, o) 순서
    return R

Rmap = gridwise_anomaly_r(obs_grid_anom, mdl_grid_anom)   # 이상 성분 넣어야 anomaly-R

fig, ax, tr = _make_geo_axes(figsize=(6, 5))
kw = {"transform": tr} if tr is not None else {}
sc = ax.pcolormesh(LON2D, LAT2D, np.ma.masked_invalid(Rmap),
                   cmap="viridis", vmin=0, vmax=1, shading="auto", **kw)   # 순차맵(0~1)
add_basemap(ax, LON2D, LAT2D)     # ★ 해안선/육지 + 위경도 라벨 (offline이면 격자선 fallback + 경고)
fig.colorbar(sc, ax=ax, label="Anomaly R")
ax.set_title("Soil-moisture anomaly-R (model vs reference)\n(advisory — reference≠truth; 계절·창정의 의존)")
fig.savefig("out/sm_anomalyR_map.png", dpi=100, bbox_inches="tight"); plt.close(fig)
# ubRMSD 지도는 cmap='magma'(비음수 순차맵), bias 지도는 cmap='RdBu_r'+TwoSlopeNorm(vcenter=0).
```

### ★ 카드14: 관측소 위치 지도 (station map, add_basemap 필수)

```python
# SAMPLE — 모든 정점 검증 보고의 서두. ★ add_basemap + ID 라벨 필수(재현성).
fig, ax, tr = _make_geo_axes(figsize=(6, 6))
kw = {"transform": tr} if tr is not None else {}
ax.scatter(lons, lats, s=40, c="crimson", edgecolor="k", zorder=5, **kw)
for sid, la, lo in zip(station_ids, lats, lons):
    ax.annotate(sid, (lo, la), xytext=(3, 3), textcoords="offset points", fontsize=8, **({} if tr is None else {}))
add_basemap(ax, lons, lats, margin_deg=1.0)   # ★ 정점 bbox+여백; 연안·산악이면 자동 10m 해안선
ax.set_title("ISMN/FLUXNET station map\n(대표성 경고: 단일 정점 ≠ 격자 화소, §G-1)")
fig.savefig("out/station_map.png", dpi=100, bbox_inches="tight"); plt.close(fig)
```

---

## §F 도메인 특이 지표 (Domain-Specific — 실존 라이브러리만)

표준 지표(RMSE/bias/Taylor/QQ)는 위에서 스킬 함수로 처리했고, 여기선 육상 고유 진단을
**numpy/scipy/xarray/pandas** 로(필요시 실존 `pytesmo`·`xskillscore`) 조립한다.

### ★ 토양수분 삼중대조 (Triple Collocation TC/ETC: 위성×모델×in-situ) — 카드2

참값 없이 세 독립 자료 각각의 무작위 오차분산을 추정. **실존 라이브러리 `pytesmo` 권장**.

```python
# SAMPLE — 세 자료(위성 x1, 모델 x2, in-situ x3)는 anomaly 공간·공통 동적범위·정합 매치업이어야 함.
# 실존 라이브러리(권장):
#   from pytesmo.metrics import tcol_metrics          # 실존: σ_ε, SNR 등
#   snr, err_std, beta = tcol_metrics(x1, x2, x3)
# pytesmo 없으면 공분산 기반 TC를 numpy 로 직접(고전 3-corner 해석해):
def triple_collocation_np(x1, x2, x3):
    """오차 표준편차 σ_ε (rescaled) — SAMPLE, 오차독립·정상성 가정(§G-2)."""
    m = np.isfinite(x1) & np.isfinite(x2) & np.isfinite(x3)
    a, b, c = x1[m], x2[m], x3[m]
    # x2 를 기준으로 스케일(β) — 실데이터는 pytesmo.scaling 로 rescale 권장
    C = np.cov(np.vstack([a, b, c]))     # 3x3 공분산
    # 고전 TC 오차분산 (Gruber et al. 2016 표기): 부호·표본에 민감 → CI 필수
    v1 = C[0,0] - C[0,1]*C[0,2]/C[1,2]
    v2 = C[1,1] - C[0,1]*C[1,2]/C[0,2]
    v3 = C[2,2] - C[0,2]*C[1,2]/C[0,1]
    return np.sqrt(np.clip([v1, v2, v3], 0, None))   # σ_ε (satellite, model, in-situ)

sig = triple_collocation_np(sat_anom, mod_anom, insitu_anom)   # SAMPLE 입력
print("TC σ_ε [sat, model, in-situ] =", np.round(sig, 4), "m3/m3")
# 함정(§G-3): 재분석·L4 를 '독립 3자'로 넣으면 오차상관으로 가정 붕괴 → σ_ε 편향.
# 부트스트랩 CI(에러바) 필수 → 막대그림(카드2)에 오차막대.
```

### ★ ET 에너지수지 닫힘 EBR + LE↔ET (카드6)

```python
# SAMPLE — flux tower 반시간 Rn·G·H·LE(W m-2). 저장항 처리방식은 캡션 명시.
Rn, G, H, LE = [np.asarray(v, float) for v in (Rn, G, H, LE)]   # SAMPLE 변수
avail = Rn - G          # 가용에너지
turb  = H + LE          # 난류플럭스
m = np.isfinite(avail) & np.isfinite(turb)
EBR = np.nansum(turb[m]) / np.nansum(avail[m])   # 닫힘비 (이상적 1)

from scipy import stats as sps
lr = sps.linregress(avail[m], turb[m])           # 실존 scipy — 기울기·절편·R
print(f"EBR={EBR:.2f}  slope={lr.slope:.2f}  r={lr.rvalue:.2f}")
# advisory(27): 관측 EBR ~0.7~0.9(불닫힘 10~30%) 흔함. 모델은 정의상 EBR≈1 → 비교시 불닫힘 감안(§G-1).

# LE(W m-2) → ET(mm/day):  ET = LE/(λ·ρ_w),  λ≈2.45e6 J/kg, ρ_w=1000 kg/m3
ET_mm_day = LE / (2.45e6 * 1000.0) * 86400.0 * 1000.0   # SAMPLE 상수(온도의존 λ 무시)
# 카드6 그림: plots 에 EBR 산점 전용 함수는 없으므로 matplotlib 로 직접 (x=Rn−G, y=H+LE, 1:1+OLS+EBR box).
```

### ★ 적설: SWE 시계열 + SCA 범주검증 F1 (카드8·9)

```python
# --- SWE bias/RMSE (정점 SNOTEL) — 실제 스킬 함수 (f, o) 순서 ---
swe_bias = mb.bias(swe_mdl, swe_obs)     # mm
swe_rmse = mb.rmse(swe_mdl, swe_obs)
# 융설 타이밍: SWE>임계(10mm) 최초/최종 초과일 → 날짜 bias(일). 표고대별 층화(§G).

# --- SCA 범주검증 (눈/무눈 이진) F1 — 강수/03 도메인에서 차용, 아래 cross-domain 절 참조 ---
```

### ★ 식생·탄소: LAI/NDVI 계절곡선 + GPP (카드10·11)

```python
# SAMPLE — DOY groupby 로 계절 climatology. LAI 유효/참 구분(군집지수 Ω) 캡션 명시.
s = pd.Series(lai_obs, index=pd.to_datetime(idx_utc))
clim_obs = s.groupby(s.index.dayofyear).mean()       # 계절곡선(관측)
clim_mdl = pd.Series(lai_mdl, index=s.index).groupby(s.index.dayofyear).mean()
# GPP 는 EC NEE 분할 산물(참값 아님) → 분할법 명시. bias/rmse 는 mb.bias/mb.rmse(f,o).
```

---

## §G ★ Cross-Domain 적용 (필수 절 — 타 도메인 기법을 이 데이터에 실제 적용)

이 도메인 관행이 아니어도 **육상 데이터에 실제로 유용한** 타 도메인 기법 3가지. 각기법에
"왜 여기서 유용한가" 1줄 + 실행 스니펫.

### CD-1. EOF/모드분해 (해양·기후 05에서 차용) → 토양수분 공간 주도모드

**왜 유용한가**: 토양수분 격자장은 강수·가뭄에 반응하는 소수의 공간 패턴이 분산 대부분을 설명 —
모델이 관측의 *주도 공간모드(가뭄 패턴 등)*를 재현하는지가 셀별 R보다 진단력이 높다.

```python
# SAMPLE — EOF/PCA(공간 주도모드). 실존: scikit-learn 또는 numpy SVD (지어내기 없음).
# 육상 관행이 아닌 05(해양/기후 변동) 기법을 토양수분 공간장에 차용.
def eof_modes(field_tyx, n_modes=3):
    """field_tyx: (t, y, x) anomaly 장 → 앞 n_modes EOF·PC (numpy SVD, SAMPLE)."""
    t = field_tyx.shape[0]
    X = field_tyx.reshape(t, -1)
    ok = np.all(np.isfinite(X), axis=0)          # 항상 유효한 셀만 (육지마스크와 결합)
    Xv = X[:, ok] - X[:, ok].mean(0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xv, full_matrices=False)
    var_frac = (S**2) / np.sum(S**2)
    return U[:, :n_modes], Vt[:n_modes], var_frac[:n_modes], ok  # PC, EOF, 분산비, 마스크

pc_o, eof_o, vf_o, ok = eof_modes(obs_grid_anom, 3)
pc_m, eof_m, vf_m, _  = eof_modes(mdl_grid_anom, 3)
# 모델·관측 EOF1 공간패턴 상관 → 실제 스킬 함수:
mode1_corr = mp.pattern_correlation(eof_o[0], eof_m[0])   # 주도모드 재현도
print(f"EOF1 var(obs)={vf_o[0]:.1%}  EOF1 pattern corr={mode1_corr:.2f}")
```

### CD-2. 삼중대조 (위성 도메인 12에서 차용) → 참값 없는 오차분해

**왜 유용한가**: ISMN 점 관측조차 대표성 오차로 "참값"이 아니다 — 위성/모델/in-situ 세 자료의
오차분산을 참값 없이 분리하면, 큰 검증차가 *모델 탓인지 기준 탓인지*를 객관적으로 가른다.
(코드는 §F 삼중대조 스니펫 참조 — `pytesmo.metrics.tcol_metrics` 실존, 또는 numpy 공분산 TC.)

```python
# SAMPLE — 위성 검증(12)의 TC 를 육상 토양수분에 적용(이미 §F에 구현).
# 핵심: in-situ σ_ε 도 유한 → "관측=진실" 가정을 깨고 대표성 오차를 정량화(§G-1).
sig_sat, sig_mod, sig_ins = triple_collocation_np(sat_anom, mod_anom, insitu_anom)
print("in-situ 도 오차 유한:", round(sig_ins, 4), "→ 관측을 truth 로 쓰지 말 것")
```

### CD-3. 범주형 F1 (강수/03에서 차용) → 적설역(SCA) 눈/무눈 이진검증

**왜 유용한가**: 적설면적은 본질적으로 이진 이벤트(눈/무눈)라, 강수 도메인의 분할표 범주지표
(POD/FAR/F1)가 연속 RMSE보다 직접적이다. **실존 `xskillscore` 권장, 없으면 numpy 2×2.**

```python
# SAMPLE — 강수/03 의 범주형(POD/FAR/F1)을 적설 SCA 에 차용.
# 실존 라이브러리(권장): import xskillscore as xs; xs.* (이진 스코어)
def sca_categorical(obs_snow_bin, mdl_snow_bin):
    """눈/무눈 2x2 → POD·FAR·precision·F1·accuracy (numpy, SAMPLE)."""
    o = np.asarray(obs_snow_bin, bool); m = np.asarray(mdl_snow_bin, bool)
    valid = np.isfinite(obs_snow_bin) & np.isfinite(mdl_snow_bin)   # 구름 화소는 별도 제외
    o, m = o[valid], m[valid]
    a = np.sum(m & o); b = np.sum(m & ~o); c = np.sum(~m & o); dd = np.sum(~m & ~o)
    pod = a/(a+c) if (a+c) else np.nan
    far = b/(a+b) if (a+b) else np.nan
    prec = a/(a+b) if (a+b) else np.nan
    f1 = 2*prec*pod/(prec+pod) if (prec+pod) else np.nan
    acc = (a+dd)/(a+b+c+dd) if (a+b+c+dd) else np.nan
    return {"POD": pod, "FAR": far, "precision": prec, "F1": f1, "accuracy": acc}

sca = sca_categorical(obs_snow >= 0.5, mdl_snow >= 0.5)   # 적설분율→이진 임계 0.5 (SAMPLE)
print(sca)
# advisory(27): 개방지 F1 높으나 삼림·구름·부분적설 전이기 급락. double-penalty(설선 어긋남) 주의(§G-4).
# 카드9 지도: hit/miss/false/corr-neg 4색 pcolormesh + add_basemap(★ 해안선/위경도 필수).
```

---

## §H 함정 및 주의 (Pitfalls — 육상 특유)

| # | 함정 | 대응 |
|---|------|------|
| H-1 | **기준 ≠ 참값** | ISMN·FLUXNET·위성·ERA5-Land 모두 reference. 축라벨 "모델 − 기준", "오차"로 단정 금지(§G-1) |
| H-2 | **점 ≠ 격자 (대표성 오차)** | `dist_km`·심도차 로그 기록. 큰 차이가 모델 탓 아닐 수 있음(§G-2) |
| H-3 | **심도 정합** | 위성 표층(0–5cm) vs 센서(5·10·20cm) vs 모델 층 혼용 금지 → 위상·진폭 오인 |
| H-4 | **재척도화 필요** | 토양수분은 자료마다 동적범위 상이 → CDF matching 후 anomaly-R/ubRMSD (`pytesmo.scaling`) |
| H-5 | **TC 오차독립 가정** | 재분석·L4 를 독립 3자로 넣지 말 것. 같은 강수강제·지면모형 공유 시 σ_ε 편향(§G-3) |
| H-6 | **EC 불닫힘** | 타워 ET/LE 10~30% 과소 가능. 닫힘 보정 프레이밍(Bowen/LE-only/미보정) 명시·민감도 병행 |
| H-7 | **주야·청천 표집편향** | 위성 LST/광학은 통과시각·청천만 표집 → 모델을 동일 sampling mask 로 |
| H-8 | **단일 그림 금지** | 정확도(산점)+편향(bias map)+분포/패턴(QQ/Taylor) 최소 3축 + 부트스트랩 CI(§G-4) |
| H-9 | **해석 임계 advisory** | ubRMSD~0.04·anomaly-R 0.3~0.7·EBR 0.7~0.9·SCA F1 = 미션/사례/관행값. 피복·계절·해상도 의존 |

---

## §I 관련 모듈 참조 (Modules)

| 모듈 | 핵심 인터페이스(실제) | 역할 |
|------|----------------------|------|
| `scripts/io_detect.py` | `open_dataset(path)` · `detect_format(path)` | 포맷 자동판별(nc/csv) + 인코딩 폴백 로딩 |
| `scripts/dataset.py` | `open_nc(path)` · `Dataset(.latlon/.coord_kind/.grid_shape/.is_mesh/.variable/.time_info/.xr)` | NetCDF 로딩·좌표 추상화(격자/mesh) |
| `scripts/preprocess.py` | `match_points_to_mesh` · `tz_to_utc` · `common_time_index` · `inject_point_coords` · `build_pairs` · `to_kelvin` · `parse_points_list` | 정점 매치업·시간대·단위 정규화 |
| `scripts/metrics_basic.py` | `bias` · `rmse` · `mae` · `si` · `nrmse` · `pearson_r` · `linregress` **(f, o 순서)** | 기본 오차 통계(NaN 마스크) |
| `scripts/metrics_distribution.py` | `qq_points` · `perkins_skill_score` · `ks_distance` · `quantiles` **(obs, fct 순서)** | 분포 비교 |
| `scripts/metrics_pattern.py` | `taylor_stats` · `target_stats`(urmsd=ubRMSD) · `pattern_correlation` **(o, f 순서)** | 패턴·Taylor/Target·ubRMSD |
| `scripts/metrics_circular.py` | `circular_mean_error` · `circular_rmse` · `circular_corr` | 방향(풍향) 원형통계(육상엔 드묾) |
| `scripts/plots.py` | `scatter_si` · `timeseries_overlay` · `qq_plot` · `taylor_diagram` · `diff_map` · **`add_basemap`** · `_make_geo_axes` | 그림(지도는 add_basemap 필수) |

**실존 외부 라이브러리(선택, 지어내기 금지)**: `numpy`·`scipy`·`xarray`·`pandas`·`matplotlib`(기본);
`pytesmo`(토양수분 anomaly/CDF matching/ubRMSD/triple collocation, pytesmo.readthedocs.io);
`xskillscore`(이진 범주지표); `cartopy`(basemap 해안선); `xesmf`(재격자화); `cmocean`(색맵).

---

## §J 출처 (Sources — 확인된 것만; 미확인은 "(확인요)")

- Gruber, A., et al. (2016) "Recent advances in (soil moisture) triple collocation analysis," *Int. J. Applied Earth Observation and Geoinformation* 45:200–211. (TC/anomaly)
- McColl, K. A., et al. (2014) "Extended triple collocation," *GRL* 41(17):6229–6236. **doi:10.1002/2014GL061322** (확인됨)
- Coll, C., et al. (2009) "Temperature-/radiance-based validations of the V5 MODIS LST product," *JGR: Atmospheres* 114, D20102. **doi:10.1029/2009JD012038** (확인됨)
- Wilson, K., et al. (2002) "Energy balance closure at FLUXNET sites," *Ag. For. Meteorol.* 113(1–4):223–243.
- Dorigo, W. A., et al. (2011) "The International Soil Moisture Network (ISMN)," *HESS*.
- Muñoz-Sabater, J., et al. (2021) "ERA5-Land," *Earth System Science Data* 13:4349–4383.
- Pastorello, G., et al. (2020) "The FLUXNET2015 dataset and the ONEFlux processing pipeline," *Scientific Data* 7:225.
- CEOS LPV *Soil Moisture Validation Good Practices Protocol* (v1, 2020); Guillevic et al. (2018) GSICS/CEOS *LST Validation Best Practice Protocol*.
- 소프트웨어: `pytesmo` (`time_series.anomaly.calc_anomaly`, `scaling.scale`, `metrics.tcol_metrics`) — pytesmo.readthedocs.io.
- **(확인요)**: 해석 임계(ubRMSD~0.04 m³/m³·anomaly-R 0.3~0.7·EBR 0.7~0.9·EC 불닫힘 10~30%·MODIS SCA POD~0.95/FAR~0.18·MODIS GPP 6~58% 과소)는 모두 미션요구/사례/관행 advisory — 피복·계절·해상도·기준자료 의존. 위 논문 중 본 세션에서 DOI 직접 확인은 McColl 2014·Coll 2009 뿐, 나머지 DOI 미표기(제목·저널·연도만).

---

*SAMPLE — 이 파일은 범용 스킬의 **육상(지표) 예시**다. 도메인 맞춤 적응 없이 그대로 운용 금지.
실데이터 구조(변수명·단위·심도·좌표·시간대·품질플래그)를 점검한 뒤 각 줄을 수정하라.*
