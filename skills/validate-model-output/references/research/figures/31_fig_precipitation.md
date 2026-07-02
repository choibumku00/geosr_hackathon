# 검증 시각화 카탈로그 — [강수 도메인편] (Verification Figures: Precipitation)

이 문서는 수치모델·재분석·위성·레이더의 **강수(precipitation)** 산출물을 **우량계(rain gauge)·격자 관측/재분석(ERA5·GPCP·APHRODITE)·위성(IMERG/GPM·CMORPH·GSMaP)·레이더 QPE** 와 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 강수 도메인편이다. 메서드(수치지표) 카드는 [`23_domain_precipitation.md`](../23_domain_precipitation.md)에 있고(**대응 메서드카탈로그: 23_domain_precipitation.md**), 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **공통/횡단 그림과의 분담**: Taylor·Target·일반 QQ·ROC·신뢰도(reliability)·rank histogram·Brier/CRPS 분해·성능도표(Roebber)·FSS 스케일-임계 히트맵·SAL 산점도·PDF/CDF·return-level 등 **도메인 무관 요약그림의 정의는 [공통편 `16_fig_common.md`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않는다. 이 파일은 **강수 고유 그림**(wet-day 강도 PDF·frequency×intensity 분해·diurnal Hovmöller·radar–gauge merging·ETCCDI 지수 지도 등)과 **공통 그림의 강수식 변형**(임계 스캔 성능도표·강수용 SAL·wet-only tail QQ·intensity-scale 플롯 등)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "교차링크"에서 가리킨다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석/위성 L3·L4/레이더 QPE) · [시계열]=우량계·AWS 관측소 CSV/텍스트(정점) · [트랙/스와스]=위성 저궤도(GPM DPR 등) · [분포]=시간정렬 불필요한 통계 비교.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 우량계·IMERG·ERA5·레이더 QPE는 모두 reference이지 truth가 아니다(게이지 undercatch, 위성 saturation, QPE Z–R 편의). 축·캡션에 "모델−기준 차"로 쓰고 "오차"로 단정하지 않는다. **IMERG Final·radar–gauge 병합산물은 게이지가 이미 반영** → 그 게이지로 "독립 검증" 금지(오차상관).
> 2. **강수는 간헐·비대칭·국소.** 값의 다수가 0이고 극치가 지배하며 위치오차가 double-penalty를 일으킨다. **단일 임계·단일 지표·단일 그림 금지** — 범주(성능도표)+분포(PDF/QQ)+공간(FSS/객체)을 함께 본다.
> 3. **wet 임계·누적창·변환을 반드시 명시.** wet 임계(0.1 vs 1 mm/day)·누적기간(1h·일)·관측기준시각(예 09 KST)·재격자(강수는 **보존적**)·변환(√/log) 선택이 모든 그림을 바꾼다.
> 4. **해석 임계는 advisory.** `FSS useful=0.5+f₀/2`, `PBIAS 등급`, `CC≥0.7` 등은 관행값이며 기후대(열대 convective vs 중위도 stratiform)·해상도·기준자료 의존. "good/bad"를 단정 표기하지 말고 영역의존 경고를 캡션에 둔다.
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **성능도표 (Roebber performance diagram, 임계 스캔)** — 강수 범주검증의 1차 종합 대표그림
2. ★ **분할표 지표 vs 임계 곡선 (FBI/POD/FAR/CSI/GSS vs threshold)** — 임계 의존성 스캔
3. ★ **FSS 스케일–임계 히트맵 (neighborhood verification)** — 위치오차·유효스케일
4. ★ **double-penalty 진단 패널 (원장·변위장·스무딩 회복)** — 왜 이웃/객체가 필요한가
5. ★ **객체기반 SAL 산점도 (S–A–L)** — 구조·양·위치 3성분 분해
6. ★ **MODE 객체 매칭 지도 (object-based, basemap)** — 객체 속성·매칭 공간진단
7. **intensity-scale (Casati ISS) 플롯** — 강도×스케일 오차 분해
8. ★ **wet-day 강수강도 PDF/CDF (log-bin)** — 약비 과다·강비 과소 분포편향
9. **frequency×intensity 분해 그림 (Δmean = f·ΔI + I·Δf)** — 총량편향의 원천
10. ★ **강수 Q-Q plot (wet-only, 고분위 tail 강조)** — 분포·극치 일치 (16 교차 + 강수특화)
11. ★ **공간 bias/PBIAS/RMSE 지도 (gridded map, basemap)** — 면적 계통오차 지리분포
12. ★ **강수 diurnal Hovmöller / 첨두시각 위상 지도** — 일변동 위상·진폭 (LST)
13. ★ **극치 return-level 플롯 (POT-GPD/GEV, CI)** — 설계강우·재현주기
14. **ETCCDI 극한지수 지도·산점 (Rx1day·R95pTOT·SDII·CDD 등)** — 표준 기후 극한
15. ★ **위성강수 매치업 산점도 (연속+범주, IMERG/GPM)** — 광역 검증 대표
16. **radar–gauge merging 진단 (G/R 산점·병합 전후 지도)** — QPE 편의·기준 격자 생성

---

### ★ 성능도표 (성능 다이어그램 / Performance diagram, Roebber, 임계 스캔)
- **무엇을 보여주나**: 임계(0.1·1·10·50 mm/day 등)마다 계산한 (SR, POD)를 한 평면에 찍고 **CSI 등치선·frequency-bias 방사선**을 배경으로 얹어, POD·FAR(=1−SR)·CSI·FBI 네 범주지표를 **한 점**으로 동시에 본, 강수 범주검증의 표준 종합 대표그림. 여러 모델·리드타임·임계를 점·궤적으로 겹쳐 비교. (공통편 §C의 성능도표를 **강수 임계 스캔·다중 사건빈도**로 특화.)
- **읽는 법**: x=성공비 SR(=1−FAR), y=POD. **곡선 등치선=CSI**(우상단일수록 높음), **대각 방사선=FBI**(대각선=1, 위=과다예보 drizzle 경향·아래=과소). *좋은 패턴*: 점이 우상단(POD↑·SR↑·CSI↑)·FBI≈1 대각선 근처. *나쁜 패턴*: 임계↑(호우)일수록 점이 좌하단으로 후퇴(정상), FBI선 1에서 크게 이탈(계통 과다/과소). 임계별 점을 선으로 이어 **임계 상승에 따른 성능 감쇠 궤적**을 본다. 부트스트랩 SR·POD 95% "cross-hair"로 표본변동 표시.
- **언제 쓰나**: [시계열]/[격자]/[트랙](임계 이진화). 강수 QPF·위성·나우캐스팅 범주 종합. 임계 스캔·다모델 비교에 강력.
- **짝지표 & 교차링크**: **POD·SR·FAR·CSI·FBI·GSS/ETS** → [`23` 분할표·CSI/GSS·HSS/PSS 카드]. 배경·기하는 **공통편 [`16` 분할표 viz & Performance diagram]** 로 교차링크(중복 정의 회피). 판별력은 ⑮/[`16` ROC]와 병행, 위치오차 분리는 ③ FSS. 드문 극한 임계는 [`23` EDI/SEDI].
- **만드는 법**: 임계별 a,b,c,d 집계(`xskillscore` 이진 지표 또는 직접) → `matplotlib`로 CSI 등치선(`np.meshgrid(SR,POD)` → `CSI=1/(1/SR+1/POD−1)`) + FBI 직선 배경 + 임계별 (SR,POD) scatter. CAWCR/`METplus`·`PyForecastTools`에도 구현. 부트스트랩(resampling with replacement)으로 cross-hair.
- **함정·주의**(§G): 분할표 단일지표(PC 등)는 **드문 사건에서 오도**(항상 'no'로 높은 PC) → CSI·SEDI 병행. **격자 double-penalty**(위치 약간 어긋나면 hit이 miss+false로 이중처벌) → ③/④와 함께 해석. 임계·사건빈도 의존 → 임계 스캔 명시. 표본 작으면 칸 0으로 지표 발산·격자 자기상관으로 유효표본 과대 → **부트스트랩 CI 필수**. **지도 아님**(축이 SR×POD) → basemap 넣지 말 것.
- **출처**: Roebber (2009, *Weather and Forecasting* 24(2):601–608, doi:10.1175/2008WAF2222159.1); CAWCR/WWRP-JWGFVR Performance Diagram 페이지(cawcr.gov.au/projects/verification/Roebber/PerformanceDiagram.html); Jolliffe & Stephenson, *Forecast Verification*.

---

### ★ 분할표 지표 vs 임계 곡선 (임계 의존 곡선 / Contingency metrics vs threshold curves)
- **무엇을 보여주나**: FBI·POD·FAR·CSI·GSS(ETS) 등을 **강수 임계(x축, log)** 에 대해 곡선으로 펼쳐, 단일 임계가 감추는 **임계 의존성**을 한눈에. "약비는 잘 잡지만 호우로 갈수록 급락" 같은 강수 특유의 임계 열화를 정량화.
- **읽는 법**: x=임계(mm/day, log), y=지표값. *읽기*: **FBI가 저임계에서 >1(drizzle 과다), 고임계에서 <1(호우 과소)** 로 교차하는 흔한 패턴; POD·CSI·GSS는 임계↑에서 하강(사건 희소). *나쁜 패턴*: FBI가 전 임계에서 크게 1 이탈(계통 과다/과소), CSI가 저임계에서도 낮음(위치·강도 모두 틀림). 여러 모델을 색으로, 부트스트랩 CI 띠 동반.
- **언제 쓰나**: [시계열]/[격자]. 임계 스캔 진단(성능도표 ①의 1차원 보완). 사건빈도 f₀도 같은 x축에 병기하면 base-rate 맥락 제공.
- **짝지표 & 교차링크**: ①과 동일 지표군 → [`23` 분할표·CSI/GSS 카드]. 극한 임계에서 CSI/GSS 퇴화 시 **[`23` EDI/SEDI]** 곡선으로 승급. base-rate 맥락은 [`16` 분할표 viz].
- **만드는 법**: 임계 리스트 루프로 a,b,c,d→지표 계산(`numpy`/`xskillscore`) → `matplotlib` `semilogx` 다곡선. CI는 부트스트랩(사례 resampling). `scores`/`METplus`에도 임계 스캔 유틸.
- **함정·주의**(§G): **단일 임계 결론 금지**(정보손실) — 이 그림 자체가 그 해법. 고임계는 표본 희소로 곡선 요동 → CI 필수·EDI/SEDI 병행. 격자면 double-penalty가 전 임계에 스며듦(③와 교차). wet 임계·누적창 명시. **지도 아님**.
- **출처**: [`23_domain_precipitation.md`]; Jolliffe & Stephenson; Ebert (2001, *Monthly Weather Review*, 강수 검증 관행); WWRP/WGNE JWGFVR verification methods 페이지.

---

### ★ FSS 스케일–임계 히트맵 (분율 스킬점수 히트맵 / Fractions Skill Score scale–threshold heatmap)
- **무엇을 보여주나**: 이웃(neighborhood) 크기(스케일)×강수 임계 격자에 FSS(0~1)를 색으로 펼친 히트맵(또는 임계 고정 FSS-vs-scale 곡선). 격자 double-penalty를 완화하고 **"어느 공간 스케일부터 예보가 유용한가(useful scale)"** 를 정량화하는 강수 공간검증의 대표 그림. (공통편 §B의 FSS 히트맵을 강수 임계·useful-scale 해석으로 특화.)
- **읽는 법**: x=이웃반경/스케일(km 또는 격자수), y=강수 임계(1·5·10·50 mm), 색=FSS. **useful-scale 경계 등치선 = 0.5+f₀/2**(f₀=관측 사건빈도). *좋은 패턴*: 작은 스케일부터 FSS가 경계 초과(녹색). *나쁜 패턴*: 큰 스케일에서도 낮음(위치·강도 모두 틀림), 고임계 행에서 useful scale이 급격히 커짐(호우 위치오차 큼). 임계 고정 FSS-vs-scale 곡선과 병용.
- **언제 쓰나**: [격자] 강수(모델·레이더 QPE·위성). 고해상도·AI 강수예보의 위치오차 진단. 임계×스케일 스캔.
- **짝지표 & 교차링크**: **FSS·useful scale·이웃검증** → [`23` FSS 카드], [`02` 공간패턴]. double-penalty 원인 진단은 ④와 짝. 정의·배경은 **공통편 [`16` FSS 공간검증 맵]** 교차링크.
- **만드는 법**: `pysteps.verification.spatialscores`의 **`fss_init`/`fss_accum`/`fss_compute`**(다사례 누적) 또는 `fss`(단일장), 대안으로 `scores.spatial.fss_2d`. 임계·스케일 리스트 스캔 → 히트맵 `matplotlib.pcolormesh`/`seaborn.heatmap`, useful-scale 등치선 overlay.
- **함정·주의**(§G): FSS는 **결정론 단일장 비교** — 앙상블이면 멤버별/확률화 별도. 도메인 가장자리·결측이 이웃합을 왜곡(패딩 규약 명시). **useful=0.5+f₀/2는 f₀ 의존** → 사건 드물면 기준선이 낮아져 "쉬워" 보임(§G-4 advisory). 임계·이웃 정의가 결과를 좌우 → 스캔·명시. 이진화로 **강도·위치 오차를 분리 못함**(⑤ SAL 병행). **지도 아님**(축이 스케일×임계) → basemap 없음.
- **출처**: Roberts & Lean (2008, *Monthly Weather Review* 136(1):78–97, doi:10.1175/2007MWR2123.1); Mittermaier & Roberts (2010, *Weather and Forecasting* 25); Skok & Roberts (2016, *QJRMS*, useful-scale 재검토); pysteps(Pulkkinen et al. 2019, *GMD* 12:4185–4219, pysteps.readthedocs.io).

---

### ★ double-penalty 진단 패널 (이중벌점 진단 / Double-penalty diagnostic panels)
- **무엇을 보여주나**: 강수 셀이 위치만 약간 어긋나도 격자지표(RMSE·CSI)가 "무강수 예보(전부 0)"보다 나빠지는 **이중 처벌**을 시각적으로 드러내는 진단 패널: (a) 관측·모델 강수장 나란히, (b) 변위(displacement) 예시, (c) **이웃 스케일↑ 시 FSS 급상승 곡선**, (d) 스무딩 후 RMSE/CSI 회복 정도. 왜 이웃(③)·객체(⑤⑥) 방법이 필요한지의 근거 그림.
- **읽는 법**: (a)(b) 두 강수장의 셀 위치 차 = 변위오차. (c) FSS가 작은 스케일에서 낮다가 스케일 키우면 **가파르게 상승** → 강도·형상은 맞고 **위치만 어긋남**(double-penalty 신호). (d) 약간의 스무딩만으로 CSI/RMSE가 크게 회복하면 위치오차 지배. *해석*: 격자 RMSE·CSI가 나쁘다고 곧 "모델이 나쁘다"로 단정 금지 — 위치오차인지 강도오차인지 구분.
- **언제 쓰나**: [격자] 고해상도 강수(대류허용 모델·AI 강수·나우캐스팅). 격자지표가 나쁠 때 원인 규명.
- **짝지표 & 교차링크**: FSS 스케일 반응(③)·객체 위치성분(⑤ SAL의 L·⑯ CRA displacement) → [`23` double-penalty·FSS·SAL 카드], [`14` AI 산출물 추가축]. 공간지표 배경은 [`02`].
- **만드는 법**: 강수장 지도는 ⑪처럼 basemap; FSS 곡선은 ③ 도구; 스무딩은 `scipy.ndimage.gaussian_filter` 후 CSI/RMSE 재계산. 변위 예시는 인위적 shift(`np.roll`)로 개념 시연 가능.
- **함정·주의**(§G): double-penalty 무시하면 고해상도·AI 강수모델을 **부당하게 저평가**(§G-6). 반대로 **과도한 스무딩은 실제 오차를 감춤**. (a)(b)의 강수장 패널은 **지도이므로 basemap(해안선/육지+위경도 라벨) 필수**([plotting_maps.md `add_basemap`]); (c)(d) 곡선 패널은 지도 아님. 관측장도 reference(레이더/위성 오차 포함).
- **출처**: Gilleland, Ahijevych, Brown, Casati & Ebert (2009, *Weather and Forecasting* 24(5), ICP 총론); Rossa, Nurmi & Ebert (2008, in *Precipitation: Advances in Measurement, Estimation and Prediction*, Springer); Roberts & Lean (2008).

---

### ★ 객체기반 SAL 산점도 (구조–양–위치 / Object-based SAL: Structure–Amplitude–Location)
- **무엇을 보여주나**: 강수장을 **구조 S·양 A·위치 L** 3성분으로 나눠 한 사례를 (S,A) 산점의 한 점(색=L)으로 표현. RMSE의 double-penalty를 피하고 **"무엇이 틀렸나"**(총량 과다? 객체가 너무 크고 평평? 위치가 밀림?)를 해석 가능하게 분해. (공통편 §B SAL을 강수 QPF 표준으로 특화.)
- **읽는 법**: x=S(구조: 객체 크기/평탄도, −2~2), y=A(진폭: 도메인평균 상대편차, −2~2), 색/마커=L(위치: 질량중심+산포 변위, 0~2). *좋은 패턴*: 점이 (0,0) 근처·L 작음. *나쁜 패턴*: **A>0 총량 과다**, **A<0 과소**; **S>0 모델 객체가 너무 크고 평평**(과평활·drizzle), S<0 너무 작고 뾰족; **L 큼=위치 어긋남**. 여러 사례를 산점으로 뿌려 사분면별 계통오차 유형 분류. 객체 매칭 불필요(변위 double-penalty 회피).
- **언제 쓰나**: [격자] 강수(모델 vs 레이더/위성/관측격자), 정해진 도메인 단위. multimodal·대류 사례 다수의 계통오차 요약.
- **짝지표 & 교차링크**: **SAL의 (S,A,L)** → [`23` 객체기반 SAL 카드], [`02`]. 세밀 객체속성은 ⑥ MODE, 변위 분해는 ⑯ CRA. 산점 배경·정의는 **공통편 [`16` 객체기반 SAL/MODE 플롯]** 교차링크.
- **만드는 법**: **`pysteps.verification.salscores.sal`**(S,A,L 3-튜플 반환, thunderstorm detection으로 객체 식별) 또는 임계 R*(최대의 1/15·상위 백분위) 지정 후 `scipy.ndimage.label`+`skimage.measure.regionprops`로 자체 구현. 다사례 (S,A,L)을 `matplotlib` scatter(색=L). 도메인 크기로 정규화(도메인 간 비교).
- **함정·주의**(§G): **객체 식별 임계 R*가 S·L을 좌우** → 명시·고정. 도메인이 크면 여러 강수계 혼재로 성분 해석 모호. A는 총량만(공간분포 무시) → S·L과 함께. 소수 사례 산점 일반화 금지. 관측 객체도 기준자료(레이더/위성) 오차 포함. **지도 아님**(축이 S×A). 지도로 객체를 보려면 ⑥.
- **출처**: Wernli, Paulat, Hagen & Frei (2008, *Monthly Weather Review* 136(11):4470–4487, doi:10.1175/2008MWR2415.1); Wernli, Hofmann & Zimmer (2009, *Weather and Forecasting* 24, SAL 적용); pysteps `salscores.sal`(pysteps.readthedocs.io).

---

### ★ MODE 객체 매칭 지도 (객체 진단평가 지도 / MODE object matching map)
- **무엇을 보여주나**: 강수 객체를 개별 식별·매칭하고 **지도 위에** 예보·관측 객체를 색칠(매칭쌍 동일색, 미매칭=놓침/오경보 강조색)해, 객체 속성(면적·강도분위·중심거리·종횡비·방향)의 공간 대응을 진단. SAL(⑤)보다 세밀한 객체 대응·속성 비교. (공통편 §B MODE를 강수 지도 표현으로 특화.)
- **읽는 법**: 지도 위 색=객체 ID(매칭쌍 동색). *좋은 패턴*: 대부분 객체가 매칭(동색)·중심거리 작음·면적비≈1. *나쁜 패턴*: 미매칭 객체 다수(놓침·오경보), 매칭객체의 중심 크게 밀림(위치오차), 면적비≫1/≪1(크기오차). 옆에 fuzzy-logic **total interest**(0~1)·속성표 병기. 대류셀·강수계 단위로 해석.
- **언제 쓰나**: [격자] 강수. 대류셀·강수계 단위 정밀 진단(광역·확산 강수엔 객체 정의 모호).
- **짝지표 & 교차링크**: **MODE 객체속성·total interest·매칭률** → [`23` MODE 카드], [`02`]. 요약 3성분은 ⑤ SAL, 변위분해는 ⑯ CRA. 정의는 **공통편 [`16` SAL/MODE 플롯]** 교차링크.
- **만드는 법**: **`MET`/`METplus` MODE-Tool**(NCAR/DTC 표준, convolution+임계 객체화→fuzzy-logic interest 매칭) 또는 Python 객체화 `scipy.ndimage.label`+`skimage.measure.regionprops`(면적·중심·축) → `matplotlib`/`cartopy` 지도에 객체 채색. 지도이므로 **[plotting_maps.md `add_basemap`]로 해안선/육지+위경도 라벨 필수**.
- **함정·주의**(§G): **평활반경·임계·interest 가중치가 결과를 지배** → 반드시 고정·명시(재현·비교 가능성). 객체 정의 모호한 광역·확산 강수에서 불안정. 매칭 안 된 객체 처리 규칙 명시. **지도형** → basemap·위경도 라벨·(모델 lon 0–360이면 −180…180 변환) 필수, 강수 필드는 `pcolormesh`+`transform=ccrs.PlateCarree()`. 관측 객체도 reference 오차.
- **출처**: Davis, Brown & Bullock (2006, *Monthly Weather Review* 134:1772–1795, "Object-based verification of precipitation forecasts, Part I/II", DOI 확인요); Davis, Brown, Bullock & Halley-Gotway (2009, *Weather and Forecasting* 24(5), MODE 적용); DTC MET/METplus User's Guide MODE-Tool(metplus.readthedocs.io).

---

### intensity-scale (Casati ISS) 플롯 (강도-스케일 스킬점수 / Intensity-Scale Skill Score plot)
- **무엇을 보여주나**: 강수 예보 오차를 **강수 강도 × 공간 스케일** 2차원으로 분해한 히트맵. 예보·관측을 임계로 이진화한 차이장에 **Haar 웨이블릿 다해상도 분석(MRA)** 을 적용해, 각 (강도, 스케일) 칸의 스킬을 색으로. 어느 강도·어느 스케일에서 스킬이 있는지(대류 소규모 강비 vs 광역 약비)를 진단.
- **읽는 법**: x=공간 스케일(웨이블릿 레벨, 2^j 격자), y=강수 강도 임계, 색=ISS(=1−MSE_scale/MSE_random). *좋은 패턴*: 큰 스케일·중간강도에서 스킬 높음(따뜻한 색). *나쁜 패턴*: 소규모·극한강도에서 낮음(찬 색, 흔한 약점), 특정 강도대 전 스케일 저조(그 강도 재현 실패). FSS(③)와 상보 — FSS는 이웃분율, ISS는 웨이블릿 스케일.
- **언제 쓰나**: [격자] 강수. 정사각(2ⁿ) 도메인 필요(패딩). 강도·스케일 동시 진단이 필요한 대류·혼합 강수.
- **짝지표 & 교차링크**: **ISS(강도×스케일)** → [`23` intensity-scale 카드], [`02`], [`05` 스펙트럼·웨이블릿]. 이웃 스케일 관점은 ③ FSS와 짝.
- **만드는 법**: 임계 이진화 후 `PyWavelets`(`pywt.wavedec2`, Haar)로 차이장 2D MRA → 스케일별 MSE→ISS 격자 → `matplotlib.pcolormesh`. R 대안 `SpatialVx::waveIS`(rdrr.io). 도메인 2^n 패딩·주기경계 처리.
- **함정·주의**(§G): **2ⁿ 격자·주기경계 가정**(비정사각·결측 처리 주의). 이진화가 강도 연속성 손실. 해석이 FSS보다 덜 직관적 → useful-scale이 필요하면 ③ 병행. 웨이블릿 종류·이진화 임계·도메인 크기 의존(advisory). **지도 아님**(축이 스케일×강도).
- **출처**: Casati, Ross & Stephenson (2004, *Meteorological Applications* 11(2):141–154, doi 확인요 / ADS 2004MeApp..11..141C); Casati (2010, *Weather and Forecasting* 25, 재정식화); Weniger, Kapp & Friederichs (2017, *QJRMS*, 웨이블릿 검증 리뷰); Briggs & Levine (1997, *Monthly Weather Review*, 웨이블릿 검증 기원).

---

### ★ wet-day 강수강도 PDF/CDF (강수강도 분포 / Wet-day intensity PDF/CDF, log-bin)
- **무엇을 보여주나**: 강수 **강도 분포**(약비~폭우)의 모델·관측 비교. wet-only(0 제외)로 그린 확률밀도(PDF)/누적분포(CDF), 그리고 계급별 **강수량 기여(amount distribution)**. 평균·총량이 못 보는 **"약비 과다 / 강비 과소"** 같은 분포 편향과 간헐성 특성(drizzle 문제)을 포착.
- **읽는 법**: x=강수강도(mm/day, **로그 bin**), y=밀도(빈도) 또는 계급 강수량 기여. *좋은 패턴*: 모델·관측 PDF/CDF 곡선 겹침. *나쁜 패턴*: **모델이 중간강도에 몰리고 저강도(drizzle) 과다·극한강도 과소**(흔한 계통오차), amount 분포 봉우리 위치가 다름(총량은 맞아도 강도구조 다름). 격자평균은 강도 꼬리를 평활 → 점 관측보다 극한 약함(자료형 대표성 명시). 고강도 bin에 부트스트랩 CI.
- **언제 쓰나**: [시계열]/[격자]. 시간·일 강도 분포. QQ(⑩)와 상보(히스토그램=밀도, QQ=분위수).
- **짝지표 & 교차링크**: **wet-day frequency·SDII·frequency/intensity 분해(⑨)·Perkins Skill Score** → [`23` 강수강도 PDF·wet-day 빈도 카드]. 분위수는 ⑩ QQ, 분포 겹침 스칼라는 [`23` Perkins]. PDF/CDF 정의·Perkins는 **공통편 [`16` Return-level & PDF/CDF/Perkins]** 교차링크.
- **만드는 법**: wet-only 서브셋(≥wet 임계) → `numpy.histogram(x, bins=np.logspace(...))`(로그 bin) 또는 `scipy.stats.gaussian_kde`; CDF는 `np.sort`/ECDF. amount distribution은 계급별 Σ강수량. `matplotlib` overlay(모델·관측). Perkins S = `np.minimum(p_m,p_o).sum()*Δx`.
- **함정·주의**(§G): **bin 선택·로그간격·wet 임계가 형상 인상을 바꿈** → 명시. 고강도 bin 표본희소로 불안정(CI 권장). 격자평균 vs 점 관측 대표성(격자는 극한 평활). 0 포함 시 점질량 왜곡 → **wet-only 권장**. 분포만 비교(동시성·상관 못 봄) → 범주·연속지표 병행. **지도 아님**.
- **출처**: [`23_domain_precipitation.md`]; Dai (2006, *Journal of Climate*, "Precipitation characteristics in eighteen coupled climate models" — frequency/intensity 편향); Sun et al. (2006, *Journal of Climate*, 빈도·강도 분해); Stephens et al. (2010, *JGR Atmospheres*, drizzle 문제); Perkins et al. (2007, *J. Climate* 20:4356–4376, doi:10.1175/JCLI4253.1).

---

### frequency×intensity 분해 그림 (빈도·강도 분해 / Frequency × intensity decomposition)
- **무엇을 보여주나**: 총 강수 평균편향 Δmean을 **빈도(f)·강도(I) 성분으로 분해**: Δmean = f·ΔI + I·Δf + Δf·ΔI. 막대/누적으로 표시해 "총량 편향이 **비를 너무 자주 뿌려서(Δf)** 인지 **강도를 잘못 잡아서(ΔI)** 인지"를 진단. wet-day 빈도(⑧과 짝)와 강도 편향을 분리.
- **읽는 법**: 막대=Δf·ΔI 기여(부호 포함), 합=Δmean. *읽기*: **Δf>0 & ΔI<0 = "too many wet days, too light"**(모델 drizzle 편향, 매우 흔함); Δf<0 & ΔI>0 = 비를 드물게·강하게. *나쁜 패턴*: 두 성분이 큰 반대부호로 상쇄되어 총량은 맞으나 물리가 틀림(총량만 보면 놓침). 지점·계절·기후대별 막대로 공간·계절 편향구조.
- **언제 쓰나**: [시계열]/[격자]. 총량은 맞는데 빈도·강도 분해가 어긋난 경우 진단. ⑧ wet-day 빈도·PDF와 한 세트.
- **짝지표 & 교차링크**: **wet-day frequency f·SDII(intensity I)·Δf·ΔI** → [`23` wet-day 빈도·강수강도 PDF 카드]. 분포 형상은 ⑧, 분위수는 ⑩.
- **만드는 법**: wet 임계로 f=P(wet)·I=mean(wet-day intensity) 산출 → 분해식 성분을 `numpy` 계산 → `matplotlib` 누적 막대. 지점·격자별 반복은 `xarray` apply.
- **함정·주의**(§G): **wet 임계 정의(0.1 vs 1 mm)가 f·I를 통째로 바꿈** → 명시. 격자평균은 약비를 더 자주 만들어 Δf를 편향(점 vs 격자 대표성). 잔차항 Δf·ΔI 무시 금지(큰 편향에서 유의). **지도 아님**(막대 그림; 공간 분포를 지도로 보려면 ⑪처럼 basemap).
- **출처**: [`23_domain_precipitation.md`]; Dai (2006); Sun et al. (2006, *Journal of Climate*); Stephens et al. (2010, drizzle 문제).

---

### ★ 강수 Q-Q plot (강수 분위수-분위수 도표 / Precipitation Q-Q plot, wet-only tail-emphasised)
- **무엇을 보여주나**: 모델·관측 강수 분위수를 1:1 대응시켜 분포 전체, 특히 **고분위(극한 강수) 꼬리** 일치를 진단. wet-only(0 제외)로 그려 점질량 왜곡을 제거하고 상위 분위(95·99·99.9%)에 초점. 평균지표가 못 잡는 극치 과소를 포착. (공통편 QQ를 **wet-only·상위 분위 조밀·강수식**으로 특화.)
- **읽는 법**: x=관측 분위수, y=모델 분위수(p=…95·99·99.9%). **상위 분위에서 1:1선 아래로 휘면 모델 극한 과소**(가장 흔한 약점), 위로 휘면 과대. 중앙부는 맞고 꼬리만 벌어지면 평균 OK·극치 NG. 격자평균은 상위 분위를 낮춤(자료형 대표성). 마커 크기로 percentile 표시, 극단 분위는 부트스트랩 CI.
- **언제 쓰나**: [격자]/[시계열]/[트랙]. 분포·극치 검증(시간정렬 불필요). quantile mapping 편향보정 전후 점검(13/15 연결).
- **짝지표 & 교차링크**: **percentile bias·KS·wet-only 분위수** → [`23` Q-Q/분위수 편향 카드]. 극단 꼬리는 ⑬(return-level)로 승급. 정의·일반 QQ는 **공통편 [`16` QQ-plot]** 교차링크. 분포 밀도는 ⑧ PDF와 짝.
- **만드는 법**: wet-only 서브셋 → `numpy.quantile`(공통 확률격자, 꼬리 조밀) 또는 `scipy.stats.probplot`. 산점 후 1:1선(`ax.axline`)·percentile 마커. 표본 적은 99.9%는 부트스트랩 CI 띠.
- **함정·주의**(§G): **분포만 비교 → 동시성·상관 못 봄**(상관 0이어도 QQ 완벽 가능) → 범주(①)·연속지표 병행. 극단 분위 불안정 → CI. **0 포함 QQ는 계단 왜곡** → wet-only. 모델·관측 wet 임계·누적창·기후대 통일 안 하면 꼬리가 인위적으로 갈림. **지도 아님**.
- **출처**: [`23_domain_precipitation.md`]; [`16_fig_common.md` QQ]; Wilks, *Statistical Methods in the Atmospheric Sciences*; Wilk & Gnanadesikan (1968, *Biometrika*).

---

### ★ 공간 bias/PBIAS/RMSE 지도 (강수 공간 차 지도 / Gridded precipitation bias / PBIAS / RMSE map)
- **무엇을 보여주나**: 우리 모델 [격자]를 격자 관측/재분석/위성강수 [격자]와 **면적 전면적**으로 비교해 bias(x,y)·PBIAS(x,y)·RMSE(x,y)·상관(x,y)을 **지도(색)** 로. 점 관측이 없는 곳까지 **계통오차의 지리적 위치·계절성**(산악 상풍측 과대·풍하측 과소, 해양 과소 등)을 진단. (공통편 §B bias/difference map을 강수·보존적 재격자로 특화.)
- **읽는 법**: 색=격자별 bias/PBIAS(**발산 색맵, 0=흰색**) 또는 RMSE(순차 색맵). *읽기*: 산악 지형강수 편향 띠, 연안·해양 과소, 계절 대비. 위도대·영역 평균선 병행. *나쁜 패턴*: 넓은 단색 영역(계통편차), **해안선 따라 줄무늬**(재격자/마스크 artifact), 격자 봉합선 줄무늬(보간 아티팩트).
- **언제 쓰나**: [격자]vs[격자] NetCDF(관측격자·ERA5·IMERG·레이더 QPE). 광역 진단, 점 검증(⑮)이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 격자별 **bias·PBIAS·RMSE·상관** → [`23` 공간 bias/RMSE 지도 카드], [`02` 공간패턴], [`15` regridding]. 점 검증 ⑮와 교차해석. 정의·발산맵은 **공통편 [`16` Bias/difference map]** 교차링크.
- **만드는 법**: `xarray`+`xesmf`(**conservative regridding**, 강수 총량 보존 — bilinear 금지)→공통 격자→격자별 통계→`matplotlib`/`cartopy` `pcolormesh`. **지도이므로 [plotting_maps.md `add_basemap`]로 해안선/육지+위경도 라벨 필수**. bias는 `TwoSlopeNorm(vcenter=0)`+`RdBu_r`/`cmocean.cm.balance`, RMSE는 `cmocean.cm.thermal`/viridis. 육지/해양·결측 마스크 통일.
- **함정·주의**(§G): **재분석·위성강수는 독립 진값 아님**(§G-1) → "정답"으로 과신 금지, 우량계와 교차. **bilinear 재격자는 강수 총량·극치 왜곡 → conservative 필수**. 관측격자 게이지 밀도 편중이 지역 신뢰도 좌우. 강수 상관은 간헐성 artefact(0 다수) 주의. **지도형** → basemap·위경도 라벨·(모델 lon 0–360이면 `((lon+180)%360)-180` 변환)·해양필드 육지마스킹·중위도 종횡비(GeoAxes 자동) 필수.
- **출처**: [`23_domain_precipitation.md`]; [`plotting_maps.md`]; Hersbach et al. (2020, *QJRMS* 146:1999–2049, ERA5); Adler et al. (2003, *Journal of Hydrometeorology* 4, GPCP 격자강수); cmocean(Thyng et al. 2016, doi:10.5670/oceanog.2016.66).

---

### ★ 강수 diurnal Hovmöller / 첨두시각 위상 지도 (일변동 진단 / Diurnal Hovmöller & peak-time phase map, LST)
- **무엇을 보여주나**: 강수의 **일변동(diurnal cycle)** — (a) **Hovmöller**(x=경도, y=하루 시각 LST, 색=합성 강수율)로 강수대의 하루 위상·전파를, (b) **첨두시각 위상 지도**(색상환=1차 조화 첨두시각 LST, 채도=진폭/평균)로 공간 위상·진폭을 모델·관측 비교. 대류강수 일변동 위상오차는 물리 모수화 결함의 대표 지표.
- **읽는 법**: (a) Hovmöller 등치선 기울기=강수대 이동(전파). (b) 색상환 지도: **육지 첨두 14–18 LST(오후~야간), 해양 04–08 LST**가 관측 전형. *나쁜 패턴*: 모델이 대류강수 첨두를 **너무 이르게(정오 무렵)** 모의(관측은 오후~야간), 진폭 과대/과소, 지형강수 야간 첨두 놓침. 모델·관측·차 3패널 권장. 진폭은 일평균의 20~50%(육지) 수준.
- **언제 쓰나**: [시계열]/[격자]. **시간(hourly) 자료 필요**. 대류허용 모델·위성(IMERG) 일변동 평가.
- **짝지표 & 교차링크**: **첨두시각(원형)·진폭비·위상차** → [`23` 계절성·일변동 카드], [`06` 시계열/위상]. Hovmöller 정의는 **공통편 [`16` Hovmöller 다이어그램]** 교차링크. 위상 wrap은 [`00` §4.2-8 원형통계].
- **만드는 법**: UTC→**LST 격자별 변환**(경도로 offset) 후 시각별 합성평균 → 1차 조화 적합(`numpy` cos/sin 회귀 또는 `scipy.optimize`로 24h+12h 2-mode fit)으로 첨두시각·진폭. Hovmöller는 `xarray` 위도평균 후 `plot.contourf(x='lon', y='hour')`. 위상 지도는 순환 색맵(`cmocean.cm.phase`/`hsv`)로 첨두시각, 지도이므로 **`add_basemap` 필수**.
- **함정·주의**(§G): **시간대(UTC/LST) 변환 오류 = 가짜 위상오차** — 격자별 LST 변환 필수. **위성은 관측시각 편중**(sun-synchronous sampling) → sampling 오차. 조화적합은 다봉(이중 첨두) 일변동을 단순화. **첨두시각은 원형통계(0/24 wrap)** — 일반 평균 금지. (b) 위상 지도는 **지도형** → basemap·위경도 라벨 필수; (a) Hovmöller는 축이 경도×시간이나 경도축이므로 위경도 라벨 권장(엄밀히 반지도).
- **출처**: [`23_domain_precipitation.md`]; Dai (2001, *Journal of Climate* 14, "Global precipitation and thunderstorm frequencies, Part II: Diurnal variations"); Covey et al. (2016, *Journal of Climate*, CMIP 일변동); Watters et al. (2021, *Remote Sensing* 11(15):1781 계열, IMERG diurnal); Hovmöller (1949, *Tellus* 1(2):62–66, doi:10.1111/j.2153-3490.1949.tb01260.x).

---

### ★ 극치 return-level 플롯 (재현수준 도표 / Extreme-value return-level plot, POT-GPD/GEV)
- **무엇을 보여주나**: 장기 모델·관측 강수의 **극치 분포**를 재현주기(return period) vs 재현수준(return level) 곡선(신뢰구간 띠)으로 진단. 50·100년 **설계강우(design storm)** 와 모델의 극한강수 재현(흔히 과소)을 평가. 방재·수공 설계의 핵심. (공통편 return-level을 강수 특화: wet-day 상위 백분위 임계·declustering·형상 ξ>0.)
- **읽는 법**: x=재현주기(로그, 년), y=강수량(mm). 점=경험분위(plotting position)·선=GPD/GEV 적합·음영=CI. *좋은 패턴*: 관측 경험점이 모델 적합곡선 **CI 띠 안**·두 곡선 중첩. *나쁜 패턴*: **모델 곡선이 관측 점 아래=극치 과소**(호우 underestimate, 흔함). 짧은 기록의 100년값 외삽은 과신 금지(넓은 CI). 극값 QQ/probability plot 동반(tail 적합).
- **언제 쓰나**: 장기 [시계열](우량계)·[격자] hindcast/재분석(가능하면 ≥30년). 일·시간 극한. 설계·위험 평가.
- **짝지표 & 교차링크**: **POT-GPD/연최대-GEV 매개변수(μ,σ,ξ)·N년 return value·부트스트랩 CI** → [`23` 극치강수 POT-GPD/GEV 카드], [`03` GEV/POT/return level]. tail은 ⑩ QQ의 극단 확대판. return-level 정의는 **공통편 [`16` Return-level & PDF/CDF]** 교차링크.
- **만드는 법**: **`pyextremes`**(`EVA` 객체: `get_extremes('POT'/'BM')`, `fit_model('GP'/'GEV')`, `plot_return_values`, `plot_diagnostic`=return level+QQ+PDF+probability) 또는 `scipy.stats.genpareto`/`genextreme`. 임계는 wet-day 상위 백분위(95~99%)·MRL(mean residual life)plot·parameter-stability로, **declustering으로 폭우일 독립성** 확보.
- **함정·주의**(§G): **임계 선택·declustering·표본수에 극도로 민감** → **부트스트랩 CI 필수**. 형상 ξ>0(두꺼운 꼬리)이 강수 전형. **격자평균은 점 극치를 과소**(areal reduction factor 차이). 비정상성(기후추세·계절)으로 단일 분포 가정 붕괴 가능(비정상 GEV 검토). 위성·레이더 극치는 알고리즘 saturation 주의. **지도 아님**(축이 재현주기×강수량).
- **출처**: [`23_domain_precipitation.md`]; Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Katz, Parlange & Naveau (2002, *Advances in Water Resources* 25, "Statistics of extremes in hydrology"); pyextremes(georgebv.github.io/pyextremes).

---

### ETCCDI 극한지수 지도·산점 (기후 극한지수 / ETCCDI precipitation indices map & scatter)
- **무엇을 보여주나**: 국제 표준 **기후 극한지수**(Rx1day·Rx5day·R95pTOT·SDII·CDD·CWD·R10mm·R20mm·PRCPTOT)를 모델·관측 간 지도(공간 편향)·산점(지점 대응)·Taylor로 비교. 기후 스케일 강수 극한·간헐성 통계의 공용어로 다운스케일·재분석·위성 평가.
- **읽는 법**: 각 지수의 (a) bias 지도(발산맵), (b) 모델 vs 관측 산점(1:1). *읽기*: **Rx1day/Rx5day(극한 강도)**·R95pTOT(극한 기여)에서 격자평균 과소, **CDD(연속 건조일)**·CWD(연속 습윤일)로 간헐성 재현, SDII(강도)·PRCPTOT(총량). *나쁜 패턴*: 산악·극한 지수 계통 과소, CDD 과대(건조 편향). 지수별 bias/RMSE·패턴상관·Taylor로 다지수 요약.
- **언제 쓰나**: 일강수 [시계열]/[격자]. 기후(다년) 비교. R95p류는 기준기간(예 1961–1990) 정의 필수.
- **짝지표 & 교차링크**: **지수별 bias·RMSE·패턴상관** → [`23` ETCCDI 극한지수 카드]. 다지수 요약은 **공통편 [`16` Taylor diagram]**, 공간 편향은 ⑪ 지도, 극한 재현주기는 ⑬.
- **만드는 법**: **`icclim`** 또는 **`xclim.indicators`**(ETCCDI 표준 구현, 수식 재구현 오류 방지)로 지수 산출 → 지도는 ⑪처럼 `cartopy`+`add_basemap`(지도형), 산점·Taylor는 지도 아님. wet 임계 1mm·동일 기준기간·결측규칙 통일.
- **함정·주의**(§G): **기준기간 불일치 시 R95p·백분위 지수 비교 무효**. wet 임계(1mm) 고정 필수. **격자평균은 Rx1day 등 극한을 과소**(점 vs 격자 대표성). 결측일 한도 통일. **climdex/icclim/xclim 등 표준 구현 사용 권장**(수식 재구현 오류 방지). 지수 지도는 **지도형** → basemap 필수; 산점/Taylor는 지도 아님.
- **출처**: Zhang et al. (2011, *WIREs Climate Change* 2, ETCCDI 지수); Klein Tank, Zwiers & Zhang (2009, WMO-TD No. 1500 / WCDMP-72, ETCCDI 지침); icclim/xclim 문서(xclim.readthedocs.io).

---

### ★ 위성강수 매치업 산점도 (위성강수 검증 산점 / Satellite precipitation matchup scatter, IMERG/GPM)
- **무엇을 보여주나**: 위성강수([격자] L3/L4 또는 [트랙])를 우량계·레이더 QPE와 콜로케이션한 산점도(밀도 hexbin)에 **연속(bias·PBIAS·RMSE·CC)+범주(POD·FAR·CSI) box**를 함께 얹어, 관측이 성긴 해역·산악의 유일한 광역 강수원인 위성강수를 **연속+범주 동시** 검증. (공통편 산점도를 강수·위성 매치업으로 특화.)
- **읽는 법**: x=우량계/레이더(기준), y=위성. 1:1선·회귀선·밀도(로그). *좋은 패턴*: 점운 1:1 밀착, 열대·convective에서 탐지 양호. *나쁜 패턴*: **약비·고체강수·산악·연안에서 저조**(위성 IR-only 시간대·지형오염), 저강도 과다탐지(FAR↑), 극한 saturation(고값 1:1 아래). box에 CC·PBIAS·RMSE·POD·FAR·CSI·N. IMERG **Early/Late/Final** 버전 구분 표기.
- **언제 쓰나**: 위성 [격자]/[트랙] vs 우량계 [시계열]/레이더 [격자]. 30분~월 누적. 광역·산악·해양.
- **짝지표 & 교차링크**: **bias·PBIAS·RMSE·CC + POD·FAR·CSI** → [`23` 위성강수 매치업 카드], [`12` 위성 매치업]. 범주 종합은 ① 성능도표, 공간 분포는 ⑪ 지도, 밀도산점 정의는 **공통편 [`16` 산점도·밀도산점도]** 교차링크.
- **만드는 법**: `xarray`로 위성 격자에 우량계 **point-to-pixel**(또는 우량계 격자화 후 grid-to-grid) 콜로케이션(동일 누적창) → `matplotlib` `hexbin(bins='log')` + 연속·범주 지표 box. 위성 QC(coast/지형·IR-only flag) 필수.
- **함정·주의**(§G): **IMERG Final은 GPCC 게이지 보정 산물** → 그 우량계로 "독립 검증" 시 오차상관(§G-2/3, TC 독립 3자 부적합) → Early/Late 또는 독립 게이지 사용. **point vs pixel 대표성 오차**. 위성은 순간관측→누적 sampling 오차. 고체강수·약강수 탐지 취약. 산출물·버전·누적창·기후대 강의존(advisory). 산점도는 **지도 아님**(트랙 위치를 보려면 ⑪처럼 basemap 지도 별도).
- **출처**: [`23_domain_precipitation.md`]; Huffman et al. (2020, in *Satellite Precipitation Measurement*, Springer, "IMERG"); Kidd & Levizzani (2011, *HESS* 15, 위성강수 검증 리뷰); Tang et al. (2020, *Remote Sensing of Environment*, IMERG V06 평가); Maggioni, Meyers & Robinson (2016, *Journal of Hydrometeorology* 17, 위성강수 오차 리뷰).

---

### radar–gauge merging 진단 (레이더-우량계 병합 진단 / Radar–gauge merging diagnostics)
- **무엇을 보여주나**: 레이더 QPE의 우량계 대비 편의(Z–R·밝은띠·빔차폐·감쇠)를 진단하는 **G/R 비 산점도**와, 병합(MFB·KED·conditional merging) **전후 격자강수 지도**를 나란히. 레이더 공간패턴+우량계 국소정확도를 합쳐 **기준 격자강수(reference)를 만드는 단계**의 검증.
- **읽는 법**: (a) G/R 산점: x=레이더, y=우량계. 1:1 아래 쏠림=레이더 과대, 위=과소; **거리에 따라 산포 증가(range degradation)**, 저강도 밝은띠 과대. (b) 병합 전후 지도: 병합 후 우량계 국소값에 맞으며 레이더 공간패턴 보존이면 양호. *나쁜 패턴*: MFB(전역 배수)만으로 국소 편의 못 잡음, 저밀도 우량계에서 크리깅 불안정(bullseye artefact), 산악 빔차폐역 근본 한계.
- **언제 쓰나**: 레이더 [격자] + 우량계 [시계열]. 시간~일 누적. 기준 격자강수 생성·QPE 편의 진단.
- **짝지표 & 교차링크**: **G/R 비·PBIAS + 병합법(MFB·KED·conditional merging)·leave-one-out CV** → [`23` 레이더 QPE·radar–gauge merging 카드], [`15` matchup·kriging]. 병합 결과를 기준으로 쓰면 ⑪/③ 그림의 관측 축이 됨.
- **만드는 법**: G/R 산점 `matplotlib`; 병합은 `pykrige`(KED/regression kriging)·`wradlib`(레이더 QC·adjust: MFB/kriging)·conditional merging 자체구현. 병합 전후 지도는 ⑪처럼 `cartopy`+**`add_basemap`**(지도형). leave-one-out으로 병합 검증.
- **함정·주의**(§G): **병합 산물은 우량계가 이미 반영** → 그 우량계로 재검증하면 독립 아님(§G-3, **leave-one-out CV 필요**). 저밀도 우량계에서 크리깅 불안정. 레이더 QC(clutter·brightband·beam blockage·attenuation) 미흡 시 병합이 오차 전파. **산악 빔차폐역은 근본적 한계**. 병합법 우열은 지역·사건 의존(advisory). 병합 전후 지도는 **지도형** → basemap·위경도 라벨 필수; G/R 산점은 지도 아님.
- **출처**: [`23_domain_precipitation.md`]; [`plotting_maps.md`]; Goudenhoofdt & Delobbe (2009, *HESS* 13, "Evaluation of radar-gauge merging methods for QPE"); Sinclair & Pegram (2005, *Atmospheric Science Letters* 6, conditional merging); Berndt, Rabiei & Haberlandt (2014, *Journal of Hydrology* 508, 병합법 비교); `wradlib`(wradlib.org).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 23(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 23(및 16 등) 교차링크 |
|---|---|---|---|---|---|
| 1 | 성능도표 (Roebber, 임계 스캔) | 시계열·격자·트랙 | 범주 종합 | POD·SR·CSI·FBI·GSS | 23 분할표/CSI·(공통 16 성능도표) |
| 2 | 분할표 지표 vs 임계 곡선 | 시계열·격자 | 임계 의존성 | FBI·POD·FAR·CSI·GSS | 23 분할표 · EDI/SEDI |
| 3 | FSS 스케일–임계 히트맵 | 격자 | 위치오차·유효스케일 | FSS·useful scale | 23 FSS · 02 · (공통 16 FSS) |
| 4 | double-penalty 진단 패널 | 격자 | 위치 vs 강도 오차 | FSS 스케일반응·SAL L | 23 double-penalty · 14 |
| 5 | 객체기반 SAL 산점도 | 격자 | 구조·양·위치 분해 | S·A·L | 23 SAL · (공통 16 SAL/MODE) |
| 6 | MODE 객체 매칭 지도 ★지도 | 격자 | 객체 속성·매칭 | 객체속성·total interest | 23 MODE · 02 |
| 7 | intensity-scale (Casati ISS) | 격자 | 강도×스케일 오차 | ISS | 23 intensity-scale · 05 |
| 8 | wet-day 강도 PDF/CDF | 시계열·격자 | 분포(강도) | SDII·Perkins S | 23 강수강도 PDF · (공통 16 PDF/CDF) |
| 9 | frequency×intensity 분해 | 시계열·격자 | 총량편향 원천 | f·I·Δf·ΔI | 23 wet-day 빈도·강도 |
| 10 | 강수 Q-Q plot (wet-only tail) | 시계열·격자·트랙 | 분포·극치 | percentile bias·KS | 23 Q-Q · (공통 16 QQ) |
| 11 | 공간 bias/PBIAS/RMSE 지도 ★지도 | 격자 | 편향+패턴(공간) | 격자별 bias·PBIAS·RMSE | 23 공간지도 · 02 · 15 |
| 12 | diurnal Hovmöller·첨두시각 지도 ★반/지도 | 시계열·격자 | 일변동 위상·진폭 | 첨두시각·진폭비 | 23 일변동 · 06 · (공통 16 Hovmöller) |
| 13 | return-level 플롯 (POT-GPD/GEV) | 시계열·격자 | 극값·재현주기 | GPD/GEV·N년값·CI | 23 극치 · 03 GEV/POT |
| 14 | ETCCDI 극한지수 지도·산점 ★지도(지수맵) | 시계열·격자 | 기후 극한·간헐성 | 지수별 bias·RMSE·패턴상관 | 23 ETCCDI · (공통 16 Taylor) |
| 15 | 위성강수 매치업 산점 (IMERG/GPM) | 격자·트랙·시계열 | 연속+범주(광역) | bias·PBIAS·CC·POD·FAR·CSI | 23 위성강수 · 12 |
| 16 | radar–gauge merging 진단 ★지도(전후맵) | 격자·시계열 | QPE 편의·기준생성 | G/R비·PBIAS·병합법 | 23 레이더 QPE · 15 |

> **묶음 권고**: 단일 그림 금지 원칙(§G)에 따라 강수 검증 보고는 최소 **①(범주 종합) + ⑧/⑩(분포·극치) + ③/⑪(공간·위치)** 3축을 기본 세트로, 고해상도·AI 강수면 **④ double-penalty + ⑤/⑥ 객체**, 극한·설계면 **⑬/⑭**, 위성·광역이면 **⑮ + ⑪**, 레이더 기준생성이면 **⑯**, 일변동·물리진단이면 **⑫**를 추가한다. 모든 임계(FSS useful=0.5+f₀/2, wet 임계 등)는 **advisory + 영역·기후대 의존 경고**로, 지도형(⑥·⑪·⑫·⑭·⑯)은 **`add_basemap`(해안선/육지+위경도 라벨)** 을 캡션·코드에 단다.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·QQ·PDF/CDF·회귀 등 표준 시각화).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (분할표·ROC·범주·분포).
- Coles (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD return level).
- Klein Tank, Zwiers & Zhang (2009) WMO-TD No. 1500 / WCDMP-72 (ETCCDI 지수 지침).

**학술 논문 (제목·저널·연도 웹 확인)**
- Roebber (2009) "Visualizing Multiple Measures of Forecast Quality," *Weather and Forecasting* 24(2):601–608. (doi:10.1175/2008WAF2222159.1)
- Roberts & Lean (2008) "Scale-Selective Verification of Rainfall Accumulations from High-Resolution Forecasts of Convective Events," *Monthly Weather Review* 136(1):78–97. (doi:10.1175/2007MWR2123.1)
- Wernli, Paulat, Hagen & Frei (2008) "SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts," *Monthly Weather Review* 136(11):4470–4487. (doi:10.1175/2008MWR2415.1)
- Casati, Ross & Stephenson (2004) "A new intensity-scale approach for the verification of spatial precipitation forecasts," *Meteorological Applications* 11(2):141–154. (ADS 2004MeApp..11..141C; DOI 확인요)
- Gilleland, Ahijevych, Brown, Casati & Ebert (2009) "Intercomparison of Spatial Forecast Verification Methods," *Weather and Forecasting* 24(5). (ICP 총론)
- Davis, Brown & Bullock (2006) "Object-Based Verification of Precipitation Forecasts, Part I/II," *Monthly Weather Review* 134:1772–1795. (DOI 확인요)
- Dai (2006) "Precipitation Characteristics in Eighteen Coupled Climate Models," *Journal of Climate* (frequency/intensity 편향).
- Dai (2001) "Global Precipitation and Thunderstorm Frequencies, Part II: Diurnal Variations," *Journal of Climate* 14.
- Sun et al. (2006) *Journal of Climate* (빈도·강도 분해); Stephens et al. (2010) *JGR Atmospheres* (drizzle 문제).
- Perkins, Pitman, Holbrook & McAneney (2007) *Journal of Climate* 20:4356–4376. (doi:10.1175/JCLI4253.1, PDF skill score)
- Zhang et al. (2011) "Indices for monitoring changes in extremes...," *WIREs Climate Change* 2.
- Katz, Parlange & Naveau (2002) "Statistics of extremes in hydrology," *Advances in Water Resources* 25.
- Huffman et al. (2020) "IMERG," in *Satellite Precipitation Measurement*, Springer.
- Kidd & Levizzani (2011) *HESS* 15 (위성강수 검증 리뷰); Tang et al. (2020) *Remote Sensing of Environment* (IMERG V06); Maggioni, Meyers & Robinson (2016) *Journal of Hydrometeorology* 17 (오차 리뷰).
- Goudenhoofdt & Delobbe (2009) "Evaluation of radar-gauge merging methods for QPE," *HESS* 13; Sinclair & Pegram (2005) *Atmospheric Science Letters* 6 (conditional merging); Berndt, Rabiei & Haberlandt (2014) *Journal of Hydrology* 508.
- Hersbach et al. (2020) "The ERA5 global reanalysis," *QJRMS* 146:1999–2049; Adler et al. (2003) GPCP, *Journal of Hydrometeorology* 4.
- Hovmöller (1949) "The Trough-and-Ridge diagram," *Tellus* 1(2):62–66. (doi:10.1111/j.2153-3490.1949.tb01260.x)
- Skok & Roberts (2016) *QJRMS* (useful-scale 재검토); Mittermaier & Roberts (2010) *Weather and Forecasting* 25.
- Covey et al. (2016) *Journal of Climate* (CMIP 일변동).

**기관 자료·기술보고 (실재 URL)**
- CAWCR/WWRP-JWGFVR Performance Diagram: https://www.cawcr.gov.au/projects/verification/Roebber/PerformanceDiagram.html
- DTC MET/METplus User's Guide — MODE / Wavelet-Stat Tool: https://metplus.readthedocs.io/projects/met/en/latest/Users_Guide/mode.html · .../wavelet-stat.html
- WMO SPICE (게이지 undercatch) — Kochendorfer et al. (2017, *HESS*).

**소프트웨어 (실존 도구)**
- `pysteps` — FSS(`verification.spatialscores.fss_init/fss_accum/fss_compute`)·SAL(`verification.salscores.sal`): https://pysteps.readthedocs.io (Pulkkinen et al. 2019, *GMD* 12:4185–4219).
- `pyextremes` — POT/GEV·return level·진단도: https://georgebv.github.io/pyextremes (`EVA`, `plot_return_values`, `plot_diagnostic`).
- `icclim` / `xclim` — ETCCDI 극한지수 표준 구현: https://xclim.readthedocs.io.
- `MET`/`METplus` — MODE-Tool·Wavelet-Stat: https://metplus.readthedocs.io.
- `scores` — FSS 등 검증(`scores.spatial.fss_2d`).
- `PyWavelets`(`pywt.wavedec2`, Haar) — intensity-scale MRA; R 대안 `SpatialVx::waveIS`.
- `pykrige`/`wradlib` — radar–gauge merging(KED·conditional merging·레이더 QC).
- `xarray`/`xesmf`(**conservative** regridding)·`cartopy`(+`add_basemap`)·`cmocean`·`matplotlib`·`numpy`·`scipy`·`xskillscore`.

**확인요 (확정 인용 금지 — §G-5)**
- Casati et al. (2004) *Meteorological Applications* 11(2):141–154 — 제목·저널·권·페이지·ADS(2004MeApp..11..141C) 확인, **DOI는 미검증(확인요)**.
- Davis, Brown & Bullock (2006) MODE Part I/II *Monthly Weather Review* 134 — 제목·저널·연도 확인, **DOI 미확정(확인요)**.
- IMERG diurnal 적용례(*Remote Sensing* 11(15):1781 계열, Watters et al. 2021) — URL 확인, **정확한 권·페이지·저자 재확인요**.
- 해석 임계(FSS useful=0.5+f₀/2, wet 임계 0.1/1 mm, CC≥0.7, 육지 첨두 14–18 LST 등)는 **관행 advisory** — 기후대·해상도·기준자료 의존(§G-4).
- IMERG Final·radar–gauge 병합산물은 **게이지 반영** → 독립 검증·독립 3자(TC) 부적합(§G-2/3, 확인·명시 필요).
