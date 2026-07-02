# 도메인: 대기질·대기화학 (Air Quality / Atmospheric Chemistry) 검증·분석 방법 카탈로그

이 문서는 화학수송모델(CTM: CMAQ, CAMx, WRF-Chem, GEOS-Chem, CAM-chem, MOZART, CHIMERE, SILAM 등)과 배출·확산 모델의 대기질 산출물(PM2.5·PM10·O3·NO2·SO2·CO·AOD 및 PM 화학종)을 지상 관측소(in-situ monitoring)·위성 컬럼(satellite column)·재분석(CAMS reanalysis, MERRA-2 aerosol 등)과 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 대기질 검증의 핵심 특성은 (1) 농도가 **로그정규(log-normal)에 가까운 심한 우측 꼬리**를 가져 로그공간·대칭 정규화 지표(MFB/MFE, FAC2)가 필수라는 점, (2) **초과사건(exceedance) 검증**(주의보/기준 초과)이 규제·보건상 1급 목적이라는 점, (3) 강한 **일변동(diurnal)·주간(weekly)·계절 주기**를 별도로 진단해야 한다는 점, (4) **측정소 대표성(representativeness)** 과 격자-점 불일치, (5) 위성 컬럼(AOD·대류권 NO2)의 **연직 적분·평균화커널(averaging kernel)** 처리다. 표준 성능기준은 Boylan & Russell(2006, PM), Emery et al.(2017, 오존/PM 광화학모델), Chang & Hanna(2004, 확산모델)에서 온다. 공통 통계지표(RMSE·bias·상관·Taylor·QQ·bootstrap 등)는 재정의하지 않고 `01`·`03`·`06`·`12`·`figures/16`으로 교차링크한다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석), [시계열]=측정소 CSV/텍스트, [트랙/타일]=위성 L2/L3(along-track·swath·gridded), [프로파일]=연직/컬럼, [화학종]=PM speciation(SO4²⁻/NO3⁻/NH4⁺/OC/EC 등).
> **"우리 모델 vs 관측/위성/재분석" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 지표는 재정의 금지** — RMSE·MAE·bias·상관·R²·Taylor/Target·bootstrap·QQ·KS·범주형 2×2 기초정의는 `01_error_statistics.md`·`03_categorical_event_extremes.md`·`06_timeseries_signal.md`·`figures/16`을 본다. 이 카드는 **대기질 특화 사용법·임계·전제·함정**만 기술한다.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **로그공간 bias·RMSE (log-space error)** — 로그정규 농도의 곱셈적 오차
- ★ **분수편향·분수오차 MFB / MFE (Mean Fractional Bias / Error)** — 대칭·유계 정규화 지표
- ★ **정규화평균편향·오차 NMB / NME (Normalized Mean Bias / Error)** — 광화학모델 1차 표준
- ★ **FAC2 (Factor of 2)** — 2배 이내 일치율, 이상치에 강건
- **기하평균편향 MG / 기하분산 VG / NMSE** — 확산모델 로그공간 성능쌍
- ★ **Boylan & Russell (2006) PM 성능 목표·기준** — MFB/MFE 목표·기준선
- ★ **Emery et al. (2017) 광화학모델 성능 벤치마크** — O3·PM2.5 NMB/NME/r 목표·기준
- **Chang & Hanna (2004) 확산모델 수용기준** — FB·NMSE·FAC2·MG·VG
- ★ **초과사건 범주형 검증 (exceedance POD/FAR/CSI)** — 기준·주의보 임계 2×2
- **오존 설계값·MDA8 검증 (design value / MDA8)** — 규제지표 재현
- ★ **일변동 검증 (diurnal cycle)** — 시간대별 bias·진폭·위상
- **주간주기·주말효과 검증 (weekly cycle / weekend effect)** — 요일 배출패턴
- **계절·월별 층화 검증 (seasonal stratification)** — 계절 의존 오차 분해
- ★ **측정소 대표성 오차 (station representativeness)** — 점-격자 불일치·측정소 분류
- **측정소 유형·환경 층화 (urban/traffic/rural/background)** — 국지 오염원 영향 분리
- ★ **위성 컬럼 매치업 — 대류권 NO2 (tropospheric NO2 column)** — OMI/TROPOMI vs 모델 컬럼
- ★ **위성 AOD 매치업 (aerosol optical depth)** — MODIS/VIIRS/AERONET vs 모델
- **평균화커널·연직민감도 적용 (averaging kernel / AK)** — 위성 컬럼 정합
- **AOD↔지상 PM 관계 검증 (AOD–PM2.5 relationship)** — 위성 추정 대리검증
- ★ **PM 화학종 분리 검증 (PM speciation: SO4/NO3/NH4/OC/EC)** — 성분별 bias·닫힘
- **질량 닫힘·미결정질량 (mass closure / reconstructed mass)** — 성분합 vs 총질량
- **오존 전구물질·광화학 지표 (NOx, VOC, HCHO/NO2, OX)** — 생성체제 진단
- **입자 수농도·크기분포 (number / size distribution)** — 에어로졸 미세물리
- ★ **분포·꼬리 비교 (QQ / PDF / KS)** — 로그정규 분포·고농도 꼬리
- ★ **Taylor / Target 다이어그램 (대기질 적용)** — 다지점·다종·다모델 요약
- **소스-수용 기여 검증 (source apportionment vs receptor)** — PMF/CMB 대조
- ★ **확률·앙상블 대기질 예보 검증 (CRPS/Brier/ROC)** — 초과확률·앙상블
- **공간장 패턴·오차지도 (spatial map / FSS)** — 격자 농도장 패턴
- ★ **재분석 격자 대조 (CAMS / MERRA-2 gridded)** — 광역 면적 bias/RMSE
- **침적·플럭스 검증 (wet/dry deposition)** — 습·건성 침적 수지
- ★ **운영·규제 검증 프레임워크 (FAIRMODE MQI / EPA modeling guidance)** — 표준 절차

---

### ★ 로그공간 bias·RMSE (로그공간 오차 / log-space error metrics)
- 무엇을 측정/검증하나: 대기질 농도는 로그정규(log-normal)에 가까운 우측 꼬리 분포라, 선형 bias/RMSE는 소수 고농도 사건에 지배된다. log(model)−log(obs)로 계산해 **곱셈적(비율) 오차**를 대칭적으로 본다.
- 정의·수식: log-bias = mean(ln mᵢ − ln oᵢ) = ln(기하평균비). log-RMSE = √[mean((ln mᵢ − ln oᵢ)²)]. exp(log-bias)가 기하평균편향(아래 MG). 선형 RMSE 정의는 `01`.
- 적용 도메인/자료형: PM2.5·PM10·NO2·SO2·CO·AOD 등 양수·우측꼬리 농도. [시계열]/[격자]/[트랙].
- 입력·전제: 양수 값만(0/음수 처리 규칙 필요 — 검출한계 이하는 LOD/2 대입 또는 제거, 규칙 명시). 관측·모델 동일 시각·위치 매치업(`15`). 단위 통일(µg/m³ 표준·기준 상태 STP 여부 확인).
- 해석 기준(advisory): 로그공간이 선형보다 저농도역 정보를 보존한다. 다만 **오존은 로그정규가 약해**(변동폭 작음) 선형·NMB가 관례 — 로그지표는 주로 PM·에어로졸·NOx·1차오염물에 권장. 임계 절대선 없음. 계절·측정소유형별로 크게 달라짐.
- 한계·주의(§G): 0/검출한계 처리 규칙이 결과를 좌우(§G-6 단일지표 금지, 규칙 반드시 보고). 오존처럼 로그정규 아닌 변수에 남용 금지. 관측 하한 절단 편향.
- 출처: Seinfeld & Pandis, *Atmospheric Chemistry and Physics* (Wiley, 농도 분포 특성 — 표준 교과서); Chang & Hanna (2004, *Meteorology and Atmospheric Physics* 87:167–196, 로그공간 지표 MG/VG 맥락).

---

### ★ 분수편향·분수오차 (분수편향 MFB / 분수오차 MFE / Mean Fractional Bias·Error)
- 무엇을 측정/검증하나: 모델과 관측을 **대칭적으로** 정규화한 편향(MFB)·오차(MFE). 저농도에서 NMB가 과대·과소로 폭주하는 문제를 완화. PM 검증의 대표 지표.
- 정의·수식: MFB = (1/N)Σ [ (mᵢ − oᵢ) / ((mᵢ + oᵢ)/2) ] = (2/N)Σ (mᵢ−oᵢ)/(mᵢ+oᵢ). MFE = (2/N)Σ |mᵢ−oᵢ|/(mᵢ+oᵢ). MFB는 −200%~+200%(±2), MFE는 0~200%(0~2)로 유계. 분모에 관측·모델 평균을 써서 어느 한쪽이 0에 가까워도 발산하지 않음.
- 적용 도메인/자료형: 주로 PM2.5·PM10·PM 화학종. NO2/SO2/CO에도 사용. [시계열]/[격자].
- 입력·전제: 매치업 쌍. 저농도(둘 다 매우 작음)에서 여전히 노이즈 큼 → 최소농도 필터 관행. 단위·상태 통일.
- 해석 기준(advisory): Boylan & Russell(2006) **목표(goal)** MFE ≤ 50% 및 |MFB| ≤ 30%, **기준(criteria)** MFE ≤ 75% 및 |MFB| ≤ 60%(아래 전용 카드). 이 임계는 미국 PM 사례 통계 기반 — 지역·화학종·해상도에 따라 달라지므로 advisory. MFB>0 과대추정.
- 한계·주의(§G): 목표/기준선은 **pass/fail 시험이 아니라 참고선**(§G-4). 화학종별로 달성 난이도 상이(질산염·유기탄소가 어려움). 저농도 필터 임계가 결과에 영향.
- 출처: Boylan & Russell (2006, *Atmospheric Environment* 40(26):4946–4959, "PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models"); Seinfeld & Pandis (교과서).

---

### ★ 정규화평균편향·오차 (정규화평균편향 NMB / 정규화평균오차 NME / Normalized Mean Bias·Error)
- 무엇을 측정/검증하나: 총합(합산) 정규화 편향·오차. 광화학모델(오존·PM) 성능평가의 가장 널리 쓰이는 표준. Emery et al.(2017) 벤치마크의 핵심 지표.
- 정의·수식: NMB = Σ(mᵢ−oᵢ) / Σoᵢ. NME = Σ|mᵢ−oᵢ| / Σoᵢ. (합산 정규화 = 관측 총량 대비.) 대안: 평균정규화편향 MNB=(1/N)Σ(mᵢ−oᵢ)/oᵢ, 평균정규화총오차 MNGE — **저농도 발산**이 심해 Emery/EPA는 NMB/NME(합산형)를 권장. 관련 절대지표(MB·RMSE)는 `01`.
- 적용 도메인/자료형: O3(특히 MDA8), PM2.5, NO2 등. [시계열]/[격자].
- 입력·전제: 매치업 쌍. 오존은 저농도·야간값 제외(예: MDA8 또는 시간 오존 ≥ 특정 임계) 관행 — 절단 임계 반드시 명시(벤치마크 값이 절단 규칙에 의존).
- 해석 기준(advisory): Emery et al.(2017) — **오존(1시간·MDA8)**: NMB ≤ ±5%(goal)·±15%(criteria), NME ≤ 15%(goal)·25%(criteria), r ≥ 0.50~0.75; **PM2.5(총질량)**: NMB·NME는 오존보다 느슨(성분·계절 의존, 예 NME ~50% 수준까지 흔함). 이 값들은 "미국 과거 사례 2/3가 달성한 수준"이라 **지역·기간·해상도 전이 시 재보정 필요**(advisory).
- 한계·주의(§G): MNB/MNGE(평균정규화형)와 혼동 금지 — 정의에 따라 값 크게 다름(§G-6 정의 명시). 벤치마크는 참고선(§G-4). 오존 절단 임계·시간정의(1h/MDA8/MDA1)에 민감.
- 출처: Emery, Liu, Russell, Odman, Yarwood & Kumar (2017, *Journal of the Air & Waste Management Association* 67(5):582–598, doi:10.1080/10962247.2016.1265027, "Recommendations on statistics and benchmarks to assess photochemical model performance"); US EPA *Modeling Guidance for Demonstrating Air Quality Goals for Ozone, PM2.5, and Regional Haze* (2018).

---

### ★ FAC2 (2배 인자 일치율 / Factor of 2)
- 무엇을 측정/검증하나: 예측이 관측의 1/2 ~ 2배 범위 안에 드는 표본 비율. 이상치에 강건하고 유계(0~1)한 확산·대기질 성능지표.
- 정의·수식: FAC2 = (0.5 ≤ mᵢ/oᵢ ≤ 2.0 인 표본 수) / N. (oᵢ=0 근처 처리 규칙 필요.) 값 1에 가까울수록 우수.
- 적용 도메인/자료형: 확산모델(점·선오염원 영향)·CTM 농도. 특히 국지 확산·트레이서 실험. [시계열]/[격자].
- 입력·전제: 매치업 쌍. 검출한계 이하·0 관측 처리 규칙 명시. 로그정규 자료에 적합.
- 해석 기준(advisory): 확산모델 관행상 FAC2 ≥ 0.5(절반 이상이 2배 이내)면 "수용 가능" 수준으로 논의(Chang & Hanna 2004) — 도시·복잡지형·화학종에 따라 달라지므로 advisory. 광역 CTM 배경농도는 더 높게 나온다.
- 한계·주의(§G): 편향 방향을 못 봄(FB·MFB 병행). "2배"는 관대한 기준 → 정밀 진단 부적합, 스크리닝용. 저농도역 비율 왜곡.
- 출처: Chang & Hanna (2004, *Meteorology and Atmospheric Physics* 87:167–196, "Air quality model performance evaluation", doi:10.1007/s00703-003-0070-7); Hanna & Chang (2012, urban dispersion 수용기준 후속).

---

### 기하평균편향·기하분산·정규화평균제곱오차 (MG / VG / NMSE)
- 무엇을 측정/검증하나: 확산모델 성능의 로그공간 3종 세트. MG(계통 곱셈편향), VG(로그공간 산포), NMSE(정규화 총오차). Chang & Hanna 수용기준의 축.
- 정의·수식: MG = exp[ mean(ln oᵢ − ln mᵢ) ](기하평균비, 1=무편향). VG = exp[ mean((ln oᵢ − ln mᵢ)²) ](1=완벽). NMSE = mean((oᵢ−mᵢ)²)/(ō·m̄)(선형 정규화 총오차). 선형 편향지표 FB = 2(ō−m̄)/(ō+m̄)와 짝.
- 적용 도메인/자료형: 로그정규 농도(PM·1차오염물·트레이서). [시계열].
- 입력·전제: 양수만(0/LOD 처리 규칙). MG/VG는 곱셈편향에, FB/NMSE는 가산편향에 민감 → 함께 봐야 편향 구조 판별.
- 해석 기준(advisory): Chang & Hanna(2004) 관행 목표 예: |FB|<0.3, NMSE<1.5, 0.7<MG<1.3, VG<1.6, FAC2>0.5 — 실험·해역 의존이라 advisory. 절대 pass/fail 아님.
- 한계·주의(§G): MG/VG는 0·저농도에 극도로 민감(로그) → LOD 처리·최소농도 컷 필수. 선형(FB/NMSE)과 로그(MG/VG)가 상충할 수 있음(동시 보고).
- 출처: Chang & Hanna (2004, *Meteorol. Atmos. Phys.* 87:167–196); Hanna, Chang & Strimaitis (1993, *Atmospheric Environment* 27A, 확산모델 통계 성능).

---

### ★ Boylan & Russell (2006) PM 성능 목표·기준 (PM performance goals & criteria)
- 무엇을 측정/검증하나: 3차원 대기질모델의 **PM(및 광소멸)** 성능을 MFB/MFE로 등급화하는 표준 기준선. "목표(goal)=최선 근접"·"기준(criteria)=수용 가능" 2단계.
- 정의·수식: **목표**: MFE ≤ +50% 그리고 −30% ≤ MFB ≤ +30%. **기준**: MFE ≤ +75% 그리고 −60% ≤ MFB ≤ +60%. 저농도로 갈수록 관대해지는 **농도 의존 완화(≤ ~2 µg/m³에서 기준 완화)** 를 원저가 도입.
- 적용 도메인/자료형: PM2.5·PM10 총질량 및 화학종(SO4/NO3/NH4/OC/EC), 광소멸(bext). [시계열]/[격자].
- 입력·전제: 매치업 쌍, MFB/MFE 계산(위 카드). 화학종별로 별도 평가 권장. 관측 불확실성(성분측정 오차) 고려.
- 해석 기준(advisory): 목표 안=우수, 기준 안=수용 가능으로 통용되나 **미국 사례 기반 참고선**. 질산염·유기물은 목표 미달이 흔함 — 지역·계절 의존이 커 advisory. good/bad 단정 금지.
- 한계·주의(§G): pass/fail로 오용 금지(§G-4). 농도 완화식·저농도 컷 정의가 결과 좌우. 화학종 미분리 총질량만 보면 상쇄 오차 은폐.
- 출처: Boylan & Russell (2006, *Atmospheric Environment* 40(26):4946–4959).

---

### ★ Emery et al. (2017) 광화학모델 성능 벤치마크 (photochemical model benchmarks)
- 무엇을 측정/검증하나: 오존·PM2.5(및 성분)에 대해 NMB·NME·r의 **목표(goal)·기준(criteria)** 을 미국 과거 광화학모델 응용 통계에서 도출한 참고 벤치마크.
- 정의·수식: 지표는 NMB·NME(위 카드)·Pearson r(`01`). **오존(MDA8·1h)**: NMB goal ≤ ±5%, criteria ≤ ±15%; NME goal ≤ 15%, criteria ≤ 25%; r 참고 ≥ 0.50(사례 2/3 달성선). **PM2.5 총질량 및 성분**은 화학종·계절별로 별도 벤치마크(총 PM2.5는 오존보다 느슨; SO4가 상대적 양호, NO3·OC·EC는 관대한 기준).
- 적용 도메인/자료형: 규제·정책 광화학 시뮬레이션(오존·PM SIP). [시계열]/[격자].
- 입력·전제: 표준 매치업·QC, 오존 시간정의·절단 규칙 통일. 성분자료(예: IMPROVE/CSN 미국, 국내는 성분측정망).
- 해석 기준(advisory): "goal=역대 최고 수준, criteria=전형적 수용 수준". **미국 응용 분포 기반**이므로 다른 국가/도시/해상도에 그대로 적용 시 재보정·맥락화 필요(§G-4). 한국 등 지역 벤치마크(예: China NO2/SO2/CO/PM10 benchmark 논문) 참조 권장.
- 한계·주의(§G): 참고선이지 합격선 아님. 지역 전이성 낮음(배출·기상 상이). r 단독 신뢰 금지(bias 병행, §G-6).
- 출처: Emery et al. (2017, *J. Air & Waste Manage. Assoc.* 67(5):582–598, doi:10.1080/10962247.2016.1265027); 후속 지역 벤치마크: "Recommendations on benchmarks for photochemical air quality model applications in China — NO2, SO2, CO and PM10" (2023, *Atmospheric Environment*) 및 China Part 2: Ozone (2025, *ACP* 25:4233).

---

### Chang & Hanna (2004) 확산모델 수용기준 (dispersion model acceptance criteria)
- 무엇을 측정/검증하나: 대기확산모델(점·면오염원, 사고·유해가스 포함)의 통계 성능을 FB·NMSE·FAC2·MG·VG로 종합 평가하는 표준 절차·수용선.
- 정의·수식: 위 MG/VG/NMSE·FAC2 카드의 지표 세트. 관행 수용선(advisory): |FB|<0.3, NMSE<4(도시)~1.5(외곽), FAC2>0.5, 0.7<MG<1.3, VG<1.6 — 실험 종류(트레이서 vs 상시망)에 따라 완화.
- 적용 도메인/자료형: 국지·중규모 확산(AERMOD/CALPUFF류)·CTM. [시계열].
- 입력·전제: 로그정규 자료, LOD 처리, 짝지은 쌍/미짝(paired-in-time vs -in-space) 구분 명시(사고 확산은 최대치 중심 미짝 평가 흔함).
- 해석 기준(advisory): 여러 지표 동시 충족을 요구(단일 지표 금지). 도시 복잡지형은 자연 산포로 기준 완화. 영역·해상도 의존 경고 동반.
- 한계·주의(§G): 확산모델 특유의 "paired vs unpaired" 평가 방식 차이가 결론을 바꿈 → 방식 명시(§G-6). 극한 단일사건 평가는 통계 불안정.
- 출처: Chang & Hanna (2004, *Meteorol. Atmos. Phys.* 87:167–196, doi:10.1007/s00703-003-0070-7).

---

### ★ 초과사건 범주형 검증 (임계 초과 POD·FAR·CSI / exceedance categorical)
- 무엇을 측정/검증하나: "농도가 대기환경기준·주의보 임계(예: 오존 0.09/0.12 ppm 시간, PM2.5 35/75 µg/m³ 일평균, PM 주의보)를 넘었는가"라는 이진 사건을 모델이 맞히는지. 보건·규제상 1급 목적.
- 정의·수식: 2×2 분할표(hit a, false alarm b, miss c, correct-negative d). POD=a/(a+c), FAR=b/(a+b), CSI(=TS)=a/(a+b+c), Bias score=(a+b)/(a+c), HSS/ETS(우연보정). 2×2 지표 기초정의·드문사건 EDI/SEDI는 `03`.
- 적용 도메인/자료형: O3·PM2.5·PM10 임계 경보. [시계열]/[격자].
- 입력·전제: 매치업 + 합의된 임계값(국가 기준·주의보 발령선). 임계 초과사건이 드물수록 표본 희소 → bootstrap CI(`01`) 동반.
- 해석 기준(advisory): POD↑·FAR↓·CSI↑ 양호. 오존/PM 고농도는 드문 사건이라 점수 불안정 — 여러 임계·계절별 평가·신뢰구간 필수(advisory). 지역·연도별로 사건 빈도가 달라 절대비교 주의.
- 한계·주의(§G): 격자 검증의 **double penalty**(위치 약간 어긋나면 miss+false 동시, §G) → 이웃검증(FSS, `02`) 병행. 단일 임계는 정보손실 → ROC(`03`)와 병행. 드문사건 편향(§G-6).
- 출처: Jolliffe & Stephenson, *Forecast Verification* (범주형 표준); Kang et al. (2007, *Journal of Geophysical Research*, 오존 초과 범주형 검증); US EPA modeling guidance.

---

### 오존 설계값·MDA8 검증 (design value / MDA8 daily maximum 8-h)
- 무엇을 측정/검증하나: 규제에서 실제 쓰는 지표(일 최대 8시간 오존 MDA8, 설계값 design value=연 4번째 최고 MDA8의 3년 평균)를 모델이 재현하는지. 원자료 시간 오존이 아니라 **규제 통계량 자체**를 검증.
- 정의·수식: MDA8 = 하루 중 이동 8시간 평균의 최대값. 설계값 = 관측·모델 각각의 규제 통계 절차 적용 후 비교. 검증은 그 통계량에 bias/NMB/NME/r(`01`) 적용.
- 적용 도메인/자료형: O3. [시계열]/[격자]. PM2.5는 98퍼센타일 일평균·연평균이 대응 규제지표.
- 입력·전제: 완전한 시간자료(8시간 이동평균 계산 규칙·결측률 기준 통일). 관측·모델 동일 절차. 관측소별.
- 해석 기준(advisory): MDA8 NMB/NME는 Emery(2017) 벤치마크 적용. 설계값은 소수 상위값 기반이라 표본·꼬리 민감 → QQ(아래)·극값(`03`) 병행. 지역 의존.
- 한계·주의(§G): 시간 오존 성능이 좋아도 MDA8·설계값은 어긋날 수 있음(꼬리·타이밍). 결측 처리 규칙이 통계량 좌우.
- 출처: US EPA *Modeling Guidance* (2018, MDA8·설계값 절차); Emery et al. (2017).

---

### ★ 일변동 검증 (일변동 / diurnal cycle)
- 무엇을 측정/검증하나: 시간대별(0~23시) 평균 농도·bias의 형태. 오존(오후 첨두)·NO2/PM(출퇴근 첨두)·야간 축적 등 배출·광화학·경계층(PBL) 혼합의 일주기를 모델이 재현하는지.
- 정의·수식: 시간대별 합성(composite) 평균 o(h), m(h) 및 시간대별 bias(h)=m(h)−o(h). 진폭(max−min)·위상(첨두시각) 오차 비교. 조화적합(1차 harmonic)으로 진폭·위상 정량화 가능(`06` 조화·분해 교차링크).
- 적용 도메인/자료형: O3·NO2·PM2.5·CO. [시계열]. 위성은 통과시각 고정이라 일변동 직접검증 불가(정지궤도 GEMS/TEMPO 예외).
- 입력·전제: 현지시각(LST) 정렬(UTC 혼용 주의). 충분한 일수. 계절별 분리(여름/겨울 일변동 상이).
- 해석 기준(advisory): 오존 야간 과대·오후 첨두 과소, NO2 첨두시각 지연 등이 전형적 오차 신호 — PBL 혼합·배출 시간분배·광화학 진단의 실마리. 절대선 없음, 계절·측정소유형 의존 경고 동반.
- 한계·주의(§G): 합성평균은 개별일 위상오차를 은폐(진폭 감쇠) → 개별일 위상 진단 병행. UTC/LST 정렬 오류가 위상오차로 오인됨.
- 출처: Seinfeld & Pandis (교과서, 광화학 일변동); Travis & Jacob (2019, *Atmospheric Chemistry and Physics*, 모델 일변동·PBL 편향 진단 사례).

---

### 주간주기·주말효과 검증 (주말효과 / weekly cycle, weekend effect)
- 무엇을 측정/검증하나: 요일별 농도 패턴(평일-주말 차이). NOx 배출 감소로 오존이 주말에 오히려 증가하는 "주말효과"를 모델이 재현하는지 → 오존 생성체제(NOx- vs VOC-limited) 진단.
- 정의·수식: 요일별 합성 평균, 평일·주말 그룹 평균차 및 유의성(t/부트스트랩, `01`). 주말/평일 비.
- 적용 도메인/자료형: O3·NO2·PM. [시계열].
- 입력·전제: 장기간(계절별 충분한 주말 수). 공휴일 처리 규칙. LST 정렬.
- 해석 기준(advisory): 주말효과 부호·크기 재현은 배출 요일분배·화학체제 정확도의 강한 진단 — 모델이 주말효과 부호를 틀리면 오존 감축전략 예측이 위험. 도시(체제)별로 부호가 달라 advisory.
- 한계·주의(§G): 표본 적으면 주말-평일 차 신뢰구간 큼. 배출 인벤토리의 요일 프로파일 가정에 결과가 좌우.
- 출처: Blanchard & Tanenbaum (2003, *J. Air & Waste Manage. Assoc.*, 주말효과); Jacob (1999) / Seinfeld & Pandis (오존 체제).

---

### 계절·월별 층화 검증 (계절 층화 / seasonal stratification)
- 무엇을 측정/검증하나: 계절·월별로 나눈 bias/NMB/NME 등의 변화. 여름 광화학(오존)·겨울 축적(PM)·황사/이류 등 계절 의존 오차 구조.
- 정의·수식: 공통 지표(`01`)를 계절/월 부분집합에 각각 적용 → 계절별 표. 계절 조화·이상치는 `06`.
- 적용 도메인/자료형: 전 화학종. [시계열]/[격자].
- 입력·전제: 각 계절 충분 표본. 특이 이벤트(황사·산불·정체) 라벨링 권장.
- 해석 기준(advisory): 여름 오존 과소·겨울 PM 과소(질산염·난방·역전층) 등 계절별 상반 편향이 흔함 → 연평균 단일 통계는 이를 상쇄해 은폐. 계절 분해가 필수 진단.
- 한계·주의(§G): 연통계만 보면 상쇄로 "양호"로 오판(§G-6). 이벤트(황사) 미제거 시 계절통계 왜곡.
- 출처: Emery et al. (2017, 계절 벤치마크 권고); 각국 CTM 평가 논문 관행.

---

### ★ 측정소 대표성 오차 (측정소 대표성 / station representativeness)
- 무엇을 측정/검증하나: 점 측정소 값과 모델 격자셀 평균값의 **공간 스케일 불일치**로 생기는 구조적 차이. 격자(수~수십 km)가 국지 오염원(도로변·굴뚝)을 평균화해 못 담는 문제.
- 정의·수식: 대표성 오차는 매치업 총오차 = 모델오차 ⊕ 관측오차 ⊕ 대표성오차의 한 성분. 삼중대조(TC/ETC, `12`)로 분리 시도 가능. 인접 관측 분산·반경 내 관측 변동으로 대표성 스케일 진단.
- 적용 도메인/자료형: 모든 화학종, 특히 NO2·1차 PM(공간 경사 급함). [시계열] vs [격자].
- 입력·전제: 측정소 메타데이터(유형·고도·주변 토지이용). 격자 해상도 명시. 도로변·산업 측정소는 광역격자와 원리상 불일치.
- 해석 기준(advisory): 도로변(traffic)·산업 측정소를 광역격자와 직접 비교하면 모델이 "과소"로 보이나 이는 대표성 문제이지 모델 결함이 아닐 수 있음 → 측정소 유형 층화(아래) 필수. 해상도가 높을수록 대표성 오차 감소.
- 한계·주의(§G): 대표성 오차를 모델오차로 오귀속 금지(§G-1 기준≠참값, 여기선 관측 대표성 한계). NO2는 특히 심함. 대표성 반경은 종·환경별 상이.
- 출처: Schutgens et al. (2016, *Atmospheric Chemistry and Physics* 16:6335, 대표성 오차·에어로졸); Janssen et al. (2008, *Atmospheric Environment*, 측정소 대표성 지도); FAIRMODE 대표성 지침.

---

### 측정소 유형·환경 층화 (urban/traffic/rural/background stratification)
- 무엇을 측정/검증하나: 측정소를 도시배경·교통(도로변)·산업·농촌/배경 등으로 분류해 각 그룹별 성능을 따로 평가. 국지 오염원 영향을 분리해 모델의 "광역 배경 재현력"과 "국지 표현력"을 구분.
- 정의·수식: 그룹별 공통 지표(`01`) 재계산·비교. 유럽 AirBase/EEA 분류, 국내 도시대기/도로변/배경 측정망 분류 활용.
- 적용 도메인/자료형: 전 화학종. [시계열].
- 입력·전제: 신뢰성 있는 측정소 분류 메타데이터. 격자 해상도와 측정소 대표 스케일의 정합.
- 해석 기준(advisory): 광역 CTM은 배경·농촌 측정소에서 양호, 도로변에서 과소가 일반적(대표성) — 유형 무시한 통합 통계는 오해 소지. 분류 자체가 국가·기관마다 달라 비교 시 규약 명시.
- 한계·주의(§G): 분류 오류·경계 사례. 도로변 측정소를 모델 검증에 쓸지 여부는 격자 해상도에 의존(고해상도만 의미).
- 출처: EEA AirBase/AQ e-Reporting 측정소 분류; FAIRMODE; Thunis et al. (2012, *Atmospheric Environment*, 측정소 유형·모델평가).

---

### ★ 위성 컬럼 매치업 — 대류권 NO2 (tropospheric NO2 column)
- 무엇을 측정/검증하나: 위성(OMI, TROPOMI, GEMS 등)이 산출한 대류권 NO2 연직컬럼(VCD, molec/cm²)을 모델 컬럼과 매치업해 배출·화학·수송을 광역 검증. 지상 NO2(농도)와는 물리량이 다름(컬럼 vs 표면농도).
- 정의·수식: 모델 3D NO2를 대류권 연직적분 → 위성 컬럼과 비교. bias·NMB·상관·회귀(`01`). **위성 평균화커널(AK) 적용** 후 비교가 원칙(아래 AK 카드). 위성 통과시각(OMI ~13:30, TROPOMI ~13:30, GEMS 정지궤도 주간 다중)에 모델 샘플링.
- 적용 도메인/자료형: 대류권 NO2 VCD. [트랙/타일] vs [격자→컬럼]. L2 swath 또는 L3 gridded.
- 입력·전제: 구름분율(cloud fraction) 필터, QA flag, 지형알베도·에어로졸 보정. 성층권 NO2 분리(대류권만). AMF(air mass factor) 가정 차이 인지. 통과시각·구름 샘플링을 모델에도 동일 적용.
- 해석 기준(advisory): 위성 NO2는 도시 상공 과소·배경 불확실 등 자체 편향이 큼 → "위성=참값" 금지(§G-1). 상대 공간패턴·시간추세(연도별 감축) 검증이 절대값보다 신뢰. 계절·구름조건 의존.
- 한계·주의(§G): AK 미적용 비교는 연직민감도 차이로 편향(§G-3). AMF·성층권 분리·구름 처리가 위성 오차의 주원. 컬럼-표면 물리량 혼동 금지.
- 출처: Boersma et al. (2011, *Atmospheric Measurement Techniques*, DOMINO NO2); van Geffen et al. (2020, *AMT*, TROPOMI NO2); Lamsal et al. (2021, *Atmos. Environ.*/OMI NO2 검증); GEMS: Kim et al. (2020, *Bulletin of the American Meteorological Society*, GEMS 정지궤도 대기질).

---

### ★ 위성 AOD 매치업 (에어로졸 광학두께 / aerosol optical depth, AOD/τ)
- 무엇을 측정/검증하나: 위성(MODIS, VIIRS, MISR, 정지 GK-2A/GOCI-II 등) AOD를 모델 산출 AOD(또는 지상 AERONET sun-photometer)와 매치업해 에어로졸 총량·광학특성을 검증.
- 정의·수식: 무차원 AOD τ(파장 명시, 통상 550nm). 모델 AOD는 에어로졸 질량·습도성장·광학모듈로 산출 → 위성/AERONET과 bias·상관·회귀·FAC2(위)·MFB/MFE. 파장 보정(Ångström 지수)으로 파장 정합.
- 적용 도메인/자료형: AOD [트랙/타일](위성 L2/L3) 및 [시계열](AERONET 지점) vs 모델 [격자].
- 입력·전제: 구름 마스크·지표반사(밝은 지표·사막·해빙 어려움) QC. 파장 통일. 위성 통과시각에 모델 샘플링. AERONET은 지점 sun-photometer(고신뢰, 대표성 제한).
- 해석 기준(advisory): AERONET 대비 위성 AOD의 기대오차(EE, 예 MODIS DT 육상 ±(0.05+0.15τ)) 안에 드는 비율(within-EE)로 위성 평가. 모델-AERONET은 로그공간·MFB 권장(에어로졸 로그정규). 지표·계절 의존 큼.
- 한계·주의(§G): AOD는 **연직적분 광학량** — 지상 PM2.5와 직접 등가 아님(경계층고·습도·연직분포 개입, 아래 카드). 밝은 지표·구름 가장자리 편향. AERONET 대표성.
- 출처: Levy et al. (2013, *AMT* 6:2989, MODIS Dark Target); Sayer et al. (2013, *JGR*, Deep Blue); Holben et al. (1998, *Remote Sensing of Environment*, AERONET); GOCI/GK-2A: Choi et al. (2018, *AMT*, GOCI YAER AOD).

---

### 평균화커널·연직민감도 적용 (평균화커널 / averaging kernel, AK)
- 무엇을 측정/검증하나: 위성 컬럼(NO2·CO·O3 등)은 고도별 민감도가 다르다. 위성 AK를 모델 프로파일에 적용해 "위성이 봤을 컬럼"으로 변환한 뒤 비교 — 위성·모델의 연직민감도 불일치 제거.
- 정의·수식: 변환컬럼 = Σ AKₖ · (모델 부분컬럼)ₖ (+ a priori 항). 위성 산출물이 제공하는 AK·a priori 프로파일 사용. 미적용 시 모델 참컬럼과 위성 산출컬럼을 부당비교.
- 적용 도메인/자료형: NO2·CO·HCHO·O3 등 위성 컬럼 검증의 전처리. [프로파일]/[트랙].
- 입력·전제: 위성 L2 AK·a priori·기압격자 제공. 모델 프로파일을 위성 연직격자로 보간. AMF 재계산 옵션(모델 프로파일로 AMF 갱신)도 존재.
- 해석 기준(advisory): AK 적용은 비교의 필수 정합단계 — 미적용 편향이 종·상황별로 수십% 발생 가능. AK가 없으면 그 한계를 명시하고 상대비교로 한정.
- 한계·주의(§G): AK/a priori는 위성 산출 가정 — 완전 제거 불가(§G-3 산출물 정합의 한계). 성층권-대류권 분리 규칙 일치 필요.
- 출처: Eskes & Boersma (2003, *Atmospheric Chemistry and Physics* 3:1285, "Averaging kernels for DOAS total column"); Boersma et al. (2016, *AMT*, NO2 AK 적용); TROPOMI/OMI product ATBD.

---

### AOD↔지상 PM 관계 검증 (AOD–PM2.5 relationship)
- 무엇을 측정/검증하나: 위성 AOD로 지상 PM2.5를 추정·검증할 때 두 물리량의 관계(경계층고 PBLH·상대습도 f(RH)·연직분포 개입)를 모델·관측으로 진단. 위성 대리검증의 타당성 점검.
- 정의·수식: PM2.5 ≈ AOD × (질량소광효율·PBLH·f(RH) 보정). 관계 회귀·잔차 분석, 계절·습도 층화 상관. 지상 PM–AOD 상관을 모델이 재현하는지.
- 적용 도메인/자료형: AOD [트랙] + PM2.5 [시계열] + PBLH/RH [격자]. 위성-지상 통합.
- 입력·전제: 동시 AOD·PM·기상. 습도성장·연직분포 가정 명시.
- 해석 기준(advisory): AOD–PM 상관은 습윤·정체 시 강하고 건조·상층 에어로졸(황사 상공 이류) 시 약함 — 관계의 계절·기상 의존을 모델이 재현하는지가 핵심. 절대 변환식은 지역보정 필수.
- 한계·주의(§G): AOD를 PM 대용으로 무비판 사용 금지(연직·습도 개입). 상층 이류 에어로졸이 지상 PM 없이 AOD만 높임.
- 출처: van Donkelaar et al. (2010, *Environmental Health Perspectives*, 위성 AOD→PM2.5); Zhang & Li (2015, *Remote Sensing of Environment*, AOD-PM 관계); Seinfeld & Pandis (f(RH)).

---

### ★ PM 화학종 분리 검증 (PM speciation: SO4²⁻/NO3⁻/NH4⁺/OC/EC/dust/sea-salt)
- 무엇을 측정/검증하나: PM2.5 총질량뿐 아니라 **성분별**로 모델 bias를 평가. 총질량이 맞아도 성분 상쇄(예: 황산염 과대 + 질산염 과소)로 우연히 맞을 수 있어, 성분 검증이 화학·배출 진단의 핵심.
- 정의·수식: 각 성분에 MFB/MFE·NMB/NME(위)·상관 적용. 성분합 vs 측정 총질량의 닫힘(아래 카드). 무기 이온·탄소(OC/EC)·먼지·해염 분류.
- 적용 도메인/자료형: PM2.5/PM10 성분. [시계열](성분측정망: 미국 IMPROVE/CSN, 국내 성분측정소) / [격자].
- 입력·전제: 성분 측정 프로토콜 일치(OC/EC 열광학법 IMPROVE vs NIOSH 차이 주의). 질산염 휘발손실(양성 아티팩트)·유기물 OM/OC 계수(1.4~2.1) 가정 명시. 반휘발성 성분(NH4NO3) 온도민감.
- 해석 기준(advisory): 질산염·유기탄소가 최난제(암모니아·이차유기 aerosol SOA 불확실) — 성분별 Boylan&Russell 목표/기준 달성도가 종별로 크게 다름(advisory). SO4가 상대적 양호가 일반적.
- 한계·주의(§G): 총질량 성능만 보고 결론 금지(§G-6 상쇄 은폐). OC/EC 측정법·OM/OC 계수·질산염 휘발이 대형 불확실원. 성분 미결정질량 처리규칙.
- 출처: Boylan & Russell (2006); Simon, Baker & Phillips (2012, *Atmospheric Environment* 61:124, "Compilation and interpretation of photochemical model performance statistics", 성분별 통계); IMPROVE/CSN 프로토콜.

---

### 질량 닫힘·재구성질량 (mass closure / reconstructed fine mass)
- 무엇을 측정/검증하나: 측정·모델 PM 성분합이 중량법 총질량과 닫히는지. 미결정질량(unidentified/other mass)·수분·유기물 계수의 정합.
- 정의·수식: 재구성질량 = SO4 + NO3 + NH4 + OM(=OC×계수) + EC + dust + sea-salt + (bound water). 총질량−재구성 = residual. 성분 기여율(%) 비교.
- 적용 도메인/자료형: PM2.5/PM10 [시계열]/[격자].
- 입력·전제: 모든 주요 성분 동시 측정/산출. OM/OC 계수·먼지 산화물 계수(예: dust=2.2×Fe 등) 가정 명시. 결합수 처리.
- 해석 기준(advisory): 잔차(미결정) 비율이 크면 성분 분류·계수 가정 재검토 신호. 계절(여름 SOA·겨울 질산염)로 기여구조 변화 — 모델이 기여율 구조를 맞추는지 진단.
- 한계·주의(§G): 계수·수분 가정이 닫힘을 좌우(임의 조정으로 억지 닫힘 금지). 측정·모델 성분 정의 불일치.
- 출처: Malm et al. (1994, *JGR*, IMPROVE reconstructed mass); Chow et al. (2015, *Aerosol and Air Quality Research*, mass closure 리뷰).

---

### 오존 전구물질·광화학 지표 (NOx, VOC, HCHO/NO2 비, OX)
- 무엇을 측정/검증하나: 오존 자체뿐 아니라 전구물질(NO2·NOx·VOC·HCHO)과 생성체제 지표를 검증해 "오존이 맞는 이유가 옳은지"를 진단. HCHO/NO2 비로 NOx-limited vs VOC-limited 체제 판별.
- 정의·수식: OX = O3 + NO2(광정상 보존량, 적정 아티팩트 완화). FNR = HCHO/NO2 컬럼비(위성/모델, 체제 임계 관행 ~1~2 경계). NO·NO2·NOx bias, VOC 종별 bias.
- 적용 도메인/자료형: 표면 [시계열] 및 위성 컬럼 HCHO/NO2 [트랙]. O3·NO2·VOC.
- 입력·전제: VOC 측정 희소(특정 캠페인 위주). 위성 HCHO 저신호·노이즈. OX는 NO 적정 효과 상쇄용.
- 해석 기준(advisory): 오존은 맞는데 FNR 체제가 틀리면 감축전략 예측이 위험 — 전구물질·체제 지표 동반검증이 정책 신뢰의 관건. 체제 임계는 지역·계절 의존이 커 advisory.
- 한계·주의(§G): 오존 단독 성능으로 화학 정합 판단 금지(§G-6). VOC 관측 부족으로 체제 검증 제약. 위성 FNR 임계 전이성 낮음.
- 출처: Duncan et al. (2010, *Atmospheric Environment*, HCHO/NO2 체제 지표); Sillman (1995, *JGR*, 광화학 지표); Seinfeld & Pandis (OX·적정).

---

### 입자 수농도·크기분포 검증 (number concentration / size distribution)
- 무엇을 측정/검증하나: 질량 외에 입자 수농도(CN/CCN)·크기분포(모드별 지름·기하표준편차)를 모델(에어로졸 미세물리: modal/sectional)과 관측(SMPS/APS)으로 비교. 신입자생성·응결·응집 과정 진단.
- 정의·수식: 로그정규 모드 파라미터(N, Dg, σg) 비교. 크기분포 dN/dlogDp 스펙트럼 매칭(로그공간 오차). 수농도는 로그정규 → 로그공간·MFB.
- 적용 도메인/자료형: [시계열](지상 SMPS/APS·항공 캠페인). 총 수농도·모드별.
- 입력·전제: 측정 크기범위·모델 모드 정합. 나노입자 측정 하한. 수농도는 초미세입자 지배(질량과 다른 정보).
- 해석 기준(advisory): 모델이 수농도를 크게 과소/과대(신입자생성·1차배출 수 배출계수 불확실)하는 경우 흔함 — 질량 성능과 별개. 관측 캠페인 의존.
- 한계·주의(§G): 질량 검증만으로 수농도 정합 보장 안 됨(§G-6). modal vs sectional 표현 차이. 측정 크기범위 절단.
- 출처: Seinfeld & Pandis (에어로졸 미세물리); Whitby (1978, *Atmospheric Environment*, 크기분포 모드); 캠페인별 평가 논문.

---

### ★ 분포·꼬리 비교 (QQ-plot / PDF / KS — 대기질 적용)
- 무엇을 측정/검증하나: 로그정규 농도의 **분포 형상과 고농도 꼬리**(고오염사건)를 모델이 재현하는지. 평균지표가 못 보는 꼬리 과소·과대. (QQ·PDF·KS 기초정의는 `01`·`03`.)
- 정의·수식: QQ = 정렬된 모델·관측 분위수 산점(로그축 권장). 상위 분위수(95/99%)에서 1:1선 이탈로 고농도 재현 판정. KS D=max|F_m−F_o|. Weibull/로그정규 적합 비교.
- 적용 도메인/자료형: PM·O3·NO2 분포 전반, 특히 고농도역. [시계열]/[격자]/[트랙].
- 입력·전제: 동일 기간 표본. 로그축 사용(선형은 꼬리 은폐). 자기상관 강함 → 유효표본 보정(KS 과민, `01`).
- 해석 기준(advisory): 상위 분위수 과소 = 고오염사건 재현 실패(규제·보건상 치명). QQ 기반 quantile mapping 보정(`13`)에도 사용. 계절 분리 권장.
- 한계·주의(§G): 자기상관으로 KS가 거의 항상 "유의" 판정(§G) → QQ 시각진단 우선. 분포만 비교(동시성 못 봄). 극단 분위수 불안정.
- 출처: Wilks (교과서); Jolliffe & Stephenson; 대기질 평가 관행(로그 QQ).

---

### ★ Taylor / Target 다이어그램 (대기질 다지점·다종 적용)
- 무엇을 측정/검증하나: 여러 측정소·화학종·모델을 상관·정규화표준편차·CRMSD(Taylor)와 bias·CRMSD(Target)로 한눈에 요약. (기초정의·작도는 `01`·`figures/16`.)
- 정의·수식: `01` 참조. 대기질에선 화학종별로 색/기호 구분, 정규화(관측 σ로) 후 다종 중첩. Target의 y축 bias 부호로 종별 과대/과소 즉시 판별.
- 적용 도메인/자료형: O3·PM·NO2 등 다종·다지점 종합. [시계열]/[격자].
- 입력·전제: 정렬된 매치업, 정규화 σ. 화학종 간 스케일 차 → 정규화 필수.
- 해석 기준(advisory): 관측점 근접=우수. Taylor는 bias 미표현 → Target·MFB 표 병행(대기질은 bias가 핵심). 측정소 유형 층화와 결합 권장.
- 한계·주의(§G): 단일 다이어그램 과신 금지 — MFB/NMB·초과사건과 병행(§G-6). 로그정규 자료는 로그변환 후 작도 고려.
- 출처: Taylor (2001, *JGR* 106(D7)); Jolliff et al. (2009, Target diagram); (공통 카드 `01` 참조).

---

### 소스-수용 기여 검증 (source apportionment vs receptor model)
- 무엇을 측정/검증하나: 모델의 소스 기여(배출부문별 tagging/DDM/brute-force)를 수용모델(PMF, CMB)의 관측기반 기여와 대조. "농도"뿐 아니라 "원인 배분"의 타당성 검증.
- 정의·수식: 부문별 기여율(%) 비교, 요인 프로파일 대응. 모델 감도(zero-out/DDM) vs PMF 요인·CMB 화학프로파일.
- 적용 도메인/자료형: PM 성분 기반. [시계열] 성분 + 모델 소스기여.
- 입력·전제: 성분 다종 동시측정(PMF). 소스 프로파일 라이브러리(CMB). 모델·수용모델 부문 정의 매핑.
- 해석 기준(advisory): 부문 기여 순위·크기 일치는 정책신뢰의 핵심. 두 접근의 부문 정의가 달라 완전 일대일 어려움 → 정성·순위 비교 중심(advisory).
- 한계·주의(§G): 수용모델도 가정·불확실성 있는 추정(§G-1 참값 아님). 요인-부문 매핑 임의성. 이차생성(SOA/질산염) 배분 난제.
- 출처: Paatero & Tapper (1994, *Environmetrics*, PMF); Watson et al. (2002, *Chemosphere*, CMB); US EPA PMF 가이드.

---

### ★ 확률·앙상블 대기질 예보 검증 (CRPS / Brier / ROC — ensemble AQ forecast)
- 무엇을 측정/검증하나: 앙상블·확률 대기질 예보(오존/PM 초과확률)의 신뢰도·해상도·예리함. 결정론 지표가 못 보는 불확실성 표현 품질. (CRPS·Brier·ROC·rank histogram 기초정의는 `03`·`figures/16`.)
- 정의·수식: `03` 참조. 대기질 적용: 특정 임계(주의보·기준) 초과확률에 Brier/BSS·ROC/AUC, 연속 농도에 CRPS/CRPSS, spread 적정성 rank histogram.
- 적용 도메인/자료형: 앙상블 O3·PM2.5(또는 초과확률) vs 측정소. [시계열]/[격자].
- 입력·전제: 앙상블 멤버/예보분포. 관측 결정론 진값. 충분한 사례·임계.
- 해석 기준(advisory): CRPS·BS 작을수록, CRPSS/BSS>0이면 기준(지속·기후) 대비 우수. 고오염 초과는 드문사건 → BS/ROC 불안정(신뢰구간). 계절·지역 의존.
- 한계·주의(§G): 결정론 단일모델 적용 불가. 드문 초과사건 점수 불안정(§G). reliability와 함께 해석.
- 출처: Hersbach (2000, CRPS); Jolliffe & Stephenson (Brier·ROC); Delle Monache et al. (2006, *Atmospheric Chemistry and Physics*, 앙상블 오존 예보); (공통 카드 `03`).

---

### 공간장 패턴·오차지도 (spatial map / FSS — 대기질 격자장)
- 무엇을 측정/검증하나: 모델 농도장의 공간 패턴(핫스팟 위치·경사)을 관측 내삽장·위성장과 비교. 격자 검증의 double penalty 완화(FSS 이웃검증). (패턴상관·FSS·SAL 기초는 `02`.)
- 정의·수식: `02` 참조. 대기질: 임계 초과 마스크에 FSS(이웃크기·임계 스캔), 핫스팟(도시·산업) 위치오차, 오차장 지도(bias(x,y)).
- 적용 도메인/자료형: PM·O3·NO2·AOD [격자] vs 위성/내삽 관측장.
- 입력·전제: 공통격자 재격자화(`15`), 관측 내삽장의 불확실성 인지. 위성장은 결측·구름 패턴.
- 해석 기준(advisory): 위치가 조금 어긋난 핫스팟은 격자별 지표에서 double penalty → FSS·객체기반(MODE, `02`)로 완화. 관측 내삽장 자체 불확실(참값 아님).
- 한계·주의(§G): 관측 내삽장을 참값처럼 신뢰 금지(§G-1). 위성 결측 패턴이 비교 편향. 재격자화 보존성.
- 출처: Roberts & Lean (2008, *Monthly Weather Review*, FSS); Wernli et al. (2008, SAL); (공통 카드 `02`).

---

### ★ 재분석 격자 대조 (CAMS / MERRA-2 gridded reanalysis difference)
- 무엇을 측정/검증하나: 우리 모델 [격자]를 대기질/에어로졸 재분석(CAMS global/regional, MERRA-2 aerosol, NAQFC 등)과 **공간 전면적**으로 비교해 bias/RMSE/상관의 지리분포·계절성을 지도화. 관측 희소 지역까지 패턴 진단.
- 정의·수식: 공통격자 재격자화(`15`) 후 격자별 시계열에 bias(x,y)/RMSE/R/NMB → 색지도. 영역·위도대 평균 병행. (격자-격자 비교 방법론은 `02`·`12`.)
- 적용 도메인/자료형: O3·PM2.5·AOD·NO2 [격자] vs [격자]. NetCDF↔NetCDF.
- 입력·전제: 시간축·격자·달력·단위 정렬, 마스크 통일. CAMS는 관측동화(위성·지상) 산물 → **독립 관측 아님**(오차 상관 주의). 해상도 차이.
- 해석 기준(advisory): 재분석과의 차이는 "모델오차"가 아니라 "모델−재분석 차이"(§G-1). 계통 bias 띠·계절성 위치 진단에 유용하되 재분석 자체 불확실성(동화 편향) 고려. 지상·위성 독립검증과 교차.
- 한계·주의(§G): 재분석 참값 과신 금지(§G-1). 우리 모델과 CAMS가 같은 배출/동화관측 공유 시 차이 과소평가(§G-2). 해상도·물리 차이가 차이의 상당부분.
- 출처: Inness et al. (2019, *Atmospheric Chemistry and Physics* 19:3515, "The CAMS reanalysis of atmospheric composition"); Randles et al. (2017, *Journal of Climate*, MERRA-2 aerosol reanalysis); (공통 §G).

---

### 침적·플럭스 검증 (wet / dry deposition flux)
- 무엇을 측정/검증하나: 습성(강수 세정)·건성 침적 플럭스와 강수 화학(pH·이온 농도)을 관측망(국내 산성강하물, 미국 NADP/CASTNET)과 비교. 질소·황 수지 닫힘.
- 정의·수식: 습성침적 = 강수량 × 강수농도 적산. 건성침적 = 침적속도 Vd × 농도. bias/NMB(`01`)·수지 비교. 침적 수지 닫힘은 `04` 교차.
- 적용 도메인/자료형: SO4·NO3·NH4 습성침적, 가스 건성침적 [시계열](주/월 적산).
- 입력·전제: 강수량 정확도(습성침적 지배인자). Vd 파라미터화 불확실. 관측망 희소·시간해상도(주적산).
- 해석 기준(advisory): 습성침적 오차는 강수 편향과 얽힘 → 강수(기상) 검증(`07`) 선행. 건성침적은 직접관측 희소로 검증 제약. 계절·강수형태 의존.
- 한계·주의(§G): 습성침적 오차를 화학오차로 오귀속 금지(강수량 개입, §G). 건성 Vd 관측 부족. 수지 닫힘(`04`)과 함께 해석.
- 출처: NADP/NTN·CASTNET 프로토콜; Wesely (1989, *Atmospheric Environment*, 건성침적 저항모형); Seinfeld & Pandis (침적).

---

### ★ 운영·규제 검증 프레임워크 (FAIRMODE MQI / EPA modeling guidance)
- 무엇을 측정/검증하나: 대기질 모델을 관측 불확실성 대비 상대평가하는 표준 절차. FAIRMODE의 **모델품질지표(MQI)·목표(MQO)** 와 미국 EPA modeling guidance가 대표. 검증의 "표준화" 자체.
- 정의·수식: FAIRMODE MQI = |m−o| / (β·U(o)) 형태(관측 불확실성 U로 정규화, β=2 관행), MQI ≤ 1이면 목표 충족. 관측 측정불확실성 U(o)를 명시적으로 넣는 게 특징(순수 오차 대신 "불확실성 대비"). EPA는 NMB/NME·MFB/MFE 벤치마크(Emery/Boylan) 기반.
- 적용 도메인/자료형: O3·PM2.5·PM10·NO2 규제 평가. [시계열] 측정소.
- 입력·전제: 측정소 자료·측정 불확실성 계수(종별 규정). 대표성·완전성(데이터 커버리지) 기준. 공통 매치업 규약.
- 해석 기준(advisory): MQI≤1은 "목표 충족"이나 이 역시 **불확실성 계수·β 가정에 의존하는 참고선**(advisory, §G-4). EPA 벤치마크도 미국 사례 기반 전이성 한계. 지역 규정(국내 대기질 예보 평가 절차) 확인.
- 한계·주의(§G): MQI가 관측 불확실성 U에 민감(U 과대=쉬운 통과). pass/fail 오용 금지(§G-4). 프레임워크 규약(β·U·완전성) 반드시 명시.
- 출처: Thunis et al. (2012, *Atmospheric Environment* 57:96, "Performance criteria to evaluate air quality modeling applications"); Janssen & Thunis (2022, *FAIRMODE Guidance Document on Modelling Quality Objectives and Benchmarking*, JRC — 확인요: 최신판 버전 재확인); US EPA (2018, *Modeling Guidance*).

---

## 출처 (References)

### 표준 참고문헌 / 교과서·지침 (실제 존재)
- Seinfeld, J. H. & Pandis, S. N. *Atmospheric Chemistry and Physics: From Air Pollution to Climate Change*, Wiley (농도 분포·광화학·에어로졸·침적 — 표준 교과서).
- Jacob, D. J. (1999) *Introduction to Atmospheric Chemistry*, Princeton University Press (오존 화학체제).
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (bias·RMSE·QQ·KS·회귀 표준정의 — 공통 `01`).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide*, Wiley (범주형·Brier·ROC — 공통 `03`).
- US EPA (2018) *Modeling Guidance for Demonstrating Air Quality Goals for Ozone, PM2.5, and Regional Haze* (MDA8·설계값·벤치마크 절차).

### 핵심 성능기준 논문 (웹으로 제목·저널·연도 확인됨)
- Boylan, J. W. & Russell, A. G. (2006) "PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models," *Atmospheric Environment*, 40(26), 4946–4959. (MFB/MFE 목표·기준)
- Emery, C., Liu, Z., Russell, A. G., Odman, M. T., Yarwood, G. & Kumar, N. (2017) "Recommendations on statistics and benchmarks to assess photochemical model performance," *Journal of the Air & Waste Management Association*, 67(5), 582–598. (doi:10.1080/10962247.2016.1265027) (O3·PM NMB/NME/r 벤치마크)
- Chang, J. C. & Hanna, S. R. (2004) "Air quality model performance evaluation," *Meteorology and Atmospheric Physics*, 87(1–3), 167–196. (doi:10.1007/s00703-003-0070-7) (FB·NMSE·FAC2·MG·VG)
- Simon, H., Baker, K. R. & Phillips, S. (2012) "Compilation and interpretation of photochemical model performance statistics published between 2006 and 2012," *Atmospheric Environment*, 61, 124–139. (성분별 성능통계)
- Thunis, P., Georgieva, E. & Pederzoli, A. (2012) "A tool to evaluate air quality model performances in regulatory applications," *Environmental Modelling & Software* / Thunis et al. (2012, *Atmospheric Environment* 57:96) (FAIRMODE MQI/MQO — 정확한 저널·권 인용 전 재확인, 확인요).

### 위성·원격탐사 (웹/문헌 확인)
- Levy, R. C. et al. (2013) "The Collection 6 MODIS aerosol products over land and ocean," *Atmospheric Measurement Techniques*, 6, 2989–3034. (MODIS Dark Target AOD)
- Sayer, A. M. et al. (2013) "Validation and uncertainty estimates for MODIS Collection 6 Deep Blue aerosol data," *Journal of Geophysical Research: Atmospheres*, 118. (Deep Blue AOD)
- Holben, B. N. et al. (1998) "AERONET—A federated instrument network and data archive for aerosol characterization," *Remote Sensing of Environment*, 66(1), 1–16. (AERONET)
- Boersma, K. F. et al. (2011) "An improved tropospheric NO2 column retrieval algorithm for OMI," *Atmospheric Measurement Techniques*, 4, 1905–1928. (DOMINO NO2)
- van Geffen, J. et al. (2020) "S5P TROPOMI NO2 slant column retrieval," *Atmospheric Measurement Techniques*, 13. (TROPOMI NO2)
- Eskes, H. J. & Boersma, K. F. (2003) "Averaging kernels for DOAS total-column satellite retrievals," *Atmospheric Chemistry and Physics*, 3, 1285–1291. (평균화커널)
- van Donkelaar, A. et al. (2010) "Global estimates of ambient fine particulate matter concentrations from satellite-based aerosol optical depth," *Environmental Health Perspectives*, 118(6). (AOD→PM2.5)
- Kim, J. et al. (2020) "New era of air quality monitoring from space: Geostationary Environment Monitoring Spectrometer (GEMS)," *Bulletin of the American Meteorological Society*, 101(1), E1–E22. (GEMS 정지궤도)
- Choi, M. et al. (2018) "GOCI Yonsei aerosol retrieval version 2 products," *Atmospheric Measurement Techniques*, 11. (GOCI/GK 정지궤도 AOD — 확인요: 정확한 권·페이지)

### 진단·과정 논문 (제목·저널 확인)
- Schutgens, N. A. J. et al. (2016) "On the spatio-temporal representativeness of observations," *Atmospheric Chemistry and Physics*, 16, 6335–6353. (대표성 오차)
- Duncan, B. N. et al. (2010) "Application of OMI observations to a space-based indicator of NOx and VOC controls on surface ozone formation," *Atmospheric Environment*, 44(18). (HCHO/NO2 체제 지표)
- Sillman, S. (1995) "The use of NOy, H2O2, and HNO3 as indicators for ozone-NOx-hydrocarbon sensitivity," *Journal of Geophysical Research*, 100(D7). (광화학 지표)
- Blanchard, C. L. & Tanenbaum, S. J. (2003) "Differences between weekday and weekend air pollutant levels," *Journal of the Air & Waste Management Association*, 53(7). (주말효과)
- Malm, W. C. et al. (1994) "Spatial and seasonal trends in particle concentration and optical extinction," *Journal of Geophysical Research*, 99(D1). (IMPROVE reconstructed mass)
- Wesely, M. L. (1989) "Parameterization of surface resistances to gaseous dry deposition," *Atmospheric Environment*, 23(6). (건성침적)
- Inness, A. et al. (2019) "The CAMS reanalysis of atmospheric composition," *Atmospheric Chemistry and Physics*, 19, 3515–3556. (CAMS 재분석)
- Randles, C. A. et al. (2017) "The MERRA-2 aerosol reanalysis, 1980 onward," *Journal of Climate*, 30. (MERRA-2 aerosol)
- Delle Monache, L. et al. (2006) "Ensemble forecasts of surface ozone," *Atmospheric Chemistry and Physics*. (앙상블 오존 — 확인요: 권·페이지)
- Paatero, P. & Tapper, U. (1994) "Positive matrix factorization," *Environmetrics*, 5(2). (PMF)

### 웹 자료 (조사 시 직접 참조)
- FAIRMODE (Forum for Air Quality Modelling in Europe) — MQI/MQO·벤치마킹 도구: https://fairmode.jrc.ec.europa.eu/
- US EPA — Air Quality Modeling / SIP Modeling Guidance: https://www.epa.gov/scram
- CF Standard Name Table (대기화학 종): https://cfconventions.org/standard-names.html

### 확인요 (웹에서 1차 확인 못 했거나 재확인 필요 항목)
- Thunis et al. (2012) — FAIRMODE MQI 관련 논문이 *Atmospheric Environment* 57:96("Performance criteria...")과 *Environmental Modelling & Software*(도구 논문)로 나뉘어 인용됨. 인용 전 대상 논문 특정·권·페이지 재확인.
- Janssen & Thunis, *FAIRMODE Guidance Document on MQO and Benchmarking* — JRC 기술문서로 판번호가 갱신됨(최신판 버전·연도 재확인).
- Choi et al. (2018) GOCI YAER·Delle Monache et al. (2006) — 저널 권·페이지 원문 재확인.
- Emery(2017) PM2.5 성분별 정확한 NMB/NME 목표·기준 수치는 원문 표에서 확인 후 인용(본 카드는 오존 수치만 구체화, PM은 "오존보다 느슨·종별 상이"로 정성 기술).
- 국내(한국) 대기질 예보 평가 절차·측정소 분류 규정은 환경부/국립환경과학원 최신 지침 확인 필요.

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(검색으로 확인된 제목·저널·연도 기재, DOI는 확인된 것만 표기, 임의 생성 금지). 성능 목표·기준(Boylan&Russell·Emery·Chang&Hanna·FAIRMODE)은 모두 **advisory 참고선**이며 pass/fail 시험이 아니다(§G-4). 재분석·위성은 참값이 아니라 기준이다(§G-1).
