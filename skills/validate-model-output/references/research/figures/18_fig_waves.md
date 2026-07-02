# 검증 시각화 카탈로그 — [파랑 도메인편] (Verification Figures: Ocean Waves)

이 문서는 수치 파랑모델(WAVEWATCH III, SWAN, WAM 등) 결과를 **부이(buoy)·위성 고도계(altimeter)·재분석(ERA5 파랑, CMEMS WAVERYS)** 과 비교·검증할 때 쓰는 **그림(figure) 레퍼런스 카탈로그**의 파랑 도메인편이다. 메서드(수치지표) 카드는 [`08_domain_waves.md`](../08_domain_waves.md)에 있고, 여기서는 **"그 지표를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 그림 카드 형식으로 정리한다.

> **공통/횡단 그림과의 분담**: Taylor·Target·일반 ROC·rank histogram·신뢰도(reliability) 도표 등 **도메인 무관 요약그림은 [공통편] 담당**이라 여기서 중복 정의하지 않는다. 이 파일은 **파랑 고유 그림**(wave rose, E(f,θ) 극좌표, partition split, altimeter along-track colocation 등)과 **공통 그림의 파랑식 변형**(SI/HH를 box로 얹은 Hs 산점도, 극치 꼬리를 강조한 QQ 등)에 집중한다. 짝이 되는 공통 그림은 각 카드의 "교차링크"에서 가리킨다.

> **자료형 약어**: [격자]=NetCDF 격자(모델/재분석) · [시계열]=부이·관측소 CSV/텍스트 · [트랙]=위성 고도계 along-track · [스펙트럼]=1D E(f) / 2D E(f,θ).

> ⚠️ **그림을 그리기 전 반드시 적용할 해석 원칙**(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)):
> 1. **기준자료 ≠ 참값.** 부이·고도계·ERA5는 모두 reference이지 truth가 아니다. 축 라벨·캡션에 "obs/reference 대비"로 쓰고 "오차"가 아니라 "모델−기준 차"로 표현한다.
> 2. **부이는 점(point) 관측.** 격자/footprint 평균과 비교할 때 **대표성 오차(representativeness error)** 가 산점·잔차에 섞인다. SI가 모두 모델 탓이 아니다.
> 3. **해석 임계는 advisory.** `SI<0.15`, `R≥0.9`, `평균파향 RMSE 20~30°` 등은 **외해 관행값**이며 해역·해상도·기준자료 의존. 그림에 "good/bad"를 단정 표기하지 말고 영역의존 경고를 캡션에 둔다.
> 4. **단일 그림 금지.** 산점도(정확도) 하나로 결론내지 말고 최소 **정확도+편향+분포/패턴** 3축(예: 산점도 + 잔차 시계열 + QQ)과 유의성(부트스트랩 신뢰구간)을 함께 낸다.
> 5. **논문 그림 복제 금지** — 아래는 *그림 유형·사양*만 기술한다. 특정 논문의 도판을 그대로 재현하지 않는다.

---

## 이 파일에 담은 그림 (한 줄 목차)
1. ★ **Hs 검증 산점도 + 회귀 + SI/HH box** — 파랑 검증의 1차 대표 그림
2. ★ **Hs 밀도 산점도 (density / hexbin scatter)** — 대용량(고도계·장기 hindcast) 매치업
3. ★ **Hs QQ-plot (파랑식, 고파고 꼬리 강조)** — 분포·극치 일치
4. ★ **model–buoy 시계열 overlay + 잔차 패널** — 사건·위상·계통편차 진단
5. ★ **주기 비교 플롯 (Tp / Tm01 / Tm02 멀티패널)** — 주기 척도 일치
6. ★ **파랑장미 (wave rose)** — Hs×파향 분포 비교
7. **파향–주기 / 파향–파고 극좌표 밀도** — 방향별 sea-state 구조
8. **방향 분산 σθ(f) 검증 플롯** — 주파수별 펼침(spread)
9. ★ **파향 원형통계 시각화** — 각도오차 rose·단위벡터 잔차
10. **1D 주파수 스펙트럼 E(f) overlay (log)** — 봉우리·tail 형상
11. **2D 방향 스펙트럼 E(f,θ) 극좌표 비교** — 다중 swell 방향
12. **windsea / swell partition 비교** — 시스템별 분리 검증
13. ★ **극치 진단: return-level (POT-GPD/GEV) + 극값 QQ** — 설계파고·재현주기
14. ★ **altimeter along-track colocation 산점도 (+ 트랙 지도)** — 위성 광역 검증
15. ★ **Triple collocation 시각화** — 기준 없는 오차분산·SNR
16. ★ **Hs bias / difference 공간 지도** — 면적 계통오차 위치

---

### ★ Hs 검증 산점도 + 회귀 + SI/HH box (유의파고 검증 산점도 / Significant wave height validation scatter)
- **무엇을 보여주나**: 매치업된 (관측 Hs, 모델 Hs) 쌍을 산점하고 1:1선·회귀선·핵심 스칼라(bias·RMSE·**SI**·R·N·HH slope)를 함께 얹은, 파랑 검증의 **표준 1장**. ECMWF/WMO LC-WFV 운영 검증의 기본 도판 양식.
- **읽는 법**: x=관측(부이/고도계/ERA5), y=모델. **1:1선**(점선)이 기준, **OLS 회귀선**(실선)과 **HH 대칭기울기선**을 함께. 점이 1:1 위/아래로 쏠리면 과대/과소(bias). 큰 값에서 회귀선이 1:1 아래로 휘면 **고파고 saturation 과소**(파랑모델 전형 약점). 텍스트 box에 SI·bias·RMSE·R·slope·N 표기. *좋은 패턴*: 점운이 1:1에 좁게 밀착, slope≈1, SI 작음. *나쁜 패턴*: 부채꼴로 퍼짐(랜덤오차 큼), 휘어짐(조건부 편향).
- **언제 쓰나**: [시계열]/[트랙]/[격자] 어디서나, 표본 수백~수천 규모. 모델·기준 1쌍 또는 다지점 집계. 정확도+편향 동시 1차 점검.
- **짝지표 & 교차링크**: **SI(파랑 1차표준)·bias·RMSE·R·OLS slope·HH symmetric slope** → [`08` Hs검증/SI/HH/회귀 카드]. 다지점·다모델 요약은 공통편 **Taylor·Target**으로 승급(중복 회피). 분포 일치는 ③ QQ와 짝.
- **만드는 법**: `matplotlib` `ax.scatter`(또는 N 크면 ②로) + `numpy.polyfit`(OLS) + HH slope는 `08` 정의식 직접 계산. SI는 **정의 명시**(σ(model−obs)/mean(obs), bias 제거형 권장). 축 동일 범위·`set_aspect('equal')`·1:1선 `ax.axline`.
- **함정·주의**: SI는 **저파고대에서 분모 효과로 과대** → sea-state bin별 SI 병기 권장. OLS는 관측 무오차 가정 → 두 자료 모두 오차인 파랑에선 **HH/직교회귀 병행**(regression dilution). box의 SI 정의(bias 포함/제거)를 캡션에 반드시. 점 부이 대표성오차가 SI에 포함됨(모델 탓 단정 금지).
- **출처**: ECMWF/WMO LC-WFV "Significant wave height / Verification results"(confluence.ecmwf.int/display/WLW); Bidlot et al. (2002, *Weather and Forecasting*); Mentaschi et al. (2013, *Ocean Modelling* 72:53–58, RMSE/SI/HH 비교); Janssen, Hansen & Bidlot (1997, *Weather and Forecasting* 12(4)).

---

### ★ Hs 밀도 산점도 (밀도/육각 산점도 / Density (hexbin) scatter)
- **무엇을 보여주나**: 매치업이 수만~수백만 쌍(고도계 along-track, 장기 hindcast)일 때 점이 겹쳐 분포가 안 보이는 문제를 **2D 밀도(색)** 로 해결한 산점도. 점운의 **코어(최빈)·꼬리**를 분리해 본다.
- **읽는 법**: 색=쌍 밀도(로그 스케일 권장). 1:1선·회귀선 위 색띠가 1:1을 따라 좁고 길면 양호. 색 코어가 1:1 위/아래로 치우치면 bias. 고밀도 코어는 1:1인데 **저밀도 꼬리(고파고)가 1:1 아래**면 평균은 맞지만 극치 과소.
- **언제 쓰나**: [트랙](고도계 super-obs) 대량 매치업, 장기 [격자]vs[격자] 점쌍. N이 커서 개별 점이 무의미할 때.
- **짝지표 & 교차링크**: ①과 동일 스칼라(SI·bias·RMSE·R) + **분위수 회귀선**(여러 percentile). 분포 꼬리는 ③ QQ로 정량화. 고도계는 ⑭와 짝.
- **만드는 법**: `matplotlib` `ax.hexbin(x,y, bins='log', mincnt=1)` 또는 `np.histogram2d`+`pcolormesh`; `scipy.stats.gaussian_kde`(소~중 규모). 색맵은 perceptually-uniform(`cmocean.cm.dense`, viridis). 1:1·회귀 overlay.
- **함정·주의**: 선형 색스케일은 코어가 모든 색을 먹어 꼬리를 가림 → **로그 카운트**. bin 크기/`gridsize`가 인상 좌우(여러 개 시도). 밀도가 "정확도"는 아님 — 스칼라 지표·QQ 병행. 자기상관 강한 시계열은 유효표본수 과대(밀도 과신 금지).
- **출처**: 밀도산점 자체는 표준 통계 시각화(Wilks, *Statistical Methods in the Atmospheric Sciences*); 고도계 대량 매치업 적용례 — Sentinel-3A/3B·Jason-3 SWH 검증(*Remote Sensing* 12(13):2079, mdpi.com/2072-4292/12/13/2079; DOI 확인요); cmocean 색맵: Thyng et al. (2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66).

---

### ★ Hs QQ-plot (파랑식 분위수-분위수 도표 / Quantile–Quantile plot, tail-emphasised)
- **무엇을 보여주나**: 모델·관측 Hs **분포의 분위수**를 1:1 대응시켜 분포 형상, 특히 **고파고 꼬리** 일치를 본다. 평균 지표가 못 잡는 분포 편향·극치 과소를 포착. (공통편의 일반 QQ를 **상위 분위수 확대·등간 percentile**로 파랑식 변형.)
- **읽는 법**: x=관측 분위수, y=모델 분위수(p=1·5·…·95·99·99.9%). **상위 분위수에서 1:1선 아래로 휘면 모델 극치 과소**(가장 흔한 약점), 위로 휘면 과대. 중앙부는 맞고 꼬리만 벌어지면 평균 OK·극치 NG. 마커 크기로 percentile 표시하면 꼬리 가독.
- **언제 쓰나**: 분포·기후 검증, 시간정렬 불필요(동일 기간 동일 모집단 가정). [시계열]/[트랙]/[격자]. quantile mapping 보정 전후 점검.
- **짝지표 & 교차링크**: **KS 통계량·percentile bias** → [`08` PDF/CDF·QQ 카드]. 동시성(상관)은 못 봄 → ①/④와 3축 구성. 극단 꼬리는 ⑬(극값 QQ·return level)로 승급. 분포 적합(Weibull/Rayleigh)과 병행.
- **만드는 법**: `numpy.quantile`(공통 확률격자) 또는 `scipy.stats.probplot`(이론분포 대비). 산점 후 1:1선·등간 percentile 마커. 표본 적은 99.9% 분위수는 부트스트랩 신뢰구간 띠.
- **함정·주의**: **분포만 비교 → 동시 일치는 못 봄**(상관 0이어도 QQ는 완벽 가능). 극단 분위수는 표본 적어 불안정 → CI 표기. 모델·관측 **Hs 정의(Hm0 vs H1/3)·cutoff** 통일 안 하면 꼬리가 인위적으로 갈림.
- **출처**: Wilks (교과서); Jolliffe & Stephenson, *Forecast Verification*; 파랑 분포·극치 검증 관행(Caires & Sterl 2005, *J. Climate* 18, 극치 분위수).

---

### ★ model–buoy 시계열 overlay + 잔차 패널 (시계열 중첩·잔차 / Time-series overlay with residual panel)
- **무엇을 보여주나**: 한 지점에서 모델·부이(또는 ERA5) Hs(및 Tp·Dir)를 **시간축에 겹쳐** 그리고, 아래 패널에 **잔차(model−obs)** 를 둔다. 폭풍 사건의 **첨두 타이밍·진폭·위상지연·계통 offset**을 직접 본다.
- **읽는 법**: 위 패널 두 선의 **첨두 시각 어긋남=위상오차**, 첨두 높이 차=진폭오차, 항상 한쪽이 위면=bias. 아래 잔차가 0 주위 무작위면 양호; **사건마다 같은 부호로 튀면 폭풍 응답 계통오차**; 잔차에 추세/계단이 있으면 비정상·센서 drift. Hs 임계선(주의보)을 얹으면 경보 관점 가독.
- **언제 쓰나**: [시계열] 단일/소수 지점 정밀 진단, 폭풍 사례 분석, 예보선행시간별 열화 점검. 산점도(집계)가 못 보는 *언제·왜*를 본다.
- **짝지표 & 교차링크**: 사건 잔차 통계(event bias/RMSE), **교차상관 lag**(위상오차 정량) → [`06` 시계열/lag·STL], [`01` bias/RMSE]. 임계초과 경보는 [`08` POD/FAR/CSI]. 다지점 요약은 공통편 Taylor.
- **만드는 법**: `pandas`/`xarray` 시간정렬 후 `matplotlib` 2-패널(`sharex`), `fill_between`로 ±잔차 음영. Dir은 0/360 wrap 때문에 별도 패널(원형). 결측 구간 끊어 그림(보간선으로 잇지 말 것).
- **함정·주의**: 모델·부이 **시간기준(UTC/순간 vs 윈도우 평균) 불일치**가 가짜 위상오차 생성. 부이 결측을 직선보간하면 사건 통계 왜곡. 한 지점 결론을 해역 전체로 일반화 금지(대표성). Dir에 일반 잔차식 쓰면 360°→0° 점프로 오류.
- **출처**: WMO LC-WFV 매치업 관행; Bidlot et al. (2002); Comparison of ECMWF Hs forecasts with buoy data(*Weather and Forecasting* 34(6), 2019, journals.ametsoc.org/view/journals/wefo/34/6/waf-d-19-0043_1.xml).

---

### ★ 주기 비교 플롯 (주기 검증 멀티패널 / Wave-period comparison: Tp / Tm01 / Tm02)
- **무엇을 보여주나**: 첨두주기 Tp, 에너지 평균주기 Tm01, 영점교차주기 Tm02(≈Tz)를 **나란한 산점/잔차 패널**로 비교. 주기 척도별로 **Tp의 불연속(첨두 점프) vs 평균주기의 안정성**을 한눈에.
- **읽는 법**: 세 패널 각각 산점+1:1+SI box. **Tp 산점이 가로·세로 줄무늬(이산 점프)** 로 흩어지면 multimodal sea에서 첨두가 windsea↔swell로 튄 것 → RMSE 크게 나옴. Tm01/Tm02는 같은 자료라도 더 좁게 정렬되면 평균주기가 더 신뢰. Tm02가 유독 퍼지면 **고주파 cutoff 불일치** 의심.
- **언제 쓰나**: [시계열]/[스펙트럼] 부이 스펙트럼 유도 주기 vs 모델. (고도계는 주기 미제공 → 부이/모델 한정.)
- **짝지표 & 교차링크**: 각 주기의 **bias·RMSE·SI·R** → [`08` 주기검증/스펙트럼 모멘트 카드]. 주기 분포는 ③ QQ. 봉우리 위치 자체는 ⑩ E(f)에서 확인.
- **만드는 법**: `wavespectra`로 모델/부이 스펙트럼에서 `tp()`, `tm01()`, `tm02()` 산출(동일 모멘트 정의 보장) → ① 양식 산점 3패널. cutoff·tail 외삽 규약 통일.
- **함정·주의**: **모멘트 정의·적분구간·tail 외삽(f⁻⁴/f⁻⁵) 불일치가 최대 오류원** — 모델·관측 동일하게. **Tp 단독 검증 금지**(불연속) → 평균주기 병행 필수. 저파고 시 주기 신뢰도↓.
- **출처**: WMO, *Guide to Wave Analysis and Forecasting* (WMO-No. 702); Bidlot et al. (2002); wavespectra(`tp`/`tm01`/`tm02`, wavespectra.readthedocs.io).

---

### ★ 파랑장미 (파랑장미 / Wave rose)
- **무엇을 보여주나**: 파향을 방위 섹터로, Hs(또는 Tp·에너지flux)를 크기 class로 누적한 **극좌표 막대 분포**. 모델·관측의 **방향별 파고 빈도 구조**(우세 파향, 고파고가 어느 방향에서 오는가)를 비교.
- **읽는 법**: 각=파향(규약 명시: 오는 곳 meteorological vs 향하는 곳 oceanographic), 반경=빈도(%), 색=Hs class. 모델·관측 장미 **두 개를 나란히** 두고 우세 섹터·고파고 색의 방향·꼬리를 대조. *좋은 패턴*: 섹터별 빈도·색 분포 일치. *나쁜 패턴*: 우세 파향 회전(편향), 고파고 class가 다른 섹터에 몰림.
- **언제 쓰나**: [시계열]/[격자] 장기 통계·기후 검증, 파향 편향의 방향성 진단. 사건별이 아니라 *분포* 비교.
- **짝지표 & 교차링크**: 평균파향 **원형 bias/RMSE**(⑨), 방향별 Hs 통계 → [`08` 파향·원형통계 카드]. 방향+주기 결합은 ⑦. 풍향 장미(기상)는 [`07`]와 형제 그림.
- **만드는 법**: **`windrose`** 라이브러리 — `WindroseAxes.from_ax()` 후 `ax.bar(wd, hs, bins=[...], nsector=16, normed=True)`. 모델·관측 2-subplot. `nsector`(기본 16=22.5°)·Hs bins 동일하게. (이름은 wind이지만 임의 방향-크기 자료에 사용.)
- **함정·주의**: **방향 규약(meteo/ocean·진북·시계방향) 불일치 시 장미가 통째로 뒤집힘** → 캡션에 규약 명시. 저파고대 파향은 신뢰도 낮음 → Hs 임계 필터 권장. 막대=빈도이지 시간정렬 일치가 아님(분포 그림). 섹터 수·bins를 모델·관측 동일하게.
- **출처**: windrose 라이브러리(python-windrose, pypi.org/project/windrose); Bowers, Morton & Mould (2000, *Applied Ocean Research* 22(1):13–30, 파향 원형통계).

---

### 파향–주기 / 파향–파고 극좌표 밀도 (방향-척도 결합 극좌표 / Directional polar density: Dir–period / Dir–Hs)
- **무엇을 보여주나**: 각=파향, 반경=주기(또는 Hs)로 잡은 **2D 극좌표 밀도(또는 binned 평균)**. windsea(짧은 주기·풍하 방향)와 swell(긴 주기·원격 방향)이 극좌표에서 **분리된 군집**으로 보여, 모델이 두 시스템의 방향-주기 관계를 맞추는지 본다.
- **읽는 법**: 짧은 주기·특정 섹터의 밀집=windsea, 긴 주기·다른 섹터의 밀집=swell. 모델·관측 극좌표를 비교해 **swell 군집의 방향·주기 위치**가 맞는지, 모델이 windsea/swell을 하나로 뭉뚱그리는지 확인. 색=밀도 또는 평균 Hs.
- **언제 쓰나**: [시계열]/[스펙트럼] multimodal sea 진단, partition(⑫) 전 정성 점검. 벌크 검증이 숨기는 이중 시스템 구조 노출.
- **짝지표 & 교차링크**: ⑫ partition Hs/Tp/Dir 정량화의 정성 짝, ⑪ 2D 스펙트럼과 상보. 방향통계는 ⑨/[`08`].
- **만드는 법**: `matplotlib` `projection='polar'` + `np.histogram2d`(θ, T)→`pcolormesh`, 또는 `scipy.stats.binned_statistic_2d`로 섹터·주기 bin 평균 Hs. `set_theta_zero_location('N')`, `set_theta_direction(-1)`로 나침반 규약.
- **함정·주의**: 방향 규약·θ 0점·회전방향을 모델·관측 동일하게(극좌표는 실수 잦음). 저파고·저에너지 군집은 노이즈 — 밀도 임계로 거름. 정성 그림 — 결론은 ⑫의 partition 통계로 확정.
- **출처**: Hanson & Phillips (2001, *JTECH* 18(2):277–293, windsea/swell 분리); Portilla, Ocampo-Torres & Monbaliu (2009, *JTECH* 26(1):107–122, doi:10.1175/2008JTECHO609.1).

---

### 방향 분산 σθ(f) 검증 플롯 (방향 펼침 스펙트럼 / Directional spread vs frequency)
- **무엇을 보여주나**: 주파수별 방향 펼침 σθ(f)를 모델·부이가 함께 그린 곡선(±불확실성 띠). 에너지가 첨두 주위로 얼마나 좁게/넓게 퍼지는지(집중도)를 **주파수 분해**해 검증. 모델이 펼침을 **과소(너무 좁게)** 모의하는 경향을 포착.
- **읽는 법**: x=주파수, y=σθ(도). 두 곡선 비교 — 모델 곡선이 부이보다 **아래(좁음)** 면 directional spread 과소(흔한 약점). swell 대역(저주파)과 windsea 대역(고주파)에서 펼침이 다름. 부이 σθ 자체에 ±불확실성(부이 종류·추정법 의존)을 띠로.
- **언제 쓰나**: [스펙트럼] 부이 방향 파라미터(a1,b1) vs 모델 2D 스펙트럼. 방향 물리(GMD/Ardhuin 파라미터화) 평가.
- **짝지표 & 교차링크**: σθ = √(2(1−r1)) → [`08` 방향분산 카드]. 평균파향(⑨)·2D 스펙트럼(⑪)과 한 묶음. cos²ˢ 펼침함수 지수 s와 환산.
- **만드는 법**: `wavespectra`로 모델 E(f,θ)→주파수별 σθ; 부이는 a1,b1에서 r1=√(a1²+b1²)/m0, σθ=√(2(1−r1)). `matplotlib` 곡선 + `fill_between` 불확실성. (지표 자체는 `08`, 그림은 곡선 overlay.)
- **함정·주의**: 부이는 **4개 Fourier 계수(a1,b1,a2,b2)만** 측정 → σθ는 근사. **MEM/MLM 추정법에 따라 값이 달라짐** → 방법 명시. 부이 종류 간 ~7.5° 차이 보고(관측 불확실성 큼) → 작은 차이 과대해석 금지.
- **출처**: Kuik, van Vledder & Holthuijsen (1988, *JPO* 18(7)); Beckman & Long (2022, *Frontiers in Marine Science* 9:966855, doi:10.3389/fmars.2022.966855, 부이 오차 정량화); Gorman (2018, "Estimation of directional spectra from wave buoys for model validation", sciencedirect.com/science/article/pii/S2210983818300087, 저널 확인요).

---

### ★ 파향 원형통계 시각화 (원형통계 도표 / Circular-statistics plots: angular error rose, unit-vector residual)
- **무엇을 보여주나**: 파향 오차(Δθ=model−obs, −180°~180° wrap)를 **원형**으로 시각화 — (a) Δθ 각도 히스토그램(원형), (b) 단위벡터 잔차 산점, (c) 평균파향 오차 rose. 0/360° 경계 때문에 직선 통계가 안 되는 파향을 올바르게 진단.
- **읽는 법**: (a) Δθ 원형히스토그램이 0°에 뾰족하면 양호; 한쪽으로 치우치면 **원형 bias**(방향 계통 회전); 양방향으로 퍼지면 무작위 방향오차. (b) 단위벡터(cosθ,sinθ) 잔차가 원점 주위 등방이면 양호. *나쁜 패턴*: 히스토그램 봉이 ±수십° 이동(계통편차), 또는 multimodal(이중 시스템 혼동).
- **언제 쓰나**: [시계열]/[스펙트럼]/[격자] 파향 검증. 저Hs·multimodal에서 파향 신뢰도 점검(Hs 임계 필터 후).
- **짝지표 & 교차링크**: **원형 bias = circmean(Δθ), 원형 RMSE = √mean(wrap(Δθ)²), 벡터 RMSE** → [`08` 파향·원형통계 카드]. 풍향(`07`)·유향(`10`)과 **공통 원형통계 코어**(00 §4.2-8 정합 권고)로 통일. 분포는 ⑥ wave rose.
- **만드는 법**: `scipy.stats.circmean`/`circstd`(또는 직접 atan2 평균). `matplotlib` `projection='polar'`로 Δθ 히스토그램; 단위벡터 잔차는 일반 산점. **wrap은 `np.angle(np.exp(1j*np.deg2rad(Δθ)))`** 로 안전 처리.
- **함정·주의**: **0/360 wrap 미처리 시 치명적**(359°와 1°의 차가 358°로 계산됨) → 반드시 단위벡터/wrap. 저Hs 파향은 정의 모호 → 임계 필터. 부이 방향 규약·모델 규약 통일. 원형평균은 분산 크면 의미 약함(R_bar 동반 보고).
- **출처**: Bowers, Morton & Mould (2000, *Applied Ocean Research* 22(1):13–30); Hanson & Jensen (2007, *JTECH* 24(3), 방향 검증); Kuik et al. (1988, *JPO* 18(7)).

---

### 1D 주파수 스펙트럼 E(f) overlay (주파수 스펙트럼 중첩 / 1-D frequency spectrum overlay, log)
- **무엇을 보여주나**: 한 시각·한 지점의 부이 E_o(f)와 모델 E_m(f)를 **같은 축에 중첩**(보통 로그 종축). 벌크 파라미터를 넘어 **에너지의 주파수 분포 형상**(저주파 swell 봉 vs 고주파 windsea 봉, tail 기울기)을 직접 비교.
- **읽는 법**: x=주파수(Hz), y=E(f)(m²/Hz, 로그). **봉우리 위치(=Tp)·봉우리 에너지·봉 개수**(uni/multimodal) 일치 확인. 로그축이 **고주파 tail(f⁻⁴/f⁻⁵) 오차**를 드러냄. *나쁜 패턴*: 저주파 swell 에너지 과소/과대, 봉우리 주파수 이동, tail 기울기 불일치. 부이 신뢰구간(자유도) 띠 동반.
- **언제 쓰나**: [스펙트럼] 부이 1D 스펙트럼(공개 흔함) vs 모델 적분 스펙트럼. 사례·시각별 정밀 진단.
- **짝지표 & 교차링크**: **봉우리 주파수/에너지 오차, log-spectral distance** √mean[(logE_m−logE_o)²] → [`08` 1D 스펙트럼·모멘트 카드]. JONSWAP/PM 적합 파라미터(α,γ,fp). 주기는 ⑤, 방향까지는 ⑪.
- **만드는 법**: `wavespectra`로 양쪽 E(f)를 **동일 주파수 격자 보간**·동일 정규화 → `matplotlib` `semilogy` overlay. 부이 cutoff 일치. log-spectral distance는 numpy로.
- **함정·주의**: **동일 주파수 격자·고주파 cutoff·tail 외삽 통일 필수**(불일치가 가짜 차이). 부이 스펙트럼 자체 노이즈·신뢰구간(낮은 자유도). 한 시각 그림 → 사례 다수·통계 병행. 선형 종축은 swell 봉을 가림 → 로그.
- **출처**: WMO Guide No. 702; Pierson & Moskowitz (1964, *JGR* 69(24)); Hasselmann et al. (1973, JONSWAP, *Dtsch. Hydrogr. Z.* Suppl. A8); IFREMER WW3 spectral analysis tutorial(data-ww3.ifremer.fr, 공개 교재).

---

### 2D 방향 스펙트럼 E(f,θ) 극좌표 비교 (방향 스펙트럼 극좌표 / 2-D directional spectrum polar, model vs buoy)
- **무엇을 보여주나**: 주파수-방향 에너지 E(f,θ)를 **극좌표(반경=주파수 또는 주기, 각=방향, 색=에너지)** 로 그려 모델·부이(또는 SAR)를 나란히. **다중 swell 시스템의 방향·주기**까지 포함한 전체 sea-state 구조를 비교.
- **읽는 법**: 각 lobe(에너지 봉)가 하나의 파랑 시스템 — 위치(방향·주파수)·세기·펼침을 모델·관측 간 대조. *좋은 패턴*: lobe 개수·방향·주파수·에너지 일치. *나쁜 패턴*: swell lobe 방향 회전, 모델이 lobe를 너무 좁게/넓게(펼침 오차 ⑧), 인공 봉우리(부이 역문제).
- **언제 쓰나**: [스펙트럼] 모델 2D 출력 vs 부이(a1..b2→MEM/MLM 재구성)·HF radar·SAR. multimodal·복잡 sea 정밀 검증.
- **짝지표 & 교차링크**: 2D 상관·RMS 차, **partition별 Hs/Tp/Dir**(⑫). σθ(⑧)·평균파향(⑨)·E(f)(⑩)의 상위 그림. → [`08` 2D 스펙트럼·partition 카드].
- **만드는 법**: **`wavespectra`** `ds.spec.plot(kind='contourf', as_period=True, logradius=True, normalised=False, cmap='cmo.thermal')` (극좌표 자동). 부이는 MEM/MLM 재구성(추정법 명시). 모델·관측 동일 (f,θ) 격자·색스케일.
- **함정·주의**: **부이 2D는 4 Fourier 계수의 역문제(under-determined)** → MEM/MLM이 **인공 lobe** 생성 가능(실제로 오해 금지). 위성 SAR은 180° 방향 모호·고주파 cutoff. 색스케일·정규화 양쪽 동일하게(아니면 가짜 차이). 추정법(MEM vs MLM) 캡션 명시.
- **출처**: Hanson & Jensen (2007, *JTECH* 24(3)); Lygre & Krogstad (1986, *JPO* 16(12), MEM); Kuik et al. (1988, *JPO* 18(7)); wavespectra 극좌표 plot(spec.plot, wavespectra.readthedocs.io).

---

### windsea / swell partition 비교 (스펙트럼 분할 검증 / Wind-sea–swell partition comparison)
- **무엇을 보여주나**: 스펙트럼을 windsea + 다중 swell로 **분할(partition)** 한 뒤 **시스템별로** Hs_i·Tp_i·Dir_i를 모델·관측 비교(시스템별 산점/시계열, 또는 1D 스펙트럼의 windsea/swell 음영 split). multimodal sea에서 벌크 검증의 한계를 넘는다.
- **읽는 법**: windsea Hs와 swell Hs를 **각각** 산점/시계열로 — 모델이 swell은 맞추나 windsea를 과소(또는 반대)인지 분리 진단. swell partition의 **도달 시각·방향 오차**(원격 폭풍 추적). E(f) split 그림은 색으로 windsea(고주파)·swell(저주파) 영역 음영.
- **언제 쓰나**: [스펙트럼] multimodal·swell-dominated 해역. 벌크 Hs는 맞는데 물리가 틀린 경우 진단. partition 매칭으로 cross-assignment 처리.
- **짝지표 & 교차링크**: 시스템별 **Hs/Tp/Dir bias·RMSE** + ① 산점 양식 재사용 → [`08` partition 카드]. 정성 짝은 ⑦(Dir–주기 극좌표), 상위는 ⑪.
- **만드는 법**: **`wavespectra`** `ds.spec.partition.ptm1(wspd, wdir, ...)`(WW3 PTM1–5)·`partition.watershed`·wave-age 방법 → 각 partition `hs()`/`tp()`/`dpm()` → ① 산점. WW3 내장 `ww3_outp` partition도 가능. windsea 판별엔 풍속·풍향 입력.
- **함정·주의**: **임계·파라미터·partition 개수에 민감**(자동화 난점) → 방법·파라미터 캡션 명시. partition **매칭 규칙**이 결과 좌우(시스템 cross-assignment). 1D partition은 방향 손실. 디지털 필터로 노이즈 봉 제거 권장.
- **출처**: Hanson & Phillips (2001, *JTECH* 18(2):277–293); Hanson et al. (2009, *JTECH* 26(8), 3모델 hindcast); Portilla et al. (2009, *JTECH* 26(1):107–122, doi:10.1175/2008JTECHO609.1); wavespectra partition(PTM1–5/watershed, wavespectra.readthedocs.io/en/latest/partitioning.html).

---

### ★ 극치 진단: return-level + 극값 QQ (극치 진단도 / Extreme-value diagnostic: return-level + tail QQ)
- **무엇을 보여주나**: 장기 모델·관측 Hs의 **극치 분포**를 (a) **return-level plot**(재현주기 vs Hs, 신뢰구간 띠)과 (b) **극값 QQ/probability plot**(적합분포 대비 경험분위수)로 진단. 50·100년 **설계파고**와 모델의 극치 재현(흔히 과소)을 평가.
- **읽는 법**: (a) x=재현주기(로그), y=Hs. 관측 경험점이 모델 적합곡선의 **CI 띠 안**이면 일치; 모델 곡선이 관측 점 아래면 **극치 과소**. (b) 극값 QQ가 1:1에서 상단 이탈하면 tail 적합 불량. 모델·관측 두 적합을 겹쳐 **재현주기별 Hs 차**와 CI 중첩 여부 판정.
- **언제 쓰나**: [시계열]/[트랙] 장기(가능하면 ≥20년) hindcast vs 장기 부이/고도계. 설계·위험 평가.
- **짝지표 & 교차링크**: **POT-GPD / 연최대-GEV 매개변수, N년 return value, 부트스트랩 CI** → [`08` 극치 카드], [`03` GEV/POT/return level]. tail은 ③ QQ의 극단 확대판. 극치 차의 유의성(00 §4.1-6 권고).
- **만드는 법**: **`pyextremes`**(`EVA` 객체: `get_extremes('POT'/'BM')`, `fit_model('GP'/'GEV')`, `plot_return_values`, `plot_diagnostic`=return level+QQ+PDF+probability) 또는 `scipy.stats.genpareto`/`genextreme`. 임계는 MRL(mean residual life) plot·parameter-stability로 결정, declustering 필수.
- **함정·주의**: **임계 선택·declustering·표본수에 극도로 민감**(불확실성 큼) → **부트스트랩 CI 필수**. 모델 시간해상도·물리(ST4/ST6)가 극치 좌우. **비정상성**(기후추세·계절)으로 단일 분포 가정이 깨질 수 있음(00 §4.2-11). 짧은 기록의 100년값 외삽은 과신 금지.
- **출처**: Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Caires & Sterl (2005, *J. Climate* 18, ERA-40 100년 return value); Caires (2011, "Extreme Value Analysis: Wave Data", JCOMM Technical Report No. 57, jodc.go.jp/info/ioc_doc/JCOMM_Tech/JCOMM-TR-057.pdf); pyextremes(georgebv.github.io/pyextremes).

---

### ★ altimeter along-track colocation 산점도 + 트랙 지도 (고도계 트랙 콜로케이션 / Altimeter along-track colocation scatter + ground-track map)
- **무엇을 보여주나**: 위성 고도계 SWH along-track super-obs를 모델 격자에 **시공간 콜로케이션**한 산점도(+SI/bias box)와, **콜로케이션 지점의 ground-track 지도**(또는 트랙 색=Δ). 부이 없는 외해까지 **광역** Hs 검증.
- **읽는 법**: 산점은 ① 양식(1:1·회귀·SI/bias). 지도는 트랙 위 색=(model−altimeter) → **계통 bias의 지리분포**(폭풍대 과소·연안 과대). *좋은 패턴*: 외해 SI 5~10%, 트랙 색 0 주위. *나쁜 패턴*: 연안 ≤~50km에서 SI 급증(land/footprint 오염), 특정 해역 색 쏠림.
- **언제 쓰나**: [트랙](Jason-3, Sentinel-3A/3B/6, SARAL, CryoSat, HY-2 등) vs 모델 [격자]·부이. 외해 광역·연안 매치업.
- **짝지표 & 교차링크**: **bias·RMSE·SI**(①), 면적 분포는 ⑯ 지도. 3자 오차는 ⑮ TC. → [`08` 고도계 콜로케이션 카드], [`12` 위성 매치업·track-vs-grid].
- **만드는 법**: `xarray`로 고도계 L2/L3 1Hz→super-obs(수~수십 km 평균), 시공간 윈도우(공간 ≤0.5~0.75°/≤25km, 시간 ≤30~60분) 매칭 → `matplotlib` 산점 + `cartopy` 트랙 지도(색=Δ). QC(rain/ice/coastal flag) 필수.
- **함정·주의**: 고도계는 **SWH·풍속만**(주기·방향 없음). 트랙 sparse → 동시 다지점 불가. **연안 footprint 오염**(≤~50km) 주의. 미션 간 **cross-calibration** 안 하면 가짜 bias. 점 부이 vs ~km 평균 **대표성 오차**. 매치업 페어링 방법(거리/시간 임계)이 결과 좌우.
- **출처**: Janssen, Hansen & Bidlot (1997, *Weather and Forecasting* 12(4)); Sentinel-3A/3B·Jason-3 SWH 검증(*Remote Sensing* 12(13):2079); 연안 페어링 방법(*Remote Sensing of Environment*, 2024); 다중콜로케이션(Janssen 외, *Ocean Science* 15:249–268, 2019, os.copernicus.org/articles/15/249/2019; DOI 10.5194/os-15-249-2019 확인요).

---

### ★ Triple collocation 시각화 (삼중 콜로케이션 도표 / Triple-collocation error-variance & SNR plot)
- **무엇을 보여주나**: 세 독립 자료(예: 모델·부이·고도계)의 **개별 무작위 오차분산(또는 RMSE)·상대 scaling·SNR**을 막대/표로 시각화. 절대 기준(truth) 없이 "어느 자료가 더 정확한가"를 객관 표시.
- **읽는 법**: 막대=각 시스템 오차표준편차(낮을수록 정확). 흔히 **부이가 최소 오차**로 나옴. ETC면 각 자료의 진값 대비 상관(SNR)도. 시간·sea-state bin별로 막대를 나누면 조건별 오차구조. *주의 패턴*: 모델·ERA5가 한 강제력 공유 시 오차상관으로 막대가 비현실적으로 낮음(가정 위배).
- **언제 쓰나**: [격자]+[시계열]+[트랙] 세 자료 공통 콜로케이션이 충분할 때. 고도계·부이·모델 Hs 상호 오차 진단.
- **짝지표 & 교차링크**: **TC/ETC 오차분산·scaling·신호대잡음** → [`08` TC 카드], [`12` TC/ETC/QC]. 콜로케이션은 ⑭, [`15` matchup·대표성오차].
- **만드는 법**: TC 방정식(공분산 관계)을 `numpy`로 직접(3×3 공분산 → var(εᵢ)·βᵢ), ETC는 추가 상관식. 막대=`matplotlib`. sea-state bin은 `scipy.stats.binned_statistic`.
- **함정·주의**: **핵심 가정 = 세 자료 오차 독립·진값과 무상관**. 모델과 ERA5가 **같은 바람 강제력/동화관측** 공유하면 위배(00 §G-2,3) → 독립성 확인·캡션 명시. **동화·보간 산물(재분석·L4)을 독립 3자로 넣지 말 것**. 표본·콜로케이션 윈도우에 민감. 공통 동적범위 필요.
- **출처**: Stoffelen (1998, *JGR* 103(C4), TC 기초); Caires & Sterl (2003, *JGR Oceans* 108(C3):3098, doi:10.1029/2002JC001491); McColl et al. (2014, *GRL* 41(17):6229–6236, doi:10.1002/2014GL061322, ETC); HY-2B 대표성·ETC(*Remote Sensing* 17(23):3829, doi:10.3390/rs17233829).

---

### ★ Hs bias / difference 공간 지도 (공간 차 지도 / Gridded Hs bias / difference map)
- **무엇을 보여주나**: 우리 모델 [격자]를 ERA5/WAVERYS [격자]와 **공간 전면적**으로 비교해 bias(x,y)·RMSE(x,y)·R(x,y)·SI(x,y)를 **지도(색)** 로. 점 관측 없는 해역까지 **계통오차의 지리적 위치·계절성**을 진단.
- **읽는 법**: 색=각 격자점 시간계열의 bias(발산 색맵, 0=흰색)/RMSE/SI. *읽기*: 폭풍대 음(과소) 띠, 연안 양(과대), 경계류·빙역 가장자리의 패턴. 위도대·영역 평균선 병행. *나쁜 패턴*: 넓은 단색 영역(계통편차), 해안선 따라 줄무늬(재격자/해안 처리 artifact).
- **언제 쓰나**: [격자]vs[격자] NetCDF. 광역 진단, 점 검증(⑭)이 못 메우는 공간 커버리지.
- **짝지표 & 교차링크**: 격자별 **bias·RMSE·SI·R** → [`08` 격자-격자 공간비교 카드], [`02` 공간패턴 검증], [`15` regridding]. 점 검증 ⑭/⑮와 교차해석.
- **만드는 법**: `xarray`+`xesmf`(conservative/bilinear regridding, 공통 격자)→격자별 통계→`matplotlib`/`cartopy` `pcolormesh`. **발산 색맵 `cmocean.cm.balance`**(bias), `cmo.amp`(RMSE). 육지/해빙 마스크 통일.
- **함정·주의**: **재분석은 독립 진값 아님**(자체 오차·동화 한계) → "정답"으로 과신 금지, 부이/고도계와 교차. ERA5 파랑 ~0.5° → **연안 표현 한계**. Hs는 비선형 → 재격자 보존성·해안선 처리 주의. **GLORYS는 파랑변수 미제공** — 파랑 대조군은 ERA5/WAVERYS(확인요). 격자 해상도 차가 차이의 상당부분일 수 있음.
- **출처**: Hersbach et al. (2020, *QJRMS* 146(730):1999–2049, ERA5); WAVERYS(*Ocean Dynamics*, 2020, doi:10.1007/s10236-020-01433-w, CMEMS 파랑 재분석); WMO LC-WFV 절차; cmocean(Thyng et al. 2016, doi:10.5670/oceanog.2016.66).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 08 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(주축) | 짝 수치지표 | 08(및 타 파일) 교차링크 |
|---|---|---|---|---|---|
| 1 | Hs 검증 산점도 + 회귀 + SI/HH box | 시계열·트랙·격자 | 정확도+편향 | SI·bias·RMSE·R·OLS/HH slope | 08 Hs/SI/HH/회귀 · (공통 Taylor/Target) |
| 2 | Hs 밀도 산점도 (hexbin) | 트랙·격자 | 정확도(대용량 분포) | SI·R·분위수회귀 | 08 Hs · 12 매치업 |
| 3 | Hs QQ-plot (꼬리 강조) | 시계열·트랙·격자 | 분포·극치 | KS·percentile bias | 08 QQ/PDF·CDF |
| 4 | model–buoy 시계열 + 잔차 | 시계열 | 편향+위상+사건 | event bias/RMSE·lag | 08 시계열 · 06 lag · 01 |
| 5 | 주기 비교 (Tp/Tm01/Tm02) | 시계열·스펙트럼 | 정확도(주기) | bias·RMSE·SI·R | 08 주기·모멘트 |
| 6 | 파랑장미 wave rose | 시계열·격자 | 분포(방향) | 원형 bias/RMSE | 08 파향·원형 · 07 풍향장미 |
| 7 | 파향–주기/파고 극좌표 밀도 | 시계열·스펙트럼 | 패턴(이중 시스템) | partition Hs/Tp/Dir | 08 partition · ⑫ |
| 8 | 방향 분산 σθ(f) | 스펙트럼 | 패턴(펼침) | σθ=√(2(1−r1)) | 08 directional spread |
| 9 | 파향 원형통계 시각화 | 시계열·스펙트럼·격자 | 편향(방향) | 원형 bias/RMSE·벡터 RMSE | 08 파향·원형 · 07·10 원형코어 |
| 10 | 1D 스펙트럼 E(f) overlay | 스펙트럼 | 패턴(주파수) | log-spectral distance·fp | 08 1D 스펙트럼·모멘트 |
| 11 | 2D 스펙트럼 E(f,θ) 극좌표 | 스펙트럼 | 패턴(주파수×방향) | 2D 상관·RMS·partition | 08 2D 스펙트럼 |
| 12 | windsea/swell partition 비교 | 스펙트럼 | 패턴(시스템별) | 시스템별 Hs/Tp/Dir | 08 partition |
| 13 | 극치 return-level + 극값 QQ | 시계열·트랙 | 극값 | GPD/GEV·N년값·CI | 08 극치 · 03 GEV/POT |
| 14 | altimeter along-track colocation 산점 + 트랙지도 | 트랙·격자 | 정확도(광역) | bias·RMSE·SI | 08 고도계 · 12 track-vs-grid |
| 15 | Triple collocation 시각화 | 격자+시계열+트랙 | 오차분해(기준없음) | TC/ETC 오차분산·SNR | 08 TC · 12 TC/ETC |
| 16 | Hs bias/difference 공간 지도 | 격자 | 편향+패턴(공간) | 격자별 bias·RMSE·SI·R | 08 격자비교 · 02 공간 · 15 regrid |

> **묶음 권고**: 단일 그림 금지 원칙(§G-6)에 따라 파랑 검증 보고는 최소 **①(정확도+편향) + ④(위상/사건) + ③(분포)** 3장을 기본 세트로, 방향이 중요하면 **⑥/⑨**, 스펙트럼이면 **⑩/⑪/⑫**, 광역이면 **⑭/⑯**, 설계·극치면 **⑬**, 기준자료 신뢰도 평가면 **⑮**를 추가한다. 모든 임계(SI<0.15 등)는 **advisory + 영역의존 경고**로 캡션에 단다.

---

## 출처 메모 (이 파일에서 인용한 1차 출처)

**표준 교과서·지침 (실재)**
- Wilks, *Statistical Methods in the Atmospheric Sciences* (산점·QQ·KS·회귀 등 표준 시각화).
- Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (분포·범주·QQ).
- WMO, *Guide to Wave Analysis and Forecasting* (WMO-No. 702) (스펙트럼·주기·방향 정의).
- Coles (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD return level).

**학술 논문 (제목·저널·연도 웹 확인)**
- Mentaschi, Besio, Cassola & Mazzino (2013) "Problems in RMSE-based wave model validations," *Ocean Modelling* 72:53–58. (SI/HH)
- Bidlot et al. (2002) "Intercomparison of the performance of operational ocean wave forecasting systems with buoy data," *Weather and Forecasting*.
- Janssen, Hansen & Bidlot (1997) "Verification of the ECMWF wave forecasting system against buoy and altimeter data," *Weather and Forecasting* 12(4).
- Bowers, Morton & Mould (2000) "Directional statistics of the wind and waves," *Applied Ocean Research* 22(1):13–30.
- Kuik, van Vledder & Holthuijsen (1988) "A method for the routine analysis of pitch-and-roll buoy wave data," *JPO* 18(7).
- Lygre & Krogstad (1986) "Maximum entropy estimation of the directional distribution in ocean wave spectra," *JPO* 16(12).
- Hanson & Phillips (2001) "Automated analysis of ocean surface directional wave spectra," *JTECH* 18(2):277–293.
- Hanson & Jensen (2007) "Directional validation of wave predictions," *JTECH* 24(3).
- Hanson et al. (2009) "Pacific hindcast performance of three numerical wave models," *JTECH* 26(8).
- Portilla, Ocampo-Torres & Monbaliu (2009) "Spectral partitioning and identification of wind sea and swell," *JTECH* 26(1):107–122. (doi:10.1175/2008JTECHO609.1)
- Caires & Sterl (2003) "Validation of ocean wind and wave data using triple collocation," *JGR Oceans* 108(C3):3098. (doi:10.1029/2002JC001491)
- Caires & Sterl (2005) "100-year return value estimates ... from the ERA-40 data," *J. Climate* 18.
- Stoffelen (1998) "Toward the true near-surface wind speed ... triple collocation," *JGR* 103(C4).
- McColl et al. (2014) "Extended triple collocation," *GRL* 41(17):6229–6236. (doi:10.1002/2014GL061322)
- Beckman & Long (2022) "Quantifying errors in wind and wave measurements from a compact, low-cost wave buoy," *Frontiers in Marine Science* 9:966855. (doi:10.3389/fmars.2022.966855)
- Hersbach et al. (2020) "The ERA5 global reanalysis," *QJRMS* 146(730):1999–2049.
- Pierson & Moskowitz (1964) *JGR* 69(24); Hasselmann et al. (1973) JONSWAP, *Dtsch. Hydrogr. Z.* Suppl. A8.

**기관 자료·기술보고 (실재 URL)**
- ECMWF/WMO Lead Centre for Wave Forecast Verification (LC-WFV): https://confluence.ecmwf.int/display/WLW/Verification+results · .../Significant+wave+height
- Bidlot, "Twenty-one years of wave forecast verification," *ECMWF Newsletter* No. 150: https://www.ecmwf.int/en/newsletter/150/meteorology/twenty-one-years-wave-forecast-verification
- Caires (2011) "Extreme Value Analysis: Wave Data," JCOMM Technical Report No. 57: https://www.jodc.go.jp/info/ioc_doc/JCOMM_Tech/JCOMM-TR-057.pdf
- Comparison of ECMWF Hs forecasts with buoy data, *Weather and Forecasting* 34(6) (2019).
- WAVERYS, *Ocean Dynamics* (2020), doi:10.1007/s10236-020-01433-w (CMEMS 파랑 재분석).
- IFREMER WW3 spectral-analysis tutorial: https://data-ww3.ifremer.fr (공개 교재).

**소프트웨어 (실존 도구)**
- `wavespectra` — 1D/2D 스펙트럼 I/O·파라미터·partition·극좌표 plot: https://wavespectra.readthedocs.io (`spec.plot(kind='contourf')`, `hs/tp/tm01/tm02/dpm`, `partition.ptm1..ptm5/watershed`).
- `windrose` — 파랑장미: https://pypi.org/project/windrose (`WindroseAxes.from_ax`, `ax.bar`).
- `pyextremes` — POT/GEV·return level·진단도: https://georgebv.github.io/pyextremes (`EVA`, `plot_return_values`, `plot_diagnostic`).
- `cmocean` — 해양 색맵(balance/amp/thermal/dense): Thyng et al. (2016, *Oceanography* 29(3), doi:10.5670/oceanog.2016.66).
- `matplotlib`, `numpy`, `scipy`(circmean/circstd·genpareto/genextreme·binned_statistic), `xarray`/`xesmf`, `cartopy`.

**확인요 (확정 인용 금지 — §G-5)**
- *Remote Sensing* 12(13):2079 (Sentinel-3A/3B·Jason-3 SWH 검증) — URL은 확인, **DOI 10.3390/rs12132079는 미검증(확인요)**.
- *Ocean Science* 15:249–268 (2019, 다중콜로케이션) — URL 확인, **DOI 10.5194/os-15-249-2019는 패턴 추정(확인요)**.
- Gorman (2018) "Estimation of directional spectra from wave buoys for model validation" — 제목·연도·ScienceDirect ID(S2210983818300087) 확인, **저널·권·DOI 미확정(확인요)**.
- *Remote Sensing of Environment* (2024) 연안 altimeter-buoy 페어링 — 08에서 인용, 본 세션 권·DOI 재확인 안 함(확인요).
- GLORYS는 물리 해양 재분석으로 **파랑변수 미제공** — 파랑 대조군은 ERA5/WAVERYS 사용(확인요).
- 해석 임계(SI<0.15, R≥0.9, 평균파향 RMSE 20~30° 등)는 **외해 관행 advisory** — 해역·해상도·기준자료 의존(§G-4).
