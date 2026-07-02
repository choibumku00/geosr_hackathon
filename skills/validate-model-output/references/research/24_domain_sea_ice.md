# 도메인: 해빙·빙권 (Sea Ice / Cryosphere) 검증·분석 방법 카탈로그

이 문서는 해빙 모델(해빙-해양 결합모델 CICE/SI3/CESM-CICE, 예보시스템 TOPAZ/neXtSIM/PIOMAS, 재분석 ORAS5/GIOMAS 등)의 산출물을 위성 수동마이크로파(passive microwave: SSMIS·AMSR2)·고도계(CryoSat-2·ICESat-2)·SMOS 밝기온도·표류부이(IABP buoy)·잠수함/계류 초음파(ULS)·항공(OIB)·해빙도(ice chart, NIC/AARI)와 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 해빙 검증의 핵심은 (1) **해빙농도(SIC, sea ice concentration, 0–1 bounded)** 의 격자별 오차, (2) **해빙범위(SIE)/해빙면적(SIA)** 등 적분량, (3) **얼음경계(ice edge) 위치·거리 오차**(IIEE·Hausdorff·SPS), (4) **해빙 표류(drift) 벡터오차**, (5) **해빙 두께(thickness)·부피(volume)·두께분포(ITD)·나이(age)**, (6) **한계빙역(MIZ)**, (7) **앙상블/확률 얼음경계 예보**의 신뢰도이다. 공통 지표(RMSE·bias·Taylor·QQ·bootstrap 등)는 01~06·figures/16을 교차링크하고, 여기서는 해빙 고유 지표·해빙 특유 전제(경계함수·bounded 변수·계절/해역 의존)에 집중한다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3-L4), [시계열]=검빙소·지수 시계열(SIE·SIV 인덱스 등), [트랙]=위성 along-track(CryoSat-2/ICESat-2 freeboard, 고도계) 또는 표류부이 궤적, [경계]=얼음경계 폴리곤/등치선(15% SIC contour), [벡터]=해빙 표류 벡터장.
> **"우리 모델 vs 위성/재분석/부이" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **bounded 변수 주의**: SIC는 [0,1] 경계변수 → 순수 정규분포 가정 지표(회귀·평균오차)를 무비판 적용하면 경계 근처에서 왜곡. 아래 각 카드의 '한계·주의' 참조.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **해빙농도 검증 (SIC / sea_ice_area_fraction) bias·RMSE** — 격자별 농도 오차, 0–1 bounded
- ★ **해빙범위 검증 (SIE / Sea Ice Extent, 15% 임계면적)** — 임계 이진화 후 면적
- ★ **해빙면적 검증 (SIA / Sea Ice Area, 농도가중 면적)** — SIE와 구분
- **해빙범위/면적 시계열·계절주기 검증** — 연주기·최소·최대 시점·진폭
- **해빙 시작·소멸일 검증 (advance / retreat / ice-free date)** — 계절 위상 오차
- ★ **통합얼음경계오차 IIEE (Goessling 2016) 와 분해(absolute extent / misplacement)** — 얼음경계 면적오차
- ★ **얼음경계 거리 오차 (Ice-edge displacement: RMS/평균/Hausdorff·Modified Hausdorff)** — 경계선 거리
- **얼음경계 거리 오차 (IIEE 기반 변위·비율 r)** — Melsom et al. 3지표 세트
- **얼음경계 검증 — NIC ice chart / 해빙도 대조** — 운영 ice edge 대조
- ★ **공간 이진장 검증 — FSS·범주형(POD/FAR/CSI) 얼음/무빙** — 이웃검증·이중벌점
- ★ **해빙 표류 벡터오차 (drift: 성분 RMSE·벡터 RMSE·속력·방향)** — sea_ice_x/y_velocity
- **해빙 표류 라그랑지안 검증 (buoy 궤적·분리거리·변형률)** — IABP 부이 대조
- ★ **해빙 두께 검증 (thickness: CryoSat-2 / SMOS / CS2SMOS / ICESat-2 / ULS·잠수함 draft)** — sea_ice_thickness
- **해빙 건현 검증 (freeboard, 고도계 트랙)** — 두께 유도 전 단계
- **적설 깊이 검증 (snow depth on sea ice)** — 두께 변환의 주 오차원
- ★ **해빙 부피 검증 (Sea Ice Volume, SIV / PIOMAS 대조)** — 두께×농도×면적 적분
- **해빙 두께분포 검증 (ITD / g(h) sub-grid distribution)** — 카테고리별 면적비
- **해빙 나이/유형 검증 (ice age / MYI·FYI fraction)** — 다년빙 비율
- **한계빙역 검증 (MIZ: 15–80% SIC 폭·면적·분율)** — marginal ice zone
- ★ **확률·앙상블 얼음경계 검증 (SPS·Brier·ROC·reliability, Spatial Probability Score)** — 확률 ice edge
- **해빙 물리·보존 점검 (얼음질량·염분·에너지 수지, ridging)** — §04 연결
- **해빙 분포·QQ·극값 (SIE 최소 극값·추세·변화점)** — 분포·추세
- ★ **격자-격자 공간비교 (재분석/위성 L4 map difference: bias·RMSE·anomaly)** — SIC/SIT 지도
- ★ **운영·커뮤니티 검증 프레임워크 (SIMIP·SIPN·CMEMS·OSI SAF 절차)** — 표준 매치업

---

### ★ 해빙농도 검증 (해빙농도 / Sea Ice Concentration, SIC = `sea_ice_area_fraction`)
- 무엇을 측정/검증하나: 각 격자의 해빙 피복비율(0=완전개빙, 1=완전피복)을 위성 수동마이크로파 SIC(예: OSI SAF·NSIDC CDR·AMSR2 ASI)나 재분석과 격자별로 비교. 해빙 검증의 가장 기본 장(field).
- 정의·수식: SIC ∈ [0,1] (또는 %). 격자별 bias(x,y)=mean(model−ref), RMSE(x,y)=√mean((model−ref)²), MAE, 영역평균·반구총계. 면적가중 필수: 지표 = Σ wᵢ(mᵢ−oᵢ)² / Σ wᵢ, wᵢ=격자 셀면적(cosφ 또는 실제 셀면적). 공통 정의는 01·figures/16 참조(재정의 안 함).
- 적용 도메인/자료형: [격자] 모델 vs [격자] 위성 L3/L4·재분석. 극점 stereographic 격자 간 재격자화 필요(§15).
- 입력·전제: 동일 극projection·동일 시각(일평균 vs 순간 구분). land/ocean mask 및 극점 데이터공백(pole hole) 통일. 위성 SIC 알고리즘(Bootstrap·NASA Team·ASI·OSI SAF)별로 값이 다름 → 대조군 알고리즘 명시. weather filter·open-water 오탐 처리.
- 해석 기준(advisory): **해역·계절 의존이 매우 큼.** 겨울 밀집빙역(consolidated pack)에서 위성 SIC 불확실성 ~5–10%, 융빙기(melt ponds)·얼음경계·MIZ에서는 20–30%까지 커진다(사례값, 절대기준 아님). 남극 겨울 SIC bias가 MODIS 대비 −0.5%~−18%·RMSE 2–24% 보고 사례 → 모델 RMSE를 이 관측불확실성과 함께 해석. good/bad 단정 금지.
- 한계·주의: SIC는 **[0,1] bounded** → 경계(0·1)에 자료가 몰려 오차분포가 비정규·비대칭. 순 bias가 상쇄로 0이어도 국지 오차 큼(RMSE·공간지도 병행). 위성 SIC 자체가 "참값"이 아니라 알고리즘 산물(§G-1). 융빙기·박빙·MIZ에서 관측·모델 모두 신뢰도 저하(§G). 재격자화가 경계에서 인위적 중간농도 생성 주의.
- 출처: OSI SAF Sea Ice Concentration product (osi-saf.eumetsat.int); Meier et al. NOAA/NSIDC Sea Ice Concentration CDR (nsidc.org); Ivanova et al. (2015) "Inter-comparison and evaluation of sea ice algorithms," *The Cryosphere* 9:1797–1817 (doi:10.5194/tc-9-1797-2015, 확인요 권/페이지); Notz et al. (2016) SIMIP.

---

### ★ 해빙범위 검증 (해빙범위 / Sea Ice Extent, SIE — 15% 임계면적)
- 무엇을 측정/검증하나: SIC ≥ 15% 인 모든 격자셀의 **면적 합**(임계 이진화 후 면적). 해빙 상태의 1차 스칼라 지표이며 위성 장기기록(1979–)과 직접 비교 가능.
- 정의·수식: SIE = Σ_{i: SICᵢ ≥ 0.15} Aᵢ (Aᵢ=셀면적). 검증은 시계열 SIE_model vs SIE_ref 에 bias·RMSE·상관·% 오차. 반구별(북극/남극)·해역별(NSIDC 지역 마스크)로 분리.
- 적용 도메인/자료형: [격자]→[시계열]로 축약. 위성 SIE(NSIDC Sea Ice Index)·재분석·모델.
- 입력·전제: **임계값(15%) 통일** — 임계에 민감(임계 5–30% 변경 시 SIE 변화; Meier & Stewart 2020 계열). 동일 격자면적 정의·동일 마스크·pole hole 처리. 위성 vs 모델 격자해상도 차이가 얼음경계 셀 계상에 영향.
- 해석 기준(advisory): SIE는 상쇄에 강건하지만 **위치오차를 못 봄**(잘못된 위치의 얼음도 상쇄되면 SIE 일치) → IIEE·경계거리 병행 필수(Goessling 2016). 반구·계절별 bias 패턴(예: 남극 여름 과소, 북극 여름 급감)을 계절성과 함께 해석. 절대 임계로 우열 단정 금지.
- 한계·주의: 15% 임계 이진화로 정보 손실(농도 정보 버림). 격자해상도가 다르면 경계 셀 수가 달라져 SIE에 계통차 발생 → 공통격자 재비교 권장. "SIE 일치=모델 우수"는 오해(위치·두께 무시).
- 출처: Fetterer et al. NSIDC *Sea Ice Index* v3 (doi:10.7265/N5K072F8, 확인요); Notz (2014) "Sea-ice extent and its trend provide limited metrics of model performance," *The Cryosphere* 8:229–243; Meier & Stewart (2019/2020) SIE 임계 민감도 계열(확인요).

---

### ★ 해빙면적 검증 (해빙면적 / Sea Ice Area, SIA — 농도가중 면적)
- 무엇을 측정/검증하나: SIE와 달리 **농도로 가중한** 실제 얼음 면적(SIA = Σ SICᵢ·Aᵢ). "얼음이 실제로 덮은 넓이". SIE−SIA 차이는 MIZ·박빙 비율의 지표.
- 정의·수식: SIA = Σ_{i: SICᵢ ≥ 0.15} SICᵢ·Aᵢ (임계 이상 셀에서 농도가중; 관행에 따라 임계 적용 여부·pole hole 채움 방식 상이 → 명시). 검증은 SIE와 동일 통계.
- 적용 도메인/자료형: [격자]→[시계열]. 위성·재분석·모델.
- 입력·전제: 임계 적용 규약·pole hole 처리·저농도 절단이 값을 좌우 → 대조군과 정확히 동일 절차. 위성 SIA는 알고리즘 SIC 오차를 직접 반영.
- 해석 기준(advisory): SIA는 SIE보다 농도오차·MIZ 재현에 민감. SIE는 잘 맞는데 SIA가 어긋나면 농도 프로파일(밀집빙 vs MIZ) 오차 시사. 계절·반구 의존 큼.
- 한계·주의: pole hole·저농도 절단·임계 규약 불일치가 계통차의 흔한 원인. SIE와 반드시 함께 보고(둘 중 하나만으로 결론 금지).
- 출처: NSIDC *Sea Ice Index* 문서(SIE·SIA 정의); Notz (2014, *The Cryosphere*); SIMIP(Notz et al. 2016).

---

### 해빙범위/면적 시계열·계절주기 검증 (Seasonal cycle of SIE/SIA)
- 무엇을 측정/검증하나: SIE/SIA 연주기의 진폭·위상(최대 3월·최소 9월 북극 등), 최소·최대 값과 발생 시점을 모델이 재현하는지.
- 정의·수식: 월평균 기후값(climatology)의 계절곡선 비교 + 최소/최대 값·발생월 오차. 편차(anomaly) 상관·계절별 bias. 공통 시계열 분해(STL·조화)는 §06 교차링크.
- 적용 도메인/자료형: [시계열](SIE/SIA 지수) 장기.
- 입력·전제: 동일 기준기간 climatology, 동일 반구·마스크. 추세 제거 여부 명시(추세 포함 시 계절진폭 왜곡 가능).
- 해석 기준(advisory): 최소기(9월 북극)·최대기 각각 오차 특성이 다름 → 분리 보고. 진폭·위상 동시 평가(진폭만 맞고 위상 어긋나면 상관 낮음).
- 한계·주의: 단일 계절곡선은 공간 위치오차를 못 봄(IIEE 병행). 위성 기록 초기(1979~1987 SMMR)와 후기 센서 전환 불연속 주의.
- 출처: Notz (2014); SIMIP(Notz et al. 2016); §06 시계열 카드.

---

### 해빙 시작·소멸일 검증 (Ice advance / retreat / ice-free date)
- 무엇을 측정/검증하나: 격자별·해역별로 얼음이 처음 형성되는 날(advance), 물러가는 날(retreat), 무빙(ice-free) 지속기간을 모델이 재현하는지. 생태·항로·계절예측에 직결.
- 정의·수식: 특정 임계(흔히 SIC=15%)를 상향/하향 교차하는 율리우스일. advance/retreat day·개빙기간(open-water duration)의 격자별 bias(일 단위)·공간지도.
- 적용 도메인/자료형: [격자] 위성 SIC 시계열 vs 모델. 남극 연구에서 표준(Stammerjohn et al. 2012).
- 입력·전제: 임계·연속성 규칙(며칠 연속 초과해야 advance로 볼지) 통일. 일자료(또는 준일자료) 필요.
- 해석 기준(advisory): retreat/advance는 서로 다른 물리(융빙 vs 결빙) → 분리 진단. 며칠~수십일 오차가 흔함(해역·연도 편차 큼). 절대기준 없음.
- 한계·주의: 임계 교차 정의·noise(단기 재결빙)에 민감. 위성 일자료의 잡음이 날짜 추정에 큰 불확실성.
- 출처: Stammerjohn, Massom, Rind & Martinson (2012) "Regions of rapid sea ice change," *Geophysical Research Letters* 39, L06501 (doi:10.1029/2012GL050874, 확인요).

---

### ★ 통합얼음경계오차 IIEE (Integrated Ice Edge Error, Goessling et al. 2016) 및 분해
- 무엇을 측정/검증하나: 모델과 기준이 "SIC 15% 이상/미만"에 **불일치하는 총 면적**. SIE가 못 잡는 얼음경계 위치오차를 면적 단위로 정량화. 사용자 관점(항로·해빙경계)에 직결.
- 정의·수식: 이진 얼음마스크 I = 1{SIC ≥ 0.15}. IIEE = ∫|I_model − I_ref| dA = A⁺ + A⁻, 여기서 A⁺=모델만 얼음(over), A⁻=기준만 얼음(under). **분해**: Absolute Extent Error AEE = |A⁺ − A⁻| (= 기존 SIE 오차의 절댓값), Misplacement Error ME = 2·min(A⁺, A⁻) (위치어긋남). IIEE = AEE + ME. (Goessling et al. 2016: 기후적으로 ME가 IIEE의 절반 이상을 차지 — SIE 오차만 보면 위치오차를 놓친다.)
- 적용 도메인/자료형: [격자]/[경계] 모델 vs 위성/재분석 이진 얼음마스크.
- 입력·전제: 동일 격자·동일 임계(15%)·동일 마스크. 면적가중(실제 셀면적). land 및 pole hole 일관 처리. 위성·모델 해상도 정합(다르면 재격자화 후).
- 해석 기준(advisory): IIEE↓ 양호하되 **AEE(범위)와 ME(위치)를 나눠 보라** — SIE는 좋은데 ME가 크면 "면적은 맞지만 위치가 틀림". 계절(9월 최소기 IIEE 급증)·반구·리드타임 의존 큼. SPS의 결정론 특수형이 IIEE(아래 확률 카드).
- 한계·주의: 15% 임계 이진화 정보손실(농도 무시). 격자해상도가 다르면 경계 셀 계상 차이로 IIEE 계통편향 → 공통격자 필수. 절대값이라 "어느 방향" 오차는 AEE 부호·공간지도로 별도 확인.
- 출처: Goessling, Tietsche, Day, Hawkins & Jung (2016) "Predictability of the Arctic sea ice edge," *Geophysical Research Letters* 43(4):1642–1650 (doi:10.1002/2015GL067232); Goessling & Jung (2018, SPS로 확장, 아래).

---

### ★ 얼음경계 거리 오차 (Ice-edge displacement: RMS / Average / Hausdorff·Modified Hausdorff)
- 무엇을 측정/검증하나: 모델 얼음경계선과 기준 경계선 사이의 **거리(km)**. IIEE가 면적이라면 이것은 경계선 간 기하학적 거리. 예보 경계 오차를 직관적 거리로 표현.
- 정의·수식: 두 경계 집합 X(모델), Y(기준)에 대해 — 평균변위 D_AVG=경계점별 최근접거리 평균; RMS 변위 D_RMS=최근접거리 제곱평균근; **Hausdorff distance** H(X,Y)=max{ sup_{x∈X} d(x,Y), sup_{y∈Y} d(y,X) } (최악점 거리); **Modified Hausdorff Distance (MHD)** = max{ mean_{x∈X} d(x,Y), mean_{y∈Y} d(y,X) } (평균화로 noise·이상치에 강건, Dukhovskoy 등 권장). Edge Displacement Error(EDE)=경계길이로 정규화한 무차원값.
- 적용 도메인/자료형: [경계](15% SIC 등치선 폴리곤) 모델 vs 위성/ice chart.
- 입력·전제: 경계 정의(SIC 임계·최대 연결성분·섬/호수 제거) 통일. 대륙연안·닫힌 만(inland) 경계 처리 규칙. 좌표계 거리계산(구면 vs 투영). 여러 개 분리된 얼음덩어리 매칭 규칙.
- 해석 기준(advisory): 순수 Hausdorff는 단일 최악점에 지배됨 → 이상치 민감; **MHD·평균변위가 더 안정적**(Dukhovskoy et al. 2015 권장). 해역·경계길이 의존 → EDE(정규화) 병행. 수십 km 오차가 단기예보에서 흔함(사례값).
- 한계·주의: 경계 추출·연결성분·연안처리 규칙에 결과가 크게 좌우(재현 위해 규칙 명시). 방향(안/밖) 정보는 별도(IIEE의 A⁺/A⁻ 병행). double counting 주의.
- 출처: Melsom, Palerme & Müller (2019) "Validation metrics for ice edge position forecasts," *Ocean Science* 15:615–630 (doi:10.5194/os-15-619-2019 → 정정: 10.5194/os-15-615-2019); Dukhovskoy et al. (2015) "Skill metrics for evaluation and comparison of sea ice models," *JGR Oceans* 120 (확인요 권/페이지); Dubuisson & Jain (1994) MHD 원 정의(*ICPR*).

---

### 얼음경계 거리 오차 — IIEE 기반 변위·비율 r (Melsom et al. 3지표 세트)
- 무엇을 측정/검증하나: IIEE(면적)를 경계길이로 나눠 "평균 경계변위(km)"로 환산하고, 상·하계 및 편향을 함께 보는 Melsom et al.(2019) 권장 3지표 세트.
- 정의·수식: D_AVG_IE(경계점 평균변위, 상한 성격), D_AVG_IIEE(=IIEE/경계길이, 하한 성격), ΔIIEE(=(A⁺−A⁻)/경계길이, 부호 있는 편향). 보조로 비율 r_AVG(두 변위의 비, 위치오차 대 범위오차 성격)·IIEE 공간지도.
- 적용 도메인/자료형: [경계]/[격자] 예보 검증.
- 입력·전제: 위 얼음경계 카드와 동일(임계·연결성·연안처리 통일). 경계길이 정의 일관.
- 해석 기준(advisory): 세 지표를 **함께** 읽어라(단일 지표로 결론 금지) — D_AVG_IE와 D_AVG_IIEE가 경계를 위/아래로 감싸고, ΔIIEE가 치우침 방향을 준다. 절대값은 해역·계절 의존.
- 한계·주의: 정의가 여럿(IE 기반 vs IIEE 기반)이라 보고 시 어느 정의인지 명시 필수. FSS(아래)와 상보적.
- 출처: Melsom, Palerme & Müller (2019, *Ocean Science* 15:615–630, doi:10.5194/os-15-615-2019).

---

### 얼음경계 검증 — NIC ice chart / 해빙도 대조 (Operational ice chart comparison)
- 무엇을 측정/검증하나: 분석가가 다중센서(SAR·광학·PMW)로 작성한 운영 해빙도(NIC/AARI/캐나다 ice chart)의 얼음경계·농도 등급(egg code)과 모델을 대조. 위성 자동 SIC보다 얼음경계·MIZ에서 신뢰도 높은 준(準)기준.
- 정의·수식: ice chart 농도등급(총농도 CT)·얼음경계를 격자화 후 IIEE·경계거리·범주형 지표 적용. egg code의 부분농도(Ca/Cb/Cc)·유형 활용 가능.
- 적용 도메인/자료형: [경계]/[격자] ice chart(폴리곤/shapefile) vs 모델.
- 입력·전제: chart 폴리곤 → 격자 변환(농도등급 중앙값 등) 규칙 명시. 분석가 주관·발행주기(주 1회 등)·subjectivity 감안. chart는 얼음이 있으면 최소농도 과대(안전측) 경향.
- 해석 기준(advisory): ice chart는 얼음경계에 대해 PMW보다 정확한 경향(MIZ·박빙 포착) → 얼음경계 검증의 유용한 대조. 다만 "참값" 아님(분석가 편차). 절대판정 금지.
- 한계·주의: 폴리곤 이산화·발행빈도·분석가 편차가 오차원. 자동 자료와 직접 비교 시 불연속.
- 출처: U.S. National Ice Center(NIC) products; Cheng et al. / WMO egg code 관행; NSIDC G10017 U.S. NIC Daily MIZ product 문서(확인요).

---

### ★ 공간 이진장 검증 — FSS·범주형 (Fractions Skill Score / POD·FAR·CSI, 얼음/무빙)
- 무엇을 측정/검증하나: "얼음 있음/없음"(SIC≥15%) 이진장의 공간 일치를 이웃검증(FSS)·2×2 분할표로 평가. 격자 double-penalty(경계 약간 어긋나면 hit+miss 이중처벌)를 완화.
- 정의·수식: 범주형(§03 재정의 안 함): POD=a/(a+c), FAR=b/(a+b), CSI=a/(a+b+c), HSS/ETS(우연보정). FSS(이웃크기 n): FSS=1−MSE(n)/MSE_ref(n), useful-scale=0.5+f₀/2(§02·figures/16 교차링크). 임계는 SIC 15%(또는 다중 임계 스캔).
- 적용 도메인/자료형: [격자] 이진 얼음마스크 예보 검증.
- 입력·전제: 동일 격자·임계·마스크. FSS 이웃크기 스캔 범위 지정. 극projection에서 이웃(km) 정의 일관.
- 해석 기준(advisory): 얼음경계는 본질적으로 이중벌점에 취약 → 점대점 CSI만 보면 과소평가. FSS로 "얼마의 공간스케일에서 유용한가"를 함께 보라. useful-scale은 해역·계절 의존(advisory).
- 한계·주의: 단일 임계·단일 이웃크기로 결론 금지(스캔). IIEE·경계거리와 상보적(면적 vs 스케일 vs 거리).
- 출처: Roberts & Lean (2008) FSS(§02); Melsom et al. (2019, FSS 얼음경계 적용); Jolliffe & Stephenson(범주형, §03).

---

### ★ 해빙 표류 벡터오차 (Sea ice drift: `sea_ice_x_velocity`/`sea_ice_y_velocity`, `sea_ice_speed`)
- 무엇을 측정/검증하나: 해빙 표류 속도·변위 벡터의 크기·방향 오차. 위성 표류자료(OSI SAF·NSIDC Polar Pathfinder·2일 변위)나 부이 대조. 역학(바람·해류 응력·유변학) 검증의 핵심.
- 정의·수식: 성분별 bias·RMSE(dX, dY 또는 u, v); **벡터 RMSE(VRMSE)** = √mean(|**v**_m − **v**_o|²) = √mean((uₘ−uₒ)²+(vₘ−vₒ)²); 속력 오차 bias/RMSE(`sea_ice_speed`); 방향 오차는 원형통계(§07 원형 카드 교차링크; 0/360 wrap). 복소/벡터 상관은 §10(Kundu·Crosby) 교차링크. 변위(2일 등) 또는 속도 중 대조군 정의와 일치.
- 적용 도메인/자료형: [벡터][격자] 위성 drift vs 모델; [트랙] 부이 변위 vs 모델 보간.
- 입력·전제: **시간창 일치**(위성 2일 변위 ↔ 모델 2일 적분변위; 순간속도와 혼동 금지). 극projection 벡터 회전(격자 x/y ↔ 지리 동/북) 정합(§15). 저속·저농도·여름 표류자료 신뢰도 저하 → QC·flag. 정지(fast ice) 영역 제외.
- 해석 기준(advisory): 위성 drift는 북반구가 남반구보다 통계 양호(OSI SAF 검증). 속력 bias는 유변학(rheology)·바람강제·해류 응력을 함께 시사. 방향·속력을 분리 진단(벡터 RMSE만으로 원인 불명). 절대기준 없음(해역·계절·센서 의존).
- 한계·주의: 위성 표류는 시공간 평활(격자·2일)된 값 → 점 부이와 대표성 오차. 여름 융빙기·저속에서 위성 추적 실패 많음. 벡터 회전 오류가 방향 검증을 망침(흔한 실수).
- 출처: Lavergne et al. (2010) "Sea ice motion from low-resolution satellite sensors," *JGR Oceans* 115, C10032 (확인요); Lavergne et al. (2023) "A climate data record of year-round global sea-ice drift from EUMETSAT OSI SAF," *ESSD* 15:5807 (doi:10.5194/essd-15-5807-2023); Sumata et al. (2014) drift product 상호비교(*JGR Oceans*, 확인요).

---

### 해빙 표류 라그랑지안 검증 (buoy 궤적·분리거리·변형률)
- 무엇을 측정/검증하나: 부이(IABP) 궤적을 모델 유속으로 적분한 가상궤적과 비교(라그랑지안). 누적 분리거리, 궤적유사도, 변형률(deformation: divergence·shear)까지.
- 정의·수식: 분리거리(separation distance) s(t)=|**x**_model(t)−**x**_buoy(t)| 시간증가; 정규화 누적 라그랑지안 분리(Liu-Weisberg skill score, §06 교차링크). 변형률: 삼각형(부이 3점) 면적변화율로 divergence·shear·total deformation, 모델 대비 PDF·multifractal scaling.
- 적용 도메인/자료형: [트랙] IABP 부이 vs 모델 유속장 적분.
- 입력·전제: 동일 시작점·시간창, 모델 유속 시공간 보간. 변형률은 부이 삼각형 규모(L)·시간규모(T) 명시(scaling 의존).
- 해석 기준(advisory): 분리거리는 시간에 따라 필연 증가(카오스) → 예보리드타임 대비 평가. 변형률 PDF의 두꺼운 꼬리·multifractal scaling 재현이 유변학 품질 지표(neXtSIM 등). 절대기준 없음.
- 한계·주의: 부이 sparse·불균등 분포. 변형률은 규모의존(scale-dependent) → 관측·모델 동일 규모로. 궤적적분 오차 누적.
- 출처: Rampal et al. (2008) sea ice deformation scaling(*JGR Oceans*, 확인요); Bouchat & Tremblay / Hutter et al. deformation 검증 계열(확인요); Liu & Weisberg (2011) trajectory skill(§06).

---

### ★ 해빙 두께 검증 (Sea ice thickness = `sea_ice_thickness`: CryoSat-2 / SMOS / CS2SMOS / ICESat-2 / ULS·잠수함 draft)
- 무엇을 측정/검증하나: 해빙 두께(m)를 위성 고도계(CryoSat-2, 두꺼운 겨울빙 강점)·SMOS(박빙 <~0.5 m 강점)·병합 CS2SMOS·ICESat-2(레이저 건현)·계류/잠수함 초음파(ULS/submarine draft)·항공(OIB)과 비교.
- 정의·수식: 두께 h의 bias·RMSE·상관·QQ. 위성 두께는 건현→두께 정수압 변환(h = f(freeboard, snow depth, ρ_ice, ρ_snow, ρ_water))으로 유도되어 불확실성 큼. 잠수함/ULS는 draft(흘수) 측정 → draft≈0.89·h 근사로 두께 환산(가정 명시). 격자평균 vs 트랙/점 대표성 유의.
- 적용 도메인/자료형: [트랙](CryoSat-2/ICESat-2 along-track, OIB), [격자](CS2SMOS L4·월평균) vs 모델; [시계열/점](ULS 계류·잠수함 draft).
- 입력·전제: 동일 기간·동일 두께정의(정수압 두께 vs draft). 위성 겨울(10–4월)만 가용(융빙기 melt pond·건현 산정 불가). 적설(snow depth) 입력 오차가 위성 두께의 최대 오차원. ULS는 draft→thickness 변환가정. 격자 대표성(점 vs 셀평균).
- 해석 기준(advisory): **센서별 유효두께대가 다름** — SMOS는 박빙(<0.5–1 m), CryoSat-2는 후빙(>~0.5 m), CS2SMOS 병합이 전 범위서 최량 경향(사례). ICESat-2와 상호검증. 모델은 후빙 과소·박빙 과대 경향 사례 보고 → 두께대별(binned) 진단 권장. 절대기준 없음(불확실성 큰 변수).
- 한계·주의: 위성 두께는 **관측이 아니라 강한 가정(밀도·적설)에 의존한 유도량** → "관측 두께"로 과신 금지(§G-1·G-3). 계절(겨울 한정)·두께대·적설 오차에 민감. draft↔thickness 변환·penetration(레이더 눈 침투) 가정 주의. 트랙 sparse.
- 출처: Ricker et al. (2017) "A weekly Arctic sea-ice thickness data record from merged CryoSat-2 and SMOS," *The Cryosphere* 11:1607–1623 (doi:10.5194/tc-11-1607-2017, 확인요); Laxon et al. (2013) CryoSat-2 두께(*GRL*); Kwok et al. (2020) ICESat-2 두께(*JGR Oceans*, 확인요); Rothrock/Wensnahan submarine draft; Tilling et al. (2018) CryoSat-2 near-real-time.

---

### 해빙 건현 검증 (Sea ice freeboard, 고도계 트랙)
- 무엇을 측정/검증하나: 두께 유도 전 단계인 건현(freeboard: 해면 위 얼음/눈 표면 높이)을 모델(또는 유도값)과 고도계 트랙에서 직접 비교. 두께 변환의 밀도·적설 가정을 우회한 진단.
- 정의·수식: radar freeboard(CryoSat-2, 눈-얼음 경계 반사 가정)·total/laser freeboard(ICESat-2). bias·RMSE·상관. 리드(lead) 기준 해면고 산정 후 얼음 표면과의 차.
- 적용 도메인/자료형: [트랙] CryoSat-2/ICESat-2 freeboard vs 모델 유도 freeboard(모델이 직접 산출 안 하면 두께로부터 역산).
- 입력·전제: 리드 탐지·해면 기준면 산정 규약. radar penetration(눈 침투율) 가정 명시. 트랙-격자 대표성.
- 해석 기준(advisory): freeboard 비교는 밀도·적설 변환오차를 분리하는 데 유용(두께 불일치가 변환에서 왔는지 진단). 센서 원리차(레이더 vs 레이저) 주의. 절대기준 없음.
- 한계·주의: 모델이 freeboard를 직접 안 주면 역산 필요(가정 재유입). penetration·리드탐지 오차. 소량(cm)이라 상대오차 큼.
- 출처: Ricker et al. (2014) CryoSat-2 freeboard 불확실성(*The Cryosphere* 8:1607, 확인요); Kwok & Cunningham (2015); Landy et al. (2020) radar penetration(확인요).

---

### 적설 깊이 검증 (Snow depth on sea ice)
- 무엇을 측정/검증하나: 해빙 위 적설 깊이. 위성 두께 변환·에너지수지의 핵심 입력이자 최대 오차원. 모델 적설 vs 기후값(Warren)·재분석·항공·부이.
- 정의·수식: 적설깊이(m)의 bias·RMSE. Warren climatology(1999)·NASA SnowModel·AMSR2 snow·OIB snow radar·부이 대조.
- 적용 도메인/자료형: [격자]/[트랙] 적설 산출물 vs 모델.
- 입력·전제: 다년빙/일년빙 위 적설 특성 상이. Warren 기후값은 1980년대 관측 기반 → 최근 박빙에 과대 가능. 항공 snow radar 불확실성.
- 해석 기준(advisory): 적설 5 cm 오차가 위성 두께에 수십 cm 영향 → 두께 검증 해석 시 반드시 병기. 계절·빙종 의존. 절대기준 없음.
- 한계·주의: 적설 관측 자체가 매우 불확실(기준자료 신뢰도 낮음, §G-1). 두께 검증과 강하게 결합 → 독립 검증 어려움.
- 출처: Warren et al. (1999) "Snow depth on Arctic sea ice," *Journal of Climate* 12:1814–1829; Kwok et al. snow radar; Liston et al. SnowModel(확인요).

---

### ★ 해빙 부피 검증 (Sea Ice Volume, SIV — PIOMAS 대조)
- 무엇을 측정/검증하나: 반구·해역 총 해빙 부피(두께×농도×면적 적분). 두께+농도를 통합한 상태량. PIOMAS 재분석·위성 두께기반 부피와 대조.
- 정의·수식: SIV = Σ SICᵢ·hᵢ·Aᵢ. 시계열 bias·RMSE·상관·계절진폭. 두께가 곱해져 두께오차가 크게 반영.
- 적용 도메인/자료형: [격자]→[시계열]. PIOMAS(모델기반 재분석, 참값 아님)·CS2SMOS 유도 부피.
- 입력·전제: 동일 영역·마스크. **PIOMAS는 관측이 아니라 동화모델 산물**(§G-1) → 기준으로 과신 금지. 위성 부피는 두께 불확실성 그대로 승계.
- 해석 기준(advisory): SIV는 SIE보다 기후민감·추세 신호가 큼(Notz 계열). 두께오차가 지배 → 두께 검증과 함께 해석. 계절진폭·최소기 값 분리. 절대기준 없음.
- 한계·주의: 기준자료(PIOMAS/위성) 불확실성이 커서 "검증"보다 "상호비교" 성격. 두께·농도 오차가 합쳐져 원인분해 어려움(두께·SIC 개별 카드 병행).
- 출처: Zhang & Rothrock (2003) PIOMAS(*Monthly Weather Review* 131:845–861, 확인요); Schweiger et al. (2011) PIOMAS 불확실성(*JGR Oceans* 116, C00D06, 확인요); Notz (2014, *The Cryosphere*).

---

### 해빙 두께분포 검증 (Ice Thickness Distribution, ITD / g(h) sub-grid)
- 무엇을 측정/검증하나: 격자 내 sub-grid 두께분포 g(h)(CICE 5카테고리 등)의 카테고리별 면적비를, 항공/ULS/위성으로 추정한 두께분포와 비교. 평균두께가 놓치는 박빙·후빙(ridge) 구조.
- 정의·수식: g(h)dh=두께가 [h,h+dh]인 면적비, ∫g(h)dh=SIC. 카테고리별 면적비 비교, 분포 형상(모드·꼬리)·QQ(§01 QQ 교차링크). ridging에 의한 후빙 꼬리 재현.
- 적용 도메인/자료형: [격자](모델 ITD) vs [트랙/점](OIB·ULS·잠수함 draft 분포).
- 입력·전제: 관측 두께분포 표본(트랙/점)과 모델 격자분포의 규모 정합. 카테고리 경계 통일. draft→thickness 변환.
- 해석 기준(advisory): 평균두께가 맞아도 분포(박빙·ridge 꼬리)가 어긋날 수 있음 → ITD로 역학(ridging·rafting) 진단. 관측 분포 표본수 적어 꼬리 불안정. 절대기준 없음.
- 한계·주의: 관측 두께분포 자체가 sparse·불확실. 모델 카테고리 이산화(5개 등)로 분포 근사. §04 ridging 보존과 연결.
- 출처: Thorndike et al. (1975) ITD 이론(*JGR* 80:4501–4513, 확인요); Hibler(1980); CICE Consortium documentation(ITD 구현).

---

### 해빙 나이/유형 검증 (Ice age / MYI·FYI fraction, `sea_ice_classification`)
- 무엇을 측정/검증하나: 다년빙(MYI)·일년빙(FYI) 비율·해빙 나이를, 위성 나이자료(EASE-Grid Sea Ice Age, Tschudi)·QuikSCAT/ASCAT 산란계 유형과 대조. 두께·역학 대리지표.
- 정의·수식: MYI/FYI 면적비·나이별 면적비 bias·RMSE·범주 일치(2×2 또는 다범주). 라그랑지안 나이추적(모델) vs 위성 나이.
- 적용 도메인/자료형: [격자] 위성 ice age/type vs 모델 나이/유형.
- 입력·전제: 나이/유형 정의(MYI 판별 기준) 통일. 위성 나이는 표류추적 누적 산물(오차 누적). 여름 융빙기 유형판별 곤란.
- 해석 기준(advisory): MYI 감소 추세 재현이 기후검증 핵심. 위성 나이 자체 불확실(라그랑지안 오차) → 상호비교 성격. 절대기준 없음.
- 한계·주의: 위성 나이는 유도량(참값 아님, §G-1). 산란계 유형은 여름·표면융해에 취약. 모델 나이추적 방식 상이.
- 출처: Tschudi et al. (2019) "EASE-Grid Sea Ice Age," NSIDC(doi:10.5067/UTAV7490FEPB, 확인요); Maslanik et al. (2007) ice age(*GRL*, 확인요).

---

### 한계빙역 검증 (Marginal Ice Zone, MIZ: 15–80% SIC 폭·면적·분율)
- 무엇을 측정/검증하나: 개빙과 밀집빙 사이 전이대(MIZ). 통상 SIC 15–80% 영역의 폭·면적·MIZ 분율(MIZ면적/총빙면적)을 모델이 재현하는지. 파-빙 상호작용·항해에 중요.
- 정의·수식: MIZ mask = 1{0.15 ≤ SIC < 0.80}. MIZ 면적·폭(경계 수직 거리)·분율. WMO 정의는 "파·너울 침투 영역"(물리)과 SIC 임계정의(대리)가 다름 → 정의 명시. 검증은 IIEE·면적·범주형 적용.
- 적용 도메인/자료형: [격자] 위성 SIC vs 모델.
- 입력·전제: MIZ 임계(15–80%) 통일. 위성 SIC의 중간농도(MIZ 대역) 불확실성이 가장 큼 → 관측 신뢰도 저하 감안. SAR·PMW 정의 차이.
- 해석 기준(advisory): MIZ 대역이 바로 위성 SIC 오차 최대 구간 → 관측불확실성 크게 병기. 모델 MIZ 폭이 과소(경계 급변) 경향 사례. 계절(여름 MIZ 확대)·반구 의존. 절대기준 없음.
- 한계·주의: 임계기반 MIZ ≠ 물리(파침투) MIZ. 중간농도 관측 신뢰도 낮음(§G-1). 파-빙 결합 없는 모델은 MIZ 물리 부재.
- 출처: Strong & Rigor (2013) Arctic MIZ 확대(*GRL* 40:4864–4868, 확인요); Rolph, Feltham & Schröder (2020) Arctic MIZ(*The Cryosphere*, 확인요); Horvat (2021) "Marginal ice zone fraction benchmarks sea ice and climate model skill," *Nature Communications* 12 (doi 확인요); WMO Sea Ice Nomenclature(WMO-No. 259).

---

### ★ 확률·앙상블 얼음경계 검증 (Spatial Probability Score SPS·Brier·ROC·reliability)
- 무엇을 측정/검증하나: 앙상블/확률 얼음경계 예보(격자별 "얼음 확률")의 신뢰도(reliability)·해상도·예리함. IIEE의 확률 확장. 계절·subseasonal 해빙예측 검증의 표준.
- 정의·수식: **Spatial Probability Score SPS** = ∫ (p_fcst(x) − o(x))² dA (격자별 (half-)Brier의 공간적분; o∈{0,1}=관측 얼음유무). 결정론(또는 앙상블평균)으로 축약하면 SPS→IIEE(Goessling & Jung 2018). 임계초과확률 Brier Score·BSS, ROC/AUC(판별력), reliability diagram, rank histogram은 §03·figures/16 교차링크(재정의 안 함).
- 적용 도메인/자료형: [격자] 앙상블 SIC/얼음확률 vs 위성 이진 얼음마스크.
- 입력·전제: 앙상블 멤버 전체 또는 예보확률장. 관측은 결정론 이진(15% 임계). 동일 격자·마스크·면적가중. 기준예보(기후·damped anomaly persistence) 정의(skill score용).
- 해석 기준(advisory): SPS↓·(기준대비 skill score) >0이면 기준예보보다 우수. reliability·ROC로 신뢰도/판별력 분리. **damped anomaly persistence를 벤치마크로** 권장(Zampieri·Niraula 계열) — 동역학 모델이 이를 못 이기면 skill 의문. 계절·리드타임 의존 큼.
- 한계·주의: 결정론 단일모델엔 SPS→IIEE로만(확률 지표 불가). 희소 극단(9월 최소)에서 Brier/ROC 불안정. 기준예보 선택이 skill score를 좌우(명시).
- 출처: Goessling & Jung (2018) "A probabilistic verification score for contours: ... Arctic ice-edge forecasts," *QJRMS* 144:1750–1761 (doi:10.1002/qj.3242, 확인요 권/페이지); Zampieri, Goessling & Jung (2018) "Bright prospects for Arctic sea ice prediction on subseasonal time scales," *GRL* 45:9731–9738 (doi:10.1029/2018GL079394); Palerme et al. (2019) "An intercomparison of verification scores for evaluating the sea ice edge position in seasonal forecasts," *GRL* 46 (doi:10.1029/2019GL082482, 확인요); Niraula & Goessling (2021, damped anomaly persistence benchmark, *JGR Oceans*, doi 확인요).

---

### 해빙 물리·보존 점검 (얼음 질량·염분·에너지 수지, ridging)
- 무엇을 측정/검증하나: 해빙 모델의 질량(결빙/융빙·이류·ridging)·염분·에너지 수지 닫힘과 ridging/rafting에 의한 두께재분배의 물리 일관성. 관측 대조보다 모델 내적 정합(§04 연결).
- 정의·수식: 얼음질량 budget: d(ρh)/dt = 열역학 성장 − 융해 + 이류 + 역학재분배(ridging). 잔차(residual)=수치 비보존. 염분수지(brine rejection)·표면에너지수지. 공통 수지닫힘 방법은 §04 교차링크(재정의 안 함).
- 적용 도메인/자료형: [격자] 모델 진단(online 항 출력 필요).
- 입력·전제: 각 수지항의 online 진단출력. 이류·재분배 스킴별 보존특성 상이.
- 해석 기준(advisory): 잔차가 성장/융해 항 대비 작아야 함(수치보존). ridging이 후빙 꼬리·SIV에 미치는 영향 점검. 절대기준 없음(모델별).
- 한계·주의: 관측 대조 아님(내적 일관성). offline 진단은 근사(§04 online-vs-offline 주의). 스킴 의존.
- 출처: §04 conservation 카드; Hibler (1979) 해빙 유변학(*JPO* 9:815–846, 확인요); CICE/Icepack documentation(질량·염분·에너지 수지).

---

### 해빙 분포·QQ·극값·추세 (SIE 최소 극값·추세·변화점)
- 무엇을 측정/검증하나: SIE/SIA/SIV 분포와 극단(9월 북극 최소 기록), 장기추세·변화점을 관측과 대조. 기후검증·기록경신 예측.
- 정의·수식: 분포 QQ/CDF·KS(§01 교차링크), 9월 최소 SIE의 GEV/추세(Mann-Kendall/Sen §06), 변화점(§06). 추세 신뢰구간·bootstrap(§01·figures/16).
- 적용 도메인/자료형: [시계열] 장기 SIE/SIV 지수.
- 입력·전제: 장기 동질 기록(센서 전환 불연속 보정). 추세는 자기상관 보정(유효표본).
- 해석 기준(advisory): 9월 최소 추세(북극 급감)·남극 근년 급감(2016~) 재현이 핵심. 극값 표본 적어 불확실. 절대기준 없음.
- 한계·주의: 위성 기록 짧음(1979~)·초기 불연속. 극값·추세 신뢰구간 필수(bootstrap). 분포만으론 공간·위치 못 봄.
- 출처: Stroeve et al. (2012) September SIE 추세(*GRL*, 확인요); §01(QQ/KS)·§06(추세·변화점)·figures/16.

---

### ★ 격자-격자 공간비교 (재분석/위성 L4 map difference: SIC·SIT bias·RMSE·anomaly)
- 무엇을 측정/검증하나: 우리 모델 [격자]를 재분석(ORAS5·GLORYS 해빙·GIOMAS)·위성 L4(SIC CDR·CS2SMOS)와 **공간 전면적**으로 비교해 bias·RMSE·상관·anomaly correlation(ACC)의 지리분포를 극지도로.
- 정의·수식: 공통 극격자 재격자화(§15) 후 격자별 bias(x,y)·RMSE(x,y)·R(x,y)·ACC. 반구총계·해역별·위도대. 공통 지표·ACC는 §01·§02·figures/16 교차링크(재정의 안 함).
- 적용 도메인/자료형: SIC·SIT·drift·나이 [격자] vs [격자]. NetCDF↔NetCDF.
- 입력·전제: **극projection·시간축·달력·마스크 정합**, land/pole hole 통일, 단위(fraction vs %). SIC 재격자화가 경계에서 인위적 중간농도 → 보존형/최근접 선택 주의. 재분석 해상도·해빙모델 차이.
- 해석 기준(advisory): 지도에서 계통 bias 위치(예: 특정 해역 과대·경계 과소)·계절성 파악. **재분석·위성 L4는 참값 아님**(§G-1) → 부이·트랙 검증과 교차. 절대판정 금지.
- 한계·주의: 재분석은 또 하나의 (동화)모델 산물 → "정답" 과신 금지. 재격자화·해상도 차가 차이 상당부분 생성. GLORYS 등은 해빙변수 제공 여부·정의 확인요.
- 출처: §01·§02·§15·figures/16; Zuo et al. (2019) ORAS5(*Ocean Science*, 확인요); OSI SAF/NSIDC L4 SIC; Ricker et al. (2017) CS2SMOS.

---

### ★ 운영·커뮤니티 검증 프레임워크 (SIMIP·SIPN·CMEMS·OSI SAF 표준 절차)
- 무엇을 측정/검증하나: 해빙 모델·예보를 커뮤니티 공통 자료·공통 지표로 표준화 검증·상호비교하는 프로토콜(검증의 "표준화" 자체).
- 정의·수식: SIMIP(CMIP6 Sea Ice MIP)=SIE·SIA·SIV·두께·drift 등 표준진단 요청. SIPN/SIPN South=계절 SIE·얼음경계 예측 상호비교(IIEE·SPS). CMEMS/Copernicus Marine 해빙 예보 검증(SIC·edge·drift). OSI SAF/NSIDC=위성 SIC·drift·edge 기준자료·검증보고서.
- 적용 도메인/자료형: 운영·기후 모델 [격자] vs 커뮤니티 기준자료.
- 입력·전제: 공통 격자·임계·마스크·매치업 규약. 지정 기준자료(위성 CDR·재분석) 사용. 리드타임·계절별 집계.
- 해석 기준(advisory): 기관·MIP 공통기준으로 모델 순위·개선추세 평가. 기준자료·규약 차이가 비교를 좌우 → 동일 프로토콜 준수. 절대판정보다 상호비교·불확실성 대비.
- 한계·주의: 기준자료 불확실성(위성 SIC 알고리즘차)·반구/해역 표본 편중. 규약 불일치가 왜곡. "참값" 없음(§G-1).
- 출처: Notz et al. (2016) "The CMIP6 Sea-Ice Model Intercomparison Project (SIMIP)," *Geoscientific Model Development* 9:3427–3446 (doi:10.5194/gmd-9-3427-2016, 확인요); Sea Ice Prediction Network (SIPN/SIPN South, arcus.org / Frontiers 2023); CMEMS/Copernicus Marine Sea Ice product QUID; OSI SAF/NSIDC validation reports.

---

## 출처 (References)

### 표준 참고문헌 / 지침 (실제 존재)
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (bias·RMSE·QQ·KS 등 공통 정의 — §01 참조).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide*, Wiley (범주형·Brier·ROC — §03 참조).
- WMO, *Sea Ice Nomenclature* (WMO-No. 259) — 해빙 유형·MIZ·egg code 용어 표준.
- Thomas, D. N. (ed.) *Sea Ice*, 3rd ed., Wiley-Blackwell (해빙 물리·관측 개관 — 확인요).

### 학술 논문 (웹으로 제목·저널·연도 확인; 권·페이지·DOI는 본문 병기, 미확인은 "확인요")
- Goessling, H. F., Tietsche, S., Day, J. J., Hawkins, E. & Jung, T. (2016) "Predictability of the Arctic sea ice edge," *Geophysical Research Letters*, 43(4), 1642–1650. (doi:10.1002/2015GL067232) — IIEE·분해(absolute/misplacement).
- Goessling, H. F. & Jung, T. (2018) "A probabilistic verification score for contours: Methodology and application to Arctic ice-edge forecasts," *Quarterly Journal of the Royal Meteorological Society*, 144. (doi:10.1002/qj.3242) — SPS(권/페이지 확인요).
- Zampieri, L., Goessling, H. F. & Jung, T. (2018) "Bright prospects for Arctic sea ice prediction on subseasonal time scales," *Geophysical Research Letters*, 45, 9731–9738. (doi:10.1029/2018GL079394)
- Palerme, C., Müller, M. & Melsom, A. (2019) "An intercomparison of verification scores for evaluating the sea ice edge position in seasonal forecasts," *Geophysical Research Letters*, 46. (doi:10.1029/2019GL082482) — MHD·SPS 상호비교(권/페이지 확인요).
- Melsom, A., Palerme, C. & Müller, M. (2019) "Validation metrics for ice edge position forecasts," *Ocean Science*, 15, 615–630. (doi:10.5194/os-15-615-2019) — 15개 얼음경계 변위지표·권장 3지표.
- Dukhovskoy, D. S. et al. (2015) "Skill metrics for evaluation and comparison of sea ice models," *Journal of Geophysical Research: Oceans*, 120. (권/페이지·doi 확인요) — Modified Hausdorff 권장.
- Notz, D. (2014) "Sea-ice extent and its trend provide limited metrics of model performance," *The Cryosphere*, 8, 229–243. (doi 확인요)
- Notz, D. et al. (2016) "The CMIP6 Sea-Ice Model Intercomparison Project (SIMIP): understanding sea ice through climate-model simulations," *Geoscientific Model Development*, 9, 3427–3446. (doi:10.5194/gmd-9-3427-2016, 확인요)
- Ivanova, N. et al. (2015) "Inter-comparison and evaluation of sea ice algorithms," *The Cryosphere*, 9, 1797–1817. (doi:10.5194/tc-9-1797-2015, 확인요)
- Ricker, R., Hendricks, S., Kaleschke, L., Tian-Kunze, X., King, J. & Haas, C. (2017) "A weekly Arctic sea-ice thickness data record from merged CryoSat-2 and SMOS," *The Cryosphere*, 11, 1607–1623. (doi:10.5194/tc-11-1607-2017, 확인요)
- Laxon, S. W. et al. (2013) "CryoSat-2 estimates of Arctic sea ice thickness and volume," *Geophysical Research Letters*, 40. (확인요)
- Kwok, R. et al. (2020) ICESat-2 sea ice thickness, *Journal of Geophysical Research: Oceans*. (권/페이지·doi 확인요)
- Lavergne, T. et al. (2023) "A climate data record of year-round global sea-ice drift from EUMETSAT OSI SAF," *Earth System Science Data*, 15, 5807–5834. (doi:10.5194/essd-15-5807-2023)
- Warren, S. G. et al. (1999) "Snow depth on Arctic sea ice," *Journal of Climate*, 12, 1814–1829. (확인요)
- Zhang, J. & Rothrock, D. A. (2003) "Modeling global sea ice with a thickness and enthalpy distribution model (PIOMAS)," *Monthly Weather Review*, 131, 845–861. (확인요)
- Schweiger, A. et al. (2011) "Uncertainty in modeled Arctic sea ice volume," *Journal of Geophysical Research: Oceans*, 116, C00D06. (확인요)
- Thorndike, A. S., Rothrock, D. A., Maykut, G. A. & Colony, R. (1975) "The thickness distribution of sea ice," *Journal of Geophysical Research*, 80, 4501–4513. (확인요)
- Hibler, W. D. III (1979) "A dynamic thermodynamic sea ice model," *Journal of Physical Oceanography*, 9, 815–846. (확인요)
- Stammerjohn, S. et al. (2012) "Regions of rapid sea ice change," *Geophysical Research Letters*, 39, L06501. (doi:10.1029/2012GL050874, 확인요)
- Strong, C. & Rigor, I. G. (2013) "Arctic marginal ice zone trending wider in summer and narrower in winter," *Geophysical Research Letters*, 40, 4864–4868. (확인요)
- Horvat, C. (2021) "Marginal ice zone fraction benchmarks sea ice and climate model skill," *Nature Communications*, 12. (doi 확인요)
- Tschudi, M. et al. (2019/2020) "EASE-Grid Sea Ice Age," NSIDC. (doi:10.5067/UTAV7490FEPB, 확인요)
- Dubuisson, M.-P. & Jain, A. K. (1994) "A modified Hausdorff distance for object matching," *Proc. 12th ICPR*. (MHD 원 정의)

### 웹 자료·기관 (조사 시 직접 참조)
- EUMETSAT OSI SAF — Sea Ice Concentration / Sea Ice Drift / Sea Ice Edge products & validation reports: https://osi-saf.eumetsat.int (osisaf-hl.met.no validation reports)
- NOAA/NSIDC — Sea Ice Concentration CDR, Sea Ice Index, Sea Ice Age, U.S. NIC MIZ (G10017): https://nsidc.org
- Sea Ice Prediction Network (SIPN / SIPN South): https://www.arcus.org/sipn ; Frontiers *Marine Science* (2023) SIPN South 6-year summary.
- Melsom et al. (2019) *Ocean Science* 15:615–630: https://os.copernicus.org/articles/15/615/2019/
- Copernicus Marine (CMEMS) Sea Ice products & QUID(quality info documents).

### 확인요 (웹에서 권/페이지·DOI 1차 확인 못 했거나 정정한 항목)
- 본문 각 카드의 "(확인요)" 표시 논문은 제목·저널·연도는 확인했으나 정확한 권·페이지·DOI는 인용 전 원문 재확인 필요(DOI 임의 생성 금지 원칙).
- Melsom et al. (2019) DOI는 **10.5194/os-15-615-2019** (본문 한 곳의 오탈자 정정 표기).
- GLORYS/재분석의 해빙변수(SIC/두께/drift) 직접 제공 여부·정의는 자료별 확인요(해빙 대조군은 OSI SAF·NSIDC CDR·CS2SMOS·PIOMAS·ORAS5 권장).
- PIOMAS·위성 두께·위성 나이는 **관측이 아니라 (동화)모델·유도 산물** → "참값" 아님(§G-1). 검증문에서 "reference/reanalysis 대비"로 표기.

> 주의(§F·§G 준수): 위 논문의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것. 해석 임계는 모두 **advisory**이며 해역·해상도·계절·기준자료 불확실성에 크게 의존한다. 어떤 지표도 단독으로 "좋음/나쁨"을 단정하지 말고 최소 정확도+편향+공간/거리 축을 함께 보고한다.
