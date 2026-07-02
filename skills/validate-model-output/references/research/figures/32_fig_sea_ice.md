# 32. 검증 시각화 카탈로그 — 해빙·빙권편 (Verification Figures: Sea Ice / Cryosphere)

이 문서는 해빙 모델(해빙-해양 결합 CICE/SI3/CESM-CICE, 예보시스템 TOPAZ/neXtSIM/PIOMAS, 재분석 ORAS5/GIOMAS 등)의 산출물을 **위성 수동마이크로파(SSMIS·AMSR2 SIC)·고도계(CryoSat-2·ICESat-2)·SMOS·병합 CS2SMOS·표류부이(IABP)·해빙도(ice chart, NIC/AARI)** 와 비교·검증할 때 쓰는 **그림(figure) 카드** 카탈로그다. 메서드(수치지표) 카드는 [`24_domain_sea_ice.md`](../24_domain_sea_ice.md)에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **대응 메서드카탈로그: [`24_domain_sea_ice.md`](../24_domain_sea_ice.md)** — 각 그림 카드는 24의 방법 카드와 짝을 이룬다(그림=어디서·어떻게 틀렸나 / 지표=얼마나 틀렸나).

> **공통/횡단 그림과의 분담**: Taylor·target·일반 QQ·ROC·reliability·rank histogram·Brier/CRPS 분해·PDF/CDF·성능다이어그램 등 **도메인 무관 요약그림은 [공통편 `16_fig_common.md`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않고 **교차링크만** 한다. 이 파일은 **해빙 고유 그림**(SIC 지도·차이지도, 얼음경계 오버레이 + IIEE 음영, SIE/SIA 계절곡선, 두께 지도·ITD, 표류 quiver, 얼음경계 확률/edge Hovmöller 등)에 집중한다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3-L4) · [시계열]=SIE·SIA·SIV 지수 시계열 · [트랙]=위성 along-track(CryoSat-2/ICESat-2 freeboard) 또는 표류부이 궤적 · [경계]=얼음경계 폴리곤/등치선(15% SIC contour) · [벡터]=해빙 표류 벡터장.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 위성 SIC(알고리즘 산물)·CS2SMOS/CryoSat-2 두께(밀도·적설 가정 유도량)·PIOMAS/ORAS5 재분석은 모두 reference이지 truth가 아니다. 축 라벨·캡션에 "모델 − 기준(reference)"으로 쓰고 "오차"로 단정하지 않는다.
> 2. **SIC는 [0,1] bounded 변수.** 경계(0·1)에 자료가 몰려 오차분포가 비정규·비대칭. 발산 색맵 0중심, 국지 RMSE·공간지도 병행. 순 bias가 상쇄로 0이어도 국지 오차 큼.
> 3. **해석 임계는 advisory.** 15% SIE 임계·"겨울 SIC 불확실성 5–10%"·"MIZ 20–30%" 등은 **해역·계절·센서 의존 사례값**이며 절대기준 아님. 그림에 good/bad를 단정 표기하지 말고 계절·해역·관측불확실성 경고를 캡션에 둔다.
> 4. **단일 그림 금지.** 얼음경계 하나만 봐도 **면적(IIEE)+거리(MHD)+스케일(FSS)** 를 함께, SIE는 **위치오차를 못 봄** → IIEE/edge 병행 필수. 최소 3축(범위+위치/거리+분포/두께) + 유의성(부트스트랩).
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문 도판을 그대로 재현하지 않는다.
> 6. **★ 지도형(위경도) 그림은 해안선/육지 + 위경도 라벨 필수** — 극projection에서는 [`plotting_maps.md`](../../plotting_maps.md)의 `add_basemap()`을 쓰고(cartopy `NorthPolarStereo`/`SouthPolarStereo` + coastline + gridlines), 정점/부이 그림은 위치 지도 + 마커 + ID를 넣는다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **SIC 공간 지도 + 15% 얼음경계 등치선** — 해빙 상태장 1차 대표 그림 (지도)
2. ★ **SIC 차이(bias) 지도 (model−reference, 발산맵)** — 계통오차의 지리분포 (지도)
3. ★ **얼음경계 오버레이 지도 (obs vs model 15% 등고선 + IIEE A⁺/A⁻ 음영)** — 얼음경계 위치오차 (지도)
4. ★ **SIE / SIA 계절곡선 + 시계열 + 잔차** — 연주기·최소·최대·추세
5. **IIEE 분해 시계열 (AEE vs ME, 리드타임)** — 범위오차 대 위치오차
6. **얼음경계 거리오차 요약 그림 (MHD·평균변위·EDE, 해역/계절 막대·박스)** — 경계선 거리
7. ★ **SIC 검증 산점도/밀도 + bounded 진단** — 격자별 농도 정확도 (공통 ①/② 변형)
8. ★ **해빙 두께 공간 지도 + 차이 지도 (CryoSat-2/CS2SMOS/ICESat-2)** — 두께장 (지도)
9. **두께대별(binned) 두께 검증 산점 (SMOS 박빙 / CryoSat-2 후빙)** — 센서 유효두께대
10. ★ **ITD 히스토그램 (카테고리별 면적비 g(h), obs vs model)** — sub-grid 두께분포
11. ★ **해빙 표류 벡터장 quiver 지도 (obs vs model, 속력 색·차이벡터)** — drift (지도)
12. **라그랑지안 부이 궤적 지도 + 분리거리 곡선** — drift 궤적 (지도 + 곡선)
13. ★ **얼음경계 확률 예보 검증 (reliability·ROC·SPS 지도)** — 앙상블 ice edge (공통 ⑫/⑬ + SPS 지도)
14. ★ **얼음경계 위도 Hovmöller (edge latitude time–longitude)** — 계절 전진/후퇴 전파
15. **FSS 스케일–임계 히트맵 (얼음/무빙 이진장)** — 공간 스케일 유용성 (공통편 교차 + 해빙주석)
16. **SIV / 부피 시계열 + 계절진폭** — 두께×농도 적분량 (PIOMAS 대조)

---

### ★ SIC 공간 지도 + 15% 얼음경계 등치선 (해빙농도 지도 / Sea ice concentration map with 15% edge contour)
- **무엇을 보여주나**: 특정 시각·월평균의 해빙농도 SIC(0–1)를 극지도에 채움(pcolormesh)으로 그리고 15% 등치선(얼음경계)을 겹친 **해빙 상태장의 1차 대표 그림**. 모델·기준(위성 SIC)을 나란히 두 패널로 배치해 밀집빙역·MIZ·얼음경계 위치를 한눈에.
- **읽는 법**: 색=SIC(순차 색맵, 예 `cmocean.cm.ice`, 0=개빙 짙은색↔1=밀집빙 흰색). 15% 등치선(굵은 실선)=관행적 얼음경계. 모델·관측 두 패널에서 밀집빙 코어·MIZ 폭·경계 위치를 대조. *좋은 패턴*: 두 패널의 경계선·농도 그라디언트 일치. *나쁜 패턴*: 경계선이 통째로 안/밖으로 밀림(위치오차), MIZ 대역(15–80%)이 모델에서 지나치게 좁음(경계 급변), 특정 해역만 농도 과대/과소.
- **언제 쓰나**: [격자] 모델 vs [격자] 위성 L3/L4·재분석. 임의 시각·월평균·계절 대표월(3월 최대·9월 최소). 정성 1차 점검.
- **짝지표 & 교차링크**: SIC 격자별 bias·RMSE(→ [`24` SIC 카드]), 얼음경계는 ③ 오버레이·IIEE와 짝. 공간 종합요약은 공통편 [`16` Taylor·bias map]로 승급. 차이 정량은 ②.
- **만드는 법**: `xarray`로 SIC 로드 → `matplotlib`+`cartopy` `ccrs.NorthPolarStereo()`/`SouthPolarStereo()` GeoAxes에 `ax.pcolormesh(lon, lat, sic, transform=ccrs.PlateCarree(), cmap=cmo.ice)`; 15% 등치선 `ax.contour(lon, lat, sic, levels=[0.15], transform=ccrs.PlateCarree())`. **해안선/육지·위경도 라벨 필수** — [`plotting_maps.md`](../../plotting_maps.md) `add_basemap()`(극 GeoAxes) 또는 `ax.add_feature(cfeature.LAND/COASTLINE)`+`ax.gridlines(draw_labels=True)`. 육지·pole hole 마스크 통일.
- **함정·주의**: **지도 필수** — 극projection에서 해안선·위경도 라벨 없으면 "어디인지" 못 읽음(§plotting_maps). 경도 0–360 vs −180–180 규약, 극점 데이터공백(pole hole) 처리 통일. 위성 SIC는 알고리즘(Bootstrap/NASA Team/ASI/OSI SAF)별로 값이 달라 대조군 명시. 재격자화가 경계에서 인위적 중간농도 생성. `contourf`는 곡선격자를 뭉갬 → `pcolormesh` 권장.
- **출처**: OSI SAF Sea Ice Concentration product (osi-saf.eumetsat.int); Lavergne et al. (2019) "Version 2 of the EUMETSAT OSI SAF and ESA CCI sea-ice concentration climate data records," *The Cryosphere* 13:49–78 (doi:10.5194/tc-13-49-2019); Meier et al. NOAA/NSIDC Sea Ice Concentration CDR (nsidc.org); cmocean: Thyng et al. (2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66).

---

### ★ SIC 차이(bias) 지도 (해빙농도 차 지도 / SIC difference (bias) map, model − reference)
- **무엇을 보여주나**: 모델 SIC와 기준(위성/재분석) SIC의 격자별 차(model−ref)를 **발산 색맵**으로 극지도에 그려, "어디서" 모델이 농도를 과대/과소하는지의 **공간 구조·계절성**을 직접 본다. bias·RMSE·anomaly correlation 지도의 대표.
- **읽는 법**: 발산 색맵(`cmocean.cm.balance` 또는 `RdBu_r`), **0=흰색**, 대칭 범위(±vmax). 빨강=모델 과대·파랑=과소. *좋은 패턴*: 전역 옅은 색·구조 없는 잡음. *나쁜 패턴*: 얼음경계 따라 쌍극자(경계 위치 어긋남=double-penalty 신호), 특정 해역 넓은 단색(계통 과대/과소), 해안선 따라 줄무늬(재격자 artifact). RMSE 지도(비음수 순차맵)와 병치.
- **언제 쓰나**: [격자]vs[격자] NetCDF. 광역 계통오차 진단, 점·트랙 검증(⑧·⑪)이 못 메우는 공간 커버리지. 계절·월별로 반복해 계절성 파악.
- **짝지표 & 교차링크**: 격자별 bias·RMSE·R·ACC(→ [`24` 격자-격자 공간비교 카드]); 공통편 [`16` bias/difference map]·[`02` 공간패턴]·[`15` regridding]. 얼음경계 국지구조는 ③과 교차. bounded 산점은 ⑦.
- **만드는 법**: `xarray`+`xesmf`(conservative/nearest regridding, 공통 극격자)→격자별 차→`cartopy` 극 GeoAxes `pcolormesh` + `TwoSlopeNorm(vcenter=0)`. **해안선/육지+위경도 라벨 필수**(`add_basemap`). SIC는 fraction/% 단위 통일, land·pole hole 마스크 통일.
- **함정·주의**: **지도 필수**(해안선·라벨). **재분석·위성 L4는 참값 아님**(§G-1) → 부이/트랙과 교차, "정답" 과신 금지. SIC bounded → 경계 근처 차이 비대칭(양극단에서 과대/과소가 물리적으로 한쪽만 가능). 재격자화 방식·해상도 차가 차이의 상당부분 생성 → 보존형·공통격자. 발산맵 비대칭이면 시각적 거짓편향. 위성 알고리즘 차가 bias에 섞임.
- **출처**: 공통편 [`16` bias map] 출처; Ivanova et al. (2015) "Inter-comparison and evaluation of sea ice algorithms," *The Cryosphere* 9:1797–1817 (doi:10.5194/tc-9-1797-2015, 확인요); Zuo et al. (2019) ORAS5 (*Ocean Science*, 확인요); cmocean (Thyng et al. 2016, doi:10.5670/oceanog.2016.66).

---

### ★ 얼음경계 오버레이 지도 + IIEE 음영 (얼음경계 오버레이·IIEE 지도 / Ice-edge overlay map with IIEE A⁺/A⁻ shading)
- **무엇을 보여주나**: 모델·기준의 **15% SIC 얼음경계선을 같은 지도에 두 선으로 겹치고**, 두 이진 얼음마스크가 불일치하는 면적을 색으로 음영(A⁺=모델만 얼음 over / A⁻=기준만 얼음 under). IIEE(통합얼음경계오차)를 **눈으로** 보여주는 해빙 특화 대표 그림.
- **읽는 법**: 두 굵은 실선=모델·관측 15% 경계. 음영 두 색: A⁺(모델이 과잉 얼음, 한 색)·A⁻(모델이 부족, 다른 색). 음영 총면적=IIEE; A⁺·A⁻가 서로 감싸는 띠=misplacement(위치어긋남 ME), 한쪽으로 편중된 넓은 음영=absolute extent error(AEE, 범위 편향). *좋은 패턴*: 두 경계선 거의 겹침·음영 얇음. *나쁜 패턴*: 경계선 전 구간 평행 이동(범위 계통편향), 특정 해역만 큰 음영(국지 위치오차·전선 이동).
- **언제 쓰나**: [격자]/[경계] 예보·재현 얼음경계 검증. IIEE 스칼라(⑤)에 공간 맥락을 줄 때. 계절(9월 최소기 음영 급증)·리드타임별.
- **짝지표 & 교차링크**: **IIEE = A⁺+A⁻, AEE=|A⁺−A⁻|, ME=2·min(A⁺,A⁻)** (→ [`24` IIEE 카드]); 거리 환산은 ⑥(MHD·EDE), 확률 확장은 ⑬(SPS), 시계열 분해는 ⑤. FSS(⑮)와 상보(면적 vs 스케일).
- **만드는 법**: 이진 얼음마스크 `I = (sic>=0.15)`; `xarray`로 `over = I_model & ~I_ref`, `under = ~I_model & I_ref`; `cartopy` 극 GeoAxes에 `ax.contourf(lon,lat, over, levels=[0.5,1], colors=['C3'], alpha=0.4)`·`under`(다른 색), 두 경계는 `ax.contour(..., levels=[0.15])`. 면적은 셀면적 가중 합. **해안선/육지+위경도 라벨 필수**(`add_basemap`). 공통격자·동일 임계(15%)·동일 마스크.
- **함정·주의**: **지도 필수**(해안선·라벨). 동일 격자·임계·마스크 아니면 IIEE 계통편향(격자해상도 차→경계 셀 계상차) → 공통격자 재격자화 후. 15% 이진화 정보손실(농도 무시). A⁺/A⁻ 색 규약 캡션 명시. land·pole hole·닫힌 만(inland) 처리 통일. 여러 분리 얼음덩어리 매칭 주의.
- **출처**: Goessling, Tietsche, Day, Hawkins & Jung (2016) "Predictability of the Arctic sea ice edge," *Geophysical Research Letters* 43(4):1642–1650 (doi:10.1002/2015GL067232); Goessling & Jung (2018, *QJRMS* 144:735–743, doi:10.1002/qj.3242, SPS 확장); OSI SAF Sea Ice Edge product.

---

### ★ SIE / SIA 계절곡선 + 시계열 + 잔차 (해빙범위·면적 계절주기·시계열 / SIE/SIA seasonal cycle, time series, residual)
- **무엇을 보여주나**: 반구총계 해빙범위 SIE(15% 임계 면적)·해빙면적 SIA(농도가중 면적)의 (a) **월평균 계절곡선**(climatology, 모델 vs 위성)과 (b) **장기 시계열 + 잔차 패널**. 연주기 진폭·위상(북극 3월 최대·9월 최소)·최소최대 값·추세·계통편차를 본다.
- **읽는 법**: (a) x=월, y=SIE/SIA(10⁶ km²), 두 곡선 겹침; **최소기(9월)·최대기(3월) 각각의 편차**·발생월 어긋남(위상). (b) 시계열 위 패널 두 선 + 아래 잔차(model−ref). *좋은 패턴*: 계절곡선·최소최대 시점 일치, 잔차 0 주위 무작위. *나쁜 패턴*: 여름 최소기만 큰 편차(융빙 물리 오차), 위상 밀림(결빙·융빙 시작 시점 오차), 잔차에 추세/계단(센서 전환 불연속·모델 drift). SIE−SIA 간극=MIZ·박빙 비율 지표.
- **언제 쓰나**: [시계열] 장기 SIE/SIA 지수. 반구·해역별(NSIDC 지역 마스크) 분리. 기후·계절검증.
- **짝지표 & 교차링크**: SIE/SIA bias·RMSE·상관·% 오차·최소최대 시점 오차(→ [`24` SIE·SIA·계절주기 카드]); 시계열 분해·추세·lag는 공통 [`06`], 추세 유의성은 [`01`/`16` bootstrap]. 위치오차는 SIE로 안 보임 → ③/⑤ IIEE 병행 필수.
- **만드는 법**: `xarray`로 SIC→SIE=`(sic>=0.15).weighted(cell_area).sum()`, SIA=`(sic.where(sic>=0.15)*cell_area).sum()`; 계절 climatology `groupby('time.month').mean()`; `matplotlib` 2패널(계절곡선 + 시계열/잔차, `sharex` 시계열). 반구·해역 마스크 분리. **이 그림은 지도 아님**(축=월·시간 × 면적) → basemap 불필요.
- **함정·주의**: **SIE는 위치오차를 못 봄**(잘못된 위치의 얼음도 상쇄되면 SIE 일치) → IIEE/edge 병행(Goessling 2016·Notz 2014). 15% 임계·pole hole·저농도 절단·격자면적 정의를 모델·기준 동일하게(임계 민감). 위성 기록 초기(1979–1987 SMMR) 및 센서 전환 불연속 주의. 단일 계절곡선은 공간 못 봄.
- **출처**: Notz (2014) "Sea-ice extent and its trend provide limited metrics of model performance," *The Cryosphere* 8:229–243; Fetterer et al. NSIDC *Sea Ice Index* v3 (doi:10.7265/N5K072F8, 확인요); Notz et al. (2016) SIMIP (*GMD* 9:3427–3446, doi:10.5194/gmd-9-3427-2016).

---

### IIEE 분해 시계열 (AEE 대 ME / IIEE decomposition time series: absolute extent vs misplacement)
- **무엇을 보여주나**: IIEE를 **절대범위오차 AEE(=SIE 오차의 절댓값)** 와 **위치어긋남 ME(misplacement)** 로 분해해 시간·리드타임·계절축에 쌓은(stacked) 곡선/막대. "SIE는 좋은데 위치가 틀렸는가"를 시계열로 진단. Goessling 2016의 핵심: 기후적으로 ME가 IIEE의 절반 이상.
- **읽는 법**: x=시간(또는 예보 리드타임/월), y=면적(10⁶ km²), 두 성분 stacked(AEE 아래·ME 위, IIEE=합). *읽기*: ME가 크고 AEE 작으면 "범위는 맞지만 위치가 틀림"(SIE만 보면 놓침); AEE가 크면 계통 범위편향. 9월 최소기에 IIEE·ME 급증하는 계절성. *나쁜 패턴*: 리드타임 따라 ME가 AEE보다 빠르게 성장(얼음경계가 SIE보다 덜 예측가능).
- **언제 쓰나**: [격자]/[경계] 예보 검증(리드타임 축)·재현(월/계절 축). ③ 지도의 정량 시계열 짝.
- **짝지표 & 교차링크**: **IIEE·AEE·ME**(→ [`24` IIEE 카드]); 공간 맥락은 ③, 거리 환산은 ⑥, SIE 시계열은 ④. 확률판은 ⑬(SPS).
- **만드는 법**: 각 시각 `A_plus`, `A_minus`(셀면적 가중) → `AEE=abs(A_plus-A_minus)`, `ME=2*min(A_plus,A_minus)` → `matplotlib` `ax.stackplot(time, AEE, ME)` 또는 stacked bar. **지도 아님**(축=시간×면적) → basemap 불필요.
- **함정·주의**: 동일 격자·임계·마스크(격자해상도 차→계통편향). 15% 이진화 정보손실. AEE는 절댓값이라 **방향(과대/과소)** 은 별도(A⁺−A⁻ 부호 또는 ③ 지도로). ME는 위치오차이지 원인 아님 → 원인은 강제력·유변학 분석.
- **출처**: Goessling et al. (2016, *GRL* 43(4):1642–1650, doi:10.1002/2015GL067232); Goessling & Jung (2018, *QJRMS* 144:735–743, doi:10.1002/qj.3242).

---

### 얼음경계 거리오차 요약 그림 (경계 거리오차 박스·막대 / Ice-edge displacement scores: MHD / mean displacement / EDE)
- **무엇을 보여주나**: 모델·기준 얼음경계선 간 **거리(km)** 지표를 해역·계절·리드타임별로 요약(막대·박스플롯). 평균변위 D_AVG, RMS 변위, **Modified Hausdorff Distance(MHD)**, 경계길이 정규화 EDE 등을 함께 표시. IIEE가 면적이라면 이것은 경계선 간 기하학적 거리로 직관적.
- **읽는 법**: x=해역/계절/리드타임 그룹, y=거리(km); 막대=평균, 박스=분포(분위수), 또는 여러 지표 group. *읽기*: MHD·RMS는 최악부 강조(이상치 민감), 평균변위·EDE는 안정적 → 함께 읽어 최악/평균을 분리. *나쁜 패턴*: 특정 해역·계절(여름 MIZ)에서 거리 급증, 순수 Hausdorff가 MHD보다 훨씬 큼(단일 최악점 지배). 수십 km가 단기예보에서 흔함(사례).
- **언제 쓰나**: [경계](15% SIC 등치선 폴리곤) 모델 vs 위성/ice chart. IIEE·FSS와 상보(면적 vs 거리 vs 스케일).
- **짝지표 & 교차링크**: **D_AVG·D_RMS·Hausdorff·MHD·EDE·Melsom 3지표(D_AVG_IE·D_AVG_IIEE·ΔIIEE)**(→ [`24` 얼음경계 거리오차 카드·IIEE 기반 변위 카드]); 면적은 ③/⑤ IIEE, 스케일은 ⑮ FSS, 확률은 ⑬ SPS. 분포 박스는 공통 통계.
- **만드는 법**: 경계 추출 `skimage.measure.find_contours(sic, 0.15)` 또는 `matplotlib` `contour` path → **구면거리**(`pyproj.Geod.inv` 또는 haversine)로 최근접거리; MHD=`scipy.spatial.distance`(directed Hausdorff `scipy.spatial.distance.directed_hausdorff`의 평균화 변형은 직접 구현). 요약은 `matplotlib` bar/`boxplot`. **이 요약 그림 자체는 지도 아님**(축=그룹×km)이나, **경계선 자체를 그리는 보조 지도는 ③에서 basemap 필수**.
- **함정·주의**: 경계 추출·연결성분·연안처리·섬 제거 규칙이 결과 크게 좌우 → 규칙 명시(재현성). **순수 Hausdorff는 단일 최악점 지배**(이상치 민감) → MHD·평균변위 권장(Dukhovskoy 2015·Melsom 2019). 좌표계 거리(구면 vs 투영) 일관. 방향(안/밖)은 별도(IIEE A⁺/A⁻). double counting 주의. 정의(IE 기반 vs IIEE 기반) 캡션 명시.
- **출처**: Melsom, Palerme & Müller (2019) "Validation metrics for ice edge position forecasts," *Ocean Science* 15:615–630 (doi:10.5194/os-15-615-2019); Melsom (2021) "Edge displacement scores," *The Cryosphere* 15:3785–3796 (doi:10.5194/tc-15-3785-2021); Dukhovskoy et al. (2015) "Skill metrics for evaluation and comparison of sea ice models," *JGR Oceans* 120 (확인요 권/페이지); Dubuisson & Jain (1994) MHD 원 정의(*ICPR*).

---

### ★ SIC 검증 산점도 / 밀도 + bounded 진단 (해빙농도 산점도 / SIC validation scatter / density, bounded-variable)
- **무엇을 보여주나**: 콜로케이션된 (기준 SIC, 모델 SIC) 격자쌍을 산점(또는 대용량이면 밀도/hexbin)하고 1:1선·회귀·핵심 스칼라(bias·RMSE·R·N)를 얹은 격자별 농도 정확도 그림. 공통편 산점도(①/②)의 **SIC bounded 변형** — [0,1] 경계에 자료가 쌓이는 구조를 함께 진단.
- **읽는 법**: x=기준 SIC, y=모델 SIC(둘 다 0–1); **1:1선**·회귀선·통계 box. **양극단(0·1)에 점이 축적**되는 것이 bounded 변수의 특징. *좋은 패턴*: 0·1 코너에 밀집 + 대각선 좁게. *나쁜 패턴*: 중간농도(MIZ 대역 0.15–0.8)에서 부채꼴 퍼짐(관측·모델 모두 신뢰도 낮은 구간), 모델이 0/1로 과도 이분(bimodal, 중간농도 과소=경계 급변), 저농도에서 계통 과대(open-water 오탐). N 크면 로그밀도.
- **언제 쓰나**: [격자]vs[격자] 콜로케이션 표본. 정확도+편향 1차 점검. 대용량이면 밀도(hexbin/hist2d).
- **짝지표 & 교차링크**: bias·RMSE·MAE·R(→ [`24` SIC 카드]); 공통편 [`16` 산점도·밀도산점도]·[`01`]. 공간분포는 ②, 분포꼬리는 공통 [`16` QQ]. bounded라 회귀 slope 해석 주의(아래).
- **만드는 법**: `matplotlib` `ax.scatter`(소~중) 또는 `ax.hexbin(o,f, bins='log', mincnt=1)`(대용량); `numpy.polyfit`/`scipy.stats.linregress`; `ax.axline((0,0),slope=1)`; 축 [0,1] 동일·`set_aspect('equal')`. **지도 아님**(축=obs×model) → basemap 불필요.
- **함정·주의**: **SIC는 [0,1] bounded** → OLS/정규분포 가정 지표가 경계에서 왜곡(양극단 잔차 한쪽만 가능, 이분산). robust/직교회귀 병행 고려. 순 bias 0이어도 국지 오차 큼(RMSE·② 지도 병행). 중간농도(MIZ)는 **관측 SIC 자체 불확실성 20–30%**(§G-1) → 모델 탓 단정 금지. 격자 자기상관으로 유효표본 과대(밀도 과신 금지).
- **출처**: 공통편 [`16` 산점도] 출처(Wilks; Jolliffe & Stephenson); Ivanova et al. (2015, *The Cryosphere* 9:1797–1817, SIC 알고리즘 불확실성); OSI SAF / NSIDC SIC CDR 검증보고서.

---

### ★ 해빙 두께 공간 지도 + 차이 지도 (해빙두께 지도 / Sea ice thickness map + difference, CryoSat-2/CS2SMOS/ICESat-2)
- **무엇을 보여주나**: 해빙 두께(m)를 극지도에 채움으로 그리고(모델 vs 위성/병합 CS2SMOS), 그 차(model−ref) 발산 지도를 병치. 두께장의 공간 패턴(중앙북극 후빙·연안 박빙·ridge 대)과 계통오차 위치를 본다.
- **읽는 법**: (a) 두께 순차 색맵(예 viridis/`cmocean.cm.deep`), 모델·관측 두 패널. (b) 차 발산맵(0=흰색). *좋은 패턴*: 후빙 코어 위치·두께 그라디언트 일치, 차 지도 옅음. *나쁜 패턴*: 중앙북극 후빙 과소(모델 흔한 약점)·연안 박빙 과대, 차 지도가 넓은 단색(계통편향), 트랙(위성 sparse) 밖 외삽 artifact.
- **언제 쓰나**: [격자](CS2SMOS L4 월평균·주간) vs 모델 [격자]; [트랙](CryoSat-2/ICESat-2 along-track)은 트랙 위 색 또는 격자화 후. **겨울(10–4월)만** 위성 가용.
- **짝지표 & 교차링크**: 두께 bias·RMSE·R·QQ(→ [`24` 두께 카드]); 두께대별은 ⑨, 분포는 ⑩ ITD, 적분량은 ⑯ SIV. 공간종합은 공통 [`16` bias map]. 적설(snow) 오차 병기(→ [`24` snow depth 카드]).
- **만드는 법**: `xarray`로 두께 로드 → `cartopy` 극 GeoAxes `pcolormesh`(두께 순차맵)·차는 `TwoSlopeNorm(vcenter=0)`+발산맵. 트랙은 `ax.scatter(lon,lat,c=thickness, transform=ccrs.PlateCarree())`. **해안선/육지+위경도 라벨 필수**(`add_basemap`). 겨울 한정·동일 두께정의(정수압 두께 vs draft) 통일.
- **함정·주의**: **지도 필수**(해안선·라벨). **위성 두께는 관측이 아니라 밀도·적설 가정에 의존한 유도량**(§G-1·G-3) → "관측 두께" 과신 금지. 적설 5 cm 오차 = 두께 수십 cm 영향(반드시 병기). 겨울 한정(융빙기 melt pond 산정 불가). 센서 유효두께대 다름(SMOS 박빙/CryoSat-2 후빙) → ⑨ 병행. 트랙 sparse → 격자화·외삽 주의(빈 셀 표시).
- **출처**: Ricker et al. (2017) "A weekly Arctic sea-ice thickness data record from merged CryoSat-2 and SMOS," *The Cryosphere* 11:1607–1623 (doi:10.5194/tc-11-1607-2017, 확인요); Laxon et al. (2013) CryoSat-2 두께(*GRL* 40); Kwok et al. (2020) ICESat-2 두께(*JGR Oceans*, 확인요); Warren et al. (1999) snow depth(*J. Climate* 12:1814–1829).

---

### 두께대별(binned) 두께 검증 산점 (Thickness validation by ice-class: SMOS thin / CryoSat-2 thick)
- **무엇을 보여주나**: 두께 산점/잔차를 **두께 구간별(binned)** 로 나눠, 박빙(<~0.5–1 m, SMOS 강점)·후빙(>~0.5 m, CryoSat-2 강점) 각 대역에서 모델 편향을 분리 진단. 센서 유효두께대가 다르다는 점을 검증 설계에 반영.
- **읽는 법**: 두께 bin(x)별 bias·RMSE 막대/박스, 또는 산점을 bin 색으로. *읽기*: SMOS 대조군에서 박빙 대역, CryoSat-2/CS2SMOS에서 후빙 대역을 주로 신뢰. *나쁜 패턴*: 모델이 후빙 과소·박빙 과대(사례 보고 경향)로 대역별 부호가 갈림 → 평균만 보면 상쇄로 숨음. 대역 경계에서 센서 전환 불연속.
- **언제 쓰나**: [트랙]/[격자] 두께, 센서별 유효대가 다를 때. ⑧ 지도의 정량 대역별 짝.
- **짝지표 & 교차링크**: 두께대별 bias·RMSE(→ [`24` 두께 카드]); 분포 전체는 ⑩ ITD, 지도는 ⑧. 공통 [`16` 오차 히스토그램]·bin 통계.
- **만드는 법**: `scipy.stats.binned_statistic`(두께 bin별 bias·RMSE) 또는 `pandas.groupby(pd.cut(...))` → `matplotlib` bar/`boxplot`. 센서별 대조군 분리. **지도 아님**(축=두께 bin×통계) → basemap 불필요.
- **함정·주의**: 센서 유효두께대 밖 값은 신뢰도 낮음(대역 명시). 적설·밀도 변환가정이 대역별로 다르게 작용. draft↔thickness 변환(ULS/잠수함) 가정 명시. 표본 적은 후빙 꼬리 불안정(CI 권장).
- **출처**: Ricker et al. (2017, *The Cryosphere* 11:1607–1623, CS2SMOS 병합·박빙/후빙 상보); Kaleschke et al. SMOS thin-ice; Laxon et al. (2013, *GRL* 40).

---

### ★ ITD 히스토그램 (해빙 두께분포 / Ice Thickness Distribution g(h) histogram, obs vs model)
- **무엇을 보여주나**: 격자 sub-grid 두께분포 g(h)(CICE 5카테고리 등)의 **카테고리별 면적비**를 막대/계단 히스토그램으로, 관측(항공 OIB·ULS·잠수함 draft 분포)과 나란히. 평균두께가 놓치는 **박빙·후빙(ridge) 꼬리** 구조를 본다.
- **읽는 법**: x=두께 카테고리(m), y=면적비(∫g(h)dh=SIC). 모델·관측 두 히스토그램 대조(막대 나란히 또는 계단 overlay). *좋은 패턴*: 모드 위치·카테고리별 면적비·꼬리 일치. *나쁜 패턴*: 후빙(ridge) 꼬리 과소(ridging 약함), 박빙 카테고리 과대/과소, 분포가 너무 좁음(카테고리 이산화 한계). 평균두께 같아도 분포 다를 수 있음.
- **언제 쓰나**: [격자](모델 ITD) vs [트랙/점](OIB·ULS draft 분포). 역학(ridging/rafting) 진단. multimodal 두께장.
- **짝지표 & 교차링크**: 카테고리별 면적비·분포 형상(모드·꼬리)·QQ(→ [`24` ITD 카드]); 평균/적분은 ⑧·⑯, §04 ridging 보존과 연결. 공통 [`16` PDF/CDF·QQ].
- **만드는 법**: 모델 카테고리별 면적비 직접(`aicen`/`vicen` 등 CICE 진단); 관측 draft/두께 표본은 `numpy.histogram`(동일 카테고리 경계). `matplotlib` `ax.bar`(나란히) 또는 `ax.step`. draft→thickness 변환(≈draft/0.89) 가정 명시. **지도 아님**(축=두께×면적비) → basemap 불필요.
- **함정·주의**: 관측 두께분포 자체 sparse·불확실(트랙/점 표본, 꼬리 불안정). 모델·관측 **규모 정합**(격자분포 vs 트랙표본)·카테고리 경계 통일. 모델 카테고리 이산화(5개 등)로 분포 근사. draft→thickness 변환가정. §04 ridging 보존 교차.
- **출처**: Thorndike, Rothrock, Maykut & Colony (1975) "The thickness distribution of sea ice," *JGR* 80:4501–4513 (확인요); Hibler (1980); CICE Consortium documentation(ITD 구현); Kwok et al. OIB/ICESat-2 두께분포.

---

### ★ 해빙 표류 벡터장 quiver 지도 (해빙 표류 벡터 지도 / Sea ice drift vector (quiver) map, obs vs model)
- **무엇을 보여주나**: 해빙 표류 속도/변위 벡터장을 극지도에 화살표(quiver)로 그려 모델·기준(위성 OSI SAF/NSIDC drift·부이)을 대조. 배경에 속력(색) 또는 차이벡터(model−obs)를 얹어 크기·방향 오차를 공간적으로 본다.
- **읽는 법**: 화살표=표류 벡터(방향·길이=속력), 배경색=속력 또는 차이벡터 크기. 모델·관측 두 패널, 또는 한 패널에 차이벡터. *좋은 패턴*: Beaufort Gyre·Transpolar Drift 등 대순환 패턴·방향 일치. *나쁜 패턴*: 방향 계통회전(바람응력·유변학 오차), 속력 계통 과대/과소, 연안·fast-ice 영역 잘못된 흐름. 차이벡터가 특정 해역에 쏠리면 국지 강제·응력 오차.
- **언제 쓰나**: [벡터][격자] 위성 drift vs 모델; [트랙] 부이 변위 vs 모델 보간. 2일 변위 등 **시간창 일치** 필수.
- **짝지표 & 교차링크**: 성분 bias·RMSE·**벡터 RMSE(VRMSE)**·속력 오차·방향 원형통계(→ [`24` 표류 벡터오차 카드]); 방향은 공통 [`07` 원형통계]·[`10` 복소/벡터상관] 코어, 라그랑지안은 ⑫. 속력장은 ② 스타일 발산 차 지도.
- **만드는 법**: `cartopy` 극 GeoAxes `ax.quiver(lon, lat, u, v, transform=ccrs.PlateCarree(), regrid_shape=..., scale=...)`; 속력배경 `pcolormesh(speed)`. **극projection 벡터 회전 필수**(격자 x/y ↔ 지리 동/북; cartopy는 `transform`+`ccrs.PlateCarree()` 벡터를 회전하나 격자상대 성분이면 사전 회전, §15). 화살표 과밀 방지(`regrid_shape`/서브샘플). **해안선/육지+위경도 라벨 필수**(`add_basemap`). fast ice 제외.
- **함정·주의**: **지도 필수**(해안선·라벨). **벡터 회전 오류가 방향검증을 망침**(흔한 실수) — 격자상대 u/v를 지리 동/북으로 회전. **시간창 일치**(위성 2일 변위 ↔ 모델 2일 적분변위; 순간속도와 혼동 금지). 위성 drift는 시공간 평활 → 점 부이와 대표성오차. 여름 융빙기·저속 위성 추적 실패 많음. 화살표 과밀·scale 임의성(캡션 명시).
- **출처**: Lavergne et al. (2023) "A climate data record of year-round global sea-ice drift from EUMETSAT OSI SAF," *ESSD* 15:5807–5834 (doi:10.5194/essd-15-5807-2023); Lavergne et al. (2010) low-resolution drift(*JGR Oceans* 115, C10032, 확인요); Sumata et al. (2014) drift 상호비교(*JGR Oceans*, 확인요).

---

### 라그랑지안 부이 궤적 지도 + 분리거리 곡선 (Lagrangian buoy trajectory map + separation-distance curve)
- **무엇을 보여주나**: IABP 부이 관측 궤적과 모델 유속으로 적분한 가상궤적을 같은 극지도에 겹치고(궤적 지도), 시간에 따른 **분리거리 s(t)** 를 별도 곡선으로. 라그랑지안 관점의 표류 검증(누적 위치오차·궤적유사도).
- **읽는 법**: (a) 지도: 부이 궤적선 vs 모델 궤적선(같은 시작점, 색=시간). 두 궤적이 갈라지는 지점·방향. (b) 곡선: x=시간, y=분리거리(km), 필연 증가(카오스). *좋은 패턴*: 궤적이 오래 함께·분리거리 완만. *나쁜 패턴*: 초반 급분리(단기 응력오차), 계통적 한쪽 편이(방향 bias), 특정 계절만 큰 분리. 예보 리드타임 대비 평가.
- **언제 쓰나**: [트랙] IABP 부이 vs 모델 유속장 적분. 개별 사례·다수 부이 앙상블. 변형률(deformation) 검증의 정성 짝.
- **짝지표 & 교차링크**: 분리거리 s(t)·정규화 누적 라그랑지안 skill(Liu-Weisberg)·변형률 PDF(→ [`24` 라그랑지안 검증 카드]); 오일러 벡터오차는 ⑪, 궤적 skill은 공통 [`06`]. 변형률 multifractal scaling(neXtSIM 계열).
- **만드는 법**: 모델 유속 시공간 보간(`xarray.interp`) 후 시간적분(RK4/Euler)으로 가상궤적; `cartopy` 극 GeoAxes에 `ax.plot(lon,lat, transform=ccrs.PlateCarree())` 두 궤적; 분리거리는 haversine/`pyproj.Geod`. 곡선은 일반 `matplotlib`. **궤적 지도는 해안선/육지+위경도 라벨 필수**(`add_basemap`); 분리거리 곡선은 지도 아님.
- **함정·주의**: **궤적 지도 basemap 필수**(해안선·라벨). 분리거리는 카오스로 필연 증가 → 예보 리드타임 문맥에서 해석(절대값 아님). 부이 sparse·불균등. 궤적적분 오차 누적(적분법·시간스텝). 변형률은 규모의존(scale-dependent) → 관측·모델 동일 규모. 동일 시작점·시간창.
- **출처**: Rampal et al. (2008) sea ice deformation scaling(*JGR Oceans*, 확인요); Bouchat & Tremblay / Hutter et al. deformation 검증 계열(확인요); Liu & Weisberg (2011) trajectory skill(→ [`06`]); IABP buoy program.

---

### ★ 얼음경계 확률 예보 검증 (확률 ice edge / Probabilistic ice-edge: reliability·ROC·SPS map)
- **무엇을 보여주나**: 앙상블 얼음경계 예보의 격자별 "얼음 확률"을 검증하는 그림 가족 — (a) **reliability diagram**(예측확률 대 관측빈도, 보정), (b) **ROC 곡선**(판별력), (c) **Spatial Probability Score(SPS) 공간 지도**(격자별 (half-)Brier 기여). 계절·subseasonal 해빙예측의 표준.
- **읽는 법**: (a) reliability: 1:1 대각선=완전보정, 아래=과신·위=과소신뢰(+sharpness). (b) ROC: 좌상단으로 부풀면 판별력↑(AUC→1). (c) SPS 지도: 격자별 Brier 기여 색(높을수록 그 위치 확률예보가 나쁨) → 어느 해역에서 확률 얼음경계가 신뢰 낮은지. *좋은 패턴*: reliability 대각선·ROC 좌상단·SPS 지도 옅음. *나쁜 패턴*: 앙상블 과소산포(reliability 과신)·특정 해역 SPS 집중.
- **언제 쓰나**: [격자] 앙상블 SIC/얼음확률 vs 위성 이진 얼음마스크. 계절예측·subseasonal. 결정론이면 SPS→IIEE로 축약(⑤).
- **짝지표 & 교차링크**: **SPS·(damped anomaly persistence 대비 skill)·Brier/BSS·AUC·reliability**(→ [`24` 확률·앙상블 얼음경계 카드]); reliability·ROC·rank hist·Brier 분해는 공통편 [`16` C절]로 교차링크(**여기서 재정의 안 함**), **SPS 공간 지도만 해빙 고유**. 결정론 IIEE는 ③/⑤.
- **만드는 법**: 확률=앙상블 중 `sic>=0.15` 멤버비율; reliability/ROC/Brier는 `xskillscore`(`xs.roc`, `xs.brier_score`)·`sklearn.calibration`(공통편 방법); **SPS 지도**=격자별 `(p_fcst - o)²`(o=관측 이진) → `cartopy` 극 GeoAxes `pcolormesh`(**해안선+위경도 라벨 필수**, `add_basemap`); SPS 스칼라=면적가중 공간적분. damped anomaly persistence 벤치마크로 skill score.
- **함정·주의**: reliability/ROC 카드 함정은 공통편 참조(보정 vs 판별 분리, 자기상관 유효표본). **SPS 지도만 지도 필수**(해안선·라벨). 결정론 단일모델은 확률지표 불가(SPS→IIEE만). 9월 최소기 극단 희소 → Brier/ROC 불안정. **기준예보(damped persistence) 선택이 skill score 좌우**(명시). 동일 격자·마스크·면적가중.
- **출처**: Goessling & Jung (2018) "A probabilistic verification score for contours ...," *QJRMS* 144:735–743 (doi:10.1002/qj.3242); Zampieri, Goessling & Jung (2018) *GRL* 45:9731–9738 (doi:10.1029/2018GL079394); Palerme et al. (2019) *GRL* 46 (doi:10.1029/2019GL082482); Niraula & Goessling (2021) damped anomaly persistence benchmark(*JGR Oceans*, doi 확인요). reliability/ROC/Brier 그림원리는 공통편 [`16`] 출처.

---

### ★ 얼음경계 위도 Hovmöller (edge latitude 시간–경도 도표 / Ice-edge latitude Hovmöller: time–longitude)
- **무엇을 보여주나**: 경도별 15% 얼음경계 위도(edge latitude)를 시간축에 펼친 채움 도표(가로=경도, 세로=시간, 색=경계 위도 또는 model−obs 차). 계절 **전진(advance)·후퇴(retreat)** 의 전파와 위상을 모델·관측에서 나란히 비교.
- **읽는 법**: 가로=경도, 세로=시간(아래로 진행), 색=얼음경계 위도(또는 편차). *읽기*: 색띠의 계절 오르내림=경계의 남북 이동(결빙 남하·융빙 북상); 모델·관측 패널에서 **전진/후퇴 시점·경도별 위상** 일치 확인. 차 패널(model−obs)로 어느 경도·시기에 경계가 밀리는지. *나쁜 패턴*: 특정 경도에서 후퇴가 이르거나 늦음(위상오차), 전진/후퇴 진폭 차. Stammerjohn류 advance/retreat 진단의 전파 버전.
- **언제 쓰나**: [격자] 위성 SIC 시계열 vs 모델(경도별 경계 위도 추출). 계절 위상·전파 진단. 반구별(북극/남극).
- **짝지표 & 교차링크**: advance/retreat day·경계 위도 bias(→ [`24` 시작·소멸일 카드·계절주기 카드]); 전파·위상은 공통 [`16` Hovmöller]로 원리 교차링크(**여기서 재정의 안 함**, 해빙 edge 특화 적용). 면적 시계열은 ④.
- **만드는 법**: 각 경도열에서 15% 교차 위도 추출(`sic` 위도방향 interp로 0.15 crossing) → (경도×시간) 2D 배열 `xr.DataArray.plot.contourf(x='lon', y='time')` 또는 `pcolormesh`; 차는 발산맵 동일 levels. **축이 경도×시간이라 엄밀히는 "지도" 아님**(Hovmöller) → basemap 불필요하나, **경도 규약(0–360 vs −180–180)·반구 명시** 필수. 동일 경도격자·levels로 모델·관측 통일.
- **함정·주의**: Hovmöller이므로 basemap은 없지만 경도 규약·반구를 캡션에 명시(안 하면 좌우 반전). 경계 위도 추출이 다중 얼음덩어리·연안에서 모호(최북/최남 경계 규칙 명시). 색 levels 모델·관측 동일(아니면 가짜 차이). 단일 경도열 평균은 비대칭 전파 가릴 수 있음. 시간 비등간격·결측이 전파 기울기 왜곡.
- **출처**: Hovmöller (1949) "The Trough-and-Ridge diagram," *Tellus* 1(2):62–66 (doi:10.1111/j.2153-3490.1949.tb01260.x, 공통편 [`16`]); Stammerjohn et al. (2012) "Regions of rapid sea ice change," *GRL* 39, L06501 (doi:10.1029/2012GL050874, 확인요, advance/retreat).

---

### FSS 스케일–임계 히트맵 (얼음/무빙 이진장 / FSS scale–threshold heatmap, ice/no-ice)
- **무엇을 보여주나**: "얼음 있음/없음"(SIC≥15%) 이진장의 공간 일치를 **이웃크기(스케일) × 임계** 히트맵으로. 얼음경계의 격자 double-penalty(경계 약간 어긋나면 hit+miss 이중처벌)를 완화해 "어느 공간 스케일부터 유용한가"를 정량화. 공통편 FSS 그림의 **해빙(15% 임계) 적용**.
- **읽는 법**: 가로=이웃반경(km/격자수), 세로=SIC 임계(15% 또는 다중), 색=FSS(0–1); useful-scale 등치선=0.5+f₀/2. *좋은 패턴*: 작은 스케일부터 useful 초과. *나쁜 패턴*: 큰 스케일에서도 낮음(위치·범위 모두 틀림). 곡선형(FSS vs scale, 임계 고정)으로도.
- **언제 쓰나**: [격자] 이진 얼음마스크 예보. IIEE(면적)·MHD(거리)와 상보(스케일 축).
- **짝지표 & 교차링크**: FSS·useful scale·POD/FAR/CSI(→ [`24` FSS·범주형 카드]); FSS 원리·히트맵은 공통편 [`16` FSS 맵]·[`02`]로 교차링크(**여기서 재정의 안 함**, 해빙 15% 임계·극projection 이웃 정의만 주석). 면적은 ③/⑤, 거리는 ⑥.
- **만드는 법**: `pysteps.verification.spatialscores.fss` 또는 `scores.spatial.fss_2d`; 히트맵 `matplotlib.pcolormesh`/`seaborn.heatmap`(임계·스케일 스캔). **극projection에서 이웃(km) 정의 일관**. **히트맵 자체는 지도 아님**(축=스케일×임계)이나 입력 이진장은 공통격자.
- **함정·주의**: 단일 임계·단일 이웃으로 결론 금지(스캔). 극projection 이웃 km 정의 일관(격자 비등간격 주의). 도메인 가장자리·pole hole 패딩 규약 명시. useful-scale 임계는 f₀(사건빈도) 의존 → 계절(빙권 넓은 겨울 vs 좁은 여름)마다 기준선 변동. IIEE·경계거리 병행(면적 vs 스케일 vs 거리).
- **출처**: Roberts & Lean (2008) "Scale-Selective Verification of Rainfall Accumulations...," *Mon. Wea. Rev.* 136:78–97 (doi:10.1175/2007MWR2123.1, 공통편 [`16`]); Melsom et al. (2019, *Ocean Science* 15:615–630, FSS 얼음경계 적용); Palerme et al. (2019, *GRL* 46, 확인요).

---

### SIV / 부피 시계열 + 계절진폭 (해빙 부피 / Sea Ice Volume time series + seasonal amplitude)
- **무엇을 보여주나**: 반구·해역 총 해빙 부피 SIV(=Σ SIC·h·A)의 시계열·계절곡선을 모델과 기준(PIOMAS 재분석·CS2SMOS 유도 부피)과 비교. 두께+농도를 통합한 상태량으로, 두께오차가 크게 반영되는 기후민감 지표.
- **읽는 법**: x=시간/월, y=SIV(10³ km³); 두 곡선 + 잔차. *읽기*: SIV는 SIE보다 추세·기후신호 큼(Notz). 계절진폭·최소기(9월) 값 분리. *나쁜 패턴*: 계통 과소(두께 과소 지배), 계절진폭 차(결빙·융빙 강도 오차), 잔차 추세(모델 drift). 두께오차가 지배 → ⑧ 두께 검증과 함께 해석.
- **언제 쓰나**: [격자]→[시계열] SIV 지수. PIOMAS·위성 유도 부피 대조. 기후·장기검증.
- **짝지표 & 교차링크**: SIV bias·RMSE·상관·계절진폭(→ [`24` SIV 카드]); 두께는 ⑧/⑨/⑩, 면적은 ④. 추세·유의성은 공통 [`06`/`01`].
- **만드는 법**: `xarray`로 `SIV=(sic*thickness*cell_area).sum(['x','y'])` → `matplotlib` 시계열/계절곡선 + 잔차. 반구·마스크 동일. **지도 아님**(축=시간×부피) → basemap 불필요.
- **함정·주의**: **PIOMAS는 관측이 아니라 동화모델 산물, 위성 부피는 두께 불확실성 승계**(§G-1) → "검증"보다 "상호비교" 성격, 과신 금지. 두께·농도 오차가 합쳐져 원인분해 어려움 → 두께(⑧)·SIC(⑦) 개별 병행. 동일 영역·마스크. 계절진폭·최소기 분리 보고.
- **출처**: Zhang & Rothrock (2003) PIOMAS(*Mon. Wea. Rev.* 131:845–861, 확인요); Schweiger et al. (2011) PIOMAS 불확실성(*JGR Oceans* 116, C00D06, 확인요); Notz (2014, *The Cryosphere* 8:229–243).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 24(및 공통 16) 교차링크

| # | 그림 (국문 / English) | 지도? | 자료형 | 검증목적(주축) | 짝 수치지표 | 24 / 16 교차링크 |
|---|---|:---:|---|---|---|---|
| 1 | SIC 지도 + 15% 경계 | ✅ | 격자 | 상태장(정성) | SIC bias·RMSE | 24 SIC · 16 bias map |
| 2 | SIC 차이(bias) 지도 | ✅ | 격자 | 편향+패턴(공간) | 격자 bias·RMSE·R·ACC | 24 격자비교 · 16 bias map · 02·15 |
| 3 | 얼음경계 오버레이 + IIEE 음영 | ✅ | 격자·경계 | 위치(면적) | IIEE·AEE·ME | 24 IIEE · ⑤⑥⑬ |
| 4 | SIE/SIA 계절곡선·시계열·잔차 | ❌ | 시계열 | 범위·위상·추세 | SIE/SIA bias·RMSE·시점오차 | 24 SIE·SIA·계절 · 06·01 |
| 5 | IIEE 분해 (AEE vs ME) | ❌ | 격자·경계 | 범위 대 위치 | IIEE·AEE·ME | 24 IIEE · ③⑬ |
| 6 | 얼음경계 거리오차 (MHD·EDE) | ❌* | 경계 | 거리 | MHD·D_AVG·EDE·ΔIIEE | 24 경계거리·IIEE변위 · ③⑮ |
| 7 | SIC 산점도/밀도 (bounded) | ❌ | 격자 | 정확도+편향 | bias·RMSE·MAE·R | 24 SIC · 16 산점도·QQ |
| 8 | 두께 지도 + 차이 지도 | ✅ | 격자·트랙 | 두께(공간) | 두께 bias·RMSE·R | 24 두께 · 16 bias map |
| 9 | 두께대별(binned) 산점 | ❌ | 트랙·격자 | 두께(대역별) | 두께대 bias·RMSE | 24 두께 · 16 히스토그램 |
| 10 | ITD 히스토그램 g(h) | ❌ | 격자·트랙 | 분포(sub-grid) | 카테고리 면적비·모드·꼬리 | 24 ITD · 16 PDF/QQ · 04 |
| 11 | 표류 벡터 quiver 지도 | ✅ | 벡터·격자 | drift(벡터) | 성분·벡터 RMSE·속력·방향 | 24 drift · 07·10 원형/벡터 |
| 12 | 부이 궤적 지도 + 분리거리 | ✅* | 트랙 | drift(라그랑지안) | 분리거리·궤적 skill·변형률 | 24 라그랑지안 · 06 |
| 13 | 확률 ice edge (reliability·ROC·SPS) | ✅* | 격자 | 확률(보정·판별) | SPS·Brier/BSS·AUC | 24 확률경계 · 16 reliability·ROC |
| 14 | edge latitude Hovmöller | ❌* | 격자 | 위상·전파 | advance/retreat·경계위도 bias | 24 시작소멸일·계절 · 16 Hovmöller |
| 15 | FSS 스케일–임계 히트맵 | ❌ | 격자 | 스케일 유용성 | FSS·useful scale·CSI | 24 FSS·범주형 · 16 FSS · 02 |
| 16 | SIV 시계열 + 계절진폭 | ❌ | 시계열 | 부피(적분) | SIV bias·RMSE·계절진폭 | 24 SIV · 06·01 |

> \* ⑥ 요약 그림은 지도 아님이나 **보조 경계선 지도(③)는 basemap 필수**; ⑫ 궤적 지도·⑬ SPS 지도는 지도 필수(reliability/ROC 부분은 지도 아님); ⑭ Hovmöller는 축이 경도×시간이라 basemap 불필요하나 경도규약·반구 명시.

> **묶음 권고**(§G-6 단일 그림 금지): 해빙 검증 보고는 최소 **①/②(SIC 상태·bias) + ③⑤(얼음경계 면적/위치 IIEE) + ④(SIE/SIA 범위·계절)** 를 기본 세트로, 두께가 중요하면 **⑧⑨⑩⑯**, 표류면 **⑪⑫**, 확률·앙상블 예측이면 **⑬**, 계절 위상·전파면 **⑭**, 스케일 유용성이면 **⑮**를 추가한다. **SIE 하나로 결론 금지**(위치오차 못 봄) — IIEE/edge 반드시 병행. 모든 임계(15%·"겨울 SIC 5–10%" 등)는 **advisory + 계절·해역·관측불확실성 경고**로 캡션에 단다.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·QQ·히스토그램·회귀 등 공통 시각화 — 공통편 [`16`]).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (범주형·ROC·reliability — 공통편 [`16`]·[`24`]).
- WMO, *Sea Ice Nomenclature* (WMO-No. 259) (해빙 유형·MIZ·egg code 용어).

**학술 논문 (제목·저널·연도 웹 확인, DOI 확인분 명기)**
- Goessling, Tietsche, Day, Hawkins & Jung (2016) "Predictability of the Arctic sea ice edge," *Geophysical Research Letters* 43(4):1642–1650. **doi:10.1002/2015GL067232** (웹 확인). — IIEE·분해(AEE/ME).
- Goessling & Jung (2018) "A probabilistic verification score for contours: Methodology and application to Arctic ice-edge forecasts," *Quarterly Journal of the Royal Meteorological Society* 144:735–743. **doi:10.1002/qj.3242** (웹 확인). — SPS.
- Zampieri, Goessling & Jung (2018) "Bright prospects for Arctic sea ice prediction on subseasonal time scales," *Geophysical Research Letters* 45:9731–9738. doi:10.1029/2018GL079394.
- Palerme, Müller & Melsom (2019) "An intercomparison of verification scores for evaluating the sea ice edge position in seasonal forecasts," *Geophysical Research Letters* 46. doi:10.1029/2019GL082482 (권/페이지 확인요).
- Melsom, Palerme & Müller (2019) "Validation metrics for ice edge position forecasts," *Ocean Science* 15:615–630. **doi:10.5194/os-15-615-2019** (웹 확인). — 얼음경계 변위지표·권장 3지표.
- Melsom (2021) "Edge displacement scores," *The Cryosphere* 15:3785–3796. **doi:10.5194/tc-15-3785-2021** (웹 확인). — 경계변위·확장 진단.
- Dukhovskoy et al. (2015) "Skill metrics for evaluation and comparison of sea ice models," *JGR Oceans* 120 (권/페이지·doi 확인요). — Modified Hausdorff 권장.
- Notz (2014) "Sea-ice extent and its trend provide limited metrics of model performance," *The Cryosphere* 8:229–243.
- Notz et al. (2016) "The CMIP6 Sea-Ice Model Intercomparison Project (SIMIP)," *Geoscientific Model Development* 9:3427–3446. doi:10.5194/gmd-9-3427-2016.
- Lavergne et al. (2019) "Version 2 of the EUMETSAT OSI SAF and ESA CCI sea-ice concentration climate data records," *The Cryosphere* 13:49–78. **doi:10.5194/tc-13-49-2019** (웹 확인).
- Lavergne et al. (2023) "A climate data record of year-round global sea-ice drift from EUMETSAT OSI SAF," *Earth System Science Data* 15:5807–5834. doi:10.5194/essd-15-5807-2023.
- Ivanova et al. (2015) "Inter-comparison and evaluation of sea ice algorithms," *The Cryosphere* 9:1797–1817 (doi:10.5194/tc-9-1797-2015, 확인요).
- Ricker et al. (2017) "A weekly Arctic sea-ice thickness data record from merged CryoSat-2 and SMOS," *The Cryosphere* 11:1607–1623 (doi:10.5194/tc-11-1607-2017, 확인요).
- Laxon et al. (2013) "CryoSat-2 estimates of Arctic sea ice thickness and volume," *GRL* 40 (확인요).
- Kwok et al. (2020) ICESat-2 sea ice thickness, *JGR Oceans* (권/페이지·doi 확인요).
- Warren et al. (1999) "Snow depth on Arctic sea ice," *Journal of Climate* 12:1814–1829 (확인요).
- Zhang & Rothrock (2003) PIOMAS, *Mon. Wea. Rev.* 131:845–861 (확인요); Schweiger et al. (2011) *JGR Oceans* 116, C00D06 (확인요).
- Thorndike et al. (1975) "The thickness distribution of sea ice," *JGR* 80:4501–4513 (확인요).
- Stammerjohn et al. (2012) "Regions of rapid sea ice change," *GRL* 39, L06501 (doi:10.1029/2012GL050874, 확인요).
- Roberts & Lean (2008) FSS, *Mon. Wea. Rev.* 136:78–97 (doi:10.1175/2007MWR2123.1); Hovmöller (1949) *Tellus* 1(2):62–66 (doi:10.1111/j.2153-3490.1949.tb01260.x). — 공통편 [`16`] 원리.
- Dubuisson & Jain (1994) "A modified Hausdorff distance for object matching," *Proc. 12th ICPR* (MHD 원 정의).

**기관 자료·기준자료 (실재 URL)**
- EUMETSAT OSI SAF — Sea Ice Concentration / Drift / Edge products & validation: https://osi-saf.eumetsat.int (validation reports: osisaf-hl.met.no).
- NOAA/NSIDC — Sea Ice Concentration CDR, Sea Ice Index, Sea Ice Age, U.S. NIC MIZ: https://nsidc.org
- Sea Ice Prediction Network (SIPN / SIPN South): https://www.arcus.org/sipn
- Copernicus Marine (CMEMS) Sea Ice products & QUID.

**소프트웨어 (실존 도구)**
- `xarray` / `xesmf` — 격자 I/O·재격자화(conservative/nearest, 극격자): https://xesmf.readthedocs.io
- `cartopy` — 극projection 지도(`NorthPolarStereo`/`SouthPolarStereo`)·해안선·gridlines: https://scitools.org.uk/cartopy (→ [`plotting_maps.md`](../../plotting_maps.md) `add_basemap`).
- `cmocean` — 해빙/해양 색맵(`ice`·`balance`·`deep`): Thyng et al. (2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66).
- `scikit-image` (`skimage.measure.find_contours`/`regionprops`) — 얼음경계 추출; `scipy.spatial`(directed Hausdorff)·`pyproj.Geod` — 경계거리.
- `pysteps.verification.spatialscores.fss` / `scores.spatial.fss_2d` — FSS; `xskillscore`(`roc`·`brier_score`·`crps_ensemble`)·`sklearn.calibration` — 확률검증(공통편 [`16`]).
- `matplotlib`, `numpy`, `scipy`(`binned_statistic`·`circmean`/`circstd`), `pandas`.

**확인요 (확정 인용 금지 — §G-5)**
- Ivanova 2015·Ricker 2017·Laxon 2013·Kwok 2020·Warren 1999·Zhang & Rothrock 2003·Schweiger 2011·Thorndike 1975·Stammerjohn 2012·Dukhovskoy 2015·Palerme 2019 — 제목·저널·연도는 확인, 정확한 권·페이지·DOI는 인용 전 원문 재확인(DOI 임의 생성 금지).
- Niraula & Goessling (2021) damped anomaly persistence benchmark — 제목·맥락 확인, 정확한 서지·DOI 확인요.
- **PIOMAS·위성 두께·위성 나이·재분석(ORAS5/GIOMAS)은 관측이 아니라 (동화)모델·유도 산물** → "참값" 아님(§G-1), "reference/reanalysis 대비"로 표기.
- GLORYS 등 재분석의 해빙변수(SIC/두께/drift) 제공 여부·정의는 자료별 확인요(해빙 대조군은 OSI SAF·NSIDC CDR·CS2SMOS·PIOMAS·ORAS5 권장).
- 해석 임계(15% SIE·"겨울 SIC 5–10%"·"MIZ 20–30%"·useful-scale 등)는 **계절·해역·센서 의존 advisory**(§G-3).
</content>
</invoke>
