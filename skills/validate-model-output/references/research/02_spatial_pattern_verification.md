# 공간장 패턴 검증 (Spatial / Field Verification)

수치모델이 산출한 격자장(NetCDF grid)을 ERA5/GLORYS 같은 재분석자료나 위성 격자장, 또는 관측 기반 격자장(예: 레이더 강수, 격자화 분석장)과 **격자장 대 격자장(grid-to-grid)**으로 비교할 때 쓰는 검증 방법을 망라한다. 전통적 격자별 오차(point-by-point)는 패턴이 조금만 어긋나도 "이중벌점(double penalty)"으로 과도하게 나쁘게 평가하므로, 공간 패턴·구조·위치·스케일을 따로 보는 방법이 발전했다. Gilleland et al.(2009)은 이들을 크게 **이웃(neighborhood/fuzzy) · 스케일분리(scale-separation) · 특징기반(feature/object-based) · 장변형(field-deformation)** 네 범주로 정리했으며, 본 문서도 이 분류를 뼈대로 한다.

> **우리 작업 맥락(수치모델 vs ERA5/GLORYS/관측/위성)에서의 권장 사용 흐름**
> 1. **먼저 1차 진단**: 격자별 오차장(RMSE/MAE/Bias 지도)과 패턴상관/ACC, Taylor 다이어그램으로 "전체적으로 얼마나·어디서·어떤 식으로 어긋났나"를 본다.
> 2. **스케일 진단**: 파워스펙트럼(DCT)·웨이블릿(Intensity-Scale)·FSS·베리오그램으로 "어느 공간 스케일에서 모델이 평활·과잉인가"를 본다.
> 3. **위치/구조 진단**: 패치형(강수·에디·전선·고수온역) 변수면 SAL·MODE·CRA·이미지워핑·거리측도(Baddeley Δ)로 위치·구조 오차를 분리한다.
> 4. **모델 간 비교의 통계적 유의성**: 두 모델(또는 두 버전)을 견줄 때는 SPCT로 손실차의 유의성을 검정한다.
> 격자장은 NetCDF로, 시계열·점관측은 CSV로 들어온다고 가정한다. 시계열·점단위 지표(RMSE/MAE/상관/Taylor 등)는 본 문서의 격자판과 동일 정의를 점 표본에 적용하면 된다.

본 문서에 담은 방법(한 줄 목차):
- **격자별 오차장 (Grid-point error maps: RMSE/MAE/Bias 지도)** — 모든 공간검증의 출발점(이중벌점 한계 포함)
- **격자별 패턴상관 (Pattern correlation, ACC 포함)** — 공간 상관·이상장 상관계수(ACC)
- **Taylor 다이어그램 (Taylor diagram)** — 상관·표준편차비·중심화 RMSD를 한 그림에 요약
- **S1 스코어 (Teweles–Wobus gradient score)** — 기압장 등 경도(gradient) 일치도
- **이웃/퍼지 검증 (Neighborhood / fuzzy verification)** — 공간 완화 기반 다중 스케일 평가 틀
- **Fractions Skill Score (FSS)** — 이웃 분율 기반 스케일별 기술점수
- **MODE (Method for Object-based Diagnostic Evaluation)** — 객체 식별·매칭·속성 비교
- **SAL (Structure–Amplitude–Location)** — 구조·진폭·위치 3성분 품질측도
- **CRA (Contiguous Rain Area)** — 연속강수역 정합·오차분해
- **이미지 워핑 / 옵티컬 플로 (Image warping / optical flow)** — 변위장 추정·DAS
- **거리기반 이진영상 측도 (Baddeley Δ, Hausdorff, FoM 등)** — 이진 패턴 거리
- **Gβ 스코어 (Gilleland 2021)** — 거리·오버랩 기반 단일 요약 공간점수
- **구조적 유사도 (SSIM, Structural Similarity)** — 휘도·대비·구조 분해 유사도
- **웨이블릿 강도-스케일 검증 (Intensity-Scale, Casati 2004)** — 강도·스케일별 MSE 기술점수
- **공간 파워스펙트럼 비교 (Spatial power spectrum / DCT spectra)** — 스케일별 분산·에너지 비교
- **베리오그램 비교 (Variogram comparison)** — 2차 공간구조 통계 비교
- **공간예측 비교검정 (SPCT, Spatial Prediction Comparison Test)** — 두 모델 손실차의 통계적 유의성 검정

---

### 격자별 오차장 (Grid-point error maps / RMSE·MAE·Bias 지도)
- **무엇을 측정/검증하나**: 두 격자장을 **같은 격자점끼리** 직접 비교해 평균오차(Bias/ME), 평균제곱근오차(RMSE), 평균절대오차(MAE), 상관 등을 (a) 도메인 한 개의 요약 숫자로, (b) **격자별 오차 지도**로 산출. 모든 공간검증의 출발점이자 기준선(baseline).
- **정의·수식**:
  - 편의(Bias/ME): `ME = (1/N) Σ w_i (f_i − o_i)`
  - 평균제곱근오차(RMSE): `RMSE = sqrt[ (1/N) Σ w_i (f_i − o_i)² ]`
  - 평균절대오차(MAE): `MAE = (1/N) Σ w_i |f_i − o_i|`
  - 중심화 RMSD(CRMSD, 편의 제거): `CRMSD² = RMSE² − ME²`
  - `w_i`는 면적 가중(위경도 격자면 cosφ 가중 권장).
- **적용 도메인/자료형**: 격자장 대 격자장(모든 변수). 위성·재분석·관측 격자장 비교에 1차로 항상 쓴다.
- **입력·전제**: 동일 격자 정렬(또는 보존적/이중선형 보간), 결측 마스킹 일치, 단위·기준면(예: SSH 기준면, 기온 고도) 일치. 면적 가중 필요.
- **해석 기준**: RMSE·MAE는 작을수록, |Bias|는 0에 가까울수록 좋음(변수 단위·도메인에 의존하는 상대 기준). 오차 지도는 "어디서" 틀렸는지(연안·전선대·산악 등)를 직접 보여 준다.
- **한계·주의**: 패턴이 조금만 어긋나도 **이중벌점(double penalty)**으로 RMSE가 급증 — 고해상도·불연속 변수(강수·반사도)에서 특히 오도. 보간 방식이 결과를 바꾸므로 명시 필요. 이 한계가 아래 공간 패턴법들이 생긴 이유다.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (오차지표 정의); Jolliffe & Stephenson, *Forecast Verification* (이중벌점 논의); Stow et al. (2009) *Journal of Marine Systems* (해양모델 skill 지표 정리).

---

### 격자별 패턴상관 / 이상장 상관계수 (Pattern correlation & Anomaly Correlation Coefficient, ACC)
- **무엇을 측정/검증하나**: 두 격자장의 공간 패턴이 얼마나 닮았는가(상대적 분포의 일치). 일반 패턴상관은 원장(原場)끼리, ACC는 기후값을 뺀 **이상장(anomaly)**끼리 공간 상관을 본다. 평균 편의(bias)나 진폭 차이에는 둔감하고, 패턴·위상(phase) 오차에 민감하다.
- **정의·수식**:
  - 패턴상관: `r = Σ w_i (f_i − f̄)(o_i − ō) / sqrt[ Σ w_i (f_i − f̄)² · Σ w_i (o_i − ō)² ]`
  - ACC: `ACC = Σ w_i (f_i′ · o_i′) / sqrt[ Σ w_i (f_i′)² · Σ w_i (o_i′)² ]`, 여기서 `f_i′ = f_i − c_i`(예보 이상장), `o_i′ = o_i − c_i`(관측/분석 이상장), `c_i`는 기후값, `w_i`는 위도 가중(cosφ 등) 면적 가중치.
- **적용 도메인/자료형**: 격자장 대 격자장. 기상(지위고도·기온·기압), 해양(SST·SSH·해류 패턴), 파랑 등 광범위. ERA5/GLORYS와의 비교에 표준적으로 사용.
- **입력·전제**: 두 장이 동일 격자에 정렬(또는 보간)되어 있어야 함. ACC는 **동일 기후값(climatology)** 정의가 양쪽에 일관되게 적용되어야 함(같은 기준기간·같은 격자). 결측 마스킹 일치 필요.
- **해석 기준**: ACC=1 완전 일치, 0이면 무상관. 관행적으로 중규모(synoptic) 예보에서 **ACC ≥ 0.6**을 "유용한 예보"의 경계로, 0.5 부근을 예측가능성 한계로 본다(ECMWF 관행).
- **한계·주의**: 편의·진폭 오차를 보지 못하므로 RMSE 등과 병행해야 함. 기후값 선택에 민감. 강한 국지 패턴에 대한 평가가 둔감할 수 있음.
- **출처**: ECMWF Forecast User Guide §6.2.2 (Anomaly Correlation Coefficient); Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification* (패턴상관 일반).

---

### Taylor 다이어그램 (Taylor diagram)
- **무엇을 측정/검증하나**: 한 변수의 공간장(또는 시계열)에 대해 **공간 상관계수 R, 표준편차의 비(σ_f/σ_o), 중심화 RMS 차이(CRMSD)** 세 가지를 **하나의 극좌표 그림**에 동시에 요약. 여러 모델·여러 버전·여러 변수를 한 그림에서 ERA5/GLORYS(기준점) 대비 비교하기에 최적.
- **정의·수식**: 세 양은 코사인 법칙으로 한 평면 위에서 연결된다 — `CRMSD² = σ_f² + σ_o² − 2 σ_f σ_o R`. 반경 = 표준편차, 방위각 = `arccos(R)`, 기준점(관측)으로부터의 거리 = CRMSD. 보통 `σ_f/σ_o`로 정규화해 무차원 다이어그램을 그린다.
- **적용 도메인/자료형**: 격자장·시계열 모두. 기상·해양·파랑 등 임의 연속 변수. 여러 후보 모델/실험을 한 장에 올려 상대 순위를 본다.
- **입력·전제**: 공통 격자·동일 마스킹에서 σ, R, CRMSD를 계산. 면적 가중 권장. **편의(평균차)는 표현되지 않으므로** Bias는 별도 보고해야 함(다이어그램은 패턴·변동성만 요약).
- **해석 기준**: 기준점(관측, R=1·σ비=1)에 **가까운 점일수록 우수**. 상관이 높고(방위각 작음), 표준편차비가 1에 가깝고(반경이 관측과 같고), CRMSD가 작을수록 좋다. 점이 관측보다 반경이 작으면 변동성 과소(과평활), 크면 과대.
- **한계·주의**: 평균 편의·위치(위상) 오차를 직접 못 본다(상관과 변동성만). 비정규·희소 분포(강수)에서는 상관·표준편차가 왜곡될 수 있어 보조지표와 병행.
- **출처**: Taylor, K. E. (2001) "Summarizing multiple aspects of model performance in a single diagram", *Journal of Geophysical Research* 106(D7), 7183–7192.

---

### S1 스코어 (S1 / Teweles–Wobus gradient score)
- **무엇을 측정/검증하나**: 값 자체가 아니라 **공간 경도(gradient)**의 일치도. 기압·지위고도 같은 연속장의 "패턴 모양"을 평가하는 고전적 점수. 일기도(prognostic chart) 검증에서 출발.
- **정의·수식**: `S1 = 100 · Σ |ΔG_f − ΔG_o| / Σ max(|ΔG_f|, |ΔG_o|)`, 여기서 `ΔG`는 인접 격자 간 값 차(경도) 성분(보통 x·y 방향 모두 합산), 첨자 f=예보, o=관측/분석.
- **적용 도메인/자료형**: 격자장. 주로 기상(해면기압 SLP, 지위고도) 등 매끄러운 연속장. 매우 불연속적인 강수에는 부적합.
- **입력·전제**: 동일 격자 정렬. 경도 계산을 위해 인접성 정의 필요(격자 간격 일정 권장).
- **해석 기준**: **0이 완벽**(낮을수록 좋음). 역사적 관행상 S1 ≈ 0~20 매우 우수, 20~40 양호, 60 이상은 무가치에 가까움(기준은 변수·도메인 의존). 같은 변수·도메인 내 시계열 추세 비교에 유용.
- **한계·주의**: 도메인 크기·격자 해상도·변수에 따라 절대값 기준이 달라져 절대 비교가 어렵다. 진폭·편의는 직접 평가하지 못함.
- **출처**: Teweles, S. & Wobus, H. B. (1954) "Verification of Prognostic Charts", *Bulletin of the American Meteorological Society* 35(10), 455–463; Jolliffe & Stephenson, *Forecast Verification*.

---

### 이웃 / 퍼지 검증 (Neighborhood / fuzzy verification)
- **무엇을 측정/검증하나**: 격자 단위의 엄격한 일치 대신, **공간(및 시간) 이웃 안에서의 일치**를 허용해 작은 위치 오차에 대한 이중벌점을 완화. 여러 이웃 크기(스케일)와 임계값에서 일치도를 표로 제시해 "어떤 스케일부터 예보가 쓸 만한가"를 평가하는 **틀(framework)**.
- **정의·수식**: 각 격자 주변 반경 n(또는 한 변 길이의 정사각/원형 윈도) 안에서 사건(임계 초과) 분율을 계산하거나, 윈도 내 최댓값·존재여부 등으로 완화한 뒤 전통 점수(POD·FAR·MSE 등)를 계산. 대표 멤버가 FSS(아래 별도 카드).
- **적용 도메인/자료형**: 격자장. 고해상도 강수·반사도·구름 등 불연속·국지 변수에 특히 유용. 해양 전선·에디 위치 비교에도 응용 가능.
- **입력·전제**: 공통 격자. 이벤트 정의를 위한 임계값(들)과 이웃 크기(들) 지정. 관측·예보 동일 마스킹.
- **해석 기준**: 단일 임계값이 없고, "스케일 대 임계값" 표/그림에서 점수가 좋아지는 스케일을 본다. 보통 점수가 무기술(no-skill) 수준을 넘는 최소 이웃 크기를 "유용 스케일(skillful scale)"로 해석.
- **한계·주의**: 윈도 형태·크기 선택에 결과가 의존. 여러 점수를 산출하므로 해석에 주의 필요. 방법군이 다양해(상한·관용 등) 비교 시 동일 정의 명시 필요.
- **출처**: Ebert, E. E. (2008) "Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework", *Meteorological Applications* 15, 51–64; Gilleland et al. (2009) *Weather and Forecasting* 24.

---

### Fractions Skill Score (FSS, 분율 기술점수)
- **무엇을 측정/검증하나**: 임계값으로 이진화한 예보·관측을 여러 이웃 스케일에서 **분율(fraction)**로 바꾼 뒤, 그 분율들의 일치 정도를 MSE 기반으로 스케일별로 평가. 이중벌점을 공정하게 다루며 "예보가 유용해지는 공간 스케일"을 정량화.
- **정의·수식**: 임계값 초과 여부로 이진화 → 각 격자 이웃(크기 n)에서 예보분율 `P_f`, 관측분율 `P_o` 계산. `FBS = (1/N) Σ (P_f − P_o)²`, `FBS_worst = (1/N)[Σ P_f² + Σ P_o²]`, `FSS = 1 − FBS / FBS_worst`.
- **적용 도메인/자료형**: 격자장. 고해상도 정량강수(QPF)·반사도 검증의 사실상 표준. 앙상블 확장판(eFSS)도 존재.
- **입력·전제**: 공통 격자, 임계값(또는 분위수 기반), 일련의 이웃 크기. 결측 일관 처리.
- **해석 기준**: 0(무기술)~1(완벽). 관행적으로 **FSS ≥ 0.5**를 "유용(skillful)"의 목표선으로, 정확히는 `FSS_useful = 0.5 + f_o/2`(f_o = 도메인 관측 기저빈도)를 기준선으로 본다. 이웃이 커질수록 FSS는 단조 증가하므로 "기준선을 처음 넘는 스케일"이 유용 스케일.
- **한계·주의**: 임계값·기저빈도에 민감. 큰 이웃에서 항상 좋아지므로 단일 숫자가 아닌 스케일 곡선으로 해석. 매우 드문 사건에서는 불안정.
- **출처**: Roberts, N. M. & Lean, H. W. (2008) "Scale-Selective Verification of Rainfall Accumulations from High-Resolution Forecasts of Convective Events", *Monthly Weather Review* 136, 78–97; Mittermaier, M. P. (2021, *Monthly Weather Review* 149(10), FSS 극한·집계 분석); Necker, T. et al. (2024, *Quarterly Journal of the Royal Meteorological Society*, 앙상블 FSS 확장).

---

### MODE (Method for Object-based Diagnostic Evaluation, 객체기반 진단평가)
- **무엇을 측정/검증하나**: 장을 평활·임계화해 **객체(object/feature)**를 식별하고, 예보-관측 객체를 매칭한 뒤 면적·중심위치·축·종횡비·강도·교차면적 등 **속성 차이**로 진단. "무엇이 어떻게 틀렸는가"를 사람이 읽기 쉬운 형태로 제공.
- **정의·수식**: (1) 합성곱 평활(convolution) + 임계(threshold)로 객체화, (2) 객체 쌍의 **관심도(interest)**를 면적비·중심거리·교차도 등의 가중합 퍼지로직으로 계산해 매칭, (3) 매칭쌍·미매칭 객체 속성 통계 산출. 시간축 확장은 MODE-TD.
- **적용 도메인/자료형**: 격자장. 강수·반사도·구름영역 등 "덩어리"가 뚜렷한 변수에 적합. 해양에서는 에디·전선·고수온역 같은 패치 비교에 응용 가능.
- **입력·전제**: 공통 격자, 평활반경·임계값 등 객체화 파라미터, 매칭 가중치 설정. 결과가 파라미터에 민감하므로 설정 명시 필요.
- **해석 기준**: 단일 점수가 아니라 속성 분포(중심변위·면적비·강도차 등)로 진단. 중심거리↓·면적비≈1·교차도↑·매칭률↑이 좋음.
- **한계·주의**: 객체화 파라미터 의존성이 큼. 약한·확산적 장에서는 객체 정의가 모호. 결과 요약·집계 방식이 표준화 덜 됨.
- **출처**: Davis, C., Brown, B., Bullock, R. (2006) "Object-Based Verification of Precipitation Forecasts. Part I (방법론) & Part II (적용)", *Monthly Weather Review* 134, 1772–1784 & 1785–1795; NCAR MET(Model Evaluation Tools) MODE 도구 문서.

---

### SAL (Structure–Amplitude–Location, 구조·진폭·위치)
- **무엇을 측정/검증하나**: 한 도메인 단위로 예보-관측 강수장을 **구조(S)·진폭(A)·위치(L)** 세 성분으로 분해해 품질을 진단. 객체기반과 통계기반을 절충한 측도.
- **정의·수식**:
  - **A(Amplitude)**: 도메인 평균값의 상대편차, `A = (⟨f⟩ − ⟨o⟩) / [0.5(⟨f⟩ + ⟨o⟩)]`, 범위 −2~+2. 양수=과대.
  - **L(Location)**: (L1) 질량중심 변위 + (L2) 객체들의 가중평균 거리 오차를 합산, 범위 0~2. 0=완벽.
  - **S(Structure)**: 임계로 정의한 객체들의 정규화 부피(크기·평탄도) 분포 비교, 범위 −2~+2. 음수=너무 작고 뾰족, 양수=너무 크고 평탄.
- **적용 도메인/자료형**: 격자장, 도메인 단위(예: 유역·모델영역). 정량강수 검증이 주용도. 반사도·기타 패치형 변수로 확장 사례 있음.
- **입력·전제**: 공통 격자, 객체 정의 임계값(보통 도메인 최댓값의 비율 R*f 또는 고정값). 도메인 경계가 결과에 영향.
- **해석 기준**: 세 성분 모두 0에 가까울수록 우수. (S,A,L)을 산점/조합으로 보아 과대·과소·위치오차·구조오차를 동시 진단. 단일 점수 없음.
- **한계·주의**: 임계값·도메인 정의에 민감. 객체가 도메인 전체로 퍼지면 S·L 해석이 약해짐. 주기 도메인에서 질량중심이 불안정할 수 있음. 앙상블·반사도용 변형판 존재.
- **출처**: Wernli, H., Paulat, M., Hagen, M., Frei, C. (2008) "SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts", *Monthly Weather Review* 136, 4470–4487; Lawson, J. R. & Gallus, W. A. (2016, 반사도 적용, *Atmospheric Science Letters* 17).

---

### CRA (Contiguous Rain Area, 연속강수역)
- **무엇을 측정/검증하나**: 임계 초과 **연속영역(entity)**을 정의하고, 예보 객체를 관측 객체에 **평행이동(또는 패턴매칭)**으로 최적 정합시켜 총오차를 **위치(displacement)·부피/체적(volume)·패턴(pattern)** 성분으로 분해. 이동 거리로 위치오차를 정량화.
- **정의·수식**: 예보장을 상관 최대(또는 MSE 최소)가 되도록 시프트 → 그 변위가 위치오차. 시프트 후 잔여 MSE를 진폭/체적오차와 미세패턴오차로 분해: `MSE_total = MSE_displacement + MSE_volume + MSE_pattern`.
- **적용 도메인/자료형**: 격자장. 강수·태풍 강우역 등 잘 정의된 강수 시스템에 강점. 단일 시스템 비교에 적합.
- **입력·전제**: 공통 격자, 임계값으로 CRA 정의, 매칭 기준(상관/MSE) 선택. 객체가 도메인 경계를 넘지 않는 편이 좋음.
- **해석 기준**: 위치오차(km)·체적오차(%)·패턴오차 비중을 본다. 위치 성분이 크면 "위상 오차", 체적 성분이 크면 "양적 편의", 패턴 성분이 크면 "미세구조 오류"로 진단.
- **한계·주의**: 평행이동만으로 회전·변형은 못 잡음. 다수·중첩 시스템에서는 매칭이 모호. 임계값 민감.
- **출처**: Ebert, E. E. & McBride, J. L. (2000) "Verification of precipitation in weather systems: determination of systematic errors", *Journal of Hydrology* 239, 179–202; Ebert, E. E. & Gallus, W. A. (2009, *Weather and Forecasting* 24, CRA 거동 이해); Chen et al. (2018, 태풍 강우 적용, *Earth and Space Science* 5).

---

### 이미지 워핑 / 옵티컬 플로 (Image warping / optical flow, 장변형 검증)
- **무엇을 측정/검증하나**: 예보장을 연속적으로 **변형(warp)**해 관측장에 맞추는 변위벡터장을 추정하고, 그 결과를 **변위(위치)오차 + 잔여 진폭오차**로 분해. 위치오차와 강도오차를 명시적으로 분리해 진단.
- **정의·수식**: 변위장 W를 추정해 `f(x + W(x))`가 관측 `o(x)`에 가깝도록 최적화(피라미드/멀티스케일 매칭, 옵티컬 플로). Keil & Craig의 **DAS(Displacement and Amplitude Score)**는 변위 크기와 변형 후 강도차의 제곱을 결합: 대략 `DAS = (1/2)(DIS/DIS_max) + (1/2)(AMP/AMP_max)` 형태.
- **적용 도메인/자료형**: 격자장. 강수·반사도뿐 아니라 매끄러운 장(기압·SST·해류 패턴)의 위상오차 평가에 적합.
- **입력·전제**: 공통 격자, 변형의 매끄러움 정규화(과적합 방지) 설정, 최적화 알고리즘 파라미터. 큰 변위·새 객체(false alarm) 처리 방식 주의.
- **해석 기준**: 변위 성분이 작을수록 위치 일치 우수, 잔여 진폭 성분이 작을수록 강도 일치 우수. DAS는 0에 가까울수록 좋음.
- **한계·주의**: 큰 변위·미스매치 객체에서 부정확. 정규화 강도에 민감. 계산비용이 큼. 거짓경보 처리(초기 FQM의 한계를 DAS가 보완).
- **출처**: Keil, C. & Craig, G. C. (2009) "A displacement and amplitude score employing an optical flow technique", *Weather and Forecasting* 24, 1297–1308; Gilleland, E., Lindström, J., Lindgren, F. (2010) "Analyzing the Image Warp Forecast Verification Method on Precipitation Fields from the ICP", *Weather and Forecasting* 25; Marzban & Sandgathe (2010) "Optical Flow for Verification", *Weather and Forecasting* 25.

---

### 거리기반 이진영상 측도 (Distance measures: Baddeley Δ, Hausdorff, Pratt FoM 등)
- **무엇을 측정/검증하나**: 임계로 이진화한 예보·관측 **마스크(set) 간의 기하학적 거리**로 패턴 일치도를 평가. 위치·형태·범위 차이에 민감한 진짜 거리(metric) 계열.
- **정의·수식**:
  - **Hausdorff 거리**: 두 집합 A,B에 대해 `H(A,B) = max( sup_{a∈A} d(a,B), sup_{b∈B} d(b,A) )`. 변형(부분/수정 Hausdorff)으로 이상치 완화.
  - **Baddeley Δ**: 거리변환(distance transform) 값을 컷오프 함수 w로 변환해 평균한 측도, `Δ^p(A,B) = [ (1/N) Σ_x |w(d(x,A)) − w(d(x,B))|^p ]^{1/p}`. Hausdorff보다 작은 변화에 안정적.
  - **Pratt FoM(Figure of Merit)**, **MED(mean error distance)** 등 관련 계열.
- **적용 도메인/자료형**: 격자장(이진화 후). 강수역·구름역·해빙역(sea-ice edge)·전선 등 "있다/없다" 패턴 위치 비교.
- **입력·전제**: 공통 격자, 임계값으로 이진화, 거리변환. 빈 집합(한쪽에 사건 없음) 처리 규칙 필요.
- **해석 기준**: 값이 작을수록 두 패턴이 공간적으로 가깝다. 절대 기준은 변수·도메인 의존이므로 사례 간 상대 비교에 주로 사용.
- **한계·주의**: 임계값·격자해상도 의존. 한쪽이 비어있으면 정의 곤란. 강도정보는 직접 반영하지 않음(형태·위치 위주).
- **출처**: Baddeley, A. J. (1992) "Errors in binary images and an Lp version of the Hausdorff metric", *Nieuw Archief voor Wiskunde* 10, 157–183; Gilleland, E. (2011) "Spatial Forecast Verification: Baddeley's Delta Metric Applied to the ICP Test Cases", *Weather and Forecasting* 26, 409–415; SpatialVx 패키지 `locmeasures2d` 문서.

---

### Gβ 스코어 (Gilleland 2021, 단일 요약 공간점수)
- **무엇을 측정/검증하나**: 거리기반 측도를 **0~1로 정규화한 단일 요약 점수**로, 두 이진 패턴의 **오버랩 부족(거짓경보+미탐지 면적)**과 **평균오차거리(MED)**를 결합해 "위치+범위가 얼마나 맞나"를 한 숫자로 표현. 빈 집합(한쪽에 사건 없음)에도 정의되도록 설계되어 Baddeley Δ·Hausdorff의 실무적 약점을 보완. 강도성능까지 결합한 변형(Gβ,IL)도 있음.
- **정의·수식**: 비매칭 면적과 거리오차의 곱 형태 항 `y`를 도메인 의존 상수 β로 정규화: 대략 `Gβ = max(1 − y/β, 0)`. β는 사용자가 정하는 "허용 가능한 나쁨" 척도(보통 도메인 격자수²의 상수배). `y`는 두 방향 비매칭 화소수와 MED를 곱해 합산.
- **적용 도메인/자료형**: 격자장(이진화 후). 강수·구름·해빙·전선 등 패치형. 여러 사례·여러 모델을 단일 점수로 줄세우기 좋아 자동 파이프라인에 적합.
- **입력·전제**: 공통 격자, 임계값으로 이진화, β 설정(도메인 크기 기반). 결측 마스킹 일치.
- **해석 기준**: **1=완벽(완전 겹침), 0=완전 불일치(β 이상으로 나쁨)**. 높을수록 좋음. β 선택으로 "얼마나 엄격히 볼지"를 조절.
- **한계·주의**: β 값 선택이 결과 스케일을 좌우(명시 필요). 강도정보는 기본형에서 빠짐(Gβ,IL로 보완). 비교적 최신 지표라 임계 관행이 아직 정착 중.
- **출처**: Gilleland, E. (2021) "Novel measures for summarizing high-resolution forecast performance", *Advances in Statistical Climatology, Meteorology and Oceanography (ASCMO)* 7, 13–34; SpatialVx 패키지 `Gbeta` 함수 문서.

---

### 구조적 유사도 (SSIM, Structural Similarity Index)
- **무엇을 측정/검증하나**: 이미지 품질 평가에서 온 측도로, 두 장을 **휘도(luminance)·대비(contrast)·구조(structure)** 세 요소로 분해해 국소 윈도별 유사도를 계산. MSE/PSNR이 못 잡는 "구조적 닮음"을 평가.
- **정의·수식**: 국소 윈도에서 `SSIM(x,y) = [(2μ_xμ_y + C1)(2σ_xy + C2)] / [(μ_x² + μ_y² + C1)(σ_x² + σ_y² + C2)]`, μ=평균(휘도), σ=표준편차(대비), σ_xy=공분산(구조), C1·C2는 안정화 상수. 전체는 윈도 평균(MSSIM).
- **적용 도메인/자료형**: 격자장. 강수·반사도·위성영상·SST 등 영상형 격자장 비교. AI 기상예측(emulator) 평가에서 활용 증가.
- **입력·전제**: 공통 격자, 윈도 크기·상수 C 설정, 보통 값 범위(동적범위) 정규화. 결측 처리 필요.
- **해석 기준**: −1~1(또는 0~1). **1=완전 동일**, 0=구조 무상관. 1에 가까울수록 좋음. 절대 임계값은 응용·정규화 방식에 의존.
- **한계·주의**: 윈도·상수·동적범위 선택에 민감. 기상 변수의 물리적 의미와 직접 연결이 약해 보조지표로 권장. 강한 비정상·희소 패턴(강수)에서 해석 주의.
- **출처**: Wang, Z., Bovik, A. C., Sheikh, H. R., Simoncelli, E. P. (2004) "Image quality assessment: from error visibility to structural similarity", *IEEE Transactions on Image Processing* 13(4), 600–612; 기상·예측 응용은 최근 문헌(예: AI 모델 평가)에서 차용.

---

### 웨이블릿 강도-스케일 검증 (Intensity-Scale skill score, Casati 2004)
- **무엇을 측정/검증하나**: 예보-관측 오차를 **공간 스케일(웨이블릿 분해)**과 **강도(임계값)**의 함수로 분해해, 어느 스케일·어느 강도에서 오차가 발생하는지 진단. 스케일분리(scale-separation) 범주의 대표.
- **정의·수식**: 임계값으로 이진화한 예보·관측의 차(이진오차장)를 2D Haar 웨이블릿으로 다중해상도(MRA) 분해 → 각 스케일 l, 강도 u에서 MSE 성분 `MSE_{l,u}` 계산 → 무작위 예보 대비 기술점수 `ISS_{l,u} = 1 − MSE_{l,u}/MSE_random`.
- **적용 도메인/자료형**: 격자장(보통 2의 거듭제곱 크기). 정량강수 검증이 주용도. 웨이블릿 국소 스펙트럼으로 앙상블 검증 확장 사례.
- **입력·전제**: 공통 격자, 2^n 크기(패딩/타일링), 임계값 집합, 전처리(디더링·재보정). 결측·경계 처리.
- **해석 기준**: 스케일×강도 평면에서 `ISS > 0`이면 무작위보다 기술 있음, 0 이하이면 무기술. 어떤 스케일/강도 영역이 좋고 나쁜지를 한눈에 진단.
- **한계·주의**: 도메인 크기 제약(2의 거듭제곱), 임계·전처리 선택에 민감. Haar 웨이블릿의 블록경계 효과. 해석에 숙련 필요.
- **출처**: Casati, B., Ross, G., Stephenson, D. B. (2004) "A new intensity-scale approach for the verification of spatial precipitation forecasts", *Meteorological Applications* 11, 141–154; Casati (2010, 개정판); Weniger, Kapp, Friederichs (2017, 국소 웨이블릿 스펙트럼, *QJRMS*); Briggs & Levine (1997, 웨이블릿 검증 선구, *MWR* 125).

---

### 공간 파워스펙트럼 비교 (Spatial power spectrum / DCT spectra comparison)
- **무엇을 측정/검증하나**: 장의 **분산이 공간 스케일(파수, wavenumber)에 어떻게 분포**하는지를 예보와 관측에서 각각 계산해 비교. 모델이 소규모를 과도하게 평활(에너지 부족)했는지, 잡음으로 과대표현(에너지 과잉)했는지를 진단. 절대 위치 일치보다 **스케일별 활성도(activity)** 일치를 본다.
- **정의·수식**: 2D 푸리에 또는 **이산코사인변환(DCT, 비주기 한정영역에 적합)**으로 장을 변환 → 파수 k별 파워(분산) `E(k)`를 방위평균해 1D 스펙트럼화 → 예보·관측 스펙트럼의 기울기·교차 스케일·소규모 에너지비를 비교. 운동에너지 스펙트럼의 `k^(−5/3)` 거동 등과 대조.
- **적용 도메인/자료형**: 격자장. 강수·반사도·바람(KE 스펙트럼)·SSH·해류 등. 고해상도 모델의 "유효해상도(effective resolution)" 진단에 표준적.
- **입력·전제**: 공통 격자, 한정영역이면 DCT 권장(또는 윈도잉·디트렌드 후 FFT). 결측 보간, 추세 제거.
- **해석 기준**: 예보 스펙트럼이 소규모(고파수)에서 관측보다 낮으면 과도한 평활(블러), 높으면 잡음·격자노이즈. 스펙트럼이 갈라지는 파장이 모델의 유효해상도 지표. 리드타임이 길수록 소규모 에너지 손실 경향.
- **한계·주의**: 위치·위상 일치는 전혀 평가하지 못함(진폭 스펙트럼만). 경계·윈도 처리에 민감. 단독 사용보다 위치기반 측도와 병행.
- **출처**: Denis, B., Côté, J., Laprise, R. (2002) "Spectral Decomposition of Two-Dimensional Atmospheric Fields on Limited-Area Domains Using the Discrete Cosine Transform (DCT)", *Monthly Weather Review* 130, 1812–1829; Skamarock, W. C. (2004) "Evaluating Mesoscale NWP Models Using Kinetic Energy Spectra", *Monthly Weather Review* 132, 3019–3032 (유효해상도·KE 스펙트럼).

---

### 베리오그램 비교 (Variogram / structure-function comparison)
- **무엇을 측정/검증하나**: 거리 h만큼 떨어진 두 지점 값 차의 분산(반변량, semivariance)을 거리의 함수로 본 **베리오그램**을 예보·관측에서 각각 구해 비교. 장의 **공간 상관거리·변동성(거칠기)** 구조가 닮았는지를 평가(2차 공간통계 기반, 위치 무관).
- **정의·수식**: `γ(h) = (1/2N(h)) Σ_{(i,j): |x_i−x_j|≈h} [z_i − z_j]²`. 예보 `γ_f(h)`와 관측 `γ_o(h)` 곡선(또는 방향별 베리오그램)을 비교; 차이를 거리별로 요약.
- **적용 도메인/자료형**: 격자장(및 점관측). 강수·SST·SSH·바람장 등 연속·준연속 변수의 공간 텍스처 비교. 비등방(anisotropy) 진단 가능.
- **입력·전제**: 공통 격자 또는 동일 영역, 거리 빈 정의, 정상성(stationarity) 가정. 추세 제거 권장.
- **해석 기준**: 두 베리오그램의 모양(나깃/sill·상관거리/range)이 가까울수록 공간구조 일치. 예보가 관측보다 sill이 낮으면 변동성 과소(과평활), 높으면 과대.
- **한계·주의**: 위치 일치는 평가 못함(스펙트럼과 유사한 한계). 정상성 가정 위배 시 해석 주의. 거리 빈·이상치에 민감.
- **출처**: Marzban, C. & Sandgathe, S. (2009) "Three spatial verification techniques: cluster analysis, variogram, and optical flow", *Weather and Forecasting* 24, 1457–1471; 지구통계 표준 교과서(예: Cressie, *Statistics for Spatial Data*).

---

### 공간예측 비교검정 (SPCT, Spatial Prediction Comparison Test)
- **무엇을 측정/검증하나**: 두 경쟁 모델(또는 두 버전)이 같은 관측장에 대해 산출한 **격자별 손실차(loss differential) 장**이 통계적으로 유의하게 0과 다른지(=한 모델이 정말로 더 낫다고 할 수 있는지)를 검정. 점수 자체가 아니라 **"차이가 유의한가"**를 답하는 가설검정 도구. 시계열의 Diebold–Mariano 검정을 공간장으로 확장한 것.
- **정의·수식**: 손실차 장 `d(s) = L(f1(s),o(s)) − L(f2(s),o(s))`를 계산(L은 임의 손실: 제곱오차, 거리지도 손실, 이미지워프 손실 등) → 공간 상관을 고려해 평균 손실차의 분산을 추정 → 검정통계량으로 H0(두 모델 손실 동일) 검정.
- **적용 도메인/자료형**: 격자장. 임의 변수(강수처럼 비정규·0 다수인 장에도 적용 사례). 모델 인터컴페어리즌, 버전 업그레이드 검증에 직접 유용.
- **입력·전제**: 두 모델의 동일 격자·동일 관측, 손실함수 선택, 공간 상관 구조 추정(블록·반변량 기반). 표본(사례·시각)이 충분해야 검정력 확보.
- **해석 기준**: p-값이 유의수준 미만이면 "두 모델 성능 차이가 유의". 손실차 부호로 어느 쪽이 우수한지 판정. 손실로 거리지도·이미지워프를 쓰면 위치오차 관점의 유의성도 검정 가능.
- **한계·주의**: 공간 상관을 제대로 반영하지 않으면 유의성을 과대평가(독립 가정의 함정). 손실함수 선택이 결론을 바꿀 수 있어 명시 필요. 표본이 작으면 검정력 낮음.
- **출처**: Gilleland, E. (2013) "Testing Competing Precipitation Forecasts Accurately and Efficiently: The Spatial Prediction Comparison Test", *Monthly Weather Review* 141(1), 340–355; Gilleland (2015, *Meteorological Applications*, 검정 개선); SpatialVx 패키지 `spct` 함수 문서.

---

## 출처(References)

> 아래는 본문에서 인용한 실제 출처다. DOI는 임의 생성하지 않았으며, 검증 가능한 표준 문헌·동료심사 논문·공식 기관 문서만 수록했다. 본 갱신에서 핵심 논문(권·페이지)은 WebSearch로 학회 원문 페이지를 확인했다.

**검증 방법론 리뷰·교과서**
- Gilleland, E., Ahijevych, D., Brown, B. G., Casati, B., Ebert, E. E. (2009). "Intercomparison of Spatial Forecast Verification Methods." *Weather and Forecasting*, 24, 1416–1430. (공간검증 4범주 분류의 표준 리뷰)
- Jolliffe, I. T. & Stephenson, D. B. (eds.). *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, Wiley. (표준 참고문헌)
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press. (표준 참고문헌)
- Ebert, E. E. (2008). "Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework." *Meteorological Applications*, 15, 51–64.
- Stow, C. A. et al. (2009). "Skill assessment for coupled biological/physical models of marine systems." *Journal of Marine Systems*, 76, 4–15. (해양모델 skill 지표 정리 — 표준 참고문헌)
- WMO/WWRP–WGNE Joint Working Group on Forecast Verification Research; CAWCR Forecast Verification 페이지(https://www.cawcr.gov.au/projects/verification/). (표준 지침·용어 — 확인요: 페이지 URL은 기관 운영에 따라 변동 가능)

**개별 방법 원전**
- Teweles, S. & Wobus, H. B. (1954). "Verification of Prognostic Charts." *Bulletin of the American Meteorological Society*, 35(10), 455–463. (S1 score)
- ECMWF Forecast User Guide, Section 6.2.2 "Anomaly Correlation Coefficient." (ACC 정의·해석 기준)
- Taylor, K. E. (2001). "Summarizing multiple aspects of model performance in a single diagram." *Journal of Geophysical Research*, 106(D7), 7183–7192. (Taylor diagram)
- Roberts, N. M. & Lean, H. W. (2008). "Scale-Selective Verification of Rainfall Accumulations from High-Resolution Forecasts of Convective Events." *Monthly Weather Review*, 136, 78–97. (FSS)
- Mittermaier, M. P. (2021). "A 'Meta' Analysis of the Fractions Skill Score: The Limiting Case and Implications for Aggregation." *Monthly Weather Review*, 149(10), 3491–3504. (FSS 집계·극한)
- Necker, T., Wolfgruber, L., Kugler, L., Weissmann, M., Dorninger, M., Serafin, S. (2024). "The fractions skill score for ensemble forecast verification." *Quarterly Journal of the Royal Meteorological Society*. doi:10.1002/qj.4824. (앙상블 FSS)
- Davis, C., Brown, B., Bullock, R. (2006). "Object-Based Verification of Precipitation Forecasts. Part I: Methodology and Application to Mesoscale Rain Areas." *Monthly Weather Review*, 134, 1772–1784. / "Part II: Application to Convective Rain Systems." 134, 1785–1795. (MODE)
- Wernli, H., Paulat, M., Hagen, M., Frei, C. (2008). "SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts." *Monthly Weather Review*, 136, 4470–4487. (SAL)
- Lawson, J. R. & Gallus, W. A. (2016). "Adapting the SAL method to evaluate reflectivity forecasts of summer precipitation in the central United States." *Atmospheric Science Letters*, 17. (SAL 반사도 적용)
- Ebert, E. E. & McBride, J. L. (2000). "Verification of precipitation in weather systems: determination of systematic errors." *Journal of Hydrology*, 239, 179–202. (CRA)
- Ebert, E. E. & Gallus, W. A. (2009). "Toward Better Understanding of the Contiguous Rain Area (CRA) Method for Spatial Forecast Verification." *Weather and Forecasting*, 24. 
- Chen, J. et al. (2018). "Application of Contiguous Rain Area (CRA) Methods to Tropical Cyclone Rainfall Forecast Verification." *Earth and Space Science*, 5.
- Keil, C. & Craig, G. C. (2009). "A Displacement and Amplitude Score Employing an Optical Flow Technique." *Weather and Forecasting*, 24(5), 1297–1308. (DAS)
- Gilleland, E., Lindström, J., Lindgren, F. (2010). "Analyzing the Image Warp Forecast Verification Method on Precipitation Fields from the ICP." *Weather and Forecasting*, 25. (image warping)
- Marzban, C. & Sandgathe, S. (2010). "Optical Flow for Verification." *Weather and Forecasting*, 25(5), 1479–1494. (옵티컬 플로 검증)
- Baddeley, A. J. (1992). "Errors in binary images and an Lp version of the Hausdorff metric." *Nieuw Archief voor Wiskunde*, 10, 157–183. (Baddeley Δ 측도)
- Gilleland, E. (2011). "Spatial Forecast Verification: Baddeley's Delta Metric Applied to the ICP Test Cases." *Weather and Forecasting*, 26, 409–415.
- Gilleland, E. (2021). "Novel measures for summarizing high-resolution forecast performance." *Advances in Statistical Climatology, Meteorology and Oceanography (ASCMO)*, 7, 13–34. (Gβ score)
- Wang, Z., Bovik, A. C., Sheikh, H. R., Simoncelli, E. P. (2004). "Image Quality Assessment: From Error Visibility to Structural Similarity." *IEEE Transactions on Image Processing*, 13(4), 600–612. (SSIM)
- Casati, B., Ross, G., Stephenson, D. B. (2004). "A new intensity-scale approach for the verification of spatial precipitation forecasts." *Meteorological Applications*, 11, 141–154. (Intensity-Scale)
- Briggs, W. M. & Levine, R. A. (1997). "Wavelets and Field Forecast Verification." *Monthly Weather Review*, 125, 1329–1341. (웨이블릿 검증 선구)
- Weniger, M., Kapp, F., Friederichs, P. (2017). "Spatial verification using wavelet transforms: a review." *Quarterly Journal of the Royal Meteorological Society* / arXiv:1605.03395.
- Denis, B., Côté, J., Laprise, R. (2002). "Spectral Decomposition of Two-Dimensional Atmospheric Fields on Limited-Area Domains Using the Discrete Cosine Transform (DCT)." *Monthly Weather Review*, 130, 1812–1829. (공간 스펙트럼/DCT)
- Skamarock, W. C. (2004). "Evaluating Mesoscale NWP Models Using Kinetic Energy Spectra." *Monthly Weather Review*, 132, 3019–3032. (유효해상도·KE 스펙트럼)
- Marzban, C. & Sandgathe, S. (2009). "Three Spatial Verification Techniques: Cluster Analysis, Variogram, and Optical Flow." *Weather and Forecasting*, 24, 1457–1471. (variogram, optical flow)
- Gilleland, E. (2013). "Testing Competing Precipitation Forecasts Accurately and Efficiently: The Spatial Prediction Comparison Test." *Monthly Weather Review*, 141(1), 340–355. (SPCT)

**도구·소프트웨어 문서**
- NCAR Model Evaluation Tools (MET): MODE / Wavelet-Stat 문서(metplus.readthedocs.io).
- SpatialVx (R 패키지): `locmeasures2d`, `Gbeta`, `spct`, `SpatialVx-package` 문서(거리기반 측도·Gβ·SPCT 구현).
- ICP (Spatial Forecast Verification Methods Intercomparison Project) reference list, NCAR/RAL.
