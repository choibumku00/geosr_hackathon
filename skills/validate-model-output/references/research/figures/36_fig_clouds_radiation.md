# 검증 시각화 카탈로그 — [구름·복사 도메인편] (Verification Figures: Clouds & Radiation)

이 문서는 지구시스템/기후·대기 모델의 **구름(cloud)·복사(radiation)** 산출물을 위성(CERES·ISCCP·MODIS·MISR·CALIPSO·CloudSat)·지상 관측망(BSRN·ARM)·재분석(ERA5)과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 구름·복사 도메인편이다. 메서드(수치지표) 카드는 **대응 메서드카탈로그: [`28_domain_clouds_radiation.md`](../28_domain_clouds_radiation.md)**에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **공통/횡단 그림과의 분담**: Taylor·Target·QQ·reliability·rank histogram·PDF/CDF·성능 다이어그램 등 **도메인 무관 요약그림은 [공통편 `figures/16`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않고 **교차링크만** 한다. 이 파일은 **구름·복사 고유 그림**(ISCCP τ–p 결합히스토그램, CFAD, SR–height 히스토그램, CRE 지도, 구름량 위도-고도 연직단면, 일변동 조화곡선 등)과 **공통 그림의 구름·복사식 변형**(복사플럭스 bias 지도, BSRN/ARM 점–격자 산점 등)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "짝지표 & 교차링크"에서 가리킨다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석/L3·L4 위성) · [시계열]=지상관측소(BSRN·ARM) 점 관측 · [트랙]=위성 연직/궤도 자료(CloudSat·CALIPSO along-track) · [히스토그램]=τ–p 등 결합분포 · [연직]=cloud fraction 연직프로파일.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats), 그리고 [`28` 도메인 §G 연결]):
> 1. **기준자료 ≠ 참값.** CERES-EBAF(TOA/Surface)·ISCCP·ERA5 복사는 모두 reference이지 truth가 아니다 — 특히 **CERES-EBAF TOA는 지구에너지불균형에 맞춘 balancing 산물**, **CERES-EBAF Surface는 위성 TOA+재분석으로 복사전달 계산한 유도(derived) 산물**이다. 축·범례·캡션에 "모델 − 기준(reference)"으로 쓰고 "오차"로 단정하지 않는다.
> 2. **사과-대-사과엔 COSP가 사실상 필수.** 모델 구름을 위성과 직접 비교하면 감지특성(τ 임계·중첩·감쇠·태양각·야간 결측) 불일치가 물리오차와 뒤섞인다. τ–p 히스토그램·CF 프로파일·CFAD·SR 히스토그램 등 **구름 진단 그림은 COSP 시뮬레이터 산물**로 그려야 결론 신뢰도가 있다.
> 3. **clear-sky 정의 일치가 결정적.** CERES clear-sky=구름 없는 장면 **샘플링**(Method I) vs 모델 clear-sky=구름 제거 **재계산**(Method II) → CRE·clear-sky 비교의 최대 함정. 그림 캡션에 정의를 명시한다.
> 4. **해석 임계는 advisory.** bias·RMSE·useful-scale·SSIM 임계 등은 **영역·계절·해상도·기준자료 의존**이며 CERES-EBAF 자체 불확실성(전지구 순 ~수 W/m²)을 하한으로 본다. 그림에 "good/bad"를 단정 표기하지 말고 영역·계절 의존 경고를 캡션에 둔다.
> 5. **단일 그림 금지.** 그림 1장으로 결론내지 말고 최소 **(복사 bias)+(구름장/연직구조)+(구름–복사 관계)** 를 함께 본다. 복사가 맞아도 구름이 틀린 **보상오차(compensating error)** 는 관계·요인분해 그림으로만 노출된다.
> 6. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문의 도판을 그대로 재현하지 않는다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **TOA 복사플럭스 bias 지도 (RSUT·OLR·net)** — 복사 검증의 1차 대표 지도(basemap)
2. ★ **지표 하향 SW↓/LW↓ bias 지도 + 위도대 평균** — 지표 복사 공간 계통오차
3. ★ **복사플럭스 검증 산점도 (model vs CERES/BSRN, +bias/RMSE box)** — 정확도+편향 1차
4. ★ **BSRN/ARM 관측소 산점도 + 위치 지도(마커·ID)** — 지상 절대검증(점–격자)
5. ★ **구름복사효과 CRE 지도 (SW·LW·net; TOA·surface)** — all-sky − clear-sky 공간분포
6. ★ **전운량 bias 지도 + 관측 스프레드 (ISCCP/MODIS/CALIPSO)** — 구름량 계통오차
7. ★ **구름분율 위도-고도 연직단면 (zonal-mean CF)** — 연직 배치 오차
8. ★ **ISCCP τ–p 결합히스토그램 비교 (joint pc–tau)** — 구름유형 구성 진단(대표)
9. ★ **구름레짐/기상상태(weather states) RFO·CRE 막대·지도** — 유형별 빈도·복사
10. ★ **CFAD: CloudSat 반사도 고도별 빈도 등고 (dBZ×height)** — 두꺼운 구름·강수 연직
11. **CALIPSO SR–height 히스토그램 (GOCCP)** — 얇은 구름 연직구조
12. ★ **운정 CTH/CTT/CTP 검증 (산점/2D 히스토그램)** — 구름 연직 배치·LW CRE
13. ★ **구름 광학두께 τ 분포·QQ ("too few, too bright")** — SW CRE 근원
14. ★ **일변동 조화곡선 + 진폭·위상 다이어그램 (harmonic dial)** — 복사·구름 일주기
15. ★ **계절순환·월평균 기후 지도 (DJF/JJA bias, 계절-위도 단면)** — 계절 bias
16. ★ **구름–복사 관계 그림 (SW CRE vs 저층운량 등, 보상오차)** — 물리 정합

---

### ★ TOA 복사플럭스 bias 지도 (대기상단 복사 편차 지도 / TOA radiative-flux bias map: RSUT / OLR / net)
- **무엇을 보여주나**: 대기상단(TOA)에서 모델이 산출한 반사 단파(reflected SW, RSUT)·외향 장파(OLR)·순플럭스(net)를 CERES-EBAF TOA와 격자별로 뺀 **공간 bias 지도(model−CERES)**. 복사 검증의 최상위 1차 그림으로, 계통오차가 "어디서"(열대수렴대·폭풍대·아열대 Sc·사막·해빙역) 생기는지 본다.
- **읽는 법**: **지도** — 색=bias(발산맵, 0=흰색, 대칭 범위). 빨강=모델 과대, 파랑=과소. *좋은 패턴*: 전역 옅은 잡음, 반구 대칭. *나쁜 패턴*: 폭풍대·남극해 RSUT 음(구름·알베도 과소), 열대 대류역 OLR 양(권운 과소→상단 너무 따뜻), 해안·재격자선 줄무늬(artifact). **위도대 평균 곡선**(zonal-mean bias)을 옆에 병치해 위도구조 요약.
- **언제 쓰나**: [격자] 모델 vs [격자] CERES-EBAF TOA(1°, 월/일). all-sky·clear-sky를 각각 지도화(둘의 차가 CRE ⑤). 복사 계통오차 공간진단의 출발.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·패턴상관** → [`28` TOA 복사플럭스 bias 카드], [`01` bias/RMSE], [`02` 공간패턴]. 요약은 [`figures/16` Bias/difference map · Taylor(⑯)]. all-sky−clear-sky는 ⑤ CRE.
- **만드는 법**: `xarray`+`xesmf`(보존형 재격자, 공통 격자)→`(model−ceres).plot` + **`cartopy`(`ccrs.PlateCarree`)로 해안선/육지+위경도 라벨 필수** (→ [`plotting_maps.md` `add_basemap()`]). 발산맵 `cmocean.cm.balance`/`RdBu_r`+`TwoSlopeNorm(vcenter=0)`. 위도대 평균은 `xarray.weighted(cos φ)`. 전지구·반구 평균 텍스트 병기. ESMValTool/E3SM Diags에 CERES 복사 진단 recipe 존재.
- **함정·주의(§G 연결)**: **CERES-EBAF TOA는 balancing 산물** → 절대 순플럭스 비교는 EEI(⑥)로, 여기선 **패턴** 위주. 입사 단파 정의(연평균 vs 순간)·야간 마스크·달력 불일치가 인위적 SW bias. **지도엔 해안선+위경도 라벨 필수**(없으면 위치판독 불가). 재격자 순서/방식이 차이장을 바꿈(모델·기준 동일 보간).
- **출처**: Loeb et al. (2018) "Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced and Filled (EBAF) Top-of-Atmosphere (TOA) Edition-4.0," *Journal of Climate* 31(2):895–918, doi:10.1175/JCLI-D-17-0208.1; Wild et al. (2013, *Climate Dynamics*, global energy balance).

---

### ★ 지표 하향 SW↓ / LW↓ bias 지도 + 위도대 평균 (지표 하향복사 편차 지도 / Surface downwelling SW↓·LW↓ bias map)
- **무엇을 보여주나**: 지표 하향 단파(SW↓, rsds)·하향 장파(LW↓, rlds)를 CERES-EBAF Surface(또는 SYN1deg)와 뺀 **공간 bias 지도**. SW↓는 구름 반사·에어로졸·표면 결합, LW↓는 수증기·기온·저층운 결합을 진단. "too much sunshine"(구름 과소→SW↓ 과대) 패턴 노출.
- **읽는 법**: **지도** — 색=bias(발산맵, 0=흰색). *나쁜 패턴*: 남극해·열대 육상 SW↓ 양(구름 과소), 극지·고산 LW↓ 음(clear-sky 수증기 continuum 과소). 위도대 평균 곡선으로 위도구조 요약. all-sky/clear-sky 지도를 나란히(구름효과 격리).
- **언제 쓰나**: [격자] CERES-EBAF Surface vs 모델. (점 절대검증은 ④ BSRN.) 지표 복사강제력 공간 계통진단.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·상관** → [`28` 지표 SW↓/LW↓ 카드], [`01`], [`02`]. clear-sky 격리는 [`28` 청천복사 카드]. all-sky−clear-sky는 ⑤ CRE(surface). 점 검증은 ④.
- **만드는 법**: `xarray`+`xesmf`→bias→**`cartopy` 해안선/육지+위경도 라벨 필수**(`add_basemap()`), `cmocean.cm.balance`+`TwoSlopeNorm(0)`. 위도대 평균 `weighted(cosφ)`.
- **함정·주의(§G 연결)**: **CERES-EBAF Surface는 유도(derived) 산물**(위성 TOA+재분석 복사전달) → 독립 진값 아님, BSRN(④)과 교차. CERES 제품 간 bias 차(SYN1deg vs EBAF) 감안. **지도 해안선+위경도 라벨 필수.** SW↓는 야간·저조도에서 무의미(주간 마스크). 부분운 순간변동 큼 → 월평균 권장.
- **출처**: Kato et al. (2018) "Surface Irradiances of Edition 4.0 CERES-EBAF Data Product," *Journal of Climate* 31(11):4501–4527, doi:10.1175/JCLI-D-17-0523.1; Wild et al. (2015, *Climate Dynamics*, surface SW).

---

### ★ 복사플럭스 검증 산점도 (복사플럭스 산점도 / Radiative-flux validation scatter, model vs CERES/BSRN)
- **무엇을 보여주나**: 매치업된 (기준 플럭스, 모델 플럭스) 쌍을 산점하고 1:1선·회귀선·핵심 스칼라(bias·RMSE·R·N)를 얹은 **정확도+편향 1차 그림**. SW↓·LW↓·RSUT·OLR·CRE 어느 플럭스에도 적용. 격자-격자 집계 또는 다지점.
- **읽는 법**: x=기준(CERES/BSRN), y=모델. **1:1선**(점선) 기준, **OLS 회귀선**(실선). 점운이 1:1 위/아래로 쏠리면 과대/과소(bias), 부채꼴로 퍼지면 랜덤오차 큼, 회귀 기울기<1이면 고값 과소·저값 과대(조건부 편향). 표본 크면 **밀도/hexbin**(로그 카운트)으로. 텍스트 box에 bias·RMSE·R·N.
- **언제 쓰나**: [격자]/[시계열] 어디서나. 모델·기준 1쌍 또는 다지점 집계. 정확도+편향 동시 1차 점검. (다변수/다지점 요약은 ⑯ Taylor로 승급.)
- **짝지표 & 교차링크**: **bias·RMSE·R·OLS slope** → [`28` 각 플럭스 카드], [`01`]. 공통 산점·밀도산점 상세는 [`figures/16` 산점도·회귀·밀도산점]. 분포는 ⑬ QQ. 지도형 공간분포는 ①/②.
- **만드는 법**: `matplotlib` `ax.scatter`(또는 N 크면 `ax.hexbin(bins='log', mincnt=1)`) + `numpy.polyfit`/`scipy.stats.linregress`. 축 동일 범위·`set_aspect('equal')`·1:1선 `ax.axline((0,0),slope=1)`. **이건 값-값 축이므로 지도 아님**(basemap 넣지 말 것).
- **함정·주의(§G 연결)**: 기준자료도 오차 → OLS regression dilution(기울기<1 편향), robust/orthogonal 병행 고려. 점 BSRN 대표성오차가 산포에 포함(모델 탓 단정 금지). SW는 주간·고태양각 필터. 산점 1장으로 결론 금지 → 공간(①②)+분포(⑬) 3축.
- **출처**: [`figures/16`](./16_fig_common.md)(산점·회귀·밀도산점 표준 시각화; Wilks; Jolliffe & Stephenson); Loeb et al. (2018, *J. Climate*, CERES-EBAF TOA Ed4); Kato et al. (2018, *J. Climate*, CERES-EBAF Surface Ed4).

---

### ★ BSRN/ARM 관측소 산점도 + 위치 지도 (지상관측망 매치업 그림 / BSRN·ARM colocation scatter + station map)
- **무엇을 보여주나**: 고정밀 지상 복사관측(BSRN·ARM 4성분 SW↓·SW↑·LW↓·LW↑)과 모델 격자값을 시공간 정합한 산점도 + **관측소 위치 지도(해안선 위 마커·ID)**. 위성이 못 주는 지표 복사의 절대검증 기준.
- **읽는 법**: **산점** — 지점별 색/마커, 1:1선·bias/RMSE box(①양식). **위치 지도** — 각 관측소를 해안선 지도 위 마커로, 옆에 관측소 ID 라벨; 각 산점/시계열 패널 구석에 인셋 로케이터맵 + 제목에 위경도(예 `Payerne (6.94°E, 46.82°N)`). *나쁜 패턴*: 특정 사이트만 큰 bias(국지 에어로졸/지형), 북반구 육상 편중.
- **언제 쓰나**: [시계열] BSRN(>70소, 4성분)·ARM(SGP 등) vs 모델·CERES-Surface 격자. 지표 4성분 절대검증·대표성오차 진단.
- **짝지표 & 교차링크**: **점–격자 대표성오차** → [`28` BSRN/ARM 매치업 카드], [`12`/`15` 매치업·대표성오차]. 성분별 bias·수지닫힘은 [`28` 지표 복사수지 Rn 카드]. 산점 공통양식은 [`figures/16`].
- **만드는 법**: 산점=`matplotlib`(위 ③). **위치 지도=`cartopy`로 해안선/육지+위경도 라벨 필수**(`add_basemap()` → [`plotting_maps.md` §C 정점/관측소]), 마커+ `ax.annotate` ID, 인셋 `ax.inset_axes(...projection=ccrs.PlateCarree())`. QC 플래그(WRMC) 필터, UTC↔지방시 정합, 태양각 계산.
- **함정·주의(§G 연결)**: **관측소 지도엔 해안선+마커+ID 필수**(위치 모르면 무의미). 점 대표성오차(부분운·국지 에어로졸) → 순간보다 일/월평균 매치. BSRN 지리 편중(북반구 육상)으로 전지구 대표성 한계. 점 관측을 격자 진값처럼 쓰지 말 것.
- **출처**: Driemel et al. (2018) "Baseline Surface Radiation Network (BSRN): structure and data description (1992–2017)," *Earth System Science Data* 10:1491–1501, doi:10.5194/essd-10-1491-2018; Ohmura et al. (1998, *BAMS*, BSRN 설립); Stokes & Schwartz (1994, *BAMS*, ARM — 확인요).

---

### ★ 구름복사효과 CRE 지도 (구름복사효과 공간지도 / Cloud radiative effect map: SW / LW / net; TOA·surface)
- **무엇을 보여주나**: 구름이 복사수지에 미치는 순효과(=all-sky − clear-sky 플럭스)를 모델·CERES 각각 지도화하고 그 **bias 지도(model−CERES)**. SW CRE(냉각, 음)·LW CRE(가열, 양)·net CRE를 TOA·surface·atmosphere(=TOA−surface)로. 구름 검증과 복사 검증을 잇는 핵심 통합그림.
- **읽는 법**: **지도** — SW CRE 지도는 음(냉각) 강한 곳=아열대 Sc·폭풍대(반사 강). bias 지도(발산맵)에서 남극해 SW CRE 양편향(=구름 너무 적거나 반사 약함)이 흔한 결함. LW CRE는 열대 대류·권운역 양(가열). *나쁜 패턴*: 폭풍대 SW CRE 과소, 열대 LW CRE 과소(권운 부족).
- **언제 쓰나**: [격자] 모델 vs CERES-EBAF(all-sky·clear-sky 동시 제공). TOA·surface 모두. 복사–구름 통합진단.
- **짝지표 & 교차링크**: 격자별 **CRE_SW/LW/net bias·RMSE** → [`28` CRE 카드], [`01`], [`02`]. 요인분해는 [`28` APRP 카드]. 구름량 관계는 ⑯. 요약은 [`figures/16` Taylor/bias map].
- **만드는 법**: `xarray`로 CRE=all-sky−clear-sky 계산 → bias → **`cartopy` 해안선/육지+위경도 라벨 필수**(`add_basemap()`), `cmocean.cm.balance`+`TwoSlopeNorm(0)`. SW CRE는 **주간·계절 마스크**(태양광 있는 곳만). ESMValTool에 CRE(SW/LW CRE) 진단 recipe.
- **함정·주의(§G 연결)**: **clear-sky 정의 불일치(CERES 샘플링 Method I vs 모델 재계산 Method II)가 CRE bias의 최대 함정** → 정의를 캡션에 명시(가능하면 정합). **지도 해안선+위경도 라벨 필수.** SW CRE 극야·야간 무의미. LW CRE 부호규약 통일.
- **출처**: Loeb et al. (2018, *J. Climate*, CERES-EBAF TOA Ed4, doi:10.1175/JCLI-D-17-0208.1); Kato et al. (2018, *J. Climate*, CERES-EBAF Surface, doi:10.1175/JCLI-D-17-0523.1); Allan (2011, *Meteorological Applications*, CRE 개념 — 확인요).

---

### ★ 전운량 bias 지도 + 관측 스프레드 (전운량 편차 지도 / Total cloud fraction bias map with obs spread)
- **무엇을 보여주나**: 격자별 전운량(clt, 0~1 또는 %)의 **model−obs bias 지도**를, **여러 관측(ISCCP·MODIS·CALIPSO-GOCCP·CERES) 스프레드와 함께**. 구름 검증의 1차 지표이자 복사 bias의 주요 원인 진단. "관측이 하나가 아님"을 명시적으로 보여줌.
- **읽는 법**: **지도** — 색=bias(발산맵). *나쁜 패턴*: 아열대 동안류·남극해 저층운 과소(파랑 띠→SW CRE 결함), 열대 권운 과대/과소. **관측 스프레드**: CALIPSO가 ISCCP·MODIS보다 총운량 높음(얇은 구름 감지) → bias 부호가 어떤 관측을 기준으로 하냐에 좌우 → 관측 min–max 밴드/여러 기준 지도 병치.
- **언제 쓰나**: [격자] 모델(clt, **COSP 산물 권장**) vs ISCCP/MODIS/GOCCP/CERES. 구름량 계통오차 공간진단.
- **짝지표 & 교차링크**: 격자별 **bias·패턴상관·RMSE** → [`28` 전운량 카드], [`02`], [`01`]. 연직 배치는 ⑦, 유형 구성은 ⑧, 공간구조(SSIM/FSS)는 [`28` 구름 공간패턴 카드]→[`figures/16`].
- **만드는 법**: `xarray`+`xesmf`→bias→**`cartopy` 해안선/육지+위경도 라벨 필수**(`add_basemap()`), `cmocean.cm.balance`. 관측 스프레드는 여러 위성 재격자 후 min–max·std 지도. **COSP-lidar/ISCCP 시뮬레이터**로 감지특성 정합.
- **함정·주의(§G 연결)**: **COSP 없이 모델 총운량을 위성과 직접 비교하면 정의 불일치(τ 임계·중첩·감쇠) 편향.** 중첩가정(random/maximum-random)·연직해상도 민감. 정지 vs 극궤도 샘플링 시각 차(일변동 aliasing). **지도 해안선+위경도 라벨 필수.**
- **출처**: Rossow & Schiffer (1999) "Advances in understanding clouds from ISCCP," *BAMS* 80(11):2261–2287; Chepfer et al. (2010, *JGR*, CALIPSO-GOCCP, doi:10.1029/2009JD012251); Pincus et al. (2012, *J. Climate*, MODIS 시뮬레이터 — 확인요).

---

### ★ 구름분율 위도-고도 연직단면 (구름분율 연직 단면 / Cloud fraction latitude–height zonal-mean cross-section)
- **무엇을 보여주나**: 대상평균(zonal-mean) 구름분율 CF(위도, 고도/기압)를 **위도–고도 채움등고(색)** 로 모델·관측(CALIPSO-GOCCP·CloudSat-CALIPSO 결합) 나란히, 그리고 차이 패널. 전운량이 맞아도 **연직 배치**(저층운·중층운·권운 고도)가 틀린 것을 노출.
- **읽는 법**: x=위도, y=고도(또는 기압, 위쪽이 상층), 색=CF. *좋은 패턴*: 열대 상층 권운·중위도 폭풍대 경사·아열대·극지 저층운 최대가 관측과 위치·강도 일치. *나쁜 패턴*: 저층운 과소(경계층 CF 부족), 권운 고도 과대/과소, 중층 "빈 구멍". 차이 패널(발산맵)로 층별 bias.
- **언제 쓰나**: [연직]/[트랙] CALIPSO/CloudSat 연직 vs 모델 연직 CF(COSP lidar/radar 산물)를 [격자]로 zonal-mean화. 연직 구조 진단.
- **짝지표 & 교차링크**: **층별 CF bias·연직 상관** → [`28` 연직 구름분율 프로파일 · 저/중/고 구름량 카드], [`02`]. 반사도 연직은 ⑩ CFAD, 얇은 구름은 ⑪ SR. 단일 프로파일은 지점 overlay(⑪형).
- **만드는 법**: `xarray`로 `.mean('lon')` → `xr.DataArray.plot.contourf(x='lat', y='height')`(모델·관측·차 3패널, 동일 levels). **축이 위도–고도라 지도(basemap) 아님**(가로만 위도, 세로는 고도). COSP CALIPSO/CloudSat 시뮬레이터 필수. ESMValTool에 CALIPSO/CloudSat CF 프로파일 진단.
- **함정·주의(§G 연결)**: **COSP CALIPSO/CloudSat 시뮬레이터 필수** — 능동센서 감쇠(두꺼운 구름 아래 신호 소실)·최소감지 반사도를 모델에도 적용. lidar 두꺼운 저층운 감쇠 vs radar 얇은권운 놓침 → 결합 산물 권장. SR/reflectivity 임계가 CF를 최대 ~0.2 바꿈(GOCCP 민감도). 색 levels 모델·관측 동일.
- **출처**: Chepfer et al. (2010) "The GCM-Oriented CALIPSO Cloud Product (CALIPSO-GOCCP)," *JGR: Atmospheres* 115:D00H16, doi:10.1029/2009JD012251; Cesana & Chepfer (2013, *JGR*, CMIP5 구름 연직구조); Kay et al. (2012, *J. Climate*, CALIPSO 시뮬레이터 평가 — 확인요).

---

### ★ ISCCP τ–p 결합히스토그램 비교 (광학두께–운정기압 결합히스토그램 / Joint cloud optical depth – cloud top pressure histogram)
- **무엇을 보여주나**: 광학두께(τ)와 운정기압(p_c)의 **2차원 결합분포**(ISCCP 표준: τ 7구간 × p_c 7구간 = 49상자, 구간 비선형)를 모델–ISCCP 간 비교. 단일 운량·τ가 못 보는 "구름 유형 구성(저층 두꺼운 Sc, 고층 얇은 권운, 깊은 대류)"을 한 장으로 진단하는 **구름 검증 대표 고급 그림**.
- **읽는 법**: x=τ(왼→오 얇음→두꺼움), y=p_c(위→아래 고층→저층, 관례상 상단이 저기압=고층), 색=CF(%). 모델·관측·차(발산맵) 3패널. *읽기*: 좌상=얇은 권운, 우상=깊은 대류, 우하=두꺼운 저층 Sc. *나쁜 패턴*: 우측(두꺼운) 상자 과다="too bright", 저층 두꺼운 상자 과소=SW 냉각 부족. 유형별 합(저/중/고 × 얇/두꺼움) 요약.
- **언제 쓰나**: [히스토그램] 모델(**COSP-ISCCP 시뮬레이터 필수 산출**) vs ISCCP D/H(pc–tau) 결합히스토그램. 구름유형 분포·복사 근원 진단.
- **짝지표 & 교차링크**: **상자별 bias·히스토그램 RMS 차** → [`28` ISCCP τ–p 히스토그램 카드]. 군집화는 ⑨ 구름레짐, τ축 단독은 ⑬, p_c축은 ⑫ 운정. COSP 전제는 [`28` COSP 카드].
- **만드는 법**: COSP-ISCCP 시뮬레이터 산출 τ–p 히스토그램(모델)·ISCCP-sim 관측(CFMIP-obs) → `matplotlib.pcolormesh`(비선형 구간은 index축+구간 라벨) 3패널. **비선형 구간 → 상자 면적가중 주의.** ESMValTool `clouds`/CFMIP 진단, E3SM Diags에 CTP-τ(ISCCP/MODIS) joint histogram 진단.
- **함정·주의(§G 연결)**: **COSP-ISCCP 없이는 성립 불가**(τ, p_c를 ISCCP 감지·중첩 규약대로 재현). passive 다층·부분운 편향이 상자 배치에 스밈. τ–p 구간 비선형(면적가중). **야간 결측→일변동 왜곡**(τ는 주간·일정 태양각만). 색스케일 모델·관측 동일.
- **출처**: Klein & Jakob (1999) "Validation and sensitivities of frontal clouds simulated by the ECMWF model," *Monthly Weather Review* 127:2514–2531(τ–p 진단 도입); Webb et al. (2001, *Climate Dynamics* 17:905–922, ERBE+ISCCP 모델평가); Klein et al. (2013) "Are climate model simulations of clouds improving? An evaluation using the ISCCP simulator," *JGR: Atmospheres* 118:1329–1342, doi:10.1002/jgrd.50141.

---

### ★ 구름레짐 / 기상상태 RFO·CRE 그림 (구름레짐 진단 / Cloud-regime (weather-state) RFO & CRE plot)
- **무엇을 보여주나**: τ–p 결합히스토그램을 k-means 군집화한 **구름레짐(weather states, WS)**(층적운·깊은대류·얇은권운 등)별 **발생빈도(RFO)** 와 **레짐별 CRE**를, (a) 레짐 centroid 히스토그램 판, (b) RFO 지리분포 지도, (c) 관측 대비 RFO·CRE 막대로 비교. 구름을 "역학적으로 의미있는 유형"으로 묶어 진단.
- **읽는 법**: (a) 각 centroid=τ–p 히스토그램 소판(⑧양식). (b) 지도=특정 레짐 RFO(%). (c) 막대=레짐별 RFO·CRE(모델 vs 관측). *읽기*: "구름유형 빈도 오차(RFO)" vs "유형 내 속성 오차(레짐 내 CRE)"를 분리. *나쁜 패턴*: 층적운 레짐 RFO 과소(남극해·아열대), 깊은대류 레짐 위치 편차.
- **언제 쓰나**: [히스토그램] 모델(COSP-ISCCP) vs ISCCP 구름레짐 산물. 영역/전지구. 유형 기반 복사·빈도 진단.
- **짝지표 & 교차링크**: **레짐 RFO·레짐별 CRE bias** → [`28` 구름레짐/기상상태 카드], ⑧(τ–p 원천)·⑤(CRE). RFO 지도는 [`02`]. centroid 군집은 §D EOF/군집 성격.
- **만드는 법**: 관측 τ–p 히스토그램을 `scikit-learn` `KMeans`로 군집(ISCCP WS centroid) → 모델 COSP 히스토그램을 동일 centroid에 최근접 할당 → RFO·CRE 집계. centroid 소판=`pcolormesh`, **RFO 지리분포 지도는 `cartopy` 해안선/육지+위경도 라벨 필수**(`add_basemap()`), 막대=`ax.bar`.
- **함정·주의(§G 연결)**: 군집 결과가 자료·k·초기화에 의존(관측 centroid를 모델에 적용=공통 기준). passive 히스토그램 편향 상속. 정지·극궤도 샘플링 차. **RFO 지도엔 해안선+위경도 라벨 필수.**
- **출처**: Jakob & Tselioudis (2003) "Objective identification of cloud regimes in the Tropical Western Pacific," *Geophysical Research Letters* 30(21):2082, doi:10.1029/2003GL018367; Tselioudis et al. (2013, *J. Climate*, global weather states — 확인요); Williams & Webb (2009, *Climate Dynamics*, cloud regimes 모델평가 — 확인요).

---

### ★ CFAD: CloudSat 반사도 고도별 빈도 등고 (반사도 고도-빈도 등고도 / Contoured Frequency by Altitude Diagram, radar reflectivity)
- **무엇을 보여주나**: 94 GHz 구름레이더 반사도(dBZ)의 **고도별 발생빈도 분포**(각 고도에서 dBZ 히스토그램을 쌓은 2D 빈도장)를 모델(COSP-CloudSat)–CloudSat CPR 비교. 두꺼운 구름·강수 응결물의 연직구조·크기 진단. 깊은대류는 중층 최대·상하 감소의 특징적 아치.
- **읽는 법**: x=반사도(dBZ), y=고도(km), 색=빈도(고도별 정규화 PDF). *좋은 패턴*: 아치 형상·최빈 dBZ·상단고도가 관측 일치. *나쁜 패턴*: 모델이 **큰 반사도를 너무 자주**(과대 응결물/강수) 또는 얇은권운(약반사) 놓침. 모델·관측·차 3패널.
- **언제 쓰나**: [트랙]/[연직] CloudSat CPR vs 모델(COSP-CloudSat radar 산출). zonal/영역별.
- **짝지표 & 교차링크**: **CFAD 차·고도별 빈도 bias** → [`28` CloudSat CFAD 카드]. 얇은 구름은 ⑪ SR, 연직 CF는 ⑦. COSP 전제 [`28` COSP 카드].
- **만드는 법**: COSP radar 시뮬레이터로 모델 반사도(감쇠·최소감지 −30 dBZ 정합) → 각 고도 `np.histogram`(dBZ) 정규화 → `pcolormesh`(dBZ×height). **축이 반사도–고도라 지도 아님.** 지표 클러터(하부 ~1km) 마스크. 색스케일·bin 모델·관측 동일.
- **함정·주의(§G 연결)**: **COSP-CloudSat 필수**(reflectivity–질량 관계·감쇠·최소감지 정합). reflectivity는 입자크기 6제곱 민감. 지표 클러터 하부 마스크. CloudSat 얇은권운 놓침 → lidar(⑪)와 상보.
- **출처**: Bodas-Salcedo et al. (2008) "Evaluating cloud systems in the Met Office global forecast model using simulated CloudSat radar reflectivities," *Journal of Geophysical Research* 113:D00A13, doi:10.1029/2007JD009620; Stephens et al. (2002, *BAMS*, CloudSat mission); Bodas-Salcedo et al. (2011, *BAMS*, COSP).

---

### CALIPSO SR–height 히스토그램 (라이다 산란비 고도분포 / Lidar scattering-ratio (SR) – height histogram, GOCCP)
- **무엇을 보여주나**: 라이다 산란비(SR=관측 후방산란/분자 후방산란)의 **고도별 분포**(SR–height 히스토그램)를 모델(COSP-lidar)–CALIPSO-GOCCP 비교. 얇은권운·저층운 등 광학적으로 얇은 구름의 연직구조(레이더가 놓치는 영역)를 진단.
- **읽는 법**: x=SR, y=고도, 색=빈도. SR>임계(예: 5)를 구름 판정. *좋은 패턴*: 고도별 SR 최빈·구름/무구름 분리가 관측 일치. *나쁜 패턴*: 저층 SR 분포 편차(저층운 과소), clear(SR≈1) 대 cloud 비율 오차. 지점 overlay(모델·관측 CF(z) 곡선)로도.
- **언제 쓰나**: [연직]/[트랙] CALIPSO-GOCCP vs 모델(COSP lidar 시뮬레이터). 얇은 구름·저층운 연직진단.
- **짝지표 & 교차링크**: **SR 분포·CF(z) bias** → [`28` CALIPSO SR 히스토그램 카드], ⑦(연직 CF)·⑩(반사도, 상보). COSP 전제 [`28` COSP 카드].
- **만드는 법**: COSP lidar 시뮬레이터로 모델 SR → 각 고도 `np.histogram`(SR) → `pcolormesh`(SR×height). **축이 SR–고도라 지도 아님.** 동일 SR 임계·연직해상도. ESMValTool에 GOCCP SR/CF 진단.
- **함정·주의(§G 연결)**: **COSP lidar 필수.** lidar 두꺼운 구름 감쇠(아래 가림). **SR 임계·연직해상도가 CF를 최대 ~0.2 바꿈**(GOCCP 민감도) → advisory. 얕은 적운역 특히 민감. radar(⑩)와 결합 권장.
- **출처**: Chepfer et al. (2010, *JGR*, CALIPSO-GOCCP, doi:10.1029/2009JD012251); Cesana & Chepfer (2013, *JGR*, CMIP5 연직구조 — 확인요); Bodas-Salcedo et al. (2011, *BAMS*, COSP).

---

### ★ 운정 CTH/CTT/CTP 검증 (운정 고도·온도·기압 검증 / Cloud-top height/temperature/pressure verification)
- **무엇을 보여주나**: 운정 고도(CTH)·온도(CTT)·기압(CTP)의 모델–위성 일치를 산점/2D 히스토그램(또는 zonal-mean 지도)으로. 구름 연직 배치·LW CRE(운정온도가 좌우) 진단. CTP는 ⑧ τ–p 히스토그램 p축과 직접 연결.
- **읽는 법**: **산점/2D 히스토그램** — x=위성 CTP(또는 CTH/CTT), y=모델, 1:1선·bias/RMSE box. *나쁜 패턴*: passive(ISCCP/MODIS)는 얇은권운 운정을 낮게(따뜻하게) 편향, active(CALIPSO)는 실제 최상단 → 관측 간 차 큼. 모델이 권운 CTH 과소=LW CRE 약화.
- **언제 쓰나**: [격자]/[트랙] ISCCP·MODIS·MISR·CALIPSO 운정 vs 모델(COSP 산물). MISR은 스테레오 기하 CTH(온도 무관).
- **짝지표 & 교차링크**: **CTH/CTT/CTP bias·RMSE·분포** → [`28` 운정 CTH/CTT/CTP 카드], [`01`]. p_c 결합은 ⑧, LW CRE는 ⑤. 산점 공통양식 [`figures/16`].
- **만드는 법**: `matplotlib` 산점/`hist2d`(모델 vs 위성, ①양식) 또는 zonal-mean이면 위도-값 곡선. **지도형(CTP 공간 bias)일 때만 `cartopy` 해안선/위경도 라벨 필수**(`add_basemap()`); 산점/2D 히스토그램은 지도 아님. COSP로 운정 정의 정합. Marchand et al.(2010) 방식의 CTH-τ 히스토그램 비교.
- **함정·주의(§G 연결)**: **운정 정의가 센서마다 다름**(passive 복사온도→고도 환산, MISR 기하, CALIPSO 광학) → "관측 진값" 단일 아님. 다층운에서 유효운정 vs 실제 최상단 불일치. COSP 없이 직접비교 편향.
- **출처**: Marchand et al. (2010) "A review of cloud top height and optical depth histograms from MISR, ISCCP, and MODIS," *JGR: Atmospheres* 115:D16206, doi:10.1029/2009JD013422; Rossow & Schiffer (1999, *BAMS*, ISCCP).

---

### ★ 구름 광학두께 τ 분포·QQ ("너무 적고 너무 밝은" 진단 / Cloud optical depth distribution & QQ, "too few, too bright")
- **무엇을 보여주나**: 구름 광학두께 τ의 모델–위성 **분포(히스토그램/PDF)와 QQ-plot**. τ는 SW 반사(구름 알베도)를 지배 → SW CRE 오차의 직접 원인. 많은 모델의 "**too few, too bright**"(구름 개수 부족을 광학두께 과대로 보상) 결함을 τ 분포 상단/QQ 꼬리에서 노출.
- **읽는 법**: **PDF overlay** — 모델·관측 τ 분포 겹침; 모델이 두꺼운 쪽(고 τ)으로 편향+얇은 구름 과소면 "too few, too bright". **QQ** — x=관측 τ 분위수, y=모델; 상단 분위수가 1:1 위로 휘면 극단 τ 과대. (공통 QQ의 τ식 변형.)
- **언제 쓰나**: [격자]/[히스토그램] ISCCP·MODIS τ vs 모델(COSP-ISCCP/MODIS 산물). in-cloud vs grid-mean τ 구분.
- **짝지표 & 교차링크**: **τ percentile bias·KS·Perkins S** → [`28` 구름 광학두께 · QQ/PDF 분포 카드], [`03`]. 공통 QQ·PDF/CDF 상세는 [`figures/16` QQ-plot · Return-level/PDF]. τ–p 결합은 ⑧, SW CRE는 ⑤.
- **만드는 법**: `numpy.quantile`(공통 확률격자)→`matplotlib` QQ 산점+1:1선; PDF=`np.histogram`/`scipy.stats.gaussian_kde` overlay. **값-분포 축이라 지도 아님.** COSP로 관측 조건(주간·태양각) 정합.
- **함정·주의(§G 연결)**: **passive τ는 주간·일정 태양각만** → 야간·저조도 결측(일변동 왜곡), 3D 복사·부분운·태양각 편향. 얼음/액체 τ 가정 차. 꼬리 분위수 표본 적어 불안정(부트스트랩 CI). 분포만 보면 동시성(상관) 못 봄 → 공간(①)+관계(⑯) 병행.
- **출처**: Marchand et al. (2010, *JGR*, τ 히스토그램 리뷰, doi:10.1029/2009JD013422); Nam et al. (2012) "The 'too few, too bright' tropical low-cloud problem in CMIP5 models," *Geophysical Research Letters* 39:L21801, doi:10.1029/2012GL053421.

---

### ★ 일변동 조화곡선 + 진폭·위상 다이어그램 (일주기 검증 / Diurnal cycle: composite curve + amplitude–phase harmonic dial)
- **무엇을 보여주나**: SW↓·구름량·대류성 구름의 하루 주기를, (a) 지방태양시별 **합성(composite) 일주기 곡선**(모델·관측 overlay)과 (b) 1차 조화적합의 **진폭·위상 다이어그램**(극좌표 dial: 각=최대시각, 반경=진폭)으로 비교. 월평균이 맞아도 일변동(대류운 최대시각 등)이 틀린 것을 노출.
- **읽는 법**: (a) x=지방시(0~24h), y=플럭스/운량; 첨두 시각 어긋남=위상오차, 첨두 높이 차=진폭오차. (b) dial — 화살표 방향=최대시각(위상), 길이=진폭; 모델·관측 화살표 대조. *나쁜 패턴*: 육상 대류운이 오후 대신 정오/저녁, 해양 최대시각 편차. 위상은 **0/24h wrap 원형량**.
- **언제 쓰나**: [시계열] BSRN/ARM(고빈도), [격자] 정지위성(운량·CRE) vs 모델(시간별≤3h 출력 필요). 대류·경계층 구름 시간구조 진단.
- **짝지표 & 교차링크**: **일변동 진폭·위상(원형)** → [`28` 일변동 카드], [`06` 조화·위상 정의]. 위상 원형통계는 §E 시계열. 공간 위상 지도는 [`02`].
- **만드는 법**: 지방시 합성 후 `numpy` 1차 조화적합(FFT 또는 최소자승 cos/sin)으로 진폭·위상 → 곡선=`matplotlib`, dial=`projection='polar'`(각=시각→2π 환산). **곡선/극좌표라 지도 아님**(단, 위상 지리분포를 그리면 그건 지도 → `add_basemap()`+위경도 라벨 필수).
- **함정·주의(§G 연결)**: **극궤도 위성은 일변동 aliasing**(고정 통과시각→일주기 불가) → 정지위성 사용. 위상 **0/24h wrap** 처리(단위벡터/원형평균). 지방태양시 정합 필수. 모델 시간별 출력 없으면 성립 불가.
- **출처**: Yang & Slingo (2001) "The diurnal cycle in the tropics," *Monthly Weather Review* 129:784–801, doi:10.1175/1520-0493(2001)129<0784:TDCITT>2.0.CO;2 (확인요); [`06_timeseries_signal.md`](../06_timeseries_signal.md)(조화·위상 정의).

---

### ★ 계절순환·월평균 기후 지도 (계절 기후 검증 / Seasonal / monthly climatology maps & season–latitude section)
- **무엇을 보여주나**: 복사플럭스·구름량·CRE의 월평균/계절(DJF·JJA) 기후 **bias 지도**와, 계절진폭·위상, **계절–위도 단면**(zonal-mean, 월×위도). 계절별로 bias 성격이 바뀌므로 연평균만으로는 불충분(몬순·해빙역 부호 반전).
- **읽는 법**: **계절 bias 지도(DJF/JJA)** — 색=bias(발산맵); 계절 반전 영역(몬순·해빙역)에서 부호가 계절마다 바뀜. **계절–위도 단면** — x=월, y=위도, 색=값/bias; 계절진폭·최대월(원형 위상) 일치 확인. *나쁜 패턴*: 특정 계절만 큰 편차(계절 물리 결함).
- **언제 쓰나**: [격자] CERES-EBAF·ISCCP·GOCCP 월평균 vs 모델. 다년 climatology. 계절 bias 진단.
- **짝지표 & 교차링크**: **계절 bias·패턴상관·계절진폭/위상** → [`28` 계절순환·월평균 카드], [`02` ACC·climatology 정합]. 일주기는 ⑭, 연평균 공간은 ①②⑤⑥. 요약 [`figures/16` Taylor].
- **만드는 법**: `xarray` `groupby('time.season')`/`'time.month'` climatology→bias→**계절 bias 지도는 `cartopy` 해안선/육지+위경도 라벨 필수**(`add_basemap()`), `cmocean.cm.balance`. 계절–위도 단면은 `.mean('lon')` 후 `contourf(x='month', y='lat')`(이건 지도 아님).
- **함정·주의(§G 연결)**: **동일 기준기간 climatology**(모델·관측)—다르면 인위적 차([`02`] ACC 원칙). 짧은 기간은 내부변동 오염. **계절 지도엔 해안선+위경도 라벨 필수.** 계절별 별도 해석(연평균 상쇄 주의).
- **출처**: Loeb et al. (2018, *J. Climate*, CERES-EBAF, doi:10.1175/JCLI-D-17-0208.1); [`02_spatial_pattern_verification.md`](../02_spatial_pattern_verification.md)(ACC·패턴상관·climatology 정합).

---

### ★ 구름–복사 관계 그림 (구름-복사 정합 진단 / Cloud–radiation relationship plot, compensating-error diagnostic)
- **무엇을 보여주나**: 개별 변수가 아니라 **구름과 복사의 관계**(예: SW CRE vs 저층운량, LW CRE vs 운정온도, 구름 알베도 vs τ)를 모델·관측에서 결합분포/회귀/조건부 합성(구름레짐별 CRE)으로 비교. "맞는 복사를 맞는 이유(구름)로" 내는지 진단 — 단일변수 검증이 못 보는 **보상오차(compensating error)** 를 노출.
- **읽는 법**: **산점/이변량 밀도/회귀** — x=구름 변수(예: 저층운량), y=복사(예: SW CRE), 모델·관측 점운·회귀선 겹침. *좋은 패턴*: 관계(기울기·곡률)가 관측과 일치. *나쁜 패턴*: 복사 bias는 작은데 관계가 틀림(구름 너무 적은데 τ 과대로 SW 보상)=물리적으로 부실. 구름레짐(⑨)별 CRE 막대와 결합하면 강력.
- **언제 쓰나**: [격자] CERES CRE + ISCCP/CALIPSO 구름 vs 모델(동일 변수쌍·격자·시각). 물리 정합·보상오차 진단.
- **짝지표 & 교차링크**: **관계 기울기·조건부 CRE bias** → [`28` 구름–복사 관계 카드], APRP 요인분해 [`28` APRP], SW CRE [`28`/⑤], 레짐 ⑨. 공통 산점 [`figures/16`].
- **만드는 법**: `matplotlib` 산점/`hexbin`(이변량 밀도)+`numpy.polyfit`(관계 회귀); 조건부 합성은 `scipy.stats.binned_statistic`(구름변수 bin별 CRE 평균). **값-값 축이라 지도 아님.**
- **함정·주의(§G 연결)**: **상관≠인과**(정합 진단, 공변). **보상오차는 단일변수 검증으로 안 보임** → 관계+요인분해(APRP) 병행 필수. clear-sky 정의(CRE)·COSP(구름) 정합 상속. 영역 의존.
- **출처**: Nam et al. (2012, *GRL*, "too few, too bright", doi:10.1029/2012GL053421); Bodas-Salcedo et al. (2014) "Origins of the solar radiation biases over the Southern Ocean in CFMIP2 models," *Journal of Climate* 27(1):41–56, doi:10.1175/JCLI-D-13-00169.1; Bony et al. (2004, *Climate Dynamics*, 구름-복사 관계 진단 — 확인요).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 28(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 28(및 타 파일)·figures 교차링크 |
|---|---|---|---|---|---|
| 1 | TOA 복사플럭스 bias 지도 (RSUT/OLR/net) | 격자 | 편향+패턴(공간) | 격자 bias·RMSE·패턴상관 | 28 TOA 플럭스 · 02 · figures/16 bias map |
| 2 | 지표 SW↓/LW↓ bias 지도 + 위도대 평균 | 격자 | 편향+패턴(공간) | 격자 bias·RMSE | 28 지표 SW↓/LW↓ · 02 · 01 |
| 3 | 복사플럭스 검증 산점도 (+bias/RMSE box) | 격자·시계열 | 정확도+편향 | bias·RMSE·R·slope | 28 각 플럭스 · figures/16 산점 |
| 4 | BSRN/ARM 산점도 + 위치 지도(마커·ID) | 시계열 | 정확도(점 절대검증) | 대표성오차·bias·RMSE | 28 BSRN/ARM · 12·15 · plotting_maps §C |
| 5 | 구름복사효과 CRE 지도 (SW/LW/net) | 격자 | 통합(구름↔복사) | CRE bias·RMSE | 28 CRE · 02 · APRP · figures/16 |
| 6 | 전운량 bias 지도 + 관측 스프레드 | 격자 | 편향+패턴(구름량) | bias·패턴상관 | 28 전운량 · 02 · 01 |
| 7 | 구름분율 위도-고도 연직단면 | 연직·트랙 | 패턴(연직 배치) | 층별 CF bias·연직상관 | 28 연직 CF·저/중/고 · 02 |
| 8 | ISCCP τ–p 결합히스토그램 | 히스토그램 | 패턴(유형 구성) | 상자별 bias·히스토그램 RMS | 28 τ–p 히스토그램 · COSP |
| 9 | 구름레짐/WS RFO·CRE | 히스토그램 | 패턴(유형 빈도·복사) | 레짐 RFO·레짐별 CRE | 28 구름레짐 · ⑧·⑤ · 02 |
| 10 | CFAD (dBZ×height 빈도) | 트랙·연직 | 패턴(반사도 연직) | CFAD 차·고도별 빈도 | 28 CloudSat CFAD · COSP |
| 11 | CALIPSO SR–height 히스토그램 | 연직·트랙 | 패턴(얇은구름 연직) | SR 분포·CF(z) bias | 28 CALIPSO SR · ⑦·⑩ |
| 12 | 운정 CTH/CTT/CTP 검증 | 격자·트랙 | 정확도(연직 배치) | CTH/CTT/CTP bias·RMSE | 28 운정 · ⑧·⑤ · 01 |
| 13 | 구름 광학두께 τ 분포·QQ | 격자·히스토그램 | 분포·극값(τ) | percentile bias·KS·Perkins | 28 COD·QQ/PDF · 03 · figures/16 QQ |
| 14 | 일변동 조화곡선 + 진폭·위상 dial | 시계열·격자 | 위상(일주기) | 일변동 진폭·위상(원형) | 28 일변동 · 06 |
| 15 | 계절순환·월평균 기후 지도 | 격자 | 편향+패턴(계절) | 계절 bias·패턴상관·진폭/위상 | 28 계절순환 · 02 · figures/16 Taylor |
| 16 | 구름–복사 관계 그림 (보상오차) | 격자 | 물리 정합 | 관계 기울기·조건부 CRE bias | 28 구름–복사 관계·APRP · ⑨·⑤ |

> **묶음 권고**: 단일 그림 금지 원칙(§G-5)에 따라 구름·복사 검증 보고는 최소 **(복사 bias 지도 ①/②/⑤) + (구름장/연직구조 ⑥/⑦ 또는 유형 ⑧) + (구름–복사 관계 ⑯)** 를 기본 세트로. 지상 절대검증이면 **④**, 유형 진단이면 **⑧/⑨**, 연직 상세면 **⑩/⑪/⑫**, τ 분포·극단이면 **⑬**, 시간구조면 **⑭/⑮**를 추가한다. **구름 진단 그림(⑥⑦⑧⑨⑩⑪⑫)은 COSP 시뮬레이터 산물**로, **CRE·clear-sky 그림(⑤ 등)은 clear-sky 정의 정합**으로, **모든 지도형 그림(①②⑤⑥ + ④/⑨/⑮의 지도 패널)은 해안선/육지+위경도 라벨(add_basemap)** 로 그린다. 모든 임계는 **advisory + 영역·계절·해상도 의존 경고**로 캡션에 단다.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 지침·프레임워크 (실재)**
- Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (산점·QQ·bias map 등 공통 시각화 → [`figures/16`]).

**학술 논문 (제목·저널·연도 웹 확인)**
- Loeb, N. G., et al. (2018) "Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced and Filled (EBAF) Top-of-Atmosphere (TOA) Edition-4.0 Data Product," *Journal of Climate* 31(2):895–918. **doi:10.1175/JCLI-D-17-0208.1** (확인).
- Kato, S., et al. (2018) "Surface Irradiances of Edition 4.0 CERES-EBAF Data Product," *Journal of Climate* 31(11):4501–4527. **doi:10.1175/JCLI-D-17-0523.1** (확인).
- Driemel, A., et al. (2018) "Baseline Surface Radiation Network (BSRN): structure and data description (1992–2017)," *Earth System Science Data* 10:1491–1501. **doi:10.5194/essd-10-1491-2018** (확인).
- Chepfer, H., et al. (2010) "The GCM-Oriented CALIPSO Cloud Product (CALIPSO-GOCCP)," *JGR: Atmospheres* 115:D00H16. **doi:10.1029/2009JD012251** (확인).
- Klein, S. A., et al. (2013) "Are climate model simulations of clouds improving? An evaluation using the ISCCP simulator," *JGR: Atmospheres* 118:1329–1342. **doi:10.1002/jgrd.50141** (확인).
- Klein, S. A., & Jakob, C. (1999) "Validation and sensitivities of frontal clouds simulated by the ECMWF model," *Monthly Weather Review* 127:2514–2531 (τ–p 진단 도입).
- Webb, M., et al. (2001) "Combining ERBE and ISCCP data to assess clouds in the Hadley Centre, ECMWF and LMD atmospheric climate models," *Climate Dynamics* 17:905–922.
- Jakob, C., & Tselioudis, G. (2003) "Objective identification of cloud regimes in the Tropical Western Pacific," *Geophysical Research Letters* 30(21):2082. **doi:10.1029/2003GL018367** (확인).
- Bodas-Salcedo, A., et al. (2008) "Evaluating cloud systems in the Met Office global forecast model using simulated CloudSat radar reflectivities," *Journal of Geophysical Research* 113:D00A13. **doi:10.1029/2007JD009620** (확인).
- Bodas-Salcedo, A., et al. (2011) "COSP: Satellite simulation software for model assessment," *BAMS* 92(8):1023–1043. **doi:10.1175/2011BAMS2856.1** (확인).
- Marchand, R., et al. (2010) "A review of cloud top height and optical depth histograms from MISR, ISCCP, and MODIS," *JGR: Atmospheres* 115:D16206. **doi:10.1029/2009JD013422** (확인).
- Nam, C., et al. (2012) "The 'too few, too bright' tropical low-cloud problem in CMIP5 models," *Geophysical Research Letters* 39:L21801. **doi:10.1029/2012GL053421** (확인).
- Bodas-Salcedo, A., et al. (2014) "Origins of the solar radiation biases over the Southern Ocean in CFMIP2 models," *Journal of Climate* 27(1):41–56. **doi:10.1175/JCLI-D-13-00169.1** (확인).
- Rossow, W. B., & Schiffer, R. A. (1999) "Advances in understanding clouds from ISCCP," *BAMS* 80(11):2261–2287.
- Wild, M., et al. (2013) "The global energy balance from a surface perspective," *Climate Dynamics* 40:3107–3134 (doi:10.1007/s00382-012-1569-8).

**소프트웨어 (실존 도구)**
- `xarray`/`xesmf`(재격자·climatology·zonal-mean), `cartopy`(지도·해안선·위경도 라벨 → [`plotting_maps.md` `add_basemap()`]), `matplotlib`(`pcolormesh`/`contourf`/`hexbin`/polar dial), `numpy`/`scipy.stats`(quantile·binned_statistic·조화적합), `scikit-learn`(`KMeans` 구름레짐), `cmocean`(balance/thermal 색맵).
- **COSP** — CFMIP Observation Simulator Package(ISCCP/MODIS/MISR/CALIPSO/CloudSat 시뮬레이터): 구름 진단 그림의 필수 전처리(Bodas-Salcedo et al. 2011; Swales et al. 2018 COSP2, *GMD* 11:77–81, doi:10.5194/gmd-11-77-2018).
- **ESMValTool** / **E3SM Diags** — 구름·복사 진단(CERES 복사, CRE, CTP-τ/ISCCP·MODIS joint histogram, CALIPSO/CloudSat CF·CFAD·SR) recipe/진단 내장(Python·xarray·cartopy 기반).

**확인요 (확정 인용 금지 — §G-6)**
- Pincus et al. (2012, *J. Climate*, MODIS 시뮬레이터) · Kay et al. (2012, *J. Climate*, CALIPSO 시뮬레이터 평가) · Cesana & Chepfer (2013, *JGR*, CMIP5 연직구조 권·DOI) · Tselioudis et al. (2013, global weather states) · Williams & Webb (2009, cloud regimes 모델평가) · Bony et al. (2004, *Climate Dynamics*, 구름-복사 관계) · Allan (2011, *Meteorological Applications*, CRE 개념) · Stokes & Schwartz (1994, *BAMS*, ARM) — 제목·연도는 [`28`]에서 인용, 본 세션 권·DOI 재확인 안 함.
- Yang & Slingo (2001, *MWR* 129:784–801) — 제목·저널·권 확인, **DOI 문자열은 패턴 추정(확인요)**.
- 해석 임계(복사 bias·RMSE·useful-scale·SSIM·SR/reflectivity 임계 등)는 **영역·계절·해상도·기준자료 의존 advisory** — CERES-EBAF 자체 불확실성(전지구 순 ~수 W/m²)을 하한으로(§G-4).
