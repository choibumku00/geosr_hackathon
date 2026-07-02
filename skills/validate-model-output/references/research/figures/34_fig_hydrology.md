# 34. 검증 시각화 카탈로그 — 수문·하천편 (Verification Figures: Hydrology / Streamflow)

이 문서는 수문·수리 모델(HEC-HMS, VIC, SWAT, mHM, GR4J, HYPE, LISFLOOD, WRF-Hydro/NWM, 육상표면모형 CLM/Noah-MP 등)이 산출한 **하천유량(river discharge)·유출(runoff)·저수량**을 관측(수위·유량관측소 hydrometric station)·재분석·위성(GRDC/USGS/WRIS, GloFAS·ERA5-Land runoff, GRACE TWS, SWOT)과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 수문 도메인편이다. 메서드(수치지표) 카드는 [`26_domain_hydrology.md`](../26_domain_hydrology.md)에 있고(**대응 메서드카탈로그: 26_domain_hydrology.md**), 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **공통/횡단 그림과의 분담**: Taylor·Target·일반 QQ·ROC·reliability·rank histogram·성능 다이어그램·PDF/CDF·Return-level(GEV/POT) 엔진 등 **도메인 무관 요약그림은 [공통편] [`16_fig_common.md`](./16_fig_common.md) 담당**이라 여기서 중복 정의하지 않는다. 이 파일은 **수문 고유 그림**(수문곡선 overlay, FDC 로그, KGE 성분, 홍수빈도, 수문서명 radar, 유역 KGE 지도, 첨두 timing, 물수지 closure 등)과 **공통 그림의 수문식 변형**(저유량 로그공간을 강조한 산점도 등)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "교차링크"에서 가리킨다.

> **자료형 약어**: [시계열]=관측소 유량/수위 CSV·일/시 시계열 · [격자]=NetCDF 격자(모델 runoff·TWS·범람지도) · [위성]=GRACE TWS·위성고도계 하천수위·SWOT · [사건]=홍수사건 추출 수문곡선.

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 관측유량은 수위–유량 관계식(rating curve)으로 환산된 **2차 산출**이고 고·저유량 극단에서 rating error가 크다. GRDC/재분석/위성도 reference이지 truth가 아니다. 축·캡션에 "모델−관측(reference)"으로 쓰고 "오차"로 단정하지 않는다.
> 2. **해석 임계는 advisory.** Moriasi 등급(NSE>0.5 등)·KGE>0.75·Fit/CSI 0.5~0.8은 **월단위·특정 유역군 관행값**이며 **일/시 단위·건조/소유역에서 훨씬 낮게 나오는 것이 정상**. good/bad를 그림에 단정 표기하지 말고 영역·시간해상도·기후 의존 경고를 캡션에 둔다.
> 3. **benchmark 대비 상대평가.** NSE<0 또는 KGE<−0.41이면 "평균유량 benchmark만도 못함"(Knoben 2019). 절대 임계보다 benchmark skill로 판정한다(→ 다서명 진단 카드).
> 4. **단일 그림 금지.** 산점도(정확도) 하나로 결론내지 말고 최소 **정확도+물수지+분포/서명** 3축(예: 수문곡선 overlay + FDC + KGE 성분)과 유의성(블록 부트스트랩)을 함께 낸다.
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문의 도판을 그대로 재현하지 않는다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **수문곡선 overlay + 잔차 패널 (obs vs sim, 사건 확대)** — 수문 검증의 1차 대표 그림
2. ★ **유황곡선 FDC (로그 종축, obs vs sim)** — 유량 분포·변동 구조 서명
3. ★ **유량 검증 산점도 (log축, 1:1·회귀·KGE/NSE box)** — 정확도+조건부 편향
4. ★ **KGE 성분 플롯 (r·β·α 막대/삼각)** — 어느 축이 문제인지 진단
5. ★ **홍수빈도 플롯 (재현주기 vs 첨두유량, GEV/GPD·CI)** — 설계홍수
6. ★ **수문서명 radar / spider (다서명 동시비교)** — FDC·BFI·감수·timing 통합
7. ★ **유역별 KGE/NSE 공간 지도 (basemap)** — 성능의 지리분포
8. ★ **첨두유량 timing 산점 (Δt·Δpeak)** — 사건 첨두 크기·시각 오차
9. ★ **물수지 closure 막대 (P−ET−Q−ΔS)** — 수지 잔차 진단
10. ★ **다지점 KGE/NSE boxplot·CDF (성능 분포)** — 대표본 성능 요약
11. ★ **FDC 서명 편향 플롯 (FHV·FLV·FMS·slope)** — 구간별 편향 정량
12. **기저유출 분리 시계열 (baseflow·BFI)** — 저류-방류 물리
13. **감수곡선 진단 (Recession: −dQ/dt vs Q, log-log)** — 감수상수·저류거동
14. **홍수범람 공간검증 지도 (Flood extent CSI, basemap)** — 침수역 일치
15. **GRACE TWS anomaly 시계열·지도 (저류변화)** — 위성 저류 제약
16. ★ **관측소 위치도 (station location map, basemap)** — 정점 위치·ID

---

### ★ 수문곡선 overlay + 잔차 패널 (수문곡선 중첩·잔차 / Hydrograph overlay with residual panel, event zoom)
- **무엇을 보여주나**: 한 관측소에서 모델·관측 유량 Q(t)를 **시간축에 겹쳐** 그리고, 아래 패널에 **잔차(sim−obs)** 를 둔다. 폭풍/융설 사건의 **첨두 타이밍·진폭·상승/하강 형상·기저유량 offset·계통편차**를 직접 본다. 대표 사건은 별도 **확대(zoom) 패널**로. 수문모델 검증의 표준 1장.
- **읽는 법**: 상단 두 선의 **첨두 시각 어긋남=timing 오차**, 첨두 높이 차=진폭 오차, 항상 한쪽이 위면 편향. 하단 잔차가 0 주위 무작위면 양호; **사건마다 같은 부호로 튀면 계통 응답오차**; 감수구간에서 모델이 항상 위면 기저 과다. 첨두는 log축이면 눌려 보이므로 사건 zoom은 선형축 권장. *좋은 패턴*: 상승·첨두·감수가 위상·크기 모두 겹침. *나쁜 패턴*: 첨두 눌림(평탄화·α<1), 첨두 지연, 감수 너무 빠름/느림(감수상수 오차).
- **언제 쓰나**: [시계열] 단일/소수 지점 정밀 진단, 홍수·융설 사례 분석, 예보 선행시간별 열화 점검. 산점도(집계)가 못 보는 *언제·왜*를 본다.
- **짝지표 & 교차링크**: 사건 KGE/NSE·**첨두·용적·timing 오차**(⑧) → [`26` 수문곡선 사건지표·첨두 timing]; 위상오차 정량(교차상관 lag)·잔차 백색성 → [`06` lag/STL]; 편향은 [`01`]. 다지점 요약은 공통편 **Taylor**([`16`]). 형상 전체는 ⑥ radar.
- **만드는 법**: `pandas`/`xarray` 시간정렬 후 `matplotlib` 2-패널(`sharex`), `fill_between`로 ±잔차 음영. **`hydrostats.visual.hydrograph`** 또는 `hydrofunctions` 그래프 유틸도 사용 가능. 결측 구간은 끊어 그림(직선보간으로 잇지 말 것). 사건 zoom은 `ax.set_xlim` 서브패널.
- **함정·주의**: 모델·관측 **시간기준(UTC/순간 vs 일평균·윈도우) 불일치**가 가짜 위상오차 생성. 관측 결측 직선보간은 사건 통계 왜곡. **log축은 첨두를 눌러** 사건 진단을 가림 → 사건 zoom은 선형. 한 지점 결론을 유역 전체로 일반화 금지(대표성). 관측유량 rating error(고유량 외삽)가 첨두 잔차에 섞임 — 모델 탓 단정 금지.
- **출처**: WMO, *Guide to Hydrological Practices* (WMO-No. 168, Vol. II 예보검증); Ewen (2011, *Hydrology Research*, hydrograph 시각오차); Roberts et al. 방식과 무관—`hydrostats`(Roberts, Williams et al. 2018, *Hydrology* 5(4):66, doi:10.3390/hydrology5040066, `hydrograph` 시각화).

---

### ★ 유황곡선 FDC (유황곡선 / Flow Duration Curve, log-y, obs vs sim)
- **무엇을 보여주나**: 유량이 특정 값을 초과하는 시간비율(초과확률 p)을 x, 유량 Q를 y(로그)로 그린 누적 서명을 **모델·관측 두 곡선 중첩**. 모델이 유량의 **전체 분포·변동성 구조**(홍수~갈수)를 시간정렬 없이 재현하는지 진단. 수문 검증 핵심 3축의 하나.
- **읽는 법**: x=초과확률(0~1 또는 %), y=Q(로그). **좌측(낮은 p)=고유량**, **우측(높은 p)=저유량**. 고유량단에서 모델선이 관측선 **아래**면 첨두 과소; 저유량단에서 벌어지면 갈수 재현 불량; 곡선 **기울기(slope)** 는 유역 반응성/변동성. *좋은 패턴*: 두 곡선이 전 구간 밀착. *나쁜 패턴*: 상단(고유량) 처짐(과소), 하단(저유량) 평탄/들뜸(기저 과다), 중간 기울기 불일치(변동성 α≠1).
- **언제 쓰나**: [시계열] 유량 분포·기후 검증(timing 불필요). 격자 유출은 셀별 FDC 가능. quantile mapping 보정 전후 점검.
- **짝지표 & 교차링크**: **Q5·Q95·FDC slope·FHV·FLV·FMS**(⑪) → [`26` FDC·FDC 서명 카드]; 분포 일치는 공통편 **QQ·PDF/CDF**([`16`]); 저유량은 ⑫ BFI. 동시성(상관)은 못 봄 → ①과 3축 구성.
- **만드는 법**: 유량 내림차순 정렬, p=m/(n+1)(Weibull plotting position) → `matplotlib` `semilogy`. **`hydrosignatures`(HyRiver)** `flow_duration_curve_slope`·`exceedance` 유틸, 또는 `numpy.sort`+`ax.semilogy` 직접. 모델·관측 **동일 기간·동일 plotting position** 강제.
- **함정·주의**: **분포만 비교 → 동시성·timing은 못 봄**(상관 0이어도 FDC 완벽 가능) → KGE/수문곡선과 상보. 기간이 다르면 직접비교 불가(FDC는 결측·기간 차에 민감). 로그축이라 저유량 차이가 시각적으로 과장/과소될 수 있음(서명 ⑪로 정량화 병행).
- **출처**: Vogel & Fennessey (1994, *Journal of Water Resources Planning and Management* 120(4):485–504); Searcy (1959, USGS Water-Supply Paper 1542-A); Yilmaz, Gupta & Wagener (2008, *WRR* 44, W09417, doi:10.1029/2007WR006716); `hydrosignatures`(HyRiver, docs.hyriver.io).

---

### ★ 유량 검증 산점도 (유량 산점도 / Discharge validation scatter, log axes, KGE/NSE box)
- **무엇을 보여주나**: 매치업된 (관측 Q, 모델 Q) 쌍을 산점하고 1:1선·회귀선·핵심 스칼라(KGE·NSE·PBIAS·r·N)를 함께 얹은 정확도 1차 그림. 유량은 동적범위가 커(홍수~갈수 수백~수천 배) **로그축**이 사실상 필수인 점이 공통편 산점도의 수문식 변형.
- **읽는 법**: x=관측, y=모델, **양축 log**. **1:1선**(점선) 기준, 회귀선(실선). 점이 1:1 위/아래로 쏠리면 과대/과소. 고유량에서 회귀선이 1:1 아래로 휘면 **첨두 과소**(수문모델 전형). 저유량 로그공간에서 점운이 부채꼴로 퍼지면 갈수 재현 불안정(+rating error). 텍스트 box에 KGE·NSE·PBIAS·r·N. *좋은 패턴*: 점운 1:1 밀착·전 구간 균질. *나쁜 패턴*: 저유량 큰 산포(로그축), 고유량 saturation.
- **언제 쓰나**: [시계열]/[격자 지점집계] 어디서나. 모델·관측 1쌍 또는 다지점 집계. 정확도+편향 동시 1차 점검.
- **짝지표 & 교차링크**: **KGE(성분 ④)·NSE·lnNSE·PBIAS·RSR·r** → [`26` NSE·KGE·PBIAS·RSR 카드]; 밀도(대용량)·1:1·회귀 일반론과 log축 처리는 공통편 **산점도·밀도산점도**([`16`]); 분포는 ② FDC / 공통 QQ.
- **만드는 법**: `matplotlib` `ax.scatter` + `ax.set_xscale('log')`/`set_yscale('log')` + `ax.axline((q0,q0),slope=1)`. 지표는 **`HydroErr`**(`kge_2012`, `nse`, `pbias`) 또는 **`hydrostats`**/`spotpy.objectivefunctions`(`kge`, `nashsutcliffe`). 축 동일 범위·`set_aspect('equal')`. 0/음수 유량은 log 전 마스킹·ε 규약 명시.
- **함정·주의**: 유량 **log축 필수**(선형축은 첨두가 모든 스케일을 먹어 저유량 구조 은폐). **OLS는 관측 무오차 가정** → rating error 큰 유량엔 부적절(robust/Theil-Sen 병기 고려). 자기상관 강한 일유량은 유효표본 과대(밀도·유의성 과신 금지). 0유량(간헐하천) log 처리 규약 명시.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·회귀); Gupta et al. (2009, *Journal of Hydrology* 377:80–91, doi:10.1016/j.jhydrol.2009.08.003, KGE); `HydroErr`/`hydrostats`(Roberts et al. 2018, *Hydrology* 5(4):66, doi:10.3390/hydrology5040066).

---

### ★ KGE 성분 플롯 (KGE 성분 분해 / KGE component plot: r · β · α)
- **무엇을 보여주나**: 낮은 KGE의 **원인**을 세 성분 — 상관 r(위상/형상), 편향비 β=μ_sim/μ_obs(총량), 변동비 α=σ_sim/σ_obs(진폭) — 으로 분리해 **막대(component bar)·삼각(scatter of β vs α, 색=r)·다지점 삼각레이더**로 표시. "어느 축이 문제인가"를 한눈에.
- **읽는 법**: 각 성분의 이상값=1(막대는 1 기준선). **β>1=과대추정, β<1=과소; α<1=변동 과소(첨두 눌림·FDC 평탄화 흔함), α>1=과대; r 낮음=timing/형상 문제**. β–α 산점(색=r)에서 점이 (1,1)에서 어느 방향으로 벗어나는지로 유형 분류. *나쁜 패턴*: "α<1 & r 양호"=첨두 과소(저류 과다 가설); "β≠1 단독"=순수 물수지 치우침.
- **언제 쓰나**: [시계열]·다지점 [격자]. KGE 단일값이 낮을 때 진단, 보정(calibration) 전후 성분 이동 추적.
- **짝지표 & 교차링크**: **r·β·α/γ**(정의 명시: KGE 2009 γ vs KGE′ 2012 α) → [`26` KGE 성분 분해 카드]; 총량은 ⑨ 물수지·PBIAS; 진폭은 ② FDC. 다지점 종합은 공통편 **Taylor/Target**([`16`], Taylor는 r·σ비만·bias 못 봄 → Target 병행).
- **만드는 법**: `spotpy.objectivefunctions.kge(..., return_all=True)`(kge·r·β·α 동시 반환) 또는 `HydroErr`/직접 `numpy`로 r=`pearsonr`, β=mean비, α=std비. 막대 `ax.bar`, β–α 산점 `ax.scatter(c=r)`, 다지점은 삼각/레이더. **어느 KGE 정의(2009 γ / 2012 α)인지 캡션 명시**.
- **함정·주의**: **KGE(2009, γ)와 KGE′(2012, α)는 값이 다름** → 정의 명시 필수. 성분은 서로 독립이 아님(β·γ 상호작용 → KGE′로 완화). **단일 성분만으로 원인 단정 금지**(귀속은 가설). 간헐/영유량 하천은 CV·α 불안정. 성분 방향(과대/과소)을 물리원인에 직결하지 말 것.
- **출처**: Gupta, Kling, Yilmaz & Martinez (2009, *Journal of Hydrology* 377(1–2):80–91, doi:10.1016/j.jhydrol.2009.08.003); Kling, Fuchs & Paulin (2012, *Journal of Hydrology* 424–425:264–277, KGE′, 권·페이지 확인요); Knoben, Freer & Woods (2019, *HESS* 23:4323–4331, doi:10.5194/hess-23-4323-2019); `spotpy`(Houska et al. 2015, *PLOS ONE* 10(12):e0145180, doi:10.1371/journal.pone.0145180).

---

### ★ 홍수빈도 플롯 (홍수빈도/재현주기 도표 / Flood frequency plot: return period vs peak discharge)
- **무엇을 보여주나**: 장기 모델·관측 유량의 **극치(연최대 또는 임계초과 첨두)** 를 재현주기(return period) 대 재현유량(return level)로 도시 — 경험분위점(plotting position)·적합곡선(GEV/GPD/LP3)·신뢰구간 띠. 50·100년 **설계홍수**와 모델의 극치 재현(흔히 과소)을 평가.
- **읽는 법**: x=재현주기(로그, 년), y=첨두유량(때로 로그). 점=경험(관측/모델 순위→plotting position), 선=분포적합, 음영=CI. **모델 적합곡선이 관측 점 아래면 극치 과소**; 관측 경험점이 모델 CI 띠 밖이면 불일치. 모델·관측 두 적합을 겹쳐 **재현주기별 유량 차와 CI 중첩** 여부로 유의성 판정. *나쁜 패턴*: 상위 재현주기에서 곡선 급격히 갈라짐(tail 적합 불량), CI 폭 과대(표본 부족).
- **언제 쓰나**: [시계열] 장기(가능하면 ≥30년) hindcast vs 장기 관측소. 설계·홍수위험 평가.
- **짝지표 & 교차링크**: **GEV/LP3/GPD 매개변수·N년 return value·부트스트랩 CI** → [`26` 홍수빈도 분석 카드]; 극치엔진(GEV/POT·declustering·return level)·tail QQ는 공통편 **Return-level & PDF/CDF**([`16`]), [`03` GEV/POT]. tail은 공통 QQ의 극단 확대판.
- **만드는 법**: **`pyextremes`**(`EVA`: `get_extremes('BM'/'POT')`, `fit_model('GEV'/'GPD')`, `plot_return_values`)·L-모멘트는 **`lmoments3`**, LP3는 `scipy.stats.pearson3`(log변환). **plotting position 공식(Weibull/Gringorten/Cunnane) 명시**. declustering(POT)·블록크기(BM)·MRL plot으로 임계 결정. CI는 부트스트랩/프로파일우도.
- **함정·주의**: **임계 선택·declustering·표본수에 극도로 민감** → **부트스트랩 CI 필수**. 짧은 기록의 100년값 외삽 과신 금지. **저수지·취수로 교란된 관측**은 자연빈도가 아니므로 자연 모델과 직접비교 부적절(자연화 여부 명시). 지역·기관별 권장분포 상이(미국 Bulletin 17C=LP3, 유럽·다수 GEV) → 분포·추정법 명시. 비정상성(추세)이면 정상 GEV 부적합.
- **출처**: Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Hosking & Wallis (1997, *Regional Frequency Analysis: An Approach Based on L-Moments*, Cambridge, L-모멘트); England et al. (2019, *USGS Techniques and Methods 4-B5*, Bulletin 17C, LP3); `pyextremes`(georgebv.github.io/pyextremes); `lmoments3`(pypi.org/project/lmoments3).

---

### ★ 수문서명 radar / spider (다서명 레이더 / Hydrological signature radar/spider chart)
- **무엇을 보여주나**: 여러 수문서명(예: KGE·lnNSE·PBIAS·BFI·FDC slope·Q5·Q95·감수상수 k·유출중심일 CT·runoff ratio)을 **정규화해 한 레이더(spider) 축들에** 얹어 모델·관측(또는 모델–관측 비 1.0 기준)을 다각형으로 비교. 단일지표 함정을 피하고 모델의 **물리적 거동을 다차원**으로 한눈에.
- **읽는 법**: 각 꼭짓점=서명 1개, 반경=값(관측 대비 비, 1.0=완전 일치 원). 모델 다각형이 **관측 다각형(또는 1.0 기준원)에 겹치면** 양호. 특정 축만 안쪽/바깥이면 그 서명(예: BFI 안쪽=기저 과소, FDC slope 바깥=변동 과대)만 문제. *좋은 패턴*: 두 다각형 형태·크기 일치. *나쁜 패턴*: 한두 축만 크게 이탈(서명 간 trade-off), 전체 축소(전반 과소).
- **언제 쓰나**: [시계열]·다유역 서명 벤치마킹. §G6 "단일지표 금지" 강제 그림. 보정 목적함수 선택·구조 진단.
- **짝지표 & 교차링크**: 서명 전부 → [`26` 다목적·다서명 진단 프레임·FDC 서명·BFI·감수·flow timing 카드]. 개별 서명은 ②·⑪·⑫·⑬로 정밀화. 종합 랭킹은 공통편 **Taylor/Target**([`16`])와 상보(Taylor=패턴, radar=물리서명).
- **만드는 법**: 서명 계산 **`hydrosignatures`(HyRiver)**·`hydrostats`·`spotpy`; 정규화(관측 대비 비 또는 min-max) 후 `matplotlib` `projection='polar'` 다각형(각 축 라벨). 다모델은 색 다른 다각형. **정규화 방식·기준(관측비 vs min-max)을 캡션 명시**(축 스케일이 형태 좌우).
- **함정·주의**: **정규화·축 순서·축 스케일이 다각형 인상을 지배** → 규약 고정·명시. 서명끼리 **상충**(첨두 vs 갈수) 가능 → trade-off로 해석(하나가 좋으면 다른 게 나쁠 수 있음). 서명은 **관측 rating error·결측에 민감**("good signatures go bad", McMillan 2023). 축이 너무 많으면 가독성 저하(핵심 6~10개).
- **출처**: Yilmaz, Gupta & Wagener (2008, *WRR* 44, W09417, doi:10.1029/2007WR006716); Euser et al. (2013, *HESS* 17:1893–1912, consistency·서명); McMillan et al. (2023, *Hydrological Processes* 37, doi:10.1002/hyp.14987, "When good signatures go bad"); `hydrosignatures`(HyRiver, docs.hyriver.io).

---

### ★ 유역별 KGE/NSE 공간 지도 (성능 공간분포 지도 / Per-catchment KGE/NSE spatial map)
- **무엇을 보여주나**: 다수 관측소(또는 유역 폴리곤/유역중심점)의 KGE·NSE·PBIAS를 **지도 위 색 마커/색칠 폴리곤**으로 — 성능의 **지리적 분포**(습윤/건조·산악/평지·인위영향 유역)를 진단. CAMELS류 대표본 검증의 표준 도판.
- **읽는 법**: 색=각 유역 지표(순차맵: KGE/NSE는 높을수록 좋음; PBIAS는 **발산맵 0=흰색**). *읽기*: 건조·소유역에서 낮은 KGE 군집(정상), 인위영향(댐·취수) 유역의 이상치, 지역적 계통 저성능(강제력/구조 문제). *나쁜 패턴*: 특정 지역 전면 저성능(입력·구조 편향), 무작위 산포(대표성 낮음).
- **언제 쓰나**: [시계열] 다지점 vs [격자] 모델. 광역·대표본(national/CAMELS) 성능 요약, 점 검증이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 유역별 **KGE·NSE·PBIAS·성분 r/β/α** → [`26` KGE·NSE·PBIAS 카드]; 값 분포는 ⑩ boxplot/CDF; 성분 진단은 ④. 격자–격자 공간비교는 공통편 **Bias/difference map**([`16`], [`02`]).
- **만드는 법**: **★ 지도형(위경도) → 해안선/육지 + 위경도 라벨 필수**([`../plotting_maps.md`](../../plotting_maps.md)의 `add_basemap(ax, lon, lat)` 사용). `matplotlib`/`cartopy` `ax.scatter(lon, lat, c=kge, transform=ccrs.PlateCarree())` 마커, 또는 `geopandas` 유역 폴리곤 `gdf.plot(column='kge', ax=ax)`. 순차맵(`viridis`)·PBIAS는 발산맵(`RdBu_r`+`TwoSlopeNorm(vcenter=0)`). 컬러바·유역 ID 병기.
- **함정·주의**: **위경도 축이면 지도** → 해안선·라벨 없으면 "어디인지" 못 읽음(add_basemap 강제, 오프라인 fallback 포함). **경도 규약(0–360 vs −180–180)** 불일치 주의. 소유역 점이 겹치면 지역 인셋·확대(`10m` 해안선). KGE 색스케일 하한이 −∞ → clip(예: −1 이하 동일색)·caption 명시. 지도색만으로 우열 단정 금지(임계 advisory).
- **출처**: Addor et al. (2017, *HESS* 21:5293–5313, CAMELS, doi:10.5194/hess-21-5293-2017); Knoben et al. (2019, *HESS* 23:4323–4331, doi:10.5194/hess-23-4323-2019, KGE 해석); Cartopy(scitools) / `geopandas`(geopandas.org); plotting_maps.md `add_basemap`.

---

### ★ 첨두유량 timing 산점 (첨두 크기·시각 오차 산점 / Peak magnitude & timing error scatter)
- **무엇을 보여주나**: 다수 홍수사건에서 사건별 **첨두유량 오차(Δpeak=%, y)** 와 **첨두 발생시각 오차(Δt=t_sim−t_obs 시간, x)** 를 산점 — 홍수예보의 실무 핵심(크기·타이밍 동시). 각 점 하나가 한 사건.
- **읽는 법**: x=timing 오차(0=완벽, 음=모델이 이름·양=모델이 늦음), y=peak 크기 오차(%, 0=완벽). **원점 근처 밀집=양호**. *읽기*: 점군이 우측 치우침=모델 첨두 지연(도달시간 과대), 하단 치우침=첨두 과소(평탄화). 색/크기로 사건규모 표시하면 대사건 편향 가독. 주변부 marginal 히스토그램으로 Δt·Δpeak 분포·중앙값. *나쁜 패턴*: 계통적 지연/과소(한쪽 사분면 쏠림).
- **언제 쓰나**: [사건] 유량 시자료 사건 추출(임계·baseflow separation). 홍수예보 검증, 도달시간·저류 진단.
- **짝지표 & 교차링크**: **Peak error(%)·Peak-timing error(시간)·사건 용적·CT** → [`26` 첨두유량 크기·시각·수문곡선 사건지표 카드]; 위상 일반론(교차상관 lag)은 [`06`]; 사건 형상 전체는 ⑥ radar·① 수문곡선 zoom.
- **만드는 법**: 사건 추출 후 `scipy.signal.find_peaks`로 첨두·시각 검출, Δpeak·Δt 계산 → `matplotlib` `ax.scatter` + marginal `seaborn.jointplot`/`ax.hist`. 다중첨두 사건 **매칭 규칙 정의**. 시자료 시간정합·UTC 통일.
- **함정·주의**: **사건정의·첨두검출 규칙에 민감**(임계·최소간격). **단일 큰 사건이 통계를 지배** → 다수 사건·분포(중앙값·MAE)로 보고. 관측 첨두 자체가 rating error(고유량 외삽)로 불확실 → Δpeak를 모델 오차로 단정 금지. 일자료는 timing 해상도 부족(시자료 권장). 다중첨두 mismatch 주의.
- **출처**: WMO, *Guide to Hydrological Practices* (WMO-No. 168, Vol. II); Ewen (2011, *Hydrology Research*, hydrograph 시각오차); protocol for hydrograph shape metrics(2025, PMC11723534, 첨두·arrival time 지표); `scipy.signal.find_peaks`(scipy.org).

---

### ★ 물수지 closure 막대 (물수지 닫힘 막대 / Water-balance closure bar: P − ET − Q − ΔS)
- **무엇을 보여주나**: 유역·격자의 물수지 성분(강수 P, 증발산 ET, 유출 Q, 저류변화 ΔS, 잔차 residual)을 **누적/그룹 막대**로 — P를 입력, ET+Q+ΔS+residual을 출력으로 놓아 **수지 잔차(닫힘 오차)** 를 시각화. 육상표면·수문모형의 1급 물리검증.
- **읽는 법**: 막대 성분 합 P = ET+Q+ΔS+residual. **residual 막대가 P의 수 %면 양호**(관행), 크면 항 누락·저류 드리프트. 모델·관측(가능한 항) 막대를 나란히 두면 어느 성분이 어긋나는지(예: ET 과대·Q 과소로 총량은 맞으나 배분 틀림). 연/계절별 막대로 계절 수지. *나쁜 패턴*: 장기 residual≠0(비보존/드리프트), 성분 배분 오류(ET↔Q 상쇄).
- **언제 쓰나**: [격자] 모형 산출(P·ET·Q·ΔS) 또는 유역집계 [시계열]; ΔS는 GRACE TWS(⑮)·토양수분 위성과 대조.
- **짝지표 & 교차링크**: **수지 잔차·유출률 runoff ratio·PBIAS** → [`26` 물수지 닫힘·유출용적/유출률 카드]; 질량·에너지 budget 일반틀은 [`04` 보존/flux]; ΔS 검증은 ⑮ GRACE. 총량 편향은 ③ 산점·④ β.
- **만드는 법**: 모든 항 **동일 유역·기간·단위(mm 또는 mm/일)** 로 집계(`xarray` 면적가중 유역평균) → `matplotlib` `ax.bar`(stacked) 또는 그룹막대. ΔS는 GRACE TWSA 차분·모델 저류 차분. residual = P−ET−Q−ΔS.
- **함정·주의**: **관측 P·ET·ΔS 자체가 큰 불확실성** → 잔차를 "모델 오차"로 단정 금지(§G1). 항 **단위·부호·유역경계·기간을 통일**(불일치가 가짜 잔차 최대 원인). **유역간 이동·취수** 명시. 장기평균 ΔS≈0 가정은 추세·저류 드리프트 있으면 위배. 모델 내부 online budget과 offline 진단 구분.
- **출처**: WMO, *Guide to Hydrological Practices* (WMO-No. 168); Rodell et al. (2004, *BAMS* 85(3):381–394, GLDAS·수지); Sheffield, Ferguson et al. (2009, *GRL* 36, 위성 물수지 닫힘, 권·DOI 확인요); Pan et al. (2012, *Journal of Climate* 25, 수지 닫힘 최적화).

---

### ★ 다지점 KGE/NSE boxplot·CDF (성능 분포 요약 / Multi-station KGE/NSE boxplot & CDF)
- **무엇을 보여주나**: 다수 관측소의 지표(KGE·NSE·lnNSE·PBIAS)를 **박스플롯(모델/실험별)** 또는 **경험적 CDF(누적분포)** 로 — 대표본에서 모델(들)의 **성능 분포·중앙값·꼬리(저성능 유역 비율)** 를 요약·비교. CAMELS류 벤치마킹 표준.
- **읽는 법**: **Boxplot**: 상자=IQR, 선=중앙값, 수염·이상점=저성능 유역. 모델 간 상자 위치·폭 비교. **CDF**: x=지표, y=누적비율; **곡선이 오른쪽(높은 KGE)일수록 우수**; benchmark 선(KGE=−0.41, NSE=0) 세로선으로 "benchmark 이기는 유역 비율" 판독. *좋은 패턴*: 중앙값 높고 저성능 꼬리 짧음. *나쁜 패턴*: 긴 하단 꼬리(다수 유역 실패), 모델 간 CDF 교차(유역 유형별 우열 반전).
- **언제 쓰나**: [시계열] 대표본 다지점·다모델·다목적함수 비교. 성능의 **분포**를 단일 대표값 대신 보여줄 때.
- **짝지표 & 교차링크**: **KGE·NSE·PBIAS 분포·benchmark skill** → [`26` 다목적·다서명 진단·benchmark 카드]; 공간분포는 ⑦ 지도; 유의성(모델 차이)은 [`01`] 부트스트랩. 종합 랭킹은 공통편 **Taylor**([`16`]).
- **만드는 법**: 지표는 `HydroErr`/`spotpy` 유역별 계산 → `matplotlib`/`seaborn` `boxplot`; CDF는 `numpy.sort`+`ax.plot(sorted, np.linspace(0,1,n))` 또는 `statsmodels` ECDF. **benchmark 세로선(KGE=−0.41, NSE=0) 표기**. KGE 하한 clip(−∞ 방지) 명시.
- **함정·주의**: 박스플롯은 **분포형(이중봉)** 을 가림 → CDF/violin 병행. 유역 표본이 **대표성 편향**(잘 관측된 습윤 유역 과대) → 유역 유형별 층화 권장. KGE=−∞ 유역이 boxplot 스케일 파괴 → clip·caption. 중앙값만으로 결론 금지(꼬리·benchmark 비율 병기).
- **출처**: Addor et al. (2017, *HESS* 21:5293–5313, doi:10.5194/hess-21-5293-2017, CAMELS); Newman et al. (2017, *HESS* 21:5293 관련 benchmark, 확인요); Knoben et al. (2019, *HESS* 23:4323–4331, doi:10.5194/hess-23-4323-2019); Kratzert et al. (2019, *HESS* 23:5089–5110, doi:10.5194/hess-23-5089-2019, LSTM CDF 벤치마크).

---

### ★ FDC 서명 편향 플롯 (FDC 서명 편향 / FDC signature bias: FHV·FLV·FMS·slope)
- **무엇을 보여주나**: FDC를 구간별로 나눠 **고유량 편향 %BiasFHV(상위 2%), 저유량 편향 %BiasFLV(하위 30%, 로그공간), 중간구간 기울기 편향 %BiasFMS(20~70%), Q5/Q95 편향**을 막대/다지점 산점으로 — 유량곡선 신호를 구간별로 정량 진단(Yilmaz 서명 집합).
- **읽는 법**: 각 서명 편향 %(0=완벽). **FHV 음(−)=첨두 과소, FLV 양(+)=저유량 과대, FMS≠0=FDC 기울기(변동성) 오차**. 다지점이면 서명별 박스/산점으로 분포. *좋은 패턴*: 세 서명 모두 0 근처. *나쁜 패턴*: FHV 크게 음(고유량 과소)+FMS 음(평탄화)=변동 눌림; FLV 크게 양=기저 과다.
- **언제 쓰나**: [시계열] FDC(②) 진단의 정량 짝. 다유역 서명 벤치마킹, 보정 목적함수 선택.
- **짝지표 & 교차링크**: **%BiasFHV·FLV·FMS·Q5·Q95** → [`26` FDC 서명 지표 카드]; 곡선 자체는 ② FDC; 종합은 ⑥ radar. KGE α(변동)와 상보(④).
- **만드는 법**: `hydrosignatures`(HyRiver) FDC 유틸 또는 직접 numpy로 구간 적분 편향 계산(Yilmaz 2008 정의: 2%/30%/20~70%). `matplotlib` `ax.bar`(서명별)·다지점 산점. **구간 정의·로그공간 규약 명시**(문헌마다 다름).
- **함정·주의**: **구간 정의(2%/30%/20~70%)는 Yilmaz 규약**이며 문헌마다 상이 → 명시. 저유량 로그공간 계산 시 **0유량 처리** 규약. 서명은 관측 rating error·결측에 민감. **여러 서명 조합**으로 해석(단일 서명 금지).
- **출처**: Yilmaz, Gupta & Wagener (2008, *WRR* 44, W09417, doi:10.1029/2007WR006716); McMillan, Westerberg & Krueger (2018, *WIREs Water*, 서명 리뷰); `hydrosignatures`(HyRiver, docs.hyriver.io).

---

### 기저유출 분리 시계열 (기저유출 분리 / Baseflow separation time series & BFI)
- **무엇을 보여주나**: 총유량 아래에 **디지털필터(Lyne–Hollick·Eckhardt)·최소값법(UKIH/HYSEP)** 으로 분리한 기저유량 b_t를 음영으로 채우고, **기저지수 BFI=Σb/ΣQ**(모델·관측)를 비교. 모델이 **저류-방류(지하수) 물리**를 재현하는지.
- **읽는 법**: 상단=총유량, 하단 음영=기저유량, 나머지=직접유출. **모델 BFI가 관측보다 낮으면 첨두 과다·기저 과소(저류 과소 가설)**. 감수구간에서 기저선이 총유량에 얼마나 붙는지로 배수 특성. *나쁜 패턴*: 모델 기저가 사건 후 너무 빨리 떨어짐(감수 빠름).
- **언제 쓰나**: [시계열] 일유량. 저류·지하수 기여 진단, 저유량 물리 평가.
- **짝지표 & 교차링크**: **BFI·기저용적** → [`26` 기저유출 분리/BFI·저수기 지수 카드]; 저류 거동은 ⑬ 감수; 저유량 분포는 ② FDC 저유량단.
- **만드는 법**: **`baseflow`**(PyPI, 다중필터)·`hydrosignatures`(HyRiver) baseflow 유틸, 또는 Eckhardt/Lyne–Hollick 직접 구현 → `matplotlib` `fill_between`. **필터 파라미터(α·BFI_max·passes) 모델·관측 동일 적용** 필수.
- **함정·주의**: 기저분리는 **개념적·비유일 해**(관측 "정답" 아님) → 절대값보다 **동일 필터 하 상대비교**. **필터 파라미터에 민감** → 동일 설정·명시. 융설·저수지 방류가 있으면 필터 가정 위배(자연화 필요).
- **출처**: Lyne & Hollick (1979, *Institute of Engineers Australia National Conference*:89–93, 페이지 확인요); Eckhardt (2005, *Hydrological Processes* 19(2):507–515, doi:10.1002/hyp.5675); Gustard, Bullock & Dixon (1992, *Low Flow Studies*, UKIH BFI); `baseflow`(pypi.org/project/baseflow), `hydrosignatures`(HyRiver).

---

### 감수곡선 진단 (감수분석 도표 / Recession analysis: −dQ/dt vs Q, log-log)
- **무엇을 보여주나**: 감수(강우 종료 후 유량 감소)구간에서 **−dQ/dt를 Q에 대해 log-log 산점**(Brutsaert–Nieber)하고 회귀선(−dQ/dt=a·Q^b)·Master Recession Curve를 얹어 **저류-방류 특성(감수상수 k, 지수 b)** 을 모델·관측 비교.
- **읽는 법**: x=Q(log), y=−dQ/dt(log). 회귀 **기울기 b≈1이면 선형저수지, b>1 비선형**; 절편으로 a·k. **모델 점운이 관측보다 위(같은 Q에서 더 빨리 감소)면 저류 과소(너무 빨리 마름)**. 하부 포락선(lower envelope)이 느린 배수(기저). *나쁜 패턴*: 모델·관측 기울기·위치 크게 다름(배수 물리 오차), 산포 과대(사건선택·노이즈).
- **언제 쓰나**: [시계열] 감수사건 추출(강우·융설 무영향 구간). 지하수 반응·배수 물리 검증.
- **짝지표 & 교차링크**: **감수상수 k·지수 b(a)** → [`26` 감수분석/MRC 카드]; 기저는 ⑫ BFI; 저유량 극치는 [`26` 저수기 지수]. 저류거동은 ⑥ radar 축.
- **만드는 법**: 감수사건 추출(강우 gap·최소지속) 후 dQ/dt 계산(bin/평활으로 노이즈 저감) → `matplotlib` log-log `scatter`+`numpy.polyfit`(log 공간 회귀). `hydrosignatures`(HyRiver) recession 유틸도. **사건선택·dQ/dt 방식 명시**.
- **함정·주의**: **dQ/dt 추정·사건선택·측정노이즈에 매우 민감**(결과 산포 큼) → 방법 고정·명시. **저유량 rating error**가 감수를 왜곡. 융설·저수지 영향 구간 배제. 단일 회귀보다 사건군·MRC로.
- **출처**: Brutsaert & Nieber (1977, *WRR* 13(3):637–643); Tallaksen (1995, *Journal of Hydrology* 165:349–370, 감수 리뷰); Stoelzle, Stahl & Weiler (2013, *HESS* 17:817–828, doi:10.5194/hess-17-817-2013, 방법 민감도).

---

### 홍수범람 공간검증 지도 (침수역 공간검증 / Flood extent verification map, CSI/Fit)
- **무엇을 보여주나**: 모델(수리모형 LISFLOOD-FP·HEC-RAS)의 **침수역(flood extent) 격자**를 관측(위성 SAR 침수도·현장)과 지도 위에서 겹쳐, hit(교집합)·miss·false-alarm 셀을 **색으로 구분**하고 **Fit/CSI=A(sim∩obs)/A(sim∪obs)** 를 표기. 침수역의 공간 일치를 진단.
- **읽는 법**: 지도 색: **hit(both)=녹색, miss(obs만)=파랑, false alarm(sim만)=빨강**. hit 영역이 넓고 miss/false가 좁으면 양호. *읽기*: 얕은 가장자리·도시역에서 false/miss 급증(경계 불확실). Fit/CSI 값 병기. *나쁜 패턴*: 침수역 전체 이동(위치 어긋남·double penalty), 특정 방향 편향.
- **언제 쓰나**: [격자] 침수 이진/수심 (모델 vs 위성 SAR·광학 침수도). 홍수 정점 시점 정합.
- **짝지표 & 교차링크**: **Fit/CSI·POD·FAR**(침수/비침수 셀) → [`26` 홍수범람 공간검증·범주형 초과검증 카드]; 범주형 일반론·성능 다이어그램은 공통편([`16`], [`03`]); 공간패턴은 [`02`].
- **만드는 법**: **★ 지도형(위경도) → 해안선/육지 + 위경도 라벨 필수**([`../plotting_maps.md`](../../plotting_maps.md)의 `add_basemap` 사용; 하천·유역 경계 오버레이 권장). 이진화 후 hit/miss/false 마스크 → `matplotlib`/`cartopy` `pcolormesh`(범주 색맵). CSI는 셀 교/합집합 카운트. 동일 격자·좌표·시각·영구수체 마스크 통일.
- **함정·주의**: **위경도 축 → 지도**(해안선/하천·라벨 필수, add_basemap). **SAR 침수도 자체 오차**(식생·도시 후방산란). **시점 불일치·해상도 차**로 double-penalty(위치 약간 어긋나면 miss+false 동시). 이진화 임계가 결과 좌우. 영구수체·도시 마스크 통일.
- **출처**: Bates & De Roo (2000, *Journal of Hydrology* 236:54–77, LISFLOOD-FP·Fit); Horritt & Bates (2002, *Journal of Hydrology* 268:87–99, 범람모형 검증); Stephens et al. (2014, *Hydrological Processes* 28, Fit 지표 한계); Cartopy(scitools).

---

### GRACE TWS anomaly 시계열·지도 (육상수저장 이상 / GRACE Terrestrial Water Storage anomaly, series & map)
- **무엇을 보여주나**: 모델 총저류변화(ΔS: 토양수분+지하수+눈+지표수)를 위성중력 GRACE/GRACE-FO의 육상수저장 이상(TWSA)과 비교 — (a) **유역평균 TWSA 시계열 overlay**(계절진폭·위상·추세), (b) **TWSA 추세/진폭 공간 지도**. 물수지 저류항의 유일한 광역 관측 제약(⑨와 짝).
- **읽는 법**: (a) x=시간, y=TWSA(cm 등가수두), 모델·GRACE 두 선 — **계절진폭·위상 일치** 우선, 장기 추세 비교. (b) 지도 색=TWSA 추세(발산맵) 또는 계절진폭. *좋은 패턴*: 계절 사이클 위상·진폭 겹침. *나쁜 패턴*: 모델 진폭 과소(저류 표현 부족), 위상 지연, 추세 부호 반대(지하수 고갈 미표현).
- **언제 쓰나**: [위성 격자] GRACE vs 모델 저류 [격자]; **대유역**([시계열]) 월단위. 물수지 닫힘(⑨) ΔS 항 검증.
- **짝지표 & 교차링크**: **TWSA 상관·RMSE·계절진폭·추세** → [`26` GRACE TWS 검증 카드]; 물수지 결합은 ⑨ closure; 시계열 overlay 일반론은 [`06`]/공통편([`16`]). 추세 지도는 [`02`].
- **만드는 법**: 시계열은 `matplotlib` overlay. **★ 지도형은 위경도 라벨 필수**([`../plotting_maps.md`](../../plotting_maps.md) `add_basemap`; GRACE는 조대해상도라 `pcolormesh`+육지마스크). GRACE **스케일링·leakage 보정** 적용, 유역평균 후 비교. 모델 저류항 정의(지하수 포함 여부) 일치.
- **함정·주의**: GRACE는 **대유역(신뢰 하한 ~10⁵ km² 안팎, 처리방식 의존, 확인요)·월단위에서만 신뢰**. 해상도 조대(수백 km)·신호 leakage. **TWS는 성분 미분리**(모델 성분과 1:1 아님). 두 미션(GRACE·FO) **공백(2017–2018)**. 추세는 mascon vs 구면조화·GIA 보정에 민감. GRACE도 reference(관측오차 有).
- **출처**: Tapley et al. (2004, *Science* 305:503–505, GRACE); Landerer & Swenson (2012, *WRR* 48, W04531, 스케일링, DOI 확인요); Scanlon et al. (2018, *PNAS* 115(6):E1080–E1089, doi:10.1073/pnas.1704665115, GRACE vs 모델); Rodell et al. (2018, *Nature* 557:651–659, doi:10.1038/s41586-018-0123-1, TWS 추세).

---

### ★ 관측소 위치도 (관측소 위치 지도 / Gauging station location map, basemap)
- **무엇을 보여주나**: 검증에 쓴 유량·수위 관측소(및 유역 경계·하천망)를 **해안선/육지 지도 위 마커+ID**로 — 읽는 사람이 "어느 유역·어디 관측소인지" 알게 하는 필수 맥락 그림. 다지점 검증(⑦·⑩)의 동반 지도.
- **읽는 법**: 마커=관측소 위치, 라벨=관측소 ID/유역명, 색/크기로 관측기간·성능·유역면적 표시 가능. 하천망·유역경계 오버레이로 상하류 관계. *좋은 패턴*: 유역 대표성 있게 분포. *읽기 포인트*: 상하류 관측소 위계, 인위영향(댐 상하류) 위치.
- **언제 쓰나**: 모든 [시계열] 다지점 검증의 맥락 그림. 산점/시계열/KGE 지도(⑦)의 위치 근거.
- **짝지표 & 교차링크**: 위치 자체(지표 아님) — ⑦ KGE 지도·⑩ boxplot의 위치 근거. 각 산점/시계열 패널에 **인셋 로케이터맵** 동반 권장([`../plotting_maps.md`](../../plotting_maps.md) §C).
- **만드는 법**: **★ 지도형(위경도) → 해안선/육지 + 위경도 라벨 필수**([`../plotting_maps.md`](../../plotting_maps.md)의 `add_basemap(ax, lon, lat)`; 정점 군집이면 `margin_deg≈0.5~1.0`·`10m` 해안선). `ax.scatter(lon, lat, marker='^')` + `ax.annotate(station_id)`(약간 offset). 하천망·유역은 `geopandas`(NHD/HydroSHEDS shapefile) `gdf.plot(ax=ax)`. 제목에 위경도(예 `Station 12345 (127.3°E, 37.5°N)`).
- **함정·주의**: **위경도 축 → 지도**(해안선·라벨 없으면 위치 못 읽음, add_basemap 강제). **경도 규약(0–360 vs −180–180)** 통일(`lon=((lon+180)%360)-180`). 연안·산악 확대엔 거친 해안선(`110m`) 금지 → `10m`. 마커 겹침 시 지역 인셋. 관측소 ID·좌표 마스킹(민감정보면 익명 ID).
- **출처**: [`../plotting_maps.md`](../../plotting_maps.md) `add_basemap`; Cartopy(scitools.org.uk/cartopy); `geopandas`(geopandas.org); HydroSHEDS(Lehner, Verdin & Jarvis 2008, *EOS* 89(10):93–94, 유역·하천망).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 26(및 타 파일) 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 26(및 타 파일) 교차링크 |
|---|---|---|---|---|---|
| 1 | 수문곡선 overlay + 잔차 (사건 zoom) | 시계열·사건 | 편향+위상+사건 | 사건 KGE/NSE·첨두·timing | 26 사건지표·첨두 · 06 lag · 01 |
| 2 | 유황곡선 FDC (log-y) | 시계열·격자 | 분포·변동 구조 | Q5·Q95·FDC slope·FHV/FLV | 26 FDC·서명 · (공통 QQ/CDF) |
| 3 | 유량 검증 산점도 (log·KGE/NSE box) | 시계열·격자 | 정확도+편향 | KGE·NSE·PBIAS·RSR·r | 26 NSE/KGE/PBIAS · (공통 산점도) |
| 4 | KGE 성분 플롯 (r·β·α) | 시계열·격자 | 원인 진단 | r·β·α/γ | 26 KGE 성분 · (공통 Taylor/Target) |
| 5 | 홍수빈도 플롯 (재현주기) | 시계열 | 극값(설계홍수) | GEV/LP3/GPD·N년값·CI | 26 홍수빈도 · 03 GEV/POT · (공통 return-level) |
| 6 | 수문서명 radar/spider | 시계열 | 다서명 종합(물리) | 서명 전부(FDC·BFI·감수·CT) | 26 다서명 진단·서명 카드 |
| 7 | 유역별 KGE/NSE 지도 (basemap) | 시계열↔격자 | 성능 공간분포 | KGE·NSE·PBIAS | 26 KGE/NSE · 02 · plotting_maps |
| 8 | 첨두유량 timing 산점 (Δt·Δpeak) | 사건 | 사건 첨두 크기·시각 | Peak error·timing error | 26 첨두·사건지표 · 06 lag |
| 9 | 물수지 closure 막대 (P−ET−Q−ΔS) | 격자·시계열 | 물수지 잔차 | 수지 잔차·runoff ratio·PBIAS | 26 물수지 닫힘·유출률 · 04 |
| 10 | 다지점 KGE/NSE boxplot·CDF | 시계열 | 성능 분포 요약 | KGE·NSE 분포·benchmark skill | 26 다서명·benchmark · 01 |
| 11 | FDC 서명 편향 (FHV·FLV·FMS) | 시계열 | 구간별 편향 | %BiasFHV/FLV/FMS·Q5/Q95 | 26 FDC 서명 |
| 12 | 기저유출 분리 시계열 (BFI) | 시계열 | 저류-방류 물리 | BFI·기저용적 | 26 baseflow/BFI |
| 13 | 감수곡선 (−dQ/dt vs Q, log-log) | 시계열 | 감수·저류거동 | 감수상수 k·지수 b | 26 감수분석/MRC |
| 14 | 홍수범람 공간검증 지도 (CSI) | 격자 | 침수역 공간일치 | Fit/CSI·POD·FAR | 26 홍수범람·범주형 · 02·03 · plotting_maps |
| 15 | GRACE TWS anomaly 시계열·지도 | 위성·격자 | 저류변화 | TWSA 상관·진폭·추세 | 26 GRACE TWS · 09⑨ · 06 |
| 16 | 관측소 위치도 (basemap) | 시계열 | 위치·맥락 | (위치) | 26 (다지점 전반) · plotting_maps §C |

> **묶음 권고**: 단일 그림 금지 원칙(§G4)에 따라 수문 검증 보고는 최소 **①(수문곡선/위상·사건) + ②(FDC/분포) + ④(KGE 성분/원인)** 3장을 기본 세트로, 극치·설계면 **⑤**, 다서명 종합이면 **⑥**, 대표본·광역이면 **⑦/⑩**, 물수지·저류면 **⑨/⑮**, 사건 첨두면 **⑧**, 저유량·물리면 **⑪/⑫/⑬**, 침수면 **⑭**를 추가한다. 다지점이면 **⑯ 위치도**를 항상 동반. 모든 임계(NSE>0.5·KGE>0.75·Fit 0.5~0.8 등)는 **advisory + 영역·시간해상도·기후 의존 경고**로 캡션에 달고, benchmark(NSE=0·KGE=−0.41) 대비 상대평가한다.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- WMO, *Guide to Hydrological Practices* (WMO-No. 168, Vol. I·II) — 유량·물수지·홍수예보·자료일관성.
- WMO, *Manual on Low-flow Estimation and Prediction* (WMO-No. 1029, 2008) — 저유량·FDC.
- Coles (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD·return level).
- Hosking & Wallis (1997) *Regional Frequency Analysis: An Approach Based on L-Moments*, Cambridge (L-모멘트).
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·회귀·QQ 표준 시각화).

**학술 논문 (제목·저널·연도 웹 확인; DOI는 확인분만)**
- Nash & Sutcliffe (1970) "River flow forecasting through conceptual models part I," *Journal of Hydrology* 10(3):282–290. (NSE)
- Gupta, Kling, Yilmaz & Martinez (2009) "Decomposition of the mean squared error and NSE performance criteria," *Journal of Hydrology* 377(1–2):80–91. (doi:10.1016/j.jhydrol.2009.08.003, KGE)
- Kling, Fuchs & Paulin (2012) "Runoff conditions in the upper Danube basin...," *Journal of Hydrology* 424–425:264–277. (KGE′, 권·페이지 확인요)
- Knoben, Freer & Woods (2019) "Technical note: Inherent benchmark or not? Comparing NSE and KGE," *HESS* 23:4323–4331. (doi:10.5194/hess-23-4323-2019)
- Moriasi et al. (2007) "Model evaluation guidelines...," *Transactions of the ASABE* 50(3):885–900. (등급 advisory)
- Yilmaz, Gupta & Wagener (2008) "A process-based diagnostic approach to model evaluation: FDC signatures," *WRR* 44:W09417. (doi:10.1029/2007WR006716, FHV/FLV/FMS)
- Vogel & Fennessey (1994) "Flow-duration curves. I," *Journal of Water Resources Planning and Management* 120(4):485–504.
- Eckhardt (2005) "How to construct recursive digital filters for baseflow separation," *Hydrological Processes* 19(2):507–515. (doi:10.1002/hyp.5675)
- Brutsaert & Nieber (1977) "Regionalized drought flow hydrographs...," *WRR* 13(3):637–643. (감수분석)
- Stoelzle, Stahl & Weiler (2013) "Are streamflow recession characteristics really characteristic?" *HESS* 17:817–828. (doi:10.5194/hess-17-817-2013)
- Addor, Newman, Mizukami & Clark (2017) "The CAMELS data set...," *HESS* 21:5293–5313. (doi:10.5194/hess-21-5293-2017)
- Kratzert et al. (2019) "Towards learning universal, regional, and local hydrological behaviors via machine learning...," *HESS* 23:5089–5110. (doi:10.5194/hess-23-5089-2019, CDF 벤치마크)
- Euser et al. (2013) "A framework to assess the realism of model structures using hydrological signatures," *HESS* 17:1893–1912.
- McMillan et al. (2023) "When good signatures go bad...," *Hydrological Processes* 37. (doi:10.1002/hyp.14987)
- Bates & De Roo (2000) "A simple raster-based model for flood inundation simulation," *Journal of Hydrology* 236:54–77. (Fit/침수역)
- Tapley et al. (2004) "GRACE measurements of mass variability in the Earth system," *Science* 305:503–505.
- Scanlon et al. (2018) "Global models underestimate large decadal ... water storage trends relative to GRACE," *PNAS* 115(6):E1080–E1089. (doi:10.1073/pnas.1704665115)
- Rodell et al. (2018) "Emerging trends in global freshwater availability," *Nature* 557:651–659. (doi:10.1038/s41586-018-0123-1)
- England et al. (2019) *Guidelines for Determining Flood Flow Frequency—Bulletin 17C*, USGS Techniques and Methods 4-B5. (LP3)

**소프트웨어 (실존 도구)**
- `HydroErr` — 수문 goodness-of-fit 지표(kge_2012·nse·pbias 등): github.com/BYU-Hydroinformatics/HydroErr.
- `hydrostats` — 시계열 오차 특성·시각화(hydrograph·scatter·qq); Roberts, Williams et al. (2018) "Hydrostats: A Python Package...," *Hydrology* 5(4):66. (doi:10.3390/hydrology5040066)
- `hydrosignatures` (HyRiver 스택) — FDC·slope·baseflow·recession 서명: docs.hyriver.io.
- `spotpy` — 목적함수(kge return_all·nashsutcliffe)·보정; Houska et al. (2015) *PLOS ONE* 10(12):e0145180. (doi:10.1371/journal.pone.0145180)
- `pyextremes` — POT/BM·GEV/GPD·return level plot: georgebv.github.io/pyextremes.
- `lmoments3` — L-모멘트 분포적합(홍수빈도·LP3): pypi.org/project/lmoments3.
- `baseflow` — 다중 기저분리 필터: pypi.org/project/baseflow.
- `matplotlib`, `numpy`, `scipy`(signal.find_peaks·stats.pearson3·genextreme/genpareto), `pandas`, `xarray`, `geopandas`, `cartopy`(→ plotting_maps.md `add_basemap`), `seaborn`.

**웹 자료 (조사 시 직접 참조)**
- GRDC (Global Runoff Data Centre): https://www.bafg.de/GRDC
- GloFAS (Global Flood Awareness System): https://www.globalfloods.eu
- USGS Bulletin 17C: https://www.usgs.gov/publications/guidelines-determining-flood-flow-frequency-bulletin-17c
- HyRiver hydrosignatures 예제: https://docs.hyriver.io/examples/notebooks/signatures.html

**확인요 (확정 인용 금지 — §G-5)**
- Kling et al. (2012) 권·페이지(*Journal of Hydrology* 424–425:264–277) — 인용 전 원문 재확인(확인요).
- Lyne & Hollick (1979) 회의록 페이지(89–93) — 이차인용 다수, 원 문헌 재확인(확인요).
- Landerer & Swenson (2012) 권·아티클번호(*WRR* 48, W04531)·DOI — 재확인(확인요).
- Sheffield, Ferguson et al. (2009) 위성 물수지 닫힘 *GRL* 권·DOI — 재확인(확인요).
- GRACE 신뢰 최소유역 규모(~10⁵ km² 안팎)는 처리방식·지역 의존 — 특정 수치 인용 시 재확인(확인요).
- Moriasi(2007) 성능등급·KGE/NSE 관행값·Fit/CSI 0.5~0.8은 **월단위·특정 유역군 advisory**이며 일/시·소유역·건조유역엔 그대로 적용 불가(§G4).
- Newman et al. benchmark(CAMELS 관련) 정확한 서지 — 재확인(확인요).
