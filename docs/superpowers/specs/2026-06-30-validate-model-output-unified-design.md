# 통합 설계 스펙: `validate-model-output` — 수치모델 후처리·검증·다축분석 자동화 스킬

- 날짜: 2026-06-30
- 작성자: 최범규 (A팀)
- 대회: 예보사업부 AI·AX 해커톤 (공통과제 = 반복 수작업 1개 자동화)
- 채점 나침반: 과정 70(①활용깊이25 ②**재현성·전파성25** ③전원참여10 ④문제정의10) + 결과 30(⑤완성도15 ⑥임팩트12 ⑦자유3). 동점 시 **②→①→③** 우선.

## 0. 이 문서의 위치 (무엇을 통합했나)

이 스펙은 다음 세 갈래를 **하나의 구현 가능한 설계**로 통합한다.

1. 팀원(오유정) 설계 `2026-06-30-validate-model-output-design.md` — 결정적 Python 코어 + `rules.yaml` + QC/예보검증 2층위 + ERA5/GFS 데모.
2. `project/research/` 검증·분석 방법 카탈로그(15파일·방법카드 ~500개) + 색인 `00_overview_taxonomy.md`(도메인→recipe 라우팅 C절, 횡단 중복방지 D절, 함정 §G).
3. `project/research/REVIEW.md`(Codex 검토) — "추가 조사 말고 코드 친화적으로 압축: 정규화→canonical metric→router/recipe→MVP범위→scaffold".

추가 합의된 방향(이 세션):
- 스킬은 "바로 분석"이 아니라 **발견(discover)→유도질문(elicit)→다축 분석→옵션 선택→구체화** 루프가 중심이다.
- 분석은 **단일 RMSE 금지 — research 카탈로그 기반 다방면 배터리**로, 마음에 드는 게 몇 개뿐일 수 있으니 **최대한 다양하게** 돌린다.
- 시간·팀원 스펙을 제약으로 깔지 않고 **프로젝트 품질**을 우선한다. 단 500개 전부 구현하는 과욕은 금지(YAGNI 유지).

## 1. 문제 정의

수치모델·AI모델 출력을 **후처리하고 검증·분석**하는 일을 하루에도 여러 번 반복한다. 출력은 NetCDF3 / NetCDF4·HDF5 / CSV·텍스트 등 포맷이 다양하고 규약이 제각각(좌표 1D/2D, 단위 K/°C, 변수명 ECMWF/GRIB/CF식)이다. 지금은 CDO/NCO·Python·ncview·wgrib2를 손으로 오가며 눈으로 확인한다. 느리고, 세션마다 절차가 흔들리며, 통과/실패 근거가 안 남고, 분석이 RMSE 한두 개에 그친다. 게다가 **사용자가 요구·보유 데이터를 명확히 말해주지 않는** 경우가 많아, 무엇을 무엇과 어떻게 비교할지부터 매번 새로 정리해야 한다.

## 2. "맨손 Claude"와의 차별 (존재 이유)

맨손 Claude의 약점: ① 재현 불가(세션마다 검증 코드가 달라짐) ② 전파 불가(노하우가 머릿속에만) ③ 검증이 "눈으로" ④ 분석이 빈약(단일 지표). 대회 최고 배점이 **②재현성·전파성**이므로 산출물은 **재사용 자산**이어야 한다.

**해법 = 결정적 코어 + 에이전트 껍질의 분업**
- 흔들리면 안 되는 검증/분석 규칙 → **결정적 Python 코드 + 선언적 yaml**에 박제(완전 재현).
- "어떤 파일이 결과물·기준인가, 어느 도메인인가, 어떤 분석을 원하나, 결과 해석·수정 제안" 같은 판단·발견·유도 → **에이전트**가 질문 주도 대화로 처리.
- 분석의 *다양성*은 research 카탈로그(검증된 방법 ~500개)를 **분석 메뉴**로 삼아 확보.

## 3. 설계 원칙

1. **입력 포맷 자동 감지 + 미지 포맷 실시간 점검**: 시그니처/확장자로 NetCDF3 / NetCDF4·HDF5 / CSV 판별·라우팅. **예상 밖 포맷이면 에이전트가 throwaway 점검 스크립트를 실시간 작성**해 구조부터 해독.
2. **격자 규약 자동 적응**: 좌표 1D(`lat/lon`)·2D(`y/x`+2D lat/lon)·경도표기(0–360 / −180–180)·위도 정/역순을 자동 인식. 코드 분기 없이 같은 경로.
3. **규칙은 선언적 yaml(직교 2종)**: `rules.yaml`(층위1 QC 임계) ⟂ `recipes.yaml`(층위2 도메인별 분석 배터리·기준자료옵션). 매칭은 변수명만 아니라 `units`/`standard_name`/패턴으로 유연하게. **동료는 코드 무수정, yaml만 추가**.
4. **단위 인식 검증·정규화**: 같은 물리량이 K/°C로 와도 `units`를 읽어 표준단위로 정규화 후 비교. 규칙없는 변수는 크래시 대신 **WARN + 통계적 이상치만**.
5. **발견·유도 우선(분석 즉시 시작 금지)**: 먼저 보유 결과물·검증데이터가 어디에 어떤 형태로 있는지 파악→인벤토리 제시→모르면 질문. 갭분석으로 "이런 기준자료가 있으면 이런 분석 가능"을 묻고, 애매하지만 가치있는 분석은 옵션으로 제시.
6. **다축 분석(단일지표 금지)**: 모든 검증은 최소 (정확도 + 패턴/분포 + 편향) 3축 + 유의성. 가능한 한 축을 넓게(공간·분포·시간·벡터·물리·해역) 돌려 **다양하게** 보여주고 사용자가 선택.
7. **canonical 단일구현**: research D절 횡단방법(RMSE·Taylor·ACC·FSS·CRPS 등)은 `metrics/`에 **한 번만** 구현해 전 도메인·해역이 재사용(중복 0).
8. **advisory 임계**(research §G): 해석 임계(SI<0.15, ACC≥0.6 등)는 영역·해상도·기준자료 의존 → 항상 "참고용" 경고. ERA5/GLORYS/위성L4는 **reference(≠truth)**로만 표기, 오차 독립성 경고.
9. **크래시 금지**: 모든 오류는 명확한 메시지로 FAIL/WARN 리포트.

## 4. 전체 아키텍처 — 폴더 구조 (전파 단위 = 자기완결 스킬 폴더)

```
skills/validate-model-output/
  SKILL.md                  # 자연어 진입점 + 4-페이즈 유도대화 알고리즘 + 사용법
                            #   (Claude Code 스킬 프런트매터 name/description 호환 → .claude/skills/에 그대로 사용 가능)
  scripts/
    cli.py                  # 통합 진입: discover | inspect | validate | verify | postprocess
    io_detect.py            # 포맷 자동감지(CDF3 / NetCDF4·HDF5 / CSV) → reader 라우팅
    dataset.py              # 공통 Dataset 추상화 (소스 포맷 무관 단일 인터페이스, xarray 래핑)
    discover.py             # PHASE0: 경로/폴더 스캔 → 파일별 인벤토리(포맷·변수·좌표·단위·시간·도메인)
    inspect.py              # 단일파일 best-effort 프로브; 전부 실패 시 "미지포맷" → 에이전트 escalate
    router.py               # 메타데이터 → (자료형·변수성질·도메인) 3-tuple 판별 (taxonomy C절 코드화)
    preprocess.py           # 전처리 게이트: 단위정규화·변수alias·좌표(1D/2D)·격자정렬·시간정합·mask·subset·pairing
    qc.py                   # 층위1 QC 체크 (rules.yaml 구동)
    verify.py               # 층위2 예보검증·다축분석 (recipes.yaml → metrics/regions 호출, 1..N 기준자료)
    derive.py               # 파생변수 (u,v → 풍속; 추후 확장)
    regions.py              # bbox + 명명해역 crop, 해역별 배터리 반복
    metrics/                # canonical 단일구현 (research D절)
      basic.py              # bias·MAE·RMSE·nRMSE·SI·Pearson r·R²
      pattern.py            # 패턴상관/ACC·Taylor·target diagram 좌표
      distribution.py       # 히스토그램/PDF·QQ·Perkins SS·KS·분위수
      spatial.py            # 차이/편향/RMSE 지도·(이벤트)FSS·RAPSD/유효해상도
      timeseries.py         # 영역평균 시계열·아노말리·lag상관·추세 (시간축>1)
      events.py             # 임계초과 POD/FAR/CSI·극값(POT/return)  [도메인·트리거 호출]
      circular.py           # 풍향/유향 원형통계(원형 평균오차·원형상관, ±180° 규약)
      vector.py             # u/v 벡터 RMSE·벡터상관 (바람/해류)
    report.py               # report.json + report.md (PASS/FAIL/WARN·메트릭·그림 링크 + 근거)
  config/
    rules.yaml              # 층위1: 변수별 물리범위·결측임계·필수속성 (유연매칭)
    recipes.yaml            # 층위2: 도메인→분석 배터리(축별 카드목록) + reference_options
    aliases.yaml            # 변수명·단위 별칭 (t2m↔2t↔TMP↔air_temperature, K↔°C, u10↔UGRD …)
  data/                     # 소형 fixture: 정상본 + 고의결함본 (실데이터 clip — git 포함)
  tests/                    # pytest: 정상=PASS / 결함=각 체크 FAIL / metric 단위테스트
  references/usage.md       # 따라하기 가이드(재현성)
```

**설계 결정**: 스크립트 분리 대신 `cli.py` 단일 진입 + 서브커맨드(로직은 모듈 분리). SKILL.md에서 `python cli.py verify …`로 일관 호출. 거대 원본(598MB ERA5 / 1.14GB GFS)은 git 제외, 작게 잘라낸 fixture만 포함.

## 5. 핵심 추상화 — 모든 모듈이 한 인터페이스로 대화

소스가 NetCDF3·NetCDF4/HDF5·CSV 어느 것이든 `io_detect.open()`이 **공통 `Dataset`**(변수→값·dims·coords·units·attrs, 좌표 1D/2D, 시간축, mask)으로 정규화. discover·qc·preprocess·verify·metrics·regions는 전부 이 `Dataset`만 알면 됨 → 포맷 분기 0, 단위 테스트 용이.

- **IO 백본 = `xarray`(엔진 `netCDF4` + `h5netcdf`)**: CF 규약·1D/2D 좌표·브로드캐스팅·결측마스킹을 표준 처리. CSV는 `pandas`→경량 Dataset 변환.
- **의존성(전부 pip 설치 확인됨)**: `xarray netCDF4 h5netcdf PyYAML matplotlib pytest` (+ 기존 numpy/pandas/scipy). `cfgrib`/`xesmf`는 제외(YAGNI).

## 6. 4-페이즈 실행 흐름

```
사용자: "이거 검증/분석 해줘"  (요구·데이터 불명확 가능)
 ┌ PHASE 0 — DISCOVER (분석 전 필수, 즉시 분석 시작 금지)
 │   ① 결과물·검증후보 위치/형태 파악: 작업폴더·지정경로 스캔 → 파일별 분류
 │       (포맷·변수·좌표·단위·시간범위·격자·도메인 + "어떻게 저장됐나")
 │       · 알려진 포맷 → io_detect/inspect 자동 파악
 │       · 예상 밖/미지 포맷 → 에이전트가 실시간 점검코드 작성해 구조 해독
 │   ② 인벤토리 표를 사용자에게 제시 (결과물 후보 / 검증 후보 / 미상)
 ├ PHASE 1 — ELICIT (질문으로 구체화, 답이 모일 때까지 유도)
 │   ③ 어느 게 '우리 결과물'·어느 게 '기준/검증'? (파일명 추정 → 확인)
 │   ④ 도메인 확정 → recipes.reference_options 기반 갭분석 질문:
 │       "이 도메인이면 [기준자료 X]가 있으면 [분석 Y]가 가능합니다. 해당 파일 있나요?"
 │   ⑤ 애매하지만 가치있는 분석은 옵션으로 제시("[1]…[2]…[3]… 무엇을 원하세요?")
 ├ PHASE 2 — VALIDATE / VERIFY (결정적 코어, 다축 배터리)
 │   ⑥ 보유 검증파일 1..N개로 검증: preprocess→qc/verify→도메인별 다축 metrics/regions
 └ PHASE 3 — REPORT (json+md: 축별 섹션 전부 + 사용한 가정·advisory·미보유로 못한 분석)
```

**핵심 규약**: 질문은 애매하게 시작해도 된다. **계속 되물어 답을 유도하고 분석을 구체화**한다. 분석을 즉시 시작하지 않는다.

### PHASE 0 — discover (`discover.py`)
- 입력: 경로 1개(파일/폴더) 또는 여러 개. 폴더면 재귀 스캔.
- 각 파일: `io_detect`로 포맷 판정 → 헤더만 읽어 변수·좌표(1D/2D)·단위·시간범위·격자형상 추출 → `router`로 도메인 추정.
- 출력: `inventory.json` + 사람용 표. 각 행 = {파일, 포맷, 도메인추정, 주요변수, 좌표/격자, 단위, 시간범위, 추정역할(결과물/기준후보)}.
- **미지 포맷**: `inspect.probe`가 시그니처+라이브러리 순차시도 후에도 실패하면 `unknown` 플래그 → SKILL.md 규칙대로 에이전트가 실시간 코드로 구조 해독 후 사용자에 보고.

### PHASE 1 — elicit (SKILL.md 대화, 데이터원=recipes.yaml)
- 역할 확인(결과물 vs 기준), 도메인 확정, 갭분석 질문, 옵션 제시. 모두 `recipes.yaml`의 도메인별 `reference_options`/`analyses`를 근거로 생성 → 즉흥 질문이 아니라 카탈로그 기반.

### PHASE 2 — validate / verify
- `validate`(층위1): 기준자료 불필요. `preprocess`(단일파일 정리)→`qc`(rules.yaml). 포맷/열림·격자스키마·값범위(units)·결측·이상치·메타·시간축.
- `verify`(층위2): 기준 1..N개. `preprocess`(쌍 정합: 단위·변수alias·격자정렬·시간정합·mask)→`recipes`가 도메인·feasibility·reference-type에 맞는 **다축 배터리** 호출(§7).

### PHASE 3 — report (`report.py`)
- `report.json`(기계) + `report.md`(사람·심사위원): 체크/메트릭별 PASS/FAIL/WARN + 근거 문장 + 그림 링크 + **사용한 가정/advisory/미수행 분석과 필요한 데이터**.

## 7. 분석 다축 배터리 (research 카탈로그를 분석 메뉴로)

(도메인 × 기준자료종류 × 가능한축)마다 **서로 보완되는 분석을 폭넓게** 돌리고, 축별 섹션으로 전부 제시 → 사용자 선택. 못 돌린 축은 "이런 데이터 있으면 가능"으로 리포트.

| 분석 축 | 분석(예) | metrics 모듈 | 카탈로그 출처 |
|---|---|---|---|
| 정확도·오차 | bias·MAE·RMSE·nRMSE·SI·r·R² | `basic.py` | `01` |
| 패턴·구조 | 패턴상관/ACC·Taylor·target·차이/편향/RMSE 지도·RAPSD/유효해상도 | `pattern.py`,`spatial.py` | `02`,`14` |
| 분포·꼬리 | 히스토그램/PDF·QQ·Perkins SS·KS·분위수·임계초과·극값 | `distribution.py`,`events.py` | `01`,`03` |
| 위상·시간 | 영역평균 시계열·아노말리·lag상관·추세 (시간축>1) | `timeseries.py` | `06` |
| 벡터·방향 | u/v 벡터RMSE·벡터상관·풍향/유향 원형통계 | `vector.py`,`circular.py` | `07`,`10` |
| 물리·파생 | 풍속 √(u²+v²) 파생 후 비교, (요청시) 보존·플럭스 | `derive.py`,(`04` 후속) | `07`,`04` |
| 공간 crop·해역별 | bbox·명명해역(동해/남해/북태평양/열대…) 잘라 해역별 배터리 | `regions.py` | `15`,`09` |

**메커니즘**
1. **feasibility 자동판정**: 시간축 스텝수·앙상블축·기준자료종류·변수성질을 보고 **돌릴 수 있는 축만** 실행. 못 돌린 축은 필요한 데이터와 함께 리포트(↔PHASE1 갭분석).
2. **reference-type 적응**: 격자 재분석=격자대격자 / 점관측 CSV=matchup·관측소 시계열·Taylor / 위성 트랙=along-track colocation(`12`,`15`).
3. **해역 crop = 1급 차원**: 전역 + 사용자지정·명명 해역별로 같은 배터리 반복 → 해역별 표·지도.
4. **출력 = 축별 섹션 전부 + advisory + 선택 유도**.

> 보유 데이터(ERA5/GFS, 단일일 20220906, 전역 721×1440)에서의 feasibility: 시계열/추세축은 자동 스킵(+"다중시각 주면 가능" 안내). 공간·분포·해역·벡터·패턴 축은 풍부하게 구동 → 단일일로도 다양한 분석 산출.

## 8. 두 yaml 직교 + canonical metrics + 라우터 (중복 제거)

- **직교(중복 아님)**: `rules.yaml`=내재 QC 임계(기준 불필요) / `recipes.yaml`=기준대비 어떤 분석을 어떤 순서로. `metrics/`=양쪽·전 도메인이 공유하는 단일구현.
- **`recipes.yaml` 구조(개념)**: 도메인 키 → `{ analyses: [축별 카드 id…], reference_options: [{type, unlocks:[분석…]}], thresholds: advisory }`. **기상=실배선(라이브 구동)**, 수온·염분·파랑·해수면 등=**recipe 정의 수록**(데이터 오면 즉시 구동) → 정직한 일반성·전파성.
- **`router.py`**: 변수명/standard_name/units → 도메인(taxonomy C절). 모호/혼합 → 공통(C-0)만 + 사용자 확인.

## 9. 컴포넌트 책임·인터페이스 (요지)

| 모듈 | 무엇을 | 입력 → 출력 | 의존 |
|---|---|---|---|
| `io_detect` | 포맷 판정·열기 | path → `Dataset` / `unknown` | dataset |
| `dataset` | 공통 자료 추상화 | xarray/pandas → `Dataset` | xarray |
| `inspect` | 단일파일 프로브 | path → 구조 JSON / unknown | io_detect |
| `discover` | 인벤토리 | paths → inventory.json+표 | io_detect, inspect, router |
| `router` | 도메인 판별 | meta → (자료형,성질,도메인) | recipes |
| `preprocess` | 정합 게이트 | Dataset(들) → 정규화·paired | aliases, dataset |
| `qc` | 층위1 체크 | Dataset+rules → 체크결과 | rules.yaml |
| `verify` | 층위2 다축 | 결과물+기준들+recipes → 메트릭/그림 | metrics, regions, preprocess |
| `derive` | 파생변수 | Dataset → 파생장(풍속 등) | dataset, numpy |
| `metrics/*` | canonical 지표 | 배열쌍 → 수치 | numpy/scipy |
| `regions` | 해역 crop·반복 | Dataset+영역 → 해역별 결과 | preprocess |
| `report` | 리포트 | 결과 → json+md+png | matplotlib |

각 모듈은 한 가지 책임, `Dataset`/결과 dict라는 명확한 인터페이스로 통신 → 독립 테스트 가능.

## 10. 리포트 형식

- `report.json`: 모든 체크·메트릭·가정·그림경로의 기계가독 구조.
- `report.md`: 심사위원/사람용. 섹션 = (요약 PASS/FAIL/WARN) → (층위1 QC 표) → (층위2 축별 분석: 정확도/패턴/분포/공간/해역/벡터…) → (그림) → (가정·advisory·미수행 분석과 필요 데이터).
- 각 항목에 **근거**(예: "t2m 12개 값 > 340K, index …", "lat 비단조 @ i=…", "남해 영역 bias=+0.8K, RMSE=1.2K").

## 11. 에러 처리

- 검증기는 **절대 크래시하지 않는다**. 파일없음/미지원포맷/손상/규칙없는변수/격자불일치/시간겹침없음 → 명확한 메시지로 FAIL 또는 WARN 기록.
- 규칙없는 변수: 크래시 대신 WARN + 통계적 이상치만. 미지 포맷: unknown 리포트 + 에이전트 escalate 경로.

## 12. 테스트 (재현성 증거 ②)

- 실 ERA5/GFS를 작게 clip해 `data/`에 fixture(정상본). 고의결함본: 값범위초과(기온 500K)·결측구멍·격자 비단조/중복·잘림/형상어긋남.
- `tests/` pytest:
  - 정상본 = 전 체크 PASS, 결함본 = 해당 체크 FAIL **자동 보증**.
  - `metrics/*` 단위테스트: 알려진 입력 → 알려진 bias/RMSE/상관.
  - preprocess 테스트: K↔°C 정규화, 변수 alias, 1D/2D 좌표, bbox subset, 시간정합.
- 원본 1.14GB는 fixture 생성 1회에만 사용, 테스트는 소형만.

## 13. 데이터·환경 전제

- 보유: `project/sample_data/nums_ex/era5_rean_glo_day_20220906.nc`(NetCDF3 64-bit offset, 598MB, K·CF명·1D좌표), `gfs_fcst_glo_day_masked_20220906.nc`(NetCDF4/HDF5, 1.14GB, GRIB→NetCDF변환·masked, °C·2D좌표 추정). 둘 다 전역 721×1440, 단일일.
- 환경: Python 3.12(miniconda3). numpy·pandas·matplotlib·scipy 설치됨; `xarray netCDF4 h5netcdf PyYAML pytest`는 pip 설치(연결·캐시 확인됨).

## 14. 데모 시나리오 (시간 유연 — 넘어도 무방)

1. `discover <sample_data 폴더>` → 인벤토리 표(결과물/기준 후보 제시) → (질문) 어느 게 결과물·기준?
2. `validate <clean ERA5>` → 전부 PASS / `validate <broken>` → 값범위·결측·격자 FAIL(각 근거).
3. `verify <GFS> --ref <ERA5>` → 단위·격자 정렬 → **다축 배터리**: bias/RMSE/MAE·Taylor·차이지도·분포QQ·풍향 원형통계·**해역별(예: 동해/남해/북태평양) 표**.
4. `postprocess`(subset+풍속) → 결과에 QC 재실행 → PASS.
5. 리포트에 "다중시각·부이 CSV가 있으면 시계열·matchup·TC 가능" 안내(갭분석).

## 15. YAGNI 경계 (reference-only — 문서/recipe로만 연결)

- 라이브 구현 안 함: 일반 regrid(xesmf)·GRIB 네이티브 reader(cfgrib)·위성 TC·AI평가·물리보존/플럭스 진단·극값 정밀추정. `recipes.yaml`·`references/`에 정의·링크만(데이터/시간 오면 가동). research 카탈로그가 근거 토대.
- 웹 UI/대시보드 없음 — CLI + 마크다운 리포트로 충분.

## 16. 성공 기준

- discover가 보유 2파일(서로 다른 포맷·규약)을 자동 인벤토리하고, 미지 포맷에 실시간 점검으로 대응.
- 같은 명령으로 ERA5/GFS QC 통과·결함본 적발, GFS를 ERA5로 **다축** 예보검증(정확도+패턴+분포+해역+벡터).
- 동료가 `rules.yaml`/`recipes.yaml`만 수정해 새 변수·도메인·기준자료에 적용(코드 무수정).
- pytest 그린, 리포트 재현 가능.

## 17. 제출 연결 (②전파성 극대화)

- 스킬 폴더 전체를 `submit/assets/`에 사본(프롬프트·SKILL.md·yaml 포함).
- `submit/PROCESS_LOG.md`에 단계별 로그 append, `submit/evidence/timestamps.txt` 자동 갱신.
- 동료 각자 다른 모드/도메인/자료로 본인 60초 시연(한 명 discover·QC, 한 명 다축 verify, 한 명 해역 crop) → ③전원참여.
