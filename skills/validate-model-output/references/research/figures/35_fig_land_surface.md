# 검증 시각화 카탈로그 — [육상(지표) 도메인편] (Verification Figures: Land Surface)

이 문서는 육상면 모델·재분석 산출물(CLM/Noah-MP/JULES/ORCHIDEE, ERA5-Land/GLDAS/MERRA-2-Land, 위성 소산물)을 **지상관측망(토양수분망 ISMN·flux tower FLUXNET·SNOTEL)·위성(마이크로파·열적외 TIR·광학)·재분석**과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 육상 도메인편이다. 메서드(수치지표) 카드는 [`27_domain_land_surface.md`](../27_domain_land_surface.md)에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **대응 메서드카탈로그: `27_domain_land_surface.md`** (이 파일의 모든 그림은 27의 메서드 카드와 짝지어 읽는다.)

> **공통/횡단 그림과의 분담**: Taylor·Target·일반 QQ·PDF/CDF·reliability·rank histogram·ROC·성능다이어그램 등 **도메인 무관 요약그림은 [공통편 `16_fig_common.md`] 담당**이라 여기서 중복 정의하지 않는다. 이 파일은 **육상 고유 그림**(토양수분 이상 시계열, 삼중대조 오차막대, ubRMSD/anomaly-R 지도, LST 일변동, ET 에너지수지 산점, SWE+SCA, 물후 LAI 계절)과 **공통 그림의 육상식 변형**(bias map을 anomaly-R/ubRMSD로 색칠, EF/EBR box를 얹은 산점 등)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "교차링크"에서 가리킨다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3·L4) · [정점]=관측소·타워 시계열(ISMN·FLUXNET·SNOTEL CSV/텍스트) · [트랙/스와스]=위성 궤도(soil moisture retrieval·LST L2) · [프로파일]=토양 깊이별.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** ISMN·FLUXNET·위성·ERA5-Land는 모두 reference이지 truth가 아니다. 축 라벨·캡션에 "모델 − 기준(reference)"으로 쓰고 "오차"로 단정하지 않는다. (특히 FLUXNET ET/GPP·타워 EBR은 **관측 자체가 불확실**하다.)
> 2. **점 관측 ≠ 격자 화소.** ISMN 센서(수십 cm²)·타워 발자국(수백 m)·SNOTEL 지점 vs 격자(수 km)의 **대표성 오차(representativeness error)** 가 산점·잔차에 섞인다. 큰 검증차가 모델 탓이 아닐 수 있다(§G-1).
> 3. **해석 임계는 advisory.** `ubRMSD~0.04 m³/m³`, `anomaly-R 0.3~0.7`, `EBR 0.7~0.9`, `SCA F1 높음` 등은 **관행/미션요구값**이며 피복·계절·해상도·기준자료 의존. 그림에 "good/bad"를 단정 표기하지 말고 영역·계절 의존 경고를 캡션에 둔다.
> 4. **단일 그림 금지.** 산점도(정확도) 하나로 결론내지 말고 최소 **정확도+편향+분포/패턴** 3축과 유의성(부트스트랩, 유효표본수 보정)을 함께 낸다.
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문의 도판을 그대로 재현하지 않는다.
> 6. ★ **지도형(위경도) 그림은 반드시 해안선/육지 + 위경도 라벨**을 넣는다 → [`plotting_maps.md`](../../plotting_maps.md)의 `add_basemap()` 사용. 정점(관측소) 그림은 위치 지도 + 마커 + ID 라벨.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **토양수분 시계열 overlay + 이상(anomaly) 패널** — 계절성 제거 후 건·습 이벤트 재현력
2. ★ **토양수분 삼중대조(TC/ETC) 오차막대** — 참값 없는 시스템별 오차분산·SNR
3. ★ **anomaly-R / ubRMSD 공간 지도 (basemap)** — 토양수분 검증지표의 지리분포
4. **CDF 매칭 전후 진단 (분포·시계열 overlay)** — 재척도화 정당성 점검
5. ★ **LST 일변동(diurnal) 곡선 + 주야 산점** — 지표온도 위상·주야 조건부 편향
6. ★ **ET 에너지수지 산점 (H+LE vs Rn−G) + EBR** — 난류플럭스 닫힘·에너지 배분
7. **증발분율(EF)/Bowen비 일변동·계절 곡선** — ET vs 가열 분할 오차
8. ★ **SWE 시계열 + 융설 타이밍 (정점·표고 층화)** — 눈 저장량·눈 위상
9. ★ **SCA 범주검증 지도 (hit/miss/false, basemap) + 성능요약** — 눈/무눈 이진 분류
10. ★ **식생 계절곡선 (LAI/NDVI phenology, SOS/EOS)** — 식생량 계절 위상·진폭
11. ★ **GPP 검증 산점 + 계절곡선 (PFT 층화)** — 탄소흡수 플럭스 (분할가정 주의)
12. **알베도 검증 산점/시계열 (blue/white/black-sky)** — 단파 반사율·눈-알베도 되먹임
13. ★ **격자-격자 bias / difference 공간 지도 (basemap)** — 재분석 대비 면적 계통오차
14. ★ **관측소 위치 지도 (station map + ID)** — 정점 검증의 위치 식별
15. **피복·PFT 층화 성능 그림 (grouped bar / heatmap)** — 조건부 강·약점
16. **토양온도·동결 프로파일 시계열 (깊이-시간 히트맵)** — 열상태·위상지연

---

### ★ 토양수분 시계열 overlay + 이상(anomaly) 패널 (토양수분 시계열·이상 도표 / Soil moisture time-series overlay + anomaly panel)
- **무엇을 보여주나**: 한 정점(또는 격자셀)에서 모델·관측(ISMN)·위성(SMAP/ASCAT) 토양수분 θ(m³/m³)를 **시간축에 겹쳐** 그리고, 아래 패널에 **이상(anomaly) δθ**(이동창 기후값 제거)를 둔다. 원자료 overlay는 **계절 순환**을, anomaly 패널은 **단기 건조·강수 이벤트(short-term drying/wetting)** 재현력을 분리해 보여 준다.
- **읽는 법**: 위 패널 x=시간, y=θ. 두 선의 **계절 진폭·평균 offset**(계통 습/건 bias) 확인. 아래 패널 δθ가 강수·건조 사건에서 **모델·관측이 같은 부호로 함께 튀면** 이벤트 재현 양호(anomaly-R 높음). *나쁜 패턴*: 원자료는 붙어 보이나(공통 계절성) anomaly가 무상관(단기 응답 실패), 동결기·강우 직후 스파이크 불일치, 재척도화 안 해서 동적범위 계통차. 강수(막대)·동결 플래그를 배경에 얹으면 가독.
- **언제 쓰나**: [정점]/[격자]/[트랙] 표층·근권(root-zone) 토양수분. 계절성 강한 지역에서 원자료 R가 과대일 때 이상 성분으로 진짜 스킬 진단.
- **짝지표 & 교차링크**: **anomaly-R, 원자료 R, ubRMSD, bias** → [27 토양수분 이상상관/ubRMSD 카드]. 시계열 위상·lag은 공통 [16 §E 시계열 overlay+잔차·lag·STL], 다지점 요약은 [16 Taylor]. 분포는 [16 QQ]. bias/RMSE 정의는 [01].
- **만드는 법**: `pandas`/`xarray` 시간정렬 → **`pytesmo`** `pytesmo.time_series.anomaly.calc_anomaly`(이동창 기후값) 또는 `calc_climatology`로 δθ 산출 → `matplotlib` 2-패널(`sharex`). 재척도화는 `pytesmo.scaling`(cdf_match/linreg). 결측 구간은 끊어 그림(직선보간으로 잇지 말 것 — 이벤트 통계 왜곡).
- **함정·주의**: 이상 정의(**창 길이·최소 표본**)에 민감 → 모델·관측 동일 규약. **표층↔근권 심도 혼용 금지**(위상·진폭 오인) → [27 토양층 정합]. 동결기·RFI 오염기는 위성·모델 신뢰 급락(마스킹). 자기상관 커서 유효표본수 작음(유의성 보정). 지도 아님(축=time×θ) → basemap 불필요.
- **출처**: Gruber et al. (2016) "Recent advances in (soil moisture) triple collocation analysis," *Int. J. Applied Earth Observation and Geoinformation (IJAEO)* 45:200–211; Dorigo et al. (2011, *HESS*, ISMN); Albergel et al. (2008, *HESS*, root-zone from surface, SWI); `pytesmo` 문서(pytesmo.readthedocs.io, anomaly/climatology).

---

### ★ 토양수분 삼중대조(TC/ETC) 오차막대 (삼중대조 오차 도표 / Triple-collocation error-standard-deviation & SNR bar plot)
- **무엇을 보여주나**: 세 독립 자료(위성 retrieval·모델/재분석·지상 in-situ)의 **개별 무작위 오차 표준편차 σ_ε(m³/m³)** 와(ETC면) **진값 대비 상관/SNR**을 막대/표로 시각화. 절대 참값(truth) 없이 "어느 자료가 더 정확한가"를 객관 표시. 육상에서 TC가 가장 성숙한 곳이 토양수분.
- **읽는 법**: 막대=각 시스템 σ_ε(낮을수록 정확). *흔한 패턴*: in-situ가 최소 오차이나 **대표성 오차 때문에 항상 그렇지는 않음**. ETC면 SNR(dB)도 병기. 피복·기후대·계절 bin별로 막대를 나누면 조건부 오차구조. *주의 패턴*: 재분석과 모델이 **같은 지면모형/강수 강제**를 공유하면 오차상관으로 막대가 비현실적으로 낮게(가정 위배). 부트스트랩 신뢰구간(에러바) 필수.
- **언제 쓰나**: [트랙/스와스](위성)+[격자](모델/재분석)+[정점](ISMN) 공통 콜로케이션이 충분할 때. 기준 없는 오차 진단·자료 신뢰 랭킹.
- **짝지표 & 교차링크**: **TC/ETC 오차분산·scaling β·SNR·fRMSE** → [27 토양수분 삼중대조 카드]. TC/ETC 코어 가정·수식은 [12]·[15]. 파랑/위성 도메인 TC 시각화와 형제(공통 접근). anomaly 공간 수행 권장(계절 공통성분 배제).
- **만드는 법**: **`pytesmo`** `pytesmo.metrics.tcol_metrics`(또는 `tcol_error`)로 σ_ε·SNR 산출 → `matplotlib` `ax.bar` + 부트스트랩 CI. 콜로케이션·rescaling은 `pytesmo.scaling`. bin은 `scipy.stats.binned_statistic`. 지도 아님(축=시스템×σ) → basemap 불필요.
- **함정·주의**: **핵심 가정 = 세 자료 오차 독립·진값과 무상관·정상성.** 육상 위반요인: (a) 두 위성/모델이 같은 강수·보조자료 공유, (b) 재분석·모델이 같은 지면모형 계열 → **오차 상관으로 σ_ε 편향**(§G-2,3). **동화·보간 산물(재분석·L4)을 독립 3자로 넣지 말 것**(§G-3). 표본·rescaling 방법에 민감. 공통 동적범위 필요.
- **출처**: Gruber et al. (2016, *IJAEO* 45:200–211, TC 리뷰); Stoffelen (1998, *JGR* 103(C4), TC 기초); McColl et al. (2014, *GRL* 41(17):6229–6236, doi:10.1002/2014GL061322, ETC); Gruber et al. (2020, *Remote Sensing of Environment*, SM 검증 good-practice); CEOS LPV *Soil Moisture Validation Good Practices Protocol* (v1, 2020); `pytesmo` `metrics.tcol_metrics`.

---

### ★ anomaly-R / ubRMSD 공간 지도 (토양수분 검증지표 지도 / Anomaly-R & ubRMSD spatial map, basemap)
- **무엇을 보여주나**: 격자 전면적으로 토양수분 검증지표(**anomaly-R, ubRMSD, bias, TC 오차**)를 격자셀마다 계산해 **지도(색)** 로. 관측 희소지역까지 **계통오차·스킬의 지리분포·계절성**을 진단(예: 밀림·복잡지형·동결기·건조초지에서 anomaly-R 대비).
- **읽는 법**: 색 = 각 격자셀 지표값. **anomaly-R/상관은 순차맵(0~1, viridis)**, **bias는 발산맵(0=흰색, RdBu_r/cmocean balance)**, **ubRMSD/RMSE는 순차맵(비음수, cmocean amp)**. *읽기*: 건조·초지에서 anomaly-R 높고, **밀림·복잡지형·RFI·동결대에서 낮음**(정상). ubRMSD가 특정 피복대에 몰리면 조건부 약점. *나쁜 패턴*: 넓은 단색 bias 영역(계통편차), 해안선/피복 경계 줄무늬(재격자·마스크 artifact).
- **언제 쓰나**: [격자]vs[격자]/[트랙] 광역 진단, 점 검증(카드14 위치도)이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 격자별 **anomaly-R·ubRMSD·bias·TC σ_ε** → [27 토양수분 이상상관/ubRMSD/TC 카드]. 공간패턴 코어는 [02], 재격자·마스크는 [15]. bias map 공통형은 [16 §B bias/difference map].
- **만드는 법**: `xarray`로 격자별 시계열 지표 산출(`pytesmo` 지표를 `xr.apply_ufunc`/`groupby`로 격자에 확장) → `cartopy`/`matplotlib` `pcolormesh`. ★ **지도이므로 `plotting_maps.md`의 `add_basemap(ax, lon, lat)`으로 해안선/육지+위경도 라벨 필수.** bias는 `TwoSlopeNorm(vcenter=0)`+발산맵, ubRMSD는 순차맵. **육지 마스크·경도 규약(0–360→−180…180) 통일**.
- **함정·주의**: ★ basemap 없으면 "어디인지" 못 읽음 → 해안선+라벨 강제(offline이면 fallback graticule). **재분석은 독립 진값 아님**(자체 오차·동화) → 지상/위성과 교차. 격자 해상도 차(ERA5-Land ~9 km vs GLDAS ~0.25°)가 차이의 상당부분. anomaly-R 지도는 계절·창정의 의존(캡션 명시). 격자 자기상관으로 유의성 과신 금지.
- **출처**: Gruber et al. (2020, *RSE*, SM good-practice); Draper et al. (2013, *GRL*, SMOS/ASCAT vs model); Muñoz-Sabater et al. (2021, *ESSD* 13, ERA5-Land); 공간비교 코어 [02]; basemap 규칙 [`plotting_maps.md`].

---

### CDF 매칭 전후 진단 (재척도화 진단 / CDF matching before/after diagnostic)
- **무엇을 보여주나**: 검증 전 자료 간 동적범위·분산·비선형 척도차를 제거하는 **재척도화(CDF/quantile matching)** 의 정당성을 (a) 매칭 전후 **CDF/PDF overlay**, (b) 매칭 전후 **시계열/산점 overlay**로 진단. 토양수분처럼 자료마다 단위·범위가 다른 변수의 필수 전처리 점검.
- **읽는 법**: (a) 매칭 후 두 CDF가 겹치면 척도차 제거 성공. (b) 매칭 후 시계열이 **동적범위는 맞고 위상·이벤트 구조는 보존**돼야 정상. *나쁜 패턴*: 매칭이 이벤트(anomaly) 정보까지 지워 시계열이 평활, 짧은 표본 CDF가 계단·과적합. **매칭이 bias를 "좋게 만든" 것으로 오해 금지**(비교 가능하게만 함).
- **언제 쓰나**: [트랙]/[격자]/[정점] 토양수분(주), 필요시 LST·ET. anomaly-R·ubRMSD 산출 직전 전처리 점검.
- **짝지표 & 교차링크**: 매칭 후 **anomaly-R·ubRMSD**(카드1,3) → [27 CDF 매칭/재척도화 카드]. quantile mapping 코어는 [13]·[15]. 분포 비교는 [16 QQ/PDF/CDF].
- **만드는 법**: **`pytesmo`** `pytesmo.scaling.scale(..., method='cdf_match'/'linreg'/'mean_std'/'min_max')` → 매칭 전후를 `scipy.stats`/`numpy` ECDF·`matplotlib` overlay. **학습기간·검증기간 분리**(과적합 방지). 지도 아님 → basemap 불필요.
- **함정·주의**: 매칭이 계통오차를 감춰 **모델 문제를 은폐**할 수 있음(bias는 별도 보고). 짧은 표본 CDF 불안정. anomaly 검증 시 매칭이 실제 오차정보까지 지우지 않게 주의. §G-6.
- **출처**: Reichle & Koster (2004, *GRL*, CDF matching for SM); Gruber et al. (2020, *RSE*, rescaling 비교); `pytesmo.scaling` 문서. 공통 QM 코어 [13].

---

### ★ LST 일변동(diurnal) 곡선 + 주야 산점 (지표온도 일변동·주야 도표 / LST diurnal cycle curve + day/night scatter)
- **무엇을 보여주나**: 지표온도(LST, skin temperature)의 **일변동(하루 24h) 곡선**을 모델·위성/지상 실측으로 겹쳐 그리고, **주간/야간 통과시각(예: MODIS/VIIRS 10:30/22:30)** 매치업을 별도 산점으로. 주간 첨두·야간 최저의 진폭·위상, 주야 조건부 bias를 본다.
- **읽는 법**: 위 곡선 x=시각(local), y=LST(K). 두 곡선의 **주간 첨두 높이·시각**(진폭·위상), 야간 최저 offset 비교. *나쁜 패턴*: 모델이 주간 첨두 과소(열관성·증발 배분 오류), 야간 과대(장파·안정경계층). 주야 산점(카드6 양식)에서 **주간·야간 bias 부호가 반대**면 일변동 진폭 오류. **위성은 청천(clear-sky)·통과시각만 표집** → 모델을 동일 마스크로 표집해야 공정.
- **언제 쓰나**: [트랙/스와스](MODIS L2/VIIRS)·[격자](L3/L4·모델 skin T) vs [정점](flux tower·전용 LST 사이트). 열적으로 균질한 사이트에서 T-b 검증.
- **짝지표 & 교차링크**: **LST bias·RMSE·상관**(주야 분리) → [27 LST T-b/R-b·주야·청천 표집편향 카드]. bias/RMSE 정의는 [01], 시계열 위상은 [16 §E]. 공간 bias는 카드13.
- **만드는 법**: `pandas` groupby(시각)로 diurnal 합성곡선; 위성 통과시각·청천 QC로 **모델을 동일 표집(sampling mask)** 후 주야 산점(`matplotlib` `ax.scatter`+1:1+bias box). 지상 LST는 4성분 복사에서 `LST=[(L↑−(1−ε)L↓)/(εσ)]^{1/4}`. 지도 아님(축=time/LST) → basemap 불필요(단 사이트 위치는 카드14 인셋으로 동반).
- **함정·주의**: **T-b는 열적 균질(단일성분) 피복에서만 유효** — 이질피복·경사면·건조지 정오에 급악화(대표성 오차). 방출률 ε·각도(view zenith)·시각 정합 필수. **청천·주간 표집은 계통적으로 더 따뜻·건조한 표본** → 표집 마스크 없이 bias 해석 금지. 구름 잦은 지역 유효표본 급감.
- **출처**: Coll et al. (2009) "Temperature-based and radiance-based validations of the V5 MODIS LST product," *JGR: Atmospheres* 114, D20102 (doi:10.1029/2009JD012038); Wan (2014, *RSE*, MODIS C6 LST); Guillevic et al. (2018, GSICS/CEOS LST Validation Best Practices); Duan et al. (2019, *RSE*, R-b over heterogeneous surfaces).

---

### ★ ET 에너지수지 산점 (H+LE vs Rn−G) + EBR (에너지수지 닫힘 산점 / Energy-balance-closure scatter + EBR)
- **무엇을 보여주나**: 지표 에너지수지 정합을 **가용에너지 (Rn−G)** 대 **난류플럭스 (H+LE)** 산점으로 그리고, **회귀기울기·절편·닫힘비 EBR = Σ(H+LE)/Σ(Rn−G)** 를 박스로. flux tower의 EC 관측 신뢰도 진단이자, 모델 에너지 배분(잠열 LE↔ET) 검증의 필수 동반 그림.
- **읽는 법**: x=Rn−G, y=H+LE, **1:1선 + OLS 회귀선**. 이상적 EBR=1·기울기=1·절편0. *실측 전형*: 점운이 1:1 아래로 눕고 **기울기 ~0.74(미보정)~0.87(보정)**, EBR ~0.7~0.9(**불닫힘 10~30%**). *읽기*: 관측 불닫힘은 EC 자체 문제(저저장·이류·발자국)일 수 있음 — "모델이 관측보다 낫다"로 오독 금지. **모델은 정의상 닫힘(EBR≈1)** 이므로 관측과 비교 시 불닫힘을 감안. 계절·시간규모(반시간~일)별로 점 색 구분.
- **언제 쓰나**: [정점] flux tower(관측 닫힘 진단)·[격자] 모델(내적 에너지수지). ET/LE 검증 보고에 반드시 동반.
- **짝지표 & 교차링크**: **EBR·회귀기울기/절편·잔차(Rn−G−H−LE)** → [27 에너지수지 닫힘(EBR)·Bowen비 프레이밍 카드]. ET/LE 정확도 산점은 [16 §A 산점도], 성분 복사는 [27 방출률/Rn]. 04(수지 닫힘) 교차.
- **만드는 법**: `pandas`로 반시간 Rn·G·H·LE 정렬 → `matplotlib` `ax.scatter`(계절/주야 색) + `scipy.stats.linregress`(기울기·절편·R) + EBR 텍스트박스. 저장항(캐노피·G 저장) 처리방식 캡션 명시. 지도 아님(축=에너지) → basemap 불필요.
- **함정·주의**: 관측 **불닫힘 원인(저저장·이류·footprint 불일치)이 미결** → "모델이 낫다" 오독 금지(관측 자체 오차, §G-1). **닫힘 보정 프레이밍**(Bowen-ratio 배분 / LE-only / 미보정)이 ET bias를 수~수십 % 이동시킴 → 반드시 명시·민감도 병행(카드7·[27 Bowen비 카드]). footprint(수백 m)≠격자(수 km) 대표성.
- **출처**: Wilson et al. (2002) "Energy balance closure at FLUXNET sites," *Ag. For. Meteorol.* 113(1–4):223–243; Foken (2008, *Ecological Applications*, closure problem); Stoy et al. (2013, *Ag. For. Meteorol.*, 다지점 닫힘); Twine et al. (2000, *Ag. For. Meteorol.*, Bowen-ratio closure). 다지점 사례 기울기 ~0.74→0.87(보정).

---

### 증발분율(EF)/Bowen비 일변동·계절 곡선 (에너지 분할 곡선 / Evaporative fraction / Bowen-ratio diurnal & seasonal curves)
- **무엇을 보여주나**: 가용에너지가 증발(LE)과 가열(H)로 나뉘는 비율 — **증발분율 EF = LE/(H+LE)** 또는 **Bowen비 β = H/LE** — 의 일변동·계절 곡선을 모델·관측으로 비교. ET 총량이 맞아도 **분할(partitioning)이 틀리면** 지면-대기 되먹임이 왜곡되므로 총 ET 검증을 보완.
- **읽는 법**: x=시각(일변동) 또는 월(계절), y=EF(0~1) 또는 β. *읽기*: EF 일변동은 정오 근처 평탄(midday self-preservation). *나쁜 패턴*: 모델이 건조/습윤 전이대·관개지에서 EF 과대/과소(수분제어 vs 에너지제어 레짐 오류). 토양수분–EF 산점으로 레짐 진단 병행.
- **언제 쓰나**: [정점] EC vs [격자] 모델. 지면-경계층 결합·물에너지 배분 진단.
- **짝지표 & 교차링크**: **EF·β bias·상관** → [27 LE/H 플럭스 분할(EF) 카드]. 닫힘 프레이밍은 카드6·[27 Bowen비]. 총 ET 정확도는 [16 §A 산점]. 04(에너지수지 성분) 교차.
- **만드는 법**: `pandas`로 EF=LE/(LE+H) 계산(닫힘 보정 프레이밍 명시) → groupby(시각/월) 곡선 `matplotlib`. midday(예: 10–14h)만 EF 안정구간 사용 권장. 지도 아님 → basemap 불필요.
- **함정·주의**: 저에너지(야간·이른 아침) EF는 분모가 작아 불안정 → midday 필터. **닫힘 보정 가정**이 EF를 이동(카드6). 총 ET만 검증하면 분할 오차 은폐(§G-6).
- **출처**: Gentine et al. (2007, *Ag. For. Meteorol.*, EF·diurnal self-preservation); Dirmeyer et al. (2018, land-atmosphere coupling metrics); Twine et al. (2000, *Ag. For. Meteorol.*).

---

### ★ SWE 시계열 + 융설 타이밍 (적설수당량 시계열·눈 위상 / SWE time-series + melt-out timing, elevation-stratified)
- **무엇을 보여주나**: 모델·재분석·위성 SWE(눈 저장 물량, mm)를 지상 관측(SNOTEL·snow pillow·snow course)과 **시계열로 겹쳐** 그리고, **적설 개시일·최대 SWE·완전 융설(melt-out)일** 을 표시. 융설 수자원·수문 타이밍의 핵심 검증. 표고대별로 여러 패널(층화).
- **읽는 법**: x=시간(수문년), y=SWE. *읽기*: 축적기 기울기(강설), 최대 SWE, 봄 융설 소멸 시각 비교. *나쁜 패턴*: 모델 최대 SWE 과소(산악·삼림), **융설 며칠~수주 조기/지연**(봄 강제·알베도 되먹임), 수동마이크로파 위성 SWE가 깊은 눈/삼림/습설에서 포화·과소. 개시·melt-out 날짜 bias(일)를 연도별 산점으로 병기.
- **언제 쓰나**: [정점] SNOTEL/snow course·[격자] 모델/재분석/위성 SWE. 표고·피복 층화(SWE는 표고 강의존).
- **짝지표 & 교차링크**: **SWE bias·RMSE·상관, 개시/melt-out 타이밍 bias(일)** → [27 SWE 검증·적설 소멸/개시 타이밍 카드]. 변화점·위상은 [06]. 눈 저장은 SCA(카드9)·TWS와 묶음.
- **만드는 법**: `pandas`/`xarray` 시계열 overlay(`matplotlib`); 개시=SWE>임계(예 10mm) 최초, melt-out=최종 초과일. **표고대별 subplot**(격자 평균표고 보정). SWE=깊이×밀도 유도 시 밀도 가정 명시. 시계열 자체는 지도 아님이나, **정점 위치는 카드14 station map + 인셋으로 동반**(표고 라벨).
- **함정·주의**: 점 SWE의 **대표성 오차 극심**(바람 재분포·수관 차단) → 관측점이 격자 대표 못하면 큰 차이가 정상(§G-1). 수동마이크로파 SWE는 깊은 눈에서 포화. 표고 정합이 최대 통제변수. 임계·재적설(re-accumulation) 처리 규칙 명시.
- **출처**: Mortimer et al. (2020, *The Cryosphere*, gridded SWE product 평가); Broxton et al. (2016, *J. Hydrometeorol.*, SWE 관측 대표성); Wrzesien et al. (2019, *GRL*, mountain SWE); Trujillo & Molotch (2014, *WRR*, melt timing).

---

### ★ SCA 범주검증 지도 (적설면적 hit/miss/false 지도 / Snow-Covered-Area categorical map + performance summary, basemap)
- **무엇을 보여주나**: "화소가 눈인가/아닌가" 이진 분류를 모델·위성이 맞히는지 — 격자셀을 **hit(둘 다 눈)·miss(관측만 눈)·false alarm(모델만 눈)·correct-neg(둘 다 무눈)** 4색으로 칠한 **범주 지도** + 성능요약(POD·FAR·F1·overall accuracy). 눈/무눈 2×2 분할표의 공간 시각화.
- **읽는 법**: 색 = 4범주(예: 파랑=hit, 빨강=false, 주황=miss, 회색=corr-neg, 흰색=구름). *읽기*: miss/false가 **삼림·구름·전이기(부분적설)·지형그림자**에 몰리면 그 조건의 약점. 요약값(공개 사례 **MODIS POD ~0.95·FAR ~0.18**, Landsat 검증 F1 사례 높음)은 개방지 기준 — 삼림/구름/부분적설에서 급락. *나쁜 패턴*: 설선(snowline) 따라 miss+false 쌍(double-penalty: 위치 약간 어긋남).
- **언제 쓰나**: [격자] 모델/위성 SCA(MODIS/VIIRS snow map) vs 기준(고해상 위성·lidar·지상). 눈/무눈 이진 검증.
- **짝지표 & 교차링크**: **POD·FAR·precision·recall·F1·overall accuracy** → [27 SCA 범주검증 카드]. 범주형 코어(POD/FAR/CSI/HSS)·성능다이어그램은 [03]·[16 §C 분할표 viz & Performance diagram]. 연속 SCF·설선고도는 [27 적설 진단]. bias map은 카드13.
- **만드는 법**: `xarray`/`numpy`로 이진화(적설분율→임계) 후 4범주 코드 → `cartopy` `pcolormesh`(이산 색맵). ★ **지도이므로 `add_basemap(ax, lon, lat)`으로 해안선/육지+위경도 라벨 필수**(DEM 등고선 얹으면 설선 가독). 지표는 `scipy`/`numpy` 또는 `xskillscore` 이진지표. **구름 화소는 별도 색**(눈 판정 불가).
- **함정·주의**: ★ basemap+표고 없으면 "어디·어느 고도" 못 읽음. **구름·삼림 차폐가 최대 오차원**(구름은 별도 처리, 눈으로 세지 말 것). double-penalty(설선 어긋남). 이진화 임계 민감(캡션 명시). 기준자료(위성)도 오차 포함(§G-1). F1/POD는 개방지·해상도 의존 advisory.
- **출처**: Salomonson & Appel (2004, *RSE*, MODIS fractional snow); Hall & Riggs (2007, *Hydrol. Processes*, MODIS snow 정확도); Stillinger et al. (2023, *The Cryosphere*, lidar 검증 F1); Rittger et al. (2021, *Frontiers in Remote Sensing* 2:647154, VIIRS/MODIS SCF in High-Mountain Asia). 범주형 코어 [03]; basemap [`plotting_maps.md`].

---

### ★ 식생 계절곡선 (LAI/NDVI 물후 / Vegetation seasonal curve: LAI/NDVI phenology, SOS/EOS)
- **무엇을 보여주나**: 모델·위성 LAI(m²/m²) 또는 NDVI/EVI의 **연중 계절곡선(climatology + 개별연도)** 을 겹쳐 그리고, **개엽(SOS)·낙엽(EOS)·생장기간(LOS)** 시점을 표시. 광합성·증발산·복사 배분을 좌우하는 식생 상태의 **계절 위상·진폭** 재현을 본다(절대값 비교보다 견고).
- **읽는 법**: x=day-of-year/월, y=LAI 또는 NDVI. *읽기*: 봄 상승 기울기(개엽 속도)·여름 최대(진폭)·가을 하강(낙엽) 비교. SOS/EOS 마커의 날짜 차 = 물후 타이밍 bias. *나쁜 패턴*: 모델 SOS 조기/지연(며칠~수십일), 여름 최대 과대/과소, **상록림에서 물후 신호 약함**. **고LAI 상록/밀림에서 위성 LAI 포화(saturation)로 과소**. NDVI는 고식생 포화·눈/구름 겨울 왜곡 → EVI 보완.
- **언제 쓰나**: [격자] MODIS(MOD15/MCD15 LAI, MOD13 VI)·Sentinel-2/3·모델 vs [정점]·phenocam·고해상 기준지도(업스케일).
- **짝지표 & 교차링크**: **LAI/NDVI bias·상관, SOS/EOS/LOS 타이밍 bias(일)** → [27 LAI·NDVI/EVI·식생 물후 카드]. 검출·변화점은 [06]. 시계열 상관은 [16 §E]. GPP(카드11)와 묶음.
- **만드는 법**: `pandas`/`xarray` groupby(DOY/월)로 계절 climatology; **유효 LAI vs 참 LAI 구분**(군집지수 Ω). SOS/EOS는 로지스틱 적합·이동평균 교차·임계(방법 고정·민감도 병행). `matplotlib` 곡선 + 마커. 지도 아님(축=time/LAI) → basemap 불필요.
- **함정·주의**: **검출법·임계·평활이 SOS를 수~수십일 이동** → 방법 고정·민감도 병행. **지상 유효LAI를 참LAI처럼 쓰면 bias**(§G). 구름 결측이 봄 SOS 왜곡·겨울 NDVI 오염(눈). 센서 간 계통차(교차보정). 화소 대표성(업스케일).
- **출처**: Yang et al. (2006, *IEEE TGRS*, MODIS LAI 검증); Fang et al. (2019, *Reviews of Geophysics*, LAI 검증 리뷰); Zhang et al. (2003, *RSE*, MODIS phenology); Richardson et al. (2013, *Ag. For. Meteorol.*, phenocam·모델); Huete et al. (2002, *RSE*, MODIS VI/EVI); CEOS LPV LAI Val Protocol.

---

### ★ GPP 검증 산점 + 계절곡선 (총일차생산 / GPP scatter + seasonal curve vs eddy covariance, PFT-stratified)
- **무엇을 보여주나**: 모델·위성 GPP(생태계 총 탄소흡수, gC m⁻² d⁻¹)를 EC 타워 유도 GPP와 **산점(정확도)+계절곡선(위상)** 으로 대조. 육상 탄소순환 검증의 중심. PFT(식물기능형)·계절 층화.
- **읽는 법**: 산점 x=타워 GPP, y=모델(1:1·회귀·bias box). 계절곡선은 봄 상승·여름 최대·가을 하강 위상. *나쁜 패턴*: 작물 등에서 **과소(공개 사례 MODIS GPP 6~58% 과소, PFT·건조도 의존)**, 여름 최대 시각 어긋남. **타워 GPP 자체가 NEE 분할(partitioning) 산물**(야간 온도반응 vs 주간 광반응)이라 "참값" 아님 — 분할법 명시.
- **언제 쓰나**: [정점] FLUXNET GPP vs [격자] MODIS(MOD17)·위성 LUE·과정모형. 일·8일·연 규모별.
- **짝지표 & 교차링크**: **GPP bias·RMSE·상관·Taylor** → [27 GPP·NEE/Reco 카드]. Taylor/산점 공통형은 [16 §A·Taylor]. 식생 상태는 카드10(LAI/NDVI). NEE·Reco 성분 병행([27]).
- **만드는 법**: `pandas` 타워-모델 정렬 → `matplotlib` 산점(PFT 색) + groupby 계절곡선. **NEE 분할법·u\* 필터·gap-filling 통일**(FLUXNET2015/ONEFlux). 지도 아님 → basemap 불필요(사이트 위치는 카드14 동반).
- **함정·주의**: **분할가정이 타워 GPP를 좌우**(불확실 기준, §G-1·§G-5). footprint(수백 m)≠격자 대표성. 관개·교란(disturbance) 처리. NEE는 GPP−Reco 상쇄 → 성분 병행([27]). PFT·계절 층화(전역 평균이 강·약점 은폐).
- **출처**: Running et al. (2004, *BioScience*, MOD17 GPP); Reichstein et al. (2005, *Global Change Biology*, NEE 분할); Pastorello et al. (2020, *Scientific Data* 7:225, FLUXNET2015/ONEFlux); Baldocchi et al. (2001, *BAMS*, FLUXNET).

---

### 알베도 검증 산점/시계열 (지표 알베도 / Surface albedo scatter & time-series: blue/white/black-sky)
- **무엇을 보여주나**: 모델·위성(MODIS MCD43) 지표 알베도(단파 반사율 0–1)를 타워 복사관측과 산점·시계열로 대조. **blue-sky(실제)/white-sky(등방)/black-sky(직달)** 구분. 지표 복사수지·에너지 배분·**눈-알베도 되먹임**의 핵심.
- **읽는 법**: 산점 x=타워, y=위성/모델(1:1·bias box). 시계열은 계절(눈·낙엽 전이) 변화. *읽기*: MCD43 사례 RMSE 초지/농지 <0.03(무설기)·<0.05(적설기), 삼림 <0.02~0.025(사례값). *나쁜 패턴*: **적설·혼합·이질피복에서 악화**, 알베도 종류(blue/white/black) 혼동, 태양천정각·계절 편의.
- **언제 쓰나**: [격자] MODIS MCD43·모델 vs [정점] flux tower(CMP/CNR 복사계). 눈/식생 계절·태양천정각 고려.
- **짝지표 & 교차링크**: **알베도 bias·RMSE·상관** → [27 지표 알베도·방출률/Rn 카드]. 산점 공통형은 [16 §A], 복사수지는 04. 눈-알베도는 SWE/SCA(카드8,9)와 되먹임.
- **만드는 법**: `pandas`로 albedo=상향/하향 단파 정렬 → `matplotlib` 산점+시계열. **blue/white/black-sky 정의 정합**(캡션 명시). 화소(500 m) vs 타워 발자국 대표성. 지도 아님 → basemap 불필요.
- **함정·주의**: **적설기·이질피복 대표성 오차 큼.** 알베도 종류 혼동 금지. 광대역(broadband) vs 분광 구분. §G-1·§G-4.
- **출처**: Cescatti et al. (2012, *RSE*, MCD43 vs FLUXNET); Wang et al. (2014, *RSE*, MCD43 검증); Schaaf et al. (2002, *RSE*, MODIS BRDF/Albedo).

---

### ★ 격자-격자 bias / difference 공간 지도 (재분석 지도차 / Gridded bias / difference map vs ERA5-Land·GLDAS, basemap)
- **무엇을 보여주나**: 우리 모델 [격자]를 육상 재분석 [격자](ERA5-Land·GLDAS·MERRA-2-Land)와 **면적 전면 비교**해 bias(x,y)·RMSE(x,y)·상관(x,y)의 지리 분포를 **지도(색)** 로. 모든 육상 변수(토양수분·LST·ET·SWE·LAI·알베도) 공통. 관측 희소지역까지 계통오차 위치·계절성 진단.
- **읽는 법**: 색 = 격자별 지표. **bias는 발산맵(0=흰색, RdBu_r/cmocean balance)**, RMSE는 순차맵(비음수). *읽기*: 계통 bias 띠(예: 반건조대 과습, 산악 SWE 과소, 밀림 LAI 포화)의 위치·계절. 위도대·영역 평균선 병행. *나쁜 패턴*: 넓은 단색(계통편차), 해안선/피복 경계 줄무늬(재격자·해상도차 artifact).
- **언제 쓰나**: [격자]vs[격자] NetCDF↔NetCDF. 광역 진단, 점 검증(카드14)이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·상관·SI** → [27 격자-격자 공간비교 카드]. 공간패턴·ACC 코어는 [02], 재격자·마스크는 [15]. 공통 bias map은 [16 §B]. 토양수분 검증지표 지도는 카드3.
- **만드는 법**: `xarray`+`xesmf`(bilinear/conservative regridding, 공통격자)→격자별 bias/RMSE→`cartopy`/`matplotlib` `pcolormesh`. ★ **지도이므로 `add_basemap(ax, lon, lat)`으로 해안선/육지+위경도 라벨 필수.** bias는 `TwoSlopeNorm(vcenter=0)`+`cmocean.cm.balance`, RMSE는 `cmo.amp`. **육지/해양/영구빙 마스크·시간축·달력·경도 규약 통일**.
- **함정·주의**: ★ basemap 없으면 위치 못 읽음(offline이면 fallback graticule). **재분석은 참값 아님**(자체 오차·동화 한계) → 지상/위성과 교차. 우리 모델과 **같은 지면모형/강제 공유 시 차이 과소**(§G-2). **해상도 차(ERA5-Land ~9 km vs GLDAS ~0.25°)가 차이의 상당부분**. 재격자 보존성·해안선 처리.
- **출처**: Muñoz-Sabater et al. (2021, *ESSD* 13:4349–4383, ERA5-Land); Rodell et al. (2004, *BAMS*, GLDAS); Reichle et al. (2017, *J. Hydrometeorol.*, MERRA-2 land); 공간비교 코어 [02]; basemap [`plotting_maps.md`].

---

### ★ 관측소 위치 지도 (정점 위치도 / Station location map + ID labels, basemap)
- **무엇을 보여주나**: 검증에 쓴 모든 정점(ISMN 토양수분망·FLUXNET 타워·SNOTEL)을 **해안선 지도 위 마커**로 찍고 **정점 ID·피복/네트워크·표고**를 라벨. 점 검증의 산점·시계열이 "어디서" 나온 값인지 독자가 항상 알게 하는 필수 동반 그림.
- **읽는 법**: x=경도, y=위도, 마커=정점(색/기호=네트워크·피복·성능). *읽기*: 정점의 지리·표고·피복 분포 편중 확인(예: 온대 편중, 산악·밀림 희소). *나쁜 패턴*: 마커만 있고 ID·좌표 없음(재현 불가), 격자 대표 못하는 이질지형에 단일 정점.
- **언제 쓰나**: 모든 [정점] 검증(토양수분·ET·GPP·SWE·알베도) 보고의 서두. 산점/시계열 패널의 인셋 로케이터로도.
- **짝지표 & 교차링크**: 정점별 **bias·RMSE·anomaly-R 등을 마커 색**으로 얹으면 성능 지도로 승급 → 카드3(토양수분 지표 지도)·카드13. 대표성 오차는 [27 관측망 대표성·업스케일].
- **만드는 법**: ★ `cartopy` GeoAxes + **`add_basemap(ax, station_lon, station_lat, margin_deg=0.5~1.0)`**(해안선/육지+위경도 라벨) → `ax.scatter`(마커) + `ax.annotate`로 정점 ID(약간 offset). 군집 촘촘하면 `10m` 해안선. 각 통계 패널엔 **인셋 로케이터맵**(단일 정점 점) + 제목에 위경도·표고. 넓은 extent 인셋으로 지역 맥락.
- **함정·주의**: ★ basemap·라벨 필수(위치 식별). 연안/산악 확대엔 `10m` 해안선(거친 해안선은 육지/바다 혼동). **경도 규약(0–360 vs −180…180)** 변환. 단일 정점이 격자를 대표 못하면 큰 검증차가 정상(§G-1) — 캡션에 대표성 경고.
- **출처**: Dorigo et al. (2011, *HESS*, ISMN); Pastorello et al. (2020, *Scientific Data* 7:225, FLUXNET2015); 정점 위치 표기 규칙 [`plotting_maps.md` §C]; Cartopy gridlines/feature 문서.

---

### 피복·PFT 층화 성능 그림 (피복 층화 도표 / Stratified-by-land-cover/PFT performance: grouped bar / heatmap)
- **무엇을 보여주나**: 검증 지표(bias·RMSE·anomaly-R·F1 등)를 **토지피복·식물기능형(PFT)·기후대(Köppen)별로 층화**해 grouped bar 또는 heatmap(행=피복, 열=지표/계절)으로. 전역 평균이 감추는 **피복별 조건부 강·약점**을 노출.
- **읽는 법**: bar/heatmap 색·높이=층별 지표. *읽기*: 밀림·도시·설원·건조지 등에서 계통차 흔함. *나쁜 패턴*: 특정 피복에서 anomaly-R 급락·bias 쏠림(그 물리/파라미터 약점). 층별 표본수 적으면 불안정(신뢰구간·N 병기).
- **언제 쓰나**: 모든 육상 변수 공통. [격자]/[정점]. 도메인 성능의 조건부 분해.
- **짝지표 & 교차링크**: 층별 **bias·RMSE·R·F1** → [27 토지피복·PFT 층화 검증 카드]. 지표 정의는 [01]/[03]. 공간분포는 카드3·13.
- **만드는 법**: `pandas` groupby(피복지도 IGBP/PFT/Köppen)로 층별 지표 → `matplotlib`/`seaborn` `heatmap`/grouped `bar` + 부트스트랩 CI·N 라벨. 지도 아님(축=피복×지표) → basemap 불필요(단 피복 분포는 카드14/13 지도로 동반).
- **함정·주의**: **피복지도 오분류·혼합화소가 층화 왜곡.** 층별 표본 적으면 신뢰구간 필수. 전역 평균 단독 금지(§G-6).
- **출처**: Friedl et al. (2010, *RSE*, MODIS land cover IGBP); Best et al. (2015, *J. Hydrometeorol.*, PLUMBER land model 벤치마킹).

---

### 토양온도·동결 프로파일 시계열 (토양온도 깊이-시간 / Soil temperature & frozen-soil depth–time heatmap)
- **무엇을 보여주나**: 층별 토양온도(°C)를 **깊이(y)–시간(x) 히트맵**으로 모델·관측 나란히, 0°C 등온선(동결심도)·동결/해빙 타이밍을 등고선으로. 표층→심층 **감쇠·위상지연**, 고위도·산악·영구동토 열상태를 본다.
- **읽는 법**: x=시간, y=깊이(아래로 증가), 색=온도. *읽기*: 표층 일·계절 진동이 심층으로 갈수록 감쇠·지연. 0°C 등온선이 동결심도. *나쁜 패턴*: 모델 동결심도 과대/과소, 심층 위상지연 어긋남(열확산·수분 오류), **눈 단열·토양수분 오차가 토양온도로 전이**. 모델·관측·차이 3패널.
- **언제 쓰나**: [프로파일] 토양온도 관측 vs [격자] 모델 층. 고위도·산악 수문·탄소(영구동토).
- **짝지표 & 교차링크**: **층별 토양온도 bias·RMSE·상관, 동결심도·동결/해빙일** → [27 동결·토양온도 카드]. 심도 정합은 [27 토양층 정합]. 위상·변화점은 [06]. Hovmöller(전파)는 [16 §B].
- **만드는 법**: `xarray`로 (깊이,시간) 2D → `matplotlib` `pcolormesh`/`contourf`(0°C 등온선 `contour`). **관측 심도·모델 층경계 정합**(깊이축 통일). 깊이-시간 히트맵은 지도 아님(y=깊이) → basemap 불필요(정점 위치는 카드14 동반).
- **함정·주의**: **심도 부정합이 위상오차로 오인**(§G-1). 눈 단열·토양수분이 토양온도 지배 → 그 오차가 전이. 심도·계절 층화. 관측 결측·센서 심도 명시.
- **출처**: Luo et al. (2003, *J. Hydrometeorol.*, soil temperature 검증); Koven et al. (2013, *J. Climate*, 영구동토 모델); Hovmöller (1949, *Tellus* 1(2), 시공간 도표 원리).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 27(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 27(및 타 파일) 교차링크 |
|---|---|---|---|---|---|
| 1 | 토양수분 시계열 + anomaly 패널 | 정점·격자·트랙 | 편향+단기이벤트 | anomaly-R·R·ubRMSD·bias | 27 이상상관/ubRMSD · 16 §E · 01 |
| 2 | 토양수분 삼중대조(TC/ETC) 오차막대 | 격자+정점+트랙 | 오차분해(기준없음) | TC/ETC σ_ε·SNR·scaling | 27 삼중대조 · 12·15 TC/ETC |
| 3 | anomaly-R / ubRMSD 공간 지도 ★map | 격자·트랙 | 정확도·편향(공간) | anomaly-R·ubRMSD·bias·TC | 27 이상상관/ubRMSD/TC · 02 · 15 |
| 4 | CDF 매칭 전후 진단 | 트랙·격자·정점 | 전처리 정당성 | anomaly-R·ubRMSD | 27 CDF매칭 · 13·15 QM · 16 QQ |
| 5 | LST 일변동 곡선 + 주야 산점 | 트랙·격자·정점 | 위상+주야편향 | LST bias·RMSE·R(주야) | 27 LST T-b/R-b·주야표집 · 01·16 §E |
| 6 | ET 에너지수지 산점 + EBR | 정점·격자 | 닫힘+에너지배분 | EBR·회귀기울기·잔차 | 27 EBR/Bowen비 · 16 §A · 04 |
| 7 | EF/Bowen비 일변동·계절 곡선 | 정점·격자 | 배분(분할) | EF·β bias·상관 | 27 LE/H 분할 · 04 |
| 8 | SWE 시계열 + 융설 타이밍 | 정점·격자 | 저장량+눈위상 | SWE bias/RMSE·타이밍 bias(일) | 27 SWE·melt타이밍 · 06 |
| 9 | SCA 범주검증 지도 ★map | 격자 | 범주(눈/무눈) | POD·FAR·F1·accuracy | 27 SCA · 03 · 16 §C |
| 10 | 식생 계절곡선 LAI/NDVI (SOS/EOS) | 격자·정점 | 위상+진폭(식생) | LAI/NDVI bias·R·SOS/EOS bias(일) | 27 LAI·NDVI·물후 · 06 · 16 §E |
| 11 | GPP 산점 + 계절곡선 (PFT) | 정점·격자 | 정확도+위상(탄소) | GPP bias·RMSE·R | 27 GPP·NEE/Reco · 16 §A·Taylor |
| 12 | 알베도 산점/시계열 (blue/white/black) | 격자·정점 | 정확도(복사) | 알베도 bias·RMSE·R | 27 알베도·방출률/Rn · 16 §A · 04 |
| 13 | 격자-격자 bias/difference 지도 ★map | 격자 | 편향+패턴(공간) | 격자별 bias·RMSE·R·SI | 27 격자비교 · 02 · 15 regrid |
| 14 | 관측소 위치 지도 ★map | 정점 | 위치 식별·대표성 | (마커 색=성능지표) | 27 대표성·업스케일 · plotting_maps §C |
| 15 | 피복·PFT 층화 성능 (bar/heatmap) | 격자·정점 | 조건부 성능 | 층별 bias·RMSE·R·F1 | 27 피복 층화 · 01·03 |
| 16 | 토양온도·동결 깊이-시간 히트맵 | 프로파일·격자 | 열상태·위상지연 | 토양온도 bias·RMSE·동결심도/일 | 27 동결·토양온도 · 06 · 16 §B |

> **묶음 권고**: 단일 그림 금지 원칙(§G-4)에 따라 육상 검증 보고는 변수별 최소 3축 세트를 기본으로 —
> - **토양수분**: ①(anomaly 이벤트) + ③(공간 anomaly-R/ubRMSD) + ②(TC 오차·기준신뢰) + [16 Taylor];
> - **ET/에너지**: ⑥(EBR 닫힘) + ⑦(EF 분할) + [16 산점](LE/ET 정확도);
> - **눈**: ⑧(SWE·타이밍) + ⑨(SCA 범주 지도);
> - **식생·탄소**: ⑩(LAI/NDVI 물후) + ⑪(GPP);
> - **광역**: ⑬(격자 bias 지도) + ⑭(정점 위치도) + ⑮(피복 층화).
> 모든 임계(ubRMSD~0.04·anomaly-R 0.3~0.7·EBR 0.7~0.9·SCA F1 등)는 **advisory + 피복·계절·해상도 의존 경고**로 캡션에 단다. ★map 표시 그림은 **`add_basemap()`으로 해안선/육지+위경도 라벨 필수**.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 지침·프로토콜 (실재)**
- CEOS LPV *Soil Moisture Validation Good Practices Protocol* (v1, 2020) — 토양수분 검증 표준.
- Guillevic et al. (2018) GSICS/CEOS *Land Surface Temperature Product Validation Best Practice Protocol* — LST T-b/R-b·주야·청천 표집.
- CEOS LPV *LAI Validation Protocol* — 유효 LAI vs 참 LAI·업스케일.

**학술 논문 (제목·저널·연도 웹 확인)**
- Gruber, A., et al. (2016) "Recent advances in (soil moisture) triple collocation analysis," *Int. J. Applied Earth Observation and Geoinformation* 45:200–211. (TC 리뷰·anomaly)
- Gruber, A., et al. (2020) "Validation practices for satellite soil moisture retrievals: What are (the) errors?" *Remote Sensing of Environment* (good-practice·rescaling·대표성).
- Stoffelen, A. (1998) "Toward the true near-surface wind speed: error modeling and calibration using triple collocation," *JGR* 103(C4). (TC 기초)
- McColl, K. A., et al. (2014) "Extended triple collocation," *GRL* 41(17):6229–6236. (doi:10.1002/2014GL061322)
- Dorigo, W. A., et al. (2011) "The International Soil Moisture Network (ISMN)," *HESS*.
- Draper, C. S., et al. (2013) "Estimating root mean square errors in remotely sensed soil moisture over continental scale domains," (SMOS/ASCAT vs model, *GRL*).
- Albergel, C., et al. (2008) "From near-surface to root-zone soil moisture using an exponential filter (SWI)," *HESS*.
- Reichle, R. H., & Koster, R. D. (2004) "Bias reduction in short records of satellite soil moisture," *GRL*. (CDF matching)
- Coll, C., et al. (2009) "Temperature-based and radiance-based validations of the V5 MODIS LST product," *JGR: Atmospheres* 114, D20102. (doi:10.1029/2009JD012038)
- Wan, Z. (2014) "New refinements and validation of the collection-6 MODIS LST product," *RSE*.
- Duan, S.-B., et al. (2019) radiance-based LST validation over heterogeneous surfaces, *RSE*.
- Wilson, K., et al. (2002) "Energy balance closure at FLUXNET sites," *Ag. For. Meteorol.* 113(1–4):223–243.
- Foken, T. (2008) "The energy balance closure problem: an overview," *Ecological Applications*.
- Stoy, P. C., et al. (2013) energy balance closure multi-site, *Ag. For. Meteorol.*
- Twine, T. E., et al. (2000) "Correcting eddy-covariance flux underestimates over a grassland," *Ag. For. Meteorol.* (Bowen-ratio closure)
- Gentine, P., et al. (2007) evaporative fraction diurnal self-preservation, *Ag. For. Meteorol.*
- Baldocchi, D., et al. (2001) "FLUXNET," *BAMS*.
- Pastorello, G., et al. (2020) "The FLUXNET2015 dataset and the ONEFlux processing pipeline," *Scientific Data* 7:225.
- Running, S. W., et al. (2004) "A continuous satellite-derived measure of global terrestrial primary production (MOD17)," *BioScience*.
- Reichstein, M., et al. (2005) "On the separation of net ecosystem exchange into assimilation and ecosystem respiration," *Global Change Biology*. (NEE 분할)
- Cescatti, A., et al. (2012) "Intercomparison of MODIS albedo (MCD43) with tower measurements (FLUXNET)," *RSE*.
- Schaaf, C. B., et al. (2002) "First operational BRDF, albedo nadir reflectance products from MODIS," *RSE*.
- Salomonson, V. V., & Appel, I. (2004) "Estimating fractional snow cover from MODIS using NDSI," *RSE*.
- Hall, D. K., & Riggs, G. A. (2007) "Accuracy assessment of the MODIS snow products," *Hydrological Processes*.
- Stillinger, T., et al. (2023) lidar-based snow cover validation (F1), *The Cryosphere*.
- Rittger, K., et al. (2021) "Evaluation of VIIRS and MODIS snow cover fraction in High-Mountain Asia," *Frontiers in Remote Sensing* 2:647154.
- Mortimer, C., et al. (2020) gridded SWE product evaluation, *The Cryosphere*.
- Broxton, P. D., et al. (2016) SWE observation representativeness, *J. Hydrometeorol.*
- Wrzesien, M. L., et al. (2019) mountain SWE, *GRL*.
- Yang, W., et al. (2006) MODIS LAI validation, *IEEE TGRS*.
- Fang, H., et al. (2019) "An overview of global Leaf Area Index (LAI)... validation," *Reviews of Geophysics*.
- Zhang, X., et al. (2003) "Monitoring vegetation phenology using MODIS," *RSE*.
- Richardson, A. D., et al. (2013) phenocam·model phenology, *Ag. For. Meteorol.*
- Huete, A., et al. (2002) "Overview of the radiometric and biophysical performance of the MODIS vegetation indices (EVI)," *RSE*.
- Muñoz-Sabater, J., et al. (2021) "ERA5-Land," *Earth System Science Data (ESSD)* 13:4349–4383.
- Rodell, M., et al. (2004) "The Global Land Data Assimilation System (GLDAS)," *BAMS*.
- Reichle, R. H., et al. (2017) MERRA-2 land surface hydrology, *J. Hydrometeorol.*
- Friedl, M. A., et al. (2010) "MODIS Collection 5 global land cover (IGBP)," *RSE*.
- Best, M. J., et al. (2015) "The plumbing of land surface models (PLUMBER)," *J. Hydrometeorol.*
- Luo, L., et al. (2003) soil temperature validation, *J. Hydrometeorol.*
- Koven, C. D., et al. (2013) permafrost carbon in CMIP5, *J. Climate*.
- Hovmöller, E. (1949) "The Trough-and-Ridge diagram," *Tellus* 1(2):62–66. (doi:10.1111/j.2153-3490.1949.tb01260.x)

**소프트웨어 (실존 도구)**
- `pytesmo` — 토양수분 검증 툴박스(anomaly/climatology·CDF matching·ubRMSD·triple collocation): https://pytesmo.readthedocs.io (`time_series.anomaly.calc_anomaly`, `scaling.scale`, `metrics.tcol_metrics`).
- `cartopy` — 지도 basemap(해안선·육지·위경도 라벨) → [`plotting_maps.md`] `add_basemap`.
- `xarray`/`xesmf` — 격자 I/O·재격자화; `matplotlib`; `scipy.stats`(linregress·binned_statistic); `numpy`; `seaborn`(heatmap); `xskillscore`(이진 범주지표); `cmocean`(balance/amp/thermal 색맵).

**확인요 (확정 인용 금지 — §G-5)**
- 해석 임계(ubRMSD~0.04 m³/m³·anomaly-R 0.3~0.7·EBR 0.7~0.9·회귀기울기 0.74→0.87·MODIS SCA POD~0.95/FAR~0.18·MCD43 albedo RMSE·MODIS GPP 6~58% 과소)는 모두 **미션요구/사례/관행 advisory** — 피복·계절·해상도·기준자료 의존(§G-4).
- 개별 논문 권·페이지·DOI 중 본 세션에서 **DOI를 직접 확인한 것은 McColl et al. 2014(10.1002/2014GL061322)·Coll et al. 2009(10.1029/2009JD012038)·Hovmöller 1949(10.1111/j.2153-3490.1949.tb01260.x)** 뿐이며, 나머지 논문의 DOI는 미표기(확인요) — 제목·저널·연도만 인용.
- FLUXNET ET/GPP·타워 EBR·MODIS/위성 소산물·재분석(ERA5-Land/GLDAS)은 모두 **reference이지 truth 아님**; 특히 GPP·EBR은 관측 자체가 분할/닫힘 가정에 의존(§G-1).
