# 검증 시각화 카탈로그 — [해양 생지화학·해색 도메인편] (Verification Figures: Ocean Biogeochemistry & Ocean Colour)

이 문서는 해양 생지화학(BGC) 모델·지구시스템모델(ESM)의 생지화학 컴포넌트(PISCES, MOM6-COBALT, MEDUSA, BLING, HAMOCC, TOPAZ 등)와 위성 해색(ocean colour) 산출물을 **정점(관측소) 시계열**(BATS·HOT·CARIACO·ESTOC), **BGC-Argo 프로파일**, **선박 병시료 DB**(GLODAPv2·SOCAT), **기후값 격자**(World Ocean Atlas·GLODAP 격자·CMEMS BGC 재분석), **위성 트랙/L3·L4 해색**(Chl-a·Kd·NPP·PIC)과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 해양 생지화학·해색 도메인편이다. 메서드(수치지표) 카드는 [`29_domain_ocean_biogeochemistry.md`](../29_domain_ocean_biogeochemistry.md)에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **대응 메서드카탈로그: `29_domain_ocean_biogeochemistry.md`** (각 그림 카드는 이 파일의 메서드 카드와 짝지어 교차링크한다).

> **공통/횡단 그림과의 분담**: Taylor·Target·QQ(일반)·reliability·rank histogram·성능 다이어그램·PDF/CDF·Hovmöller·EOF 등 **도메인 무관 요약그림은 [공통편 `16_fig_common.md`] 담당**이라 여기서 중복 정의하지 않고 **교차링크만** 한다. 이 파일은 **생지화학 고유 그림**(로그-로그 Chl-a 매치업 산점, log 색 Chl 지도, 위도-깊이 O2/영양염 단면, BGC-Argo 프로파일 비교, pCO2 지도, Ω 아라고나이트, 탄산계 내부정합 등)과 **공통 그림의 생지화학식 변형**(log 공간 QQ/PDF, MdSA box를 얹은 Chl 산점 등)에 집중한다.

> **자료형 약어**(29와 동일): [격자]=NetCDF 격자(모델/재분석/기후값) · [정점]=관측정점 시계열(BATS·HOT 등 CSV) · [프로파일]=BGC-Argo·CTD-로제트 깊이별 · [트랙/L2]=위성 along-track/L2 · [L3/L4]=합성·보간 위성 격자 · [병시료]=선박 이산 시료(GLODAP·SOCAT).

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 위성 Chl·WOA·GLODAP·SOCAT·BGC-Argo는 모두 reference이지 truth가 아니다. 특히 위성 Chl·NPP·PFT는 **알고리즘 산물**이다. 축·범례·캡션에 "모델 − 기준(reference)"으로 쓰고 "오차"가 아니라 "모델−기준 차"로 표현한다.
> 2. **로그정규 변수는 log10 공간에서.** Chl-a·영양염·NPP는 수 자릿수에 걸쳐 분포 → 선형공간 RMSE는 고농도 연안값이 지배해 오해를 부른다. 축·색·통계 모두 log10 공간 명시(→ 29 엽록소 로그통계 카드, Campbell 1995).
> 3. **탄산계는 규약이 결정적.** pH 스케일(total/free/seawater)·K1K2 상수 조·압력·온도기준·영양염 입력이 다르면 수십 μatm·0.01 pH·포화수심 수백 m 차이가 "모델 오차"로 오인된다. 비교 전 **동일 규약으로 CO2SYS 재계산**(→ 29 탄산계 내부정합 카드).
> 4. **해석 임계는 advisory.** 위성 Chl "±35%(0.35 log10)", pH 추세 "−0.02/decade", Stow CF<1·MEF>0 등은 **관행값**이며 해역(Case-1/Case-2)·수형·계절·센서·알고리즘 의존. 그림에 "good/bad"를 단정하지 말고 영역·계절 의존 경고를 캡션에 둔다.
> 5. **단일 그림 금지.** 산점도(정확도) 하나로 결론내지 말고 최소 **정확도+편향+분포/패턴**(예: log 산점 + bias 지도 + log QQ)과 유의성(부트스트랩 CI)을 함께 낸다.
> 6. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문 도판을 그대로 재현하지 않고, 우리 데이터로 직접 렌더링해 무저작권 예시를 만든다.

> ★ **지도형(위경도) 그림 공통 규칙**: 축이 경도·위도이면 지도다 → **해안선/육지 + 라벨된 위경도 격자선 필수**([`plotting_maps.md`](../../plotting_maps.md)의 `add_basemap()` 사용). 해양 전용 필드는 육지 마스킹 후 육지를 데이터 **위**로. bias는 발산맵+0=흰색(`TwoSlopeNorm`/`cmocean.cm.balance`), 비음수(RMSE·MdSA)는 순차맵. 경도 0–360↔−180–180 규약·날짜변경선 주의. 정점 그림은 위치 지도+마커+ID(§C).

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **로그-로그 Chl-a 매치업 산점 + MdSA/bias box** — 해색 검증의 1차 대표 그림
2. ★ **표층 Chl-a 지도 (log 색, basemap)** — 위성 vs 모델 공간 분포
3. ★ **Chl-a log-bias / log-RMSD 공간 지도** — 계통편차의 지리 위치
4. ★ **Chl 계절주기·개화 phenology 곡선** — 진폭·위상·개화 개시일
5. ★ **위도-깊이 단면 (O2·영양염·DIC 등치선+차 단면)** — 심층 3차원 구조
6. ★ **BGC-Argo 연직 프로파일 비교 (+정점 위치 지도)** — 프로파일 단위 검증
7. ★ **산소최소층(OMZ) 진단 그림** — 저산소 등치면·부피·코어수심
8. ★ **표층 pCO2 / ΔpCO2 지도 (SOCAT 매치업)** — 해–기 CO2 플럭스 패턴
9. ★ **pH / 아라고나이트 포화도 Ω 진단** — 산성화·포화수심·부식성 수체
10. ★ **탄산계 내부정합 진단 (CO2SYS closure)** — 2쌍 유도 잔차
11. ★ **T–S / property–property 산점 (Redfield·TA–SSS·AOU 관계)** — 화학량론·보존관계
12. ★ **log 공간 QQ / PDF·CDF 비교** — 저·고농도 꼬리, 로그정규 분포
13. ★ **순1차생산 NPP 검증 (알고리즘 envelope 산점)** — 위성/모델 NPP
14. **식물플랑크톤 PFT·크기분율 검증 (혼동행렬·분율 지도)** — 군집 구조
15. ★ **생지화학 다변수 스킬 요약 (Target/Taylor/cost-function 히트맵)** — 종합틀
16. **경보·임계 사건 검증 (HAB/저산소/저Ω 초과)** — 성능 다이어그램·POD/FAR

---

### ★ 로그-로그 Chl-a 매치업 산점 + MdSA/bias box (엽록소 로그-로그 매치업 산점 / Chlorophyll-a log–log match-up scatter with MdSA box)
- **무엇을 보여주나**: 매치업된 (관측 Chl-a, 모델/위성 Chl-a) 쌍을 **양축 log10** 산점하고 1:1선·Type-II(직교/RMA) 회귀선·핵심 스칼라(log-bias·log-RMSD·MdSA·기하 bias비·slope·R(log)·N)를 함께 얹은, 해색 검증의 **표준 1장**. NASA OBPG 해색 검증의 기본 도판 양식(Bailey–Werdell 매치업 통과분).
- **읽는 법**: x=관측(위성 L3/L4·HPLC·정점), y=모델/알고리즘, **둘 다 log10축**(0.01~30 mg m⁻³ 4-decade). **1:1선**(점선)이 기준, **Type-II 회귀선**(실선)을 함께(OLS는 회귀희석 편향). 텍스트 box에 MdSA(%)·기하 bias비·slope·R(log)·N. *좋은 패턴*: 점운이 1:1에 좁게 밀착, 4-decade 전체에서 slope≈1, MdSA 작음. *나쁜 패턴*: 저Chl(<0.1) 외해에서 y가 1:1 위로(모델 과대) 부채꼴, 고Chl(>1) 개화에서 1:1 아래로 휨(과소); 저·고농도에서 각기 다른 기울기=조건부 편향(Case-2 실패 신호).
- **언제 쓰나**: [L3/L4]·[정점]·[병시료] 매치업, 표본 수십~수천. 위성 알고리즘·모델 vs in situ 정확도+편향 1차 점검. **로그정규 변수(NPP·영양염)에도 같은 양식 재사용**.
- **짝지표 & 교차링크**: **log-bias·log-RMSD·MdSA·기하 bias비·Type-II slope·R(log)·winning%** → [29 엽록소 로그통계 카드], [29 해색 밴드비·불확실성 카드], [29 해색 매치업 프로토콜]. 대용량이면 밀도산점([`16`](./16_fig_common.md) 밀도/hexbin) 승급. 분포 일치는 ⑫ log QQ, 종합비교는 [`16`](./16_fig_common.md) Taylor/Target.
- **만드는 법**: `matplotlib` `ax.scatter(np.log10(o), np.log10(m))` 또는 축을 `ax.set_xscale('log')`. Type-II 회귀는 직교/RMA(자체 구현 또는 `scipy.odr`); MdSA는 29 정의식 `100*(10**np.median(np.abs(np.log10(m/o)))−1)`을 numpy로. 축 동일 범위·`set_aspect('equal')`·1:1선 `ax.axline((0.01,0.01),(30,30))`. 저·고Chl 구간 분리 box 권장.
- **함정·주의**: **선형 vs log 공간 혼용 시 결론이 뒤집힘** → 공간 명시 필수(§ 원칙 2). OLS slope는 회귀희석 → **Type-II** 병행. 위성 Chl은 알고리즘 산물(진값 아님) → "모델−위성 차". 3×3 매치업 대표성 오차(점 vs ~km²)가 산포에 포함. 연안 Case-2 과대·과소 심함(외해/연안 분리 보고).
- **출처**: Bailey & Werdell (2006, *Remote Sensing of Environment* 102(1–2):12–23, 매치업 프로토콜); Seegers et al. (2018, *Optics Express* 26(6):7404–7422, MdSA 등 성능지표, [opg.optica.org](https://opg.optica.org/oe/fulltext.cfm?uri=oe-26-6-7404)); Campbell (1995, *JGR Oceans* 100(C7):13237–13254, 로그정규); Stow et al. (2009, *J. Marine Systems* 76:4–15, 회귀희석 논의).

---

### ★ 표층 Chl-a 지도 (log 색, basemap) (표층 엽록소 지도 / Surface chlorophyll-a map, log colour)
- **무엇을 보여주나**: 모델 표층 Chl [격자]와 위성 [L3/L4] Chl(OC-CCI·GlobColour·MODIS·VIIRS·OLCI)을 **나란한 지도 패널**(모델 / 위성 / 차)로 그려 개화대·빈영양 gyre·용승대·연안의 **공간 분포·강도**를 대조. 생지화학 모델의 1차 정성 진단.
- **읽는 법**: 색=Chl(**log10 스케일**, `cmocean.cm.algae`), 위경도 라벨+해안선. 세 패널(model·satellite·model−satellite). *좋은 패턴*: 아열대 gyre 저Chl·고위도·용승대·연안 고Chl의 위치·경계가 일치. *나쁜 패턴*: 모델 연안 개화 과대(육지 인접 붉은 띠), 외해 빈영양 과소(gyre 너무 진함), 적도용승·서안경계류 위치 어긋남. 차 패널은 log-차 발산맵.
- **언제 쓰나**: [격자] 모델 vs [L3/L4] 위성 기후값·월합성. 정성 공간 개요(정량은 ③으로).
- **짝지표 & 교차링크**: 격자별 **log-bias·log-RMSD·R·MdSA**(③에서 정량화) → [29 위성 vs 모델 표층 Chl 공간검증 카드]. 패턴상관·Taylor·ACC는 [`16`](./16_fig_common.md). 계절구조는 ④.
- **만드는 법**: `xarray`+`cartopy` `pcolormesh(..., norm=LogNorm(), cmap=cmocean.cm.algae, transform=ccrs.PlateCarree())`. **★ `add_basemap()`으로 해안선/육지+위경도 라벨 필수**([`plotting_maps.md`](../../plotting_maps.md)). 육지 마스킹 후 `cfeature.LAND` 높은 zorder. 재격자화(§15) 공통 격자.
- **함정·주의**: **★ 지도인데 basemap(해안선·위경도 라벨) 누락 = 위치 식별 불가** → `add_basemap` 필수. **선형 색스케일은 gyre 저Chl를 뭉갬 → log 색 필수**. 위성 Chl은 표층 ~1 광학심도 신호, 모델은 격자층 평균 → 대표성 차. 위성 L4는 보간·병합 산물(§G-3, "정답" 아님). 경도 0–360↔−180–180·연안 Case-2 오차.
- **출처**: Sathyendranath et al. (ESA Ocean Colour CCI 산출물 문서); Gregg & Casey (2004, *RSE*, 전지구 위성-모델 Chl 비교); cmocean(Thyng et al. 2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66, [tos.org](https://tos.org/oceanography/assets/docs/29-3_thyng.pdf), `algae` 색맵).

---

### ★ Chl-a log-bias / log-RMSD 공간 지도 (엽록소 로그편차 지도 / Gridded Chl log-bias / log-RMSD map)
- **무엇을 보여주나**: 모델 표층 Chl [격자]를 위성 [L3/L4]와 **공간 전면적**으로 비교해 각 격자점 시계열의 **log10-bias(x,y)·log-RMSD(x,y)·MdSA(x,y)·R(x,y)** 를 지도(색)로. 정점 없는 해역까지 계통편차의 **지리적 위치·계절성** 진단.
- **읽는 법**: bias는 **발산맵(0=흰색)**, log10 단위(예 ±1 = 10배). 붉음=모델 과대(연안 흔함), 파랑=과소(외해 빈영양 흔함). RMSD/MdSA는 순차맵. 위도대·해역 평균선 병행. *나쁜 패턴*: 연안 따라 넓은 붉은 띠(연안 개화 과대), 아열대 gyre 파란 영역(빈영양 과소), 적도용승대 부호 쏠림.
- **언제 쓰나**: [격자]vs[L3/L4] NetCDF. 광역 진단, 점 검증(⑥)이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 격자별 **log-bias·log-RMSD·MdSA·R** → [29 위성 vs 모델 표층 Chl 공간검증 카드], [29 기후값 격자-격자 공간비교]. 공간패턴·재격자는 [`16`](./16_fig_common.md) bias map·ACC, `02`·`15`. 점 검증 ⑥와 교차해석.
- **만드는 법**: `xarray`+`xesmf`(conservative/bilinear 재격자, 공통 격자)→각 격자점 log10 통계→`cartopy` `pcolormesh`. **발산 색맵 `cmocean.cm.balance`**(bias)·`cmo.matter`/`amp`(RMSD). **★ `add_basemap()` 필수**, 육지/구름·극야 마스크 통일, `TwoSlopeNorm(vcenter=0)`.
- **함정·주의**: **★ 지도 → basemap 필수**(해안선·위경도 라벨). **log 공간에서 통계**(선형 bias는 연안 지배). 위성 L4는 독립 진값 아님(§G-1, 부이·정점 교차). 재격자 순서·방식이 차이장을 바꿈(§15). 위성 표층 vs 모델 격자층 대표성. 연안 Case-2·극지 저광 오차 큼(영역 분리 경고).
- **출처**: Gregg & Casey (2004, *RSE*); Sathyendranath et al. (OC-CCI 문서); Séférian et al. (2020, *Current Climate Change Reports*, CMIP6 BGC 평가); cmocean(Thyng et al. 2016, doi:10.5670/oceanog.2016.66).

---

### ★ Chl 계절주기·개화 phenology 곡선 (엽록소 계절주기·개화 시점 / Chl seasonal cycle & bloom phenology)
- **무엇을 보여주나**: 한 해역·정점의 Chl **월기후값 곡선**을 모델·위성이 함께 그리고, **개화 개시(bloom onset)·최성기(peak)·기간**을 표시. 평균 통계가 못 보는 **진폭·위상·시간구조** 검증(온대 춘계개화 / 아열대 겨울1회 / 극지 짧은 여름 체제).
- **읽는 법**: x=월(1–12, 순환), y=Chl(log 권장). 두 곡선의 **최대월 어긋남=위상오차**, 봉우리 높이 차=진폭오차, 개시일 수직선 차=phenology 오차. *좋은 패턴*: 진폭·최성기월·개시일 일치. *나쁜 패턴*: 모델 개화 조기/지연(혼합층·성층·광 커플링 문제), 진폭 과소(개화 못 잡음), 아열대에서 봉우리 없음. 다년 평균으로 노이즈 저감, 결측(극야) 구간 표시.
- **언제 쓰나**: [L3/L4]·[정점]·[격자] Chl 시계열. 체제별 계절·개화 진단. 사건이 아니라 *시간구조* 비교.
- **짝지표 & 교차링크**: **계절 진폭·위상오차·개화 개시일·기간** → [29 엽록소 계절주기·개화 시점 카드]. 조화적합(연·반년)은 `05`/`06`, 시계열 overlay+잔차·lag는 [`16`](./16_fig_common.md) 시계열 가족. 진폭·위상 종합은 Taylor.
- **만드는 법**: `pandas`/`xarray` `groupby('time.month').mean()`로 월기후값 → `matplotlib` overlay. 개시일은 임계법(중앙값+5%)·누적법·변곡점법 중 **정의 명시**. 위상은 순환(월) 시차. 결측은 끊어 그림(직선보간 금지).
- **함정·주의**: **개화 개시 정의(임계/누적/변곡)마다 값이 달라짐** → 정의·임계 캡션 명시(모델·위성 동일). **극야·구름 결측이 고위도 개시 추정 왜곡**(보간법 명시). 한 해역 결론을 전 해역 일반화 금지. log/선형 공간 통일.
- **출처**: Racault et al. (2012, *Ecological Indicators*, ocean-colour phytoplankton phenology); Siegel et al. (2002, *Science* 296:730–733, 북대서양 춘계개화·임계심도); Henson et al. (개화 phenology 검증 관행).

---

### ★ 위도-깊이 단면 (O2·영양염·DIC 등치선+차 단면) (연직 단면 비교 / Latitude–depth section: isolines + difference)
- **무엇을 보여주나**: O2·NO3·PO4·Si·DIC·pH 등의 **위도-깊이(또는 경도-깊이) 단면**을 모델·관측(WOA/GLODAP) 나란히, 그리고 **차 단면**(model−obs)으로. 표층·격자통계가 못 보는 **심층 3차원 구조**(재광물화·환기·OMZ·심층 재고)의 계통편차 위치를 본다.
- **읽는 법**: x=위도, y=깊이(로그 또는 상부 확대, **아래로 증가**), 색/등치선=변수. 3패널(model·obs·diff). *좋은 패턴*: 약층·등치선 경사·심층 값이 일치. *나쁜 패턴*: 심층 O2 음(모델 재광물화 과강/환기 과약), 열대 중층 저산소 과강·과약, 심층 DIC 양(재광물화 과강), 약층 심도 이동. 차 단면은 발산맵(0=흰색).
- **언제 쓰나**: [프로파일]/[격자] BGC-Argo·GLODAP·WOA vs 모델. 심층·수직구조 진단. (지리축 아님 → basemap 불필요, 단 단면 위치 인셋 지도 권장.)
- **짝지표 & 교차링크**: **깊이별 bias·RMSE 프로파일·약층 심도·등밀도면 값** → [29 연직 프로파일·단면 비교 카드], [29 용존산소·영양염·DIC 카드]. 프로파일 형상은 ⑥, OMZ 부피는 ⑦. Taylor/Target은 [`16`](./16_fig_common.md).
- **만드는 법**: `xarray` 경도평균(`.mean('lon')`) 후 `matplotlib` `contourf`/`pcolormesh`(y=depth, `ax.invert_yaxis()`). **★ 단면이 어디 경도대인지 위치 인셋 지도**(`add_basemap` 소형)로 표시 권장(정점 그림 규칙 §C 준용). 발산맵 `cmocean.cm.balance`(차), 순차 `cmo.oxy`(O2)/`cmo.tempo`.
- **함정·주의**: **등수심 vs 등밀도 비교 선택이 결론 좌우**(약층 이동에 등수심 민감 → 성층 오차를 생물오차로 오인) → 선택 명시, 심층은 등밀도 유리. **단위 통일**(μmol kg⁻¹ vs μmol L⁻¹, 밀도 환산). WOA/GLODAP는 보간 기후값(sparse, §G-3). 수직해상도 보간(§15).
- **출처**: Stow et al. (2009, *J. Marine Systems* 76:4–15); WOCE/GO-SHIP 단면 관행; Séférian et al. (2020, *Current Climate Change Reports*, CMIP6 BGC 단면 진단); cmocean(Thyng et al. 2016, `oxy`/`tempo`/`deep` 색맵).

---

### ★ BGC-Argo 연직 프로파일 비교 (+정점/플로트 위치 지도) (프로파일 비교 / BGC-Argo vertical profile comparison + float map)
- **무엇을 보여주나**: BGC-Argo(또는 GLODAP/정점) O2·NO3·pH·Chl 형광 **연직 프로파일**을 모델 콜로케이션 프로파일과 **겹쳐** 그리고, 옆에 **플로트/정점 위치 지도**(마커+ID). 프로파일 단위로 약층·DCM·심층 구조를 진단하고 동시에 float 센서 편향(ship crossover)을 본다.
- **읽는 법**: 좌: y=깊이(아래로 증가), x=변수, 모델선·관측선(±관측 불확실 띠) 겹침. 우: 위경도 지도에 플로트 궤적·정점 마커+ID. *좋은 패턴*: 약층 심도·표층값·심층값 일치, DCM(심층엽록소극대) 심도 일치. *나쁜 패턴*: 표층 Chl은 맞아도 DCM 심도/강도 어긋남(위성이 못 보는 부분), 약층 과천/과심, 심층 O2 계통 offset.
- **언제 쓰나**: [프로파일] BGC-Argo·GLODAP·정점 vs [격자] 모델. 심층·DCM·적분 검증(위성 표층 불가 영역).
- **짝지표 & 교차링크**: **깊이/밀도면별 bias·RMSE·약층 심도·DCM·float 편향** → [29 BGC-Argo 매치업·플랫폼 오차 카드], [29 적분·재고량 카드], [29 영양염 프로파일·약층 심도 카드]. 단면은 ⑤, 프로파일 통계 종합은 Taylor([`16`](./16_fig_common.md)).
- **만드는 법**: `argopy`로 BGC-Argo adjusted 자료 로드 → `xarray` 콜로케이션(§15) → `matplotlib` 프로파일 overlay(`ax.invert_yaxis()`). **★ 위치 지도는 `add_basemap()`으로 해안선+위경도 라벨, 각 플로트/정점에 마커+ID 라벨**([`plotting_maps.md`](../../plotting_maps.md) §C). 인셋 로케이터맵 권장.
- **함정·주의**: **★ 위치 지도 필수(해안선+마커+ID)** — 프로파일이 어디 것인지 못 읽음. **float QC 등급·보정 적용분(adjusted) 사용, raw 금지**(§G-3). Chl 형광은 slope factor(공장기본값 ~2배 과대)·NPQ(주간 소광) 보정, O2는 air-calibration, pH는 체계적 편향 보정 명시. 점 vs 격자 대표성. 등수심/등밀도 선택.
- **출처**: Claustre, Johnson & Takeshita (2020, *Annual Review of Marine Science* 12:23–48, BGC-Argo 리뷰); Johnson et al. (2017, *JGR Oceans*, SOCCOM float QC); Cornec et al. (2021, *GBC*, BGC-Argo DCM); `argopy`(euroargodev.github.io/argopy).

---

### ★ 산소최소층(OMZ) 진단 그림 (산소최소층 진단 / Oxygen minimum zone: iso-surface, volume, core depth)
- **무엇을 보여주나**: 모델이 산소최소층(OMZ)의 **강도·부피·수직범위·수평위치**를 관측(WOA·GLODAP·BGC-Argo)과 일치시키는지 — (a) 저산소 임계 등치면의 **수평 범위 지도**, (b) OMZ **부피·코어수심 막대**(model vs obs ±CI), (c) 위도-깊이 단면의 저산소 코어. 저산소는 생태·탈질·N2O의 핵심 → BGC 모델 난제.
- **읽는 법**: (a) 지도: O2<θ(예 60·20·5 μmol kg⁻¹) 등치면 면적·위치(발산 아님, 임계 명시). (b) 막대: 저산소 수체 부피·최소 O2·코어수심을 model/obs 비교, CI 겹침으로 판정. (c) 단면: 코어 심도·두께. *나쁜 패턴*: 대서양 OMZ 과강, 인도양·아라비아해 부피 과소·과천(CMIP 공통 편차), 코어수심 이동.
- **언제 쓰나**: [격자] 모델 vs [격자] WOA·[프로파일] BGC-Argo. 동태평양·아라비아해·벵골만·동남태평양 OMZ.
- **짝지표 & 교차링크**: **저산소 부피 ∫∫∫1[O2<θ]dV·코어수심·최소O2·수평면적** → [29 산소최소층 진단 카드], [29 용존산소 카드], [29 AOU 카드]. 단면은 ⑤, 임계초과 사건은 ⑯.
- **만드는 법**: `xarray`로 O2<θ 마스크 → 부피는 층두께×면적(cosφ) 가중합, 코어수심은 `argmin('depth')`. (a) 등치면 면적 지도 `cartopy` `contourf`(**★ `add_basemap()` 필수**). (b) 막대 `matplotlib`. 순차 색맵 `cmocean.cm.oxy`(O2 전용, 저산소 강조 이산화). 임계·밀도면 정의 통일.
- **함정·주의**: **임계값·등수심/등밀도 선택에 극도로 민감** → 명시(§G-4). 조밀도 낮은 격자·수직해상도가 OMZ 두께 왜곡. 저농도(O2<수 μmol)는 모델·센서 모두 불확실. 관측 기후값 sparse(§G-3). (a)는 지도 → basemap 필수. **CMIP는 열대 OMZ 재현이 체계적으로 어려움** → good/bad 단정 금지.
- **출처**: Cabré et al. (2015, *Biogeosciences* 12:5429, CMIP5 OMZ); Bianchi et al. (2012, *Global Biogeochemical Cycles*, OMZ 부피·N2O); Busecke et al. (2022, *AGU Advances* 3, doi:10.1029/2021AV000470, Pacific OMZ); Oschlies et al. (2018, *Nature Geoscience* 11:467–473, 탈산소).

---

### ★ 표층 pCO2 / ΔpCO2 지도 (SOCAT 매치업) (표층 pCO2·해–기 플럭스 / Surface pCO2 & ΔpCO2 map, SOCAT match-up)
- **무엇을 보여주나**: 모델 표층 해양 pCO2(fCO2)를 SOCAT 관측(cruise/gridded)과 **시공간 콜로케이션**한 산점도(bias/RMSE box, μatm)와, ΔpCO2=pCO2_ocean−pCO2_air 또는 해–기 플럭스의 **공간 지도**. 해양 탄소흡수원 검증의 핵심.
- **읽는 법**: 산점은 ① 양식(선형축, μatm; pCO2는 log 불필요). 지도는 ΔpCO2(발산맵, 0=흰색): 음(흡수, 고위도)·양(방출, 적도용승). 계절진폭·위도대 평균 플럭스 병행. *좋은 패턴*: 흡수/방출 패턴·계절진폭·위도대 플럭스 일치. *나쁜 패턴*: 적도용승 방출 과대/과소, 남대양 흡수 오차, 계절진폭 축소. pCO2는 온도민감(∂lnpCO2/∂T≈4.23%/℃) → 열/비열 성분(Takahashi) 분해 병행.
- **언제 쓰나**: [트랙/병시료] SOCAT vs [격자] 모델. 해–기 플럭스·탄소흡수 패턴.
- **짝지표 & 교차링크**: **ΔpCO2·bias·RMSE·계절진폭·위도대 플럭스** → [29 표층 pCO2 검증 카드]. 위성/트랙 콜로케이션은 `12`, 매치업 대표성은 `15`. 산점은 ①과 형제.
- **만드는 법**: `xarray`로 SOCAT gridded(월 1°) 또는 cruise 콜로케이션(§15) → `matplotlib` 산점 + `cartopy` ΔpCO2 지도(**★ `add_basemap()` 필수**, `TwoSlopeNorm(vcenter=0)`, `cmocean.cm.balance`). fCO2↔pCO2 fugacity 변환·온도기준 통일. 플럭스는 k(풍속의존)·용해도식 명시.
- **함정·주의**: **★ 지도 → basemap 필수**. **fCO2 vs pCO2 변환 통일**. **SOCAT는 시공간 편중**(북반구·항로 집중, 남대양·겨울 sparse) → 미표집 해역 외삽 주의. 플럭스 오차는 ΔpCO2·k·풍속 오차의 곱 전파. 온도기준(현장 SST) 정합.
- **출처**: Bakker et al. (2016, *ESSD* 8:383–413, SOCATv3, doi:10.5194/essd-8-383-2016, [essd.copernicus.org](https://essd.copernicus.org/articles/8/383/2016/)); Takahashi et al. (2009, *Deep-Sea Research II* 56:554–577, 표층 pCO2 기후·해–기 플럭스); Wanninkhof (2014, *L&O Methods* 12:351–362, 가스전달속도); Fay et al. / RECCAP2 해양 탄소 검증 프레임.

---

### ★ pH / 아라고나이트 포화도 Ω 진단 (pH·포화도 Ω / pH & aragonite saturation state)
- **무엇을 보여주나**: 모델 표층·심층 pH(total scale)와 아라고나이트/칼사이트 포화도 Ω, **포화수심(saturation horizon, Ω=1)** 을 관측 유도값(GLODAP·정점·BGC-Argo)과 비교 — (a) 표층 Ω_ar/pH 지도, (b) **Ω 연직 프로파일·포화수심 단면**, (c) pH 산성화 추세(dpH/dt) 시계열. 산성화·석회화 생물 영향의 핵심.
- **읽는 법**: (a) 지도: Ω_ar(극지·용승대에서 1 근접, 취약). (b) 프로파일: Ω=1 도달 수심(포화수심) model vs obs 비교; 부식성(Ω<1) 수체 부피. (c) 추세: pH 시계열 기울기(관측대 ≈−0.02/decade). *나쁜 패턴*: 포화수심 수백 m 이동(상수·압력보정 차이일 수 있음), 표층 Ω_ar bias, 추세 과소.
- **언제 쓰나**: [병시료] GLODAP·[정점] BATS/HOT/ESTOC·[프로파일] BGC-Argo pH 유도 vs [격자] 모델.
- **짝지표 & 교차링크**: **Ω_ar bias·포화수심·부식성 부피·pH bias·dpH/dt** → [29 아라고나이트/칼사이트 포화도 Ω 카드], [29 pH 검증 카드]. 유도 전제는 ⑩ CO2SYS closure. 추세는 `06`(MK/Sen), 단면은 ⑤.
- **만드는 법**: **`PyCO2SYS`** 로 DIC·TA(또는 pH·pCO2)에서 Ω·포화수심 유도(Ksp Mucci 1983, 압력보정). (a)/(b) `cartopy`/`matplotlib`(**★ 지도면 `add_basemap()` 필수**). (c) 추세 `scipy.stats`/Mann–Kendall(`pymannkendall`). Ω<1 발산·순차 색맵.
- **함정·주의**: **Ω는 다단계 유도량(오차 전파 큼)·상수·압력식 차이가 포화수심 수백 m 이동** → 규약(Ksp·K1K2·pH 스케일·압력보정) 명시(§ 원칙 3, ⑩). **BGC-Argo pH 센서 편향**(pCO2 과대·흡수 과소로 전파) → 진값처럼 쓰지 말 것. total scale 통일. 추세는 다년(≥10년). (a)/(b) 지도 → basemap.
- **출처**: Mucci (1983, *American Journal of Science* 283:780–799, 아라고나이트·칼사이트 Ksp); Orr et al. (2005, *Nature* 437:681–686, 산성화·포화 감소); Feely et al. (2004, *Science* 305:362–366, CaCO3 포화·용해); Jiang et al. (2015, *GBC*, 표층 Ω 기후); Williams et al. (2017, *GBC*, SOCCOM float pH 편향).

---

### ★ 탄산계 내부정합 진단 (CO2SYS closure) (탄산계 내부정합 / Carbonate system closure diagnostic)
- **무엇을 보여주나**: 탄산계 4대 변수(DIC·TA·pH·pCO2) 중 **두 쌍**(예: DIC+TA vs pH+pCO2)으로 계산한 유도변수 값의 **잔차(내부 불일치)** 를 산점/히스토그램으로. 관측 QC·모델 정합성 척도이자, 모델-관측 탄산계 비교의 **전제 진단**.
- **읽는 법**: x=쌍1 유도 pCO2(또는 pH), y=쌍2 유도값, 1:1선. *좋은 패턴*: 잔차가 관측 불확실성(수 μatm·~0.01 pH) 내, 0 중심 무작위. *나쁜 패턴*: 계통 offset(상수 조·pH 스케일 불일치 신호 — "모델 오차"가 아니라 규약 불일치!), sea-state/해역별 부호 쏠림(저알칼리·연안·고온 상수 불확실).
- **언제 쓰나**: [병시료] GLODAP·[정점] BATS/HOT·[격자] 모델 탄산계. pH·pCO2·Ω·DIC 비교 **전** 반드시 1회.
- **짝지표 & 교차링크**: **두 쌍 유도 잔차·내부 불일치** → [29 탄산계 내부정합 검증 카드](CO2SYS/PyCO2SYS 공통 엔진). 하위 그림 ⑧ pCO2·⑨ pH/Ω의 전제. 잔차 분포는 [`16`](./16_fig_common.md) 오차 히스토그램.
- **만드는 법**: **`PyCO2SYS`** 로 동일 규약(pH total scale, K1K2 Lueker et al. 2000, KSO4·KF·total boron, T·S·P·PO4·Si 입력)으로 두 쌍 각각 유도 → 잔차 산점/히스토그램 `matplotlib`. **모델·관측 동일 규약으로 재계산**(핵심).
- **함정·주의**: **상수 조·pH 스케일·온도기준 불일치가 "모델 오차"로 오인되는 대표적 함정**(§ 원칙 3) → 규약 캡션 명시·양쪽 동일 재계산. 저알칼리·연안·고온에서 상수 불확실. 압력·온도(현장 vs 25℃) 정합. 영양염 입력 유무 명시.
- **출처**: Humphreys et al. (2022, *Geoscientific Model Development* 15:15–43, PyCO2SYS, doi:10.5194/gmd-15-15-2022, [gmd.copernicus.org](https://gmd.copernicus.org/articles/15/15/2022/)); Lewis & Wallace (1998, CO2SYS, ORNL/CDIAC); Lueker, Dickson & Keeling (2000, *Marine Chemistry* 70:105–119, K1/K2); Dickson, Sabine & Christian (2007, *Guide to Best Practices for Ocean CO2 Measurements*, PICES Special Pub. 3).

---

### ★ T–S / property–property 산점 (Redfield·TA–SSS·AOU 관계) (특성–특성 산점 / Property–property scatter: Redfield, TA–SSS, AOU)
- **무엇을 보여주나**: 두 생지화학·물리 변수의 **관계선**을 모델·관측이 함께 그린 산점 — (a) NO3 vs PO4(Redfield 기울기 ≈16), (b) TA vs SSS(보존 회귀), (c) AOU vs NO3(재광물화 화학량론), (d) O2 vs 밀도(수괴). 벌크 bias가 못 보는 **화학량론·수괴·보존관계**의 재현성을 진단.
- **읽는 법**: 점운의 **기울기·절편·산포**를 model/obs 대조. (a) N:P 기울기 이탈=질소고정/탈질 불균형(N*=NO3−16·PO4로 보조). (b) TA–SSS 기울기/절편 이탈=CaCO3 순환·담수수지 문제(nTA=TA·35/SSS로 담수효과 제거). (c) AOU–NO3 기울기=재광물화 화학량론. *나쁜 패턴*: 모델 관계선이 관측과 다른 기울기(과정 오류), 산포 과대(수괴 혼합 부실).
- **언제 쓰나**: [병시료] GLODAP·[프로파일] BGC-Argo·[격자] 모델. 화학량론·보존·수괴 진단(과정 검증). 지리축 아님 → basemap 불필요.
- **짝지표 & 교차링크**: **N:P·N\*·TA–SSS 회귀계수·AOU:NO3 기울기** → [29 영양염 카드(Redfield·N\*)], [29 전알칼리도 카드(TA–SSS)], [29 AOU 카드]. Type-II 회귀·산점은 [`16`](./16_fig_common.md). 밀도면 수괴는 T–S diagram(수온·염분 도메인 [`19`](./19_fig_temp_salinity.md)).
- **만드는 법**: `matplotlib` `ax.scatter` + Type-II 회귀(`scipy.odr`, OLS는 회귀희석). 밀도 색(`cmocean.cm.dense`). nTA·N* 등 유도량은 numpy. 수괴 구분은 밀도/depth 색.
- **함정·주의**: **유도량(N\*·nTA·AOU)은 두 변수 오차 전파** → 산포 과해석 금지. TA–SSS 선형성은 **강·해빙·연안에서 붕괴**(별도 취급). AOU는 preformed O2=포화 가정(극지·고생산 편향). OLS 기울기 회귀희석 → Type-II. nTA는 SSS 기준(35) 명시.
- **출처**: Gruber & Sarmiento (1997, *Global Biogeochem. Cycles*, N*); Lee et al. (2006, *GRL* 33:L19605, 표층 TA 경험식); Redfield (화학량론); Ito, Follows & Boyle (2004, *GRL*, preformed/AOU); Olsen et al. (2016, *ESSD* 8:297–323, GLODAPv2).

---

### ★ log 공간 QQ / PDF·CDF 비교 (로그공간 분포 비교 / Log-space QQ & PDF/CDF)
- **무엇을 보여주나**: Chl-a·영양염·NPP 등 **로그정규 변수**의 분포를 **log10 공간**에서 QQ-plot·PDF/CDF로 모델·관측 비교. 저농도(외해 빈영양) 왼쪽 꼬리·고농도(개화) 오른쪽 꼬리의 일치와 기하평균·기하표준편차·왜도 재현을 본다. (공통편 일반 QQ/PDF를 **log축·꼬리 강조**로 생지화학식 변형.)
- **읽는 법**: **QQ**: x=관측 분위수(log10), y=모델 분위수. 하단(저Chl)에서 1:1 위로 휘면 모델 저농도 과대(외해 빈영양 못 잡음, 흔한 약점), 상단(고Chl)에서 1:1 아래로 휘면 개화 과소. **PDF/CDF**: log축에서 겹칠수록 좋음, 왜도·꼬리 차이 주목. *나쁜 패턴*: 분포가 좁음(개화·저농도 극단 못 재현), 위치 이동(기하 bias).
- **언제 쓰나**: [L3/L4]·[정점]·[격자] Chl·영양염·NPP 분포·기후 검증(시간정렬 불필요). quantile mapping 보정 전후 점검.
- **짝지표 & 교차링크**: **KS·Perkins S·기하평균 GM·기하표준편차 GSD·percentile bias** → [29 로그정규분포 진단 카드(Campbell)], [29 로그공간 분포·꼬리 비교 카드]. 일반 QQ·PDF/CDF·Perkins·return-level은 [`16`](./16_fig_common.md) 승급. 분포 적합(log-normal)과 병행.
- **만드는 법**: `numpy.quantile(np.log10(x), p)`(공통 확률격자, 꼬리 조밀) → `ax.scatter`+1:1. PDF `scipy.stats.gaussian_kde`(log값)·CDF `np.sort`. GM=`10**np.mean(np.log10(x))`, GSD=`10**np.std(...)`. 표본 적은 꼬리 분위수는 부트스트랩 CI 띠.
- **함정·주의**: **선형 QQ/PDF는 로그정규 변수 성능을 오판**(고농도 지배) → log 공간 필수(§ 원칙 2). **분포만 비교 → 동시(시간) 일치는 못 봄**(상관 0이어도 QQ 완벽 가능) → ①/④와 3축. 0·음수·결측 처리(log 전 clip/제거). 이질 수괴 혼합 시 로그정규 약화(수괴별 분리, Campbell). 꼬리 분위수 표본 적음→CI.
- **출처**: Campbell (1995, *JGR Oceans* 100(C7):13237–13254, 로그정규); Seegers et al. (2018, *Optics Express* 26(6):7404–7422, [opg.optica.org](https://opg.optica.org/oe/fulltext.cfm?uri=oe-26-6-7404)); Wilks(교과서, QQ·분포검정 — [`16`](./16_fig_common.md) 공통); Perkins et al. (2007, *J. Climate* 20:4356–4376, PDF skill, doi:10.1175/JCLI4253.1).

---

### ★ 순1차생산 NPP 검증 (알고리즘 envelope 산점) (순1차생산 검증 / Net primary production: algorithm-envelope scatter)
- **무엇을 보여주나**: 모델 순1차생산(NPP, mg C m⁻² d⁻¹)을 **여러 위성 NPP 알고리즘**(VGPM·Eppley-VGPM·CbPM)·현장 ¹⁴C 정점(BATS/HOT/CARIACO)과 비교하되, 단일 위성값이 아닌 **알고리즘 범위(envelope)** 대비로 산점/시계열. 생태계 탄소흐름의 핵심량(단, 위성 NPP 자체가 불확실).
- **읽는 법**: 산점(log 권장) x=위성/현장 NPP, y=모델; 회색 띠=알고리즘 envelope(VGPM~CbPM 범위). *좋은 패턴*: 모델이 envelope 안, 위도대·계절 적분생산 일치. *나쁜 패턴*: envelope 밖 계통편차, 극지·고생산 과대/과소. 전지구 총량은 30~70 Gt C/yr 폭(알고리즘 산포 큼) → 단일값 합격 판정 금지.
- **언제 쓰나**: [L3/L4] 위성 NPP vs [격자] 모델; [정점] ¹⁴C vs 위성/모델. 계절·위도대·해역대 적분생산.
- **짝지표 & 교차링크**: **연직적분 NPP bias·RMSE·log 통계·적분생산** → [29 순1차생산 NPP 카드], [29 수출생산·POC 플럭스 카드]. log 산점은 ①, 분포는 ⑫. 지도면 basemap.
- **만드는 법**: VGPM/CbPM 산물(Oregon State Ocean Productivity) 로드 → `xarray` 콜로케이션(§15) → `matplotlib` 산점(log)·envelope `fill_between`. 정의(부피 vs 연직적분·일 vs 연) 통일. 지도는 `add_basemap`.
- **함정·주의**: **위성 NPP 알고리즘 불확실성이 매우 큼**(§G-1) → **단일 위성 NPP를 기준삼아 합격 판정 금지**, envelope 대비. VGPM 고생산·극지 편향, CbPM 후방산란 가정 의존. ¹⁴C 정점은 배양법·기간 차이. log 공간(NPP 광범위 분포).
- **출처**: Behrenfeld & Falkowski (1997, *L&O* 42(1):1–20, VGPM); Behrenfeld et al. (2005, *GBC* 19:GB1006, CbPM); Carr et al. (2006, *Deep-Sea Res. II* 53:741–770, NPP 모델 상호비교); Saba et al. (2011, *Biogeosciences*, NPP 모델-현장 비교).

---

### 식물플랑크톤 PFT·크기분율 검증 (군집 구조 / Phytoplankton functional type & size-class validation)
- **무엇을 보여주나**: 모델 식물플랑크톤 기능형군(PFT: 규조·와편모·남세균·피코)·크기분율(micro/nano/pico)을 위성 PFT·HPLC 색소(CHEMTAX) 관측과 비교 — (a) 그룹별 Chl 분율 지도, (b) 우점군 **혼동행렬**, (c) 크기분율 vs 총Chl 관계. 벌크 Chl이 숨기는 군집 구조 검증.
- **읽는 법**: (a) 분율(0~1) 지도 model/obs. (b) 혼동행렬: 대각선 강함=우점군 일치, 비대각=혼동(예 규조↔피코). (c) 분율-Chl 관계선 이탈=크기구조 오류. *좋은 패턴*: 우점군·크기구조의 위도·계절 패턴 일치. *나쁜 패턴*: 모델 규조 과대(고위도), 피코 과소(gyre).
- **언제 쓰나**: [L3] 위성 PFT·[정점] HPLC vs [격자] 모델 그룹 Chl. 군집 구조 진단.
- **짝지표 & 교차링크**: **분율 MAE·우점군 일치율·혼동행렬** → [29 식물플랑크톤 기능형군 PFT 카드]. 혼동행렬·범주형은 [`16`](./16_fig_common.md) 성능 다이어그램·[`03`], 분율 지도는 basemap.
- **만드는 법**: 분율 지도 `cartopy` `pcolormesh`(**★ `add_basemap()` 필수**). 혼동행렬 `sklearn.metrics.confusion_matrix`+`seaborn.heatmap`. PFT 정의(크기 vs 분류군) **매핑 명시**(모델·위성 다름).
- **함정·주의**: **위성 PFT는 Chl에서 통계추정(불확실 큼, §G-1)**. 모델 그룹 수·정의가 관측과 불일치 → 정의 매핑 명시, 직접 비교 곤란. HPLC-CHEMTAX 가정 의존. (a) 지도 → basemap.
- **출처**: Bracher et al. (2017, *Frontiers in Marine Science*, PFT 원격탐사 리뷰); Hirata et al. (2011, *Biogeosciences*, size class from ocean colour); Mackey et al. (1996, *MEPS*, CHEMTAX).

---

### ★ 생지화학 다변수 스킬 요약 (Target/Taylor/cost-function 히트맵) (다변수 스킬 요약 / Multi-variable BGC skill summary)
- **무엇을 보여주나**: 여러 생지화학 변수(Chl·NO3·PO4·O2·DIC·pCO2·pH 등)를 **공통 스킬지표 세트**로 요약해 모델 전반의 성능·편향을 한 도표에 — (a) 다변수 **Target diagram**(bias vs unbiased-RMSD), (b) 다변수 **Taylor diagram**, (c) 변수×지표 **cost-function/스킬 히트맵**(Stow 2009 RI·MEF·CF). 커플드 물리-생지화학 모델 평가의 관행틀.
- **읽는 법**: (a) Target: 각 변수 점이 원점 근접=양호(사분면으로 bias+분산 유형). (b) Taylor: REF 근접=양호. (c) 히트맵: 행=변수, 열=지표(CF·MEF·RI·log-bias), 색=값(CF 작을수록·MEF 클수록 양호). *좋은 패턴*: 대부분 변수 원점/REF 근접. *나쁜 패턴*: 특정 변수(흔히 심층 O2·pCO2·규산) 크게 이탈.
- **언제 쓰나**: 다변수·다지점 [격자]/[정점]/[프로파일] 종합. 모델 버전·튜닝 비교, 리포트 요약 1장. 지리축 아님 → basemap 불필요.
- **짝지표 & 교차링크**: **Stow RI·MEF·CF·AE(bias)·상관 + Target(bias vs uRMSD)·Taylor** → [29 생지화학 모델 스킬 종합틀(Stow 2009) 카드]. Target·Taylor 본체는 [`16`](./16_fig_common.md)(공통, 여기선 다변수 적용·교차링크만). log 변수는 log 공간 스킬.
- **만드는 법**: Target/Taylor는 `skill_metrics`(`sm.target_diagram`·`sm.taylor_diagram`); 통계는 `xskillscore`/numpy(변수별 정규화 ÷σ_obs·log 변환). 히트맵 `matplotlib.pcolormesh`/`seaborn.heatmap`. CF=(1/N)Σ|M−O|/σ_obs 등 **정의 명시**.
- **함정·주의**: **단일 스킬점수로 순위 확정 금지**(§G-6, 다축·유의성 동반). **Stow 등급(CF<1·MEF>0)은 advisory**(변수·해역·해상도·기준자료 의존, good 자동판정 금지). **Target diagram은 bias는 보이나 분포·꼬리 무관**, Taylor는 bias 못 봄 → 병행. log/선형 공간 혼용 주의. 변수별 정규화 기준 통일.
- **출처**: Stow et al. (2009, *J. Marine Systems* 76:4–15, skill assessment); Jolliff et al. (2009, *J. Marine Systems* 76:64–82, target diagram, doi:10.1016/j.jmarsys.2008.05.014); Doney et al. (2009, *J. Marine Systems* 76:95–112, upper-ocean ecosystem-BGC skill); Allen et al. (2007, *J. Marine Systems*, 운영 BGC 스킬).

---

### 경보·임계 사건 검증 (HAB/저산소/저Ω 초과) (임계 사건 검증 / Threshold-event verification: HAB / hypoxia / corrosive)
- **무엇을 보여주나**: 생지화학 임계 초과 사건 — **녹조(HAB: Chl>임계)·저산소(hypoxia: O2<임계)·부식성(corrosive: Ω_ar<1)** — 을 모델이 관측과 일치시키는지 이진 범주 검증. 성능 다이어그램(POD·SR·CSI·bias)·사건 지도·시계열로.
- **읽는 법**: **성능 다이어그램**([`16`](./16_fig_common.md)): x=SR(=1−FAR), y=POD, CSI 등치선·bias 방사선; 우상단·대각선(bias=1) 근접=양호. **사건 지도**: hit/miss/false-alarm 색칠(발산 아님, 범주색). *나쁜 패턴*: 저산소 miss 다발(모델 O2 과대), HAB false alarm(연안 Chl 과대), bias 1에서 크게 이탈.
- **언제 쓰나**: [격자]/[정점]/[L3] 임계 이진화. 경보·위험 관점(연안 저산소·적조·산성화 부식성).
- **짝지표 & 교차링크**: **POD·FAR·SR·CSI·FBI·SEDI(드문사건)** → [29 경보·임계 사건 검증 카드]. 성능 다이어그램·ROC·reliability는 [`16`](./16_fig_common.md), `03`·`14`. OMZ 부피는 ⑦, Ω는 ⑨.
- **만드는 법**: 임계 이진화 후 a,b,c,d 집계(numpy/`xskillscore`) → 성능 다이어그램 `matplotlib`(CSI 등치선). 사건 지도 `cartopy`(**★ `add_basemap()` 필수**, 범주 색). 부트스트랩 CI.
- **함정·주의**: **드문 사건은 단일지표(PC) 오도**(항상 'no'로 높음) → CSI·SEDI 병행. **임계·사건빈도 의존** → 임계 스캔·정의 명시(§G-4). 격자 자기상관으로 유효표본 과대 → 부트스트랩 CI. 위성 Chl/센서 O2 기준 오차 포함(사건이 관측 기준자료 정의에 민감). 사건 지도 → basemap.
- **출처**: Roebber (2009, *Wea. Forecasting* 24:601–608, 성능 다이어그램, doi:10.1175/2008WAF2222159.1); Jolliffe & Stephenson, *Forecast Verification*; Feely et al. (2004, *Science* 305:362–366, 부식성); Cabré et al. (2015, *Biogeosciences* 12:5429, 저산소).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 29(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 29(및 타 파일) 교차링크 |
|---|---|---|---|---|---|
| 1 | 로그-로그 Chl-a 매치업 산점 + MdSA box | L3/L4·정점·병시료 | 정확도+편향(log) | log-bias·log-RMSD·MdSA·기하bias비·Type-II slope·R | 29 엽록소로그·해색밴드비·매치업 · (16 밀도산점/Taylor) |
| 2 | 표층 Chl-a 지도 (log 색, basemap) | 격자·L3/L4 | 패턴(공간분포) | 격자 log-bias·R·MdSA | 29 위성vs모델 Chl공간 · 16 bias/ACC |
| 3 | Chl log-bias/log-RMSD 공간 지도 | 격자·L3/L4 | 편향+패턴(공간) | 격자 log-bias·log-RMSD·MdSA·R | 29 Chl공간·기후격자비교 · 16·02·15 |
| 4 | Chl 계절주기·개화 phenology 곡선 | L3/L4·정점·격자 | 위상+진폭(시간) | 진폭·위상·개화 개시일·기간 | 29 계절주기·개화 · 05/06 · 16 시계열 |
| 5 | 위도-깊이 단면 (O2/영양염/DIC) | 프로파일·격자 | 패턴(심층구조) | 깊이별 bias·약층심도·등밀도값 | 29 프로파일·단면·O2·영양염·DIC · 16 Taylor |
| 6 | BGC-Argo 연직 프로파일 비교 (+지도) | 프로파일·격자 | 정확도+구조(프로파일) | 깊이별 bias·DCM·float 편향 | 29 BGC-Argo·적분재고·약층 · plotting_maps §C |
| 7 | 산소최소층(OMZ) 진단 | 격자·프로파일 | 패턴+재고(저산소) | 저산소 부피·코어수심·최소O2·면적 | 29 OMZ·O2·AOU · ⑤·⑯ |
| 8 | 표층 pCO2/ΔpCO2 지도 (SOCAT) | 트랙/병시료·격자 | 정확도+패턴(탄소) | ΔpCO2·bias·RMSE·계절진폭·플럭스 | 29 pCO2 · 12 매치업 · 15 |
| 9 | pH/아라고나이트 Ω 진단 | 병시료·정점·프로파일·격자 | 편향+추세+수직(산성화) | Ω_ar bias·포화수심·부식성부피·pH bias·dpH/dt | 29 Ω·pH · ⑩ closure · 06 추세 · ⑤ |
| 10 | 탄산계 내부정합 (CO2SYS closure) | 병시료·정점·격자 | 정합성(전제) | 두 쌍 유도 잔차·내부 불일치 | 29 탄산계 내부정합 · 16 오차 히스토그램 |
| 11 | property–property 산점 (Redfield/TA–SSS/AOU) | 병시료·프로파일·격자 | 패턴(화학량론·보존) | N:P·N\*·TA–SSS 회귀·AOU:NO3 | 29 영양염·TA·AOU · 16 산점·Type-II · 19 T–S |
| 12 | log 공간 QQ / PDF·CDF | L3/L4·정점·격자 | 분포·꼬리(log) | KS·Perkins S·GM·GSD·percentile bias | 29 로그정규·로그공간분포 · 16 QQ/PDF |
| 13 | NPP 검증 (알고리즘 envelope 산점) | L3/L4·정점·격자 | 정확도(생산, envelope) | 적분NPP bias·RMSE·log 통계 | 29 NPP·수출생산 · ①·⑫ |
| 14 | PFT·크기분율 검증 | L3·정점·격자 | 패턴(군집) | 분율 MAE·우점군 일치율·혼동행렬 | 29 PFT · 16 성능다이어그램·03 |
| 15 | 다변수 스킬 요약 (Target/Taylor/히트맵) | 다변수 격자/정점/프로파일 | 종합요약 | Stow RI·MEF·CF·bias + Target·Taylor | 29 Stow 종합틀 · 16 Target/Taylor |
| 16 | 경보·임계 사건 (HAB/저산소/저Ω) | 격자·정점·L3 | 범주형 사건 | POD·FAR·SR·CSI·FBI·SEDI | 29 경보·임계사건 · 16 성능다이어그램·03·14 · ⑦·⑨ |

> **묶음 권고**: 단일 그림 금지 원칙(§G-5)에 따라 생지화학 검증 보고는 최소 **①(log 정확도+편향) + ③(공간 bias 지도) + ⑫(log 분포)** 3장을 기본 세트로, 심층·수직이 중요하면 **⑤/⑥/⑦**, 탄소계면 **⑧/⑨/⑩(+⑪)**, 생산·군집이면 **⑬/⑭**, 종합요약은 **⑮**, 경보 관점이면 **⑯**을 추가한다. **모든 지도형(②③⑦⑧⑨⑬⑭⑯)은 `add_basemap()`으로 해안선·위경도 라벨 필수**, 정점/프로파일(⑥)은 위치 지도+마커+ID. 모든 임계(±35% Chl·CF<1·−0.02 pH/decade 등)는 **advisory + 영역·계절·수형 의존 경고**로 캡션에 단다. **탄산계 비교는 ⑩ closure로 규약 통일 후**.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·QQ·KS·회귀·분포 등 표준 시각화 — [`16`](./16_fig_common.md) 공통).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (범주·확률·ROC).
- Sarmiento & Gruber (2006) *Ocean Biogeochemical Dynamics*, Princeton (표준 교과서, 확인요 — 판본별 페이지).
- Dickson, Sabine & Christian (2007) *Guide to Best Practices for Ocean CO2 Measurements*, PICES Special Pub. 3 (탄산계 규약·상수).

**학술 논문 (제목·저널·연도 웹 확인)**
- Campbell (1995) "The lognormal distribution as a model for bio-optical variability in the sea," *JGR Oceans* 100(C7):13237–13254. (로그정규)
- Bailey & Werdell (2006) "A multi-sensor approach for the on-orbit validation of ocean color satellite data products," *Remote Sensing of Environment* 102(1–2):12–23. (매치업 프로토콜)
- Seegers et al. (2018) "Performance metrics for the assessment of satellite data products: an ocean color case study," *Optics Express* 26(6):7404–7422. (MdSA)
- Stow et al. (2009) "Skill assessment for coupled biological/physical models of marine systems," *J. Marine Systems* 76:4–15.
- Jolliff et al. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment," *J. Marine Systems* 76:64–82. (doi:10.1016/j.jmarsys.2008.05.014, target diagram)
- Doney et al. (2009) "Skill metrics for confronting global upper ocean ecosystem-biogeochemistry models," *J. Marine Systems* 76:95–112.
- Bakker et al. (2016) "A multi-decade record of high-quality fCO2 data in version 3 of the Surface Ocean CO2 Atlas (SOCAT)," *ESSD* 8:383–413. (doi:10.5194/essd-8-383-2016)
- Takahashi et al. (2009) "Climatological mean and decadal change in surface ocean pCO2, and net sea–air CO2 flux," *Deep-Sea Research II* 56:554–577.
- Wanninkhof (2014) "Relationship between wind speed and gas exchange over the ocean revisited," *L&O Methods* 12:351–362.
- Humphreys et al. (2022) "PyCO2SYS v1.8: marine carbonate system calculations in Python," *Geoscientific Model Development* 15:15–43. (doi:10.5194/gmd-15-15-2022)
- Lueker, Dickson & Keeling (2000) "Ocean pCO2 calculated from DIC, TA, and the K1 and K2 ...," *Marine Chemistry* 70:105–119.
- Mucci (1983) "The solubility of calcite and aragonite in seawater ...," *American Journal of Science* 283:780–799. (Ksp)
- Orr et al. (2005) "Anthropogenic ocean acidification over the twenty-first century ...," *Nature* 437:681–686.
- Feely et al. (2004) "Impact of anthropogenic CO2 on the CaCO3 system in the oceans," *Science* 305:362–366.
- Cabré et al. (2015) "Consistent global responses of marine ecosystems to future climate change across the IPCC AR5 ... (CMIP5 OMZ)," *Biogeosciences* 12:5429.
- Behrenfeld & Falkowski (1997) "Photosynthetic rates derived from satellite-based chlorophyll concentration (VGPM)," *L&O* 42(1):1–20.
- Behrenfeld et al. (2005) "Carbon-based ocean productivity and phytoplankton physiology from space (CbPM)," *GBC* 19:GB1006.
- Carr et al. (2006) "A comparison of global estimates of marine primary production ...," *Deep-Sea Res. II* 53:741–770.
- Claustre, Johnson & Takeshita (2020) "Observing the global ocean with Biogeochemical-Argo," *Annual Review of Marine Science* 12:23–48.
- Cornec et al. (2021) "Deep chlorophyll maxima in the global ocean (BGC-Argo)," *GBC*.
- Racault et al. (2012) "Phytoplankton phenology in the global ocean," *Ecological Indicators*.
- Siegel et al. (2002) "The North Atlantic spring phytoplankton bloom and Sverdrup's critical depth hypothesis," *Science* 296:730–733.
- Gruber & Sarmiento (1997) "Global patterns of marine nitrogen fixation and denitrification (N*)," *Global Biogeochem. Cycles*.
- Lee et al. (2006) "Global relationships of total alkalinity with salinity and temperature ...," *GRL* 33:L19605.
- Olsen et al. (2016) "The Global Ocean Data Analysis Project version 2 (GLODAPv2)," *ESSD* 8:297–323.
- Hirata et al. (2011) "Synoptic relationships between surface Chl-a and diagnostic pigments (size class)," *Biogeosciences*.
- Bracher et al. (2017) "Obtaining phytoplankton diversity from ocean color: a review," *Frontiers in Marine Science*.
- Roebber (2009) "Visualizing Multiple Measures of Forecast Quality," *Wea. Forecasting* 24:601–608. (doi:10.1175/2008WAF2222159.1)
- Séférian et al. (2020) "Tracking improvement in simulated marine biogeochemistry (CMIP6)," *Current Climate Change Reports*.

**기관 자료·기술보고 (실재)**
- SOCAT: https://www.socat.info ; Bakker et al. (2016) ESSD 8:383–413.
- ESA Ocean Colour CCI (OC-CCI): Sathyendranath et al. 산출물 문서 (https://www.oceancolour.org).
- NASA OBPG ocean colour validation / performance metrics: https://oceancolor.gsfc.nasa.gov.
- Oregon State Ocean Productivity (VGPM/CbPM NPP 산물): http://sites.science.oregonstate.edu/ocean.productivity.
- World Ocean Atlas (WOA, O2·영양염 기후값), GLODAPv2 (탄소계) — NOAA NCEI.

**소프트웨어 (실존 도구)**
- `PyCO2SYS` — 탄산계 유도·Ω·포화수심(Humphreys et al. 2022, doi:10.5194/gmd-15-15-2022): https://pyco2sys.readthedocs.io.
- `argopy` — BGC-Argo 접근/QC: https://euroargodev.github.io/argopy.
- `cmocean` — 해양 색맵(`algae`/`oxy`/`balance`/`dense`/`deep`/`tempo`/`matter`): Thyng et al. (2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66).
- `skill_metrics`(SkillMetrics: `sm.target_diagram`/`sm.taylor_diagram`), `xskillscore`, `xesmf`(재격자), `cartopy`(지도), `matplotlib`, `numpy`, `scipy`(odr·stats), `pandas`/`xarray`, `seaborn`(히트맵), `sklearn`(confusion_matrix), `pymannkendall`(추세).
- 지도 basemap 헬퍼 `add_basemap()` → [`plotting_maps.md`](../../plotting_maps.md) (해안선/육지+위경도 라벨, cartopy+오프라인 fallback).

**확인요 (확정 인용 금지 — §G-6)**
- Sarmiento & Gruber (2006) 교과서 — 판본별 페이지 상이(확인요, DOI 없음).
- Williams et al. (2017, *GBC*, SOCCOM float pH 편향) — 권·페이지 재확인 안 함(확인요).
- Séférian et al. (2020, *Current Climate Change Reports*) — 권·페이지 미확정(확인요).
- 해석 임계(위성 Chl ±35%≈0.35 log10, pH −0.02/decade, Stow CF<1·MEF>0, 저산소 60/20/5 μmol kg⁻¹, HAB Chl 임계 등)는 **관행 advisory** — 해역(Case-1/Case-2)·수형·계절·센서·알고리즘 의존(§G-4).
- 위성 NPP 전지구 총량 30~70 Gt C/yr 폭·알고리즘 산포 — 검증 기준 아님, envelope 대비(§G-1).
