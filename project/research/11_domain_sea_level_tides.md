# 도메인: 해수면·조위 검증 방법 카탈로그 (Sea level / Tides Verification Methods)

이 문서는 수치모델이 산출한 해수면(sea level)·조위(tide) 결과를 검조소(tide gauge), 위성고도계(satellite altimetry), 재분석/기준 조석모델(reference tide model), 해양재분석(예 GLORYS) 및 대기재분석(예 ERA5 평균해면기압 → 역기압효과)과 자동 비교·검증하기 위한 분석/검증 방법을 망라한 레퍼런스다. 조석은 결정론적(astronomically deterministic) 신호이므로 일반 통계검증과 달리 **분조(constituent)별 진폭·지각 오차**, **벡터/복소 차이(vector/complex difference)**, **조위편차(residual)·폭풍해일(storm surge)**, **극치해면 재현빈도(return period)** 같은 도메인 고유 지표를 함께 다룬다. 입력은 NetCDF 격자자료(모델 해면고도·조화상수·재분석 SSH/SLA)와 CSV/텍스트 시계열(검조소 수위)을 가정한다. 일반적인 RMSE·상관·편향 등 공통 통계지표는 별도 공통 문서를 참조하고, 여기서는 해수면·조위 특화 항목에 집중한다.

> **자료별 핵심 주의(정렬·기준):** 비교 전에 반드시 ① 수직기준(datum) 통일 — 검조소 상대해면 vs 위성/모델 절대해면(지오이드 기준), ② 평균(mean)·계절·교점주기 제거 기준 일치, ③ 시간기준(UTC) 정렬, ④ 보정 일치 — 조석보정(tide correction)·역기압/대기보정(DAC)·VLM 보정이 양쪽에 동일하게 적용됐는지 확인한다. 이 전제를 어기면 모든 지표가 오염된다.

## 이 파일에 담은 방법(목차)

- 조화분석(harmonic analysis)으로 조화상수 추정 — T_TIDE / UTide
- 조석 admittance / 응답법 (tidal admittance, response method)
- 분조별 진폭 오차 (amplitude error, ΔH)
- 분조별 지각 오차 (phase/epoch error, ΔG)
- 복소/벡터 차이 (vector difference, complex amplitude difference D)
- 분조별 RMS (RMS per constituent, ½D 환산)
- 다분조 종합 RMS / RSS (total RMS, root-sum-square over constituents)
- 조석예측 시계열 RMS (RMS of tidal prediction)
- 조석 분산 설명률 / 신호대잡음비 (variance explained, SNR, percent energy)
- 스펙트럼·코히어런스 분석 (spectral / coherence analysis of sea level)
- 조위편차·잔차 분석 (non-tidal residual / sea level residual)
- 스큐서지 (skew surge)
- 폭풍해일 검증 지표 (storm surge skill: peak/timing error, 99th percentile, POD/FAR)
- 역기압효과·동적대기보정 검증 (inverse barometer / DAC verification)
- 해양재분석 SSH/ADT 비교 (reanalysis SSH/ADT vs tide gauge/altimetry, GLORYS·ERA5)
- 계절해면 주기 검증 (seasonal cycle, Sa/Ssa)
- 평균해수면 추세 (MSL trend) 와 수직지각운동(VLM)·GIA 보정
- 해수면수지 폐합 — 스테릭·질량 분해 (sea level budget: steric/manometric)
- 조석형태계수 (tidal form factor F)
- 조석 datum 검증 (MHW/MLW/MLLW/LAT, chart datum)
- 극치해면 재현빈도 — 연최대 GEV/Gumbel
- 극치해면 재현빈도 — POT/GPD (peaks-over-threshold)
- 결합확률법 (Joint Probability Method, JPM / SSJPM)
- 위성고도계 SLA 검증 — 검조소 대조
- 위성고도계 교차점 분석 (crossover analysis)
- 내부조석 검증 (internal tide verification)
- 삼중자료 대조 (triple collocation)
- 조석 에일리어싱 점검 (tidal aliasing in altimetry)
- 검조소 자료 품질관리(QC): datum 안정성·스파이크·버디체크
- 테일러 다이어그램·표준 통계 종합 (도메인 적용 주석)

---

### 조화분석으로 조화상수 추정 (Harmonic Analysis / Tidal Constituent Estimation)
- 무엇을 측정/검증하나: 조위·해면 시계열에서 각 분조(M2, S2, N2, K2, K1, O1, P1, Q1 등)의 진폭(amplitude H)과 지각(Greenwich phase lag G, epoch)을 최소제곱으로 추정한다. 모델 검증의 입력(조화상수)을 만드는 전처리 단계이자 그 자체가 분석 방법.
- 정의·수식: 수위 η(t) = Z0 + Σ_k f_k H_k cos(ω_k t + (V0+u)_k − G_k). f, u는 18.6년 교점주기(nodal) 보정, V0는 천문초기위상. 미지수는 각 분조의 코사인·사인 계수 a_k=H_k cos G_k, b_k=H_k sin G_k 이며 선형 최소제곱으로 구한 뒤 H_k=√(a²+b²), G_k=atan2(b,a).
- 적용 도메인/자료형: 검조소 시계열(시간별 수위), 모델 격자점 시계열, 위성고도계 트랙 시계열. 모델이 직접 조화상수를 출력하면 분석 생략 가능.
- 입력·전제: 등간격(또는 처리 가능한 비등간격) 수위 시계열. 분조 분해능은 레일리 기준(Rayleigh criterion)으로 record 길이에 의해 제한 — 인접 분조 분리에 최소 1/Δf 길이 필요(예 S2-K2 분리에 약 1년). 교점보정·추론(inference)으로 짧은 기록 보완.
- 해석 기준: 추정 진폭·지각의 신뢰구간(confidence interval)과 SNR로 유효성 판단(SNR≥2 권장). 잔차분산이 작을수록 적합 양호.
- 한계·주의: 기록이 짧으면 인접 분조가 섞임(레일리 미충족). 비선형 천해분조(M4, MS4 등)·기상조(radiational)·비정상성(seasonality)은 별도 처리. 위성고도계는 샘플링 주기로 인한 에일리어싱 주의(별도 카드 참조).
- 출처: Pawlowicz, Beardsley & Lentz (2002) "Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE", Computers & Geosciences 28, 929–937. Codiga (2011) "Unified Tidal Analysis and Prediction Using the UTide Matlab Functions" (GSO Tech. Report 2011-01). Foreman (1977/2004) 조화분석 절차. Pugh & Woodworth (2014) "Sea-Level Science" (Cambridge).

---

### 조석 admittance / 응답법 (Tidal Admittance / Response Method)
- 무엇을 측정/검증하나: 관측 조석과 천문조석 위치퍼텐셜(tidal potential) 사이의 주파수별 전달함수(admittance, 복소 이득·위상)를 추정한다. 모델·관측의 admittance가 일치하는지로 조석 응답의 물리적 타당성을 검증하고, 짧은 기록에서도 인접 분조를 분리하지 않고 평활하게 추정할 수 있다.
- 정의·수식: 분조 k의 admittance Z(ω_k) = H_k^obs / H_k^equil · e^{i(G_k^obs − G_k^equil)} (관측 조화상수를 평형조(equilibrium tide) 진폭·위상으로 정규화). admittance는 주파수의 완만한 함수라 가정 → 분해된 주파수들 사이를 보간해 해소 안 된 분조의 응답을 추론. 응답법(Munk & Cartwright)은 조석퍼텐셜에 가중치(response weights)를 적용해 예측.
- 적용 도메인/자료형: 검조소·모델·고도계 시계열. 특히 위성고도계처럼 분조가 에일리어싱되어 직접 조화분리가 어려운 자료, 또는 수개월 짧은 기록에 유효.
- 입력·전제: 정확한 천문조석퍼텐셜(예 Cartwright–Tayler–Edden 전개). admittance가 주파수에 따라 매끄럽다는 가정(공진 근처에선 위반).
- 해석 기준: 모델·관측 admittance의 진폭비(≈1)·위상차(≈0)가 분조군별로 일치하면 양호. admittance가 1을 크게 벗어나거나 주파수에 급변하면 천해 비선형·공진 영향 또는 모델 결함 신호.
- 한계·주의: 천해·만(bay) 공진역에서는 admittance가 매끄럽지 않아 보간 가정 위반. radiational 성분(S2, Sa)은 중력조 admittance와 다른 응답을 보임 — 분리 필요.
- 출처: Munk & Cartwright (1966) "Tidal spectroscopy and prediction", Phil. Trans. R. Soc. London A 259, 533–581. Cartwright & Tayler (1971), Cartwright & Edden (1973) 조석퍼텐셜 전개. Pugh & Woodworth (2014) "Sea-Level Science".

---

### 분조별 진폭 오차 (Amplitude Error, ΔH)
- 무엇을 측정/검증하나: 특정 분조의 모델 진폭 H_m과 관측(검조소/altimetry) 진폭 H_o의 차이. 분조 에너지 재현 정확도.
- 정의·수식: ΔH = H_m − H_o (또는 |H_m − H_o|). 다지점 평균은 RMS(ΔH)=√(⟨(H_m−H_o)²⟩) 또는 MAE(ΔH)=⟨|H_m−H_o|⟩.
- 적용 도메인/자료형: 격자 조석모델 vs 검조소/altimetry 조화상수. 분조별로 따로 계산.
- 입력·전제: 동일 분조의 모델·관측 진폭. 모델 격자점을 검조소 위치로 보간(최근접·이중선형). 단위 통일(cm/m).
- 해석 기준: 절대 임계값은 분조·해역에 따라 다름. 심해(>1km) M2는 복소 RMSE 수 cm 수준이 통상 양호, 천해·연안은 10 cm 이상도 흔함(예 동중국·서한반도 연안 M2 최대 불일치가 30 cm를 넘는 사례 보고). 상대오차(ΔH/H_o)로 보조 평가.
- 한계·주의: 진폭만 보면 지각 오차를 못 잡는다 — 반드시 지각 또는 벡터차와 병행. 작은 분조는 관측 불확실성이 커서 절대오차가 오해를 부른다.
- 출처: Stammer et al. (2014) "Accuracy assessment of global barotropic ocean tide models", Reviews of Geophysics 52, 243–282 (doi:10.1002/2014RG000450). 동중국해 검증 사례: Lee et al. (2025) J. Marine Sci. Eng. 13(3):395 (MDPI). 동아시아 주변해 비교: Cont. Shelf Res. / J. Sea Res. 201:102527 (2024).

---

### 분조별 지각 오차 (Phase / Epoch Error, ΔG)
- 무엇을 측정/검증하나: 특정 분조의 모델 지각 G_m과 관측 지각 G_o의 차이. 조석 위상(타이밍) 재현 정확도.
- 정의·수식: ΔG = G_m − G_o를 (−180°, 180°]로 wrapping. 다지점 MAE(ΔG)=⟨|wrap(G_m−G_o)|⟩.
- 적용 도메인/자료형: 격자 조석모델 vs 검조소/altimetry. 분조별 계산.
- 입력·전제: 동일 기준(Greenwich phase, 협정세계시 기준)으로 정의된 지각. 기준시간·경도보정이 일치해야 비교 가능.
- 해석 기준: 각도 오차이므로 시간으로 환산하면 직관적(예 M2 주기 12.42h에서 1° ≈ 2.07분). 수 도(°) 이내면 우수, 수십 도는 부진. 작은 진폭 분조의 지각은 의미가 약함.
- 한계·주의: 진폭이 작을수록 지각 추정 불확실성 급증 — 진폭 가중 또는 SNR 임계로 걸러야 한다. 위상 wrapping 실수(±360°) 빈번. 단독으로는 종합 오차가 안 됨.
- 출처: Pawlowicz et al. (2002), T_TIDE. Stammer et al. (2014), Reviews of Geophysics 52. Pugh & Woodworth (2014).

---

### 복소/벡터 차이 (Vector / Complex Amplitude Difference, D)
- 무엇을 측정/검증하나: 진폭과 지각을 한 지표로 통합한 분조별 오차. 조석검증의 사실상 표준 지표.
- 정의·수식: 분조를 복소수 Z = H e^{iG}(= H cosG + i H sinG)로 표현. 벡터차 D = |Z_m − Z_o| = √[(H_m cosG_m − H_o cosG_o)² + (H_m sinG_m − H_o sinG_o)²]. 코사인 in-phase 성분 차 C = H_m cosG_m − H_o cosG_o, 사인 quadrature 성분 차 S = H_m sinG_m − H_o sinG_o → D = √(C²+S²).
- 적용 도메인/자료형: 모든 조석모델 검증(격자/검조소/altimetry). 분조별로 계산 후 종합.
- 입력·전제: 모델·관측 모두 동일 분조의 (H,G) 쌍. 동일 위상 기준. 모델 격자→검조소 위치 보간.
- 해석 기준: D가 작을수록 양호. 글로벌 조석모델 심해 M2 복소 RMSE 약 2–5 cm가 현대 기준의 "우수" 영역, 천해는 10 cm 이상이 흔함. D는 진폭+지각 오차를 동시에 반영하므로 단일 순위 매기기에 적합.
- 한계·주의: D는 분조별 값 — 여러 분조 종합엔 RSS 필요(별도 카드). 관측 조화상수 자체 불확실성(짧은 기록·QC 미흡)이 D에 섞인다.
- 출처: Stammer et al. (2014), Reviews of Geophysics 52, 243–282. Andersen, Egbert 등 GOT/FES/TPXO 평가 관행. 조류 벡터차 평가의 유사 개념: Cummins & Oey 류 "model tidal currents against observations" 평가(Cont. Shelf Res.) — 본 문서에서는 수위 조화상수 벡터차로 적용.

---

### 분조별 RMS (RMS per Constituent, ½D 환산)
- 무엇을 측정/검증하나: 한 분조의 정현파 오차를 시간평균 RMS로 환산한 값. 벡터차 D와 직접 연결.
- 정의·수식: 진폭 D의 정현파 오차 신호의 RMS = D/√2. 코사인·사인 성분으로 보면 RMS = √[(C²_rms + S²_rms)] 형태로, 문헌에 따라 C_rms, S_rms를 √2 정규화해 정의(Stammer et al. 표기 D_rms = (C²_rms + S²_rms)^{1/2}).
- 적용 도메인/자료형: 조석모델 분조 검증. 분조별 RMS는 종합 RMS(RSS)의 구성요소.
- 입력·전제: 분조별 (H,G) 모델·관측. 정의(정규화 √2 포함 여부)를 문헌과 일치시켜야 비교 가능.
- 해석 기준: 작을수록 양호. 분조 RMS의 제곱합 제곱근이 그 분조 집합의 총 조석 오차.
- 한계·주의: D와 RMS의 √2 정규화 차이를 혼동하면 값이 어긋난다 — 항상 정의를 명시하라.
- 출처: Stammer et al. (2014), Reviews of Geophysics 52, 243–282 (D_rms 정의). Ray (2013) GOT 모델 평가.

---

### 다분조 종합 RMS / RSS (Total Tidal RMS, Root-Sum-Square over Constituents)
- 무엇을 측정/검증하나: 여러 분조의 오차를 한 수치로 통합한 모델의 전체 조석 정확도.
- 정의·수식: RSS = √(Σ_k (D_k/√2)²) = √(½ Σ_k D_k²). 여기서 D_k는 분조 k의 벡터차. 흔히 "8대 분조 종합 RMS" 또는 root-sum-square(RSS)로 보고. 잔차제곱합(residual sum of squares, RSS)과 약어가 겹치니 문맥 구분.
- 적용 도메인/자료형: 글로벌/지역 조석모델 랭킹. FES, TPXO, GOT, EOT 등 모델 상호비교의 표준 요약치.
- 입력·전제: 동일 분조 집합, 동일 검조소/altimetry 집합. 깊이대(예 >1000m vs <1000m)·연안근접도별 층화 비교 권장.
- 해석 기준: Stammer et al.(2014) 보고 — 8대 분조 종합 RSS가 원양(pelagic)·대륙붕(shelf)·연안(coastal) 각각 약 0.9, 5.0, 6.5 cm 수준이 현대 최상위 모델의 기준선. 동중국 주변해처럼 천해·복잡 해역은 EOT20이 RSS 약 11.1 cm로 보고(Lee et al. 2025). 깊이·연안 근접도에 따라 크게 변하므로 항상 데이터셋·깊이대를 명시.
- 한계·주의: 분조 집합·정규화·검조소 표본에 민감. 모델 간 공정비교엔 동일 프로토콜 필요. 천해 비선형분조 누락 시 과소평가.
- 출처: Stammer et al. (2014), Reviews of Geophysics 52, 243–282. Lee et al. (2025) J. Marine Sci. Eng. 13(3):395. Carrère et al. (FES 시리즈) 평가. Egbert & Erofeeva (TPXO/OTIS) 문서.

---

### 조석예측 시계열 RMS (RMS of Tidal Prediction)
- 무엇을 측정/검증하나: 조화상수 비교 대신, 모델·관측 조화상수로 동일 기간을 재구성(예측)해 만든 조위 시계열 사이의 RMS 오차. 실무에 직접 와닿는 종합지표.
- 정의·수식: η_pred(t) = Z0 + Σ_k f_k H_k cos(ω_k t + (V0+u)_k − G_k). RMS = √(⟨(η_m(t) − η_o(t))²⟩) (관측 직접 또는 관측 조화상수 재구성과 비교).
- 적용 도메인/자료형: 검조소 위치에서 모델 조석 예측 검증. 항만·연안 운영검증에 적합.
- 입력·전제: 동일 시간격자·동일 datum(평균해수면 기준 정렬). 교점보정·기준시각 일치.
- 해석 기준: RMS를 관측 조석 표준편차로 정규화하면 상대성능(설명분산) 파악. 작을수록 양호.
- 한계·주의: 관측 시계열엔 비조석 성분(해일·계절)이 섞여 있어 순수 조석 RMS와 다름 — 비교 대상(관측 조위만 vs 전체 수위)을 명확히. 위상 작은 어긋남이 시계열 RMS를 부풀린다(→ 스큐서지/복소차로 보완).
- 출처: Pugh & Woodworth (2014) "Sea-Level Science". Codiga (2011) UTide. WMO/IOC 조석예측 검증 관행(표준 참고문헌).

---

### 조석 분산 설명률 / 신호대잡음비 (Variance Explained, SNR, Percent Energy)
- 무엇을 측정/검증하나: 조화모형이 관측 수위 분산 중 얼마를 설명하는지, 각 분조가 유의한지.
- 정의·수식: 설명분산 = 1 − Var(잔차)/Var(관측). 분조 SNR = (분조 진폭)² / (진폭 추정분산). percent energy = 분조 에너지 / 총 분석 에너지. 분조 유의성 판단에 SNR≥1~2 관행.
- 적용 도메인/자료형: 검조소·모델 조화분석 품질평가, 분조 선택.
- 입력·전제: 조화분석 결과의 잔차분산·계수 공분산(또는 부트스트랩/몬테카를로 추정).
- 해석 기준: 조석 우세 해역은 설명분산이 매우 높음(>90%). 낮으면 비조석 변동(해일·하천류)·QC 문제 의심.
- 한계·주의: 잔차에 잔여 조석이 남으면(레일리 미충족, 위상 오차) SNR이 왜곡. 적색잡음 가정 위반 시 신뢰구간 과소.
- 출처: Codiga (2011) UTide (SNR·percent energy·Rayleigh 변형 진단). Pawlowicz et al. (2002) T_TIDE (신뢰구간·SNR).

---

### 스펙트럼·코히어런스 분석 (Spectral / Coherence Analysis of Sea Level)
- 무엇을 측정/검증하나: 모델·관측 수위 시계열의 파워스펙트럼밀도(PSD)와 두 시계열 간 코히어런스(coherence)·위상을 비교해, 조석대역(diurnal/semidiurnal/higher harmonics)과 비조석 대역의 에너지 분포·동조 정도를 주파수별로 검증.
- 정의·수식: PSD S(f) = |FFT(η)|² 의 기대값(Welch 평균). 교차스펙트럼 S_xy(f)로부터 코히어런스 γ²(f) = |S_xy|²/(S_xx S_yy) (0~1), 위상 φ(f)=arg(S_xy). 조석선스펙트럼이 솟는지, 잔차의 적색잡음 기울기가 맞는지 확인.
- 적용 도메인/자료형: 검조소·모델·고도계 수위/잔차 시계열. 조석제거 품질·천해 비선형 고조파 진단.
- 입력·전제: 등간격 충분히 긴 기록, 적절한 윈도(Hann)·세그먼트 평균. 결측 보간/마스킹.
- 해석 기준: 조석대역 PSD가 관측과 일치하고, 조석 라인에서 코히어런스≈1·위상차≈0이면 양호. 천해(M4/MS4) 고조파 에너지 재현, 잔차대역 코히어런스로 비조석 변동 동조 평가.
- 한계·주의: 스펙트럼 누설(leakage)·해상도 한계로 인접 분조 분리 제약. 비정상(계절·해면상승) 신호는 사전 제거 필요. 코히어런스는 표본수에 의존(세그먼트 적으면 과대).
- 출처: Munk & Cartwright (1966) tidal spectroscopy. Emery & Thomson "Data Analysis Methods in Physical Oceanography" (스펙트럼·코히어런스 표준). Pugh & Woodworth (2014).

---

### 조위편차·잔차 분석 (Non-tidal Residual / Sea Level Residual)
- 무엇을 측정/검증하나: 관측(또는 모델) 수위에서 천문조석 예측을 뺀 비조석 잔차. 해일·기압효과·계절·하천 영향 등. 모델의 비조석 해면 변동 재현을 검증.
- 정의·수식: residual(t) = η_obs(t) − η_tide_pred(t). 모델 검증 시 모델 잔차와 관측 잔차를 RMSE·상관·편향으로 비교.
- 적용 도메인/자료형: 검조소 시계열, 모델 수위 시계열. 폭풍해일·계절해면 검증의 출발점.
- 입력·전제: 신뢰성 있는 조화상수(예측 정확도가 잔차 품질을 좌우). datum·시간 정렬.
- 해석 기준: 잔차 RMSE가 작고 피크 잔차(해일)를 잘 따라가면 양호. 잔차에 남은 조석 진동(조석-해일 상호작용, 위상오차)은 결함 신호.
- 한계·주의: 조화분석의 위상 작은 오차가 잔차에 인공 첨두(artificial peak)를 만든다 — 이 때문에 스큐서지가 대안으로 선호됨. 천해 조석-해일 비선형 상호작용은 단순 차감으로 분리 안 됨.
- 출처: Williams, Horsburgh et al. (2016) — skew surge/non-tidal residual 비교(GRL). Pugh & Woodworth (2014). Muis et al. (2016) "A global reanalysis of storm surges and extreme sea levels", Nature Communications 7:11969.

---

### 스큐서지 (Skew Surge)
- 무엇을 측정/검증하나: 각 조석주기에서 관측 최고수위와 예측 천문 고조(high water)의 차이. 비조석 잔차의 조석위상 의존 문제를 회피한 폭풍해일 지표.
- 정의·수식: skew surge = (관측 한 조석주기 최대수위) − (그 주기의 예측 천문 고조위). 고조 시각이 달라도 무방(위상 독립).
- 적용 도메인/자료형: 검조소·모델 수위. 반일주조 우세 해역에서 특히 유효. 폭풍해일 모델 검증·극치분석 입력.
- 입력·전제: 정확한 천문조 예측(고조위·시각), 조석주기 단위 분할.
- 해석 기준: 모델 스큐서지와 관측 스큐서지의 분포·피크 일치도(RMSE·상관·QQ)로 평가. 잔차 기반 결과와 거의 동등하면서 위상오차 영향이 작음.
- 한계·주의: 일주조 우세·복잡 조석 해역에서는 "한 주기 최대" 정의가 모호해질 수 있다. 조석-해일 상호작용이 강하면 여전히 편향.
- 출처: Williams, J., Horsburgh, K.J., et al. (2016) "Tide and skew surge independence: New insights for flood risk", Geophysical Research Letters 43, 6410–6417 (doi:10.1002/2016GL069522). 중국 연안 비교: "Comparison between the skew surge and residual water level along the coastline of China", J. Hydrology (2021). Pugh & Woodworth (2014).

---

### 폭풍해일 검증 지표 (Storm Surge Skill: Peak/Timing Error, Percentile, Event Scores)
- 무엇을 측정/검증하나: 폭풍해일(또는 총수위) 모델의 피크 크기·발생시각 오차, 고분위 사건 재현, 임계초과 탐지능.
- 정의·수식: peak error = 모델 피크 − 관측 피크; timing error = 피크 시각 차. 고분위 평가: 관측 99퍼센타일 초과 표본에 대한 RMSE/편향, 또는 분위수기반 MAD(percentile-weighted MAD). 사건형 점수: 임계 초과 여부로 POD(=hits/(hits+misses)), FAR(=false alarms/(hits+false alarms)), CSI 등 분할표(contingency) 지표.
- 적용 도메인/자료형: 검조소·모델 해일/총수위 시계열. 연안 침수·경보 검증.
- 입력·전제: 동일 datum·시간격자, 사건 임계(절대 또는 분위) 사전정의.
- 해석 기준: 전체 RMSE뿐 아니라 고분위(99p) 성능을 별도 보고하는 것이 중요. 피크 과소예측·지연은 경보에 치명적. 편향·산포·이벤트 점수를 함께. (Campos-Caba et al. 2024는 ERA5 강제 모델이 극값을 과소예측하는 경향을 보고 — 강제자료 출처별 차이 유의.)
- 한계·주의: 단일 지표로 해일성능을 못 잡는다 — 평균·고분위·피크·타이밍·이벤트 점수를 조합해야. 임계 선택이 점수를 좌우.
- 출처: Campos-Caba et al. (2024) "Assessing storm surge model performance: what error indicators can measure the model's skill?", Ocean Science 20, 1513–1535. Muis et al. (2016), Nat. Commun. 7:11969 (GTSR). Fernández-Montblanc 등 GTSM 검증 사례.

---

### 역기압효과·동적대기보정 검증 (Inverse Barometer / Dynamic Atmospheric Correction)
- 무엇을 측정/검증하나: 대기압 변화에 대한 해면의 정역학적 반응(역기압효과, IB)과 고주파 바람·기압 강제의 동적 반응(DAC)을 모델·관측이 옳게 재현·보정하는지. ERA5 등 대기재분석 평균해면기압으로부터 IB/DAC를 산출해 모델 잔차·고도계 SLA 보정의 일관성을 검증.
- 정의·수식: 정적 역기압 η_IB = −(1/ρg)(P − P̄) ≈ −0.9948 cm/hPa (P̄ 전지구 평균기압). 동적대기보정 DAC = MOG2D 바로트로픽 모델(고주파, <20일)응답 + 저주파 IB. 보정 후 잔차/SLA의 기압 의존성이 제거됐는지 회귀·상관으로 확인.
- 적용 도메인/자료형: 검조소 잔차 vs ERA5 기압, 고도계 SLA(DAC 적용/미적용), 모델 수위. NetCDF 기압격자(ERA5)+검조소 CSV.
- 입력·전제: 시·공간 동기화된 평균해면기압(ERA5 등), 바다 전체 평균기압 제거, 검조소 위치 보간.
- 해석 기준: IB/DAC 보정 후 수위-기압 회귀기울기가 0에 가까워지고 잔차분산이 줄면 보정 양호. ~−1 cm/hPa 근방의 IB 민감도 재현. 고주파(<3일)·고위도는 동적 응답이 IB와 달라 DAC가 IB보다 우수.
- 한계·주의: 천해·만에서는 정적 IB 가정이 깨짐(동적응답 필요). 검조소·고도계·모델 사이에 DAC 적용 여부가 다르면 직접 비교 불가 — 보정 상태를 반드시 메타데이터로 확인.
- 출처: Carrère & Lyard (2003) "Modeling the barotropic response of the global ocean to atmospheric wind and pressure forcing — comparisons with observations", Geophysical Research Letters 30(6), 1275 (MOG2D/DAC). AVISO/CMEMS Dynamic Atmospheric Correction 처리문서. Pugh & Woodworth (2014).

---

### 해양재분석 SSH/ADT 비교 (Reanalysis SSH/ADT vs Tide Gauge/Altimetry — GLORYS·ERA5)
- 무엇을 측정/검증하나: 우리 모델의 해면고도(SSH)/절대역학지형(ADT)을 해양재분석(예 CMEMS GLORYS12, 1/12°)·고도계 격자(DUACS)·검조소 수위와 비교해 평균상태·변동성·추세의 일관성 검증. 조석을 제거한 비조석 해면(비조석 SSH/SLA) 비교가 핵심.
- 정의·수식: SLA = SSH − MSS(평균해면), ADT = SLA + MDT(평균역학지형) = MSS−geoid+SLA. 비교지표는 상관 R, RMSE, 표준편차비, 추세차(mm/yr), 그리고 패턴 비교(EOF/공간상관). 검조소는 평균제거·VLM 보정 후 SLA로 환산.
- 적용 도메인/자료형: NetCDF 격자(모델 SSH, GLORYS SSH/ADT, DUACS SLA) + 검조소 CSV. 비조석 해면 변동·중규모·계절·경년(ENSO 등) 검증.
- 입력·전제: 동일 기준기간 평균제거, 동일 조석·DAC 보정 상태, MDT 기준 통일. GLORYS는 고도계 SLA를 동화하나 검조소는 동화하지 않으므로 검조소는 (준)독립 검증자료로 사용 가능. 시·공간 매칭(최근접/이중선형).
- 해석 기준: 연안 SSH 상관 높을수록(>0.8) 양호, RMSE 수 cm. 추세가 통계적으로 구분 불가하면 일관성 양호. ADT의 평균 공간패턴(주요 해류 위치)이 재현되는지 확인.
- 한계·주의: 재분석도 "진리"가 아니다(동화·모델 오차 포함) — 삼중대조로 상호불확실성 분리 권장. 연안은 고도계·재분석 품질이 모두 낮음. MDT 기준·지오이드 모델 차이가 ADT 비교에 직접 영향.
- 출처: Lellouche et al. (2021) "The Copernicus Global 1/12° Oceanic and Sea Ice GLORYS12 Reanalysis", Frontiers in Earth Science 9:698876. CMEMS DUACS/SEALEVEL 검증 보고서(QUID). 미국 동안 재분석 평가: "An evaluation of eight global ocean reanalyses for the Northeast U.S. Continental Shelf", Prog. Oceanogr. (2023).

---

### 계절해면 주기 검증 (Seasonal Sea Level Cycle, Sa/Ssa)
- 무엇을 측정/검증하나: 연주기(Sa)·반년주기(Ssa) 해면 변동의 진폭·위상을 모델·관측이 일치시키는지. 스테릭(가열·담수)·기압·바람 강제의 계절 응답 재현 검증.
- 정의·수식: 월평균(또는 일평균) 수위에 연·반년 정현파 회귀: η(t)=ā + A_Sa cos(2π t/T_y − φ_Sa) + A_Ssa cos(4π t/T_y − φ_Ssa). 모델·관측의 (A,φ) 비교, 계절기후값(climatological monthly mean)의 RMSE.
- 적용 도메인/자료형: 검조소 월평균(PSMSL), 모델·재분석 SSH, 고도계 SLA. 계절해면·스테릭 검증.
- 입력·전제: 다년 기록으로 안정한 계절기후값, 추세·경년변동 제거.
- 해석 기준: 계절진폭·위상 일치(진폭차 수 cm 이내, 위상차 수십 일 이내면 양호). 위상이 크게 어긋나면 스테릭/질량 응답 시기 오류.
- 한계·주의: Sa는 중력조가 아닌 기상·스테릭 기원이라 조석 admittance와 분리. 연안은 하천·계절순환 영향이 커 변동 큼. 짧은 기록은 경년변동이 계절추정 오염.
- 출처: Pugh & Woodworth (2014) "Sea-Level Science". Vinogradov et al. (2008) "Annual cycle in coastal sea level", J. Climate. PSMSL 계절해면 자료.

---

### 평균해수면 추세와 수직지각운동·GIA 보정 (MSL Trend, VLM & GIA Correction)
- 무엇을 측정/검증하나: 장기 평균해수면(MSL) 변화율(mm/yr)과 그 불확실성. 검조소 상대해면 vs 위성/모델 절대해면 비교 시 지반운동 보정.
- 정의·수식: 월평균 MSL 시계열에 선형(또는 가속도 포함) 회귀: MSL(t)=a+b·t(+c·t²). b가 추세. 절대해면 = 상대해면(검조소) + VLM. VLM은 GNSS(@검조소) 또는 GIA 모델(예 ICE-6G/Peltier, ANU)로 보정.
- 적용 도메인/자료형: 검조소 월평균 수위(PSMSL), 위성고도계 GMSL, 모델 해면. 기후·해면상승 검증.
- 입력·전제: 충분히 긴 기록(>30년 권장), 계절·교점주기 제거, datum 연속성. GNSS-VLM은 5–20년이라 장기 외삽 가정 주의.
- 해석 기준: 20세기 글로벌 추세 약 1.7–1.8 mm/yr, 고도계 GMSL은 1993년 이후 평균 ~3.3 mm/yr이며 가속(≈0.08 mm/yr²) 보고. 지역추세 불확실성은 ~1 mm/yr 수준까지 커질 수 있음. (구체 수치는 분석기간·자료에 따라 다르니 항상 기간 명시.)
- 한계·주의: 검조소는 상대해면(지반운동 포함) — VLM 미보정 시 절대해면과 직접 비교 불가. GIA 모델 간 차이가 추세 불확실성에 기여. 자기상관 고려한 추세 표준오차 사용.
- 출처: NOAA Tides & Currents Sea Level Trends 방법론. Peltier (2004)/Peltier et al. (2015) ICE-5G/ICE-6G(VM5a) GIA. PSMSL 데이터 가이드. Nerem et al. (2018) "Climate-change–driven accelerated sea-level rise detected in the altimeter era", PNAS 115, 2022–2025. Prandi et al. (2021) 지역해면 추세·불확실성(Sci. Rep.).

---

### 해수면수지 폐합 — 스테릭·질량 분해 (Sea Level Budget: Steric/Manometric Decomposition)
- 무엇을 측정/검증하나: 총해면 변화를 스테릭(steric, 열·염팽창)과 질량(manometric/barystatic, 해수질량 변화) 성분으로 분해하고, "총해면(고도계) ≈ 스테릭(Argo) + 질량(GRACE)"의 폐합(closure)으로 모델·관측의 물리적 정합성을 검증.
- 정의·수식: η_total = η_steric + η_mass. 스테릭 = 수온·염분 적분(밀도변화); 질량 = GRACE 해양질량(또는 OBP). 폐합잔차 = η_total − (η_steric+η_mass)가 작아야 함. 추세·시계열·공간패턴으로 비교.
- 적용 도메인/자료형: 고도계 GMSL/지역 SLA, Argo 스테릭, GRACE 질량, 모델 SSH/스테릭/질량. 기후 검증.
- 입력·전제: 동일 기간·지역, 일관된 기준면, 적분 깊이(Argo 보통 2000m) 명시. 빙하성지각균형(GIA) 보정(특히 GRACE).
- 해석 기준: 글로벌 폐합잔차가 불확실성(수 0.x mm/yr) 내면 양호(Leuliette & Miller 2009류). 모델이 총해면을 맞춰도 성분 비율이 틀리면 물리과정 오류 신호. 지역(예 북대서양)은 잔차가 크게 남는 사례 보고.
- 한계·주의: 깊은바다(>2000m) 스테릭 누락, GRACE 신호누설·GIA 불확실성, 지역폐합은 운동·재분배 때문에 어려움. 모델 검증 시 성분별 출력이 있어야 적용.
- 출처: Leuliette & Miller (2009) "Closing the sea level rise budget with altimetry, Argo, and GRACE", Geophysical Research Letters 36, L04608. WCRP Global Sea Level Budget Group (2018), Earth Syst. Sci. Data. AVISO Global Mean Sea Level Budget 자료.

---

### 조석형태계수 (Tidal Form Factor, F)
- 무엇을 측정/검증하나: 해역의 조석 유형(반일주조/일주조/혼합형) 분류. 모델이 조석 체질을 옳게 재현하는지 정성 검증·표본 층화에 사용.
- 정의·수식: F = (H_K1 + H_O1) / (H_M2 + H_S2). F<0.25 반일주조, 0.25–1.5 혼합(반일주 우세), 1.5–3.0 혼합(일주 우세), >3.0 일주조.
- 적용 도메인/자료형: 검조소·모델 조화상수. 분류·지도화·검증 층화.
- 입력·전제: K1, O1, M2, S2 진폭. 모델·관측 동일 분조.
- 해석 기준: 모델 F와 관측 F의 분류 일치 여부. 경계 부근(혼합형)은 민감.
- 한계·주의: 4개 분조만 사용 — 천해·복잡 해역의 비선형성은 반영 못 함. 단독 검증지표가 아니라 보조·분류용.
- 출처: 형태계수 (K1+O1)/(M2+S2)는 van der Stok (1897) 기원, Defant (1958) "Ebb and Flow: The Tides of Earth, Air, and Water"(Univ. Michigan Press)에서 4구간 분류로 정착. Pugh & Woodworth (2014) "Sea-Level Science"(현대 교과서 정의).

---

### 조석 datum 검증 (Tidal Datums: MHW/MLW/MLLW/LAT, Chart Datum)
- 무엇을 측정/검증하나: 모델·분석이 산출한 조석 기준면(평균고조위 MHW, 평균저조위 MLW, 평균최저저조위 MLLW, 최저천문조위 LAT/약최저저조위 등)이 표준 정의·관측과 맞는지.
- 정의·수식: 19년(National Tidal Datum Epoch) 평균에서 MHW=고조 평균, MLW=저조 평균, MLLW=하루 두 저조 중 낮은 쪽 평균, MTL=(MHW+MLW)/2, LAT=조화예측 최저치. 한국 약최저저조위(해도기준면)는 주요 분조 진폭 합으로 근사.
- 적용 도메인/자료형: 검조소 통계, 모델 조석예측에서 datum 산출. 항해해도·연안공학.
- 입력·전제: 충분히 긴 예측/관측(이상적으로 19년 epoch), 일관된 수직기준.
- 해석 기준: 모델 datum과 공식 검조소 datum의 차이(cm). chart datum 정의 일치(국가별 상이 — LAT, MLLW, Z0−Σamplitudes 등).
- 한계·주의: 국가·기관별 datum 정의가 달라 직접 비교 시 정의 통일 필수. 짧은 기록은 19년 epoch로 환산 필요(동시관측 비교법).
- 출처: NOAA CO-OPS Tidal Datums 정의(National Tidal Datum Epoch). IHO Resolution(Chart Datum=LAT 권고). Pugh & Woodworth (2014).

---

### 극치해면 재현빈도 — 연최대 GEV/Gumbel (Extreme Sea Level Return Period: Annual Maxima)
- 무엇을 측정/검증하나: 극치 총수위(또는 해일)의 재현기간(예 50·100년 빈도) 추정과 모델·관측 간 비교 검증.
- 정의·수식: 연최대(annual maxima) 표본에 일반극치분포 GEV 적합: G(z)=exp{−[1+ξ(z−μ)/σ]^{−1/ξ}}. ξ=0이면 Gumbel. 재현수위 z_T는 1−1/T 분위수. 신뢰구간은 프로파일우도/델타법/부트스트랩.
- 적용 도메인/자료형: 검조소·모델 연최대 수위 시계열. 연안 침수·설계해면.
- 입력·전제: 충분히 긴 기록(최소 수십 년), 정상성(또는 비정상 GEV로 추세 반영), 독립 연최대.
- 해석 기준: 모델·관측 재현수위 곡선의 일치, QQ/PP plot, 적합도(AD/KS). 100년 빈도 신뢰구간 폭으로 불확실성 평가.
- 한계·주의: 연 1값이라 표본이 적어 외삽 신뢰구간이 넓다(POT가 대안). 해면상승·기후 비정상성 무시 시 과소추정. 조석-해일 의존 무시 위험.
- 출처: Coles (2001) "An Introduction to Statistical Modeling of Extreme Values" (Springer). Menéndez & Woodworth (2010) "Changes in extreme high water levels based on a quasi-global tide-gauge data set", JGR Oceans 115, C10011. "Evaluation of GEV model for frequency analysis of annual maximum water levels", Ocean Engineering (2008).

---

### 극치해면 재현빈도 — POT/GPD (Peaks-Over-Threshold)
- 무엇을 측정/검증하나: 높은 임계를 초과하는 모든 사건을 활용해 재현수위를 추정 — 연최대보다 표본을 늘려 불확실성 축소.
- 정의·수식: 임계 u 초과량 (X−u)에 일반파레토분포 GPD 적합: H(y)=1−[1+ξy/σ̃]^{−1/ξ}. 사건 발생을 포아송으로 모형화(POT=Poisson-GPD), 재현수위 결합. 임계 선택은 평균초과도표(mean residual life)·모수안정도표.
- 적용 도메인/자료형: 검조소·모델 수위. 극치 검증·설계.
- 입력·전제: 사건 독립화(declustering, 폭풍 단위로), 임계 적절성, 충분한 초과표본.
- 해석 기준: GEV와 일관된 재현수위, 더 좁은 신뢰구간. 임계 민감도 점검.
- 한계·주의: 임계·declustering 선택이 결과를 좌우(주관성). 조석성분 때문에 사건이 비독립일 수 있어 스큐서지 기반 극치(SSJPM)가 선호되기도.
- 출처: Coles (2001), Springer. Davison & Smith (1990) "Models for exceedances over high thresholds", J. R. Statist. Soc. B 52, 393–442 (GPD/POT). Arns et al. (2013) "Estimating extreme water level probabilities: A comparison of the direct methods and recommendations", Coastal Engineering 81, 51–66.

---

### 결합확률법 (Joint Probability Method, JPM / Skew Surge JPM)
- 무엇을 측정/검증하나: 총수위 극치를 천문조석과 해일의 결합확률로 분해·합성해 재현빈도 추정. 직접관측 극치가 부족할 때 강력.
- 정의·수식: 총수위 분포 = 조석분포 ⊛ 해일분포(독립 가정 시 합성곱 convolution). SSJPM은 스큐서지 분포와 조석 고조 분포를 결합. 의존이 있으면 copula로 결합.
- 적용 도메인/자료형: 검조소·모델 조석+해일. 설계해면, 모델 극치 검증.
- 입력·전제: 조석·해일의 분리·분포추정, 독립성 가정(또는 copula로 의존 반영). 충분한 해일 표본.
- 해석 기준: JPM 재현수위 vs 직접 GEV/POT 추정 일치. 의존 무시 시 동시극치 과소평가 — copula로 보정.
- 한계·주의: 조석-해일 비독립(상호작용) 해역에서 단순 합성곱은 편향. 계절성·해면상승 반영 필요.
- 출처: Pugh & Vassie (1980) "Applications of the joint probability method for extreme sea level computations", Proc. Inst. Civ. Eng. Batstone et al. (2013) "A UK best-practice approach for extreme sea-level analysis along complex topographic coastlines", Ocean Engineering 71, 28–39 (Skew Surge JPM). 결합확률·copula 적용: "A probabilistic approach to combine sea level rise, tide and storm surge ... return periods", Coastal Engineering (2024).

---

### 위성고도계 SLA 검증 — 검조소 대조 (Altimetry SLA Validation vs Tide Gauges)
- 무엇을 측정/검증하나: 위성고도계 해면고도이상(Sea Level Anomaly, SLA) 또는 모델 SLA를 독립 검조소 수위와 비교해 정확도·일관성 검증.
- 정의·수식: 검조소 부근 고도계 SLA와 검조소 SLA(평균·VLM 보정 후)의 상관·RMSE·표준편차차. 추세 비교는 mm/yr. 매칭은 "영향권(zone of influence)" 반경 내 트랙 평균.
- 적용 도메인/자료형: 고도계 트랙/격자 SLA(NetCDF), 검조소 시계열(CSV). 연안·외해.
- 입력·전제: 시·공간 매칭, 동일 기준기간 평균제거, 검조소 VLM 보정(절대 vs 상대해면), 조석·역기압(DAC) 보정 일치.
- 해석 기준: 연안 SLA 상관 높을수록(>0.7~0.9) 양호, RMSE 수 cm. GMSL 추세는 독립 검조소·모델과 통계적으로 구분 불가하면 일관성 양호.
- 한계·주의: 연안 고도계는 육지오염·궤도오차로 품질 저하 — 연안 재처리(X-TRACK 등) 필요. 검조소는 지반운동 포함. 시·공간 대표성 차이.
- 출처: Mitchum (1998/2000) "Monitoring the stability of satellite altimeters with tide gauges", J. Atmos. Oceanic Technol. Oelsmann et al. (2021) "The zone of influence: matching sea level variability from coastal altimetry and tide gauges for vertical land motion estimation", Ocean Science 17, 35–57. SWOT SLA 검증: Zhu, Peng & Shen (2025) Water 17(21):3066. CMEMS/DUACS 검증 보고서.

---

### 위성고도계 교차점 분석 (Crossover Analysis)
- 무엇을 측정/검증하나: 상승·하강 궤도(또는 다른 미션) 트랙이 교차하는 지점에서 SLA 차이로 궤도오차·내부 일관성·랜덤오차 평가.
- 정의·수식: 교차점 SLA 차 Δ = SLA_asc − SLA_desc(시간차 보정). 교차점차의 분산이 측정+처리 오차의 척도. crossover adjustment로 잔여 궤도오차 보정.
- 적용 도메인/자료형: 고도계 along-track SLA. 미션 내(self-crossover)·미션 간(dual).
- 입력·전제: 시간차에 따른 실제 해면변동 분리(작은 Δt 선택), 조석·DAC 보정 적용.
- 해석 기준: 교차점차 분산·RMS가 작을수록 자료 일관성 양호. 시계열 추세에 영향하는 잔여 궤도오차 식별.
- 한계·주의: 교차점 시간차 동안 실제 변동이 오차로 흡수될 수 있음. 연안은 교차점 자료 희소.
- 출처: 고도계 표준 처리(Crossover adjustment) — AVISO/CMEMS 처리문서. "Aliased Tidal Variability in Mesoscale Sea Level Anomaly Maps", J. Atmos. Oceanic Technol. (PMC6999748). SWOT/Jason 검증 문헌.

---

### 내부조석 검증 (Internal Tide Verification)
- 무엇을 측정/검증하나: 성층 효과로 발생하는 내부조석(internal/baroclinic tide)의 해면고도 서명(coherent SSH signature)을 모델·고도계·내부조석모델(예 HRET, Zaron)과 비교해 진폭·위상·전파를 검증. 바로트로픽 조석 제거 후의 잔여 조석대역 SSH가 핵심.
- 정의·수식: 고도계 SSH에서 바로트로픽 조석을 제거하고 분조주파수(M2 등)에 plane-wave 적합 → 진폭·파장·전파방향. 모델 내부조석 SSH와 복소차/상관 비교. coherent 성분과 incoherent(시간변동) 성분 분리.
- 적용 도메인/자료형: 고도계 along-track SSH(다년 적합), 고해상 모델 SSH. 심해·대륙붕단 내부조석 활발 해역.
- 입력·전제: 정밀 바로트로픽 조석 제거, 다년 기록(coherent 신호 누적), 성층·모드 구조 정보.
- 해석 기준: M2 내부조석 SSH 진폭 보통 수 mm~수 cm. 모델·고도계 진폭·위상 일치(복소상관)면 양호. SWOT 광폭관측으로 공간구조 직접검증 가능.
- 한계·주의: incoherent 내부조석은 시간평균 고도계로 안 잡힘. 진폭이 작아 SNR 낮음 — 다년 누적·정밀 보정 필요. 메소스케일과 혼선.
- 출처: Zaron (2019) "Baroclinic tidal sea level from exact-repeat mission altimetry" (HRET), J. Phys. Oceanogr. 49, 193–210. Ray & Zaron (2016) 내부조석 글로벌 지도. Stammer et al. (2014) 내부조석 절(節).

---

### 삼중자료 대조 (Triple Collocation)
- 무엇을 측정/검증하나: 세 독립 추정치(예 고도계, 검조소, 모델/재분석)의 오차분산을 동시에 추정 — 어느 것도 "진리"로 가정하지 않고 각 자료의 랜덤오차를 분리.
- 정의·수식: 세 자료가 공통 신호 + 독립 오차라 가정, 자료쌍 공분산으로 각 자료 오차분산 σ²_i를 푼다(가법오차모형). 스케일링/편향 보정 포함 변형 존재.
- 적용 도메인/자료형: SLA·수위 세 출처(예 고도계·검조소·GLORYS). 위성검증, 모델·관측 상호불확실성 분리.
- 입력·전제: 세 자료 시·공간 매칭, 오차 상호독립·공통신호 선형관계 가정.
- 해석 기준: 각 자료의 오차표준편차(cm) 산출 → 어느 자료가 가장 정밀한지·모델 오차수준 평가.
- 한계·주의: 오차 독립 가정 위반(공통 조석·기압 보정 오차, 재분석이 고도계를 동화한 경우) 시 편향. 표본 충분해야 안정.
- 출처: Stoffelen (1998) "Toward the true near-surface wind speed: error modeling and calibration using triple collocation", JGR Oceans 103, 7755–7766 (방법 원형). Gruber et al. (2016) triple collocation 리뷰(방법 일반). SLA 적용: SWOT/altimetry 검증 문헌(Water 17(21):3066, 2025 등).

---

### 조석 에일리어싱 점검 (Tidal Aliasing in Altimetry / Sampling)
- 무엇을 측정/검증하나: 고도계 반복주기·샘플링 때문에 조석신호가 저주파로 접혀 SLA·중규모 지도에 잡음으로 나타나는지 점검. 모델·자료의 조석 제거 품질 검증.
- 정의·수식: 분조 주파수 f_tide가 샘플링 f_s로 에일리어싱되면 겉보기 주파수 f_alias = |f_tide − n·f_s|. 예 Jason 9.9156일 반복에서 M2·S2·K1이 특정 저주파로 접힘.
- 적용 도메인/자료형: 고도계 SLA, 조석모델 제거 후 잔차. 중규모 해면 분석 품질.
- 입력·전제: 미션 반복주기, 적용 조석모델. 잔여 조석은 스펙트럼·교차점에서 식별.
- 해석 기준: 에일리어싱 주파수 대역의 잔여 에너지가 작을수록 조석제거 양호. 잔여 M2/S2 SLA가 보이면 조석모델 결함.
- 한계·주의: 연안·천해는 조석모델 정확도 낮아 에일리어싱 잔차 큼. 분석 윈도가 에일리어싱 주기보다 짧으면 분리 불가.
- 출처: "Aliased Tidal Variability in Mesoscale Sea Level Anomaly Maps", J. Atmos. Oceanic Technol. (PMC6999748). "Residual M2 and S2 ocean tide signals in complex coastal zones identified by X-Track reprocessed altimetry data" (2023), Cont. Shelf Res. Ray & Zaron 내부조석/에일리어싱 연구.

---

### 검조소 자료 품질관리 QC (Tide Gauge Quality Control: Datum Stability, Spikes, Buddy Check)
- 무엇을 측정/검증하나: 검증의 기준자료인 검조소 수위의 신뢰성 — datum 이동/드리프트, 스파이크, 시각오류, 결측을 탐지·보정. 잘못된 기준자료는 모든 검증을 오염시킨다.
- 정의·수식: (a) 스파이크/이상치: 시간차분·이동중앙값·표준편차 임계. (b) datum 이동: 벤치마크 수준측량, 인접 검조소·고도계 대조. (c) 버디체크(buddy check): 인접 검조소·모델·altimetry와의 잔차로 드리프트·점프 탐지. (d) 시각오류: 조석 위상 정렬 점검.
- 적용 도메인/자료형: 검조소 시계열(CSV/텍스트). 모든 해수면·조위 검증의 전처리.
- 입력·전제: 인접관측/기준자료, 벤치마크 수준측량 이력, 메타데이터(센서 교체·교정 이력).
- 해석 기준: 물리적으로 불가능한 점프·스파이크 제거, datum 연속성 확인. UHSLC식 Research-Quality(완전검수) vs Fast-Delivery(최소검수) 구분 인지.
- 한계·주의: 실시간 자료(예 IOC SLMF)는 무검수일 수 있음 — 검증 기준으로 쓰기 전 QC 필수. 과도한 자동제거는 진짜 극치(해일 피크)를 깎을 위험.
- 출처: IOC/UNESCO (2020) "Quality Control of in situ Sea Level Observations: a review and progress towards automated quality control" (IOC Manuals and Guides 83). UHSLC 데이터 품질등급. PSMSL/GLOSS 가이드. "Offsets in tide-gauge reference levels detected by satellite altimetry"(고도계 기반 datum 점검) 사례.

---

### 테일러 다이어그램·표준 통계 종합 (Taylor Diagram & Standard Statistics — 도메인 적용 주석)
- 무엇을 측정/검증하나: 상관계수·표준편차비·중심화 RMSE를 한 그림에 종합해 모델 다수를 한눈에 비교. 해수면·해일 시계열, 잔차 검증에 적용.
- 정의·수식: 중심화 RMSE² = σ_m² + σ_o² − 2σ_m σ_o R (코사인 법칙). 테일러 다이어그램은 R, σ_m/σ_o, CRMSE를 극좌표로 배치.
- 적용 도메인/자료형: 수위/잔차/해일 시계열. 분조 진폭·지각에는 직접 부적합(복소차·벡터차 사용).
- 입력·전제: 동일 기간·datum로 정렬된 모델·관측 시계열, 평균 제거(중심화).
- 해석 기준: 관측점(REF)에 가까운 모델이 우수. 상관 높고 표준편차비 1, CRMSE 작을수록 좋음.
- 한계·주의: 평균 편향(bias)은 중심화 통계에 안 나타남 — 편향은 따로 보고. 조화상수 검증은 본 다이어그램 대신 벡터차/RSS를 써야 한다.
- 출처: Taylor (2001) "Summarizing multiple aspects of model performance in a single diagram", JGR 106, 7183–7192. Wilks "Statistical Methods in the Atmospheric Sciences"(표준 참고문헌). Jolliffe & Stephenson "Forecast Verification: A Practitioner's Guide"(표준 참고문헌).

---

## 비교 워크플로우 요약 (우리 모델 vs ERA5/GLORYS/관측/위성)

1. **자료 적재·정렬:** NetCDF 격자(모델 SSH/조화상수, GLORYS SSH/ADT, 고도계 SLA, ERA5 MSLP) + 검조소 CSV. 시간(UTC)·좌표·단위 통일, 모델 격자→관측점 보간.
2. **기준·보정 통일:** datum(상대 vs 절대), 평균·계절 제거 기준, 조석보정·DAC·VLM 적용 여부를 양쪽에서 일치(미일치 시 비교 불가). → 「역기압/DAC 검증」·「QC」 카드.
3. **조석 분리:** 검조소·모델에서 조화분석(T_TIDE/UTide)으로 조화상수·예측 산출. → 「조화분석」·「admittance」.
4. **조석 검증:** 분조별 ΔH·ΔG, 벡터차 D, 분조 RMS, 종합 RSS, 형태계수, datum. → 도메인 핵심.
5. **비조석 해면 검증:** 잔차/스큐서지/해일 지표, ERA5 IB·GLORYS SSH·고도계 SLA와 상관·RMSE·테일러·스펙트럼·삼중대조. 계절(Sa/Ssa)·추세(MSL/VLM)·수지폐합.
6. **극치 검증:** 연최대 GEV, POT/GPD, JPM/SSJPM 재현수위 비교.
7. **위성 특화:** SLA 검조소 대조(zone of influence), 교차점, 에일리어싱, 내부조석.

---

## 출처(References)

- Pawlowicz, R., Beardsley, B., Lentz, S. (2002). Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE. *Computers & Geosciences*, 28, 929–937.
- Codiga, D.L. (2011). Unified Tidal Analysis and Prediction Using the UTide Matlab Functions. GSO Technical Report 2011-01, Univ. of Rhode Island.
- Foreman, M.G.G. (1977/2004). Manual for Tidal Heights Analysis and Prediction. Institute of Ocean Sciences (Pacific Marine Science Report).
- Munk, W.H., Cartwright, D.E. (1966). Tidal spectroscopy and prediction. *Philosophical Transactions of the Royal Society of London A*, 259, 533–581.
- Cartwright, D.E., Tayler, R.J. (1971); Cartwright, D.E., Edden, A.C. (1973). New computations of the tide-generating potential. *Geophysical Journal of the RAS*.
- Pugh, D., Woodworth, P. (2014). *Sea-Level Science: Understanding Tides, Surges, Tsunamis and Mean Sea-Level Changes*. Cambridge University Press.
- Emery, W.J., Thomson, R.E. (2001). *Data Analysis Methods in Physical Oceanography*. Elsevier. — 스펙트럼·코히어런스 표준(표준 참고문헌).
- Stammer, D., et al. (2014). Accuracy assessment of global barotropic ocean tide models. *Reviews of Geophysics*, 52, 243–282. doi:10.1002/2014RG000450.
- Lee et al. (2025). Accuracy Assessment of Ocean Tide Models in the Eastern China Marginal Seas Using Tide Gauge and GPS Data. *J. Marine Science and Engineering*, 13(3):395 (MDPI). doi:10.3390/jmse13030395.
- A comparison of global and regional ocean tide models with tide gauges in the East Asian marginal seas (2024). *Journal of Sea Research*, 201:102527.
- Ray, R.D. (2013). Precise comparisons of bottom-pressure and altimetric ocean tides. *JGR Oceans* (GOT 평가).
- Williams, J., Horsburgh, K.J., et al. (2016). Tide and skew surge independence: New insights for flood risk. *Geophysical Research Letters*, 43, 6410–6417. doi:10.1002/2016GL069522.
- Comparison between the skew surge and residual water level along the coastline of China (2021). *Journal of Hydrology*.
- Muis, S., et al. (2016). A global reanalysis of storm surges and extreme sea levels. *Nature Communications*, 7:11969. doi:10.1038/ncomms11969.
- Campos-Caba, R., et al. (2024). Assessing storm surge model performance: what error indicators can measure the model's skill? *Ocean Science*, 20, 1513–1535. doi:10.5194/os-20-1513-2024.
- Carrère, L., Lyard, F. (2003). Modeling the barotropic response of the global ocean to atmospheric wind and pressure forcing — comparisons with observations. *Geophysical Research Letters*, 30(6), 1275. (MOG2D / Dynamic Atmospheric Correction.)
- Lellouche, J.-M., et al. (2021). The Copernicus Global 1/12° Oceanic and Sea Ice GLORYS12 Reanalysis. *Frontiers in Earth Science*, 9:698876.
- An evaluation of eight global ocean reanalyses for the Northeast U.S. Continental Shelf (2023). *Progress in Oceanography*.
- Vinogradov, S.V., et al. (2008). The annual cycle in coastal sea level. *Journal of Climate*. — 계절해면(표준 참고문헌, 확인요).
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*. Springer.
- Davison, A.C., Smith, R.L. (1990). Models for exceedances over high thresholds. *J. Royal Statistical Society B*, 52, 393–442.
- Menéndez, M., Woodworth, P.L. (2010). Changes in extreme high water levels based on a quasi-global tide-gauge data set. *JGR Oceans*, 115, C10011.
- Arns, A., et al. (2013). Estimating extreme water level probabilities: A comparison of the direct methods and recommendations for best practice. *Coastal Engineering*, 81, 51–66.
- Evaluation of GEV model for frequency analysis of annual maximum water levels in the coast of the United States (2008). *Ocean Engineering*. — (확인요)
- Pugh, D.T., Vassie, J.M. (1980). Applications of the joint probability method for extreme sea level computations. *Proc. Institution of Civil Engineers*.
- Batstone, C., et al. (2013). A UK best-practice approach for extreme sea-level analysis along complex topographic coastlines (Skew Surge JPM). *Ocean Engineering*, 71, 28–39.
- A probabilistic approach to combine sea level rise, tide and storm surge into representative return periods of extreme total water levels (2024). *Coastal Engineering*. — (확인요)
- Mitchum, G.T. (1998/2000). Monitoring the stability of satellite altimeters with tide gauges. *J. Atmospheric and Oceanic Technology*.
- Oelsmann, J., et al. (2021). The zone of influence: matching sea level variability from coastal altimetry and tide gauges for vertical land motion estimation. *Ocean Science*, 17, 35–57.
- Zhu, H., Peng, F., Shen, Y. (2025). Validation of Sea Level Anomalies from the SWOT Altimetry Mission Around the Coastal Regions of East Asia and the US West Coast. *Water*, 17(21):3066. doi:10.3390/w17213066.
- Aliased Tidal Variability in Mesoscale Sea Level Anomaly Maps. *J. Atmospheric and Oceanic Technology* (PMC6999748).
- Residual M2 and S2 ocean tide signals in complex coastal zones identified by X-Track reprocessed altimetry data (2023). *Continental Shelf Research*.
- Zaron, E.D. (2019). Baroclinic tidal sea level from exact-repeat mission altimetry (HRET). *Journal of Physical Oceanography*, 49, 193–210.
- Ray, R.D., Zaron, E.D. (2016). M2 internal tides and their observed wavenumber spectra from satellite altimetry. *JGR Oceans*.
- Stoffelen, A. (1998). Toward the true near-surface wind speed: error modeling and calibration using triple collocation. *JGR Oceans*, 103, 7755–7766. doi:10.1029/97JC03180.
- Gruber, A., et al. (2016). Recent advances in (soil moisture) triple collocation analysis. *Int. J. Applied Earth Observation* (방법 일반 리뷰).
- Nerem, R.S., et al. (2018). Climate-change–driven accelerated sea-level rise detected in the altimeter era. *PNAS*, 115, 2022–2025.
- Leuliette, E.W., Miller, L. (2009). Closing the sea level rise budget with altimetry, Argo, and GRACE. *Geophysical Research Letters*, 36, L04608.
- WCRP Global Sea Level Budget Group (2018). Global sea-level budget 1993–present. *Earth System Science Data*, 10, 1551–1590.
- Prandi, P., et al. (2021). Local sea level trends, accelerations and uncertainties over 1993–2019. *Scientific Reports* / *Scientific Data*.
- NOAA CO-OPS — Sea Level Trends methodology & Tidal Datums (National Tidal Datum Epoch). NOAA Tides & Currents.
- Peltier, W.R. (2004); Peltier, W.R., Argus, D.F., Drummond, R. (2015). ICE-5G / ICE-6G(VM5a) Glacial Isostatic Adjustment models. *JGR Solid Earth*.
- PSMSL — Permanent Service for Mean Sea Level; GLOSS (Global Sea Level Observing System).
- IOC/UNESCO (2020). Quality Control of in situ Sea Level Observations: a review and progress towards automated quality control. IOC Manuals and Guides 83.
- UHSLC (University of Hawaii Sea Level Center) data quality levels (Research-Quality vs Fast-Delivery).
- IHO — Resolution on Chart Datum (Lowest Astronomical Tide). International Hydrographic Organization.
- Taylor, K.E. (2001). Summarizing multiple aspects of model performance in a single diagram. *Journal of Geophysical Research*, 106, 7183–7192.
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences*. Academic Press. — 표준 참고문헌.
- Jolliffe, I.T., Stephenson, D.B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science*. Wiley. — 표준 참고문헌.
- van der Stok, J.P. (1897); Defant, A. (1958). *Ebb and Flow: The Tides of Earth, Air, and Water* (Univ. of Michigan Press) — 조석형태계수 분류 정착.
