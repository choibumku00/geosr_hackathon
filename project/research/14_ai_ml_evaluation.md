# 14. AI/ML 기반 평가·검증 (AI/ML Evaluation)

수치모델·통계모델을 대체·보강하는 AI/ML 산출물(emulator, super-resolution/downscaling, 편향보정, 데이터기반 예보, 이상탐지 등)을 권위 재분석자료(ERA5/GLORYS)·관측·위성과 비교·검증하기 위한 방법 카탈로그다. 기존 통계 검증지표(RMSE, ACC 등)를 그대로 쓰되, **AI 특유의 실패양상**(블러링·물리위반·과신뢰·분포외 발산·환각)을 잡아내는 추가 지표에 초점을 둔다. 결정론(deterministic) 점수, 확률·앙상블 점수, 영상품질 점수, 물리정합성 점수, 불확실성·보정 점수, 설명가능성 진단을 함께 사용하는 것이 원칙이며, **단일 지표로 AI 산출물을 판정하지 말 것**(특히 픽셀 MSE는 블러를 보상하므로 스펙트럼·구조 지표와 병용 필수).

> 이 문서는 본 Skill의 references/recipes 토대다. 각 방법은 "우리 수치모델 산출(NetCDF 격자 + CSV/텍스트 시계열) vs ERA5/GLORYS/관측소/위성" 비교 시나리오에서 실제로 호출할 수 있도록 메서드 카드 형식으로 정리했다. 모든 출처는 웹으로 1차 확인했으며(2026-06 기준), 확인 못 한 표준 지침은 '확인요'로 명시했다. **DOI/arXiv 식별번호를 임의로 생성하지 않았다.**

## 이 파일에 담은 방법 (목차)
- **결정론·일반 ML 회귀 검증**: RMSE/MAE/Bias, 정규화 오차(NRMSE/nMAE), 결정계수 R², 스킬스코어(MSESS), 이상상관계수 ACC, Kling-Gupta Efficiency(KGE), Taylor 다이어그램
- **유의성·모델간 비교**: Diebold-Mariano 검정, 부트스트랩 신뢰구간, 패러다임상 평가 함정
- **범주형·극값 검증**: 분할표 지표(POD/FAR/CSI/ETS/HSS), 극값 전용(SEDI/EDS), 분위수·극값 분포 비교
- **이중벌점·공간 검증**: Double penalty 진단, Fractions Skill Score(FSS)·이웃검증, 파워스펙트럼·RAPSD·유효해상도(effective resolution)
- **Super-resolution / Downscaling 영상품질**: PSNR, SSIM/MS-SSIM, LPIPS(perceptual), 스펙트럼 충실도(spectral fidelity), FID
- **분포 비교**: Wasserstein(EMD)·KS 거리, 분위수-분위수(Q-Q)·PDF 적합
- **편향보정 검증**: Quantile Mapping(QM)·QDM·DQM 평가, CDF/분위수 보존·변화신호 보존, ML post-processing(EMOS/DRN) 검증, analog 검증
- **확률·앙상블 검증**: CRPS·fair CRPS, Brier Score·BSS, Energy Score, Variogram Score, 순위 히스토그램(rank histogram), Spread-skill ratio, PIT/신뢰도도표
- **불확실성정량화(UQ)·보정(calibration)**: Calibration error(ECE)·신뢰성, Sharpness, 예측구간 PICP/MPIW, Conformal Prediction
- **물리제약(PINN)·물리정합성**: PDE 잔차(residual), 보존량(질량·에너지) 점검, 경계·초기조건 위반, 물리적 타당성
- **이상탐지(Anomaly detection) 검증**: Precision/Recall/F1, ROC-AUC·PR-AUC, point-adjust F1, affiliation/VUS, MTTD
- **분포외·안정성(emulator/surrogate)**: Out-of-distribution 일반화, 장기 롤아웃 드리프트·안정성, 기후통계 보존, 보존성 진단
- **설명가능성(XAI)·신뢰도 진단**: 순열 중요도(permutation importance), SHAP, Integrated Gradients/saliency, 충실도(faithfulness)·안정성 진단, 기후과학 XAI 평가 프로토콜
- **데이터기반 예보 종합검증**: WeatherBench2 표준세트, scores 라이브러리, 데이터누수·평가 함정(잘못된 baseline·climatology 누수)

---

## 결정론·일반 ML 회귀 검증

### 평균제곱근오차 / 평균절대오차 / 편향 (RMSE / MAE / Bias)
- **무엇을 측정/검증하나**: AI 예측값과 기준(관측·재분석)의 평균적 오차 크기와 계통편향. AI 검증의 가장 기본 1차 지표.
- **정의·수식**:
  - RMSE = √(mean[(ŷ−y)²]); MAE = mean[|ŷ−y|]; Bias(ME) = mean[ŷ−y]
- **적용 도메인/자료형**: 격자·시계열 공통(기온·SST·SSH·파고·풍속 등 연속변수). 격자장은 위도 가중(cos φ) RMSE를 표준으로 사용(WeatherBench2).
- **입력·전제**: 동일 격자·동일 시각으로 정렬·보간(regrid) 후 계산. 결측 동일 마스킹. 관측소(CSV) 대 격자는 최근접/이중선형 보간 후 짝지음.
- **해석 기준**: 작을수록 좋음. RMSE는 큰 오차에 민감(이상치·극값 강조), MAE는 강건. RMSE>MAE 격차가 크면 산발적 큰 오차 존재. **단독 사용 시 블러링을 "개선"으로 오판**할 수 있으니 스펙트럼 지표와 병용.
- **한계·주의**: MSE 계열은 평균으로 회귀(blur)하는 모델에 유리하게 작용 → AI 산출물의 과도한 평활을 보상함(double penalty 문제와 직결).
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (Academic Press, 표준 교과서); WeatherBench2 (Rasp et al. 2024, *JAMES*, doi:10.1029/2023MS004019).

### 정규화 오차 (Normalized RMSE / MAE, NRMSE / nMAE / Percent Bias)
- **무엇을 측정/검증하나**: 변수·지역 간 스케일이 다를 때 오차를 **무차원화**해 공정 비교(여러 변수·관측소를 한 표로).
- **정의·수식**: NRMSE = RMSE/σ_obs (또는 /range, /mean); PBIAS = 100·Σ(ŷ−y)/Σy [%].
- **적용 도메인/자료형**: 다변수·다지점 비교(기온·SST·SSH·파고 동시), 관측소 CSV 패널.
- **입력·전제**: 정규화 기준(표준편차/범위/평균) 명시·고정. 0 근처 변수는 /mean 회피.
- **해석 기준**: 작을수록 좋음. NRMSE<1이면 기후변동성보다 오차 작음. PBIAS의 부호로 과대/과소 진단.
- **한계·주의**: 정규화 기준 선택이 값에 직접 영향 → 보고 시 기준 명시 필수.
- **출처**: Wilks 교과서; 수문 모델 평가 관행(Moriasi et al. 2007, *Trans. ASABE*, PBIAS 등급 — 표준 참고문헌, 확인요).

### 결정계수 (R² / Coefficient of Determination)
- **무엇을 측정/검증하나**: AI 모델이 기준 분산을 설명하는 비율(설명력).
- **정의·수식**: R² = 1 − SS_res/SS_tot = 1 − Σ(y−ŷ)²/Σ(y−ȳ)²
- **적용 도메인/자료형**: 시계열·산점도 기반 검증(관측소 회귀, downscaling 1:1 비교).
- **입력·전제**: 짝지어진(paired) 예측-관측 샘플. 평균 ȳ는 검증 기간 기준.
- **해석 기준**: 1에 가까울수록 좋음, 0이면 평균예측 수준, 음수면 평균보다 나쁨. **R²만으로 편향을 못 잡음**(상관 높아도 계통편향 존재 가능).
- **한계·주의**: 분산이 큰 변수에서 과대평가되기 쉬움. Nash-Sutcliffe Efficiency(NSE, 수문)와 형식 동일.
- **출처**: Wilks (표준 교과서); Nash & Sutcliffe (1970, *J. Hydrol.* 10, 282–290, 수문 NSE).

### 평균제곱오차 스킬스코어 (MSE Skill Score, MSESS)
- **무엇을 측정/검증하나**: AI 모델이 **기준 예측(reference)** 대비 얼마나 향상됐는가(예: 기후값·지속성·기존 수치모델 대비).
- **정의·수식**: MSESS = 1 − MSE_model/MSE_ref. ref가 climatology면 ACC와 연결.
- **적용 도메인/자료형**: 격자·시계열 공통. **AI vs 기존모델/기후값 비교의 핵심.**
- **입력·전제**: 공정한 reference 선택이 결정적(아래 '평가 함정' 참조). climatology 누수 금지.
- **해석 기준**: >0이면 reference보다 우수, 1이면 완벽. 음수면 기준보다 못함.
- **한계·주의**: reference를 약하게 잡으면 점수 부풀려짐 → 강한 baseline(IFS/HRES, 기존 수치모델) 사용 권장.
- **출처**: Murphy (1988, *Monthly Weather Review* 116, 2417–2424, "Skill Scores Based on the Mean Square Error..."); Jolliffe & Stephenson, *Forecast Verification*.

### 이상상관계수 (Anomaly Correlation Coefficient, ACC)
- **무엇을 측정/검증하나**: 기후값을 제거한 **이상(anomaly) 패턴의 공간/시간 상관**. ML 일기예보 표준 스킬지표.
- **정의·수식**: ACC = Σ(ŷ′·y′)/√(Σŷ′²·Σy′²), 여기서 ′=값−기후값.
- **적용 도메인/자료형**: 격자장(500hPa 지위·기온 등), 위도 가중 적용.
- **입력·전제**: 정확한 기후평년값(climatology) 정의 필요. AI·기준 동일 기후값 사용.
- **해석 기준**: 1에 가까울수록 좋음. 관행상 ACC≈0.6이 "유용한 예보" 임계로 인용됨(중기예보).
- **한계·주의**: 진폭오차에 둔감(패턴만 봄). 기후값 정의에 민감.
- **출처**: Jolliffe & Stephenson, *Forecast Verification*; WeatherBench2 (Rasp et al. 2024); WMO/WWRP 검증 지침(표준 참고문헌, 확인요).

### Kling-Gupta Efficiency (KGE)
- **무엇을 측정/검증하나**: 오차를 **상관(r)·변동성비(α)·편향비(β)** 3성분으로 동시 진단하는 종합 효율(왜 틀렸는지까지 분해).
- **정의·수식**: KGE = 1 − √[(r−1)² + (α−1)² + (β−1)²], α=σ_sim/σ_obs, β=μ_sim/μ_obs. (r=Pearson 상관)
- **적용 도메인/자료형**: 시계열 검증(관측소 수온·해수면·유량·기온), 격자 1:1 비교에도 확장 가능.
- **입력·전제**: 짝지어진 예측-관측, 충분한 표본(σ·μ 추정 안정).
- **해석 기준**: 1=완벽, KGE>−0.41이면 평균예측(mean benchmark)보다 우수로 통용. α<1=변동성 과소(평활/블러 신호), β≠1=계통편향. **NSE/R²보다 진단력이 큼**(분산 과소를 잡아냄 → AI 평활 진단에 유용).
- **한계·주의**: KGE 값 자체보다 3성분 분해를 함께 보고해야 의미. 음수영역 해석은 벤치마크 의존.
- **출처**: Gupta, Kling, Yilmaz, Martinez (2009) "Decomposition of the mean squared error and NSE performance criteria." *Journal of Hydrology* 377, 80–91 (doi:10.1016/j.jhydrol.2009.08.003).

### Taylor 다이어그램 (Taylor Diagram)
- **무엇을 측정/검증하나**: 여러 모델/실험의 **상관·표준편차비·중심화 RMSD를 한 평면에 동시** 요약(여러 AI 후보 vs 기준을 한눈에 순위·진단).
- **정의·수식**: 코사인 법칙 σ_d² = σ_f² + σ_r² − 2σ_fσ_r·R 을 극좌표로 도시(반경=σ, 방위각=R, 등고선=centered RMSD).
- **적용 도메인/자료형**: 격자장·시계열(여러 변수·여러 모델 비교, 다운스케일 후보 선택).
- **입력·전제**: 짝지어진 모델-기준 패턴, 표준편차·상관 계산 가능. 보통 σ_r로 정규화.
- **해석 기준**: 기준점(REF: R=1, σ비=1)에 가까울수록 좋음. 반경이 기준보다 작으면 분산 과소(평활), 크면 과대.
- **한계·주의**: 편향(평균오차)은 표시 안 됨 → bias 별도 보고. 중심화 RMSD만 다룸.
- **출처**: Taylor, K.E. (2001) "Summarizing Multiple Aspects of Model Performance in a Single Diagram." *Journal of Geophysical Research* 106(D7), 7183–7192 (doi:10.1029/2000JD900719).

---

## 유의성·모델간 비교 (Significance / Inter-model comparison)

### Diebold-Mariano 검정 (Diebold-Mariano Test)
- **무엇을 측정/검증하나**: 두 예측(예: 우리 AI vs ERA5/기존 수치모델)의 **정확도 차이가 통계적으로 유의**한지(단순 점수 우열이 우연인지 판정).
- **정의·수식**: 손실차 d_t = g(e_t^A) − g(e_t^B)(g=손실, 예 제곱오차)의 평균이 0인지 검정. DM = d̄ / √(V̂(d̄)) ~ N(0,1), V̂는 자기상관(HAC) 보정 장기분산.
- **적용 도메인/자료형**: 시계열·격자(격자점별·도메인평균 손실 시계열). AI vs baseline 공정 비교의 핵심 통계 도구.
- **입력·전제**: 두 모델을 **동일 사례·동일 기준**에 대해 평가한 손실 시계열, 시간상관 보정(HAC). 작은 표본은 Harvey-Leybourne-Newbold(HLN) 수정.
- **해석 기준**: |DM|>1.96이면 5% 유의로 두 모델 정확도 다름. 부호로 우열.
- **한계·주의**: 예측이 시계열로 정렬되고 자기상관 보정해야 타당. 네스티드(한 모델이 다른 모델의 특수경우)면 표준 DM 부적절.
- **출처**: Diebold, F.X. & Mariano, R.S. (1995) "Comparing Predictive Accuracy." *Journal of Business & Economic Statistics* 13(3), 253–263; (구현) `scores` 패키지(Leeuwenburg et al. 2024, JOSS).

### 부트스트랩 신뢰구간·블록 부트스트랩 (Bootstrap CI / Block Bootstrap)
- **무엇을 측정/검증하나**: 점수(RMSE·CRPS·ACC 등)의 **불확실성(신뢰구간)**과 모델 간 차이의 유의성을 분포가정 없이 추정.
- **정의·수식**: 사례를 복원추출(시계열은 블록 단위) → 점수 분포 → 백분위 CI. 차이의 CI가 0을 포함하지 않으면 유의.
- **적용 도메인/자료형**: 모든 검증 점수의 불확실성 보고(격자·시계열).
- **입력·전제**: 충분한 독립 사례(또는 블록으로 시간상관 보존), 재표본 수(예 1000).
- **해석 기준**: CI 좁고 0을 배제하면 신뢰성 높은 차이. WeatherBench2도 스코어 차이에 부트스트랩 CI 권장.
- **한계·주의**: 강한 시공간 상관 시 블록 크기 선택 민감. 사례수 적으면 과신뢰.
- **출처**: Wilks 교과서(부트스트랩 검증); Efron & Tibshirani, *An Introduction to the Bootstrap* (표준 참고문헌, 확인요).

---

## 범주형·극값 검증 (Categorical / Extreme verification)

### 분할표 지표 (Contingency Table: POD / FAR / CSI / ETS / HSS)
- **무엇을 측정/검증하나**: 임계 초과 이진사건(강수>임계, 고파랑, 폭염 등)의 **적중·오탐·미탐** 균형. AI 강수·해상 사건 예보 검증의 표준.
- **정의·수식**: 2×2표(hits a, false alarms b, misses c, correct negatives d)에서 POD=a/(a+c), FAR=b/(a+b), CSI=a/(a+b+c), ETS=(a−a_rand)/(a+b+c−a_rand)(우연 보정), HSS=무작위 대비 정확도 개선.
- **적용 도메인/자료형**: 격자·시계열 이진사건(강수·구름·파고·해빙 임계 등), 위성/레이더 대비 AI.
- **입력·전제**: 임계값 정의, 예측·관측 동일 격자·이진화.
- **해석 기준**: POD·CSI·ETS·HSS는 클수록(1=완벽), FAR는 작을수록 좋음. ETS는 우연·기저율 보정해 드문 사건에 더 공정. HSS>0이면 무작위보다 우수.
- **한계·주의**: 임계·기저율 의존. 매우 드문 극값은 표본부족·기저율 편향(아래 SEDI 권장).
- **출처**: Wilks 교과서(분할표·ETS·HSS); Jolliffe & Stephenson, *Forecast Verification*; WMO/WWRP 검증 지침(확인요).

### 극값 전용 점수 (SEDI / EDS, Extremal Dependence Indices)
- **무엇을 측정/검증하나**: **희소 극값**(폭풍·극한강수·극한파고) 사건의 예보능력. 기저율이 0에 가까워질 때 ETS/CSI가 퇴화하는 문제를 보완.
- **정의·수식**: SEDI = [log F − log H − log(1−F) + log(1−H)] / [log F + log H + log(1−F) + log(1−H)], H=POD, F=POFD. (base-rate에 점근적으로 무관)
- **적용 도메인/자료형**: 격자·시계열 극값 이진사건(고임계 강수·풍속·파고·해수면).
- **입력·전제**: 극값 임계(높은 분위수), 충분한 사건수.
- **해석 기준**: 1=완벽, 0=무스킬. base-rate 의존이 낮아 드문 사건 모델 비교에 적합.
- **한계·주의**: 사건수 극소 시 추정 불안정(부트스트랩 CI 병행).
- **출처**: Ferro, C.A.T. & Stephenson, D.B. (2011) "Extremal Dependence Indices: Improved Verification Measures for Deterministic Forecasts of Rare Binary Events." *Weather and Forecasting* 26, 699–713.

---

## 이중벌점·공간 검증 (AI 블러링 진단의 핵심)

### 이중벌점 진단 (Double Penalty Diagnosis)
- **무엇을 측정/검증하나**: MSE 손실로 학습한 결정론 AI가 소규모 구조를 **평활(blur)**시켜 RMSE는 좋아 보이나 실제 패턴이 흐려지는 현상.
- **정의·수식**: 변위오차 d에 대해 파수 k 성분 벌점이 ~k²로 커짐 → 모델이 고파수를 죽여 ensemble-mean 같은 흐린 해를 학습. 직접 점수보다 **증상 진단**(스펙트럼·유효해상도·구조지표 동시검토)로 판정.
- **적용 도메인/자료형**: 격자장(강수·바람·SSH 등 소규모 구조 풍부한 변수).
- **입력·전제**: 고해상 기준장과 비교, 파워스펙트럼·FSS·SSIM 병행.
- **해석 기준**: RMSE 양호하지만 파워스펙트럼 고파수 결손·SSIM 저하·FSS 소규모 결손이면 블러링 확정.
- **한계·주의**: 픽셀지표만 보면 놓침. 생성형(diffusion)·스펙트럼 손실로 완화 가능.
- **출처**: Lam et al. (2023, GraphCast, *Science*, arXiv:2212.12794); Subich et al. (2025) "Fixing the Double Penalty in Data-Driven Weather Forecasting Through a Modified Spherical Harmonic Loss Function." arXiv:2501.19374; WeatherBench2.

### 이웃검증·강수예보 분수스킬점수 (Fractions Skill Score, FSS / Neighbourhood verification)
- **무엇을 측정/검증하나**: 임계값 초과 사건(강수 등)의 **이웃(neighbourhood) 규모별 공간 일치도**. 위치 약간 어긋나도 합리적으로 점수화 → 이중벌점 완화.
- **정의·수식**: FSS = 1 − MSE(P_f,P_o)/[mean(P_f²)+mean(P_o²)], P=이웃 내 사건 분율. 스케일 n을 키우며 평가.
- **적용 도메인/자료형**: 격자(강수·구름·파고 임계 사건), 위성/레이더 대비 AI 강수.
- **입력·전제**: 임계값(예: 1, 10mm/h)·이웃 크기 지정. 예측·관측 동일 격자.
- **해석 기준**: 0(무스킬)~1(완벽), 관행상 FSS_useful=0.5+f/2(f=기저율) 초과면 유용. FSS=0.5에 도달하는 최소 스케일이 모델의 공간 유효성(believable scale).
- **한계·주의**: 임계·스케일 선택 의존. 앙상블용 pFSS 확장 존재.
- **출처**: Roberts, N.M. & Lean, H.W. (2008) *Monthly Weather Review* 136, 78–97; Necker et al. (2024, *QJRMS*, 앙상블 FSS); Mittermaier, M. (2025, *MWR* 153(6), FSS 스킬 도출).

### 파워스펙트럼·반경평균 스펙트럼·유효해상도 (Power Spectrum / RAPSD / Effective Resolution)
- **무엇을 측정/검증하나**: AI 산출물이 **각 공간 스케일에서 올바른 에너지(변동성)**를 갖는가. 블러링·과평활을 정량화하는 핵심 진단.
- **정의·수식**: 2D FFT로 파워스펙트럼 → 반경평균(RAPSD, Radially Averaged Power Spectral Density). 모델/기준 스펙트럼 비를 파수별로 비교. 유효해상도 = 모델 스펙트럼이 기준 대비 일정 비율(예: 0.5) 이하로 떨어지는 파장.
- **적용 도메인/자료형**: 격자장(강수·바람·SST 등), super-resolution 산출물.
- **입력·전제**: 동일 격자·동일 도메인, 윈도잉(주기경계 아니면 tapering) 권장.
- **해석 기준**: 기준 스펙트럼과 일치하면 좋음. 고파수에서 power 결손=과평활(블러). 유효해상도 파장이 격자간격보다 훨씬 크면 미세구조 표현 실패.
- **한계·주의**: 위상(phase)은 못 봄(에너지만). 스펙트럼은 맞아도 위치가 틀릴 수 있어 SSIM/FSS 병용.
- **출처**: WeatherBench2 (Rasp et al. 2024); Subich et al. (2025, arXiv:2501.19374, 유효해상도 1250→160km 사례); spateGAN-ERA5 강수 RAPSD 평가(arXiv:2411.16098).

---

## Super-resolution / Downscaling 영상품질 검증

### 최대신호대잡음비 (Peak Signal-to-Noise Ratio, PSNR)
- **무엇을 측정/검증하나**: 초해상/다운스케일 복원장의 픽셀단위 충실도(잡음 대비 신호).
- **정의·수식**: PSNR = 10·log₁₀(MAX²/MSE) [dB], MAX=신호 최대값.
- **적용 도메인/자료형**: 격자 영상(기온·SST·강수 super-resolution), 위성영상 복원.
- **입력·전제**: 동일 정규화·동일 동적범위. **물리량은 MAX 정의가 모호**하므로 주의.
- **해석 기준**: 높을수록 좋음(보통 30dB↑ 양호). 단, 흐려도 PSNR 높을 수 있음.
- **한계·주의**: 인지품질·구조와 약한 상관. 기상/해양 물리량은 이론적 MAX가 없어 부적합할 때가 많음 → RMSE·SSIM 권장.
- **출처**: Wang et al. (2004, *IEEE TIP*, SSIM 논문 내 PSNR 비교); climate downscaling 평가 관행.

### 구조적 유사도 지수 / 다중스케일 SSIM (SSIM / MS-SSIM)
- **무엇을 측정/검증하나**: 휘도·대비·구조 3성분의 **구조적 유사도**. 블러·구조손실에 민감해 super-resolution 검증에 적합.
- **정의·수식**: SSIM(x,y)=[(2μ_xμ_y+C₁)(2σ_xy+C₂)]/[(μ_x²+μ_y²+C₁)(σ_x²+σ_y²+C₂)]. MS-SSIM은 여러 스케일에서 가중 평균.
- **적용 도메인/자료형**: 격자 영상(기온·강수·바람장 복원), 위성·다운스케일 산출물.
- **입력·전제**: 동일 정규화. 윈도(예 11×11) 기반 국소 계산.
- **해석 기준**: 1에 가까울수록 좋음. MS-SSIM은 소규모·대규모 구조 동시 보존 평가에 유용(기후 다운스케일 권장).
- **한계·주의**: 자연영상 통계 가정 → 물리장에 직접 적용 시 보정 필요(C1,C2·동적범위 설정). 위상 일치는 별도(FSS).
- **출처**: Wang, Z. et al. (2004) *IEEE Trans. Image Processing* 13(4), SSIM; Wang, Z. et al. (2003, MS-SSIM, Asilomar).

### 학습기반 인지유사도 (LPIPS, Learned Perceptual Image Patch Similarity / perceptual metric)
- **무엇을 측정/검증하나**: 사전학습 CNN 특징공간 거리로 측정한 **인지적(perceptual) 차이**. GAN/diffusion super-resolution의 "리얼함"을 평가.
- **정의·수식**: LPIPS = Σ_l w_l·||φ_l(x)−φ_l(y)||² (φ_l=l층 정규화 특징, w_l=학습 가중).
- **적용 도메인/자료형**: 격자/위성 영상 복원(특히 생성형 산출물).
- **입력·전제**: 보통 RGB 3채널·자연영상 사전학습망 → 물리채널은 의사색/표준화 매핑 필요.
- **해석 기준**: 낮을수록 인지유사. SRGAN 등 미세구조 잘 살리면 낮은 LPIPS.
- **한계·주의**: 물리적 정확성 보장 아님(그럴듯하나 틀린 디테일 가능). 도메인 외(기상) 일반화 한계 → 물리지표 병용 필수.
- **출처**: Zhang, R. et al. (2018, CVPR, "The Unreasonable Effectiveness of Deep Features as a Perceptual Metric"); 원격탐사 SR 다운스트림 벤치마크(arXiv:2605.00310, "Beyond Visual Fidelity...").

### 스펙트럼 충실도 (Spectral Fidelity)
- **무엇을 측정/검증하나**: 복원장의 **파워스펙트럼이 고해상 기준과 일치**하는지(고주파 디테일을 진짜 복원했는지, 가짜로 만들었는지).
- **정의·수식**: 모델/기준 RAPSD 비를 파수별 비교, 또는 스펙트럼 RMSE·log-spectral distance. (위 '파워스펙트럼' 카드의 SR 적용판)
- **적용 도메인/자료형**: super-resolution/downscaling 격자 산출물.
- **입력·전제**: 동일 격자·도메인, 윈도잉.
- **해석 기준**: 고주파 대역 스펙트럼이 기준과 정합하면 진짜 디테일 복원. 결손=과평활, 과잉=환각/노이즈 주입.
- **한계·주의**: 에너지만 봄(위상·위치 별도). 위성 분광(hyperspectral)에서는 채널 간 spectral angle(SAM)로 확장.
- **출처**: 강수 SR/다운스케일 평가관행(WeatherBench2; spateGAN-ERA5 arXiv:2411.16098); 분광영상 SAM은 원격탐사 표준(확인요).

### 프레셰 인셉션 거리 (Fréchet Inception Distance, FID)
- **무엇을 측정/검증하나**: 생성형(diffusion/GAN) 산출물 **집합의 분포**가 실제 분포와 얼마나 가까운지(품질+다양성).
- **정의·수식**: FID = ||μ_r−μ_g||² + Tr(Σ_r+Σ_g−2(Σ_rΣ_g)^½), μ/Σ는 Inception 특징의 평균·공분산.
- **적용 도메인/자료형**: 생성형 강수·바람장·위성영상 등 분포 단위 평가.
- **입력·전제**: 충분한 표본수, 특징추출망(자연영상 Inception → 지구과학은 도메인 특징/통계로 대체 권장).
- **해석 기준**: 낮을수록 실제분포에 근접. **상대비교용**(절대값 해석 신중).
- **한계·주의**: Inception이 자연영상 학습 → 물리장 직접적용 한계. 분포 일치≠개별 정확. 표본수에 편향.
- **출처**: Heusel, M. et al. (2017, NeurIPS, FID); 생성형 기상 평가 적용 사례 다수.

---

## 분포 비교 (Distribution comparison)

### Wasserstein 거리 / Earth Mover's Distance (Wasserstein / EMD)
- **무엇을 측정/검증하나**: AI 산출물의 **값 분포(PDF/히스토그램) 전체**가 기준과 얼마나 다른지(평균·분산을 넘어 분포 형태·극값 꼬리 비교).
- **정의·수식**: 1차원 W₁(P,Q)=∫|F_P(x)−F_Q(x)|dx (CDF 차의 적분). 다변량은 최적수송 비용.
- **적용 도메인/자료형**: 격자·시계열 값 분포(기후통계 보존, 생성형 산출물 분포 검증, SST/파고 분포).
- **입력·전제**: 충분한 표본, 동일 단위. 공간위치 무관(분포만 비교).
- **해석 기준**: 작을수록 분포 일치. 평활 모델은 꼬리(극값) 분포 축소 → W₁ 증가로 드러남.
- **한계·주의**: 위치·시간 짝지음 정보 없음(언제·어디서 틀렸는지 모름) → RMSE/공간지표 병용.
- **출처**: 최적수송(optimal transport) 표준(Villani, *Optimal Transport*, 확인요); 기후 emulator 분포 평가 관행.

### 콜모고로프-스미르노프 거리 / Q-Q 적합 (KS distance / Q-Q fit)
- **무엇을 측정/검증하나**: 두 분포(예측 vs 관측)의 **최대 CDF 차이**(KS)와 분위수별 일치(Q-Q plot)로 분포 형태·꼬리 적합 진단.
- **정의·수식**: KS = sup_x |F_pred(x) − F_obs(x)|. Q-Q는 예측분위수 vs 관측분위수 산점(대각선=완벽).
- **적용 도메인/자료형**: 시계열·격자 값 분포(편향보정 전후 분포 일치, 극값 꼬리).
- **입력·전제**: 충분한 표본. KS 검정은 독립표본 가정(시간상관 시 p값 과신뢰 주의).
- **해석 기준**: KS→0, Q-Q가 대각선 위면 분포 일치. Q-Q 꼬리 이탈=극값 표현 실패.
- **한계·주의**: KS는 분포 중앙에 민감(꼬리 둔감) → 극값은 Q-Q·Wasserstein 병용. 시간상관 시 검정 p값 신뢰 낮음.
- **출처**: Wilks 교과서(분포 비교·Q-Q); 편향보정 평가 표준 관행(아래 QM 카드).

---

## 편향보정 검증 (Bias correction / post-processing)

### 분위수 매핑 계열 평가 (Quantile Mapping / QDM / DQM Evaluation)
- **무엇을 측정/검증하나**: CDF/분위수 기반 편향보정(empirical QM, Quantile Delta Mapping, Detrended QM)이 **분포·극값·변화신호**를 올바로 보정·보존하는가.
- **정의·수식**: QM: x_corr=F_obs⁻¹(F_mod(x)). QDM: 분위수 추세 detrend→QM→추세 재부여(변화신호 보존). DQM: 평균추세 제거→eqm→재부여.
- **적용 도메인/자료형**: 시계열(관측소)·격자 둘 다. 기상/해양 변수(기온·강수·풍속·SST).
- **입력·전제**: 학습기간/검증기간 분리(교차검증). 동일 분포 가정의 적정성 점검.
- **해석 기준**: 검증기간 CDF·분위수·극값(예 99퍼센타일) 일치, 평균·표준편차 보존, **미래 변화신호(climate change signal) 보존**(QDM 우수, eqm은 신호 희석).
- **한계·주의**: 비정상성·외삽(관측범위 밖 극값) 취약. 분위수별 보존 성능 상이(eqm은 평균/퍼센타일 오차, QDM은 표준편차 오차 보고).
- **출처**: Cannon, A.J., Sobie, S.R., Murdock, T.Q. (2015) "Bias Correction of GCM Precipitation by Quantile Mapping (QDM)." *Journal of Climate* 28, 6938–6959 (doi:10.1175/JCLI-D-14-00754.1); UTCDW Guidebook(토론토대); xclim/downscaleR 문서.

### ML 사후보정 검증 (ML Post-processing: EMOS / DRN / Quantile Regression Evaluation)
- **무엇을 측정/검증하나**: 신경망 기반 사후보정(Distributional Regression Network, EMOS, NN quantile regression)이 **앙상블/결정론 예보의 편향·과소산포를 교정**했는지.
- **정의·수식**: 보정 전후의 CRPS·BSS·rank histogram·PIT 비교(아래 확률검증 지표 사용). 보정으로 CRPS 감소율이 핵심 KPI.
- **적용 도메인/자료형**: 시계열·격자(관측소 기온·풍속·강수 사후보정), 재분석·관측 대비.
- **입력·전제**: 독립 검증기간, 관측 ground truth, 일관된 변수단위.
- **해석 기준**: CRPS·CRPSS 개선(+), rank histogram 평탄화, PIT 균일화, sharpness 유지하며 calibration 개선.
- **한계·주의**: 과적합·관측 대표성 문제. 보정이 sharpness를 과도하게 줄이면(너무 퍼지면) 정보손실.
- **출처**: Rasp, S. & Lerch, S. (2018) *Monthly Weather Review* 146, 3885–3900 (NN post-processing); Gneiting et al. (2005, EMOS); Vannitsem, S. et al. (2021, *BAMS*, 통계 후처리 리뷰).

### 아날로그 기법 검증 (Analog Method Evaluation)
- **무엇을 측정/검증하나**: 과거 유사 상태(analog)를 검색해 다운스케일/보정하는 기법의 재현성·확률스킬.
- **정의·수식**: 유사도(거리)로 K개 analog 선택→통계 산출. 검증은 CRPS·Brier·상관·신뢰도로.
- **적용 도메인/자료형**: 격자→지점 다운스케일, 강수·기온.
- **입력·전제**: 충분히 긴 과거 풀(analog library), 적절한 predictor·거리척도.
- **해석 기준**: 확률·결정론 스킬이 climatology·QM 대비 향상이면 유효.
- **한계·주의**: 무관측 극값(전례 없는 사건) 재현 불가. 풀 길이 의존.
- **출처**: Zorita, E. & von Storch, H. (1999) *Journal of Climate* 12, 2474–2489 (analog method); 통계 다운스케일 리뷰.

---

## 확률·앙상블 검증 (Probabilistic / Ensemble verification)

### 연속순위확률점수 / 공정 CRPS (CRPS / fair CRPS)
- **무엇을 측정/검증하나**: 확률·앙상블 예측 분포 전체의 정확도(결정론 MAE의 확률 일반화). AI 확률예보 검증의 사실상 표준.
- **정의·수식**: CRPS(F,y)=∫(F(x)−1{x≥y})²dx. 앙상블판은 닫힌형 존재. **fair CRPS**는 유한 멤버수 편향을 보정(소규모 앙상블 과대평가 방지).
- **적용 도메인/자료형**: 격자·시계열, 앙상블/분포 예측(생성형 downscaling 포함).
- **입력·전제**: 예측 분포(또는 멤버)와 관측 짝. 위도가중(격자).
- **해석 기준**: 작을수록 좋음. CRPSS=1−CRPS/CRPS_ref로 스킬화. fair 버전을 멤버수 다른 모델 비교 시 사용.
- **한계·주의**: 일변량(grid point) 점수 → 공간 의존구조 못 봄(→ Energy/Variogram Score 병용). 멤버수 보정 주의.
- **출처**: Hersbach, H. (2000) *Weather and Forecasting* 15, 559–570 (CRPS 분해); Gneiting, T. & Raftery, A.E. (2007) *JASA* 102, 359–378 (proper scoring rules); WeatherBench2.

### 브라이어 점수 / 브라이어 스킬스코어 (Brier Score / BSS)
- **무엇을 측정/검증하나**: 이진사건(임계 초과: 강수>10mm, 폭풍 발생 등) 확률예측의 정확도.
- **정의·수식**: BS = mean[(p−o)²], o∈{0,1}. BSS=1−BS/BS_ref. 신뢰도·해상도·불확실성으로 분해 가능(Murphy 1973).
- **적용 도메인/자료형**: 격자·시계열 이진사건(임계·극값).
- **입력·전제**: 임계값 정의, 관측 이진라벨.
- **해석 기준**: BS 작을수록, BSS>0이면 reference 우수. 분해로 신뢰도(reliability)·해상도(resolution) 진단.
- **한계·주의**: 임계·기저율 의존. 드문 사건은 표본부족.
- **출처**: Brier, G.W. (1950) *Monthly Weather Review* 78, 1–3; Murphy (1973, 분해); Jolliffe & Stephenson, *Forecast Verification*.

### 에너지 점수 (Energy Score, ES)
- **무엇을 측정/검증하나**: **다변량/공간 앙상블** 예측의 정확도(CRPS의 다차원 일반화). 격자장 전체를 한 번에 평가.
- **정의·수식**: ES = E||X−y|| − ½E||X−X′|| (X,X′은 예측분포 독립표본, ||·||=유클리드).
- **적용 도메인/자료형**: 격자 다변량(여러 격자점·변수 동시), 생성형 앙상블 다운스케일.
- **입력·전제**: 다수 멤버, 동일 차원 벡터화.
- **해석 기준**: 작을수록 좋음. 공간 의존을 일부 반영.
- **한계·주의**: 공간 상관구조 변화에 둔감하다는 보고 → Variogram Score 보완.
- **출처**: Gneiting, T. et al. (2008, *TEST* 17, Energy Score); Gneiting & Raftery (2007, *JASA*).

### 베리오그램 점수 (Variogram Score, VS)
- **무엇을 측정/검증하나**: 예측장의 **공간 상관/구조(분산구조)**가 관측과 일치하는지. 블러·공간패턴 오류에 Energy Score보다 민감.
- **정의·수식**: VS_p = Σ_{i,j} w_{ij}(|y_i−y_j|^p − E|X_i−X_j|^p)² (보통 p=0.5).
- **적용 도메인/자료형**: 격자 앙상블·생성형 산출물(강수·바람 구조 검증).
- **입력·전제**: 멤버 다수, 가중 w_{ij}(거리 기반) 설정.
- **해석 기준**: 작을수록 공간구조 정합. 생성형이 구조 잘 살리면 낮음.
- **한계·주의**: 평균 편향엔 둔감(구조 전용). ES와 병행 권장.
- **출처**: Scheuerer, M. & Hamill, T.M. (2015) *Monthly Weather Review* 143, 1321–1334 (Variogram-based proper scoring rules).

### 순위 히스토그램 (Rank Histogram / Talagrand diagram)
- **무엇을 측정/검증하나**: 앙상블 **신뢰도(reliability)와 산포(spread) 적정성** — 관측이 앙상블 내 어느 순위에 떨어지는 빈도.
- **정의·수식**: 각 시점 관측의 앙상블 내 순위 집계 후 분포 시각화.
- **적용 도메인/자료형**: 격자·시계열 앙상블.
- **입력·전제**: 멤버 동질성(exchangeable), 충분한 사례수.
- **해석 기준**: **평탄=잘 보정**. U자형=과소산포(under-dispersion, AI 앙상블 흔한 문제), 종(∩)형=과대산포, 기울기=계통편향.
- **한계·주의**: 관측오차 미반영 시 왜곡. 시각 진단(점수 아님).
- **출처**: Hamill, T.M. (2001) *Monthly Weather Review* 129, 550–560 (rank histogram 해석); Talagrand et al. (1997).

### 산포-스킬 비율 / 스프레드-스킬 도표 (Spread-Skill Ratio / Spread-Skill plot)
- **무엇을 측정/검증하나**: 앙상블 평균산포(spread)가 실제 오차(RMSE)와 균형 잡혔는지(잘 보정된 앙상블은 spread≈RMSE).
- **정의·수식**: SSR = ensemble spread(표준편차) / RMSE(앙상블평균). 도표는 binned spread vs RMSE를 1:1선과 비교.
- **적용 도메인/자료형**: 격자·시계열 앙상블, 생성형 다운스케일 앙상블.
- **입력·전제**: 멤버 다수, 위도가중.
- **해석 기준**: SSR≈1 이상적. <1=과소산포(과신뢰), >1=과대산포. AI 앙상블은 흔히 <1.
- **한계·주의**: 시간/공간 평균방식에 민감. 관측오차 보정 필요.
- **출처**: Fortin, V. et al. (2014, *J. Hydrometeorology* 15, spread-skill); WeatherBench2.

### PIT 히스토그램 / 신뢰도 도표 (PIT histogram / Reliability diagram)
- **무엇을 측정/검증하나**: 확률적분변환(PIT)의 균일성으로 **연속 예측분포의 보정(calibration)** 평가 / 이진확률의 신뢰성(예측확률 vs 관측빈도).
- **정의·수식**: PIT=F(y); 잘 보정되면 PIT~Uniform(0,1). 신뢰도 도표는 예측확률 bin별 관측상대빈도 plot.
- **적용 도메인/자료형**: 시계열·격자 확률예측.
- **입력·전제**: 충분한 사례, 정확한 관측.
- **해석 기준**: PIT 평탄·신뢰도선이 대각선이면 잘 보정. 처짐=과신뢰/과소신뢰.
- **한계·주의**: 사례수 부족 시 잡음. 연속판 PIT은 rank histogram의 연속 대응.
- **출처**: Gneiting, T. et al. (2007) *J. R. Statist. Soc. B* 69, 243–268 ("Probabilistic forecasts, calibration and sharpness"); Wilks 교과서.

---

## 불확실성정량화(UQ)·보정 (Uncertainty Quantification / Calibration)

### 기대 보정오차 / 회귀 보정 (Expected Calibration Error / Calibration for regression)
- **무엇을 측정/검증하나**: AI가 내놓는 불확실성(예측구간·확률)이 **실제 빈도와 일치**하는지(over/under-confidence).
- **정의·수식**: 분류 ECE=Σ_b (|acc_b−conf_b|)·(n_b/N). 회귀는 예측분위수 c의 실제 포함율이 c와 일치하는지(calibration plot)로 측정.
- **적용 도메인/자료형**: 분류(이상/사건)·회귀(연속 물리량) AI.
- **입력·전제**: 검증세트, 예측 신뢰도/분위수.
- **해석 기준**: ECE→0, 회귀 calibration 곡선이 대각선이면 잘 보정.
- **한계·주의**: bin 수 민감. calibration만으로 부족(sharpness 함께 봐야 함).
- **출처**: Guo, C. et al. (2017, ICML, "On Calibration of Modern Neural Networks"); Kuleshov, V. et al. (2018, ICML, "Accurate Uncertainties for Deep Learning Using Calibrated Regression").

### 예리함 (Sharpness)
- **무엇을 측정/검증하나**: 예측분포의 **집중도(좁을수록 정보 많음)** — calibration을 만족하는 한 좁을수록 좋음.
- **정의·수식**: 평균 예측구간폭 또는 예측분산의 평균(관측 무관, 예측만으로 계산).
- **적용 도메인/자료형**: 회귀·확률 AI.
- **입력·전제**: 예측분포만 필요.
- **해석 기준**: calibration 전제 하에 작을수록 좋음. "calibration 우선, sharpness 차선"(Gneiting 원칙).
- **한계·주의**: 보정 없이 sharpness만 좋으면 과신뢰 위험. 단독 해석 금지.
- **출처**: Gneiting, T. et al. (2007, *JRSS-B*); Kuleshov & Deshpande (2022, ICML, calibrated & sharp).

### 예측구간 포함율·평균폭 (PICP / MPIW, Prediction Interval Coverage / Mean Width)
- **무엇을 측정/검증하나**: 명목 신뢰수준(예 90%)의 예측구간이 실제로 그 비율을 **포함**하는지(PICP)와 구간폭(MPIW)의 trade-off.
- **정의·수식**: PICP = (구간이 관측 포함한 비율). MPIW = 평균 구간폭. 결합지표 CWC 등.
- **적용 도메인/자료형**: 회귀 UQ(분위수회귀·앙상블·conformal).
- **입력·전제**: 명목수준 지정, 검증 관측.
- **해석 기준**: PICP≈명목수준이면서 MPIW 작을수록 좋음. PICP<명목=과신뢰.
- **한계·주의**: 평균 포함율 OK여도 조건부(상황별) 보정 실패 가능.
- **출처**: Khosravi, A. et al. (2011, *IEEE Trans. Neural Networks*, PI 평가).

### 등각예측 (Conformal Prediction)
- **무엇을 측정/검증하나**: 분포가정 없이 **유한표본에서 명목 커버리지를 보장**하는 예측구간/집합(AI UQ의 신뢰성 보강).
- **정의·수식**: 보정세트의 비순응점수(nonconformity score) 분위수로 구간 구성 → P(y∈Ĉ)≥1−α 보장(교환가능성 가정 하).
- **적용 도메인/자료형**: 회귀·분류 AI UQ(격자·시계열). 격자/시계열은 교환가능성 위반 보정판(conformal under distribution shift) 필요.
- **입력·전제**: 독립 보정세트, (시공간 상관 시) 적절한 변형. 명목수준 α.
- **해석 기준**: 실측 커버리지가 1−α에 일치하면 유효. 구간폭이 좁을수록(효율) 좋음.
- **한계·주의**: 표준 CP는 i.i.d./교환가능 가정 → 시계열·분포이동에 직접 적용 시 커버리지 붕괴 가능(전용판 사용).
- **출처**: Angelopoulos, A.N. & Bates, S. (2023) "Conformal Prediction: A Gentle Introduction." *Foundations and Trends in ML* 16(4).

---

## 물리제약(PINN)·물리정합성 (Physics consistency)

### PDE 잔차 / 물리손실 평가 (PDE Residual / Physics Loss Evaluation)
- **무엇을 측정/검증하나**: PINN·물리제약 모델의 출력이 **지배방정식(PDE)을 얼마나 만족**하는가(자동미분으로 잔차 평가).
- **정의·수식**: 잔차 r(x)=N[û](x)−f(x); 지표=콜로케이션점 mean(r²)(test residual). 경계·초기조건 잔차 별도.
- **적용 도메인/자료형**: 격자·연속장(유체·열·파동 등 물리지배 분야).
- **입력·전제**: 지배방정식·계수·정의역, 자동미분 가능한 모델.
- **해석 기준**: 잔차→0이면 물리 만족. 데이터 적합과 함께 봐야(consistency gap).
- **한계·주의**: 잔차 작아도 데이터-물리 불일치(consistency barrier)면 한계. 잔차≠해의 정확도.
- **출처**: Raissi, M., Perdikaris, P., Karniadakis, G.E. (2019) *Journal of Computational Physics* 378, 686–707 (PINN 원전); Becerra-Zuniga et al. (2026) "On the Role of Consistency Between Physics and Data in PINNs." arXiv:2602.10611.

### 보존량 점검 (Conservation Diagnostics: 질량·에너지·운동량)
- **무엇을 측정/검증하나**: AI 산출장이 **물리 보존법칙**(질량·에너지·운동량·수분)을 시·공간적으로 보존하는가.
- **정의·수식**: 전역적분 변화량 |∫q dV(t)−∫q dV(0)|, 또는 발산·플럭스 잔차. 표준화하여 상대오차로.
- **적용 도메인/자료형**: 격자(대기·해양 emulator·예보), 장기 롤아웃.
- **입력·전제**: 보존변수·적분영역·경계플럭스 정의.
- **해석 기준**: 상대 보존오차가 작고 시간에 따라 누적 발산 없으면 좋음. 누적 드리프트=불안정 신호.
- **한계·주의**: 데이터기반 모델은 보존을 명시적으로 안 지킴 → 진단·제약 필요. 경계처리 민감.
- **출처**: Beucler, T. et al. (2021) *Physical Review Letters* 126, 098302 (conservation-constrained ML); ACE2-SOM 보존 진단 사례(arXiv:2412.04418).

### 물리적 타당성·경계/초기조건 위반 (Physical Plausibility / BC-IC Violation)
- **무엇을 측정/검증하나**: 음의 강수·과포화·비물리적 극값·경계 불연속 등 **물리적으로 불가능한 출력**의 발생 여부.
- **정의·수식**: 제약위반율(예 음수 강수 비율), 경계조건 잔차, 안정도(CFL 유사) 점검.
- **적용 도메인/자료형**: 격자 AI 산출(강수·습도·해수면 등 부호·범위 제약 변수).
- **입력·전제**: 물리적 허용범위·경계조건 명세.
- **해석 기준**: 위반율 0에 가까울수록 좋음. 빈번한 위반=후처리/제약 필요.
- **한계·주의**: 통계지표(RMSE)는 양호해도 물리위반 잠복 가능 → 별도 점검 필수.
- **출처**: Kashinath, K. et al. (2021) *Phil. Trans. R. Soc. A* 379 (physics-informed ML 리뷰); WGNE/도메인 검증 관행(확인요).

---

## 이상탐지 검증 (Anomaly detection)

### 정밀도·재현율·F1 (Precision / Recall / F1)
- **무엇을 측정/검증하나**: 이상(센서이상·극값·결측패턴 등) 탐지의 적중·누락·오탐 균형.
- **정의·수식**: Precision=TP/(TP+FP), Recall=TP/(TP+FN), F1=2PR/(P+R).
- **적용 도메인/자료형**: 시계열·격자 이상탐지(관측 QC, 모델산출 이상).
- **입력·전제**: 라벨(정상/이상), 임계값 결정.
- **해석 기준**: 1에 가까울수록 좋음. 클래스 불균형(이상 희소)에서 F1·PR 중시.
- **한계·주의**: 임계 의존, 라벨 품질 의존.
- **출처**: Wilks(분할표); 시계열 이상탐지 서베이(arXiv:2211.05244).

### ROC-AUC / PR-AUC
- **무엇을 측정/검증하나**: 임계 비의존 탐지능력. ROC-AUC(TPR-FPR), PR-AUC(정밀-재현; 희소사건에 더 적합).
- **정의·수식**: 임계 변화에 따른 곡선하 면적.
- **적용 도메인/자료형**: 시계열·격자 이상점수.
- **입력·전제**: 연속 이상점수(score)와 라벨.
- **해석 기준**: 1=완벽, 0.5=무작위. 희소 이상에는 **PR-AUC 우선**(ROC는 낙관적).
- **한계·주의**: 시계열 순서·시간상관 무시 → 시계열 전용지표 병용.
- **출처**: Davis, J. & Goadrich, M. (2006, ICML, PR vs ROC); 이상탐지 서베이.

### 점조정 F1 / 사건기반·근접기반 지표 (Point-Adjust F1 / Affiliation / VUS)
- **무엇을 측정/검증하나**: 이상이 **구간(segment)**으로 나타나는 시계열 특성을 반영한 평가(한 점만 맞춰도 구간 인정 등)와 그 함정 보완.
- **정의·수식**: Point-Adjust: 구간 내 1점 탐지 시 구간 전체 정탐 처리. Affiliation: 예측-실제 사건 간 시간거리 기반 정밀/재현. VUS-ROC/PR: 라벨경계 완충(buffer) 적용 면적.
- **적용 도메인/자료형**: 시계열 이상탐지(센서·관측 QC).
- **입력·전제**: 구간 라벨, (VUS는) 버퍼크기.
- **해석 기준**: 높을수록 좋음. **단, Point-Adjust는 점수 과대평가 경향** → Affiliation/VUS로 교차확인.
- **한계·주의**: PA-F1은 랜덤점수도 부풀려질 수 있어 비판 많음. 단독 사용 지양.
- **출처**: Xu et al. (2018, PA 도입); Huet, A. et al. (2022, KDD, Affiliation); Paparrizos, J. et al. (2022, VLDB, VUS); Kim, S. et al. (2022, AAAI, point-adjust 비판).

### 평균 탐지지연 (Mean Time To Detect, MTTD)
- **무엇을 측정/검증하나**: 이상 시작부터 탐지까지 **지연시간**(운영 조기경보 품질).
- **정의·수식**: MTTD = mean(탐지시각 − 실제시작시각).
- **적용 도메인/자료형**: 실시간 시계열 모니터링.
- **입력·전제**: 사건 시작시각 라벨.
- **해석 기준**: 짧을수록 좋음. 정밀/재현과 trade-off 함께 제시.
- **한계·주의**: 미탐 사건 처리방식 명시 필요.
- **출처**: 이상탐지 평가 관행(서베이/운영 모니터링 문헌, 확인요).

---

## 분포외·안정성 (Emulator / Surrogate 검증)

### 분포외 일반화 (Out-of-Distribution Generalization)
- **무엇을 측정/검증하나**: emulator가 **학습 분포 밖**(다른 CO₂ 강제력·미관측 극값·다른 계절/지역)에서도 정확한가.
- **정의·수식**: in-sample vs out-of-sample 지표(RMSE/CRPS) 비교, 분포외 시나리오 별 성능저하율.
- **적용 도메인/자료형**: 격자 기후/기상 emulator, 시나리오 예측.
- **입력·전제**: 의도적으로 분리한 OOD 검증세트(시간·강제력·지역 holdout).
- **해석 기준**: OOD 성능저하가 작을수록 좋음. 급격한 발산=외삽 실패.
- **한계·주의**: 학습기간 내 교차검증만으론 OOD 안전성 보장 못함.
- **출처**: 기후 emulator OOD 연구(Causal Climate Emulation with Bayesian Filtering, arXiv:2506.09891; LUCIE-3D, arXiv:2509.02061); WeatherBench2 평가철학.

### 장기 롤아웃 안정성·드리프트 (Long-Rollout Stability / Drift)
- **무엇을 측정/검증하나**: 자기회귀(autoregressive) emulator를 장기간 반복적분할 때 **오차누적·발산·기후 드리프트** 여부.
- **정의·수식**: 적분길이별 RMSE 성장곡선, 전역 평균/분산의 시간추세(드리프트), 발산(blow-up) 발생 시점.
- **적용 도메인/자료형**: 격자 기상/기후 자기회귀 emulator(SFNO·diffusion 등).
- **입력·전제**: 장기 롤아웃 실행, 기준 기후통계.
- **해석 기준**: 안정(통계 정상상태 유지)·드리프트 미미하면 좋음. 멱급수적 오차폭증·통계 표류=불안정.
- **한계·주의**: 단기 스코어 좋아도 장기 불안정 흔함. 롤아웃 중 OOD 진입이 원인.
- **출처**: Pedersen et al. (2025) "Thermalizer: Stable autoregressive neural emulation of spatiotemporal chaos." arXiv:2503.18731; Spherical DYffusion(arXiv:2406.14798); LUCIE-3D(arXiv:2509.02061).

### 기후통계 보존 (Climate Statistics Preservation)
- **무엇을 측정/검증하나**: emulator 장기적분이 **장기 평균·분산·극값분포·스펙트럼·변동성(ENSO 등)**을 재현하는가(개별 시점 정확도와 별개).
- **정의·수식**: 장기 PDF/분위수 비교(Wasserstein/KS), 파워스펙트럼·자기상관, 변동성 지수(예 Niño3.4) 통계 비교.
- **적용 도메인/자료형**: 격자 기후 emulator.
- **입력·전제**: 충분히 긴 적분·기준 기후통계.
- **해석 기준**: 통계분포·스펙트럼·변동성이 기준과 일치하면 좋음.
- **한계·주의**: 시점별 RMSE 좋아도 기후통계 왜곡 가능(평활로 분산 과소).
- **출처**: ACE2-SOM(arXiv:2412.04418); Spherical DYffusion(Rühling Cachay et al., arXiv:2406.14798); 기후 emulator 평가 관행.

---

## 설명가능성(XAI)·신뢰도 진단

### 순열 변수중요도 (Permutation Feature Importance)
- **무엇을 측정/검증하나**: 입력변수를 무작위 섞었을 때 **성능저하량**으로 각 변수의 기여도 측정(모델 비의존).
- **정의·수식**: Imp_j = err(섞은 j) − err(원본). 반복평균.
- **적용 도메인/자료형**: 모든 ML(표·격자·시계열). predictor 중요도 진단.
- **입력·전제**: 검증세트, 성능지표 정의.
- **해석 기준**: 클수록 중요. 음수≈무관/노이즈.
- **한계·주의**: **상관변수에서 왜곡**(중요도 분산·이중계산). 인과 아님.
- **출처**: Breiman, L. (2001) *Machine Learning* 45, 5–32 (Random Forests, permutation importance); Molnar, C. *Interpretable Machine Learning*.

### SHAP (SHapley Additive exPlanations)
- **무엇을 측정/검증하나**: 게임이론 Shapley 값으로 각 입력의 **예측 기여(개별·전역)**를 공정 배분.
- **정의·수식**: φ_i = Σ 가중[f(S∪{i})−f(S)] (모든 부분집합 S에 대한 한계기여 평균).
- **적용 도메인/자료형**: 표·격자·시계열 ML(기후 emulator 변수기여 분석 사례 다수).
- **입력·전제**: 배경분포(baseline), (근사용) 충분한 표본.
- **해석 기준**: 부호=증감 방향, 크기=기여. 일관성·국소정확성 보장.
- **한계·주의**: 상관변수 가정·배경분포 선택에 민감, 계산비용 큼. 상관·인과 혼동 주의.
- **출처**: Lundberg, S.M. & Lee, S.-I. (2017, NeurIPS, SHAP); 기후 모델 적용 사례 다수.

### Integrated Gradients / Saliency (속성귀인, Attribution)
- **무엇을 측정/검증하나**: 신경망 출력에 대한 **입력 픽셀/변수의 기여(gradient 기반)**. CNN 기상모델 진단에 사용.
- **정의·수식**: IG_i = (x_i−x_i')·∫₀¹ ∂f(x'+α(x−x'))/∂x_i dα (baseline x').
- **적용 도메인/자료형**: 신경망(격자 CNN·트랜스포머), 위성·기상장.
- **입력·전제**: baseline 선택, 미분가능 모델.
- **해석 기준**: 완전성(기여 합=출력차) 등 공리 만족. 큰 |IG|=영향 큼.
- **한계·주의**: baseline 의존, 잡음. saliency는 불안정할 수 있음 → SmoothGrad 등 보완.
- **출처**: Sundararajan, M., Taly, A., Yan, Q. (2017, ICML, Integrated Gradients); Simonyan et al. (2014, saliency).

### 설명 충실도·안정성 진단 / 기후 XAI 평가 프로토콜 (Explanation Faithfulness / Stability)
- **무엇을 측정/검증하나**: XAI 설명이 모델을 **진짜 반영(faithful)**하고 입력 소교란에 **안정(robust)**한지(설명 자체의 검증). 여러 XAI 방법 중 도메인에 맞는 것을 선택·순위화.
- **정의·수식**: 충실도=중요특징 제거 시 성능하락(deletion/insertion AUC). 안정성(robustness)=입력 소교란 대비 설명변화(Lipschitz). 그 외 randomization·complexity·localization 등 다축 스킬스코어.
- **적용 도메인/자료형**: 모든 XAI 산출(특히 기후·기상 CNN/MLP).
- **입력·전제**: 다수 설명 샘플, 교란 프로토콜, ground-truth 부재 시 대리 평가축.
- **해석 기준**: 제거 시 빠른 성능하락=충실, 교란에 설명 안정=신뢰. 방법 간 스킬스코어로 순위.
- **한계·주의**: XAI 결과를 무비판 신뢰 금지(설명도 검증 대상). 방법 간 불일치 흔하고 아키텍처 의존.
- **출처**: Alvarez-Melis, D. & Jaakkola, T. (2018, robustness of interpretability, arXiv:1806.08049); Bommer et al. (2024) "Finding the Right XAI Method — A Guide for the Evaluation and Ranking of Explainable AI Methods in Climate Science." *Artificial Intelligence for the Earth Systems* 3(3) (arXiv:2303.00652).

---

## 데이터기반 예보 종합검증·평가 함정

### WeatherBench2 표준 평가세트 (Standardized Benchmark Evaluation)
- **무엇을 측정/검증하나**: 데이터기반 글로벌 일기예보를 ERA5/IFS 대비 **표준·재현가능**하게 비교(공정 baseline·공통 지표·공통 데이터).
- **정의·수식**: 위도가중 RMSE·ACC·bias + 강수 등 추가지표 + 확률(CRPS, spread-skill, rank histogram) 묶음.
- **적용 도메인/자료형**: 글로벌 격자 1~14일 예보. (해양·지역모델엔 동일 철학 적용 가능)
- **입력·전제**: 공통 격자·기간·평가코드, 동일 ground truth.
- **해석 기준**: 강한 baseline(IFS HRES/ENS) 대비 일관된 향상이면 신뢰.
- **한계·주의**: 단일 점수로 순위 매기지 말 것(블러 보상). 스펙트럼·물리지표 병행 필요.
- **출처**: Rasp, S. et al. (2024) *JAMES* (WeatherBench2, doi:10.1029/2023MS004019); github.com/google-research/weatherbench2.

### 검증 구현 라이브러리 (Verification Tooling: scores / xskillscore)
- **무엇을 측정/검증하나**: 위 지표들을 NetCDF/xarray 격자·CSV 시계열에 **재현가능·표준구현**으로 계산(직접 코딩 오류 방지).
- **정의·수식**: (도구) RMSE/MAE/MSESS, CRPS(ensemble·CDF), Brier, FSS, PIT, threshold-weighted CRPS, Diebold-Mariano 검정 등 내장.
- **적용 도메인/자료형**: 격자(xarray/NetCDF/Zarr/GRIB)·시계열(pandas). 본 Skill 파이프라인의 계산 백엔드로 적합.
- **입력·전제**: xarray 정렬된 예측·기준(동일 좌표), 위도가중 옵션.
- **해석 기준**: 표준구현 사용으로 지표 정의 일관성 확보(팀·기관 간 비교 가능).
- **한계·주의**: 도구 기본옵션(가중·결측 처리)을 명시·고정해야 재현성 보장.
- **출처**: Leeuwenburg et al. (2024) "scores: A Python package for verifying and evaluating models and predictions with xarray." *JOSS* (doi:10.21105/joss.06889); xskillscore(오픈소스, 확인요).

### 평가 함정·데이터 누수 점검 (Evaluation Pitfalls / Data Leakage)
- **무엇을 측정/검증하나**: AI 평가의 **타당성 자체**(약한 baseline, climatology 누수, 학습-검증 시간겹침, 관측-평가 동일출처, 마스킹 불일치)를 점검.
- **정의·수식**: 정성 체크리스트 + 누수 민감도(누수 제거 전후 점수차).
- **적용 도메인/자료형**: 모든 AI 검증 파이프라인.
- **입력·전제**: 데이터 출처·시간분할 추적.
- **해석 기준**: 시간 holdout 엄격·강 baseline·동일 마스킹·climatology 분리면 신뢰. 점수가 비현실적으로 높으면 누수 의심.
- **한계·주의**: 가장 흔한 과대평가 원인이 데이터 누수·약한 baseline. 검증 설계가 점수보다 중요.
- **출처**: Kapoor, S. & Narayanan, A. (2023) "Leakage and the Reproducibility Crisis in ML-based Science." *Patterns* 4(9); WeatherBench2 평가 가이드.

---

## 출처 (References)

> 아래 출처는 2026-06 기준 웹으로 1차 확인했다. arXiv 식별번호 중 일부(2602.x, 2605.x, 2509.x, 2506.x 등)는 2025–2026 프리프린트로, 정식 게재 시 DOI가 바뀔 수 있다. 핵심 표준 지표(CRPS, FSS, SSIM, Brier, ACC, KGE 등)는 정식 저널 원전을 우선 인용하라. **DOI를 임의 생성하지 않았으며**, 확인 못 한 표준 지침류는 '확인요'로 표기했다.

### 표준 교과서·지침
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences* (Academic Press, 4th ed. 2019) — RMSE/MAE/Bias, R², 분할표(ETS/HSS), 분포비교 등.
- Jolliffe, I.T. & Stephenson, D.B. (eds.) *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley, 2nd ed. 2012) — ACC, BSS, 확률검증 종합.
- Molnar, C. *Interpretable Machine Learning* (온라인서적) — permutation importance, SHAP 등 XAI.
- WMO/WWRP 예보 검증 지침 및 JCOMM 해양 검증 지침(표준 참고문헌, 확인요).

### 결정론·스킬스코어·종합지표
- Murphy, A.H. (1988) "Skill Scores Based on the Mean Square Error and Their Relationships to the Correlation Coefficient." *Monthly Weather Review* 116(12), 2417–2424 (doi:10.1175/1520-0493(1988)116<2417:SSBOTM>2.0.CO;2).
- Nash, J.E. & Sutcliffe, J.V. (1970) "River flow forecasting through conceptual models." *Journal of Hydrology* 10, 282–290. (NSE)
- Gupta, H.V., Kling, H., Yilmaz, K.K., Martinez, G.F. (2009) "Decomposition of the mean squared error and NSE performance criteria." *Journal of Hydrology* 377(1-2), 80–91 (doi:10.1016/j.jhydrol.2009.08.003). (KGE)
- Taylor, K.E. (2001) "Summarizing Multiple Aspects of Model Performance in a Single Diagram." *Journal of Geophysical Research* 106(D7), 7183–7192 (doi:10.1029/2000JD900719). (Taylor diagram)

### 유의성·모델간 비교
- Diebold, F.X. & Mariano, R.S. (1995) "Comparing Predictive Accuracy." *Journal of Business & Economic Statistics* 13(3), 253–263.
- Wilks 교과서(부트스트랩 검증); Efron, B. & Tibshirani, R. *An Introduction to the Bootstrap* (Chapman & Hall, 1993 — 표준 참고문헌, 확인요).

### 범주형·극값 검증
- Ferro, C.A.T. & Stephenson, D.B. (2011) "Extremal Dependence Indices: Improved Verification Measures for Deterministic Forecasts of Rare Binary Events." *Weather and Forecasting* 26, 699–713. (SEDI/EDS)
- (분할표 POD/FAR/CSI/ETS/HSS) Wilks 교과서; Jolliffe & Stephenson, *Forecast Verification*.

### 공간·이중벌점·스펙트럼
- Roberts, N.M. & Lean, H.W. (2008) "Scale-Selective Verification of Rainfall Accumulations... (FSS)." *Monthly Weather Review* 136, 78–97.
- Necker, T. et al. (2024) "The fractions skill score for ensemble forecast verification." *QJRMS*. (pFSS)
- Mittermaier, M. (2025) "How to Derive Skill from the Fractions Skill Score." *Monthly Weather Review* 153(6).
- Subich, C., Husain, S.Z., Separovic, L., Yang, J. (2025) "Fixing the Double Penalty in Data-Driven Weather Forecasting Through a Modified Spherical Harmonic Loss Function." arXiv:2501.19374. — 블러링·유효해상도 1250→160km.
- Lam, R. et al. (2023) "GraphCast: Learning skillful medium-range global weather forecasting." *Science* (arXiv:2212.12794).

### 영상품질(super-resolution)·분포
- Wang, Z., Bovik, A.C., Sheikh, H.R., Simoncelli, E.P. (2004) "Image Quality Assessment: From Error Visibility to Structural Similarity (SSIM)." *IEEE Trans. Image Processing* 13(4).
- Wang, Z. et al. (2003) "Multiscale Structural Similarity (MS-SSIM)." Asilomar.
- Zhang, R. et al. (2018) "The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS)." *CVPR*.
- Heusel, M. et al. (2017) "GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)." *NeurIPS*.
- "Beyond Visual Fidelity: Benchmarking Super-Resolution Models for Large-Scale Remote Sensing Imagery via Downstream Task Integration." arXiv:2605.00310 (원격탐사 SR 벤치마크).
- Wasserstein/EMD: Villani, C. *Optimal Transport: Old and New* (Springer, 2009 — 표준 참고문헌, 확인요); KS·Q-Q는 Wilks 교과서.

### 편향보정·후처리
- Cannon, A.J., Sobie, S.R., Murdock, T.Q. (2015) "Bias Correction of GCM Precipitation by Quantile Mapping (QDM)." *Journal of Climate* 28, 6938–6959 (doi:10.1175/JCLI-D-14-00754.1).
- Zorita, E. & von Storch, H. (1999) "The Analog Method..." *Journal of Climate* 12, 2474–2489.
- Rasp, S. & Lerch, S. (2018) "Neural Networks for Postprocessing Ensemble Weather Forecasts." *Monthly Weather Review* 146, 3885–3900.
- Gneiting, T. et al. (2005) "Calibrated Probabilistic Forecasting Using Ensemble Model Output Statistics (EMOS)." *MWR* 133.
- Vannitsem, S. et al. (2021) "Statistical Postprocessing for Weather Forecasts: Review..." *BAMS*.
- UTCDW Guidebook (University of Toronto); xclim/downscaleR(climate4R) 문서.

### 확률·앙상블 검증
- Hersbach, H. (2000) "Decomposition of the Continuous Ranked Probability Score (CRPS)." *Weather and Forecasting* 15, 559–570.
- Gneiting, T. & Raftery, A.E. (2007) "Strictly Proper Scoring Rules, Prediction, and Estimation." *JASA* 102, 359–378.
- Gneiting, T. et al. (2007) "Probabilistic Forecasts, Calibration and Sharpness." *J. R. Statist. Soc. B* 69, 243–268.
- Gneiting, T. et al. (2008) "Assessing probabilistic forecasts of multivariate quantities... (Energy Score)." *TEST* 17.
- Scheuerer, M. & Hamill, T.M. (2015) "Variogram-Based Proper Scoring Rules for Probabilistic Forecasts of Multivariate Quantities." *Monthly Weather Review* 143, 1321–1334.
- Brier, G.W. (1950) "Verification of Forecasts Expressed in Terms of Probability." *Monthly Weather Review* 78, 1–3.
- Hamill, T.M. (2001) "Interpretation of Rank Histograms for Verifying Ensemble Forecasts." *Monthly Weather Review* 129, 550–560.
- Fortin, V. et al. (2014) "Why Should Ensemble Spread Match the RMSE...?" *Journal of Hydrometeorology* 15.
- Ferro, C.A.T., Richardson, D.S., Weigel, A.P. (2008) "On the effect of ensemble size on the discrete and continuous ranked probability scores." *Meteorological Applications* 15, 19–24 (doi:10.1002/met.45). (멤버수 보정 → fair scores 토대; "fair scores" 명명은 Ferro 2014, *QJRMS*.)

### 불확실성정량화·보정
- Guo, C. et al. (2017) "On Calibration of Modern Neural Networks." *ICML*.
- Kuleshov, V. et al. (2018) "Accurate Uncertainties for Deep Learning Using Calibrated Regression." *ICML*.
- Kuleshov, V. & Deshpande, S. (2022) "Calibrated and Sharp Uncertainties in Deep Learning via Density Estimation." *ICML* (PMLR 162).
- Khosravi, A. et al. (2011) "Comprehensive Review of Neural Network-Based Prediction Intervals..." *IEEE Trans. Neural Networks*.
- Angelopoulos, A.N. & Bates, S. (2023) "Conformal Prediction: A Gentle Introduction." *Foundations and Trends in ML* 16(4).

### 물리제약(PINN)·물리정합성
- Raissi, M., Perdikaris, P., Karniadakis, G.E. (2019) "Physics-informed neural networks." *Journal of Computational Physics* 378, 686–707.
- Beucler, T. et al. (2021) "Enforcing Analytic Constraints in Neural Networks Emulating Physical Systems." *Physical Review Letters* 126, 098302.
- Kashinath, K. et al. (2021) "Physics-informed machine learning: case studies for weather and climate modelling." *Phil. Trans. R. Soc. A* 379.
- Becerra-Zuniga et al. (2026) "On the Role of Consistency Between Physics and Data in Physics-Informed Neural Networks." arXiv:2602.10611.

### 이상탐지
- Davis, J. & Goadrich, M. (2006) "The Relationship Between Precision-Recall and ROC Curves." *ICML*.
- Huet, A. et al. (2022) "Local Evaluation of Time Series Anomaly Detection Algorithms (Affiliation)." *KDD*.
- Paparrizos, J. et al. (2022) "Volume Under the Surface (VUS)..." *VLDB*.
- Kim, S. et al. (2022) "Towards a Rigorous Evaluation of Time-series Anomaly Detection (point-adjust 비판)." *AAAI*.
- "Deep Learning for Time Series Anomaly Detection: A Survey." arXiv:2211.05244.

### 설명가능성(XAI)
- Breiman, L. (2001) "Random Forests." *Machine Learning* 45, 5–32. (permutation importance)
- Lundberg, S.M. & Lee, S.-I. (2017) "A Unified Approach to Interpreting Model Predictions (SHAP)." *NeurIPS*.
- Sundararajan, M., Taly, A., Yan, Q. (2017) "Axiomatic Attribution for Deep Networks (Integrated Gradients)." *ICML*.
- Alvarez-Melis, D. & Jaakkola, T. (2018) "On the Robustness of Interpretability Methods." arXiv:1806.08049.
- Bommer, P. et al. (2024) "Finding the Right XAI Method — A Guide for the Evaluation and Ranking of Explainable AI Methods in Climate Science." *Artificial Intelligence for the Earth Systems* 3(3) (arXiv:2303.00652).

### 데이터기반 예보·emulator·평가 함정·도구
- Rasp, S. et al. (2024) "WeatherBench 2: A Benchmark for the Next Generation of Data-Driven Global Weather Models." *JAMES* (doi:10.1029/2023MS004019); github.com/google-research/weatherbench2.
- Bi, K. et al. (2023) "Accurate medium-range global weather forecasting with 3D neural networks (Pangu-Weather)." *Nature*.
- Kapoor, S. & Narayanan, A. (2023) "Leakage and the Reproducibility Crisis in Machine-Learning-Based Science." *Patterns* 4(9).
- Leeuwenburg, T. et al. (2024) "scores: A Python package for verifying and evaluating models and predictions with xarray." *Journal of Open Source Software* (doi:10.21105/joss.06889).
- 기후 emulator 안정성·OOD: Pedersen et al. "Thermalizer" (arXiv:2503.18731); Rühling Cachay et al. "Probabilistic Emulation of a Global Climate Model with Spherical DYffusion" (arXiv:2406.14798); "LUCIE-3D" (arXiv:2509.02061); "ACE2-SOM" (arXiv:2412.04418); "Causal Climate Emulation with Bayesian Filtering" (arXiv:2506.09891).

> 주의: 본 카탈로그는 검증 가능한 1차 출처 위주로 작성했다. 표준 교과서/지침(Wilks, Jolliffe & Stephenson, WMO/WWRP/JCOMM) 중 직접 확인하지 못한 항목은 '확인요'로 표기했고, 핵심 지표는 정식 저널 원전을 우선 인용했다.
