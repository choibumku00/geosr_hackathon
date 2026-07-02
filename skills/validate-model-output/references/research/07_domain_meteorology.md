# 도메인: 기상·대기 (Meteorology / Atmosphere) — 분석·검증 방법 카탈로그

이 문서는 수치모델(NWP·다운스케일링) 결과를 ERA5 같은 권위 재분석자료·관측소·위성과 비교·검증할 때 쓰는 기상·대기 도메인의 분석/검증 방법을 망라한 레퍼런스다. 바람(u/v·풍속·풍향), 2m 기온, 해면기압(MSLP), 강수(연속+범주+공간+극값), 상대습도, 경계층·안정도, 분포 비교, 공간(객체/이웃) 검증, 다운스케일링·바이어스보정 검증, 확률·앙상블 검증, 그리고 ERA5를 기준값으로 사용할 때의 주의점을 다룬다. 각 방법은 "메서드 카드" 형식으로 정의·수식·적용 자료형·해석 기준·한계·출처를 정리했다.

**핵심 원칙 3가지** — (1) 검증 지표는 변수의 통계적 성질(연속/범주/원형/벡터/확률/극값)에 맞춰 골라야 한다. (2) 단일 지표가 아니라 다수 지표를 함께 봐야 한다(예: ME+RMSE+상관+분포). (3) "우리 모델 vs ERA5/관측/위성" 비교는 거의 항상 **격자↔지점 정합(시공간 정렬·보간·재격자화)** 단계를 먼저 거쳐야 하며, 이 전처리가 결과를 좌우한다(아래 '시공간 정합' 카드 참조).

## 이 파일에 담은 방법 (한 줄 목차)
- **시공간 정합·전처리**: 격자↔지점 보간, 공통격자 재격자화, 페어링·결측·이중계산 주의 (← 모든 비교의 전제)
- **연속 변수 기본 통계**: 평균오차/편향 ME·Bias, 평균절대오차 MAE, 평균제곱근오차 RMSE, MSE 분해, 상관계수, NRMSE/정규화
- **종합·요약 진단**: Taylor 다이어그램, Willmott 일치도지수 d, Murphy MSE Skill Score, Murphy–Winkler 분포지향(joint distribution) 검증틀
- **바람 벡터 검증**: 벡터 RMSE(VRMSE), 풍속 RMSE/Bias, u·v 성분 검증, 벡터 상관
- **풍향(원형 변수) 검증**: 원형 평균오차·MAE(±180° 보정), 원형 상관, 풍향 RMSE 한계
- **2m 기온**: 기온 편향·RMSE, 일변동·주야 분리 검증, 고도보정(lapse-rate) 주의
- **해면기압 MSLP·종관장**: 편향·RMSE, S1 경도 점수, 500 hPa 이상편차 상관 ACC, 종관 패턴 검증
- **강수(연속)**: 강수 RMSE/MAE 주의(double penalty), 로그/제곱근 변환, 강수 분포·분위(QQ) 검증
- **강수(범주)**: 분할표, POD·FAR·FBI·CSI·ETS·HSS·HK(PSS)
- **강수(극값·희박사건)**: 극값의존지수 EDI/SEDI(희박사건 비퇴화 점수)
- **강수(공간·이웃·객체)**: Fractions Skill Score FSS, 강도-스케일(intensity-scale), SAL, MODE(객체기반), 공간검증법 비교(SVMI)
- **분포·확률밀도 비교**: QQ-플롯, Kolmogorov–Smirnov, Perkins PDF 기량점수, 분산비
- **상대습도·습도 변수**: RH 검증, 노점·비습 검증, 포화·상한 절단 주의
- **경계층·안정도**: 경계층고도(PBLH) 검증, 안정도(Richardson 수·Monin–Obukhov 길이) 평가
- **다운스케일링·바이어스보정 검증**: PP/MOS 교차검증, 분위매핑(quantile mapping) 검증, 분포·극값·변동성·시간상관·비정상성 검증
- **확률·앙상블 검증**: Brier Score/BSS, CRPS/CRPSS, ROC/AUC, Rank histogram, 신뢰도 다이어그램
- **ERA5를 기준으로 쓸 때 주의점**(메서드 카드 형태로 정리)

---

### 시공간 정합·페어링 (검증 전처리 Spatiotemporal Matching / Pairing)
- **무엇을 측정/검증하나**: 측정이 아니라 **모든 비교의 전제 조건**. "우리 모델(NetCDF 격자) vs ERA5(격자) vs 관측소(CSV 시계열) vs 위성"을 같은 시각·같은 위치·같은 변수정의로 맞추는 단계. 잘못하면 이후 모든 지표가 무의미해진다.
- **정의·방법**:
  - **격자→지점**: 모델/재분석 격자값을 관측소 위경도로 보간(최근접 nearest, 양선형 bilinear, 거리역가중 IDW). 표면변수(기온·기압)는 표고차 보정 동반.
  - **지점→격자**: 지점관측을 격자에 객관분석(크리깅·OI)하면 대표성 오차 유입 — 가급적 "격자를 지점으로" 방향 권장.
  - **격자↔격자(재격자화 regridding)**: 해상도 다른 두 격자는 공통격자로 재격자화. 보존적(conservative) 재격자화는 강수·플럭스 등 적분량에, 양선형/이중삼차는 연속장에 사용.
  - **시간정합**: 순간값 vs 누적값(강수), 시각정의(UTC/local, 적분 시간창 00–01 vs 정시), 시간평균 변수의 라벨링을 일치시켜야 함.
- **적용 도메인/자료형**: 격자(NetCDF)·시계열(CSV)·위성 전반.
- **입력·전제**: 좌표계·투영·시간대 메타데이터 정확. 결측 동기화 마스크. 관측 품질관리(QC) 선행.
- **해석 기준**: 정합 자체엔 점수가 없으나, 보간법·재격자화법·임계 페어링 규칙을 **반드시 문서화**해야 재현·비교가 가능.
- **한계·주의**: 보간이 극값을 평활(약화)시킴 → 극값 검증 전 보간 최소화. 최근접은 위치오차, 양선형은 평활. 누적강수 시간창 불일치는 흔한 치명적 오류. 위성 격자(swath)와 모델 격자의 발자국(footprint)·관측시각 차이 보정 필요.
- **출처**: WMO/WWRP-JWGFVR Forecast Verification 권고(검증 전 정합 절차); CDO/xESMF 등 재격자화 도구 문서(보존적 재격자화 관행) — 표준 실무 관행.

---

### 평균오차·편향 (평균오차 Mean Error / Bias)
- **무엇을 측정/검증하나**: 모델이 관측·기준값 대비 평균적으로 과대/과소 예측하는 계통오차(systematic bias).
- **정의·수식**: ME = (1/N) Σ (F_i − O_i). F=예측, O=관측. 양수면 과대, 음수면 과소.
- **적용 도메인/자료형**: 모든 연속 변수(기온·기압·풍속·습도). 격자(격자점별/영역평균)·시계열 모두.
- **입력·전제**: 예측·관측이 동일 시각·동일 위치로 정렬(보간)되어 있어야 함. 결측 동기 처리 필요.
- **해석 기준**: 0에 가까울수록 좋음. 단, 양/음 오차가 상쇄돼 0이 될 수 있어 ME만으로는 정확도를 못 본다 — 반드시 RMSE/MAE와 병행.
- **한계·주의**: 부호 상쇄로 오차 크기를 과소평가. 풍향 등 원형 변수에는 그대로 쓰면 안 됨(원형 평균 사용).
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (표준 교과서); WMO/WWRP-JWGFVR 검증 지침.

---

### 평균절대오차 (평균절대오차 Mean Absolute Error, MAE)
- **무엇을 측정/검증하나**: 오차의 평균 크기(부호 무시). 전형적 오차 규모.
- **정의·수식**: MAE = (1/N) Σ |F_i − O_i|.
- **적용 도메인/자료형**: 모든 연속 변수, 격자·시계열.
- **입력·전제**: 정렬·동기화된 예측·관측 쌍.
- **해석 기준**: 작을수록 좋음. 변수 단위와 같아 해석 직관적. RMSE보다 이상치(outlier)에 덜 민감.
- **한계·주의**: 큰 오차를 RMSE만큼 강하게 벌하지 않음. 풍향은 ±180° 보정 후 사용.
- **출처**: Willmott & Matsuura (2005, *Climate Research* 30, 79–82) — MAE vs RMSE 비교; Wilks (표준 교과서).

---

### 평균제곱근오차 (평균제곱근오차 Root Mean Square Error, RMSE)
- **무엇을 측정/검증하나**: 오차의 표준적 크기. 큰 오차에 가중(제곱)되는 정확도 지표.
- **정의·수식**: RMSE = sqrt( (1/N) Σ (F_i − O_i)² ). 관계: MSE = Bias² + 분산성분(오차분산). 중심화 RMSE(CRMSE)는 평균을 뺀 후 계산(편향 제외).
- **적용 도메인/자료형**: 모든 연속 변수, 격자·시계열. 기상 검증의 사실상 표준 지표.
- **입력·전제**: 정렬·동기화. 분포가 비대칭(강수 등)이면 변환 고려.
- **해석 기준**: 작을수록 좋음. 변수별 관행적 목표치 존재(예: 단기 2m 기온 ~1–2 K, MSLP ~1–2 hPa는 좋은 수준 — 자료·리드타임 의존).
- **한계·주의**: 큰 오차·이상치에 민감, N 의존, 변수 단위 의존. 원형 변수에 직접 적용 불가.
- **출처**: Wilks (표준 교과서); Chai & Draxler (2014, *Geoscientific Model Development* 7, 1247–1250) — RMSE 사용 정당성.

---

### 정규화 RMSE·무차원 오차 (정규화오차 NRMSE / Normalized Errors)
- **무엇을 측정/검증하나**: 단위·규모가 다른 변수(기온 K vs 풍속 m/s vs 강수 mm)나 지역을 가로질러 오차를 **무차원으로 비교**.
- **정의·수식**: NRMSE = RMSE / (관측 범위 또는 관측 평균 또는 관측 표준편차). 표준편차 정규화 시 NRMSE = RMSE/s_O(Taylor 다이어그램의 반경 축과 연결). 백분율로도 표기.
- **적용 도메인/자료형**: 다변수·다지역 종합 비교, 격자·시계열.
- **입력·전제**: 정규화 분모를 무엇으로 쓸지 일관·명시(범위 vs 평균 vs 표준편차로 값이 크게 달라짐).
- **해석 기준**: 작을수록 좋음. 변수 간 상대 순위 비교에 유용.
- **한계·주의**: 분모 선택에 민감. 관측 평균이 0 근처면(예: 이상편차) 불안정. 절대 임계 관행 없음.
- **출처**: Wilks (표준); 정규화 관행은 Taylor (2001) 다이어그램과 함께 통용.

---

### MSE 분해 (평균제곱오차 분해 MSE Decomposition)
- **무엇을 측정/검증하나**: 전체 오차를 편향·분산·위상(상관) 성분으로 분리해 오차 원인 진단.
- **정의·수식**: MSE = (F̄ − Ō)² + (s_F − s_O)² + 2 s_F s_O (1 − r). 차례로 편향제곱, 분산차, 상관부족(위상오차) 기여.
- **적용 도메인/자료형**: 모든 연속 변수, 시계열·격자.
- **입력·전제**: 표준편차 s_F, s_O와 상관 r 계산 가능해야 함.
- **해석 기준**: 각 항의 상대 크기로 "계통편향형 vs 변동성부족형 vs 위상어긋남형" 오차 진단.
- **한계·주의**: 정상성(stationarity) 가정. 분포가 크게 비정규면 해석 제한.
- **출처**: Murphy (1988, *Monthly Weather Review* 116, 2417–2424) — skill score와 분해; Taylor (2001, *Journal of Geophysical Research* 106(D7)).

---

### 피어슨 상관계수 (피어슨 상관 Pearson Correlation, r / 이상편차 상관 ACC)
- **무엇을 측정/검증하나**: 예측·관측의 시간/공간 변동 패턴 일치(위상·동조성). 크기보다 패턴.
- **정의·수식**: r = Σ(F−F̄)(O−Ō) / sqrt(Σ(F−F̄)² Σ(O−Ō)²). 기후값 제거 후 계산 시 이상편차상관(Anomaly Correlation Coefficient, ACC).
- **적용 도메인/자료형**: 모든 연속 변수, 시계열·공간장(특히 MSLP·지위고도 패턴).
- **입력·전제**: 정렬. ACC는 동일 기후평균 필요.
- **해석 기준**: 1에 가까울수록 좋음. 종관 패턴 예측에서 ACC≥0.6은 흔히 "유용한 예측" 기준으로 통용(아래 500 hPa ACC 카드 참조).
- **한계·주의**: 편향에 둔감(절대값 차이 못 봄), 이상치 민감, 비선형 관계 과소평가. 자료 시계열의 자기상관 때문에 유효표본수가 줄어 유의성 과대평가될 수 있음.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (표준); Wilks (표준 교과서).

---

### Taylor 다이어그램 (Taylor Diagram)
- **무엇을 측정/검증하나**: 상관계수, 표준편차(변동성), 중심화 RMSE를 한 평면에 동시 표시해 여러 모델·변수를 종합 비교.
- **정의·수식**: 코사인 법칙 기하 — 방위각=상관 r, 반경=표준편차 비, 기준점과의 거리=중심화 RMSE. 관계: CRMSE² = s_F² + s_O² − 2 s_F s_O r.
- **적용 도메인/자료형**: 격자장·시계열, 다중 모델/실험 비교에 특히 유용.
- **입력·전제**: 예측·관측 표준편차와 상관 산출. 보통 표준편차 정규화(관측으로 나눔).
- **해석 기준**: 기준점(관측)에 가까운 점일수록 우수(상관 높고 변동성 일치).
- **한계·주의**: 평균편향(ME)은 표시 안 됨 — 별도 확인 필요. 중심화 통계라 bias 정보 손실. (보완: 마커 크기/색으로 bias를 덧입히는 변형 사용 권장.)
- **출처**: Taylor (2001, *Journal of Geophysical Research* 106(D7), 7183–7192).

---

### Willmott 일치도지수 (Index of Agreement, d)
- **무엇을 측정/검증하나**: 예측-관측 일치도를 0–1로 표준화한 무차원 지표(상관의 대안).
- **정의·수식**: d = 1 − [ Σ(F−O)² / Σ(|F−Ō| + |O−Ō|)² ]. 개선판 d1(절대값), refined d_r 존재.
- **적용 도메인/자료형**: 연속 변수(기온·습도·기압 등), 시계열·격자.
- **입력·전제**: 정렬된 쌍, 관측 평균 Ō.
- **해석 기준**: 1에 가까울수록 좋음. 단독 사용보다 RMSE/MAE 보조 지표로.
- **한계·주의**: 큰 값에 민감(제곱), 절대 해석 기준 모호, 모델 간 상대비교용으로 적절.
- **출처**: Willmott (1981, *Physical Geography* 2, 184–194); Willmott et al. (2012, *Int. J. Climatology* 32, 2088–2094) refined d_r.

---

### Murphy 기량점수 (평균제곱오차 기량점수 MSE Skill Score, MSESS)
- **무엇을 측정/검증하나**: 기준예보(기후값·지속성) 대비 모델의 상대적 향상(skill).
- **정의·수식**: SS = 1 − MSE_forecast / MSE_reference. 기준이 기후값이면 MSESS, 지속성이면 그에 대한 skill.
- **적용 도메인/자료형**: 모든 연속 변수, 시계열·격자.
- **입력·전제**: 동일 표본에 대한 기준예보 MSE 산출 필요.
- **해석 기준**: 1=완벽, 0=기준과 동등, <0=기준보다 나쁨.
- **한계·주의**: 기준예보 선택에 결과가 크게 좌우됨 — 기준을 반드시 명시.
- **출처**: Murphy (1988, *Monthly Weather Review* 116, 2417–2424); Jolliffe & Stephenson (표준).

---

### 분포지향 검증틀 (Murphy–Winkler 결합분포 Distributions-Oriented Verification)
- **무엇을 측정/검증하나**: 단일 요약점수 대신 **예측·관측의 결합분포 p(F,O)**를 검증의 출발점으로 삼는 일반 틀. 정확도·편향뿐 아니라 신뢰도(reliability)·분해능(resolution)·예리함(sharpness)·불확실성을 한 체계에서 진단.
- **정의·수식**: 결합분포를 두 방식으로 분해 — (1) **보정-정련(calibration-refinement)**: p(F,O)=p(O|F)·p(F) → 신뢰도·예리함. (2) **우도-기준율(likelihood-base rate)**: p(F,O)=p(F|O)·p(O) → 판별력·기준빈도. 많은 표준점수(Brier 분해, ME, 상관)가 이 틀의 특수해.
- **적용 도메인/자료형**: 연속·범주·확률 예보 전반, 시계열·격자.
- **입력·전제**: 충분한 표본으로 조건부 분포 추정 가능해야 함. 구간화(binning) 필요.
- **해석 기준**: 단일 점수가 아니라 "왜 좋은/나쁜가"를 조건부로 진단. 신뢰도 다이어그램·조건부 quantile 플롯이 이 틀의 시각화.
- **한계·주의**: 표본이 적으면 조건부 분포 추정 불안정. 요약점수보다 해석·계산이 무겁다.
- **출처**: Murphy & Winkler (1987, *Monthly Weather Review* 115, 1330–1338) — general framework; Jolliffe & Stephenson, *Forecast Verification* (표준, 본 틀 정리).

---

### 벡터 RMSE (벡터 평균제곱근오차 Vector RMSE, VRMSE)
- **무엇을 측정/검증하나**: 바람을 u·v 2차원 벡터로 보고 풍속·풍향 오차를 동시에 반영한 전체 벡터오차.
- **정의·수식**: VRMSE = sqrt( (1/N) Σ [ (u_F−u_O)² + (v_F−v_O)² ] ). 벡터차의 크기 RMS. (풍속 RMSE보다 항상 크거나 같음 — 방향오차 포함하므로.)
- **적용 도메인/자료형**: 바람장(격자·관측소·라디오존데·산란계 위성), 시계열·격자.
- **입력·전제**: u=−ws·sin(θ), v=−ws·cos(θ) 등 일관된 부호 규약으로 u/v 변환. 동일 고도·시각 정렬.
- **해석 기준**: 작을수록 좋음. 풍속·풍향 오차를 한 지표로 요약하므로 풍계 검증의 권장 1차 지표.
- **한계·주의**: 속도·방향 기여를 분리해 보여주지 않음(원인 진단엔 성분/풍향 별도 필요). 단위는 m/s.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (벡터검증 장); WMO/WWRP-JWGFVR 표면바람 검증 지침.

---

### 풍속 검증 (풍속 편향·RMSE Wind Speed Bias / RMSE)
- **무엇을 측정/검증하나**: 풍속(스칼라) 자체의 계통오차·정확도. 풍력·해상·항공 응용에 직접적.
- **정의·수식**: 풍속 ws = sqrt(u²+v²)에 ME·MAE·RMSE 일반식 적용.
- **적용 도메인/자료형**: 관측소·부이·산란계(scatterometer) 위성, 격자·시계열.
- **입력·전제**: 동일 측정고도(보통 10 m). 고도 다르면 로그/멱법칙 풍속 보정(roughness, z0) 필요.
- **해석 기준**: 작을수록 좋음. 풍력 응용은 약풍(<3 m/s)·강풍 구간별로 분리 평가가 관행.
- **한계·주의**: 재분석/모델은 복잡지형 과소·평탄해안 과대 경향(ERA5 카드 참조). 풍속만 보면 방향오차 놓침. 풍속은 양의 왜도 분포라 평균지표 외에 분위(QQ)·분포 비교 권장.
- **출처**: Carvalho et al. / "Evaluation of ERA5, ERA5-Land, CERRA and NEWA datasets in reproducing observed near-surface wind speeds across Spain" (*ScienceDirect*, 2026); WMO 표면바람 검증 지침.

---

### 바람 성분 검증 (u·v 성분 Bias / RMSE)
- **무엇을 측정/검증하나**: 동서(u)·남북(v) 성분 각각의 편향·오차. 계통적 방향치우침 진단.
- **정의·수식**: u, v 각각에 ME·RMSE 적용. u-bias·v-bias로 평균 풍계 치우침 파악.
- **적용 도메인/자료형**: 바람장(격자·관측·연직 프로파일), 시계열·격자.
- **입력·전제**: 일관된 u/v 부호 규약, 동일 고도·시각.
- **해석 기준**: 각 성분 bias가 0에 가까울수록 좋음. u/v bias 조합으로 평균 풍향 치우침 해석.
- **한계·주의**: 성분 RMSE는 직관성 낮음 — VRMSE/풍속/풍향으로 보완.
- **출처**: Jolliffe & Stephenson (벡터검증); Schuhen, Thorarinsdottir & Gneiting (2012, *Monthly Weather Review* 140(10), 3204–3219) — wind vector EMOS(성분 정규화·보정 사례).

---

### 벡터 상관 (벡터 상관 Vector Correlation)
- **무엇을 측정/검증하나**: 2차원 바람 벡터 시계열의 방향·크기 동조성(스칼라 상관의 벡터 확장).
- **정의·수식**: Crosby/Breaker/Gemmill (1993) 텐서 기반 벡터상관계수(0–2 범위 정규화 버전). 복소수 u+iv 상관으로도 계산.
- **적용 도메인/자료형**: 바람·해류 등 2D 벡터 시계열, 관측소·격자.
- **입력·전제**: 동기화된 벡터 쌍, 좌표계 일관성.
- **해석 기준**: 값이 클수록(정규화 정의의 상한에 가까울수록) 벡터 변동 동조성 높음.
- **한계·주의**: 정의가 여럿이라 사용한 정의 명시 필요. 편향은 못 봄.
- **출처**: Crosby, Breaker & Gemmill (1993, *Journal of Atmospheric and Oceanic Technology* 10(3), 355–367) — vector correlation.

---

### 풍향 원형 검증 (풍향 원형통계 Wind Direction Circular Statistics)
- **무엇을 측정/검증하나**: 풍향(0–360° 순환 변수)의 계통적 회전편향·평균 방향오차. 일반 산술평균/RMSE를 쓰면 360°↔0° 불연속으로 오류 발생.
- **정의·수식**: 방향차를 (−180°, +180°]로 보정: Δθ = ((θ_F − θ_O + 180) mod 360) − 180. 원형 평균은 단위벡터 합 atan2(Σsinθ, Σcosθ). 원형 분산 = 1 − R̄ (R̄=평균 결과길이). 풍향 MAE = mean(|Δθ|), 풍향 RMSE = sqrt(mean(Δθ²)).
- **적용 도메인/자료형**: 풍향(관측소·부이·산란계), 시계열·격자.
- **입력·전제**: 약풍 시 풍향이 불안정 → 풍속 임계값(예: ≥1–2 m/s)으로 필터링하는 관행.
- **해석 기준**: |편향|·MAE 작을수록 좋음. 풍향 RMSE의 이론적 최대는 180°, "상대 RMSE = RMSE/180°"로 정규화하기도 함.
- **한계·주의**: 약풍에서 풍향 정의 모호 → 가중(풍속가중) 또는 임계 필터 필요. 표준 검증 패키지(MET 등)도 별도 처리 권고.
- **출처**: Mardia & Jupp, *Directional Statistics* (Wiley, 표준); dtcenter/MET 문서(풍향 RMSE/Bias/MAE 처리 관행).

---

### 2m 기온 검증 (지상 2m 기온 2-m Temperature Verification)
- **무엇을 측정/검증하나**: 지상 2m 기온의 편향·정확도. 주야·일변동 재현, 지형/표면 영향.
- **정의·수식**: ME·MAE·RMSE 일반식. 일변동(diurnal) 검증은 시간대(local hour)별로 분리 집계.
- **적용 도메인/자료형**: 관측소(AWS)·격자(재분석/모델 2m), 시계열·격자.
- **입력·전제**: 관측소 표고와 모델 격자 표고 차이 보정(보통 환경감률 −6.5 K/km lapse-rate). 동일 시각(UTC/local).
- **해석 기준**: RMSE 작을수록 좋음. 주간 최고/야간 최저 따로 보면 모델 표면·복사·경계층 결함 진단. 단기 RMSE ~1–2 K가 흔한 양호 기준(자료 의존).
- **한계·주의**: 고지대·해안에서 격자 대표성·표고 불일치로 큰 오차. 야간 강안정층(역전층) 재현이 어려움. lapse-rate 보정 자체가 오차원.
- **출처**: Wilks (표준 교과서); "Investigation on potential and limitations of ERA5 downscaled by a convection-permitting model over Italy" (*Climate Dynamics*, 2023) — ERA5 2m 기온 평탄·해안 과대 경향.

---

### 해면기압 검증 (해면기압 MSLP Verification)
- **무엇을 측정/검증하나**: 해면기압(MSLP)의 편향·정확도와 종관 패턴(저기압 위치·강도) 재현.
- **정의·수식**: ME·RMSE 일반식. 패턴 평가는 공간 ACC, 등압선 경도는 S1 점수 사용.
- **적용 도메인/자료형**: 관측소(해면환산)·격자(재분석/모델), 시계열·격자.
- **입력·전제**: 관측소 기압의 해면환산 정확성, 동일 시각.
- **해석 기준**: RMSE 작을수록 좋음(단기 ~1–2 hPa 양호). 저기압 중심위치 오차(km)·중심기압 오차를 별도 산출하기도.
- **한계·주의**: 고지대 해면환산 오차. 평균 RMSE는 작아도 폭풍(개별 저기압) 강도/위치 오차는 클 수 있음 — event-based 검증 병행.
- **출처**: Jolliffe & Stephenson (표준); WMO NWP 검증 권고.

---

### S1 경도 점수 (기압장 경도 점수 S1 Gradient Score)
- **무엇을 측정/검증하나**: 기압·지위고도 등 장(field)의 수평 경도(gradient) 예측 정확도 — 종관 패턴 위치/형태 평가의 고전 지표.
- **정의·수식**: S1 = 100 × Σ|ΔG_F − ΔG_O| / Σ max(|ΔG_F|, |ΔG_O|). ΔG는 인접 격자 간 경도. 0=완벽, 클수록 나쁨.
- **적용 도메인/자료형**: 격자장(MSLP·500hPa 고도), 공간장 검증.
- **입력·전제**: 동일 격자, 경도 계산 방향 일관.
- **해석 기준**: 역사적으로 S1≈20 우수, ≈70 무기량 수준(자료·해상도 의존). 모델 개선 추적의 장기 지표.
- **한계·주의**: 해상도·격자 간격에 민감, 절대 임계값은 상대적. 현대엔 ACC·RMSE 보조로 사용.
- **출처**: Teweles & Wobus (1954, *Bulletin of the American Meteorological Society* 35, 455–463) — S1 score(고전); WMO 검증 권고에 수록.

---

### 500 hPa 이상편차 상관 (종관장 이상편차 상관 500-hPa Geopotential ACC)
- **무엇을 측정/검증하나**: 500 hPa 지위고도(또는 MSLP) 이상편차장의 공간 패턴 예측력 — 전 세계 운영센터의 **중기예보 표준 스코어카드 지표**.
- **정의·수식**: ACC = Σ(F'−F̄')(O'−Ō') / sqrt(Σ(F'−F̄')² Σ(O'−Ō')²), 여기서 '는 기후값을 뺀 이상편차. 보통 영역·계절 기후값 사용.
- **적용 도메인/자료형**: 격자 종관장(500 hPa Z, MSLP, 850 hPa T), 공간장.
- **입력·전제**: 동일 기후평균(climatology) 정의. 위도 가중(area weighting) 적용.
- **해석 기준**: 운영 관행상 **ACC ≈ 0.6**을 "유용 예측한계(useful skill)", **ACC ≈ 0.5**를 무기량 경계로 본다. 1에 가까울수록 우수.
- **한계·주의**: 사용한 기후값·영역·가중에 민감. 편향(ME)은 못 봄 — RMSE/bias 병행. 이상편차 정의가 센터마다 달라 절대 비교 시 주의.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (표준, ACC 장); WMO 측면(WMO Manual on the GDPFS) 표준 검증 스코어 — 표준 지침(확인요).

---

### 강수 연속 검증 (강수량 연속 Continuous Precipitation Verification)
- **무엇을 측정/검증하나**: 강수량(연속, 비대칭·0 과다 분포)의 편향·정확도.
- **정의·수식**: ME·MAE·RMSE 적용. 강한 비대칭 때문에 로그(log(x+a))/제곱근 변환 후 평가하거나 분위(QQ) 비교 권장.
- **적용 도메인/자료형**: 관측소·레이더·위성(강수)·격자, 시계열·격자.
- **입력·전제**: 누적시간(1h/24h) 일치, 게이지 손실(undercatch) 보정 유의.
- **해석 기준**: RMSE/MAE 작을수록 좋음. 단, 0이 많고 극값이 길어 평균지표 해석 주의 — 분포·분위 비교가 더 유익.
- **한계·주의**: 적은 수의 강한 강수가 RMSE를 지배. "double penalty"(위치 약간 어긋난 강한 비가 miss+false alarm로 이중 처벌)로 고해상 모델이 불리해짐 → 범주/공간 검증 병행 필수.
- **출처**: Wilks (표준); CAWCR(호주) Forecast Verification 페이지(연속 강수 지표).

---

### 강수 범주 검증: 분할표 (분할표 Contingency Table 기반 범주 점수)
- **무엇을 측정/검증하나**: 임계값(예: ≥1, ≥10 mm) 초과 사건(event/non-event)의 적중·실패. 예/아니오 예보 품질.
- **정의·수식**: 2×2 분할표 a=hits, b=false alarms, c=misses, d=correct negatives. 파생:
  - 적중률 POD(=H) = a/(a+c)
  - 오경보비 FAR = b/(a+b)
  - 빈도편향 FBI = (a+b)/(a+c)
  - 임계성공지수 CSI(=TS) = a/(a+b+c)
  - 동등위협점수 ETS(Gilbert) = (a − a_r)/(a+b+c − a_r), a_r=(a+b)(a+c)/n (무작위 hit 제거)
  - Heidke 기량점수 HSS, Hanssen–Kuipers 판별 HK(=PSS)=POD − POFD
- **적용 도메인/자료형**: 강수·임계초과 사건(돌풍·결빙 등), 격자·관측소.
- **입력·전제**: 임계값 정의, 사건이 너무 희박하지 않게 표본 확보.
- **해석 기준**: POD↑·FAR↓·CSI↑·ETS↑가 좋음. FBI=1이 빈도 일치(>1 과다예보). ETS/HSS/HK는 무작위 대비 기량(0=무기량, 1=완벽). 희박사건엔 ETS·HK도 퇴화 → EDI/SEDI 권장(아래 카드).
- **한계·주의**: 임계값 선택에 강하게 의존(다수 임계 평가 권장). 위치오차에 매우 민감(double penalty). 표본수·기후빈도에 점수 좌우.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (분할표 장); Wilks (표준); CAWCR Forecast Verification.

---

### 강수 극값·희박사건 검증 (극값의존지수 Extremal Dependence Index, EDI / SEDI)
- **무엇을 측정/검증하나**: 임계값을 매우 높게(희박사건: 극한강수·폭풍) 잡았을 때 표준 범주점수(CSI·ETS)가 0이나 자명한 값으로 **퇴화(degenerate)**하는 문제를 피해, 희박사건 예보의 판별력을 안정적으로 측정.
- **정의·수식**: H=POD=a/(a+c), F=POFD=b/(b+d)로 두면 EDI = [log F − log H] / [log F + log H]. SEDI는 (1−H),(1−F)까지 포함해 대칭화: SEDI = [log F − log H + log(1−H) − log(1−F)] / [log F + log H + log(1−H) + log(1−F)]. 범위 −1~+1(1=완벽).
- **적용 도메인/자료형**: 강수·돌풍·결빙 등 임계 희박사건, 격자·관측소.
- **입력·전제**: 임계값(높은 분위, 예: 95·99 퍼센타일) 정의, 분할표 산출.
- **해석 기준**: 사건이 드물어질수록(기준빈도 base rate↓) 비퇴화·기준율 독립이라 극한 검증에 적합. 0=무기량, 양수=기량.
- **한계·주의**: 극히 작은 표본에선 여전히 불안정(부트스트랩 신뢰구간 권장). H 또는 F가 0이면 정의 불가(보정 필요).
- **출처**: Ferro & Stephenson (2011, *Weather and Forecasting* 26(5), 699–713) — EDI/SEDI; North et al. (2013, *Meteorological Applications* 20) SEDI 적용 평가.

---

### 강수 분포·분위 비교 (분포검증 QQ-plot / Kolmogorov–Smirnov / Perkins PDF 기량점수)
- **무엇을 측정/검증하나**: 평균·RMSE가 같아도 다를 수 있는 **분포 전체의 일치**(꼬리·극값·강도 빈도). 강수·풍속처럼 비대칭 변수에 특히 중요.
- **정의·수식**:
  - **QQ-플롯**: 모델·관측의 동일 분위수를 산점. 대각선에서 벗어난 패턴으로 과소/과대·꼬리 편향 진단.
  - **Kolmogorov–Smirnov(KS) 통계**: D = max|CDF_F(x) − CDF_O(x)|. 두 분포 차이의 최대값(0에 가까울수록 일치). p값으로 동일분포 가설 검정.
  - **Perkins 기량점수(S_score)**: 두 PDF를 같은 구간으로 히스토그램화해 겹치는 면적 합 = Σ min(freq_F, freq_O). 0(전혀 안 겹침)~1(완전 일치).
- **적용 도메인/자료형**: 강수·풍속·기온 등 연속 변수의 기후분포, 시계열·격자(공간 풀링).
- **입력·전제**: 충분한 표본, 동일 구간화. KS는 독립표본 가정(자기상관 강하면 p값 과신 주의).
- **해석 기준**: QQ 대각선 근접, KS D 작음, Perkins S→1이 좋음. 다운스케일/바이어스보정 산출물의 분포 재현 평가에 핵심.
- **한계·주의**: KS는 분포 중앙에 민감·꼬리에 둔감. 시계열 자기상관 시 KS p값 신뢰 저하. Perkins는 구간폭(bin) 선택에 민감.
- **출처**: Wilks (표준, QQ·KS); Perkins et al. (2007, *Journal of Climate* 20(17), 4356–4376) — PDF 기반 기량점수.

---

### 강수 공간 검증: Fractions Skill Score (이웃기반 분율 기량점수 FSS)
- **무엇을 측정/검증하나**: 이웃(neighborhood) 크기를 키워가며 강수의 공간 변위(displacement)를 관용하고, 어느 공간 스케일부터 예보가 "유용"한지 평가.
- **정의·수식**: 임계값으로 이진화 후, 반경 n 이웃 내 분율 P_F, P_O 계산. FSS = 1 − MSE(P_F,P_O) / MSE_ref, MSE_ref = (1/N)(ΣP_F² + ΣP_O²). 0=무기량, 1=완벽.
- **적용 도메인/자료형**: 고해상 격자 강수(또는 구름·반사도·위성영상), 공간장.
- **입력·전제**: 동일 격자(또는 공통 격자로 재격자화), 임계값·이웃반경 다중 설정.
- **해석 기준**: FSS가 0.5+f₀/2(f₀=관측 사건 빈도)를 넘는 최소 이웃반경이 "기량 스케일(skillful scale)". 값이 빨리 1에 도달할수록 좋음.
- **한계·주의**: 임계값·이웃반경·도메인 크기에 의존. double penalty를 완화하지만 제거하진 않음. 앙상블 확장판(Necker et al. 2024) 존재.
- **출처**: Roberts & Lean (2008, *Monthly Weather Review* 136, 78–97); Mittermaier & Roberts (2010, *Weather and Forecasting* 25(1)); Necker et al. (2024, *Quarterly Journal of the Royal Meteorological Society* 150, 4457–4477) 앙상블 FSS.

---

### 강도-스케일 검증 (강도-스케일 Intensity-Scale Verification)
- **무엇을 측정/검증하나**: 강수 예보 기량을 강도(임계)와 공간 스케일(웨이블릿 분해)의 함수로 동시 분해.
- **정의·수식**: 예보-관측 이진오차장을 웨이블릿(예: Haar)으로 다중스케일 분해하고 스케일별 MSE 기량점수 산출.
- **적용 도메인/자료형**: 격자 강수장, 공간 검증.
- **입력·전제**: 2의 거듭제곱 격자(웨이블릿 요구), 공통 격자.
- **해석 기준**: 어떤 강도·어떤 스케일에서 기량이 있는지 2D 맵으로 진단.
- **한계·주의**: 도메인/격자 제약, FSS보다 해석이 복잡. 공간검증법 상호비교(ICP/SVMI) 권장 도구 중 하나.
- **출처**: Casati et al. (2004, *Meteorological Applications* 11, 141–154) — intensity-scale; Casati (2010, *Weather and Forecasting* 25(1)) 갱신판.

---

### 강수 공간 검증: SAL (구조-진폭-위치 Structure–Amplitude–Location)
- **무엇을 측정/검증하나**: 도메인(예: 유역) 단위로 강수장의 **구조(S)·진폭(A)·위치(L)** 세 성분을 따로 진단하는 객체기반(feature-based) 공간 검증. double penalty를 회피.
- **정의·수식**:
  - **A(진폭)** = (도메인평균 F − 도메인평균 O) / [0.5(F̄+Ō)] — 총강수 과대(+)/과소(−), 범위 −2~+2.
  - **L(위치)** = 질량중심 거리 + 객체 분산 차이 항(도메인 크기로 정규화), 0~2.
  - **S(구조)** = 강수객체의 크기·형태(객체별 최대값 정규화 적분) 차이, −2~+2. (S>0=객체가 너무 넓고 평평, S<0=너무 좁고 뾰족.)
- **적용 도메인/자료형**: 격자 강수(레이더·위성·모델), 사전지정 도메인(유역·관심영역).
- **입력·전제**: 공통 격자, 객체 식별 임계값(보통 도메인 최대의 일정 비율). 도메인 경계 정의가 결과에 영향.
- **해석 기준**: S·A·L 모두 0에 가까울수록 완벽. 세 성분을 함께 보면 "양은 맞는데 위치 틀림" 같은 오차 유형을 분리 진단.
- **한계·주의**: 도메인 선택·임계값에 민감. 객체가 도메인을 벗어나면 L 왜곡. 단일 종합점수가 아님(3성분 동시 해석 필요).
- **출처**: Wernli, Paulat, Hagen & Frei (2008, *Monthly Weather Review* 136(11), 4470–4487) — SAL; Gilleland et al. (2009) ICP에 포함.

---

### 강수 공간 검증: MODE (객체기반 진단평가 Method for Object-Based Diagnostic Evaluation)
- **무엇을 측정/검증하나**: 강수(또는 반사도·구름) 장에서 **객체(feature)를 식별·매칭**해 객체 속성(면적·위치·방향·강도)의 예보-관측 차이를 진단. "예보된 비구역이 실제 비구역과 얼마나 닮았나"를 사람이 보는 방식으로 정량화.
- **정의·수식**: (1) 합성곱 평활+임계값으로 객체 정의 → (2) 객체쌍 속성(중심거리·면적비·교차·방향·종횡비)으로 퍼지논리 "총관심도(total interest)" 계산 → (3) 임계 이상이면 매칭. 매칭/비매칭 객체수, 속성별 편향 산출.
- **적용 도메인/자료형**: 고해상 격자 강수·레이더 반사도·구름, 공간장.
- **입력·전제**: 공통 격자, 평활반경·임계값·관심도 가중 설정.
- **해석 기준**: 객체 위치·크기·강도 편향을 물리적으로 해석. 전통 점수가 0인데도 "거의 맞았다"를 보여줄 수 있음(double penalty 회피).
- **한계·주의**: 평활·임계·매칭 파라미터에 민감(설정 문서화 필수). 객체가 합쳐지거나 쪼개지면 매칭 모호. 요약 단일점수가 아니라 진단 도구.
- **출처**: Davis, Brown & Bullock (2006, *Monthly Weather Review* 134, 1772–1784, Part I) — MODE; Davis et al. (2009, *Weather and Forecasting* 24) NSSL/SPC 적용; MET 소프트웨어 구현.

---

### 공간 검증법 비교·선택 (공간검증 상호비교 ICP / Spatial Methods Intercomparison)
- **무엇을 측정/검증하나**: 개별 점수가 아니라, 고해상 강수 검증에서 **어떤 공간검증법(이웃/스케일분리/객체/장변형)을 언제 쓸지** 선택하기 위한 메타 레퍼런스.
- **정의·수식**: 4범주 — (1) 이웃(neighborhood/fuzzy): FSS 등, (2) 스케일분리(scale-separation): intensity-scale, (3) 객체/특징(feature-based): SAL·MODE, (4) 장변형(field-deformation): 광류·변위벡터.
- **적용 도메인/자료형**: 고해상 격자 강수·반사도, 공간장.
- **입력·전제**: 동일 사례·공통 격자로 여러 방법 동시 적용 권장.
- **해석 기준**: "double penalty에 강한 단일 점수는 없다" — 목적(위치오차 허용/규모/객체속성)에 따라 방법 조합. 전통 격자점 점수(RMSE·CSI)와 공간점수를 함께 보고.
- **한계·주의**: 방법마다 파라미터·해석이 달라 결과 비교가 어렵다. 메타 분석은 표준 사례셋(ICP cases) 기반.
- **출처**: Gilleland, Ahijevych, Brown, Casati & Ebert (2009, *Weather and Forecasting* 24, 1416–1430) — ICP 종합; Ebert (2008, *Meteorological Applications*) 이웃기반 리뷰.

---

### 상대습도·습도 변수 검증 (상대습도/노점/비습 Humidity Verification)
- **무엇을 측정/검증하나**: 상대습도(RH), 노점온도(Td), 비습/혼합비의 편향·정확도. 구름·강수·안개 진단에 직결.
- **정의·수식**: 변수별 ME·MAE·RMSE. RH는 [0,100%] 절단변수라 상·하한 근처 분포 왜곡 주의. 노점/비습은 거의 비절단 연속이라 보조 검증에 유용.
- **적용 도메인/자료형**: 관측소·라디오존데(연직)·위성(가강수량 TPW), 시계열·격자.
- **입력·전제**: RH 산출식·기준(물/얼음 포화) 일관, 동일 고도·시각.
- **해석 기준**: RMSE 작을수록 좋음. 야간 포화(안개)·저습 구간 분리 평가가 유익.
- **한계·주의**: RH는 포화(100%) 절단으로 RMSE가 사건구간에서 왜곡 → 노점/비습 병행 권장. 라디오존데 습도 센서 저온 편향.
- **출처**: Wilks (표준); WMO 라디오존데 비교(WMO-IOM 보고서) 관행.

---

### 경계층고도 검증 (행성경계층고도 PBLH Verification)
- **무엇을 측정/검증하나**: 모델이 산출/진단한 경계층고도(PBLH)를 라디오존데·라이다·윈드프로파일러 기준과 비교.
- **정의·수식**: 기준 PBLH 산출법: 벌크 리처드슨수법(Richardson number, RM), 온위경도법(GMθ), RH경도법(GMRH), 파셀법(parcel). 검증은 ME·RMSE·상관.
- **적용 도메인/자료형**: 연직 프로파일(라디오존데/라이다), 시계열(주야).
- **입력·전제**: 안정도 분류(대류 CBL/중립 NBL/안정 SBL)별 분리 평가. 기준 산출법 명시(법마다 PBLH 다름).
- **해석 기준**: 주간 CBL은 비교적 일치(상관 ~0.7+ 보고), 야간 SBL은 정의 모호로 불확실 큼.
- **한계·주의**: "참값" 자체가 산출법 의존이라 기준 정의 통일 필요. 야간·전이시간대 큰 불확실성.
- **출처**: Seidel et al. (2010, *Journal of Geophysical Research* 115, D16113) — PBLH 산출법; *Atmospheric Measurement Techniques*(Copernicus) 라디오존데 PBLH 검색법 평가(14권 2021, 16권 2023).

---

### 안정도·난류 모수 검증 (대기안정도 Stability / Monin–Obukhov Verification)
- **무엇을 측정/검증하나**: 대기안정도 지표(벌크 리처드슨수 Ri, Monin–Obukhov 길이 L, 안정도 클래스)와 지표 플럭스의 모델 재현.
- **정의·수식**: Ri = (g/θ)(∂θ/∂z)/(∂U/∂z)². L = −u*³θ_v / (κ g w'θ_v'). 검증은 관측 플럭스타워(에디공분산) 대비 ME·RMSE·산점도.
- **적용 도메인/자료형**: 플럭스타워·라디오존데·연직 프로파일, 시계열.
- **입력·전제**: 표면 플럭스(현열·잠열·운동량) 관측, 안정/불안정 구간 분리.
- **해석 기준**: 안정도 클래스 적중률·플럭스 RMSE로 평가. 야간 안정층에서 모델 과대혼합 경향 점검.
- **한계·주의**: 플럭스 관측 자체 불확실성, 표면 비균질성. 안정도 클래스 경계 임의성.
- **출처**: Stull, *An Introduction to Boundary Layer Meteorology* (Springer, 표준); Monin–Obukhov 상사이론(고전).

---

### 다운스케일링 검증: 교차검증·분포·극값 (다운스케일링 검증 Downscaling Validation)
- **무엇을 측정/검증하나**: 역학적/통계적 다운스케일(PP·MOS) 산출물이 국지 관측의 분포·극값·변동성·시간상관·비정상성을 재현하는지.
- **정의·수식**: 교차검증(leave-one-out / k-fold, 또는 train/test 기간분리) 하에 (1) 정확도: RMSE·상관·범주점수, (2) 분포: 분위(QQ)·확률밀도 일치·KS통계·Perkins S, (3) 극값: 분위·재현주기·극값지수(예: ETCCDI), (4) 변동성: 분산비·일변동, (5) 시간구조: 자기상관·연속건조/습윤일수, (6) 비정상성: 보정·검증기간 기후차를 키워 외삽 성능 평가.
- **적용 도메인/자료형**: 통계 다운스케일(PP=관측-대규모 예측자 학습, MOS=모델출력 보정), 시계열·격자.
- **입력·전제**: 독립 검증표본 확보(누설 방지), 예측자/예측대상 정렬.
- **해석 기준**: 단일 RMSE 최소화에만 의존 금지 — PP/회귀계열은 분산 과소(variance deflation) 경향이라 분포·극값·변동성 지표를 반드시 함께. 비정상성 검증으로 기후변화 외삽 신뢰도 평가.
- **한계·주의**: 교차검증 누설(인접시간 상관), "perfect predictor" 가정의 한계, MOS는 모델버전 변경에 민감. 결정론 회귀는 극값 과소.
- **출처**: Maraun & Widmann, *Statistical Downscaling and Bias Correction for Climate Research* (Cambridge University Press, 2018, 표준); Gutiérrez et al. (2019, *Int. J. Climatology* 39, 3750–3785) VALUE; Legasa et al. (2023, *Geophysical Research Letters* 50(9), e2022GL102525) PP 평가.

---

### 바이어스보정 검증 (분위매핑 Quantile Mapping / Bias Correction Validation)
- **무엇을 측정/검증하나**: 모델/재분석 출력을 관측 분포에 맞추는 바이어스보정(특히 분위매핑 QM·QDM)이 **독립 검증기간**에서 분포·극값·시간구조를 실제로 개선하는지(또는 인위적 왜곡을 넣는지).
- **정의·수식**: QM: x_corr = CDF_obs⁻¹(CDF_mod(x_mod)). QDM(Quantile Delta Mapping)은 변화신호(추세) 보존. 검증은 교차검증 하에 QQ·KS·Perkins S·극값지수·시간상관 변화로 평가.
- **적용 도메인/자료형**: 기온·강수·풍속의 격자/지점 보정, 시계열·격자.
- **입력·전제**: 보정용·검증용 기간 분리(누설 금지), 충분한 분위 추정 표본. 강수는 건일(dry day) 빈도 보정(빈도 적합) 필요.
- **해석 기준**: 분포 일치↑·시간상관/변동성 보존 여부 확인. **평균만 개선되고 극값/시간구조가 망가지면 실패**로 판정.
- **한계·주의**: QM은 시간상관·일관성(변수간/공간) 깨뜨릴 수 있고 외삽(보정범위 밖 극값)에 약함. 표본 밖 분위는 외삽 가정 필요. "정상성(stationarity)" 가정 — 미래기후 적용 시 위험.
- **출처**: Maraun & Widmann (2018, 표준, QM/bias correction 장); Cannon, Sobie & Murdock (2015, *Journal of Climate* 28) — QDM(추세보존 분위매핑).

---

### 확률·앙상블 검증: Brier Score (브라이어 점수 Brier Score / BSS)
- **무엇을 측정/검증하나**: 이진사건(예: 강수≥10mm) 확률예보의 정확도와 신뢰도/분해능.
- **정의·수식**: BS = (1/N) Σ (p_i − o_i)², o∈{0,1}. Murphy 분해: BS = 신뢰도(Reliability) − 분해능(Resolution) + 불확실성(Uncertainty). 기량점수 BSS = 1 − BS/BS_ref(보통 기후값).
- **적용 도메인/자료형**: 확률예보(앙상블·통계), 사건 임계값별.
- **입력·전제**: 확률예보 p와 관측 이진 o, 충분한 표본.
- **해석 기준**: BS 작을수록 좋음, BSS>0이면 기준보다 기량. 신뢰도 항 작을수록 보정 양호.
- **한계·주의**: 희박사건은 불확실성항이 작아 BSS 불안정. 표본/구간화 의존.
- **출처**: Brier (1950, *Monthly Weather Review* 78, 1–3); Murphy (1973, *Journal of Applied Meteorology* 12, 595–600) 분해; Wilks (표준).

---

### 확률·앙상블 검증: CRPS (연속순위확률점수 CRPS / CRPSS)
- **무엇을 측정/검증하나**: 연속 변수의 전체 예측분포(앙상블/확률) 정확도. 결정론 MAE의 확률 일반화.
- **정의·수식**: CRPS = ∫ [F_pred(x) − H(x − o)]² dx (F=예측 CDF, H=헤비사이드). 결정론 예보면 CRPS=MAE로 환원. 신뢰도/분해능 분해 가능. CRPSS = 1 − CRPS/CRPS_ref.
- **적용 도메인/자료형**: 앙상블 NWP·확률 다운스케일(기온·풍속·강수 등), 시계열·격자.
- **입력·전제**: 예측분포(앙상블 멤버 또는 모수분포), 관측값.
- **해석 기준**: 작을수록 좋음(변수 단위). CRPSS>0이면 기준보다 기량.
- **한계·주의**: 강수처럼 0집중 분포는 변형(CRPS for mixed dist) 필요. 작은 앙상블은 편향 → 공정(fair) CRPS 사용 고려.
- **출처**: Hersbach (2000, *Weather and Forecasting* 15, 559–570) — ensemble CRPS 분해; Gneiting & Raftery (2007, *Journal of the American Statistical Association* 102, 359–378) proper scoring rules.

---

### 확률 판별력: ROC / AUC (수신자조작특성 ROC Curve / Area Under Curve)
- **무엇을 측정/검증하나**: 확률예보가 사건/비사건을 **판별(discrimination)**하는 능력 — 보정과 무관하게 "임계 확률을 바꿔가며" POD vs POFD 궤적으로 평가.
- **정의·수식**: 확률 임계값을 0→1로 바꾸며 POD(=H)와 POFD(=F) 산출 → ROC 곡선. 곡선 아래 면적 AUC가 판별력 요약(0.5=무판별, 1=완벽).
- **적용 도메인/자료형**: 확률·앙상블 예보(임계 사건별), 시계열·격자.
- **입력·전제**: 확률예보와 관측 이진, 충분한 표본.
- **해석 기준**: AUC>0.5면 판별력 있음, ≥0.7 흔히 "유용" 기준. 신뢰도(reliability)와 함께 봐야(ROC는 보정 무관).
- **한계·주의**: 보정(편향)은 못 봄 — 신뢰도 다이어그램과 병행. 희박사건·작은 표본에서 AUC 불안정.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (ROC 장); Wilks (표준); Mason & Graham (2002, *Quarterly Journal of the Royal Meteorological Society* 128) ROC 유의성.

---

### 앙상블 신뢰도: Rank Histogram & 신뢰도 다이어그램 (순위 히스토그램 Rank Histogram / Reliability Diagram)
- **무엇을 측정/검증하나**: 앙상블의 통계적 신뢰성(spread-skill). 관측이 앙상블 분포 내 어디에 떨어지는지, 확률예보가 실제 빈도와 맞는지.
- **정의·수식**: Rank histogram(Talagrand) — 각 케이스에서 관측의 앙상블 내 순위 빈도. 균일=신뢰. U자=과소산포(under-dispersion), ∩자=과대산포, 기울기=편향. Reliability diagram — 예보확률 vs 관측상대빈도 그래프(대각선=완벽 신뢰).
- **적용 도메인/자료형**: 앙상블·확률예보, 시계열·격자.
- **입력·전제**: 충분한 케이스, 적절한 구간화(binning).
- **해석 기준**: rank hist 균일·reliability 대각선 근접이 좋음. spread/skill 비율로 산포 적정성 정량화.
- **한계·주의**: 표본 적으면 노이즈, 관측오차가 산포해석 왜곡. rank hist는 신뢰도만(정확도 아님) 봄.
- **출처**: Hamill (2001, *Monthly Weather Review* 129, 550–560) — rank histogram 해석; Wilks (reliability diagram, 표준).

---

### ERA5를 기준값으로 쓸 때 주의점 (ERA5 as Reference — Caveats)
- **무엇을 측정/검증하나**: ERA5(또는 ERA5-Land)를 "관측 대용 기준"으로 삼아 모델을 검증할 때 발생하는 기준자체의 편향·대표성 한계.
- **정의·수식**: 별도 수식 없음. ERA5는 동화된 모델산출(약 31 km 격자)이지 직접 관측이 아님 — "기준의 오차"를 항상 고려.
- **적용 도메인/자료형**: 격자 비교(2m 기온·10m 바람·MSLP·강수·습도) 전반.
- **입력·전제**: ERA5와 모델의 격자·시각·변수정의(예: 누적강수 시간창) 정합. 비교 전 공통격자 재격자화.
- **해석 기준(권고)**:
  - **바람**: 복잡/산악지형 풍속 **과소**(거친 지형 평활·국지 가속 미해상), 평탄·해안에서 **과대**(육해 혼합·거칠기 단순화) 경향 → 지형별 분리·가능하면 실측(부이/산란계) 병용.
  - **2m 기온**: 평탄·해안 약한 **과대**, 고지대(서부 북미·중앙아시아~중국 서부 등)에서 큰 오차 → 표고차 lapse-rate 보정.
  - **강수**: ERA5 강수는 동화·모수화 산물로 불확실 큼 → 강수 검증의 기준으로는 게이지/레이더/위성(IMERG 등) 우선.
  - **희박/극한 사건**: ERA5는 평활화로 극값 과소 경향 → 극값 검증을 ERA5만으로 하지 말 것(EDI/SEDI·QQ로 분포·꼬리 점검).
- **한계·주의**: ERA5 자체가 관측밀도 낮은 지역·해상·고지대에서 신뢰 저하. 동화 관측과 검증 관측이 겹치면 "독립성" 위반. 시간평균 변수의 시각정의 주의. 지역재분석(CERRA·NEWA 등)이 지역 응용에선 더 적합할 수 있음.
- **출처**: Hersbach et al. (2020, *Quarterly Journal of the Royal Meteorological Society* 146, 1999–2049) — ERA5 소개; ERA5/ERA5-Land/CERRA/NEWA 풍속 평가(*ScienceDirect*, 2026); ERA5 CPM 다운스케일 평가(*Climate Dynamics*, 2023).

---

## 출처(References)

표준 참고문헌(실재 확인) 및 본 조사에서 웹으로 점검한 논문·지침. **본 개정에서 WebSearch로 서지정보(저널·권·페이지)를 직접 확인한 항목은 [확인됨]으로 표시**했다. 그 외 '표준 교과서/표준 지침'은 해당 분야의 정전(canonical) 문헌으로 실재하나 본 문서에서 페이지/DOI를 일일이 검증하지 않았다(인용 시 원문 확인 권장). DOI는 임의 생성하지 않았다.

**표준 교과서·지침(canonical)**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences* (Academic Press). — 연속·범주·확률·분포 검증 전반.
- Jolliffe, I. T. & Stephenson, D. B. (eds.) *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley). — 벡터검증·분할표·ROC·skill score·결합분포틀.
- Mardia, K. V. & Jupp, P. E. *Directional Statistics* (Wiley). — 풍향 원형통계.
- Stull, R. B. *An Introduction to Boundary Layer Meteorology* (Springer). — 안정도·Monin–Obukhov.
- Maraun, D. & Widmann, M. *Statistical Downscaling and Bias Correction for Climate Research* (Cambridge University Press, 2018). — 다운스케일링·바이어스보정 검증.
- WMO / WWRP-JWGFVR Forecast Verification 지침 및 CAWCR(호주) Forecast Verification 페이지(https://www.cawcr.gov.au/projects/verification/). — 범주·연속·공간 지표 정의(표준 지침). WMO Manual on the GDPFS — 운영 표준 스코어(ACC 등, 확인요).

**논문·기술문헌(본 조사에서 점검)**
- Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single diagram. *Journal of Geophysical Research* 106(D7), 7183–7192. — Taylor 다이어그램.
- Murphy, A. H. (1988). Skill scores based on the mean square error and their relationships to the correlation coefficient. *Monthly Weather Review* 116, 2417–2424. — MSE skill score·분해.
- Murphy, A. H. & Winkler, R. L. (1987). A general framework for forecast verification. *Monthly Weather Review* 115, 1330–1338. — 결합분포 검증틀. **[확인됨]**
- Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology* 12, 595–600. — Brier score 분해.
- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78, 1–3.
- Willmott, C. J. (1981). On the validation of models. *Physical Geography* 2, 184–194; Willmott et al. (2012) refined index of agreement, *Int. J. Climatology* 32, 2088–2094. — 일치도지수 d / d_r.
- Willmott, C. J. & Matsuura, K. (2005). Advantages of the MAE over RMSE. *Climate Research* 30, 79–82.
- Chai, T. & Draxler, R. R. (2014). RMSE or MAE? *Geoscientific Model Development* 7, 1247–1250.
- Teweles, S. & Wobus, H. B. (1954). Verification of prognostic charts. *Bulletin of the American Meteorological Society* 35, 455–463. — S1 score(고전). **[확인됨]**
- Roberts, N. M. & Lean, H. W. (2008). Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events. *Monthly Weather Review* 136, 78–97. — Fractions Skill Score(FSS).
- Mittermaier, M. & Roberts, N. (2010). Intercomparison of spatial forecast verification methods: identifying skillful spatial scales using the FSS. *Weather and Forecasting* 25(1), 343–354.
- Necker, T. et al. (2024). The fractions skill score for ensemble forecast verification. *Quarterly Journal of the Royal Meteorological Society* 150, 4457–4477 (DOI 10.1002/qj.4824). — 앙상블 FSS. **[확인됨]**
- Casati, B., Ross, G. & Stephenson, D. B. (2004). A new intensity-scale approach for the verification of spatial precipitation forecasts. *Meteorological Applications* 11, 141–154; Casati (2010, *Weather and Forecasting* 25) 갱신판.
- Wernli, H., Paulat, M., Hagen, M. & Frei, C. (2008). SAL—A novel quality measure for the verification of quantitative precipitation forecasts. *Monthly Weather Review* 136(11), 4470–4487. — SAL. **[확인됨]**
- Davis, C., Brown, B. & Bullock, R. (2006). Object-based verification of precipitation forecasts. Part I. *Monthly Weather Review* 134, 1772–1784. — MODE. **[확인됨]**
- Gilleland, E., Ahijevych, D., Brown, B. G., Casati, B. & Ebert, E. E. (2009). Intercomparison of spatial forecast verification methods. *Weather and Forecasting* 24, 1416–1430. — ICP/공간검증법 비교. **[확인됨]**
- Ferro, C. A. T. & Stephenson, D. B. (2011). Extremal dependence indices: improved verification measures for deterministic forecasts of rare binary events. *Weather and Forecasting* 26(5), 699–713. — EDI/SEDI. **[확인됨]**
- Perkins, S. E. et al. (2007). Evaluation of the AR4 climate models' simulated daily max/min temperature and precipitation over Australia using PDFs. *Journal of Climate* 20(17), 4356–4376. — Perkins PDF 기량점수. **[확인됨]**
- Crosby, D. S., Breaker, L. C. & Gemmill, W. H. (1993). A proposed definition for vector correlation in geophysics. *Journal of Atmospheric and Oceanic Technology* 10(3), 355–367. — 벡터 상관. **[확인됨]**
- Schuhen, N., Thorarinsdottir, T. L. & Gneiting, T. (2012). Ensemble model output statistics for wind vectors. *Monthly Weather Review* 140(10), 3204–3219. — wind vector EMOS. **[확인됨]**
- Hersbach, H. (2000). Decomposition of the continuous ranked probability score for ensemble prediction systems. *Weather and Forecasting* 15, 559–570. — CRPS.
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association* 102, 359–378.
- Hamill, T. M. (2001). Interpretation of rank histograms for verifying ensemble forecasts. *Monthly Weather Review* 129, 550–560.
- Mason, S. J. & Graham, N. E. (2002). Areas beneath the ROC curve: statistical significance and interpretation. *Quarterly Journal of the Royal Meteorological Society* 128. — ROC 유의성.
- Seidel, D. J. et al. (2010). Estimating climatological PBL heights from radiosonde observations. *Journal of Geophysical Research* 115, D16113. — PBLH 산출법.
- *Atmospheric Measurement Techniques* (Copernicus), Evaluation of retrieval methods for PBL height from radiosonde data (14, 5977, 2021; 16, 4289, 2023). — PBLH 검증.
- Gutiérrez, J. M. et al. (2019). An intercomparison of a large ensemble of statistical downscaling methods over Europe (VALUE). *International Journal of Climatology* 39, 3750–3785.
- Legasa, M. N. et al. (2023). Assessing three perfect prognosis methods for statistical downscaling of climate change precipitation scenarios. *Geophysical Research Letters* 50(9), e2022GL102525 (DOI 10.1029/2022GL102525). **[확인됨]**
- Cannon, A. J., Sobie, S. R. & Murdock, T. Q. (2015). Bias correction of GCM precipitation by quantile mapping: how well do methods preserve changes? (QDM). *Journal of Climate* 28, 6938–6959.
- Hersbach, H. et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society* 146, 1999–2049. — ERA5.
- "Evaluation of ERA5, ERA5-Land, CERRA and NEWA datasets in reproducing observed near-surface wind speeds across Spain" (*ScienceDirect*, 2026). — ERA5 지형별 풍속 과소/과대. **[확인됨: 존재]**
- "Investigation on potential and limitations of ERA5 downscaled by a convection-permitting model over Italy" (*Climate Dynamics*, 2023). — ERA5 2m 기온 평탄·해안 과대.

*주: [확인됨] 표시 항목은 본 개정 작업에서 WebSearch로 저널·권·페이지·DOI를 대조해 실재를 확인한 것이다. 표시가 없는 표준 교과서/지침은 정전 문헌으로 실재하나 세부 서지(쇄·페이지)는 원문 확인을 권한다. 이전 판에 있던 출처 미상 인용(저자 불명의 "Pinson et al." 표기, arXiv 식별번호 미검증 항목)은 검증 가능한 정확한 서지로 교체했다.*
