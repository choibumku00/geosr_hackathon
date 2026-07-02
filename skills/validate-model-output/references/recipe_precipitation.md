# Recipe: 강수 검증 (Precipitation Validation)

> ## SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> 이 스킬(`validate-model-output`)은 **특정 분야 전용이 아니라 범용**이다.
> 이 파일은 그 범용 검증 파이프라인을 **강수(precipitation) 한 예시**로 풀어 쓴
> worked SAMPLE 레시피일 뿐이며, 완비된 실행 코드가 아니다.
> 실 데이터(모델 NetCDF·우량계 CSV·IMERG/레이더 격자 등)의 **변수명·단위·누적창·좌표
> 위상·wet 임계**에 따라 각 단계를 반드시 수정해서 사용한다.
> - 아래 코드의 `# SAMPLE` 주석이 붙은 줄은 **네 데이터에 맞게 바꿔야 하는 자리**다.
> - reference(우량계·IMERG·ERA5·레이더 QPE)는 **참값(truth)이 아니라 기준(reference)** 이다.
> - 강수는 **간헐·비대칭·국소** → **단일 임계·단일 지표·단일 그림 금지**(§H).

---

## 0. 이 레시피가 다루는 자료형 (Data Form)

대표 자료형 = **격자(gridded) 강수 [격자] + (선택) 우량계 점 [시계열]**
- **[격자]**: 모델/재분석/위성 L3·L4/레이더 QPE (NetCDF, `time × lat × lon` 또는 mesh).
  강수 고유 성질 — 값 다수가 0(**간헐성**), 양수·오른쪽으로 **두꺼운 꼬리**, 위치가 국소(**patchy**)라 위치오차가 double-penalty.
- **[시계열]**: 우량계·AWS 관측소 CSV(정점). cp949 인코딩·KST(+09) 시각·한글 컬럼이 흔함.

> 강수 검증은 연속 오차지표(RMSE)만으로 부족하다. 방법 카드
> `references/research/23_domain_precipitation.md` 근거에 따라
> **범주형(POD/FAR/CSI/GSS/HSS)·이웃(FSS)·분포(강도 PDF·QQ)·극치(POT-GPD/GEV·ETCCDI)·공간지도**
> 를 함께 본다.

---

## 빠른 참조 (Quick Reference)

| 단계 | **실제 스킬 함수** (module.func) | 대응 그림 카드 (`figures/31_fig_precipitation.md`) |
|------|--------------------------------|--------------------------------------------------|
| A. 열기·구조 점검 | `io_detect.open_dataset` · `dataset.open_nc` · `Dataset.coord_kind/latlon/grid_shape/variable/time_info` | — |
| B. 전처리·매치업 | `preprocess.tz_to_utc` · `preprocess.common_time_index` · `preprocess.match_points_to_mesh` · `preprocess.inject_point_coords` · `preprocess.build_pairs` | — |
| C. 연속 오차 | `metrics_basic.bias/mae/rmse/nrmse/si/pearson_r/linregress` | ⑮ 위성 매치업 산점 · ⑪ 공간지도 |
| D. 분포·꼬리 | `metrics_distribution.qq_points/quantiles/perkins_skill_score/ks_distance` | ⑧ wet-day 강도 PDF · ⑩ 강수 QQ |
| E. 그림(공통) | `plots.scatter_si` · `plots.timeseries_overlay` · `plots.qq_plot` · `plots.taylor_diagram` · `plots.diff_map`(+`plots.add_basemap`) | ①⑮ 산점 · ⑪ bias지도 · ⑩ QQ |
| F. 종합 | `metrics_pattern.taylor_stats/target_stats/pattern_correlation` + `plots.taylor_diagram` | (공통 16 Taylor/Target) |
| G. 캡션 §G | 모든 그림에 advisory·reference≠truth 캡션(각 `plots.*` 내장) | 전 그림 |
| **강수 특화** | numpy/scipy/xarray/pandas 자작 + (실존) `pysteps`·`pyextremes`·`xclim`·`xskillscore` | ① 성능도표 · ③ FSS · ⑤ SAL · ⑬ return-level · ⑭ ETCCDI |

> **인자 순서 주의(실함수 시그니처 그대로)**:
> `metrics_basic.*(f, o)` — 예보 먼저. `metrics_pattern.*(o, f)` — 관측 먼저.
> `metrics_distribution.qq_points(obs, fct)` · `plots.scatter_si(o, f, out_png)` — 관측 먼저.
> 헷갈리면 각 §의 코드 주석을 따르라.

---

## §A 열기·구조 점검 (Open & Inspect) — 실제 스킬 함수

```python
# SAMPLE — 파일 경로·포맷·변수명은 네 데이터로 교체하라.
import numpy as np
from io_detect import open_dataset          # scripts/io_detect.py
from dataset import open_nc, Dataset        # scripts/dataset.py

# 모델 강수 격자 열기 (한글 경로 안전: open_nc 가 h5netcdf/scipy 폴백 내장)
d_mod = open_dataset("model_precip.nc")     # SAMPLE 경로 → Dataset 반환
# (직접 xarray 가 필요하면) xr_ds = open_nc("model_precip.nc"); d_mod = Dataset(xr_ds, source="model")

# --- 구조/메타 점검 (실제 Dataset 메서드) ---
print(d_mod.data_var_names())               # 변수 목록 — 강수 변수명 확인 (pr, tp, precipitation, rain...)
kind  = d_mod.coord_kind()                  # "1d" | "2d" | "mesh" | "none"
ll    = d_mod.latlon()                       # (lat_name, lon_name, is_2d) | None
shape = d_mod.grid_shape()                   # (nlat, nlon) | (ny, nx) | (n_nodes,) | None
tinfo = d_mod.time_info()                    # {"name","n_steps","start","end"} | None

# 강수 변수 메타(단위!) 점검 — SAMPLE: 변수명을 네 파일에 맞춰라
var = d_mod.variable("pr")                   # SAMPLE 변수명 "pr"
print(var.units, var.standard_name, var.long_name)   # 예: "kg m-2 s-1" / "precipitation_flux"
```

> **강수 필수 게이트(§H-1·H-2)** — 지표 계산 전에 반드시:
> 1. **단위 통일**: `kg m-2 s-1` → `mm/day`는 **×86400**. `mm/h` ↔ `mm/day`는 ×24.
>    (온도만 다루는 `preprocess.to_kelvin` 같은 단위 헬퍼는 강수엔 없음 → 아래처럼 직접 환산.)
> 2. **누적창·기준시각 정합**: 순간 강수율(flux) vs 누적량(amount)을 동일 창(1h·일·월)으로.
>    우량계 일강수 관측기준시각(예 09 KST)과 모델 누적창 정렬.
> 3. **wet 임계 명시**: 보통 0.1 또는 1 mm/day. 이 값이 wet-day 빈도·범주지표 전체를 바꾼다.

```python
# SAMPLE — 강수 단위 환산 (네 파일 units 속성에 맞춰 분기하라)
pr = d_mod.xr["pr"]                          # SAMPLE 변수명
u  = (var.units or "").lower()
if u in ("kg m-2 s-1", "kg/m2/s", "mm/s"):
    pr_mmday = pr * 86400.0                  # flux → mm/day
elif u in ("mm/h", "mm hr-1"):
    pr_mmday = pr * 24.0
else:
    pr_mmday = pr                            # SAMPLE: 이미 mm/day 라고 가정 — 실데이터에서 확인!
```

---

## §B 전처리·매치업 (Preprocess & Matchup) — 실제 스킬 함수

### B-1 우량계 CSV → UTC 정렬 [시계열]

```python
# SAMPLE — 컬럼명·인코딩·결측기호·시간대를 네 파일로 교체하라.
import pandas as pd
from preprocess import tz_to_utc, common_time_index   # scripts/preprocess.py

# io_detect 는 CSV 도 열지만(utf-8→cp949→euc-kr→latin-1 폴백), 컬럼 alias 는 직접.
df = pd.read_csv("gauge.csv", encoding="cp949",         # SAMPLE 인코딩
                 na_values=["-", "999", "9999", "-99.9"])  # SAMPLE 결측기호
ALIAS = {"일시": "datetime", "지점": "station_id",
         "강수량(mm)": "rain_obs"}                        # SAMPLE 한글→영문
df = df.rename(columns={k: v for k, v in ALIAS.items() if k in df.columns})

# 시간대 → UTC (우량계 KST 가 흔함 → 모델 UTC 와 9h 어긋남 방지)
t_utc, assumed = tz_to_utc(df["datetime"].values, tz="KST")   # SAMPLE tz — 메타로 확인!
if assumed:
    print("경고: 시간대 미확인 → UTC 가정. KST 면 'KST'/'+09:00' 명시하라(§H-3).")
```

### B-2 정점 좌표 주입 + mesh/격자 최근접 매칭

```python
# SAMPLE — 정점 위치·mesh 여부를 네 데이터로 점검하라.
from preprocess import inject_point_coords, match_points_to_mesh, build_pairs

# 정점 ID → (lat, lon) 매핑 (에이전트/CLI 가 실데이터 메타로 구성)
GAUGE_LL = {"서울_108": (37.57, 126.97),      # SAMPLE {id: (lat, lon)}
            "부산_159": (35.10, 129.03)}
station_ids = ["서울_108", "부산_159"]        # SAMPLE
g_lat, g_lon = inject_point_coords(station_ids, GAUGE_LL)

# 모델이 비정형 mesh 이면 최근접 노드 매칭 (정규격자면 xr.sel(method="nearest") 사용)
if d_mod.is_mesh():
    mesh_lat = d_mod.xr["latitude"].values    # SAMPLE: mesh 는 data_var 로 lat/lon 저장되기도
    mesh_lon = d_mod.xr["longitude"].values
    idx, dist_km = match_points_to_mesh(mesh_lon, mesh_lat, g_lon, g_lat, max_km=25.0)  # SAMPLE 25km
    # 대표성 오차 로그: 최근접 거리 > 격자간격이면 비교 품질 저하(§H-2)
    print("최근접 거리(km):", np.round(dist_km, 1), " 제외(-1):", (idx < 0).sum())
else:
    # SAMPLE — 정규격자 점 추출 (변수·좌표명 교체)
    idx = None
    pt = d_mod.xr["pr"].sel(lat=("pts", g_lat), lon=("pts", g_lon), method="nearest")  # SAMPLE
```

### B-3 시간 교집합으로 매치업 페어 만들기

```python
# SAMPLE — 시간 해상도·정렬 허용오차를 네 데이터로 점검하라.
model_t = d_mod.xr["time"].values                          # SAMPLE 시간축
i_obs, i_mod = common_time_index(t_utc, model_t)           # 두 시계열 교집합 인덱스
obs_rain   = df["rain_obs"].values[i_obs]                   # SAMPLE
model_rain = pr_mmday.values[i_mod, 0]                      # SAMPLE: 첫 정점 예시 — 실데이터 맞춤
# 롱포맷이 필요하면(선택): build_pairs(stations, times, model_vals(T×S), obs_vals(T×S))
```

---

## §C 연속 오차 검증 (Continuous Metrics) — 실제 스킬 함수

방법 카드: "연속 오차통계의 강수 적용" · 그림 ⑮(매치업 산점)·⑪(공간지도)

```python
# SAMPLE — metrics_basic 은 (f, o) = (예보, 관측) 순서다! 강수는 wet-only 병행 권장.
import metrics_basic as mb                     # scripts/metrics_basic.py

f = np.asarray(model_rain, float)              # 예보(모델)
o = np.asarray(obs_rain,   float)              # 관측(우량계 = reference, truth 아님)

stats = {
    "bias":  mb.bias(f, o),                    # mean(f - o): +면 과대예보
    "mae":   mb.mae(f, o),
    "rmse":  mb.rmse(f, o),                    # 강수: 소수 극치에 지배됨(§H-4) → 변환 병행
    "nrmse": mb.nrmse(f, o),                   # RMSE / |mean(o)|
    "si":    mb.si(f, o),                      # 불편RMSE / |mean(o)| (Scatter Index)
    "r":     mb.pearson_r(f, o),               # 주의: 0 다수 포함 시 상관 인위 상승 → wet-only 병행
}
slope, intercept = mb.linregress(f, o)         # f ~ slope*o + intercept
print({k: round(v, 3) for k, v in stats.items()}, "slope=", round(slope, 3))

# --- 강수 특화: PBIAS(총량 상대편의, 위성/QPE 표준) + wet-only 상관 (자작; 실존 numpy) ---
def pbias(f, o):                               # PBIAS = 100·Σ(f-o)/Σo
    m = np.isfinite(f) & np.isfinite(o)
    return 100.0 * np.sum(f[m] - o[m]) / np.sum(o[m])

WET = 1.0                                       # SAMPLE wet 임계 mm/day — 반드시 명시(§H-1)
wet = (o >= WET) | (f >= WET)                  # wet-only 서브셋
print("PBIAS(%)=", round(pbias(f, o), 1),
      " wet-only r=", round(mb.pearson_r(f[wet], o[wet]), 3))
```

> **해석(advisory)**: PBIAS 부호=과대/과소. bias=0이 정확을 뜻하지 않음(양·음 상쇄).
> 0 포함 상관은 wet/dry 일치가 상관을 부풀리는 **간헐성 artefact** → 범주·분포 지표 병행 필수.

---

## §D 분포·꼬리 검증 (Distribution & Tail) — 실제 스킬 함수

방법 카드: "강수강도 PDF" · "Q-Q / 분위수 편향" · "Perkins Skill Score" · 그림 ⑧⑩

```python
# SAMPLE — metrics_distribution 은 (obs, fct) 순서. 강수는 wet-only 로 점질량 왜곡 제거!
import metrics_distribution as md              # scripts/metrics_distribution.py

o_wet = o[o >= WET]                            # SAMPLE wet-only (0 제외) — 강수 QQ 표준
f_wet = f[f >= WET]

# Q-Q 비교점 (고분위=극한강수 꼬리 진단) — 상위분위 조밀히 보려면 n_quantiles↑
obs_q, fct_q = md.qq_points(o_wet, f_wet, n_quantiles=100)   # (obs_q, fct_q)
# 특정 상위 분위수만: quantiles(x, p)  (p 는 [0,1])
p_hi = [0.90, 0.95, 0.99, 0.999]              # SAMPLE 극한 분위
print("obs 상위분위:", np.round(md.quantiles(o_wet, p_hi), 1))
print("mdl 상위분위:", np.round(md.quantiles(f_wet, p_hi), 1))

# Perkins Skill Score (PDF 중첩도 [0,1]) + KS 거리
pss = md.perkins_skill_score(o_wet, f_wet, bins=30)   # SAMPLE bins — 강수는 로그폭이 이상적(§주의)
ks  = md.ks_distance(o_wet, f_wet)
print("Perkins PSS=", round(pss, 3), " KS D=", round(ks, 3))
```

> **주의**: `perkins_skill_score`/`ks_distance` 의 bin 은 선형이다. 강수 강도는 수십 배 범위라
> **로그 bin**이 이상적 — 형상 인상이 bin 에 좌우되므로(§H) 로그-bin PDF 는 §강수특화에서 별도로 그린다.
> 상위분위(99.9%)는 표본희소 → 부트스트랩 CI 권장.

---

## §E 그림 (Figures, 공통 SAMPLE) — 실제 스킬 함수

모든 `plots.*` 는 PNG 절대경로를 반환하고 **advisory·reference≠truth 캡션이 내장**돼 있다(§G 강제).
지도형은 `plots.diff_map` 이 내부에서 **`plots.add_basemap`(해안선+육지+위경도 라벨)** 을 호출한다.

```python
# SAMPLE — 출력 경로·단위 문자열을 네 작업에 맞춰라.
import plots

# ⑮/① 산점(SI·1:1·OLS 내장): scatter_si(o, f, out_png, units)  ← (관측, 예보) 순서!
p1 = plots.scatter_si(o, f, "out/precip_scatter.png", units="mm/day")

# 시계열 오버레이: timeseries_overlay(t, o, f, out_png)
p2 = plots.timeseries_overlay(model_t[i_mod], o, f, "out/precip_ts.png")

# ⑩ Q-Q 그림: qq_plot(o, f, out_png)  — wet-only 배열을 넣어 강수 특화
p3 = plots.qq_plot(o_wet, f_wet, "out/precip_qq.png")

# (공통) Taylor: taylor_diagram(o, f, out_png) — 여러 지점/계절 비교시 반복 호출
p4 = plots.taylor_diagram(o, f, "out/precip_taylor.png")
print(p1, p2, p3, p4, sep="\n")
```

### ⑪ 공간 bias 지도 (지도형 — add_basemap 필수)

```python
# SAMPLE — 격자 lat/lon·차원 순서를 네 데이터로 점검하라. 강수는 conservative 재격자 권장(§H).
# 모델 vs 격자관측(IMERG/ERA5/레이더 QPE): 공통 격자·기간으로 정합했다고 가정.
import xarray as xr

d_obs = open_dataset("imerg_precip.nc")        # SAMPLE 관측격자 (reference, truth 아님!)
# 시간평균 강수차(F−O). 실데이터: 단위·누적창·마스크 통일 선행.
mod_mean = pr_mmday.mean("time").values        # SAMPLE (ny, nx)
obs_mean = d_obs.xr["precipitation"].mean("time").values   # SAMPLE 변수명·차원
diff = mod_mean - obs_mean                      # 예보 − 관측 (mm/day)

lat2d = d_mod.xr[ll[0]].values                  # SAMPLE: latlon() 이 준 이름 사용
lon2d = d_mod.xr[ll[1]].values                  # 1D 좌표면 np.meshgrid 로 2D 화
if lat2d.ndim == 1:
    lon2d, lat2d = np.meshgrid(lon2d, lat2d)    # SAMPLE
# lon 이 0–360 이면 -180..180 변환: lon2d = ((lon2d + 180) % 360) - 180

# diff_map 이 내부에서 add_basemap 호출(해안선/위경도), 2D면 pcolormesh·1D면 scatter
p5 = plots.diff_map(lat2d, lon2d, diff, "out/precip_bias_map.png",
                    units="mm/day", title="Precip bias (Model − IMERG)")   # SAMPLE 제목
```

> **지도 규칙(그림카드 §G)**: 축이 위경도인 그림은 반드시 `add_basemap`(=`diff_map` 내장)으로
> 해안선+위경도 라벨. `diff_map` 은 bias 발산맵(RdBu_r, 0중심)을 자동 사용.
> 성능도표·FSS 히트맵·QQ·PDF 는 **지도가 아니므로 basemap 을 넣지 말 것**.

---

## §F 종합 검증 (Taylor / Target) — 실제 스킬 함수

방법 카드: 01 교차링크(Taylor·target 공통) · 그림 (공통 16)

```python
# SAMPLE — metrics_pattern 은 (o, f) = (관측, 예보) 순서다!
import metrics_pattern as mp                    # scripts/metrics_pattern.py

ts = mp.taylor_stats(o, f)                       # {std_ratio, corr, crmsd, n}
tg = mp.target_stats(o, f)                       # {bias, urmsd, rmsd, n}
pc = mp.pattern_correlation(obs_mean, mod_mean)  # 공간 스냅샷 패턴상관 (2D 장 비교)
print("Taylor:", {k: round(v,3) for k,v in ts.items() if k!='n'})
print("Target:", {k: round(v,3) for k,v in tg.items() if k!='n'}, " 공간r=", round(pc,3))
# 여러 지점/계절 (S,A,L)·(σ*,R) 을 모아 한 Taylor 에 겹치면 계통오차 유형이 보인다.
```

---

## §강수특화 (Precipitation-Specific) — 실존 라이브러리로

아래는 이 스킬 모듈이 제공하지 않는 강수 고유 지표다. **실존 라이브러리만** 사용
(`numpy/scipy/xarray/pandas` + 필요시 `pysteps`·`pyextremes`·`xclim`·`xskillscore`).
지어낸 함수 금지 — 없으면 numpy 로 자작.

### PS-1 범주형 2×2 분할표 · CSI · GSS(ETS) · HSS · POD/FAR/FBI (그림 ①②)

```python
# SAMPLE — 임계는 여러 개 스캔하라(단일임계 결론 금지, §H). 자작(numpy) — 실존.
def contingency(f, o, thr):
    """임계 thr 초과 이진사건 2×2 (a=hit, b=false, c=miss, d=corr-neg)."""
    m = np.isfinite(f) & np.isfinite(o)
    fe, oe = f[m] >= thr, o[m] >= thr
    a = int(np.sum(fe & oe)); b = int(np.sum(fe & ~oe))
    c = int(np.sum(~fe & oe)); dd = int(np.sum(~fe & ~oe))
    return a, b, c, dd

def cat_scores(a, b, c, d):
    n = a + b + c + d
    pod = a / (a + c) if (a + c) else np.nan          # hit rate
    far = b / (a + b) if (a + b) else np.nan
    sr  = 1 - far                                      # success ratio
    csi = a / (a + b + c) if (a + b + c) else np.nan   # Threat Score
    fbi = (a + b) / (a + c) if (a + c) else np.nan     # frequency bias
    a_rand = (a + b) * (a + c) / n if n else np.nan
    gss = (a - a_rand) / (a + b + c - a_rand) if (a + b + c - a_rand) else np.nan   # ETS
    pc  = (a + d) / n if n else np.nan
    pc_rand = ((a+b)*(a+c) + (c+d)*(b+d)) / n**2 if n else np.nan
    hss = (pc - pc_rand) / (1 - pc_rand) if (1 - pc_rand) else np.nan
    pofd = b / (b + d) if (b + d) else np.nan
    pss = pod - pofd                                    # Peirce SS (= TSS)
    return dict(POD=pod, FAR=far, SR=sr, CSI=csi, FBI=fbi, GSS=gss, HSS=hss, PSS=pss)

for thr in [0.1, 1, 10, 50]:                            # SAMPLE 임계 스캔 mm/day
    a, b, c, dd = contingency(f, o, thr)
    print(thr, {k: (round(v,3) if np.isfinite(v) else None) for k,v in cat_scores(a,b,c,dd).items()})

# 실존 대안: xskillscore (xarray 통합) — DataArray 입력
# import xskillscore as xs; xs.<binary metrics>  (설치돼 있으면 사용)
```
> **왜/주의**: CSI·GSS 는 기저율 의존 → 건조역·고임계에서 낮은 게 정상(모델 열등 아님).
> 극한(50 mm) 임계는 사건 희소로 GSS/HSS 퇴화 → **EDI/SEDI**(PS-2) 사용. 격자면 double-penalty 유의.

### PS-2 드문사건 지수 EDI / SEDI (극한 강수 임계, 그림 ①②)

```python
# SAMPLE — H·F 가 0/1 이면 log 정의 붕괴 → 표본확대·부트스트랩 CI 필수. 자작(numpy) — 실존.
def edi_sedi(a, b, c, d):
    H = a / (a + c) if (a + c) else np.nan             # hit rate
    F = b / (b + d) if (b + d) else np.nan             # false alarm rate
    if not (0 < H < 1 and 0 < F < 1):
        return dict(EDI=np.nan, SEDI=np.nan)           # 정의 불가 가드
    edi  = (np.log(F) - np.log(H)) / (np.log(F) + np.log(H))
    sedi = ((np.log(F) - np.log(H) - np.log(1-F) + np.log(1-H)) /
            (np.log(F) + np.log(H) + np.log(1-F) + np.log(1-H)))
    return dict(EDI=float(edi), SEDI=float(sedi))

a, b, c, dd = contingency(f, o, thr=50)                 # SAMPLE 극한 임계
print("극한 50mm:", edi_sedi(a, b, c, dd))
```
> **왜**: 극한 임계에서 CSI/GSS 는 0으로 퇴화하지만 SEDI 는 **비퇴화·기저율 독립** — 호우 검증에 필수.

### PS-3 이웃 검증 FSS (double-penalty 완화·유효스케일, 그림 ③④)

```python
# SAMPLE — pysteps 는 실존. 없으면 아래 numpy 자작으로. 공통격자 2D 강수장 필요.
# from pysteps.verification.spatialscores import fss          # 단일장
# score = fss(mod_field2d, obs_field2d, thr=10.0, scale=20)   # SAMPLE thr·scale
# 다사례 누적: fss_init(thr, scale) → fss_accum(...) → fss_compute(...)

# --- numpy 자작 FSS (실존 함수 없을 때) ---
from scipy.ndimage import uniform_filter
def fss_np(fcst2d, obs2d, thr, n):                      # n = 이웃 한 변(격자수)
    Pf = uniform_filter((fcst2d >= thr).astype(float), size=n, mode="constant")
    Po = uniform_filter((obs2d  >= thr).astype(float), size=n, mode="constant")
    mse     = np.nanmean((Pf - Po) ** 2)
    mse_ref = np.nanmean(Pf ** 2) + np.nanmean(Po ** 2)
    return 1 - mse / mse_ref if mse_ref > 0 else np.nan

for n in [1, 3, 9, 27]:                                  # SAMPLE 이웃 스케일(격자수)
    print("FSS thr=10, n=%2d:" % n, round(fss_np(mod_mean, obs_mean, 10.0, n), 3))
# useful scale: FSS 가 (0.5 + f0/2) 넘는 최소 n (f0 = 관측 사건빈도) — advisory(§H)
```
> **왜**: 위치가 조금 어긋난 강수 셀이 격자 CSI/RMSE 에서 이중처벌(miss+false). FSS 는
> 스케일을 키우며 "어느 스케일부터 유용한가"를 진단 → 고해상도·AI 강수모델 부당 저평가 방지.

### PS-4 로그-bin 강도 PDF / frequency×intensity 분해 (그림 ⑧⑨)

```python
# SAMPLE — 로그 bin. wet-only. 자작(numpy) — 실존. (Perkins 는 §D 의 md.perkins_skill_score 로.)
bins = np.logspace(np.log10(WET), np.log10(max(o_wet.max(), f_wet.max())), 30)  # SAMPLE
ho, _ = np.histogram(o_wet, bins=bins, density=True)
hf, _ = np.histogram(f_wet, bins=bins, density=True)   # matplotlib 로 overlay 하면 ⑧

# frequency×intensity 분해: Δmean = f·ΔI + I·Δf + Δf·ΔI
f_o = np.mean(o >= WET); I_o = np.mean(o[o >= WET])     # 관측 빈도·강도
f_m = np.mean(f >= WET); I_m = np.mean(f[f >= WET])     # 모델
dmean = f_m*I_m - f_o*I_o
print("Δf=%.3f ΔI=%.2f  Δmean=%.2f" % (f_m-f_o, I_m-I_o, dmean))
```
> **왜**: 총량이 맞아도 "비를 너무 자주·약하게(drizzle: Δf>0 & ΔI<0)" 라는 계통오차를 분리.

### PS-5 극치 POT-GPD / 연최대-GEV / 재현주기 (그림 ⑬)

```python
# SAMPLE — pyextremes(실존) 권장. 없으면 scipy.stats.genpareto/genextreme.
# import pandas as pd
# from pyextremes import EVA
# s = pd.Series(o_series, index=pd.to_datetime(t_index))    # SAMPLE 일강수 시계열(장기 ≥30y 권장)
# eva = EVA(s); eva.get_extremes("POT", threshold=s.quantile(0.99))   # SAMPLE 상위1% 임계
# eva.fit_model("GP"); print(eva.get_return_value(return_period=[50, 100]))  # 50·100년 재현값
# eva.plot_diagnostic()   # return level + QQ + PDF + probability

# --- scipy 자작(라이브러리 없을 때) ---
from scipy import stats
thr99 = np.nanpercentile(o_wet, 99)                     # SAMPLE POT 임계
exceed = o_wet[o_wet > thr99] - thr99
c, loc, scale = stats.genpareto.fit(exceed, floc=0)    # 형상 c=ξ (강수는 ξ>0 전형)
print("GPD ξ=%.3f σ=%.2f" % (c, scale))
```
> **왜/주의**: 방재·설계강우 핵심. 임계·declustering·표본에 극민감 → **부트스트랩 CI 필수**.
> 격자평균은 점 극치를 과소(areal reduction). 짧은 기록의 100년 외삽 과신 금지.

### PS-6 ETCCDI 강수 극한지수 (Rx1day·R95pTOT·SDII·CDD 등, 그림 ⑭)

```python
# SAMPLE — xclim/icclim(실존, ETCCDI 표준 구현) 권장 — 수식 재구현 오류 방지.
# import xclim.indicators.atmos as atmos
# rx1day = atmos.max_1day_precipitation_amount(pr_mmday, freq="YS")     # SAMPLE
# sdii   = atmos.daily_pr_intensity(pr_mmday, thresh="1 mm/day", freq="YS")
# cdd    = atmos.maximum_consecutive_dry_days(pr_mmday, thresh="1 mm/day", freq="YS")
# 지수별 bias 지도는 §E ⑪ 처럼 plots.diff_map(+add_basemap), 산점/Taylor 는 지도 아님.
```
> **주의**: R95p 류는 **기준기간(예 1961–1990) 정의가 값을 좌우** → 통일. wet 임계 1mm 고정. 표준구현 사용.

---

## §X ★ Cross-Domain 적용 (필수 절) — 타 도메인 기법을 이 강수 데이터에

이 도메인 관행이 아니어도 **이 데이터에 유용한** 타 도메인 검증 기법을 실제로 적용한다.
각 기법에 "왜 여기서 유용한가" + 실존 함수/코드.

### X-1 Taylor / Target 다이어그램 (공통 — 이미 스킬 함수 존재)
- **왜**: 여러 지점·계절·모델의 강수 σ비·상관·중심오차를 **한 그림**에 겹쳐 계통오차 유형을 비교.
  강수는 지점·계절 편차가 커서 다중 오버레이가 특히 유용.
```python
# 실제 스킬 함수 사용 — 반복 호출로 다중 겹치기
import metrics_pattern as mp, plots
for season, (os_, fs_) in season_pairs.items():          # SAMPLE {계절: (obs, mdl)}
    print(season, mp.taylor_stats(os_, fs_))
    plots.taylor_diagram(os_, fs_, f"out/taylor_{season}.png")   # SAMPLE
```

### X-2 Rank histogram (Talagrand) + CRPS — 앙상블 검증 (카드 13)
- **왜**: 강수 앙상블(예보 멤버들)의 **spread 적정성**을 진단. 결정론 지표로는 못 보는
  과소·과대분산(U자/역U자 rank histogram)을 잡는다. 극한 강수는 twCRPS 로 꼬리 강조.
```python
# SAMPLE — 실존 라이브러리 xskillscore. 앙상블 강수 [members × time] 필요.
# import xskillscore as xs
# rh   = xs.rank_histogram(obs_da, ens_da, member_dim="member")   # rank histogram
# crps = xs.crps_ensemble(obs_da, ens_da)                         # CRPS (0질량·꼬리 유의)
# 또는 numpy 자작 rank: 각 관측이 정렬된 멤버들 중 몇 번째인지 히스토그램.
```

### X-3 파워스펙트럼 / RAPSD 유효해상도 — AI·ML 평가 (카드 14)
- **왜**: 고해상도·AI 강수모델이 **격자만큼 미세한 구조를 실제로 담는지**(과평활 여부)를
  방사 평균 파워스펙트럼밀도(RAPSD)로 진단. RMSE 가 좋아도 blur 된 강수장을 걸러낸다.
```python
# SAMPLE — pysteps 실존: RAPSD. 없으면 numpy FFT 자작.
# from pysteps.utils.spectral import rapsd
# psd_m, freq = rapsd(mod_field2d, return_freq=True)     # 모델
# psd_o, _    = rapsd(obs_field2d, return_freq=True)      # 관측
# 두 PSD 가 고주파에서 갈라지는 파장 = 유효해상도(모델이 그보다 잘게는 못 그림).

# --- numpy FFT 자작(라이브러리 없을 때) ---
def radial_psd(field2d):
    F = np.fft.fftshift(np.fft.fft2(field2d - np.nanmean(field2d)))
    P = np.abs(F) ** 2
    ny, nx = field2d.shape
    y, x = np.indices((ny, nx)); cy, cx = ny//2, nx//2
    r = np.hypot(x - cx, y - cy).astype(int)
    return np.bincount(r.ravel(), P.ravel()) / np.bincount(r.ravel())
print("RAPSD(model)[:5]=", np.round(radial_psd(mod_mean)[:5], 1))   # SAMPLE
```

> **cross-domain 요약**: Taylor/Target(공통·스킬함수) + rank histogram/CRPS(앙상블·13) +
> RAPSD 유효해상도(AI·14) 를 강수에 끌어와, 결정론 단일지표가 못 보는 **분산·구조·꼬리**를 본다.

---

## §H 함정·주의 (Pitfalls — §G 캡션 근거)

| # | 함정 | 실무 대응 |
|---|------|-----------|
| H-1 | **wet 임계·누적창·단위 불일치** | 0.1 vs 1 mm/day, 1h vs 일, `kg m-2 s-1`×86400 — 보고문에 명시. bilinear 재격자 금지 → **conservative**(강수 총량 보존). |
| H-2 | **대표성 오차** | 점(우량계) vs 격자평균 스케일 불일치. `match_points_to_mesh` 의 `dist_km` 로그 기록. 격자평균은 극치·강도꼬리 평활. |
| H-3 | **시간축 불일치** | 우량계 KST(+09) vs 모델 UTC → `tz_to_utc(..., tz="KST")`. `assumed=True` 면 경고. |
| H-4 | **RMSE 극치 지배 / 상관 artefact** | 두꺼운 꼬리 → RMSE 는 소수 극치에 좌우. 0 포함 상관은 간헐성으로 부풀림 → wet-only·범주·분포 병행. |
| H-5 | **reference ≠ truth** | IMERG Final·radar–gauge 병합은 **게이지 반영** → 그 게이지로 독립검증·TC 3자 부적합. 재분석·위성 "정답" 과신 금지. |
| H-6 | **double-penalty** | 고해상도·AI 강수: 격자 RMSE/CSI 나쁨 ≠ 모델 나쁨(위치오차일 수). FSS(PS-3)·SAL 로 위치 vs 강도 구분. |
| H-7 | **단일 임계·지표·그림 금지** | 최소 **①범주 종합 + ⑧/⑩분포·극치 + ③/⑪공간** 3축. 해석 임계(FSS useful=0.5+f₀/2 등)는 advisory. |

---

## §I 관련 방법·그림 카드 참조

| 자료 | 경로 | 역할 |
|------|------|------|
| 방법 카드(강수) | `references/research/23_domain_precipitation.md` | 검증 항목 근거·수식·출처 |
| 그림 카드(강수) | `references/research/figures/31_fig_precipitation.md` | ①~⑯ 강수 그림 유형·읽는 법 |
| 그림 카드(공통) | `references/research/figures/16_fig_common.md` | Taylor·QQ·성능도표·return-level 공통 정의 |
| 지도 그리기 | `references/plotting_maps.md` | `add_basemap` 상세·오프라인 캐시 |
| 스킬 스크립트 | `scripts/metrics_basic.py`·`metrics_distribution.py`·`metrics_pattern.py`·`metrics_circular.py`·`plots.py`·`preprocess.py`·`io_detect.py`·`dataset.py` | 실제 함수 구현 |

---

## §J 출처 (References — 확인된 것만 DOI, 나머지 "확인요")

**표준 교과서·지침(실재)**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (bias·RMSE·QQ·PDF 공통 정의).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide*, Wiley (범주 CSI/HSS/PSS·ROC).
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD/POT).
- WMO (2009) Klein Tank, Zwiers & Zhang, *Guidelines on Analysis of extremes in a changing climate*, WCDMP-72 / WMO-TD No. 1500 (ETCCDI 지수·SDII).

**학술 논문(제목·저널·연도 확인; DOI는 확인된 것만)**
- Roberts & Lean (2008) "Scale-selective verification of rainfall accumulations…," *Monthly Weather Review* 136(1):78–97, doi:10.1175/2007MWR2123.1 (FSS).
- Roebber (2009) "Visualizing multiple measures of forecast quality," *Weather and Forecasting* 24(2):601–608, doi:10.1175/2008WAF2222159.1 (성능도표).
- Wernli, Paulat, Hagen & Frei (2008) "SAL—A novel quality measure…," *Monthly Weather Review* 136(11):4470–4487, doi:10.1175/2008MWR2415.1 (SAL).
- Ferro & Stephenson (2011) "Extremal dependence indices…," *Weather and Forecasting* 26(5):699–713 (EDI/SEDI).
- Schaefer (1990) "The critical success index…," *Weather and Forecasting* 5(4):570–575 (CSI).
- Hogan et al. (2010) "Equitability revisited…," *QJRMS* 136:2652–2657 (GSS/ETS).
- Perkins, Pitman, Holbrook & McAneney (2007) *Journal of Climate* 20(17):4356–4376, doi:10.1175/JCLI4253.1 (Perkins SS).
- Dai (2006) "Precipitation characteristics in eighteen coupled climate models," *Journal of Climate* 19(18):4605–4630 (frequency/intensity 편향).
- Sun et al. (2006) "How often does it rain?" *Journal of Climate* 19(6):916–934 (빈도·강도 분해).
- Zhang et al. (2011) "Indices for monitoring changes in extremes…," *WIREs Climate Change* 2(6):851–870 (ETCCDI).
- Hersbach et al. (2020) "The ERA5 global reanalysis," *QJRMS* 146(730):1999–2049 (ERA5 기준).
- Adler et al. (2003) GPCP monthly analysis, *Journal of Hydrometeorology* 4(6):1147–1167 (GPCP 격자강수 기준).
- Huffman et al. (2020) "IMERG," in *Satellite Precipitation Measurement*, Springer, 343–353 (IMERG).
- Goudenhoofdt & Delobbe (2009) "Evaluation of radar-gauge merging methods for QPE," *HESS* 13(2):195–203.
- Kochendorfer et al. (2017) "…wind-induced precipitation measurement errors," *HESS* 21(4):1973–1989 (WMO-SPICE undercatch).
- Moriasi et al. (2007) *Transactions of the ASABE* 50(3):885–900 (PBIAS 기준 — 수문 관행).

**소프트웨어(실존 도구)**
- `pysteps` — FSS(`verification.spatialscores.fss`/`fss_init`/`fss_accum`/`fss_compute`)·SAL(`verification.salscores.sal`)·RAPSD(`utils.spectral.rapsd`): https://pysteps.readthedocs.io (Pulkkinen et al. 2019, *GMD* 12:4185–4219).
- `pyextremes` — POT/GEV·return level·진단도(`EVA`, `plot_return_values`, `plot_diagnostic`): https://georgebv.github.io/pyextremes.
- `xclim`/`icclim` — ETCCDI 극한지수 표준 구현: https://xclim.readthedocs.io.
- `xskillscore` — rank histogram·CRPS·범주 지표(xarray 통합).
- `xarray`/`xesmf`(**conservative** regridding)·`cartopy`(+`add_basemap`)·`numpy`·`scipy`·`pandas`·`matplotlib`.

**확인요(확정 인용 금지)**
- Casati, Ross & Stephenson (2004) *Meteorological Applications* 11(2):141–154 — 제목·저널·권·페이지 확인, **DOI 미검증(확인요)**.
- Davis, Brown & Bullock (2006) MODE Part I/II, *Monthly Weather Review* 134:1772–1795 — 제목·저널·연도 확인, **DOI 미확정(확인요)**.
- WWRP/WGNE JWGFVR 페이지·DTC MET/METplus URL·버전 — 변동 가능(확인요).
- 해석 임계(FSS useful=0.5+f₀/2, wet 임계 0.1/1 mm, CC≥0.7 등)는 **관행 advisory** — 기후대·해상도·기준자료 의존(§H).

---

*SAMPLE — 이 파일은 범용 스킬의 강수 예시다. 실 데이터 구조를 실시간 점검하고
변수명·단위·누적창·wet 임계·좌표에 맞춰 각 단계를 수정한 뒤 사용하라. 그대로 실행 금지.*
