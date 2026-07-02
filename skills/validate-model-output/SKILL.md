---
name: validate-model-output
description: Use when you need to QC-check, validate, or compare numerical/AI/satellite model output (NetCDF3/4, GRIB-derived, or CSV) against reanalysis/observation/satellite references — including mixed conventions (K vs °C, 1D/2D grids, unstructured mesh, Korean cp949 CSV, KST vs UTC), or when the user is unsure what data they have or how to verify it. Covers waves/meteorology/ocean/currents/sea-level/satellite/AI-ML domains, recommends paper-based verification methods (including cross-domain ones when useful), draws map-based figures with coastlines and lat/lon labels, and iteratively deepens the verification (analyze results → suggest and run additional checks).
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

> **자동 분석 금지.** DISCOVER로 포맷·구조·좌표·역할을 먼저 파악하고, PHASE 1에서 사용자에게 확인받기 전에는 지표·플롯 분석을 시작하지 마라. 파일명 휴리스틱만으로 "모델 출력 / 기준자료" 역할을 단정하지 마라.

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

> **필수 항목(역할·도메인·기준자료·시간대(TZ)·좌표 출처)이 확정되기 전에는 PHASE 2 분석을 시작하지 마라.** 에이전트가 스스로 추정한 값(단위·컬럼 의미·TZ 등)은 "추정"임을 밝히고, 모호하면 반드시 사용자에게 되물어 확정한 뒤 진행한다.

| 질문 | 목적 |
|------|------|
| 어느 파일이 "우리 결과물(모델 출력)"이고 어느 것이 "기준/검증(관측·재분석)"인가? | 역할 확정(파일명 휴리스틱만으로 확정 금지) |
| 분석 도메인이 무엇인가? (파랑·기상·해양·해수면·해빙·수문·대기질… 지구시스템 어느 분야든; 미상 가능) | 카탈로그 매핑 — 미상이면 데이터특성 기반 일반 배터리로 진행 |
| **산출물 종류**: 물리모델 / AI·ML / 위성(원격탐사) 중 무엇인가? (복수 가능) | AI·위성은 도메인이 아니라 물리 도메인 배터리에 **얹는 평가축**(§2-C) |
| **자료형**: 격자(grid/mesh)인가 정점(점)·시계열인가? | `characterize`가 자동 감지하나 확인. 정점·시계열도 격자와 동급 1급 경로(§2-C) |
| 관심 변수·기간·해역은? | 분석 범위 결정 |
| 기준자료(ERA5·관측 CSV·위성 고도계 등)를 보유 중인가? | 보유 시 다축 검증. **미보유 시** 도메인 카드의 대표 기준자료(예: 토양수분→ISMN/SMAP, ET→FLUXNET, SST→GHRSST, 파랑→부이/고도계)를 근거로 **확보 후보를 능동 제안** + 단독 QC·내부통계 안내 |
| 모델과 기준자료의 **단위·스케일이 일치**하는가? (예: m³/m³ vs %, K vs °C, Pa vs hPa) | 불일치 시 매칭 전 정규화(`preprocess`) — 놓치면 전 지표 무의미 |
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
> 5. **끝내 좌표를 못 구하면** 정점 위치도·격자↔점 매칭을 **"불가"로 보고**하고 강행하지 마라. 좌표 없는 정점을 조용히 건너뛰어(예: `continue`) 검증이 축소된 채 '성공'처럼 보이게 하지 말 것.
>
> **코어 자동 경로에 points.list 전용 파서를 박지 말 것** — `preprocess.parse_points_list(path)` 는 에이전트/CLI가 명시 호출할 때만 사용.

> **★ 기준자료 메타 재탐색 (G4)**
> 사용자가 기준자료(재분석·관측·위성 등)를 보유하면, 그 파일도 모델 파일과 **동일하게** discover/inspect(+필요시 throwaway 코드)로 변수명·단위·컬럼 의미·좌표·시간대(TZ)·도메인을 재파악하라. "기준자료라 구조가 자명하다"고 가정하지 말 것. 단위·격자·TZ가 모델과 다르면 매칭 전에 정규화(`preprocess`)한다.

**카탈로그 근거**: `references/research/01~15` (지표 메서드) + `references/research/figures/16~22` (그림 유형).
기준자료를 보유하지 않은 경우 가능한 분석(QC·내부통계·도메인 분포 진단)을 먼저 제안하고,
기준자료 확보 후 비교검증이 가능함을 안내한다.

---

## PHASE 2 — 적응형 분석 (도메인 맞춤 코드 실시간 작성)

### 2-A. 데이터 특성 우선 판별 (characterize — 도메인은 2차)

**분야를 먼저 정하지 말고, 데이터 특성(자료형·변수성질)을 먼저 파악하라.** 이것이 범용성의 핵심이다 — 검증법은 분야가 아니라 자료형·변수성질에서 따라 나오므로, 카탈로그에 없는 분야(대기질·수문/하천·해빙·토양수분·우주기상 등)도 동작한다. 도메인은 *2차 힌트*일 뿐이다.

```python
import sys; sys.path.insert(0, "scripts")
from io_detect import open_dataset
from router import characterize
d = open_dataset("path/to/file")
prof = characterize(d)
print(prof["data_form"])        # {'form':'grid'|'mesh'|'point_timeseries'|'profile'|'spectrum'|..., 'has_ensemble':..}
print(prof["variable_natures"]) # {변수: ['vector'|'circular'|'nonnegative'|'extreme_prone'|'fraction'|..]}
print(prof["domain"])           # {'domain':.., 'confidence':.., 'candidates':{..}, 'ambiguous':bool}  ← 2차 힌트
print(prof["triggers"])         # 데이터에서 감지된 추가 검증축(앙상블·극값·방향·벡터·스펙트럼)
print(prof["note"])             # 다음 행동 지침
```

**★ 절대 멈추지 마라 (미지/애매 도메인 안전망)**: `domain=='unknown'` 이거나 `ambiguous=True`여도 **강제로 도메인을 끼워 맞추지 마라.** `characterize`가 준 **일반 배터리(C-0) + triggers**로 진행하고, ELICIT에서 사용자에게 도메인·역할을 확인한다. 도메인 표에 없는 분야는 "가장 가까운 카드 + 데이터특성 트리거"로 조합한다. (`references/research/00_overview_taxonomy.md` C-0 공통·C-2 트리거·D 횡단표가 근거.)

> **★ 고신뢰 오탐 방지 (weak_evidence)**: `characterize`가 `weak_evidence=True`(대표변수 headline 없이 잡혔거나 일부 물리변수가 어느 도메인에도 미매칭 = `unmatched_vars>0`)를 주면 **confidence가 1.0이어도 도메인을 단정하지 마라.** 또한 **단위·standard_name이 없는 물리변수**(예: 정체불명 `t2`)는 정체·단위(기온이면 K인지 °C인지 — 오판 시 bias 273 틀어짐)를 **반드시 사용자에게 되물어 확정**한 뒤 분석하라. 소수 변수 하나의 일반매칭만으로 도메인을 확정하고 나머지 변수를 방치하지 말 것.

#### 데이터 성질 → 검증법 (분야 무관 규칙)

| 감지된 성질·자료형 | 반드시 쓰는(피하는) 방법 | 카탈로그 |
|---|---|---|
| **원형(circular)** 파향·풍향·유향 | 원형통계(circmean/circstd)·circular RMSE·0/360 wrap. **일반 평균/RMSE 금지** | `08`·`10`, figures `18`/`20` |
| **벡터(vector)** u/v 성분 | 복소·벡터 상관(Kundu/Crosby)·성분별 오차·벡터 RMSE | `10` |
| **양수·꼬리(nonnegative/extreme_prone)** 강수·파고·풍속·유량 | 로그/√ 변환·곱셈적 지표·QQ + **극치(POT/GPD·GEV·재현주기)** | `01`·`03` |
| **분율(fraction 0–1)** 해빙율·구름량 | bounded 지표·(임계화 시)Brier·reliability | `03` |
| **앙상블 축 존재** | rank histogram·CRPS·reliability·spread-skill | `03`·`13`·`14` |
| **격자·mesh(공간)** | 공간 bias/RMSE map(**해안선+위경도 필수**)·패턴상관/ACC·FSS | `02`, figures `16` |
| **프로파일/단면(vertical)** | 깊이별 매치업·단면·T-S 다이어그램 | `09` |
| **스펙트럼(spectrum)** | PSD·파수/방향 스펙트럼·유효해상도 | `05`·`08` |

> 이 표가 곧 범용 엔진이다: 도메인이 무엇이든(심지어 미상이어도) 감지된 성질에 해당하는 행을 모두 적용하면 최소 다축 검증이 성립한다.

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
| 파랑(waves) | `references/research/08_domain_waves.md` | `references/research/figures/18_fig_waves.md` | Hs 산점도+SI/bias/RMSE + 시계열/잔차 + QQ·파랑장미 |
| 기상(meteorology) | `references/research/07_domain_meteorology.md` | `references/research/figures/17_fig_meteorology.md` | 풍속·기온 bias/RMSE/SI + 공간지도 + 시계열 |
| 해양온도·염분 | `references/research/09_domain_ocean_temp_salinity.md` | `references/research/figures/19_fig_temp_salinity.md` | SST/S bias/RMSE + 깊이단면 + T-S 다이어그램 |
| 해류 | `references/research/10_domain_currents_circulation.md` | `references/research/figures/20_fig_currents.md` | 속도 벡터 오차 + 유향 원형통계 + 공간지도 |
| 해수면 | `references/research/11_domain_sea_level_tides.md` | `references/research/figures/21_fig_sea_level.md` | SSH bias/RMSE + 조화분석 + 시계열 |
| 위성·원격탐사(satellite) | `references/research/12_satellite_remote_sensing.md` | `references/research/figures/22_fig_satellite.md` | 매치업 산점 + 대표성오차 + track/grid 공간지도 |
| AI·ML 산출물 | `references/research/14_ai_ml_evaluation.md` | `references/research/figures/16_fig_common.md` | 결정론지표 + 분포/스펙트럼(블러 진단) + 앙상블·UQ(rank hist/CRPS) |
| 강수(precipitation) | `references/research/23_domain_precipitation.md` | `references/research/figures/31_fig_precipitation.md` | 범주형 탐지(POD/FAR/CSI/ETS/HSS) + 공간·double-penalty(FSS·SAL/MODE) + 분포·극치(강도 PDF·POT/GEV·ETCCDI) |
| 해빙·빙권(sea ice) | `references/research/24_domain_sea_ice.md` | `references/research/figures/32_fig_sea_ice.md` | SIC 농도장(bias/RMSE, 0–1) + 얼음경계·범위(SIE/IIEE·Hausdorff) + 두께·표류(freeboard·drift 벡터) |
| 대기질·대기화학(air quality) | `references/research/25_domain_air_quality.md` | `references/research/figures/33_fig_air_quality.md` | 로그공간 성능기준(MFB/MFE·NMB/NME·FAC2) + 초과사건·주기(POD/FAR·일변동) + 측정소 대표성·위성 컬럼(NO2·AOD) |
| 수문·하천(hydrology) | `references/research/26_domain_hydrology.md` | `references/research/figures/34_fig_hydrology.md` | 유량곡선 적합(KGE/NSE·PBIAS) + 수문서명·물수지(FDC·BFI·closure) + 극치·시기(홍수빈도·첨두 timing) |
| 육상(지표, land surface) | `references/research/27_domain_land_surface.md` | `references/research/figures/35_fig_land_surface.md` | 물·에너지(토양수분 삼중대조·LST·ET·EBR) + 저장·눈(SWE·SCA) + 식생·복사(LAI·GPP·알베도) |
| 구름·복사(clouds & radiation) | `references/research/28_domain_clouds_radiation.md` | `references/research/figures/36_fig_clouds_radiation.md` | 복사플럭스 bias·수지닫힘 + 구름장(운량·연직·τ–p) + 구름복사효과 CRE(COSP) |
| 해양 생지화학·해색 | `references/research/29_domain_ocean_biogeochemistry.md` | `references/research/figures/37_fig_ocean_biogeochemistry.md` | 로그정규 해색통계(log10·MdSA·매치업) + 탄산계·산성화(pCO2·pH·Ω) + 표층/심층·계절(WOA/GLODAP/BGC-Argo) |
| 우주기상(space weather) | `references/research/30_domain_space_weather.md` | `references/research/figures/38_fig_space_weather.md` | 지수 fit(RMSE·PE) + 사건탐지(HSS·POD/FAR) + timing(ΔtA·DTW) |

> **★ cross-domain 적용 (도메인에 가두지 마라 — 추천이 아니라 실행)**: 위 표(도메인별 3축)는 출발점일 뿐이다. **도메인 배터리만 돌리고 끝내지 마라.** 명백한 도메인 지표에 더해, 그 도메인에서 관행이 아니어도 **이 데이터에 유용한 타 도메인·공통 검증법을 반드시 함께 탐색하고, 유용하면 실제로 수행**하라(무엇을·왜 적용했는지 보고에 명시). 근거는 `references/research/00_overview_taxonomy.md`의 C-2(비도메인 트리거)·D절(횡단표), **실제 적용 예는 `references/recipe_*.md`의 "cross-domain 적용" 절**:
> - **어느 도메인이든 공통(항상 고려)**: Taylor/Target 다이어그램, bootstrap 유의성, QQ·분포거리(Perkins/KS) → `references/research/figures/16_fig_common.md`
> - **데이터 특성 트리거(해당하면 실행)**: 앙상블 차원 → 확률검증(rank histogram·CRPS·reliability); 극값 꼬리 → 극치(POT/GPD·GEV·재현주기) `03`; 2D 영상형 필드 → 공간구조(SSIM/FSS) `02`; 방향변수 → 원형통계 `10`; AI 산출물 → 스펙트럼·구조지표·UQ/OOD `14`.
> - 적용한 타 도메인 기법마다 "왜 이 데이터에 유용한지" 1줄 근거를 붙여라(§G 근거 명시).

> **참고 문서**: 실데이터 적응 패턴 `references/adapting.md` · **도메인 worked 레시피 `references/recipe_*.md`**(기상·파랑·강수·해빙·대기질·수문·육상·해양BGC — 각 실제 스킬 함수 사용 + "cross-domain 적용" 절 포함, 모두 SAMPLE) · 지도 그림 `references/plotting_maps.md` · **새 분야 추가 `references/extending.md`** · 데이터 흐름 `references/architecture.md`.

**단일 지표 금지 — 최소 3축 + §G 준수**:
- **정확도+편향축**: bias·RMSE·SI·R 등 수치지표
- **패턴/위상축**: 시계열 중첩·잔차·공간지도
- **분포축**: QQ·PDF/CDF·파랑장미 등 분포 그림
- **§G(해석 함정)**: 모든 임계는 advisory, 기준자료≠참값, 대표성 오차 언급

#### ★ AI·위성은 '도메인'이 아니라 '얹는 축'(overlay)

AI·ML·위성은 분야가 아니라 **어느 물리 도메인 위에나 얹히는 평가축**이다. 물리 도메인 배터리를 먼저 깔고 그 위에 축을 더한다:
- **AI·ML 축**: 결정론 지표 + UQ(ECE/PICP/CRPS)·OOD/롤아웃 안정성·스펙트럼(블러/유효해상도)·물리정합(보존량/PDE residual). → `references/research/14_ai_ml_evaluation.md`
- **위성 축**: 시공간 매치업·대표성오차·삼중대조(TC/ETC)·L2/L3/L4 처리수준. → `references/research/12_satellite_remote_sensing.md`
- 예) *AI 해빙농도 예보 검증* = 해빙(물리 도메인: SIC/SIE·IIEE) + AI 축(UQ·스펙트럼) + (위성 대조 시) 위성 축(매치업·대표성오차).

#### ★ 정점(점)·시계열 검증 — 격자와 동급 1급 경로

`data_form=='point_timeseries'`(검조소·부이·관측소·ADCP CSV 등)는 격자 못지않은 1급 경로다. 격자↔점 비교는 최근접/이중선형 매치업(`preprocess`) 후:
- **정점별 + 통합 지표**: 정점마다 bias·RMSE·SI·R을 내고, 전 정점 pooled 통계도 함께(정점 간 편차 = 공간대표성 신호).
- **시간축**: 관측·모델 시계열 overlay + 잔차, **위상**(교차상관 best_lag·DTW), 결측 정렬.
- **분포축**: QQ·PDF/CDF (+극값이면 POT/GEV).
- **위치 식별(필수)**: 정점을 **해안선+위경도 지도**에 마커+ID로 표시(§PHASE3 원칙 6, `references/plotting_maps.md`). "어느 정점인지" 모르면 검증 무의미.
- **대표성 오차**: 점 관측 vs 격자셀/footprint 평균 차이가 지표에 섞임을 캡션에 명시.

### 2-D. 워크플로 골격 (분야·자료형 무관) + 분야별 레시피

아래는 **어느 분야·자료형에도 공통인 골격**(열기 → 데이터특성 파악 → (기준자료 있으면) 매치업·정규화 → 다축 지표 → 다축 그림 → 반복 심화)의 최소 스켈레톤이다. **특정 분야(파랑 등)에 매이지 않는다** — 구체 코드는 아래 분야별 레시피를 출발점으로 삼되 **변수명·좌표·단위·기간은 실시간 점검 후 맞춤 수정**하라.

> **다른 분야 worked 예시**: 정점·시계열(대기질 `references/recipe_air_quality.md`·수문 `references/recipe_hydrology.md`), 격자·bounded(해빙 `references/recipe_sea_ice.md`), 범주형·이웃(강수 `references/recipe_precipitation.md`), 삼중대조(육상 `references/recipe_land_surface.md`), 로그정규(해양BGC `references/recipe_ocean_biogeochemistry.md`) — 각 실제 스킬 함수 + cross-domain 적용 절 포함. **모두 SAMPLE이니 그대로 실행하지 말고 네 데이터 구조에 맞춰 새로 짜라.**

```python
# SAMPLE 골격 (분야·자료형 무관) — 실데이터 구조를 실시간 점검하고 맞춤 코드로 적응하라.
import os, sys
SKILL = os.environ.get("SKILL", os.getcwd())              # 스킬 폴더($SKILL): 설치 위치/CLI 인자로 교체
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from io_detect import open_dataset
from router import characterize
import metrics_basic as mb                                # 실제 함수·인자순서는 scripts/ 확인
from plots import scatter_si, timeseries_overlay, diff_map, qq_plot, taylor_diagram, add_basemap

# 1) 열기 + 데이터 특성 파악(도메인은 2차). 미지/근거빈약(weak_evidence)·무단위 변수는 사용자에 확인 후 진행.
d = open_dataset("<model.nc | .csv>")                     # 실제 경로/CLI 인자로
prof = characterize(d)                                    # data_form·variable_natures·triggers·domain·weak_evidence·note
print(prof["data_form"], prof["domain"], prof["triggers"], prof["note"])

# 2) 기준자료가 있으면 열고 '메타 재탐색' 후 매치업·정규화(preprocess):
#    격자↔정점 = match_points_to_mesh / inject_point_coords · 시간대 = tz_to_utc · 단위불일치(K/°C·m3/m3 vs %) 정규화
#    정점 좌표를 끝내 못 구하면 '정점검증 불가'로 보고(강행 금지).

# 3) 다축 지표(성질에 맞게, 단일 지표 금지): 정확도+편향 / 분포 / 시간·공간
#    예) mb.bias(f, o), mb.rmse(f, o)  ← 실제 인자 순서는 metrics_basic.py 확인
#    원형변수=metrics_circular · 분포=metrics_distribution · 공간=metrics_pattern

# 4) 다축 그림: scatter_si / timeseries_overlay / qq_plot / taylor_diagram
#    지도형(격자 bias·정점 위치)은 diff_map 또는 add_basemap → 해안선+위경도 필수

# 5) cross-domain 적용(필수): triggers 반영 — 앙상블→CRPS·rank hist / 극값→POT·GEV
#    / 방향→원형통계 / 2D 필드→FSS·SSIM  (관행 아니어도 이 데이터에 유용하면 실제로 수행)

# 6) §G 캡션(기준자료≠참값·임계 advisory·단일지표 금지) 삽입 + PHASE 4 반복 심화.
```

**이 골격은 SAMPLE이다 — 그대로 실행하지 말고 네 데이터에 맞춰 새로 짜라.** 분야별 구체 코드(실제 스킬 함수 + cross-domain 적용 절)는 `references/recipe_*.md`(파랑·기상·강수·해빙·대기질·수문·육상·해양BGC)를 출발점으로 삼되, 변수명·좌표·단위·시간대·격자/mesh 위상·컬럼명은 실시간 점검 후 조정한다.

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

**리포트 필수 캡션 원칙** (`references/research/00_overview_taxonomy.md` §G 준수):
1. 기준자료 ≠ 참값: 부이·고도계·ERA5는 reference이지 truth가 아님. 캡션에 "관측 대비" 또는 "ERA5 reference 대비"로 표현.
2. 해석 임계는 advisory: `SI < 0.15`, `R ≥ 0.9`, `평균파향 RMSE 20~30°` 등은 외해 관행값. 해역·해상도 의존. "good/bad" 단정 금지.
3. 단일 그림 금지: 최소 정확도(산점도/지표) + 편향/위상(시계열/잔차) + 분포(QQ/파랑장미) 3장 세트.
4. 대표성 오차 언급: 점 부이 vs 격자/footprint 평균의 차이가 SI에 포함됨.
5. 근거 명시: 사용한 지표 정의(SI는 bias 제거형 vs 포함형)와 참고문헌 출처.
6. **지도 위 그림엔 위치정보 필수**: 위경도 좌표계 그림(정점 위치도·격자 bias/RMSE map·mesh 노드·위성 트랙)은 **해안선/육지 윤곽 + 위경도 눈금 라벨**을 반드시 포함해 "어디인지" 식별 가능해야 한다. 정점 검증은 정점 마커+ID 라벨 + 데이터 범위로 확대(zoom) + 필요시 위치 인셋맵. → 드롭인 헬퍼·오프라인 대응은 `references/plotting_maps.md`, 코드 진입점은 `scripts/plots.py`. 산점도·QQ·Taylor·시계열·로즈처럼 축이 지리좌표가 아닌 그림엔 지도를 넣지 않는다.

---

## PHASE 4 — DEEPEN (반복 심화 — 단일 패스 종료 금지)

**1차 REPORT로 끝내지 마라.** 검증은 지표 한 번 산출이 아니라, 결과를 읽고 다음 검증을 제안·수행하며 품질을 끌어올리는 **반복 과정**이다. 새 실패모드가 안 나올 때까지 아래 루프를 돈다.

1. **판독**: 1차 결과를 구조적으로 읽는다 — 잔차의 공간편향? 분포 꼬리 어긋남(QQ)? 위상 지연(best_lag≠0)? 특정 해역·계절·조건에서만 나쁜가? §G 함정에 걸리지 않았나?
2. **약점 → 다음 검증 선택**: 관찰된 약점을 겨냥해 `references/research/`(특히 `00`의 C-2 트리거·D절)에서 **추가할 2차 검증**을 근거와 함께 고른다. 증상별 예시:

   | 1차에서 관찰된 증상 | 추가할 2차 검증 | 카탈로그 |
   |---|---|---|
   | QQ 상단 꼬리 편차 큼 | 극치분석(POT/GPD·GEV·재현주기) | `03` |
   | best_lag≠0 / 위상 어긋남 | lag 상관·DTW·교차상관 | `06` |
   | 잔차가 특정 해역/계절 집중 | 해역별·계절별 층화(`--regions`)·bias map | `02`,`figures/16` |
   | 앙상블 차원 존재 | 확률검증(rank histogram·CRPS·reliability) | `figures/16`,`14` |
   | 공간 패턴 의심 | 패턴상관/ACC·EOF·FSS | `02`,`05` |
   | 편향 원인 불명 | 조건부 편향(값·시간·조건별)·층별 분해 | `01`,`06` |
3. **수행**: 선택한 검증을 SAMPLE 코드 적응 또는 신규 작성으로 실행한다(구조가 다르면 그 자리에서 맞춤 코드).
4. **누적·재판독**: 결과를 리포트에 추가하고 1로 돌아간다.
5. **종료 조건**: 새 실패모드/의문이 더 안 나오고 최소 3축 + 도메인 특이 축 + 유의성이 채워졌을 때 멈춘다. 매 라운드에서 "다음에 무엇을·왜 더 볼지"를 사용자에게 제안하고 방향을 정하게 한다.

> 반복 심화 체크리스트(복붙용):
> ```
> [ ] 1차 3축(정확도·분포·시간/공간) 완료
> [ ] 잔차/꼬리/위상/공간·계절 층화 판독
> [ ] 극값(필요시) · 확률(앙상블시) · 공간패턴 축 추가
> [ ] cross-domain 공통(Taylor/Target·유의성) 추가
> [ ] 지도 그림에 해안선+위경도 확인
> [ ] 새 실패모드 없음 → 종료
> ```

---

## 도메인별 카탈로그 빠른 참조

```
references/research/            # ← $SKILL 기준 내부 경로. 도메인 분석 전 항상 00부터 열어 라우팅하라.
  00_overview_taxonomy.md                    — 전체 검증 체계·C절(도메인→recipe)·D절(횡단표)·§G(해석 함정 6원칙)
  01_error_statistics.md                     — bias·RMSE·MAE·NRMSE·스킬스코어
  02_spatial_pattern_verification.md         — 공간 패턴(EOF·상관지도·FSS·SAL/MODE)
  03_categorical_event_extremes.md           — POD·FAR·CSI·GEV/GPD·재현주기
  04_conservation_energy_flux.md             — 보존·에너지·플럭스 정합
  05_spectral_eof_modal.md                   — 스펙트럼·EOF·모드분해
  06_timeseries_signal.md                    — 시계열·lag 상관·STL
  07_domain_meteorology.md                   — 기상 도메인 카드
  08_domain_waves.md                         — 파랑 도메인 카드 ★
  09_domain_ocean_temp_salinity.md           — 해양 수온·염분
  10_domain_currents_circulation.md          — 해류·순환
  11_domain_sea_level_tides.md               — 해수면·조석
  12_satellite_remote_sensing.md             — 위성·고도계·콜로케이션
  13_model_intercomparison_downscaling.md    — 다모델 비교·다운스케일
  14_ai_ml_evaluation.md                     — AI/ML 모델 평가
  15_preprocessing_regridding_colocation.md  — 재격자·콜로케이션 전처리
  23_domain_precipitation.md                 — 강수(범주형·FSS·SAL/MODE·극치·QPE)
  24_domain_sea_ice.md                       — 해빙·빙권(SIC·SIE/IIEE·표류·두께)
  25_domain_air_quality.md                   — 대기질·화학(로그통계·초과사건·MFB/NMB·위성)
  26_domain_hydrology.md                     — 수문·하천(KGE/NSE·FDC·홍수빈도)
  27_domain_land_surface.md                  — 육상(토양수분 TC·LST·ET·적설·식생)
  28_domain_clouds_radiation.md              — 구름·복사(플럭스 bias·운량·CRE·COSP)
  29_domain_ocean_biogeochemistry.md         — 해양 BGC·해색(Chl-a·탄산계·영양염·O2)
  30_domain_space_weather.md                 — 우주기상(Kp/Dst·TEC·태양풍·사건)
  figures/
    16_fig_common.md                         — 공통 그림(Taylor·Target·QQ·rank histogram) ★
    17_fig_meteorology.md … 22_fig_satellite.md · 31_fig_precipitation.md … 38_fig_space_weather.md — 도메인별 그림 카탈로그 ★
```

> **원칙**: 기준자료는 truth가 아니라 reference. 해석 임계는 advisory.
> 단일 지표/그림으로 결론내지 않는다.
> scripts는 완비가 아닌 SAMPLE — 실데이터 구조 맞춤 코드를 그 자리에서 작성하라.
