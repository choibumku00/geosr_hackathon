---
name: validate-model-output
description: Use when you need to QC-check, validate, or compare numerical/AI model output (NetCDF3/4, GRIB-derived, or CSV) against reanalysis/observation/satellite references — including mixed conventions (K vs °C, 1D/2D grids, unstructured mesh, Korean cp949 CSV), or when the user is unsure what data they have or how to verify it (waves/meteorology/ocean domains).
---

# validate-model-output — Live-Adaptive 검증 두뇌

> **scripts는 "대략적 구조 파악 + 적응의 출발점이 되는 SAMPLE/템플릿"이다.
> 완비 코드가 아니다. 실데이터에서 구조가 예상과 다르면(mesh/cp949/미지포맷/변수명 불일치 등)
> 그 자리에서 throwaway 구조점검 코드를 작성해 확인하고 도메인 맞춤 코드로 적응하라.**

---

## 0. 설치 · 경로 규약 (먼저 읽기 — 모든 예시에 적용)

이 스킬의 코드는 **이 SKILL.md와 같은 폴더**의 `scripts/`·`config/`에 있다. 설치 위치를 `$SKILL`이라 하자
(스킬로 등록 시 보통 `~/.claude/skills/validate-model-output`, 이 저장소에선 `skills/validate-model-output`).

- **의존성(1회)**: `pip install -r "$SKILL/requirements.txt"`
- **★ 아래 모든 예시의 `python scripts/...` 와 `sys.path.insert(0, "scripts")` 는 `$SKILL` 기준이다.**
  현재 작업 폴더(CWD)가 `$SKILL`이 아니면 **풀 경로로** 실행하라:
  - 셸: `python "$SKILL/scripts/cli.py" discover <데이터경로>`  ← 데이터는 절대경로 권장
  - 파이썬: `sys.path.insert(0, "<$SKILL>/scripts")`
  - `cli.py`는 자기 폴더를 `sys.path`에 넣으므로 **어느 CWD에서 풀 경로로 불러도 동작**한다.
- `$SKILL` 실제 경로를 모르면 먼저 확인: `ls "$SKILL/scripts/cli.py"` (또는 SKILL.md가 있는 폴더가 곧 `$SKILL`).

> 한 줄 요약: **명령의 `scripts/`를 `$SKILL/scripts/`로 바꿔 읽어라.** 그러면 어느 프로젝트에서도 동작한다.

---

## PHASE 0 — DISCOVER (분석 전 필수)

### 0-A. 기본 인벤토리

```
python scripts/cli.py discover <폴더 또는 파일...>
```
→ 파일별 포맷·도메인·좌표·역할추정 표 + `inventory.json`.

단일 파일 구조 점검:
```
python scripts/cli.py inspect <파일>
```

### 0-B. 샘플이 못 열거나 구조가 예상 밖이면 — 즉석 throwaway 점검

`openable=false`, `unknown=true`, 또는 인벤토리 결과가 아래 중 하나라도 해당되면
**즉석 throwaway 구조점검 코드를 직접 작성해 실행**하고 결과를 사용자에게 보고한다.
보고 후 reader 확장 또는 도메인 맞춤 파서를 결정한다.

| 증상 | 의심 원인 | 점검 방법 |
|------|-----------|-----------|
| NetCDF 열기 실패 / OSError | 한글 경로, engine 미지정 | `dataset.open_nc(path)` 경유(engine 자동 폴백); `head_hex`로 매직 확인 |
| `lat/lon` 좌표 없음 / `coord_kind='none'` | 비정형 mesh (WW3 UGRID 등) — lat/lon이 좌표가 아닌 data variable | `ds.xr.data_vars` 목록 + 첫 5행 출력으로 구조 확인 |
| CSV UnicodeDecodeError | 한글 헤더, cp949 인코딩 | `pd.read_csv(path, encoding='cp949')` 시도; 컬럼명 alias 매핑 |
| 변수명이 예상 이름과 다름 | 기관별 변수명 관행 차이 | 변수목록 전체 출력 후 유사어 매핑 확인 |
| 단위·dimensions 이상 | 전처리 안 된 원시 출력 | `d.variables()` 전체 출력, `units`·`standard_name` 확인 |

**throwaway 코드 예시 (WW3 mesh 구조 확인)**:
```python
# 즉석 throwaway — 이 파일의 구조를 파악하고 버린다
# open_dataset → Dataset 래퍼(coord_kind/latlon/variables() 메서드 제공)
# open_nc      → xr.Dataset 직접(구조 확인, xr API 그대로 사용)
import sys; sys.path.insert(0, "scripts")
from io_detect import open_dataset   # Dataset 래퍼 반환
d = open_dataset("path/to/file.nc")
print("data_vars:", d.data_var_names())
print("coord_kind:", d.coord_kind())
print("latlon:", d.latlon())
# mesh면 lat/lon이 data_var에 있을 것
import numpy as np
for n in d.data_var_names():
    v = d.variable(n)
    print(f"  {n}: dims={v.dims}, units={v.units}, std={v.standard_name}")
```

**한글 경로 NetCDF 쓰기는 반드시 `dataset.write_nc(ds, dest, **kw)` 경유.**
CSV cp949 읽기는 `pd.read_csv(path, encoding='cp949')`; 컬럼명은 한글 alias→영문 매핑 후 사용.

---

## PHASE 1 — ELICIT (질문으로 구체화)

인벤토리를 사용자에게 제시한 뒤 아래 항목을 확인한다.
사용자가 모르는 것은 가능한 분석을 안내하고 선택하게 한다.

| 질문 | 목적 |
|------|------|
| 어느 파일이 "우리 결과물(모델 출력)"이고 어느 것이 "기준/검증(관측·재분석)"인가? | 역할 확정(파일명 휴리스틱만으로 확정 금지) |
| 분석 도메인이 파랑·기상·해양온도·해류·해수면 중 어느 것인가? | 카탈로그(`project/research/07~11`) 매핑 |
| 관심 변수·기간·해역은? | 분석 범위 결정 |
| 기준자료(ERA5·관측 CSV·위성 고도계 등)를 보유 중인가? | 보유 시 다축 검증, 미보유 시 단독 QC+내부통계 |
| 시간축 시간대(TZ)는? (**★**) | CF `units` ("hours since … UTC") 로 확인. CSV엔 보통 TZ 표기 없음. 모호하면 사용자에 질문. 부이(KST 흔함) vs 모델(UTC)이면 → 아래 ★시간대 처리 참조. |
| 점관측 CSV에 위경도(lat/lon) 컬럼이 있는가? (**★ R3-b**) | 없으면 폴더에서 좌표 파일(points.list 등) 탐색 또는 사용자에 질문 → 아래 ★점관측 좌표 참조. |

> **★ 시간대(TZ) 확인 절차**
> 1. NetCDF: CF `time` 변수의 `units` 속성 ("hours since 1900-01-01 00:00:00 UTC") 우선 확인.
> 2. CSV: 보통 TZ 표기 없음 → 컬럼이나 헤더에 표기가 있으면 읽고, 없으면 사용자에 질문.
> 3. 부이(KST 흔함) vs 모델(UTC) 불일치 시 **매칭 전** `preprocess.tz_to_utc(times, tz='KST')` 로 UTC 정규화.
> 4. TZ 미확인 시: UTC 가정하고 진행 (`assumed=True` 플래그 반환) + 리포트 경고:
>    "TZ 미확인=UTC가정; 부이 KST vs 모델 UTC면 9h 어긋남 위험".

> **★ 점관측 좌표 출처 (R3-b)**
> 점관측 CSV에 lat/lon 없으면:
> 1. 같은 폴더·상위 폴더에서 좌표 파일(points.list, stations.csv, station_info.xlsx 등) 탐색.
> 2. 없으면 사용자에 질문.
> 3. 형식을 실시간으로 파악해 `{정점ID: (lat, lon)}` 매핑 생성.
> 4. `preprocess.inject_point_coords(station_ids, mapping)` 으로 주입.
>
> **코어 자동 경로에 points.list 전용 파서를 박지 말 것** — `preprocess.parse_points_list(path)` 는 에이전트/CLI가 명시 호출할 때만 사용.

**카탈로그 근거**: `project/research/01~15` (지표 메서드) + `project/research/figures/16~22` (그림 유형).
기준자료를 보유하지 않은 경우 가능한 분석(QC·내부통계·도메인 분포 진단)을 먼저 제안하고,
기준자료 확보 후 비교검증이 가능함을 안내한다.

---

## PHASE 2 — 적응형 분석 (도메인 맞춤 코드 실시간 작성)

### 2-A. 도메인 판별

```python
import sys; sys.path.insert(0, "scripts")
from io_detect import open_dataset   # Dataset 래퍼 반환 (detect_domain에 전달)
from router import detect_domain
d = open_dataset("path/to/file")     # Dataset 래퍼; d.xr 로 xr.Dataset 접근
result = detect_domain(d)
print(result)  # {'domain': 'waves', 'confidence': 0.6, 'matched': {...}}
```

도메인이 불확실하면(`confidence < 0.3` 또는 `domain='unknown'`) 사용자에게 보고하고
변수목록을 함께 제시해 도메인을 확인받는다.

### 2-B. QC 실행 (출발 템플릿)

```
python scripts/cli.py validate <파일> --out <폴더>
```
→ PASS/FAIL/WARN 리포트 (`report.json` + `report.md`).

**QC 스크립트(`scripts/qc.py`, `scripts/rules.py`)는 SAMPLE 템플릿이다.**
실데이터에서 변수명·단위·fill_value가 다르면 그 자리에서 `rules.yaml` 규칙을 추가하거나
throwaway 코드로 도메인 맞춤 범위검사를 보강한다.

### 2-C. 도메인별 적응형 분석

도메인이 확정되면 아래 카탈로그를 레퍼런스로 삼아
**그 데이터·그 도메인에 맞는 코드를 실시간 작성**한다.
`scripts/` 파일들은 출발점이지 완성본이 아니다 — 구조가 다르면 새로 작성한다.

| 도메인 | 지표 카탈로그 | 그림 카탈로그 | 핵심 3축 |
|--------|--------------|--------------|---------|
| 파랑(waves) | `project/research/08_domain_waves.md` | `project/research/figures/18_fig_waves.md` | Hs 산점도+SI/bias/RMSE + 시계열/잔차 + QQ·파랑장미 |
| 기상(meteorology) | `project/research/07_domain_meteorology.md` | `project/research/figures/17_fig_meteorology.md` | 풍속·기온 bias/RMSE/SI + 공간지도 + 시계열 |
| 해양온도·염분 | `project/research/09_domain_ocean_temp_salinity.md` | `project/research/figures/19_fig_temp_salinity.md` | SST/S bias/RMSE + 깊이단면 + T-S 다이어그램 |
| 해류 | `project/research/10_domain_currents_circulation.md` | `project/research/figures/20_fig_currents.md` | 속도 벡터 오차 + 유향 원형통계 + 공간지도 |
| 해수면 | `project/research/11_domain_sea_level_tides.md` | `project/research/figures/21_fig_sea_level.md` | SSH bias/RMSE + 조화분석 + 시계열 |

**단일 지표 금지 — 최소 3축 + §G 준수**:
- **정확도+편향축**: bias·RMSE·SI·R 등 수치지표
- **패턴/위상축**: 시계열 중첩·잔차·공간지도
- **분포축**: QQ·PDF/CDF·파랑장미 등 분포 그림
- **§G(해석 함정)**: 모든 임계는 advisory, 기준자료≠참값, 대표성 오차 언급

### 2-D. 파랑 예시 (WW3 mesh + 부이 cp949)

실데이터 구조가 `data/ww3_mesh_like.nc` + `data/buoy_obs_like.csv`(cp949)와 유사하면
아래 흐름을 출발점으로 쓰되, **변수명·노드 수·컬럼명·기간은 반드시 실시간 점검 후 조정**한다.

```python
# SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
import sys; sys.path.insert(0, "scripts")
import pandas as pd
import numpy as np
from io_detect import open_dataset   # Dataset 래퍼 — coord_kind/variables() 등 사용 가능

# ── 1. mesh NetCDF 열기 (lat/lon은 data_var)
# open_dataset이 내부적으로 open_nc(한글경로 안전) 를 호출한다
d = open_dataset("data/ww3_mesh_like.nc")
lon_node = d.xr["longitude"].values   # 실데이터에서 변수명 확인 필수
lat_node = d.xr["latitude"].values
hs_model = d.xr["hs"].values          # shape: (time, node)
times_model = d.xr["time"].values

# ── 2. 부이 CSV cp949 + 한글 alias
df = pd.read_csv("data/buoy_obs_like.csv", encoding="cp949")
# 실데이터 컬럼명 확인 후 alias 매핑
alias = {"일시": "time", "지점": "station",
         "유의파고": "hs_obs", "파향": "dir_obs", "파주기": "tp_obs"}
df = df.rename(columns={k: v for k, v in alias.items() if k in df.columns})
df["time"] = pd.to_datetime(df["time"])

# ── 3. 점 매치업(최근접 노드 + 시간 정렬) — 실데이터 해상도에 맞게 조정
from scipy.spatial import cKDTree
tree = cKDTree(np.column_stack([lon_node, lat_node]))
matched_rows = []
for stn, grp in df.groupby("station"):
    lon_s = float(grp["longitude"].iloc[0]) if "longitude" in grp else None
    lat_s = float(grp["latitude"].iloc[0]) if "latitude" in grp else None
    if lon_s is None:
        continue   # 부이 좌표가 별도 파일에 있으면 거기서 조인
    _, idx = tree.query([lon_s, lat_s])
    for _, row in grp.iterrows():
        t_match = np.argmin(np.abs(times_model - np.datetime64(row["time"])))
        matched_rows.append({
            "time": row["time"],
            "station": stn,
            "hs_obs": row["hs_obs"],
            "hs_model": hs_model[t_match, idx],
        })
pairs = pd.DataFrame(matched_rows).dropna()

# ── 4. 3축 지표 계산
diff = pairs["hs_model"] - pairs["hs_obs"]
bias  = float(diff.mean())
rmse  = float(np.sqrt((diff**2).mean()))
si    = float(diff.std() / pairs["hs_obs"].mean())  # ECMWF LC-WFV 정의(bias 제거)
r     = float(np.corrcoef(pairs["hs_obs"], pairs["hs_model"])[0, 1])
print(f"N={len(pairs)}, bias={bias:.3f} m, RMSE={rmse:.3f} m, SI={si:.3f}, R={r:.3f}")

# ── 5. 파향 원형통계 (0/360° wrap 필수)
if "dir_obs" in df.columns:
    d_diff = np.deg2rad(pairs.get("dir_obs", pd.Series(dtype=float))
                         - pairs.get("dir_model", pd.Series(dtype=float)))
    # wrap: np.angle(np.exp(1j * d_diff))
    # 실데이터: 부이 파향 컬럼명·모델 파향 변수명 확인 필수
    pass

# ── 6. 3축 그림 (산점도 + 시계열 + QQ) — figures/18_fig_waves.md 참조
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# [0] 산점도
axes[0].scatter(pairs["hs_obs"], pairs["hs_model"], alpha=0.4, s=15)
lim = max(pairs[["hs_obs","hs_model"]].max())
axes[0].plot([0,lim],[0,lim],"k--", lw=0.8)
axes[0].set(xlabel="Obs Hs (m)", ylabel="Model Hs (m)",
            title=f"Scatter\nbias={bias:.2f} m  SI={si:.2f}  R={r:.2f}")
# [1] 잔차 시계열 (단일 지점 첫 번째)
stn0 = pairs["station"].iloc[0]
sub = pairs[pairs["station"]==stn0].sort_values("time")
axes[1].plot(sub["time"], sub["hs_obs"],   label="obs")
axes[1].plot(sub["time"], sub["hs_model"], label="model")
axes[1].set(title=f"Time-series: {stn0}", ylabel="Hs (m)")
axes[1].legend()
# [2] QQ
q_obs = np.quantile(pairs["hs_obs"],   np.linspace(0.01,0.99,50))
q_mod = np.quantile(pairs["hs_model"], np.linspace(0.01,0.99,50))
axes[2].plot(q_obs, q_mod, "o", ms=4)
axes[2].plot([0,q_obs.max()],[0,q_obs.max()],"k--", lw=0.8)
axes[2].set(xlabel="Obs quantile", ylabel="Model quantile", title="QQ")
plt.tight_layout()
plt.savefig("hs_validation_3axis.png", dpi=120)
# 캡션 필수: "부이=reference(not truth); 임계SI<0.15는 외해 advisory; 단일 그림으로 결론내지 말 것"
```

**이 코드는 SAMPLE이다.** 실데이터에서는:
- 부이 좌표가 별도 파일에 있을 수 있다 → 아래 ★점관측 좌표(2-E) 참조
- 모델 변수명·부이 컬럼명이 다를 수 있다 → alias 매핑 조정
- mesh 위상(node/element dim 이름)이 다를 수 있다 → `d.data_var_names()` 후 적응
- 시간 해상도·형식이 다를 수 있다 → `pd.to_datetime` 파싱 방법 조정
- 부이 시간대가 KST일 수 있다 → 아래 ★시간대(2-E) 참조
- 파향이 meteorological/oceanographic 규약 중 어느 쪽인지 확인 → wrap 방향 조정

---

### 2-E. ★ 시간대 정규화 & 점관측 좌표 주입

#### ① 시간대(TZ) 정규화

CF time units로 TZ를 확인한다. CSV는 표기가 없는 경우가 많으므로 사용자에게 확인하거나
컬럼 표기(예: "2024-01-01 09:00+09:00")에서 파악한다.

```python
# SAMPLE — 실데이터 TZ 확인 후 tz 인자 조정
import sys; sys.path.insert(0, "scripts")
from preprocess import tz_to_utc

# NetCDF 시간은 보통 CF UTC — d.xr["time"].attrs["units"] 로 확인
# 부이 CSV가 KST(UTC+9)인 경우 아래처럼 정규화
times_buoy_utc, assumed = tz_to_utc(df["time"].values, tz="KST")
# tz=None이면 UTC 가정, assumed=True 반환
if assumed:
    import warnings
    warnings.warn(
        "TZ 미확인=UTC가정; 부이 KST vs 모델 UTC면 9h 어긋남 위험",
        stacklevel=2,
    )
# 리포트 캡션에도 동일 경고 삽입: "관측 시간 TZ 미확인 — UTC 가정, KST면 9h 편이 발생"
```

#### ② 점관측 좌표 주입 (R3-b)

점관측 CSV에 lat/lon 컬럼이 없으면 좌표 파일을 별도로 탐색하거나 사용자에게 받는다.
형식은 실데이터마다 다르므로 에이전트가 실시간으로 파악해 매핑을 생성한다.

```python
# SAMPLE — 형식에 맞게 파싱 방법 조정 (하드코딩 금지)
from preprocess import inject_point_coords
# 예: TSV, CSV, YAML, JSON 어떤 형식이든 실시간 파악 후 매핑 생성
mapping = {
    "부산_앞바다": (35.12, 129.04),
    "제주_성산":   (33.46, 126.93),
}
# preprocess.parse_points_list(path) — 에이전트/CLI가 명시 호출, 코어 자동경로 금지
# 좌표 주입
lats, lons = inject_point_coords(df["station"].values, mapping)
# 이후 cKDTree 매칭에 lats/lons 사용
```

**코어에 points.list 전용 파서를 자동 경로로 박지 말 것.**
`preprocess.parse_points_list(path)` 는 에이전트나 CLI 스크립트가 필요 시 명시적으로 호출하는 도우미 함수다.

---

## PHASE 3 — REPORT

```python
import sys; sys.path.insert(0, "scripts")
from report import write_report
write_report(qc_result, output_dir="results/")
```

**리포트 필수 캡션 원칙** (`project/research/figures/18_fig_waves.md` §G 준수):
1. 기준자료 ≠ 참값: 부이·고도계·ERA5는 reference이지 truth가 아님. 캡션에 "관측 대비" 또는 "ERA5 reference 대비"로 표현.
2. 해석 임계는 advisory: `SI < 0.15`, `R ≥ 0.9`, `평균파향 RMSE 20~30°` 등은 외해 관행값. 해역·해상도 의존. "good/bad" 단정 금지.
3. 단일 그림 금지: 최소 정확도(산점도/지표) + 편향/위상(시계열/잔차) + 분포(QQ/파랑장미) 3장 세트.
4. 대표성 오차 언급: 점 부이 vs 격자/footprint 평균의 차이가 SI에 포함됨.
5. 근거 명시: 사용한 지표 정의(SI는 bias 제거형 vs 포함형)와 참고문헌 출처.

---

## 도메인별 카탈로그 빠른 참조

```
project/research/
  00_overview_taxonomy.md   — 전체 검증 체계·§G(해석 함정 7원칙)
  01_error_statistics.md    — bias·RMSE·MAE·NRMSE·스킬스코어
  02_spatial_pattern.md     — 공간 패턴(EOF·상관지도)
  03_categorical_extremes.md — POD·FAR·CSI·GEV/GPD·재현주기
  05_spectral_eof.md        — 스펙트럼·EOF·모드분해
  06_timeseries_signal.md   — 시계열·lag 상관·STL
  07_domain_meteorology.md  — 기상 도메인 카드
  08_domain_waves.md        — 파랑 도메인 카드 ★
  09_domain_ocean_temp_salinity.md
  10_domain_currents_circulation.md
  11_domain_sea_level_tides.md
  12_satellite_remote_sensing.md — 위성·고도계·콜로케이션
  14_ai_ml_evaluation.md   — AI/ML 모델 평가
  15_preprocessing_regridding.md — 재격자·콜로케이션 전처리
  figures/
    16_fig_common.md        — 공통 그림(Taylor·Target·rank histogram)
    17~22_fig_*.md          — 도메인별 그림 카탈로그 ★
```

> **원칙**: 기준자료는 truth가 아니라 reference. 해석 임계는 advisory.
> 단일 지표/그림으로 결론내지 않는다.
> scripts는 완비가 아닌 SAMPLE — 실데이터 구조 맞춤 코드를 그 자리에서 작성하라.
