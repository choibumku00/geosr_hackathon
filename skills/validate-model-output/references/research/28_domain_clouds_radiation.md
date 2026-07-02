# 도메인: 구름·복사 (Clouds & Radiation) 검증·분석 방법 카탈로그

이 문서는 지구시스템/기후·대기 모델의 **구름(cloud)·복사(radiation)** 산출물을 위성(CERES·ISCCP·CloudSat·CALIPSO·MODIS·MISR)·지상 관측망(BSRN·ARM)·재분석(ERA5 등)과 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 구름·복사 검증의 핵심 3축은 (1) **복사플럭스 bias**(단파 SW/장파 LW, 하향·상향, 지표 및 TOA)와 **지표복사수지 닫힘**, (2) **구름장 검증**(구름량 cloud fraction의 공간·연직 분포, 운정 고도·온도, 광학두께 COD, ISCCP τ–p 결합히스토그램·구름레짐), (3) **구름복사효과 CRE**(all-sky − clear-sky) 및 이들의 **일변동·계절변동·영역 의존성**이다. 모델–위성 구름 비교의 사과-대-사과(apples-to-apples)를 위해 **위성 시뮬레이터(COSP)** 사용이 사실상 표준이며, 이 원칙이 본 도메인 카드 전반을 관통한다.

표준 오차지표(RMSE·MAE·bias·상관·Taylor/Target·bootstrap·QQ 등)는 여기서 재정의하지 않고 **`01_error_statistics.md`·`02_spatial_pattern_verification.md`·`03_categorical_event_extremes.md`·`figures/16`(그림 카탈로그)로 교차링크**만 한다. 이 카드는 구름·복사 **고유** 방법과, 공통 지표를 이 도메인에 적용할 때의 전제·함정에 집중한다.

> **자료형 표기 약어**: [격자]=NetCDF 격자(모델/재분석/L3·L4 위성), [시계열]=지상관측소(BSRN·ARM) 점 관측, [트랙]=위성 연직/궤도 자료(CloudSat·CALIPSO along-track), [히스토그램]=τ–p 등 결합분포, [연직]=cloud fraction 연직프로파일.
> **"우리 모델 vs CERES/관측/재분석" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 함정**: 재분석·위성 L4는 참값이 아니라 기준(reference)이다 — `00_overview_taxonomy.md` §G 원칙을 이 도메인에도 그대로 강제한다. 특히 CERES-EBAF Surface·ERA5 복사는 이미 모델/복사전달을 거친 산물이므로 "관측 진값"으로 과신 금지.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **TOA 복사플럭스 bias (반사단파 RSUT·외향장파 OLR·흡수단파)** — 위성 대비 계통오차
- ★ **지표 하향 단파 검증 (SW↓, surface_downwelling_shortwave)** — BSRN/CERES 대비
- ★ **지표 하향 장파 검증 (LW↓, surface_downwelling_longwave)** — 수증기·구름 결합
- ★ **지표 상향 플럭스·알베도 (SW↑/LW↑, surface albedo)** — 표면 반사·방출
- ★ **지표 복사수지 닫힘 (Surface radiation budget closure, Rn)** — 순복사 잔차
- ★ **TOA 에너지수지 닫힘 / 지구 에너지불균형 (EEI)** — 전지구 순플럭스
- ★ **전운량 검증 (total cloud fraction, cloud_area_fraction)** — 공간 bias·상관
- ★ **연직 구름분율 프로파일 (cloud fraction profile)** — CALIPSO/CloudSat 대비
- ★ **저·중·고 구름량 분리 검증 (low/mid/high cloud fraction)** — 층별 진단
- ★ **구름 공간패턴 검증 (SSIM·FSS·패턴상관)** — §02 교차링크(구름장 적용)
- ★ **구름복사효과 CRE (SW·LW·net, TOA·surface)** — all-sky − clear-sky
- **CRE 커널·근사분해 (approximate partial radiative perturbation, APRP)** — SW CRE 요인분해
- ★ **운정 고도·온도·기압 검증 (CTH/CTT/CTP)** — 위성 운정 대비
- ★ **구름 광학두께 검증 (cloud optical depth, COD/τ)** — 분포·bias
- **구름 수·빙 경로 (LWP/IWP) 검증** — 마이크로파·위성 대비
- ★ **ISCCP τ–p 결합히스토그램 비교 (joint pc–tau histogram)** — 구름유형 분포
- ★ **구름레짐 / 기상상태 분류 (cloud regimes / weather states)** — 군집기반 진단
- ★ **위성 시뮬레이터 COSP (ISCCP/MODIS/MISR/CALIPSO/CloudSat)** — 사과-대-사과 필수전제
- **CloudSat 반사도·CFAD (레이더 reflectivity 연직분포)** — 강수·두꺼운 구름
- **CALIPSO 산란비 SR 히스토그램 (SR–height, GOCCP)** — 얇은 구름·연직구조
- ★ **일변동 검증 (diurnal cycle: 진폭·위상, 조화적합)** — 복사·구름 일주기
- ★ **계절순환·월평균 지도 검증 (seasonal/monthly climatology)** — 계절 bias
- ★ **구름–복사 관계 검증 (CRE vs cloud fraction, SWCRE 감도)** — 물리 정합
- **구름 위상(액체/얼음) 검증 (cloud phase / SLF)** — 남극해 SW bias 근원
- **청천 복사 검증 (clear-sky flux·에어로졸·수증기 분리)** — 구름 외 오차 격리
- ★ **지상관측망 매치업 (BSRN·ARM colocation)** — 점–격자 대표성오차
- **QQ·PDF 분포 비교 (플럭스·COD 분포·꼬리)** — §01/§03 교차링크
- ★ **Taylor·Target 종합 요약 (다지점·다변수)** — §01 교차링크(구름·복사 적용)

---

### ★ TOA 복사플럭스 bias (반사단파 RSUT / 외향장파 OLR / 흡수단파)
- 무엇을 측정/검증하나: 대기상단(TOA)에서 모델이 산출한 반사 단파(reflected SW, RSUT), 외향 장파(OLR=`toa_outgoing_longwave_flux`), 입사 단파, 흡수 단파(=입사−반사)를 위성(CERES-EBAF TOA)과 비교해 계통 bias·공간분포를 진단. 복사 검증의 최상위 1차 지표.
- 정의·수식: bias(x,y)=mean(model−CERES), RMSE·상관은 §01. net TOA = SW_in − SW_up − LW_up. all-sky·clear-sky를 각각 비교(둘의 차가 CRE). 전지구·위도대 평균, 반구 대칭성도 병행.
- 적용 도메인/자료형: [격자] 모델 vs [격자] CERES-EBAF TOA(1°, 월/일). NetCDF↔NetCDF.
- 입력·전제: 동일 기간·공통 격자로 재격자화(보존형 권장), 입사 단파의 태양상수·궤도(지구-태양 거리)·달력 정합. all-sky/clear-sky 정의 통일 — **모델 clear-sky는 구름 제거 재계산(Method II)**이라 CERES의 clear-sky 판별(구름 없는 장면 샘플링)과 정의가 달라 clear-sky·CRE 비교 시 편향 유발(카드 '청천 복사' 참조).
- 해석 기준(advisory): CERES-EBAF TOA 자체 불확실성(전지구 순 ~수 W/m² 수준)을 하한으로 본다. 특정 RMSE·bias 임계로 good/bad 단정 금지 — **영역·계절·해상도 의존**(폭풍대·열대수렴대·사막·해빙역에서 bias 성격이 다름). RSUT bias는 흔히 구름량·구름 알베도 오차와 결합해 해석해야 함.
- 한계·주의(§G 연결): CERES-EBAF는 TOA 순플럭스를 지구에너지불균형 관측 추정치에 맞춰 조정(balancing)한 산물 → "절대 진값" 아님. 입사 단파 정의(연평균 vs 순간)·야간 마스크 불일치가 인위적 SW bias를 만든다.
- 출처: Loeb et al. (2018) "Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced and Filled (EBAF) Top-of-Atmosphere (TOA) Edition-4.0," *Journal of Climate* 31(2):895–918 (doi:10.1175/JCLI-D-17-0208.1); NASA CERES EBAF 문서; Wild et al. (2013, *Climate Dynamics*, global energy balance).

---

### ★ 지표 하향 단파 검증 (SW↓ / surface_downwelling_shortwave_flux_in_air)
- 무엇을 측정/검증하나: 지표에 도달하는 하향 단파복사(global horizontal irradiance)를 모델이 정확히 모의하는지. 구름 반사·에어로졸·표면 알베도가 결합된 핵심 표면 강제력.
- 정의·수식: bias/RMSE/상관은 §01. 지상관측(BSRN/ARM) 1분~시간 자료를 모델 시간축으로 집계. all-sky vs clear-sky SW↓ 분리로 구름 효과 격리.
- 적용 도메인/자료형: [시계열] BSRN/ARM 점 관측, [격자] CERES-EBAF Surface·SYN1deg vs 모델 [격자]. CF standard_name: `surface_downwelling_shortwave_flux_in_air`(모델 변수 rsds).
- 입력·전제: 점–격자 대표성오차(카드 'BSRN 매치업'), 지형 그림자·경사 보정(산악), 태양천정각 계산 정합. clear-sky 판별(구름 마스크) 통일.
- 해석 기준(advisory): 다수 모델·재분석이 **구름 과소 → SW↓ 과대(too much sunshine)** 경향(특히 남극해·열대 육상). CERES-Surface 제품 간 bias 차(예: SYN1deg가 EBAF보다 SW↓ 과대 보고 사례 존재)를 감안 — 절대 임계 단정 금지, 계절·구름레짐 의존.
- 한계·주의(§G 연결): CERES-EBAF Surface는 위성 TOA + 재분석 대기상태로 복사전달 계산한 **유도(derived) 산물** → 독립 진값 아님. 지상 SW↓는 국지 에어로졸·부분운(broken cloud) 순간 변동이 커 순간 매치업 노이즈 큼(시간평균 권장).
- 출처: Kato et al. (2018) "Surface Irradiances of Edition 4.0 CERES-EBAF Data Product," *Journal of Climate* 31(11):4501–4527 (doi:10.1175/JCLI-D-17-0523.1); Driemel et al. (2018) "Baseline Surface Radiation Network (BSRN): structure and data description (1992–2017)," *Earth System Science Data* 10:1491–1501 (doi:10.5194/essd-10-1491-2018); Wild et al. (2015, *Climate Dynamics*, surface SW).

---

### ★ 지표 하향 장파 검증 (LW↓ / surface_downwelling_longwave_flux_in_air)
- 무엇을 측정/검증하나: 대기(수증기·구름·CO₂·기온)가 지표로 방출하는 하향 장파복사. 야간 냉각·온실효과·구름 저층 진단의 핵심.
- 정의·수식: bias/RMSE는 §01. clear-sky LW↓는 대기 수증기·기온 프로파일에 지배, CRE_LW(surface)=all-sky−clear-sky LW↓.
- 적용 도메인/자료형: [시계열] BSRN/ARM(pyrgeometer), [격자] CERES-EBAF Surface vs 모델(rlds). CF: `surface_downwelling_longwave_flux_in_air`.
- 입력·전제: 근지표 기온·수증기 동시 검증 필요(LW↓ 오차의 상당부분이 기온·수증기 오차 전가). 구름 저면 고도·운량 정합.
- 해석 기준(advisory): 건조·한랭 대기(극지·고산)에서 clear-sky LW↓ 모의가 특히 어려움(수증기 연속흡수 continuum 파라미터화 민감). 임계 단정 금지 — 대기상태·계절 의존.
- 한계·주의(§G 연결): LW↓ bias는 복사코드 오차·구름 오차·상태변수(T, q) 오차가 뒤섞임 → clear-sky/all-sky 분리와 상태변수 동시 검증 없이는 원인 귀속 불가.
- 출처: Kato et al. (2018, *J. Climate*, CERES-EBAF Surface Ed4); Driemel et al. (2018, *ESSD*, BSRN); Wild (2020, *Reviews of Geophysics*/관련 종설, global energy balance — 확인요).

---

### ★ 지표 상향 플럭스 및 알베도 (SW↑ / LW↑ / surface albedo)
- 무엇을 측정/검증하나: 지표 반사 단파(SW↑), 방출 장파(LW↑), 그로부터 유도되는 지표 알베도(=SW↑/SW↓)·표면 방출온도. 눈·해빙·사막·식생 표면 특성 검증.
- 정의·수식: albedo = SW↑/SW↓. LW↑ ≈ εσT_s⁴(+반사 LW↓). bias/RMSE는 §01.
- 적용 도메인/자료형: [시계열] BSRN(4성분 복사), [격자] CERES-Surface·MODIS 알베도 vs 모델(rsus, rlus).
- 입력·전제: SW↑는 SW↓ 정확도에 의존(비율 산정 시 저조도 순간 불안정 → 주간·고태양각 필터). 표면 방출률 ε·skin temperature 정의 정합.
- 해석 기준(advisory): 눈·해빙 알베도 phase/두께 의존이 커 계절·표면상태별로 해석. 단일 임계 금지.
- 한계·주의(§G 연결): 알베도는 SW↓·SW↑ 두 오차의 비율 → 소분모(저조도)·부분운에서 불안정. MODIS 알베도도 BRDF 모델 산물(진값 아님).
- 출처: Kato et al. (2018, *J. Climate*, CERES-EBAF Surface); Schaaf et al. (2002, *Remote Sensing of Environment*, MODIS BRDF/albedo — 확인요); Driemel et al. (2018, *ESSD*, BSRN 4성분).

---

### ★ 지표 복사수지 닫힘 (Surface radiation budget closure, net radiation Rn)
- 무엇을 측정/검증하나: 4성분 복사(SW↓, SW↑, LW↓, LW↑)로 구성되는 지표 순복사 Rn = (SW↓−SW↑)+(LW↓−LW↑)의 모델·관측 일치와 성분 간 상쇄오차. 지표 에너지수지(현열·잠열·지중열 SEB)와의 연결 진단.
- 정의·수식: Rn = SW_net + LW_net. 관측 잔차 검증은 §04(보존·수지 닫힘)의 표면강제 개념과 연결. 성분별 bias의 부호·상쇄 분석.
- 적용 도메인/자료형: [시계열] BSRN/ARM/FLUXNET(4성분 + 난류플럭스), [격자] CERES-Surface vs 모델.
- 입력·전제: 4성분 동시 관측·동일 시각. 지표 에너지수지 닫힘(SEB closure) 자체가 관측에서도 불완전(관측 SEB 잔차 통상 존재) → "닫힘"의 기준을 관측 불확실성 안에서 판단.
- 해석 기준(advisory): 성분별 bias가 상쇄해 Rn이 우연히 맞을 수 있음(보상오차) → 반드시 4성분 각각 검증. 임계 단정 금지.
- 한계·주의(§G 연결): 관측 SEB 자체 미닫힘(에너지 불균형)이 알려진 문제 → 관측을 절대기준으로 삼지 말 것. §04 수지닫힘 카드와 교차.
- 출처: Wild et al. (2013) "The global energy balance from a surface perspective," *Climate Dynamics* 40:3107–3134 (doi:10.1007/s00382-012-1569-8); Stephens et al. (2012) "An update on Earth's energy balance in light of the latest global observations," *Nature Geoscience* 5:691–696 (doi:10.1038/ngeo1580).

---

### ★ TOA 에너지수지 닫힘 / 지구 에너지불균형 (Earth energy imbalance, EEI)
- 무엇을 측정/검증하나: 전지구 평균 TOA 순플럭스(입사 SW − 반사 SW − OLR)가 관측 EEI(양의 소량, 수증·해양 열저장과 정합)와 맞는지. 모델의 장기 에너지 표류(drift) 진단.
- 정의·수식: EEI = ⟨SW_in − SW_up − LW_up⟩(전지구·연평균). 관측 EEI는 해양 열함량 변화율(OHC)로 제약. 모델은 스핀업·drift 점검.
- 적용 도메인/자료형: [격자] 모델 전지구 적분 vs CERES-EBAF(+해양 OHC 관측). §04 전지구 에너지수지와 연결.
- 입력·전제: 면적가중(cosφ) 전지구 평균, 장기(≥연) 평균, drift 제거. CERES-EBAF는 절대값을 EEI 관측에 맞춰 조정했으므로 절대 순플럭스 비교엔 부적합(패턴·시간변화 위주).
- 해석 기준(advisory): 관측 EEI는 소량의 양(net 흡수) — 모델이 부호·크기 정합하는지, 인위적 drift가 없는지. 절대값 임계보다 "관측 불확실성 대비 정합".
- 한계·주의(§G 연결): CERES 절대값은 balancing 적용 산물 → 절대 비교 부적절. 모델 top-of-model vs TOA 차이(상부 대기 흡수) 주의.
- 출처: Loeb et al. (2018, *J. Climate*, CERES-EBAF TOA Ed4); von Schuckmann et al. (2020) "Heat stored in the Earth system: where does the energy go?," *Earth System Science Data* 12:2013–2041 (doi:10.5194/essd-12-2013-2020).

---

### ★ 전운량 검증 (Total cloud fraction, cloud_area_fraction)
- 무엇을 측정/검증하나: 격자별 전운량(0~1 또는 %)의 모델–위성 공간 일치·계통 bias. 구름 검증의 1차 지표이자 복사 bias의 주요 원인 진단.
- 정의·수식: bias(x,y)=mean(model−obs), 공간 RMSE·패턴상관은 §01/§02. 전운량은 연직 중첩가정(random/maximum-random overlap)에 의존 → 모델 진단과 위성 관측 정의 통일 필요.
- 적용 도메인/자료형: [격자] 모델(clt) vs ISCCP·MODIS·CALIPSO-GOCCP·CERES 구름 [격자]. CF: `cloud_area_fraction`(전운량), `cloud_area_fraction_in_atmosphere_layer`(층운량).
- 입력·전제: **위성 시뮬레이터(COSP) 사용 강력 권장** — 위성은 광학적으로 얇은 구름·중첩을 다르게 감지(passive ISCCP는 τ 임계, active CALIPSO는 얇은권운 민감). 시뮬레이터 없이 모델 총운량을 위성과 직접 비교하면 정의 불일치로 편향.
- 해석 기준(advisory): 위성 간에도 전운량이 다름(CALIPSO가 ISCCP·MODIS보다 총운량 높음 — 얇은 구름 감지) → "관측"이 하나가 아님. 임계 단정 금지, 관측 스프레드 안에서 상대평가.
- 한계·주의(§G 연결): 중첩가정·τ 감지임계·연직해상도에 결과 민감. 정지위성 vs 극궤도 샘플링 시각 차(일변동 aliasing).
- 출처: Rossow & Schiffer (1999) "Advances in understanding clouds from ISCCP," *Bulletin of the American Meteorological Society* 80(11):2261–2287; Chepfer et al. (2010, *JGR*, CALIPSO-GOCCP, 아래 카드); Pincus et al. (2012, *J. Climate*, MODIS 시뮬레이터·구름 비교 — 확인요).

---

### ★ 연직 구름분율 프로파일 (Cloud fraction profile)
- 무엇을 측정/검증하나: 고도(또는 기압)별 구름분율의 연직 분포를 모델–위성 연직관측(CALIPSO·CloudSat)과 비교. 저층운·중층운·권운의 고도 배치 오차 진단(전운량이 맞아도 연직 배치가 틀릴 수 있음).
- 정의·수식: CF(z) 프로파일 비교. 연직 상관·층별 bias, zonal-mean CF(위도–고도 단면) 지도.
- 적용 도메인/자료형: [연직]/[트랙] CALIPSO-GOCCP·CloudSat-CALIPSO 결합 vs 모델 연직 CF(COSP lidar/radar 시뮬레이터 산물). [격자]로 zonal-mean화.
- 입력·전제: **COSP CALIPSO/CloudSat 시뮬레이터 필수** — 능동센서의 감쇠(attenuation, 두꺼운 구름 아래 신호 소실)·최소감지 반사도를 모델에도 적용해야 공정 비교. 연직해상도·SR 임계 정합.
- 해석 기준(advisory): 저층운 과소·권운 배치 오차가 흔함 — 영역·계절 의존. lidar는 두꺼운 저층운에 감쇠(위 구름에 가림), radar는 얇은권운 놓침 → 두 센서 상보(결합 산물 권장).
- 한계·주의(§G 연결): 단일 센서로는 연직 전 구간 불완전(lidar 감쇠 vs radar 최소감지). SR/reflectivity 임계 선택이 CF를 최대 ~0.2까지 바꿈(GOCCP 민감도).
- 출처: Chepfer et al. (2010) "The GCM-Oriented CALIPSO Cloud Product (CALIPSO-GOCCP)," *Journal of Geophysical Research: Atmospheres* 115:D00H16 (doi:10.1029/2009JD012251); Kay et al. (2012, *J. Climate*, CESM CALIPSO 시뮬레이터 평가 — 확인요); Cesana & Chepfer (2013, *JGR*, CMIP5 구름 연직구조).

---

### ★ 저·중·고 구름량 분리 검증 (Low / mid / high cloud fraction)
- 무엇을 측정/검증하나: 운정 기압 구간으로 나눈 저층(>680 hPa)·중층(680–440 hPa)·고층(<440 hPa) 구름량을 각각 검증(ISCCP 관례 구간). 층별로 복사효과·오차 성격이 달라 분리 진단이 필수.
- 정의·수식: ISCCP 고도 구분 기준으로 층별 CF 집계 후 bias/상관. 저층운은 SW 냉각(알베도), 고층운은 LW 가열(온실) 지배.
- 적용 도메인/자료형: [격자] 모델(cll/clm/clh) vs ISCCP·MODIS·CALIPSO 층운량. COSP-ISCCP 시뮬레이터 산물 권장.
- 입력·전제: 층 경계·중첩가정·τ 임계 정합. 저층운은 상위 구름에 가려 위성 감지 어려움(passive) → 시뮬레이터로 동일 조건.
- 해석 기준(advisory): 해양 저층운(Sc) 과소가 SW bias(남극해·아열대 동안류)의 흔한 근원 — 영역 의존. 임계 단정 금지.
- 한계·주의(§G 연결): passive 위성은 다층·중첩 시 최상단만 감지 → 저·중층 과소. 시뮬레이터 없는 층별 직접비교는 편향.
- 출처: Rossow & Schiffer (1999, *BAMS*, ISCCP 층 구분); Klein et al. (2013) "Are climate model simulations of clouds improving? An evaluation using the ISCCP simulator," *Journal of Geophysical Research: Atmospheres* 118:1329–1342 (doi:10.1002/jgrd.50141).

---

### ★ 구름 공간패턴 검증 (SSIM / FSS / 패턴상관 — 구름장 적용)
- 무엇을 측정/검증하나: 구름량·플럭스 **공간장(map)**의 구조적 유사성·이웃기반 일치·패턴상관. 격자별 bias가 못 보는 "구름 위치·형태" 오차를 포착. AI/다운스케일 구름 산출물 평가에 특히 유용.
- 정의·수식: 재정의 없이 §02(공간패턴 검증)와 `figures/16` 교차링크. SSIM(구조유사도), FSS(이웃 임계초과 분율, useful-scale), 패턴상관/ACC를 구름 필드에 적용.
- 적용 도메인/자료형: [격자] 구름량·SW↓·CRE 지도. 위성 L3/L4 vs 모델(COSP 산물).
- 입력·전제: 동일 격자·마스크. FSS는 임계·이웃크기 스캔(§02 공통), SSIM은 동적범위 정규화.
- 해석 기준(advisory): §02의 원칙 준용 — useful-scale·SSIM 임계는 advisory, **해상도·영역 의존**. double-penalty(위치 약간 어긋나면 이중감점) 주의.
- 한계·주의(§G 연결): 공간 지표는 자료형·해상도에 강하게 의존 → §02 캐비앗 상속. 위성-모델 해상도 불일치 시 재격자화 산물.
- 출처: §02_spatial_pattern_verification.md(SSIM·FSS·패턴상관 정의 및 출처); `figures/16`(그림 카탈로그). (구름장 적용 사례: Klein et al. 2013, *JGR*; Bodas-Salcedo et al. 2011, *BAMS*.)

---

### ★ 구름복사효과 CRE (SW / LW / net; TOA·surface)
- 무엇을 측정/검증하나: 구름이 복사수지에 미치는 순효과 = all-sky − clear-sky 플럭스. 구름 검증과 복사 검증을 잇는 핵심 통합지표. TOA·surface·대기(atmosphere=TOA−surface) 각각.
- 정의·수식: CRE_SW = (SW_net,allsky − SW_net,clearsky), CRE_LW = (LW_net,allsky − LW_net,clearsky)_부호규약 주의, CRE_net = CRE_SW + CRE_LW. TOA에서 CRE_SW<0(냉각), CRE_LW>0(가열), 전지구 net CRE<0(순냉각). bias/RMSE는 §01.
- 적용 도메인/자료형: [격자] 모델 vs CERES-EBAF(all-sky·clear-sky 동시 제공). TOA·surface 모두.
- 입력·전제: **clear-sky 정의 일치가 결정적** — CERES clear-sky는 "구름 없는 장면 샘플링"(관측), 모델 clear-sky는 통상 "구름 제거 재계산" → 정의 불일치가 CRE bias로 나타남. 가능하면 모델도 샘플링 정합(또는 편향 명시).
- 해석 기준(advisory): 전지구 net CRE ~순냉각(SW CRE ~수십 W/m² 음, LW CRE ~수십 W/m² 양 — 값은 자료·기간 의존). 지역 CRE bias(예: 남극해 SW CRE 과소음=구름 너무 적거나 반사 약함) 진단. 임계 단정 금지, 영역·계절 의존.
- 한계·주의(§G 연결): clear-sky 정의 불일치(Method I 샘플링 vs Method II 재계산)로 인한 인위적 편향이 CRE 비교의 최대 함정. SW CRE는 태양광 있는 곳만 유효(주간·계절 마스크).
- 출처: Loeb et al. (2018, *J. Climate*, CERES-EBAF TOA Ed4); Allan (2011, *Meteorological Applications*, CRE 개념 — 확인요); Sohn et al. (clear-sky 정의 차이 — 확인요). GFDL "Cloud Radiative Effect" 기술설명.

---

### CRE 요인분해 / 근사부분복사섭동 (Approximate Partial Radiative Perturbation, APRP)
- 무엇을 측정/검증하나: SW CRE(또는 planetary albedo) 오차를 구름량(cloud amount)·구름 광학두께(optical thickness/scattering)·표면 알베도·대기 흡수 등 **기여요인별로 분해**해 "어느 물리량이 복사 bias를 만드는가"를 귀속.
- 정의·수식: APRP는 단파 복사를 소수의 물리 파라미터(대기 산란/흡수, 구름 산란/흡수, 표면 알베도)로 근사한 뒤 각 파라미터 교란의 복사 기여를 분리. 커널(radiative kernel)법과 상보.
- 적용 도메인/자료형: [격자] 두 상태(모델 vs 관측/기준, 또는 모델A vs 모델B)의 SW 플럭스·구름속성. CERES + 구름속성.
- 입력·전제: all-sky/clear-sky SW, 구름 속성(운량·τ). 근사(선형·독립성) 가정.
- 해석 기준(advisory): "SW bias의 X%가 구름량, Y%가 구름 광학두께 탓" 식 귀속 — 근사 오차 동반. 절대값보다 상대 기여 해석.
- 한계·주의(§G 연결): 선형·독립 근사 → 강한 비선형·다층 상황에서 오차. 요인 상호작용(cross-term) 잔차 존재.
- 출처: Taylor et al. (2007) "Estimating shortwave radiative forcing and response in climate models," *Journal of Climate* 20(11):2530–2543 (doi:10.1175/JCLI4143.1); Zelinka et al. (2012, *J. Climate*, cloud radiative kernels — 확인요).

---

### ★ 운정 고도·온도·기압 검증 (CTH / CTT / CTP)
- 무엇을 측정/검증하나: 운정 고도(cloud top height), 운정 온도(temperature), 운정 기압(pressure)의 모델–위성 일치. 구름의 연직 배치·LW CRE(운정 온도가 좌우) 진단.
- 정의·수식: bias/RMSE/분포 비교는 §01. 위성 CTP는 ISCCP τ–p의 p축(아래 히스토그램 카드)과 연결. CTT는 LW 방출온도 결정.
- 적용 도메인/자료형: [격자]/[트랙] ISCCP·MODIS·MISR·CALIPSO 운정 vs 모델(COSP 산물). MISR은 스테레오 CTH(온도 무관).
- 입력·전제: 위성 운정 정의 차이 — passive(ISCCP/MODIS)는 복사온도→고도 환산(다층 시 최상단·유효고도), MISR은 기하학적 CTH, CALIPSO는 광학적 운정. 시뮬레이터로 정의 정합.
- 해석 기준(advisory): passive는 얇은권운 운정을 낮게(따뜻하게) 편향, active는 실제 최상단 감지 → 관측 간 차 큼. 임계 단정 금지.
- 한계·주의(§G 연결): 운정 정의가 센서마다 다름 → "관측 진값" 단일 아님. 다층운에서 유효운정과 실제 최상단 불일치.
- 출처: Marchand et al. (2010) "A review of cloud top height and optical depth histograms from MISR, ISCCP, and MODIS," *Journal of Geophysical Research: Atmospheres* 115:D16206 (doi:10.1029/2009JD013422); Rossow & Schiffer (1999, *BAMS*, ISCCP).

---

### ★ 구름 광학두께 검증 (Cloud optical depth, COD / τ)
- 무엇을 측정/검증하나: 구름 광학두께 τ의 모델–위성 분포·bias. τ는 SW 반사(구름 알베도)를 지배 → SW CRE 오차의 직접 원인.
- 정의·수식: τ 분포(히스토그램/평균)·bias. QQ로 꼬리(두꺼운 대류운) 비교. ISCCP τ–p 히스토그램의 τ축과 연결.
- 적용 도메인/자료형: [격자]/[히스토그램] ISCCP·MODIS τ vs 모델(COSP-ISCCP/MODIS 산물).
- 입력·전제: **passive τ는 주간·일정 태양각 조건에서만 산출** → 야간·저조도 결측, 태양각 층화. COSP로 관측 조건 정합. in-cloud vs grid-mean τ 구분.
- 해석 기준(advisory): 많은 모델이 "너무 적고 너무 두꺼운(too few, too bright)" 구름 경향(개수 부족을 광학두께 과대로 보상) → τ 분포가 실제보다 두꺼운 쪽 편향. 영역·구름유형 의존, 임계 단정 금지.
- 한계·주의(§G 연결): passive τ는 3D 복사·부분운·태양각 편향. 얼음/액체 τ 산출 가정 차이. 야간 결측으로 일변동 왜곡.
- 출처: Marchand et al. (2010, *JGR*, τ 히스토그램 리뷰); Nam et al. (2012) "The 'too few, too bright' tropical low-cloud problem in CMIP5 models," *Geophysical Research Letters* 39:L21801 (doi:10.1029/2012GL053421).

---

### 구름 수·빙 경로 검증 (Liquid / Ice Water Path, LWP / IWP)
- 무엇을 측정/검증하나: 연직 적분 구름 수액량(LWP)·빙량(IWP)의 모델–위성 일치. 구름 광학두께·복사효과·강수 효율의 물리 근원.
- 정의·수식: LWP=∫ρ_l q_l dz, IWP=∫ρ_i q_i dz. bias/분포 비교는 §01/§03. 강수 성분 포함/제외 정의 통일(모델은 종종 부유 응결물만, 위성은 강수 포함 가능).
- 적용 도메인/자료형: [격자] 마이크로파 LWP(SSM/I·AMSR, 해상), MODIS LWP/IWP, CloudSat IWP vs 모델(clwvi, clivi).
- 입력·전제: **강수/비강수 응결물 정의 불일치**가 최대 함정(모델 vs 위성). 해상 마이크로파는 육상 미가용. IWP 위성 산출 불확실성 매우 큼(가정 의존).
- 해석 기준(advisory): IWP 관측 불확실성이 커 모델 비교 신뢰도 낮음 → LWP(해상 MW) 우선. 임계 단정 금지.
- 한계·주의(§G 연결): 위성 LWP/IWP는 강한 retrieval 가정 산물(입자크기·상). 정의(강수 포함 여부)·표면(해/육) 제약.
- 출처: Elsaesser et al. (2017, *J. Climate*, MAC-LWP — 확인요); Duncan & Eriksson (2018, *Atmospheric Chemistry and Physics*, IWP 불확실성 — 확인요); Waliser et al. (2009, *JGR*, cloud ice 모델-관측).

---

### ★ ISCCP τ–p 결합히스토그램 비교 (Joint cloud optical depth – cloud top pressure histogram)
- 무엇을 측정/검증하나: 광학두께(τ)와 운정기압(p_c)의 **2차원 결합분포**를 모델–ISCCP 간 비교. 단일 운량·τ가 못 보는 "구름 유형 구성(저층 두꺼운 Sc, 고층 얇은 권운, 깊은 대류 등)"을 한 장으로 진단. 구름 검증의 대표 고급 진단.
- 정의·수식: ISCCP 표준 격자는 τ 6구간 × p_c 7구간 = 42개 상자의 CF 분포(구간은 비선형). 모델–관측 히스토그램 차(상자별 bias), 히스토그램 거리(예: 상자별 RMS), 유형별 합(저/중/고 × 얇/두꺼움).
- 적용 도메인/자료형: [히스토그램] 모델(COSP-ISCCP 시뮬레이터 필수 산출) vs ISCCP D/H(pc–tau) 결합히스토그램.
- 입력·전제: **COSP-ISCCP 시뮬레이터 없이는 성립 불가** — 모델 τ, p_c를 ISCCP 감지·중첩 규약대로 재현해야 함. τ 임계(가시성)·주간 제약 정합.
- 해석 기준(advisory): 상자별 차로 "어떤 구름유형이 과다/과소"인지 직접 판독(예: 저층 두꺼운 구름 과소 → SW 냉각 부족). 임계 단정 대신 유형 분포 형태로 해석. 영역별 히스토그램 별도.
- 한계·주의(§G 연결): passive 다층·부분운 편향이 상자 배치에 스며듦. τ–p 구간 비선형 → 상자 면적가중 주의. 야간 결측(일변동 왜곡).
- 출처: Klein & Jakob (1999) "Validation and sensitivities of frontal clouds simulated by the ECMWF model," *Monthly Weather Review* 127:2514–2531(τ–p 진단 도입); Webb et al. (2001) "Combining ERBE and ISCCP data to assess clouds in the Hadley Centre, ECMWF and LMD atmospheric climate models," *Climate Dynamics* 17:905–922; Klein et al. (2013, *JGR*, ISCCP 시뮬레이터 평가).

---

### ★ 구름레짐 / 기상상태 분류 (Cloud regimes / Weather states)
- 무엇을 측정/검증하나: τ–p 결합히스토그램을 군집화(k-means)해 얻은 **구름레짐(weather states, WS)**(예: 층적운 레짐, 깊은대류 레짐, 얇은권운 레짐 등)의 발생빈도·복사효과를 모델–관측 비교. 구름을 개별 격자가 아니라 "역학적으로 의미있는 유형"으로 묶어 진단.
- 정의·수식: 관측 τ–p 히스토그램을 k-means로 군집(ISCCP WS 세트) → 각 레짐 중심(centroid)과 발생빈도(RFO)·레짐별 CRE. 모델(COSP 히스토그램)을 동일 centroid에 할당해 RFO·CRE 비교.
- 적용 도메인/자료형: [히스토그램] 모델(COSP-ISCCP) vs ISCCP 구름레짐 산물. 영역/전지구.
- 입력·전제: COSP 히스토그램 필수. 관측에서 정의된 centroid를 모델에 적용(공통 기준). 군집 수·초기화 민감.
- 해석 기준(advisory): 레짐별 RFO 오차·레짐 내 CRE 오차로 "구름유형 빈도 오차 vs 유형 내 속성 오차" 분리. 임계 단정 금지, 영역·계절 의존.
- 한계·주의(§G 연결): 군집 결과가 자료·k에 의존. passive 히스토그램 편향 상속. 정지·극궤도 샘플링 차.
- 출처: Jakob & Tselioudis (2003) "Objective identification of cloud regimes in the Tropical Western Pacific," *Geophysical Research Letters* 30(21):2082 (doi:10.1029/2003GL018367); Tselioudis et al. (2013, *J. Climate*, global weather states — 확인요); Williams & Webb (2009, *Climate Dynamics*, cloud regimes 모델평가 — 확인요).

---

### ★ 위성 시뮬레이터 COSP (ISCCP/MODIS/MISR/CALIPSO/CloudSat simulator)
- 무엇을 측정/검증하나: 방법이라기보다 **필수 전처리·비교 프레임워크**. 모델 대기상태에서 "위성이 실제로 보았을 구름"을 모의(subcolumn 생성 + 각 센서 관측연산자) → 위성 산출물과 사과-대-사과 비교를 가능케 함. ISCCP/MODIS/MISR(passive)·CALIPSO/CloudSat(active) 시뮬레이터 통합.
- 정의·수식: 모델 격자 → SCOPS(subcolumn overlap sampling) → 각 시뮬레이터가 센서 감지특성(τ 임계·최소 반사도·감쇠·태양각) 적용 → 위성-정합 구름 진단(τ–p 히스토그램, CF 프로파일, reflectivity CFAD, SR 히스토그램 등) 산출.
- 적용 도메인/자료형: 모델 [격자]→위성정합 진단([히스토그램]/[연직]). 위 구름 카드 대부분의 전제.
- 입력·전제: 모델 3D 구름속성(운량·수·빙 함량·유효반경)·중첩가정·서브그리드 변동. 관측은 동일 시뮬레이터 규약으로 만든 CFMIP-obs(GOCCP·ISCCP-sim 등).
- 해석 기준(advisory): 시뮬레이터 적용 후에도 남는 차이가 "실제 모델 오차"에 가깝다. 시뮬레이터 미적용 직접비교는 정의불일치 오차와 물리오차가 뒤섞임 → 결론 신뢰도 낮음.
- 한계·주의(§G 연결): 시뮬레이터 자체 가정(서브그리드 중첩·유효반경)도 오차원. 버전(COSP1/COSP2) 간 차. 계산비용 큼.
- 출처: Bodas-Salcedo et al. (2011) "COSP: Satellite simulation software for model assessment," *Bulletin of the American Meteorological Society* 92(8):1023–1043 (doi:10.1175/2011BAMS2856.1); Swales et al. (2018) "The Cloud Feedback Model Intercomparison Project Observational Simulator Package: Version 2 (COSP2)," *Geoscientific Model Development* 11:77–81 (doi:10.5194/gmd-11-77-2018).

---

### CloudSat 레이더 반사도 CFAD (Contoured Frequency by Altitude Diagram)
- 무엇을 측정/검증하나: 94 GHz 구름레이더 반사도(dBZ)의 고도별 발생빈도 분포(CFAD)를 모델(COSP-CloudSat)–관측 비교. 두꺼운 구름·강수 응결물의 연직구조·크기 진단.
- 정의·수식: 각 고도에서 반사도 히스토그램 → 2D(고도×dBZ) 빈도장. 모델–관측 CFAD 차. reflectivity는 입자 크기·수농도의 6제곱 등에 민감.
- 적용 도메인/자료형: [트랙]/[연직] CloudSat CPR vs 모델(COSP-CloudSat 산출). zonal/영역.
- 입력·전제: COSP radar 시뮬레이터로 모델 반사도 계산(감쇠·최소감지 −30 dBZ 정합). 강수/구름 응결물 구분.
- 해석 기준(advisory): CloudSat은 얇은권운(약반사) 놓침·지표근처 클러터 → 저고도·약반사 해석 주의. 영역 의존.
- 한계·주의(§G 연결): reflectivity–질량 관계 가정 민감. 지표 클러터(하부 ~1km) 마스크. lidar와 상보 필요.
- 출처: Bodas-Salcedo et al. (2008) "Evaluating cloud systems in the Met Office global forecast model using simulated CloudSat radar reflectivities," *Journal of Geophysical Research* 113:D00A13 (doi:10.1029/2007JD009620); Stephens et al. (2002, *BAMS*, CloudSat mission).

---

### CALIPSO 산란비 SR 히스토그램 (Scattering Ratio–height, GOCCP)
- 무엇을 측정/검증하나: 라이다 산란비(SR) 프로파일의 고도별 분포(SR–height 히스토그램)를 모델(COSP-lidar)–CALIPSO-GOCCP 비교. 얇은권운·저층운 등 광학적으로 얇은 구름의 연직구조 진단(레이더가 놓치는 영역).
- 정의·수식: SR = 관측 후방산란 / 분자 후방산란. SR>임계(예: 5)를 구름으로 판정. 고도별 SR 분포·CF(z)·저/중/고/총 CF 산출.
- 적용 도메인/자료형: [연직]/[트랙] CALIPSO-GOCCP vs 모델(COSP lidar 시뮬레이터).
- 입력·전제: 동일 SR 임계·연직해상도. lidar는 두꺼운 구름에 감쇠(아래 가림).
- 해석 기준(advisory): SR 임계·연직해상도 선택이 CF를 최대 ~0.2 변화(GOCCP 민감도) → advisory. 얕은 적운역 특히 민감.
- 한계·주의(§G 연결): lidar 감쇠로 두꺼운 저층운 아래 정보 손실. 임계 의존. radar와 결합 권장.
- 출처: Chepfer et al. (2010, *JGR*, CALIPSO-GOCCP, doi:10.1029/2009JD012251); Cesana & Chepfer (2013, *JGR*, CMIP5 연직구조 — 확인요).

---

### ★ 일변동 검증 (Diurnal cycle: 진폭·위상, 조화적합)
- 무엇을 측정/검증하나: SW↓·구름량·대류성 구름의 하루 주기(진폭·최대시각/위상)를 모델–관측 비교. 대류·경계층 구름의 시간구조 진단(월평균이 맞아도 일변동이 틀릴 수 있음).
- 정의·수식: 시간별 합성(composite) 일주기 → 1차 조화적합(diurnal harmonic)으로 진폭·위상 추출(재정의는 §06 시계열/조화). 위상은 원형량(시각) 취급.
- 적용 도메인/자료형: [시계열] BSRN/ARM(고빈도), [격자] 정지위성(운량·CRE) vs 모델(시간별 출력 필요).
- 입력·전제: 모델 시간별(≤3h) 출력, 지방태양시 정합. 정지위성(고빈도) vs 극궤도(고정시각, 일변동 불가) 구분.
- 해석 기준(advisory): 대류운 최대시각(육상 오후 vs 해양 새벽) 위상오차가 흔함 — 지역 의존. 위상은 시각 순환량으로 해석. 임계 단정 금지.
- 한계·주의(§G 연결): 극궤도 위성은 일변동 aliasing(고정 통과시각). 위상은 0/24h wrap 처리 필요.
- 출처: Yang & Slingo (2001) "The diurnal cycle in the tropics," *Monthly Weather Review* 129:784–801 (doi:10.1175/1520-0493); §06_timeseries_signal.md(조화·위상 정의).

---

### ★ 계절순환·월평균 지도 검증 (Seasonal / monthly climatology maps)
- 무엇을 측정/검증하나: 복사플럭스·구름량·CRE의 월평균/계절(DJF·JJA) 기후값 지도와 계절진폭·위상의 모델–관측 일치. 계절별로 bias 성격이 바뀌므로 연평균만으로는 불충분.
- 정의·수식: 월/계절 climatology의 bias(x,y)·패턴상관(§01/§02). 계절진폭·최대월(원형 위상). zonal-mean 계절-위도 단면.
- 적용 도메인/자료형: [격자] CERES-EBAF·ISCCP·GOCCP 월평균 vs 모델. 다년 평균.
- 입력·전제: 동일 기준기간 climatology(§02 ACC 원칙: climatology 정의 일치). 충분한 연수.
- 해석 기준(advisory): 계절 반전 영역(몬순·해빙역)에서 bias 부호가 계절마다 바뀜 → 계절별 별도 해석. 임계 단정 금지.
- 한계·주의(§G 연결): 짧은 기간 climatology는 내부변동 오염. 기준기간 불일치가 인위적 차. §G 원칙 상속.
- 출처: Loeb et al. (2018, *J. Climate*, CERES-EBAF); §02(ACC·패턴상관·climatology 정합).

---

### ★ 구름–복사 관계 검증 (CRE vs cloud fraction 등 물리 정합)
- 무엇을 측정/검증하나: 개별 변수가 아니라 **구름과 복사의 관계**(예: 저층운량↔SW CRE, 운정온도↔LW CRE, τ↔구름 알베도)가 관측과 정합하는지. "맞는 복사를 맞는 이유(구름)로" 내는지 진단(보상오차 검출).
- 정의·수식: 두 변수의 결합분포·회귀(예: SW CRE = f(low CF))를 모델·관측에서 비교. 조건부 합성(예: 구름레짐별 CRE), 산점/이변량 분포.
- 적용 도메인/자료형: [격자] CERES CRE + ISCCP/CALIPSO 구름 vs 모델(동일 변수쌍).
- 입력·전제: 동일 격자·시각의 변수쌍. 인과가 아니라 정합 진단(공변). 구름레짐(위 카드)과 결합하면 강력.
- 해석 기준(advisory): 복사 bias가 작아도 관계가 틀리면(예: 구름 너무 적은데 광학두께 과대로 SW 보상) 물리적으로 부실 → 관계 검증으로 노출. 영역 의존, 임계 단정 금지.
- 한계·주의(§G 연결): 상관≠인과. 보상오차는 단일변수 검증으로 안 보임 → 관계·요인분해(APRP) 병행 필수.
- 출처: Nam et al. (2012, *GRL*, "too few, too bright"); Bony et al. (2004, *Climate Dynamics*, 구름-복사 관계 진단 — 확인요); Bodas-Salcedo et al. (2011, *BAMS*, COSP).

---

### 구름 위상(액체/얼음) 검증 (Cloud phase / Supercooled Liquid Fraction, SLF)
- 무엇을 측정/검증하나: 과냉각 액체·얼음 구름의 비율(위상)을 모델–위성(CALIPSO 위상) 비교. 남극해 SW bias·구름 알베도의 핵심 근원(액체가 얼음보다 반사 강함).
- 정의·수식: SLF = 액체 CF / (액체+얼음 CF), 온도(등온선)별 SLF 곡선. bias/프로파일 비교.
- 적용 도메인/자료형: [연직]/[격자] CALIPSO 위상·DARDAR vs 모델(COSP 위상 진단).
- 입력·전제: 위성 위상 판별(편광 lidar)과 모델 위상 진단 정합. 온도 층화.
- 해석 기준(advisory): 모델이 과냉각액체 과소(너무 빨리 얼림) → 남극해 구름 반사 약화 → SW↓ 과대 경향(영역 의존). 임계 단정 금지.
- 한계·주의(§G 연결): lidar 위상은 감쇠·최상단 편향. DARDAR 등 retrieval 가정 의존. §G 상속.
- 출처: Bodas-Salcedo et al. (2014) "Origins of the solar radiation biases over the Southern Ocean in CFMIP2 models," *Journal of Climate* 27(1):41–56 (doi:10.1175/JCLI-D-13-00169.1); Cesana et al. (2015, *JGR*, CALIPSO cloud phase — 확인요); Kay et al. (2016, *J. Climate*, Southern Ocean SW/phase — 확인요).

---

### 청천 복사 검증 (Clear-sky flux: 에어로졸·수증기 기여 분리)
- 무엇을 측정/검증하나: 구름 없는 조건의 복사플럭스(clear-sky SW/LW)를 검증해 **구름 이외**(수증기·에어로졸·기온·표면 알베도) 오차를 격리. CRE 계산의 기준면이자 복사코드 자체 검증.
- 정의·수식: clear-sky bias/RMSE(§01). clear-sky SW↓는 에어로졸 광학두께(AOD)·수증기에, clear-sky LW↓는 수증기·기온에 지배.
- 적용 도메인/자료형: [시계열] BSRN clear-sky, [격자] CERES clear-sky vs 모델. AERONET AOD 병행.
- 입력·전제: **clear-sky 정의 통일이 결정적** — CERES(구름 없는 장면 샘플링) vs 모델(구름 제거 재계산)의 정의 차. 에어로졸·수증기 입력 정합.
- 해석 기준(advisory): clear-sky bias가 크면 복사코드·에어로졸·수증기 문제(구름 아님)를 시사 → 원인 격리. 임계 단정 금지.
- 한계·주의(§G 연결): 정의 불일치(샘플링 vs 재계산)가 clear-sky·CRE 비교의 최대 함정(위 CRE 카드와 동일 원리). 에어로졸 강제력 불확실.
- 출처: Kato et al. (2018, *J. Climate*, CERES-EBAF Surface, clear-sky 정의); Loeb et al. (2018, *J. Climate*, TOA clear-sky); Sohn et al.(clear-sky sampling vs computation 차이 — 확인요).

---

### ★ 지상관측망 매치업 (BSRN / ARM colocation, 점–격자 대표성오차)
- 무엇을 측정/검증하나: 고정밀 지상 복사관측(BSRN·ARM)과 모델 격자값을 시공간 정합해 검증. 위성이 못 주는 지표 4성분 복사의 절대검증 기준.
- 정의·수식: 점 관측을 모델 격자·시간으로 매칭(최근접/보간), 시간평균 집계. 대표성오차(점 vs 격자 평균)는 §12/§15 개념 상속.
- 적용 도메인/자료형: [시계열] BSRN(>70소, 4성분)·ARM(SGP 등) vs 모델·CERES-Surface 격자.
- 입력·전제: 관측 QC(WRMC 플래그), 지형·시간대(UTC↔지방시), 태양각. 점 대표성(국지 에어로졸·부분운) → 순간보다 일/월평균 매치.
- 해석 기준(advisory): 점–격자 대표성오차가 SW↓ 순간 비교의 상당부분(부분운 변동) → 시간평균으로 완화. 사이트 분포 편중(북반구 육상) 주의.
- 한계·주의(§G 연결): BSRN 사이트 지리 편중 → 전지구 대표성 한계. 점 관측을 격자 진값처럼 쓸 때 대표성오차. §15 매치업 전제 준용.
- 출처: Driemel et al. (2018, *ESSD*, BSRN, doi:10.5194/essd-10-1491-2018); Ohmura et al. (1998, *BAMS*, BSRN 설립); Stokes & Schwartz (1994, *BAMS*, ARM — 확인요).

---

### QQ / PDF 분포 비교 (플럭스·COD 분포·꼬리)
- 무엇을 측정/검증하나: 복사플럭스·구름량·τ의 **분포 전체**(형상·꼬리) 일치. 평균 지표가 못 잡는 분포 편향(예: 두꺼운 구름 꼬리, 저조도 첨두) 포착.
- 정의·수식: 재정의 없이 §01(QQ-plot)·§03(PDF/CDF·KS·Perkins skill score) 교차링크. τ·CRE·SW↓ 분포에 적용.
- 적용 도메인/자료형: [격자]/[시계열]/[히스토그램]. 시간정렬 불필요(분포 비교).
- 입력·전제: 동일 기간·모집단. 자기상관 강한 시계열은 유효표본 보정(§03).
- 해석 기준(advisory): §01/§03 원칙 준용 — 꼬리는 표본 적어 불안정. "too few, too bright"는 τ QQ 상단에서 노출. 임계 단정 금지.
- 한계·주의(§G 연결): 분포만 보고 동시성(상관)은 못 봄. KS는 자기상관 시 과민(§03 캐비앗).
- 출처: §01_error_statistics.md(QQ), §03_categorical_event_extremes.md(PDF/CDF·KS·Perkins).

---

### ★ Taylor · Target 종합 요약 (다지점·다변수 — 구름·복사 적용)
- 무엇을 측정/검증하나: 여러 변수(SW↓·OLR·CRE·구름량)·여러 모델·여러 영역을 상관·표준편차·CRMSD(Taylor)와 bias·CRMSD(Target)로 한눈에 요약.
- 정의·수식: 재정의 없이 §01(Taylor·Target diagram)·`figures/16` 교차링크. 구름·복사 변수·영역을 점으로 배치.
- 적용 도메인/자료형: [격자]/[시계열] 다변수·다모델 종합.
- 입력·전제: 정규화 σ, 정렬 쌍. Taylor는 bias 미표현 → Target·bias표 병행(§01).
- 해석 기준(advisory): 관측점 근접=우수(상대). §G 원칙: 절대 등급화 금지, 관측 불확실성 대비.
- 한계·주의(§G 연결): §01 캐비앗 상속(Taylor bias 미표현). 변수 단위·정규화 정합.
- 출처: §01_error_statistics.md(Taylor·Target 정의 및 출처: Taylor 2001; Jolliff et al. 2009); `figures/16`.

---

## 출처 (References)

### 표준 참고문헌 / 데이터셋 문서 (실제 존재)
- Loeb, N. G. et al. (2018) "Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced and Filled (EBAF) Top-of-Atmosphere (TOA) Edition-4.0 Data Product," *Journal of Climate*, 31(2), 895–918. (doi:10.1175/JCLI-D-17-0208.1)
- Kato, S. et al. (2018) "Surface Irradiances of Edition 4.0 Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced and Filled (EBAF) Data Product," *Journal of Climate*, 31(11), 4501–4527. (doi:10.1175/JCLI-D-17-0523.1)
- Rossow, W. B. & Schiffer, R. A. (1999) "Advances in understanding clouds from ISCCP," *Bulletin of the American Meteorological Society*, 80(11), 2261–2287.
- Bodas-Salcedo, A. et al. (2011) "COSP: Satellite simulation software for model assessment," *Bulletin of the American Meteorological Society*, 92(8), 1023–1043. (doi:10.1175/2011BAMS2856.1)
- Swales, D. J., Pincus, R. & Bodas-Salcedo, A. (2018) "The Cloud Feedback Model Intercomparison Project Observational Simulator Package: Version 2 (COSP2)," *Geoscientific Model Development*, 11, 77–81. (doi:10.5194/gmd-11-77-2018)
- Chepfer, H. et al. (2010) "The GCM-Oriented CALIPSO Cloud Product (CALIPSO-GOCCP)," *Journal of Geophysical Research: Atmospheres*, 115, D00H16. (doi:10.1029/2009JD012251)
- Marchand, R., Ackerman, T., Smyth, M. & Rossow, W. B. (2010) "A review of cloud top height and optical depth histograms from MISR, ISCCP, and MODIS," *Journal of Geophysical Research: Atmospheres*, 115, D16206. (doi:10.1029/2009JD013422)
- Driemel, A. et al. (2018) "Baseline Surface Radiation Network (BSRN): structure and data description (1992–2017)," *Earth System Science Data*, 10, 1491–1501. (doi:10.5194/essd-10-1491-2018)
- Klein, S. A. et al. (2013) "Are climate model simulations of clouds improving? An evaluation using the ISCCP simulator," *Journal of Geophysical Research: Atmospheres*, 118, 1329–1342. (doi:10.1002/jgrd.50141)
- Webb, M., Senior, C., Bony, S. & Morcrette, J.-J. (2001) "Combining ERBE and ISCCP data to assess clouds in the Hadley Centre, ECMWF and LMD atmospheric climate models," *Climate Dynamics*, 17, 905–922.
- Klein, S. A. & Jakob, C. (1999) "Validation and sensitivities of frontal clouds simulated by the ECMWF model," *Monthly Weather Review*, 127, 2514–2531.
- Jakob, C. & Tselioudis, G. (2003) "Objective identification of cloud regimes in the Tropical Western Pacific," *Geophysical Research Letters*, 30(21), 2082. (doi:10.1029/2003GL018367)
- Bodas-Salcedo, A. et al. (2008) "Evaluating cloud systems in the Met Office global forecast model using simulated CloudSat radar reflectivities," *Journal of Geophysical Research*, 113, D00A13. (doi:10.1029/2007JD009620)
- Bodas-Salcedo, A. et al. (2014) "Origins of the solar radiation biases over the Southern Ocean in CFMIP2 models," *Journal of Climate*, 27(1), 41–56. (doi:10.1175/JCLI-D-13-00169.1)
- Nam, C., Bony, S., Dufresne, J.-L. & Chepfer, H. (2012) "The 'too few, too bright' tropical low-cloud problem in CMIP5 models," *Geophysical Research Letters*, 39, L21801. (doi:10.1029/2012GL053421)
- Taylor, K. E., Crucifix, M., Braconnot, P. et al. (2007) "Estimating shortwave radiative forcing and response in climate models," *Journal of Climate*, 20(11), 2530–2543. (doi:10.1175/JCLI4143.1) (APRP)
- Wild, M. et al. (2013) "The global energy balance from a surface perspective," *Climate Dynamics*, 40, 3107–3134. (doi:10.1007/s00382-012-1569-8)
- Stephens, G. L. et al. (2012) "An update on Earth's energy balance in light of the latest global observations," *Nature Geoscience*, 5, 691–696. (doi:10.1038/ngeo1580)
- von Schuckmann, K. et al. (2020) "Heat stored in the Earth system: where does the energy go?," *Earth System Science Data*, 12, 2013–2041. (doi:10.5194/essd-12-2013-2020)
- Yang, G.-Y. & Slingo, J. (2001) "The diurnal cycle in the tropics," *Monthly Weather Review*, 129, 784–801.

### 교차링크 (공통 방법 — 본 카드에서 재정의하지 않음)
- `01_error_statistics.md` — RMSE·MAE·bias·상관·R²·Taylor·Target·bootstrap.
- `02_spatial_pattern_verification.md` — SSIM·FSS·패턴상관/ACC(구름장 적용).
- `03_categorical_event_extremes.md` — PDF/CDF·KS·Perkins skill score·QQ·극값.
- `04_conservation_energy_flux.md` — 에너지수지·수지닫힘(지표·전지구).
- `06_timeseries_signal.md` — 일변동 조화적합·위상.
- `12_satellite_remote_sensing.md`·`15_preprocessing_regridding_colocation.md` — 매치업·대표성오차·재격자.
- `figures/16`(그림 카탈로그) — Taylor/Target·QQ·τ–p 히스토그램·CFAD·연직 CF 단면 등 그림 유형.

### 확인요 (웹으로 1차 확인 못 했거나 재확인 필요 — 확정 인용 금지)
- Cesana, G. & Chepfer, H. (2013) CMIP5 구름 연직구조(CALIPSO-GOCCP) — 제목·권·페이지 재확인.
- Kay, J. E. et al. (2012) CESM CALIPSO 시뮬레이터 평가 — 서지 재확인.
- Pincus, R. et al. (2012) MODIS 시뮬레이터 구름 비교 — 서지 재확인.
- Zelinka, M. D. et al. (2012) cloud radiative kernels — 서지 재확인.
- Tselioudis, G. et al. (2013) global weather states — 서지 재확인.
- Williams, K. D. & Webb, M. J. (2009) cloud regimes 모델평가, *Climate Dynamics* — 재확인.
- Bony, S. et al. (2004) 구름-복사 관계 진단, *Climate Dynamics* — 재확인.
- Cesana, G. et al. (2015) CALIPSO cloud phase; Kay, J. E. et al. (2016) Southern Ocean SW/phase — 서지 재확인.
- Elsaesser, G. S. et al. (2017) MAC-LWP; Duncan, D. I. & Eriksson, P. (2018) IWP 불확실성; Waliser, D. E. et al. (2009) cloud ice — 재확인.
- Schaaf, C. B. et al. (2002) MODIS BRDF/albedo, *Remote Sensing of Environment* — 재확인.
- Ohmura, A. et al. (1998) BSRN 설립, *BAMS*; Stokes, G. M. & Schwartz, S. E. (1994) ARM, *BAMS* — 재확인.
- Allan, R. P. (2011) CRE 개념, *Meteorological Applications*; Sohn et al. clear-sky 정의 차이 — 재확인.
- Wild, M. (2020) global energy balance 종설 — 저널·연도 재확인.

> 주의(§00 §F·§G 준용): CERES-EBAF·ISCCP·GOCCP·재분석은 **기준(reference)이지 참값이 아니다.** 위 논문의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인하며, DOI를 명시한 항목은 이 세션에서 확인된 것이고 "(확인요)"는 확정 인용 금지. 해석 임계(bias·SI·CF·CRE 등)는 모두 advisory이며 영역·해상도·계절·기준자료에 따라 달라지므로 자동 good/bad 단정을 금한다.
