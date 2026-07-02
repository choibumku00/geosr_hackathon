# 분석·검증 방법 카탈로그 (Analysis & Verification Method Catalog)

지오시스템리서치 예보사업부의 **재사용 가능한 Claude Skill** — "우리 수치모델 결과(NetCDF 격자자료 + CSV/텍스트 시계열)를 ERA5/GLORYS 등 권위 재분석자료·관측소·위성자료와 자동 비교·검증" — 의 **방법론 레퍼런스(references) 및 레시피(recipes) 토대**다. 도메인(기상/파랑/수온·염분/해류·조류/해수면/위성)을 자동 판별해 도메인에 맞는 분석을 수행하는 것을 목표로 한다.

- **언어 규칙**: 한국어 서술 + 표준 기술용어 영문 병기(예: 평균제곱근오차 RMSE).
- **수록 형식**: 모든 방법은 통일된 **메서드 카드**(무엇을 측정/검증하나 · 정의·수식 · 적용 도메인/자료형 · 입력·전제 · 해석 기준 · 한계·주의 · 출처)로 작성.
- **출처 원칙**: 검증 가능한 실제 출처만 인용. 표준 교과서·지침은 그렇게 표기. **DOI를 지어내지 않음.** 미확인 항목은 "(확인요)".
- **규모**: 15개 카탈로그 파일, **방법카드 약 500개**.

> ⚠️ **자동 분석 전 반드시 읽을 원칙** → [`00_overview_taxonomy.md` §G 검증 해석의 함정](./00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)
> 핵심: 기준자료(ERA5/GLORYS/위성 L4)는 **참값이 아니라 reference** · 오차 독립성 점검 · 동화·보간 산물을 독립관측 취급 금지 · 해석 임계값은 **advisory** · "확인요" 출처 확정인용 금지 · 단일 지표 금지(정확도+편향+패턴+유의성).

---

## 1. 카탈로그 목적

1. **빠짐없는 망라**: 해양·기상 수치모델 검증에 쓰이는 분석·검증 방법을 가능한 한 모두 수집한다.
2. **자동 라우팅 가능한 구조**: 각 카드에 "적용 도메인/자료형"을 명시해, Skill이 입력 자료의 도메인·자료형을 보고 **어떤 카드를 호출할지 자동 결정**할 수 있게 한다.
3. **재현 가능한 검증**: 정의·전제·해석 임계·한계를 함께 적어, 같은 입력이면 같은 결론에 이르도록 한다.
4. **Skill recipes의 원천**: 도메인별 "기본 분석 묶음(default bundle)"을 정의해 Skill recipes로 직접 옮긴다(→ `00_overview_taxonomy.md` C절).

---

## 2. 파일 목록 (각 1줄 설명 · 상대경로 링크)

> 먼저 **[00. 색인·분류체계](./00_overview_taxonomy.md)** 를 읽으면 전체 구조와 도메인 라우팅 표를 한눈에 본다.

**색인**
- [`00_overview_taxonomy.md`](./00_overview_taxonomy.md) — 전체 분류체계(11범주 트리)·4축 라우팅·도메인→레시피 매핑·횡단 방법 정규화표.

**분석 유형(횡단) — 모든 도메인 공통으로 끌어 쓰는 방법**
- [`01_error_statistics.md`](./01_error_statistics.md) — 오차·정확도 통계(RMSE·MAE·bias, 효율 NSE/KGE, 상관·회귀, Taylor/target, 유의성 bootstrap).
- [`02_spatial_pattern_verification.md`](./02_spatial_pattern_verification.md) — 공간장 패턴 검증(이웃/FSS, 스케일분리/스펙트럼·웨이블릿, 객체 MODE/SAL/CRA, 장변형, 거리측도, SPCT).
- [`03_categorical_event_extremes.md`](./03_categorical_event_extremes.md) — 범주형 분할표·확률(Brier/ROC)·앙상블(rank hist)·드문사건(EDI/SEDI)·극값(GEV/POT/return level/MHW).
- [`04_conservation_energy_flux.md`](./04_conservation_energy_flux.md) — 보존·에너지·플럭스 진단(수지 닫힘, KE/EKE/APE/LEC, 와도/PV, 수송/MOC/AMOC, WMT, 스펙트럼 에너지).
- [`05_spectral_eof_modal.md`](./05_spectral_eof_modal.md) — 스펙트럼(PSD·multitaper·Lomb-Scargle·파수·k-ω·회전)·조화/조석·EOF/SVD/CCA·POD/SPOD/DMD.
- [`06_timeseries_signal.md`](./06_timeseries_signal.md) — 시계열·신호(교차상관/lag·위상진폭·분해 STL·추세 MK/Sen·변화점·필터·웨이블릿·DTW).

**도메인 특화**
- [`07_domain_meteorology.md`](./07_domain_meteorology.md) — 기상·대기(바람 벡터·풍향 원형통계·기온·MSLP/ACC·강수 연속/범주/공간/극값·습도·PBL·다운스케일·앙상블·ERA5 기준 주의점).
- [`08_domain_waves.md`](./08_domain_waves.md) — 파랑(Hs·주기·파향 원형통계·SI·스펙트럼 1D/2D·windsea/swell partition·극치·triple collocation·WMO-JCOMM 운영틀).
- [`09_domain_ocean_temp_salinity.md`](./09_domain_ocean_temp_salinity.md) — 수온·염분(SST/SSS·Argo 프로파일·T-S 수괴·MLD·OHC·전선·단면·등밀도면·TEOS-10·GODAE Class-4·GLORYS 주의점).
- [`10_domain_currents_circulation.md`](./10_domain_currents_circulation.md) — 해류·조류·순환(복소/벡터상관·주축타원·조류타원·회전스펙트럼·수송·MKE/EKE·표면류 분해·Okubo-Weiss·eddy census·FTLE/LCS).
- [`11_domain_sea_level_tides.md`](./11_domain_sea_level_tides.md) — 해수면·조위(조화상수·진폭/지각오차·복소차·해일/skew surge·역기압/DAC·SSH/ADT·재현빈도·해수면수지·QC).

**자료원·비교틀·평가틀·전처리**
- [`12_satellite_remote_sensing.md`](./12_satellite_remote_sensing.md) — 위성·원격탐사(매치업·대표성오차·TC/ETC/QC·고도계 track-vs-grid/파수스펙·SST L2/L3/L4·산란계 풍·해색 Chl-a·crossover·불확실성 검증).
- [`13_model_intercomparison_downscaling.md`](./13_model_intercomparison_downscaling.md) — 모델 상호비교·앙상블·다운스케일링(CMIP/CORDEX·regridding·MMEM·성능독립성 가중·Diebold-Mariano·spread-skill·QM/QDM·VALUE).
- [`14_ai_ml_evaluation.md`](./14_ai_ml_evaluation.md) — AI/ML 평가(double-penalty/RAPSD·영상품질 SSIM/LPIPS/FID·물리정합 PINN/보존량·UQ ECE/conformal·이상탐지·OOD/롤아웃·XAI·WeatherBench2).
- [`15_preprocessing_regridding_colocation.md`](./15_preprocessing_regridding_colocation.md) — 전처리·격자정합·시공간 매칭(보간/재격자·kriging/OI/DIVA·좌표·벡터회전·마스크·시간정합·matchup·대표성오차·QC·climatology·bias correction·detiding).

---

## 3. 사용법 — 이 카탈로그를 Skill recipes로 옮기는 법

이 카탈로그는 **참조(references)와 레시피(recipes)의 원천**이다. Skill은 다음 흐름으로 동작하도록 설계한다: **(1) 입력 메타데이터(변수명·CF standard_name·차원·앙상블축)로 `자료형·변수성질·도메인` 3-tuple을 판별하고, (2) `00_overview_taxonomy.md` C절의 "도메인 → 기본 묶음(default bundle)" 표에서 해당 메서드 카드 목록을 가져온 뒤, (3) 모든 recipe의 선행 단계로 `15`(전처리·정합)를 강제 적용하고, (4) 각 메서드 카드를 검증 함수 1개로 구현해(입력·전제·출력·해석임계 포함) 순서대로 호출하며, (5) 단일 지표 금지 원칙에 따라 최소 "정확도+패턴/분포+편향" 3축과 유의성(bootstrap/DM/SPCT)을 함께 보고한다.** 횡단 방법(Taylor·ACC·FSS·CRPS·TC 등)은 파일마다 중복 정의되어 있으므로, `00`의 D절 정규화표에 따라 **단일 구현 + 도메인별 파라미터/임계** 패턴으로 묶어 중복을 제거한다.

**한 줄 요약 흐름**: `입력 → [라우터: 자료형·변수성질·도메인 판별] → [전처리 게이트 15] → [도메인 default bundle 호출(01·02 공통 + 도메인 07~11 + 트리거 03/04/05/06/12/13/14)] → [3축+유의성 보고] → 해석임계는 관행값+영역의존 경고`

---

## 4. 추가 조사 권장 (Gaps)

15개 파일을 교차 점검한 결과, 다음 주제는 **빠졌거나(누락) · 얕거나(보강) · 교차정합이 필요(정합)** 하다. Skill 신뢰성을 위해 우선순위대로 정리한다.

### 4.1 누락(추가 카탈로그/카드 필요)

1. **관측 불확실성·대표성을 검증식에 반영하는 절차** — 부이·Argo·검조소의 측정오차와 점-격자 대표성오차를 RMSE에서 분리(예: error-in-variables, representativeness-aware skill). 현재 `12`/`15`에 개념은 있으나 *검증 지표에 직접 반영하는 레시피*가 없음.
2. **해빙(sea ice) 도메인** — 해빙 농도·두께·가장자리(ice edge) 검증(IIEE: Integrated Ice-Edge Error, SIE/SIA, edge 거리측도). 극지·고위도 모델 검증에 표준이나 도메인 파일이 없음.
3. **생지화학·해색 정량검증** — `12`의 Chl-a matchup을 넘어, 영양염·DO·pH·1차생산·log-normal 변수 전용 통계, 위상(blooming timing) 검증. 연안·환경 응용에서 수요.
4. **하천유입·연안 경계·하구(estuary) 변수** — 염분 전선·plume·하천유량 경계조건 검증. 연안 모델 특화.
5. **대기-해양 결합 플럭스 검증** — 표면 운동량/열/담수 플럭스 자체의 관측(에디공분산·OAFlux·계류)과의 검증. `04`는 모델 내부 닫힘 중심.
6. **공식 신뢰구간을 갖춘 극값 검증** — `03`/`08`/`11`에 GEV/POT는 있으나, *모델 vs 관측 극값분포 차이의 유의성 검정*(예: 매개변수 신뢰구간 중첩, L-moment 기반 비교)이 약함.
7. **계산 비용·확장성 메모** — FTLE/LCS, image warping, SPCT, MBCn 등은 대용량 격자에서 비용이 큼. 각 카드에 *근사·청크·다운샘플 전략*이 없음.

### 4.2 보강(있으나 얕음)

8. **원형(방향) 통계 일관성** — 풍향(`07`)·파향(`08`)·유향(`10`)이 각자 원형통계를 정의. 공통 "원형통계 코어"(원형 평균/분산/상관/RMSE, ±180° 규약)로 통일 필요.
9. **벡터 변수 검증의 통일** — 바람(`07`)·해류(`10`)의 벡터 RMSE·벡터상관 정의가 분산. 단일 벡터검증 모듈로 정규화 권장.
10. **불규칙·결측 자료의 스펙트럼·EOF** — Lomb-Scargle(`05`/`06`), DINEOF(`15`)는 있으나, 결측이 EOF/coherence/Taylor에 미치는 편향과 보정이 카드 간 흩어져 있음.
11. **비정상성(non-stationarity)·기후추세 하의 검증** — `06` 추세·변화점, `03` 비정상 극값은 있으나, *추세가 있는 자료에서 climatology·return period·MHW baseline 선택*이 결과를 좌우하는 점을 횡단 가이드로 보강.
12. **TEOS-10/단위·기준면 정합의 실패 사례집** — `09`/`11`/`15`에 분산. datum·기준온도·염분 표준(PSU vs g/kg)·SSH 기준면(geoid/MDT) 불일치가 만드는 *가짜 bias 카탈로그* 필요.

### 4.3 정합(교차 일관성 점검)

13. **횡단 방법 단일 구현화** — `00` D절 정규화표 대상(RMSE·Taylor·ACC·FSS·SAL/MODE·GEV/POT·TC·CRPS·조화분석·rotary/EOF·QM·matchup)을 *코드 레벨에서 단일 함수*로 강제. 현재는 정의가 파일마다 미세하게 다를 수 있음(예: SI의 bias 제거 여부, nRMSE 분모, ACC 중심/비중심).
14. **해석 임계값 출처 추적** — SI<0.15, ACC≥0.6, NSE 등급, FSS useful-scale 등 관행 임계가 변수·해역·해상도 의존. *임계값 → 출처/적용범위* 매핑표를 별도 부록으로.
15. **앙상블·확률 트리거의 일관 적용** — `03`/`13`/`14`에 rank hist·CRPS·Brier·reliability가 중복. 앙상블 축 감지 시 *어느 파일의 정의를 canonical로 쓸지* 명시.
16. **AI/ML 평가와 물리검증의 연결** — `14`의 물리정합(보존량·PDE residual)과 `04`의 보존 진단이 분리. AI emulator 검증 시 `04` 카드를 직접 재사용하는 교차링크 필요.

---

## 5. 작성·유지 규칙 (기여자용)

- 새 방법은 **메서드 카드 7항목**(측정대상·정의수식·적용도메인/자료형·입력전제·해석기준·한계·출처)을 모두 채운다.
- 파일 머리의 **"한 줄 목차"** 에 항목을 추가하고, 필요하면 `00_overview_taxonomy.md`의 트리·라우팅 표·정규화표를 갱신한다.
- 출처는 실제 확인된 것만. DOI/arXiv 번호는 확인된 것만 표기하고 미확인은 "(확인요)".
- 횡단 방법을 추가할 때는 D절 정규화표를 보고 **중복 정의 대신 교차링크**를 우선한다.
