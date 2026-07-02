# Recipe: 수문·하천 검증 (Hydrology / Streamflow Validation)

> ## ⚠️ SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> 이 스킬(`validate-model-output`)은 **특정 분야 전용이 아니라 범용**이다. 이 파일은 그 범용 파이프라인을
> **수문·하천(hydrology) 한 예시**로 구체화한 worked SAMPLE일 뿐이다.
> 아래 코드는 "대략적 흐름 + 출발점 템플릿"이며 완비된 코드가 아니다.
> 실 데이터(모델 유량 NetCDF·관측소 유량 CSV 등)의 **변수명·단위(m³/s vs mm/day)·시간대(KST/UTC)·
> 좌표 위상(격자/mesh)·결측기호·유량 rating 규약**에 따라 각 단계를 반드시 수정해서 사용한다.
>
> **검증 해석 원칙(§00 §G 강제)**: ① 관측유량은 수위–유량 관계식(rating curve)으로 환산된 **2차 산출**이고
> 고·저유량 극단에서 rating error가 크다 → "모델−관측(reference)"으로 쓰고 "오차"로 단정하지 마라.
> ② Moriasi 등급·KGE>0.75·Fit 0.5~0.8은 **월단위·특정 유역군 advisory**이며 일/시·건조·소유역에선 낮게 나오는 게 정상.
> ③ NSE<0 또는 **KGE<−0.41**이면 "평균유량 benchmark만도 못함"(Knoben 2019) → benchmark 대비 상대평가.
> ④ **단일 그림/지표 금지** — 최소 3축(수문곡선/위상 + FDC/분포 + KGE 성분/원인).

---

## 빠른 참조 (Quick Reference) — 단계 → 실제 스킬 함수 → 대응 그림카드

| 단계 | 실제 스킬 함수 (모듈.함수) | 대응 Figure 카드(34_fig_hydrology) |
|------|---------------------------|-------------------------------------|
| A. 열기·구조 점검 | `io_detect.open_dataset` · `io_detect.detect_format` · `dataset.open_nc` · `Dataset.data_var_names/variable/latlon/coord_kind/grid_shape/time_info` | — |
| B. 정점 매치업·tz | `preprocess.tz_to_utc` · `preprocess.common_time_index` · `preprocess.match_points_to_mesh` · `preprocess.inject_point_coords` · `preprocess.build_pairs` | ⑯ 관측소 위치도 |
| C. 다축 정확도 지표 | `metrics_basic.bias/mae/rmse/si/nrmse/pearson_r/linregress` | ③ 유량 산점도(log) |
| D. 분포·서명 | `metrics_distribution.qq_points/perkins_skill_score/ks_distance` (+ FDC/서명은 numpy) | ② FDC · ⑪ FDC 서명 편향 |
| E. 종합 패턴 | `metrics_pattern.taylor_stats/target_stats/pattern_correlation` | (공통) Taylor/Target · ④ KGE 성분 |
| F. 그림 | `plots.scatter_si` · `plots.timeseries_overlay` · `plots.qq_plot` · `plots.diff_map`(add_basemap 내장) · `plots.taylor_diagram` · `plots.add_basemap` | ①③②⑦⑯ 등 |
| G. 도메인 특이지표 | KGE/KGE′·NSE·PBIAS·FDC·감수·홍수빈도 = numpy/scipy(+선택 실존 라이브러리) | ④⑤⑥⑫⑬ |
| ★ Cross-domain | DTW·lag상관(06) · 웨이블릿/스펙트럼(05) · 극치 POT/GEV(03) | ①⑤ 보강 |

> **도메인 특이지표(KGE/NSE/FDC/감수/홍수빈도)는 이 스킬 스크립트에 전용 함수가 없다.**
> 아래 §G에서 **numpy/scipy로 직접** 구현하거나(권장, 의존성 0) **실존 라이브러리**
> (`HydroErr`·`spotpy`·`hydrosignatures`·`pyextremes`·`lmoments3`·`baseflow`)로 계산한다. 지어낸 함수는 없다.

---

## §A 열기 · 구조/메타 점검 (Open & Inspect)

대표 자료형: **[시계열] 하천 유량 점(관측소) CSV** + **[격자/mesh] 모델 유량 NetCDF**.

```python
# SAMPLE — 실데이터 경로·변수명·인코딩을 반드시 실시간 점검하라.
# 이 스킬은 scripts/ 를 플랫 모듈로 import 한다(패키지 아님).
import sys, os
SKILL = os.environ.get("SKILL", os.getcwd())   # $SKILL = 스킬 설치 폴더(설치 위치/CLI 인자로 교체)
sys.path.insert(0, os.path.join(SKILL, "scripts"))

from io_detect import open_dataset, detect_format      # 실제 함수
from dataset import open_nc, Dataset                    # 실제 함수/클래스

# --- A-1 포맷 자동 판별 + 열기 (CDF/HDF/CSV; 한글 경로·cp949 폴백 내장) ---
fmt = detect_format("model_discharge.nc")   # "netcdf3" | "netcdf4" | "csv" | "unknown"
d   = open_dataset("model_discharge.nc")     # -> dataset.Dataset (xarray 래핑)
# CSV 관측도 동일 진입점: obs = open_dataset("gauge_obs.csv")

# --- A-2 구조·메타 점검 (실제 Dataset 메서드) ---
print(d.data_var_names())        # 예: ['discharge', 'runoff', 'lat', 'lon', ...]
v = d.variable("discharge")      # Variable(name, dims, shape, units, standard_name, long_name, attrs)
print(v.units, v.dims, v.shape)  # ← 단위가 'm3 s-1' 인지 'mm/day' 인지 반드시 확인 (SAMPLE)

print(d.coord_kind())   # "1d" | "2d" | "mesh" | "none"
print(d.latlon())       # (lat_name, lon_name, is_2d) | None
print(d.grid_shape())   # 격자 (ny,nx)/(nlat,nlon) 또는 mesh (n_nodes,)
print(d.time_info())    # {"name","n_steps","start","end"} | None  ← tz 표기 확인
print(d.is_mesh())      # WRF-Hydro/NWM route link 등 mesh면 True
```

> **실데이터 점검 항목 (수문 특이)**
> - 유량 단위: **체적유량 m³/s** vs **격자 유출 깊이 mm/day** — 혼동 시 유역면적 A로 환산 필요(`Q[m³/s]=runoff[mm/day]·A[km²]/86.4`). (SAMPLE — 네 유역면적으로 수정)
> - 관측소 시각: **KST(+09:00) 흔함** → §B `tz_to_utc` 로 UTC 정렬 (모델은 보통 UTC).
> - 결측기호: 관측 CSV의 `-`, `999`, `9999`, `-9999` 등 → `open_dataset`은 그대로 읽으므로 아래에서 마스킹.
> - 0유량(간헐하천)·음수유량(rating 외삽) → log지표·CV 계산 전 처리 규약 명시.

---

## §B 정점 매치업 · 시간대 (Station Matchup & TZ)

```python
# SAMPLE — 관측 CSV 컬럼명·na 기호·tz 는 네 파일에 맞춰 바꿔라.
import numpy as np
import pandas as pd
from preprocess import tz_to_utc, common_time_index, match_points_to_mesh, \
                       inject_point_coords, build_pairs   # 실제 함수

# --- B-1 관측 CSV (cp949 + 한글 컬럼 alias) ---
obs = pd.read_csv("gauge_obs.csv", encoding="cp949",
                  na_values=["-", "999", "9999", "-9999"])   # ← na 기호 SAMPLE
ALIAS = {"일시": "datetime", "관측소": "station_id", "유량(m3/s)": "q_obs"}  # ← 헤더 SAMPLE
obs = obs.rename(columns={k: v for k, v in ALIAS.items() if k in obs.columns})

# --- B-2 시간대 정규화: 관측 KST → UTC (모델 UTC 가정) ---
# tz_to_utc 반환: (times_utc: datetime64[ns], assumed: bool)  ← assumed=True면 tz 미확인 경고
obs_t_utc, assumed = tz_to_utc(obs["datetime"].values, tz="KST")  # ← 실데이터 tz 로 수정
if assumed:
    print("경고: 관측 tz 미확인 → UTC 가정. KST면 tz='KST' 명시하라.")

# --- B-3 모델 mesh → 관측점 최근접 노드 매칭 (WRF-Hydro/NWM 등 mesh일 때) ---
# 정규 격자면 이 블록 대신 d.xr.sel(lat=..., lon=..., method="nearest") 사용 (SAMPLE)
if d.is_mesh():
    lat_name, lon_name = "latitude", "longitude"    # ← mesh 좌표 data_var 명 확인 후 수정
    mesh_lat = d.xr[lat_name].values                # shape (N_node,)
    mesh_lon = d.xr[lon_name].values
    # 관측소 ID → 위경도 (mapping 은 네 관측망 메타로 구성)
    STN = {"1018680": (37.54, 127.30), "1007625": (37.20, 127.05)}  # {id:(lat,lon)} SAMPLE
    lats, lons = inject_point_coords(list(STN), STN)
    idx, dist_km = match_points_to_mesh(mesh_lon, mesh_lat, lons, lats, max_km=5.0)
    # 실데이터: 대표성 오차 → 최근접 거리 로그로 남겨라 (max_km 초과는 idx=-1)
    print("최근접 노드 거리(km):", dist_km)   # 큰 거리는 비교 품질 저하 → 캡션에 기록

# --- B-4 모델·관측 시각 교집합 정렬 ---
model_t = d.time_info()   # {"name",...}; 실제 시각축은 d.xr[model_t["name"]].values
mt = np.asarray(d.xr[model_t["name"]].values, dtype="datetime64[ns]")
i_obs, i_mod = common_time_index(obs_t_utc, mt)   # 교집합 인덱스 (정렬)
# 정렬된 매치업 벡터 (한 관측소 예; 다지점은 build_pairs 로 롱포맷)
q_obs = obs["q_obs"].values[i_obs]
q_mod = d.xr["discharge"].values                  # shape 조정 필요 (SAMPLE: [time, node])
q_mod = q_mod[i_mod, idx[0]] if d.is_mesh() else q_mod[i_mod]
```

> **함정(수문)**: KST↔UTC 9h 어긋남이 **가짜 위상오차**를 만든다(§06 lag로 검출). mesh 최근접 거리가
> 크면 대표성 오차(점 vs 격자평균) → §26 물수지·FDC 해석에 주의. 인위취수·저수지 하류 관측소는
> 자연유량 모델과 직접 비교 부적절(자연화 여부 명시).

---

## §C 다축 정확도 지표 (Accuracy Metrics — 실제 함수)

Figure: **③ 유량 검증 산점도(log·KGE/NSE box)**

```python
# SAMPLE — 실제 metrics_basic 함수 사용. 인자 순서는 (f, o) = (forecast/model, obs)!
from metrics_basic import bias, mae, rmse, si, nrmse, pearson_r, linregress  # 실제 함수

def accuracy_row(q_mod, q_obs) -> dict:
    """다축 정확도 — 실제 스킬 함수만 사용 (NaN 마스크는 각 함수 내장)."""
    slope, intercept = linregress(q_mod, q_obs)   # f ~ slope*o + intercept
    return {
        "n":      int(np.sum(np.isfinite(q_mod) & np.isfinite(q_obs))),
        "bias":   bias(q_mod, q_obs),      # mean(f-o) ; + = 과대추정
        "mae":    mae(q_mod, q_obs),
        "rmse":   rmse(q_mod, q_obs),
        "si":     si(q_mod, q_obs),        # 불편RMSE/|mean(o)| (Scatter Index)
        "nrmse":  nrmse(q_mod, q_obs),     # RMSE/|mean(o)|
        "r":      pearson_r(q_mod, q_obs),
        "slope":  slope, "intercept": intercept,
    }

row = accuracy_row(q_mod, q_obs)
print(f"Bias={row['bias']:.2f} m3/s  RMSE={row['rmse']:.2f}  SI={row['si']:.3f}  r={row['r']:.3f}")
```

> **주의**: 유량은 동적범위가 커(홍수~갈수 수백~수천 배) RMSE/bias는 **첨두에 지배**된다.
> → 반드시 §G 로그변환 지표(lnNSE·KGE_log)·§D FDC와 병행. `si`·`nrmse` 분모(|mean o|)는 §00에서
> 정의차가 있으니(range/std 사례) 실데이터 규약 명시.

---

## §D 분포 · 유황곡선 서명 (Distribution & FDC Signatures)

Figure: **② FDC(로그 종축)**, **⑪ FDC 서명 편향(FHV·FLV·FMS)**

```python
# SAMPLE — 실제 metrics_distribution 함수 + 수문 고유 FDC(numpy 직접).
from metrics_distribution import qq_points, perkins_skill_score, ks_distance  # 실제 함수

# --- D-1 분포 일치 (실제 함수; timing 무관) ---
obs_q, mod_q = qq_points(q_obs, q_mod, n_quantiles=50)   # QQ 분위점 쌍
pss = perkins_skill_score(q_obs, q_mod, bins=30)         # 분포 공통면적 [0,1]
ksd = ks_distance(q_obs, q_mod)                          # KS D (최대 CDF 차)
print(f"Perkins SS={pss:.3f}  KS D={ksd:.3f}")

# --- D-2 유황곡선 FDC (수문 고유; Weibull plotting position, numpy 직접) ---
def fdc(q):
    """FDC: (초과확률 p, 내림차순 유량). p = m/(n+1) (Weibull)."""
    q = np.asarray(q, float); q = q[np.isfinite(q)]
    qs = np.sort(q)[::-1]
    n = qs.size
    p = np.arange(1, n + 1) / (n + 1)     # 초과확률
    return p, qs
p_o, q_o_fdc = fdc(q_obs)
p_m, q_m_fdc = fdc(q_mod)

# --- D-3 FDC 서명 편향 (Yilmaz 2008: FHV 상위2%, FLV 하위30% 로그, FMS 20~70% 기울기) ---
def fdc_signatures(q_obs, q_mod):
    def hv(q, hi=0.02):                     # high-flow volume (상위 hi 비율)
        qs = np.sort(q[np.isfinite(q)])[::-1]; k = max(1, int(len(qs) * hi))
        return qs[:k].sum()
    def lv(q, lo=0.30):                     # low-flow volume, 로그공간 (하위 lo 비율)
        qs = np.sort(q[np.isfinite(q)]); k = max(1, int(len(qs) * lo))
        qs = qs[:k]; qs = qs[qs > 0]
        return -np.sum(np.log(qs) - np.log(qs.min())) if qs.size else np.nan
    def fms(q, lo=0.2, hi=0.7):             # mid-segment FDC slope (log)
        qs = np.sort(q[np.isfinite(q)] )[::-1]; n = len(qs)
        q1, q2 = qs[int(n*lo)], qs[int(n*hi)]
        return (np.log(q1) - np.log(q2)) if q1 > 0 and q2 > 0 else np.nan
    return {
        "pBiasFHV": 100 * (hv(q_mod) - hv(q_obs)) / hv(q_obs),      # −=첨두 과소
        "pBiasFMS": 100 * (fms(q_mod) - fms(q_obs)) / abs(fms(q_obs)),
        "Q5_obs":  np.nanpercentile(q_obs, 95),  "Q5_mod": np.nanpercentile(q_mod, 95),  # 5%초과=95백분위
        "Q95_obs": np.nanpercentile(q_obs, 5),   "Q95_mod": np.nanpercentile(q_mod, 5),
    }
sig = fdc_signatures(q_obs, q_mod)   # ← 구간정의(2%/30%/20~70%)는 Yilmaz 규약 SAMPLE, 문헌마다 다름
```

> **함정**: FDC는 **동시성·timing을 못 본다**(상관 0이어도 FDC 완벽 가능) → §C·수문곡선과 상보.
> 기간이 다르면 직접비교 불가. 로그축 시각 왜곡 → 서명(FHV/FLV/FMS)으로 정량 병행. 0유량 로그처리 규약 명시.

---

## §E 종합 패턴 (Taylor / Target — 실제 함수)

Figure: **(공통) Taylor/Target**, **④ KGE 성분**

```python
# SAMPLE — 실제 metrics_pattern 함수. 인자 순서 (o, f) = (obs, forecast)에 주의!
from metrics_pattern import taylor_stats, target_stats, pattern_correlation  # 실제 함수

tay = taylor_stats(q_obs, q_mod)   # {"std_ratio","corr","crmsd","n"}
tar = target_stats(q_obs, q_mod)   # {"bias","urmsd","rmsd","n"}
# 다지점/다변수를 한 Taylor에 겹쳐 유역 특성 파악 (로그유량으로도 반복 권장)
```

---

## §F 그림 (Plots — 실제 함수; 지도형은 add_basemap 필수)

```python
# SAMPLE — 실제 plots 함수. scatter/timeseries/qq 는 (o, f) 순, out_png 경로 지정.
from plots import scatter_si, timeseries_overlay, qq_plot, diff_map, \
                  taylor_diagram, add_basemap   # 실제 함수

scatter_si(q_obs, q_mod, "out/fig03_scatter.png", units="m3/s")        # ③ 산점(1:1+OLS+SI)
timeseries_overlay(mt[i_mod], q_obs, q_mod, "out/fig01_hydrograph.png") # ① 수문곡선 overlay
qq_plot(q_obs, q_mod, "out/fig_qq.png")                                 # QQ
taylor_diagram(q_obs, q_mod, "out/fig_taylor.png")                     # 공통 Taylor

# ⑦ 유역별 KGE 지도 / ⑯ 관측소 위치도 — ★ 지도형: add_basemap 로 해안선+위경도 필수
import matplotlib.pyplot as plt
from plots import _make_geo_axes            # cartopy 있으면 GeoAxes, 없으면 fallback
fig, ax, tr = _make_geo_axes(figsize=(6, 5))
kw = {"transform": tr} if tr is not None else {}
kge_per_stn = [ ... ]                        # ← §G KGE 를 관측소별로 계산해 채워라 (SAMPLE)
sc = ax.scatter(lons, lats, c=kge_per_stn, cmap="viridis", vmin=-0.41, vmax=1.0, s=60, **kw)
add_basemap(ax, lons, lats)                  # ★ 해안선·육지·위경도 라벨(오프라인이면 격자선 fallback)
fig.colorbar(sc, ax=ax, label="KGE (benchmark −0.41)")
ax.set_title("Per-station KGE (advisory — reference≠truth)")
fig.savefig("out/fig07_kge_map.png", dpi=100, bbox_inches="tight")

# 격자 편차 지도(모델−관측 유출)면 diff_map 이 add_basemap 을 자동 호출
# diff_map(lat2d, lon2d, (runoff_mod - runoff_obs), "out/fig_diffmap.png", units="mm/day")
```

> `plots.scatter_si`는 내부 SI를 `RMSE/mean(|obs|)×100 [%]`로 계산(§C `si`의 불편RMSE 정의와 다름) — 캡션 명시.
> 유량 산점은 로그축이 사실상 필수지만 `scatter_si`는 선형이므로, 저유량 구조를 보려면 로그값을 넣거나 커스텀.

---

## §G 도메인 특이 지표 (KGE/NSE·PBIAS·감수·홍수빈도 — 실존 라이브러리)

Figure: **④ KGE 성분**, **⑤ 홍수빈도**, **⑥ 수문서명 radar**, **⑫ 기저분리**, **⑬ 감수**

이 지표들은 스킬 스크립트에 전용 함수가 없다 → **numpy/scipy 직접**(의존성 0) 또는 **실존 라이브러리**.

```python
# --- G-1 NSE / lnNSE / PBIAS / RSR (numpy 직접; Nash&Sutcliffe 1970, Moriasi 2007) ---
def nse(sim, obs):
    m = np.isfinite(sim) & np.isfinite(obs); s, o = sim[m], obs[m]
    return 1.0 - np.sum((s - o)**2) / np.sum((o - o.mean())**2)
def ln_nse(sim, obs, eps=None):
    eps = eps if eps else 0.01 * np.nanmean(obs)   # ← ε 규약 명시 (0유량 처리)
    return nse(np.log(sim + eps), np.log(obs + eps))
def pbias(sim, obs):                                # 100·Σ(sim−obs)/Σobs (부호규약 명시!)
    m = np.isfinite(sim) & np.isfinite(obs); s, o = sim[m], obs[m]
    return 100.0 * np.sum(s - o) / np.sum(o)
def rsr(sim, obs):                                  # RMSE / STDEV_obs = sqrt(1−NSE)
    return np.sqrt(1.0 - nse(sim, obs))

# --- G-2 KGE(2009) / KGE′(2012) + 성분 분해 r·β·α (Gupta 2009; Kling 2012) ---
def kge_components(sim, obs, variant="2012"):
    m = np.isfinite(sim) & np.isfinite(obs); s, o = sim[m], obs[m]
    r = np.corrcoef(s, o)[0, 1]
    beta = s.mean() / o.mean()                              # 편향비 (총량)
    if variant == "2012":
        alpha = s.std() / o.std()                           # KGE′ 변동비 α (진폭)
        kge = 1 - np.sqrt((r-1)**2 + (beta-1)**2 + (alpha-1)**2)
        return {"kge_prime": kge, "r": r, "beta": beta, "alpha": alpha}
    gamma = (s.std()/s.mean()) / (o.std()/o.mean())         # KGE(2009) 변동비 γ = CV비
    kge = 1 - np.sqrt((r-1)**2 + (beta-1)**2 + (gamma-1)**2)
    return {"kge": kge, "r": r, "beta": beta, "gamma": gamma}

comp = kge_components(q_mod, q_obs, variant="2012")   # ← 어느 정의(2009 γ/2012 α)인지 캡션 명시
# 해석: α<1=변동 과소(첨두 눌림), β>1=과대추정, r 낮음=timing/형상. benchmark: KGE<−0.41 이면 평균만도 못함.

# --- G-2b (선택) 실존 라이브러리로 동일 계산: HydroErr / spotpy ---
# import HydroErr as he;  he.kge_2012(q_mod, q_obs);  he.nse(q_mod, q_obs);  he.pbias(q_mod, q_obs)
# import spotpy;  spotpy.objectivefunctions.kge(q_obs, q_mod, return_all=True)  # (kge,r,β,α)

# --- G-3 기저유출 분리 · BFI (Lyne–Hollick 1979 디지털필터; numpy) ---
def lyne_hollick_bfi(q, a=0.925, passes=3):     # ← α·passes 모델/관측 동일 적용 필수
    q = np.asarray(q, float); qf = q.copy()
    for _ in range(passes):
        f = np.zeros_like(qf); f[0] = qf[0]
        for t in range(1, len(qf)):
            f[t] = a*f[t-1] + (1+a)/2*(qf[t]-qf[t-1])
        qf = np.clip(qf - np.maximum(f, 0), 0, None)  # 기저 = 총 − 직접
    base = q - (q - qf); base = np.minimum(qf, q)
    return base, np.nansum(base) / np.nansum(q)       # BFI = Σbase/Σq
# base_o, bfi_o = lyne_hollick_bfi(q_obs);  base_m, bfi_m = lyne_hollick_bfi(q_mod)
# (선택) 실존: `baseflow` (PyPI, 다중필터) / `hydrosignatures`(HyRiver)

# --- G-4 감수분석 Brutsaert–Nieber −dQ/dt = a·Q^b (log-log 회귀; numpy) ---
def recession_bn(q):
    q = np.asarray(q, float); dq = -np.diff(q)
    m = (dq > 0) & (q[:-1] > 0)                        # 감수구간만
    x, y = np.log(q[:-1][m]), np.log(dq[m])
    b, loga = np.polyfit(x, y, 1)                      # 기울기 b≈1=선형저수지, b>1 비선형
    return {"b": b, "a": np.exp(loga)}
# (선택) 실존: `hydrosignatures`(HyRiver) recession 유틸

# --- G-5 홍수빈도: 연최대 GEV (scipy.stats.genextreme; POT는 genpareto) ---
from scipy import stats
def flood_frequency_gev(q, times, return_periods=(2,5,10,50,100)):
    df = pd.DataFrame({"q": q}, index=pd.to_datetime(times))
    ams = df["q"].resample("YS").max().dropna().values   # 연최대 (AMS)
    c, loc, scale = stats.genextreme.fit(ams)            # L-모멘트 원하면 lmoments3
    rl = {T: float(stats.genextreme.ppf(1 - 1/T, c, loc, scale)) for T in return_periods}
    return rl   # {재현주기: 재현유량}  ← 부트스트랩 CI 필수, 임계·표본수 민감
# (선택) 실존: `pyextremes`(EVA: get_extremes 'BM'/'POT', fit_model 'GEV'/'GPD', plot_return_values)
#            `lmoments3` (L-모멘트), scipy.stats.pearson3 (LP3, log변환)
```

> **§G 공통 함정**: ① 모든 지표는 **benchmark 대비**(NSE=0·KGE=−0.41) 상대평가. ② 감수·기저분리·홍수빈도는
> 사건선택·필터파라미터·declustering·표본수에 **극도로 민감** → 방법 고정·명시 + 블록 부트스트랩 CI.
> ③ 저유량/고유량 극단은 관측 rating error 최대 → 모델 탓 단정 금지.

---

## §★ Cross-domain 적용 (필수 절 — 타 도메인 기법을 이 데이터에 실제 적용)

수문 관행이 아니어도 **유량 시계열에 유용한** 타 도메인 기법. 각 기법에 "왜 여기서 유용한가" + 실제 스니펫.

### ★1 DTW · lag 상관 — 수문곡선 위상오차 (06 시계열/신호에서 차용)

> **왜 유용?** 첨두 timing이 어긋나면 KGE r이 부당하게 낮아진다. **lag 상관**은 계통 시간지연(도달시간·저류
> 과다)을 분리해 "형상은 맞는데 늦다"를 정량화하고, **DTW**는 비선형 위상 뒤틀림(사건마다 다른 지연)까지 정렬거리로 잰다.

```python
# SAMPLE — lag 상관(numpy)로 최적 지연·계통 위상오차 검출
def lag_correlation(q_obs, q_mod, max_lag=24):    # 시자료면 max_lag=24 → ±24h
    m = np.isfinite(q_obs) & np.isfinite(q_mod); o, f = q_obs[m], q_mod[m]
    lags, corrs = [], []
    for L in range(-max_lag, max_lag+1):
        if   L < 0: r = np.corrcoef(o[-L:], f[:L])[0,1] if -L < len(o) else np.nan
        elif L > 0: r = np.corrcoef(o[:-L], f[L:])[0,1] if  L < len(o) else np.nan
        else:       r = np.corrcoef(o, f)[0,1]
        lags.append(L); corrs.append(r)
    best = lags[int(np.nanargmax(corrs))]
    return {"best_lag": best, "r_at_best": np.nanmax(corrs)}   # best_lag≠0 → 계통 timing 오차
# DTW (선택, 실존 라이브러리): from dtaidistance import dtw; dtw.distance(q_obs, q_mod)
#   또는 tslearn.metrics.dtw — 사건별 비선형 위상뒤틀림 정렬거리
```

### ★2 웨이블릿 / 스펙트럼 — 계절·저수기 주기 구조 (05 스펙트럼에서 차용)

> **왜 유용?** 유량엔 연주기·계절·저수기(다년) 신호가 겹친다. **스펙트럼/웨이블릿**으로 모델이 계절진폭·주기적
> 저류 리듬을 재현하는지(FDC·NSE가 못 보는 주파수영역)를 진단한다. 온난편향→융설 조기화가 연주기 위상 이동으로 보인다.

```python
# SAMPLE — Welch 파워스펙트럼으로 연/계절 피크 비교 (scipy.signal, 실존)
from scipy import signal
def spectrum_compare(q_obs, q_mod, fs=1.0):    # fs: 샘플/day (일자료면 1.0)
    o = np.nan_to_num(q_obs - np.nanmean(q_obs))
    f = np.nan_to_num(q_mod - np.nanmean(q_mod))
    fo, Po = signal.welch(o, fs=fs, nperseg=min(365, len(o)))
    fm, Pm = signal.welch(f, fs=fs, nperseg=min(365, len(f)))
    return (fo, Po), (fm, Pm)   # 1/365 day⁻¹ 부근 연주기 피크 진폭·위치 비교
# 웨이블릿(선택, 실존): import pywt; cwt,freqs = pywt.cwt(q, scales, "morl") — 저수기 주기의 시간변화
```

### ★3 극치 POT/GPD — 임계초과 첨두의 상위꼬리 (03 극치에서 차용)

> **왜 유용?** 연최대(AMS)만 쓰면 표본이 적다. **POT(peaks-over-threshold)+GPD**는 임계 초과 첨두를 모두 써
> 상위꼬리(설계홍수) 적합을 강화한다. 홍수예보·구조물 설계에서 §G-5 GEV의 상보 기법.

```python
# SAMPLE — POT + GPD (scipy.stats.genpareto, 실존). declustering·임계는 실데이터로 조정
from scipy import stats
def pot_gpd(q, thresh_pct=95, min_sep=3):          # 임계 = 95백분위, 첨두 최소간격 SAMPLE
    q = np.asarray(q, float)
    u = np.nanpercentile(q, thresh_pct)
    peaks_idx = signal.find_peaks(np.nan_to_num(q), height=u, distance=min_sep)[0]  # declustering
    exc = q[peaks_idx] - u
    c, loc, scale = stats.genpareto.fit(exc, floc=0)
    lam = len(exc) / (np.sum(np.isfinite(q)))       # 평균 초과율
    def return_level(T):                            # N년 재현유량
        return u + stats.genpareto.ppf(1 - 1/(T*lam*365), c, loc, scale)
    return {"threshold": u, "shape_c": c, "scale": scale, "RL100": return_level(100)}
# (선택) 실존: pyextremes EVA(get_extremes 'POT', fit_model 'GPD')
```

> **cross-domain 공통 주의**: 이 기법들도 §00 §G 원칙 그대로 — reference≠truth, 단일지표 금지,
> 결과는 블록 부트스트랩 CI로 유의성 확인. 자기상관 강한 일유량은 유효표본 과대(과신) 주의.

---

## §H 함정 및 주의사항 (Pitfalls — 수문 특이)

1. **단위/면적 환산**: 격자 유출(mm/day) ↔ 관측 체적유량(m³/s)은 유역면적으로 환산. 혼용 시 PBIAS·물수지 전면 왜곡.
2. **시간대·시각기준**: 관측 KST vs 모델 UTC 9h; 순간값 vs 일평균/윈도우 불일치 → 가짜 위상오차(§B `tz_to_utc`, ★1 lag).
3. **rating error**: 관측유량은 2차 산출, 고·저유량 외삽 구간 불확실 최대 → 첨두·감수 잔차를 모델 탓으로 단정 금지.
4. **0유량·간헐하천**: log지표·CV·KGE α 불안정 → ε 규약 명시 또는 zero-flow 별도 지표.
5. **인위영향**: 저수지 방류·취수·유역간 이동 → 자연유량 모델과 직접비교 부적절(자연화·기간 명시).
6. **benchmark 상대평가**: NSE<0 / KGE<−0.41 이면 평균유량만도 못함 → 절대임계보다 skill로 판정.
7. **단일 그림/지표 금지**: 최소 ①수문곡선(위상) + ②FDC(분포) + ④KGE 성분(원인) 3축.

---

## §I 권장 보고 세트 (Figures Bundle)

| 목적 | 그림(34_fig 카드) | 지표(26 카드) |
|------|-------------------|----------------|
| 기본 3축 | ① 수문곡선 overlay · ② FDC · ④ KGE 성분 | KGE/NSE·성분 r/β/α · FDC 서명 |
| 정확도 | ③ 유량 산점(log) | bias·rmse·si·r (metrics_basic) |
| 극치·설계 | ⑤ 홍수빈도(재현주기) | GEV/GPD·N년값·부트스트랩 CI |
| 다서명 종합 | ⑥ 수문서명 radar | FDC·BFI·감수 k·CT·runoff ratio |
| 대표본·광역 | ⑦ 유역별 KGE 지도(add_basemap) · ⑩ boxplot/CDF | KGE·NSE 분포·benchmark skill |
| 물수지·저류 | ⑨ 물수지 closure · ⑮ GRACE TWS | 잔차·runoff ratio · TWSA |
| 사건 첨두 | ⑧ 첨두 timing 산점 | peak error·timing error |
| 저유량·물리 | ⑪ FDC 서명 · ⑫ 기저분리 · ⑬ 감수 | FHV/FLV/FMS · BFI · k,b |
| 맥락(다지점) | ⑯ 관측소 위치도(add_basemap) | (위치) |

---

## 연관 모듈 참조 (실제 스크립트)

| 모듈 | 실제 인터페이스 | 역할 |
|------|-----------------|------|
| `scripts/io_detect.py` | `open_dataset`, `detect_format` | 포맷 판별·열기(nc/csv, cp949 폴백) |
| `scripts/dataset.py` | `open_nc`, `Dataset(.latlon/.coord_kind/.grid_shape/.time_info/.is_mesh/.variable)` | NetCDF 로딩·좌표 추상화 |
| `scripts/preprocess.py` | `tz_to_utc`, `common_time_index`, `match_points_to_mesh`, `inject_point_coords`, `build_pairs` | tz·시각정렬·mesh 매치업 |
| `scripts/metrics_basic.py` | `bias/mae/rmse/si/nrmse/pearson_r/linregress` | 기본 오차통계 |
| `scripts/metrics_distribution.py` | `qq_points/perkins_skill_score/ks_distance` | 분포 비교 |
| `scripts/metrics_pattern.py` | `taylor_stats/target_stats/pattern_correlation` | Taylor/Target 통계 |
| `scripts/metrics_circular.py` | `circular_mean_error/circular_rmse/circular_corr` | (수문 통상 미사용; 풍향 등 순환량 필요시) |
| `scripts/plots.py` | `scatter_si/timeseries_overlay/qq_plot/diff_map/taylor_diagram/wave_rose/add_basemap` | 그림(지도형 add_basemap 필수) |

---

## 출처 (References — 확인된 것만; 미확인은 "(확인요)")

- Nash & Sutcliffe (1970) *Journal of Hydrology* 10(3):282–290. (NSE)
- Gupta, Kling, Yilmaz & Martinez (2009) *Journal of Hydrology* 377(1–2):80–91, doi:10.1016/j.jhydrol.2009.08.003. (KGE)
- Kling, Fuchs & Paulin (2012) *Journal of Hydrology* 424–425:264–277. (KGE′; 권·페이지 확인요)
- Knoben, Freer & Woods (2019) *HESS* 23:4323–4331, doi:10.5194/hess-23-4323-2019. (NSE↔KGE benchmark)
- Moriasi et al. (2007) *Transactions of the ASABE* 50(3):885–900. (PBIAS/RSR/NSE 등급 — 월단위 advisory)
- Yilmaz, Gupta & Wagener (2008) *WRR* 44:W09417, doi:10.1029/2007WR006716. (FDC 서명 FHV/FLV/FMS)
- Vogel & Fennessey (1994) *J. Water Resources Planning and Management* 120(4):485–504. (FDC)
- Lyne & Hollick (1979) *Institute of Engineers Australia Nat. Conf.*:89–93. (기저분리 필터; 페이지 확인요)
- Eckhardt (2005) *Hydrological Processes* 19(2):507–515, doi:10.1002/hyp.5675. (기저분리 재귀필터)
- Brutsaert & Nieber (1977) *WRR* 13(3):637–643. (감수분석)
- Coles (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer. (GEV/GPD·POT)
- Hosking & Wallis (1997) *Regional Frequency Analysis (L-Moments)*, Cambridge.
- England et al. (2019) *USGS Techniques and Methods 4-B5* (Bulletin 17C). (LP3 홍수빈도)
- WMO, *Guide to Hydrological Practices* (WMO-No. 168); *Manual on Low-flow* (WMO-No. 1029).
- 소프트웨어(실존): `numpy`·`scipy`(signal.find_peaks·stats.genextreme/genpareto/pearson3)·`pandas`·`xarray`·
  `matplotlib`·`cartopy`; `HydroErr`(github.com/BYU-Hydroinformatics/HydroErr)·`spotpy`(Houska 2015, *PLOS ONE*
  10(12):e0145180)·`hydrosignatures`(HyRiver, docs.hyriver.io)·`pyextremes`(georgebv.github.io/pyextremes)·
  `lmoments3`(pypi)·`baseflow`(pypi)·`dtaidistance`/`tslearn`(DTW)·`pywt`(웨이블릿).
- Cross-domain 방법카드 출처: 06 시계열/신호(lag·DTW), 05 스펙트럼/웨이블릿, 03 극치(GEV/POT) — research/ 카드 참조.

---

*SAMPLE — 이 스킬은 범용이며 이 파일은 수문·하천 한 예시다. 실 데이터 구조를 실시간 점검 후 도메인 맞춤 수정하라. 그대로 실행 금지.*
