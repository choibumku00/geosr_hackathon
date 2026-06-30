# 00. 분석·검증 방법 카탈로그 — 색인·분류체계·도메인 라우팅 (Overview & Taxonomy)

이 문서는 `project/research/` 아래 15개 카탈로그 파일(01~15)의 **분석·검증 방법 전체를 가로지르는 색인·분류체계**이며, 동시에 재사용 Skill의 **recipes(레시피) 설계 토대**다. 우리 수치모델 결과(NetCDF 격자자료, CSV/텍스트 시계열)를 ERA5/GLORYS 등 권위 재분석자료, 관측소·위성 자료와 자동 비교·검증할 때, **도메인(기상/파랑/수온·염분/해류·조류/해수면/위성)을 자동 판별 → 도메인에 맞는 메서드 카드 묶음을 자동 호출**하는 흐름을 표준화한다.

> **이 문서의 두 가지 역할**
> 1. **분류체계(Taxonomy)**: "어떤 종류의 검증 방법이 있는가"를 트리/표로 정리해, 개별 카드가 어느 범주에 속하는지 라우팅한다.
> 2. **도메인 라우팅(Domain → Recipe)**: "도메인이 X로 판별되면 기본으로 어떤 카드를 돌리는가"를 표로 제시한다. 이것이 곧 Skill의 recipe 초안이다.

---

## A. 카탈로그 구성 한눈에 (파일 색인)

| # | 파일 | 분류 축 | 다루는 핵심 | 방법카드(≈) |
|---|---|---|---|---|
| 01 | `01_error_statistics.md` | 분석유형 | 오차·정확도 통계(RMSE·MAE·bias·효율·상관·Taylor/target·유의성) | 28 |
| 02 | `02_spatial_pattern_verification.md` | 분석유형 | 공간장 패턴 검증(이웃/스케일분리/객체/장변형/거리측도/SPCT) | 17 |
| 03 | `03_categorical_event_extremes.md` | 분석유형 | 범주형·확률·앙상블·드문사건·극값(GEV/POT/MHW) | 38 |
| 04 | `04_conservation_energy_flux.md` | 분석유형 | 보존·에너지·플럭스 진단(수지닫힘·KE/EKE·수송·MOC·WMT) | 38 |
| 05 | `05_spectral_eof_modal.md` | 분석유형 | 스펙트럼·EOF·모달(PSD·파수·회전·조화·EOF/SVD/SPOD/DMD) | 24 |
| 06 | `06_timeseries_signal.md` | 분석유형 | 시계열·신호(교차상관·분해·추세·변화점·필터·웨이블릿·DTW) | 26 |
| 07 | `07_domain_meteorology.md` | 도메인 | 기상·대기(바람·기온·MSLP·강수·습도·PBL·다운스케일·앙상블) | 39 |
| 08 | `08_domain_waves.md` | 도메인 | 파랑(Hs·주기·파향·스펙트럼·partition·극치·TC·고도계) | 31 |
| 09 | `09_domain_ocean_temp_salinity.md` | 도메인 | 수온·염분(SST/SSS·프로파일·수괴·MLD·OHC·전선·단면) | 30 |
| 10 | `10_domain_currents_circulation.md` | 도메인 | 해류·조류·순환(벡터/복소상관·조류타원·회전스펙·수송·와류·LCS) | 22 |
| 11 | `11_domain_sea_level_tides.md` | 도메인 | 해수면·조위(조화상수·진폭/지각오차·해일·재현빈도·해수면수지) | 30 |
| 12 | `12_satellite_remote_sensing.md` | 자료원 | 위성·원격탐사(매치업·대표성오차·TC/ETC·고도계/SST/풍/해색) | 21 |
| 13 | `13_model_intercomparison_downscaling.md` | 비교틀 | 모델상호비교·앙상블·다운스케일(CMIP·MMEM·가중·QM·DM검정) | 31 |
| 14 | `14_ai_ml_evaluation.md` | 평가틀 | AI/ML 평가(영상품질·물리정합·UQ·이상탐지·OOD·XAI) | 65 |
| 15 | `15_preprocessing_regridding_colocation.md` | 전처리 | 전처리·격자정합·시공간 매칭(보간·재격자·마스크·matchup·QC) | 32 |

**전체 방법카드 합계: 약 500개** (파일 머리의 "한 줄 목차" 일부 항목은 다수 메서드를 묶고 있어, 실제 메서드 카드 수는 목차 불릿 수보다 많다.)

---

## B. 분석 유형 분류체계 (Taxonomy Tree)

카탈로그 전체를 11개 상위 범주로 묶는다. 같은 메서드(예: Taylor 다이어그램, FSS, ACC, Triple Collocation)는 여러 범주·여러 파일에 **교차 등장**한다 — 아래 트리는 "1차 소속"을 기준으로 하되, 교차 위치를 괄호로 병기한다.

```
분석·검증 방법 (Analysis & Verification Methods)
│
├─ 1. 정확도·오차 통계 (Accuracy / Error statistics)            [01, +07/09/13/14]
│   ├─ 점추정 오차: RMSE, MSE, MAE, ME/bias
│   ├─ 상대·정규화 오차: MAPE, SMAPE, PBIAS, nRMSE, RSR, MASE, SI, HH
│   ├─ 오차 분해: systematic/unsystematic, CRMSD, ubRMSE, MSE 분해
│   ├─ 상관·회귀: Pearson r, Spearman ρ, R², 회귀 기울기/절편
│   ├─ 효율·일치도: NSE, KGE/KGE', Willmott d/dr, Murphy MSSS
│   └─ 요약·유의성: Taylor diagram & TSS, Target diagram, within-tolerance, bootstrap/유효표본
│
├─ 2. 공간장 패턴 검증 (Spatial / field verification)          [02, +07/13/14]
│   ├─ 격자별 오차·패턴: 오차장 지도, 패턴상관/ACC, Taylor, S1 gradient
│   ├─ 이웃/퍼지(neighborhood): fuzzy framework, FSS
│   ├─ 스케일분리(scale-separation): 파워스펙트럼/DCT, 웨이블릿 Intensity-Scale, variogram
│   ├─ 특징/객체기반(feature/object): MODE, SAL, CRA
│   ├─ 장변형(field-deformation): image warping/optical flow(DAS)
│   ├─ 거리측도: Baddeley Δ, Hausdorff, Pratt FoM, Gβ score
│   ├─ 영상품질: SSIM(+14 PSNR/MS-SSIM/LPIPS/FID)
│   └─ 유의성: SPCT(공간 Diebold-Mariano)
│
├─ 3. 범주형·사건·극값·확률 (Categorical / event / extremes / probabilistic)  [03, +07/08]
│   ├─ 2×2 분할표 지표: PC, FBI, POD, FAR, POFD, SR, CSI, ETS/GSS, HSS, PSS/TSS, OR/ORSS
│   ├─ 드문사건 전용: EDI, SEDI, EDS/SEDS
│   ├─ 확률예보: Brier(+분해), BSS, reliability diagram, ROC/AUC
│   ├─ 다범주·확률분포: RPS/RPSS, CRPS/twCRPS, Gerrity, SEEPS, multi-cat HSS
│   ├─ 앙상블 신뢰성: rank histogram(Talagrand), spread–skill
│   └─ 극값 통계: GEV/block-maxima, POT/GPD, return period/level, ETCCDI, MHW
│
├─ 4. 보존·물리·에너지·플럭스 (Conservation / physics / energy / flux)  [04, +10]
│   ├─ 수지 닫힘(budget closure): 질량·체적, 운동량, 열, 염, online-vs-offline
│   ├─ 에너지: KE, EKE, MKE, APE, Lorenz energy cycle
│   ├─ 와도·역학: 상대/행성/절대 와도, PV, enstrophy, divergence, 지형류/열풍, Bernoulli
│   ├─ 수송: 체적/열/염·담수 수송, MHT 분해, MOC/AMOC, 순압유선함수, Sverdrup, Ekman
│   ├─ 수괴·표층강제: WMT, MLD·부력플럭스
│   ├─ 스펙트럼 에너지: KE 파수스펙트럼, 에너지/엔스트로피 캐스케이드, coarse-graining flux
│   └─ 보존성 점검: isopycnal budget, 수치 diapycnal mixing, 전지구 에너지/물수지
│
├─ 5. 스펙트럼·EOF·모달 (Spectral / EOF / modal)                [05, +04/06]
│   ├─ 스펙트럼: PSD(Welch), multitaper, Lomb-Scargle, 기울기, 파수, k-ω, 회전(rotary)
│   ├─ 조화/조석: harmonic·tidal analysis(T_TIDE/UTide)
│   ├─ 교차·고차: cross-spectrum/coherence, bispectrum
│   ├─ 시간-주파수: CWT, XWT/WTC, EMD/EEMD/HHT
│   └─ 모달분해: EOF/PCA, REOF, CEOF, EEOF/M-SSA, SSA/MC-SSA, SVD/MCA, CCA, POD, SPOD, DMD
│
├─ 6. 시계열·신호 (Time-series / signal)                        [06, +05]
│   ├─ 지연·위상: 교차상관/lag, 위상·진폭오차, ACF/PACF
│   ├─ 분해·계절: STL, classical decomposition, 계절기후값/조화적합
│   ├─ 추세·변화점: Mann-Kendall/Sen, change-point(Pettitt/CUSUM/PELT/BCP)
│   ├─ 필터·변동성: 디지털 필터(Butterworth/Lanczos/Godin), 분산비/F/Levene
│   ├─ 응답·전달: admittance/gain/transfer function, spectral diagram
│   └─ 스케일링·형상: DFA/장기기억, DTW, point/mooring 워크플로
│
├─ 7. 도메인 특화 (Domain-specific)                             [07~11]
│   ├─ 기상·대기 [07]        ├─ 파랑 [08]        ├─ 수온·염분 [09]
│   ├─ 해류·조류·순환 [10]   └─ 해수면·조위 [11]
│   (각 도메인은 위 1~6 범주의 부분집합 + 도메인 고유 지표로 구성 — C절 참조)
│
├─ 8. 위성·원격탐사 (Satellite / remote sensing)                [12, +08/09/11]
│   ├─ 매칭·오차구조: matchup/colocation, 매치업 통계, 대표성오차, TC/ETC/QC
│   ├─ 공통통계(위성판): Taylor, 분포비교, anomaly 상관, 사건/객체 검증
│   ├─ 도메인별 위성: 고도계 SLA/ADT(track vs grid)·파수스펙트럼, SST L2/L3/L4, 산란계 풍, 해색 Chl-a
│   └─ 처리·불확실성: L2→L3 비닝, crossover, uncertainty validation(u-plot)
│
├─ 9. 모델 상호비교·앙상블·다운스케일링 (Intercomparison / ensemble / downscaling)  [13, +03/14]
│   ├─ 비교틀: CMIP/CORDEX 규약, regridding, 해상도 보정, grid-to-grid
│   ├─ 유의성: Diebold-Mariano, bootstrap CI
│   ├─ 앙상블: MMEM, 성능·독립성 가중(ClimWIP), spread-skill, rank hist, CRPS(+분해)/CRPSS, Brier/BSS, reliability, log/ignorance, ROC
│   └─ 다운스케일/보정: PP, MOS, quantile mapping/QDM, MBCn, 분산팽창, VALUE 프레임워크
│
├─ 10. AI/ML 평가 (AI/ML evaluation)                            [14]
│   ├─ 회귀·유의성: RMSE/MAE/bias·정규화, R², MSESS, ACC, KGE, Taylor, DM/bootstrap
│   ├─ 공간·이중벌점: double penalty, FSS, RAPSD/유효해상도
│   ├─ 영상품질: PSNR, SSIM/MS-SSIM, LPIPS, spectral fidelity, FID
│   ├─ 분포·편향보정: Wasserstein/KS, Q-Q/PDF, QM/QDM/DQM, EMOS/DRN, analog
│   ├─ 확률·UQ: CRPS/fair-CRPS, Energy/Variogram score, PIT, ECE/sharpness, PICP/MPIW, conformal
│   ├─ 물리정합: PDE residual(PINN), 보존량 점검, 경계/초기조건 위반
│   ├─ 이상탐지: P/R/F1, ROC-AUC/PR-AUC, point-adjust, affiliation/VUS, MTTD
│   ├─ OOD·안정성: 일반화, 롤아웃 드리프트, 기후통계 보존
│   └─ XAI: permutation importance, SHAP, integrated gradients, faithfulness
│
└─ 11. 전처리·격자정합·시공간 매칭 (Preprocessing / regridding / colocation)  [15, ←모든 분석의 전제]
    ├─ 보간/재격자: bilinear, bicubic/spline, nearest, IDW, 1st/2nd conservative, patch, weights 검증
    ├─ 지구통계 격자화: kriging, OI/객관분석, DIVA
    ├─ 좌표·격자: 투영변환, 경도/날짜변경선/극, 회전/곡선/비정규격자, 벡터 회전, land-sea mask
    ├─ 시간: 동기화/재표본, 평균/누적 정합
    ├─ 매칭·표본: matchup 윈도, paired-sample/독립성, 대표성오차, triple collocation
    ├─ 메타데이터: UDUNITS, CF convention/standard_name
    └─ 자료처리: 결측/QC, gap filling(DINEOF), climatology/anomaly, 표준화편차, bias correction/QM, detiding, 필터, 수직보간
```

### 분류 축 4종 (메서드 카드를 라우팅하는 직교 축)

분류체계를 한 트리로만 보면 교차항목이 많아진다. 실제 Skill 라우팅은 아래 **4개의 직교 축**을 조합해 카드를 선택하는 것이 효율적이다.

| 축 | 값(예시) | 라우팅 근거 |
|---|---|---|
| **자료형(data form)** | 격자(NetCDF) / 점·시계열(CSV) / 위성트랙(along-track) / 스펙트럼 | 입력 파일 구조에서 자동 판별 |
| **변수성질(variable nature)** | 연속 / 범주(임계) / 원형(방향) / 벡터 / 확률·앙상블 / 극값 | 변수명·차원·앙상블축 유무로 판별 |
| **검증목적(question)** | 정확도 / 패턴·구조 / 위상·시간 / 분포·꼬리 / 물리보존 / 변동모드 | 사용자 의도 또는 기본 묶음 |
| **도메인(domain)** | 기상 / 파랑 / 수온·염분 / 해류·조류 / 해수면 / 위성 | 변수·표준이름·메타데이터로 자동 판별(C절) |

---

## C. 도메인 자동판별 → 추천 분석 묶음 (Domain → Recipe 매핑)

Skill이 입력 NetCDF/CSV의 **변수명·CF standard_name·차원**으로 도메인을 자동 판별한 뒤, 아래 표의 **기본 묶음(default bundle)** 을 호출한다. 모든 도메인은 **공통 전제(전처리·공통 오차통계)** 를 먼저 거친다.

### C-0. 모든 도메인 공통 (항상 실행)

| 단계 | 묶음 | 카드 출처 |
|---|---|---|
| 0. 전처리·정합 | 보간/재격자, land-sea mask, 시간 동기화, matchup 윈도, paired-sample, 단위·CF 정합, 결측/QC | `15` 전반 |
| 1. 1차 오차통계 | ME/bias, MAE, RMSE, (정규화) nRMSE/SI, Pearson r, R² | `01` |
| 2. 종합 요약 | Taylor diagram(+TSS), Target diagram, (격자면) ACC/패턴상관 | `01`, `02` |
| 3. 유의성 | bootstrap/블록부트스트랩 CI, 유효표본 보정, (모델비교 시) Diebold-Mariano/SPCT | `01`, `02`, `13` |

### C-1. 도메인별 추천 묶음

| 판별 도메인 | 대표 변수(standard_name 예) | 자료형 | **기본 메서드 묶음 (default recipe)** | 주 출처 파일 |
|---|---|---|---|---|
| **기상·대기** | `eastward_wind`/`northward_wind`, `air_temperature`(2m), `air_pressure_at_mean_sea_level`, `precipitation`, `relative_humidity` | 격자+시계열 | 공통(C-0) + **바람**: VRMSE·벡터상관·u/v 성분; **풍향**: 원형 평균오차/원형상관(±180° 보정); **기온**: bias/RMSE·일변동·lapse-rate; **MSLP/종관**: S1 gradient·500hPa ACC; **강수**: double-penalty 주의·log/√변환·QQ → 범주(POD/FAR/CSI/ETS/HSS/PSS) → 극값(EDI/SEDI) → 공간(FSS/SAL/MODE/intensity-scale); **분포**: KS·Perkins PDF; **앙상블**: Brier/BSS·CRPS·ROC·rank hist·reliability | `07`(+01,02,03,13) |
| **파랑(waves)** | `sea_surface_wave_significant_height`(Hs/Hm0), `*_period`(Tp/Tm01/Tm02), `*_to_direction`(Dir) | 격자+시계열+트랙+스펙트럼 | 공통(C-0) + **벌크**: Hs bias/RMSE/**SI**(파랑 1차표준)/R·OLS slope·HH symmetric slope·Willmott d·NSE; **주기**: Tp/Tm01/Tm02; **파향**: 원형통계·circular RMSE·directional spread; **분포·극치**: QQ·POT-GPD/GEV·return period; **스펙트럼**: 1D E(f)·2D E(f,θ)·moments·windsea/swell partition; **위성**: altimeter colocation·triple collocation; **운영틀**: WMO-JCOMM/ECMWF LC-WFV | `08`(+01,03,05,12) |
| **수온·염분** | `sea_water_temperature`/`sea_surface_temperature`, `sea_water_salinity`/`sea_surface_salinity` | 격자+프로파일+시계열 | 공통(C-0) + **표층**: SST(GHRSST L4/in situ)·SSS(SMOS/SMAP/Argo) bias/RMSE·robust(MAD); **프로파일**: Argo match-up 깊이별; **수괴**: T-S diagram·spiciness; **혼합층**: MLD·ILD/BLT; **적분량**: OHC·salt/FW content·D20/약층; **전선**: SST front(Canny/Cayula-Cornillon)·gradient; **단면/등밀도면**: section·isopycnal; **분포·변동**: PDF/Q-Q/Perkins·EOF·파수스펙; **전제**: TEOS-10 변환; **운영틀**: GODAE Class-4 | `09`(+01,02,05,12) |
| **해류·조류·순환** | `eastward_sea_water_velocity`/`northward_sea_water_velocity`, 유향, 수송 | 격자+시계열(ADCP/표류부이/HF radar) | 공통(C-0) + **성분**: u/v RMSE/MAE/bias; **벡터**: 복소상관(Kundu)·벡터상관(Crosby)·벡터/복소 RMSE; **방향**: 원형통계·주축/변동타원; **분포**: 속력 Q-Q/PDF; **라그랑지안**: PVD·입자추적·표류부이 분리거리; **조석류**: 조화분석·조류타원·회전스펙트럼(Gonella CW/CCW); **수송·에너지**: volume transport·Sverdrup·MKE/EKE; **표면류 분해**: 지형류+Ekman+Stokes; **와류**: Okubo-Weiss·eddy census·FTLE/FSLE·LCS; **공간**: EOF·패턴상관·Taylor | `10`(+04,05,12) |
| **해수면·조위** | `sea_surface_height_above_geoid`/`*_above_reference_ellipsoid`(SSH/SLA/ADT), 조위 | 격자+시계열(검조소)+트랙 | 공통(C-0, datum/보정 정합 강조) + **조석**: 조화상수 추정·admittance·진폭오차 ΔH·지각오차 ΔG·복소차 D·분조 RMS·다분조 RSS·form factor·datum; **비조석**: residual·skew surge·폭풍해일(peak/timing·99p·POD/FAR)·역기압/DAC; **재분석/위성**: SSH/ADT vs tide-gauge/altimetry·crossover·내부조석·aliasing 점검·triple collocation; **계절·추세**: Sa/Ssa·MSL trend·VLM/GIA·해수면수지(steric/manometric); **극치**: GEV/Gumbel·POT/GPD·JPM; **QC**: datum 안정성·spike·buddy check | `11`(+01,03,05,12) |
| **위성·원격탐사**(자료원 축) | (위 변수 + L2/L3/L4 처리수준 메타) | 트랙+격자 | 공통(C-0) + **매칭**: spatiotemporal matchup·대표성오차·**TC/ETC/QC**; **분포·사건**: QQ/CDF·anomaly 상관·categorical·object-based; **고도계**: along-track vs gridded·wavenumber spectrum/유효해상도; **SST**: L2/L3/L4(GHRSST)·skin-bulk/diurnal·front; **풍**: scatterometer 벡터; **해색**: Chl-a(Bailey-Werdell/Zibordi, log10); **처리**: L2→L3 비닝·crossover·uncertainty u-plot | `12`(+08,09,11) |

### C-2. 비도메인 트리거 (변수성질·작업유형으로 추가 호출)

| 트리거 조건(자동 감지) | 추가로 끌어오는 묶음 | 출처 |
|---|---|---|
| **앙상블 축이 존재** | rank histogram, spread-skill(+ratio), CRPS(+분해)/CRPSS, Brier/BSS, reliability, ROC | `03`, `13`, `14` |
| **비교 대상이 또 다른 모델** | Diebold-Mariano, bootstrap CI, SPCT, MMEM, 성능·독립성 가중 | `13`, `02`, `01` |
| **산출물이 AI/ML 모델** | double-penalty 진단, RAPSD/유효해상도, SSIM/LPIPS/FID, 물리정합(보존량/PDE residual), UQ(ECE/PICP/conformal), OOD/롤아웃, XAI | `14` |
| **다운스케일/편향보정 수행** | PP/MOS, quantile mapping/QDM, MBCn, 분산팽창, VALUE 프레임워크, CDF/변화신호 보존 | `13`, `14` |
| **물리 일관성 점검 요청** | 수지 닫힘(질량/운동량/열/염), KE/EKE, 와도/PV/enstrophy, 수송/MOC, WMT, 지형류/열풍 | `04` |
| **변동모드·전파구조 관심** | EOF/REOF/CEOF, SVD/MCA, CCA, SSA/MC-SSA, POD/SPOD, DMD, k-ω | `05` |
| **위상·시간지연·추세·변화점** | 교차상관/lag, 위상·진폭오차, STL, Mann-Kendall/Sen, change-point, DTW, 필터링 | `06` |
| **불규칙·결측 시계열** | Lomb-Scargle, multitaper, gap filling(DINEOF), paired-sample 재정의 | `05`, `06`, `15` |

---

## D. 교차 등장(횡단) 방법 — 중복 정의 방지용 정규화 표

같은 방법이 여러 파일에 등장한다. Skill 구현 시 **단일 구현(canonical) + 도메인별 파라미터/임계** 패턴을 권장한다. 주요 횡단 방법:

| 방법 | 등장 파일 | 정규화 권고 |
|---|---|---|
| RMSE/MAE/bias | 01, 07, 08, 09, 10, 13, 14 | 단일 구현, 면적가중(cosφ) 옵션·결측마스크 공통 |
| Taylor diagram(+TSS) | 01, 02, 05, 06, 08, 09, 10, 12, 13, 14 | 단일 구현, 평균제거(bias는 별도/target diagram 보고) |
| Anomaly Correlation(ACC) | 01, 02, 07, 09, 12, 13 | 동일 climatology 정의 강제(기준기간·격자 일치) |
| FSS / 이웃검증 | 02, 03, 07, 13, 14 | 임계·이웃크기 스캔 공통, useful-scale=0.5+f₀/2 |
| SAL / MODE | 02, 03, 07, 13 | 객체화 파라미터(평활반경·임계) 명시·고정 |
| GEV·POT/GPD·return level | 03, 08, 11 | 단일 극값 엔진, declustering·임계선택 공통 |
| Triple Collocation(TC/ETC) | 08, 11, 12, 15 | 단일 구현, 자료 3종 오차 무상관 가정 점검 |
| CRPS·Brier·rank hist·reliability | 03, 07, 08, 13, 14 | 앙상블 축 감지 시 공통 호출 |
| 조화·조석분석(T_TIDE/UTide) | 05, 06, 11 | 단일 엔진, Rayleigh·nodal 보정 공통 |
| Rotary spectrum·EOF·PSD | 05, 06, 09, 10 | 신호처리 코어 공유(window·detrend·정규화 일치) |
| Quantile mapping/QDM | 13, 14, 15 | bias-correction 코어 공유, 추세보존(QDM) 옵션 |
| Matchup/colocation·대표성오차 | 08, 09, 11, 12, 15 | 전처리 코어(15)로 일원화 |

---

## E. Skill recipes로 옮기는 설계 지침 (구현 메모)

1. **라우터(router) 우선**: 입력 메타데이터 → (자료형, 변수성질, 도메인) 3-tuple 판별 → C절 표에서 default bundle 선택. 판별 불가/혼합 도메인은 공통(C-0)만 적용 후 사용자에게 도메인 확인.
2. **전처리 게이트(15) 필수 선행**: 모든 recipe는 `15`의 정합 단계를 통과해야 하며, **모델·참조에 동일 처리·동일 순서**를 강제(spurious difference 방지).
3. **카드=함수, 묶음=recipe**: 메서드 카드 1개 = 검증 함수 1개(입력·전제·출력·해석임계 포함). 도메인 묶음 = 카드의 정렬된 호출 목록(C-1).
4. **단일 지표 금지 원칙**: 모든 recipe는 최소 (정확도 + 패턴/분포 + 편향) 3축을 보고. AI/극값/강수는 추가 축(스펙트럼/공간/극값) 강제.
5. **해석임계는 관행값으로 기본 제공하되 영역·해상도 의존 경고**를 항상 출력.
6. **유의성 기본 동반**: 모델 비교·랭킹에는 bootstrap CI(자기상관 시 블록)·DM/SPCT를 기본 첨부.

---

## F. 출처 표기 원칙(공통)

본 카탈로그 전체는 **검증 가능한 실제 출처만** 인용한다. 표준 교과서·지침(Wilks, Jolliffe & Stephenson, WMO/JCOMM, Taylor 2001, Willmott, Murphy 1988, Stow et al. 2009, Coles 2001, Emery & Thomson, Vallis 2017, Griffies 2004 등)은 그 형태로 표기하고, **DOI는 확인된 것만** 적으며 지어내지 않는다. 1차 출처 미열람 항목은 각 파일에서 "(확인요)"로 명시한다.

---

## G. 검증 해석의 함정 — 반드시 지킬 원칙 (Critical caveats)

> Skill이 분석을 **자동화**하기 때문에, 아래 원칙을 어기면 "그럴듯하지만 틀린 결론"을 빠르게 대량생산하게 된다. 모든 recipe·해석 문장 생성은 이 원칙을 강제한다.

1. **기준자료 ≠ 참값(truth).** ERA5/GLORYS/재분석/위성 L4는 "참값"이 아니라 **기준(reference)**이다. 보고문에 "truth/정답"이라 쓰지 말고 "reference/reanalysis 대비"로 표현한다. 차이는 "모델 오차"가 아니라 "모델−기준 차이"다.
2. **오차 독립성 점검.** 우리 모델과 기준자료(ERA5/GLORYS)가 **같은 강제력·같은 동화관측**을 공유하면 두 자료의 오차가 상관되어 **차이를 과소평가**한다. 비교 전 자료 출처·동화 입력의 독립성을 확인하고, 의존 가능성이 있으면 보고문에 명시한다.
3. **동화·보간 산물을 독립 관측처럼 쓰지 말 것.** 재분석·GHRSST L4·격자화 위성자료는 이미 보간·동화된 산물이다. 삼중대조(TC) 등 "오차 무상관 가정"이 필요한 기법에 이런 자료를 독립 3자로 넣으면 가정이 깨진다.
4. **해석 임계값은 advisory(참고).** `SI<0.15`, `ACC≥0.6`, `NSE 등급`, `FSS useful-scale` 등 관행 임계는 **변수·해역·해상도·기준자료에 따라 달라진다.** 자동으로 "좋음/나쁨"을 단정하지 말고, ① 임계는 advisory로 표시, ② 영역·해상도 의존 경고 항상 동반, ③ 가능하면 "기준자료 불확실성 대비 상대평가". (구현 시 `thresholds.yml`에 `metric·domain·variable·source·applicability`로 분리 권장.)
5. **"확인요" 출처는 확정 인용 금지.** 각 파일의 "(확인요)" 표시 출처·기관 페이지(WMO/JCOMM 등)·기술문서 URL은 변동·미검증 가능성이 있다. 자동 인용문에서 **확정 출처처럼 단정하지 않는다.**
6. **단일 지표 금지.** 어떤 recipe도 지표 1개로 결론내지 않는다. 최소 **정확도 + 편향 + 패턴/분포** 3축 + **유의성**(bootstrap/DM/SPCT)을 함께 보고한다(강수·극값·AI 산출물은 공간/극값/스펙트럼 축 추가).
