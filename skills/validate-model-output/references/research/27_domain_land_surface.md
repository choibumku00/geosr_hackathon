# 도메인: 육상(지표) (Land Surface) 검증·분석 방법 카탈로그

이 문서는 육상(지표) 모델·재분석 산출물(예: 육상면 모델 CLM/Noah-MP/JULES/ORCHIDEE, 재분석 ERA5-Land/GLDAS/MERRA-2-Land, 위성 소산물)의 결과를 지상관측망(flux tower·토양수분망·검조 아님·기상관측소), 위성(수동/능동 마이크로파·열적외·광학), 재분석자료와 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 육상 검증의 핵심 3축은 (1) **물·에너지 상태량**(토양수분·지표온도 LST·증발산 ET·지표 에너지수지), (2) **저장/눈 상태량**(적설 SWE·적설면적 SCA), (3) **식생·복사 상태량**(LAI/NDVI·GPP·알베도)이며, 여기에 (4) 시간규모(일변동·계절·경년)와 (5) 공간 이질성(sub-grid heterogeneity·대표성 오차)이 항상 얽힌다. 표준 지표(RMSE·bias·상관·Taylor·QQ·bootstrap)는 재정의하지 않고 공통 카드로 교차링크하며, 이 도메인 고유의 지표·전제(anomaly R·ubRMSD·삼중대조·에너지수지 닫힘·SCA F1·radiance-based LST 검증 등)를 상세히 다룬다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3·L4), [정점]=관측소·타워 시계열(토양수분망·flux tower CSV/텍스트), [트랙/스와스]=위성 궤도(soil moisture retrieval·LST L2), [프로파일]=토양 깊이별.
> **"우리 모델 vs ERA5-Land/관측/위성" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 지표 교차링크**: RMSE·bias·MAE·CRMSD·상관 R → `01_error_statistics.md`; QQ·PDF/CDF·KS → `01`; Taylor/Target diagram → `01`(+figures `16`); 범주형(POD/FAR/CSI/HSS) → `03`; 극값(GEV/POT) → `03`; 삼중대조(TC/ETC) 코어·매치업·대표성오차 → `12`·`15`; 공간패턴(FSS/ACC/pattern corr) → `02`; 시계열(분해·추세·변화점) → `06`. **이 파일은 이들을 재정의하지 않고 육상 맥락의 전제·해석·함정만 덧붙인다.**

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **토양수분 이상상관 (Anomaly R, soil moisture)** — 계절성 제거 후 단기 건·습 이벤트 재현력
- ★ **비편향 RMSD (ubRMSD)** — bias 제거 무작위오차(토양수분 검증 1차 표준)
- ★ **토양수분 삼중대조 (Triple Collocation TC/ETC: 위성×모델×in-situ)** — 참값 없는 오차분산·신호대잡음
- **CDF 매칭 / 재척도화 (CDF matching, rescaling)** — 계통차 제거 후 비교(척도 이질성)
- **토양수분 깊이·층 정합 (soil layer / depth matching)** — 모델 층 두께 vs 관측 심도
- **관측망 대표성·업스케일 (ISMN representativeness, upscaling)** — 점↔격자 지지면적 차이
- ★ **지표온도 LST 편차 검증 (temperature-based, T-b)** — 지상 LST 직접대조
- ★ **LST 복사기반 검증 (radiance-based, R-b)** — 지상 LST 없이 위성 검증
- **주야·구름 표집 편향 (diurnal / clear-sky sampling bias)** — LST·위성 표집의 조건부 편향
- ★ **증발산 ET 검증 (FLUXNET/eddy covariance)** — 잠열 LE↔ET 타워 대조
- ★ **지표 에너지수지 닫힘 (energy balance closure, EBR)** — Rn−G vs H+LE 불일치 진단
- **Bowen비·보정 프레이밍 (Bowen-ratio / residual closure)** — EC 불닫힘 배분
- **잠열·현열 플럭스 분할 (LE/H flux partitioning)** — 증발산 vs 가열 배분 오차
- **ET 물수지 교차검증 (basin water-balance ET)** — P−Q−ΔS 잔차 대조
- ★ **적설수당량 SWE 검증 (SWE bias/RMSE, snow pillow/course)** — 눈 저장량 정점 대조
- ★ **적설면적 SCA 범주검증 (F1·POD·FAR·overall accuracy)** — 눈/무눈 이진 분류 검증
- **적설 관련 진단 (SCF·눈깊이·SCD·적설선 고도)** — 적설분율·지속일·설선
- **적설 소멸/개시 타이밍 (melt-out / onset date)** — 눈 위상 오차
- ★ **엽면적지수 LAI 검증 (LAI direct/indirect validation)** — 식생량 상태 대조
- ★ **식생지수 NDVI/EVI 비교 (vegetation index)** — 광학 반사도 기반 녹지도
- **식생 물후 (phenology: SOS/EOS/LOS)** — 개엽·낙엽 시기 검증
- ★ **총일차생산 GPP 검증 (GPP vs eddy covariance)** — 탄소흡수 플럭스 대조 + 분할 주의
- **순생태계교환 NEE / 생태계호흡 Reco** — 탄소수지 성분 검증
- ★ **지표 알베도 검증 (surface albedo, MCD43 vs tower)** — 단파 반사율 대조
- **지표 방출률·순복사 (emissivity / net radiation Rn)** — 복사수지 성분
- **런오프·하천유출 검증 (runoff / streamflow, KGE·NSE)** — 수문 배출 대조
- **지하수·육수저장 TWS 검증 (GRACE terrestrial water storage)** — 총 육수저장 이상 대조
- **동결·해빙·토양온도 (frozen soil / soil temperature profile)** — 토양 열상태 프로파일
- ★ **격자-격자 공간비교 (ERA5-Land/GLDAS map difference)** — 면적 bias/RMSE·패턴 지도
- **토지피복·PFT 층화 검증 (stratified by land cover / PFT)** — 피복별 조건부 성능
- **anomaly / 계절기후값 분해 검증** — 평균장·계절·이상 성분 분리 평가

---

### ★ 토양수분 이상상관 (토양수분 이상상관 / Soil moisture anomaly correlation, R_anom)
- 무엇을 측정/검증하나: 계절 순환(seasonal cycle)을 제거한 토양수분 이상(anomaly)의 모델·관측 상관. 원자료 상관은 공통 계절성 때문에 인위적으로 높아지므로, 단기 건조·강수 이벤트(short-term drying/wetting) 재현력을 보려면 이상상관이 핵심.
- 정의·수식: 이동창(예: 5주) 기후값을 제거해 이상 δθ 산출 후 Pearson R 계산: R_anom = corr(δθ_model, δθ_obs). 원자료 상관 R(공통 카드 `01`)과 병행 보고. 유의성은 유효표본수 보정(자기상관 큼).
- 적용 도메인/자료형: 표층·근권(root-zone) 토양수분. [격자](모델·재분석) vs [정점](ISMN 관측망)·[트랙/스와스](SMAP/SMOS/ASCAT). 통상 부피함수율(m³/m³).
- 입력·전제: 동일 심도·동일 시간창 정합. 계절기후값 정의(창 길이·최소 표본) 통일. 관측·모델 모두 결측·품질플래그(ISMN quality flag) 적용. 재척도화(CDF matching)로 척도차 사전 제거 권장.
- 해석 기준(advisory): 위성 표층 토양수분 R_anom는 지역·피복에 따라 0.3~0.7대가 흔함(관행값, 절대기준 아님) — **밀림·복잡지형·동결기·RFI 오염 지역은 크게 낮아지고, 건조·초지에서 높아진다.** 계절·해상도 의존이 크므로 값 하나로 "좋음/나쁨" 단정 금지.
- 한계·주의(§G): 계절성이 강한 지역은 원자료 R가 과대. 이상 정의(창·기간)에 민감. 관측점과 격자의 지지면적 차이(대표성 오차)·심도 불일치가 R를 낮춘다. §G-1(기준≠참값)·§G-4(임계 advisory) 준수.
- 출처: Gruber et al. (2016) "Recent advances in (soil moisture) triple collocation analysis," *Int. J. Applied Earth Observation and Geoinformation* 45:200–211; Dorigo et al. (2011, *HESS*, ISMN); Entekhabi et al. (2010, SMAP mission, *Proc. IEEE* 98(5)).

---

### ★ 비편향 RMSD (비편향 평균제곱근차 / unbiased RMSD, ubRMSD)
- 무엇을 측정/검증하나: 계통차(bias)와 척도차를 제거한 무작위 오차의 크기. 토양수분 검증의 사실상 1차 표준(위성 소산물 요구사양이 ubRMSD로 명시됨).
- 정의·수식: ubRMSD = √{ mean[ ((θ_m − θ̄_m) − (θ_o − θ̄_o))² ] } = CRMSD(공통 카드 `01`의 중심화 RMSD와 동일 개념). 관계: RMSE² = bias² + ubRMSD². (수식 상세·bias/RMSE 정의는 `01` 참조 — 여기선 재정의 안 함.)
- 적용 도메인/자료형: 토양수분(주로), 필요시 LST·SWE에도 적용. [격자]/[정점]/[트랙].
- 입력·전제: 정합된 매치업 쌍. **평균 제거(bias 제거)만 하는 ubRMSD와, 분산까지 맞추는 재척도화 후 지표를 구분**해 보고. 부피함수율 단위(m³/m³) 통일.
- 해석 기준(advisory): SMAP 등 위성 표층 토양수분 목표 ubRMSD는 ~0.04 m³/m³ 수준으로 자주 인용되나 이는 **미션 요구사양(관행)**이며 지역·피복·계절에 따라 실측은 크게 달라진다. 절대 등급화 금지.
- 한계·주의(§G): bias를 지워버리므로 계통 습·건은 못 봄(bias 표 병행 필수). 관측 자체 오차·대표성 오차가 ubRMSD에 섞인다(TC로 분리 가능). §G-6(단일지표 금지).
- 출처: Entekhabi et al. (2010, *Proc. IEEE*, SMAP 요구사양); Gruber et al. (2016, *IJAEO* 45); Draper et al. (2013, *GRL*, SMOS/ASCAT vs model). 공통 CRMSD 정의는 `01_error_statistics.md`.

---

### ★ 토양수분 삼중대조 (삼중대조 / Triple Collocation TC·ETC: 위성×모델×in-situ)
- 무엇을 측정/검증하나: 절대 참값 없이 **세 독립 자료(위성 retrieval·모델/재분석·지상 in-situ)** 각각의 무작위 오차 표준편차와(ETC는) 진값 대비 상관(신호대잡음)까지 추정. 육상 도메인에서 TC가 가장 활발히 발전한 곳이 토양수분.
- 정의·수식: 각 자료 xᵢ = αᵢ + βᵢ·Θ + εᵢ 선형모형, 세 자료 공분산 관계로 βᵢ·var(εᵢ) 해석적 추정. ETC는 각 자료의 진값 상관 ρᵢ,Θ 산출. (TC/ETC 코어 수식·가정은 `12`·`15`에서 정의 — 여기선 토양수분 특유 전제만.)
- 적용 도메인/자료형: 표층 토양수분(가장 성숙). [트랙/스와스](위성)+[격자](모델/재분석)+[정점](ISMN). LST·ET로 확장 시도도 있음.
- 입력·전제: **세 자료의 오차 무상관·진값과 무상관·오차 정상성** 가정. 육상 특유 위반요인: (a) 두 위성/모델이 같은 강제 강수·같은 보조자료 공유, (b) 재분석과 모델이 같은 지면모형 계열 → 오차 상관. 공통 동적영역·충분한 콜로케이션 수 필요. 흔히 anomaly 공간에서 수행(계절 공통성분이 βΘ에 흡수되지 않도록).
- 해석 기준(advisory): 각 시스템 오차 σ_ε(m³/m³)·fRMSE·SNR 보고. in-situ가 대개 최소오차로 나오지만 **대표성 오차 때문에 항상 그런 것은 아님.** 지역·피복 층화해 제시.
- 한계·주의(§G): 오차 독립 가정 위배 시 오차분산 편향(§G-2·§G-3). 재분석·L4 격자자료를 "독립 3자"로 넣으면 가정 붕괴(§G-3). 표본·rescaling 방법에 민감.
- 출처: Gruber et al. (2016, *IJAEO* 45:200–211, TC 리뷰); Stoffelen (1998, *JGR*, TC 기초); McColl et al. (2014, *GRL* 41(17), ETC); Gruber et al. (2020, *Remote Sensing of Environment*, SM 검증 good-practice). CEOS LPV *Soil Moisture Validation Good Practices Protocol* (v1, 2020).

---

### CDF 매칭 / 재척도화 (누적분포 매칭 / CDF matching, rescaling)
- 무엇을 측정/검증하나: 검증 전에 자료 간 계통차·분산차·비선형 척도차를 제거하는 전처리(토양수분처럼 자료마다 동적범위·단위가 달라 직접 비교가 어려운 변수의 필수 단계). 이후 anomaly R·ubRMSD를 공정하게 산출.
- 정의·수식: 선형(평균·표준편차 매칭), 분위수(quantile/CDF) 또는 다항 CDF 매칭으로 소스 자료를 기준 자료 분포에 사상. (quantile mapping 코어는 `13`·`15` — 여기선 토양수분 적용 주의만.)
- 적용 도메인/자료형: 토양수분(주), 필요시 LST·ET. [트랙]/[격자]/[정점].
- 입력·전제: 매칭 학습기간과 검증기간 분리(과적합 방지). anomaly 검증 시 매칭이 실제 오차정보까지 지우지 않도록 주의(bias는 별도 보고).
- 해석 기준(advisory): 매칭은 "정확도를 좋게 만드는" 것이 아니라 **비교 가능하게** 만드는 것 — 매칭 후 R·ubRMSD만 보고 절대정확도로 오해 금지.
- 한계·주의(§G): 매칭이 계통오차를 감춰 모델 문제를 은폐할 수 있음. 짧은 표본 CDF 불안정. §G-6.
- 출처: Reichle & Koster (2004, *GRL*, CDF matching for SM); Gruber et al. (2020, *RSE*, rescaling 비교). 공통 QM 코어는 `13_model_intercomparison_downscaling.md`·`15`.

---

### 토양수분 깊이·층 정합 (토양층 정합 / soil layer & depth matching)
- 무엇을 측정/검증하나: 모델 토양층(두께·중심심도)과 관측 센서 심도·위성 감지심도의 정합. 부정합은 위상·진폭 오차로 오인된다.
- 정의·수식: 위성 표층은 감지심도 ~0–5 cm(마이크로파 파장 의존), 관측망은 5·10·20·50 cm 등 이산 센서, 모델은 층별 부피함수율. 근권(root-zone)은 지수필터(exponential filter, SWI) 또는 층 가중평균으로 유도.
- 적용 도메인/자료형: [프로파일] 관측·모델 vs [트랙] 위성 표층. 표층/근권 구분 필수.
- 입력·전제: 관측 심도·모델 층경계·위성 감지심도 명시. 근권 유도 시 필터 시간상수 T의 지역의존.
- 해석 기준(advisory): 표층↔근권을 섞으면 상관·bias 해석 붕괴. 심도 일치가 가장 큰 오차 통제 변수.
- 한계·주의(§G): 위성 감지심도는 습도·식생·주파수 따라 변동(고정 가정 위험). SWI 필터 상수 튜닝이 결과 좌우.
- 출처: Wagner et al. (1999, *RSE*, SWI/exponential filter); Albergel et al. (2008, *HESS*, root-zone from surface). CEOS LPV SM Protocol (2020).

---

### 관측망 대표성·업스케일 (ISMN 대표성 / representativeness & upscaling)
- 무엇을 측정/검증하나: 점 관측(수십 cm² 센서)과 격자/위성 화소(수 km²)의 지지면적(support) 차이에서 오는 대표성 오차. 검증차의 상당부분이 모델오차가 아니라 표집 규모 차이일 수 있음.
- 정의·수식: 대표성 오차 σ_rep 추정(밀집 관측 클러스터 분산, 변동함수 variogram, TC로 in-situ 오차 분리). 다중 센서 평균으로 화소 대표값 업스케일.
- 적용 도메인/자료형: [정점] 토양수분망·flux tower vs [격자]/[트랙]. LST·ET·알베도 공통 이슈.
- 입력·전제: 화소 내 관측 밀도·이질성 정보. 지형·토양·피복 이질성 클수록 σ_rep 큼.
- 해석 기준(advisory): 단일 점이 화소를 대표하지 못하는 지역에서는 큰 검증차가 정상 — "모델 나쁨"으로 단정 금지(§G-1).
- 한계·주의(§G): 대표성 오차와 모델오차 혼동이 육상 검증의 최대 함정. §G-1·§G-3.
- 출처: Gruber et al. (2020, *RSE*, representativeness); Nicolai-Shaw et al. (2015, *RSE*, upscaling). 대표성오차 코어는 `12`·`15`.

---

### ★ 지표온도 LST 편차 검증 (온도기반 / Temperature-based, T-b validation)
- 무엇을 측정/검증하나: 위성/모델 지표온도(LST, skin temperature)를 지상 실측 LST와 직접 대조해 bias/RMSE 산출. 열적외(TIR) 소산물 검증의 기본.
- 정의·수식: LST_sat − LST_ground 매치업에 bias·RMSE·상관(공통 카드 `01`). 지상 LST는 하향/상향 장파·방출률로부터 LST = [ (L↑ − (1−ε)L↓) / (εσ) ]^{1/4} 로 산출.
- 적용 도메인/자료형: [트랙/스와스](MODIS L2·VIIRS)·[격자](L3/L4·모델 skin T) vs [정점](flux tower·전용 LST 사이트). CF: `surface_temperature`.
- 입력·전제: **열적으로 균질한(단일성분) 피복**에서만 T-b 유효(호수·조밀식생·사막 등 m→km 스케일 균질). 방출률 ε 정확도, 각도(view/zenith)·시각 정합, 구름 제거.
- 해석 기준(advisory): MODIS C6 LST 사례 bias ~0.3–0.8 K, RMSE ~0.5–0.8 K 보고(사례값, 절대기준 아님). **이질피복·건조지 정오·경사면에서 크게 악화**; 시각·계절·각도 의존 경고 동반.
- 한계·주의(§G): 균질 사이트가 드물어 T-b는 지역 편중. 화소 내 이질성 시 대표성 오차 큼. 구름·에어로졸 잔차. §G-4.
- 출처: Coll et al. (2009) "Temperature-based and radiance-based validations of the V5 MODIS LST product," *JGR: Atmospheres* 114, D20102 (doi:10.1029/2009JD012038); Wan (2014, *RSE*, MODIS C6 LST); Guillevic et al. (2018, GSICS/CEOS LST Val Best Practices).

---

### ★ LST 복사기반 검증 (복사기반 / Radiance-based, R-b validation)
- 무엇을 측정/검증하나: 지상 LST 실측 없이, 위성 관측시각의 대기 프로파일·방출률로 top-of-atmosphere 복사를 모의해 LST를 역산·대조. T-b가 불가능한 이질피복·전지구로 검증 확장.
- 정의·수식: 대기복사전달모형(RTM)에 위성 LST + 대기 T/수증기 프로파일 + ε 입력 → 모의 복사 vs 관측 복사(또는 역산 LST) 비교. 주야 모두 가능(지상 LST 불요).
- 적용 도메인/자료형: [트랙/스와스] TIR LST 검증. 프로파일(재분석/라디오존데)·방출률 지도 필요. CF: `surface_temperature`.
- 입력·전제: 정확한 대기 프로파일·방출률·RTM. 소규모 방출률 변동이 작은 사이트 선호. 구름 없는 화소.
- 해석 기준(advisory): R-b는 T-b가 못 미치는 피복까지 검증하나 **대기 프로파일·ε 오차가 결과를 좌우** — 두 방법 병행이 표준. 값은 사이트·대기상태 의존.
- 한계·주의(§G): 대기·방출률 입력 오차가 LST 오차로 전이(순환논리 위험). 프로파일 시공간 정합 중요. §G-3.
- 출처: Coll et al. (2009, *JGR* 114, D20102); Wan & Li (2008, *IEEE TGRS*, R-b); Duan et al. (2019, *RSE*, R-b over heterogeneous surfaces).

---

### 주야·구름 표집 편향 (주야·청천 표집편향 / diurnal & clear-sky sampling bias)
- 무엇을 측정/검증하나: LST·위성 광학 소산물이 특정 시각(위성 통과)·청천(clear-sky)에서만 표집되어 생기는 조건부 편향. 모델(연속) vs 위성(조건부 표집) 비교 시 이를 맞추지 않으면 가짜 bias.
- 정의·수식: 모델을 **위성 통과시각·청천 화소로 동일 표집(sampling mask)** 후 비교. 주야 각각 bias·RMSE 분리. 청천 편향은 흐린 날 배제로 인한 (통상 더 따뜻·건조한) 표본 치우침.
- 적용 도메인/자료형: LST·ET·알베도·NDVI 위성검증 공통. [트랙]/[격자].
- 입력·전제: 위성 QC·구름플래그, 모델 시각별 출력. 표집 마스크를 모델·관측 동일 적용.
- 해석 기준(advisory): 청천·주간 표집은 계통적으로 극값 쪽으로 치우침 — 표집 정합 없이 bias 해석 금지.
- 한계·주의(§G): 구름 잦은 지역은 유효표본 급감(대표성 붕괴). §G-3.
- 출처: Guillevic et al. (2018, LST Val Best Practices); Ershadi et al. (2014, *Ag. For. Meteorol.*, ET 표집). §G 및 `15`(QC·매치업).

---

### ★ 증발산 ET 검증 (증발산 / Evapotranspiration, FLUXNET·eddy covariance)
- 무엇을 측정/검증하나: 모델 증발산(ET)·잠열플럭스(LE)를 에디공분산(eddy covariance, EC) 타워 관측과 대조. 물·에너지 순환 결합의 핵심 검증량.
- 정의·수식: LE(W m⁻²) ↔ ET(mm; ET = LE/(λρ_w)) 환산. bias·RMSE·상관·Taylor(공통 `01`). 반드시 **에너지수지 닫힘(아래 카드)** 상태를 함께 보고. 일·월·연 누적 규모별 검증.
- 적용 도메인/자료형: [정점] FLUXNET/AmeriFlux/ICOS 타워 vs [격자] 모델·재분석·위성 ET(예: MOD16·PML). CF: `water_evapotranspiration_flux`(또는 `surface_upward_latent_heat_flux`).
- 입력·전제: 타워 발자국(footprint)과 격자 대표성 정합. gap-filling·야간 u* 필터·energy-balance 보정 방식 명시(FLUXNET2015/ONEFlux). 강수·관개 이벤트 처리.
- 해석 기준(advisory): 타워 ET는 EC 불닫힘 때문에 통상 **10~30% 과소** 가능 — 보정 여부가 bias를 크게 바꾼다. 피복·건조도·시간규모 의존이 커 절대등급 금지.
- 한계·주의(§G): footprint(수백 m)≠격자(수 km) 대표성 오차. 이류(advection)·야간 플럭스 불확실. 닫힘 보정 방법이 결과 좌우(§G). §G-1·§G-6.
- 출처: Baldocchi et al. (2001, *BAMS*, FLUXNET); Pastorello et al. (2020, *Scientific Data* 7:225, FLUXNET2015/ONEFlux); Mu et al. (2011, *RSE*, MOD16 ET 검증).

---

### ★ 지표 에너지수지 닫힘 (에너지수지 닫힘 / Energy Balance Closure, EBR)
- 무엇을 측정/검증하나: 관측(또는 모델) 지표 에너지수지의 정합성 — 가용에너지(순복사−지중열, Rn−G)가 난류플럭스(현열+잠열, H+LE)와 얼마나 일치하는지. EC 관측 신뢰도 진단이자 모델 에너지 배분 검증.
- 정의·수식: 닫힘비 EBR = Σ(H+LE) / Σ(Rn−G). 회귀기울기(y=H+LE, x=Rn−G)·잔차 = Rn−G−H−LE도 보고. 이상적 EBR=1, 회귀기울기=1.
- 적용 도메인/자료형: [정점] flux tower(관측 닫힘)·[격자] 모델(내적 에너지수지). CF 성분: `surface_net_downward_radiative_flux`·`surface_upward_sensible_heat_flux`·`surface_upward_latent_heat_flux`·`downward_heat_flux_in_soil`.
- 입력·전제: Rn·G·H·LE 동시 관측(또는 모델 성분). 저장항(캐노피·광합성·G 저장) 처리 방식 명시. 시간규모(반시간~일)별 닫힘.
- 해석 기준(advisory): FLUXNET 다지점에서 관측 EBR ~0.7~0.9(불닫힘 10~30%)가 흔함(사례·관행값). **모델은 정의상 닫히므로(EBR≈1) 관측과의 비교 시 불닫힘을 감안**해야 공정. 지점·시간규모 의존.
- 한계·주의(§G): 관측 불닫힘의 원인(저저장·이류·발자국 불일치)이 미결 → "모델이 관측보다 낫다"로 오독 금지(관측 자체 오차). §G-1.
- 출처: Wilson et al. (2002) "Energy balance closure at FLUXNET sites," *Ag. For. Meteorol.* 113(1–4):223–243; Foken (2008, *Ecological Applications*, closure problem); Stoy et al. (2013, *Ag. For. Meteorol.*, 닫힘 다지점).

---

### Bowen비·잔차 프레이밍 (보웬비 강제닫힘 / Bowen-ratio & residual closure)
- 무엇을 측정/검증하나: EC 불닫힘 잔차(Rn−G−H−LE)를 H·LE에 어떻게 배분하느냐(닫힘 보정 가정). 배분 방식이 ET/현열 검증 bias를 직접 바꾸므로 반드시 명시·병행.
- 정의·수식: (a) Bowen-ratio 보존 배분(잔차를 β=H/LE 비율로 분배), (b) LE에만 배분(잔차 전부 LE), (c) 미보정 원자료. 세 프레이밍 결과를 함께 보고 권장.
- 적용 도메인/자료형: [정점] EC ET·H 검증의 전처리 선택. LE↔ET 환산과 결합.
- 입력·전제: 잔차·β 산출 가능. 어떤 프레이밍을 썼는지 보고문에 명기.
- 해석 기준(advisory): 배분 가정 하나로 ET bias가 수~수십 % 이동 — "정답 배분"은 없으므로 **가정 명시 + 민감도 병행**이 표준.
- 한계·주의(§G): 배분 가정을 숨기면 재현 불가·비교 왜곡. §G-5(불확실 가정 단정 금지)·§G-6.
- 출처: Twine et al. (2000, *Ag. For. Meteorol.*, Bowen-ratio closure); Mauder et al. (2018, *Ag. For. Meteorol.*, 보정 비교).

---

### 잠열·현열 플럭스 분할 (에너지 분할 / LE–H flux partitioning, EF)
- 무엇을 측정/검증하나: 가용에너지가 증발(LE)과 가열(H)로 나뉘는 비율(증발분율 EF = LE/(H+LE), 또는 Bowen비 β=H/LE)의 모델 재현. ET 총량이 맞아도 분할이 틀리면 지면-대기 되먹임이 왜곡.
- 정의·수식: EF = LE/(LE+H). β = H/LE. 관측·모델 EF/β를 bias·상관으로 비교, 일변동·계절 곡선 대조.
- 적용 도메인/자료형: [정점] EC vs [격자] 모델. 지면-경계층 결합 진단.
- 입력·전제: H·LE 동시 관측·모델 성분. 닫힘 보정 프레이밍 명시(위 카드).
- 해석 기준(advisory): 건조/습윤 전이대·관개지에서 EF 오차 큼. 토양수분–EF 관계(수분제어 vs 에너지제어 레짐)로 진단.
- 한계·주의(§G): 총 ET만 검증하면 분할 오차 은폐. §G-6.
- 출처: Gentine et al. (2007, *Ag. For. Meteorol.*, EF·diurnal); Dirmeyer et al. (2018, land-atmosphere coupling metrics). `04`(에너지수지 성분) 교차.

---

### ET 물수지 교차검증 (유역 물수지 ET / basin water-balance ET)
- 무엇을 측정/검증하나: 유역 규모에서 ET를 물수지 잔차(ET ≈ P − Q − ΔS)로 독립 추정해 모델·위성 ET와 교차검증. 타워 발자국을 넘어 격자 규모 검증.
- 정의·수식: P(강수)−Q(하천유출)−ΔS(저수량변화, GRACE 등) = ET. 연·계절 규모에서 적용(ΔS 무시 시 오차).
- 적용 도메인/자료형: [격자] 유역평균 P·ET·ΔS + [정점] 하천유출. CF: `water_evapotranspiration_flux`.
- 입력·전제: 폐합 유역·정확한 P·Q·ΔS. 짧은 기간은 ΔS 필수. 인위 취수·저수지 영향 배제.
- 해석 기준(advisory): 연 규모에서 견고, 월 이하는 ΔS 불확실로 약함. P·Q 오차가 ET 잔차에 누적.
- 한계·주의(§G): 잔차법이라 입력 오차 전부가 ET로 몰림. §G-1·§G-6.
- 출처: Zhang et al. (2016, *WRR*, water-balance ET); Rodell et al. (2004, *BAMS*, GLDAS water budget). `04`(수지 닫힘) 교차.

---

### ★ 적설수당량 SWE 검증 (적설수당량 / Snow Water Equivalent, SWE)
- 무엇을 측정/검증하나: 모델·재분석·위성 SWE(눈 저장 물량)를 지상 관측(snow pillow·snow course·SNOTEL)과 대조. 융설 수자원·수문 예측의 핵심.
- 정의·수식: SWE(mm) 매치업에 bias·RMSE·상관(공통 `01`). 적설깊이(snow depth)와 밀도로부터 SWE 유도 시 밀도 가정 명시. 누적·최대 SWE·SWE 곡선 검증.
- 적용 도메인/자료형: [정점] SNOTEL/snow course vs [격자] 모델·재분석·위성(수동마이크로파 SWE는 삼림·습설에서 불확실). CF: `surface_snow_amount`(kg m⁻²) 또는 눈물당량.
- 입력·전제: 지형·표고 정합(SWE는 표고에 강의존 → 격자 평균 표고 보정). 관측점 대표성(바람 재분포·수관차단). 밀도 환산 일관.
- 해석 기준(advisory): 산악·삼림·습설에서 위성·모델 SWE 오차 급증. 관측점 자체가 격자를 대표 못하는 경우 큰 차이가 정상 — 절대등급 금지. 표고·피복 층화 권장.
- 한계·주의(§G): 점 SWE의 대표성 오차 극심(눈 재분포). 수동마이크로파 SWE는 깊은 눈에서 포화. §G-1.
- 출처: Mortimer et al. (2020, *The Cryosphere*, gridded SWE product 평가); Broxton et al. (2016, *J. Hydrometeorol.*, SWE 관측 대표성); Wrzesien et al. (2019, *GRL*, mountain SWE).

---

### ★ 적설면적 SCA 범주검증 (적설면적 / Snow-Covered Area, F1·POD·FAR·overall accuracy)
- 무엇을 측정/검증하나: "화소가 눈인가/아닌가"의 이진 분류를 모델·위성이 맞히는지. 눈/무눈 2×2 분할표 기반 범주 검증.
- 정의·수식: 2×2(hit·miss·false·correct-neg)에서 POD=a/(a+c), FAR=b/(a+b), precision=a/(a+b), recall=POD, **F1 = 2·precision·recall/(precision+recall)**, overall accuracy=(a+d)/N. (범주형 지표 코어·HSS/CSI는 `03` — 여기선 눈 적용만.)
- 적용 도메인/자료형: [격자] 모델/위성 SCA(MODIS/VIIRS snow map) vs 기준(고해상 위성·lidar·지상). CF: 적설분율/이진 마스크.
- 입력·전제: 구름 화소 처리(구름은 눈 판정 불가 → 별도), 임계(적설분율→이진) 통일, 기준자료 QC. 지형그림자·삼림 하부 눈 주의.
- 해석 기준(advisory): 개방지 F1·overall accuracy 높게 나오나(공개 사례 Landsat F1 ~97%, MODIS POD ~0.95·FAR ~0.18 — 사례값) **삼림·구름·전이기(부분적설)에서 급락**. 계절·피복·해상도 의존 경고 동반.
- 한계·주의(§G): 구름·삼림차폐가 최대 오차원. 격자 double-penalty(위치 약간 어긋나면 miss+false). 이진화 임계 민감. §G-4.
- 출처: Salomonson & Appel (2004, *RSE*, MODIS fractional snow); Hall & Riggs (2007, *Hydrol. Processes*, MODIS snow 정확도); Stillinger et al. (2023, *The Cryosphere*, lidar 검증 F1). 범주형 코어 `03_categorical_event_extremes.md`.

---

### 적설 관련 진단 (적설분율 SCF·눈깊이·지속일 SCD·설선 고도)
- 무엇을 측정/검증하나: 이진 SCA를 넘어선 연속·유도 적설 진단 — 적설분율(SCF, 0–1), 눈깊이(snow depth), 적설지속일(snow cover duration, SCD), 적설선 고도(snowline elevation).
- 정의·수식: SCF는 연속값 → bias/RMSE·상관. SCD = 연중 적설 임계 초과 일수. 설선고도 = SCF=0.5 등고선의 표고 중앙값. 눈깊이는 밀도로 SWE와 연계.
- 적용 도메인/자료형: [격자] 위성 SCF·모델 vs 지상. 표고 DEM 결합.
- 입력·전제: SCF 임계·표고 구간 정의. 구름 gap-filling 방식 명시.
- 해석 기준(advisory): SCD·설선은 표고 의존이 지배적 — 표고대별 층화 필수. SCF 연속검증이 이진 SCA보다 정보량 큼.
- 한계·주의(§G): 구름 보간 산물을 독립검증에 쓰면 순환. §G-3.
- 출처: Salomonson & Appel (2004, *RSE*, SCF); Notarnicola et al. (2013, *RSE*, SCD/설선). `03`·`06`(추세·타이밍) 교차.

---

### 적설 소멸·개시 타이밍 (융설·개시일 / melt-out & onset date)
- 무엇을 측정/검증하나: 적설의 계절 위상 — 첫 적설 개시일과 완전 융설(melt-out) 날짜의 모델·관측 일치. 수문 타이밍·수자원 예측에 직결.
- 정의·수식: 임계(예: SWE>10 mm 또는 SCF>0.5) 최초·최종 초과일. 타이밍 bias(일)·RMSE(일). (변화점·위상 검출은 `06`.)
- 적용 도메인/자료형: [정점] SWE·[격자] SCF 시계열. 연도별 날짜 시계열.
- 입력·전제: 임계·연도 정의 통일. 재적설(re-accumulation) 처리 규칙.
- 해석 기준(advisory): 융설일은 봄 강제·알베도 되먹임에 민감 → 며칠~수주 편차 흔함. 표고·피복 층화.
- 한계·주의(§G): 임계 선택에 민감. 위성 구름 결측이 개시·소멸일 왜곡. §G-4.
- 출처: Trujillo & Molotch (2014, *WRR*, melt timing); Chen et al. (2018, *RSE*, snow onset/end). `06`(변화점) 교차.

---

### ★ 엽면적지수 LAI 검증 (엽면적지수 / Leaf Area Index)
- 무엇을 측정/검증하나: 모델·위성 LAI(단위지면당 편측 엽면적, m²/m²)를 지상 실측·기준 위성과 대조. 광합성·증발산·복사 배분을 좌우하는 식생 상태량.
- 정의·수식: LAI 매치업 bias·RMSE·상관(공통 `01`). 지상 LAI는 직접(엽 채취) 또는 간접(광학 LAI-2000·반구사진, "유효 LAI" = 실제 LAI×군집지수 Ω) 측정 — 유효/참 LAI 구분 명시.
- 적용 도메인/자료형: [격자] MODIS(MOD15/MCD15)·Sentinel-3·모델 vs [정점]·고해상 기준지도(업스케일). CF: `leaf_area_index`.
- 입력·전제: 유효 LAI vs 참 LAI 정합(군집지수 Ω). 화소 대표성(업스케일 필요). 계절·PFT별.
- 해석 기준(advisory): 상록수·밀림 고LAI에서 위성 포화(saturation)로 과소·불확실. 낙엽림 계절진폭 검증이 유효. 절대등급보다 계절곡선·PFT 층화.
- 한계·주의(§G): 위성 LAI 알고리즘·구름·BRDF 잔차. 지상 유효LAI를 참LAI처럼 쓰면 bias(§G). §G-1.
- 출처: Yang et al. (2006, *IEEE TGRS*, MODIS LAI 검증); Fang et al. (2019, *Reviews of Geophysics*, LAI 검증 리뷰); CEOS LPV LAI Val Protocol.

---

### ★ 식생지수 NDVI/EVI 비교 (식생지수 / Vegetation index)
- 무엇을 측정/검증하나: 광학 반사도 기반 녹지도(NDVI=(NIR−R)/(NIR+R), EVI 개선판)의 모델·위성 정합·시계열 상관. LAI/GPP의 대리변수이자 물후 지표.
- 정의·수식: NDVI·EVI 매치업 bias·상관·시계열 교차상관(`06`). NDVI는 고식생에서 포화·토양·대기 영향 → EVI가 보완.
- 적용 도메인/자료형: [격자] MODIS(MOD13)·Sentinel-2/3·재분석 결합 vs 기준. CF: 표준명 없음(관례상 도메인 별칭 필요).
- 입력·전제: 대기보정·BRDF·구름/눈 마스크. 센서 간 밴드·spectral response 차이 보정. 청천 표집 편향(위 카드).
- 해석 기준(advisory): NDVI 포화·토양배경·눈 오염 주의. 계절 위상·진폭 검증이 절대값 비교보다 견고.
- 한계·주의(§G): 센서 간 계통차(교차보정 필요). 눈·구름 잔차가 겨울 NDVI 왜곡. §G-3.
- 출처: Huete et al. (2002, *RSE*, MODIS VI/EVI); Tucker (1979, *RSE*, NDVI). `06`(시계열·물후) 교차.

---

### 식생 물후 (식생 물후 / phenology: SOS·EOS·LOS)
- 무엇을 측정/검증하나: 개엽(start of season, SOS)·낙엽(end of season, EOS)·생장기간(length, LOS)의 모델·위성 일치. 탄소·물순환 계절 위상 검증.
- 정의·수식: NDVI/EVI/LAI 시계열에서 임계·변곡(로지스틱 적합·이동평균 교차)으로 SOS/EOS 검출 → 타이밍 bias(일). (검출·변화점은 `06`.)
- 적용 도메인/자료형: [격자] 위성 VI·모델 vs 지상 phenocam·관측. 연도별 날짜.
- 입력·전제: 검출법·임계 통일(방법 의존 큼). 결측 보간·평활 명시.
- 해석 기준(advisory): 검출법에 따라 SOS가 수~수십 일 이동 — 방법 고정·민감도 병행. 상록림은 물후 신호 약함.
- 한계·주의(§G): 임계·평활 선택 민감. 구름 결측이 봄 SOS 왜곡. §G-4.
- 출처: Zhang et al. (2003, *RSE*, MODIS phenology); Richardson et al. (2013, *Ag. For. Meteorol.*, phenocam·모델). `06` 교차.

---

### ★ 총일차생산 GPP 검증 (총일차생산 / Gross Primary Production vs eddy covariance)
- 무엇을 측정/검증하나: 모델·위성 GPP(생태계 총 탄소흡수, gCm⁻²d⁻¹)를 EC 타워 유도 GPP와 대조. 육상 탄소순환 검증의 중심.
- 정의·수식: GPP 매치업 bias·RMSE·상관·Taylor(공통 `01`). **GPP는 직접 측정이 아니라 NEE를 분할(partitioning)해 얻음** → 분할법(야간 온도반응 vs 주간 광반응) 명시. 일·8일·연 규모별.
- 적용 도메인/자료형: [정점] FLUXNET GPP vs [격자] MODIS(MOD17)·위성 LUE·과정모형. CF: `gross_primary_productivity_of_biomass_expressed_as_carbon`(확인요) 또는 도메인 별칭.
- 입력·전제: NEE 분할법·u* 필터·gap-filling 통일. footprint 대표성. 관개·교란(disturbance) 처리.
- 해석 기준(advisory): MODIS GPP 사례 작물서 6~58% 과소(사례값, PFT·건조도 의존). **타워 GPP 자체가 분할가정에 의존**하므로 "참값" 아님(§G-1). PFT·계절 층화.
- 한계·주의(§G): 분할가정이 타워 GPP를 좌우(불확실 기준). footprint 대표성. §G-1·§G-5.
- 출처: Running et al. (2004, *BioScience*, MOD17 GPP); Reichstein et al. (2005, *Global Change Biology*, NEE 분할); Pastorello et al. (2020, *Scientific Data* 7:225, FLUXNET2015).

---

### 순생태계교환 NEE / 생태계호흡 Reco (탄소수지 성분)
- 무엇을 측정/검증하나: NEE(순 CO₂ 교환)·Reco(생태계호흡) 성분의 모델 재현. GPP−Reco=NEP 관계로 탄소수지 정합.
- 정의·수식: NEE·Reco bias·상관, 일변동·계절 곡선. NEE는 EC 직접측정(부호규약 명시: 대기흡수 음). Reco는 야간 NEE 온도반응 외삽.
- 적용 도메인/자료형: [정점] FLUXNET vs [격자] 과정모형. 탄소플럭스.
- 입력·전제: 부호규약·u* 필터·gap-fill 통일. 야간 저혼합 시 NEE 과소.
- 해석 기준(advisory): 야간 플럭스·저장항 불확실 큼. Reco는 외삽 산물(불확실 기준).
- 한계·주의(§G): NEE는 GPP·Reco 상쇄 → 성분 병행 필수(§G-6). §G-5.
- 출처: Reichstein et al. (2005, *GCB*, 분할); Aubinet et al. (2012, *Eddy Covariance* 교과서, Springer).

---

### ★ 지표 알베도 검증 (지표 알베도 / Surface albedo, MCD43 vs tower)
- 무엇을 측정/검증하나: 모델·위성 지표 알베도(단파 반사율, 0–1)를 타워 복사관측과 대조. 지표 복사수지·에너지 배분·눈-알베도 되먹임의 핵심.
- 정의·수식: 알베도 = 상향/하향 단파. blue-sky(실제)·white-sky(등방)·black-sky(직달) 구분. bias·RMSE(공통 `01`). 광대역(broadband)·분광 구분.
- 적용 도메인/자료형: [격자] MODIS MCD43·모델 vs [정점] flux tower(CMP/CNR 복사계). CF: `surface_albedo`.
- 입력·전제: blue/white/black-sky 정의 정합. 화소 대표성(500 m vs 타워 발자국). 눈/식생 계절. 태양천정각.
- 해석 기준(advisory): MCD43 사례 RMSE 초지/농지 <0.03(무설기)·<0.05(적설기), 삼림 <0.02~0.025(사례값). **적설·혼합·이질피복에서 악화**; 계절·피복 의존 경고 동반.
- 한계·주의(§G): 적설기·이질피복 대표성 오차 큼. 알베도 종류(blue/white/black) 혼동 금지. §G-1·§G-4.
- 출처: Cescatti et al. (2012, *RSE*, MCD43 vs FLUXNET); Wang et al. (2014, *RSE*, MCD43 검증); Schaaf et al. (2002, *RSE*, MODIS BRDF/Albedo).

---

### 지표 방출률·순복사 (방출률 ε / 순복사 Rn)
- 무엇을 측정/검증하나: 지표 방출률(emissivity, ε)과 순복사(net radiation, Rn=단파순+장파순)의 모델·위성 정합. LST·에너지수지의 상류 입력.
- 정의·수식: Rn = (1−α)S↓ + εL↓ − εσT_s⁴. 성분별(단파·장파) 및 순 Rn bias·상관. ε는 TIR 소산물·스펙트럼 라이브러리와 대조.
- 적용 도메인/자료형: [정점] 타워 4성분 복사계 vs [격자] 모델·위성. CF: `surface_net_downward_radiative_flux` 등 성분.
- 입력·전제: 4성분 복사 동시관측 또는 모델 성분. ε·α 정합. 지중열 G와 결합해 에너지수지 카드로.
- 해석 기준(advisory): Rn은 성분오차 상쇄로 순값이 맞아도 성분이 틀릴 수 있음(성분 병행). ε 오차가 LST·장파에 전이.
- 한계·주의(§G): 순 Rn만 보면 성분오차 은폐(§G-6). §G-6.
- 출처: Wang & Dickinson (2013, *Reviews of Geophysics*, Rn/복사); Hulley et al. (2015, *IEEE TGRS*, emissivity). `04`(복사수지) 교차.

---

### 런오프·하천유출 검증 (지표유출 / runoff & streamflow, KGE·NSE)
- 무엇을 측정/검증하나: 모델 지표유출·하천유출을 관측 하천유량과 대조. 육상 물수지의 배출 성분 검증.
- 정의·수식: KGE(상관·bias비·변동비 결합)·NSE·PBIAS(공통 효율지표는 `01`). 유출은 로그·√변환으로 저·고유량 균형. 유량곡선(FDC)·수문곡선 대조.
- 적용 도메인/자료형: [정점] 하천 게이지 vs [격자] 모델 유출(하도 라우팅 필요). CF: `runoff_flux`/`water_volume_transport_in_river_channel`.
- 입력·전제: 유역 경계·라우팅·인위 규제(댐·취수) 처리. 유량 관측 rating curve 오차.
- 해석 기준(advisory): 첨두 타이밍·저유량 재현 별도 평가. KGE·NSE는 극값 가중 다름 → 병행. 유역·기후 의존.
- 한계·주의(§G): 인위 규제·라우팅 오차가 물리오차와 섞임. §G-6.
- 출처: Gupta et al. (2009, *J. Hydrology*, KGE); Nash & Sutcliffe (1970, *J. Hydrology*, NSE — `01` 참조). `06`(수문곡선) 교차.

---

### 지하수·육수저장 TWS 검증 (총육수저장 / Terrestrial Water Storage, GRACE)
- 무엇을 측정/검증하나: 모델 총 육수저장 이상(TWSA: 토양수분+지하수+눈+지표수+식생수 합)을 GRACE/GRACE-FO 위성 중력 관측과 대조. 통합 물수지 검증.
- 정의·수식: TWSA(cm 상당수두) 이상 시계열 bias·상관·진폭비. GRACE는 큰 유역(~수십만 km²) 평균·월 규모.
- 적용 도메인/자료형: [격자] 모델 저장 성분 합 vs GRACE mascon/구면조화. 유역·월 규모.
- 입력·전제: GRACE 공간필터·leakage 보정, 모델을 GRACE 커널로 평활(fingerprint 정합). 저장 성분 정의 일치.
- 해석 기준(advisory): 소유역·아월(sub-monthly)은 GRACE 해상도 밖 → 큰 유역·계절/경년만 유효. 진폭·위상 별도.
- 한계·주의(§G): GRACE 자체 오차·leakage 큼(기준≠참값). 성분 분해 불가(합만). §G-1.
- 출처: Tapley et al. (2004, *Science*, GRACE); Rodell et al. (2004, *BAMS*, GLDAS/TWS); Scanlon et al. (2018, *PNAS*, model-GRACE 비교).

---

### 동결·해빙·토양온도 (토양온도·동결 / soil temperature profile & frozen soil)
- 무엇을 측정/검증하나: 토양온도 프로파일·동결심도·동결/해빙 타이밍의 모델 재현. 고위도·산악 수문·탄소(영구동토)에 직결.
- 정의·수식: 층별 토양온도 bias·RMSE·상관. 0°C 등온선 심도(동결심도)·동결/해빙일 타이밍. 표층↔심층 감쇠·위상지연.
- 적용 도메인/자료형: [프로파일] 토양온도 관측 vs [격자] 모델 층. CF: `soil_temperature`.
- 입력·전제: 관측 심도·모델 층 정합(위 층정합 카드). 눈 단열·수분 영향.
- 해석 기준(advisory): 눈덮임 단열·토양수분이 토양온도를 지배 → 눈·수분 오차가 전이. 심도·계절 층화.
- 한계·주의(§G): 심도 부정합이 위상오차로 오인. §G-1.
- 출처: Luo et al. (2003, *J. Hydrometeorol.*, soil temperature 검증); Koven et al. (2013, *J. Climate*, 영구동토 모델).

---

### ★ 격자-격자 공간비교 (재분석 지도차 / ERA5-Land·GLDAS map difference)
- 무엇을 측정/검증하나: 우리 모델 [격자]를 ERA5-Land·GLDAS·MERRA-2-Land 등 육상 재분석 [격자]와 **면적 전면 비교**해 bias/RMSE/상관·SI의 지리 분포를 지도화. 관측 희소 지역까지 계통오차 위치·계절성 진단.
- 정의·수식: 공통 격자 재격자화(bilinear/conservative) 후 격자별 시계열에 bias(x,y)·RMSE(x,y)·R(x,y) → 색지도. 영역·위도대 평균·ACC(공통 `02`) 병행.
- 적용 도메인/자료형: 토양수분·LST·ET·SWE·LAI·알베도 [격자] vs [격자]. NetCDF↔NetCDF.
- 입력·전제: **시간축·격자·달력·마스크(육지/해양/영구빙) 정합**, 단위 일치. 재격자화 시 보존·해안선·해상도 차 주의. ERA5-Land ~9 km·GLDAS ~0.25° 등 해상도 차 명시.
- 해석 기준(advisory): 계통 bias 띠(예: 반건조대 과습·산악 SWE 과소)의 위치·계절 파악. **재분석은 참값 아님**(자체 오차·동화 한계) → 지상·위성 검증과 교차해석.
- 한계·주의(§G): 재분석은 또 하나의 모델 산출(§G-1). 우리 모델과 같은 지면모형/강제 공유 시 차이 과소(§G-2). 해상도 차가 차이의 상당부분. §G-1·§G-2.
- 출처: Muñoz-Sabater et al. (2021, *ESSD* 13, ERA5-Land); Rodell et al. (2004, *BAMS*, GLDAS); Reichle et al. (2017, *J. Hydrometeorol.*, MERRA-2 land). 공간비교 코어 `02`.

---

### 토지피복·PFT 층화 검증 (피복 층화 / stratified by land cover / PFT)
- 무엇을 측정/검증하나: 검증 지표를 토지피복·식물기능형(PFT)·기후대별로 층화해 조건부 성능을 진단. 전역 평균이 감추는 피복별 강·약점 노출.
- 정의·수식: 화소·타워를 피복지도(예: MODIS IGBP)·PFT·Köppen 기후대로 분류 후 각 층에서 bias/RMSE/R 별도 산출·비교. (층화·집계 관행.)
- 적용 도메인/자료형: 모든 육상 변수 공통. [격자]/[정점].
- 입력·전제: 일관된 피복/PFT 지도·화소 분류. 혼합화소 처리. 층별 표본수 충분.
- 해석 기준(advisory): 밀림·도시·설원 등에서 계통차 흔함. 층별 표본 적으면 불안정(신뢰구간 동반).
- 한계·주의(§G): 피복지도 오분류가 층화 왜곡. 혼합화소. §G-6.
- 출처: Friedl et al. (2010, *RSE*, MODIS land cover); Best et al. (2015, *J. Hydrometeorol.*, PLUMBER land model 벤치마킹).

---

### anomaly / 계절기후값 분해 검증 (성분 분해 / mean–seasonal–anomaly decomposition)
- 무엇을 측정/검증하나: 육상 변수를 평균장(mean)·계절순환(seasonal cycle)·이상(anomaly) 성분으로 분해해 각 성분별로 검증. 계절성이 상관을 부풀리는 함정을 회피(토양수분 anomaly R와 동일 철학, 전 변수 확장).
- 정의·수식: X = X̄ + X_seasonal(월/조화 기후값) + X'(이상). 성분별 bias·RMSE·R. (STL·조화적합 등 분해 코어는 `06`.)
- 적용 도메인/자료형: 토양수분·LST·ET·LAI·GPP 시계열. [격자]/[정점].
- 입력·전제: 기후값 기준기간·정의 통일(모델·관측 동일). 결측 처리.
- 해석 기준(advisory): 원자료 상관이 높아도 이상성분 상관은 낮을 수 있음 → 반드시 성분 분리 보고. 계절진폭 위상오차 별도.
- 한계·주의(§G): 기후값 정의 불일치가 인위 bias. 짧은 기간 계절값 불안정. §G-6.
- 출처: Entekhabi et al. (2010, *J. Hydrometeorol.*, SM 검증 metric 분해); Koster et al. (2009, *GRL*, seasonal vs anomaly skill). 분해 코어 `06`.

---

## 출처 (References)

### 표준 프로토콜·지침 (실제 존재)
- CEOS Land Product Validation (LPV) Subgroup, *Soil Moisture Product Validation Good Practices Protocol*, v1.0 (2020). — 토양수분 검증 표준(anomaly R·ubRMSD·TC·대표성).
- CEOS LPV, *LAI / FAPAR Validation Best Practices* (Fernandes et al.). (확인요 — 버전·연도 인용 전 재확인)
- Guillevic, P. et al. (2018) *Land Surface Temperature Product Validation Best Practice Protocol*, CEOS LPV / GSICS. (LST T-b·R-b·표집)
- FLUXNET / ONEFlux processing (FLUXNET2015): Pastorello, G. et al. (2020) "The FLUXNET2015 dataset and the ONEFlux processing pipeline for eddy covariance data," *Scientific Data* 7:225.

### 학술 논문·자료 (웹으로 제목·저널·연도 확인; 권·페이지는 본문 병기)
- Gruber, A., Su, C.-H., Zwieback, S., Crow, W., Dorigo, W. & Wagner, W. (2016) "Recent advances in (soil moisture) triple collocation analysis," *International Journal of Applied Earth Observation and Geoinformation*, 45:200–211.
- Gruber, A. et al. (2020) "Validation practices for satellite soil moisture retrievals: What are (the) errors?," *Remote Sensing of Environment*, 244:111806.
- Stoffelen, A. (1998) "Toward the true near-surface wind speed: Error modeling and calibration using triple collocation," *JGR*, 103(C4). (TC 기초 — `12` 공통)
- McColl, K. A. et al. (2014) "Extended triple collocation," *Geophysical Research Letters*, 41(17), 6229–6236 (doi:10.1002/2014GL061322). (`12` 공통)
- Entekhabi, D. et al. (2010) "The Soil Moisture Active Passive (SMAP) mission," *Proceedings of the IEEE*, 98(5), 704–716. (ubRMSD 요구사양)
- Entekhabi, D., Reichle, R. H., Koster, R. D. & Crow, W. T. (2010) "Performance metrics for soil moisture retrievals and application requirements," *Journal of Hydrometeorology*, 11(3), 832–840. (SM metric 분해)
- Dorigo, W. et al. (2011) "The International Soil Moisture Network (ISMN)," *Hydrology and Earth System Sciences*, 15, 1675–1698.
- Wagner, W., Lemoine, G. & Rott, H. (1999) "A method for estimating soil moisture from ERS scatterometer... (SWI)," *Remote Sensing of Environment*, 70(2), 191–207.
- Albergel, C. et al. (2008) "From near-surface to root-zone soil moisture using an exponential filter," *HESS*, 12, 1323–1337.
- Reichle, R. H. & Koster, R. D. (2004) "Bias reduction in short records of satellite soil moisture (CDF matching)," *Geophysical Research Letters*, 31, L19501.
- Coll, C. et al. (2009) "Temperature-based and radiance-based validations of the V5 MODIS land surface temperature product," *JGR: Atmospheres*, 114, D20102 (doi:10.1029/2009JD012038).
- Wan, Z. (2014) "New refinements and validation of the collection-6 MODIS land-surface temperature/emissivity product," *Remote Sensing of Environment*, 140, 36–45.
- Duan, S.-B. et al. (2019) "Radiance-based validation of land surface temperature products over heterogeneous surfaces," *Remote Sensing of Environment*. (R-b 이질피복)
- Wilson, K. et al. (2002) "Energy balance closure at FLUXNET sites," *Agricultural and Forest Meteorology*, 113(1–4), 223–243.
- Foken, T. (2008) "The energy balance closure problem: An overview," *Ecological Applications*, 18(6), 1351–1367.
- Twine, T. E. et al. (2000) "Correcting eddy-covariance flux underestimates over a grassland," *Agricultural and Forest Meteorology*, 103, 279–300. (Bowen-ratio closure)
- Baldocchi, D. et al. (2001) "FLUXNET: A new tool to study the temporal and spatial variability of ecosystem-scale carbon dioxide, water vapor, and energy flux densities," *BAMS*, 82(11), 2415–2434.
- Mu, Q., Zhao, M. & Running, S. W. (2011) "Improvements to a MODIS global terrestrial evapotranspiration algorithm (MOD16)," *Remote Sensing of Environment*, 115, 1781–1800.
- Running, S. W. et al. (2004) "A continuous satellite-derived measure of global terrestrial primary production (MOD17)," *BioScience*, 54(6), 547–560.
- Reichstein, M. et al. (2005) "On the separation of net ecosystem exchange into assimilation and ecosystem respiration," *Global Change Biology*, 11, 1424–1439. (NEE 분할)
- Cescatti, A. et al. (2012) "Intercomparison of MODIS albedo retrievals and in situ measurements across the global FLUXNET network," *Remote Sensing of Environment*, 121, 323–334.
- Schaaf, C. B. et al. (2002) "First operational BRDF, albedo nadir reflectance products from MODIS," *Remote Sensing of Environment*, 83, 135–148. (MCD43)
- Huete, A. et al. (2002) "Overview of the radiometric and biophysical performance of the MODIS vegetation indices (EVI)," *Remote Sensing of Environment*, 83, 195–213.
- Yang, W. et al. (2006) "MODIS leaf area index products: From validation to algorithm improvement," *IEEE Transactions on Geoscience and Remote Sensing*, 44(7). 
- Fang, H. et al. (2019) "An overview of global leaf area index (LAI): Methods, products, validation, and applications," *Reviews of Geophysics*, 57, 739–799.
- Hall, D. K. & Riggs, G. A. (2007) "Accuracy assessment of the MODIS snow products," *Hydrological Processes*, 21, 1534–1547.
- Salomonson, V. V. & Appel, I. (2004) "Estimating fractional snow cover from MODIS," *Remote Sensing of Environment*, 89, 351–360.
- Mortimer, C. et al. (2020) "Evaluation of long-term Northern Hemisphere snow water equivalent products," *The Cryosphere*, 14, 1579–1594.
- Muñoz-Sabater, J. et al. (2021) "ERA5-Land: A state-of-the-art global reanalysis dataset for land applications," *Earth System Science Data*, 13, 4349–4383.
- Rodell, M. et al. (2004) "The Global Land Data Assimilation System (GLDAS)," *BAMS*, 85(3), 381–394.
- Tapley, B. D. et al. (2004) "GRACE measurements of mass variability in the Earth system," *Science*, 305, 503–505.
- Gupta, H. V. et al. (2009) "Decomposition of the mean squared error and NSE... (KGE)," *Journal of Hydrology*, 377, 80–91.
- Best, M. J. et al. (2015) "The plumbing of land surface models: Benchmarking model performance (PLUMBER)," *Journal of Hydrometeorology*, 16, 1425–1442.
- Friedl, M. A. et al. (2010) "MODIS Collection 5 global land cover," *Remote Sensing of Environment*, 114, 168–182.
- Wang, Z. & Dickinson, R. E. (2013) — surface net radiation, *Reviews of Geophysics*. (권·페이지 확인요)

### 웹 자료 (조사 시 직접 참조)
- CEOS LPV *Soil Moisture Validation Good Practices Protocol* (v1, 2020): https://lpvs.gsfc.nasa.gov/PDF/CEOS_SM_LPV_Protocol_V1_20201027_final.pdf
- NASA MODIS Land — MOD17 (GPP/NPP) Validation Status: https://modis-land.gsfc.nasa.gov/ValStatus.php?ProductID=MOD17
- ISMN (International Soil Moisture Network): https://ismn.earth
- FLUXNET / FLUXNET2015 (ONEFlux): https://fluxnet.org

### 확인요 (웹 1차 확인 못 했거나 권·페이지 미확정)
- CF standard name `gross_primary_productivity_of_biomass_expressed_as_carbon` — GPP 표준명 존재하나 정확 표기·플럭스 부호 규약은 인용 전 CF 표준명 표에서 재확인(확인요).
- NDVI/EVI에는 승인된 CF standard_name이 없음 — 도메인 라우팅은 변수명 별칭(ndvi/evi/lai_*) 패턴으로 처리 필요.
- CEOS LPV LAI/FAPAR Best Practices의 버전·연도, Wang & Dickinson (2013) 권·페이지 — 인용 전 재확인.
- Duan et al. (2019) *RSE* 권·페이지 미확정(확인요).

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(검색으로 확인된 제목·저널·연도를 기재, DOI 임의 생성 금지 — DOI 명시 항목만 이 세션에서 확인됨). 기준자료(ERA5-Land·GLDAS·GRACE·위성 L3/L4)는 **참값이 아니라 기준**이며, 해석 임계는 모두 **advisory**로서 영역·해상도·계절·기준자료에 따라 달라진다(§G 준수).
