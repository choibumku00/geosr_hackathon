# Recipe: 해빙·빙권 검증 (Sea Ice / Cryosphere Model Validation)

> ## ⚠️ SAMPLE — 실데이터에 맞춰 맞춤 수정하라. 그대로 실행 금지.
> 이 스킬(`validate-model-output`)은 **특정 분야 전용이 아니라 범용**이다.
> 이 파일은 그 범용 스킬을 **해빙·빙권(sea_ice)** 이라는 한 예시 도메인에 적용해 본
> **worked SAMPLE 레시피**일 뿐이다. 코드는 항상 "SAMPLE(출발점) → 사용자 데이터에 맞춰
> 변수명·단위·좌표·마스크·투영·시각규약을 실시간 점검 후 맞춤 수정"이 원칙이다.
> **완비된 파이프라인이 아니다** — SIC(0–1 bounded)·두께·표류·얼음경계 등 해빙 자료의
> 구조를 반드시 먼저 확인하고 각 단계를 고쳐 써라.
>
> 대응 방법·그림 카드(근거):
> - 방법: `references/research/24_domain_sea_ice.md`
> - 그림: `references/research/figures/32_fig_sea_ice.md`
> - 지도: `references/plotting_maps.md` (극projection에서 `add_basemap()` 사용법·오프라인 대응)

---

## 대표 자료형 (Data Forms this recipe targets)

| 자료형 | 예 | 이 레시피에서 |
|--------|-----|--------------|
| **[격자] SIC** | `sea_ice_area_fraction` ∈ **[0,1] bounded** (모델 vs 위성 OSI SAF/NSIDC CDR·재분석 ORAS5) | §B·§C·§E |
| **[격자] 두께** | `sea_ice_thickness` (모델 vs CS2SMOS·CryoSat-2·ICESat-2, **겨울 한정**) | §D·§F |
| **[격자→시계열] 적분량** | SIE·SIA·SIV (15% 임계면적·농도가중·부피) | §F |
| **[경계] 얼음경계** | 15% SIC 등치선 폴리곤 (IIEE·MHD) | §E |
| **[벡터/격자] 표류** | `sea_ice_x/y_velocity`, `sea_ice_speed` (OSI SAF drift·IABP 부이) | §G (cross-domain) |
| **극지 지도** | `add_basemap()` — **극투영 주의**(§맵 주의) | §전반 |

> **극투영 주의(★)**: 이 스킬의 `plots.add_basemap()`·`_make_geo_axes()`는 **PlateCarree** GeoAxes를
> 만든다. 해빙은 극지역이라 관행상 `NorthPolarStereo`/`SouthPolarStereo`가 더 적합하다.
> `add_basemap`은 극에서도 해안선+위경도 라벨을 그려 "일단 위치가 보이는" 안전한 출발점이지만,
> **제대로 된 극지도**는 아래처럼 GeoAxes를 극투영으로 직접 만들고(그 위에도 `add_basemap`으로
> 해안선/라벨을 얹은 뒤) `set_boundary`로 원형 경계를 잡아야 한다. 이 부분은 SAMPLE이며
> 네 데이터의 반구(북극/남극)·경도규약(0–360 vs −180–180)에 맞춰 바꿔라.

---

## 빠른 참조 (Quick Reference) — 단계 → **실제 스킬 함수** → 그림 카드

| 단계 | 실제 스킬 함수 (모듈.함수 — 읽은 시그니처) | 대응 그림 카드(32) |
|------|-------------------------------------------|--------------------|
| A. 열기·구조 점검 | `io_detect.open_dataset(path)` → `Dataset`; `dataset.open_nc(path)`; `Dataset.coord_kind()`·`.latlon()`·`.grid_shape()`·`.variable(name)`·`.time_info()`·`.xr` | — |
| A′. 정점/mesh 매치업·tz | `preprocess.match_points_to_mesh(...)`, `preprocess.tz_to_utc(times, tz)`, `preprocess.common_time_index(t1,t2)`, `preprocess.inject_point_coords(ids, mapping)` | — |
| B. SIC 정확도(면적가중) | `metrics_basic.bias/mae/rmse/nrmse/si/pearson_r/linregress`; 면적가중은 도메인 코드(numpy) | Fig 07 SIC 산점(bounded) · Fig 02 bias map |
| C. SIC 분포(bounded) | `metrics_distribution.qq_points`, `.perkins_skill_score`, `.ks_distance`, `.quantiles` | Fig 07 · 공통 QQ |
| D. 두께 정확도·분포 | `metrics_basic.*` + `metrics_distribution.qq_points`; 두께대별은 `scipy.stats.binned_statistic` | Fig 08 두께지도 · Fig 09 binned · Fig 10 ITD |
| E. 얼음경계(면적·거리) | IIEE/AEE/ME (numpy 면적가중); MHD는 `scipy.spatial`·`pyproj.Geod`; 경계추출 `skimage.measure.find_contours` | Fig 03 오버레이+IIEE · Fig 05 분해 · Fig 06 거리 |
| F. 종합·적분량 | `metrics_pattern.taylor_stats/target_stats/pattern_correlation`; SIE/SIA/SIV는 `xarray` weighted sum | Fig 01 상태지도 · Fig 04 계절곡선 · Fig 16 SIV |
| G. cross-domain(★) | FSS(`pysteps`/`scores`) · SAL/MODE 객체(`scipy.ndimage`) · 표류 원형·벡터(`metrics_circular.*`) | Fig 15 FSS · Fig 11 quiver · Fig 14 Hovmöller |
| 그림 | `plots.scatter_si`, `.timeseries_overlay`, `.diff_map`, `.qq_plot`, `.taylor_diagram`, `.wave_rose`, `.add_basemap`, `._make_geo_axes` | (전반) |

> **§G 캡션 원칙(반드시)**: 위성 SIC(알고리즘 산물)·CS2SMOS/CryoSat-2 두께(밀도·적설 가정 유도량)·
> PIOMAS/ORAS5 재분석은 **reference이지 truth가 아니다**. 축·캡션에 "모델 − 기준(reference)"으로 쓰고,
> 15%·"겨울 SIC 5–10%"·"MIZ 20–30%" 등 임계는 **advisory(계절·해역·센서 의존)**로 표기한다.
> `plots.py`의 그림 함수들은 제목에 이미 `(advisory — reference≠truth)`를 넣는다.

---

## §A 열기 · 구조/메타 점검 (Open & Inspect)

```python
# SAMPLE — 실데이터 변수명·단위·좌표·마스크를 반드시 실시간 점검하라.
# scripts/ 는 conftest.py 가 sys.path 에 넣으므로 플랫 import 가능(패키지 아님).
from io_detect import open_dataset          # scripts/io_detect.py
from dataset import open_nc, Dataset        # scripts/dataset.py
import numpy as np

# 한글/비-ASCII 경로 안전 (Windows netCDF4 Errno22 우회 내장)
d = open_dataset("cice_sic_202303.nc")      # → Dataset (fmt 자동판별)
# 또는 직접:  d = Dataset(open_nc("path.nc"), source="cice", fmt="netcdf4")

# 좌표 위상 — SAMPLE: 극격자는 대개 2d 곡선격자 또는 mesh
kind  = d.coord_kind()        # "1d" | "2d" | "mesh" | "none"
ll    = d.latlon()            # (lat_name, lon_name, is_2d) | None
shape = d.grid_shape()        # (ny,nx) / (nlat,nlon) / (n_nodes,)
tinfo = d.time_info()         # {"name","n_steps","start","end"} | None
print(kind, ll, shape, tinfo)

# 변수 메타(단위/표준명) — SIC 가 fraction(0–1) 인지 percent(0–100) 인지 확인
for name, v in d.variables().items():
    print(name, v.dims, v.shape, "units=", v.units, "std=", v.standard_name)

xr_ds = d.xr                  # 내부 xarray.Dataset 접근

# ── SIC 변수 꺼내기 (SAMPLE: 네 파일 변수명으로 교체) ─────────────
SIC_VAR = "aice"              # SAMPLE — CICE 'aice' / OSI SAF 'ice_conc' / CDR 'cdr_seaice_conc'
sic = xr_ds[SIC_VAR]
# 단위 정규화 — percent 면 0–1 로 (SAMPLE: units 문자열 실제 확인)
if (d.variable(SIC_VAR).units or "").strip() in ("%", "percent"):
    sic = sic / 100.0
sic = sic.clip(0.0, 1.0)      # [0,1] bounded 강제 — SAMPLE(경계 넘는 채움값 정리)
```

> **실데이터 점검 항목 (SAMPLE)**
> - SIC 단위: fraction[0,1] vs percent[0,100]. 채움값(예 −999, 1.27e9)·pole hole 처리.
> - 좌표: 극 stereographic 곡선격자(2d) vs mesh. 경도 0–360 vs −180–180.
> - land/ocean mask, `MAPSTA`·`tmask` 유무. 셀면적(`tarea`/`cell_area`/`areacello`) 변수 존재?
> - 시각규약: 일평균 vs 순간. 위성 SIC 알고리즘(Bootstrap/NASA Team/ASI/OSI SAF) 명시.

### A′ 매치업·시간대(정점/mesh인 경우) — `preprocess`

```python
# SAMPLE — 부이(IABP)·계류(ULS) 점자료를 격자/mesh 모델에 맞출 때만.
from preprocess import (match_points_to_mesh, tz_to_utc,
                        common_time_index, inject_point_coords)

# (1) 비정형 mesh(neXtSIM 등) 최근접 노드 매칭 — cKDTree + km 거리 필터
#     mesh_lon/lat: data_var 로 저장돼 있을 수 있음 → is_mesh()/_find_data_var 로 확인
idx, dist_km = match_points_to_mesh(mesh_lon, mesh_lat, buoy_lon, buoy_lat, max_km=50.0)
# idx == -1 은 max_km 초과 → 제외. dist_km 를 로그에 남겨라(대표성 오차 근거).

# (2) 시간대 정규화 — 부이 KST(+9) ↔ 모델 UTC 어긋남 방지
buoy_t_utc, assumed = tz_to_utc(buoy_times, tz="KST")   # KST → -9h
if assumed:
    print("경고: TZ 미확인 — UTC 가정. 부이 메타 재확인 필요")

# (3) 두 시계열 교집합 인덱스 (스텝 정렬)
i_obs, i_mdl = common_time_index(buoy_t_utc, model_times)
```

---

## §B SIC 정확도 (Accuracy) — **면적가중 필수**, bounded 주의

Figure: **Fig 07 SIC 산점/밀도(bounded)** · **Fig 02 bias map**

```python
# SAMPLE — SIC 는 [0,1] bounded. 순 bias 가 0이어도 국지오차 큼 → RMSE·지도 병행.
import numpy as np
import metrics_basic as mb        # scripts/metrics_basic.py — 실제 시그니처: (f, o)

# ── 공통격자 정합(재격자화)은 이 코드 범위 밖 ──
# 위성/재분석과 모델은 극격자가 다르다 → 실데이터에선 xesmf(conservative/nearest)로
# 공통 극격자에 먼저 맞춰라. 재격자화가 경계에서 인위적 중간농도 만드니 보존형 주의.
#   import xesmf as xe; regridder = xe.Regridder(ds_mdl, ds_ref, "conservative")

# model, ref, area 는 동일 (ny,nx) 2D numpy (SAMPLE: 네 정합 결과로 교체)
model = sic.isel(time=0).values                      # SAMPLE 시각 인덱스
ref   = xr_ds_ref["ice_conc"].isel(time=0).values    # SAMPLE 위성 SIC
area  = xr_ds["tarea"].values                        # 셀면적 (m^2) — SAMPLE 변수명

# 유효 셀(둘 다 finite + 해양)만
ocean = np.isfinite(model) & np.isfinite(ref)        # SAMPLE: + land/pole hole mask
o = ref[ocean]; f = model[ocean]; w = area[ocean]

# 스킬 함수(비가중) — 인자 순서는 (forecast, observation)!
print("bias =", mb.bias(f, o))          # mean(f - o)
print("rmse =", mb.rmse(f, o))
print("mae  =", mb.mae (f, o))
print("r    =", mb.pearson_r(f, o))
slope, intercept = mb.linregress(f, o)  # f ~ slope*o + intercept
print("slope=", slope, "intercept=", intercept)

# ── 면적가중 bias/RMSE (해빙 필수) — 스킬엔 없으니 도메인 코드로 ──
def area_weighted_bias(f, o, w):
    return float(np.sum(w * (f - o)) / np.sum(w))
def area_weighted_rmse(f, o, w):
    return float(np.sqrt(np.sum(w * (f - o) ** 2) / np.sum(w)))
print("area-wt bias =", area_weighted_bias(f, o, w))
print("area-wt rmse =", area_weighted_rmse(f, o, w))
```

> **주의(SAMPLE)**: `metrics_basic.si`/`nrmse`는 분모가 `|mean(o)|`다. SIC는 영역평균이
> 작을 수 있어(여름·저농도) SI가 불안정 → 해빙에선 **면적가중 RMSE + bias**를 1차로,
> SI는 참고로만. slope 해석도 bounded라 OLS가 경계에서 왜곡(§C 하단 참고).

### 그림 — 산점(bounded) · bias 지도

```python
# SAMPLE — plots.py 실제 함수. scatter_si(o, f, out_png, units): 인자 순서 (obs, fct)!
from plots import scatter_si, diff_map

scatter_si(o, f, "out/sic_scatter.png", units="frac")   # 1:1 + OLS + SI + n

# bias 지도: 2D lat/lon + (model−obs) → add_basemap 자동(해안선+위경도).
lat2d = xr_ds[ll[0]].values; lon2d = xr_ds[ll[1]].values   # ll=(lat,lon,is_2d)
diff2d = np.where(ocean, model - ref, np.nan)              # F−O, land=NaN
diff_map(lat2d, lon2d, diff2d, "out/sic_bias_map.png",
         units="frac", title="SIC bias (model − reference)")
```

---

## §C SIC 분포 (Distribution) — bounded 꼬리 주의

Figure: **Fig 07(부채꼴 진단)** · 공통 QQ

```python
# SAMPLE — 실데이터 분포 꼬리(0·1 경계 축적) 처리 점검.
import metrics_distribution as md   # scripts/metrics_distribution.py

# qq_points(obs, fct, n_quantiles) → (obs_q, fct_q)   ※ 순서 (obs, fct)
obs_q, fct_q = md.qq_points(o, f, n_quantiles=50)

# Perkins Skill Score (공통면적 유사도 [0,1]) — bins 는 SIC 스케일에 맞춰
pss = md.perkins_skill_score(o, f, bins=20)   # SAMPLE: 0·1 몰림이면 bins 늘려라
ks  = md.ks_distance(o, f)                     # KS D-통계량 [0,1]
print("PSS =", pss, "KS =", ks)

# 그림 — plots.qq_plot(o, f, out_png)  ※ 순서 (obs, fct)
from plots import qq_plot
qq_plot(o, f, "out/sic_qq.png")
```

> **bounded 함정(SAMPLE)**: SIC는 0·1에 자료가 몰려 OLS/정규분포 가정 지표가 경계에서
> 왜곡된다. QQ에서 양극단 계단, 산점에서 MIZ대(0.15–0.8) 부채꼴 퍼짐은 **관측 SIC 자체
> 불확실성(20–30%)** 일 수 있으니 모델 탓 단정 금지(reference≠truth).

---

## §D 해빙 두께 검증 (Thickness) — 겨울 한정·두께대별

Figure: **Fig 08 두께 지도+차이** · **Fig 09 두께대별 산점** · **Fig 10 ITD**

```python
# SAMPLE — 위성 두께는 관측이 아니라 밀도·적설 가정 유도량. 겨울(10–4월)만 가용.
import numpy as np, metrics_basic as mb, metrics_distribution as md
from plots import scatter_si, diff_map

h_mdl = xr_ds["hi"].isel(time=0).values          # SAMPLE: CICE 'hi' (격자평균 두께 m)
h_ref = xr_ds_ref["sea_ice_thickness"].isel(time=0).values   # SAMPLE: CS2SMOS L4
m = np.isfinite(h_mdl) & np.isfinite(h_ref) & (h_ref > 0)    # 위성 유효셀만
of, ff = h_ref[m], h_mdl[m]

print("thk bias =", mb.bias(ff, of), " rmse =", mb.rmse(ff, of), " r =", mb.pearson_r(ff, of))
scatter_si(of, ff, "out/thk_scatter.png", units="m")
diff_map(lat2d, lon2d, np.where(m, h_mdl - h_ref, np.nan),
         "out/thk_bias_map.png", units="m", title="SIT bias (model − reference)")

# ── 두께대별(binned) — 센서 유효두께대(SMOS 박빙 / CryoSat-2 후빙) 분리 ──
from scipy.stats import binned_statistic          # 실존
edges = np.array([0, 0.5, 1.0, 2.0, 3.0, 5.0])    # SAMPLE 두께대(m)
bstat, _, _ = binned_statistic(of, ff - of, statistic="mean", bins=edges)  # 대역별 bias
print("binned bias by thickness class:", bstat)

# ── ITD(두께분포) QQ — CICE 카테고리 면적비 vs 관측 draft 분포 ──
obs_q, mdl_q = md.qq_points(of, ff, n_quantiles=40)   # SAMPLE: 분포형 비교
```

> **주의(SAMPLE)**: 적설 5 cm 오차 = 위성 두께 수십 cm → 두께 검증엔 **적설 오차 병기**.
> ULS/잠수함은 draft 측정 → thickness ≈ draft/0.89 (가정 명시). 위성 두께는 "참값" 아님.

---

## §E 얼음경계 검증 (Ice Edge) — 면적(IIEE) + 거리(MHD)

Figure: **Fig 03 오버레이+IIEE 음영(지도)** · **Fig 05 IIEE 분해** · **Fig 06 거리**

```python
# SAMPLE — 동일 공통격자·동일 임계(15%)·동일 마스크·면적가중 필수(아니면 IIEE 계통편향).
import numpy as np

THRESH = 0.15                                   # SAMPLE: 15% 임계 (민감 — 도메인 확인)
I_mdl = (model >= THRESH)                        # 이진 얼음마스크
I_ref = (ref   >= THRESH)
valid = np.isfinite(model) & np.isfinite(ref)   # SAMPLE: + land/pole hole

# ── IIEE (Goessling et al. 2016) 및 분해 (면적가중) ──
A_plus  = float(np.sum(area[valid & I_mdl & ~I_ref]))   # 모델만 얼음 (over)
A_minus = float(np.sum(area[valid & ~I_mdl & I_ref]))   # 기준만 얼음 (under)
IIEE = A_plus + A_minus
AEE  = abs(A_plus - A_minus)                     # = SIE 오차 절댓값 (absolute extent)
ME   = 2.0 * min(A_plus, A_minus)                # misplacement (위치어긋남)
print(f"IIEE={IIEE:.3e}  AEE={AEE:.3e}  ME={ME:.3e}  (m^2)  IIEE=AEE+ME? {abs(IIEE-(AEE+ME))<1}")

# ── 얼음경계 오버레이 + IIEE 음영 지도 (Fig 03) — 극투영 GeoAxes(SAMPLE) ──
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from plots import add_basemap
try:
    import cartopy.crs as ccrs
    fig = plt.figure(figsize=(6, 6))
    ax  = fig.add_subplot(111, projection=ccrs.NorthPolarStereo())   # SAMPLE: 북극. 남극이면 SouthPolarStereo
    tr  = ccrs.PlateCarree()
    over  = np.where(valid & I_mdl & ~I_ref, 1.0, np.nan)
    under = np.where(valid & ~I_mdl & I_ref, 1.0, np.nan)
    ax.pcolormesh(lon2d, lat2d, np.ma.masked_invalid(over),  transform=tr, cmap="autumn", alpha=0.5)
    ax.pcolormesh(lon2d, lat2d, np.ma.masked_invalid(under), transform=tr, cmap="winter", alpha=0.5)
    ax.contour(lon2d, lat2d, model, levels=[THRESH], colors="red",  linewidths=1.5, transform=tr)  # 모델 경계
    ax.contour(lon2d, lat2d, ref,   levels=[THRESH], colors="black",linewidths=1.5, transform=tr)  # 기준 경계
    add_basemap(ax, lon2d, lat2d)   # 해안선+위경도 라벨(극에서도 안전 fallback)
    ax.set_title("Ice edge overlay + IIEE (A+ over / A- under)\n(advisory — reference≠truth)", fontsize=9)
    fig.savefig("out/iceedge_iiee.png", dpi=100, bbox_inches="tight"); plt.close(fig)
except Exception as e:
    print("SAMPLE: cartopy 극투영 실패 시 diff_map 등으로 대체 —", e)

# ── 얼음경계 거리: Modified Hausdorff Distance (MHD) — 실존 라이브러리 ──
# 경계점 추출 → 구면거리. skimage.find_contours 는 격자인덱스 반환 → lon/lat 로 변환 필요.
from skimage.measure import find_contours          # scikit-image (실존)
from scipy.spatial.distance import directed_hausdorff  # 실존 (순수 Hausdorff)
# MHD 는 평균화 변형 → 직접 구현(Dukhovskoy 2015 권장; 순수 Hausdorff는 이상치 민감)
from scipy.spatial import cKDTree
def mhd_km(edge_a_lonlat, edge_b_lonlat):
    """두 경계 점집합(각 (N,2) lon,lat)의 Modified Hausdorff Distance(km, 근사평면)."""
    # SAMPLE: 정밀 구면거리는 pyproj.Geod.inv 로 교체. 여기선 km 근사(§preprocess 방식).
    def _to_km(pts):
        p = np.asarray(pts, float); latm = np.deg2rad(np.mean(p[:,1]))
        return np.column_stack([p[:,0]*111.2*np.cos(latm), p[:,1]*111.2])
    A, B = _to_km(edge_a_lonlat), _to_km(edge_b_lonlat)
    dA = cKDTree(B).query(A)[0].mean(); dB = cKDTree(A).query(B)[0].mean()
    return float(max(dA, dB))
# edge_mdl_ll, edge_ref_ll 은 find_contours 인덱스를 lon2d/lat2d 로 보간해 만든 (N,2) — SAMPLE
# print("MHD =", mhd_km(edge_mdl_ll, edge_ref_ll), "km")
```

> **경계 추출 규칙 명시(SAMPLE)**: 최대 연결성분·섬/닫힌 만 제거·연안처리 규칙에 결과가
> 크게 좌우된다 → 재현 위해 규칙을 캡션·로그에 남겨라. 순수 Hausdorff(`directed_hausdorff`)는
> 단일 최악점 지배 → MHD/평균변위 권장.

---

## §F 종합 · 적분량 (Taylor/Target · SIE/SIA/SIV)

Figure: **Fig 01 SIC 상태 지도** · **Fig 04 SIE/SIA 계절곡선** · **Fig 16 SIV** · 공통 Taylor

```python
# SAMPLE — Taylor/Target 패턴지표(공간장 한 스냅샷 또는 시계열).
import metrics_pattern as mp    # scripts/metrics_pattern.py — 인자 순서 (o=obs, f=model)!

ts = mp.taylor_stats(o, f)      # {"std_ratio","corr","crmsd","n"}
tg = mp.target_stats(o, f)      # {"bias","urmsd","rmsd","n"}
pc = mp.pattern_correlation(ref, model)   # 공간 패턴 상관(2D→내부 flatten, o,f 순)
print(ts, tg, "pattern_corr =", pc)

from plots import taylor_diagram
taylor_diagram(o, f, "out/sic_taylor.png")   # ※ (obs, fct, out_png)

# ── 적분량: SIE / SIA / SIV — xarray weighted sum (SAMPLE) ──
# cell_area 는 xarray DataArray (m^2). 1e12 m^2 = 1e6 km^2.
cell_area = xr_ds["tarea"]                     # SAMPLE 변수명
sic_da    = sic                                # (time, y, x) [0,1]
ice_mask  = sic_da >= 0.15
SIE = (ice_mask * cell_area).sum(dim=[d for d in cell_area.dims]) / 1e12          # 10^6 km^2
SIA = (sic_da.where(ice_mask) * cell_area).sum(dim=[d for d in cell_area.dims]) / 1e12
# SIV 는 두께 필요: (time,y,x)
thick_da = xr_ds["hi"]                          # SAMPLE
SIV = (sic_da * thick_da * cell_area).sum(dim=[d for d in cell_area.dims]) / 1e12  # 10^3 km^3 (단위 확인)
print("SIE(t0)=", float(SIE.isel(time=0)), "SIA(t0)=", float(SIA.isel(time=0)))

# 계절곡선/시계열 오버레이 (모델 vs 기준 SIE) — 지도 아님
from plots import timeseries_overlay
# timeseries_overlay(t, o, f, out_png): SIE 시계열이면 o=기준SIE, f=모델SIE
# timeseries_overlay(model_times, sie_ref.values, SIE.values, "out/sie_ts.png")
```

> **주의(SAMPLE)**: SIE는 **위치오차를 못 본다**(잘못된 위치의 얼음도 상쇄되면 SIE 일치) →
> §E IIEE/edge 반드시 병행. PIOMAS/재분석 SIV는 관측 아님 → "검증"보다 "상호비교". SIV 단위
> (10^3 km^3 등)는 셀면적·두께 단위로 반드시 재확인.

---

## §G ★ Cross-Domain 적용 (필수 절 — 타 도메인 기법을 이 데이터에)

> 아래는 **해빙 도메인 관행이 아니어도 이 데이터에 유용한 타 도메인 기법**을 실제로 적용한다.
> 각 기법에 "왜 여기서 유용한가" 1줄 + 실행 가능한 SAMPLE 스니펫. 실존 라이브러리만 사용.

### G-1. FSS / 이웃검증 (강수 검증 02에서 차용) → 얼음경계 이중벌점 완화

**왜 유용한가**: 얼음경계(SIC≥15% 이진장)는 강수처럼 경계가 조금만 어긋나도 hit+miss로
이중처벌(double-penalty)된다. 강수 검증의 FSS(이웃검증)로 "어느 공간스케일부터 유용한가"를
정량화하면 점대점 CSI가 놓치는 스케일 정보를 얻는다. → **Fig 15 FSS 스케일–임계 히트맵**.

```python
# SAMPLE — 실존: pysteps.verification.spatialscores.fss (또는 'scores' 패키지 scores.spatial)
import numpy as np
try:
    from pysteps.verification.spatialscores import fss   # 실존
    # I_mdl, I_ref 는 §E 이진 얼음마스크 (0/1). NaN 은 0 으로(육지) — SAMPLE 처리
    fmask = np.where(np.isfinite(model), (model >= 0.15).astype(float), 0.0)
    omask = np.where(np.isfinite(ref),   (ref   >= 0.15).astype(float), 0.0)
    for scale in [1, 3, 5, 11, 21]:          # 이웃크기(격자수) 스캔 — SAMPLE
        val = fss(fmask, omask, thr=0.5, scale=scale)   # thr=0.5: 이진장 임계
        print(f"FSS scale={scale}: {val:.3f}")
    # useful-scale = 0.5 + f0/2 (f0=사건빈도). 계절(겨울 넓음/여름 좁음)마다 기준선 변동.
except ImportError:
    print("SAMPLE: pip install pysteps (또는 scores). 이웃검증은 얼음경계 double-penalty 완화에 유용.")
```

### G-2. SAL / MODE 객체기반 검증 (강수/대류 02에서 차용) → 빙맥·리드·얼음덩어리 객체

**왜 유용한가**: 강수 MODE/SAL은 강수 "덩어리(object)"의 위치·면적·구조를 매칭한다. 해빙의
개별 **얼음덩어리·폴리냐·리드(lead)·빙맥(ridge)** 을 객체로 라벨링해 개수·면적·중심 변위를
비교하면, 격자별 지표가 못 보는 "덩어리 단위" 오차(모델이 폴리냐를 아예 안 만드는지 등)를 잡는다.

```python
# SAMPLE — 실존: scipy.ndimage.label / center_of_mass (MODE/객체검증의 핵심 도구)
from scipy import ndimage                        # 실존
lbl_m, n_m = ndimage.label(model >= 0.15)        # 모델 얼음 객체 라벨
lbl_r, n_r = ndimage.label(ref   >= 0.15)        # 기준 얼음 객체
print(f"객체 수: model={n_m}, ref={n_r}")         # 개수 차 = fragmentation 오차 신호
# 최대 객체 면적·중심(SAL 의 Location/Amplitude 유사)
sizes_m = ndimage.sum(np.ones_like(lbl_m), lbl_m, index=range(1, n_m + 1))
com_m   = ndimage.center_of_mass(model >= 0.15, lbl_m, index=int(np.argmax(sizes_m)) + 1)
print("최대 얼음덩어리 면적(셀수)=", sizes_m.max(), " 중심(y,x)=", com_m)
# SAMPLE: 중심을 lon/lat 로 변환해 model↔ref 매칭·변위(km) 계산 → MODE 스타일 객체 매칭.
# 폴리냐/리드는 (model < 0.15) & (내부) 로 개빙 객체를 라벨링해 동일 절차.
```

### G-3. 벡터·원형 통계 (해류 10 / 파향 07에서 차용) → 해빙 표류(drift) 방향·속력

**왜 유용한가**: 해빙 표류는 해류·바람처럼 **벡터장**이다. 파향/풍향 검증의 원형통계와
해류의 벡터 RMSE를 그대로 쓰면 표류 **방향오차(0/360 wrap 안전)** 와 **속력오차**를 분리
진단할 수 있다(벡터 RMSE만으론 원인 불명). → **Fig 11 quiver 지도**.

```python
# SAMPLE — 실존 스킬 함수 그대로: metrics_circular (파향 검증용) 을 표류 방향에 재사용.
import numpy as np
import metrics_circular as mc     # scripts/metrics_circular.py

# 표류 성분 (u,v) [m/s 또는 2일 변위]. ★ 극투영 격자상대 u/v 는 지리 동/북으로 회전 후 사용.
u_m, v_m = xr_ds["uvel"].values, xr_ds["vvel"].values          # SAMPLE 변수명
u_o, v_o = xr_ds_ref["u"].values, xr_ds_ref["v"].values         # SAMPLE 위성/부이 drift
m = np.isfinite(u_m) & np.isfinite(v_m) & np.isfinite(u_o) & np.isfinite(v_o)

# 방향(도, 0=N 관행이면 arctan2(u,v)) — 원형통계로 방향오차
dir_m = (np.degrees(np.arctan2(u_m[m], v_m[m]))) % 360.0
dir_o = (np.degrees(np.arctan2(u_o[m], v_o[m]))) % 360.0
print("표류 방향 CME =", mc.circular_mean_error(dir_m, dir_o), "deg")  # (forecast, observed)
print("표류 방향 cRMSE =", mc.circular_rmse(dir_m, dir_o), "deg")
print("표류 방향 circ_corr =", mc.circular_corr(dir_m, dir_o))

# 속력·벡터 RMSE (해류 도메인 지표) — numpy
spd_m = np.hypot(u_m[m], v_m[m]); spd_o = np.hypot(u_o[m], v_o[m])
import metrics_basic as mb
print("속력 bias =", mb.bias(spd_m, spd_o), " rmse =", mb.rmse(spd_m, spd_o))
VRMSE = float(np.sqrt(np.mean((u_m[m]-u_o[m])**2 + (v_m[m]-v_o[m])**2)))
print("벡터 RMSE =", VRMSE)

# 표류 방향 분포를 로즈로(파향 로즈 함수 재사용) — 방향×속력
from plots import wave_rose
wave_rose(dir_o, spd_o, "out/drift_rose_obs.png")   # SAMPLE: 관측 표류 방향분포
```

> **표류 함정(SAMPLE)**: ★**시간창 일치**(위성 2일 변위 ↔ 모델 2일 적분변위; 순간속도와 혼동 금지).
> ★**극투영 벡터 회전**(격자상대 u/v → 지리 동/북) 안 하면 방향검증이 통째로 틀린다(흔한 실수).
> 여름 융빙기·저속·fast ice는 위성 추적 실패 많음 → QC/flag 후 제외.

### G-4. Hovmöller (대기/해양 시공간 진단에서 차용) → 얼음경계 위도 전파

**왜 유용한가**: 대기 파동 진단의 Hovmöller(시간×경도)를 얼음경계 위도에 쓰면 계절
**전진(advance)·후퇴(retreat)** 의 경도별 위상·전파를 한 그림에 본다. → **Fig 14**.

```python
# SAMPLE — 각 경도열에서 15% 교차 위도 추출 → (경도×시간) 배열 → pcolormesh (basemap 불필요, 축=경도×시간)
# 경도규약(0–360 vs −180–180)·반구를 캡션에 명시(안 하면 좌우 반전).
# edge_lat[time, lon] = (각 시각·경도에서 sic 가 0.15 를 남↔북 교차하는 위도)  ← 도메인 코드
# import matplotlib.pyplot as plt
# plt.pcolormesh(lon_1d, model_times, edge_lat, cmap="viridis"); plt.xlabel("Longitude"); plt.ylabel("Time")
```

---

## §H 함정 · 주의사항 (Pitfalls — 해빙 특화)

| # | 함정 | 대응(SAMPLE) |
|---|------|--------------|
| H-1 | **SIC는 [0,1] bounded** | 순 bias 상쇄 주의 → 면적가중 RMSE·공간지도 병행. OLS slope 경계 왜곡. |
| H-2 | **면적가중 누락** | 극격자 셀면적 불균일 → `tarea`/`cell_area`로 가중(§B·§E·§F). |
| H-3 | **격자해상도 차 → IIEE 계통편향** | 공통 극격자 재격자화(xesmf) 후 동일 임계·마스크. |
| H-4 | **위성 두께 = 유도량** | 밀도·적설 가정 산물(참값 아님). 적설오차 병기. 겨울 한정. |
| H-5 | **표류 벡터 회전·시간창** | 격자상대 u/v→지리 회전; 위성 2일 변위↔모델 2일 적분(§G-3). |
| H-6 | **극투영 지도** | `add_basemap`은 PlateCarree 기본 → 극은 `NorthPolarStereo` GeoAxes 직접(§E). |
| H-7 | **reference≠truth** | 위성 SIC(알고리즘)·재분석·PIOMAS 모두 reference. 캡션·축 라벨 준수. |
| H-8 | **단일 지표 금지** | SIE만으로 결론 금지 → 범위(SIE)+위치(IIEE/MHD)+분포/두께 최소 3축. |
| H-9 | **인자 순서** | `metrics_basic.*(f,o)` vs `metrics_pattern.*(o,f)` vs `plots.*(o,f)` — 혼동 주의(아래). |

> **★ 인자 순서 요약(읽은 시그니처 기준)**:
> - `metrics_basic.bias/rmse/mae/nrmse/si/pearson_r/linregress(f, o)` — **(forecast, obs)**
> - `metrics_circular.circular_mean_error/circular_rmse/circular_corr(forecast_deg, observed_deg)` — **(forecast, obs)**
> - `metrics_distribution.qq_points/perkins_skill_score/ks_distance(obs, fct)` — **(obs, forecast)**
> - `metrics_pattern.taylor_stats/target_stats/pattern_correlation(o, f)` — **(obs, forecast)**
> - `plots.scatter_si/timeseries_overlay/qq_plot/taylor_diagram(o, f, out_png)` — **(obs, forecast)**
> - `plots.diff_map(lat, lon, diff, out_png, ...)`; `plots.add_basemap(ax, lon, lat, ...)`

---

## §I 그림 카탈로그 매핑 (Fig 32 → 함수)

| Fig # (32) | 이름 | 지도? | 스킬/실존 함수 |
|------------|------|:----:|----------------|
| 01 | SIC 상태 지도 + 15% 경계 | ✅ | 극 GeoAxes `pcolormesh`+`contour`(0.15) + `plots.add_basemap` |
| 02 | SIC 차이(bias) 지도 | ✅ | `plots.diff_map` (2D→발산맵+basemap) |
| 03 | 얼음경계 오버레이+IIEE 음영 | ✅ | 극 GeoAxes(§E) + `plots.add_basemap` |
| 04 | SIE/SIA 계절곡선·시계열 | ❌ | `xarray` weighted sum + `plots.timeseries_overlay` |
| 05 | IIEE 분해(AEE vs ME) | ❌ | numpy 면적가중(§E) + `matplotlib.stackplot` |
| 06 | 얼음경계 거리(MHD·EDE) | ❌* | `skimage.find_contours`+`scipy.spatial`/`pyproj.Geod`(§E) |
| 07 | SIC 산점/밀도(bounded) | ❌ | `plots.scatter_si` + `metrics_basic.*` |
| 08 | 두께 지도+차이 | ✅ | `plots.diff_map` + 극 GeoAxes |
| 09 | 두께대별 산점 | ❌ | `scipy.stats.binned_statistic`(§D) |
| 10 | ITD 히스토그램 g(h) | ❌ | `numpy.histogram` + `metrics_distribution.qq_points` |
| 11 | 표류 quiver 지도 | ✅ | 극 GeoAxes `quiver`(벡터 회전) + `plots.add_basemap`(§G-3) |
| 13 | 확률 ice edge(reliability·ROC·SPS) | ✅* | `xskillscore`(roc·brier_score) + SPS 지도(numpy+basemap) |
| 14 | edge latitude Hovmöller | ❌* | `pcolormesh`(경도×시간)(§G-4) |
| 15 | FSS 스케일–임계 히트맵 | ❌ | `pysteps...fss`(§G-1) + `matplotlib.pcolormesh` |
| 16 | SIV 시계열 | ❌ | `xarray` weighted sum(§F) + `plots.timeseries_overlay` |

> \* Fig 06/14는 요약/Hovmöller라 지도 아님(단 §E 보조 경계선 지도는 basemap 필수);
> Fig 13 SPS 지도·Fig 11 quiver는 지도 필수.

---

## 연관 모듈 참조 (실제 스크립트)

| 모듈 | 이 레시피에서 쓴 실제 함수 |
|------|---------------------------|
| `scripts/io_detect.py` | `open_dataset`, `detect_format`, `UnknownFormatError` |
| `scripts/dataset.py` | `open_nc`, `Dataset(.coord_kind/.latlon/.grid_shape/.variable/.variables/.time_info/.xr/.is_mesh)` |
| `scripts/preprocess.py` | `match_points_to_mesh`, `tz_to_utc`, `common_time_index`, `inject_point_coords`, `build_pairs` |
| `scripts/metrics_basic.py` | `bias`, `mae`, `rmse`, `nrmse`, `si`, `pearson_r`, `linregress` |
| `scripts/metrics_distribution.py` | `quantiles`, `qq_points`, `perkins_skill_score`, `ks_distance` |
| `scripts/metrics_pattern.py` | `taylor_stats`, `target_stats`, `pattern_correlation` |
| `scripts/metrics_circular.py` | `circular_mean_error`, `circular_rmse`, `circular_corr` |
| `scripts/plots.py` | `add_basemap`, `_make_geo_axes`, `scatter_si`, `timeseries_overlay`, `diff_map`, `qq_plot`, `taylor_diagram`, `wave_rose` |

외부 실존 라이브러리(필요시): `numpy`, `scipy`(`spatial`·`stats.binned_statistic`·`ndimage`),
`xarray`, `pandas`, `xesmf`(재격자화), `scikit-image`(`find_contours`), `pyproj`(`Geod`),
`pysteps`/`scores`(FSS), `xskillscore`(확률검증), `cartopy`(극투영·`add_basemap`), `cmocean`(색맵).

---

## 출처 (References — 확인된 DOI만; 미확인은 "(확인요)")

- Goessling, Tietsche, Day, Hawkins & Jung (2016) "Predictability of the Arctic sea ice edge," *GRL* 43(4):1642–1650. **doi:10.1002/2015GL067232** — IIEE·분해(AEE/ME).
- Goessling & Jung (2018) "A probabilistic verification score for contours...," *QJRMS* 144:735–743. **doi:10.1002/qj.3242** — SPS.
- Melsom, Palerme & Müller (2019) "Validation metrics for ice edge position forecasts," *Ocean Science* 15:615–630. **doi:10.5194/os-15-615-2019** — 경계변위·권장 3지표.
- Melsom (2021) "Edge displacement scores," *The Cryosphere* 15:3785–3796. **doi:10.5194/tc-15-3785-2021**.
- Notz (2014) "Sea-ice extent and its trend provide limited metrics of model performance," *The Cryosphere* 8:229–243.
- Notz et al. (2016) SIMIP, *GMD* 9:3427–3446. **doi:10.5194/gmd-9-3427-2016** (확인요 권/페이지).
- Lavergne et al. (2019) OSI SAF/ESA CCI SIC CDR v2, *The Cryosphere* 13:49–78. **doi:10.5194/tc-13-49-2019**.
- Lavergne et al. (2023) OSI SAF sea-ice drift CDR, *ESSD* 15:5807–5834. **doi:10.5194/essd-15-5807-2023**.
- Roberts & Lean (2008) FSS, *Mon. Wea. Rev.* 136:78–97. **doi:10.1175/2007MWR2123.1** (cross-domain G-1).
- Dukhovskoy et al. (2015) "Skill metrics for ... sea ice models," *JGR Oceans* 120 (권/페이지·doi 확인요) — MHD 권장.
- Dubuisson & Jain (1994) "A modified Hausdorff distance for object matching," *Proc. 12th ICPR* — MHD 원 정의.
- Ivanova et al. (2015) 위성 SIC 알고리즘 상호비교, *The Cryosphere* 9:1797–1817 (doi:10.5194/tc-9-1797-2015, 확인요).
- Ricker et al. (2017) CS2SMOS 병합 두께, *The Cryosphere* 11:1607–1623 (doi:10.5194/tc-11-1607-2017, 확인요).
- Warren et al. (1999) "Snow depth on Arctic sea ice," *J. Climate* 12:1814–1829 (확인요) — 적설=두께 최대 오차원.
- Zhang & Rothrock (2003) PIOMAS, *Mon. Wea. Rev.* 131:845–861 (확인요) — SIV 대조(참값 아님).
- Thorndike et al. (1975) "The thickness distribution of sea ice," *JGR* 80:4501–4513 (확인요) — ITD.
- Stammerjohn et al. (2012) "Regions of rapid sea ice change," *GRL* 39, L06501 (doi:10.1029/2012GL050874, 확인요) — advance/retreat(§G-4).
- 기관: EUMETSAT OSI SAF (https://osi-saf.eumetsat.int) · NOAA/NSIDC (https://nsidc.org) · SIPN (https://www.arcus.org/sipn) · CMEMS.

> 주의: "확인요" 표시 논문의 정확한 권·페이지·DOI는 인용 전 원문 재확인(DOI 임의 생성 금지).
> 모든 해석 임계(15% SIE·"겨울 SIC 5–10%"·"MIZ 20–30%"·useful-scale)는 **advisory** —
> 해역·해상도·계절·기준자료 불확실성에 크게 의존한다. 어떤 지표도 단독으로 "좋음/나쁨" 단정 금지.

---

*SAMPLE — 이 스킬은 범용이며 이 파일은 해빙·빙권 한 예시다. 실데이터 구조(변수명·단위·좌표·마스크·투영·시각규약) 점검 후 반드시 맞춤 수정하라. 그대로 실행 금지.*
