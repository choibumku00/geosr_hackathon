# 도메인: 해양 생지화학·해색 (Ocean Biogeochemistry & Ocean Colour) 검증·분석 방법 카탈로그

이 문서는 해양 생지화학(BGC) 모델·지구시스템모델(ESM)의 생지화학 컴포넌트(예: PISCES, MOM6-COBALT, MEDUSA, BLING, HAMOCC, TOPAZ)와 위성 해색(ocean colour) 산출물의 결과를 **정점(관측소)·시계열 자료**(BATS·HOT·CARIACO·유럽 정점, BGC-Argo 프로파일), **격자·재분석 기후값**(World Ocean Atlas, GLODAPv2 격자, CMEMS BGC 재분석), **위성 트랙/L3·L4**(해색 Chl-a, PIC, Kd) 자료와 대조·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다.

해양 생지화학 검증의 핵심 특성은 다른 해양 도메인과 다르다: (1) **로그정규분포 변수** — 엽록소 Chl-a·영양염은 수 자릿수(orders of magnitude)에 걸쳐 분포하므로 log10 변환 후 통계를 내는 것이 표준이다(Campbell 1995). (2) **탄산계(carbonate system)의 내부 정합성** — pH·pCO2·DIC·전알칼리도(TA)는 열역학적으로 서로 유도되므로 어느 두 변수를 입력했는지, 어느 pH 스케일(total/free/seawater)·어느 상수(K1,K2) 조를 썼는지가 결정적이다. (3) **관측 자료 자체가 이질적** — 해색 위성(Bailey–Werdell 매치업 프로토콜), 선박 병 시료(GLODAP·SOCAT), 자율 플랫폼(BGC-Argo)이 서로 정확도·대표성·오차구조가 다르다. (4) **표층 vs 심층·계절주기** — 표층은 위성·계절 blooming, 심층은 산소최소층(OMZ)·재광물화(remineralization)·심층 영양염이 지배하므로 검증 축을 나눠야 한다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석/기후값), [정점]=관측정점 시계열(BATS·HOT 등 CSV), [프로파일]=BGC-Argo·CTD-로제트 깊이별 프로파일, [트랙/L2]=위성 along-track/L2, [L3/L4]=합성·보간 위성 격자, [병시료]=선박 이산 시료(GLODAP·SOCAT).
> **"우리 모델 vs 관측/재분석/위성" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 지표(RMSE·MAE·bias·상관·Taylor·QQ·bootstrap·KS·회귀 등)는 여기서 재정의하지 않고** `01_error_statistics.md`, `03_categorical_event_extremes.md`, `05_spectral_eof_modal.md`, `06_timeseries_signal.md`, `12_satellite_remote_sensing.md`, `15_preprocessing_regridding_colocation.md`, figures/16(진단 그림 카탈로그)로 **교차링크**만 한다. 이 카드는 생지화학 고유의 적용·전제·해석·함정에 집중한다.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **엽록소 로그통계 검증 (Chl-a log10 statistics)** — log10 변환 후 bias/RMSE/상관(생지화학 1차 표준)
- ★ **해색 매치업 프로토콜 (Bailey–Werdell / Zibordi 매치업)** — 3×3 윈도우·QC·시공간 임계
- **로그정규분포 진단 (log-normal / Campbell 통계)** — 기하평균·기하표준편차·분포 검정
- ★ **해색 밴드비·불확실성 지표 (band-ratio·MdSA·slope·win% 등)** — 해색 전용 성능지표
- **위성 vs 모델 표층 Chl-a 공간 검증 (gridded Chl map)** — L3/L4 대 모델 격자 편차지도
- **엽록소 계절주기·개화 시점 검증 (seasonal cycle·bloom phenology)** — 진폭·위상·개화 개시일
- ★ **용존산소 검증 (dissolved O2: WOA·BGC-Argo)** — 표층/심층·AOU·포화도
- ★ **산소최소층 진단 (OMZ: 등치면 부피·수심·수평범위)** — 저산소 임계 부피·OMZ 두께
- **겉보기산소이용률 AOU (Apparent Oxygen Utilization)** — 재광물화·환기 진단
- ★ **영양염 검증 (질산·인산·규산: WOA·GLODAP)** — 표층 고갈·심층 재생·Redfield 비
- **영양염 프로파일·약층 심도 검증 (nutricline depth)** — 질산선 수심·수직구배
- ★ **탄산계 내부정합 검증 (carbonate system closure: CO2SYS)** — 2변수 입력·유도변수 잔차
- ★ **표층 pCO2 검증 (SOCAT 매치업)** — ΔpCO2·해–기 플럭스·계절진폭
- ★ **pH 검증 (total scale) 및 산성화 추세** — pH bias·연 추세·플랫폼 편향
- **전알칼리도 검증 (Total Alkalinity: TA–SSS 관계)** — TA-염분 회귀·GLODAP 대조
- **용존무기탄소 DIC 검증 (GLODAP)** — 표층/심층 DIC·인위탄소(Cant)
- ★ **아라고나이트/칼사이트 포화도 Ω 검증** — Ω_ar·포화수심(saturation horizon)
- ★ **BGC-Argo 매치업·플랫폼 오차 (float–ship crossover)** — 프로파일 콜로케이션·QC·보정
- ★ **순1차생산 NPP 검증 (VGPM·CbPM·14C 정점)** — 위성/모델 NPP·적분생산량
- **수출생산·POC 플럭스 검증 (export / e-ratio·sediment trap)** — 침강플럭스·f-ratio
- **식물플랑크톤 기능형군 PFT 검증 (size class·HPLC pigment)** — micro/nano/pico 분율
- **투광층·Kd(490)·투명도 검증 (euphotic depth·diffuse attenuation)** — 빛환경 진단
- **적분·재고량 검증 (depth-integrated Chl / nutrient inventory / OHC-유사 탄소재고)** — 연직적분·수지
- ★ **연직 프로파일·단면 비교 (profile·section: 심층구조)** — 깊이별 bias·등치선 단면
- ★ **생지화학 모델 스킬 종합틀 (Stow 2009 / target·Taylor·cost function)** — 다변수 스킬 요약
- **기후값 격자-격자 공간비교 (WOA/GLODAP 대조 맵)** — 연·계절 기후 편차·위도-깊이 단면
- **로그공간 분포·꼬리 비교 (PDF/CDF·QQ, log축)** — 저농도/고농도 꼬리 진단
- **경보·임계 사건 검증 (녹조/저산소/저Ω 임계 초과)** — HAB·hypoxia·corrosive 사건 POD/FAR
- **불확실성·대표성 오차 (관측 불확실성 대비 상대평가)** — 관측 오차 예산·대표성

---

### ★ 엽록소 로그통계 검증 (엽록소 / Chlorophyll-a, log10 statistics)
- 무엇을 측정/검증하나: 모델·위성이 산출한 표층 엽록소 농도(Chl-a, mg m⁻³)가 관측(위성 L3/L4·정점·HPLC)과 일치하는지. 생지화학 검증의 가장 기본이자 1차 지표.
- 정의·수식: Chl-a는 수 자릿수에 걸친 **로그정규(log-normal)** 분포이므로 통계는 **log10 변환 후** 계산이 표준. 검증량은 대개 log10 공간에서 bias Δ = mean(log₁₀M − log₁₀O), RMSD = √mean[(log₁₀M − log₁₀O)²], 상관 R(log₁₀). 선형공간으로 되돌린 지표: median symmetric accuracy MdSA = 100·(10^(median|log₁₀(M/O)|) − 1) %, 기하평균 편향비 = 10^(mean(log₁₀(M/O))). RMSE·상관·회귀의 정의 자체는 §01, QQ는 §03/figures/16 참조.
- 적용 도메인/자료형: [L3/L4] 위성 Chl vs [격자] 모델; [정점]·HPLC vs 위성/모델. CF: `mass_concentration_of_chlorophyll_in_sea_water`, `mass_concentration_of_chlorophyll_a_in_sea_water`.
- 입력·전제: **log10 변환 필수**(선형공간 RMSE는 고농도 연안값이 지배해 오해 유발). 위성-in situ 매치업은 아래 Bailey–Werdell 카드의 QC 통과분만 사용. 정점 자료는 형광(fluorometric) vs HPLC 방식 차이 명시. 결측(구름)·저광 고위도 겨울 마스크.
- 해석 기준(advisory): 전지구 외해(Case-1) 위성 Chl의 목표 불확실성은 관행적으로 **±35%(0.35 in log₁₀ 근방)** 수준으로 논의되나, 이는 **해역·수형(Case-1/Case-2 연안)·계절·센서·알고리즘 의존**이며 절대 합격선이 아니다. 연안·고탁도·극지·저광 환경은 오차가 크게 증가 → 단정 금지, 영역·계절 분리 보고.
- 한계·주의(§G): 선형 vs 로그 지표 혼용 시 결론이 뒤집힘(반드시 공간 명시). 위성 Chl 자체가 알고리즘 산물(진값 아님) → "모델 오차"가 아니라 "모델−위성 차이". 연안 Case-2에서 위성 과대·과소 심함. §G-1·G-4 준수.
- 출처: Campbell (1995, JGR Oceans 100(C7):13237–13254, "The lognormal distribution as a model for bio-optical variability in the sea"); Bailey & Werdell (2006, Remote Sensing of Environment 102(1–2):12–23); Seegers et al. (2018, Optics Express 26(6):7404–7422, "Performance metrics for the assessment of satellite data products", MdSA 제안); NASA OBPG ocean colour validation practice.

---

### ★ 해색 매치업 프로토콜 (Bailey–Werdell / Zibordi 매치업)
- 무엇을 측정/검증하나: 위성 해색 산출물(Chl-a, Rrs, Kd 등)을 현장(in situ) 관측과 짝지어 검증하기 위한 **표준 시공간 매치업·품질관리(QC) 절차**. 위성 해색 검증의 절차적 표준.
- 정의·수식: in situ 지점 중심 **3×3 화소 윈도우** 추출 → (1) 유효화소 ≥ 50% 조건, (2) 중앙값 ±1.5σ 벗어난 화소 제외(필터링 평균), (3) 남은 화소 변동계수 CV = σ/mean ≤ 0.15(균질성)일 때만 채택, (4) 시간차 ≤ ±3~6시간(관행), (5) 태양천정각·관측각·플래그(구름·글린트·연안) QC. Rrs·Chl 각각에 bias·MdSA·slope·R(log) 산출. Zibordi 계열(AERONET-OC)은 고정 정점 초분광 관측으로 밴드별 Rrs 검증을 정형화.
- 적용 도메인/자료형: [트랙/L2]·[L3] 위성 해색 vs [정점]·HPLC·초분광 부이. §12(위성 매치업)·§15(콜로케이션) 코어 공유.
- 입력·전제: 위성·현장 자료의 대기보정·밴드 매칭·단위 통일. 현장 자료의 QC 등급(예: NOMAD·SeaBASS 등급). 연안(≤ ~1화소) 육지·저면반사 오염 제거.
- 해석 기준(advisory): 채택 매치업 수·공간 CV를 함께 보고. 매치업이 적으면(특히 극지·연안) 통계 불안정 → 신뢰구간(bootstrap, §01) 동반. 임계(50%·1.5σ·CV0.15)는 **관행값이며 센서·해역별 조정** 필요.
- 한계·주의(§G): 매치업 규약(윈도우·시간창·QC)이 다르면 결과가 크게 달라져 기관 간 비교 왜곡 → 규약 명시 필수. 3×3 윈도우 대표성 오차(점 vs ~km²). 대기보정 실패가 저Chl 외해에서 과대편향 유발.
- 출처: Bailey & Werdell (2006, RSE 102(1–2):12–23, "A multi-sensor approach for the on-orbit validation of ocean color satellite data products"); Zibordi, Mélin & Berthon (계열, IEEE TGRS / AERONET-OC 검증 프로토콜); Valente et al. (2022, ESSD 14:5737, 전지구 bio-optical in situ 컴파일 v3 — 매치업 DB 출처).

---

### 로그정규분포 진단 (log-normal / Campbell 통계)
- 무엇을 측정/검증하나: Chl-a·영양염 등 로그정규 변수의 **분포 형상(기하평균·기하표준편차·왜도)** 을 모델·관측 간 비교. 단순 산술평균이 왜곡되는 변수의 분포 재현성 진단.
- 정의·수식: 기하평균 GM = 10^(mean(log₁₀x)), 기하표준편차 GSD = 10^(std(log₁₀x)). log₁₀x의 정규성 검정(Shapiro–Wilk/Anderson–Darling, §03). 분포 비교는 log축 PDF/CDF·KS(§03)·QQ(figures/16).
- 적용 도메인/자료형: [격자]·[정점]·[L3] Chl-a·`mole_concentration_of_nitrate_in_sea_water` 등. 기후·장기 통계.
- 입력·전제: 0·음수·결측 처리(log 전 하한값 clip 또는 제거). 이질 수괴 혼합 시 로그정규 가정 약화(수괴별 분리 권장, Campbell 1995).
- 해석 기준(advisory): GM·GSD를 산술평균 대신 대표값으로 보고. 모델이 저농도 외해를 과대(분포 왼쪽 꼬리 부족)하는지, 고농도 개화를 과소하는지 분포로 진단.
- 한계·주의(§G): 산술평균 편차만 보면 로그정규 변수의 성능을 오판. 표본 자기상관 시 정규성·KS 과민(§G-6, 유효표본 보정).
- 출처: Campbell (1995, JGR Oceans 100(C7):13237–13254); Wilks(교과서, 분포 검정 — §01/03 공통).

---

### ★ 해색 밴드비·불확실성 지표 (band-ratio / MdSA·slope·bias·win%)
- 무엇을 측정/검증하나: 해색 알고리즘·모델 Chl의 성능을 **로그정규에 적합한 전용 지표**로 정량화(대칭성·저항성 강조). 일반 RMSE의 편중을 보완.
- 정의·수식: median symmetric accuracy MdSA = 100·(10^(median|log₁₀(M/O)|) − 1); 기하 bias(대칭 %) = sign·100·(10^(median(log₁₀(M/O))) − 1); log-space slope/intercept(Type-II/직교회귀 권장, §01); winning percentage(어느 알고리즘이 더 근접한 매치업 비율). 표준 밴드비 알고리즘 계열(OC4/OC5/OC6, OCI/Hu 3-band)의 산출값을 대상변수로 함.
- 적용 도메인/자료형: [트랙/L2]·[L3] Chl·Rrs. 알고리즘·센서·모델 간 상호비교.
- 입력·전제: log10 공간. 매치업 QC 통과분. 저Chl(<0.1)·고Chl(>1) 영역 분리 보고(밴드비는 저농도에서 잡음 큼).
- 해석 기준(advisory): MdSA는 이상치에 강건(중앙값 기반)해 평균 RMSE보다 안정. 값은 해역·센서·수형 의존 → 절대기준 아님.
- 한계·주의(§G): 밴드비 알고리즘은 CDOM·부유퇴적물 많은 Case-2에서 실패. slope를 OLS로 뽑으면 회귀희석 편향 → Type-II 회귀 권장.
- 출처: Seegers et al. (2018, Optics Express 26(6):7404–7422, MdSA 등 성능지표); O'Reilly & Werdell (2019, RSE, OC4/5/6 알고리즘); Hu, Lee & Franz (2012, JGR Oceans 117:C01011, doi:10.1029/2011JC007395, 3-band OCI); NASA OBPG "Performance metrics" 노트(oceancolor.gsfc.nasa.gov).

---

### 위성 vs 모델 표층 Chl-a 공간 검증 (gridded Chl map difference)
- 무엇을 측정/검증하나: 모델 표층 Chl [격자]를 위성 [L3/L4] 기후값·월합성과 **공간 전면적으로** 비교해 log-bias·RMSD·상관의 지리 분포를 지도화. 정점이 없는 해역의 계통편차 위치 진단.
- 정의·수식: 공통 격자 재격자화(§15) 후 각 격자점에서 log10 bias(x,y)·RMSD(x,y)·R(x,y)·MdSA(x,y) 산출 → 색지도. 위도대·해역(외해/연안/극지·부영양대) 평균 병행. 패턴상관·Taylor는 §01/02·figures/16.
- 적용 도메인/자료형: [격자] 모델 Chl vs [L3/L4] OC-CCI·GlobColour·MODIS·VIIRS·OLCI.
- 입력·전제: **동일 기간·동일 정의**(위성 표층 광학심도 가중 vs 모델 최상층·연직적분 차이 주의), log 변환, 구름·극야 마스크 통일. 위성 L4는 이미 보간·병합 산물(§G-3).
- 해석 기준(advisory): 적도용승대·서안경계류·극지 개화의 위치·강도 편차 진단. 모델은 흔히 연안 개화 과대, 외해 빈영양 과소 경향(사례적 관찰).
- 한계·주의(§G): 위성 Chl은 표층 ~1 광학심도 신호, 모델은 격자층 평균 → 대표성 차이. 위성 L4를 "정답"으로 과신 금지(§G-1). 연안 Case-2 오차.
- 출처: Sathyendranath et al. (OC-CCI, ESA Ocean Colour CCI 산출물 문서); NASA OBPG; Gregg & Casey (2004, RSE, 전지구 위성-모델 Chl 비교 관행).

---

### 엽록소 계절주기·개화 시점 검증 (seasonal cycle / bloom phenology)
- 무엇을 측정/검증하나: Chl의 **계절 진폭·위상·개화 개시(bloom onset)·최성기(peak)·기간**을 모델이 위성과 일치시키는지. 평균 통계가 못 보는 시간구조 검증.
- 정의·수식: 월기후값 곡선 비교(진폭·최대월). 개화 개시일: 임계법(중앙값+5% 등)·누적법·변곡점법. 위상오차는 순환(월) 시차. 조화적합(연·반년 성분, §05/06)로 진폭·위상 추출.
- 적용 도메인/자료형: [L3/L4]·[정점]·[격자] Chl 시계열. 온대(춘계 개화)·아열대(연1회 겨울)·극지(짧은 여름) 체제별.
- 입력·전제: 다년 평균으로 노이즈 저감. 결측(극야·구름) 보간법 명시(개화 개시 추정에 민감). 위성·모델 동일 임계·동일 정의.
- 해석 기준(advisory): 개시일 오차 수주(week) 이내면 양호로 논의되나 **체제·정의·결측 의존**. 모델의 개화 조기/지연은 혼합층·성층·광 커플링 문제 신호.
- 한계·주의(§G): 개화 개시 정의(임계/누적/변곡)마다 값이 달라짐 → 정의 명시. 극야 결측이 고위도 개시 추정 왜곡.
- 출처: Racault et al. (2012, Ecological Indicators, phytoplankton phenology from ocean colour); Siegel et al. (2002, Science 296:730–733, "The North Atlantic spring phytoplankton bloom and Sverdrup's critical depth"); Cole, Henson et al. (개화 phenology 검증 관행).

---

### ★ 용존산소 검증 (dissolved O2: WOA·BGC-Argo·GLODAP)
- 무엇을 측정/검증하나: 모델 용존산소가 표층(환기·용해도)·심층(재광물화·순환)에서 관측 기후값(WOA)·프로파일(BGC-Argo·GLODAP)과 일치하는지. 생지화학·물리 커플링의 통합 진단자.
- 정의·수식: 표층/심층·수심대별 bias·RMSE(§01, μmol kg⁻¹ 또는 mL L⁻¹ 단위 통일). 포화도 O2sat = O2/O2eq(T,S)·100%(Garcia–Gordon 용해도). AOU는 아래 별도 카드. 연직 단면 bias(위도-깊이)로 심층 구조 진단.
- 적용 도메인/자료형: [격자] 모델 vs [격자] WOA / [프로파일] BGC-Argo·[병시료] GLODAP. CF: `mole_concentration_of_dissolved_molecular_oxygen_in_sea_water`, `mass_concentration_of_oxygen_in_sea_water`.
- 입력·전제: **단위·기준 통일**(μmol kg⁻¹ vs μmol L⁻¹ vs mL L⁻¹ — 밀도 환산 필요). BGC-Argo O2 센서 드리프트·대기 재보정(air-calibration) 여부 확인. 심층은 밀도면/등압면 비교가 유리(등수심 비교는 약층 이동에 민감).
- 해석 기준(advisory): 표층은 용해도가 지배해 bias 작음이 흔함. **심층·OMZ는 모델 편차가 크고 부호가 해역 의존**(대서양 OMZ 과대, 인도양 과소 등 CMIP 공통 편차 보고) → 절대기준 없이 해역·수심대 분리 보고.
- 한계·주의(§G): 등수심 vs 등밀도 비교 선택이 결론 좌우. WOA는 보간 기후값(§G-3). 센서 O2와 병 시료(Winkler) 기준 차이. §G-1·G-4.
- 출처: Garcia & Gordon (1992, Limnology & Oceanography 37(6):1307–1312, O2 용해도); Garcia et al. (World Ocean Atlas Vol.3 Dissolved Oxygen, NOAA Atlas NESDIS); Olsen et al. (2016, ESSD 8:297–323, GLODAPv2); Oschlies et al. (2018, Nature Geoscience 11:467–473, "Drivers and mechanisms of ocean deoxygenation"); Cabré et al. (2015, Biogeosciences, CMIP5 OMZ 편차).

---

### ★ 산소최소층 진단 (OMZ: 저산소 등치면 부피·수심·수평범위)
- 무엇을 측정/검증하나: 모델이 산소최소층(OMZ)의 **강도·부피·수직 범위·수평 위치**를 관측과 일치시키는지. 저산소는 생태·탈질·N2O 배출의 핵심 → 생지화학 모델의 난제.
- 정의·수식: 저산소 임계(예: O2 < 60·20·5 μmol kg⁻¹, suboxic·hypoxic 기준 명시)로 등치면(iso-surface) 정의 → **저산소 수체 부피(∫∫∫ 1[O2<θ] dV)**, OMZ 상·하 경계 수심(iso-oxygen depth), 최소 O2 값·수심, OMZ 코어 위치. 관측(WOA·GLODAP·BGC-Argo)과 부피·수심·면적 비교.
- 적용 도메인/자료형: [격자] 모델 vs [격자] WOA·[프로파일] BGC-Argo. 동태평양·아라비아해·벵골만·동남태평양 주요 OMZ.
- 입력·전제: 임계값·밀도면 정의 통일. 격자 부피 가중(cosφ·층두께). 저농도 정밀도(모델·센서 모두 O2<수μmol에서 불확실).
- 해석 기준(advisory): 부피·코어수심 신뢰구간 겹침으로 판단. **CMIP 계열은 열대 OMZ 재현이 체계적으로 어려움**(대서양 과강, 인도양 과약, 아라비아해 부피 과소·과천화 등 다수 보고) → good/bad 단정 금지, 임계·해역 명시.
- 한계·주의(§G): 임계·등수심/등밀도 선택에 극도로 민감. 조밀도 낮은 격자·수직해상도가 OMZ 두께 왜곡. 관측 기후값도 sparse(§G-3).
- 출처: Bianchi et al. (2012, Global Biogeochemical Cycles, OMZ 부피·N2O); Cabré et al. (2015, Biogeosciences 12:5429, "Consistent global responses of marine ecosystems... CMIP5"); Busecke et al. (2022, AGU Advances 3, doi:10.1029/2021AV000470, Pacific OMZ); Sharma et al. (2021, Ocean Science 17:1303, 아라비아해 OMZ CMIP5 불확실성).

---

### 겉보기산소이용률 AOU (Apparent Oxygen Utilization)
- 무엇을 측정/검증하나: AOU = O2sat(T,S) − O2로, 수괴가 표층을 떠난 뒤 **호흡(재광물화)으로 소비한 산소량**의 대리지표. 순환연령·재광물화 강도 진단.
- 정의·수식: AOU = O2eq(T,S) − O2_obs(μmol kg⁻¹). preformed O2·환기 진단에 사용. 모델·관측 AOU를 수심대·밀도면별 비교.
- 적용 도메인/자료형: [격자]·[프로파일] O2 → AOU 유도. GLODAP·WOA·BGC-Argo.
- 입력·전제: O2 용해도(Garcia–Gordon) 동일식 사용. AOU는 표층 O2 불평형(과·미포화)을 무시하는 가정 포함 → 극지·고생산해역에서 편향.
- 해석 기준(advisory): AOU 과대 = 모델 재광물화 과강 또는 환기 과약. 심층 AOU 편차로 순환-생물 원인 분리(단, 결합 진단 필요).
- 한계·주의(§G): AOU는 preformed O2=포화 가정에 의존(현실은 불평형) → "preformed" 추적자 병행 권장. §G-4.
- 출처: Ito, Follows & Boyle (2004, GRL, preformed/AOU); Garcia & Gordon (1992); GLODAPv2(Olsen et al. 2016) 유도변수 관행.

---

### ★ 영양염 검증 (질산·인산·규산: WOA·GLODAP)
- 무엇을 측정/검증하나: 모델 거대영양염(질산 NO3, 인산 PO4, 규산 Si(OH)4)이 표층 고갈·심층 재생·전지구 재고를 관측 기후값과 일치시키는지. 1차생산·재광물화 제어의 핵심.
- 정의·수식: 표층/심층 bias·RMSE(§01, μmol kg⁻¹ 또는 μmol L⁻¹ 통일). 로그/제곱근 변환(표층 저농도 왜도) 고려. Redfield 비(N:P≈16, C:N:P=106:16:1) 진단, 잉여영양(N* = NO3 − 16·PO4)으로 질소고정·탈질 균형 검증.
- 적용 도메인/자료형: [격자] 모델 vs [격자] WOA / [병시료]·[프로파일] GLODAP·BGC-Argo(질산 센서). CF: `mole_concentration_of_nitrate_in_sea_water`, `mole_concentration_of_phosphate_in_sea_water`, `mole_concentration_of_silicate_in_sea_water`.
- 입력·전제: 단위·기준(kg vs L) 통일. 표층 저농도(검출한계 근처) 정밀도 주의. 등수심 vs 등밀도 비교 선택.
- 해석 기준(advisory): 심층 영양염 재고(전지구 적분)와 표층 잔여 영양(용승·개화대)을 나눠 평가. 모델의 표층 질산 과잉(HNLC 아닌데 잔존)·규산 편차는 규조·철제한 문제 신호. 해역·수심 의존 → 단정 금지.
- 한계·주의(§G): N* 등 유도량은 두 변수 오차 전파. 규산은 규조·용해에 민감해 편차 큼. WOA·GLODAP 보간 산물(§G-3).
- 출처: Garcia et al. (World Ocean Atlas Vol.4 Nutrients, NOAA Atlas NESDIS); Olsen et al. (2016, ESSD 8:297–323, GLODAPv2); Gruber & Sarmiento (1997, Global Biogeochem. Cycles, N*); Sarmiento & Gruber (2006, *Ocean Biogeochemical Dynamics*, Princeton — 표준 교과서, 확인요).

---

### 영양염 프로파일·약층 심도 검증 (nutricline depth)
- 무엇을 측정/검증하나: 질산선(nutricline)·규산선 등 **영양염 수직구배와 그 심도**를 모델이 재현하는지. 표층 공급·신생산 잠재력 진단.
- 정의·수식: 질산선 심도 = NO3가 특정 임계(예: 1 μmol kg⁻¹)에 도달하는 수심, 또는 최대 수직구배 dNO3/dz 수심. 프로파일 곡선 형상(§ 프로파일 카드)·수심 bias.
- 적용 도메인/자료형: [프로파일] BGC-Argo(질산)·GLODAP vs 모델 연직 프로파일.
- 입력·전제: 임계·구배 정의 통일. 수직해상도 차이 보간. 저농도 센서 정밀도.
- 해석 기준(advisory): 질산선 과천/과심은 성층·혼합·재광물화 커플링 신호. 임계 정의 의존 → 명시.
- 한계·주의(§G): 임계·구배법이 값 좌우. 아열대 gyre의 깊은 질산선은 관측 sparse.
- 출처: Sarmiento & Gruber (2006, 교과서, 확인요); Omand & Mahadevan (nutricline 관련, JGR/DSR); BGC-Argo nitrate QC 관행(Johnson et al.).

---

### ★ 탄산계 내부정합 검증 (carbonate system closure: CO2SYS/PyCO2SYS)
- 무엇을 측정/검증하나: 해양 탄산계 4대 측정변수(DIC, TA, pH, pCO2) 중 **2개를 입력해 나머지 2개를 계산**했을 때, 모델·관측의 유도변수 잔차와 **내부 열역학 정합성**. 탄산계 검증의 전제이자 자체 진단.
- 정의·수식: 입력 2변수 + T·S·P·영양염(PO4·Si) → K1,K2,KB,Ksp 등 해리상수 조로 나머지 유도(CO2SYS/PyCO2SYS). 서로 다른 두 쌍(예: DIC+TA vs pH+pCO2)으로 계산한 값의 차이 = **내부 불일치**(관측 QC·모델 정합성 척도). 아래 pH·pCO2·TA·DIC·Ω 카드의 공통 엔진.
- 적용 도메인/자료형: [병시료] GLODAP·[정점] BATS/HOT·[격자] 모델 탄산계. CF: `sea_water_ph_reported_on_total_scale`, `mole_concentration_of_dissolved_inorganic_carbon_in_sea_water` 등.
- 입력·전제: **pH 스케일(total/free/seawater) 통일**·**K1,K2 상수 조(예: Lueker et al. 2000, Mehrbach refit) 명시**·KSO4·KF·total boron 식 명시. 압력·온도(현장 vs 25℃) 정합. 영양염 입력 유무.
- 해석 기준(advisory): 두 쌍 유도 pCO2 차이가 관측 불확실성(수 μatm) 내면 정합. **상수 조·스케일이 다르면 수십 μatm·0.01 pH 차이 발생** → 모델-관측 비교 전 반드시 동일 규약으로 재계산.
- 한계·주의(§G): 상수 조·스케일 불일치가 "모델 오차"로 오인되는 대표적 함정. 저알칼리·연안·고온에서 상수 불확실. §G-4.
- 출처: Lewis & Wallace (1998, CO2SYS, ORNL/CDIAC); Humphreys et al. (2022, Geosci. Model Dev. 15:15–43, PyCO2SYS, doi:10.5194/gmd-15-15-2022); Lueker, Dickson & Keeling (2000, Marine Chemistry 70:105–119, K1/K2); Dickson, Sabine & Christian (2007, *Guide to Best Practices for Ocean CO2 Measurements*, PICES Special Pub. 3).

---

### ★ 표층 pCO2 검증 (SOCAT 매치업·해–기 CO2 플럭스)
- 무엇을 측정/검증하나: 모델 표층 해양 pCO2(또는 fCO2)가 선박 관측 대규모 DB(SOCAT)와 일치하는지, 나아가 해–기 CO2 플럭스·계절진폭·탄소흡수 패턴을 재현하는지. 해양 탄소흡수원 검증의 핵심.
- 정의·수식: ΔpCO2 = pCO2_ocean − pCO2_air. 해–기 플럭스 F = k·s·ΔpCO2(k=가스전달속도(풍속의존), s=용해도). 검증: SOCAT 궤적/격자에 시공간 콜로케이션 후 bias·RMSE(§01, μatm)·계절진폭·위도대 평균 플럭스. pCO2는 온도민감(∂lnpCO2/∂T≈4.23%/℃) → 열·비열 성분 분해(Takahashi) 진단.
- 적용 도메인/자료형: [트랙/병시료] SOCAT cruise/gridded vs [격자] 모델. CF: `surface_partial_pressure_of_carbon_dioxide_in_sea_water`, `surface_partial_pressure_of_carbon_dioxide_in_air`.
- 입력·전제: fCO2 vs pCO2 변환(fugacity 보정) 통일. SOCAT 격자(월 1°) vs cruise 자료 선택. 온도 기준(현장 SST) 정합. 풍속 산물(플럭스는 k에 민감)·용해도식 명시.
- 해석 기준(advisory): 계절진폭·연평균 흡수 패턴 일치가 핵심. **SOCAT는 시공간 편중**(북반구·항로 집중, 남대양·겨울 sparse) → 미표집 해역 외삽 주의. 값은 해역·계절 의존.
- 한계·주의(§G): 플럭스 오차는 ΔpCO2·k·풍속 오차의 곱 전파. SOCAT 표집 편중을 무시하면 전지구 흡수 추정 왜곡. §G-1·G-4.
- 출처: Bakker et al. (2016, ESSD 8:383–413, SOCATv3, doi:10.5194/essd-8-383-2016); Takahashi et al. (2009, Deep-Sea Research II 56:554–577, 표층 pCO2 기후·해–기 플럭스); Wanninkhof (2014, L&O Methods 12:351–362, 가스전달속도); Fay et al. / RECCAP2 해양 탄소 검증 프레임.

---

### ★ pH 검증 (total scale) 및 산성화 추세
- 무엇을 측정/검증하나: 모델 표층·심층 pH(total scale)가 관측(GLODAP·정점·BGC-Argo pH 센서)과 일치하는지, 장기 산성화 추세(dpH/dt)를 재현하는지.
- 정의·수식: pH bias·RMSE(§01). 산성화 추세는 시계열 선형/Mann–Kendall(§06)로 dpH/dt(≈ −0.02/decade 관측대). 계절·수심대 분리. pH는 탄산계 유도량 → CO2SYS 규약(위 카드) 통일 후 비교.
- 적용 도메인/자료형: [병시료] GLODAP·[정점] BATS/HOT/ESTOC·[프로파일] BGC-Argo pH vs [격자] 모델. CF: `sea_water_ph_reported_on_total_scale`.
- 입력·전제: **total scale 통일**(free/seawater scale 혼용 금지, 0.01~0.12 pH 차이). 현장 T·P의 pH vs 25℃ pH 구분. BGC-Argo pH 센서 편향(아래 float 카드) 보정 여부.
- 해석 기준(advisory): 추세는 다년(≥10년) 필요. **BGC-Argo pH는 체계적 편향(pCO2 과대·탄소흡수 과소로 전파)** 보고 → 플랫폼 편향을 관측 불확실성으로 반영. 값·추세는 해역·수심 의존.
- 한계·주의(§G): 스케일·상수·온도기준 불일치가 겉보기 bias 생성(§ CO2SYS 카드). 센서 pH 편향을 진값처럼 쓰지 말 것(§G-3).
- 출처: Bates et al. (BATS/ESTOC/HOT 산성화 시계열, Oceanography 27(1)); Lauvset et al. (GLODAP pH 추세); Williams et al. (2017, GBC, SOCCOM float pH); Nature Sci. Reports (2026, "A systematic bias in float pH...", doi 확인요) — float pH 편향.

---

### 전알칼리도 검증 (Total Alkalinity: TA–SSS 관계)
- 무엇을 측정/검증하나: 모델 전알칼리도(TA)가 관측과 일치하는지. TA는 주로 염분·수온의 보존적 함수 → **TA–SSS 회귀**로 진단하는 것이 효과적.
- 정의·수식: TA bias·RMSE(§01, μmol kg⁻¹). 지역별 TA = a + b·SSS(+c·SST) 경험식(예: LIAR/Lee et al. 2006) 회귀계수 비교. 정규화 TA(nTA=TA·35/SSS)로 담수·증발효과 제거 후 생물·CaCO3 효과 분리.
- 적용 도메인/자료형: [병시료] GLODAP·[정점] vs [격자] 모델. CF: `sea_water_alkalinity_expressed_as_mole_equivalent`.
- 입력·전제: 단위(μmol kg⁻¹) 통일. 담수유입·해빙 해역은 TA–SSS 관계 붕괴(별도 취급). CaCO3 생성·용해 신호는 nTA로 진단.
- 해석 기준(advisory): TA–SSS 기울기·절편이 관측 경험식과 일치하면 보존적 순환·염분 재현 양호. 편차는 CaCO3 순환·담수수지 문제 신호. 해역 의존.
- 한계·주의(§G): 강·해빙·연안에서 TA–SSS 선형성 실패. nTA 사용 시 SSS 기준(35) 명시.
- 출처: Lee et al. (2006, GRL 33:L19605, 전지구 표층 TA 경험식); Carter et al. (2018, L&O Methods, LIAR/LINR); Olsen et al. (2016, GLODAPv2).

---

### 용존무기탄소 DIC 검증 (GLODAP·인위탄소 Cant)
- 무엇을 측정/검증하나: 모델 용존무기탄소(DIC)가 표층·심층에서 관측과 일치하는지, 인위기원 탄소(Cant) 침투를 재현하는지.
- 정의·수식: DIC bias·RMSE(§01, μmol kg⁻¹). 표층 nDIC(염분정규화)·심층 DIC 단면. Cant는 back-calculation(ΔC*·TrOCA·eMLR) 관측 추정치와 비교(방법 의존 큼). 재광물화 신호는 DIC:AOU:NO3 화학량론으로 진단.
- 적용 도메인/자료형: [병시료] GLODAP·[정점] vs [격자] 모델. CF: `mole_concentration_of_dissolved_inorganic_carbon_in_sea_water`.
- 입력·전제: 단위 통일. Cant 관측 추정은 방법(eMLR 등)마다 다름 → 방법 명시. 심층은 밀도면 비교 유리.
- 해석 기준(advisory): 표층 DIC 계절진폭·심층 저장·Cant 침투수심을 나눠 평가. 심층 DIC 과대는 재광물화 과강/순환 과약 신호. 해역·수심 의존.
- 한계·주의(§G): Cant는 직접 관측 불가(추정치, §G-1). eMLR 등 방법 불확실성 큼.
- 출처: Olsen et al. (2016, ESSD 8:297–323, GLODAPv2); Sabine et al. (2004, Science 305:367–371, 전지구 인위탄소 재고); Gruber et al. (2019, Science 363:1193, Cant 변화 eMLR).

---

### ★ 아라고나이트/칼사이트 포화도 Ω 검증 (saturation state·saturation horizon)
- 무엇을 측정/검증하나: 모델 탄산칼슘 포화도 Ω(아라고나이트·칼사이트)와 **포화수심(saturation horizon, Ω=1)** 을 관측 유도값과 일치시키는지. 해양 산성화·석회화 생물 영향의 핵심.
- 정의·수식: Ω = [Ca²⁺][CO3²⁻]/Ksp*(광물·T·S·P). Ω<1이면 부식성(corrosive). 검증: 표층 Ω_ar bias, 포화수심(Ω_ar=1 도달 수심) 비교, 부식성 수체 부피. Ω는 DIC·TA(또는 pH·pCO2)에서 CO2SYS로 유도 → 규약 통일 전제.
- 적용 도메인/자료형: [병시료] GLODAP·[정점] 유도 Ω vs [격자] 모델. (직접 CF 표준명은 드물어 DIC/TA/pH로 유도)
- 입력·전제: Ksp 상수(Mucci 1983 등)·pH 스케일·K1K2 조 통일. 압력보정(심층 포화수심에 결정적). 영양염 입력.
- 해석 기준(advisory): 표층 Ω_ar은 극지·용승대에서 1에 근접(취약). **포화수심은 상수·압력보정에 매우 민감** → 규약 명시. good/bad 단정 금지, 해역·수심 분리.
- 한계·주의(§G): Ω는 다단계 유도량(오차 전파 큼). 상수·압력식 차이가 포화수심 수백 m 이동 유발. §G-4.
- 출처: Mucci (1983, American Journal of Science 283:780–799, 아라고나이트·칼사이트 Ksp); Feely et al. (2004, Science 305:362–366, CaCO3 포화·용해); Orr et al. (2005, Nature 437:681–686, 산성화·아라고나이트 포화 감소); Jiang et al. (2015, GBC, 표층 Ω 기후).

---

### ★ BGC-Argo 매치업·플랫폼 오차 (float–ship crossover·QC·보정)
- 무엇을 측정/검증하나: BGC-Argo 자율 프로파일 플로트 자료(O2·NO3·pH·Chl 형광·후방산란·조도)로 모델을 **프로파일 단위**로 검증하고, 동시에 float 자체의 플랫폼 편향(ship crossover 대비)을 진단.
- 정의·수식: float 프로파일 ↔ 모델 격자 시공간 콜로케이션(§15), 깊이/밀도면별 bias·RMSE(§01). float ↔ 근접 선박(GLODAP) crossover로 센서 편향·드리프트 추정. float Chl 형광은 slope factor(공장기본값 2배 과대 알려짐)·NPQ(주간 소광) 보정, O2는 air-calibration.
- 적용 도메인/자료형: [프로파일] BGC-Argo vs [격자] 모델·[병시료] GLODAP.
- 입력·전제: **float QC 등급·보정 적용분(adjusted) 사용**(raw 금지). Chl 형광 slope·NPQ 보정, O2 gain, pH 편향 보정 명시. 프로파일 대표성(점 vs 격자).
- 해석 기준(advisory): float은 시공간 커버리지(특히 남대양·겨울) 강점이나 **센서 편향이 변수별로 다름**(pH 편향 → pCO2 과대). 편향을 관측 불확실성 예산에 반영. 해역·변수 의존.
- 한계·주의(§G): raw float 자료를 진값처럼 사용 금지(§G-3). 형광 Chl은 HPLC 대비 편향 큼. 삼중대조 등 "독립성" 가정 시 float-선박-모델 상관 주의(§G-2).
- 출처: Claustre, Johnson & Takeshita (2020, Annual Review of Marine Science 12:23–48, BGC-Argo 리뷰); Roemmich et al. (Argo program); Johnson et al. (2017, JGR Oceans, SOCCOM float QC); Xing et al. (형광 NPQ 보정); BG (2023, 20:1405, BGC-Argo로 BGC 모델 평가·관측망 설계).

---

### ★ 순1차생산 NPP 검증 (Net Primary Production: VGPM·CbPM·¹⁴C 정점)
- 무엇을 측정/검증하나: 모델 순1차생산(NPP, mg C m⁻² d⁻¹)이 위성기반 NPP 산물(VGPM·Eppley-VGPM·CbPM)·현장 ¹⁴C 배양(정점 BATS/HOT/CARIACO) 관측과 일치하는지. 생태계 탄소흐름의 핵심량.
- 정의·수식: 연직적분 NPP(∫ PP dz) 비교. bias·RMSE·log 통계(NPP도 광범위 분포 → log 권장). 위성 NPP 모델: VGPM(Chl·광·온도의존 효율), Eppley-VGPM(지수 온도의존), CbPM(탄소기반, Cphyto·성장률). 계절·위도대·해역대 적분생산 비교.
- 적용 도메인/자료형: [L3/L4] 위성 NPP vs [격자] 모델; [정점] ¹⁴C vs 위성/모델. CF: `net_primary_production_of_biomass_expressed_as_carbon_per_unit_volume_in_sea_water`(부피) / 연직적분량.
- 입력·전제: **위성 NPP 자체가 모델 산물**(진값 아님, 알고리즘 의존 큰 산포). 정의(부피 vs 연직적분·일 vs 연) 통일. ¹⁴C 정점은 배양법·기간 차이.
- 해석 기준(advisory): 위성 NPP 알고리즘 간 차이가 크므로(전지구 총량 30~70 Gt C/yr 폭) **단일 위성 NPP를 기준삼아 합격 판정 금지** → 여러 알고리즘 범위(envelope) 대비. 해역·계절 분리.
- 한계·주의(§G): 위성 NPP 알고리즘 불확실성이 매우 큼(§G-1). VGPM은 고생산·극지에서 편향. Cphyto 기반(CbPM)은 후방산란 가정 의존.
- 출처: Behrenfeld & Falkowski (1997, L&O 42(1):1–20, VGPM); Behrenfeld et al. (2005, GBC 19:GB1006, CbPM 탄소기반); Carr et al. (2006, Deep-Sea Res. II 53:741–770, NPP 모델 상호비교); Saba et al. (2011, Biogeosciences, NPP 모델-현장 비교).

---

### 수출생산·POC 플럭스 검증 (export production / e-ratio·sediment trap)
- 무엇을 측정/검증하나: 모델의 유기탄소 수출(export, 진광층 하부로의 POC 침강플럭스)과 e-ratio(export/NPP)·f-ratio를 관측(침강물 트랩·²³⁴Th·역추정)과 비교. 생물펌프 강도 검증.
- 정의·수식: POC 플럭스(mg C m⁻² d⁻¹) 깊이별 감쇠(Martin curve F(z)=F100·(z/100)^−b). e-ratio = export/NPP. 트랩·²³⁴Th·산소이용 기반 관측과 bias 비교.
- 적용 도메인/자료형: [정점]·[관측] 트랩/²³⁴Th vs [격자] 모델 수출플럭스.
- 입력·전제: 수출 기준수심(100 m·진광층 하부·Ez) 통일. 트랩 포집효율·²³⁴Th 방법 불확실성.
- 해석 기준(advisory): e-ratio는 온도·군집 의존(고위도 높음). Martin b(감쇠지수) 비교로 재광물화 심도 진단. 관측 sparse·불확실 → 정성 비교 위주.
- 한계·주의(§G): 트랩 편향·수심 정의 불일치가 큰 산포 유발. 관측 sparse(§G-3).
- 출처: Martin et al. (1987, Deep-Sea Research 34:267–285, Martin curve); Buesseler et al. (2007, Science 316:567, 진광층 수출); Henson et al. (2011, GRL, e-ratio 전지구); Siegel et al. (2014, GBC, export 검증).

---

### 식물플랑크톤 기능형군 PFT 검증 (size class / HPLC pigment)
- 무엇을 측정/검증하나: 모델 식물플랑크톤 기능형군(PFT: 규조·와편모·남세균·피코 등)·크기분율(micro/nano/pico)이 위성 PFT·HPLC 색소 관측과 일치하는지.
- 정의·수식: 분율(0~1) 또는 그룹별 Chl 비교. 위성 PFT(밴드비·abundance-based)·HPLC 진단색소(CHEMTAX) 대조. 분율 오차(MAE·혼동행렬)·우점군 일치율.
- 적용 도메인/자료형: [L3] 위성 PFT·[정점] HPLC vs [격자] 모델 그룹 Chl.
- 입력·전제: PFT 정의(크기 vs 분류군) 통일. 위성 PFT는 Chl에서 통계추정(불확실 큼). HPLC-CHEMTAX 가정.
- 해석 기준(advisory): 우점군·크기구조의 위도·계절 패턴 일치 위주. 위성/모델 PFT 정의가 다르면 직접 비교 곤란 → 정의 매핑 명시.
- 한계·주의(§G): 위성 PFT 불확실성 큼(§G-1). 모델 그룹 수·정의가 관측과 불일치.
- 출처: Bracher et al. (2017, Frontiers in Marine Science, PFT 원격탐사 리뷰); Hirata et al. (2011, Biogeosciences, size class from ocean colour); Mackey et al. (1996, MEPS, CHEMTAX).

---

### 투광층·Kd(490)·투명도 검증 (euphotic depth / diffuse attenuation)
- 무엇을 측정/검증하나: 모델·위성의 빛 감쇠(Kd490)·진광층 심도(Zeu, 1% 광량)·투명도가 일치하는지. 광환경은 1차생산·성층 커플링의 입력.
- 정의·수식: Kd(490)(m⁻¹) bias·RMSE(로그 고려). Zeu = 4.6/Kd(균질 가정) 또는 Chl-Zeu 경험식(Morel–Maritorena). 위성 Kd vs 모델 광감쇠.
- 적용 도메인/자료형: [L3] 위성 Kd490 vs [격자] 모델; [정점] PAR 프로파일.
- 입력·전제: Kd 정의(490 nm vs PAR) 통일. 위성 Kd 알고리즘 의존. 연안 CDOM·부유물 영향.
- 해석 기준(advisory): Zeu·Kd의 위도·계절 패턴 일치. 연안에서 위성 Kd 오차 큼 → 외해/연안 분리.
- 한계·주의(§G): Kd-Chl 경험식은 Case-1 가정(연안 실패). §G-4.
- 출처: Morel et al. (2007, RSE, Zeu from ocean colour); Lee et al. (2005, JGR, Kd490); Mueller (2000, SeaWiFS Kd 알고리즘).

---

### 적분·재고량 검증 (depth-integrated Chl / nutrient·carbon inventory)
- 무엇을 측정/검증하나: 표층값이 아닌 **연직적분량·전지구 재고**(적분 Chl, 심층엽록소극대 DCM, 영양염·DIC·탄소 재고)를 모델이 관측과 일치시키는지. 표층만으로 놓치는 수체 총량 검증.
- 정의·수식: ∫ Chl dz(mg m⁻²)·DCM 심도·전지구 영양염/탄소 적분(면적·부피 가중). 재고 bias·수지 닫힘(§04 교차).
- 적용 도메인/자료형: [프로파일]·[격자] 적분. BGC-Argo(적분 Chl·DCM)·GLODAP(탄소재고).
- 입력·전제: 적분 상·하한·수직해상도 통일. DCM은 프로파일 필요(위성 표층 불가).
- 해석 기준(advisory): 표층 Chl은 맞아도 DCM·적분 Chl이 틀릴 수 있음 → 표층/적분 분리 평가. 재고는 전지구 수지 진단.
- 한계·주의(§G): 위성은 표층만 → 적분·DCM 검증엔 프로파일 필수. 적분구간 불일치 편향.
- 출처: Cornec et al. (2021, GBC, BGC-Argo DCM 전지구); Uitz et al. (2006, JGR, 적분 Chl·군집); Sarmiento & Gruber (2006, 교과서, 확인요).

---

### ★ 연직 프로파일·단면 비교 (profile / section: 심층구조)
- 무엇을 측정/검증하나: O2·영양염·DIC·pH 등의 **연직 프로파일 형상**과 **위도-깊이/경도-깊이 단면**을 모델이 관측과 일치시키는지. 표층·격자통계가 못 보는 심층 3차원 구조 진단.
- 정의·수식: 깊이별 bias·RMSE 프로파일; 단면 등치선(모델 vs WOA/GLODAP) 중첩·차이 단면; 등밀도면 값 비교. 프로파일 형상 지표(약층 심도·구배). Taylor/Target은 §01·figures/16.
- 적용 도메인/자료형: [프로파일] BGC-Argo·GLODAP·[격자] WOA vs [격자] 모델.
- 입력·전제: **등수심 vs 등밀도 비교 선택 명시**(약층 이동에 등수심 민감). 수직해상도 보간(§15). 단위 통일.
- 해석 기준(advisory): 심층 재광물화·환기 구조의 계통편차 위치를 단면으로 파악. 등밀도 비교가 순환-생물 원인분리에 유리. 해역·수심 의존.
- 한계·주의(§G): 등수심 비교는 성층 오차를 생물오차로 오인 가능. 관측 프로파일 sparse(§G-3).
- 출처: Stow et al. (2009, J. Marine Systems 76:4–15); WOCE/GO-SHIP 단면 관행; Séférian et al. (2020, Current Climate Change Reports, CMIP6 BGC 평가 — 단면 진단).

---

### ★ 생지화학 모델 스킬 종합틀 (Stow 2009 / target·Taylor·cost function)
- 무엇을 측정/검증하나: 여러 생지화학 변수(Chl·NO3·O2·pCO2 등)를 **공통 스킬지표 세트**로 요약해 모델 전반의 성능·편향을 한눈에 비교하는 표준 프레임. 커플드 물리-생지화학 모델 평가의 관행틀.
- 정의·수식: Stow et al.(2009) 권고 지표 묶음 — 상관 r, RMSE, reliability index RI, average error(AE=bias), average absolute error, modelling efficiency(MEF), cost function CF. Jolliff et al.(2009) target diagram(bias vs unbiased-RMSD, §08 파랑카드·figures/16과 공유), Taylor diagram(§01). 다변수 정규화 후 한 도표에 배치.
- 적용 도메인/자료형: 다변수·다지점 [격자]/[정점]/[프로파일] 종합. 로그 변수는 log 공간 스킬.
- 입력·전제: 변수별 정규화(관측 σ)·log 변환(Chl·영양염). 공통 매치업. cost function 정의(예: CF=(1/N)Σ|M−O|/σ_obs) 명시.
- 해석 기준(advisory): Stow 계열 관행 등급(예: CF<1, MEF>0 등)은 **advisory** — 변수·해역·해상도·기준자료 의존이며 "good/reasonable" 자동판정 금지(§G-4). target diagram 원점 근접·Taylor 관측점 근접으로 상대비교.
- 한계·주의(§G): 단일 스킬점수로 순위 확정 금지(§G-6, 다축·유의성 동반). 로그/선형 공간 혼용 주의. 등급 임계 남용 경계.
- 출처: Stow et al. (2009, Journal of Marine Systems 76:4–15, "Skill assessment for coupled biological/physical models of marine systems"); Jolliff et al. (2009, J. Marine Systems 76:64–82, target diagram); Doney et al. (2009, J. Marine Systems 76:95–112, "Skill metrics for confronting global upper ocean ecosystem-biogeochemistry models"); Allen et al. (2007, J. Marine Systems, 운영 BGC 스킬).

---

### 기후값 격자-격자 공간비교 (WOA/GLODAP 대조 맵·위도-깊이 단면)
- 무엇을 측정/검증하나: 모델 [격자]를 관측 기후값 격자(WOA 영양염·O2, GLODAPv2 탄소계, OC-CCI Chl)와 **전면적 공간 비교**해 표층 편차지도·위도-깊이 단면 편차를 산출. 정점 없는 해역까지 계통편차 위치·계절성 진단.
- 정의·수식: 공통 격자 재격자화(§15) 후 표층 편차지도(bias·RMSD·상관, log 변수는 log공간)·경도평균 위도-깊이 단면 편차. 영역·위도대 평균. 패턴상관·Taylor는 §01/02.
- 적용 도메인/자료형: [격자] 모델 vs [격자] WOA/GLODAPv2/OC-CCI 기후.
- 입력·전제: 동일 기간·기준기간, 단위·CF·마스크 통일, 등수심/등밀도 선택. 기후값은 보간 산물(§G-3).
- 해석 기준(advisory): 용승대·OMZ·극지 개화 등 편차 hotspot의 위치·계절 파악. 기후값은 진값 아님(§G-1) → 정점·프로파일과 교차해석.
- 한계·주의(§G): 재격자화(비선형 log 변수) 보존성·해안선 처리. 관측 sparse 해역 기후값 신뢰 낮음.
- 출처: Garcia et al. (World Ocean Atlas, NOAA); Lauvset et al. (2016, ESSD 8:325–340, GLODAPv2 mapped climatology); Sathyendranath et al. (OC-CCI); Séférian et al. (2020, CMIP6 BGC 평가).

---

### 로그공간 분포·꼬리 비교 (PDF/CDF·QQ, log축)
- 무엇을 측정/검증하나: Chl·영양염·NPP 등 로그정규 변수의 **분포 전체와 저·고농도 꼬리**를 모델·관측 간 비교. 평균 지표가 못 보는 분포 편향·극값 진단.
- 정의·수식: log축 PDF/CDF 중첩·KS(§03)·QQ(figures/16). Perkins skill score(분포 겹침, §03/07)도 log축 적용. 저농도(빈영양)·고농도(개화) 꼬리 이탈 판정.
- 적용 도메인/자료형: [격자]/[정점]/[L3] 장기 통계. 시간정렬 불필요(분포).
- 입력·전제: log 변환·동일 기간·동일 모집단. 자기상관 시 유효표본 보정(§G-6).
- 해석 기준(advisory): 상위 꼬리 과소 = 개화 과소, 하위 꼬리 부족 = 빈영양 외해 과대. QQ와 상보.
- 한계·주의(§G): 분포만 비교(동시성 못 봄). 자기상관 KS 과민.
- 출처: Campbell (1995); Perkins et al. (2007, J. Climate, PDF skill — §07 공유); Wilks(교과서, KS/QQ — §01/03).

---

### 경보·임계 사건 검증 (녹조·저산소·부식성 임계 초과)
- 무엇을 측정/검증하나: "Chl > 녹조임계", "O2 < 저산소임계", "Ω_ar < 1(부식성)" 같은 **이진 사건**을 모델이 맞히는지. 연속 지표가 못 주는 운영·생태 경보 관점.
- 정의·수식: 2×2 분할표 → POD·FAR·CSI·HSS 등(정의·수식은 §03/07 참조). 임계는 위해기준(HAB Chl·hypoxia 2 mg L⁻¹≈62 μmol kg⁻¹·Ω<1)으로 설정. 사건 부피·면적·기간 비교도 병행.
- 적용 도메인/자료형: [격자]/[정점]/[L3] Chl·O2·Ω 임계. HAB·연안 저산소·산성화 노출.
- 입력·전제: 합의 임계·정렬 매치업. 드문 사건 표본 충분(신뢰구간 동반).
- 해석 기준(advisory): 단일 임계는 정보손실 → 여러 임계·ROC(§03) 병행. 격자 double-penalty 주의(§02). 임계는 지역·규제 의존.
- 한계·주의(§G): 사건 희소 시 점수 불안정. 위성 결측(구름)이 개화 사건 탐지 저해.
- 출처: Jolliffe & Stephenson(교과서, 범주형 — §03); Stumpf et al. (HAB nowcast 검증 관행); Breitburg et al. (2018, Science 359:eaam7240, 저산소 확산).

---

### 불확실성·대표성 오차 (관측 불확실성 대비 상대평가)
- 무엇을 측정/검증하나: 생지화학 관측 자체의 오차·대표성(점 vs 격자·표층 vs 광학심도·형광 vs HPLC·센서 편향)을 **오차 예산으로 정량화**해, 모델-관측 차이를 관측 불확실성 대비 상대평가. 과대·과소 판정의 과신을 방지.
- 정의·수식: 관측 오차 성분(측정정밀도 + 대표성 오차 + 알고리즘/센서 편향) 합산 → 모델-관측 차이가 이 예산을 넘는지 판정. 삼중대조(TC/ETC, §12/15)로 기준 없이 오차분산 추정(단, 독립성 가정 §G-2·G-3).
- 적용 도메인/자료형: 전 변수. 위성(대표성)·float(센서편향)·병시료(정밀) 이질 자료 결합 시 필수.
- 입력·전제: 각 자료의 오차 메타데이터. TC는 세 독립자료·오차 무상관 가정(모델·재분석 강제력 공유 시 위배).
- 해석 기준(advisory): 차이 < 관측불확실성이면 "구분 불가"로 보고(모델 우수/열등 단정 금지). 위성·float 편향은 진값 아님.
- 한계·주의(§G): TC 독립성 가정 위배가 흔함(§G-2·G-3). 대표성 오차 무시가 대표적 과신 원인(§G-4).
- 출처: §12/§15의 매치업·대표성오차·TC/ETC 카드(공통 구현); Bailey & Werdell (2006, 매치업 대표성); Gregg & Casey (2004, 위성-모델 오차); Stoffelen (1998)·McColl et al. (2014, ETC — §08/12 공유).

---

## 출처 (References)

### 표준 참고문헌 / 교과서·지침·프로토콜 (실제 존재)
- Sarmiento, J. L. & Gruber, N. (2006) *Ocean Biogeochemical Dynamics*, Princeton University Press (BGC 변수·화학량론·수지 표준 교과서 — 확인요).
- Dickson, A. G., Sabine, C. L. & Christian, J. R. (eds.) (2007) *Guide to Best Practices for Ocean CO2 Measurements*, PICES Special Publication 3 (탄산계 측정·pH 스케일·상수 표준).
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (RMSE·bias·KS·QQ·회귀 — §01 공통).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification*, Wiley (범주형·확률 — §03 공통).

### 통계·성능지표 (해색·로그정규)
- Campbell, J. W. (1995) "The lognormal distribution as a model for bio-optical variability in the sea," *Journal of Geophysical Research: Oceans*, 100(C7), 13237–13254. (Chl 로그정규·log10 통계)
- Seegers, B. N., Stumpf, R. P., Schaeffer, B. A., Loftin, K. A. & Werdell, P. J. (2018) "Performance metrics for the assessment of satellite data products: an ocean color case study," *Optics Express*, 26(6), 7404–7422. (MdSA 등 대칭 성능지표)
- Bailey, S. W. & Werdell, P. J. (2006) "A multi-sensor approach for the on-orbit validation of ocean color satellite data products," *Remote Sensing of Environment*, 102(1–2), 12–23. (해색 매치업 프로토콜)
- Hu, C., Lee, Z. & Franz, B. (2012) "Chlorophyll a algorithms for oligotrophic oceans: A novel approach based on three-band reflectance difference," *Journal of Geophysical Research: Oceans*, 117, C01011. (doi:10.1029/2011JC007395) (OCI 3-band)
- Valente, A. et al. (2022) "A compilation of global bio-optical in situ data for ocean colour satellite applications – version three," *Earth System Science Data*, 14, 5737–5770. (매치업 DB)

### 관측 자료·기후값 (검증 기준자료)
- Bakker, D. C. E. et al. (2016) "A multi-decade record of high-quality fCO2 data in version 3 of the Surface Ocean CO2 Atlas (SOCAT)," *Earth System Science Data*, 8, 383–413. (doi:10.5194/essd-8-383-2016)
- Olsen, A. et al. (2016) "The Global Ocean Data Analysis Project version 2 (GLODAPv2) – an internally consistent data product for the world ocean," *Earth System Science Data*, 8, 297–323.
- Lauvset, S. K. et al. (2016) "A new global interior ocean mapped climatology: the 1°×1° GLODAP version 2," *Earth System Science Data*, 8, 325–340.
- Garcia, H. E. et al. *World Ocean Atlas* (Vol.3 Dissolved Oxygen; Vol.4 Nutrients), NOAA Atlas NESDIS (기후값 격자).
- Claustre, H., Johnson, K. S. & Takeshita, Y. (2020) "Observing the global ocean with Biogeochemical-Argo," *Annual Review of Marine Science*, 12, 23–48. (BGC-Argo)

### 탄산계·산성화
- Lewis, E. & Wallace, D. W. R. (1998) *Program Developed for CO2 System Calculations (CO2SYS)*, ORNL/CDIAC-105.
- Humphreys, M. P. et al. (2022) "PyCO2SYS v1.8: marine carbonate system calculations in Python," *Geoscientific Model Development*, 15, 15–43. (doi:10.5194/gmd-15-15-2022)
- Lueker, T. J., Dickson, A. G. & Keeling, C. D. (2000) "Ocean pCO2 calculated from dissolved inorganic carbon, alkalinity, and equations for K1 and K2...," *Marine Chemistry*, 70, 105–119.
- Mucci, A. (1983) "The solubility of calcite and aragonite in seawater at various salinities, temperatures, and one atmosphere total pressure," *American Journal of Science*, 283, 780–799.
- Lee, K. et al. (2006) "Global relationships of total alkalinity with salinity and temperature in surface waters of the world's oceans," *Geophysical Research Letters*, 33, L19605.
- Feely, R. A. et al. (2004) "Impact of anthropogenic CO2 on the CaCO3 system in the oceans," *Science*, 305, 362–366.
- Orr, J. C. et al. (2005) "Anthropogenic ocean acidification over the twenty-first century and its impact on calcifying organisms," *Nature*, 437, 681–686.
- Sabine, C. L. et al. (2004) "The oceanic sink for anthropogenic CO2," *Science*, 305, 367–371.
- Gruber, N. et al. (2019) "The oceanic sink for anthropogenic CO2 from 1994 to 2007," *Science*, 363, 1193–1199.
- Takahashi, T. et al. (2009) "Climatological mean and decadal change in surface ocean pCO2, and net sea–air CO2 flux over the global oceans," *Deep-Sea Research II*, 56, 554–577.
- Wanninkhof, R. (2014) "Relationship between wind speed and gas exchange over the ocean revisited," *Limnology and Oceanography: Methods*, 12, 351–362.

### 산소·OMZ·영양염
- Garcia, H. E. & Gordon, L. I. (1992) "Oxygen solubility in seawater: Better fitting equations," *Limnology and Oceanography*, 37(6), 1307–1312.
- Oschlies, A., Brandt, P., Stramma, L. & Schmidtko, S. (2018) "Drivers and mechanisms of ocean deoxygenation," *Nature Geoscience*, 11, 467–473.
- Cabré, A., Marinov, I., Bernardello, R. & Bianchi, D. (2015) "Oxygen minimum zones in the tropical Pacific across CMIP5 models," *Biogeosciences*, 12, 5429–5454.
- Busecke, J. J. M., Resplandy, L., Ditkovsky, S. J. & John, J. G. (2022) "Diverging fates of the Pacific Ocean oxygen minimum zone and its core in a warming world," *AGU Advances*, 3. (doi:10.1029/2021AV000470)
- Gruber, N. & Sarmiento, J. L. (1997) "Global patterns of marine nitrogen fixation and denitrification," *Global Biogeochemical Cycles*, 11, 235–266. (N*)
- Breitburg, D. et al. (2018) "Declining oxygen in the global ocean and coastal waters," *Science*, 359, eaam7240.

### 1차생산·수출·군집
- Behrenfeld, M. J. & Falkowski, P. G. (1997) "Photosynthetic rates derived from satellite-based chlorophyll concentration," *Limnology and Oceanography*, 42(1), 1–20. (VGPM)
- Behrenfeld, M. J. et al. (2005) "Carbon-based ocean productivity and phytoplankton physiology from space," *Global Biogeochemical Cycles*, 19, GB1006. (CbPM)
- Carr, M.-E. et al. (2006) "A comparison of global estimates of marine primary production from ocean color," *Deep-Sea Research II*, 53, 741–770. (NPP 상호비교)
- Martin, J. H., Knauer, G. A., Karl, D. M. & Broenkow, W. W. (1987) "VERTEX: carbon cycling in the northeast Pacific," *Deep-Sea Research*, 34, 267–285. (Martin curve)
- Siegel, D. A. et al. (2002) "The North Atlantic spring phytoplankton bloom and Sverdrup's critical depth hypothesis," *Science*, 296, 730–733.
- Racault, M.-F. et al. (2012) "Phytoplankton phenology in the global ocean," *Ecological Indicators*, 14, 152–163.

### 모델 스킬·평가틀
- Stow, C. A. et al. (2009) "Skill assessment for coupled biological/physical models of marine systems," *Journal of Marine Systems*, 76, 4–15.
- Doney, S. C. et al. (2009) "Skill metrics for confronting global upper ocean ecosystem-biogeochemistry models against field and remote sensing data," *Journal of Marine Systems*, 76, 95–112.
- Jolliff, J. K. et al. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment," *Journal of Marine Systems*, 76, 64–82. (target diagram — §08과 공유)
- Séférian, R. et al. (2020) "Tracking improvement in simulated marine biogeochemistry between CMIP5 and CMIP6," *Current Climate Change Reports*, 6, 95–119.

### 웹 자료 (조사 시 직접 참조)
- NASA Ocean Biology Processing Group (OBPG) — ocean colour validation·performance metrics: https://oceancolor.gsfc.nasa.gov
- ESA Ocean Colour CCI (OC-CCI), Sathyendranath et al. 산출물 문서: https://climate.esa.int/en/projects/ocean-colour/
- SOCAT (Surface Ocean CO2 Atlas): https://www.socat.info
- GLODAP (Global Ocean Data Analysis Project): https://www.glodap.info
- BGC-Argo program / SOCCOM: https://biogeochemical-argo.org , https://soccom.princeton.edu

### 확인요 (웹에서 1차 확인 못 했거나 정정한 항목)
- Sarmiento & Gruber (2006) *Ocean Biogeochemical Dynamics* — BGC 표준 교과서로 통용되나 이 세션 웹 재확인 안 함(확인요).
- Nature *Scientific Reports* (2026, "A systematic bias in float pH leads to overestimation of derived pCO2...") — 제목·저널은 검색으로 확인, 정확 권·페이지·DOI는 인용 전 재확인(확인요).
- Doney et al. (2009)·Allen et al. (2007) 권·페이지는 *Journal of Marine Systems* 76 특집(BGC skill assessment) 내 논문으로 확인되나 개별 페이지 재확인 권장(확인요).
- CF standard_name: `net_primary_production_of_biomass_expressed_as_carbon_per_unit_volume_in_sea_water`·`sea_water_alkalinity_expressed_as_mole_equivalent`·`mole_concentration_of_dissolved_inorganic_carbon_in_sea_water`는 CF 표준표에 존재하나 버전에 따라 표기 상이 가능 — 라우터 매핑 시 CF 표준표 대조 권장(확인요).

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(검색으로 확인된 제목·저널·연도 기재, DOI는 확인된 것만 표기, 임의 생성 금지). 논문 그림은 복제하지 않으며 유형·사양만 참조한다. 기준자료(WOA·GLODAP·SOCAT·위성 L3/L4·재분석)는 진값이 아니라 reference이며, 관측 불확실성·대표성 오차를 항상 병기해 상대평가한다(§G 원칙 준수).
