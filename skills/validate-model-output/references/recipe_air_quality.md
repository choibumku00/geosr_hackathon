# Recipe: 대기질·대기화학 검증 (Air Quality / Atmospheric Chemistry Validation)

> # ⚠️ SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> **이 스킬(`validate-model-output`)은 특정 분야 전용이 아니라 범용(general-purpose)이다.**
> 이 파일은 그 범용 스킬을 **대기질·대기화학(air_quality)** 한 도메인에 적용한 **하나의 예시(worked SAMPLE)** 일 뿐이다.
> 아래 코드는 "완비된 파이프라인"이 아니라 **출발점 템플릿**이다 — 실 데이터(CMAQ/WRF-Chem 산출·측정소 CSV·위성 컬럼·CAMS 재분석 등)의
> **변수명·단위·좌표 위상(격자/점/mesh)·시간대**에 따라 각 단계를 **반드시 수정**해서 쓴다.
> 곳곳의 `# SAMPLE` 주석은 "네 데이터에 맞춰 바꿔라"는 표시다.
>
> **방법 근거**: [`research/25_domain_air_quality.md`](research/25_domain_air_quality.md) (메서드 카드) ·
> **그림 근거**: [`research/figures/33_fig_air_quality.md`](research/figures/33_fig_air_quality.md) (그림 카드).
> **해석 원칙(§G)**: 기준자료(측정소·위성·재분석)는 **reference이지 truth가 아니다**; 측정소는 **점(point) 관측**(대표성 오차);
> 농도는 **로그정규(우측 꼬리)** → 로그축·MFB/MFE·FAC2 기본(단, **오존은 로그정규 약함** → 선형·NMB 관례);
> 임계선(Boylan&Russell·Emery·FAC2·MQI)은 **advisory**; **단일 그림 금지**; 총 PM2.5가 맞아도 **성분 상쇄** 의심.

---

## 빠른 참조 (Quick Reference)

| 단계 | 실제 스킬 함수 (module.func) | 대응 그림카드 (33_fig) |
|------|------------------------------|------------------------|
| A. 열기·구조 점검 | `io_detect.open_dataset` · `dataset.open_nc` · `Dataset.coord_kind/latlon/grid_shape/time_info/variables` | — |
| B. 매치업·시간대 | `preprocess.tz_to_utc` · `common_time_index` · `match_points_to_mesh` · `inject_point_coords` · `build_pairs` | ② 측정소 위치도 |
| C. 다축 기본지표 | `metrics_basic.bias/mae/rmse/nrmse/si/pearson_r/linregress` | ① 로그산점+FAC2 · ⑬ 시계열 |
| D. 분포·꼬리 | `metrics_distribution.qq_points/quantiles/perkins_skill_score/ks_distance` | ⑧ QQ(로그·꼬리) |
| E. 종합요약 | `metrics_pattern.taylor_stats/target_stats/pattern_correlation` | ⑦ soccer/target · Taylor |
| F. 그림 | `plots.scatter_si/timeseries_overlay/diff_map/qq_plot/taylor_diagram` (지도는 `plots.add_basemap`) | ①②⑧⑨⑬⑭ |
| G. 방향(선택: 풍향) | `metrics_circular.circular_mean_error/circular_rmse/circular_corr` | (풍향 로즈: `plots.wave_rose`) |
| **도메인 특화(numpy/scipy/pandas 직접)** | MFB/MFE·NMB/NME·FAC2 · 초과사건 POD/FAR/CSI · 일변동/주말 · MFB bugle | ①③④⑤⑥⑪⑫⑮ |
| **★ cross-domain(§CD)** | POT/GPD·GEV(scipy) · rank histogram/CRPS · Taylor/target | ⑧ 꼬리 · (앙상블) |

**대표 자료형(이 SAMPLE이 다루는 것)**: 측정소 점(정점)·시계열 CSV(한글 **cp949**, 로그정규 농도 PM2.5/PM10/O3/NO2) + (선택) 위성 컬럼(트랙/타일 NO2·AOD) + (선택) 재분석 격자(CAMS/MERRA-2).

---

## §0 임포트 & 경로 (Imports)

```python
# SAMPLE — scripts/ 가 sys.path 에 있어야 flat import 가능(conftest.py가 등록; CLI/노트북은 아래처럼 직접 추가).
import sys, os
SKILL = os.environ.get("SKILL", os.getcwd())   # $SKILL = 스킬 설치 폴더(설치 위치/CLI 인자로 교체)
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import numpy as np
import pandas as pd

# 실제 스킬 모듈 (flat 모듈명 — 지어낸 이름 아님)
import io_detect                 # open_dataset, detect_format
from dataset import open_nc, Dataset
import preprocess                # tz_to_utc, common_time_index, match_points_to_mesh, inject_point_coords, build_pairs
import metrics_basic as mb       # bias, mae, rmse, nrmse, si, pearson_r, linregress
import metrics_distribution as md  # quantiles, qq_points, perkins_skill_score, ks_distance
import metrics_pattern as mp     # taylor_stats, target_stats, pattern_correlation
import metrics_circular as mc    # circular_mean_error, circular_rmse, circular_corr
import plots                     # scatter_si, timeseries_overlay, diff_map, qq_plot, taylor_diagram, wave_rose, add_basemap

OUT = r"out_air_quality"  # SAMPLE — 그림 저장 폴더. 네 경로로 교체
os.makedirs(OUT, exist_ok=True)
```

---

## §A 열기 · 구조/메타 점검 (Open & Inspect)

대기질 데이터는 (1) 측정소 시계열 CSV(한글 cp949, `일시`·`측정소명`·`PM25`…), (2) 모델/재분석 NetCDF 격자, (3) 위성 L2/L3 트랙/타일로 온다. 먼저 **구조를 실시간 점검**한다.

```python
# ---- A-1 측정소 CSV 열기 (한글 cp949 자동 폴백은 io_detect 내장) -------------
# SAMPLE — open_dataset() 는 utf-8→cp949→euc-kr→latin-1 순으로 폴백한다(io_detect._CSV_ENCODINGS).
ds_obs = io_detect.open_dataset(r"airkorea_2023.csv")   # SAMPLE 경로
print("fmt:", ds_obs.fmt, "| vars:", ds_obs.data_var_names())  # 구조 확인

# CSV 는 to_xarray() 로 감싸여 있으니, 세밀 조작은 pandas 로 다시 읽는 편이 편하다.
# SAMPLE — 한글 컬럼 → 영문 alias. 실 헤더에 맞춰 반드시 수정하라.
df = pd.read_csv(r"airkorea_2023.csv", encoding="cp949",
                 na_values=["-", "", "결측", "9999", "-999"])   # SAMPLE 결측기호
ALIAS = {
    "일시":       "datetime",     # SAMPLE — "측정일시"/"날짜" 등일 수 있음
    "측정소명":   "station",      # SAMPLE — "지점"/"stationCode"
    "PM25":       "pm25_obs",     # µg/m³   (로그정규)
    "PM10":       "pm10_obs",     # µg/m³   (로그정규)
    "O3":         "o3_obs",       # ppm 또는 ppb — 단위 확인! (오존은 선형 관례)
    "NO2":        "no2_obs",      # ppb/ppm
    "풍속":       "wspd_obs",     # m/s  (선택)
    "풍향":       "wdir_obs",     # deg  (선택, §G 원형통계)
}
df = df.rename(columns={k: v for k, v in ALIAS.items() if k in df.columns})
df["datetime"] = pd.to_datetime(df["datetime"])   # SAMPLE — 포맷 안 맞으면 format= 지정

# ---- A-2 모델/재분석 NetCDF 열기 (한글 경로 안전) ---------------------------
# SAMPLE — open_nc 는 기본→h5netcdf→scipy 엔진 폴백(Windows 한글경로 우회) 내장.
dmod = io_detect.open_dataset(r"cmaq_pm25_2023.nc")   # 또는 Dataset(open_nc(path), ...)
print("coord_kind:", dmod.coord_kind())    # '1d' | '2d' | 'mesh' | 'none'
print("latlon:", dmod.latlon())            # (lat_name, lon_name, is_2d) | None
print("grid_shape:", dmod.grid_shape())    # (ny,nx) | (nlat,nlon) | (n_nodes,)
print("time:", dmod.time_info())           # {'name','n_steps','start','end'} | None
for name, v in dmod.variables().items():   # 변수·단위·표준명 점검
    print(f"  {name}: dims={v.dims} units={v.units} std={v.standard_name}")
```

> **실데이터 점검 체크리스트 (SAMPLE)**
> - 오존 단위가 **ppm vs ppb** — 벤치마크(Emery) 절단임계와 단위가 엮인다. 통일 필수.
> - PM 단위 µg/m³, **기준상태(STP) 보정 여부** 확인.
> - 검출한계(LOD) 이하·0·음수 처리 규칙을 **미리 정해 기록**(로그지표·FAC2가 이 규칙에 좌우됨, §25 log-space 카드).
> - 시간대: 측정소 CSV는 **KST(+09:00)**, 모델/위성은 보통 **UTC** → §B 에서 정렬.

---

## §B 매치업 · 시간대 정렬 (Matchup & Time Alignment)

```python
# ---- B-1 시간대 → UTC (측정소 KST → UTC) ------------------------------------
# SAMPLE — 측정소가 KST면 반드시 -9h. tz 모르면 assumed=True 로 경고를 남긴다.
obs_time_utc, assumed = preprocess.tz_to_utc(df["datetime"].values, tz="KST")  # SAMPLE tz
if assumed:
    print("[경고] 관측 시간대 미확인 — UTC로 가정함 (9h 위상오차 위험)")

# ---- B-2 모델 격자 → 측정소 점 추출 -----------------------------------------
# 측정소 좌표(위경도). SAMPLE — AirKorea/EEA 측정소 메타에서 구성하라.
STN_LATLON = {                    # {station: (lat, lon)}  — SAMPLE 값
    "종로구":   (37.572, 126.979),
    "부산_광복": (35.099, 129.033),
    "대전_문창": (36.322, 127.421),
}
stn_ids = list(STN_LATLON.keys())
lat_pt, lon_pt = preprocess.inject_point_coords(stn_ids, STN_LATLON)

# 모델이 mesh(비정형)면 최근접 노드, 정규격자면 xarray.sel(method="nearest").
xr_mod = dmod.xr
if dmod.coord_kind() == "mesh":
    lat_name, lon_name = "latitude", "longitude"     # SAMPLE — is_mesh()가 True인 data_var명 확인
    mesh_lon = xr_mod[lon_name].values
    mesh_lat = xr_mod[lat_name].values
    node_idx, dist_km = preprocess.match_points_to_mesh(
        mesh_lon, mesh_lat, lon_pt, lat_pt, max_km=15.0)   # SAMPLE — 격자해상도에 맞춘 임계
    print("최근접 노드 거리(km):", dict(zip(stn_ids, np.round(dist_km, 1))))
    # SAMPLE — 변수명 "PM25"는 네 모델 출력명으로 교체. (T, node)
    mod_pm25 = xr_mod["PM25"].values[:, node_idx]        # shape (T, n_stn)
else:
    # 정규격자: 측정소별 nearest 셀
    lat_name, lon_name, _ = dmod.latlon()
    cols = []
    for la, lo in zip(lat_pt, lon_pt):
        sub = xr_mod["PM25"].sel({lat_name: la, lon_name: lo}, method="nearest")
        cols.append(sub.values)
    mod_pm25 = np.column_stack(cols)                     # (T, n_stn)
mod_time = np.asarray(xr_mod[dmod.time_info()["name"]].values, dtype="datetime64[ns]")

# ---- B-3 관측을 (T, n_stn) 격자로 피벗 --------------------------------------
# SAMPLE — long → wide. 관측 시각은 이미 UTC(obs_time_utc)로 맞춘 것을 쓴다.
df["_t"] = obs_time_utc
obs_wide = (df.pivot_table(index="_t", columns="station", values="pm25_obs")
              .reindex(columns=stn_ids))
obs_time = np.asarray(obs_wide.index.values, dtype="datetime64[ns]")
obs_pm25 = obs_wide.values                              # (T_obs, n_stn)

# ---- B-4 공통 시각 교집합으로 정렬 -----------------------------------------
i_obs, i_mod = preprocess.common_time_index(obs_time, mod_time)
O = obs_pm25[i_obs, :]      # (T_common, n_stn)   관측(reference)
M = mod_pm25[i_mod, :]      # (T_common, n_stn)   모델
t_common = obs_time[i_obs]

# 롱포맷(측정소별 층화·groupby 용) — 선택
pairs = preprocess.build_pairs(stn_ids, t_common, M, O, var_name="pm25")
# pairs.columns == ['station','time','model','obs']
```

> **함정 (SAMPLE로 반드시 점검)**: mesh의 `latitude/longitude`가 coord가 아니라 **data variable**일 수 있다(`Dataset.is_mesh()` 확인). 최근접 거리 `max_km`는 **격자 해상도**에 맞춰라(도시 NO2는 대표성 오차 큼, §25). KST/UTC 어긋나면 일변동(§도메인)에서 **가짜 위상오차**로 나타난다.

---

## §C 다축 기본지표 (Core Metrics — 실제 metrics_basic 사용)

지표 하나로 결론내지 말고 **정확도+편향+분포+사건**을 함께 낸다(§G-5).

```python
# ---- C-1 측정소별 + 통합 기본지표 (실제 함수) --------------------------------
def core_stats(o, f):
    """metrics_basic 실제 함수만 사용. (f=예보/모델, o=관측)"""
    return {
        "n":      int(np.isfinite(np.asarray(o,float).ravel() + np.asarray(f,float).ravel()).sum()),
        "bias":   mb.bias(f, o),        # mean(f-o) — 양수=과대
        "mae":    mb.mae(f, o),
        "rmse":   mb.rmse(f, o),
        "nrmse":  mb.nrmse(f, o),       # RMSE/|mean(o)|
        "si":     mb.si(f, o),          # 불편RMSE/|mean(o)| (Scatter Index)
        "r":      mb.pearson_r(f, o),
        "slope":  mb.linregress(f, o)[0],   # o→f 회귀 기울기
        "intercept": mb.linregress(f, o)[1],
    }

# 통합(전 측정소·전시각 flatten)
overall = core_stats(O, M)
print("통합:", {k: (round(v,3) if isinstance(v,float) else v) for k,v in overall.items()})

# 측정소별
per_station = {stn: core_stats(O[:, j], M[:, j]) for j, stn in enumerate(stn_ids)}
```

### C-2 도메인 특화 지표 — 로그공간·대칭 정규화 (numpy 직접; §25 근거)

> 실존 스킬 함수에는 MFB/MFE·NMB/NME·FAC2 가 **없다** → 도메인 카드(§25) 정의식대로 **numpy로 직접** 구현(카드가 지시한 라이브러리). PM은 로그정규라 이 지표들이 1급.

```python
def _finite(o, f):
    o = np.asarray(o, float).ravel(); f = np.asarray(f, float).ravel()
    m = np.isfinite(o) & np.isfinite(f)
    return o[m], f[m]

def mfb(o, f):   # Mean Fractional Bias  ∈ [-2, 2]  (Boylan & Russell 2006)
    o, f = _finite(o, f); s = o + f; k = s != 0
    return float(np.mean(2.0 * (f[k] - o[k]) / s[k]))

def mfe(o, f):   # Mean Fractional Error ∈ [0, 2]
    o, f = _finite(o, f); s = o + f; k = s != 0
    return float(np.mean(2.0 * np.abs(f[k] - o[k]) / s[k]))

def nmb(o, f):   # Normalized Mean Bias  (Emery 2017; 합산정규화)  = Σ(f-o)/Σo
    o, f = _finite(o, f); so = np.sum(o)
    return float(np.sum(f - o) / so) if so != 0 else np.nan

def nme(o, f):   # Normalized Mean Error = Σ|f-o|/Σo
    o, f = _finite(o, f); so = np.sum(o)
    return float(np.sum(np.abs(f - o)) / so) if so != 0 else np.nan

def fac2(o, f, eps=1e-9):   # Factor of 2 (Chang & Hanna 2004)
    o, f = _finite(o, f); k = np.abs(o) > eps          # SAMPLE — LOD/0 처리규칙 명시
    ratio = f[k] / o[k]
    return float(np.mean((ratio >= 0.5) & (ratio <= 2.0))) if k.any() else np.nan

def log_bias(o, f, eps=1e-9):   # log-space bias = ln(기하평균비) (§25 log-space 카드)
    o, f = _finite(o, f); k = (o > eps) & (f > eps)     # 양수만
    return float(np.mean(np.log(f[k]) - np.log(o[k]))) if k.any() else np.nan

aq = {stn: {"MFB": mfb(O[:,j], M[:,j]), "MFE": mfe(O[:,j], M[:,j]),
            "NMB": nmb(O[:,j], M[:,j]), "NME": nme(O[:,j], M[:,j]),
            "FAC2": fac2(O[:,j], M[:,j]), "log_bias": log_bias(O[:,j], M[:,j])}
      for j, stn in enumerate(stn_ids)}
print("측정소별 대기질 지표:", aq)
```

> **해석 (advisory — 지역/화학종/해상도 의존, §G-4)**: Boylan & Russell(2006) PM **목표** |MFB|≤30%·MFE≤50%, **기준** |MFB|≤60%·MFE≤75%. Emery et al.(2017) 오존 NMB≤±5%(goal)/±15%(criteria)·NME≤15/25%. FAC2≥0.5(Chang & Hanna 2004). **pass/fail 시험 아님.**

---

## §D 분포·꼬리 (Distribution & Tails — 실제 metrics_distribution 사용)

고농도 꼬리(고오염 에피소드) 재현이 규제·보건상 핵심. **로그축 QQ**로 본다(그림카드 ⑧).

```python
o_flat, f_flat = O.ravel(), M.ravel()

# 실제 함수: qq_points / quantiles / perkins_skill_score / ks_distance
obs_q, mod_q = md.qq_points(o_flat, f_flat, n_quantiles=50)   # (obs_q, fct_q)
pss = md.perkins_skill_score(o_flat, f_flat, bins=30)         # 분포 공통면적 ∈[0,1]
ks  = md.ks_distance(o_flat, f_flat)                          # KS D ∈[0,1]

# 상위 분위수(고농도) bias 만 따로 — SAMPLE
p_tail = [0.90, 0.95, 0.99]
q_o = md.quantiles(o_flat, p_tail)
q_m = md.quantiles(f_flat, p_tail)
tail_bias = {f"p{int(p*100)}": float(q_m[i] - q_o[i]) for i, p in enumerate(p_tail)}
print("PSS:", round(pss,3), "| KS D:", round(ks,3), "| 꼬리 bias:", tail_bias)
```

> **주의(§G)**: 자기상관 때문에 KS는 거의 항상 "유의" → **QQ 시각진단 우선**. 로그축 필수(선형은 꼬리 은폐). 계절 분리 권장(여름 O3·겨울 PM 꼬리 상이).

---

## §E 종합요약 (Taylor / Target — 실제 metrics_pattern 사용)

다지점·다종을 한 눈에. Taylor는 bias를 못 보므로 **Target·MFB 병행**(대기질은 bias가 핵심, §33 ⑦).

```python
tay = mp.taylor_stats(O, M)     # {'std_ratio','corr','crmsd','n'}
tar = mp.target_stats(O, M)     # {'bias','urmsd','rmsd','n'}
pat = mp.pattern_correlation(O, M)   # 공간 스냅샷 패턴 상관(격자장에 유용)
print("Taylor:", tay, "\nTarget:", tar, "\npattern r:", round(pat,3))
```

---

## §F 그림 (Figures — 실제 plots 사용; 지도는 add_basemap 필수)

```python
# ① 농도 산점 (로그정규 — 실 그림카드는 로그축 권장; scatter_si는 선형 SAMPLE)
p1 = plots.scatter_si(o_flat, f_flat, os.path.join(OUT, "01_scatter_pm25.png"), units="µg/m³")

# ⑬ 시계열 오버레이 (한 측정소; 고오염 에피소드 위상·계통 offset)
j = 0
p13 = plots.timeseries_overlay(t_common, O[:, j], M[:, j],
                               os.path.join(OUT, f"13_ts_{stn_ids[j]}.png"))

# ⑧ QQ (분포·고농도 꼬리)
p8 = plots.qq_plot(o_flat, f_flat, os.path.join(OUT, "08_qq_pm25.png"))

# ⑦/Taylor
p7 = plots.taylor_diagram(O, M, os.path.join(OUT, "07_taylor_pm25.png"))

# ②/⑭ 지도형 — 측정소 위치 + bias  (★ add_basemap 필수: 해안선+위경도)
# diff_map 은 1D 점 입력이면 scatter 맵 + add_basemap 자동 적용.
site_bias = np.array([per_station[s]["bias"] for s in stn_ids])   # 측정소별 bias
p2 = plots.diff_map(lat_pt, lon_pt, site_bias,
                    os.path.join(OUT, "02_14_station_bias_map.png"),
                    units="µg/m³", title="PM2.5 station bias (F-O)")
print("saved:", p1, p13, p8, p7, p2, sep="\n  ")
```

### F-2 도메인 특화 그림 (numpy/matplotlib/pandas 직접 — §33 근거)

실존 스킬에 없는 대기질 고유 그림은 실존 라이브러리로 직접 그린다(§33이 지시).

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ③ MFB / MFE "bugle" plot (Boylan & Russell 농도 의존 goal/criteria) --------
def bugle(o, f, out_png):   # SAMPLE — 측정소별 점 + goal/criteria 곡선
    o, f = _finite(o, f)
    xg = np.logspace(np.log10(max(o.min(),0.1)), np.log10(o.max()), 200)  # 관측 농도축(log)
    # 농도 완화식 근사(SAMPLE — 원저 식으로 교체): 저농도에서 벌어지게
    goal_mfb = 0.30 + 0.7*np.exp(-xg/2.0);  crit_mfb = 0.60 + 1.0*np.exp(-xg/2.0)
    fig, ax = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    # 측정소별 MFB/MFE 를 관측평균 위치에 점으로
    for j, s in enumerate(stn_ids):
        om = np.nanmean(O[:, j])
        ax[0].plot(om, mfb(O[:,j], M[:,j])*100, "o"); ax[1].plot(om, mfe(O[:,j], M[:,j])*100, "s")
    ax[0].plot(xg,  goal_mfb*100, "g-", xg, -goal_mfb*100, "g-", lw=0.8)
    ax[0].plot(xg,  crit_mfb*100, "r--", xg, -crit_mfb*100, "r--", lw=0.8)
    ax[0].set_ylabel("MFB [%]"); ax[1].set_ylabel("MFE [%]"); ax[1].set_xlabel("Obs conc [µg/m³]")
    ax[1].set_xscale("log"); ax[0].set_title("MFB/MFE bugle (advisory — reference≠truth; goal/criteria는 참고선)")
    fig.tight_layout(); fig.savefig(out_png, dpi=100); plt.close(fig); return out_png
bugle(o_flat, f_flat, os.path.join(OUT, "03_bugle_pm25.png"))

# ④ 초과사건 POD/FAR/CSI (범주형; §25) — numpy 직접 -----------------------------
def exceedance_scores(o, f, thr):   # 2×2: a hit, b false, c miss
    o, f = _finite(o, f); oe, fe = o >= thr, f >= thr
    a = int(np.sum(oe & fe)); b = int(np.sum(~oe & fe)); c = int(np.sum(oe & ~fe))
    pod = a/(a+c) if (a+c) else np.nan
    far = b/(a+b) if (a+b) else np.nan
    csi = a/(a+b+c) if (a+b+c) else np.nan
    fbias = (a+b)/(a+c) if (a+c) else np.nan
    return {"thr": thr, "a": a, "b": b, "c": c, "POD": pod, "FAR": far, "CSI": csi, "FBIAS": fbias}
# PM2.5 일평균 주의보 임계 SAMPLE(µg/m³) — 네 규제 임계로 교체
for thr in [35.0, 75.0]:
    print("초과사건:", exceedance_scores(o_flat, f_flat, thr))

# ⑤ 일변동 합성 (diurnal; LST 정렬 필수) — pandas 직접 -------------------------
# SAMPLE — t_common 은 UTC. 한국이면 +9h 로 LST 변환 후 시간대 groupby.
dfd = pairs.copy()
dfd["hour_lst"] = (pd.to_datetime(dfd["time"]) + pd.Timedelta(hours=9)).dt.hour  # SAMPLE +9
diur = dfd.groupby("hour_lst")[["obs", "model"]].mean()
fig, ax = plt.subplots(2,1, figsize=(6,5), sharex=True)
ax[0].plot(diur.index, diur["obs"], "k-o", label="Obs"); ax[0].plot(diur.index, diur["model"], "r--s", label="Model")
ax[0].legend(); ax[0].set_ylabel("conc")
ax[1].bar(diur.index, diur["model"]-diur["obs"]); ax[1].axhline(0, color="k", lw=0.6)
ax[1].set_ylabel("bias(h)"); ax[1].set_xlabel("Hour (LST)")
ax[0].set_title("Diurnal composite (advisory — reference≠truth)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "05_diurnal.png"), dpi=100); plt.close(fig)

# ⑥ 주말효과 / ⑫ 측정소 유형 box / ⑮ 계절 히트맵 도 pandas.groupby + matplotlib/seaborn 로 동일 패턴.
```

### F-3 위성 컬럼·재분석 격자 (선택 — 지도형은 add_basemap 필수, §33 ⑨⑭)

```python
# ⑨ 위성 대류권 NO2 컬럼 vs 모델 (트랙/타일). ⑭ CAMS/MERRA-2 재분석 격자 bias.
# SAMPLE — 위성은 truth 아님(§G-1); 통과시각·구름·QA 필터 + 평균화커널(AK) 적용이 원칙(§25 AK 카드).
sat = io_detect.open_dataset(r"tropomi_no2_L3.nc")      # SAMPLE
xr_sat = sat.xr
lat2d = xr_sat["latitude"].values; lon2d = xr_sat["longitude"].values   # SAMPLE 변수명
no2_sat = xr_sat["tropospheric_NO2_column"].values                      # molec/cm²
no2_mod = xr_mod["NO2_column"].values                                   # SAMPLE — AK 적용 후 컬럼
# 격자 정합(재격자)은 xarray+xesmf 로(실존). 여기선 동일격자 가정 SAMPLE.
diff2d = no2_mod - no2_sat
plots.diff_map(lat2d, lon2d, diff2d, os.path.join(OUT, "09_no2_col_diff.png"),
               units="molec/cm²", title="NO2 column model-satellite")  # 2D → pcolormesh + add_basemap
```

---

## §CD ★ Cross-domain 적용 (필수 절 — 타 도메인 기법을 이 데이터에)

대기질 관행이 아니어도 **이 데이터(로그정규 농도·고오염 에피소드·앙상블)** 에 유용한 타 도메인 기법을 실제로 적용한다. 각 기법에 **"왜 여기서 유용한가"** 1줄 + 스니펫.

### CD-1 극치 이론 POT/GPD · GEV (파랑/해수면·강수에서 차용 → 고농도 에피소드)

> **왜 유용?** PM/오존 **고오염 에피소드**는 평균지표·QQ가 못 보는 꼬리 사건 — 극치통계로 "재현수준(return level)"을 모델이 재현하는지 정량화(§25 QQ/꼬리 카드가 극값 `03` 병행 권고).

```python
from scipy import stats   # 실존
def gpd_return_level(x, q=0.95, T_ratio=100.0):
    """POT(peaks-over-threshold)+GPD: 임계 초과분에 일반화파레토 적합 → return level. (SAMPLE)"""
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    u = np.quantile(x, q)                      # SAMPLE — 임계는 mean residual life plot로 선택
    exceed = x[x > u] - u
    if exceed.size < 30: return np.nan         # 표본 부족 가드
    c, loc, scale = stats.genpareto.fit(exceed, floc=0.0)
    rate = exceed.size / x.size
    # T_ratio 배 관측기간에 해당하는 초과확률의 return level
    p = 1.0 / (T_ratio * rate)
    return float(u + stats.genpareto.ppf(1 - p, c, loc=0.0, scale=scale))
print("obs GPD RL:", gpd_return_level(o_flat), "| mod GPD RL:", gpd_return_level(f_flat))

# GEV(블록 최대: 일최고 PM 연/월 블록) — SAMPLE
def gev_return_level(block_max, T=10.0):
    bm = np.asarray(block_max, float); bm = bm[np.isfinite(bm)]
    if bm.size < 10: return np.nan
    c, loc, scale = stats.genextreme.fit(bm)
    return float(stats.genextreme.ppf(1 - 1.0/T, c, loc=loc, scale=scale))
```

### CD-2 앙상블 검증: rank histogram · CRPS (앙상블 예보/기후 03·13에서 차용)

> **왜 유용?** 앙상블 대기질 예보(오존/PM 초과확률)의 **spread 적정성·확률 정확도**는 결정론 지표가 못 본다. 초과확률에는 Brier, 연속농도에는 CRPS(§25 앙상블 카드).

```python
def rank_histogram(obs_1d, ens_2d):
    """obs_1d: (T,), ens_2d: (T, m). 관측이 정렬 앙상블 내 몇 번째 순위인지 히스토그램. (SAMPLE)"""
    obs_1d = np.asarray(obs_1d, float); ens_2d = np.asarray(ens_2d, float)
    ranks = []
    for o, mem in zip(obs_1d, ens_2d):
        if not np.isfinite(o) or not np.all(np.isfinite(mem)): continue
        ranks.append(int(np.sum(mem < o)))       # 0..m
    return np.bincount(ranks, minlength=ens_2d.shape[1] + 1)

def crps_ensemble(obs_1d, ens_2d):
    """CRPS(경험 앙상블) = E|X-o| - 0.5 E|X-X'|. (Hersbach 2000) (SAMPLE — 소표본은 properscoring 권장)"""
    obs_1d = np.asarray(obs_1d, float); ens_2d = np.asarray(ens_2d, float)
    out = []
    for o, mem in zip(obs_1d, ens_2d):
        mem = mem[np.isfinite(mem)]
        if not np.isfinite(o) or mem.size == 0: continue
        t1 = np.mean(np.abs(mem - o))
        t2 = 0.5 * np.mean(np.abs(mem[:, None] - mem[None, :]))
        out.append(t1 - t2)
    return float(np.mean(out)) if out else np.nan
# 앙상블이 있으면: rank_histogram(O[:,0], ens[:,0,:]) / crps_ensemble(...)
```

### CD-3 Taylor / Target 다이어그램 (공통 — 이미 §E에서 실제 함수로 적용)

> **왜 유용?** 도메인 무관 요약그림. 대기질에선 화학종별 색으로 다종 중첩 + Target y축 bias 부호로 **종별 과대/과소** 즉시 판별(§33 ⑦). `metrics_pattern.taylor_stats/target_stats` 로 계산, `plots.taylor_diagram` 로 작도(§E·§F 참조).

---

## §G 함정 & 캡션 (Pitfalls & Captions — 그림마다 §G 캡션 강제)

- **G-1 reference ≠ truth**: 측정소·위성(TROPOMI/MODIS)·CAMS/MERRA-2 모두 reference. 축·캡션에 "모델 − 기준(reference)". 위성·재분석을 "정답"으로 단정 금지(AMF·구름·동화 오차).
- **G-2 측정소는 점 관측**: 격자 평균과 비교 시 **대표성 오차**. 도로변/산업 측정소의 "과소"는 모델 결함이 아닐 수 있음 → 측정소 유형 층화(§33 ⑫).
- **G-3 로그정규 꼬리**: 선형 bias는 소수 고농도가 지배 → 로그축·MFB/MFE·FAC2 기본. **단 오존은 로그정규 약함** → 선형·NMB 관례.
- **G-4 임계는 advisory**: Boylan&Russell MFB±30/±60%·MFE 50/75%, Emery O3 NMB±5/±15%·NME 15/25%, FAC2≥0.5, FAIRMODE MQI≤1 — **미국/유럽 사례 기반 참고선**, 지역·화학종·해상도·계절 의존. good/bad 단정 금지.
- **G-5 단일 그림 금지**: 최소 **①(로그산점+FAC2) + ③(MFB/MFE bugle) + ⑧(QQ 꼬리) + ④(초과사건)** 4장. 다지점은 ⑦+②. 총 PM2.5가 맞아도 **성분 상쇄** 의심(⑪ speciation 병행).
- **G-6 단일 지표 금지 · 정의 명시**: NMB(합산) vs MNB(평균) 혼동 금지. 0/LOD 처리규칙·오존 절단임계·paired vs unpaired 방식을 **반드시 기록**.

> plots.py의 모든 그림은 제목에 `(advisory — reference≠truth)`를 자동으로 붙인다. 도메인 특화 그림(§F-2/CD)도 동일 문구를 캡션에 넣어라.

---

## §H Figure 카탈로그 매핑 (33_fig_air_quality → 이 레시피)

| §33 그림 | 이 레시피 단계 | 함수/구현 |
|----------|----------------|-----------|
| ① 로그산점+FAC2 | §F ①, §C-2 FAC2 | `plots.scatter_si` (+로그축 수정) · `fac2()` |
| ② 측정소 위치도 | §F ②/⑭ | `plots.diff_map`(1D점→scatter+`add_basemap`) |
| ③ MFB/MFE bugle | §F-2 ③ | `mfb()/mfe()` + matplotlib |
| ④ 초과사건 performance | §F-2 ④ | `exceedance_scores()` (POD/FAR/CSI) |
| ⑤ 일변동 합성 | §F-2 ⑤ | pandas `groupby(hour_lst)` |
| ⑥ 주말효과 | §F-2(패턴) | pandas `groupby(dayofweek)` |
| ⑦ soccer/target · Taylor | §E, §F ⑦ | `metrics_pattern.target_stats/taylor_stats` · `plots.taylor_diagram` |
| ⑧ QQ(로그·꼬리) | §D, §F ⑧ | `metrics_distribution.qq_points` · `plots.qq_plot` |
| ⑨ 위성 NO2 컬럼 지도 | §F-3 ⑨ | `plots.diff_map`(2D→pcolormesh+`add_basemap`) |
| ⑩ AOD 매치업 | §C-2(FAC2/MFB)+§F① | numpy + `plots.scatter_si` |
| ⑪ PM speciation | (성분별 §C-2 반복) | `mfb/nmb` 성분별 + matplotlib stacked/box |
| ⑫ 측정소 유형 box | (pairs+메타 groupby) | pandas/seaborn boxplot |
| ⑬ 시계열+잔차 | §F ⑬ | `plots.timeseries_overlay` |
| ⑭ 재분석 bias 지도 | §F-3 | `plots.diff_map` 2D + `add_basemap` |
| ⑮ 계절 히트맵 | (pandas pivot) | seaborn heatmap |
| ⑯ FNR 체제 지도 | (위성 HCHO/NO2) | `plots.diff_map` 2D + `add_basemap` |

---

## 연관 모듈 참조 (실제 스크립트)

| 모듈 | 실제 공개 함수 | 역할 |
|------|----------------|------|
| `scripts/io_detect.py` | `open_dataset`, `detect_format` | 포맷 자동판별(nc/csv, cp949 폴백) |
| `scripts/dataset.py` | `open_nc`, `write_nc`, `Dataset`(`latlon/is_mesh/coord_kind/grid_shape/time_info/variables`) | NetCDF 로딩·좌표/mesh 추상화(한글경로 안전) |
| `scripts/preprocess.py` | `tz_to_utc`, `common_time_index`, `match_points_to_mesh`, `inject_point_coords`, `build_pairs`, `parse_points_list`, `to_kelvin` | 매치업·시간대·mesh→점 |
| `scripts/metrics_basic.py` | `bias`, `mae`, `rmse`, `nrmse`, `si`, `pearson_r`, `linregress` | 기본 오차통계(NaN 마스크) |
| `scripts/metrics_distribution.py` | `quantiles`, `qq_points`, `perkins_skill_score`, `ks_distance` | 분포·꼬리 |
| `scripts/metrics_pattern.py` | `taylor_stats`, `target_stats`, `pattern_correlation` | Taylor/Target/패턴상관 |
| `scripts/metrics_circular.py` | `circular_mean_error`, `circular_rmse`, `circular_corr` | 풍향 원형통계(선택) |
| `scripts/plots.py` | `add_basemap`, `scatter_si`, `timeseries_overlay`, `diff_map`, `qq_plot`, `taylor_diagram`, `wave_rose` | 그림(지도는 `add_basemap` 필수) |

> **도메인 특화 지표/그림(MFB/MFE·NMB/NME·FAC2·POD/FAR/CSI·bugle·일변동·speciation·극치·CRPS)** 은 스킬 함수에 없으므로 **numpy/scipy/pandas/matplotlib(+선택 xarray/xesmf/seaborn — 모두 실존)** 로 §25·§33 정의식대로 직접 구현했다.

---

## 출처 (확인된 것만; 미확인은 "(확인요)")

- Boylan & Russell (2006) *Atmospheric Environment* 40(26):4946–4959 — MFB/MFE goal·criteria·bugle.
- Emery et al. (2017) *J. Air & Waste Manage. Assoc.* 67(5):582–598, **doi:10.1080/10962247.2016.1265027** — NMB/NME/r 벤치마크.
- Chang & Hanna (2004) *Meteorol. Atmos. Phys.* 87:167–196, **doi:10.1007/s00703-003-0070-7** — FB·NMSE·FAC2·MG·VG.
- Roebber (2009) *Wea. Forecasting* 24:601–608, **doi:10.1175/2008WAF2222159.1** — performance diagram.
- Jolliff et al. (2009) *J. Marine Systems* 76:64–82, **doi:10.1016/j.jmarsys.2008.05.014** — target diagram.
- Hersbach (2000) *Wea. Forecasting* 15:559 — CRPS (앙상블). Taylor (2001) *JGR* 106(D7) — Taylor diagram.
- Eskes & Boersma (2003) *ACP* 3:1285–1291 — averaging kernel(위성 컬럼 정합).
- Gelaro et al. (2017) *J. Climate* 30:5419–5454, **doi:10.1175/JCLI-D-16-0758.1** — MERRA-2.
- Coles (2001) *An Introduction to Statistical Modeling of Extreme Values* (Springer) — POT/GPD·GEV(cross-domain 근거).
- FAIRMODE *Guidance Document on MQO and Benchmarking* (JRC) — MQI/MQO·soccer/target.
- Thunis et al. (2012) DELTA, *Environmental Modelling & Software* — 권·페이지·DOI **(확인요)**.
- Inness et al. (2019) CAMS reanalysis, *ACP* 19:3515 — DOI 패턴 **(확인요)**.
- 해석 임계(MFB±30/±60%·Emery NMB±5/±15%·FAC2≥0.5·MQI≤1)는 미국/유럽 사례 기반 **advisory** — 지역·화학종·해상도·계절 의존(§G-4).

---

*SAMPLE — 범용 스킬의 대기질 예시. 실 데이터 구조(변수명·단위·좌표·시간대)를 실시간 점검하고 도메인 맞춤 코드로 적응한 뒤 사용하라. 그대로 실행 금지.*
