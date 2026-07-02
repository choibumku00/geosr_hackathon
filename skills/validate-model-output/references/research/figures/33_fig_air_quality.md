# 33. 검증 시각화 카탈로그 — 대기질·대기화학편 (Verification Figures: Air Quality / Atmospheric Chemistry)

이 문서는 화학수송모델(CTM: CMAQ, CAMx, WRF-Chem, GEOS-Chem, CAM-chem, CHIMERE, SILAM 등)·배출/확산 모델의 대기질 산출물(PM2.5·PM10·O3·NO2·SO2·CO·AOD 및 PM 화학종)을 **지상 측정소(in-situ)·위성 컬럼(satellite column)·재분석(CAMS, MERRA-2 aerosol 등)** 과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 대기질 도메인편이다. 메서드(수치지표) 카드는 [`25_domain_air_quality.md`](../25_domain_air_quality.md)에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **대응 메서드카탈로그: `25_domain_air_quality.md`** — 각 그림 카드의 "짝지표 & 교차링크"는 25번 카드의 방법과 짝지어진다.

> **공통/횡단 그림과의 분담**: Taylor·Target(일반)·QQ·ROC·reliability·rank histogram·Brier/CRPS 분해·performance(Roebber) diagram·bias map 골격 등 **도메인 무관 요약그림은 [공통편] [`16_fig_common.md`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않고 **교차링크**만 한다. 이 파일은 **대기질 고유 그림**(로그-로그 산점+FAC2 보조선, MFB/MFE bugle plot, 초과사건 performance diagram, 위성 NO2/AOD 컬럼 지도, 일변동·주말효과 합성, PM speciation box, FAIRMODE soccer/target 등)과 **공통 그림의 대기질식 변형**(로그축·꼬리 강조 QQ, bias 부호를 종별로 얹은 target 등)에 집중한다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석) · [시계열]=측정소 CSV/텍스트 · [트랙/타일]=위성 L2 swath / L3 gridded · [프로파일]=연직/컬럼 · [화학종]=PM speciation(SO4²⁻/NO3⁻/NH4⁺/OC/EC 등).

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 측정소·위성(TROPOMI/MODIS)·CAMS/MERRA-2는 모두 reference이지 truth가 아니다. 축·범례·캡션에 "모델 − 기준(reference)"으로 쓰고, 특히 **위성 컬럼·재분석을 "정답"으로 단정 금지**(위성 자체 편향·AMF·구름 처리 오차 큼).
> 2. **측정소는 점(point) 관측.** 격자(수~수십 km) 평균과 비교하면 **대표성 오차(representativeness error)** 가 섞인다 — 도로변(traffic)·산업 측정소의 "과소"는 모델 결함이 아니라 대표성일 수 있다(측정소 유형 층화 필수).
> 3. **농도는 로그정규(우측 꼬리).** 선형 산점·bias는 소수 고농도가 지배 → **로그축·MFB/MFE·FAC2** 를 기본으로. (단, **오존은 로그정규가 약해** 선형·NMB가 관례.)
> 4. **해석 임계는 advisory.** Boylan&Russell(2006) MFB±30/±60%·MFE 50/75%, Emery(2017) O3 NMB±5/±15%, FAC2≥0.5, FAIRMODE MQI≤1 등은 **미국/유럽 사례 기반 참고선**이며 지역·화학종·해상도·계절 의존. 그림에 "good/bad"를 단정하지 말고 캡션에 영역의존 경고.
> 5. **단일 그림 금지.** 산점(정확도) 하나로 결론내지 말고 최소 **정확도+편향+분포/사건** (예: 로그산점 + MFB/MFE bugle + QQ + 초과사건 performance) 다축과 유의성(부트스트랩 CI)을 함께 낸다. **총 PM2.5가 맞아도 성분 상쇄**로 우연일 수 있으니 speciation 병행.
> 6. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문 도판을 그대로 재현하지 않는다. 예시 이미지는 우리 데이터로 직접 렌더링.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **농도 로그-로그 산점도 + FAC2 보조선** — 대기질 검증의 1차 대표 그림(로그정규)
2. ★ **측정소 위치 지도 (basemap + 마커 + ID + 유형색)** — "어디서 검증했나"
3. ★ **MFB / MFE bugle 플롯 (Boylan & Russell)** — 농도 의존 목표/기준선 대비 성능
4. ★ **초과사건 performance diagram (Roebber) + 임계 스캔** — 경보/기준 초과 검증
5. ★ **일변동 합성 플롯 (diurnal cycle) + bias 패널** — 시간대별 진폭·위상
6. **주말효과·주간주기 플롯 (weekend effect)** — 요일 배출·오존 생성체제
7. ★ **soccer / target 플롯 (FAIRMODE MQI, 대기질 target)** — 다지점·다종 편향+산포 요약
8. ★ **농도 QQ-plot (로그축·고농도 꼬리 강조)** — 분포·고오염사건 재현
9. ★ **위성 대류권 NO2 컬럼 지도 (모델 vs 위성 vs 차)** — 배출·화학 광역 검증
10. ★ **위성/AERONET AOD 매치업 (산점 + within-EE envelope)** — 에어로졸 총량
11. ★ **PM 화학종 stacked bar / box plot (speciation)** — 성분별 bias·상쇄 은폐 진단
12. ★ **측정소 유형별 box plot (urban/traffic/rural/background)** — 유형 층화 성능
13. **model–obs 시계열 overlay + 잔차 패널** — 사건·위상·계통 offset 진단
14. ★ **재분석 격자 bias/difference 지도 (CAMS/MERRA-2)** — 면적 계통오차 위치
15. **계절·월별 층화 성능 히트맵 (seasonal stratification)** — 계절 의존 오차 분해
16. **오존 생성체제 진단 지도 (HCHO/NO2 = FNR)** — NOx- vs VOC-limited

---

### ★ 농도 로그-로그 산점도 + FAC2 보조선 (농도 로그산점도 / Concentration log–log scatter with FAC2 guide lines)
- **무엇을 보여주나**: 매치업된 (관측 농도, 모델 농도) 쌍을 **양대수(log–log) 축**에 산점하고, 1:1선 + **FAC2 보조선(y=2x, y=0.5x)** + 회귀·핵심 스칼라(bias·NMB·NME·MFB·FAC2·r·N)를 얹은 대기질 검증의 **표준 1장**. 로그정규 농도의 곱셈적 관계와 저~고농도 전 구간을 한 화면에.
- **읽는 법**: x=관측(측정소/위성/재분석), y=모델, **양축 로그**. **1:1선**(점선)이 기준, **FAC2 밴드**(±factor 2, y=2x·y=0.5x 두 선) 안에 든 점 비율이 FAC2. 점운이 밴드 안에 좁게 밀착하면 양호. *나쁜 패턴*: 저농도역에서 점이 위로 벌어짐(모델 배경 과대), 고농도역에서 1:1 아래로 휨(고오염사건 과소 — 흔한 약점), 부채꼴 산포(랜덤오차 큼). 텍스트 box에 MFB·NMB·FAC2·r·N.
- **언제 쓰나**: [시계열]/[격자]/[트랙] 어디서나, PM2.5·PM10·NO2·SO2·CO·AOD 등 **로그정규 농도**. 정확도+편향 1차 점검. (오존은 로그정규 약함 → 선형축 산점 병행.)
- **짝지표 & 교차링크**: **FAC2·MFB/MFE·NMB/NME·log-bias·r** → [`25` FAC2/MFB·MFE/NMB·NME/로그공간 카드]. 산점 골격·회귀희석은 공통 [`figures/16` 산점도·밀도산점]. 분포는 ⑧ QQ, 편향 요약은 ③ bugle·⑦ target.
- **만드는 법**: `matplotlib` `ax.scatter` + `ax.set_xscale('log')`/`set_yscale('log')`; N 크면 `ax.hexbin(bins='log')`. 1:1 `ax.axline((1,1),slope=1)`(로그축), FAC2선은 `ax.plot([lo,hi],[2*lo,2*hi])`·`[0.5*lo,0.5*hi]`. 축 동일 범위·`set_aspect('equal')`. 지표는 25 정의식으로 직접 계산. 0/검출한계는 LOD/2 대입 또는 제거(규칙 캡션 명시).
- **함정·주의**: **0·음수·검출한계 처리 규칙이 로그축·FAC2를 좌우**(반드시 명시). OLS는 관측 무오차 가정 → 두 자료 모두 오차인 대기질에선 편향(회귀희석) → robust/직교회귀 병행(§16). FAC2는 편향 방향을 못 봄 → MFB 병행. 측정소 대표성오차가 산포에 포함(모델 탓 단정 금지). §G-5.
- **출처**: Chang & Hanna (2004, *Meteorol. Atmos. Phys.* 87:167–196, doi:10.1007/s00703-003-0070-7, FAC2·로그공간); Seinfeld & Pandis, *Atmospheric Chemistry and Physics* (Wiley, 로그정규 농도 분포); Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·회귀).

---

### ★ 측정소 위치 지도 (측정소 위치도 / Monitoring-station location map with basemap + markers + IDs)
- **무엇을 보여주나**: 검증에 쓴 지상 측정소를 **해안선/육지 basemap 위 마커**로 찍고 **측정소 ID·유형(도시배경/교통/산업/농촌배경)** 을 색·기호로 구분한 위치도. "검증 결과가 **어느 지점·어떤 환경**에서 나온 것인가"를 통계와 직접 연결하는 필수 그림. 마커 색을 종별 bias·성능으로 칠하면 "성능 지도"로 확장.
- **읽는 법**: x=경도, y=위도, **해안선+육지+위경도 라벨** 위 마커. 색/기호=측정소 유형(예: 파랑=배경, 빨강=교통, 세모=산업). 마커 옆 **ID 라벨**. *읽기*: 교통·산업 측정소가 광역격자와 겹치는지(대표성), 측정소가 도시에 편중돼 배경 커버가 빈약한지, (성능색 버전) 특정 도시권에 과소 bias가 몰리는지.
- **언제 쓰나**: [시계열] 다지점 검증의 **개요 그림**. 모든 대기질 검증 보고의 서두. 유형 층화(⑫)·대표성(§25) 해석의 지리적 근거.
- **짝지표 & 교차링크**: 측정소 **유형 층화·대표성 오차** → [`25` 측정소 대표성/유형 층화 카드]. 지도 규칙은 [`plotting_maps.md`]. 격자 bias 지도는 ⑭. 유형별 통계 분포는 ⑫ box.
- **만드는 법**: **`plotting_maps.md`의 `add_basemap(ax, lon, lat)` 사용 필수**(cartopy `ccrs.PlateCarree()` GeoAxes) — 해안선/육지+위경도 라벨. 마커 `ax.scatter(lon, lat, c=type_color, transform=ccrs.PlateCarree())`, ID는 `ax.annotate`(약간 offset). 확대 군집은 `add_basemap`이 span으로 `10m` 해안선 자동 선택. 지역 맥락 인셋(`ax.inset_axes`+`add_basemap`) 권장.
- **함정·주의**: **★ 지도형(위경도) 그림 — 해안선/육지+위경도 라벨 필수(`add_basemap`).** 없으면 위치 식별 불가. **경도 규약(0–360 vs −180–180) 불일치**로 마커가 화면 밖(`lon=((lon+180)%360)-180` 변환). 연안 확대에 거친 해안선(`110m`)이면 육/해 구분 불가 → `10m`. 측정소 밀집 시 ID 라벨 겹침(우선순위·리더선). 유형 메타데이터 오류·국가별 분류 규약 차이 명시.
- **출처**: [`plotting_maps.md`] (add_basemap·정점 위치도 규칙); Cartopy Feature interface (scitools.org.uk/cartopy); EEA AirBase/AQ e-Reporting 측정소 분류; Janssen et al. (2008, *Atmospheric Environment*, 측정소 대표성 지도).

---

### ★ MFB / MFE bugle 플롯 (분수편향·오차 bugle 플롯 / MFB & MFE "bugle" plots, Boylan & Russell)
- **무엇을 보여주나**: 측정소(또는 시각)별 **분수편향 MFB·분수오차 MFE** 를 **관측 농도(x)** 에 대해 산점하고, **Boylan & Russell(2006)의 농도 의존 목표(goal)·기준(criteria) 곡선**(나팔=bugle 모양)을 겹친 PM 성능 등급 그림. 저농도에서 기준선이 벌어지는 "나팔" 형상이라 bugle plot.
- **읽는 법**: x=관측 농도(µg/m³, 보통 로그), y=MFB(위)·MFE(아래) [%]. **안쪽 곡선=goal(MFB ±30%, MFE 50%), 바깥 곡선=criteria(MFB ±60%, MFE 75%)**, 저농도(≤~2 µg/m³)로 갈수록 완화(벌어짐). 점이 goal 안=우수, criteria 안=수용 가능, 밖=미달. *읽기*: 점이 위(MFB>0)로 몰리면 과대, 아래로 몰리면 과소; 고농도역에서 criteria 밖으로 이탈하면 고오염 재현 실패. 화학종별 색.
- **언제 쓰나**: [시계열]/[격자] PM2.5·PM10 총질량 및 **화학종별**(SO4/NO3/NH4/OC/EC), 광소멸(bext). 규제·정책 PM 성능평가의 표준.
- **짝지표 & 교차링크**: **MFB·MFE + 농도 의존 goal/criteria** → [`25` MFB/MFE·Boylan&Russell 카드]. 편향 요약은 ⑦ target, 성분 상쇄는 ⑪ speciation. NMB/NME 벤치마크(오존)는 ⑦/텍스트표.
- **만드는 법**: MFB=(2/N)Σ(mᵢ−oᵢ)/(mᵢ+oᵢ)·MFE=(2/N)Σ|mᵢ−oᵢ|/(mᵢ+oᵢ)를 측정소별 계산(`numpy`); `matplotlib` 2-패널 산점 + goal/criteria 곡선(Boylan&Russell 농도 완화식 직접 구현, `ax.plot`으로 상·하한). 로그 x축. 화학종별 마커/색.
- **함정·주의**: **목표/기준선은 pass/fail 시험이 아니라 참고선**(§G-4) — "criteria 안이니 검증됨" 식 오용 금지. **미국 사례 기반**이라 한국·타 지역 전이 시 재보정·맥락화. **저농도 완화식·최소농도 컷 정의**가 등급을 좌우(명시). 총질량만 보면 성분 상쇄 은폐(⑪ 병행). 질산염·유기탄소는 목표 미달이 흔함.
- **출처**: Boylan & Russell (2006, *Atmospheric Environment* 40(26):4946–4959, "PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models"); Simon, Baker & Phillips (2012, *Atmospheric Environment* 61:124, 성분별 성능 통계 편람).

---

### ★ 초과사건 performance diagram (초과사건 성능도표 / Exceedance performance diagram, Roebber, with threshold scan)
- **무엇을 보여주나**: "농도가 대기환경기준·주의보 임계(예: O3 시간 0.09/0.12 ppm, PM2.5 일평균 35/75 µg/m³, PM 주의보)를 넘었는가"라는 이진 초과사건을 모델이 맞히는지를, **POD·SR(=1−FAR)·CSI·frequency bias 를 한 평면에** 얹은 Roebber 성능도표로. 여러 임계·계절·모델을 점/궤적으로 스캔.
- **읽는 법**: x=성공비 SR(=1−FAR), y=POD; **곡선 등치선=CSI**(우상단↑), **방사 직선=frequency bias**(대각=1, 위=과대예보·아래=과소). 좋음=점이 우상단(POD·SR·CSI↑)·대각(bias≈1) 근처. *나쁜 패턴*: 좌하단(놓침·오경보 많음), bias선 1에서 크게 벗어남(초과 과대/과소 예보). 임계별 점을 이어 궤적으로 임계 민감도.
- **언제 쓰나**: [시계열]/[격자] O3·PM2.5·PM10 임계 경보 검증. 보건·규제상 **1급 목적**. 임계 스캔·다모델·계절 비교.
- **짝지표 & 교차링크**: **POD·FAR·SR·CSI·FBI·HSS/ETS·(드문사건)SEDI** → [`25` 초과사건 범주형 카드]. performance diagram 골격·CSI 등치선은 공통 [`figures/16` 분할표 viz & Performance diagram]. 확률화는 ROC([`figures/16`]), 위치오차 완화는 공간 FSS([`figures/16`]).
- **만드는 법**: 임계 이진화 후 2×2(a,b,c,d) 집계 → POD·SR·CSI(`numpy`/`xskillscore`); `matplotlib`로 CSI 등치선(`np.meshgrid` SR,POD → CSI=1/(1/SR+1/POD−1))+bias 직선, 임계별 점 overlay. 드문 초과 → 부트스트랩 CI(`figures/16`).
- **함정·주의**: 격자 검증의 **double penalty**(위치 약간 어긋나면 miss+false 동시, §G) → 이웃검증 **FSS** 병행([`figures/16`]). 고농도 초과는 **드문 사건**이라 점수 불안정 → 여러 임계·계절·CI 필수(§G-6). 지역·연도별 사건 빈도 차로 절대비교 주의. 단일 임계는 정보손실 → ROC 병행.
- **출처**: Roebber (2009, *Wea. Forecasting* 24:601–608, doi:10.1175/2008WAF2222159.1, performance diagram); Jolliffe & Stephenson, *Forecast Verification* (범주형); Kang et al. (2007, *J. Geophys. Res.*, 오존 초과 범주형 검증); US EPA modeling guidance.

---

### ★ 일변동 합성 플롯 (일변동 합성 / Diurnal composite plot with bias panel)
- **무엇을 보여주나**: 시간대별(0~23시 LST) **합성(composite) 평균 농도** 를 모델·관측이 함께 그린 곡선(±산포 띠)과, 아래 패널에 **시간대별 bias(h)=m(h)−o(h)**. 오존 오후 첨두·NO2/PM 출퇴근 첨두·야간 축적 등 배출·광화학·경계층(PBL) 혼합의 일주기를 모델이 재현하는지.
- **읽는 법**: x=시각(LST), y=농도. 두 곡선의 **첨두 시각 어긋남=위상오차**, 첨두 높이 차=진폭오차, 항상 한쪽이 위=계통 offset. 아래 bias 패널이 특정 시간대(예: 오존 야간 과대·오후 첨두 과소, NO2 첨두 지연)에 몰리면 PBL 혼합·배출 시간분배·광화학 진단 실마리. ±산포(사이 분위수) 띠로 변동성.
- **언제 쓰나**: [시계열] O3·NO2·PM2.5·CO. 계절 분리(여름/겨울 일변동 상이). (위성은 통과시각 고정이라 일변동 직접검증 불가 — 정지궤도 GEMS/TEMPO 예외.)
- **짝지표 & 교차링크**: 시간대별 bias·**진폭/위상 오차**(1차 harmonic 적합) → [`25` 일변동 카드], 조화·분해는 [`06`]. 요일축은 ⑥ 주말효과, 계절축은 ⑮. 사건별 위상은 ⑬ 시계열.
- **만드는 법**: `pandas` `groupby(local_hour)` 합성 평균·분위수 → `matplotlib` 2-패널(`sharex`), `fill_between`로 산포 띠. 진폭·위상은 `numpy.fft`/최소자승 1차 harmonic. **LST 정렬 필수**(UTC 혼용 금지). 계절별 subplot.
- **함정·주의**: **UTC/LST 정렬 오류가 가짜 위상오차** 생성(가장 흔한 실수). **합성평균은 개별일 위상오차를 은폐**(진폭 감쇠) → 개별일 위상 진단 병행. 계절·측정소유형별 크게 달라짐(분리). 결측 시간대 편향.
- **출처**: Seinfeld & Pandis (교과서, 광화학 일변동); Travis & Jacob (2019, *Atmospheric Chemistry and Physics*, 모델 일변동·PBL 편향 진단); Emery et al. (2017, 시간정의 권고).

---

### 주말효과·주간주기 플롯 (주말효과 / Weekend-effect & weekly-cycle plot)
- **무엇을 보여주나**: 요일별(월~일) 합성 평균 농도와 **평일-주말 그룹 차**(±신뢰구간)를 모델·관측으로 비교. NOx 배출 감소로 오존이 주말에 오히려 증가하는 "주말효과"를 모델이 재현하는지 → 오존 생성체제(NOx- vs VOC-limited) 진단.
- **읽는 법**: x=요일, y=농도(또는 주말/평일 비). 모델·관측 두 곡선의 **주말 상승/하강 부호·크기** 일치 확인. *나쁜 패턴*: 모델이 주말효과 **부호를 틀림**(관측은 주말 O3↑인데 모델은 ↓) → 화학체제/배출 요일분배 오류 → 감축전략 예측 위험. 평일-주말 차 막대에 CI.
- **언제 쓰나**: [시계열] O3·NO2·PM 장기 자료(계절별 충분한 주말 수). 배출 요일 프로파일·화학체제 검증.
- **짝지표 & 교차링크**: 요일 합성·**평일/주말 차 유의성**(t/부트스트랩, [`01`]) → [`25` 주말효과 카드]. 생성체제는 ⑯ FNR, 일축은 ⑤. 계절은 ⑮.
- **만드는 법**: `pandas` `groupby(dayofweek)` 합성 + 평일/주말 그룹 평균·부트스트랩 CI(`scipy`/직접); `matplotlib` 막대/선 + 오차막대. **공휴일 처리 규칙**·LST 정렬 명시.
- **함정·주의**: 표본 적으면 주말-평일 차 CI 큼(장기 필요). **배출 인벤토리의 요일 프로파일 가정**에 결과가 좌우(모델이 관측 부호를 못 맞추면 인벤토리 의심). 도시(체제)별 부호 상이(advisory). 공휴일 오분류.
- **출처**: Blanchard & Tanenbaum (2003, *J. Air & Waste Manage. Assoc.*, 주말효과); Seinfeld & Pandis / Sillman (1995, *JGR*, 오존 생성체제).

---

### ★ soccer / target 플롯 (FAIRMODE 축구장 / target 플롯 / FAIRMODE soccer plot & target diagram, MQI)
- **무엇을 보여주나**: 다수 측정소·화학종·모델을 **한 점씩** 찍어 편향(bias)+중심화 RMS차(CRMSE)를 요약하되, **관측 불확실성으로 정규화**해 **모델품질지표 MQI(원점거리)** 로 등급화한 FAIRMODE 규제 표준 그림("soccer plot"=target). Taylor가 못 보는 **bias 부호**를 전면에.
- **읽는 법**: x=(부호부여) CRMSE/정규화, y=bias/정규화, **원점=완벽**, **반경 1 원(=MQI=1)** 이 "품질 목표 통과선". 각 측정소=점, 원점 거리=그 측정소 MQI. 좋음=점이 반경 1 안(초록 "골대"). 위/아래=과대/과소, 좌/우=모델 변동이 관측보다 작음/큼. 종별 색으로 다종 중첩. (대기질용 일반 target은 [`figures/16`] 골격 + y축 bias 부호로 종별 과대/과소 즉시 판별.)
- **언제 쓰나**: [시계열]/[격자] O3·PM·NO2 등 **다지점·다종·다모델 종합요약**. 규제·정책 벤치마킹(EU AQD, FAIRMODE MQO). 측정소 유형 층화와 결합.
- **짝지표 & 교차링크**: **MQI·bias·CRMSE·정규화(측정 불확실성 U)** → [`25` Taylor/Target 대기질 적용 카드]. target/Taylor 골격은 공통 [`figures/16` Target diagram·Taylor diagram]. 편향 상세는 ③ bugle, 유형별은 ⑫.
- **만드는 법**: **`skill_metrics`**(`sm.target_diagram`) 또는 FAIRMODE **DELTA/DELTA-Light** 툴 관행 재현; bias·CRMSE·σ는 `numpy`/`xskillscore`, MQI=RMSE/(β·U(측정불확실성)) 정규화·β=2 관행. `matplotlib`로 반경 1 원(골대)·종별 색. 측정 불확실성 U(오염종별 모델) 문서화.
- **함정·주의**: **MQI≤1 은 pass/fail 아님, advisory**(§G-4) — 측정 불확실성 U 모델·β 값에 민감(캡션 명시). Target/soccer도 **위상오차는 CRMSE에 섞여** 분리 안 됨. 단일 다이어그램 과신 금지 → MFB/NMB·초과사건 병행(§G-6). 로그정규 자료는 로그변환 후 작도 고려. 정규화 기준 통일.
- **출처**: Thunis et al. (2012, *Environmental Modelling & Software* 33?, "A tool to evaluate air quality model performances in regulatory applications", DELTA, 권·doi 확인요); FAIRMODE *Guidance Document on Modelling Quality Objectives and Benchmarking* (JRC, v3.x, MQI/MQO·target); Jolliff et al. (2009, *J. Marine Systems* 76:64–82, doi:10.1016/j.jmarsys.2008.05.014, target diagram 원형).

---

### ★ 농도 QQ-plot (농도 분위수-분위수 / Concentration Q–Q plot, log-axis, tail-emphasised)
- **무엇을 보여주나**: 모델·관측 농도 **분포의 분위수**를 1:1 대응시켜 분포 형상, 특히 **고농도 꼬리(고오염사건)** 일치를 본다. 평균지표가 못 잡는 꼬리 과소·과대를 포착. (공통 QQ를 **로그축·상위 분위수 확대**로 대기질식 변형.)
- **읽는 법**: x=관측 분위수, y=모델 분위수(p=1·5·…·95·99·99.9%), **로그축 권장**(선형은 꼬리 은폐). **상위 분위수에서 1:1 아래로 휘면 고오염 재현 실패**(규제·보건상 치명적), 위로 휘면 과대. 중앙부 맞고 꼬리만 벌어지면 평균 OK·극치 NG. 마커 크기로 percentile 표시. quantile mapping 보정 전후 점검.
- **언제 쓰나**: 분포·기후 검증, 시간정렬 불필요(동일 기간 동일 모집단). [시계열]/[격자]/[트랙]. PM·O3·NO2 전반, 특히 고농도역.
- **짝지표 & 교차링크**: **KS D·percentile bias·상위분위수 bias** → [`25` 분포·꼬리 QQ/PDF/KS 카드]. QQ 골격은 공통 [`figures/16` QQ-plot], 극값은 return-level([`figures/16`]). quantile mapping은 [`13`].
- **만드는 법**: `numpy.quantile`(공통 확률격자, 꼬리 조밀) 또는 `scipy.stats.probplot`(로그정규 대비); 산점 후 1:1선·로그축·percentile 마커. 표본 적은 99.9%는 부트스트랩 CI 띠.
- **함정·주의**: **분포만 비교 → 동시성(상관) 못 봄**(상관 0이어도 QQ 완벽 가능) → ①/⑬과 3축. **자기상관으로 KS가 거의 항상 "유의"** 판정(§G) → QQ 시각진단 우선. 극단 분위수 불안정(CI). 계절 분리 권장(여름 O3·겨울 PM 꼬리 상이). 0/LOD 처리로 저분위수 왜곡.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (분위수·확률그림); Jolliffe & Stephenson, *Forecast Verification*; 대기질 평가 관행(로그 QQ, 고농도 꼬리).

---

### ★ 위성 대류권 NO2 컬럼 지도 (대류권 NO2 컬럼 지도 / Tropospheric NO2 column map, model vs satellite vs difference)
- **무엇을 보여주나**: 위성(TROPOMI, OMI, GEMS 등) 대류권 NO2 연직컬럼(VCD, molec/cm²)과 **동일 통과시각·구름조건에 샘플링한 모델 컬럼**을 **나란한 3-패널 지도(모델 / 위성 / 차)** 로. 배출·화학·수송을 부이 없는 도시·광역까지 검증. (지상 NO2 농도와는 물리량이 다름 — 컬럼 vs 표면.)
- **읽는 법**: 3-패널 모두 **해안선+위경도 라벨** 위 컬럼 색(순차맵, 도시 핫스팟). 차 패널은 **발산맵·0=흰색**(model−satellite). *읽기*: 도시 상공 모델 과대/과소(빨강/파랑 핫스팟), 배출 인벤토리 위치·강도 오차, 풍하 수송 꼬리. *좋은 패턴*: 공간패턴(도시 핫스팟 위치)·상대 크기 일치. *나쁜 패턴*: 도시 bias 쏠림, 넓은 단색(계통), 재격자 줄무늬.
- **언제 쓰나**: [트랙/타일] TROPOMI/OMI/GEMS L2 swath·L3 gridded vs 모델 [격자→컬럼]. 광역 배출 검증, 연도별 감축 추세.
- **짝지표 & 교차링크**: 격자별 **bias·NMB·상관** + **평균화커널(AK) 적용** → [`25` 위성 NO2 컬럼/AK 카드]. bias 지도 골격은 공통 [`figures/16` Bias/difference map], 매치업·대표성은 [`12`]. AOD는 ⑩, 생성체제는 ⑯ FNR.
- **만드는 법**: `xarray`로 위성 L2/L3 로드, **구름분율·QA flag 필터**; 모델 3D NO2 대류권 연직적분 후 **위성 통과시각·구름 샘플링**·**AK 적용**(Σ AKₖ·부분컬럼). **`plotting_maps.md` `add_basemap` 사용 필수**(cartopy) — 곡선격자는 `pcolormesh(transform=ccrs.PlateCarree())`. 차 패널 `TwoSlopeNorm(vcenter=0)`+`RdBu_r`.
- **함정·주의**: **★ 지도형 — 해안선/육지+위경도 라벨 필수(`add_basemap`).** **경도 0–360→−180–180 변환**. **AK 미적용 비교는 연직민감도 차로 편향**(§G-3, 수십% 가능). **위성=참값 금지**(§G-1) — AMF·성층권 분리·구름 처리가 위성 오차 주원 → **상대 공간패턴·추세**가 절대값보다 신뢰. **컬럼(molec/cm²) ↔ 표면농도 물리량 혼동 금지**. 재격자 보존성.
- **출처**: van Geffen et al. (2020, *AMT*, TROPOMI NO2); Boersma et al. (2011, *AMT*, DOMINO NO2); Eskes & Boersma (2003, *ACP* 3:1285, averaging kernel); GMD 16:509 (2023, "Comparing Sentinel-5P TROPOMI NO2 with CAMS regional AQ ensemble", gmd.copernicus.org/articles/16/509/2023, doi 확인요); GEMS: Kim et al. (2020, *BAMS*, 정지궤도 대기질).

---

### ★ 위성/AERONET AOD 매치업 (에어로졸 광학두께 매치업 / AOD matchup scatter with within-EE envelope)
- **무엇을 보여주나**: 위성(MODIS, VIIRS, GK-2A/GOCI-II 등) 또는 지상 AERONET AOD와 모델 AOD를 매치업한 산점도(1:1·회귀·MFB/FAC2 box)에, 위성 평가용 **기대오차(Expected Error, EE) 포락선**(예 MODIS DT 육상 ±(0.05+0.15τ))을 겹쳐 within-EE 비율로 평가. 에어로졸 총량·광학특성 검증.
- **읽는 법**: x=기준(AERONET/위성), y=모델(또는 y=위성·x=AERONET). **1:1선 + EE 포락선 두 선**(±(0.05+0.15τ)). within-EE 안에 든 비율이 성능. *읽기*: 저AOD 과대(배경), 고AOD 과소(고농도/황사 이류 과소), EE 밖 이탈. MFB/FAC2 box(로그정규). 파장(550nm) 명시.
- **언제 쓰나**: AOD [트랙/타일](위성 L2/L3)·[시계열](AERONET 지점) vs 모델 [격자]. 에어로졸 검증·위성 산출물 평가.
- **짝지표 & 교차링크**: **within-EE·MFB/MFE·FAC2·log-bias·r** → [`25` 위성 AOD 매치업 카드]. 산점 골격 [`figures/16`], AOD↔PM 관계는 [`25` AOD–PM 카드]. 공간분포는 ⑭ 지도. AERONET 위치는 ② 위치도.
- **만드는 법**: `xarray`로 위성 L2/L3·모델 AOD 로드, **구름마스크·지표반사 QC**·**위성 통과시각 샘플링**·**Ångström 파장 보정**; AERONET 지점 매치업. `matplotlib` 산점 + EE 포락선(`ax.plot` 두 곡선) + MFB box. 로그축 옵션.
- **함정·주의**: **AOD는 연직적분 광학량 — 지상 PM2.5와 직접 등가 아님**(PBLH·f(RH)·연직분포 개입 → 별도 AOD–PM 카드). **밝은 지표(사막·해빙)·구름 가장자리 편향**. **AERONET은 고신뢰지만 지점 대표성 제한**. 파장 통일 안 하면 가짜 차이. 로그정규 → 선형 bias보다 MFB 권장.
- **출처**: Levy et al. (2013, *AMT* 6:2989, MODIS Dark Target, EE 정의); Sayer et al. (2013, *JGR*, Deep Blue); Holben et al. (1998, *Remote Sensing of Environment* 66, AERONET); GOCI/GK-2A: Choi et al. (2018, *AMT*, GOCI YAER AOD).

---

### ★ PM 화학종 stacked bar / box plot (성분 분리 / PM speciation stacked bar & box plot)
- **무엇을 보여주나**: PM2.5 총질량을 **성분(SO4²⁻/NO3⁻/NH4⁺/OC/EC/dust/sea-salt)별로 분해**해 모델·관측을 **나란한 stacked bar**(성분 기여 µg/m³)로, 그리고 성분별 bias 분포를 **box plot**으로. **총질량이 맞아도 성분 상쇄(황산염 과대+질산염 과소)** 로 우연히 맞을 수 있어, 성분 검증이 화학·배출 진단의 핵심.
- **읽는 법**: (stacked) 좌=관측·우=모델 막대(계절·측정소별 쌍), 색=성분; 총 높이 비슷해도 **색 비율 다르면 상쇄 오차**. (box) x=성분, y=bias(또는 MFB), 상자가 0에서 벗어난 성분이 문제종. *읽기*: 질산염·유기탄소(OC) 상자가 크게 편향(최난제), SO4 상대 양호가 일반적. 계절 분리(겨울 질산염·여름 SOA).
- **언제 쓰나**: [시계열]/[격자] PM2.5/PM10 **성분측정망**(미 IMPROVE/CSN, 국내 성분측정소) vs 모델. 화학·배출 진단.
- **짝지표 & 교차링크**: 성분별 **MFB/MFE·NMB/NME·질량 닫힘** → [`25` PM speciation·mass closure 카드], bugle는 ③. box 골격은 오차분포([`figures/16` 오차 히스토그램]의 성분 변형). 종별 target은 ⑦.
- **만드는 법**: `pandas`로 성분 매치업 → `matplotlib` stacked `ax.bar`(관측/모델 쌍) + 성분별 bias `ax.boxplot`/`seaborn.boxplot`. OM=OC×계수(1.4~2.1)·dust 산화물 계수 가정 명시. 계절 facet.
- **함정·주의**: **총질량 성능만 보고 결론 금지**(§G-6 상쇄 은폐). **OC/EC 측정법(IMPROVE 열광학 vs NIOSH)·OM/OC 계수·질산염 휘발손실(반휘발성 NH4NO3)** 이 대형 불확실원 → 프로토콜·계수 캡션 명시. 성분 정의 불일치. 미결정질량(other) 처리규칙.
- **출처**: Boylan & Russell (2006, *Atmos. Environ.* 40:4946); Simon, Baker & Phillips (2012, *Atmos. Environ.* 61:124, 성분별 성능 통계); Malm et al. (1994, *JGR*, IMPROVE reconstructed mass); Chow et al. (2015, *Aerosol Air Qual. Res.*, mass closure).

---

### ★ 측정소 유형별 box plot (측정소 유형 층화 box / Station-type box plot: urban/traffic/rural/background)
- **무엇을 보여주나**: 측정소를 **도시배경/교통(도로변)/산업/농촌배경** 으로 분류해 각 그룹별 성능지표(bias·NMB·MFB·상관·RMSE)의 분포를 **box plot(그룹=상자)** 으로 비교. 국지 오염원 영향을 분리해 모델의 "광역 배경 재현력"과 "국지 표현력"을 구분.
- **읽는 법**: x=측정소 유형, y=성능지표(예 bias 또는 MFB). 각 상자=그 유형 측정소들의 지표 분포(중앙값·IQR·이상치). *읽기*: **교통·산업 상자가 크게 음(과소)** 이면 대개 대표성 문제(광역격자가 국지 첨두 못 담음)이지 모델 결함이 아닐 수 있음; 배경·농촌 상자가 0 근처면 광역 재현 양호. 유형 간 중앙값 차·산포 비교.
- **언제 쓰나**: [시계열] 다지점 검증에서 **유형 층화 필수 그림**(통합 통계의 오해 방지). NO2·1차 PM(공간경사 급함)에서 특히 중요. 격자 해상도 정합 판단.
- **짝지표 & 교차링크**: 그룹별 **bias·NMB·MFB·r + 대표성 오차** → [`25` 측정소 유형 층화·대표성 카드]. 위치·유형색은 ② 위치도, 성분은 ⑪. 오차분포 골격 [`figures/16`].
- **만드는 법**: 측정소 메타(유형)로 `pandas.groupby` → 그룹별 지표 산출 → `seaborn.boxplot(x='type', y='bias')`/`matplotlib.boxplot`. 그룹 n·이상치 표기. (선택) 유형별 색을 ② 위치도와 통일.
- **함정·주의**: **대표성 오차를 모델오차로 오귀속 금지**(§G-1, 여기선 관측 대표성 한계). **도로변 측정소를 광역격자 검증에 쓸지는 해상도 의존**(고해상도만 의미) — 저해상도면 제외/별도. **분류 규약이 국가·기관마다 상이**(EEA vs 국내 도시대기/도로변/배경) → 규약 명시. 그룹 표본 적으면 상자 불안정.
- **출처**: Thunis et al. (2012, *Atmospheric Environment* 49?, 측정소 유형·모델평가, 확인요); EEA AirBase/AQ e-Reporting 측정소 분류; FAIRMODE 대표성 지침; Janssen et al. (2008, *Atmos. Environ.*, 대표성).

---

### model–obs 시계열 overlay + 잔차 패널 (시계열 중첩·잔차 / Time-series overlay with residual panel)
- **무엇을 보여주나**: 한 측정소에서 모델·관측 농도(O3·PM2.5·NO2 등)를 **시간축에 겹쳐** 그리고, 아래 패널에 **잔차(model−obs)** 를 둔다. 고오염 에피소드(황사·정체·오존 사건)의 **첨두 타이밍·진폭·위상지연·계통 offset**을 직접 본다.
- **읽는 법**: 위 패널 두 선의 **첨두 시각 어긋남=위상오차**, 첨두 높이 차=진폭오차, 항상 한쪽이 위=bias. 아래 잔차가 0 주위 무작위면 양호; **에피소드마다 같은 부호로 튀면 사건 계통오차**(고농도 과소 흔함); 잔차 추세/계단=비정상·센서 drift. 기준·주의보 임계선을 얹으면 경보 관점 가독.
- **언제 쓰나**: [시계열] 단일/소수 측정소 정밀 진단, 고오염 사례 분석, 예보선행시간별 열화 점검. 산점(집계)이 못 보는 *언제·왜*.
- **짝지표 & 교차링크**: 사건 잔차 통계(event bias/RMSE)·**교차상관 lag**(위상) → [`25` 일변동/계절], [`06` lag·STL], [`01` bias/RMSE]. 임계초과 경보는 ④ performance. 다지점 요약은 ⑦ target.
- **만드는 법**: `pandas`/`xarray` 시간정렬(LST/UTC 통일) 후 `matplotlib` 2-패널(`sharex`), `fill_between`로 ±잔차 음영. 결측 구간 끊어 그림(직선보간으로 잇지 말 것 — 사건 통계 왜곡).
- **함정·주의**: 모델·관측 **시간기준(UTC/LST·순간 vs 시간평균) 불일치**가 가짜 위상오차. 결측 직선보간 금지. 한 측정소 결론을 광역 일반화 금지(대표성). 로그정규 변수는 로그 y축 병행 고려.
- **출처**: Wilks / Jolliffe & Stephenson (시계열 진단); Emery et al. (2017, 사례·시간정의); Seinfeld & Pandis (에피소드 물리).

---

### ★ 재분석 격자 bias/difference 지도 (재분석 대조 지도 / Gridded bias map vs CAMS / MERRA-2 reanalysis)
- **무엇을 보여주나**: 우리 모델 [격자]를 **CAMS reanalysis·MERRA-2 aerosol** 등 재분석 [격자]와 **공간 전면적**으로 비교해 bias(x,y)·RMSE(x,y)·상관(x,y)을 **지도(색)** 로. 측정소 없는 해역·산악·국외까지 **계통오차의 지리적 위치·계절성**을 진단.
- **읽는 법**: **해안선+위경도 라벨** 위 색=각 격자점 bias(발산맵, 0=흰색)/RMSE(순차맵). *읽기*: 도시권 양(과대)·배경 음(과소) 띠, 황사 이류경로·국경(배출 인벤토리 차) 패턴, 계절별 반전(여름 O3·겨울 PM). *나쁜 패턴*: 넓은 단색(계통편차), 해안선 줄무늬(재격자 artifact), 격자해상도 차 아티팩트.
- **언제 쓰나**: [격자]vs[격자] NetCDF. 광역 진단, 점 검증(①·⑫)이 못 메우는 공간 커버리지. PM·O3·NO2·AOD.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·상관·NMB** → [`25` 재분석 격자 대조 카드], [`02` 공간패턴], [`15` regridding]. bias map 골격은 공통 [`figures/16` Bias/difference map]. 점 검증 ①/⑫와 교차. 위성 지도는 ⑨.
- **만드는 법**: `xarray`+`xesmf`(conservative/bilinear regridding, 공통 격자)→격자별 통계→**`plotting_maps.md` `add_basemap`**(cartopy)+`pcolormesh`. **발산맵 `cmocean.cm.balance`/`RdBu_r`+`TwoSlopeNorm(vcenter=0)`**(bias), 순차맵(RMSE). 육지/해양·결측 마스크 통일.
- **함정·주의**: **★ 지도형 — 해안선/육지+위경도 라벨 필수(`add_basemap`).** **경도 0–360→−180–180 변환**. **재분석은 독립 진값 아님**(자체 오차·동화 한계, §G-1) → "정답" 과신 금지, 측정소·위성과 교차. **CAMS/MERRA-2 해상도(~0.4~0.75°)** 로 도시 표현 한계. 재격자 보존성·해상도 차가 차이의 상당부분일 수 있음.
- **출처**: Inness et al. (2019, *ACP* 19:3515, CAMS reanalysis, doi 확인요); Gelaro et al. (2017, *J. Climate* 30:5419, MERRA-2, doi:10.1175/JCLI-D-16-0758.1); WMO/EPA 절차; cmocean (Thyng et al. 2016, doi:10.5670/oceanog.2016.66).

---

### 계절·월별 층화 성능 히트맵 (계절 층화 히트맵 / Seasonal-stratification performance heatmap)
- **무엇을 보여주나**: 계절/월(행) × 화학종·측정소유형(열)로 나눈 성능지표(NMB/NME/MFB/r)를 **색 히트맵**으로. 여름 광화학(O3)·겨울 축적(PM)·황사 이류 등 **계절 의존 오차 구조**를 한눈에. 연평균 단일 통계가 상쇄로 은폐하는 계절 반전 편향을 노출.
- **읽는 법**: 행=계절/월, 열=종/유형, 색=지표(bias는 발산맵 0=흰색). *읽기*: **여름 O3 과소·겨울 PM 과소(질산염·난방·역전층)** 등 계절별 상반 부호(발산색 반전)가 흔함 → 연평균만 보면 상쇄로 "양호" 오판. 특정 월 이상치(황사·산불) 강조.
- **언제 쓰나**: [시계열]/[격자] 전 화학종의 계절 분해 진단. 각 계절 충분 표본 필요.
- **짝지표 & 교차링크**: 계절 부분집합 **NMB/NME/MFB/r**([`01`] 지표를 계절별 적용) → [`25` 계절 층화 카드]. 일축은 ⑤, 요일축은 ⑥. 이벤트(황사) 라벨링은 [`03`] 극값.
- **만드는 법**: `pandas`로 계절/월 부분집합별 지표 계산 → 피벗테이블 → `seaborn.heatmap`(발산 cmap·`center=0`)/`matplotlib.pcolormesh`. 특이 이벤트(황사·산불) 라벨/제외 옵션.
- **함정·주의**: **연통계만 보면 계절 상쇄로 오판**(§G-6 — 이 그림의 존재 이유). **이벤트(황사) 미제거 시 계절통계 왜곡** → 라벨링. 각 셀 표본 수 병기(적으면 색 불안정). 색범위 종별 통일 안 하면 오해.
- **출처**: Emery et al. (2017, 계절 벤치마크 권고); Seinfeld & Pandis (계절 광화학·에어로졸); 각국 CTM 평가 논문 관행.

---

### 오존 생성체제 진단 지도 (생성체제 지도 / Ozone-regime diagnostic map: HCHO/NO2 = FNR)
- **무엇을 보여주나**: 위성/모델 **HCHO/NO2 컬럼비(FNR, Formaldehyde-to-NO2 Ratio)** 를 지도로 그려 오존 생성체제(**NOx-limited vs VOC-limited vs 전이**)의 공간분포를 모델·위성으로 대조. "오존이 맞는 이유가 옳은지"(감축전략 방향)를 진단.
- **읽는 법**: **해안선+위경도 라벨** 위 색=FNR, **체제 임계(관행 ~1~2 경계)** 로 3구간(저FNR=VOC-limited 도심·고FNR=NOx-limited 교외). 모델·위성 지도 비교: 도시권 VOC-limited 영역·경계 위치 일치? *나쁜 패턴*: 모델이 체제 경계를 잘못 그림 → NOx/VOC 감축전략 예측 위험. 차 지도로 체제 편차.
- **언제 쓰나**: [트랙/타일] 위성 HCHO·NO2 컬럼 + [격자→컬럼] 모델. 오존 정책·전구물질 검증. 여름 광화학 활발기.
- **짝지표 & 교차링크**: **FNR·체제 분류·OX·NOx/VOC bias** → [`25` 오존 전구물질·광화학 지표 카드]. NO2 컬럼은 ⑨, 주말효과(체제 간접증거)는 ⑥. bias map 골격 [`figures/16`].
- **만드는 법**: 위성 HCHO·NO2 L2/L3(QC·AK) → FNR=HCHO/NO2; 모델 동일 산출. **`plotting_maps.md` `add_basemap`**(cartopy)+`pcolormesh`, 체제 임계 등치선(`ax.contour`). 통과시각·구름 샘플링 통일.
- **함정·주의**: **★ 지도형 — 해안선/육지+위경도 라벨 필수(`add_basemap`).** **위성 HCHO 저신호·노이즈** 크고 **FNR 체제 임계 전이성 낮음**(지역·계절 의존, advisory §G-4). AK·성층권 분리 필요(⑨ 주의 준용). **오존 단독 성능으로 화학 정합 판단 금지**(§G-6) — 체제 진단은 보조. 경도 규약 변환.
- **출처**: Duncan et al. (2010, *Atmospheric Environment* 44:2213, HCHO/NO2 체제 지표); Sillman (1995, *JGR* 100:14175, 광화학 지표); Martin et al. (2004, *JGR*, 위성 FNR); Seinfeld & Pandis (OX·적정).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 25(및 타 파일)·figures/16 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 25(및 타 파일)·figures/16 교차링크 |
|---|---|---|---|---|---|
| 1 | 농도 로그-로그 산점 + FAC2 | 시계열·격자·트랙 | 정확도+편향 | FAC2·MFB·NMB·log-bias·r | 25 FAC2/MFB/NMB · figures/16 산점 |
| 2 | 측정소 위치 지도 (basemap+ID) | 시계열 | 위치·유형 개요 | 대표성·유형 층화 | 25 대표성/유형 · plotting_maps |
| 3 | MFB/MFE bugle (Boylan&Russell) | 시계열·격자 | 편향(농도의존 등급) | MFB·MFE·goal/criteria | 25 MFB·MFE/B&R |
| 4 | 초과사건 performance diagram | 시계열·격자 | 범주형 사건 | POD·SR·CSI·FBI·HSS | 25 초과사건 · figures/16 performance |
| 5 | 일변동 합성 + bias | 시계열 | 편향+위상(일주기) | 시간대 bias·진폭/위상 | 25 일변동 · 06 조화 |
| 6 | 주말효과·주간주기 | 시계열 | 편향(요일)·체제 | 평일/주말 차·유의성 | 25 주말효과 · 01 |
| 7 | soccer/target (FAIRMODE MQI) | 시계열·격자 | 편향+산포 종합 | MQI·bias·CRMSE | 25 Taylor/Target · figures/16 target |
| 8 | 농도 QQ-plot (로그·꼬리) | 시계열·격자·트랙 | 분포·고농도 꼬리 | KS·percentile bias | 25 QQ/PDF/KS · figures/16 QQ |
| 9 | 위성 NO2 컬럼 지도 (model/sat/차) | 트랙·격자 | 편향+패턴(광역) | bias·NMB·상관·AK | 25 위성 NO2/AK · figures/16 bias map · 12 |
| 10 | 위성/AERONET AOD 매치업 | 트랙·시계열·격자 | 정확도(에어로졸) | within-EE·MFB·FAC2·r | 25 위성 AOD · figures/16 산점 |
| 11 | PM speciation stacked/box | 시계열·격자 | 편향(성분·상쇄) | 성분 MFB/NMB·mass closure | 25 speciation/mass closure · 03 bugle |
| 12 | 측정소 유형별 box | 시계열 | 편향(유형 층화) | 그룹 bias/NMB/MFB·대표성 | 25 유형 층화/대표성 · figures/16 |
| 13 | 시계열 overlay + 잔차 | 시계열 | 편향+위상+사건 | event bias/RMSE·lag | 25 일변동/계절 · 06 lag · 01 |
| 14 | 재분석 bias 지도 (CAMS/MERRA-2) | 격자 | 편향+패턴(공간) | 격자별 bias·RMSE·상관 | 25 재분석 대조 · figures/16 bias map · 02·15 |
| 15 | 계절 층화 성능 히트맵 | 시계열·격자 | 편향(계절 분해) | 계절별 NMB/NME/MFB/r | 25 계절 층화 · 01 |
| 16 | 생성체제 지도 (HCHO/NO2 FNR) | 트랙·격자 | 패턴(화학체제) | FNR·체제 분류·OX | 25 오존 전구물질 · figures/16 bias map |

> **묶음 권고**: 단일 그림 금지 원칙(§G-5)에 따라 대기질 검증 보고는 최소 **①(정확도+편향, 로그산점+FAC2) + ③(MFB/MFE bugle) + ⑧(QQ·꼬리) + ④(초과사건)** 4장을 기본 세트로, 다지점 요약은 **⑦(soccer/target)+②(위치도)**, 시간구조는 **⑤(일변동)/⑥(주말)/⑬(시계열)/⑮(계절)**, PM 화학은 **⑪(speciation)**, 위성·광역은 **⑨(NO2)/⑩(AOD)/⑭(재분석 지도)/⑯(FNR)**, 유형별은 **⑫**를 추가한다. 모든 임계(MFB±30%·Emery NMB±5%·FAC2≥0.5·MQI≤1 등)는 **advisory + 지역·화학종·해상도 의존 경고**로 캡션에 단다. **총 PM2.5가 맞아도 성분 상쇄를 의심**(⑪ 병행), **위성·재분석은 reference이지 truth 아님**.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- Seinfeld & Pandis, *Atmospheric Chemistry and Physics: From Air Pollution to Climate Change* (Wiley) — 로그정규 농도·광화학·일변동·에어로졸 미세물리·f(RH).
- Wilks, *Statistical Methods in the Atmospheric Sciences* — 산점·QQ·KS·회귀 표준 시각화.
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* — 범주형·분포·ROC.
- US EPA, *Modeling Guidance for Demonstrating Air Quality Goals for Ozone, PM2.5, and Regional Haze* (2018) — MDA8·설계값·NMB/NME 절차.
- FAIRMODE, *Guidance Document on Modelling Quality Objectives and Benchmarking* (JRC) — MQI/MQO·target(soccer) plot.

**학술 논문 (제목·저널·연도 웹 확인)**
- Boylan & Russell (2006) "PM and light extinction model performance metrics, goals, and criteria for three-dimensional air quality models," *Atmospheric Environment* 40(26):4946–4959. (MFB/MFE goal/criteria·bugle)
- Emery, Liu, Russell, Odman, Yarwood & Kumar (2017) "Recommendations on statistics and benchmarks to assess photochemical model performance," *J. Air & Waste Manage. Assoc.* 67(5):582–598, **doi:10.1080/10962247.2016.1265027**. (NMB/NME/r 벤치마크)
- Chang & Hanna (2004) "Air quality model performance evaluation," *Meteorol. Atmos. Phys.* 87:167–196, **doi:10.1007/s00703-003-0070-7**. (FB·NMSE·FAC2·MG·VG)
- Roebber (2009) "Visualizing Multiple Measures of Forecast Quality," *Wea. Forecasting* 24:601–608, **doi:10.1175/2008WAF2222159.1**. (performance diagram)
- Jolliff et al. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment," *J. Marine Systems* 76:64–82, **doi:10.1016/j.jmarsys.2008.05.014**. (target diagram)
- Simon, Baker & Phillips (2012) "Compilation and interpretation of photochemical model performance statistics," *Atmospheric Environment* 61:124–139. (성분별 성능 통계)
- Blanchard & Tanenbaum (2003) 주말효과, *J. Air & Waste Manage. Assoc.*
- Duncan et al. (2010) "Application of OMI observations to a space-based indicator of NOx and VOC controls," *Atmospheric Environment* 44:2213–2223. (HCHO/NO2 FNR 체제)
- Sillman (1995) "The use of NOy, H2O2, and HNO3 as indicators for ozone-NOx-VOC sensitivity," *JGR* 100:14175. (광화학 지표)
- Levy et al. (2013) "The Collection 6 MODIS aerosol products (Dark Target)," *AMT* 6:2989–3034. (AOD EE)
- Sayer et al. (2013) MODIS Deep Blue, *JGR*.
- Holben et al. (1998) "AERONET—A federated instrument network...," *Remote Sensing of Environment* 66:1–16.
- van Geffen et al. (2020) TROPOMI NO2, *AMT*.
- Boersma et al. (2011) DOMINO tropospheric NO2, *AMT*.
- Eskes & Boersma (2003) "Averaging kernels for DOAS total-column satellite retrievals," *ACP* 3:1285–1291. (AK)
- Gelaro et al. (2017) "The Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2)," *J. Climate* 30:5419–5454, **doi:10.1175/JCLI-D-16-0758.1**.
- Malm et al. (1994) IMPROVE reconstructed mass, *JGR*; Chow et al. (2015) mass closure, *Aerosol Air Qual. Res.*
- Thyng et al. (2016) cmocean, *Oceanography* 29(3), **doi:10.5670/oceanog.2016.66**.

**기관 자료·기술보고 (실재 URL)**
- FAIRMODE — Forum for Air Quality Modelling in Europe: https://fairmode.jrc.ec.europa.eu · DELTA Tool/Benchmarking, MQI/MQO target(soccer) plot.
- FAIRMODE *Guidance Document on Modelling Quality Objectives and Benchmarking* (JRC): https://publications.jrc.ec.europa.eu/repository/bitstream/JRC120649/mqoguidance_online.pdf
- EEA AirBase / AQ e-Reporting 측정소 분류(도시배경/교통/산업/농촌배경).
- "Comparing Sentinel-5P TROPOMI NO2 column observations with the CAMS regional air quality ensemble," *GMD* 16:509 (2023): https://gmd.copernicus.org/articles/16/509/2023

**소프트웨어 (실존 도구)**
- `matplotlib`(scatter/hexbin/boxplot/pcolormesh·log축·TwoSlopeNorm), `numpy`(MFB/MFE/NMB/FAC2 직접), `pandas`(groupby 합성·계절/요일 층화), `seaborn`(boxplot·heatmap).
- `xarray`+`xesmf`(재격자), `cartopy`(지도·`plotting_maps.md`의 `add_basemap`).
- `skill_metrics`(`sm.target_diagram`·`sm.taylor_diagram`), FAIRMODE **DELTA / DELTA-Light**(규제 벤치마킹·target).
- `xskillscore`(범주형·상관·rmse), `scipy.stats`(probplot·KS·부트스트랩), `cmocean`(balance/thermal 색맵).
- 위성 처리: `harp`/Atmospheric Toolbox·`xarray`(L2/L3·구름·QA·AK 적용).

**확인요 (확정 인용 금지 — §G-6)**
- Thunis et al. (2012) DELTA "A tool to evaluate air quality model performances in regulatory applications," *Environmental Modelling & Software* — 저널 확인, **권·페이지·DOI 미확정(확인요)**.
- Thunis et al. (2012, 측정소 유형·모델평가, *Atmospheric Environment*) — 권·페이지 **(확인요)**.
- Inness et al. (2019) CAMS reanalysis, *ACP* 19:3515 — 권·페이지 확인, **DOI 패턴 추정(확인요)**.
- GMD 16:509 (2023, TROPOMI–CAMS NO2) — URL 확인, **DOI 미검증(확인요)**.
- Martin et al. (2004) 위성 FNR, *JGR* — 권·페이지 **(확인요)**.
- 해석 임계(Boylan&Russell MFB±30/±60%·MFE 50/75%, Emery O3 NMB±5/±15%·NME 15/25%·r≥0.5, FAC2≥0.5, Chang&Hanna |FB|<0.3, FAIRMODE MQI≤1)는 **미국/유럽 사례 기반 advisory** — 지역·화학종·해상도·계절 의존(§G-4).
- 위성 EE(MODIS DT 육상 ±(0.05+0.15τ))·FNR 체제 임계(~1~2)는 산출물·지역 의존 advisory.
