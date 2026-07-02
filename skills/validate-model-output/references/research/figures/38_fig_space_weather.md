# 검증 시각화 카탈로그 — [우주기상 도메인편] (Verification Figures: Space Weather)

이 문서는 우주기상(space weather) 모델 산출물 — 지자기지수(Dst/SYM-H/Kp/ap/AE), 전리층 총전자량(TEC), 태양풍(V·n·Bz·clock angle), CME/충격파 도달, 태양플레어 확률, F10.7 — 을 **관측(WDC Kyoto 지수·GNSS/IGS GIM·L1 위성 ACE/DSCOVR/Wind·GOES X선·ionosonde)·경험모델·재분석**과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 우주기상 도메인편이다. 메서드(수치지표) 카드는 [`30_domain_space_weather.md`](../30_domain_space_weather.md)에 있고(**대응 메서드카탈로그: 30_domain_space_weather.md**), 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **공통/횡단 그림과의 분담**: Taylor·Target·일반 QQ·ROC·reliability·rank histogram·Brier/CRPS 분해·PDF/CDF·return-level 등 **도메인 무관 요약그림은 [공통편] [`16_fig_common.md`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않는다. 이 파일은 **우주기상 고유 그림**(Dst 폭풍 시계열+PE, CME 도달시각 오차 다이어그램, 전지구 TEC 지도, Kp 스택바, IMF clock angle 원형통계, dSTEC pass 등)과 **공통 그림의 우주기상식 변형**(플레어 확률 reliability, 폭풍임계 사건탐지 ROC, DTW 위상정렬)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "교차링크"에서 가리킨다.

> **자료형 약어**(30과 동일): [시계열]=관측소·L1위성 지수/성분 시계열(Dst 1h·SYM-H/AE 1min·태양풍 1min·TEC 15min) · [격자]=글로벌 TEC 지도(GIM)·전리층 격자 NetCDF · [정점]=단일 GNSS/지자기/ionosonde 관측소 · [사건]=폭풍/플레어/CME 도달 이벤트 목록 · [프로파일]=RO 전자밀도 프로파일 · [트랙]=고도계 along-track VTEC.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** WDC 지수·GIM·L1 관측·재분석은 모두 reference이지 truth가 아니다. **GIM은 이미 보간·동화 산물**이고(§G-1,3) real-time Dst는 나중에 final로 개정된다. 축·캡션은 "모델−기준(reference)"으로 쓰고 "오차"로 단정하지 않는다.
> 2. **해석 임계·사례수치는 advisory.** Dst RMSE 수십 nT·CME MAE≈10 h·TEC RMSE 야간 1–2/주간 4–5 TECU·Kp MAE 0.5–1.0 등은 **특정 사건·표본·모델의 값**이며 태양활동 위상(극대/극소)·위도대(적도이상대·오로라대)·폭풍여부·리드타임에 강하게 의존. good/bad를 그림에 단정 표기하지 말고 조건을 캡션에 둔다.
> 3. **단일 그림/지표 금지.** 연속오차(RMSE) 하나로 결론내지 말고 최소 **fit(RMSE·PE) + 사건탐지(HSS·POD/FAR) + 타이밍(Δt·DTW)** 3축과 persistence/climatology 기준 스킬을 함께 낸다(Liemohn et al. 2018).
> 4. **원형변수 주의.** IMF clock angle·자기지방시(MLT) 위상은 **0/360° wrap** 처리(단위벡터/원형통계) — 직선 통계 금지.
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문 도판을 그대로 재현하지 않는다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **Dst/SYM-H 폭풍 시계열 overlay + 잔차·PE 패널** — 우주기상 검증의 1차 대표 그림
2. ★ **Dst/SYM-H 검증 산점도 + 회귀 (폭풍/정온 층화)** — 정확도+조건부편향
3. ★ **prediction-efficiency (PE)·스킬 vs 리드타임 곡선** — 분산설명·persistence 대비 스킬
4. ★ **지자기폭풍 사건탐지 분할표 + ROC (임계 스캔)** — Dst/Kp 임계 초과 경보
5. ★ **DTW 위상정렬 시각화 (Dst warping path)** — 형상 vs 타이밍 분리
6. **폭풍 개시·저점 timing 오차 다이어그램** — 위상-진폭 산점
7. ★ **Kp/ap 스택 막대·계단 시계열 (관측 vs 모델)** — 3시간 준로그 지수
8. **태양풍 다패널 시계열 (V·n·Bz·clock angle) + L1 전파정렬** — 폭풍 구동입력
9. ★ **IMF clock angle 원형통계 시각화** — 원형 오차·남향 Bz 사건
10. ★ **전지구 TEC 지도 (GIM, 관측/모델/차 3패널, basemap)** — 전리층 공간구조
11. ★ **TEC bias/RMSE 공간 지도 + MLT–위도 재구성 (basemap)** — 계통오차 지리·지방시 위치
12. **dSTEC pass 곡선 (관측소별 상대 slant TEC, 위치 지도)** — offset-무관 구배 검증
13. ★ **CME 도달시각 오차 다이어그램 (Δt scatter·히스토그램·lead-time)** — CCMC scoreboard
14. ★ **CME 도달 사건탐지 분할표/ROC (hit/miss/false)** — 도달여부 판별
15. ★ **태양플레어 확률예보 reliability + ROC (attributes)** — X/M급 보정·판별
16. **F10.7·27일 주기 위상 검증 (시계열 + Lomb–Scargle/coherence)** — 태양자전 재현

---

### ★ Dst/SYM-H 폭풍 시계열 overlay + 잔차·PE 패널 (지자기지수 폭풍 시계열 검증 / Geomagnetic-index storm time-series overlay with residual & PE panel)
- **무엇을 보여주나**: 한 폭풍 사건(또는 연속 기간)에서 모델·관측 Dst(1h) 또는 SYM-H(1min)를 **시간축에 겹쳐** 그리고, 아래 패널에 **잔차(model−obs)** 와 이동창 RMSE/PE를 둔다. 폭풍의 **급시작(SSC)·주경 저점 timing·진폭·회복기 응답**을 직접 본다. 우주기상 모델 검증의 fit-performance 1차 대표 도판(관측 red / 모델 blue 관행).
- **읽는 법**: 위 패널 두 선의 **주경 저점 시각 어긋남=timing 오차**, 저점 깊이 차=진폭오차, 항상 한쪽이 위/아래면=bias. 아래 잔차가 0 주위 무작위면 양호; **폭풍마다 같은 부호로 튀면(예: 주경 저점을 얕게) 계통 과소** — 모델이 강폭풍을 잘 못 잡는 전형. 회복기(recovery)에서 잔차가 오래 남으면 환전류 소멸(decay) 모의 오류. 폭풍임계선(예 Dst=−50/−100 nT)을 얹으면 경보 관점 가독. *나쁜 패턴*: 저점 위상밀림, 회복기 계단형 잔차, real-time↔final 지수 혼용으로 인한 오프셋.
- **언제 쓰나**: [시계열] 단일/소수 폭풍 정밀 진단, 리드타임(1h/3h/6h ahead)별 열화 점검. 산점도(집계)가 못 보는 *언제·왜*를 본다.
- **짝지표 & 교차링크**: RMSE·MAE·ME·PE·R(→[`30` 지자기지수 시계열/PE 카드], [`01` bias/RMSE]), 사건 timing은 ⑥, 위상은 ⑤ DTW. 잔차 백색성·lag는 공통편 **시계열 overlay+잔차** ([`16` E절])로 교차. 다모델 요약은 공통편 **Taylor** ([`16` A절]).
- **만드는 법**: `pandas`/`xarray` 시간정렬(UTC) 후 `matplotlib` 2–3패널(`sharex`), `fill_between`로 ±잔차 음영. 지수·태양풍 자동수집은 `spaceweather`(GFZ/OMNI)·`pysat`·SpacePy(OMNI); 결측 구간 끊어 그림(보간선으로 잇지 말 것). PE 이동창은 §PE 정의(30)로 numpy.
- **함정·주의**(§G): **real-time Dst vs final Dst 혼용이 가짜 오차**(§G-1) — 버전 통일. 모델·관측 **시간기준·지수 산출 규약(관측소 세트·baseline·Sq 제거) 불일치**가 가짜 위상/offset. 한 사건 결론을 전 사건으로 일반화 금지. RMSE는 강폭풍에 지배됨 → 정온/폭풍 분리·persistence 기준 병기(§G-6 단일지표 금지).
- **출처**: Liemohn et al. (2018) "Model Evaluation Guidelines for Geomagnetic Index Predictions," *Space Weather* 16(12):2079–2102, doi:10.1029/2018SW002067; Wanliss & Showalter (2006, *JGR* 111:A02202, doi:10.1029/2005JA011034, Dst vs SYM-H); WDC for Geomagnetism, Kyoto (Dst/SYM-H 산출).

---

### ★ Dst/SYM-H 검증 산점도 + 회귀 (폭풍/정온 층화) (지자기지수 검증 산점도 / Geomagnetic-index validation scatter, storm/quiet-stratified)
- **무엇을 보여주나**: 매치업된 (관측, 모델) 지수 쌍을 산점하고 1:1선·회귀선·핵심 스칼라(bias·RMSE·PE·R·N)를 얹은 정확도+조건부편향 1장. Dst 음의 값(폭풍)이 좌하단에 몰리므로 **폭풍/정온 색분리** 또는 밀도색을 권장.
- **읽는 법**: x=관측 Dst(nT), y=모델. **1:1선**(점선)이 기준, **OLS 회귀선**(실선). 강한 음의 Dst(폭풍)에서 점이 1:1 위(=덜 음수=과소)로 휘면 **강폭풍 과소**(가장 흔한 약점). 정온대(0 근처)만 밀착하고 꼬리가 벌어지면 평균 OK·극한 NG. box에 bias·RMSE·PE·R·N. *좋은 패턴*: 점운이 폭풍대까지 1:1 밀착, slope≈1, PE 큼. *나쁜 패턴*: 폭풍대 부채꼴/휨(조건부 편향).
- **언제 쓰나**: [시계열] 대량 매치업, 모델·기준 1쌍 또는 다모델 집계. 정확도+편향 동시 1차 점검. 표본 크면 밀도(hexbin)로.
- **짝지표 & 교차링크**: **bias·RMSE·PE·R·OLS slope** → [`30` 지자기지수/PE 카드]. 분포·극치 꼬리는 공통편 **QQ-plot** ([`16` A절])로, 대용량 밀도는 공통편 **밀도산점도**로 승급(중복 회피). 다모델은 **Taylor/Target** ([`16`]).
- **만드는 법**: `matplotlib` `ax.scatter`(폭풍/정온 색) 또는 `ax.hexbin(bins='log')` + `scipy.stats.linregress`(slope·r). PE는 30 정의로 계산. 축 동일 범위·`set_aspect('equal')`·1:1선 `ax.axline`. 폭풍 마스크는 Dst 임계.
- **함정·주의**(§G): **OLS는 관측 무오차 가정** → 지수 자체 불확실(관측소 세트 의존)로 regression dilution → robust/직교회귀 병행. R²(association)와 PE/NSE(bias·기울기 반영)는 **다른 양** — 혼동 금지(30). 전체 산점 하나로 폭풍 성능 판단 금지(정온 다수가 통계를 지배) → 폭풍/정온 분리.
- **출처**: Liemohn et al. (2018), doi:10.1029/2018SW002067; 공통 산점·회귀 시각화 표준(Wilks, *Statistical Methods in the Atmospheric Sciences*); 회귀희석 논의는 [`16`] 산점도 카드.

---

### ★ prediction-efficiency (PE)·스킬 vs 리드타임 곡선 (예측효율/스킬 리드타임 곡선 / Prediction-efficiency & skill-score vs lead-time curve)
- **무엇을 보여주나**: PE(=1−Σ(o−m)²/Σ(o−ō)²)·상관 R·RMSE 또는 persistence 기준 Skill Score(SS)를 **리드타임(1·3·6·…h ahead)** 축으로 그린 스킬감쇠 곡선. RMSE가 못 주는 "설명력"과 실질 예측가치가 리드타임에 따라 어디서 무너지는지 본다.
- **읽는 법**: x=리드타임(h), y=PE(또는 SS, 0~1·음수 가능). **PE=1 완전, PE=0 평균예측 수준, PE<0 평균보다 못함**; persistence 기준 **SS>0이어야 실질 예측가치**. 좋음 = 오래 높은 PE 유지·감쇠 완만. 나쁨 = 짧은 리드에서 PE 급락 또는 persistence 아래(SS<0). 정온/폭풍 곡선 분리(폭풍기 PE는 분모 팽창으로 후하게 나올 수 있음).
- **언제 쓰나**: [시계열] Dst/SYM-H/AE·TEC·태양풍 성분의 리드타임별 스킬 요약. 모델 간·버전 간 비교.
- **짝지표 & 교차링크**: **PE·NSE·R²·SS(persistence/climatology 기준)** → [`30` PE/R² 카드], [`01` 스킬스코어]. 공간 패턴 스킬감쇠는 공통편 **ACC 리드타임 곡선** ([`16` B절]). 확률판이면 CRPSS(→⑮·[`16`]).
- **만드는 법**: 리드타임별 매치업 → PE/R/RMSE numpy 계산 → `matplotlib` 다선 곡선(부트스트랩 CI 띠). persistence 기준분모 명시. 자기상관 강한 시계열은 유효표본 보정(블록 부트스트랩).
- **함정·주의**(§G): **기준(평균 vs persistence vs climatology) 명시 필수** — 기준이 다르면 같은 모델도 점수가 달라진다. 계절·태양주기 변동 큰 자료는 분모가 커져 PE가 과하게 후해짐 → 층화. persistence 대비 비교 없이 "낮은 RMSE=좋음" 착시 금지(§G-6).
- **출처**: Liemohn et al. (2018), doi:10.1029/2018SW002067; Nash & Sutcliffe (1970, *J. Hydrology* 10(3), 효율지표 원형); persistence SS는 [`01`]·Jolliffe & Stephenson, *Forecast Verification*.

---

### ★ 지자기폭풍 사건탐지 분할표 + ROC (임계 스캔) (폭풍 사건탐지 시각화 / Geomagnetic-storm event-detection contingency & ROC)
- **무엇을 보여주나**: "폭풍 임계(Dst≤−50/−100/−250 nT, Kp≥5/7)를 넘었는가"라는 이진 사건의 2×2 분할표(hit/miss/false/correct-neg)를 모자이크/열지도로, 그리고 여러 임계·리드타임을 **성능 다이어그램(Roebber)** 또는 **ROC 곡선**으로. 연속오차가 못 주는 운영 경보 관점.
- **읽는 법**: 분할표 색=칸 빈도. 성능 다이어그램: 가로=SR(=1−FAR)·세로=POD·CSI 등치선·bias 방사선(우상단·대각선 근처=양호). ROC: 좌상단으로 부풀면 판별력↑(AUC→1). *좋은 패턴*: HSS↑·POD↑·FAR↓. *나쁜 패턴*: 강임계(intense/great storm)에서 사건 희소로 점이 불안정·CI 폭 급증. 임계별 궤적으로 강폭풍일수록 어려움 노출.
- **언제 쓰나**: [시계열]→[사건] Dst/SYM-H/Kp 임계. 우주기상 event-detection 축(Liemohn et al. 2018). 여러 임계·리드타임 스캔.
- **짝지표 & 교차링크**: **POD·FAR·CSI·HSS·bias score·TSS·SEDI**(드문 사건) → [`30` 폭풍 사건탐지/드문사건 카드], [`03` 분할표·SEDI]. 그림 프레임(분할표 viz·성능 다이어그램·ROC)은 공통편 [`16` C절]로 **교차링크만**(중복 정의 금지). 확률이면 reliability(⑮).
- **만드는 법**: a,b,c,d 집계(임계·매칭윈도 명시) → 지표 numpy/`xskillscore`; 성능 다이어그램·ROC는 [`16`] 공통 구현 재사용(`matplotlib` CSI 등치선, `sklearn.metrics.roc_curve`/`xskillscore.roc`). bootstrap CI 필수.
- **함정·주의**(§G): **사건 정의(순간 초과 vs 사건단위)·매칭 윈도가 점수를 좌우** → 명시. 희소사건(great storm)에서 HSS/CSI 불안정 → **base-rate 강건 SEDI/TSS 병행**(§G-6). 격자/자기상관으로 유효표본 과대 → bootstrap. real-time↔final 지수 통일.
- **출처**: Liemohn et al. (2018), doi:10.1029/2018SW002067; Sharpe & Murray (2017, *Space Weather*, Met Office 우주기상 예보 검증); 분할표·성능 다이어그램·ROC 표준은 [`16`]·Jolliffe & Stephenson, *Forecast Verification*.

---

### ★ DTW 위상정렬 시각화 (Dst warping path) (동적시간왜곡 정렬도 / Dynamic-time-warping alignment plot for Dst)
- **무엇을 보여주나**: 예측·관측 Dst/SYM-H 시계열을 비선형 시간정렬한 **DTW 정렬경로(누적거리 행렬 + 최적경로)** 와, 정렬선(연결선)이 얹힌 두 시계열 overlay. point-wise RMSE가 부당하게 벌하는 "**위상만 어긋난 좋은 형상**"을 형상거리와 timing shift로 분리해 본다.
- **읽는 법**: (a) 비용행렬 히트맵 위 **최적경로가 대각선에 가까우면 시간왜곡 작음**(위상 정확); 대각선에서 크게 벗어나면 warping 큼(모델이 늦거나 이름). 경로 기울기 구간=국소 지연/선행. (b) overlay의 연결선이 수직에 가까우면 동시성 양호, 사선으로 길게 늘어지면 위상밀림. *좋은 패턴*: 작은 DTW distance + 작은 warping. *나쁜 패턴*: band 한계까지 붙은 경로(과도 warping — 물리적으로 비현실적).
- **언제 쓰나**: [시계열] Dst/SYM-H/AE·태양풍. ML Dst 예측 벤치마킹에서 RMSE와 병행해 "형상 vs 타이밍" 진단.
- **짝지표 & 교차링크**: **DTW distance·warping amount(timing shift)** → [`30` DTW 카드], [`06` DTW/위상·진폭]. RMSE(진폭)는 ①/②와 병행. 공통편 시계열 **DTW** ([`16` E절])로 일반 정의 교차.
- **만드는 법**: `dtaidistance`(`dtw.warping_path`, `dtw.distance`)·`tslearn.metrics.dtw_path`·`dtw-python`. **Sakoe–Chiba band**로 window 제약(과도 warping 방지) 필수. 진폭 정규화 후 정렬; 비용행렬은 `matplotlib` `imshow` + 경로 오버레이.
- **함정·주의**(§G): **band 제약 없으면 물리적으로 불가능한 정렬 허용** → window 필수. 절대 진폭오차는 DTW가 못 봄 → RMSE 별도. **표준 스킬임계 없음**(상대비교 전용) — good/bad 단정 금지. 진폭 정규화 방식이 결과에 영향(명시).
- **출처**: Laperre, Amaya & Lapenta (2020) "Dynamic Time Warping as a New Evaluation for Dst Forecast With Machine Learning," *Frontiers in Astronomy and Space Sciences* 7:39, doi:10.3389/fspas.2020.00039; DTW 원리 Sakoe & Chiba (1978, *IEEE Trans. ASSP*, DOI 확인요).

---

### 폭풍 개시·저점 timing 오차 다이어그램 (개시/저점 timing 산점 / Storm-onset & minimum timing-error diagram)
- **무엇을 보여주나**: 사건별 **timing 오차 Δt=t_model−t_obs**(급시작 SSC 개시·주경 저점 각각)를 산점/히스토그램으로, 흔히 **진폭오차(peak/저점 Dst 차)를 함께 2D 산점**으로. 위상과 진폭을 한 그림에서 분리해 "정시에 왔나 vs 세기가 맞나"를 본다.
- **읽는 법**: x=timing 오차 Δt(h, 양수=지연예측), y=진폭오차(nT). 원점 근처 밀집=양호. x축 한쪽 쏠림=계통 선행/지연 bias; y축 쏠림=계통 과소/과대. 히스토그램으로 |Δt| MAE·표준편차. *나쁜 패턴*: 진폭은 맞는데 x축으로 넓게 퍼짐(형상 OK·타이밍 NG → ⑤ DTW로 확인), 또는 2단 폭풍에서 저점 매칭 실패로 이봉.
- **언제 쓰나**: [시계열]→[사건] Dst/SYM-H 저점·SSC 개시. 리드타임·폭풍유형(CME vs CIR)별 층화.
- **짝지표 & 교차링크**: **timing bias·|Δt| MAE·SD + 진폭오차** → [`30` SSC/저점 timing 카드]. 위상 상세는 ⑤ DTW·[`06`]. 사건탐지(왔나/안왔나)는 ④.
- **만드는 법**: 개시/저점 검출(임계교차·평활 후 argmin) 규약 통일 → 사건별 Δt·진폭차 → `matplotlib` 2D 산점 + 주변 히스토그램(`seaborn.jointplot` 대안). 사건 수 적으면 bootstrap CI.
- **함정·주의**(§G): **개시·저점 검출 규약(임계·평활·최소 지속)이 결과를 좌우** → 명시·고정. 저점이 편평/다봉이면 검출 모호(2단 폭풍 매칭 규칙). 진폭 RMSE가 좋아도 timing 크게 어긋날 수 있음(위상-진폭 분리 필요). 사건 수 적으면 통계 불안정.
- **출처**: Liemohn et al. (2018), doi:10.1029/2018SW002067; Pulkkinen et al. (2013, *Space Weather* 11, GIC/dB/dt 검증 timing·spatial); 위상오차 일반론 [`06_timeseries_signal.md`].

---

### ★ Kp/ap 스택 막대·계단 시계열 (관측 vs 모델) (Kp/ap 막대·계단 검증도 / Kp/ap stacked-bar & step time-series)
- **무엇을 보여주나**: 3시간 준로그 지수 Kp(0~9, 1/3 단계)를 **관측·모델 나란한/겹친 막대(또는 계단)** 로, 흔히 활동도별 색(정온=녹, minor≥5=주황, strong≥7=적)으로. 계단형·비선형인 Kp를 연속선으로 왜곡하지 않고 3시간 bin 구조 그대로 비교. ap(선형 nT 등가) 산점을 짝으로.
- **읽는 법**: x=시간(3h bin), y=Kp. 관측·모델 막대 높이·색 class 대조. **±1 Kp 이내면 실용 적중**; class 경계(5·7)에서 넘나들면 경보 관점 오탐/누락. *좋은 패턴*: bin별 높이·색 일치, class 전이 시점 정확. *나쁜 패턴*: 폭풍 bin을 한 단계 낮게(과소), 급변(SSC) bin의 계단 지연(3시간 지수라 순간 timing은 못 잡음). 물리진폭 비교는 ap 산점에서(준로그 왜곡 회피).
- **언제 쓰나**: [시계열](3h) Kp/ap 예측. nowcast(추정) vs forecast 구분. GFZ Potsdam 공식 Kp/ap 기준.
- **짝지표 & 교차링크**: **Kp MAE/RMSE(1/3 단계)·±1 Kp 적중률·ap 변환 RMSE** → [`30` Kp/ap 카드]. 폭풍임계 사건탐지(Kp≥5)는 ④. 확률 Kp는 reliability(⑮·[`16`]). 27일 주기는 ⑯.
- **만드는 법**: `matplotlib` `ax.bar`(관측/모델 offset) 또는 `ax.step`; Kp class 색맵. ap는 표준 Kp→ap 환산 후 산점. Kp/ap 수집 `spaceweather`(kp.gfz-potsdam.de). 3h UTC bin 정렬.
- **함정·주의**(§G): **Kp를 선형 연속량처럼 평균/RMSE 하면 준로그 왜곡** → ap 변환 병행. 3시간 지수라 **급변 timing은 못 잡음**(별도 timing 카드⑥). nowcast↔forecast·실시간↔definitive Kp 혼용 금지. bootstrap CI(→[`30`]).
- **출처**: Matzka et al. (2021) "The Geomagnetic Kp Index and Derived Indices of Geomagnetic Activity," *Space Weather* 19 (GFZ Kp/ap 정의; 권·페이지 확인요); Liemohn et al. (2018), doi:10.1029/2018SW002067; `spaceweather` (pypi.org/project/spaceweather, GFZ/OMNI 지수 접근).

---

### 태양풍 다패널 시계열 (V·n·Bz·clock angle) + L1 전파정렬 (태양풍 성분 다패널 / Solar-wind multi-panel time series with L1 propagation alignment)
- **무엇을 보여주나**: 태양풍 속도 V·밀도 n·IMF Bz(GSM)·clock angle θ를 **세로로 쌓은 다패널 시계열**로 L1 관측(ACE/DSCOVR/Wind)과 모델(WSA-ENLIL 등)을 겹쳐, CIR/CME 통과 구조(shock·sheath·ejecta)를 성분별로 비교. **L1→magnetopause 전파지연 정렬 전후**를 함께 보여 정렬이 잔차상관을 개선하는지 진단.
- **읽는 법**: 각 패널 두 선 대조 — V·n의 급상승(shock)·plateau, **Bz의 남향(<0) 구간과 지속시간**(지자기활동 구동)이 핵심. clock angle은 원형패널(0/360 wrap). 정렬 전엔 위상밀림, 정렬 후 겹침 개선=전파lag 타당. *나쁜 패턴*: Bz를 직선 평균만 보면 부호·구조 놓침; shock timing 밀림; 좌표계(GSM vs GSE) 혼용으로 Bz 부호 반전.
- **언제 쓰나**: [시계열] L1 관측 vs 태양풍 예측. CME 도달 후 sheath/ejecta 구조 비교, 지수예측 입력 정확도 진단.
- **짝지표 & 교차링크**: V·n·Bz **RMSE·MAE·bias·R**·남향 Bz 사건/지속시간 → [`30` 태양풍/L1 전파 카드]. clock angle 원형통계는 ⑨. 전파lag 오차는 [`30` L1→magnetopause 카드]. 다패널 overlay+잔차 프레임은 [`16` E절].
- **만드는 법**: OMNI/L1 수집 SpacePy·`pysat`·`sunpy`(timeseries) → `matplotlib` `sharex` 다패널. 전파정렬은 flat-delay(Δt=X_L1/Vx) 또는 상평면(phase-front) 후 재정렬. clock angle θ=atan2(By,Bz)는 원형패널. GSM/GSE 통일.
- **함정·주의**(§G): **자기장 좌표계(GSM/GSE) 통일 안 하면 Bz 부호 오류**. **clock angle 직선 RMSE 금지**(원형통계→⑨). L1→magnetopause 전파지연 미정렬 시 인위적 위상오차(뒤따르는 지수검증에 전파). **Bz는 본질적으로 예측난도 최고**(작은 스케일 요동) → RMSE 크게 나오는 것이 정상, 남향 이벤트 탐지·지속시간이 실용 지표(절대기준 강요 금지).
- **출처**: Owens et al. (2008, *Space Weather*, 태양풍 예측 검증); Weimer et al. (2003, *JGR*, phase-front 전파); Liemohn et al. (2018), doi:10.1029/2018SW002067; L1 전파기법 비교 Mailyan et al. (2008, *Ann. Geophys.*, 확인요).

---

### ★ IMF clock angle 원형통계 시각화 (clock angle 원형통계 / IMF clock-angle circular-statistics plots)
- **무엇을 보여주나**: IMF clock angle θ=atan2(By,Bz)(및 그 오차 Δθ=model−obs, −180°~180° wrap)를 **원형**으로 — (a) θ 원형히스토그램(관측·모델 나란히), (b) Δθ 원형히스토그램, (c) 단위벡터 잔차 산점. 0/360° 경계 때문에 직선 통계가 안 되는 방향변수를 올바르게 진단하고, **남향 Bz(θ≈180°) 구동 방향**의 재현을 본다.
- **읽는 법**: (a) θ 분포에서 **남향(θ≈180°)·북향(θ≈0°) 빈도** 대조 — 남향 우세 구간을 모델이 재현하나. (b) Δθ 원형히스토그램이 0°에 뾰족=양호; 한쪽 치우침=**원형 bias**(방향 계통 회전); 양방향 퍼짐=무작위. (c) 단위벡터(cosθ,sinθ) 잔차가 원점 주위 등방이면 양호. *나쁜 패턴*: Δθ 봉이 ±수십° 이동(계통편차).
- **언제 쓰나**: [시계열] IMF θ 검증(L1 관측 vs 예측). 남향 Bz 구동 방향의 계통오차 진단.
- **짝지표 & 교차링크**: **원형 bias=circmean(Δθ)·원형 RMSE=√mean(wrap(Δθ)²)·벡터 RMSE** → [`30` 태양풍(clock angle 원형통계) 카드]. 풍향([`07`]·[`17`])·유향([`10`])과 **공통 원형통계 코어**(00 §4.2 정합 권고)로 통일. 파랑 파향 원형통계([`18` ⑨])와 형제 그림.
- **만드는 법**: `scipy.stats.circmean`/`circstd`(또는 atan2 평균). `matplotlib` `projection='polar'`로 θ·Δθ 히스토그램; 단위벡터 잔차는 일반 산점. **wrap은 `np.angle(np.exp(1j*np.deg2rad(Δθ)))`** 로 안전 처리. By·Bz는 GSM.
- **함정·주의**(§G): **0/360 wrap 미처리 시 치명적**(359°와 1° 차가 358°로 계산) → 반드시 단위벡터/wrap. **직선 RMSE 금지**. 저 |B|(약한 자기장)에서 clock angle 정의 모호 → |B| 임계 필터. 원형평균은 분산 크면 의미 약함(R_bar 동반). GSM/GSE 통일.
- **출처**: 원형통계 일반론 Bowers, Morton & Mould (2000, *Applied Ocean Research* 22(1):13–30); Fisher, *Statistical Analysis of Circular Data* (Cambridge, 원형통계 표준); 우주기상 clock angle 원형 처리는 [`30`]·[`07`] 교차.

---

### ★ 전지구 TEC 지도 (GIM, 관측/모델/차 3패널, basemap) (전지구 TEC 지도 / Global TEC map (GIM): obs / model / difference, 3-panel)
- **무엇을 보여주나**: 특정 UT의 전지구 VTEC를 **관측 GIM(IGS/JPL/CODE)·모델·차(model−obs) 3패널** 지도(색=TECU)로. **적도이상대(EIA)의 두 crest·주야 경계·오로라대** 등 전리층 대규모 구조를 모델이 재현하는지 공간적으로 본다. ★ 지도형(위경도)이므로 **해안선/육지 + 위경도 라벨 필수**.
- **읽는 법**: 관측·모델 패널: 색=VTEC(0~100+ TECU, 순차맵). 주간·적도 부근 고 TEC(EIA 두 crest), 야간·고위도 저 TEC 확인. 차 패널: 발산맵·**0=흰색**, 빨강=과대·파랑=과소. *좋은 패턴*: EIA crest 위치·세기·주야 경계가 관측과 일치, 차 패널 옅음. *나쁜 패턴*: crest 위치 이동·세기 과소, 야간 과대, 차 패널의 넓은 단색대(계통편차).
- **언제 쓰나**: [격자] 모델 VTEC vs GIM. 폭풍 전/중/후 스냅샷, 대규모 구조 정성 점검(정량은 ⑪).
- **짝지표 & 교차링크**: 격자별 **ME(bias)·RMSE·R**(→⑪ 정량), 공간패턴 일치는 공통편 **패턴상관/ACC 맵** ([`16` B절]). → [`30` 전리층 TEC/GIM 격자비교 카드], [`01`·`02`]. 차 지도 프레임은 공통편 **bias/difference map**.
- **만드는 법**: IONEX→`xarray`(또는 GIM 전용 파서) → **`cartopy`** GeoAxes 3패널 `pcolormesh`(`transform=ccrs.PlateCarree()`) + **`add_basemap()`**([`plotting_maps.md`])로 해안선/육지+위경도 라벨. 순차맵(TEC)·발산맵(차, `TwoSlopeNorm(vcenter=0)`+`RdBu_r`/`cmocean.balance`). **경도 0–360→−180–180 변환**(`lon=((lon+180)%360)-180`) 안 하면 화면 밖.
- **함정·주의**(§G): ★ **basemap 필수** — 해안선/육지·위경도 라벨 없으면 "어디인지" 못 읽음; 연안/전지구는 span 자동 해상도(`add_basemap`). **경도 규약(0–360 vs −180–180) 불일치 시 대륙이 반대편**(→[`plotting_maps.md` E-2]). **GIM은 이미 보간·동화 산물**(§G-1,3) — "정답" 과신 금지; **해양·극지 GIM은 관측 sparse로 자체 오차 큼** → 그 영역 차이는 GIM 오차일 수 있음. 재격자 보간·색스케일 양 패널 통일.
- **출처**: Hernández-Pajares et al. (2009, *J. Geodesy*, IGS GIM); Chou et al. (2023) "Validation of Ionospheric Modeled TEC ... 2013 March and 2021 November Geomagnetic Storms," *Space Weather* 21, doi:10.1029/2023SW003480; Liu et al. (2022, *Space Weather* 20, doi:10.1029/2022SW003135, ML 전지구 TEC 지도); `cartopy`·`add_basemap`([`plotting_maps.md`]).

---

### ★ TEC bias/RMSE 공간 지도 + MLT–위도 재구성 (basemap) (TEC 계통오차 공간·지방시 지도 / TEC bias/RMSE spatial map & MLT–latitude reconstruction)
- **무엇을 보여주나**: 모델 [격자] TEC를 GIM과 전 기간 비교해 격자점별 **bias(lat,lon)·RMSE·R를 지도(색)** 로(★ 지도형 → basemap 필수), 그리고 축을 **자기지방시(MLT)×지자기위도**로 재구성한 짝 그림으로 계통오차의 **지리·지방시·계절 구조**(적도이상대 crest 과소, 야간 과대 등)를 진단. 점 관측 없는 해양·극지까지 커버.
- **읽는 법**: 지도 패널: 발산맵 bias(0=흰), 순차맵 RMSE. **EIA(±10~20° 자기위도) 오차대·오로라대·주야 경계** 위치 확인. MLT–위도 패널: 가로=MLT(0~24)·세로=자기위도·색=bias/RMSE → **어느 지방시·위도에서 계통오차 최대**인지(주간 EIA crest, 야간 등). *나쁜 패턴*: EIA crest 계통 과소 띠, 야간 과대, 특정 MLT 섹터 쏠림.
- **언제 쓰나**: [격자]vs[격자] 광역·장기 진단. 점 검증(⑫ dSTEC·ionosonde)이 못 메우는 공간·지방시 커버리지.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·R + 4범주(accuracy/bias/association/precision) 프레임** → [`30` GIM 격자-격자 카드], [`02` 공간패턴]. 지도 프레임은 공통편 **bias/difference map** ([`16` B절]). basemap 규칙은 [`plotting_maps.md`].
- **만드는 법**: `xarray`+공통 격자 재격자 → 격자별 통계 → **`cartopy`** `pcolormesh` + **`add_basemap()`**. MLT–위도 재구성은 UT·경도→MLT, 지리위도→**AACGMv2 자기위도**(`aacgmv2` 라이브러리) 변환 후 `pcolormesh`/`binned_statistic_2d`. 발산맵(bias)·순차맵(RMSE).
- **함정·주의**(§G): ★ **지도 패널 basemap(해안선+위경도 라벨) 필수**; 경도 0–360→−180–180 변환; 해양 격자 육지 마스킹(→[`plotting_maps.md` E-4]). **GIM 자체 불확실성**(관측 sparse 해역)이 차이에 섞임(§G-1). DCB 보정 오차가 bias로 위장. **MLT–위도 재구성은 지도가 아님**(축이 지방시·자기위도) → basemap 넣지 말 것([`plotting_maps.md` B]).
- **출처**: Chou et al. (2023), doi:10.1029/2023SW003480; CCMC/SWPC GloTEC 검증(accuracy/bias/association/precision 프레임); AACGM-v2 자기좌표 변환 `aacgmv2`(aacgmv2.readthedocs.io); 지도 규칙 [`plotting_maps.md`].

---

### dSTEC pass 곡선 (관측소별 상대 slant TEC, 위치 지도) (dSTEC pass 검증도 / Differential slant-TEC pass curve with station map)
- **무엇을 보여주나**: 위성·수신기 편이(DCB)·offset에 오염된 절대 TEC 대신, 한 위성 pass 내 **최고앙각 기준 상대 slant TEC 변화 dSTEC(t)=STEC(t)−STEC(t_ref)** 를 관측·모델이 함께 그린 곡선(여러 pass 오버레이) + **관측소 위치 지도**(정점 마커+ID). offset 오차를 소거하고 시공간 gradient 재현력을 평가.
- **읽는 법**: x=pass 내 시간(또는 앙각), y=dSTEC(TECU, t_ref에서 0). 관측·모델 곡선의 **모양·기울기(구배) 일치** 확인. *좋은 패턴*: 곡선 겹침, dSTEC RMSE 작음. *나쁜 패턴*: 모델이 상승/하강 구배를 과소(구배 재현 불량), pass 끝(저앙각)에서 벌어짐. 관측소 위치 지도로 어느 지역 pass인지 식별(정점 검증이므로 위치 필수).
- **언제 쓰나**: [정점] 관측소별 GNSS pass vs 모델 slant TEC. GIM/모델의 **offset-무관** 정확도 평가(절대 bias와 분리).
- **짝지표 & 교차링크**: **dSTEC RMSE(TECU)** → [`30` dSTEC 카드]. 절대 bias는 ⑪·[`30` TEC 카드]와 병행. 위성 대조(RO·altimeter)는 [`30`]·[`12`·`22`]. 정점 위치 지도 규칙은 [`plotting_maps.md` C].
- **만드는 법**: 위성 pass별 최고앙각 t_ref 식별·사이클슬립 제거 → dSTEC 관측/모델(모델은 **시선방향 적분**, 매핑함수 아님) → `matplotlib` 곡선 오버레이. 관측소 위치는 **`cartopy`+`add_basemap()`** 마커+`annotate`(ID), 확대 군집은 `10m` 해안선(→[`plotting_maps.md` C·E]).
- **함정·주의**(§G): **dSTEC는 상대변화만 평가 → 절대 TEC bias는 못 봄**(절대검증 병행). pass 짧으면 통계 빈약. 매핑함수 미사용이라 slant 적분 정확도 필요. **관측소 지도에 basemap·ID 필수**(정점 위치 식별). t_ref(최고앙각) 규약 통일.
- **출처**: Hernández-Pajares et al. (2017, *J. Geodesy*, dSTEC 검증법; 확인요); PPP+IRI 가상국 dSTEC 개선(~19.8%) 사례(*Adv. Space Res.* 계열, 권·페이지 확인요); 정점 지도 규칙 [`plotting_maps.md`].

---

### ★ CME 도달시각 오차 다이어그램 (Δt scatter·히스토그램·lead-time) (CME 도달시각 오차도 / CME arrival-time error diagram: Δt scatter, histogram, lead-time)
- **무엇을 보여주나**: CME·행성간충격파의 지구/L1 **도달시각 오차 ΔtA=t_predicted−t_observed**(양수=지연예측)를 (a) 예측 vs 관측 산점(1:1선), (b) ΔtA 히스토그램(bias·MAE·SD box), (c) **lead-time vs ΔtA** 산점으로. CCMC CME scoreboard의 다중모델 매치업 종합. 우주기상 조기경보 대표 지표.
- **읽는 법**: (a) 예측=관측 1:1선 주위 밀집=양호; 계통 위/아래=지연/선행 bias. (b) 히스토그램 중심=bias(음수=조기예측 경향 보고됨), 폭=MAE/SD; **다중모델 종합 MAE≈10 h·SD>20 h 규모**(advisory 사례값). (c) lead-time↔ΔtA에 **짧은 transit time에 지연예측, 긴 transit에 조기예측** 경향이 관찰됨. *나쁜 패턴*: 넓은 산포(SD 큼), 강한 계통 bias, 소표본 낙관편향.
- **언제 쓰나**: [사건] CME별(관측 도달=충격파/ICME 개시) vs 모델(WSA-ENLIL+Cone·DBM·ML). hit인 사건만 timing 통계(miss/false는 ⑭ 별도).
- **짝지표 & 교차링크**: **ΔtA mean(bias)·MAE·SD** → [`30` CME 도달시각 오차 카드], [`30` CCMC scoreboard 카드]. 도달여부(hit/miss/false)는 ⑭. 소표본 → bootstrap. 분포 비교는 공통편 [`16`].
- **만드는 법**: 사건 매치업 테이블 → `matplotlib` 산점(예측 vs 관측·1:1선)·히스토그램·lead-time 산점. bias/MAE/SD numpy. CCMC CME scoreboard(ccmc.gsfc.nasa.gov) 자료 구조 참조. 소표본 bootstrap CI.
- **함정·주의**(§G): **"도달" 정의(충격파 도착 vs ICME 개시) 통일 필수**. **표본 편향**(강한 CME·hit만 집계 시 낙관) — hit 통계만 보고 miss/false 무시 금지(→⑭). **ΔtA>30 h는 흔히 miss로 처리**(정의 명시). 소표본 → CI 필수. 도달시각·transit time 상관은 인과 아님.
- **출처**: Riley et al. (2018) "Forecasting the Arrival Time of Coronal Mass Ejections: Analysis of the CCMC CME Scoreboard," *Space Weather* 16(9):1245–1260, doi:10.1029/2018SW001962; Wold et al. (2018, *JSWSC* 8:A17, WSA-ENLIL+Cone: ME −4.0 h, MAE 10.4 h); Kay & Palmerio (2024) "Updating Measures of CME Arrival Time Errors," *Space Weather*, doi:10.1029/2024SW003951 (bias −2.5 h, MAE 13.2 h, SD 17.4 h; 권·페이지 확인요).

---

### ★ CME 도달 사건탐지 분할표/ROC (hit/miss/false) (CME 도달 사건탐지 시각화 / CME-arrival event-detection contingency & ROC)
- **무엇을 보여주나**: CME가 **지구에 도달하는가/안 하는가**(및 예측 여부)를 2×2 분할표(hit·miss·false alarm·correct-neg)로, 여러 모델/기간을 성능 다이어그램·ROC로. timing 오차(⑬)와 별개로 "예측한 CME가 실제 왔나, 온 CME를 예측했나"를 판별.
- **읽는 법**: 분할표 색=칸 빈도. 성능 다이어그램/ROC로 POD·FAR·CSI·HSS. **FAR가 높은 경향**(오지 않은 CME 과다예측)이 보고됨 → 운영 경보 부담. *좋은 패턴*: 우상단(POD↑·SR↑). *나쁜 패턴*: 좌하단, bias≫1(과다예측). glancing blow(측면 스침)·arrival window 정의가 판정을 좌우.
- **언제 쓰나**: [사건] CME 사건목록. CCMC scoreboard·운영 예보 판별 평가. timing(⑬)과 반드시 함께.
- **짝지표 & 교차링크**: **POD·FAR·CSI·HSS·bias score** → [`30` CME 도달 사건탐지 카드]. 분할표 viz·성능 다이어그램·ROC 프레임은 공통편 [`16` C절]로 **교차링크만**. timing은 ⑬. 폭풍 사건탐지(④)와 형제.
- **만드는 법**: a,b,c,d 집계(도달 판정·매칭 규칙 명시) → [`16`] 공통 성능 다이어그램·ROC 재사용. bootstrap CI.
- **함정·주의**(§G): **catalogue 불완전**(약한 CME 누락)·**glancing 판정 주관성**이 큰 불확실성. **"도달" 판정 기준(중심 hit vs glancing)·arrival window 합의** 필수. timing(hit만)과 반드시 함께 보고. 소표본 → CI.
- **출처**: Riley et al. (2018), doi:10.1029/2018SW001962; Verbeke et al. (2019, *Space Weather*, CME 도달 검증 metric 논의); 분할표·ROC 표준 [`03_categorical_event_extremes.md`]·[`16`].

---

### ★ 태양플레어 확률예보 reliability + ROC (attributes) (플레어 확률예보 신뢰도·판별도 / Solar-flare probabilistic-forecast reliability & ROC)
- **무엇을 보여주나**: 태양플레어(C/M/X급) 발생 **확률예보**의 (a) reliability(attributes) diagram — 예측확률 대 관측빈도(no-skill·no-resolution·climatology 선 포함, sharpness 인셋), (b) ROC/AUC — 판별력. 결정론 지표가 못 주는 확률 품질(보정+판별)을 짝으로.
- **읽는 법**: (a) reliability: 가로=예측확률·세로=관측빈도·**1:1 대각선=완전보정**; 아래=과신(overconfident), 위=과소신뢰; sharpness 막대로 예측확률 분포. (b) ROC: 좌상단 부풀수록 판별력↑(AUC→1, 대각선=무기술). *좋은 패턴*: reliability 점이 대각선·AUC 큼·TSS>0. *나쁜 패턴*: 희소 X급에서 표본 적어 reliability 점 요동(고확률 bin만 신뢰). 보정(calibration)은 reliability를 개선하나 ROC/PR엔 영향 적음.
- **언제 쓰나**: [시계열]/[사건] 플레어 확률예보 vs GOES X선 관측. 우주기상 확률예보 검증 대표. 희소·불균형 사건 → base-rate 강건 지표 중시.
- **짝지표 & 교차링크**: **Brier(+분해)·BSS·AUC·TSS·SEDI·sharpness** → [`30` 플레어 확률예보/드문사건 카드], [`03` Brier·ROC·SEDI]. reliability·ROC·Brier/CRPS 분해 프레임은 공통편 [`16` C절]로 **교차링크만**(중복 정의 금지). 앙상블 우주기상은 rank hist/CRPS(공통편·[`30`]).
- **만드는 법**: reliability `sklearn.calibration.calibration_curve` 또는 기상용 `scores`/`xskillscore`; consistency bar는 부트스트랩. ROC `sklearn.metrics.roc_curve`/`roc_auc_score`. GOES X선 플럭스 `sunpy`(goes timeseries)로 사건 라벨(≥M1.0/≥X1.0). bootstrap CI.
- **함정·주의**(§G): **불균형 사건에서 accuracy·Brier가 base-rate에 지배** → TSS/SEDI 병행(§G-6). reliability는 **표본 많은 확률구간만 신뢰**(consistency bar 필수). ROC(판별)와 reliability(보정)는 **상보** — 하나로 결론 금지. 예보-관측 사건 정의(임계·유효기간 24h 등) 통일. 희소 X급 CI 폭 넓음 명시.
- **출처**: Kubo, Den & Ishii (2017) "Verification of operational solar flare forecast: Case of RWC Japan," *JSWSC* 7:A20; Bloomfield et al. (2012, *ApJL*, TSS 플레어 권고); Camporeale (2025) "Verification of the NOAA SWPC Solar Flare Forecast (1998–2024)," *Space Weather*, doi:10.1029/2025SW004546 (reliability·ROC 최신 검증; 권·페이지 확인요); reliability/ROC 표준 [`16`]·Jolliffe & Stephenson.

---

### F10.7·27일 주기 위상 검증 (시계열 + Lomb–Scargle/coherence) (F10.7 주기·위상 검증도 / F10.7 27-day cycle phase verification: time series + Lomb–Scargle/coherence)
- **무엇을 보여주나**: 10.7 cm 태양전파플럭스 F10.7의 (a) 리드타임별 관측·예측 overlay 시계열, (b) **27일 태양자전 주기 대역의 스펙트럼(Lomb–Scargle)·cross-spectrum/coherence·위상지연**. RMSE가 못 주는 "27일 주기 위상 재현"(실용 스킬)을 본다. 대기항력·전리층 모델의 핵심 구동입력.
- **읽는 법**: (a) 시계열: 리드타임 길수록 예측이 관측 27일 파동을 못 따라감(위상밀림·진폭축소). (b) Lomb–Scargle PSD에서 **~27일(및 반값 ~13.5일) 봉우리** 위치·세기 일치; coherence가 27일 대역에서 높고 **위상지연 작으면 자전 구동 재현 양호**. *나쁜 패턴*: 27일 봉 이동/약화, 위상지연 큼, 장기예측이 climatology 아래(SS<0). adjusted vs observed flux 혼용 offset.
- **언제 쓰나**: [시계열] F10.7 예측 vs 관측(DRAO Penticton). 장기 hindcast 기후·주기 검증. Kp·TEC의 27일 재현에도 동형 적용.
- **짝지표 & 교차링크**: **리드타임별 RMSE·MAE·bias(sfu)·27일 대역 coherence·위상지연·persistence 기준 SS** → [`30` F10.7 카드], [`30` 주기·계절 위상 카드]. PSD/Lomb–Scargle·coherence 정의는 [`05_spectral_eof_modal.md`]·[`06_timeseries_signal.md`]. 스킬 vs 리드는 ③.
- **만드는 법**: `astropy.timeseries.LombScargle`(불규칙·결측 표본)·`scipy.signal.welch`(등간격); cross-spectrum/coherence `scipy.signal.coherence`·`pycwt`(wavelet coherence). `matplotlib` 시계열 overlay + 스펙트럼 패널. adjusted(1 AU)/observed 통일, UTC 정렬, 플레어 전파버스트 오염 제거.
- **함정·주의**(§G): **detrend·window·정규화를 모델·관측 동일하게**(아니면 가짜 차이). **결측엔 Welch 대신 Lomb–Scargle**. 짧은 기간은 11년 주기 미분해; **태양주기 비정상성**(진폭 변동) 주의. 장기예측은 태양주기 예측 불확실성에 지배 → **climatology/persistence 대비 스킬**로 평가(F10.7 단독은 EUV 완전대리 아님).
- **출처**: Petrova et al. (2021) "Medium-term Predictions of F10.7 and F30 cm Solar Radio Flux with the Adaptive Kalman Filter," *ApJS* 254 (RMSE ~5–27 sfu; DOI 확인요); NOAA SWPC 45-day Ap/F10.7 forecast; Lomb–Scargle `astropy`(docs.astropy.org); 주기·위상 정의 [`05`]·[`06`].

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 30(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 30(및 타 파일) 교차링크 |
|---|---|---|---|---|---|
| 1 | Dst/SYM-H 폭풍 시계열 + 잔차·PE | 시계열 | 편향+위상+사건(fit) | RMSE·MAE·PE·R | 30 지수시계열/PE · 01 · (16 시계열) |
| 2 | Dst/SYM-H 검증 산점도 (폭풍/정온) | 시계열 | 정확도+조건부편향 | bias·RMSE·PE·R·slope | 30 지수/PE · (16 산점·QQ) |
| 3 | PE·스킬 vs 리드타임 곡선 | 시계열 | 분산설명·persistence 스킬 | PE·NSE·R²·SS | 30 PE/R² · 01 · (16 ACC 리드) |
| 4 | 폭풍 사건탐지 분할표+ROC | 시계열→사건 | 범주형 경보 | POD·FAR·CSI·HSS·SEDI | 30 사건탐지 · 03 · (16 C절) |
| 5 | DTW 위상정렬 (Dst) | 시계열 | 형상 vs 타이밍 | DTW distance·warping | 30 DTW · 06 · (16 E절) |
| 6 | 개시·저점 timing 오차 다이어그램 | 시계열→사건 | 위상+진폭 | timing bias·|Δt| MAE | 30 SSC/저점 timing · 06 |
| 7 | Kp/ap 스택 막대·계단 | 시계열(3h) | 준로그 지수 정확도 | Kp MAE·±1 적중·ap RMSE | 30 Kp/ap · 04 · (16 reliability) |
| 8 | 태양풍 다패널 (V·n·Bz·θ)+전파정렬 | 시계열 | 구동입력 정확도 | RMSE·bias·남향 Bz 사건 | 30 태양풍/L1 · 09 · (16 E절) |
| 9 | IMF clock angle 원형통계 | 시계열 | 방향(원형) 편향 | 원형 bias/RMSE·벡터 RMSE | 30 태양풍 · 07·10·18⑨ 원형코어 |
| 10 | 전지구 TEC 지도 (GIM 3패널, basemap) | 격자 | 공간구조(정성) | 격자 bias·R·패턴상관 | 30 TEC/GIM · 01·02 · (16 B절) |
| 11 | TEC bias/RMSE 지도+MLT–위도 (basemap) | 격자 | 편향+패턴(공간·지방시) | 격자 bias·RMSE·R·4범주 | 30 GIM 격자비교 · 02 · (16 B절) |
| 12 | dSTEC pass 곡선 (+위치 지도) | 정점 | offset-무관 구배 | dSTEC RMSE | 30 dSTEC · 12·22 |
| 13 | CME 도달시각 오차 다이어그램 | 사건 | 타이밍(도달) | ΔtA bias·MAE·SD | 30 CME 도달시각·scoreboard |
| 14 | CME 도달 사건탐지 분할표/ROC | 사건 | 도달여부 판별 | POD·FAR·CSI·HSS·bias | 30 CME 사건탐지 · 03 · (16 C절) |
| 15 | 플레어 확률예보 reliability+ROC | 시계열/사건 | 확률 보정+판별 | Brier/BSS·AUC·TSS·SEDI | 30 플레어/드문사건 · 03 · (16 C절) |
| 16 | F10.7·27일 주기 위상 검증 | 시계열 | 주기·위상 | RMSE·coherence·위상지연·SS | 30 F10.7·주기 · 05·06 |

> **묶음 권고**: 단일 그림 금지 원칙(§G-6)에 따라 지자기지수 검증 보고는 최소 **①(fit·시계열+PE) + ④(사건탐지) + ⑤/⑥(타이밍)** 3축을 기본 세트로, 확률/앙상블이면 **⑦/⑮**(reliability·ROC), 전리층이면 **⑩/⑪**(+⑫ 정점), 태양풍/CME 구동이면 **⑧/⑨/⑬/⑭**, 태양활동/주기면 **⑯**를 추가한다. 모든 임계·사례수치(Dst RMSE·CME MAE≈10 h·TEC RMSE·Kp MAE 등)는 **advisory + 조건(태양활동 위상·위도대·폭풍여부·리드타임) 경고**로 캡션에 단다. persistence/climatology 기준 스킬을 반드시 병기(Liemohn et al. 2018).

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**핵심 도메인 지침·프레임워크 (실재)**
- Liemohn, M. W. et al. (2018) "Model Evaluation Guidelines for Geomagnetic Index Predictions," *Space Weather* 16(12):2079–2102, **doi:10.1029/2018SW002067** (지자기지수 fit+event 이원 프레임 — 이 도메인 핵심 지침).
- Riley, P. et al. (2018) "Forecasting the Arrival Time of Coronal Mass Ejections: Analysis of the CCMC CME Scoreboard," *Space Weather* 16(9):1245–1260, **doi:10.1029/2018SW001962** (CME 도달시각·사건탐지).
- NASA Community Coordinated Modeling Center (CCMC) — CME Scoreboard·지자기지수·전리층 검증: https://ccmc.gsfc.nasa.gov
- NOAA SWPC — 45-day Ap/F10.7 forecast·GloTEC: https://www.swpc.noaa.gov ; ISES(RWC 검증): http://www.spaceweather.org

**학술 논문 (제목·저널·연도 웹 확인)**
- Wold, A. M. et al. (2018) "Verification of real-time WSA-ENLIL+Cone simulations of CME arrival-time at the CCMC from 2010–2016," *JSWSC* 8:A17. (ME −4.0 h, MAE 10.4 h)
- Kay, C. & Palmerio, E. (2024) "Updating Measures of CME Arrival Time Errors," *Space Weather*, **doi:10.1029/2024SW003951** (bias −2.5 h, MAE 13.2 h, SD 17.4 h; 권·페이지 확인요).
- Laperre, B., Amaya, J. & Lapenta, G. (2020) "Dynamic Time Warping as a New Evaluation for Dst Forecast With Machine Learning," *Frontiers in Astronomy and Space Sciences* 7:39, **doi:10.3389/fspas.2020.00039**.
- Chou, M.-Y. et al. (2023) "Validation of Ionospheric Modeled TEC in the Equatorial Ionosphere During the 2013 March and 2021 November Geomagnetic Storms," *Space Weather* 21, **doi:10.1029/2023SW003480**.
- Liu, L. et al. (2022) "Machine Learning Prediction of Global Ionospheric TEC Maps," *Space Weather* 20, **doi:10.1029/2022SW003135**.
- Kubo, Y., Den, M. & Ishii, M. (2017) "Verification of operational solar flare forecast: Case of RWC Japan," *JSWSC* 7:A20.
- Camporeale, E. (2025) "Verification of the NOAA SWPC Solar Flare Forecast (1998–2024)," *Space Weather*, **doi:10.1029/2025SW004546** (reliability·ROC·PR; 권·페이지 확인요).
- Wanliss, J. A. & Showalter, K. M. (2006) "High-resolution global storm index: Dst versus SYM-H," *JGR* 111:A02202, **doi:10.1029/2005JA011034**.
- Verbeke, C. et al. (2019, *Space Weather*, CME 도달 검증 metric 논의; 권·페이지 확인요).
- Bloomfield, D. S. et al. (2012, *ApJL*, TSS 플레어 검증 권고; DOI 확인요).
- Pulkkinen, A. et al. (2013, *Space Weather* 11, dB/dt·GIC 검증 timing·spatial; 권·페이지 확인요).

**표준 교과서·정의 (실재; 공통편·30과 공유)**
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·QQ·회귀·reliability 표준).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (분할표·HSS·Brier·ROC·확률검증).
- Nash & Sutcliffe (1970, *J. Hydrology* 10(3), 효율지표 원형 — PE/NSE 골격).
- Fisher, *Statistical Analysis of Circular Data* (Cambridge, 원형통계); Bowers, Morton & Mould (2000, *Applied Ocean Research* 22(1):13–30, 원형통계).
- Sakoe & Chiba (1978, *IEEE Trans. ASSP*, DTW; DOI 확인요).

**소프트웨어 (실존 도구)**
- `cartopy` + **`add_basemap()`**(→[`plotting_maps.md`]) — TEC 지도·정점 위치 지도의 해안선/육지+위경도 라벨(필수).
- `aacgmv2` — AACGM-v2 지자기좌표 변환(MLT–자기위도 재구성): https://aacgmv2.readthedocs.io
- `spaceweather` — Kp/ap·OMNI 지수 접근(GFZ/celestrak/OMNI): https://pypi.org/project/spaceweather ; `pysat`(Stoneback et al. 2018, *JGR*), SpacePy(OMNI·CDF), `sunpy`(GOES X선 timeseries — 플레어 라벨).
- `astropy.timeseries.LombScargle`(불규칙 표본 27일 주기)·`scipy.signal`(welch·coherence)·`pycwt`(wavelet coherence).
- `dtaidistance`/`tslearn`/`dtw-python`(DTW, Sakoe–Chiba band).
- `sklearn.metrics`(roc_curve·roc_auc_score)·`sklearn.calibration`(calibration_curve)·`xskillscore`/`scores`(기상 확률·분할표)·`matplotlib`/`numpy`/`scipy.stats`(circmean/circstd·linregress).
- 공통 그림(Taylor·Target·QQ·reliability·ROC·rank hist·Brier/CRPS·return-level)은 **재구현 말고 [`16_fig_common.md`] 재사용**.

**확인요 (확정 인용 금지 — §G-5)**
- Kay & Palmerio (2024) 및 Camporeale (2025)·Verbeke (2019): 제목·저널·연도·핵심수치는 웹 확인, **정확한 권·페이지·일부 DOI는 인용 전 원문 재확인(확인요)**.
- Petrova et al. (2021, F10.7 Kalman filter, *ApJS* 254): 제목·저널·연도·RMSE 범위 확인, **DOI 확인요**.
- Matzka et al. (2021, Kp/ap 정의), Pulkkinen et al. (2013), Hernández-Pajares et al. (2009/2017, IGS GIM·dSTEC), Bloomfield et al. (2012), Sakoe & Chiba (1978): 주제·저자·저널은 표준 인용이나 이 세션에서 권·페이지·DOI 전부 재확인은 못 함(**확인요**).
- 해석 임계·사례수치(Dst RMSE 수십 nT·CME MAE≈10 h·TEC RMSE 야간 1–2/주간 4–5 TECU·Kp MAE 0.5–1.0·F10.7 RMSE 5–27 sfu 등)는 **특정 사건·표본·모델 advisory** — 태양활동 위상·위도대·폭풍여부·리드타임 의존(§G-4).
- 지자기지수(Kp/Dst/ap/AE/SYM-H)·F10.7·TEC는 정식 CF standard_name 부재 사례 많음 → 변수명·단위(nT/TECU/sfu) 기반 라우팅(→[`30`]).
