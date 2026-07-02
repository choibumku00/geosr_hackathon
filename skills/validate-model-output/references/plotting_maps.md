# 지도 기반 검증 그림 (Geospatial verification plots)

> **핵심 규칙**: 그림의 축이 **지리좌표(경도·위도)** 이면 그것은 "지도"다 — **해안선/육지 윤곽 + 위경도 눈금 라벨**을 반드시 넣어 "어디인지" 식별 가능하게 하라. 사람은 지도 없는 격자/정점 그림에서 위치를 못 읽는다.
> scripts/plots.py의 SAMPLE은 의존성 최소화를 위해 지도 없이 그린다 — **실데이터 그림에는 아래 `add_basemap()`으로 지도를 반드시 씌워라.**

## 목차 (TOC)
- [A. `add_basemap()` 드롭인 헬퍼 (cartopy + 안전 fallback)](#a-add_basemap-드롭인-헬퍼)
- [B. 지도가 필요한 그림 vs 아닌 그림 (판단 규칙)](#b-지도가-필요한-그림-vs-아닌-그림)
- [C. 정점/관측소 검증 — 위치를 분명히](#c-정점관측소-검증--위치를-분명히)
- [D. 오프라인/무네트워크 대응](#d-오프라인무네트워크-대응)
- [E. 흔한 함정](#e-흔한-함정)
- [출처](#출처)

---

## A. `add_basemap()` 드롭인 헬퍼

설계: (1) cartopy + Natural Earth 데이터가 있으면 해안선 + 육지 + 라벨된 위경도 격자선을 그리고 데이터 bbox+여백으로 extent 자동설정; (2) cartopy가 없거나 데이터를 못 받거나(오프라인/프록시) 어느 단계든 실패하면 — **격자선만 있는 graticule로 강등 + 경고**를 내서 그림이 절대 비지 않고 실패가 보이게 한다. zoom 폭에 따라 해안선 해상도 자동 선택.

`scripts/plots.py`에 이미 이식돼 있다 — `from plots import add_basemap`. 아래는 그 정의(참조·복붙용):

```python
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def _data_bbox(lon, lat, margin_deg=0.5):
    """데이터의 [w, e, s, n] 경계 + 여백 (NaN 안전). 단일 정점도 0크기 안 되게 최소폭 보장."""
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)
    w = np.nanmin(lon) - margin_deg
    e = np.nanmax(lon) + margin_deg
    s = np.nanmin(lat) - margin_deg
    n = np.nanmax(lat) + margin_deg
    if e - w < 2 * margin_deg:
        c = 0.5 * (w + e); w, e = c - margin_deg, c + margin_deg
    if n - s < 2 * margin_deg:
        c = 0.5 * (s + n); s, n = c - margin_deg, c + margin_deg
    return [w, e, s, n]


def _auto_resolution(extent):
    """지도 span(도)으로 Natural Earth 해안선 해상도 선택."""
    span = max(extent[1] - extent[0], extent[3] - extent[2])
    if span <= 15:   return '10m'   # 지역/연안 확대 → 정밀
    if span <= 60:   return '50m'
    return '110m'                   # 전지구/해역 → 저해상도로 충분


def _fallback_graticule(ax, extent, msg):
    """cartopy 불가 시 순수 matplotlib 격자선(위경도 라벨) — 그림이 비지 않게 + 경고."""
    warnings.warn(
        f"add_basemap: 해안선 없이 격자선만 그림 ({msg}). "
        "제대로 된 지도를 원하면 cartopy 설치 + Natural Earth 데이터 캐시.",
        RuntimeWarning,
    )
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    # 중위도 왜곡 보정(1° lon ≠ 1° lat)
    ax.set_aspect(1.0 / np.cos(np.deg2rad(0.5 * (extent[2] + extent[3]))))
    ax.grid(True, linestyle='--', color='0.6', alpha=0.6)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{abs(x):g}°{'E' if x >= 0 else 'W'}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda y, _: f"{abs(y):g}°{'N' if y >= 0 else 'S'}"))
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.text(0.99, 0.01, "no coastline (offline)", transform=ax.transAxes,
            ha='right', va='bottom', fontsize=7, color='crimson', alpha=0.8)
    return ax


def add_basemap(ax, lon, lat, margin_deg=0.5, resolution=None,
                land=True, gridlabels=True):
    """지리 basemap(해안선+육지+라벨된 위경도 격자선)을 ax에 추가하고
    extent를 (lon, lat) bbox + 여백으로 설정한다.

    cartopy 경로를 쓰려면 ax가 GeoAxes여야 한다:
        import cartopy.crs as ccrs
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    일반 Axes를 넘기면 격자선-only fallback으로 동작한다.
    cartopy/데이터 부재 시에도 절대 예외를 던지지 않는다. ax를 반환.
    """
    extent = _data_bbox(lon, lat, margin_deg)
    if resolution is None:
        resolution = _auto_resolution(extent)

    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    except Exception as e:                       # cartopy 미설치
        return _fallback_graticule(ax, extent, f"cartopy import 실패: {e}")

    if not hasattr(ax, "projection"):            # GeoAxes 아님
        return _fallback_graticule(ax, extent, "ax가 cartopy GeoAxes가 아님")

    try:
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        if land:
            ax.add_feature(cfeature.LAND.with_scale(resolution),
                           facecolor='0.85', zorder=0)
        ax.add_feature(cfeature.COASTLINE.with_scale(resolution),
                       linewidth=0.6, zorder=1)
        # ax.add_feature(cfeature.BORDERS.with_scale(resolution), linewidth=0.4)
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=gridlabels,
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xformatter = LongitudeFormatter()     # 축마다 새 인스턴스 필요
        gl.yformatter = LatitudeFormatter()
        return ax
    except Exception as e:
        # 대개 Natural Earth shapefile 미캐시 + 네트워크 없음.
        try:
            ax.set_extent(extent, crs=ccrs.PlateCarree())
        except Exception:
            pass
        return _fallback_graticule(ax, extent, f"cartopy 런타임 오류: {e}")
```

메모:
- `.with_scale('10m'|'50m'|'110m')` 로 해상도 제어(= `ax.coastlines(resolution='10m')`).
- 해안선은 위(`zorder=1`), 육지는 아래(`zorder=0`) → scatter/pcolormesh 데이터가 깔끔히 겹침.
- `LongitudeFormatter()`/`LatitudeFormatter()`는 축마다 **새 인스턴스**로 생성(한 인스턴스는 한 축만).

---

## B. 지도가 필요한 그림 vs 아닌 그림

**규칙**: **축 중 하나라도 경도 또는 위도이면 지도** → 해안선/육지 + 라벨된 위경도 격자선 필수. 두 축이 모두 "데이터 공간"(값·분위수·시간·방향·주파수)이면 지도가 아니다 → basemap 넣지 말 것.

| 그림 유형 | 지도 필요? | 축 |
|---|:---:|---|
| 정점/관측소 위치도 | ✅ | lon × lat |
| 격자 bias/difference map (model−obs) | ✅ | lon × lat |
| RMSE/SI/상관 공간 map | ✅ | lon × lat |
| 위성/고도계 track 콜로케이션 map | ✅ | lon × lat |
| 모델 도메인/mesh 노드 개요 | ✅ | lon × lat |
| 산점도 1:1 (model vs obs) | ❌ | obs × model |
| QQ / 분위수 | ❌ | obs q × model q |
| Taylor / target | ❌ | std·상관 공간 |
| 시계열 | ❌ | time × value |
| 파랑/해류 로즈 | ❌ | 방향×크기(polar) |
| PDF/CDF/히스토그램 | ❌ | value × density |
| 스펙트럼 | ❌ | freq × energy |

자동 적용: x/y 변수명·단위가 lon/lat로 해석되면 `add_basemap()` 경유, 아니면 일반 플롯.

---

## C. 정점/관측소 검증 — 위치를 분명히

읽는 사람이 정점이 **어디인지** 항상 알게:

1. **위치 마커 지도**: 모든 정점을 해안선 지도 위 마커로(`add_basemap`), extent는 정점 군집 + 여백(`margin_deg≈0.5~1.0`)으로 확대. 군집이 촘촘하면 `10m` 해안선 필수(→ E).
2. **정점 ID 라벨**: 각 마커 옆에 정점ID(`ax.annotate`/`ax.text`, 약간 offset). 번호/색을 패널 제목과 맞춤.
3. **각 산점/시계열 패널에 위치 동반**: 패널 구석에 **인셋 로케이터맵**(해안선 위 단일 정점 점) + 제목에 위경도, 예 `Buoy 22101 (129.87°E, 35.35°N)`. 통계와 장소를 직접 연결.
4. **지역 맥락 인셋**: 확대 군집엔 넓은 extent 인셋 + 확대영역 사각형 표시.
5. **위경도 항상 표기**: 확대 지도에도 라벨된 격자선(add_basemap 기본). 격자선이 성기면 제목/캡션에 좌표 명기.

인셋 로케이터 스케치:
```python
import cartopy.crs as ccrs
axins = ax.inset_axes([0.68, 0.02, 0.30, 0.30], projection=ccrs.PlateCarree())
add_basemap(axins, region_lon, region_lat, margin_deg=1.0, gridlabels=False)
axins.plot(st_lon, st_lat, 'r*', ms=8, transform=ccrs.PlateCarree())
```

---

## D. 오프라인/무네트워크 대응

실패 원인: cartopy는 첫 사용 시 Natural Earth shapefile을 네트워크에서 받는다. **네트워크 없음/프록시/서버 다운**이면 `add_feature`/`coastlines`가 예외·행업 → "빈 지도"의 원인. 대응:

1. **graceful fallback(위 헬퍼 내장)** — 어떤 실패든 라벨 격자선-only로 강등 + 경고. 그림은 비지 않고 원인은 로그됨.
2. **Natural Earth 미리 캐시**: 네트워크 되는 머신에서
   ```bash
   cartopy_feature_download physical            # coastline, land, ocean, lakes
   ```
   캐시 위치(기본): `~/.local/share/cartopy/shapefiles/natural_earth/...` (Windows: `%LOCALAPPDATA%\cartopy\...`). 커스텀 경로는 env `CARTOPY_DATA_DIR`(풀 경로, `~` 확장 안 됨) 또는 코드 `cartopy.config["pre_existing_data_dir"] = "/path"`.
3. **conda 오프라인 번들**: `conda install -c conda-forge cartopy_offlinedata` (shapefile 동봉, 다운로드 불필요).
4. **해상도 vs 용량**: `110m`(작음/전지구) · `50m`(지역) · `10m`(연안 확대, 큼). 실제 쓰는 해상도만 캐시.
5. **geopandas 대안**: cartopy 없이 스킬에 해안선 shapefile을 동봉하면 `geopandas.read_file("coastline.shp")` → `gdf.plot(ax=ax)` 로 일반 Axes에 그리고 격자선은 수동. 다운로드 의존 제거.
6. **`mpl_toolkits.basemap` 쓰지 말 것** — deprecated. cartopy가 후속.

---

## E. 흔한 함정

1. **연안 확대에 해안선이 너무 거침**: 기본/`110m`는 연안 스케일에서 뭉개져 정점이 육지인지 바다인지 안 보임. 지역/연안엔 `10m`(또는 `50m`). `add_basemap`이 span으로 자동 선택.
2. **경도 규약 불일치(0–360 vs −180–180)**: Natural Earth 해안선은 −180…180. 모델 lon이 0…360이면 날짜변경선 부근/해역 전체가 반대편/화면 밖. 그리기 전 변환: `lon = ((lon + 180) % 360) - 180`. 태평양 중심은 `ccrs.PlateCarree(central_longitude=180)`.
3. **`pcolormesh` vs `contourf` (곡선/비정형 격자)**: 곡선(2D lon/lat)·비정형은 `pcolormesh`(삼각 mesh는 `tripcolor`/`tricontourf`) + `transform=ccrs.PlateCarree()`. `contourf`는 보간으로 mesh를 뭉갬. 가능하면 셀 **모서리** 좌표를 넘겨 반셀 밀림 방지.
4. **해양 격자의 육지 마스킹**: 해양 전용 필드는 육지에서 `np.ma.masked_where`/NaN 후, 육지를 필드 **위**(`cfeature.LAND` 높은 zorder)로 그려 보간 쓰레기가 대륙에 번지지 않게.
5. **bias 발산 컬러바의 0중심**: model−obs bias는 발산맵 + **0=흰색**. `matplotlib.colors.TwoSlopeNorm(vcenter=0, vmin=..., vmax=...)` + `RdBu_r`(또는 `cmocean.cm.balance`). RMSE/SI 등 비음수는 순차맵(`cmocean.cm.thermal`/`viridis`).
6. **중위도 종횡비 왜곡**: PlateCarree에서 1° lon ≠ 1° lat. GeoAxes는 자동 처리, fallback은 `set_aspect(1/cos(mean_lat))`(내장).
7. **중복 눈금 라벨**: `gl.top_labels=False`, `gl.right_labels=False`로 정리.

---

## 출처
- Cartopy: Gridlines and tick labels — https://cartopy.readthedocs.io/latest/gallery/gridlines_and_labels/gridliner.html
- Cartopy: Feature interface — https://scitools.org.uk/cartopy/docs/latest/matplotlib/feature_interface.html
- Cartopy: natural_earth shapereader / 데이터 캐시(issue #1325, #1072)
- GeoViews: Using Features Offline (cartopy_offlinedata, CARTOPY_DATA_DIR)
- Pythia Foundations: Introduction to Cartopy
- NOAA WAVEWATCH III Production Validation Archive; "Problems in RMSE-based wave model validations" (Ocean Modelling, Mentaschi et al. 2013)
