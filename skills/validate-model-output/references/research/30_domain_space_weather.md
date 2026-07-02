# 도메인: 우주기상 (Space Weather) 검증·분석 방법 카탈로그

이 문서는 우주기상(space weather) 수치·경험·기계학습 모델의 산출물 — 지자기지수(Kp/Dst/ap/AE/SYM-H), 전리층 총전자량(TEC), 태양풍(속도·밀도·자기장 Bz), 태양복사플럭스(F10.7), CME/충격파 도달시각, 태양플레어·양성자 사건 확률 — 을 관측(지자기 관측소, GNSS TEC, L1 태양풍 위성 ACE/DSCOVR, 전파망원경)·경험모델·재분석과 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다.

우주기상 검증의 핵심 3축은 (1) **연속 시계열 적합(fit-performance)** — RMSE·MAE·prediction efficiency(PE)·상관, (2) **사건 탐지(event-detection)** — 폭풍/플레어 임계 초과의 분할표 기반 Heidke skill score(HSS)·POD·FAR·bias, (3) **타이밍(timing/phase)** — 폭풍 개시(SSC)·CME 도달시각·주기 위상 오차다. 이 도메인의 표준화는 **CCMC(NASA Community Coordinated Modeling Center) 검증 프레임워크·scoreboard**와 **Liemohn et al.(2018) "Model Evaluation Guidelines for Geomagnetic Index Predictions"**, **ISES(국제우주환경서비스) RWC 검증 관행**이 제공한다.

> **자료형 표기 약어**: [시계열]=관측소·L1위성 시계열(지자기 1min/1h, 태양풍 1min, TEC 15min 등), [격자]=글로벌 TEC 지도(GIM)·전리층 격자 NetCDF, [정점]=단일 GNSS 관측소·검조소식 지자기 관측소, [사건]=폭풍/플레어/도달 이벤트 목록.
> **표준명 주의**: 지자기지수(Kp/Dst/ap/AE/SYM-H)·F10.7·TEC 는 **CF standard_name 이 정식으로 존재하지 않는 경우가 많다** → 이름 `Kp`/`Dst`/`ap`/`AE`/`SYM-H`/`F10.7`/`TEC`/`tec` 그대로 사용하고, 라우터는 변수명·단위(nT, TECU, sfu)·차원으로 판별한다.
> **공통 지표 교차링크**: RMSE·MAE·bias·상관·Taylor·QQ·bootstrap·분할표(POD/FAR/CSI/HSS)·Brier/ROC·CRPS·극값(GEV/POT)은 **재정의하지 않는다** → `01_error_statistics.md`, `03_categorical_event_extremes.md`, `06_timeseries_signal.md`, `05_spectral_eof_modal.md`, `figures/16` 참조. 본 카드는 **우주기상 고유의 정의·전제·임계·주의**만 기술한다.
> **해석 임계는 advisory** — 태양활동 위상(극대기/극소기)·위도대(적도·중위도·오로라대)·폭풍/정온 여부·리드타임에 따라 크게 변한다. good/bad 단정 금지(§G 연결).

## 이 파일에 담은 방법 (한 줄 목차)
- **지자기지수 시계열 검증 (Dst/SYM-H/AE fit-performance)** — RMSE·MAE·PE·상관 (→01)
- **prediction efficiency (PE) / 결정계수 R²** — 분산 정규화 스킬
- **Kp/ap 이산·준로그 지수 검증** — 3시간 계단·부트스트랩 (→01)
- **지자기폭풍 사건 탐지 (임계 초과 분할표: HSS·POD·FAR·CSI)** — Dst/Kp 임계 (→03)
- **폭풍 개시·급시작(SSC) timing 오차** — 개시시각·주경 저점 위상
- **동적시간왜곡 (Dynamic Time Warping, DTW) — Dst 위상평가** (→06)
- **AE/AL/AU 오로라대 전류지수 검증** — substorm·고분해 (→01)
- **태양풍 시계열 검증 (V, n, Bz, IMF clock angle)** — L1 예측 대조 (→01)
- **태양풍 도달시각/전파 오차 (L1→magnetopause propagation lag)** — 시간정렬
- **CME/충격파 도달시각 오차 (arrival time error ΔtA)** — CCMC scoreboard
- **CME 도달 사건 탐지 (hit/miss/false alarm)** — 도달여부 분할표 (→03)
- **전리층 TEC 검증 (bias/RMSE, TECU)** — GNSS 지상 대조 (→01)
- **글로벌 TEC 지도(GIM) 격자-격자 공간비교** — 위도·지방시 의존 (→01,02)
- **차분 STEC (dSTEC) 검증** — 관측소별 상대 slant TEC
- **전리층 위성 검증 (radio occultation·altimeter VTEC)** — COSMIC·Jason (→12)
- **foF2/hmF2/NmF2 임계주파수 검증 (ionosonde)** — 수직탐측 대조
- **F10.7 / 태양복사플럭스 예측 검증 (sfu)** — 리드타임별 RMSE (→01)
- **태양플레어 확률예보 검증 (Brier·ROC·reliability)** — X/M급 (→03)
- **드문 사건 스킬 (TSS·SEDI·ETS·climatology 기준)** — 극한 폭풍 (→03)
- **확률·앙상블 우주기상 검증 (CRPS·rank histogram)** — 앙상블 Kp/Dst (→03)
- **분포·QQ 비교 (Dst/TEC 분포·꼬리)** — 극한값 재현 (→01, figures/16)
- **극한 지자기 사건 통계 (GEV/POT return level)** — 100년 폭풍 (→03)
- **주기·계절 위상 검증 (27일 자전·연·태양주기)** — 스펙트럼·위상 (→05,06)
- **CCMC 검증 프레임워크·scoreboard (운영 표준)** — 매치업·집계

---

### 지자기지수 시계열 검증 (Dst / SYM-H / AE fit-performance)
- 무엇을 측정/검증하나: 모델이 예측한 지자기지수(Dst=환전류 강도, SYM-H=1분 대칭 H성분, AE=오로라대 전류) 시계열이 관측(WDC Kyoto, USGS 등)과 연속적으로 일치하는지. 우주기상 모델 검증의 1차 fit-performance 축.
- 정의·수식: 매치업 쌍 (mᵢ, oᵢ)에 대해 RMSE·MAE·ME(bias)·Pearson R 적용(정의는 `01_error_statistics.md`). Dst/SYM-H 단위 nT. 리드타임(예: 1h/3h/6h ahead)별로 분리 집계하는 것이 관행.
- 적용 도메인/자료형: L1 태양풍 입력 → 지수 예측 모델(경험/물리/ML). [시계열](관측소 유도 지수) vs 모델 예측 [시계열].
- 입력·전제: 관측·모델 동일 시간분해(Dst 1h, SYM-H 1min, AE 1min)·동일 시각 정렬(UTC). 지수 산출 규약(관측소 세트·기준선 baseline·태양정온일 Sq 제거)이 관측·모델 간 동일해야 함. 결측·데이터 갭 제거.
- 해석 기준(advisory): RMSE는 **정온기보다 폭풍 주경(main phase)에서 급증**하며, 큰 폭풍 사례에서 Dst RMSE 수십 nT 규모 보고(사례값; 절대기준 아님). 지수·리드타임·폭풍강도에 따라 크게 변하므로 반드시 조건 명시. RMSE 단독 판단 금지 → PE·R²·사건탐지 병행(Liemohn et al. 2018 권고).
- 한계·주의(§G): RMSE는 진폭이 큰 폭풍에 지배됨 → 정온기 성능을 가림. persistence(지속예보)·climatology 기준 스킬과 비교하지 않으면 "낮은 RMSE=좋음"이 착시일 수 있음(§G-6 단일지표 금지). 지수 재산출 버전(예: real-time vs final Dst)이 다르면 인위적 오차.
- 출처: Liemohn, M. W. et al. (2018) "Model Evaluation Guidelines for Geomagnetic Index Predictions," *Space Weather*, 16(12), 2079–2102, doi:10.1029/2018SW002067; Liemohn et al. (2021, *Space Weather*, RMSE·R² 보완 논의); WDC for Geomagnetism, Kyoto (Dst/AE 산출).

---

### prediction efficiency (PE) / 결정계수 R²
- 무엇을 측정/검증하나: 모델이 관측의 **분산을 얼마나 설명**하는지 — persistence/평균 대비 실질 스킬. RMSE가 못 주는 "설명력"을 정규화된 0~1(음수 가능) 스케일로 제시. 우주기상(특히 Dst) 검증의 표준 스킬지표.
- 정의·수식: PE = 1 − Σ(oᵢ−mᵢ)² / Σ(oᵢ−ō)² (관측 평균 기준으로 정규화한 잔차분산). 형태상 Nash–Sutcliffe efficiency·R²(결정계수)와 동일 골격(→ NSE는 `08`/수문 카드, 여기선 우주기상 관행명 PE 사용). PE=1 완전, PE=0 평균예측 수준, PE<0 평균보다 못함. 관측 표준편차 대비 오차 정규화 형태 PE = 1 − (RMS/SD)² 로도 표기.
- 적용 도메인/자료형: Dst/SYM-H/AE·TEC·태양풍 성분 [시계열].
- 입력·전제: 정렬 매치업. 기준(평균 vs persistence) 명시 — persistence를 기준분모로 쓰면 Skill Score(SS)로 부름. 자기상관 강한 시계열은 유효표본 보정 필요.
- 해석 기준(advisory): PE↑ 양호. 폭풍기 PE는 큰 변동 덕에 정온기보다 높게(후하게) 나올 수 있음(분모 팽창) → 정온/폭풍 분리 보고. persistence 기준 SS>0이어야 실질 예측가치.
- 한계·주의(§G): R²(상관제곱, association)와 PE/NSE(bias·기울기 반영)는 **다른 양** — 혼동 금지. Liemohn et al.(2018)은 PE·R²·상관을 함께 볼 것을 권고. 계절·태양주기 변동 큰 자료에서 분모가 커져 점수가 과하게 후해짐.
- 출처: Liemohn et al. (2018), doi:10.1029/2018SW002067; Nash & Sutcliffe (1970, *J. Hydrology* — 효율 원형); 우주기상 Dst 예측 논문 다수(PE·SS 관행).

---

### Kp / ap 이산·준로그 지수 검증
- 무엇을 측정/검증하나: 3시간 간격 준로그 지수 Kp(0~9, 1/3 단계 28수준)와 선형화 등가 ap의 예측 일치. Kp는 계단형·비선형이라 연속지표를 그대로 쓰면 왜곡.
- 정의·수식: Kp 매치업에 MAE·RMSE(Kp 단위, 1/3 단계)와 ±1 Kp 이내 적중률. **Kp는 준로그** → 물리 진폭 비교는 선형 ap(nT 등가)로 변환 후 RMSE 권장. 폭풍 임계(Kp≥5 minor storm, ≥7 strong)는 사건탐지 카드로.
- 적용 도메인/자료형: Kp/ap 예측 모델 [시계열](3h). GFZ Potsdam 공식 Kp/ap 기준.
- 입력·전제: 3시간 UTC bin 정렬. Kp의 이산·비선형성 고려(연속 RMSE 해석 주의). nowcast(추정) vs forecast Kp 구분.
- 해석 기준(advisory): Kp MAE ~0.5~1.0 단위 규모가 흔히 보고되나 극대기·폭풍기에 악화(사례값; 절대기준 아님). ±1 Kp 적중률 병행.
- 한계·주의(§G): Kp를 선형 연속량처럼 평균/RMSE 하면 준로그 왜곡 → ap 변환 병행. 3시간 지수라 급변(SSC) timing은 못 잡음(별도 timing 카드). bootstrap CI 동반(→01).
- 출처: Matzka et al. (2021, *Space Weather*, Kp/ap 정의·GFZ); Liemohn et al. (2018), doi:10.1029/2018SW002067; 확률 Kp 예보 검증 논문(예: Kp probabilistic prediction, *JSWSC* 2020).

---

### 지자기폭풍 사건 탐지 (임계 초과 분할표: HSS·POD·FAR·CSI)
- 무엇을 측정/검증하나: "폭풍 임계(예: Dst ≤ −50 nT moderate, ≤ −100 nT intense; Kp ≥ 5)를 넘었는가"라는 이진 사건을 모델이 맞히는지. 연속오차가 못 주는 운영 경보 관점.
- 정의·수식: 2×2 분할표(hit a, false alarm b, miss c, correct-negative d) → POD=a/(a+c), FAR=b/(a+b), CSI=a/(a+b+c), **HSS(Heidke Skill Score)**=우연 대비 개선(HSS=1 완전, 0 무스킬), bias score=(a+b)/(a+c). 정의 전체는 `03_categorical_event_extremes.md`.
- 적용 도메인/자료형: Dst/SYM-H/Kp 임계 사건 [시계열]→[사건]. 우주기상 모델 검증의 event-detection 축(Liemohn et al. 2018).
- 입력·전제: 합의된 임계·시간 매칭 윈도(사건은 지속시간 있음 → 순간초과 vs 사건단위 정의 명시). 극한 폭풍은 사건 희소 → 표본 부족.
- 해석 기준(advisory): HSS↑·POD↑·FAR↓ 양호. 임계가 강할수록(intense storm) 사건 희소 → 점수 불안정·climatology 기준 필요. 단일 임계 결론 금지 → 여러 임계·ROC 병행.
- 한계·주의(§G): 희소사건에서 HSS/CSI 불안정 → SEDI/TSS 등 base-rate 강건 지표 병행(→03). 사건 정의(순간 vs 사건단위)·매칭 윈도가 점수를 좌우. bootstrap CI 필수.
- 출처: Liemohn et al. (2018), doi:10.1029/2018SW002067; Jolliffe & Stephenson, *Forecast Verification* (분할표 표준); Sharpe & Murray (2017, *Space Weather*, Met Office 우주기상 예보 검증).

---

### 폭풍 개시·급시작(SSC) timing 오차
- 무엇을 측정/검증하나: 폭풍 급시작(sudden storm commencement)·주경 저점(main phase minimum) 등 **사건 발생 시각**을 모델이 얼마나 정확히 맞히는지(진폭이 아니라 위상). 운영 경보 리드타임 평가의 핵심.
- 정의·수식: timing error Δt = t_model_event − t_obs_event(개시·저점 각각). 통계: 평균 timing bias, |Δt| MAE, 표준편차. 사건별 검출은 임계교차·저점탐색 알고리즘으로 정의. 진폭오차(peak Dst 차)와 함께 보고.
- 적용 도메인/자료형: Dst/SYM-H 저점 timing, SSC 개시 timing [시계열]→[사건].
- 입력·전제: 개시·저점 검출 규약 통일(임계·평활·최소 지속). 관측·모델 동일 시간분해. 다중 저점(2단 폭풍)의 매칭 규칙 명시.
- 해석 기준(advisory): timing bias(선행/지연)와 |Δt| MAE(시간 단위)로 보고. 리드타임·폭풍유형(CME vs CIR)에 강하게 의존 → 조건 명시. good/bad 단정 금지.
- 한계·주의(§G): 진폭 RMSE가 좋아도 timing이 크게 어긋날 수 있음(위상-진폭 분리 필요) → DTW 카드 병행. 저점이 편평하거나 다봉이면 검출 모호. 사건 수 적으면 통계 불안정(bootstrap).
- 출처: Liemohn et al. (2018), doi:10.1029/2018SW002067; Pulkkinen et al. (2013, *Space Weather*, GIC/ dB/dt 검증에서 timing·spatial 평가); 교차상관/위상오차 일반론은 `06_timeseries_signal.md`.

---

### 동적시간왜곡 (Dynamic Time Warping, DTW) — Dst 위상평가
- 무엇을 측정/검증하나: 예측·관측 시계열을 비선형 시간정렬해 **형상(shape) 일치와 시간지연(lag)을 동시에** 평가. point-wise RMSE가 벌하는 "위상만 어긋난 좋은 형상"을 공정하게 채점. Dst/SYM-H 예측 평가에 도입됨.
- 정의·수식: DTW distance = 최적 정렬 경로 상의 누적 국소거리 최소값. 정렬 경로에서 timing shift(warping amount) 추출 → 형상거리와 위상오차 분리. 일반 정의·제약(Sakoe–Chiba band)은 `06_timeseries_signal.md`.
- 적용 도메인/자료형: Dst/SYM-H/AE·태양풍 [시계열]. ML Dst 예측 벤치마킹.
- 입력·전제: 시계열 정규화(진폭 스케일)·window 제약 설정. 인접점 정렬 허용범위(band)를 물리적으로 타당하게 제한(과도한 warping 방지).
- 해석 기준(advisory): DTW distance↓ 양호, 추출된 warping이 작을수록 위상 정확. RMSE와 병행해 "형상 vs 타이밍" 진단.
- 한계·주의(§G): DTW는 과도 warping 시 물리적으로 비현실적 정렬을 허용 → band 제약 필수. 절대 진폭오차는 별도 지표로. 표준 스킬임계 없음(상대비교용).
- 출처: Laperre, Amaya & Lapenta (2020) "Dynamic Time Warping as a New Evaluation for Dst Forecast With Machine Learning," *Frontiers in Astronomy and Space Sciences*, 7:39, doi:10.3389/fspas.2020.00039.

---

### AE / AL / AU 오로라대 전류지수 검증
- 무엇을 측정/검증하나: 오로라대 전기제트(electrojet) 강도 지수 AE(=AU−AL)·AL(하한)·AU(상한)의 예측 일치. substorm 활동·고위도 에너지 유입 지표.
- 정의·수식: 1분 분해 AE/AL/AU에 RMSE·MAE·bias·상관(→01). substorm onset은 AL 급강하 사건탐지로(분할표). AL은 음의 큰 값(강한 서향 전류)이 중요.
- 적용 도메인/자료형: 오로라대 관측소망 유도 지수 [시계열] vs 모델. IMAGE/SuperMAG 확장 지수(SME/SML)도 대조군.
- 입력·전제: 관측소 커버리지(경도 공백)·지수 산출 규약 통일. AE는 관측소 세트 의존성 큼(공식 12소 AE vs SuperMAG SME 차이) → 기준 명시.
- 해석 기준(advisory): 급변(substorm)에서 RMSE·timing 오차 급증. 고분해 1분 지수라 위상오차 민감 → DTW/교차상관 병행.
- 한계·주의(§G): AE는 지상망 밀도·경도분포에 강하게 의존 → 관측 자체 불확실성 큼(대표성). 공식 AE와 SuperMAG SME 혼용 금지(정의 다름).
- 출처: WDC Kyoto (AE 산출); Newell & Gjerloev (2011, *JGR*, SuperMAG SME/SML); Liemohn et al. (2018), doi:10.1029/2018SW002067.

---

### 태양풍 시계열 검증 (V, n, Bz, IMF clock angle)
- 무엇을 측정/검증하나: 태양풍 속도 V, 밀도 n, 행성간자기장(IMF) 성분 특히 Bz(GSM), clock angle의 모델(태양풍 전파모델/CME 시뮬레이션 WSA-ENLIL 등) 대 L1 관측(ACE/DSCOVR/Wind) 일치. 지자기폭풍 구동 입력의 정확도.
- 정의·수식: V·n·Bz에 RMSE·MAE·bias·상관(→01). Bz는 부호(남향 Bz<0가 지자기활동 구동)가 핵심 → 부호 적중·남향 지속시간 사건 평가. IMF clock angle θ=atan2(By,Bz)는 원형변수 → 원형통계(→07 풍향 카드 방식 참조: wrap·원형 RMSE).
- 적용 도메인/자료형: L1 관측 [시계열] vs 태양풍 예측 [시계열]. CME 도달 후 sheath/ejecta 구조 비교.
- 입력·전제: L1→모델 좌표·시간 정렬. 자기장 좌표계(GSM vs GSE) 통일. clock angle은 원형변수(0/360 wrap 처리 필수).
- 해석 기준(advisory): V·n은 CIR/CME 통과 시 급변 → 진폭·timing 분리. **Bz는 본질적으로 예측난도 최고**(작은 스케일 요동) → RMSE 크게 나오는 것이 정상; 남향 이벤트 탐지·지속시간이 실용 지표. 절대기준 강요 금지.
- 한계·주의(§G): Bz를 직선 통계로만 보면 부호·구조를 놓침. clock angle 직선 RMSE 금지(원형통계). L1→magnetopause 전파지연(아래 카드)을 정렬하지 않으면 인위적 오차.
- 출처: Owens et al. (2008, *Space Weather*, 태양풍 예측 검증); Liemohn et al. (2018), doi:10.1029/2018SW002067; 원형통계 일반론은 `07_domain_meteorology.md`(풍향)·`10`(유향).

---

### 태양풍 도달시각/전파 오차 (L1→magnetopause propagation lag)
- 무엇을 측정/검증하나: L1(약 150만 km 상류) 관측·모델 태양풍이 지구 자기권계면(magnetopause)에 도달하는 **전파지연(lag)** 을 모델이 정확히 재현하는지. 지수예측 입력정렬의 전제.
- 정의·수식: 표준 전파는 flat-delay(Δt=X_L1/Vx) 또는 최소분산·상평면(minimum variance / phase-front) 기법. 검증은 예측 lag vs 실제 도달(자기권 응답 개시) timing 오차, 또는 정렬 후 잔차상관 개선량.
- 적용 도메인/자료형: L1 [시계열] → 지구 응답 [시계열] 정렬. 태양풍 전파 알고리즘 평가.
- 입력·전제: 위성 위치(X_GSE)·속도 성분. 상평면 방법은 자기장 불연속면 기울기 가정. 급경사 불연속(CME sheath)에서 flat-delay 오차 큼.
- 해석 기준(advisory): lag 오차 수 분~수십 분 규모(구조·기법 의존). 정렬 후 지수예측 상관 개선으로 간접 평가. 절대 임계 없음(상대비교).
- 한계·주의(§G): 부정확한 lag는 뒤따르는 모든 지수검증 오차로 전파 → 정렬을 먼저 검증. 상평면 방법은 평면파 가정 위배 시 실패. 위성 궤도 위치오차 반영.
- 출처: Weimer et al. (2003, *JGR*, phase-front propagation); Mailyan et al. (2008, *Ann. Geophys.*, 태양풍 전파기법 비교); 교차상관 시간정렬 일반론 `06_timeseries_signal.md`.

---

### CME/충격파 도달시각 오차 (arrival time error ΔtA)
- 무엇을 측정/검증하나: 코로나질량방출(CME)·행성간충격파의 지구(또는 L1) **도달시각**을 모델(WSA-ENLIL+Cone, 드래그기반 DBM, ML 등)이 얼마나 정확히 예측하는지. 우주기상 조기경보의 대표 지표.
- 정의·수식: arrival time error ΔtA = t_predicted − t_observed(양수=지연예측). 통계: mean error(bias), MAE=mean|ΔtA|, 표준편차. CCMC CME scoreboard가 다중 모델 매치업으로 집계.
- 적용 도메인/자료형: CME 사건별 [사건](관측 도달=충격파/ICME 개시 timing) vs 모델 예측. WSA-ENLIL+Cone, DBM, 통계·ML 모델.
- 입력·전제: "도달" 정의 통일(충격파 도착 vs ICME 개시). 관측 도달은 L1 태양풍 급변으로 식별. hit인 사건만 timing 통계(miss/false는 사건탐지 카드 별도).
- 해석 기준(advisory): 다중모델 종합 MAE 약 **10시간 규모**(Riley et al. 2018: MAE≈10 h, RMSE>20 h; Wold et al. 2018 WSA-ENLIL+Cone: ME −4.0 h, MAE 10.4 h; Kay et al. 2024 갱신 표본: bias −2.5 h, MAE 13.2 h, SD 17.4 h — 모두 사례/표본값, 절대기준 아님). 표본·기간·모델에 따라 변동 큼.
- 한계·주의(§G): 표본 편향(강한 CME·hit만 집계 시 낙관 편향)·도달 정의 불일치가 통계를 좌우. hit 통계만 보고 miss/false 무시 금지 → 도달 사건탐지 카드 병행. 소표본 → bootstrap CI.
- 출처: Riley, P. et al. (2018) "Forecasting the Arrival Time of Coronal Mass Ejections: Analysis of the CCMC CME Scoreboard," *Space Weather*, 16(9), 1245–1260, doi:10.1029/2018SW001962; Wold et al. (2018, *JSWSC* 8:A17, WSA-ENLIL+Cone 실시간 검증); Kay, C. & Palmerio, E. (2024) "Updating Measures of CME Arrival Time Errors," *Space Weather*, doi:10.1029/2024SW003951 (권·페이지 확인요).

---

### CME 도달 사건 탐지 (hit / miss / false alarm)
- 무엇을 측정/검증하나: CME가 **지구에 도달하는가/안 하는가**(및 예측 여부)를 분할표로 평가 → timing 오차와 별개로 "예측한 CME가 실제 왔나, 온 CME를 예측했나".
- 정의·수식: hit(예측O·관측O), miss(예측X·관측O), false alarm(예측O·관측X), correct-negative. POD·FAR·CSI·HSS·bias(→03). glancing blow(측면 스침)·arrival window 정의가 판정에 영향.
- 적용 도메인/자료형: CME 사건목록 [사건]. CCMC scoreboard·운영 예보.
- 입력·전제: "도달" 판정 기준(중심 hit vs glancing)·관측 진리목록(catalogue) 합의. 예측·관측 CME 매칭 규칙.
- 해석 기준(advisory): FAR가 높은 경향(오지 않은 CME 과다예측) 보고됨 — 운영 경보 부담. POD/FAR trade-off 명시.
- 한계·주의(§G): catalogue 불완전(약한 CME 누락)·glancing 판정 주관성이 큰 불확실성. timing(hit만)과 반드시 함께 보고. 소표본.
- 출처: Riley et al. (2018), doi:10.1029/2018SW001962; Verbeke et al. (2019, *Space Weather*, CME 도달 검증 metric 논의); 분할표 표준 `03_categorical_event_extremes.md`.

---

### 전리층 TEC 검증 (bias / RMSE, TECU)
- 무엇을 측정/검증하나: 모델(경험 IRI/NeQuick, 물리 WAM-IPE/TIE-GCM, 동화 GloTEC 등)이 산출한 총전자량 TEC(수직 VTEC)가 지상 GNSS 유도 TEC와 얼마나 일치하는지. 전리층 검증의 1차 지표.
- 정의·수식: 매치업에 ME(bias), RMSE, MAE(단위 TECU=10¹⁶ el/m²), 상관(→01). 4범주(accuracy=RMSE, bias=ME, association=R, precision) 프레임(CCMC/SWPC 관행). ME<0=모델 과소, >0=과대.
- 적용 도메인/자료형: 모델 VTEC [격자]/[정점] vs GNSS 지상 VTEC [정점]/[격자 GIM]. 15분~1시간 분해.
- 입력·전제: GNSS TEC의 위성·수신기 편이(DCB) 보정·매핑함수(사각 STEC→VTEC) 규약 통일. 동일 시각·격자점 보간. 지방시(LT)·지자기위도 층화 권장.
- 해석 기준(advisory): RMSE는 **주야·위도·태양활동에 강하게 의존** — 야간 저활동 1~2 TECU, 주간 고활동 4~5 TECU 규모 보고(사례값). 폭풍 주경에 RMSE 증가·회복기 감소 경향(모델별 상이). 적도 이상대(EIA)에서 오차 최대. 조건 없는 단일 RMSE 해석 금지.
- 한계·주의(§G): GIM(격자 TEC)은 이미 보간·동화 산물 → 독립 진값 아님(§G-1,3), TC 등 무상관 가정 기법에 넣지 말 것. DCB 보정 오차가 bias로 위장. 매핑함수 가정(얇은 층 고도)이 저앙각에서 오차.
- 출처: Chou, M.-Y. et al. (2023) "Validation of Ionospheric Modeled TEC in the Equatorial Ionosphere During the 2013 March and 2021 November Geomagnetic Storms," *Space Weather*, 21, doi:10.1029/2023SW003480; CCMC/SWPC GloTEC 검증(accuracy/bias/association/precision 프레임); IGS GIM 산출 관행.

---

### 글로벌 TEC 지도(GIM) 격자-격자 공간비교
- 무엇을 측정/검증하나: 모델 [격자] TEC를 참조 GIM(IGS/JPL/CODE) [격자]와 **공간 전면적으로** 비교해 bias/RMSE/상관의 지리·지방시 분포를 지도화. 점 관측 없는 해역·극지까지 계통오차 위치 진단.
- 정의·수식: 공통 격자로 재격자화 후 격자점별 시간계열에 bias(lat,lon)·RMSE·R → 색지도. 지자기위도·지방시(LT) 축 재구성(적도이상대·중위도 홈·오로라대 구조 확인). 공간패턴 일치는 ACC/패턴상관(→02).
- 적용 도메인/자료형: 모델 VTEC [격자] vs GIM [격자]. NetCDF↔IONEX.
- 입력·전제: 좌표·시각·달력 정렬, TECU 단위·격자 정의 통일. GIM 자체 불확실성(관측 sparse 해역 보간 오차) 인지.
- 해석 기준(advisory): 계통 bias 띠(적도이상대 crest 과소/과대, 야간 과대 등)의 위치·지방시·계절성 파악. 지도에서 EIA·주야 경계 구조 재현 여부.
- 한계·주의(§G): GIM은 "정답"이 아니라 또 하나의 동화 산물 → 과신 금지(§G-1). 해양·극지 GIM은 관측 부족으로 자체 오차 큼 → 그 영역 차이는 GIM 오차일 수 있음. 재격자화 보간 산물 주의.
- 출처: Hernández-Pajares et al. (2009, *J. Geodesy*, IGS GIM); Chou et al. (2023), doi:10.1029/2023SW003480; 격자-격자 비교 일반론 `01`·`02`.

---

### 차분 STEC (dSTEC) 검증
- 무엇을 측정/검증하나: 위성·수신기 편이(DCB)·상수 offset에 오염된 절대 TEC 대신, **한 위성 pass 내 최고앙각 기준 상대 slant TEC 변화(dSTEC)** 로 모델을 검증 → offset 오차 제거하고 시공간 gradient 재현력 평가.
- 정의·수식: dSTEC(t) = STEC_obs(t) − STEC_obs(t_ref) 를 모델의 동일 차분과 비교(RMSE, TECU). t_ref는 pass 내 최고앙각(오차 최소) 시각. 절대 편이 소거.
- 적용 도메인/자료형: 관측소별 GNSS pass [정점] vs 모델 slant TEC. GIM/모델 정확도의 offset-무관 평가.
- 입력·전제: 위성 pass별 최고앙각 식별, 사이클슬립 제거. 모델 STEC는 시선방향 적분(매핑함수 아님)으로 산출.
- 해석 기준(advisory): dSTEC RMSE가 낮으면 상대변화(구배) 재현 양호 — 절대 bias와 분리 해석. 개선사례 최대 ~20% 보고(방법 비교; 사례값).
- 한계·주의(§G): dSTEC는 상대변화만 평가 → 절대 TEC bias는 못 봄(절대검증 병행). pass 짧으면 통계 빈약. 매핑함수 미사용이라 slant 적분 정확도 필요.
- 출처: Hernández-Pajares et al. (2017, *J. Geodesy*, dSTEC 검증법); 최근 PPP+IRI 가상국 결합 검증(dSTEC 19.8% 개선, *Adv. Space Res.* 계열, 권·페이지 확인요).

---

### 전리층 위성 검증 (radio occultation · altimeter VTEC)
- 무엇을 측정/검증하나: 지상 GNSS가 없는 해양·극지까지 위성으로 전리층 모델 검증 — GNSS radio occultation(COSMIC/COSMIC-2)의 전자밀도 프로파일·NmF2·hmF2, 위성고도계(Jason/Sentinel) 이중주파 VTEC.
- 정의·수식: RO NmF2/hmF2·프로파일에 bias/RMSE(→01), 고도계 VTEC(위성-전리층 사이 적분)에 bias/RMSE. 위성 대조는 `12_satellite_remote_sensing.md`(매치업·대표성오차) 연결.
- 적용 도메인/자료형: RO [프로파일]·altimeter [트랙] vs 모델 [격자].
- 입력·전제: RO는 국소구형대칭(Abel inversion) 가정 → 수평구배 큰 곳(EIA·오로라대) 오차. altimeter VTEC는 위성 아래(해양)만·plasmasphere 상부 제외분 고려.
- 해석 기준(advisory): RO/altimeter는 지상 GNSS와 상보(공간 커버리지 넓음, 정확도는 상황 의존). 위도·지방시 층화 필수.
- 한계·주의(§G): RO Abel 가정 위배(수평구배)·altimeter 대양 한정·상부 plasmasphere 미포함 → 절대값 직접비교 시 주의. 위성 대표성오차(→12).
- 출처: Chou et al. (2023), doi:10.1029/2023SW003480; COSMIC/COSMIC-2 전리층 검증 논문; 위성 매치업 일반론 `12_satellite_remote_sensing.md`.

---

### foF2 / hmF2 / NmF2 임계주파수 검증 (ionosonde)
- 무엇을 측정/검증하나: 전리층 F2층 임계주파수 foF2(∝√NmF2), 최대전자밀도 고도 hmF2를 수직탐측기(ionosonde) 관측과 대조 → TEC(적분량)가 못 주는 층상 구조·피크 재현.
- 정의·수식: foF2(MHz)·hmF2(km)·NmF2에 bias/RMSE/상관(→01). foF2·NmF2 관계 NmF2 ∝ foF2². M(3000)F2 factor 유도 hmF2 규약 통일.
- 적용 도메인/자료형: ionosonde 관측소 [정점] vs 모델 프로파일. IRI/물리모델 검증 핵심.
- 입력·전제: ionosonde 자동 스케일링 품질(수동검수)·관측소망 분포. 폭풍기 확산 F(spread-F)로 스케일 실패.
- 해석 기준(advisory): foF2는 태양활동·지방시·위도 의존 강함. 폭풍기 음/양의 storm effect 재현 여부. 중위도보다 적도·고위도 오차 큼.
- 한계·주의(§G): 자동 스케일 오류가 관측 오차로 유입. 관측소 sparse(특히 해양·남반구). TEC과 foF2는 다른 양(적분 vs 피크) — 함께 봐야 층상 진단.
- 출처: Bilitza et al. (2017, *Space Weather*, IRI 모델·검증); ionosonde 스케일링 URSI 규약; 관련 TEC 검증 Chou et al. (2023).

---

### F10.7 / 태양복사플럭스 예측 검증 (sfu)
- 무엇을 측정/검증하나: 10.7 cm 태양전파플럭스 F10.7(태양활동·상층대기 가열 대리지표)의 예측(리드타임 1일~수개월~수년)이 관측(DRAO Penticton)과 일치하는지. 대기항력·전리층 모델의 핵심 구동입력.
- 정의·수식: 리드타임별 RMSE·MAE·bias(단위 sfu=10⁻²² W m⁻² Hz⁻¹), 상관(→01). 27일 태양자전 주기 위상 재현(→ 주기 카드). persistence/climatology 기준 스킬 비교.
- 적용 도메인/자료형: F10.7 예측 [시계열] vs 관측. adjusted vs observed flux 구분.
- 입력·전제: adjusted(1 AU 보정) vs observed 통일, UTC 정렬. 결측·플레어 전파버스트 오염 제거.
- 해석 기준(advisory): 중기(월단위) RMSE 약 5~27 sfu 규모 보고(Kalman filter 사례; 리드타임 길수록 증가; 절대기준 아님). 극대기 변동 큼 → 조건 명시. 27일 위상 예측이 실용 스킬.
- 한계·주의(§G): 장기예측은 태양주기 예측 불확실성에 지배 → climatology 대비 스킬로 평가. F10.7 단독으로 EUV 완전대리 아님(스펙트럼 차이). persistence 기준 필수.
- 출처: Petrova et al. (2021) "Medium-term Predictions of F10.7 and F30 cm Solar Radio Flux with the Adaptive Kalman Filter," *ApJS* 254, doi (확인요); NOAA SWPC 45-day Ap/F10.7 forecast; ISES 태양주기 예측 관행.

---

### 태양플레어 확률예보 검증 (Brier · ROC · reliability)
- 무엇을 측정/검증하나: 태양플레어(C/M/X급) 발생 **확률예보**의 신뢰도(reliability)·판별력(ROC)·정확도(Brier). 결정론 지표로 못 보는 확률 품질. 우주기상 확률예보 검증의 대표.
- 정의·수식: Brier Score BS·BSS, reliability diagram, ROC/AUC, TSS(True Skill Statistic)(정의는 `03_categorical_event_extremes.md`). 플레어는 희소·불균형 사건 → base-rate 강건 지표(TSS·SEDI) 중시.
- 적용 도메인/자료형: 플레어 확률예보 [시계열]/[사건] vs GOES X선 플럭스 관측. RWC/운영기관 예보.
- 입력·전제: 임계(≥M1.0, ≥X1.0)·예보 유효기간(24h 등) 통일. 사건 불균형 심함(X급 극희소).
- 해석 기준(advisory): BSS>0·AUC>0.5·TSS>0이면 climatology/무스킬보다 우수. 희소 X급은 점수 불안정 → CI 필수. 여러 임계 병행.
- 한계·주의(§G): 불균형 사건에서 accuracy·Brier가 base-rate에 지배됨 → TSS/SEDI 병행(§G-6). reliability는 표본 많은 확률구간만 신뢰. 예보-관측 사건 정의 통일.
- 출처: Kubo, Den & Ishii (2017) "Verification of operational solar flare forecast: Case of RWC Japan," *JSWSC* 7:A20; Bloomfield et al. (2012, *ApJL*, TSS 플레어 검증 권고); Jolliffe & Stephenson (확률검증 표준).

---

### 드문 사건 스킬 (TSS · SEDI · ETS · climatology 기준)
- 무엇을 측정/검증하나: 극한 지자기폭풍·강한 플레어·SEP 등 **희소 사건**에서 base-rate에 강건한 스킬. 일반 HSS/CSI가 희소사건에서 불안정·오해를 주는 문제 보완.
- 정의·수식: TSS(=POD−POFD, Peirce), SEDI(Symmetric Extremal Dependence Index), ETS(Gilbert Skill Score) — 정의 전체 `03_categorical_event_extremes.md`. climatology·persistence를 기준 예보로 skill score 산출.
- 적용 도메인/자료형: Dst≤−250 nT(great storm)·X급 플레어·SEP 사건 [사건].
- 입력·전제: 충분한 사건 수 확보(어려움) → 장기간 표본·bootstrap. base-rate 명시.
- 해석 기준(advisory): TSS·SEDI가 base-rate 무관하게 판별력 반영 → 희소사건 우선. climatology 기준 SS>0 확인.
- 한계·주의(§G): 극희소 사건은 어떤 지표도 표본에 민감 → CI 폭 넓음 명시. 단일 지표·단일 임계 결론 금지.
- 출처: Ferro & Stephenson (2011, *Weather and Forecasting*, SEDI); Bloomfield et al. (2012, TSS); 우주기상 극한사건 검증 관행; 극값 통계는 `03_categorical_event_extremes.md`.

---

### 확률·앙상블 우주기상 검증 (CRPS · rank histogram)
- 무엇을 측정/검증하나: 앙상블/확률 우주기상 예보(예: 확률 Kp, 앙상블 Dst, 앙상블 태양풍/CME) 의 신뢰도·해상도·예리함·spread 적정성. 결정론 지표로 못 보는 불확실성 표현 품질.
- 정의·수식: CRPS(+분해)·CRPSS, Brier/BSS, rank histogram(Talagrand), spread–skill — 정의는 `03_categorical_event_extremes.md`·`figures/16`.
- 적용 도메인/자료형: 앙상블 Kp/Dst/태양풍 [시계열]/[사건].
- 입력·전제: 앙상블 멤버 전체 또는 예보 분포. 관측 결정론 진값. 충분 사례.
- 해석 기준(advisory): CRPS↓·CRPSS>0 양호. rank histogram 평탄=적정 spread, U자=과소분산, ∩자=과대분산. 확률 Kp 예보에 적용 사례 있음.
- 한계·주의(§G): 결정론 단일모델엔 부적용(앙상블 전용). 희소 극단에서 불안정. spread가 관측대표성오차를 포함하는지 유의.
- 출처: Hersbach (2000, *Weather and Forecasting*, CRPS); 확률 Kp 예측(예: *JSWSC* 2020, "Probabilistic prediction of geomagnetic storms and the Kp index"); `03`·`figures/16` 교차.

---

### 분포·QQ 비교 (Dst / TEC 분포·꼬리)
- 무엇을 측정/검증하나: 모델·관측 Dst(또는 TEC/AE) 분포 전체·특히 **극한 꼬리**(강한 폭풍·고 TEC) 재현. 평균 지표가 못 잡는 분포 편향.
- 정의·수식: QQ-plot(분위수 대응)·PDF/CDF 중첩·KS 통계량 — 정의는 `01_error_statistics.md`·`figures/16`. Dst 음의 꼬리(강폭풍)·TEC 상위 꼬리 집중 점검.
- 적용 도메인/자료형: 장기 통계(기후) 검증. 시간정렬 불필요. [시계열]/[격자].
- 입력·전제: 동일 기간·모집단. 자기상관 강한 시계열 → 유효표본 보정(KS 과민).
- 해석 기준(advisory): 상위/하위 분위수에서 1:1선 이탈로 극값 과소/과대 진단(모델은 극한 폭풍 과소 경향 흔함). QQ는 분포만(동시성 못 봄).
- 한계·주의(§G): 자기상관으로 KS가 거의 항상 "유의" → 신중. 극단 분위수 표본 빈약. quantile mapping 보정 진단에도 사용.
- 출처: Wilks (교과서); `01_error_statistics.md`·`figures/16` 교차링크.

---

### 극한 지자기 사건 통계 (GEV / POT return level)
- 무엇을 측정/검증하나: 모델이 극한 지자기 사건(예: 100년 재현 최소 Dst, 극한 dB/dt GIC 위험)의 통계·재현주기를 관측과 일치시키는지. 위험평가·인프라 설계용.
- 정의·수식: 연최소 Dst → GEV, 임계초과(POT) → GPD, 재현레벨(return level) — 단일 극값 엔진은 `03_categorical_event_extremes.md`. Dst는 음의 극값(최소) → 부호 반전 후 적합.
- 적용 도메인/자료형: 장기 지자기 hindcast·dB/dt [시계열] vs 장기 관측.
- 입력·전제: 충분히 긴 동질 기간(태양주기≥1~2), 사건 독립성(declustering), 비정상성(태양주기) 고려.
- 해석 기준(advisory): 재현레벨(50/100년) 모델-관측 신뢰구간 겹침. QQ로 꼬리 적합. 모델 극값 과소 경향 흔함.
- 한계·주의(§G): 임계·declustering·표본에 큰 민감도(불확실성 큼). 태양주기 비정상성 무시 위험. bootstrap CI 필수. dB/dt(GIC)는 공간·timing 검증 별도(Pulkkinen 2013).
- 출처: Coles (2001, *Statistical Modeling of Extreme Values*); Pulkkinen et al. (2013, *Space Weather*, GIC/dB/dt 검증); 극값 통계 `03_categorical_event_extremes.md`.

---

### 주기·계절 위상 검증 (27일 자전 · 연 · 태양주기)
- 무엇을 측정/검증하나: 우주기상 변수의 준주기 성분 — 27일 태양자전(F10.7·Kp의 재현성), 연·반년(전리층·지자기), 11년 태양주기 — 위상·진폭을 모델이 재현하는지.
- 정의·수식: PSD(Welch)·Lomb–Scargle(불규칙 표본)·cross-spectrum/coherence·위상오차 — 정의는 `05_spectral_eof_modal.md`·`06_timeseries_signal.md`. 27일 주기 대역 위상지연·coherence 집중.
- 적용 도메인/자료형: F10.7·Kp·TEC·Dst [시계열]. 장기 hindcast 기후검증.
- 입력·전제: detrend·window·정규화 통일(모델·관측 동일). 결측 시 Lomb–Scargle. 태양주기 비정상성 주의.
- 해석 기준(advisory): 27일 대역 coherence 높고 위상지연 작으면 자전 구동 재현 양호. 반년/연 변동(전리층) 위상 점검.
- 한계·주의(§G): 짧은 기간은 11년 주기 미분해. 비정상 스펙트럼(진폭 변동) 주의. 위상만/진폭만 결론 금지.
- 출처: `05_spectral_eof_modal.md`·`06_timeseries_signal.md`(PSD·Lomb–Scargle·coherence 정의); 우주기상 27일 주기 분석 관행.

---

### CCMC 검증 프레임워크·scoreboard (운영 표준)
- 무엇을 측정/검증하나: 다수 우주기상 모델을 공통 사건·공통 지표로 표준 검증·상호비교하는 기관 프레임워크(검증의 "표준화" 자체). NASA CCMC의 CME scoreboard·지자기지수·전리층(GloTEC 등) 검증, ISES RWC 운영검증.
- 정의·수식: 표준 지표 묶음 — 연속(RMSE·MAE·bias·PE·R)+사건(POD·FAR·HSS·CSI)+timing(ΔtA)+확률(Brier·ROC·CRPS). Liemohn et al.(2018)의 지자기지수 fit+event 이원 프레임, CCMC 4범주(accuracy/bias/association/precision) TEC 프레임.
- 적용 도메인/자료형: 다중 모델 [시계열]/[격자]/[사건] vs 공통 관측(WDC Kyoto 지수·IGS GIM·GNSS·L1 위성).
- 입력·전제: 공통 QC 관측·동일 매치업 규약·동일 사건목록. real-time vs final 지수·adjusted vs observed flux 구분. 모델간 동일 조건.
- 해석 기준(advisory): 기관 공통 기준으로 모델 순위·연도별 개선 추세 평가. 어떤 단일 지표도 순위 확정 금지 → 다지표 종합(Liemohn et al. 2018).
- 한계·주의(§G): 관측망 편중(고위도·해양 sparse)·사건목록 불완전·규약 차이가 비교 왜곡. 기준자료(GIM·재분석)는 진값 아님(§G-1). scoreboard 표본기간 편향 유의.
- 출처: Liemohn, M. W. et al. (2018), *Space Weather*, 16(12), 2079–2102, doi:10.1029/2018SW002067; Riley et al. (2018), doi:10.1029/2018SW001962 (CME scoreboard); NASA CCMC (ccmc.gsfc.nasa.gov, scoreboards·검증); ISES(spaceweather.org, RWC 검증).

---

## 출처 (References)

### 표준 참고문헌 / 지침 (실제 존재)
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (RMSE·MAE·bias·KS·QQ 표준 정의).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, Wiley (분할표·HSS·Brier·ROC·확률검증 표준).
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD, POT — 극한 지자기 사건).
- Nash, J. E. & Sutcliffe, J. V. (1970) "River flow forecasting through conceptual models part I," *Journal of Hydrology*, 10(3) (효율지표 원형 — PE/NSE 골격).

### 학술 논문 (웹으로 제목·저널·연도 확인됨; 권·페이지는 본문 병기, DOI는 확인분만 표기)
- Liemohn, M. W. et al. (2018) "Model Evaluation Guidelines for Geomagnetic Index Predictions," *Space Weather*, 16(12), 2079–2102. doi:10.1029/2018SW002067. (지자기지수 fit+event 검증 프레임 — 이 도메인의 핵심 지침; ADS bibcode 2018SpWea..16.2079L)
- Riley, P. et al. (2018) "Forecasting the Arrival Time of Coronal Mass Ejections: Analysis of the CCMC CME Scoreboard," *Space Weather*, 16(9), 1245–1260. doi:10.1029/2018SW001962. (CME 도달시각 다중모델 MAE≈10h)
- Wold, A. M. et al. (2018) "Verification of real-time WSA-ENLIL+Cone simulations of CME arrival-time at the CCMC from 2010–2016," *Journal of Space Weather and Space Climate*, 8, A17. (ME −4.0h, MAE 10.4h — 권·A번호 확인분)
- Kay, C. & Palmerio, E. (2024) "Updating Measures of CME Arrival Time Errors," *Space Weather*. doi:10.1029/2024SW003951. (bias −2.5h, MAE 13.2h, SD 17.4h; 권·페이지 확인요)
- Laperre, B., Amaya, J. & Lapenta, G. (2020) "Dynamic Time Warping as a New Evaluation for Dst Forecast With Machine Learning," *Frontiers in Astronomy and Space Sciences*, 7:39. doi:10.3389/fspas.2020.00039.
- Chou, M.-Y. et al. (2023) "Validation of Ionospheric Modeled TEC in the Equatorial Ionosphere During the 2013 March and 2021 November Geomagnetic Storms," *Space Weather*, 21. doi:10.1029/2023SW003480.
- Kubo, Y., Den, M. & Ishii, M. (2017) "Verification of operational solar flare forecast: Case of Regional Warning Center Japan," *Journal of Space Weather and Space Climate*, 7, A20. (플레어 확률검증)
- Matzka, J. et al. (2021) "The Geomagnetic Kp Index and Derived Indices of Geomagnetic Activity," *Space Weather*, 19. (Kp/ap 정의·GFZ — 권·페이지 확인요)
- Hersbach, H. (2000) "Decomposition of the continuous ranked probability score for ensemble prediction systems," *Weather and Forecasting*, 15(5), 559–570. (CRPS)
- Ferro, C. A. T. & Stephenson, D. B. (2011) "Extremal dependence indices," *Weather and Forecasting*, 26 (SEDI — 권·페이지 확인요).
- Pulkkinen, A. et al. (2013) "Community-wide validation of geospace model ground magnetic field perturbation predictions to support model transition to operations," *Space Weather*, 11. (dB/dt·GIC 검증·timing·spatial — 권·페이지 확인요)
- Bilitza, D. et al. (2017) "International Reference Ionosphere 2016," *Space Weather*, 15. (IRI foF2/hmF2 검증 — 권·페이지 확인요)

### 웹 자료 / 기관 프레임워크 (조사 시 직접 참조)
- NASA Community Coordinated Modeling Center (CCMC) — CME Scoreboard·지자기지수·전리층 검증: https://ccmc.gsfc.nasa.gov
- NOAA SWPC — 45-day Ap and F10.7 forecast, GloTEC: https://www.swpc.noaa.gov
- International Space Environment Service (ISES) — RWC 운영 예보·검증: http://www.spaceweather.org
- WDC for Geomagnetism, Kyoto — Dst/AE 지수 산출.
- IGS/CODE/JPL — Global Ionosphere Maps (GIM, IONEX).

### 확인요 (웹 1차 확인 못 했거나 정정 필요)
- Kay & Palmerio (2024) 및 Wold et al. (2018): DOI/권·A번호는 검색으로 제목·저널·연도·핵심수치 확인, 정확한 페이지·DOI는 인용 전 원문 재확인(확인요).
- Petrova et al. (2021, F10.7 Kalman filter, *ApJS* 254): 제목·저널·연도·RMSE 범위 확인, DOI 확인요.
- Matzka et al. (2021), Ferro & Stephenson (2011), Pulkkinen et al. (2013), Bilitza et al. (2017), Newell & Gjerloev (2011), Weimer et al. (2003), Owens et al. (2008), Hernández-Pajares et al. (2009/2017): 주제·저자·저널은 표준 인용이나 이 세션에서 권·페이지·DOI 전부 재확인은 못 함(확인요).
- 지자기지수(Kp/Dst/ap/AE/SYM-H)·F10.7·TEC 는 정식 CF standard_name 부재 사례가 많음 → 변수명·단위(nT/TECU/sfu) 기반 라우팅. TEC은 일부 데이터셋이 비표준 `tec`/`vtec`/`TEC` 이름 사용.

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(DOI는 이 세션에서 웹 확인된 것만 표기, 임의 생성 금지 원칙 준수). 해석 임계·사례 수치는 모두 특정 사건·표본·모델의 값으로 절대기준이 아니며(§G-4 advisory), 태양활동 위상·위도대·폭풍여부·리드타임 조건을 반드시 동반해 보고한다.
