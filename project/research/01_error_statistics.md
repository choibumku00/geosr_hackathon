# 01. 오차·정확도 통계 지표 (Error / Accuracy Statistics)

본 문서는 수치모델 결과를 ERA5/GLORYS 등 재분석자료, 관측소·위성 자료와 비교·검증할 때 사용하는 **연속변수(continuous variable) 오차·정확도 통계 지표**를 망라한 카탈로그다. 기상·파랑·수온·해류·해수면 등 도메인 공통으로 쓰이는 점추정 오차 지표(RMSE, MAE, bias 등), 효율·일치도 계열(NSE, KGE, Willmott d), 상관·회귀 진단, 공간장(spatial field) 평가(anomaly correlation), 위성검증 표준(ubRMSE), 그리고 요약 시각화(Taylor / target diagram)와 유의성 검정(bootstrap)을 포함한다. 각 메서드 카드는 정의·수식, 적용 자료형, 해석 임계값 관행, 한계, 검증 가능한 출처를 담는다. 모든 지표는 **모델값과 참조값을 동일 시·공간으로 정렬(co-location)·보간한 짝지어진 표본(paired samples)** 을 전제로 한다.

> **NetCDF 격자 + CSV/텍스트 시계열 비교 실무 메모.** "우리 모델 vs ERA5/GLORYS"는 보통 동일 격자(또는 재격자화 후) 점별 매칭 → 공간장 지표(RMSE field, ACC, Taylor)로 평가하고, "우리 모델 vs 관측소/부이 CSV"는 최근접·이중선형 보간으로 모델을 관측점에 추출 → 시계열 지표(RMSE, bias, SI, KGE 등)로 평가한다. "우리 모델 vs 위성(고도계·SST 등)"은 시·공간 매칭 윈도우를 정의한 뒤 매칭쌍에 ubRMSE/bias/r를 적용한다. 면적 가중(area weighting, cosφ)·결측 마스크·단위 일치는 모든 계산의 전제다.

## 한 줄 목차
- **평균제곱근오차 (RMSE)** — 오차 크기의 대표 척도, 큰 오차에 민감
- **평균제곱오차 (MSE)** — RMSE의 제곱, bias²+variance로 분해 가능
- **평균절대오차 (MAE)** — 이상치에 강건한 평균 오차 크기
- **평균오차 / 편향 (ME / bias)** — 계통적 과대·과소 추정량
- **평균절대백분율오차 (MAPE)** — 상대(%) 오차 평균
- **대칭 평균절대백분율오차 (SMAPE)** — MAPE의 비대칭·발산 보정형
- **백분율 편향 (PBIAS)** — 총량 기준 % 편향 (수문 표준)
- **정규화 RMSE (nRMSE / NRMSE)** — 스케일 제거한 RMSE
- **RMSE-표준편차 비 (RSR)** — RMSE/σ_o, NSE와 직결되는 표준화 지표
- **평균절대 스케일오차 (MASE)** — naive 기준 대비 스케일프리 오차
- **산포지수 (Scatter Index, SI)** — 평균 대비 정규화 RMSE (파랑·해양 표준)
- **HH 지표 (symmetric normalized RMSE)** — bias 왜곡을 보정한 산포 척도
- **RMSE 분해 (systematic / unsystematic, MSEs/MSEu)** — 오차의 계통·비계통 성분 분리
- **중심화 RMS 차이 (Centered RMSD / CRMSD)** — 평균 제거 후 패턴 오차
- **불편 RMSE (ubRMSE)** — bias 제거 RMSE, 위성검증 표준(=CRMSD)
- **Pearson 상관계수 (r)** — 선형 동조성
- **Spearman 순위상관 (ρ)** — 단조 관계(비선형 허용)
- **결정계수 (R²)** — 설명된 분산 비율
- **이상편차 상관 (Anomaly Correlation, ACC)** — 기후값 제거 후 공간 패턴 상관 (공간장 표준)
- **회귀 기울기·절편 (slope / intercept)** — 조건부 편향·증폭/감쇠 진단
- **Nash–Sutcliffe 효율 (NSE)** — 평균 기준 대비 상대 성능
- **Kling–Gupta 효율 (KGE / KGE')** — 상관·변동성·편향 3성분 통합
- **Willmott 일치도 지수 (d, dr)** — 0~1 정규화 일치도 (refined 포함)
- **Murphy 기술점수 (MSSS)** — 기준 예측 대비 MSE 개선율
- **Taylor 다이어그램 & Taylor skill score** — 상관·표준편차·CRMSD 동시 요약
- **Target 다이어그램** — bias와 unbiased RMSD 기여도 요약
- **일치 비율·임계 정확도 (within-tolerance fraction)** — 허용오차 내 비율
- **유의성 검정 / 신뢰구간 (bootstrap, 유효표본)** — 지표 차이가 통계적으로 유의한지

---

### 평균제곱근오차 (Root Mean Square Error / RMSE)
- **무엇을 측정/검증하나:** 모델값과 참조값의 평균적 오차 크기(원자료와 동일 단위). 정확도(accuracy)의 가장 널리 쓰이는 단일 척도.
- **정의·수식:** RMSE = sqrt( (1/N) Σ (mᵢ − oᵢ)² ). (mᵢ: 모델, oᵢ: 관측/참조, N: 표본수)
- **적용 도메인/자료형:** 모든 도메인(기상·파랑·수온·해류·해수면). 격자(점별 매칭 후 전역 평균; 공간 평균은 면적 가중 cosφ 권장) 및 시계열 모두. 위성-모델 매칭에도 사용.
- **입력·전제:** 동일 단위·동일 위치·동일 시각으로 정렬된 짝지어진 표본. 결측 제거. 격자는 동일 해상도로 보간하거나 관측점에 최근접/이중선형 보간.
- **해석 기준:** 작을수록 좋음. 0이 완벽. 절대 기준은 변수·스케일 의존 → 보통 nRMSE/SI/RSR나 기준 모델과 비교해 판단. 변수 표준편차 대비 작아야(RSR<1) 의미가 있음.
- **한계·주의:** 큰 오차(이상치)에 제곱항으로 민감 → 소수 큰 편차가 값을 지배. 단독으로는 계통/비계통, 편향/산포를 구분 못함. RMSE는 음의 bias 모의에서 체계적으로 더 작게 나오는 경향이 있어 RMSE만으로 우열을 매기면 왜곡 가능(Mentaschi et al. 2013). 두 모델 RMSE 차이는 bootstrap로 유의성 확인 권장.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences* (표준 교과서); Jolliffe & Stephenson, *Forecast Verification* (표준 참고문헌).

---

### 평균제곱오차 (Mean Square Error / MSE)
- **무엇을 측정/검증하나:** 오차 제곱의 평균. RMSE의 제곱이며, NSE·MSSS·KGE 등 다수 지표의 기초.
- **정의·수식:** MSE = (1/N) Σ (mᵢ − oᵢ)². **분해:** MSE = bias² + s_err² (오차의 평균² + 오차의 분산), 또는 MSE = (σ_m − σ_o)² + 2σ_mσ_o(1 − r) + (m̄ − ō)² 형태로도 분해 가능(분산오차·상관 결손·평균오차).
- **적용 도메인/자료형:** 전 도메인, 격자·시계열. 주로 분해/스킬스코어의 중간량으로 사용.
- **입력·전제:** RMSE와 동일.
- **해석 기준:** 작을수록 좋음(단위가 제곱이라 직관성 낮음 → 보통 RMSE로 환산해 보고).
- **한계·주의:** 단위가 원변수의 제곱이라 해석이 비직관적. 이상치 민감성은 RMSE와 동일(또는 더 강함).
- **출처:** Murphy (1988), *Monthly Weather Review* 116, 2417–2424 (MSE 분해·스킬); Wilks, *Statistical Methods in the Atmospheric Sciences*.

---

### 평균절대오차 (Mean Absolute Error / MAE)
- **무엇을 측정/검증하나:** 오차 절대값의 평균. 오차의 전형적 크기를 이상치에 강건하게 표현.
- **정의·수식:** MAE = (1/N) Σ |mᵢ − oᵢ|.
- **적용 도메인/자료형:** 전 도메인, 격자·시계열. 위성·관측 매칭 공통.
- **입력·전제:** 짝지어진 표본, 동일 단위.
- **해석 기준:** 작을수록 좋음. 항상 MAE ≤ RMSE. RMSE/MAE 비가 1에 가까우면 오차가 균질, 1보다 크게 벌어지면 큰 이상오차 존재를 시사(상한은 sqrt(N)).
- **한계·주의:** 절대값이라 미분 불연속(최적화에 불리). 큰 오차를 RMSE만큼 강조하지 않으므로, 극값 성능이 중요한 경우 RMSE와 병행 보고 권장.
- **출처:** Willmott & Matsuura (2005), *Climate Research* 30, 79–82 (MAE vs RMSE 논의); Wilks, *Statistical Methods in the Atmospheric Sciences*.

---

### 평균오차 / 편향 (Mean Error / Bias / ME)
- **무엇을 측정/검증하나:** 모델의 계통적 과대(+)·과소(−) 추정. 부호가 있는 평균 차이.
- **정의·수식:** ME = bias = (1/N) Σ (mᵢ − oᵢ) = m̄ − ō.
- **적용 도메인/자료형:** 전 도메인, 격자·시계열. 격자에서는 공간 평균 편향, 시계열에서는 시간 평균 편향.
- **입력·전제:** 짝지어진 표본, 동일 단위. (격자 전역 편향은 면적 가중 평균 권장.)
- **해석 기준:** 0에 가까울수록 좋음. 부호로 과대/과소 방향 판단. RMSE와 함께 보고해 "정확도(RMSE) vs 계통편향(bias)"을 구분.
- **한계·주의:** 양·음 오차가 상쇄되어 0이라도 산포가 클 수 있음 → 반드시 RMSE/MAE와 병행. Taylor diagram은 평균을 제거하므로 bias를 보여주지 못함 → bias는 별도 보고하거나 target diagram 사용.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; WMO/JCOMM 검증 지침(표준 참고문헌).

---

### 평균절대백분율오차 (Mean Absolute Percentage Error / MAPE)
- **무엇을 측정/검증하나:** 관측값 대비 상대(%) 오차의 평균. 스케일이 다른 변수 간 비교에 유용.
- **정의·수식:** MAPE = (100/N) Σ |(mᵢ − oᵢ) / oᵢ|  [%].
- **적용 도메인/자료형:** 시계열 위주(양의 값이 명확한 변수: 풍속, 유의파고, 유속 크기 등). 0 근처·음수 값 변수에는 부적합.
- **입력·전제:** oᵢ ≠ 0, 가급적 oᵢ > 0. 동일 위치·시각 정렬.
- **해석 기준:** 작을수록 좋음. 관행적 대략 기준: <10% 매우 좋음, 10–20% 좋음, 20–50% 보통(변수·분야 의존, 절대 기준 아님).
- **한계·주의:** 관측값이 0에 가까우면 폭증/정의 불가. 과소예측(상한 100%)과 과대예측(상한 없음)에 비대칭. 해수면 편차·수온(°C)처럼 0이 임의 기준인 변수에는 부적절 → SMAPE 등 대안 고려.
- **출처:** Hyndman & Koehler (2006), *International Journal of Forecasting* 22, 679–688 (정확도 지표 비교, MAPE 한계).

---

### 대칭 평균절대백분율오차 (Symmetric Mean Absolute Percentage Error / SMAPE)
- **무엇을 측정/검증하나:** MAPE의 비대칭성과 0 근처 발산을 완화한 상대(%) 오차. 분모에 관측·모델의 평균을 써서 과대·과소예측을 대칭적으로 다룸.
- **정의·수식:** SMAPE = (100/N) Σ |mᵢ − oᵢ| / ( (|mᵢ| + |oᵢ|)/2 )  [%]. (분모를 |mᵢ|+|oᵢ|로 두면 상한이 200% 대신 100%가 되는 변형도 통용 → 정의 명시 필요.)
- **적용 도메인/자료형:** 시계열 위주, 양의 변수(풍속·파고·유속). 다변수 상대정확도 비교.
- **입력·전제:** |mᵢ|+|oᵢ| > 0. 동일 정렬 표본.
- **해석 기준:** 작을수록 좋음, 0%가 완벽. 변형(0–100% vs 0–200%)에 따라 절대 기준이 달라지므로 정의를 병기해 해석.
- **한계·주의:** mᵢ, oᵢ가 모두 0에 가까우면 여전히 불안정. 음수·0교차 변수(수온 °C, 해수면 편차)에는 부적절. "대칭"이라는 이름과 달리 과대/과소예측 페널티가 완전 대칭은 아니라는 비판도 있음 → 절대값 지표(MAE/RMSE)와 병행 권장.
- **출처:** Hyndman & Koehler (2006), *International Journal of Forecasting* 22, 679–688 (백분율 오차 지표 논의); M3-Competition 관행(표준 참고문헌).

---

### 백분율 편향 (Percent Bias / PBIAS)
- **무엇을 측정/검증하나:** 총량(또는 평균) 기준의 % 편향. 모델이 전체적으로 과대/과소하는 경향과 그 크기.
- **정의·수식:** PBIAS = 100 × [ Σ (mᵢ − oᵢ) / Σ oᵢ ]  [%]. (부호: 양수=과대, 음수=과소 — 수문 관행. 일부 정의는 부호 반대)
- **적용 도메인/자료형:** 시계열·유량·플럭스 등 적산이 의미 있는 변수. 해양·기상에서 누적/총량 편향 점검에 활용.
- **입력·전제:** Σ oᵢ ≠ 0, 가급적 양의 변수. 동일 기간·동일 위치.
- **해석 기준 (Moriasi et al. 2007, 유량 기준 관행):** |PBIAS| < 10% 매우 좋음, 10–15% 좋음, 15–25% 보통, > 25% 불만족(변수·분야에 따라 조정; 2015 갱신판은 변수별 표를 세분화).
- **한계·주의:** 양·음 오차 상쇄로 산포를 못 봄. 0 근처/음수 변수엔 부적합. 분야별 임계값을 그대로 이식하지 말 것.
- **출처:** Moriasi et al. (2007), *Transactions of the ASABE* 50(3), 885–900 (PBIAS 임계값 표); Moriasi et al. (2015), *Transactions of the ASABE* 58(6), 1763–1785 (갱신판); Gupta et al. (1999).

---

### 정규화 RMSE (Normalized RMSE / nRMSE / NRMSE)
- **무엇을 측정/검증하나:** RMSE를 스케일 상수로 나눠 무차원화 → 변수·지역 간 비교 가능.
- **정의·수식:** nRMSE = RMSE / D. 분모 D는 관행에 따라 (a) 관측 평균 ō, (b) 관측 표준편차 σ_o, (c) 관측 범위(max−min), (d) 사분위범위 IQR 등. **반드시 분모를 명시**해야 함.
- **적용 도메인/자료형:** 전 도메인, 격자·시계열. 다변수 대시보드/스코어카드에서 공통 척도화에 사용.
- **입력·전제:** 분모로 쓸 스케일량이 0이 아니고 안정적. 동일 정렬 표본.
- **해석 기준:** 작을수록 좋음. 평균 정규화 시 SI와 동일(아래 참조). 표준편차 정규화 시 RMSE/σ_o = RSR이고 sqrt(1−NSE)와 직접 연결(RSR·NSE 참조).
- **한계·주의:** 분모 선택에 따라 값이 크게 달라져 보고 간 비교가 어려움 → 정의를 항상 병기. 평균이 0 근처면 폭증.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; (분모 정의 다양 — 표준 참고문헌).

---

### RMSE-표준편차 비 (RMSE-observations Standard deviation Ratio / RSR)
- **무엇을 측정/검증하나:** RMSE를 관측 표준편차로 정규화한 표준화 오차. "오차가 관측 자연변동성에 비해 얼마나 큰가"를 한 값으로.
- **정의·수식:** RSR = RMSE / σ_o = sqrt( Σ(oᵢ−mᵢ)² ) / sqrt( Σ(oᵢ−ō)² ). 관계: RSR = sqrt(1 − NSE), 즉 RSR² = 1 − NSE.
- **적용 도메인/자료형:** 전 도메인, 시계열·격자 점매칭. 다변수 스코어카드에서 nRMSE(σ 정규화)와 동일물.
- **입력·전제:** σ_o > 0(관측이 충분한 변동성). 짝지어진 표본.
- **해석 기준 (Moriasi et al. 2007, 유량 관행):** RSR ≤ 0.50 매우 좋음, 0.50–0.60 좋음, 0.60–0.70 보통, > 0.70 불만족. 0이 완벽(작을수록 좋음).
- **한계·주의:** NSE와 일대일 대응이므로 NSE의 한계(첨두 편중, 분산 큰 자료에서 양호하게 나옴)를 그대로 상속. 관측 변동성이 작은 구간에서 과민.
- **출처:** Moriasi et al. (2007), *Transactions of the ASABE* 50(3), 885–900 (RSR 정의·임계값 표); Moriasi et al. (2015), *Transactions of the ASABE* 58(6), 1763–1785.

---

### 평균절대 스케일오차 (Mean Absolute Scaled Error / MASE)
- **무엇을 측정/검증하나:** 단순 기준(naive 예측: 보통 1스텝 지속성)의 오차로 정규화한 스케일프리 오차. 서로 다른 단위·스케일의 시계열을 한 척도로 비교.
- **정의·수식:** MASE = MAE_model / MAE_naive, 여기서 MAE_naive = (1/(N−1)) Σ_{i=2}^{N} |oᵢ − o_{i−1}| (계절성 있으면 |oᵢ − o_{i−m}|, m=계절주기). 분모는 in-sample naive 오차.
- **적용 도메인/자료형:** 시계열(풍속·수온·해수면·파고 등) 다지점/다변수 비교. 격자보다 시계열 평가에 적합.
- **입력·전제:** 시간순 정렬된 시계열(naive 차분 가능). 결측 처리 시 차분 정의 주의.
- **해석 기준:** MASE < 1 이면 naive(지속성)보다 나음, =1 동일, >1 못함. 작을수록 좋음, 스케일프리라 변수 간 직접 비교 가능.
- **한계·주의:** naive 기준 정의(1스텝 vs 계절)에 따라 값이 달라짐 → 명시. 강한 추세/계절 자료에서 naive가 매우 나빠 MASE가 낙관적으로 보일 수 있음. 공간장 평가에는 부적합.
- **출처:** Hyndman & Koehler (2006), *International Journal of Forecasting* 22, 679–688 (MASE 제안·권고).

---

### 산포지수 (Scatter Index / SI)
- **무엇을 측정/검증하나:** 관측 평균 대비 RMSE 비율(%). 파랑·해양 모델 검증의 사실상 표준 무차원 정확도 척도.
- **정의·수식:** SI = RMSE / ō  (또는 ×100 %). 일부 정의는 **편향 제거** RMSE 사용: SI = sqrt( Σ[(mᵢ−m̄) − (oᵢ−ō)]² ) / ō — 보고 시 정의 명시 필요.
- **적용 도메인/자료형:** 파랑(유의파고 Hs, 첨두주기 Tp), 풍속, 유속 등 양의 시계열·위성 매칭. WAVEWATCH III/SWAN 등 파랑모델 평가에 표준.
- **입력·전제:** ō > 0, 짝지어진 표본. 부이·위성 고도계 매칭 시 시·공간 윈도우 정의 필요.
- **해석 기준 (파랑 Hs 관행):** SI < 0.15(15%) 우수, 0.15–0.25 양호, > 0.30 개선 필요(지역·자료 의존, 절대 기준 아님).
- **한계·주의:** RMSE 기반이라 음의 bias에서 체계적으로 작아짐 → 음편향 모델이 부당하게 좋아 보일 수 있음. 따라서 HH 지표와 bias를 함께 보고 권장(Mentaschi et al. 2013).
- **출처:** Mentaschi et al. (2013), *Ocean Modelling* 72, 53–58 ("Problems in RMSE-based wave model validations"); 파랑 검증 관행(표준 참고문헌).

---

### HH 지표 (Symmetric Normalized RMSE / Hanna–Heinold Index)
- **무엇을 측정/검증하나:** bias에 의한 SI/nRMSE 왜곡을 보정한, 분자·분모 대칭형 정규화 RMSE. 산포와 편향을 함께 반영하되 null bias에서 최소화(음편향 모델을 부당하게 우대하지 않음).
- **정의·수식:** HH = sqrt( Σ (mᵢ − oᵢ)² / Σ (mᵢ · oᵢ) ). (Hanna & Heinold 1985; Mentaschi et al. 2013 재조명)
- **적용 도메인/자료형:** 파랑·풍속·해양 양의 변수 시계열·위성 매칭. 음/양 편향 모델을 공정하게 비교할 때.
- **입력·전제:** mᵢ, oᵢ > 0 (분모 Σ mᵢoᵢ > 0). 짝지어진 표본.
- **해석 기준:** 작을수록 좋음. SI와 유사 스케일로 해석하되 음편향 보상이 핵심 장점.
- **한계·주의:** 양의 변수에 한정. SI만큼 보편 보고되진 않아 단독보다는 SI·bias와 병기 권장.
- **출처:** Mentaschi et al. (2013), *Ocean Modelling* 72, 53–58; 원형은 Hanna & Heinold (1985), *Development and Application of a Simple Method for Evaluating Air Quality Models* (API Publication No. 4409) — 대기확산 모델 평가 지표.

---

### RMSE 분해 — 계통/비계통 오차 (Systematic / Unsystematic RMSE, MSEs / MSEu)
- **무엇을 측정/검증하나:** 총 오차를 회귀선으로 설명되는 **계통(systematic)** 성분(편향·증폭/감쇠 등 교정 가능)과 잔차인 **비계통(unsystematic)** 성분(무작위, 환원 불가)으로 분리.
- **정의·수식:** 관측에 대한 모델 회귀로 적합값 m̂ᵢ = a + b·oᵢ 를 구해
  RMSEs = sqrt( (1/N) Σ (m̂ᵢ − oᵢ)² ),  RMSEu = sqrt( (1/N) Σ (mᵢ − m̂ᵢ)² ),  RMSE² = RMSEs² + RMSEu².
- **적용 도메인/자료형:** 전 도메인, 시계열·격자 점매칭. 모델 교정 여지 진단에 유용.
- **입력·전제:** 모델 대 관측 선형회귀(보통 m on o). 충분한 표본수와 선형성 가정.
- **해석 기준:** RMSEu가 RMSE의 대부분이고 RMSEs가 작으면 "교정 가능한 계통오차가 적다"(좋은 모델). RMSEs가 크면 bias/스케일 보정 여지 큼.
- **한계·주의:** 회귀 방향(m on o vs o on m) 선택에 따라 분해가 달라짐 → 정의 명시. 비선형 관계엔 부정확.
- **출처:** Willmott (1981), *Physical Geography* 2, 184–194; Willmott (1982), *Bulletin of the American Meteorological Society* 63, 1309–1313.

---

### 중심화 RMS 차이 (Centered RMS Difference / CRMSD / cRMSE)
- **무엇을 측정/검증하나:** 각 장(field)에서 평균을 뺀 뒤의 RMS 차이 = **편향을 제거한 패턴 오차**. Taylor diagram의 거리축.
- **정의·수식:** CRMSD = sqrt( (1/N) Σ [ (mᵢ − m̄) − (oᵢ − ō) ]² ). 관계식: CRMSD² = σ_m² + σ_o² − 2σ_mσ_o·r. 또한 RMSE² = bias² + CRMSD².
- **적용 도메인/자료형:** 격자 공간장(공간 패턴 평가), 시계열(변동 패턴). Taylor diagram 작성의 핵심량.
- **입력·전제:** 짝지어진 표본, 표준편차·상관 계산 가능. 공간장은 동일 격자/마스크.
- **해석 기준:** 작을수록 패턴 일치 좋음. bias와 분리되므로 "평균은 맞지만 변동 패턴이 어긋남" 같은 진단 가능.
- **한계·주의:** 평균을 빼므로 **편향 정보 소실** → 반드시 bias와 병행. r과 σ에 의해 결정되는 종속량. (위성검증 분야의 ubRMSE와 수학적으로 동일.)
- **출처:** Taylor (2001), *Journal of Geophysical Research* 106(D7), 7183–7192.

---

### 불편 RMSE (Unbiased RMSE / ubRMSE)
- **무엇을 측정/검증하나:** 평균(bias)을 제거한 RMSE = 산포·시간변동 일치만 평가. 위성·재분석 검증에서 "절대값은 어긋나도 변동(dynamics)은 맞는가"를 보는 표준 지표(특히 토양수분, SST, 해수면 검증).
- **정의·수식:** ubRMSE = sqrt( (1/N) Σ [ (mᵢ − m̄) − (oᵢ − ō) ]² ) = sqrt( RMSE² − bias² ). (CRMSD와 동일물; 위성검증 문헌에서의 명칭.)
- **적용 도메인/자료형:** 위성-모델/관측 매칭(고도계 SLA, SST, 토양수분 등), 재분석 비교. 격자·시계열 모두. "우리 모델 vs 위성"에서 계통편차가 대표성 불일치로 큰 경우 특히 유용.
- **입력·전제:** 짝지어진 표본, bias 산출 가능. RMSE ≥ |bias| (수치적으로 항상 성립).
- **해석 기준:** 작을수록 좋음. bias와 함께 보고하면 RMSE를 "계통편차(bias) + 변동오차(ubRMSE)"로 완전 분해해 진단 가능.
- **한계·주의:** bias 정보를 버리므로 **반드시 bias와 병행**. 절대 정확도가 중요한 응용(예: 해수면 절대 수위)에는 단독 부적합.
- **출처:** Entekhabi, Reichle, Koster & Crow (2010), "Performance Metrics for Soil Moisture Retrievals and Application Requirements." *Journal of Hydrometeorology* 11(3), 832–840; (Taylor 2001의 CRMSD와 동일 정의).

---

### Pearson 상관계수 (Pearson Correlation Coefficient / r)
- **무엇을 측정/검증하나:** 모델-관측 간 **선형** 동조성(변동의 위상·동시성). 크기 오차나 bias는 보지 않음.
- **정의·수식:** r = Σ(mᵢ−m̄)(oᵢ−ō) / sqrt( Σ(mᵢ−m̄)² · Σ(oᵢ−ō)² ).
- **적용 도메인/자료형:** 전 도메인, 시계열(시간 상관)·격자(공간 패턴 상관). 공간 anomaly 상관은 아래 ACC 참조.
- **입력·전제:** 대략 선형 관계, 등분산, 이상치 적음. 짝지어진 표본.
- **해석 기준:** −1~1, 1이 완벽 양의 상관. 관행적 대략: |r|>0.9 매우 강, 0.7–0.9 강, 0.5–0.7 보통(분야 의존). 시계열은 자기상관으로 유효표본 감소 → 유의성 보수적 판단(유효표본 N_eff 사용).
- **한계·주의:** 비선형 관계·이상치에 취약. bias/증폭을 못 봄(완벽 상관이라도 스케일이 2배일 수 있음) → slope·bias와 병행. 평균/분산 정보 없음.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification*.

---

### Spearman 순위상관 (Spearman Rank Correlation / ρ)
- **무엇을 측정/검증하나:** 순위 기반 **단조(monotonic) 관계** 강도. 비선형이라도 일관된 증감이면 포착, 이상치에 강건.
- **정의·수식:** 값들을 순위로 변환 후 Pearson r 적용. (동순위 없을 때 ρ = 1 − 6Σdᵢ²/[N(N²−1)], dᵢ는 순위차)
- **적용 도메인/자료형:** 전 도메인 시계열·산점도. 분포가 치우치거나 비선형 반응(예: 파고-풍속) 평가에 유용.
- **입력·전제:** 순서형/연속형, 짝지어진 표본.
- **해석 기준:** −1~1, Pearson과 유사 해석. ρ ≫ r 이면 강한 비선형 단조성 시사.
- **한계·주의:** 크기·간격 정보 손실(순위만). 절대 정확도/bias 평가 불가 → 보조 지표.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; 표준 통계 교재(표준 참고문헌).

---

### 결정계수 (Coefficient of Determination / R²)
- **무엇을 측정/검증하나:** 관측 분산 중 모델(또는 회귀)로 설명되는 비율.
- **정의·수식:** 선형회귀 맥락에서 R² = r²(Pearson). 일반(예측 기반): R² = 1 − Σ(oᵢ−mᵢ)² / Σ(oᵢ−ō)² (이 형태는 NSE와 동일).
- **적용 도메인/자료형:** 전 도메인, 시계열·격자. 산점도·회귀 진단의 보조.
- **입력·전제:** 정의(상관² vs 1−SSE/SST)를 명시. 짝지어진 표본.
- **해석 기준:** 0~1(상관² 정의). 1이 완벽. 변수·분야 의존. (Moriasi 2015는 R²만으로 부족하다며 회귀 기울기·절편 동반 보고를 권고.)
- **한계·주의:** r² 정의는 **bias·기울기 오차에 둔감**(완전히 빗나가도 r²=1 가능) → 단독 사용 금지. "1−SSE/SST" 정의는 음수도 가능하며 사실상 NSE이므로 혼동 주의.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; Nash & Sutcliffe (1970, NSE 형태 R²); Moriasi et al. (2015).

---

### 이상편차 상관 (Anomaly Correlation Coefficient / ACC)
- **무엇을 측정/검증하나:** 기후값(climatology)을 제거한 **이상편차(anomaly)** 끼리의 공간(또는 시간) 상관 → 모델이 기후 평균을 넘어 "이상 패턴(저기압·온난수괴 등)"을 얼마나 재현하는지. 수치예보 공간장 검증의 표준 스코어.
- **정의·수식:** 각 격자에서 기후값 cᵢ를 빼 a^m_i = mᵢ−cᵢ, a^o_i = oᵢ−cᵢ. ACC = Σ wᵢ a^m_i a^o_i / sqrt( Σ wᵢ (a^m_i)² · Σ wᵢ (a^o_i)² ) (wᵢ=면적가중 cosφ). 중심형(평균 제거)·비중심형 변형 존재 → 정의 명시.
- **적용 도메인/자료형:** 격자 공간장(기상 500 hPa 지위, SST, SLA 등) vs ERA5/GLORYS 기후값 기준. 리드타임별 스킬 곡선 작성에 표준.
- **입력·전제:** 동일 격자의 기후값 필드(예: ERA5 30년 평균) 필수. 면적 가중, 동일 마스크.
- **해석 기준 (수치예보 관행):** ACC > 0.6 "유용한 예보(useful)"의 통상 경계, > 0.8 매우 좋음, ≈0 기후값 대비 무가치, <0 역위상(오해 유발). 변수·리드타임 의존.
- **한계·주의:** 기후값 정의(기간·해상도)에 민감 → 동일 기후값 사용 필수. 평균 이상편차 제거 여부(중심/비중심)로 값이 달라짐. 진폭 오차는 약하게만 반영(상관 계열 공통 한계) → RMSE/bias와 병행.
- **출처:** Jolliffe & Stephenson, *Forecast Verification*; WMO 검증 지침(표준 참고문헌); ECMWF Forecast User Guide, Sec. 6.2.2 (Anomaly Correlation Coefficient).

---

### 회귀 기울기·절편 (Regression Slope / Intercept)
- **무엇을 측정/검증하나:** 모델을 관측에 회귀(또는 그 역)했을 때의 기울기 b와 절편 a → 조건부 편향, 증폭(b>1)/감쇠(b<1), 가법 편향(a) 진단.
- **정의·수식:** 최소제곱: b = Σ(oᵢ−ō)(mᵢ−m̄)/Σ(oᵢ−ō)², a = m̄ − b·ō. 이상적으로 a≈0, b≈1. (직교/RMA 회귀는 양변 오차 가정 시 대안)
- **적용 도메인/자료형:** 전 도메인, 산점도 동반 시계열·매칭쌍.
- **입력·전제:** 회귀 방향 명시(보통 model on obs). 선형성·이상치 점검.
- **해석 기준:** b가 1, a가 0에 가까울수록 좋음. b<1 & 큰 값 과소·작은 값 과대 등 조건부 편향 해석. 95% 신뢰구간이 (a=0,b=1)을 포함하는지 검정.
- **한계·주의:** OLS는 독립변수 오차 무시 → 회귀희석(b 과소추정). 양변 측정오차 크면 직교회귀(Type II) 고려. 방향 바꾸면 결과 달라짐.
- **출처:** Wilks, *Statistical Methods in the Atmospheric Sciences*; Piñeiro et al. (2008), *Ecological Modelling* 216, 316–322 (관측 vs 예측 회귀 방향 논의).

---

### Nash–Sutcliffe 효율 (Nash–Sutcliffe Efficiency / NSE)
- **무엇을 측정/검증하나:** "관측 평균을 예측으로 쓰는 기준(benchmark)" 대비 모델의 상대적 설명력. 수문 표준 효율 지표.
- **정의·수식:** NSE = 1 − Σ(oᵢ−mᵢ)² / Σ(oᵢ−ō)² = 1 − MSE/σ_o². (= 1 − (RMSE/σ_o)² = 1 − RSR²)
- **적용 도메인/자료형:** 시계열(유량·수위·수온·해수면 등) 중심, 격자 점매칭에도. 해양·기상 시계열 평가에 널리 차용.
- **입력·전제:** 짝지어진 표본, 관측 분산 σ_o²>0. 결측 처리.
- **해석 기준 (Moriasi et al. 2007 관행):** NSE=1 완벽, >0 평균예측보다 나음(최소 수용), >0.5 만족, >0.65 좋음, >0.75 매우 좋음, ≤0 평균보다 못함. (2015 갱신판은 변수·시간해상도별 표를 세분화.)
- **한계·주의:** 제곱오차라 **첨두/큰 값에 가중**, 저변동(저유량) 구간 과소평가. 분모가 관측 분산이라 분산이 큰 자료에서 높게 나오기 쉬움. 계절성 큰 자료는 부풀려짐 → 기준예측(평균)의 적절성 재고. (Schaefli & Gupta 2007; Knoben et al. 2019)
- **출처:** Nash & Sutcliffe (1970), *Journal of Hydrology* 10(3), 282–290; Moriasi et al. (2007), *Transactions of the ASABE* 50(3), 885–900.

---

### Kling–Gupta 효율 (Kling–Gupta Efficiency / KGE, KGE')
- **무엇을 측정/검증하나:** 상관(r)·변동성비(α)·편향비(β)의 세 성분을 균형 있게 통합한 효율. NSE의 첨두 편중을 완화.
- **정의·수식:** KGE = 1 − sqrt[ (r−1)² + (α−1)² + (β−1)² ], 여기서 r=Pearson 상관, α = σ_m/σ_o(변동성비), β = m̄/ō(편향비). **2012 개정 KGE'**: α 대신 변동계수비 γ = (σ_m/m̄)/(σ_o/ō) 사용해 편향-변동 교차상관 제거(Kling et al. 2012). 가중형: 각 항에 s_r, s_α, s_β 스케일 적용 가능(Gupta et al. 2009).
- **적용 도메인/자료형:** 시계열(유량·수온·해수면·파고 등), 격자 점매칭. 해양·기상 시계열 종합 평가에 확산 중.
- **입력·전제:** σ_o>0, ō≠0(β 정의). 짝지어진 표본. 양의 변수에서 β 해석이 명확.
- **해석 기준:** KGE=1 완벽. KGE > −0.41 이면 "평균예측 기준(NSE=0 대응)"보다 나음(Knoben et al. 2019) — 0보다 작다고 무조건 나쁜 것 아님에 유의. 관행적으로 >0.75 좋음, 0.5–0.75 보통(분야 의존).
- **한계·주의:** β가 ō≈0 변수(해수면 편차·수온 anomaly)에서 불안정 → 변수 단위/기준점 주의. 세 성분(r, α, β)을 항상 분해 보고해 어떤 성분이 나쁜지 진단할 것. KGE와 NSE의 임계값을 동일시하지 말 것.
- **출처:** Gupta et al. (2009), *Journal of Hydrology* 377, 80–91; Kling et al. (2012), *Journal of Hydrology* 424–425, 264–277; Knoben et al. (2019), *HESS* 23, 4323–4331.

---

### Willmott 일치도 지수 (Willmott Index of Agreement / d, dr)
- **무엇을 측정/검증하나:** 모델-관측 일치 정도를 0~1(원형) 또는 −1~1(refined)로 정규화. NSE/상관의 대안적 일치도.
- **정의·수식:**
  - 원형 d (Willmott 1981): d = 1 − Σ(mᵢ−oᵢ)² / Σ( |mᵢ−ō| + |oᵢ−ō| )².
  - 수정형 d1 (Willmott 1985): 제곱 대신 절대값(차수 1) 사용 → 이상치 둔감.
  - **refined dr (Willmott et al. 2012):** Σ|mᵢ−oᵢ| 와 c·Σ|oᵢ−ō| (c=2) 비교로 −1~1 경계. dr = 1 − Σ|mᵢ−oᵢ| / (c·Σ|oᵢ−ō|) if Σ|mᵢ−oᵢ| ≤ c·Σ|oᵢ−ō|, else 반대 형태.
- **적용 도메인/자료형:** 전 도메인 시계열·격자 점매칭. 기상·수문·해양 모델 평가 공통.
- **입력·전제:** 짝지어진 표본, ō 계산 가능.
- **해석 기준:** d, dr 모두 1이 완벽. d는 항상 높게(0.6~0.9+) 나오는 경향이라 비교 해석에 주의. dr는 더 보수적이고 모델 정확도와 더 합리적으로 비례.
- **한계·주의:** 원형 d는 분모 구조상 값이 부풀려져 변별력이 약함(Willmott 본인 지적). refined dr 권장. dr는 과대/과소 방향(부호 편향)은 알려주지 않음.
- **출처:** Willmott (1981), *Physical Geography* 2, 184–194; Willmott et al. (2012), *International Journal of Climatology* 32, 2088–2094 (refined dr).

---

### Murphy 기술점수 (Murphy Skill Score / MSSS)
- **무엇을 측정/검증하나:** 기준(reference) 예측 대비 MSE가 얼마나 개선됐는지의 비율. 일반화된 기술점수(skill score) 틀.
- **정의·수식:** SS = 1 − MSE_forecast / MSE_reference. 기준이 관측 평균(climatology)이면 NSE와 동일. 기준이 지속성(persistence), 다른 모델, 재분석일 수도 있음. 완전형: SS = r² − [r − σ_m/σ_o]² − [(m̄−ō)/σ_o]² (상관·조건부편향·무조건편향 분해; Murphy 1988).
- **적용 도메인/자료형:** 전 도메인, 시계열·격자. "모델 대 재분석/관측 기후값/지속성" 상대평가에 핵심.
- **입력·전제:** 동일 표본에서 forecast와 reference 둘 다 계산. 기준 정의 명시 필수.
- **해석 기준:** SS=1 완벽, SS>0 기준보다 나음, SS=0 동일, SS<0 기준보다 못함. % 개선으로 보고.
- **한계·주의:** 기준 선택이 결과를 좌우 → 무엇을 기준으로 했는지 반드시 명시(climatology/persistence/타모델). MSE 기반이라 이상치 민감.
- **출처:** Murphy (1988), *Monthly Weather Review* 116, 2417–2424; Murphy & Epstein (1989), *Monthly Weather Review* 117, 572–581; Jolliffe & Stephenson, *Forecast Verification*.

---

### Taylor 다이어그램 & Taylor 기술점수 (Taylor Diagram & Taylor Skill Score)
- **무엇을 측정/검증하나:** 상관(r)·표준편차비·중심화 RMS차(CRMSD) 세 통계를 한 평면에 동시 요약 → 여러 모델/변수의 패턴 성능을 한눈에 비교.
- **정의·수식:** 코사인 법칙 관계 CRMSD² = σ_m² + σ_o² − 2σ_mσ_o·r 를 극좌표로 도시(방위각=arccos r, 반경=σ_m, 참조점=σ_o). **Taylor skill score:** S = 4(1+r) / [ (σ̂ + 1/σ̂)² (1+r₀) ], σ̂=σ_m/σ_o(정규화 표준편차비), r₀=달성 가능한 최대 상관(보통 1). σ̂→1, r→1이면 S→1; r→−1 또는 σ̂→∞이면 S→0; 완벽 분산·무상관이면 S→0.5.
- **적용 도메인/자료형:** 격자 공간장·시계열 다중 비교(기상·해양·기후 표준). 정규화(σ/σ_o)하면 다변수 동시 표시 가능.
- **입력·전제:** 각 모델의 σ_m, r, (CRMSD) 계산. 평균 제거(중심화) 전제.
- **해석 기준:** 참조점(관측)에 가까울수록 좋음(r→1, σ_m→σ_o, CRMSD→0). skill score 1이 완벽.
- **한계·주의:** **bias(평균오차) 정보 없음** → target diagram/별도 bias 보고로 보완. 패턴 위주 평가임을 명시.
- **출처:** Taylor (2001), *Journal of Geophysical Research* 106(D7), 7183–7192; Taylor (2005), *Taylor Diagram Primer* (PCMDI/LLNL 기술문서).

---

### Target 다이어그램 (Target Diagram)
- **무엇을 측정/검증하나:** 총 RMSD에 대한 **bias(MBE)** 와 **unbiased RMSD(uRMSD=CRMSD)** 의 기여를 한 평면에 도시 → Taylor가 못 보여주는 편향까지 포함한 요약.
- **정의·수식:** y축 = bias(부호 있음), x축 = sign(σ_m−σ_o)·uRMSD(부호 부여로 모델 과대/과소산포 구분), 원점으로부터 거리 = 총 RMSD. 보통 σ_o로 정규화. 관계: RMSD² = bias² + uRMSD².
- **적용 도메인/자료형:** 해양·생지화학·기상 다지점/다변수 스킬 요약(연안 모델 표준). 격자·시계열 모두.
- **입력·전제:** bias, uRMSD(=CRMSD), σ_m, σ_o 계산. 정규화 시 σ_o>0.
- **해석 기준:** 원점에 가까울수록 좋음. y>0 과대편향, y<0 과소편향. x>0 모델 변동성 과대, x<0 과소. 정규화 단위원(반경 1)은 "관측 평균만큼의 RMSD" 기준선으로 자주 사용(반경<1이면 평균예측보다 나음).
- **한계·주의:** uRMSD에 부여하는 부호 규약이 구현마다 다름 → 정의 명시. bias와 패턴을 분리하지만 상관 r 자체는 직접 표시 안 함(Taylor와 상호보완).
- **출처:** Jolliff et al. (2009), *Journal of Marine Systems* 76(1–2), 64–82 ("Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment").

---

### 일치 비율 / 임계 정확도 (Within-Tolerance Fraction / Hit Fraction)
- **무엇을 측정/검증하나:** 오차가 사전 정의한 허용오차 ε 이내인 표본 비율. 실무 합격 기준 점검(예: |모델−관측| ≤ 0.5 m).
- **정의·수식:** Frac = (1/N) Σ 𝟙( |mᵢ − oᵢ| ≤ ε ) × 100 [%]. (상대 허용오차 |mᵢ−oᵢ|/oᵢ ≤ τ 형태도 가능)
- **적용 도메인/자료형:** 전 도메인 시계열·매칭쌍. 운영 검증·품질기준(예: 파고 ±0.5 m, 수온 ±1 °C) 충족률 보고.
- **입력·전제:** 허용오차 ε(또는 τ) 사전 합의·명시. 짝지어진 표본.
- **해석 기준:** 높을수록 좋음(예: 90% 이상 합격). 임계값은 업무·사양 의존.
- **한계·주의:** ε에 임의성 → 반드시 근거와 함께 명시. 합격/불합격 이분화로 오차 크기 정보 손실 → RMSE 등과 병행. 분포 꼬리 정보 손실.
- **출처:** 운영 검증 관행(WMO/JCOMM 검증 지침 — 표준 참고문헌).

---

### 유의성 검정 / 신뢰구간 (Significance Testing & Confidence Intervals for Error Metrics)
- **무엇을 측정/검증하나:** 위 지표값(특히 두 모델 간 RMSE/bias/상관 차이)이 표본 변동을 넘어 **통계적으로 유의**한지. "모델 A가 B보다 RMSE 0.02 m 작다"가 우연인지 실제 개선인지 판정.
- **정의·수식:** 짝지은 차이 dᵢ = e^A_i − e^B_i (예: 제곱오차 차)의 평균에 대한 검정. **Bootstrap CI:** 표본(블록 단위)을 복원추출해 지표를 수천 번 재계산 → 2.5/97.5 백분위수로 95% CI. 차이의 95% CI가 0을 포함하지 않으면 유의. 자기상관 자료는 **블록 부트스트랩**(연속 블록 단위 재추출)으로 의존성 보존. 모수적 대안: 유효표본수 N_eff = N(1−ρ₁)/(1+ρ₁) (ρ₁=1차 자기상관)로 자유도 보정.
- **적용 도메인/자료형:** 전 도메인 시계열·격자(공간 상관 큰 자료). 모델 비교·랭킹의 신뢰성 보고에 필수.
- **입력·전제:** 시·공간 의존 구조 파악(블록 길이 선택). 짝지은 표본(동일 검증집합에서 두 모델 평가).
- **해석 기준:** 차이 CI가 0을 가로지르면 "유의한 차이 없음" → 단순 순위 매김 자제. p<0.05 또는 95% CI 비포함을 관행 기준.
- **한계·주의:** 기본(naive) 부트스트랩은 강한 의존 자료에서 CI를 과소추정 → 블록/페어드 기법 필수. 다중비교 시 보정(예: FDR). 표본이 작으면 BCa 보정 권장.
- **출처:** DelSole, T. & Tippett, M.K. (2020). "Bootstrap Methods for Statistical Inference. Part I: Comparative Forecast Verification for Continuous Variables." *Journal of Atmospheric and Oceanic Technology* 37(11), 1917–1932; Wilks, *Statistical Methods in the Atmospheric Sciences* (유효표본·재표본 검정).

---

## 출처 (References)

검증 가능한 실제 출처만 수록한다. DOI는 확인된 것만 표기하고, 정착된 교과서·표준지침은 그렇게 명시한다. (이번 개정에서 Hanna & Heinold 1985의 정확한 서지(API Pub. 4409), Mentaschi 2013, Taylor 2001 skill score 식, Moriasi 2015 갱신판, Entekhabi 2010 ubRMSE, DelSole & Tippett 2020, Hyndman & Koehler 2006 MASE를 웹으로 교차확인함.)

**표준 교과서 / 지침 (Standard texts & guidelines)**
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences*. Academic Press (여러 판). — RMSE/MAE/bias/상관/스킬스코어 등 일반 검증지표 표준 교과서.
- Jolliffe, I.T. & Stephenson, D.B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science*. Wiley (2nd ed., 2012). — 예보검증 표준 참고서(ACC 포함).
- WMO / JCOMM 검증 지침 (operational verification guidance). — 운영 검증 관행 (표준 참고문헌, 세부 임계값 확인요).
- ECMWF Forecast User Guide, Section 6.2.2 *Anomaly Correlation Coefficient*. — ACC 정의·해석(온라인 기술문서).

**오차·정확도·분해 (Error / decomposition)**
- Murphy, A.H. (1988). "Skill scores based on the mean square error and their relationships to the correlation coefficient." *Monthly Weather Review* 116, 2417–2424.
- Murphy, A.H. & Epstein, E.S. (1989). "Skill scores and correlation coefficients in model verification." *Monthly Weather Review* 117, 572–581.
- Willmott, C.J. (1981). "On the validation of models." *Physical Geography* 2, 184–194.
- Willmott, C.J. (1982). "Some comments on the evaluation of model performance." *Bulletin of the American Meteorological Society* 63, 1309–1313.
- Willmott, C.J. & Matsuura, K. (2005). "Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance." *Climate Research* 30, 79–82.
- Willmott, C.J., Robeson, S.M. & Matsuura, K. (2012). "A refined index of model performance." *International Journal of Climatology* 32, 2088–2094.
- Hyndman, R.J. & Koehler, A.B. (2006). "Another look at measures of forecast accuracy." *International Journal of Forecasting* 22, 679–688. (MAPE/SMAPE 한계, MASE 제안)
- Entekhabi, D., Reichle, R.H., Koster, R.D. & Crow, W.T. (2010). "Performance Metrics for Soil Moisture Retrievals and Application Requirements." *Journal of Hydrometeorology* 11(3), 832–840. (ubRMSE 표준화)

**효율 지표 (Efficiency metrics)**
- Nash, J.E. & Sutcliffe, J.V. (1970). "River flow forecasting through conceptual models part I — A discussion of principles." *Journal of Hydrology* 10(3), 282–290.
- Moriasi, D.N. et al. (2007). "Model evaluation guidelines for systematic quantification of accuracy in watershed simulations." *Transactions of the ASABE* 50(3), 885–900. (NSE/PBIAS/RSR 임계값 표)
- Moriasi, D.N., Gitau, M.W., Daggupati, P. & Pai, N. (2015). "Hydrologic and Water Quality Models: Performance Measures and Evaluation Criteria." *Transactions of the ASABE* 58(6), 1763–1785. (2007 갱신판, 변수별 기준 세분화)
- Gupta, H.V., Kling, H., Yilmaz, K.K. & Martinez, G.F. (2009). "Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling." *Journal of Hydrology* 377, 80–91.
- Kling, H., Fuchs, M. & Paulin, M. (2012). "Runoff conditions in the upper Danube basin under an ensemble of climate change scenarios." *Journal of Hydrology* 424–425, 264–277. (KGE' 개정형)
- Knoben, W.J.M., Freer, J.E. & Woods, R.A. (2019). "Technical note: Inherent benchmark or not? Comparing Nash–Sutcliffe and Kling–Gupta efficiency scores." *Hydrology and Earth System Sciences* 23, 4323–4331.

**요약 시각화 (Summary diagrams)**
- Taylor, K.E. (2001). "Summarizing multiple aspects of model performance in a single diagram." *Journal of Geophysical Research* 106(D7), 7183–7192.
- Taylor, K.E. (2005). *Taylor Diagram Primer*. PCMDI/LLNL 기술문서.
- Jolliff, J.K. et al. (2009). "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment." *Journal of Marine Systems* 76(1–2), 64–82. (target diagram)

**해양·파랑 도메인 (Ocean / wave domain)**
- Mentaschi, L., Besio, G., Cassola, F. & Mazzino, A. (2013). "Problems in RMSE-based wave model validations." *Ocean Modelling* 72, 53–58 (DOI: 10.1016/j.ocemod.2013.08.003). (SI/nRMSE 편향 왜곡, HH 지표 권고)
- Hanna, S.R. & Heinold, D.W. (1985). *Development and Application of a Simple Method for Evaluating Air Quality Models*. American Petroleum Institute (API) Publication No. 4409. (HH symmetric normalized RMSE 원형 — 대기확산 모델 평가)

**회귀 진단 (Regression diagnostics)**
- Piñeiro, G., Perelman, S., Guerschman, J.P. & Paruelo, J.M. (2008). "How to evaluate models: Observed vs. predicted or predicted vs. observed?" *Ecological Modelling* 216, 316–322.

**유의성 검정 (Significance testing)**
- DelSole, T. & Tippett, M.K. (2020). "Bootstrap Methods for Statistical Inference. Part I: Comparative Forecast Verification for Continuous Variables." *Journal of Atmospheric and Oceanic Technology* 37(11), 1917–1932.

**보조 (Context)**
- Schaefli, B. & Gupta, H.V. (2007). "Do Nash values have value?" *Hydrological Processes* 21, 2075–2080. (NSE 기준예측 한계 논의)
