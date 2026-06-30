# 도메인: 파랑 (Ocean Waves) 검증·분석 방법 카탈로그

이 문서는 수치 파랑모델(WAVEWATCH III, SWAN, WAM 등)의 결과를 부이(buoy)·위성 고도계(altimeter)·재분석자료(ERA5, GLORYS 등 — 단 GLORYS는 해양순환 재분석으로 파랑변수는 직접 제공하지 않으므로 실제로는 ECMWF ERA5 파랑, CMEMS WAVERYS 파랑 재분석 등을 대조군으로 쓴다)와 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 파랑 검증의 핵심은 (1) 벌크 파라미터(유의파고 Hs, 주기 Tp/Tm/Tz, 파향 Dir)의 통계적 일치도, (2) 파향의 원형통계(circular statistics) 처리, (3) 1D/2D 스펙트럼 및 windsea/swell 분리(partition) 비교, (4) 극치파고(extreme) 검증, (5) (앙상블이면) 확률예보 검증이다. 표준 지표는 평균오차(bias), 평균제곱근오차(RMSE), 산포지수(scatter index, SI), 상관계수(correlation), 대칭기울기(symmetric slope)이며, ECMWF/WMO-JCOMM Lead Centre for Wave Forecast Verification(LC-WFV)이 운영 표준 절차를 제공한다. 본 카탈로그는 그 Skill의 references/recipes 토대로 쓰인다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석), [시계열]=부이·관측소 CSV/텍스트, [트랙]=위성 고도계 along-track, [스펙트럼]=1D/2D 스펙트럼.
> **"우리 모델 vs ERA5/관측/위성" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **유의파고 검증 (Hs/Hm0 verification)** — 벌크 파고 일치도, bias/RMSE/SI/상관
- ★ **평균오차 Bias / 평균오차절댓값 MAE** — 계통오차 진단
- ★ **평균제곱근오차 RMSE / 중심화 RMSE (CRMSD)** — 무작위+계통 오차
- ★ **산포지수 SI (Scatter Index)** — 파랑 검증의 1차 표준 지표
- **선형회귀 기울기·절편 (OLS slope / intercept)** — 산점도 추세·조건부 편향
- **HH 대칭기울기 회귀 (Hanson–Hipps / symmetric slope)** — 등가 변수 회귀
- ★ **상관계수 R (Pearson) 와 결정계수 R²** — 선형 상관
- **Willmott 일치도 지수 d (Index of Agreement)** — 정규화 적합도
- **Nash–Sutcliffe 효율 NSE** — 모델 설명력
- ★ **주기 검증 (Tp / Tm01 / Tm02·Tz)** — 첨두/평균/영점교차 주기
- ★ **파향 검증과 원형통계 (Directional / circular statistics)** — 각도 평균·원형 RMSE
- **방향 분산 / 펼침 (Directional spread)** — 파향 집중도 검증
- ★ **QQ-plot (분위수-분위수 도표)** — 분포 꼬리·극치 일치
- ★ **Taylor 다이어그램** — 상관·표준편차·CRMSD 동시 요약
- **목표 다이어그램 (Target diagram)** — bias 대 CRMSD 분해
- **1D 주파수 스펙트럼 비교 (frequency spectrum)** — E(f) 형상·로그오차
- **2D 방향 스펙트럼 비교 (directional spectrum)** — E(f,θ) 비교
- **스펙트럼 모멘트 비교 (spectral moments mₙ)** — m0·m1·m2 유도 파라미터
- **스펙트럼 분할 / windsea·swell 분리 (spectral partitioning)** — watershed/Hanson–Phillips
- ★ **극치파고 분석 (Extreme value analysis)** — POT-GPD / 연최대-GEV / 재현주기
- ★ **위성 고도계 대조 (altimeter collocation)** — super-obs·시공간 콜로케이션
- ★ **삼중 콜로케이션 (Triple collocation, TC/ETC)** — 기준자료 없는 오차분산 추정
- ★ **확률밀도·누적분포 비교 (PDF/CDF, KS 검정)** — 분포 동질성
- **범주형/임계 초과 검증 (Categorical / threshold: POD·FAR·CSI)** — 고파고 경보 검증
- **확률예보 검증 (CRPS / Brier / ROC, 앙상블)** — 앙상블 파랑예보 신뢰도·해상도
- ★ **재분석 격자-격자 공간비교 (gridded reanalysis map difference)** — ERA5 등 면적 bias/RMSE 지도
- ★ **운영 검증 프레임워크 (WMO-JCOMM / ECMWF LC-WFV)** — 표준 절차·매치업

---

### ★ 유의파고 검증 (유의파고 / Significant wave height, Hs·Hm0)
- 무엇을 측정/검증하나: 모델이 산출한 유의파고가 관측(부이·고도계) 또는 재분석(ERA5)과 통계적으로 일치하는지. 파랑 검증의 가장 기본이자 1차 지표.
- 정의·수식: 스펙트럼 0차 모멘트 기반 Hm0 = 4·√m0 (m0 = ∫S(f)df). 시간영역 정의 H1/3(상위 1/3 파의 평균)과 구분(둘은 근사적으로만 같음). 검증은 모델·관측 매치업 쌍에 bias, RMSE, SI, R을 적용.
- 적용 도메인/자료형: [격자](모델·ERA5) vs [시계열](부이) / [트랙](고도계). NetCDF 격자 → 관측 지점 보간 후 비교.
- 입력·전제: 동일 시각·동일 위치로 정렬(콜로케이션). 모델 격자값을 관측 위치로 보간(역거리가중 IDWI 또는 최근접). 고도계는 1Hz/super-obs 평균화 필요. 모델·관측의 Hs 정의(Hm0 vs H1/3)·기준시각(순간 vs 윈도우 평균) 통일.
- 해석 기준(관행): 외해 운영모델 기준 Hs RMSE 약 0.2~0.5 m, SI 약 0.10~0.20, R ≥ 0.90이면 양호. 연안·복잡지형은 SI가 커진다. WW3/SWAN 사례에서 RMSE 0.49~0.63 m, R 0.89~0.90 보고(개별 사례값이므로 절대기준 아님).
- 한계·주의: 저파고대에서 SI가 과대평가됨(분모 효과). 관측 자체 오차(부이 ±0.1 m 수준)와 대표성 오차(representativeness; 점 부이 vs 격자/footprint 평균)를 고려해야 함.
- 출처: Janssen, Hansen & Bidlot (1997, Weather and Forecasting 12(4)); Bidlot et al. (2002, Weather and Forecasting); ECMWF/WMO LC-WFV; HY-2B 고도계 검증(MDPI Remote Sensing, doi:10.3390/rs17233829).

---

### ★ 평균오차 / 절대평균오차 (Bias / Mean Absolute Error, MAE)
- 무엇을 측정/검증하나: Bias는 모델의 계통적 과대/과소 추정(평균 치우침). MAE는 부호 무관 평균 오차 크기.
- 정의·수식: Bias = mean(model − obs) = (1/N)Σ(mᵢ − oᵢ). MAE = (1/N)Σ|mᵢ − oᵢ|. 정규화 bias = Bias / mean(obs).
- 적용 도메인/자료형: 모든 벌크 파라미터(Hs, Tp, Tm, Dir). [격자]/[시계열]/[트랙] 공통.
- 입력·전제: 정렬된 매치업 쌍. 파향은 원형통계로 별도 처리(아래 카드 참조 — 직선 bias 식 적용 금지).
- 해석 기준: Bias > 0이면 모델 과대추정. Hs bias가 평균파고의 ±5% 이내면 보통 양호로 본다. 고도계 검증 사례에서 SWH bias 0.14 m 보고(사례값).
- 한계·주의: bias가 0이어도 양·음 오차 상쇄로 정확하다는 뜻은 아님(RMSE 병행 필수). MAE는 RMSE보다 큰 오차에 덜 민감(이상치에 강건).
- 출처: Wilks, *Statistical Methods in the Atmospheric Sciences* (표준 교과서); Mentaschi et al. (2013, Ocean Modelling 72:53–58, 오차지표 비교).

---

### ★ 평균제곱근오차 / 중심화 RMSE (RMSE / Centered RMS Difference, CRMSD)
- 무엇을 측정/검증하나: RMSE는 계통+무작위 오차를 합친 전체 오차 크기. CRMSD(=평균 제거 후 RMSE)는 bias를 제거한 순수 패턴/변동 오차.
- 정의·수식: RMSE = √[(1/N)Σ(mᵢ−oᵢ)²]. CRMSD = √[(1/N)Σ((mᵢ−m̄)−(oᵢ−ō))²]. 관계식: RMSE² = Bias² + CRMSD².
- 적용 도메인/자료형: 모든 연속 파라미터. Taylor/Target 다이어그램의 기본 구성요소.
- 입력·전제: 정렬된 쌍. RMSE는 단위 동반(m, s, °).
- 해석 기준: 작을수록 양호. CRMSD를 bias와 분리해 보면 "치우침 문제"인지 "변동 재현 문제"인지 진단 가능.
- 한계·주의: 제곱 가중이라 이상치(outlier)·극치에 민감. 평균을 과소추정하는 모델이 RMSE상 유리하게 보이는 함정 존재(Mentaschi et al. 2013) → SI/HH 병행. NRMSE = RMSE/mean(obs)로 정규화해 사례 간 비교.
- 출처: Wilks (교과서); Taylor (2001, JGR 106(D7)); Jolliffe & Stephenson, *Forecast Verification*; Mentaschi et al. (2013).

---

### ★ 산포지수 (산포지수 / Scatter Index, SI)
- 무엇을 측정/검증하나: 무작위 오차를 관측 평균으로 정규화한 값. 파랑 검증에서 가장 널리 쓰이는 1차 표준 지표.
- 정의·수식: (ECMWF LC-WFV 정의) SI = σ(model − obs) / mean(obs) = CRMSD/mean(obs) — 즉 "예측-관측 차의 표준편차(=bias 제거)를 관측 평균으로 정규화". **주의**: 일부 문헌은 bias 미제거 RMSE/mean(obs)를 SI로 사용하므로 보고 시 정의를 반드시 명시. 예: 차 표준편차 0.5 m, 관측평균 2 m → SI = 25%.
- 적용 도메인/자료형: 주로 Hs, 그 외 Tp·풍속에도 적용. [격자]/[시계열]/[트랙].
- 입력·전제: 정렬된 매치업. 관측 평균이 작으면(저파고대) 불안정.
- 해석 기준(관행): Hs SI < 0.15 우수, 0.15~0.25 양호, > 0.30 개선 필요(외해 기준). 고도계 SWH 검증 사례 SI 9.4%, WW3 ST4 심해 사례 SI 0.16 보고(사례값, 절대기준 아님).
- 한계·주의: 정의(bias 포함/제거)에 따라 값이 달라지므로 보고 시 명시. 저파고 환경에서 과대.
- 출처: ECMWF/WMO LC-WFV "Verification results"; Bidlot et al. (2002).

---

### 선형회귀 기울기·절편 (최소제곱 / OLS slope and intercept)
- 무엇을 측정/검증하나: 산점도(obs를 x, model을 y)에 직선을 적합해 조건부 편향(파고가 클수록/작을수록 과대·과소되는 경향)을 정량화. 단일 bias가 못 보는 진폭(amplitude) 오차를 드러낸다.
- 정의·수식: model = a + b·obs를 최소제곱 적합. 기울기 b<1이면 모델이 큰 값에서 과소(에너지 saturation 흔함), 절편 a≠0이면 저파고대 offset. 종종 "강제 원점통과(b only)" 적합도 병행.
- 적용 도메인/자료형: Hs·Tp 산점도. [시계열]/[트랙]/[격자].
- 입력·전제: 정렬된 매치업. OLS는 x(관측)를 무오차로 가정 → 두 자료 모두 오차가 크면 기울기가 1쪽으로 편향(regression dilution) → HH 대칭회귀나 직교회귀 권장.
- 해석 기준: 기울기≈1, 절편≈0이 이상적. 고파고 과소(b<1)는 파랑모델의 전형적 약점.
- 한계·주의: OLS slope를 "대칭" 지표로 오해 금지(아래 HH 카드와 구분). 이상치 민감.
- 출처: Wilks (교과서, 회귀 기본); Mentaschi et al. (2013, 회귀·HH 비교).

---

### HH 대칭기울기 회귀 (Hanson–Hipps 대칭회귀 / HH symmetric slope regression)
- 무엇을 측정/검증하나: 모델과 관측을 동등한(symmetric) 변수로 보고 추세 기울기/정규화 오차를 추정. OLS가 한 변수를 무오차로 가정하는 편향을 보정.
- 정의·수식: x·y를 대칭 취급하는 회귀(주축/직교회귀 계열). Mentaschi et al.(2013)이 정식화한 HH 지표 = √[ Σ(mᵢ−oᵢ)² / Σ(mᵢ·oᵢ) ] 형태로, 평균 과소추정 모델을 부당하게 우대하지 않는 정규화 오차를 제공.
- 적용 도메인/자료형: Hs·Tp 산점도 검증. 부이/고도계 대조.
- 입력·전제: 두 자료 모두 측정오차가 있다는 가정(파랑 검증의 현실).
- 해석 기준: HH 지표가 작을수록 양호. 기울기 1, 절편 0에 가까울수록 양호. RMSE가 평균 과소추정으로 왜곡될 때 HH가 더 공정한 순위를 준다.
- 한계·주의: OLS slope와 혼동 금지. 대칭회귀는 과대·과소를 한쪽으로 몰지 않음.
- 출처: Mentaschi, Besio, Cassola & Mazzino (2013, Ocean Modelling 72:53–58 — HH 지표 정식 제안); Hanson et al. (2009, JTECH 26(8) — spectral partition 검증에서 HH 사용).

---

### ★ 상관계수 / 결정계수 (Pearson R / R²)
- 무엇을 측정/검증하나: 모델-관측 변동의 선형 동조성. R²는 설명된 분산비.
- 정의·수식: R = cov(m,o)/(σ_m·σ_o). R² = R의 제곱.
- 적용 도메인/자료형: Hs(높음), Tp(중간), Dir(원형R 별도) — [시계열]/[격자].
- 입력·전제: 정렬된 쌍. 정상성·선형성 가정. 자기상관 강한 시계열은 유효표본수 보정 필요.
- 해석 기준: Hs R ≥ 0.90 우수. Tp는 multimodal sea에서 R이 낮아짐.
- 한계·주의: R이 높아도 bias·기울기 오류는 못 잡음(회귀·bias 병행). 위상(시간지연) 오차에 민감. 파향에는 직접 적용 불가(원형 상관 사용).
- 출처: Wilks; Taylor (2001).

---

### Willmott 일치도 지수 (Index of Agreement, d)
- 무엇을 측정/검증하나: 0~1로 정규화된 모델-관측 일치도. R과 달리 bias·기울기 오류에 민감.
- 정의·수식: d = 1 − [Σ(mᵢ−oᵢ)²] / [Σ(|mᵢ−ō|+|oᵢ−ō|)²]. 개선판 d1(절대값형), dr(refined, Willmott 2012)도 존재.
- 적용 도메인/자료형: Hs·수위 등 파랑/해양 변수. [시계열].
- 입력·전제: 정렬된 쌍.
- 해석 기준: d → 1 완전일치. 0.9 이상 양호로 보고하는 관행.
- 한계·주의: 제곱형(d)은 극치에 민감 → 절대값형(d1)·dr 병행 권장. 단독 사용 비권장(다른 지표와 함께).
- 출처: Willmott (1981, *Physical Geography* 2); Willmott et al. (1985, JGR); Willmott, Robeson & Matsuura (2012, *Int. J. Climatology*, dr 지표).

---

### Nash–Sutcliffe 효율 (NSE)
- 무엇을 측정/검증하나: 모델이 관측 평균 대비 분산을 얼마나 설명하는지(수문학 기원, 파랑 시계열에도 사용).
- 정의·수식: NSE = 1 − [Σ(mᵢ−oᵢ)²]/[Σ(oᵢ−ō)²].
- 적용 도메인/자료형: Hs·Tp [시계열].
- 입력·전제: 정렬된 쌍.
- 해석 기준: 1 완전, 0이면 평균예측 수준, < 0이면 평균보다 못함. 통상 >0.5 양호로 보고(수문 관행, 파랑엔 절대기준 아님).
- 한계·주의: 극치(분산) 가중이 큼. 계절 변동이 큰 자료에서 과대평가(분모가 커져 점수가 후함).
- 출처: Nash & Sutcliffe (1970, *Journal of Hydrology*).

---

### ★ 주기 검증 (첨두주기 Tp / 평균주기 Tm01·Tm02·Tz)
- 무엇을 측정/검증하나: 파의 시간 척도 재현. Tp=스펙트럼 첨두주기, Tm01=에너지 평균주기(m0/m1), Tm02=Tz≈√(m0/m2)=영점교차주기.
- 정의·수식: Tp = 1/f_peak. Tm01 = m0/m1. Tm02 = √(m0/m2). 검증은 bias/RMSE/SI/R 적용.
- 적용 도메인/자료형: 모델 vs 부이 스펙트럼 유도값. [시계열]/[스펙트럼]. (고도계는 주기 미제공)
- 입력·전제: 모델·관측 모두 동일 모멘트 정의를 써야 함(정의 불일치가 흔한 오류원). 부이 고주파 절단(cutoff)이 Tm02에 크게 영향.
- 해석 기준: Tp는 multimodal(windsea+swell) 시 첨두 점프로 RMSE가 크게 나옴 → Tm01/Tm02가 더 안정적. 평균주기 SI < 0.1이면 양호.
- 한계·주의: Tp는 불연속(에너지 두 봉우리가 비슷하면 첨두가 튐) → Tp 단독 검증은 오해 소지. 평균주기 병행 필수.
- 출처: WMO, *Guide to Wave Analysis and Forecasting* (WMO-No. 702); Bidlot et al. (2002).

---

### ★ 파향 검증과 원형통계 (파향 / Mean wave direction, circular statistics)
- 무엇을 측정/검증하나: 평균파향(Dir)의 모델-관측 일치. 각도는 0/360° 경계 때문에 일반 산술평균·RMSE 사용 불가 → 원형통계 필요.
- 정의·수식: 각도차 Δθ를 (−180°,180°]로 wrap. 원형평균 = atan2(Σsinθ, Σcosθ). 원형 bias = 원형평균(Δθ). 원형 RMSE = √[mean(wrap(Δθ)²)]. 또는 단위벡터로 변환해 벡터 오차(vector RMSE) 계산.
- 적용 도메인/자료형: 부이(방향분해 Fourier 계수 a1,b1 기반), 모델 평균파향. [시계열]/[스펙트럼]/[격자].
- 입력·전제: 모델·관측 방향 규약 통일(oceanographic "향하는 곳" vs meteorological "오는 곳", 진북 기준, 시계방향/반시계). 저파고 시 파향 신뢰도 낮음 → Hs 임계로 필터.
- 해석 기준: 평균파향 RMSE 20~30°면 일반적; 첨두파향(peak dir)은 변동이 커 RMSE 더 큼(부이 비교 사례 ~21.9°, Beckman & Long 2022).
- 한계·주의: 0/360 wrap 미처리 시 치명적 오류. 저Hs·multimodal에서 파향 정의가 모호.
- 출처: Bowers, Morton & Mould (2000, *Applied Ocean Research* 22(1):13–30, "Directional statistics of the wind and waves"); Hanson & Jensen (2007, JTECH 24(3), "Directional Validation of Wave Predictions"); Kuik, van Vledder & Holthuijsen (1988, JPO, 부이 방향 파라미터).

---

### 방향 분산 / 펼침 (Directional spread, σθ)
- 무엇을 측정/검증하나: 에너지가 첨두파향 주위로 얼마나 좁게/넓게 퍼져 있는지(파향 집중도).
- 정의·수식: σθ = √(2(1−r1)) (r1 = √(a1²+b1²)/m0, 1차 Fourier 계수 기반). cos²ˢ 펼침함수의 지수 s와 관계(s 클수록 좁음).
- 적용 도메인/자료형: 부이 방향 스펙트럼 vs 모델 2D 스펙트럼. [스펙트럼].
- 입력·전제: 부이의 a1,b1,a2,b2 또는 모델 E(f,θ). 주파수별/벌크 둘 다 가능.
- 해석 기준: 모델이 펼침을 과소(너무 좁게) 모의하는 경향 보고됨. 부이 종류 간에도 ~7.5° 차이 보고(Beckman & Long 2022) → 관측 불확실성 큼.
- 한계·주의: 부이가 제한된 Fourier 차수(a1,b1,a2,b2 4개)만 측정 → 진짜 펼침의 근사. MEM/MLM 추정법에 따라 값 달라짐.
- 출처: Kuik et al. (1988, JPO); Beckman & Long (2022, *Frontiers in Marine Science*, doi:10.3389/fmars.2022.966855, 부이 오차 정량화).

---

### ★ QQ-plot (분위수-분위수 도표 / Quantile–Quantile plot)
- 무엇을 측정/검증하나: 모델·관측 분포의 분위수를 서로 대응시켜 분포 형상·특히 극치 꼬리(고파고)의 일치를 진단. 평균 지표가 못 잡는 분포 편향 포착.
- 정의·수식: 정렬된 모델 분위수 q_m(p) vs 관측 분위수 q_o(p)를 (p=1..99%) 산점. 1:1선과의 이탈로 판정.
- 적용 도메인/자료형: Hs·Tp 분포 전반, 특히 고파고 영역. [격자]/[시계열]/[트랙].
- 입력·전제: 동일 기간 표본. 시간 정렬 불필요(분포 비교)지만 동일 모집단 가정.
- 해석 기준: 상위 분위수에서 1:1선 아래로 휘면 모델이 극치 과소추정(파랑모델 흔한 약점). QQ 기반 quantile mapping 보정에도 사용.
- 한계·주의: 분포만 비교 → 동시 일치(상관)는 못 봄. 표본 적은 극단 분위수는 불안정.
- 출처: Wilks (교과서); Jolliffe & Stephenson; 파랑 검증 다수 논문 관행.

---

### ★ Taylor 다이어그램 (Taylor diagram)
- 무엇을 측정/검증하나: 상관계수 R, 정규화 표준편차, 중심화 RMSD(CRMSD)를 단일 극좌표에 동시 표현해 여러 모델/지점을 한눈에 비교.
- 정의·수식: 반경 = σ_model/σ_obs, 방위각 = arccos(R), 관측점과의 거리 ∝ CRMSD. 코사인 법칙 CRMSD² = σ_m² + σ_o² − 2σ_mσ_oR 이용.
- 적용 도메인/자료형: Hs·Tp·풍속 등 다지점·다모델 요약. [시계열]/[격자].
- 입력·전제: 정렬된 쌍, 정규화 σ.
- 해석 기준: 관측점(R=1, σ비=1)에 가까울수록 우수.
- 한계·주의: bias는 표현 못 함(중심화) → Target diagram·bias 표 병행 필요.
- 출처: Taylor (2001, JGR 106(D7)); Taylor (2005, *Taylor Diagram Primer*, PCMDI/LLNL).

---

### 목표 다이어그램 (Target diagram)
- 무엇을 측정/검증하나: Bias(부호 포함)와 CRMSD(부호 포함)를 2D 평면에 그려 계통오차 대 무작위오차를 분해 시각화. Taylor가 못 보는 bias를 보완.
- 정의·수식: x축 = ±CRMSD(부호=σ_m−σ_o 부호), y축 = bias. 원점으로부터 거리 = RMSE.
- 적용 도메인/자료형: 다지점 Hs/Tp 종합 진단. [시계열]/[격자].
- 입력·전제: 정규화(관측 σ로 나눔) 권장.
- 해석 기준: 원점에 가까울수록 양호. y축 위/아래로 과대/과소 즉시 판별.
- 한계·주의: 상관은 직접 안 보임(Taylor와 짝).
- 출처: Jolliff et al. (2009, *Journal of Marine Systems* 76:64–82, "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment").

---

### 1D 주파수 스펙트럼 비교 (frequency spectrum, E(f))
- 무엇을 측정/검증하나: 벌크 파라미터를 넘어 에너지의 주파수 분포 형상까지 일치하는지(저주파 swell 봉 vs 고주파 windsea 봉).
- 정의·수식: 모델 E_m(f) vs 부이 E_o(f) 비교. 지표: 주파수별 bias, log-spectral distance = √mean[(log E_m − log E_o)²](꼬리 강조), 봉우리 주파수/에너지 오차. JONSWAP/Pierson–Moskowitz 형상 적합으로 파라미터(α, γ, fp) 비교도 가능.
- 적용 도메인/자료형: 부이 1D 스펙트럼(흔히 공개), 모델 적분 스펙트럼. [스펙트럼].
- 입력·전제: 동일 주파수 격자로 보간, 동일 정규화. 부이 고주파 절단(cutoff) 일치.
- 해석 기준: 봉우리 위치·에너지 일치, 저주파 swell 에너지 과소/과대 여부. log 스케일이 꼬리 오차를 드러냄.
- 한계·주의: 부이 스펙트럼 자체 노이즈·신뢰구간(자유도). 고주파 tail은 부이/모델 모두 불확실.
- 출처: WMO Guide No. 702; Pierson & Moskowitz (1964, JGR); Hasselmann et al. (1973, JONSWAP report, *Dtsch. Hydrogr. Z.* 부록 A8).

---

### 2D 방향 스펙트럼 비교 (directional spectrum, E(f,θ))
- 무엇을 측정/검증하나: 주파수-방향 2차원 에너지 분포 전체의 일치(다중 swell 시스템 방향까지).
- 정의·수식: E_m(f,θ) vs E_o(f,θ). 부이는 a1,b1,a2,b2로부터 MEM/MLM으로 재구성. 비교: 2D 상관, RMS 차, 분할(partition)별 일치.
- 적용 도메인/자료형: 모델 2D 스펙트럼 출력 vs 부이/HF radar/SAR 방향 스펙트럼. [스펙트럼].
- 입력·전제: 동일 (f,θ) 격자. 부이 방향 추정법(MEM/MLM) 명시 — 결과가 추정법에 의존.
- 해석 기준: 분할 후 각 시스템의 Hs·Tp·Dir 매칭으로 정량화(아래 partition 카드).
- 한계·주의: 부이 2D 재구성은 4 Fourier 계수의 역문제(under-determined → 인공 봉우리 가능). 위성 SAR은 180° 방향 모호성·고주파 cutoff.
- 출처: Hanson & Jensen (2007, JTECH 24(3)); Lygre & Krogstad (1986, JPO, MEM); Kuik et al. (1988, JPO).

---

### 스펙트럼 모멘트 비교 (Spectral moments, mₙ)
- 무엇을 측정/검증하나: 스펙트럼 모멘트 mₙ = ∫ fⁿ S(f) df 자체와 그로부터 유도되는 적분 파라미터(Hm0, Tm01, Tm02, 파랑 steepness 등)를 모델·관측 간 일관 비교. 벌크 파라미터 검증의 공통 토대.
- 정의·수식: m0=∫S df, m1=∫f·S df, m2=∫f²·S df. Hm0=4√m0, Tm01=m0/m1, Tm02=√(m0/m2). 평균 파장·평균파주기·평균제곱경사(mean square slope)도 고차 모멘트로 정의.
- 적용 도메인/자료형: 부이·모델·재분석 [스펙트럼] → 적분 파라미터 [시계열]/[격자].
- 입력·전제: **적분 주파수 구간·고주파 cutoff·tail 외삽 규약을 모델·관측 간 동일하게** 맞춰야 함(가장 흔한 불일치원). 부이 저주파 noise 제거.
- 해석 기준: 모멘트 차수가 높을수록(고주파 강조) 불확실성 증가 → m0·m1은 안정, m2 이상은 cutoff 민감. Hs(m0)부터 검증하고 단계적으로 고차로.
- 한계·주의: 동일 적분구간 미통일 시 bias가 인위적으로 발생. tail 외삽(f^−4 / f^−5) 방식 차이 주의.
- 출처: WMO Guide No. 702; Holthuijsen, *Waves in Oceanic and Coastal Waters* (Cambridge, 2007, 모멘트·파라미터 정의 — 표준 교과서, 확인요).

---

### 스펙트럼 분할 / windsea·swell 분리 (Spectral partitioning, watershed / Hanson–Phillips)
- 무엇을 측정/검증하나: 스펙트럼을 개별 파랑 시스템(windsea + 다중 swell)으로 분리한 뒤 시스템별로 검증 → multimodal sea에서 벌크 검증의 한계 극복.
- 정의·수식: 역(inverted) 스펙트럼에 watershed 알고리즘(Hasselmann et al. 1996; Hanson & Phillips 2001) 적용해 봉우리별 영역 분할. 각 partition의 Hs_i, Tp_i, Dir_i 산출. windsea/swell 판별은 wave age(파령) 또는 1차원 임계.
- 적용 도메인/자료형: 모델·부이·위성 1D/2D 스펙트럼. WW3에 내장(ww3_outp partition). [스펙트럼].
- 입력·전제: 전체 2D(또는 1D) 스펙트럼, 풍속(windsea 판별용). 디지털 필터로 노이즈 봉우리 제거 권장.
- 해석 기준: windsea Hs와 swell Hs를 따로 검증; swell 도달시각·방향 오차 진단. partition 매칭으로 cross-assignment 처리.
- 한계·주의: 임계/파라미터에 민감(자동화 난점). partition 개수·매칭 규칙이 결과 좌우. 1D는 방향 정보 손실.
- 출처: Hanson & Phillips (2001, JTECH 18(2):277–293, "Automated Analysis of Ocean Surface Directional Wave Spectra"); Hanson et al. (2009, JTECH 26(8), "Pacific Hindcast Performance of Three Numerical Wave Models"); Portilla, Ocampo-Torres & Monbaliu (2009, JTECH 26(1):107–122).

---

### ★ 극치파고 분석 (Extreme value analysis: POT-GPD / 연최대-GEV / 재현주기)
- 무엇을 측정/검증하나: 모델이 극단 파고(폭풍 파고)와 재현주기(return period) 설계파고를 관측과 일치시키는지. 설계·위험 평가의 핵심.
- 정의·수식: (1) 연최대(AM) → GEV 적합. (2) 임계초과(POT) → 독립 폭풍 첨두에 GPD(일반파레토) 적합, 평균초과율 λ와 결합해 N년 재현값 산출. 임계는 보통 91~99 퍼센타일 또는 평균잔여수명(MRL) 도표로 결정.
- 적용 도메인/자료형: 장기 모델 hindcast vs 장기 부이/고도계 [시계열]/[트랙].
- 입력·전제: 충분히 긴 동질 기간(가능하면 ≥20년). 폭풍 첨두의 독립성(declustering) 확보. 비정상성(기후변화/계절) 고려.
- 해석 기준: 재현주기별 Hs(예: 50년·100년) 모델-관측 신뢰구간 겹침 여부. QQ로 꼬리 적합 점검. 모델은 극치 과소 경향이 흔함.
- 한계·주의: 임계 선택·declustering·표본수에 큰 민감도(불확실성 큼). 모델 시간해상도·물리(ST4/ST6)가 극치 좌우. 신뢰구간(부트스트랩) 동반 필수.
- 출처: Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Caires & Sterl (2005, *Journal of Climate*, ERA-40 100-year return value).

---

### ★ 위성 고도계 대조 (Altimeter collocation: super-obs, 시공간 매치업)
- 무엇을 측정/검증하나: 고도계 SWH 트랙으로 모델을 광역 검증(부이 없는 외해 포함). 부이↔고도계 교차검증으로 고도계 보정도.
- 정의·수식: 1Hz(~7km) 고도계 자료를 super-observation(예: 수~수십 km 평균)으로 묶어 노이즈 저감 후 모델 격자에 시공간 콜로케이션. 통상 임계: 공간 ≤ 0.5~0.75°, 시간 ≤ 30~60분. bias/RMSE/SI 산출.
- 적용 도메인/자료형: 위성 [트랙](Jason, Sentinel-3/6, SARAL, CryoSat, HY-2 등) vs 모델 [격자]·부이.
- 입력·전제: 고도계 SWH 사전 보정·QC(rain/ice/coastal flag 제거). 연안 ≤ ~50km는 land/footprint 오염 주의. 미션 간 cross-calibration.
- 해석 기준: 외해 SWH SI 보통 5~10%(고도계-부이), bias 수 cm~0.15 m. 연안에서 SI 급증.
- 한계·주의: 고도계는 SWH·풍속만(주기·방향 없음). 트랙 sparse → 동시 다지점 불가. 대표성 오차(점 부이 vs ~km 평균).
- 출처: Janssen, Hansen & Bidlot (1997, Weather and Forecasting 12(4)); HY-2B 검증 (MDPI *Remote Sensing*, doi:10.3390/rs17233829); "Impact of altimeter-buoy data-pairing methods on the validation of Sentinel-3A coastal significant wave heights" (*Remote Sensing of Environment*, 2024, Elsevier).

---

### ★ 삼중 콜로케이션 (Triple Collocation, TC / Extended TC, ETC)
- 무엇을 측정/검증하나: 절대 기준(truth) 없이 세 독립 자료(예: 모델·부이·고도계) 각각의 무작위 오차분산과 상대 보정계수를 추정. "어느 자료가 더 정확한가"를 객관 산출.
- 정의·수식: 각 자료 xᵢ = αᵢ + βᵢ·T + εᵢ 모형. 세 자료의 공분산 관계로 βᵢ, var(εᵢ) 해석적 추정. ETC는 추가로 각 자료의 진값 대비 상관계수(신호 대 잡음)까지 산출.
- 적용 도메인/자료형: 모델·부이·고도계(또는 2위성) Hs. [격자]+[시계열]+[트랙].
- 입력·전제: 세 자료의 오차가 서로 독립·진값과 무상관, 공통 동적영역. 충분한 공통 콜로케이션 수.
- 해석 기준: 보고: 각 시스템 RMSE·scaling. 부이가 흔히 최소 오차 기준으로 나옴.
- 한계·주의: 오차 독립 가정 위배(예: 모델과 ERA5가 같은 바람 강제력 공유 → 상관) 시 편향. 표본·콜로케이션 윈도우에 민감.
- 출처: Stoffelen (1998, JGR, "Toward the true near-surface wind speed: ... triple collocation"); Caires & Sterl (2003, JGR Oceans 108(C3), doi:10.1029/2002JC001491, "Validation of ocean wind and wave data using triple collocation"); McColl et al. (2014, GRL 41(17):6229–6236, doi:10.1002/2014GL061322, Extended TC).

---

### ★ 확률밀도·누적분포 비교 (PDF/CDF, Kolmogorov–Smirnov)
- 무엇을 측정/검증하나: 모델·관측 Hs(또는 Tp) 분포 전체의 동질성. 분포 형상·왜도·꼬리.
- 정의·수식: PDF/CDF 중첩 도표; KS 통계량 D = max|F_m(x) − F_o(x)|. Hs는 종종 Weibull/Rayleigh로 적합 비교.
- 적용 도메인/자료형: 장기 통계(기후) 검증. 시간정렬 불필요. [격자]/[시계열]/[트랙].
- 입력·전제: 동일 기간·동일 모집단 가정. 표본 독립성(자기상관 보정).
- 해석 기준: KS p값으로 분포 차이 유의성. QQ와 상보적.
- 한계·주의: 자기상관 강한 시계열은 유효표본수 과대 → KS 과민(거의 항상 "유의" 판정). 분포만 보고 동시성은 못 봄.
- 출처: Wilks (교과서); Jolliffe & Stephenson.

---

### 범주형 / 임계 초과 검증 (Categorical / threshold: POD·FAR·CSI)
- 무엇을 측정/검증하나: "Hs가 경보 임계(예: 3 m, 4 m)를 넘었는가"라는 이진 사건을 모델이 맞히는지. 연속 오차지표가 못 주는 운영 경보 관점의 적중/오경보를 평가.
- 정의·수식: 2×2 분할표(hit a, false alarm b, miss c, correct-negative d)에서 POD=a/(a+c), FAR=b/(a+b), CSI(=TS)=a/(a+b+c), Bias score=(a+b)/(a+c), HSS/ETS(우연 보정). 임계는 위험관리 기준(고파주의보 등)으로 설정.
- 적용 도메인/자료형: Hs 임계 경보. [시계열]/[격자].
- 입력·전제: 정렬된 매치업 + 합의된 임계값. 표본 충분(특히 드문 고파고 사건).
- 해석 기준: POD↑·FAR↓·CSI↑ 양호. 임계가 높을수록 사건 희소 → 점수 불안정(신뢰구간 동반).
- 한계·주의: 단일 임계는 정보 손실 → 여러 임계·ROC(아래)와 병행. 격자 검증은 double-penalty(위치 약간 어긋나면 hit+false 둘 다) 주의.
- 출처: Jolliffe & Stephenson, *Forecast Verification* (범주형 점수 표준); Wilks (교과서).

---

### 확률예보 검증 (CRPS / Brier Score / ROC — 앙상블 파랑예보)
- 무엇을 측정/검증하나: 앙상블 파랑예보(예: ECMWF-ENS 파랑)의 확률적 신뢰도(reliability)·해상도(resolution)·예리함(sharpness). 단일 결정론 지표로는 못 보는 불확실성 표현의 품질.
- 정의·수식: CRPS = ∫[F_fcst(x) − 1{x≥obs}]² dx (작을수록 좋음; 결정론이면 MAE로 환원). Brier Score BS = mean[(p_fcst − o)²] (특정 임계 초과확률의 정확도; o∈{0,1}). ROC: 임계별 POD 대 POFD 곡선, 면적 AUC로 판별력. Rank histogram(Talagrand)으로 앙상블 spread 적정성.
- 적용 도메인/자료형: 앙상블 Hs(또는 임계 초과확률) vs 부이/고도계. [시계열]/[트랙].
- 입력·전제: 앙상블 멤버 전체 또는 예보 분포. 관측은 결정론 진값. 충분한 사례·임계.
- 해석 기준: CRPS·BS는 작을수록, CRPSS·BSS(기준대비 skill score)는 >0이면 기준예보보다 우수. ROC AUC>0.5 판별력 있음. Rank histogram 평탄=잘 보정, U자=과소분산, ∩자=과대분산.
- 한계·주의: 결정론 단일 모델에는 적용 불가(앙상블 전용). 희소 극단사건에서 BS/ROC 불안정.
- 출처: Hersbach (2000, *Weather and Forecasting* 15(5):559–570, "Decomposition of the CRPS for Ensemble Prediction Systems"); Jolliffe & Stephenson (Brier·ROC 표준); Wilks (교과서).

---

### ★ 재분석 격자-격자 공간비교 (Gridded reanalysis map difference: ERA5 등)
- 무엇을 측정/검증하나: 우리 모델 [격자]를 ERA5(또는 WAVERYS 등 파랑 재분석) [격자]와 **공간 전면적으로** 비교해 bias/RMSE/상관의 지리적 분포를 지도화. 점 관측이 없는 해역까지 패턴·계통오차 위치를 진단.
- 정의·수식: 공통 격자로 재격자화(conservative/bilinear regridding) 후 각 격자점 시간계열에 bias(x,y), RMSE(x,y), R(x,y), SI(x,y) 산출 → 등치선/색지도. 영역 평균·위도대 평균도 병행.
- 적용 도메인/자료형: Hs·Tm·Dir·풍속 [격자] vs [격자]. NetCDF↔NetCDF.
- 입력·전제: **시간축·격자 정의 정렬**(좌표·달력·시간대), 단위 일치, 마스크(육지/해빙) 통일. 재격자화 시 보존성(특히 Hs는 비선형)·해안선 처리 주의. ERA5는 ~0.5°(파랑) → 연안 표현 한계.
- 해석 기준: 지도에서 계통 bias 띠(예: 폭풍대 과소, 연안 과대)의 위치·계절성 파악. 재분석은 "절대 진실"이 아님(자체 오차·동화 한계) → 부이/고도계 검증과 교차해석.
- 한계·주의: 재분석은 독립 진값이 아니라 또 하나의 모델 산출 → "정답"으로 과신 금지. 격자 해상도·물리 차이가 차이의 상당부분을 만들 수 있음. 콜로케이션 대표성 오차 대신 격자 representativeness 차이 존재.
- 출처: Hersbach et al. (2020, *QJRMS*, "The ERA5 global reanalysis" — ERA5 자료 출처); WMO LC-WFV 절차(매치업·집계 관행). (GLORYS는 물리 해양 재분석으로 파랑변수 직접 미제공 — 파랑 대조군으로는 ERA5/WAVERYS 사용. 확인요)

---

### ★ 운영 검증 프레임워크 (WMO-JCOMM / ECMWF LC-WFV 표준 절차)
- 무엇을 측정/검증하나: 전 지구 운영 파랑모델들을 공통 부이·고도계 매치업으로 표준화 검증·상호비교하는 기관 절차(검증의 "표준화" 자체).
- 정의·수식: 표준 파라미터(Hs, Tp/Tm, 풍속)에 bias·RMSE·SI·R·산점도. 시간 매칭은 검증시각 중심 윈도우 평균, 공간은 역거리가중(IDWI) 보간. 월별/예보선행시간별 집계.
- 적용 도메인/자료형: 운영 모델 [격자] vs 공유 부이망·[트랙] 고도계.
- 입력·전제: 공통 QC된 부이 목록, 동일 매치업 규약, 미션 보정 고도계.
- 해석 기준: 기관 간 동일 기준으로 모델 순위·시간추세(연도별 개선) 평가. ECMWF는 20여 년 검증 추세 발표.
- 한계·주의: 부이 분포 편중(북반구 외해 위주). 연안·남반구 표본 부족. 규약 차이가 비교 왜곡.
- 출처: Bidlot et al. (2002, Weather and Forecasting, 운영 검증·SI); Bidlot (ECMWF Newsletter No. 150, "Twenty-one years of wave forecast verification"); WMO LC-WFV (community.wmo.int/Marine/WFV; confluence.ecmwf.int/display/WLW).

---

## 출처 (References)

### 표준 참고문헌 / 교과서·지침 (실제 존재)
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (bias·RMSE·MAE·KS·회귀 등 표준 정의).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, Wiley (범주형·확률·ROC·Brier).
- WMO, *Guide to Wave Analysis and Forecasting* (WMO-No. 702) — 스펙트럼·주기·파향·모멘트 정의 및 검증 관행.
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD, POT).
- Holthuijsen, L. H. (2007) *Waves in Oceanic and Coastal Waters*, Cambridge University Press (스펙트럼 모멘트·파라미터 정의 — 확인요).
- The WAVEWATCH III Development Group (2016) *User Manual and System Documentation of WAVEWATCH III* (partition·출력).

### 학술 논문 (웹으로 제목·저널·연도 확인됨; 권·페이지는 본문에 병기)
- Taylor, K. E. (2001) "Summarizing multiple aspects of model performance in a single diagram," *Journal of Geophysical Research*, 106(D7), 7183–7192. (Taylor diagram)
- Taylor, K. E. (2005) *Taylor Diagram Primer*, PCMDI/LLNL (기술노트).
- Willmott, C. J. (1981) "On the validation of models," *Physical Geography*, 2(2), 184–194. (Index of agreement)
- Willmott, C. J., Robeson, S. M. & Matsuura, K. (2012) "A refined index of model performance," *International Journal of Climatology*, 32. (dr 지표)
- Nash, J. E. & Sutcliffe, J. V. (1970) "River flow forecasting through conceptual models part I — A discussion of principles," *Journal of Hydrology*, 10(3). (NSE)
- Kuik, A. J., van Vledder, G. Ph. & Holthuijsen, L. H. (1988) "A method for the routine analysis of pitch-and-roll buoy wave data," *Journal of Physical Oceanography*, 18(7). (방향 파라미터·spread)
- Lygre, A. & Krogstad, H. E. (1986) "Maximum entropy estimation of the directional distribution in ocean wave spectra," *Journal of Physical Oceanography*, 16(12). (MEM)
- Hanson, J. L. & Phillips, O. M. (2001) "Automated analysis of ocean surface directional wave spectra," *Journal of Atmospheric and Oceanic Technology*, 18(2), 277–293. (watershed partitioning)
- Hanson, J. L., Tracy, B. A., Tolman, H. L. & Scott, R. D. (2009) "Pacific hindcast performance of three numerical wave models," *Journal of Atmospheric and Oceanic Technology*, 26(8). (HH 지표·partition 검증)
- Hanson, J. L. & Jensen, R. E. (2007) "Directional validation of wave predictions," *Journal of Atmospheric and Oceanic Technology*, 24(3). (방향 검증)
- Portilla, J., Ocampo-Torres, F. J. & Monbaliu, J. (2009) "Spectral partitioning and identification of wind sea and swell," *Journal of Atmospheric and Oceanic Technology*, 26(1), 107–122. (doi:10.1175/2008JTECHO609.1)
- Bowers, J. A., Morton, I. D. & Mould, G. I. (2000) "Directional statistics of the wind and waves," *Applied Ocean Research*, 22(1), 13–30. (파향 원형통계)
- Bidlot, J.-R., Holmes, D. J., Wittmann, P. A., Lalbeharry, R. & Chen, H. S. (2002) "Intercomparison of the performance of operational ocean wave forecasting systems with buoy data," *Weather and Forecasting*. (운영 검증·SI)
- Janssen, P. A. E. M., Hansen, B. & Bidlot, J.-R. (1997) "Verification of the ECMWF wave forecasting system against buoy and altimeter data," *Weather and Forecasting*, 12(4), 763–784.
- Caires, S. & Sterl, A. (2003) "Validation of ocean wind and wave data using triple collocation," *Journal of Geophysical Research: Oceans*, 108(C3), 3098. (doi:10.1029/2002JC001491) (TC)
- Caires, S. & Sterl, A. (2005) "100-year return value estimates for ocean wind speed and significant wave height from the ERA-40 data," *Journal of Climate*, 18. (극치)
- Stoffelen, A. (1998) "Toward the true near-surface wind speed: Error modeling and calibration using triple collocation," *Journal of Geophysical Research*, 103(C4). (TC 기초)
- McColl, K. A., Vogelzang, J., Konings, A. G., Entekhabi, D., Piles, M. & Stoffelen, A. (2014) "Extended triple collocation: Estimating errors and correlation coefficients with respect to an unknown target," *Geophysical Research Letters*, 41(17), 6229–6236. (doi:10.1002/2014GL061322) (ETC)
- Mentaschi, L., Besio, G., Cassola, F. & Mazzino, A. (2013) "Problems in RMSE-based wave model validations," *Ocean Modelling*, 72, 53–58. (RMSE·SI·HH 지표 비교)
- Jolliff, J. K., Kindle, J. C., Shulman, I., Penta, B., Friedrichs, M. A. M., Helber, R. & Arnone, R. A. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment," *Journal of Marine Systems*, 76, 64–82. (Target diagram)
- Pierson, W. J. & Moskowitz, L. (1964) "A proposed spectral form for fully developed wind seas based on the similarity theory of S. A. Kitaigorodskii," *Journal of Geophysical Research*, 69(24). (PM 스펙트럼)
- Hasselmann, K. et al. (1973) "Measurements of wind-wave growth and swell decay during the Joint North Sea Wave Project (JONSWAP)," *Deutsche Hydrographische Zeitschrift*, Suppl. A8, No. 12. (JONSWAP 스펙트럼)
- Hersbach, H. (2000) "Decomposition of the continuous ranked probability score for ensemble prediction systems," *Weather and Forecasting*, 15(5), 559–570. (CRPS)
- Hersbach, H. et al. (2020) "The ERA5 global reanalysis," *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999–2049. (ERA5 자료 출처)
- Beckman, J. N. & Long, J. W. (2022) "Quantifying errors in wind and wave measurements from a compact, low-cost wave buoy," *Frontiers in Marine Science*, 9:966855. (doi:10.3389/fmars.2022.966855)

### 웹 자료 (조사 시 직접 참조)
- ECMWF / WMO Lead Centre for Wave Forecast Verification (LC-WFV), "Verification results" — Scatter Index 정의: https://confluence.ecmwf.int/display/WLW/Verification+results
- WMO Marine — Wave Forecast Verification: https://community.wmo.int/en/activity-areas/Marine/WFV
- Bidlot, J.-R. "Twenty-one years of wave forecast verification," *ECMWF Newsletter* No. 150: https://www.ecmwf.int/en/newsletter/150/meteorology/twenty-one-years-wave-forecast-verification
- "Representativeness Error Assessment and Multi-Method Scaling of HY-2B Altimeter Significant Wave Height," *Remote Sensing* (MDPI), doi:10.3390/rs17233829 — 고도계 콜로케이션·ETC·sea-state binned 진단. (출판연도 2025로 확인; 본문은 vol 17/issue 23/art 3829)
- "Impact of altimeter-buoy data-pairing methods on the validation of Sentinel-3A coastal significant wave heights," *Remote Sensing of Environment* (2024, Elsevier) — 연안 고도계-부이 매치업 방법론.

### 확인요 (웹에서 1차 확인 못 했거나 정정한 항목)
- ~~Bidlot & Holt (2006, JCOMM Tech. Report)~~ → 1차 확인 실패. 운영 검증 출처는 위 ECMWF Newsletter No.150 및 Bidlot et al.(2002)로 대체. JCOMM Tech. Report 인용 시 원문 번호 재확인 필요.
- Holthuijsen (2007) *Waves in Oceanic and Coastal Waters* — 스펙트럼 모멘트 정의의 표준 교과서로 통용되나 이 세션에서 웹 재확인은 안 함(확인요).
- GLORYS: CMEMS 물리 해양 재분석으로 **파랑(Hs/Tp/Dir) 변수는 직접 제공하지 않음**. 파랑 대조군으로는 ERA5 파랑 또는 CMEMS WAVERYS(파랑 재분석)를 사용해야 함 — 원 임무문의 "GLORYS 파랑 비교"는 변수 가용성 확인 필요(확인요).

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(여기서는 검색으로 확인된 제목·저널·연도·권을 기재, DOI 임의 생성 금지 원칙 준수). DOI를 명시한 항목은 이 세션에서 웹으로 확인된 것.
