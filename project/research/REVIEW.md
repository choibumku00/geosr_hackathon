# Research Catalog Review — 모델 후처리 및 검증 자동화

검토일: 2026-06-30  
검토자: Codex  
대상: `project/research/` 전체 문헌·방법론 카탈로그

## 1. 우리가 하려는 것에 대한 이해

목표는 단순히 RMSE 표 몇 개를 자동으로 뽑는 도구가 아니다. 최종 산출물은 **수치모델 결과를 ERA5/GLORYS 같은 재분석자료, 관측소 CSV, 위성/원격탐사 자료와 비교·검증하는 범용 분석 Skill**이다.

이 Skill은 다음 흐름을 가져야 한다.

1. 입력 파일(NetCDF 격자, CSV/텍스트 시계열)의 메타데이터를 읽는다.
2. 변수명, CF `standard_name`, 차원, 좌표, 단위, 앙상블축 유무로 도메인과 자료형을 판별한다.
3. 모든 비교 전에 전처리·정합 게이트를 통과시킨다.
4. 도메인별 기본 recipe를 호출한다.
5. 결과를 단일 지표가 아니라 `정확도 + 편향 + 패턴/분포 + 유의성 + 필요 시 물리/스펙트럼/극값` 묶음으로 보고한다.

따라서 이번 research의 품질 기준은 "논문 목록이 많은가"가 아니라, **Skill의 router, recipes, canonical metric 함수, 해석 문장으로 옮길 수 있는 구조인가**다.

## 2. 총평

**판정: 매우 잘 됨. 구현 전 정규화만 필요.**

카탈로그는 해양·기상 수치모델 검증에 필요한 방법을 넓게 포괄하고 있고, 단순 통계뿐 아니라 전처리, 공간검증, 극값, 물리 보존성, 스펙트럼, 시계열, 위성, AI/ML 평가까지 잘 잡았다. 특히 `00_overview_taxonomy.md`가 단순 색인을 넘어 **도메인 자동판별 → 추천 recipe 매핑**까지 제공하고 있어, 바로 Skill 설계의 중심 문서로 쓸 수 있다.

다만 연구 결과를 그대로 코드로 옮기면 중복·형식 차이·임계값 출처 문제 때문에 구현이 흔들릴 수 있다. 다음 단계에서는 research 내용을 다시 조사할 필요보다, **canonical schema와 priority recipe를 뽑는 정규화 작업**이 중요하다.

## 3. 잘된 점

### 3.1 범위가 충분히 넓다

다음 요구가 모두 반영되어 있다.

- 모델 vs 모델 비교: `13_model_intercomparison_downscaling.md`
- 모델 vs 관측 비교: `01`, `06`, `15`, 도메인 파일 전반
- 모델 vs ERA5/GLORYS 비교: `07`, `09`, `11`, `13`, `15`
- 모델 vs 위성자료 비교: `12_satellite_remote_sensing.md`
- 특정 영역 crop/영역 평균/단면/매치업: `15`, `09`, `10`, `11`
- RMSE/bias/correlation 등 기본 통계: `01`
- 흐름·에너지·보존성: `04`, `10`
- 공간 패턴·이중벌점·객체기반 검증: `02`, `03`, `14`
- 스펙트럼·EOF·조화분석: `05`, `06`, `10`, `11`
- AI/ML 평가와 물리검증: `14`

### 3.2 Skill 구조로 옮기기 좋은 중심 문서가 있다

`00_overview_taxonomy.md`의 C절과 D절이 특히 중요하다.

- C-0: 모든 도메인 공통 전처리·기본통계·유의성 recipe
- C-1: 기상, 파랑, 수온·염분, 해류·조류, 해수면·조위, 위성 도메인별 recipe
- C-2: 앙상블, 모델간 비교, AI 산출물, 편향보정, 물리 일관성 등 비도메인 트리거
- D절: RMSE, Taylor, ACC, FSS, TC, CRPS, 조화분석 등 중복 구현을 막는 canonical table

이 문서는 구현 시 `references/recipes.md`의 초안으로 바로 사용할 수 있다.

### 3.3 전처리의 중요성을 제대로 잡았다

`15_preprocessing_regridding_colocation.md`는 모든 검증의 선행 게이트로 충분하다. 특히 다음 항목이 잘 들어가 있다.

- CF/단위/좌표/경도 표기 정합
- 격자 보간과 보존 재매핑
- land-sea mask 처리
- 시간 동기화와 누적/평균 변수 정합
- matchup window와 paired sample 구성
- 대표성오차, triple collocation
- climatology/anomaly, detiding, 필터, bias correction

이 파일은 실제 Skill 구현에서 가장 먼저 호출되는 `preprocess_and_pair()` 설계의 기반으로 쓰면 된다.

### 3.4 물리 검증이 단순 통계와 잘 분리되어 있다

`04_conservation_energy_flux.md`는 "수치모델다운 검증"을 잘 담고 있다. 질량/체적, 운동량, 열/염 수지, KE/EKE, PV, transport, MOC, WMT, 스펙트럼 에너지 플럭스까지 들어 있다.

중요한 점은 이 파일이 **offline 후처리로 가능한 것과 online diagnostic이 있어야 정확한 것**을 구분하고 있다는 것이다. Skill이 자동으로 "가능한 분석"과 "필요 입력 부족"을 설명하는 데 유용하다.

### 3.5 AI/ML 파일은 해커톤 주제 확장에 좋다

`14_ai_ml_evaluation.md`는 전통 검증지표를 반복하는 데 그치지 않고, AI 특유의 실패양상을 잡는다.

- 블러링과 double penalty
- RAPSD/effective resolution
- SSIM/LPIPS/FID 등 영상 품질 지표
- UQ calibration, conformal prediction
- OOD, long rollout drift
- 물리 잔차/PDE residual, 보존량 점검
- 데이터 누수와 baseline 함정

단, 구현 1차 범위에서는 전부 넣기보다 `RMSE/MAE/bias + ACC + FSS/RAPSD + UQ 기본 + 물리 체크 연결` 정도만 넣는 것이 현실적이다.

## 4. 주의할 점 / 보완 필요

### 4.1 형식 정규화 필요

대부분 파일은 메서드 카드를 `###` heading과 굵은 라벨(`**무엇을 측정/검증하나**`)로 작성했다. 하지만 일부 파일은 형식이 다르다.

- `03_categorical_event_extremes.md`: 메서드 heading이 `##`
- `09_domain_ocean_temp_salinity.md`: 메서드 heading이 `##`
- `06_timeseries_signal.md`: 카드 라벨이 굵은 형식이 아님
- `12_satellite_remote_sensing.md`: 카드 라벨이 굵은 형식이 아님

사람이 읽기에는 문제 없지만, 나중에 자동 파서로 "카드 목록 추출 → 함수 stub 생성"을 하려면 정규화가 필요하다.

권장: 모든 파일을 아래 형식으로 통일한다.

```markdown
### 방법명 (Korean / English)
- **무엇을 측정/검증하나**:
- **정의·수식**:
- **적용 도메인/자료형**:
- **입력·전제**:
- **해석 기준**:
- **한계·주의**:
- **출처**:
```

### 4.2 위성 파일은 내용은 좋지만 구현 우선순위가 높다

`12_satellite_remote_sensing.md`는 필수 라벨 형식만 다를 뿐 내용은 상당히 좋다. 특히 matchup, 대표성오차, TC/ETC/QC, GHRSST, altimetry, ocean color가 들어 있다.

다만 우리 Skill이 "관측/재분석/위성 모두 비교 가능"을 표방하려면 위성 쪽은 핵심 차별점이다. 따라서 다음 단계에서 다음 4개는 canonical 함수 후보로 승격하는 것이 좋다.

- `satellite_matchup()`
- `triple_collocation()`
- `altimetry_track_vs_grid()`
- `sst_skin_bulk_note_or_check()`

### 4.3 임계값은 그대로 자동판정에 쓰면 위험하다

여러 파일에 `SI < 0.15`, `ACC >= 0.6`, `NSE 등급`, `FSS useful scale` 같은 관행 기준이 들어 있다. 이것은 해석문 생성에는 유용하지만, 자동으로 "좋음/나쁨"을 단정하면 위험하다.

권장:

- 1차 구현에서는 모든 threshold를 `advisory`로 표시한다.
- 변수, 해역, 해상도, 기준자료에 따라 달라진다는 경고를 항상 붙인다.
- 추후 `thresholds.yml` 같은 별도 파일에 `metric, domain, variable, source, applicability`를 분리한다.

### 4.4 중복 정의가 많아 canonical metric 설계가 필수다

RMSE, bias, correlation, Taylor diagram, ACC, FSS, TC, CRPS, harmonic analysis가 여러 파일에 반복 등장한다. 이것은 research 단계에서는 자연스럽지만, 구현 단계에서는 위험하다.

권장 canonical module:

- `metrics/basic.py`: bias, MAE, RMSE, nRMSE, SI, correlation
- `metrics/pattern.py`: ACC, Taylor, target diagram
- `metrics/events.py`: contingency, POD/FAR/CSI/ETS/HSS, Brier, ROC
- `metrics/spatial.py`: FSS, SAL/MODE wrapper, spectra
- `metrics/timeseries.py`: lag correlation, phase/amplitude, trend/change point
- `metrics/physical.py`: budget closure, KE/EKE, transport
- `metrics/satellite.py`: matchup, TC/ETC, uncertainty validation

### 4.5 모든 방법을 구현 대상으로 보면 범위가 폭발한다

카탈로그는 약 500개 방법을 담고 있다. 이것은 reference로는 강점이지만, 해커톤 구현 범위로는 너무 넓다.

1차 데모는 아래 정도가 적절하다.

1. NetCDF/CSV 로더와 도메인 탐지
2. 전처리·정합 기본: 시간 공통구간, 단위, 결측, 영역 crop, 격자→격자 또는 격자→점 매칭
3. 공통 통계: bias, MAE, RMSE, correlation, nRMSE/SI
4. 공간장: 모델/기준/차이 지도, Taylor/target 또는 scatter
5. 도메인 2개: 수온·염분 + 파랑 또는 수온·염분 + 해수면
6. Markdown report 자동생성

물리 보존성, 위성 TC, AI 평가, 극값은 "고급 recipe"로 문서상 연결하되 데모에서는 선택 실행으로 두는 것이 좋다.

## 5. 파일별 간단 평가

| 파일 | 평가 | 메모 |
|---|---|---|
| `00_overview_taxonomy.md` | 매우 좋음 | Skill router/recipe의 중심 문서로 사용 가능 |
| `01_error_statistics.md` | 매우 좋음 | 기본 통계와 한계 설명 충실. canonical metric의 출발점 |
| `02_spatial_pattern_verification.md` | 좋음 | FSS, SAL, MODE, SPCT 등 공간검증 체계 좋음 |
| `03_categorical_event_extremes.md` | 좋음 | 내용 충실. heading 형식만 정규화 필요 |
| `04_conservation_energy_flux.md` | 매우 좋음 | 수치모델다운 물리 검증 축. 단, online 입력 필요 여부를 구현에서 표시해야 함 |
| `05_spectral_eof_modal.md` | 좋음 | 스펙트럼/EOF/조화분석 포괄. 계산비용·입력조건 체크 필요 |
| `06_timeseries_signal.md` | 좋음 | 시계열 비교에 실용적. 라벨 형식 정규화 필요 |
| `07_domain_meteorology.md` | 좋음 | 기상 recipe 넓음. 강수 공간검증까지 포함 |
| `08_domain_waves.md` | 매우 좋음 | 파랑 도메인 데모 후보로 좋음. SI/HH/altimeter/TC 구성 우수 |
| `09_domain_ocean_temp_salinity.md` | 매우 좋음 | 수온·염분 도메인 데모 후보로 가장 적합. heading 형식만 정규화 필요 |
| `10_domain_currents_circulation.md` | 좋음 | 벡터/복소상관, 조류타원, Lagrangian, EKE 등 좋음 |
| `11_domain_sea_level_tides.md` | 좋음 | 조석/해수면 특화가 충실. datum 정합 주의 필요 |
| `12_satellite_remote_sensing.md` | 좋음 | 내용은 좋고 중요도 높음. 라벨 형식 정규화 필요 |
| `13_model_intercomparison_downscaling.md` | 좋음 | 모델간 비교, 앙상블, bias correction까지 잘 포괄 |
| `14_ai_ml_evaluation.md` | 좋음 | AI 평가 확장성 좋음. 1차 구현 범위는 좁혀야 함 |
| `15_preprocessing_regridding_colocation.md` | 매우 좋음 | 모든 recipe의 선행 게이트로 적합 |

## 6. 다음 단계 권장

### 6.1 Research 정규화 산출물 만들기

다음 파일을 새로 만드는 것을 권장한다.

- `project/spec/metric_schema.md`: 메서드 카드 표준 schema
- `project/spec/domain_router.md`: 변수명/CF standard_name → 도메인 매핑
- `project/spec/default_recipes.md`: C-0 공통 + 도메인별 1차 recipe
- `project/spec/implementation_scope.md`: 해커톤 데모에서 구현할 것과 reference로만 둘 것

### 6.2 구현 1차 범위

가장 현실적인 MVP:

- 입력: 로컬 NetCDF 2개 또는 NetCDF+CSV
- 기능: 변수 자동탐지, 영역 crop, 시간 공통구간, 단위 확인, 기본 통계, 공간/시계열 그림, markdown report
- 도메인: 수온·염분 + 파랑
- 산출물: `outputs/<run_id>/stats.csv`, `figures/*.png`, `report.md`

### 6.3 당장 고칠 필요는 없지만 기록할 리스크

- 일부 출처는 `확인요`로 남아 있어 자동 인용문 생성 시 "확정 출처"처럼 쓰면 안 된다.
- `WMO/JCOMM`, 기관 페이지, 일부 기술문서는 URL 변동 가능성이 있다.
- ERA5/GLORYS를 "truth"로 쓰는 문장은 금지하고, 항상 "reference/reanalysis"로 표현해야 한다.
- GLORYS/ERA5와 우리 모델이 동일 강제력이나 동화자료를 공유하면 오차 독립성이 깨진다.
- 위성 L4, GHRSST, 재분석자료는 이미 보간/동화된 산물이므로 독립 관측처럼 취급하면 안 된다.

## 7. 결론

현재 research는 해커톤 주제의 기반으로 충분하다. 특히 `00`, `01`, `08`, `09`, `12`, `15`를 중심으로 MVP를 만들면 **범용 분석 Skill**이라는 방향성과 **수치모델/AI 역할 분담**이 모두 산다.

다음 작업은 추가 논문 수집이 아니라, research를 코드 친화적으로 압축하는 것이다.

우선순위:

1. 카드 형식 정규화
2. canonical metric 목록 확정
3. 도메인 router와 default recipe 문서화
4. MVP 구현 범위 확정
5. Skill scaffold 작성
