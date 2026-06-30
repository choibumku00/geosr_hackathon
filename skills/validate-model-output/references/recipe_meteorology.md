# Recipe: 기상 격자 검증 (Meteorology Grid Validation)

> **SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.**
> 이 문서는 GFS ↔ ERA5 비교 흐름을 출발점으로 제시하는 템플릿이다.
> 실 데이터의 변수명·단위·격자·시간 기준이 다를 수 있으므로 각 단계를 반드시 수정해서 사용한다.

---

## 빠른 참조 (Quick Reference)

| 단계 | 핵심 함수 | 주요 Figure |
|------|-----------|-------------|
| A. 전처리 | `open_nc`, `Dataset.coord_kind()`, 단위 변환 | — |
| B. 기온 | `metrics_accuracy(t_ref, t_test)` | Fig 01 Scatter · Fig 02 Bias Map |
| C. 바람 | `metrics_wind(u_ref, v_ref, u_test, v_test)` | Fig 03 Scatter WS · Fig 04 WD Rose |
| D. 차이지도 | `plot_diff_map(lon, lat, diff)` | Fig 05 Diff Map |
| E. Taylor | `plot_taylor(stats)` | Fig 06 Taylor |
| F. 해역 crop | `crop_region(lon, lat, bbox)` | Fig 07 Region |

---

## §A 전처리 (Preprocessing)

### A-1 모델 NetCDF 열기

```python
# SAMPLE — GFS / ERA5 파일 열기; 한글 경로 우회는 open_nc() 내장
from dataset import open_nc, Dataset
from io_detect import open_dataset
from router import detect_domain

# GFS (GRIB → NetCDF 변환 후 or wgrib2 출력)
xr_gfs  = open_nc("gfs_fcst.nc")
# ERA5 (Copernicus CDS 다운로드, NetCDF4)
xr_era5 = open_nc("era5_reanalysis.nc")

d_gfs  = Dataset(xr_gfs,  source="GFS",  fmt="netcdf4")
d_era5 = Dataset(xr_era5, source="ERA5", fmt="netcdf4")

# 도메인 자동 판별
dom_gfs  = detect_domain(d_gfs)   # 기대: {"domain": "meteorology", ...}
dom_era5 = detect_domain(d_era5)
```

### A-2 단위 정규화 (°C ↔ K, hPa ↔ Pa)

```python
# SAMPLE — 실데이터에서 units attribute 를 반드시 확인하라
import numpy as np

def ensure_celsius(arr: np.ndarray, units: str) -> np.ndarray:
    """기온을 °C 로 통일."""
    units = (units or "").strip().lower()
    if units in ("k", "kelvin"):
        return arr - 273.15
    if units in ("c", "celsius", "degc", "°c"):
        return arr
    raise ValueError(f"알 수 없는 기온 단위: '{units}' — 실데이터 확인 필요")

def ensure_ms(arr: np.ndarray, units: str) -> np.ndarray:
    """풍속을 m/s 로 통일."""
    units = (units or "").strip().lower()
    if units in ("m/s", "m s-1", "ms-1"):
        return arr
    if units in ("kt", "knots", "kts"):
        return arr * 0.51444
    if units in ("km/h",):
        return arr / 3.6
    raise ValueError(f"알 수 없는 풍속 단위: '{units}' — 실데이터 확인 필요")

# 사용 예
var_t2m_gfs  = d_gfs.variable("TMP_2maboveground")   # 변수명은 모델마다 다름
var_t2m_era5 = d_era5.variable("t2m")

t_gfs  = ensure_celsius(xr_gfs["TMP_2maboveground"].values,
                         var_t2m_gfs.units or "K")
t_era5 = ensure_celsius(xr_era5["t2m"].values,
                         var_t2m_era5.units or "K")
```

### A-3 2D / 1D 격자 정렬 (Grid Alignment)

```python
# SAMPLE — GFS 1D × ERA5 1D, 또는 GFS 2D vs ERA5 1D 조합 등 다양
import numpy as np
import xarray as xr

def align_grids(ds_ref: xr.Dataset, ds_test: xr.Dataset,
                method: str = "nearest") -> xr.Dataset:
    """
    ds_ref 격자에 ds_test 를 보간·정렬.
    1D × 1D : xr.interp 사용.
    2D / 비정형 : scipy NearestNDInterpolator 권장 (SAMPLE).
    """
    kind_ref  = Dataset(ds_ref).coord_kind()   # '1d'|'2d'|'none'
    kind_test = Dataset(ds_test).coord_kind()

    if kind_ref == "1d" and kind_test == "1d":
        return ds_test.interp(
            lat=ds_ref["lat"], lon=ds_ref["lon"],
            method=method, kwargs={"fill_value": np.nan}
        )
    # 2D 또는 비정형 → 직접 구현 필요 (recipe_waves §A-3 참조)
    raise NotImplementedError(
        f"격자 조합 ({kind_ref}, {kind_test})은 직접 구현 필요 — 실데이터 확인"
    )
```

> **실데이터 점검 항목**
> - 경도 범위: -180–180 vs 0–360 → `lon = (lon + 180) % 360 - 180` 로 통일
> - 위도 방향: 남→북 vs 북→남 → `lat[::-1]` 또는 `ds.sortby("lat")`
> - 시간 기준: UTC 확인; GFS fcst 시각은 base_time + lead_time 으로 계산
> - 변수명: GFS `TMP_2maboveground` vs ERA5 `t2m` vs RDAPS `T2` 등

---

## §B 기온 검증 (Temperature Validation)

Figure 카탈로그: **Fig 01 T2m Scatter**, **Fig 02 Bias Map**

```python
# SAMPLE metrics_accuracy — recipe_waves §B 와 동일 구조
import numpy as np

def metrics_accuracy(obs: np.ndarray, mdl: np.ndarray) -> dict:
    """
    기온(°C)·기타 연속변수 정확도.
    obs, mdl : 동일 shape, NaN 포함 가능.
    """
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    n = len(o)
    if n < 2:
        return {"n": n, "bias": np.nan, "rmse": np.nan,
                "si": np.nan, "r": np.nan, "slope": np.nan}
    bias  = float(np.mean(m - o))
    rmse  = float(np.sqrt(np.mean((m - o)**2)))
    mu_o  = float(np.mean(o))
    si    = rmse / abs(mu_o) if abs(mu_o) > 0 else np.nan
    r     = float(np.corrcoef(o, m)[0, 1])
    slope = float(np.polyfit(o, m, 1)[0])
    return {"n": n, "bias": bias, "rmse": rmse, "si": si, "r": r, "slope": slope}

# 사용 예 — 격자 평균 비교 (flatten 후 matchup)
stats_t2m = metrics_accuracy(t_era5.ravel(), t_gfs.ravel())
print(f"T2m  Bias={stats_t2m['bias']:.2f}°C  RMSE={stats_t2m['rmse']:.2f}°C  r={stats_t2m['r']:.3f}")
```

### 기온 지표 참고 기준

| 지표 | 양호 | 주의 | 불량 |
|------|------|------|------|
| Bias (°C) | |·| < 0.5 | 0.5–2.0 | > 2.0 |
| RMSE (°C) | < 1.5 | 1.5–3.0 | > 3.0 |
| r | > 0.98 | 0.90–0.98 | < 0.90 |

---

## §C 바람 검증 (Wind Validation)

Figure 카탈로그: **Fig 03 Wind Speed Scatter**, **Fig 04 Wind Direction Rose Overlay**

### C-1 풍속·풍향 변환

```python
# SAMPLE — u/v 성분 → 풍속·풍향 변환; 실데이터 단위 확인
import numpy as np

def uv_to_speed_dir(u: np.ndarray, v: np.ndarray) -> tuple:
    """
    u (eastward), v (northward) → (speed, direction_deg).
    direction: 기상학적 관습(바람이 불어오는 방향, 0°=N, 90°=E).
    """
    speed = np.sqrt(u**2 + v**2)
    # atan2 결과는 수학적 각도(E기준 반시계) → 기상 방향으로 변환
    wdir  = (270.0 - np.rad2deg(np.arctan2(v, u))) % 360.0
    return speed, wdir

# GFS
u10_gfs  = ensure_ms(xr_gfs["UGRD_10maboveground"].values,
                      d_gfs.variable("UGRD_10maboveground").units or "m/s")
v10_gfs  = ensure_ms(xr_gfs["VGRD_10maboveground"].values,
                      d_gfs.variable("VGRD_10maboveground").units or "m/s")
ws_gfs, wd_gfs   = uv_to_speed_dir(u10_gfs, v10_gfs)

# ERA5
u10_era5 = ensure_ms(xr_era5["u10"].values, d_era5.variable("u10").units or "m/s")
v10_era5 = ensure_ms(xr_era5["v10"].values, d_era5.variable("v10").units or "m/s")
ws_era5, wd_era5 = uv_to_speed_dir(u10_era5, v10_era5)
```

### C-2 풍속 정확도

```python
stats_ws = metrics_accuracy(ws_era5.ravel(), ws_gfs.ravel())
print(f"WS10  Bias={stats_ws['bias']:.2f}m/s  RMSE={stats_ws['rmse']:.2f}m/s  r={stats_ws['r']:.3f}")
```

### C-3 풍향 원형통계

```python
# SAMPLE metrics_directional — recipe_waves §E 와 동일 구조
import numpy as np

def metrics_directional(dir_obs: np.ndarray, dir_mdl: np.ndarray,
                         deg: bool = True) -> dict:
    """원형 통계(Circular Statistics) — 풍향(WD) 검증."""
    mask = np.isfinite(dir_obs) & np.isfinite(dir_mdl)
    o, m = dir_obs[mask], dir_mdl[mask]
    if deg:
        o, m = np.deg2rad(o), np.deg2rad(m)
    mean_obs = float(np.arctan2(np.mean(np.sin(o)), np.mean(np.cos(o))))
    mean_mdl = float(np.arctan2(np.mean(np.sin(m)), np.mean(np.cos(m))))
    diff = m - o
    diff = (diff + np.pi) % (2 * np.pi) - np.pi
    circ_bias = float(np.mean(diff))
    circ_rmse = float(np.sqrt(np.mean(diff**2)))
    if deg:
        mean_obs  = np.rad2deg(mean_obs) % 360
        mean_mdl  = np.rad2deg(mean_mdl) % 360
        circ_bias = np.rad2deg(circ_bias)
        circ_rmse = np.rad2deg(circ_rmse)
    return {"mean_dir_obs": mean_obs, "mean_dir_mdl": mean_mdl,
            "circ_bias_deg": circ_bias, "circ_rmse_deg": circ_rmse}

stats_wd = metrics_directional(wd_era5.ravel(), wd_gfs.ravel())
print(f"WD circ_bias={stats_wd['circ_bias_deg']:.1f}°  circ_RMSE={stats_wd['circ_rmse_deg']:.1f}°")
```

---

## §D 차이지도 (Difference Map)

Figure 카탈로그: **Fig 05 T2m Diff Map**, **Fig 06 WS10 Diff Map**

```python
# SAMPLE plot_diff_map — 공간 분포로 계통 오차 구역 파악
import numpy as np

def plot_diff_map(lon2d: np.ndarray, lat2d: np.ndarray,
                  diff: np.ndarray, title: str = "Model - Reference",
                  vmax: float | None = None):
    """
    Fig 05/06 — (모델 − 참조) 2D 차이지도.
    lon2d, lat2d, diff : 동일 (ny, nx) shape.
    vmax: colorbar 대칭 최대값; None 이면 자동.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mc

        if vmax is None:
            vmax = float(np.nanpercentile(np.abs(diff), 95))
        norm = mc.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

        fig, ax = plt.subplots(figsize=(9, 6))
        pcm = ax.pcolormesh(lon2d, lat2d, diff, cmap="RdBu_r", norm=norm)
        fig.colorbar(pcm, ax=ax, label="Model − Ref")
        ax.set(title=title, xlabel="Longitude", ylabel="Latitude")
        return fig
    except ImportError:
        return None   # no-crash

# 사용 예 — ERA5 를 참조로 GFS 차이
diff_t2m = t_gfs - t_era5   # (ny, nx) 또는 (time, ny, nx) → 시간평균 후
fig_diff  = plot_diff_map(lon2d, lat2d, diff_t2m.mean(axis=0),
                           title="GFS T2m − ERA5 T2m (°C)")
```

---

## §E Taylor Diagram (종합 검증)

Figure 카탈로그: **Fig 07 Taylor Diagram**

```python
# SAMPLE — recipe_waves §F 와 동일 구조; 기상 변수 여러 개를 한 그림에 비교
import numpy as np

def taylor_stats(obs: np.ndarray, mdl: np.ndarray) -> dict:
    mask = np.isfinite(obs) & np.isfinite(mdl)
    o, m = obs[mask], mdl[mask]
    sig_o  = float(np.std(o))
    sig_m  = float(np.std(m))
    r      = float(np.corrcoef(o, m)[0, 1])
    crmse  = float(np.sqrt(sig_o**2 + sig_m**2 - 2 * sig_o * sig_m * r))
    return {"sigma_ref": sig_o, "sigma_test": sig_m, "r": r, "crmse": crmse,
            "sigma_norm": sig_m / sig_o if sig_o > 0 else np.nan}

# 여러 변수 한번에
stats_all = {
    "T2m":  taylor_stats(t_era5.ravel(),  t_gfs.ravel()),
    "WS10": taylor_stats(ws_era5.ravel(), ws_gfs.ravel()),
}
for name, s in stats_all.items():
    print(f"{name:6s}  σ_norm={s['sigma_norm']:.3f}  r={s['r']:.3f}  CRMSE={s['crmse']:.3f}")
```

---

## §F 해역 Crop (Region Masking)

Figure 카탈로그: **Fig 08 Region Mask**

```python
# SAMPLE — 1D 격자 자료는 xr.sel 로 간단히 crop 가능
def crop_domain_1d(ds: "xr.Dataset", lat_name: str, lon_name: str,
                    bbox: tuple) -> "xr.Dataset":
    """
    bbox = (lon_min, lon_max, lat_min, lat_max)
    1D lat/lon 격자 전용. 2D는 Boolean mask 적용.
    """
    lon_min, lon_max, lat_min, lat_max = bbox
    return ds.sel(
        **{lat_name: slice(lat_min, lat_max),
           lon_name: slice(lon_min, lon_max)}
    )

# 한반도 주변 해역
BBOX_KOR = (124.0, 132.0, 33.0, 38.5)

xr_gfs_kor  = crop_domain_1d(xr_gfs,  "lat", "lon", BBOX_KOR)
xr_era5_kor = crop_domain_1d(xr_era5, "latitude", "longitude", BBOX_KOR)
# 주의: ERA5 위도가 역순(90→-90)이면 slice(38.5, 33.0) 로 수정
```

---

## §G 함정 및 주의사항 (Pitfalls)

### G-1 기온 단위 혼용 (°C vs K)

- GFS GRIB2 → NetCDF 변환 도구에 따라 °C 또는 K 로 저장됨
- ERA5 CDS 다운로드: 기본 K → ensure_celsius() 필수
- 점검: `d.variable("t2m").units` 또는 `xr_ds["t2m"].attrs["units"]`

### G-2 경도 0–360 vs -180–180 충돌

```python
# 0–360 → -180–180 변환 (ERA5 ↔ GFS 흔한 조합)
import numpy as np
import xarray as xr

def wrap_lon(ds: xr.Dataset, lon_name: str = "lon") -> xr.Dataset:
    lon = ds[lon_name].values
    if lon.max() > 180:
        lon = (lon + 180) % 360 - 180
        ds  = ds.assign_coords({lon_name: lon})
        ds  = ds.sortby(lon_name)
    return ds
```

### G-3 시간 기준·예보 리드타임

- GFS `init_time + lead_hour` ≠ ERA5 valid_time 직접 비교 주의
- 단기 예보(06h이내) vs 중기(72h+): 오차 특성이 다름 — 리드타임별로 분리 검증 권장
- 점검: `d.time_info()` → `start`, `end`, `n_steps` 확인

### G-4 압력 레벨 자료

- ERA5 다중 레벨(pressure_level) vs GFS 단일 레벨 NetCDF 비교 시:
  원하는 레벨(예: 850 hPa)을 `.sel(level=850)` 로 슬라이스한 뒤 비교
- 단위: hPa (ERA5) vs Pa (일부 GFS) — `1 hPa = 100 Pa`

### G-5 2D/1D 좌표 혼용

```python
# 실데이터 coord_kind 점검 예
from dataset import Dataset
d = Dataset(open_nc("gfs_fcst.nc"), source="GFS")
print(d.coord_kind())   # '1d' | '2d' | 'none'
print(d.latlon())       # (lat_name, lon_name, is_2d)
print(d.grid_shape())   # (ny, nx)
```

---

## §H Figure 카탈로그 전체 (Figures Catalog)

| Fig # | 이름 | 축(X → Y) | 함수 | 비고 |
|--------|------|-----------|------|------|
| **01** | T2m Scatter | ERA5 → GFS | `plot_scatter(t_ref, t_test)` | 1:1 선 |
| **02** | T2m Bias Map | 위경도 → bias | `plot_map(lon, lat, bias)` | 공간 분포 |
| **03** | WS10 Scatter | ERA5 → GFS | `plot_scatter(ws_ref, ws_test)` | 풍속 |
| **04** | WD Rose Overlay | 방향 → 빈도 | `plot_rose_overlay(wd_ref, wd_test)` | 풍향 |
| **05** | T2m Diff Map | 위경도 → ΔT | `plot_diff_map(lon, lat, diff)` | [§D] |
| **06** | WS10 Diff Map | 위경도 → ΔWS | `plot_diff_map(lon, lat, diff)` | [§D] |
| **07** | Taylor Diagram | σ·r 극좌표 | `plot_taylor(stats_list)` | 다중 변수 |
| **08** | Region Mask | 위경도 지도 | `plot_map_mask(lon, lat, mask)` | [§F] |
| **09** | T2m RMSE Map | 위경도 → RMSE | `plot_map(lon, lat, rmse)` | 공간 |
| **10** | WS RMSE Map | 위경도 → RMSE | `plot_map(lon, lat, rmse)` | 공간 |
| **11** | T2m Bias by Season | 계절 → bias | `plot_bar_season(...)` | 계절 변동 |
| **12** | Diurnal Cycle | 시 → T2m | `plot_diurnal(t_obs, t_mdl)` | 일변화 |
| **13** | Wind Hodograph | U → V | `plot_hodograph(u, v)` | 바람 벡터 |
| **14** | T2m Timeseries | Datetime → T2m | `plot_timeseries(...)` | 지점 |
| **15** | WS Timeseries | Datetime → WS | `plot_timeseries(...)` | 지점 |
| **16** | Precip Scatter | ERA5 → GFS | `plot_scatter(prcp_ref, prcp_test)` | 강수 |
| **17** | MSLP Bias Map | 위경도 → bias | `plot_map(lon, lat, mslp_bias)` | 해면기압 |
| **18** | Multi-var Table | 변수 × 지표 | `render_table(stats_dict)` | 보고서 요약 |

> Fig 07 Taylor · Fig 18 Multi-var Table 은 최종 보고서에서 항상 포함 권장.

---

## 연관 모듈 참조

| 모듈 | 핵심 인터페이스 | 역할 |
|------|----------------|------|
| `scripts/dataset.py` | `open_nc`, `Dataset` | NetCDF 로딩·좌표 추상화 |
| `scripts/io_detect.py` | `open_dataset`, `detect_format` | 포맷 자동 판별 |
| `scripts/router.py` | `detect_domain` | 도메인 분류(meteorology/waves/…) |
| `scripts/qc.py` | `run_qc`, `check_variable` | 층위1 QC(범위·결측·격자·시간) |
| `scripts/report.py` | `write_report`, `render_markdown` | QC 리포트 생성 |
| `config/domains.yaml` | meteorology 도메인 규칙 | 변수 표준명·패턴 |

---

*SAMPLE — 도메인 맞춤 적응 없이 그대로 운용 금지. 실 데이터 구조 점검 후 수정.*
