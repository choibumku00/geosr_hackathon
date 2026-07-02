# 도메인: 강수 (Precipitation) 검증·분석 방법 카탈로그

이 문서는 수치모델·재분석·위성·레이더의 **강수(precipitation)** 산출물을 우량계(rain gauge) 관측소·격자 관측/재분석(ERA5, GPCP, IMERG, CMORPH 등)·레이더 QPE와 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 강수는 다른 대기변수와 근본적으로 다른 통계 성질을 가진다 — (1) **간헐성(intermittency)**: 값의 상당수가 0(무강수)이고 wet/dry 이진 성격이 강함, (2) **비대칭·두꺼운 꼬리(skewed, heavy-tailed)** 분포로 극치가 지배적, (3) **불연속·공간 국소성(patchy)**으로 위치 오차가 double-penalty를 유발. 따라서 연속 오차지표(RMSE 등)만으로는 부족하며, **범주형 분할표(POD/FAR/CSI/ETS/HSS/PSS/FBI)·드문사건 지수(EDI/SEDI)·이웃 검증(FSS)·객체기반(SAL/MODE/CRA)·분포(강수일빈도·강도 PDF·Q-Q)·극치(POT-GPD/GEV/ETCCDI)·스케일 분리(intensity-scale 웨이블릿)**가 강수 검증의 1급 도구다. 정점(우량계) 시계열과 격자·위성/레이더 자료형을 모두 1급으로 다룬다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3·L4/레이더 QPE), [시계열]=우량계·AWS 관측소 CSV/텍스트(정점), [트랙/스와스]=위성 저궤도 관측(GPM DPR 등), [분포]=시간정렬 불필요한 통계적 비교.
> **"우리 모델 vs 관측/재분석/위성·레이더" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 방법 교차링크**: RMSE·MAE·bias·상관·Taylor·target·bootstrap·QQ·KS·PDF 등 도메인 무관 지표는 여기서 재정의하지 않고 `01_error_statistics.md`(정확도), `02_spatial_pattern_verification.md`(공간패턴), `03_categorical_event_extremes.md`(범주·확률·극값), `06_timeseries_signal.md`(시계열), `figures/16`(그림 카탈로그)로 **교차링크**만 한다. 이 카드는 강수 고유 처리(0 처리·변환·임계·간헐성)만 상술한다.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **강수 전처리·변환 (0 처리 / log·√·Box–Cox / 누적기간 정합 / 게이지 undercatch)** — 강수 검증의 필수 게이트
- ★ **연속 오차통계의 강수 적용 (bias·MAE·RMSE·PBIAS·상관)** — 01 교차링크 + 강수 주의점
- ★ **wet-day 빈도·강수확률 (wet-day frequency, P(rain))** — 간헐성 1차 진단
- ★ **강수강도 PDF / 강도별 기여 (intensity histogram, SDII, amount·frequency 분해)** — 분포 형상
- ★ **Q-Q plot / 분위수 편향 (quantile bias)** — 분포·꼬리 일치 (01/03 교차링크 + 강수 특화)
- **Perkins Skill Score (PDF 중첩도)** — 분포 겹침 정량
- ★ **범주형 2×2 분할표 기본 (contingency table: FBI·POD·FAR·SR·POFD)** — 임계 초과 사건 탐지
- ★ **CSI / GSS(ETS) (Critical Success Index / Gilbert Skill Score)** — 강수 표준 스킬
- ★ **HSS / PSS (Heidke / Peirce Skill Score)** — 우연·기저율 보정 스킬
- **다범주 검증 (multi-category: 강수 계급 HSS·Gerrity·SEEPS)** — 3계급 이상
- ★ **드문사건 지수 (EDI / SEDI / EDS)** — 극한 강수 임계에서 비퇴화 지표
- ★ **이웃(퍼지) 검증 / FSS (Fractions Skill Score)** — double-penalty 완화·유효스케일
- ★ **double-penalty 진단** — 고해상도 강수의 위치 오차 함정
- **intensity-scale 웨이블릿 검증 (Casati ISS)** — 강도×스케일 오차 분해
- ★ **객체기반 SAL (Structure–Amplitude–Location)** — 강수장 구조·양·위치 3성분
- **객체기반 MODE (Method for Object-based Diagnostic Evaluation)** — 객체 속성·매칭
- **객체기반 CRA (Contiguous Rain Area)** — 위치·양·패턴 오차 분해
- ★ **극치강수 — POT-GPD / 연최대-GEV / 재현주기** — 설계강우·호우 재현값
- ★ **ETCCDI 강수 극한지수 (Rx1day·Rx5day·R95pTOT·SDII·CDD·CWD·R20mm 등)** — 표준 기후 극한
- ★ **위성강수 매치업 검증 (IMERG/GPM·CMORPH·GSMaP vs 우량계/레이더)** — 연속+범주 동시
- ★ **레이더 QPE 검증과 우량계 보정 (radar–gauge merging: MFB·KED·conditional merging)** — QPE 편의·병합
- ★ **공간 bias/RMSE·상관 지도 (gridded map difference)** — 면적 계통오차 지리 분포 (02 교차링크)
- **확률·앙상블 강수 검증 (Brier/BSS·ROC·reliability·CRPS·rank hist)** — 03 교차링크 + 강수 임계
- **강수 계절성·일변동 검증 (diurnal cycle·seasonal cycle·강수 harmonics)** — 위상·진폭 (06 교차링크)
- **강수 마스크·wet/dry 공간패턴 (rain area·패턴상관·ACC)** — 강수역 재현
- ★ **운영·기관 검증 프레임워크 (WMO/WWRP-JWGFVR, MET/METplus, GPM Ground Validation)** — 표준 절차

---

### ★ 강수 전처리·변환 (0 처리 / log·√·Box–Cox / 누적기간 정합 / 게이지 undercatch)
- 무엇을 측정/검증하나: 검증 자체가 아니라 **모든 강수 검증의 필수 선행 게이트**. 강수의 0값·비대칭·누적기간 불일치를 정렬하지 않으면 이후 모든 지표가 왜곡된다.
- 정의·수식: (1) **0 처리**: 강수는 mixed distribution(점질량 at 0 + 연속 양의 꼬리) → 로그 변환 시 log(x+ε) 또는 wet-only 서브셋 분리. (2) **분산안정 변환**: √x, log(x+1), Box–Cox로 우측 꼬리 압축(RMSE·상관의 극치 지배 완화). (3) **누적기간 정합**: 순간 강수율(flux) vs 누적량(amount)을 동일 창(1h·3h·일·월)으로 통일; 관측 관측시각(예: 09 KST 일강수)과 모델 누적창 정렬. (4) **게이지 undercatch 보정**: 바람에 의한 포집손실(고체강수에서 심함) — WMO SPICE 보정계수 고려.
- 적용 도메인/자료형: 모든 강수 [격자]/[시계열]/[트랙]. 검증 전 공통 전처리(`15_preprocessing_regridding_colocation.md`와 연결).
- 입력·전제: 모델·관측 **동일 단위**(mm, mm/h, kg m⁻² s⁻¹) 환산(1 kg m⁻² s⁻¹ = 86400 mm/day), **동일 누적창·동일 관측기준시각**, 재격자화 시 **보존적(conservative) 재격자**(강수는 면적 총량 보존이 중요 — bilinear은 총량 왜곡).
- 해석 기준(advisory): 변환·누적창·wet 임계(보통 0.1 또는 1 mm/day)를 **보고문에 반드시 명시**. 임계·변환 선택이 결과를 좌우하므로 단정 금지. 계절(겨울 고체강수)·지형(산악 undercatch)·해상도 의존 경고 동반.
- 한계·주의(§G): 누적창·기준시각 불일치는 인위적 bias의 최대 원천. bilinear 재격자는 강수 총량·극치를 뭉갬 → conservative 권장. 게이지 자체가 저평가(특히 강풍·눈)임을 "관측=참값"으로 오인 금지(§G-1). wet 임계 정의가 wet-day 빈도·범주 지표 전체를 바꾼다.
- 출처: WMO *Guidelines on the Calculation of Climate Normals* (WMO-No. 1203); Kochendorfer et al. (2017, *Hydrology and Earth System Sciences*, WMO-SPICE undercatch); Ebert (2001, *Monthly Weather Review*, 강수 검증 전처리 관행).

---

### ★ 연속 오차통계의 강수 적용 (bias·MAE·RMSE·PBIAS·상관 — 01 교차링크)
- 무엇을 측정/검증하나: 강수량의 평균 치우침(bias)·전체 오차(RMSE)·상대 편의(PBIAS)·선형 상관. 정의·수식은 재정의하지 않음 → `01_error_statistics.md`(bias/MAE/RMSE/CRMSD/상관/Taylor/target) 참조.
- 정의·수식: 공통 정의는 01 참조. 강수 특화: **PBIAS = 100·Σ(mᵢ−oᵢ)/Σoᵢ**(총량 상대편의, 위성·QPE 검증 표준). RMSE는 극치 지배가 심해 변환 후(√/log) 병행 권장.
- 적용 도메인/자료형: 강수량 [격자]/[시계열]/[트랙]. 위성·레이더 QPE 연속검증의 기본.
- 입력·전제: 정렬된 매치업, 동일 누적창·단위(위 전처리 카드 통과). 상관은 wet-only vs all-pairs를 구분 보고(0 다수 포함 시 상관이 인위적으로 상승).
- 해석 기준(advisory): PBIAS 부호=과대/과소. IMERG-우량계 검증 사례에서 CC·PBIAS·RMSE를 함께 보고하는 것이 관행(개별 사례값은 지역·계절·해상도 의존 — 절대기준 아님). 저강수·건조역에서 상대지표 불안정.
- 한계·주의(§G): 강수는 두꺼운 꼬리라 RMSE가 소수 극치에 지배됨 → 단독 사용 시 오도. 0을 포함한 상관은 wet/dry 일치가 상관을 부풀림(간헐성 artefact) → 범주 지표·분포 지표 병행 필수(§G-6 단일지표 금지). bias=0이 정확을 뜻하지 않음(양·음 상쇄).
- 출처: `01_error_statistics.md`; Wilks, *Statistical Methods in the Atmospheric Sciences*; Moriasi et al. (2007, *Transactions of the ASABE*, PBIAS 기준 — 수문 관행).

---

### ★ wet-day 빈도·강수확률 (wet-day frequency, P(rain ≥ threshold))
- 무엇을 측정/검증하나: 모델이 **비가 오는 빈도** 자체(간헐성)를 관측과 맞히는지. 강수량이 맞아도 빈도가 틀리면(예: 약한 비를 너무 자주 = "drizzle problem") 물리적으로 다른 강수. 강수 검증의 1차 간헐성 진단.
- 정의·수식: wet-day frequency f = (임계 초과일 수)/(전체 일 수), 임계는 통상 0.1 또는 1 mm/day. 모델·관측 f 비교; wet-day 강도 SDII = 총강수/wet-day 수(아래 카드와 연결). frequency bias FBI(범주 카드)와 직결.
- 적용 도메인/자료형: [시계열](우량계)·[격자]. 일·시간 단위.
- 입력·전제: 동일 wet 임계·동일 누적창. 모델 격자평균 vs 점 관측의 대표성 차이(격자는 면적평균이라 약한 비가 더 자주 나타나는 경향).
- 해석 기준(advisory): 모델이 wet-day를 과다·약강도 편향("too many wet days, too light") 보이는 것이 흔한 계통오차. 임계·해상도·격자대표성에 따라 크게 달라짐 → advisory. 관측망 밀도가 낮으면 격자 f 신뢰도 저하.
- 한계·주의(§G): wet 임계 정의가 결과를 좌우(0.1 vs 1 mm) → 반드시 명시. 점(게이지) vs 격자평균 대표성 오차. 총량이 맞아도 빈도·강도 분해가 어긋날 수 있어 amount/frequency 분해(아래) 병행.
- 출처: Dai (2006, *Journal of Climate*, "Precipitation characteristics in eighteen coupled climate models" — frequency/intensity 편향); Sun et al. (2006, *Journal of Climate*, 강수 빈도·강도 분해); Stephens et al. (2010, *JGR Atmospheres*, drizzle 문제).

---

### ★ 강수강도 PDF / 강도별 기여 (intensity histogram, SDII, amount·frequency 분해)
- 무엇을 측정/검증하나: 강수 **강도 분포**(약비~폭우)의 형상과, 총강수량에 대한 강도별 기여를 모델·관측 간 비교. 평균·총량이 못 보는 "약비 과다 / 강비 과소" 같은 분포 편향 포착.
- 정의·수식: 강도 계급별 히스토그램(빈도)과 계급별 강수량 기여(amount distribution). **SDII = 연총강수/wet-day 수**(ETCCDI). 흔히 총 편향을 Δmean = f·ΔI + I·Δf + Δf·ΔI 로 frequency(f)·intensity(I) 성분 분해.
- 적용 도메인/자료형: [시계열]/[격자]. 시간·일 강도.
- 입력·전제: 동일 누적창·wet 임계. 로그 간격 bin 권장(강도가 수십 배 범위). 표본 충분(고강도 bin은 희소).
- 해석 기준(advisory): 모델이 중간강도에 몰리고 극한강도 과소인 경우가 흔함. bin 경계·누적창·기후대(열대 convective vs 중위도 stratiform)에 의존 → advisory. QQ와 상보적(히스토그램=밀도, QQ=분위수).
- 한계·주의(§G): bin 선택이 형상 인상을 바꿈. 고강도 bin 표본희소로 불안정(부트스트랩 CI 권장). 격자평균은 강도 꼬리를 평활화(점 관측보다 극한 약함) → 자료형 대표성 명시.
- 출처: Dai (2006); Sun et al. (2006); Klein Tank, Zwiers & Zhang (2009, WMO-TD No. 1500, ETCCDI 지수·SDII).

---

### ★ Q-Q plot / 분위수 편향 (quantile bias — 01/03 교차링크 + 강수 특화)
- 무엇을 측정/검증하나: 모델·관측 강수 분위수를 대응시켜 분포 전체, 특히 **고분위(극한 강수) 꼬리**의 일치를 진단. 일반 정의·도표는 `01`/`03`/`figures/16` 참조 → 여기서는 강수 특화만.
- 정의·수식: 공통 QQ 정의는 01 참조. 강수 특화: **wet-only 분위수**(0 제외)로 그려 점질량 왜곡 제거; 상위 분위(95/99/99.9%)에 초점; QQ 기반 quantile mapping이 강수 편향보정의 표준(13/15 연결).
- 적용 도메인/자료형: [격자]/[시계열]/[트랙]. 분포 비교(시간정렬 불필요).
- 입력·전제: 동일 기간·동일 누적창·wet 임계 통일. 극단 분위는 표본 다수 필요.
- 해석 기준(advisory): 상위 분위에서 1:1선 아래로 휘면 극한 과소(모델 흔한 약점). 기후대·해상도·누적창 의존 → advisory. 격자평균은 상위 분위를 낮춤.
- 한계·주의(§G): 분포만 비교(동시성·상관은 못 봄) → 범주·연속지표 병행. 극단 분위 불안정. 0 포함 QQ는 계단 왜곡.
- 출처: `01_error_statistics.md`; Wilks; `13_model_intercomparison_downscaling.md`(quantile mapping).

---

### Perkins Skill Score (PDF 중첩도, PSS_Perkins)
- 무엇을 측정/검증하나: 모델·관측 강수 **확률밀도함수의 겹치는 면적**을 단일 값(0~1)으로 요약. 분포 유사성의 스칼라 지표.
- 정의·수식: S_score = Σ min(Z_model,i, Z_obs,i) — 각 bin에서 두 정규화 도수(빈도)의 최솟값 합. 1이면 완전 중첩, 0이면 무중첩. (Peirce PSS와 이름 혼동 주의 — 별개 지표.)
- 적용 도메인/자료형: [격자]/[시계열]. 강수 강도 분포.
- 입력·전제: 동일 bin·정규화. wet-only 또는 0 포함 여부 명시.
- 해석 기준(advisory): 1에 가까울수록 분포 유사. bin·표본에 민감 → advisory, 절대 등급화 지양.
- 한계·주의(§G): 분포만(위치·상관 무시). bin 경계 의존. Peirce Skill Score(PSS, 범주)와 약어 충돌 — 문서에 "Perkins" 명기.
- 출처: Perkins, Pitman, Holbrook & McAneney (2007, *Journal of Climate* 20(17), "Evaluation of the AR4 climate models' simulated daily maximum temperature, minimum temperature, and precipitation over Australia using probability density functions").

---

### ★ 범주형 2×2 분할표 기본 (contingency table: FBI·POD·FAR·SR·POFD)
- 무엇을 측정/검증하나: "강수가 임계(예: 0.1, 1, 10, 50 mm/day)를 넘었는가"라는 이진 사건의 탐지 성능. 강수 검증의 핵심 축. 공통 정의·전체 지표군은 `03_categorical_event_extremes.md` 참조 → 여기서는 강수 적용을 상술.
- 정의·수식: 2×2 분할표 (hit a, false alarm b, miss c, correct-negative d). **FBI(frequency bias)=(a+b)/(a+c)** (예보빈도/관측빈도, >1 과다예보), **POD(=hit rate)=a/(a+c)**, **FAR=b/(a+b)**, **SR(success ratio)=1−FAR=a/(a+b)**, **POFD=b/(b+d)**. 임계별로 반복.
- 적용 도메인/자료형: [시계열]/[격자]. 임계 스캔 필수(단일 임계 정보손실).
- 입력·전제: 정렬된 매치업 + 합의된 임계 집합. 격자 검증은 정확 위치일치 요구 → double-penalty 유발(아래 FSS로 완화).
- 해석 기준(advisory): POD↑·FAR↓·FBI≈1 양호. 임계↑(호우)일수록 사건 희소 → 지표 불안정·CI 필수. 성능도표(Roebber performance diagram)로 POD·SR·CSI·FBI 동시 시각화 권장.
- 한계·주의(§G): 단일 임계 결론 금지(여러 임계·ROC 병행). 격자 double-penalty(위치 조금 어긋나면 hit이 false+miss로 이중처벌). 희소 사건에서 FAR·POD 불안정.
- 출처: `03_categorical_event_extremes.md`; Jolliffe & Stephenson, *Forecast Verification*; Roebber (2009, *Weather and Forecasting* 24(2), performance diagram); WWRP/WGNE JWGFVR verification methods 페이지.

---

### ★ CSI / GSS(ETS) (Critical Success Index / Gilbert Skill Score = Equitable Threat Score)
- 무엇을 측정/검증하나: 강수 사건 탐지의 종합 스킬. CSI(=Threat Score)는 correct-negative를 제외한 적중률; GSS(ETS)는 우연 적중을 보정. 강수 QPF 검증의 가장 널리 쓰이는 스킬 점수.
- 정의·수식: **CSI(=TS)=a/(a+b+c)**. **GSS(ETS)=(a−a_random)/(a+b+c−a_random)**, a_random=(a+b)(a+c)/n (무작위 기대 hit). 범위: CSI 0~1, GSS −1/3~1(0=무스킬).
- 적용 도메인/자료형: [시계열]/[격자]. 임계별.
- 입력·전제: 정렬 매치업·임계. 표본 n·기저율(base rate)이 GSS 보정에 필요.
- 해석 기준(advisory): 높을수록 양호. **CSI·GSS는 기저율(사건 빈도)에 의존** — 임계가 높거나 건조역이면 낮게 나오는 것이 정상(모델 열등이 아닐 수 있음). 지역·계절·임계 간 직접 비교 주의(§G-4).
- 한계·주의(§G): CSI는 우연보정 없어 사건빈도 큰 곳에서 높게 나옴 → GSS 병행. 희소 극한 강수에서 GSS도 퇴화(0으로 수렴) → 드문사건 지수(EDI/SEDI) 사용. double-penalty 영향.
- 출처: `03_categorical_event_extremes.md`; Schaefer (1990, *Weather and Forecasting* 5(4), "The critical success index as an indicator of warning skill"); Gilbert (1884, *Monthly Weather Review*, GSS 원형); Hogan et al. (2010, *Quarterly Journal of the Royal Meteorological Society*, "Equitability revisited").

---

### ★ HSS / PSS (Heidke Skill Score / Peirce Skill Score = True Skill Statistic)
- 무엇을 측정/검증하나: 우연 대비 스킬을 다른 방식으로 보정한 이진(및 다범주) 스킬. HSS는 무작위 기대 대비 정확도 개선; PSS(=TSS=Hanssen–Kuipers)는 POD−POFD로 판별력.
- 정의·수식: **HSS = (PC − PC_random)/(1 − PC_random)**, PC=(a+d)/n. **PSS(=TSS)=POD − POFD = a/(a+c) − b/(b+d)**. 범위: HSS ≤1, PSS −1~1.
- 적용 도메인/자료형: [시계열]/[격자]. 임계별·다범주 확장 가능.
- 입력·전제: 완전 분할표(correct-negative d 포함). d가 매우 크면(건조역) 지표 성질이 바뀜.
- 해석 기준(advisory): HSS·PSS >0 무작위보다 나음. **PSS는 기저율에 덜 민감**하지만 희소사건에서 POD 지배로 불안정. 지역·임계 의존 → advisory.
- 한계·주의(§G): HSS는 correct-negative(d)에 민감 → 건조역에서 부풀 수 있음. PSS는 극히 드문 사건에서 사실상 POD로 퇴화 → EDI/SEDI 권장. 다범주 HSS는 계급 정의 명시.
- 출처: `03_categorical_event_extremes.md`; Jolliffe & Stephenson; Hanssen & Kuipers (1965, KNMI, PSS 원형); Heidke (1926, *Geografiska Annaler*, HSS 원형).

---

### 다범주 검증 (multi-category: 강수 계급 HSS·Gerrity·SEEPS)
- 무엇을 측정/검증하나: 강수를 3계급 이상(예: dry / light / heavy)으로 나눠 계급 예측 정확도를 종합. 특히 **SEEPS**는 ECMWF 운영 강수검증의 표준(dry·light·heavy 3범주, 기후 백분위 기반).
- 정의·수식: k×k 분할표. **다범주 HSS**(우연보정), **Gerrity Skill Score**(scoring matrix로 오분류 거리 가중), **SEEPS(Stable Equitable Error in Probability Space)**: 지역·계절 기후로 dry/light 경계(습윤일 하위 1/3)와 light/heavy 경계 설정 후 확률공간 오차. SEEPS는 1−skill 형태로 보고(작을수록 양호).
- 적용 도메인/자료형: [시계열]/[격자]. 일강수 표준.
- 입력·전제: 계급 경계 정의(SEEPS는 각 지점 기후 백분위 필요). 최소 30년급 기후 권장(SEEPS).
- 해석 기준(advisory): SEEPS는 지역기후로 정규화되어 지역 간 비교에 유리하나, 기후 표본·건조지 정의에 민감 → advisory. 계급 경계 변경이 결과를 바꿈.
- 한계·주의(§G): 계급 경계 임의성. SEEPS는 매우 건조한 지점(습윤일 <10%)에서 정의 곤란 → 제외 관행. 다범주 지표는 계급 정의를 반드시 병기.
- 출처: `03_categorical_event_extremes.md`; Rodwell, Richardson, Hewson & Haiden (2010, *Quarterly Journal of the Royal Meteorological Society* 136, "A new equitable score suitable for verifying precipitation in numerical weather prediction" — SEEPS); Gerrity (1992, *Monthly Weather Review* 120, Gerrity score); North et al. (2013, *Meteorological Applications* 20, SEEPS·SEDI 6h 강수 평가, doi:10.1002/met.1405).

---

### ★ 드문사건 지수 (EDI / SEDI / EDS — 극한 강수 임계)
- 무엇을 측정/검증하나: **호우·극한 강수처럼 임계가 높아 사건이 희소할 때** 기존 스킬(CSI·GSS·HSS)이 0으로 퇴화(base-rate degeneracy)하는 문제를 극복. 극치 임계에서도 비퇴화·기저율 독립 스킬.
- 정의·수식: hit rate H=a/(a+c), false alarm rate F=b/(b+d)로부터 **EDI = (log F − log H)/(log F + log H)**; **SEDI = [log F − log H − log(1−F) + log(1−H)] / [log F + log H + log(1−F) + log(1−H)]**. SEDI는 EDS·EDI의 결함(퇴화·기저율 의존·hedging 취약) 보완: **비퇴화(nondegenerating)·기저율 독립(base-rate independent)·점근 공정(asymptotically equitable)**.
- 적용 도메인/자료형: [시계열]/[격자]. 높은 강수 임계(예: 95/99 백분위, 50 mm/day).
- 입력·전제: 완전 분할표. H·F가 0/1이면 log 정의 불가 → 소표본 처리·부트스트랩 CI 필수.
- 해석 기준(advisory): 1에 가까울수록 양호, 0=무스킬. **기저율 독립**이 장점이나 극소표본에서 분산 큼 → CI 동반. 임계·표본에 여전히 민감(advisory).
- 한계·주의(§G): H 또는 F=0(완전적중/무오경보)이면 정의 붕괴 → 표본 확대·정규화. 여전히 이진사건(강도 정보 손실). 극한 임계 검증은 표본희소로 불확실 → 부트스트랩 필수.
- 출처: `03_categorical_event_extremes.md`; Ferro & Stephenson (2011, *Weather and Forecasting* 26(5), "Extremal dependence indices: Improved verification measures for deterministic forecasts of rare binary events"); Stephenson, Casati, Ferro & Wilson (2008, *Meteorological Applications* 15, EDS); North et al. (2013, *Meteorological Applications* 20, doi:10.1002/met.1405).

---

### ★ 이웃(퍼지) 검증 / FSS (Fractions Skill Score)
- 무엇을 측정/검증하나: 고해상도 강수 예보가 위치가 조금 어긋났을 때 격자단위 지표가 주는 **double-penalty를 완화**하고, "어느 공간 스케일부터 예보가 쓸모 있는가(useful scale)"를 진단. 강수 공간검증의 대표적 이웃(neighborhood) 방법.
- 정의·수식: 임계로 예보·관측을 이진화 후, 각 격자 주변 n×n 이웃에서 **초과 격자 비율(fraction)**을 계산. **FSS = 1 − MSE(fractions) / MSE_ref**, MSE_ref = [Σ P_f² + Σ P_o²]/N (완전 불일치 기준). 범위 0(무일치)~1(완전). **유효스케일(useful scale)**: FSS가 **0.5 + f₀/2**(f₀=관측 사건빈도)를 넘는 최소 이웃 크기.
- 적용 도메인/자료형: [격자] 강수(모델·레이더 QPE·위성). 임계×이웃크기 스캔.
- 입력·전제: 공통 격자로 정합된 모델·관측 [격자]. 임계·이웃크기 집합 지정. 관측장 필수(격자 관측/레이더/위성).
- 해석 기준(advisory): 작은 이웃에서 FSS 낮고 스케일 키우면 상승 → useful scale이 클수록 위치오차 큼. useful-scale 기준 0.5+f₀/2는 관행값(§G-4 advisory) — 영역·해상도·임계·사건빈도 의존.
- 한계·주의(§G): 임계·이웃크기 선택이 결과를 좌우 → 스캔·명시 필수. 강도 오차와 위치 오차를 분리하진 못함(이진화). 관측 격자 대표성·결측이 fraction을 왜곡.
- 출처: `02_spatial_pattern_verification.md`; Roberts & Lean (2008, *Monthly Weather Review* 136(1), "Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events"); Mittermaier & Roberts (2010, *Weather and Forecasting* 25); Skok & Roberts (2016, *QJRMS*, useful-scale 재검토).

---

### ★ double-penalty 진단
- 무엇을 측정/검증하나: 고해상도 강수 예보가 **위치가 약간 어긋난 강수 셀** 때문에 격자 지표(RMSE·CSI 등)에서 "놓침(miss)+오경보(false alarm)"로 **이중 처벌**받는 현상 자체를 인식·정량. 왜 이웃/객체 방법이 필요한지의 근거.
- 정의·수식: 개념적 진단. 완벽한 강도·형상이라도 Δx만큼 변위되면 RMSE가 강수 없는 예보(전부 0)보다 나빠질 수 있음. 진단: (a) 이웃 스케일↑ 시 FSS 급상승 여부, (b) 객체기반(SAL/CRA) 위치성분 분리, (c) 스무딩 후 지표 회복 정도.
- 적용 도메인/자료형: [격자] 고해상도 강수(대류허용 모델·AI 강수·나우캐스팅).
- 입력·전제: 고해상도 모델·관측 [격자] 쌍.
- 해석 기준(advisory): 해상도가 높고 강수가 국소·대류성일수록 double-penalty 심함. "격자 RMSE·CSI가 나쁘다"를 곧 "모델이 나쁘다"로 단정 금지 — 위치오차인지 강도오차인지 이웃/객체 검증으로 구분해야 함.
- 한계·주의(§G): double-penalty를 무시하면 고해상도·AI 강수모델을 부당하게 저평가(§G-6, AI 산출물 추가축 강제). 반대로 과도한 스무딩은 실제 오차를 감춤.
- 출처: `02_spatial_pattern_verification.md`, `14_ai_ml_evaluation.md`; Gilleland, Ahijevych, Brown, Casati & Ebert (2009, *Weather and Forecasting* 24(5), "Intercomparison of spatial forecast verification methods" — ICP 총론); Rossa, Nurmi & Ebert (2008, in *Precipitation: Advances in Measurement, Estimation and Prediction*, Springer).

---

### intensity-scale 웨이블릿 검증 (Casati Intensity-Scale Skill Score, ISS)
- 무엇을 측정/검증하나: 강수 예보 오차를 **강수 강도 × 공간 스케일**의 2차원으로 분해. 어느 강도·어느 스케일에서 스킬이 있는지/없는지 진단(대류 소규모 강비 vs 광역 약비).
- 정의·수식: 예보·관측을 임계로 이진화한 차이장에 **Haar 웨이블릿 다해상도 분석(MRA)** 적용, 각 스케일별 MSE로부터 **ISS = 1 − MSE_scale / MSE_random**를 강도·스케일 격자로 표. Briggs & Levine(1997) 웨이블릿 검증을 강수용으로 확장.
- 적용 도메인/자료형: [격자] 강수. 정사각(2ⁿ) 도메인 필요(패딩).
- 입력·전제: 공통 격자·2의 거듭제곱 크기. 임계 이진화. 결측 없음(또는 채움).
- 해석 기준(advisory): 큰 스케일·중간강도에서 스킬 높고 소규모·극한강도에서 낮은 패턴이 흔함. 웨이블릿 종류·이진화 임계·도메인 크기 의존 → advisory.
- 한계·주의(§G): 2ⁿ 격자·주기경계 가정. 이진화가 강도 연속성 손실. 해석이 FSS보다 덜 직관적. 결측·비정사각 도메인 처리 주의.
- 출처: `02_spatial_pattern_verification.md`, `05_spectral_eof_modal.md`; Casati, Ross & Stephenson (2004, *Meteorological Applications* 11(2), "A new intensity-scale approach for the verification of spatial precipitation forecasts"); Casati (2010, *Weather and Forecasting* 25, 재정식화); Weniger, Kapp & Friederichs (2017, *QJRMS*, 웨이블릿 검증 리뷰).

---

### ★ 객체기반 SAL (Structure–Amplitude–Location)
- 무엇을 측정/검증하나: 강수장을 **구조(S)·양(A)·위치(L)** 3성분으로 나눠 진단. RMSE의 double-penalty를 피하고 "무엇이 틀렸는가"(총량 과다? 객체가 너무 큼? 위치가 밀림?)를 해석 가능하게 분해.
- 정의·수식: 도메인 내 강수 객체를 임계(예: R* = 최대의 1/15 또는 상위 백분위)로 식별. **A**=(⟨R_f⟩−⟨R_o⟩)/(0.5(⟨R_f⟩+⟨R_o⟩)) 도메인평균 상대편차(−2~2). **L**=L1+L2, L1=질량중심 변위/최대거리, L2=객체별 가중평균 산포거리 차. **S**=객체 부피/최대값 비 기반 크기·형상 지표(−2~2). 세 성분 모두 0이면 완전 일치. **객체 매칭 불필요**(변위 double-penalty 회피).
- 적용 도메인/자료형: [격자] 강수(모델 vs 레이더/위성/관측격자). 정해진 도메인 단위.
- 입력·전제: 공통 격자·정의된 도메인. 객체 식별 임계 R* 지정. 도메인 크기로 정규화(도메인 간 비교 가능).
- 해석 기준(advisory): A>0 총량 과다, S>0 객체 과대/과평활, L>0 위치·산포 오차. R* 임계·도메인 정의에 민감 → advisory. 단일 대류셀 vs 광역 강수에서 성분 해석 달라짐.
- 한계·주의(§G): 객체 식별 임계가 S·L을 좌우. 도메인이 크면 여러 강수계 혼재로 성분 해석 모호. A는 총량만(공간분포 무시) → S·L과 함께 해석.
- 출처: `02_spatial_pattern_verification.md`, `03_categorical_event_extremes.md`; Wernli, Paulat, Hagen & Frei (2008, *Monthly Weather Review* 136(11), "SAL—A novel quality measure for the verification of quantitative precipitation forecasts", doi:10.1175/2008MWR2415.1); Wernli, Hofmann & Zimmer (2009, *Weather and Forecasting* 24, SAL 적용).

---

### 객체기반 MODE (Method for Object-based Diagnostic Evaluation)
- 무엇을 측정/검증하나: 강수 객체를 개별 식별·매칭하고 **속성별 오차(면적·강도·중심·방향·종횡비)**를 정량. SAL보다 세밀한 객체 대응·속성 비교 제공. MET/METplus에 구현.
- 정의·수식: (1) convolution(평활)+임계로 객체 식별, (2) 예보·관측 객체 쌍의 속성(중심거리·면적비·교차각·강도분위 등)으로 **fuzzy-logic total interest**(0~1) 산출, (3) interest 임계로 매칭. 매칭 객체의 속성차·매칭률로 진단.
- 적용 도메인/자료형: [격자] 강수. 대류셀·강수계 단위.
- 입력·전제: 공통 격자. convolution 반경·임계·interest 가중치 지정(결과가 이 파라미터에 의존).
- 해석 기준(advisory): 매칭 객체의 중심거리·면적비로 위치·크기 오차 해석. **평활반경·임계·가중치를 고정·명시**해야 재현·비교 가능(§G-4). 강수 유형별 파라미터 민감.
- 한계·주의(§G): 파라미터(평활·임계·가중치)에 강하게 의존 → 반드시 보고. 객체 정의가 모호한 광역·확산 강수에서 불안정. 매칭 안 된 객체 처리 규칙 명시.
- 출처: `02_spatial_pattern_verification.md`; Davis, Brown & Bullock (2006, *Monthly Weather Review* 134, "Object-based verification of precipitation forecasts, Part I/II"); Davis, Brown, Bullock & Halley-Gotway (2009, *Weather and Forecasting* 24(5), MODE 적용); DTC MET/METplus User's Guide(MODE-Tool).

---

### 객체기반 CRA (Contiguous Rain Area)
- 무엇을 측정/검증하나: 연속 강수역(CRA)을 최적 이동(pattern matching)으로 정렬해 총오차를 **위치(displacement)·양(volume/amplitude)·미세패턴(pattern)** 오차로 분해. 초기 객체기반 검증법으로 위치오차 정량의 원형.
- 정의·수식: 사용자 지정 등우량선(isohyet)으로 CRA 정의 → 예보 CRA를 관측에 맞춰 이동해 상관 최대(또는 MSE 최소)인 변위 탐색 → **MSE_total = MSE_displacement + MSE_volume + MSE_pattern**로 분해.
- 적용 도메인/자료형: [격자] 강수계(특히 이동성 시스템·TC 강우). 
- 입력·전제: 공통 격자. isohyet 임계·최대 탐색변위 지정. 관측 격자 필수.
- 해석 기준(advisory): 위치성분이 크면 변위오차 지배. 매칭 기준(상관 vs MSE)·임계에 따라 분해가 달라짐 → advisory. 여러 CRA 겹침 시 매칭 모호.
- 한계·주의(§G): isohyet 임계·탐색범위 의존. 강수계가 병합/분리되면 CRA 정의 불안정. 분해가 매칭 기준에 민감.
- 출처: `02_spatial_pattern_verification.md`; Ebert & McBride (2000, *Journal of Hydrology* 239, "Verification of precipitation in weather systems: Determination of systematic errors"); Ebert & Gallus (2009, *Weather and Forecasting* 24(5), CRA 재검토).

---

### ★ 극치강수 — POT-GPD / 연최대-GEV / 재현주기
- 무엇을 측정/검증하나: 모델·재분석·위성이 **극한 강수와 재현주기(return period) 설계강우**를 관측과 일치시키는지. 방재·수공 설계의 핵심. 일반 극값이론 엔진은 `03_categorical_event_extremes.md`와 공유 → 여기서는 강수 특화.
- 정의·수식: (1) **연최대(AM) → GEV** 적합(위치·척도·형상 μ,σ,ξ). (2) **임계초과(POT) → GPD**(일반파레토) 적합 + 평균초과율 λ로 N년 재현값 산출. 강수 특화: 임계는 wet-day 상위 백분위(예: 95~99%), declustering으로 폭우일 독립성 확보, 형상 ξ>0(두꺼운 꼬리)이 강수의 전형.
- 적용 도메인/자료형: 장기 [시계열](우량계)·[격자] hindcast/재분석. 일·시간 극한.
- 입력·전제: 충분히 긴 동질 기간(가능하면 ≥30년). 독립 극값(declustering). 비정상성(기후변화·계절)·격자 대표성 고려.
- 해석 기준(advisory): 재현주기별 강수(50·100년) 신뢰구간 겹침으로 판정. QQ로 꼬리 적합 점검. **격자평균은 점 극치를 과소** → 자료형 대표성 명시. 임계·declustering·표본에 큰 민감도(부트스트랩 CI 필수).
- 한계·주의(§G): 임계 선택·declustering이 재현값을 크게 바꿈. 격자 vs 점 극치의 areal reduction factor(ARF) 차이. 짧은 기록·비정상성에서 재현값 불확실. 위성·레이더 극치는 알고리즘 saturation 주의.
- 출처: `03_categorical_event_extremes.md`; Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Katz, Parlange & Naveau (2002, *Advances in Water Resources* 25, "Statistics of extremes in hydrology").

---

### ★ ETCCDI 강수 극한지수 (Rx1day·Rx5day·R95pTOT·SDII·CDD·CWD·R10mm·R20mm·PRCPTOT)
- 무엇을 측정/검증하나: 국제 표준 **기후 극한지수**로 모델·재분석·위성의 강수 극한·간헐성 통계를 관측과 비교. 기후 스케일 강수 검증·다운스케일 평가의 공용어.
- 정의·수식(주요): **Rx1day**=연 최대 1일 강수, **Rx5day**=연 최대 연속 5일 강수, **R95pTOT**=기준기간(예:1961–1990) wet-day 95백분위 초과일의 연총강수, **SDII**=연총강수/wet-day(≥1mm) 수, **CDD**=최대 연속 건조일(<1mm), **CWD**=최대 연속 습윤일(≥1mm), **R10mm/R20mm**=일강수≥10/20mm 일수, **PRCPTOT**=wet-day 연총강수. (전체 27지수 중 강수 관련.)
- 적용 도메인/자료형: 일강수 [시계열]/[격자]. 기후(다년) 비교.
- 입력·전제: 일강수·동일 wet 임계(1mm)·동일 기준기간(백분위 지수). 결측 규칙(연간 결측일 한도) 통일. R95p류는 기준기간 정의가 값을 좌우.
- 해석 기준(advisory): 지수별 bias/RMSE·패턴상관·Taylor로 비교. **기준기간·결측처리·격자대표성**에 민감 → advisory. 격자평균은 Rx1day 등 극한을 과소.
- 한계·주의(§G): 기준기간 불일치 시 R95p·백분위 지수 비교 무효. wet 임계(1mm) 고정 필수. 격자 vs 점 대표성. climdex/icclim 등 표준 구현 사용 권장(수식 재구현 오류 방지).
- 출처: Zhang et al. (2011, *WIREs Climate Change* 2, "Indices for monitoring changes in extremes based on daily temperature and precipitation data"); Klein Tank, Zwiers & Zhang (2009, WMO-TD No. 1500 / WCDMP-72, ETCCDI 지침); Karl, Nicholls & Ghazi (1999, *Climatic Change*, CCl/CLIVAR 지수 기원).

---

### ★ 위성강수 매치업 검증 (IMERG/GPM·CMORPH·GSMaP vs 우량계/레이더)
- 무엇을 측정/검증하나: 위성강수 산출물([격자] L3/L4 또는 [트랙])을 우량계·레이더 QPE와 비교해 **연속(양)+범주(탐지)** 정확도를 동시 진단. 위성강수는 관측이 성긴 해역·산악의 유일한 광역 강수원이라 검증이 특히 중요.
- 정의·수식: 연속: bias/PBIAS/RMSE/CC(위 연속 카드) + 범주: POD/FAR/CSI(위 범주 카드)를 함께. GPM DPR(레이더)·GMI(마이크로파)·IMERG(다위성 병합) 등 산출물별. 매치업은 위성 격자에 우량계 point-to-pixel 또는 우량계 격자화 후 grid-to-grid.
- 적용 도메인/자료형: 위성 [격자]/[트랙] vs 우량계 [시계열] / 레이더 [격자]. 30분~월 다양한 누적.
- 입력·전제: 동일 누적창(IMERG 30분·일 등), point-to-pixel 대표성 오차 인지, 위성 QC(coast/기온·지형 오염, IR-only 시간대), 우량계 밀도. IMERG는 Early/Late(준실시간)/Final(게이지 보정) 버전 구분 — Final은 GPCC 게이지가 이미 반영되어 우량계와 독립 아님(§G-3).
- 해석 기준(advisory): 열대·convective에서 탐지 양호, 약비·고체강수·산악·연안에서 저조가 흔함. 산출물·버전·누적창·기후대에 강하게 의존 → advisory. IMERG-우량계 CC·POD·CSI 사례값은 지역별로 크게 다름(절대기준 아님).
- 한계·주의(§G): IMERG **Final은 게이지 보정 산물** → 우량계로 "독립 검증" 시 오차 상관(§G-2/3, TC에 독립 3자로 부적합). point vs pixel 대표성 오차. 위성은 순간 관측→누적 표현에 sampling 오차. 고체강수·약강수 탐지 취약.
- 출처: Huffman et al. (2020, in *Satellite Precipitation Measurement*, Springer, "Integrated Multi-satellitE Retrievals for GPM (IMERG)"); Kidd & Levizzani (2011, *HESS* 15, 위성강수 검증 리뷰); Tang et al. (2020, *Remote Sensing of Environment*, IMERG V06 평가); Maggioni, Meyers & Robinson (2016, *Journal of Hydrometeorology* 17, 위성강수 오차 리뷰).

---

### ★ 레이더 QPE 검증과 우량계 보정 (radar–gauge: MFB·KED·conditional merging)
- 무엇을 측정/검증하나: 레이더 정량강수추정(QPE)의 우량계 대비 편의(Z–R 관계·밝은띠·빔차폐·감쇠 기인)를 검증하고, 레이더의 공간패턴 + 우량계의 국소정확도를 **병합(merging)**해 기준 격자강수를 생성. 격자 강수검증의 관측 기준(reference) 자체를 만드는 단계이기도 함.
- 정의·수식: 편의 진단: 우량계-레이더 쌍의 G/R 비·PBIAS·산점. 병합법: **MFB(mean-field bias)** 전역 배수보정, **RIDW/RK(regression kriging)**, **KED(kriging with external drift)** — 레이더를 외부드리프트로 크리깅, **conditional merging** — 우량계 크리깅 + 레이더 편차 크리깅 결합(공간패턴 보존). 
- 적용 도메인/자료형: 레이더 [격자] + 우량계 [시계열]. 시간~일 누적.
- 입력·전제: 우량계 밀도·품질, 레이더 QC(clutter·brightband·beam blockage·attenuation 보정), 동일 시각·누적. 지형(빔차폐)·거리(range degradation) 의존.
- 해석 기준(advisory): KED·conditional merging이 미세 공간패턴을 잘 보존한다는 보고가 많으나, **우량계 밀도·지형·강수유형에 강하게 의존** → advisory. 특정 병합법의 우열은 지역·사건별로 다름.
- 한계·주의(§G): 병합 산물은 **우량계가 이미 반영**되어 그 우량계로 재검증하면 독립 아님(§G-3, 교차검증·leave-one-out 필요). 저밀도 우량계에서 크리깅 불안정. 레이더 QC 미흡 시 병합이 오차 전파. 산악 빔차폐역은 근본적 한계.
- 출처: `15_preprocessing_regridding_colocation.md`(matchup·kriging); Sinclair & Pegram (2005, *Atmospheric Science Letters* 6, conditional merging); Goudenhoofdt & Delobbe (2009, *HESS* 13, "Evaluation of radar-gauge merging methods for quantitative precipitation estimates"); Berndt, Rabiei & Haberlandt (2014, *Journal of Hydrology* 508, 병합법 비교).

---

### ★ 공간 bias/RMSE·상관 지도 (gridded map difference — 02 교차링크)
- 무엇을 측정/검증하나: 우리 모델 [격자]를 격자 관측/재분석/위성강수 [격자]와 **면적 전면적**으로 비교해 bias·RMSE·상관·PBIAS의 지리적 분포를 지도화. 점 관측이 없는 곳까지 계통오차 위치(산악 과대·해양 과소 등)를 진단. 일반 공간지표는 `02`/`figures/16` 참조 → 강수 특화만.
- 정의·수식: 공통 격자로 **보존적 재격자화** 후 격자점 시계열에 bias(x,y)·RMSE(x,y)·PBIAS(x,y)·상관(x,y) 산출 → 지도. 패턴상관/ACC(anomaly correlation)는 강수 아노말리에 적용(동일 climatology 강제).
- 적용 도메인/자료형: 강수 [격자] vs [격자](관측격자·ERA5·IMERG). NetCDF↔NetCDF.
- 입력·전제: 시간축·격자·달력·단위 정렬, **강수는 보존적 재격자**(총량 보존), land-sea/결측 마스크 통일. 관측격자 자체 불확실성(게이지 밀도) 인지.
- 해석 기준(advisory): 계통 bias 띠(산악 상풍측 과대, 풍하측 과소 등)의 위치·계절성 파악. 재분석·위성은 "참값"이 아님(§G-1) → 우량계 검증과 교차. 해상도·재격자법 차이가 차이의 상당부분(advisory).
- 한계·주의(§G): 재분석·위성강수는 독립 진값 아님(§G-1). bilinear 재격자는 강수 총량·극치 왜곡 → conservative 필수. 관측격자 게이지 밀도 편중이 지역 신뢰도를 좌우. 강수 상관은 간헐성 artefact 주의(0 다수).
- 출처: `02_spatial_pattern_verification.md`, `13_model_intercomparison_downscaling.md`; Hersbach et al. (2020, *QJRMS* 146, ERA5); Adler et al. (2003, *Journal of Hydrometeorology* 4, GPCP 격자강수 — 기준자료).

---

### 확률·앙상블 강수 검증 (Brier/BSS·ROC·reliability·CRPS·rank histogram — 03 교차링크)
- 무엇을 측정/검증하나: 앙상블/확률 강수예보의 신뢰도(reliability)·해상도(resolution)·예리함(sharpness). 정의·수식은 `03_categorical_event_extremes.md`·`13`·`14` 참조 → 여기서는 강수 임계 특화.
- 정의·수식: 공통 정의는 03 참조. 강수 특화: 임계 초과확률(예: P(≥10mm))에 **Brier Score/BSS·reliability diagram·ROC/AUC**; 연속 강수량에 **CRPS**(변환·검열 강수에 fair-CRPS·censored 처리); rank histogram으로 spread 적정성; 극한 임계는 **twCRPS(threshold-weighted)**로 꼬리 강조.
- 적용 도메인/자료형: 앙상블 강수 [격자]/[시계열]. 임계·누적창별.
- 입력·전제: 앙상블 멤버 또는 예보분포, 관측 진값, 충분 사례. 강수 임계 정의.
- 해석 기준(advisory): BS/CRPS 작을수록, BSS/CRPSS>0이면 기준보다 우수. reliability 대각선=잘 보정, ROC AUC>0.5 판별력. rank histogram U자=과소분산. 임계·기후대 의존(advisory).
- 한계·주의(§G): 결정론 단일모델엔 부적용(앙상블 전용). 희소 극한 임계에서 BS·ROC 불안정. CRPS는 강수 0질량·꼬리 처리 유의.
- 출처: `03_categorical_event_extremes.md`, `13`, `14`; Hersbach (2000, *Weather and Forecasting* 15(5), CRPS); Jolliffe & Stephenson.

---

### 강수 계절성·일변동 검증 (diurnal cycle·seasonal cycle·harmonics — 06 교차링크)
- 무엇을 측정/검증하나: 강수의 **일변동(diurnal cycle)** 위상(첨두 시각)·진폭과 **계절 사이클**을 모델이 재현하는지. 특히 대류강수 일변동 위상오차는 물리모수화 결함의 지표. 시계열 도구는 `06_timeseries_signal.md` 참조 → 강수 특화만.
- 정의·수식: 시각별/월별 평균 강수의 **1차 조화(harmonic) 적합**으로 위상(첨두시각)·진폭 추출, 모델-관측 위상차·진폭비 비교. 벡터 평균(원형)으로 첨두시각 표현.
- 적용 도메인/자료형: [시계열]/[격자]. 아일리(hourly) 자료 필요(일변동).
- 입력·전제: 시간대(UTC/LST) 통일, 충분한 표본(다일·다년 합성). 위성은 관측시각 편중 주의.
- 해석 기준(advisory): 모델이 대류강수 첨두를 **너무 이르게(정오 무렵)** 모의하는 편향이 흔함(관측은 오후~야간). 지형·기후대·해상도 의존 → advisory. 대류허용 모델이 위상 개선 경향.
- 한계·주의(§G): 시간대·관측 sampling 오차(특히 위성). 조화적합은 다봉(이중 첨두) 일변동을 단순화. 첨두시각은 원형통계(0/24 wrap) 처리.
- 출처: `06_timeseries_signal.md`; Dai (2001, *Journal of Climate* 14, "Global precipitation and thunderstorm frequencies, Part II: Diurnal variations"); Covey et al. (2016, *Journal of Climate*, CMIP 일변동 평가).

---

### 강수 마스크·wet/dry 공간패턴 (rain area·패턴상관·ACC)
- 무엇을 측정/검증하나: 강수가 **어디에 있는가**(강수역 rain area)의 공간패턴 일치. wet/dry 마스크의 공간 상관·면적 일치. 강도와 분리해 "강수역 위치" 재현을 진단.
- 정의·수식: 임계 이진화 후 wet 면적비·패턴상관(binary 또는 강도), rain-area overlap(교집합/합집합, IoU/Jaccard), ACC(anomaly correlation, 아노말리 강제 climatology). FSS의 이진 기반과 연결.
- 적용 도메인/자료형: [격자] 강수. 임계별.
- 입력·전제: 공통 격자·임계·climatology(ACC). 관측격자 필수.
- 해석 기준(advisory): overlap·패턴상관 높을수록 강수역 재현 양호. 임계·해상도·격자대표성 의존 → advisory. double-penalty로 격자 이진상관이 낮을 수 있음(FSS 병행).
- 한계·주의(§G): 이진화로 강도 손실. 임계 의존. double-penalty(위치오차)로 상관 저평가 → 이웃(FSS) 병행. ACC는 동일 climatology 강제(§ 00-D).
- 출처: `02_spatial_pattern_verification.md`; Ebert (2008, *Meteorological Applications* 15, 이웃/fuzzy 강수검증 총론).

---

### ★ 운영·기관 검증 프레임워크 (WMO/WWRP-JWGFVR, MET/METplus, GPM Ground Validation)
- 무엇을 측정/검증하나: 강수 검증을 표준화·재현가능하게 수행하는 기관 절차·소프트웨어. 검증 "표준화" 자체 — 지표 선택·매치업·집계 규약을 공유해 기관·모델 간 비교를 가능하게 함.
- 정의·수식: **WWRP/WGNE JWGFVR**(공동 검증 작업반) 권고 지표·관행(범주·공간·확률). **DTC MET/METplus**: Grid-Stat(격자 연속·범주·이웃/FSS), MODE/MODE-TD(객체), Point-Stat(점 매치업), Series-Analysis, Wavelet-Stat(intensity-scale) 등 강수 검증 도구 일체. **GPM Ground Validation**: 위성강수 지상검증 프로토콜.
- 적용 도메인/자료형: 모든 강수 [격자]/[시계열]/[트랙].
- 입력·전제: 공통 QC 관측, 합의된 임계·이웃·객체 파라미터, 동일 매치업·집계 규약.
- 해석 기준(advisory): 기관 간 동일 규약으로 모델 순위·연도별 추세 평가. 규약·관측망 차이가 비교를 왜곡할 수 있음(advisory).
- 한계·주의(§G): 관측망 편중(육상·선진지역 위주)·규약 차이. 표준 도구라도 파라미터(임계·이웃·객체) 선택은 사용자 책임(§G-4). 확정 URL·버전은 변동 가능(§G-5, 확인요).
- 출처: WMO WWRP/WGNE Joint Working Group on Forecast Verification Research(JWGFVR) — Forecast Verification 방법 페이지(www.cawcr.gov.au/projects/verification/, 확인요); DTC *MET Users Guide* / *METplus Users Guide*(met.readthedocs.io, 확인요); Ebert et al. (2013, *Meteorological Applications* 20, "Progress and challenges in forecast verification").

---

## 출처 (References)

### 표준 참고문헌 / 교과서·지침 (실제 존재)
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (bias·RMSE·범주·분포 표준 정의 — 공통, `01` 참조).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, Wiley (범주형 CSI/HSS/PSS·확률·ROC — 공통, `03` 참조).
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD/POT — 공통, `03` 참조).
- WMO (2009) Klein Tank, A. M. G., Zwiers, F. W. & Zhang, X. *Guidelines on Analysis of extremes in a changing climate*, WCDMP-72 / WMO-TD No. 1500 (ETCCDI 지수·SDII 정의).
- WMO *Guidelines on the Calculation of Climate Normals* (WMO-No. 1203) (누적·기준기간 관행).

### 학술 논문 (웹으로 제목·저널·연도 확인됨; 권·페이지는 본문에 병기)
- Roberts, N. M. & Lean, H. W. (2008) "Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events," *Monthly Weather Review*, 136(1), 78–97. (FSS)
- Casati, B., Ross, G. & Stephenson, D. B. (2004) "A new intensity-scale approach for the verification of spatial precipitation forecasts," *Meteorological Applications*, 11(2), 141–154. (intensity-scale 웨이블릿)
- Wernli, H., Paulat, M., Hagen, M. & Frei, C. (2008) "SAL—A novel quality measure for the verification of quantitative precipitation forecasts," *Monthly Weather Review*, 136(11), 4470–4487. (doi:10.1175/2008MWR2415.1) (SAL)
- Davis, C., Brown, B. & Bullock, R. (2006) "Object-based verification of precipitation forecasts. Part I: Methods and application to mesoscale rain areas," *Monthly Weather Review*, 134(7), 1772–1784. (MODE)
- Ebert, E. E. & McBride, J. L. (2000) "Verification of precipitation in weather systems: Determination of systematic errors," *Journal of Hydrology*, 239(1–4), 179–202. (CRA)
- Gilleland, E., Ahijevych, D., Brown, B. G., Casati, B. & Ebert, E. E. (2009) "Intercomparison of spatial forecast verification methods," *Weather and Forecasting*, 24(5), 1416–1430. (공간검증·double-penalty ICP)
- Ferro, C. A. T. & Stephenson, D. B. (2011) "Extremal dependence indices: Improved verification measures for deterministic forecasts of rare binary events," *Weather and Forecasting*, 26(5), 699–713. (EDI/SEDI)
- Stephenson, D. B., Casati, B., Ferro, C. A. T. & Wilson, C. A. (2008) "The extreme dependency score: a non-vanishing measure for forecasts of rare events," *Meteorological Applications*, 15(1), 41–50. (EDS)
- North, R., Trueman, M., Mittermaier, M. & Rodwell, M. J. (2013) "An assessment of the SEEPS and SEDI metrics for the verification of 6 h forecast precipitation accumulations," *Meteorological Applications*, 20(2), 164–175. (doi:10.1002/met.1405) (SEEPS/SEDI)
- Rodwell, M. J., Richardson, D. S., Hewson, T. D. & Haiden, T. (2010) "A new equitable score suitable for verifying precipitation in numerical weather prediction," *Quarterly Journal of the Royal Meteorological Society*, 136(650), 1344–1363. (SEEPS)
- Roebber, P. J. (2009) "Visualizing multiple measures of forecast quality," *Weather and Forecasting*, 24(2), 601–608. (performance diagram)
- Schaefer, J. T. (1990) "The critical success index as an indicator of warning skill," *Weather and Forecasting*, 5(4), 570–575. (CSI)
- Hogan, R. J., Ferro, C. A. T., Jolliffe, I. T. & Stephenson, D. B. (2010) "Equitability revisited: Why the 'equitable threat score' is not equitable," *Quarterly Journal of the Royal Meteorological Society*, 136, 2652–2657. (ETS/GSS)
- Perkins, S. E., Pitman, A. J., Holbrook, N. J. & McAneney, J. (2007) "Evaluation of the AR4 climate models' simulated daily maximum temperature, minimum temperature, and precipitation over Australia using probability density functions," *Journal of Climate*, 20(17), 4356–4376. (Perkins Skill Score)
- Dai, A. (2006) "Precipitation characteristics in eighteen coupled climate models," *Journal of Climate*, 19(18), 4605–4630. (frequency/intensity 편향)
- Sun, Y., Solomon, S., Dai, A. & Portmann, R. W. (2006) "How often does it rain?" *Journal of Climate*, 19(6), 916–934. (빈도·강도 분해)
- Zhang, X., Alexander, L., Hegerl, G. C., Jones, P., Klein Tank, A., Peterson, T. C., Trewin, B. & Zwiers, F. W. (2011) "Indices for monitoring changes in extremes based on daily temperature and precipitation data," *WIREs Climate Change*, 2(6), 851–870. (ETCCDI 지수)
- Ebert, E. E. (2008) "Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework," *Meteorological Applications*, 15(1), 51–64. (이웃/fuzzy 총론)
- Ebert, E. E. (2001) "Ability of a poor man's ensemble to predict the probability and distribution of precipitation," *Monthly Weather Review*, 129(10), 2461–2480. (강수 검증 전처리 관행)
- Huffman, G. J. et al. (2020) "Integrated Multi-satellitE Retrievals for the Global Precipitation Measurement (GPM) mission (IMERG)," in *Satellite Precipitation Measurement*, Springer, 343–353. (IMERG)
- Kidd, C. & Levizzani, V. (2011) "Status of satellite precipitation retrievals," *Hydrology and Earth System Sciences*, 15(4), 1109–1116. (위성강수 리뷰)
- Maggioni, V., Meyers, P. C. & Robinson, M. D. (2016) "A review of merged high-resolution satellite precipitation product accuracy during the Tropical Rainfall Measuring Mission (TRMM) era," *Journal of Hydrometeorology*, 17(4), 1101–1117. (위성강수 오차 리뷰)
- Goudenhoofdt, E. & Delobbe, L. (2009) "Evaluation of radar-gauge merging methods for quantitative precipitation estimates," *Hydrology and Earth System Sciences*, 13(2), 195–203. (radar–gauge merging)
- Sinclair, S. & Pegram, G. (2005) "Combining radar and rain gauge rainfall estimates using conditional merging," *Atmospheric Science Letters*, 6(1), 19–22. (conditional merging)
- Hersbach, H. (2000) "Decomposition of the continuous ranked probability score for ensemble prediction systems," *Weather and Forecasting*, 15(5), 559–570. (CRPS — 공통)
- Hersbach, H. et al. (2020) "The ERA5 global reanalysis," *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999–2049. (ERA5 기준자료)
- Adler, R. F. et al. (2003) "The version-2 Global Precipitation Climatology Project (GPCP) monthly precipitation analysis (1979–present)," *Journal of Hydrometeorology*, 4(6), 1147–1167. (GPCP 격자강수 기준)
- Ebert, E. et al. (2013) "Progress and challenges in forecast verification," *Meteorological Applications*, 20(2), 130–139. (검증 프레임워크)
- Dai, A. (2001) "Global precipitation and thunderstorm frequencies. Part II: Diurnal variations," *Journal of Climate*, 14(6), 1112–1128. (일변동)
- Moriasi, D. N. et al. (2007) "Model evaluation guidelines for systematic quantification of accuracy in watershed simulations," *Transactions of the ASABE*, 50(3), 885–900. (PBIAS 기준 — 수문 관행)
- Kochendorfer, J. et al. (2017) "The quantification and correction of wind-induced precipitation measurement errors," *Hydrology and Earth System Sciences*, 21(4), 1973–1989. (WMO-SPICE undercatch)

### 웹 자료 (조사 시 직접 참조 — 확인요: URL·버전 변동 가능)
- WMO WWRP/WGNE Joint Working Group on Forecast Verification Research (JWGFVR), "Forecast Verification — Issues, Methods and FAQ": https://www.cawcr.gov.au/projects/verification/ (확인요)
- DTC MET / METplus Users Guide (Grid-Stat/MODE/Wavelet-Stat): https://met.readthedocs.io , https://metplus.readthedocs.io (확인요)
- ETCCDI / climdex 지수 정의: https://etccdi.pacificclimate.org/list_27_indices.shtml (확인요)
- NASA GPM / IMERG: https://gpm.nasa.gov (확인요)

### 확인요 (웹에서 1차 확인 못 했거나 정정한 항목)
- Gilbert (1884, *Monthly Weather Review*) GSS 원형 — 역사적 원전, 재인용 관행. GSS/ETS 실사용은 Schaefer(1990)·Hogan et al.(2010) 참조.
- Hanssen & Kuipers (1965, KNMI), Heidke (1926, *Geografiska Annaler*), Gerrity (1992, *MWR* 120) — 역사적 원전으로 통용되나 이 세션 웹 재확인은 부분적(확인요).
- Casati (2010, *Weather and Forecasting* 25, intensity-scale 재정식화) — 제목·연도 재확인 권장(확인요).
- Katz, Parlange & Naveau (2002, *Advances in Water Resources* 25) — 강수 극값 리뷰로 통용, 권·페이지 재확인 권장(확인요).

> 주의(공통, `00_overview_taxonomy.md` §F·§G 준수): 위 문헌의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(DOI는 확인된 것만 표기, 임의 생성 금지). 논문 그림은 복제하지 않으며 유형·사양만 기술한다. 재분석·위성·병합 QPE는 "참값"이 아니라 기준(reference)이며, 게이지 보정 산물(IMERG Final·radar–gauge merged)은 우량계와 오차가 상관될 수 있어 독립 검증·TC 독립 3자로 부적합함을 항상 명시(§G-1/2/3). 모든 해석 임계(CSI 등급·FSS useful-scale·SI 등)는 advisory이며 영역·해상도·계절·기준자료 의존 경고를 동반한다(§G-4).
