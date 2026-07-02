# Recipe: 해양 생지화학·해색 검증 (Ocean Biogeochemistry & Ocean Colour Validation)

> # ⚠️ SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> **이 스킬은 범용(any earth-system model output)이며, 이 파일은 그중 "해양 생지화학·해색"
> 한 예시(worked SAMPLE)일 뿐이다.** 아래 코드는 완비된 파이프라인이 아니라 **출발점 템플릿**이다.
> 실제 데이터(위성 해색 L3/L4·BGC-Argo 프로파일·GLODAP/SOCAT 병시료·WOA 기후값·모델 NetCDF 등)의
> **변수명·단위·좌표 위상(격자/mesh)·pH 스케일·상수 조**에 따라 각 단계를 반드시 수정해서 쓴다.
> 코드 곳곳의 `# SAMPLE ←` 주석은 "네 데이터에 맞춰 바꿔라"는 표시다.
>
> **대표 자료형(this example)**: 엽록소 로그정규(Chl-a log-normal) — 위성 해색 L3 격자 + BGC-Argo 점/프로파일.
> 방법 근거: `references/research/29_domain_ocean_biogeochemistry.md`,
> 그림 근거: `references/research/figures/37_fig_ocean_biogeochemistry.md`.

---

## 0. 이 도메인의 3대 특이사항 (왜 파랑·기상과 다른가)

1. **로그정규 변수** — Chl-a·영양염·NPP는 수 자릿수(orders of magnitude)에 걸쳐 분포.
   → **log10 변환 후** bias/RMSE/상관을 낸다(선형공간 RMSE는 고농도 연안값이 지배해 오해; Campbell 1995).
2. **기준자료 ≠ 참값(reference ≠ truth)** — 위성 Chl·NPP·PFT는 **알고리즘 산물**, WOA·GLODAP·SOCAT은 보간/편중 DB.
   → 캡션·범례에 "오차"가 아니라 **"모델 − 기준(reference) 차"**로 쓴다.
3. **탄산계는 규약이 결정적** — pH 스케일(total/free/seawater)·K1K2 상수 조·압력·온도기준·영양염 입력이 다르면
   수십 μatm·0.01 pH·포화수심 수백 m 차이가 "모델 오차"로 오인된다. → **동일 규약으로 PyCO2SYS 재계산** 후 비교.

> 이하 코드는 스킬의 **실제 함수**(`scripts/`)를 그대로 쓰되, 도메인 특이 지표(log10·MdSA·해색 매치업·
> 위도-깊이 단면·pCO2/pH·계절주기)는 **실존 라이브러리**(numpy/scipy/xarray/pandas, 필요시 PyCO2SYS/argopy)로 작성한다.

---

## 빠른 참조 (Quick Reference) — 단계 → 실제 스킬 함수 → 대응 그림카드

| 단계 | 실제 스킬 함수 (모듈.함수) | 대응 그림카드(37 도메인편) |
|------|---------------------------|----------------------------|
| A. 열기·구조/메타 점검 | `io_detect.open_dataset` · `dataset.open_nc` · `Dataset.coord_kind/latlon/grid_shape/variables/time_info` | — |
| B. 정점 매치업·시간대 | `preprocess.match_points_to_mesh` · `tz_to_utc` · `common_time_index` · `inject_point_coords` | Fig ⑥ BGC-Argo 프로파일(+지도) |
| C. 다축 정확도(log 공간) | `metrics_basic.bias/rmse/si/pearson_r/linregress` (on `log10`) + 도메인 MdSA(numpy) | Fig ① log-log Chl 매치업 산점 |
| D. 분포·꼬리(log 공간) | `metrics_distribution.qq_points/perkins_skill_score/ks_distance` (on `log10`) | Fig ⑫ log QQ / PDF·CDF |
| E. 종합 패턴 | `metrics_pattern.taylor_stats/target_stats/pattern_correlation` | Fig ⑮ 다변수 스킬(Target/Taylor) |
| F. 그림 | `plots.scatter_si/timeseries_overlay/diff_map/qq_plot/taylor_diagram` + `plots.add_basemap` | Fig ①②③④⑤⑫ |
| G. 캡션(§G advisory) | (모든 그림 함수에 내장된 §G advisory 문구) | 전 카드 공통 원칙 |

> **★ 지도형(위경도) 그림은 반드시 `plots.add_basemap()`** 로 해안선+라벨된 위경도 격자선을 넣는다
> (cartopy 없으면 격자선 fallback + 경고). 상세: `references/plotting_maps.md`.

---

## §A 열기 · 구조/메타 점검 (Open · Inspect structure/metadata)

```python
# SAMPLE — 실데이터에선 변수명·단위·좌표를 실시간 점검하고 바꿔라.
import sys, os
sys.path.insert(0, os.path.join("skills", "validate-model-output", "scripts"))  # SAMPLE ← 경로 조정
import numpy as np

from io_detect import open_dataset            # 실제 함수: 포맷 자동판별(nc3/nc4/csv)
from dataset import open_nc, Dataset          # 실제 함수: 한글경로 안전 NetCDF 로더

# --- 모델/위성 표층 Chl NetCDF (L3/L4 격자 또는 모델 격자) ---
d_mod = open_dataset("model_chl_surface.nc")  # SAMPLE ← 파일명
# open_dataset 은 Dataset 을 반환. NetCDF 라면 내부적으로 open_nc(한글경로 폴백) 사용.

# --- 구조/메타 점검 (실제 Dataset 메서드) ---
print("data vars :", d_mod.data_var_names())      # 실제: 변수 목록
print("coord_kind:", d_mod.coord_kind())          # 실제: '1d'|'2d'|'mesh'|'none'
print("latlon    :", d_mod.latlon())              # 실제: (lat_name, lon_name, is_2d) | None
print("grid_shape:", d_mod.grid_shape())          # 실제: (ny,nx)|(nlat,nlon)|(n_nodes,)
print("time_info :", d_mod.time_info())           # 실제: {name,n_steps,start,end}|None

# 변수 메타(단위·standard_name) 확인 — 로그정규/탄산계는 단위·CF명이 결정적
for name, var in d_mod.variables().items():
    print(name, "| units:", var.units, "| std_name:", var.standard_name)

# SAMPLE ← 네 데이터의 Chl 변수명·CF명으로 바꿔라.
#   흔한 CF: mass_concentration_of_chlorophyll_in_sea_water (mg m-3)
CHL_VAR = "chl"      # SAMPLE ← 실제 변수명
xr_mod  = d_mod.xr   # 실제: 내부 xarray.Dataset 접근

# 표층 슬라이스 (모델이 depth 축을 가지면 최상층 선택) — SAMPLE
chl_mod = xr_mod[CHL_VAR]
if "depth" in chl_mod.dims:
    chl_mod = chl_mod.isel(depth=0)     # SAMPLE ← 축 이름/방향 확인(surface=0?)
```

> **§A 실데이터 점검 항목**
> - Chl 변수의 **단위**가 `mg m-3` 인지, 로그 전 **0·음수·결측(구름)** 마스크가 필요한지.
> - `coord_kind()` 가 `mesh` 면 §B의 `match_points_to_mesh` 로 노드 매칭.
> - 위성 L3/L4는 **표층 ~1 광학심도** 신호, 모델은 **격자층 평균** → 대표성 차이(§G).
> - 경도 규약 `0–360 ↔ −180–180`·날짜변경선 주의.

---

## §B 정점/프로파일 매치업 · 시간대 정규화 (Point matchup · TZ)

BGC-Argo 점(또는 정점 BATS/HOT)을 모델 격자/mesh에 콜로케이션한다.

```python
# SAMPLE — float/정점 좌표·시간대는 데이터마다 다르다. 실시간 점검하라.
from preprocess import (
    match_points_to_mesh,   # 실제: cKDTree 최근접 노드 + km 거리필터(-1=제외)
    tz_to_utc,              # 실제: KST/UTC → UTC datetime64 (assumed 플래그 반환)
    common_time_index,      # 실제: 두 시계열 교집합 인덱스
    inject_point_coords,    # 실제: {id:(lat,lon)} → lat/lon 배열
)

# --- BGC-Argo(또는 정점) 좌표 주입 ---  SAMPLE ← 네 float ID/좌표로
float_ids = ["6901580", "6902547"]                     # SAMPLE
mapping   = {"6901580": (34.5, 129.2),                 # SAMPLE {id:(lat,lon)}
             "6902547": (33.1, 127.8)}
pt_lat, pt_lon = inject_point_coords(float_ids, mapping)

# --- 모델이 비정형 mesh 인 경우: 최근접 노드 매칭 ---
if d_mod.coord_kind() == "mesh":
    lat_dv = xr_mod["latitude"].values   # SAMPLE ← mesh lat/lon 은 data_var 일 수 있음
    lon_dv = xr_mod["longitude"].values
    idx, dist_km = match_points_to_mesh(lon_dv, lat_dv, pt_lon, pt_lat, max_km=25.0)  # SAMPLE ← 허용거리
    # idx == -1 인 관측점은 매치업 제외(거리 초과). dist_km 는 로그에 남겨라.
    print("matched node idx:", idx, "| dist(km):", np.round(dist_km, 1))

# --- 시간대: BGC-Argo/위성은 대개 UTC, 국내 정점 CSV 는 KST 가 흔함 ---
# SAMPLE ← 관측 시각의 실제 TZ 를 확인해서 넘겨라.
obs_t_utc, assumed = tz_to_utc(obs_times_raw, tz="UTC")   # 정점 CSV 면 tz="KST"
if assumed:
    print("경고: 시간대 미확인 → UTC 가정. KST 데이터면 9h 어긋남 위험.")

# --- 모델·관측 시간 교집합 정렬 ---
i_obs, i_mod = common_time_index(obs_t_utc, model_times_utc)   # SAMPLE ← 두 시간축
```

> **§B 함정(§G-2 대표성·독립성)**
> - **BGC-Argo 는 반드시 adjusted(보정) 자료 사용** — Chl 형광 slope(공장 기본값 ~2배 과대)·NPQ(주간 소광)·
>   O2 air-calibration·pH 편향 보정. raw 를 진값처럼 쓰지 마라.
> - 점(float) vs 격자 평균 → 스케일 불일치. `dist_km` 를 로그에 기록.

---

## §C 다축 정확도 검증 — **log10 공간** (Accuracy, log space)

Chl-a는 로그정규 → 스킬의 실제 `metrics_basic` 함수를 **log10 변환값**에 적용한다.
도메인 전용 MdSA(중앙값 대칭정확도)는 실존 numpy 로 계산.

```python
# SAMPLE — Chl 은 log10 공간 통계가 표준. 선형/로그 혼용 시 결론이 뒤집힌다(§G).
import numpy as np
import metrics_basic as mb   # 실제: bias/mae/rmse/nrmse/si/pearson_r/linregress

def _log10_clip(x, floor=1e-3):
    """0·음수·결측을 하한 clip 후 log10. SAMPLE ← floor 는 센서 검출한계로 조정."""
    x = np.asarray(x, dtype=float)
    x = np.where(np.isfinite(x) & (x > 0), x, np.nan)
    x = np.where(x < floor, floor, x)          # SAMPLE ← 하한 clip vs 제거 선택
    return np.log10(x)

# obs = 위성/현장 Chl(reference), mod = 모델/알고리즘 Chl
lo = _log10_clip(chl_obs)     # SAMPLE ← 네 관측 Chl 배열
lm = _log10_clip(chl_mod_at_obs)   # SAMPLE ← 매치업된 모델 Chl 배열

# --- 실제 스킬 함수로 log 공간 다축 지표 ---
stats_log = {
    "log_bias":  mb.bias(lm, lo),        # 실제 함수 (f=모델, o=관측)
    "log_rmse":  mb.rmse(lm, lo),        # 실제 함수 = log-RMSD
    "log_si":    mb.si(lm, lo),          # 실제 함수 (불편RMSE/mean)
    "log_r":     mb.pearson_r(lm, lo),   # 실제 함수
}
slope, intercept = mb.linregress(lm, lo)  # 실제 함수 (o→f OLS, log 공간)
stats_log["log_slope"], stats_log["log_intercept"] = slope, intercept

# --- 도메인 전용 지표 (실존 numpy; Seegers et al. 2018 MdSA) ---
def mdsa_pct(mod, obs):
    """Median Symmetric Accuracy [%] = 100*(10^median|log10(M/O)| − 1). 이상치에 강건."""
    m = np.asarray(mod, float); o = np.asarray(obs, float)
    mask = np.isfinite(m) & np.isfinite(o) & (m > 0) & (o > 0)
    if mask.sum() == 0:
        return float("nan")
    return 100.0 * (10.0 ** np.median(np.abs(np.log10(m[mask] / o[mask]))) - 1.0)

def geo_bias_ratio(mod, obs):
    """기하평균 편향비 = 10^median(log10(M/O)). 1=무편향, >1=과대."""
    m = np.asarray(mod, float); o = np.asarray(obs, float)
    mask = np.isfinite(m) & np.isfinite(o) & (m > 0) & (o > 0)
    if mask.sum() == 0:
        return float("nan")
    return float(10.0 ** np.median(np.log10(m[mask] / o[mask])))

stats_log["MdSA_pct"]      = mdsa_pct(chl_mod_at_obs, chl_obs)
stats_log["geo_bias_ratio"] = geo_bias_ratio(chl_mod_at_obs, chl_obs)
print(stats_log)
```

> **§C 해석(advisory — 절대 합격선 아님)**
> - 외해 Case-1 위성 Chl 목표 불확실성은 관행적으로 **±35%(~0.35 in log10)** 로 논의되나
>   **해역(Case-1/Case-2 연안)·계절·센서·알고리즘 의존**. 연안·극지·저광은 오차 급증 → 영역·계절 분리 보고.
> - OLS slope 는 **회귀희석 편향** → 필요시 Type-II(직교/RMA)로 병행(`scipy.odr`, 실존).
> - 위성 Chl 은 알고리즘 산물 → "모델 오차"가 아니라 "모델 − 위성 차"(§0-2).

---

## §D 분포·꼬리 검증 — **log10 공간** (Distribution, log space)

시간정렬이 안 맞아도 되는 분포 일치. 스킬의 실제 `metrics_distribution` 을 log 값에 적용.

```python
# SAMPLE — 로그정규 변수는 log 공간 QQ/PDF 로. 선형 QQ 는 고농도가 지배(§G).
import metrics_distribution as md   # 실제: qq_points/perkins_skill_score/ks_distance/quantiles

lo_all = _log10_clip(chl_obs_field)      # SAMPLE ← 관측 분포 표본(격자/트랙 전체)
lm_all = _log10_clip(chl_mod_field)      # SAMPLE ← 모델 분포 표본

# QQ 비교점 (실제 함수) — 꼬리 강조하려면 n_quantiles 늘려라
obs_q, mod_q = md.qq_points(lo_all, lm_all, n_quantiles=101)   # 실제 함수

# 분포 유사도 (실제 함수)
pss = md.perkins_skill_score(lo_all, lm_all, bins=40)   # 실제: 공통면적 [0,1]
ksD = md.ks_distance(lo_all, lm_all)                    # 실제: KS 통계량 D

# 도메인 전용: 기하평균 GM·기하표준편차 GSD (Campbell 1995, 실존 numpy)
def gm_gsd(x):
    lx = _log10_clip(x); lx = lx[np.isfinite(lx)]
    return float(10 ** np.mean(lx)), float(10 ** np.std(lx))
gm_o, gsd_o = gm_gsd(chl_obs_field)
gm_m, gsd_m = gm_gsd(chl_mod_field)
print(f"PSS={pss:.3f}  KS-D={ksD:.3f}  GM(o/m)={gm_o:.3f}/{gm_m:.3f}  GSD(o/m)={gsd_o:.2f}/{gsd_m:.2f}")
```

> **§D 주의**: 분포만 비교하면 **동시(시간) 일치는 못 본다**(상관 0이어도 QQ 완벽 가능) → §C·§F와 3축으로.
> 이질 수괴 혼합 시 로그정규 가정 약화(수괴별 분리; Campbell 1995).

---

## §E 종합 패턴 (Taylor / Target / pattern correlation)

여러 변수(Chl·NO3·O2·pCO2)를 한 요약틀로. 스킬의 실제 `metrics_pattern` 사용.

```python
# SAMPLE — 로그 변수는 log 공간 통계로 정규화. 변수별 σ_obs 로 정규화.
import metrics_pattern as mp   # 실제: taylor_stats/target_stats/pattern_correlation

t_chl  = mp.taylor_stats(lo_all, lm_all)   # 실제: {std_ratio, corr, crmsd, n}  ← log 공간
tg_chl = mp.target_stats(lo_all, lm_all)   # 실제: {bias, urmsd, rmsd, n}
pc_chl = mp.pattern_correlation(chl_obs_map, chl_mod_map)  # 실제: 공간 패턴 상관(2D 장)
print("Taylor:", t_chl, "| Target:", tg_chl, "| pattern r:", pc_chl)

# 다변수 스킬 히트맵(Stow 2009 관행: RI/MEF/CF)은 실존 라이브러리로 —
# xskillscore(있으면) 또는 numpy 로 변수별 정규화 스킬 계산 후 seaborn.heatmap.  SAMPLE
```

> **§E 주의**: **단일 스킬점수로 순위 확정 금지**(다축·부트스트랩 CI 동반). Target은 bias/분산은 보나 꼬리는 못 보고,
> Taylor는 bias 못 봄 → 병행. Stow 등급(CF<1·MEF>0)은 **advisory**.

---

## §F 그림 (Figures — 실제 `plots` 함수 + `add_basemap`)

스킬의 실제 그림 함수는 §G advisory 캡션을 내장한다. **로그정규 변수는 log10 값을 넘겨라.**

```python
# SAMPLE — 산출 경로·단위·log 변환 여부를 데이터에 맞춰 바꿔라.
import plots   # 실제: scatter_si/timeseries_overlay/diff_map/qq_plot/taylor_diagram + add_basemap
OUT = "submit/evidence/figs"   # SAMPLE ← 산출 폴더

# Fig ① log-log Chl 매치업 산점 (log10 값을 넘겨 로그축 효과)
# 주의: scatter_si 는 축 라벨이 Observation/Forecast. log 값을 넣었으면 units="log10(mg m-3)".
p1 = plots.scatter_si(lo, lm, f"{OUT}/fig01_chl_matchup_log.png",
                      units="log10(mg m-3)")   # 실제 함수 (o, f, out, units)

# Fig ⑫ log QQ (실제 함수) — log 값 입력
p12 = plots.qq_plot(lo_all, lm_all, f"{OUT}/fig12_chl_qq_log.png")   # 실제 함수

# Fig ④ 시계열 오버레이 (예: 정점 표층 Chl; 선형/로그 선택) 
p4 = plots.timeseries_overlay(t_axis, chl_obs_ts, chl_mod_ts,
                              f"{OUT}/fig04_chl_timeseries.png")     # 실제 함수

# Fig ③ 공간 log-bias 지도 (★ add_basemap 자동 포함 — diff_map 내부에서 호출)
# diff = 모델 − 관측 (log 공간). 2D 격자면 pcolormesh, 점이면 scatter.
log_bias_map = _log10_clip(chl_mod_grid) - _log10_clip(chl_obs_grid)   # SAMPLE
p3 = plots.diff_map(lat2d, lon2d, log_bias_map, f"{OUT}/fig03_chl_logbias_map.png",
                    units="log10(mg m-3)", title="Chl log-bias (model − satellite)")  # 실제 함수

# Fig ⑮ Taylor (실제 함수) — log 값 입력
p15 = plots.taylor_diagram(lo_all, lm_all, f"{OUT}/fig15_chl_taylor_log.png")   # 실제 함수
print("saved:", p1, p12, p4, p3, p15)
```

**§G 캡션 (모든 그림에 자동 포함되는 advisory — 반드시 유지)**
- **reference ≠ truth**: 위성 Chl·NPP·PFT·WOA·GLODAP·SOCAT·BGC-Argo 는 기준(reference)이지 참값이 아니다.
  축·범례·캡션에 "모델 − 기준 차"로 표기.
- **advisory 임계**: 위성 Chl "±35%(0.35 log10)", pH "−0.02/decade", Stow "CF<1·MEF>0" 는 관행값 —
  **해역·수형(Case-1/2)·계절·센서·알고리즘 의존**. "good/bad" 단정 금지.
- **단일 그림 금지**: 정확도(①) + 편향/공간(③) + 분포(⑫) 최소 3장 + 부트스트랩 CI(§01).
- **지도형은 `add_basemap` 필수**(해안선·라벨된 위경도). 로그정규 색은 **log10/LogNorm**.

---

## ★ §X Cross-domain 적용 (필수 절) — 타 도메인 기법을 이 데이터에 끌어오기

이 도메인 관행이 아니어도 **이 Chl/생지화학 데이터에 유용한** 타 도메인 기법 3가지. 각각 "왜 여기서 유용한가" + 코드.

### X-1 분포거리 (Perkins Skill Score / KS·log QQ) — **분포·기후 도메인(§14)에서 차용**
**왜 유용한가**: 해색 관행은 매치업 산점(bias/MdSA)에 치우쳐 **분포 형상**을 놓친다. 모델이 저농도 외해(왼쪽 꼬리)를
과대하거나 개화 고농도(오른쪽 꼬리)를 과소하는지는 **분포거리**로만 드러난다 — 평균 통계가 0이어도 꼬리가 틀릴 수 있다.

```python
# SAMPLE — 이미 §D에서 실제 함수 사용. 여기선 "왜"를 강조한 cross-domain 관점.
import metrics_distribution as md
pss = md.perkins_skill_score(lo_all, lm_all, bins=40)   # 실제: 분포 공통면적
ksD = md.ks_distance(lo_all, lm_all)                    # 실제: 최대 CDF 차(꼬리 민감)
obs_q, mod_q = md.qq_points(lo_all, lm_all, n_quantiles=101)  # 실제: log QQ 점
# 해석: log QQ 하단(저Chl) 1:1 위로 휨 → 외해 빈영양 과대(흔한 약점). 상단 아래로 휨 → 개화 과소.
```

### X-2 연직 프로파일·위도-깊이 단면 — **수온·염분 도메인(§09)에서 차용**
**왜 유용한가**: 위성 Chl 은 **표층만** 본다 → 심층엽록소극대(DCM)·심층 O2/영양염 구조는 안 보인다.
수온·염분 도메인의 **프로파일/단면 비교**를 그대로 가져오면 BGC-Argo 로 심층 3차원 편차 위치를 진단할 수 있다.
등수심 vs 등밀도 선택이 결론을 좌우(성층 오차를 생물오차로 오인 방지).

```python
# SAMPLE — 깊이별 bias 프로파일 + 위도-깊이 단면(실존 numpy/xarray/matplotlib).
import numpy as np, xarray as xr, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

# 깊이별 bias 프로파일 (모델 − 관측, 실제 metrics_basic.bias 를 층마다)
import metrics_basic as mb
depths = xr_mod["depth"].values          # SAMPLE ← 축 이름/단위 확인
bias_z = [mb.bias(mod_prof[k], obs_prof[k]) for k in range(len(depths))]  # 실제 함수 반복

# 위도-깊이 단면 차(경도평균) — 등수심 예시(등밀도면 비교가 유리한 경우 명시)
sec_mod = xr_mod["o2"].mean("lon")       # SAMPLE ← 변수/축, μmol kg-1 단위 통일
sec_obs = woa_o2.mean("lon")             # SAMPLE ← WOA 재격자 후
diff_sec = (sec_mod - sec_obs)
fig, ax = plt.subplots(figsize=(6, 4))
pc = ax.pcolormesh(diff_sec["lat"], diff_sec["depth"], diff_sec.values,
                   cmap="RdBu_r", shading="auto")   # 발산맵(0=흰색)
ax.invert_yaxis(); ax.set(xlabel="Latitude", ylabel="Depth (m)",
                          title="O2 model − WOA (lat–depth, advisory)")
fig.colorbar(pc, ax=ax, label="Δ O2 [µmol kg⁻¹]")
fig.savefig("submit/evidence/figs/figX2_o2_section_diff.png", dpi=100); plt.close(fig)
# 단면은 지리축이 아니므로 basemap 불필요. 단, 단면 위치 인셋 지도(add_basemap 소형) 권장.
```

### X-3 삼중대조 / 위성 매치업 QC — **위성 원격탐사 도메인(§12)에서 차용**
**왜 유용한가**: 해색 검증에서 "모델 − 위성"만 보면 **위성 자신의 오차**를 모델 탓으로 돌린다. 위성 도메인의
**3×3 매치업 QC**(균질성 CV·유효화소율)와 **삼중대조(triple collocation)** 개념을 끌어오면 float·위성·모델
세 소스의 오차를 분리 논의할 수 있다(단, float-위성-모델 상관 시 독립성 가정 주의; §G-2).

```python
# SAMPLE — Bailey–Werdell 3×3 매치업 QC (실존 numpy). in situ 지점 중심 3×3 화소.
import numpy as np
def matchup_qc(win3x3, valid_frac_min=0.5, cv_max=0.15):   # SAMPLE ← 임계는 센서·해역별 조정
    """win3x3: (9,) 화소값(구름=NaN). 유효율·±1.5σ 필터·CV 기준으로 채택 여부·대표값."""
    w = np.asarray(win3x3, float)
    if np.isfinite(w).mean() < valid_frac_min:
        return None                      # 유효화소 부족 → 기각
    v = w[np.isfinite(w)]
    med, sd = np.median(v), np.std(v)
    v = v[np.abs(v - med) <= 1.5 * sd]   # ±1.5σ 필터링 평균
    if v.size == 0 or (np.std(v) / np.mean(v)) > cv_max:   # 균질성 CV
        return None                      # 비균질 → 기각
    return float(np.mean(v))             # 채택 대표값
# 채택 매치업 수·CV 를 반드시 함께 보고(적으면 bootstrap CI). 위성 Chl 은 alg 산물(§0-2).
```

---

## §Y 탄산계 확장 (Carbonate system) — 규약 통일이 전제

Chl 외에 pCO2/pH/Ω를 다룰 때는 **비교 전 반드시 동일 규약으로 PyCO2SYS 재계산**한다(실존 라이브러리).

```python
# SAMPLE — PyCO2SYS(Humphreys et al. 2022, GMD) 실존. 규약 명시가 핵심(§0-3).
# pip install PyCO2SYS
import PyCO2SYS as pyco2   # 실존 라이브러리
res = pyco2.sys(
    par1=dic, par1_type=2,      # SAMPLE ← DIC (µmol kg-1)
    par2=alk, par2_type=1,      # SAMPLE ← TA  (µmol kg-1)
    temperature=sst, salinity=sss, pressure=pres,   # SAMPLE ← 현장 T/S/P
    total_phosphate=po4, total_silicate=si,         # SAMPLE ← 영양염 입력
    opt_pH_scale=1,             # 1=total scale (free/seawater 혼용 금지)
    opt_k_carbonic=10,          # SAMPLE ← 10=Lueker et al. 2000 (K1,K2 조 명시!)
)
pco2_derived = res["pCO2"]      # µatm
omega_ar     = res["saturation_aragonite"]
# 탄산계 내부정합(Fig ⑩): 두 쌍(DIC+TA vs pH+pCO2)으로 각각 유도해 잔차 비교 후 모델-관측 대조.
```

> **§Y 함정(§0-3)**: pH 스케일·K1K2 조·압력/온도기준·영양염 입력 불일치가 "모델 오차"로 오인되는 대표 함정.
> **모델·관측을 동일 규약으로 재계산**하고 규약을 캡션에 명시. SOCAT pCO2 는 fCO2↔pCO2 변환·시공간 편중 주의.

---

## §Z 함정 및 주의사항 (Pitfalls — 이 도메인 특유)

| # | 함정 | 대응 |
|---|------|------|
| Z-1 | **선형/로그 공간 혼용** | Chl·영양염·NPP 는 전 지표 **log10 공간**으로 통일(§C·§D). |
| Z-2 | **기준자료를 참값으로 과신** | 위성 Chl/NPP/PFT=알고리즘 산물, WOA/GLODAP=보간, SOCAT=편중 → "모델 − 기준 차"(§0-2). |
| Z-3 | **탄산계 규약 불일치** | pH 스케일·K1K2·압력·영양염 통일 후 PyCO2SYS 재계산(§Y). |
| Z-4 | **BGC-Argo raw 사용** | adjusted 자료 + Chl 형광 slope/NPQ·O2 gain·pH 편향 보정(§B). |
| Z-5 | **표층 vs 격자층/광학심도 대표성** | 위성 표층 신호 vs 모델 격자평균 — 대표성 차 명시(§A). |
| Z-6 | **단위 혼용** | µmol kg⁻¹ vs µmol L⁻¹ vs mL L⁻¹(밀도 환산), 표층 vs 연직적분 정의 통일. |
| Z-7 | **등수심 vs 등밀도** | 심층 비교는 등밀도면이 유리(약층 이동에 등수심 민감; §X-2). |
| Z-8 | **연안 Case-2·극지 저광** | 밴드비/Kd 실패 급증 → 외해/연안·영역·계절 분리 보고. |

---

## §W 실제 함수·라이브러리 인벤토리 (이 레시피가 실제로 호출하는 것)

**스킬 실제 함수(모듈.함수):**
- `io_detect.open_dataset`, `io_detect.detect_format`
- `dataset.open_nc`, `dataset.Dataset`(`.xr/.coord_kind/.latlon/.grid_shape/.variables/.variable/.data_var_names/.time_info/.is_mesh`)
- `preprocess.match_points_to_mesh`, `preprocess.tz_to_utc`, `preprocess.common_time_index`, `preprocess.inject_point_coords`, `preprocess.parse_points_list`, `preprocess.build_pairs`
- `metrics_basic.bias/mae/rmse/nrmse/si/pearson_r/linregress`
- `metrics_distribution.qq_points/perkins_skill_score/ks_distance/quantiles`
- `metrics_pattern.taylor_stats/target_stats/pattern_correlation`
- `metrics_circular.circular_mean_error/circular_rmse/circular_corr` (풍향/해류방향 등 방향변수 필요시)
- `plots.scatter_si/timeseries_overlay/diff_map/qq_plot/taylor_diagram` + `plots.add_basemap`

**실존 외부 라이브러리(지어내기 아님):** numpy · scipy(`scipy.odr` Type-II 회귀, `scipy.stats`) · xarray · pandas ·
matplotlib · (선택) cartopy(지도) · PyCO2SYS(탄산계, Humphreys et al. 2022 GMD, doi:10.5194/gmd-15-15-2022) ·
argopy(BGC-Argo 로드, euroargodev.github.io/argopy) · (선택) xskillscore/skill_metrics(다변수 스킬·Taylor/Target).

---

## 참고문헌 (확인된 DOI만; 미확인은 "(확인요)")

- Campbell (1995) *JGR Oceans* 100(C7):13237–13254 — 로그정규 bio-optical 변동.
- Bailey & Werdell (2006) *Remote Sensing of Environment* 102(1–2):12–23 — 위성 해색 매치업 프로토콜.
- Seegers et al. (2018) *Optics Express* 26(6):7404–7422 — MdSA 등 성능지표.
- Hu, Lee & Franz (2012) *JGR Oceans* 117:C01011, doi:10.1029/2011JC007395 — 3-band OCI.
- Perkins et al. (2007) *J. Climate* 20:4356–4376, doi:10.1175/JCLI4253.1 — PDF skill score.
- Stow et al. (2009) *J. Marine Systems* 76:4–15 — 커플드 BGC 모델 스킬 평가.
- Jolliff et al. (2009) *J. Marine Systems* 76:64–82, doi:10.1016/j.jmarsys.2008.05.014 — Target diagram.
- Humphreys et al. (2022) *Geoscientific Model Development* 15:15–43, doi:10.5194/gmd-15-15-2022 — PyCO2SYS.
- Lueker, Dickson & Keeling (2000) *Marine Chemistry* 70:105–119 — K1/K2 상수.
- Mucci (1983) *American Journal of Science* 283:780–799 — 아라고나이트·칼사이트 Ksp.
- Bakker et al. (2016) *ESSD* 8:383–413, doi:10.5194/essd-8-383-2016 — SOCATv3.
- Olsen et al. (2016) *ESSD* 8:297–323 — GLODAPv2.
- Thyng et al. (2016) *Oceanography* 29(3), doi:10.5670/oceanog.2016.66 — cmocean 색맵.
- Sarmiento & Gruber (2006) *Ocean Biogeochemical Dynamics*, Princeton — 표준 교과서 (확인요).

---

*SAMPLE — 이 스킬은 범용이며 이 파일은 해양 생지화학·해색 한 예시다. 도메인 맞춤 적응 없이 그대로 운용 금지.
실 데이터 구조(변수명·단위·좌표·pH 스케일·상수 조)를 점검한 뒤 각 줄을 수정하라.*
