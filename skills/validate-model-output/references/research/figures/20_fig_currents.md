# 20. 검증 시각화 레퍼런스 — 해류·조류·순환 도메인편 (Validation Figures: Currents / Circulation)

본 문서는 재사용 Skill의 **references — 검증 시각화(그림) 카탈로그** 시리즈의 **[해류·조류·순환 도메인편]**이다. 수치모델 해류장(u/v, 유향, 수송, 와류)을 ERA5/GLORYS 등 재분석, 정점·표류 관측(ADCP·표류부이), HF radar 표면류, 위성 고도계 지형류와 **비교·검증할 때 어떤 그림을 어떻게 그리고 어떻게 읽을지**를 "그림 카드"로 정리한다. 대응하는 수치지표(메서드)는 [`10_domain_currents_circulation.md`](../10_domain_currents_circulation.md)에 있으며, 본 문서는 그 카드와 **교차링크로 연결**하고 중복 정의를 피한다.

> **이 문서의 범위와 경계**
> - **여기서 다룸**: 해류·조류 **고유의 벡터/방향/회전/라그랑지안/와류** 그림 — quiver·streamline·벡터 오버레이, current rose, 변동·조류타원, 회전스펙트럼 CW/CCW, PVD, 드리프터 분리거리, 속력 분포, 성분 산점, 수송 시계열, MKE/EKE 맵, Okubo–Weiss, eddy census, FTLE/LCS.
> - **여기서 안 다룸(중복 방지)**: 모든 도메인 공통·횡단 그림(일반 Taylor diagram, target diagram, 일반 오차장 지도, 일반 시계열 비교, bootstrap CI 그림 등)은 **[공통편]** 담당. 본편은 필요 시 교차링크만 한다(예: 벡터 통계 요약은 성분별 Taylor → 공통편).
>
> **그림 해석의 대전제(→ [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats))**
> 1. **기준자료 ≠ 참값.** GLORYS·OSCAR·위성 지형류·HF radar L4는 reference이지 truth가 아니다. 그림 캡션·해석에 "truth/정답" 금지, "모델−기준 차이"로 표기.
> 2. **임계는 advisory.** "벡터상관 |ρ|≥0.7", "EKE 비 0.8~1.2", "분리거리 임계" 등은 해역·해상도·자료정밀도 의존 → 단정 금지, 영역의존 경고 동반.
> 3. **단일 그림 금지.** 한 그림으로 결론내지 않는다. 최소 (정확도+편향+패턴/분포) 3축 + 유의성을 함께 본다. 벡터는 **크기·방향·회전을 분리**해 본다(속력만 맞아도 방향이 틀릴 수 있음).
> 4. **모델·관측을 동일 처리.** 같은 격자·같은 필터·같은 기간·같은 검출 알고리즘으로 양측을 처리해야 그림 비교가 유효(spurious difference 방지, →`15`).

## 한 줄 목차 (이 파일에 담은 그림 카드 16종)
1. 벡터장 quiver 맵 (Vector field quiver map)
2. 유선장 streamline 맵 (Streamline map)
3. 모델–관측 벡터 오버레이 (Model–obs vector overlay)
4. 유향장미 — current rose (Current rose)
5. 주축·변동타원 맵 (Principal-axis / variance ellipse map)
6. 조류타원 맵 (Tidal current ellipse map)
7. 회전스펙트럼 CW/CCW 그림 (Rotary spectrum plot)
8. 누적변위도 PVD (Progressive vector diagram)
9. 드리프터 궤적 비교·분리거리 (Drifter trajectory & separation distance)
10. 속력 분포 Q-Q / PDF / CDF (Speed distribution plots)
11. u/v 성분 산점도 (Component scatter / density)
12. 수송 시계열·단면 수송 (Volume transport time series & section)
13. MKE / EKE 맵 (Mean & eddy kinetic energy map)
14. Okubo–Weiss 맵 (Okubo–Weiss map)
15. 와류 센서스·궤적 (Eddy census & track plot)
16. FTLE / LCS 맵 (FTLE / LCS ridge map)

> **그림→검증목적→짝지표→10 교차링크 요약표**는 문서 끝에 있다.

---

### 1. 벡터장 quiver 맵 (Vector field quiver map)
- **무엇을 보여주나**: 격자 해류장(u/v)을 화살표(quiver)로 그려, 모델의 평균류·순환 패턴(경계류·환류·연안류 분기)을 한눈에. 화살표 길이·방향=유속 크기·방향, 배경 컬러=속력 또는 와도. 모델·기준(GLORYS 등)을 같은 스케일로 나란히(side-by-side) 배치해 정성 비교.
- **읽는 법**: 화살표 방향=흐름 방향(진북 기준), 길이∝속력(범례 화살표로 스케일 명시 필수). 배경색은 cmocean `speed`(0 기준 순차) 또는 와도는 `balance`(0 중심 발산형). 좋은 패턴: 경계류 축 위치·폭·방향이 기준과 일치, 환류 중심이 맞음. 나쁜 패턴: 화살표가 과밀(over-plot)해 패턴 안 보임, 모델 경계류가 기준 대비 폭 넓고 약함(저해상도 신호), 연안에서 화살표가 육지로 향함(마스크·좌표 오류).
- **언제 쓰나**: 자료형=격자(NetCDF, 모델/재분석/위성 지형류). 검증목적=평균 순환 구조의 1차 정성 점검(정량 전 단계).
- **짝지표 & 교차링크**: 벡터 평균류·steadiness, 벡터 RMSE → [10 #벡터 평균류·유속/유향 통계], [10 #벡터 RMSE·복소 RMSE]. 공간 일치도는 [10 #흐름장 공간 패턴 비교]. 배경 와도는 [10 #Okubo-Weiss](본편 #14).
- **만드는 법**: `matplotlib` `ax.quiver(x, y, u, v, ...)` 또는 `xarray` `ds.plot.quiver(x='lon', y='lat', u='u', v='v')`; 격자 솎기(`u[::n,::n]`)로 과밀 방지, `scale`·`quiverkey`로 범례. 배경 `ax.pcolormesh(..., cmap=cmocean.cm.speed)`. 지도투영은 `cartopy`. 면적가중·진북정렬은 `15`(벡터 회전) 선행.
- **함정·주의**: 격자 간격 불균일/곡선격자면 화살표 밀도 왜곡 → 균일 재격자 후 솎기. 위경도 그대로 그리면 고위도에서 동서 화살표 과장 → 투영 또는 종횡비 보정. **스케일 화살표(quiverkey) 없으면 정량 비교 불가**. 모델·기준은 반드시 동일 색·동일 화살표 스케일.
- **출처**: `matplotlib.pyplot.quiver` 공식 문서(https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html); `xarray.Dataset.plot.quiver`(https://docs.xarray.dev/en/stable/generated/xarray.Dataset.plot.quiver.html); cmocean 색지도 Thyng et al. (2016), "True colors of oceanography," *Oceanography*, 29(3), 9–13 (DOI 확인요) — 패키지(https://matplotlib.org/cmocean/). 해류장 표준은 Emery & Thomson, *Data Analysis Methods in Physical Oceanography*. *(논문 그림 복제 아님 — 유형·사양만 기술.)*

---

### 2. 유선장 streamline 맵 (Streamline map)
- **무엇을 보여주나**: 흐름의 접선 곡선(streamline)을 연속적으로 그려 순환 경로·환류·분기·수렴을 매끄럽게 표현. quiver가 점별 벡터라면 streamline은 흐름의 **위상적 구조**(환류 중심, 분리/재부착)를 강조. 선 굵기·색을 속력에 매핑하면 속력장도 동시 표현.
- **읽는 법**: 선의 방향=흐름 경로, 선 밀도/굵기=속력(옵션). 좋은 패턴: 모델·기준의 환류 중심 위치, 경계류 분리점(separation latitude), 재순환 셀이 일치. 나쁜 패턴: 모델에서 환류가 닫히지 않거나 분리점이 크게 이동, 연안에서 streamline이 부자연스럽게 끊김(마스크/발산 처리 문제).
- **언제 쓰나**: 자료형=격자(2D 수평 흐름장). 검증목적=순환의 **구조·위상** 정성 비교(중규모·경계류·환류).
- **짝지표 & 교차링크**: 순압유선함수(transport streamfunction)·수송 → [10 #수송량](본편 #12), [`04_conservation_energy_flux.md`] 순압유선함수. 공간 패턴상관 → [10 #흐름장 공간 패턴 비교].
- **만드는 법**: `matplotlib` `ax.streamplot(x, y, u, v, density=..., color=speed, linewidth=...)`; **규칙격자 필요**(비정규격자는 재격자 선행, →`15`). 속력 매핑 `color=np.hypot(u,v)`, `cmap=cmocean.cm.speed`.
- **함정·주의**: `streamplot`은 **등간격 규칙격자만** 입력 가능(곡선/비정규격자 직접 불가). 결측(NaN)이 있으면 적분이 끊김 → 마스크/채움 명시. density 과대 시 시각적 혼잡, 과소 시 구조 누락. streamline은 **순간 흐름**의 접선(시변 흐름의 실제 입자경로(pathline)와 다름) → 라그랑지안 해석엔 PVD·입자추적(본편 #8·#9) 사용.
- **출처**: `matplotlib` streamplot 문서 및 quiver/stream 튜토리얼(https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html, https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.15-Quiver-and-Stream-Plots/). 흐름 위상 구조 개념은 표준 유체역학/물리해양 교과서. *(논문 그림 복제 아님.)*

---

### 3. 모델–관측 벡터 오버레이 (Model–obs vector overlay)
- **무엇을 보여주나**: 동일 위치·동일 시각의 모델 벡터와 관측 벡터(HF radar 격자, ADCP 정점, 드리프터, 위성 지형류)를 **같은 그림에 색을 달리해 겹쳐** 그려, 크기·방향 편차를 직접 눈으로 비교. 차이 벡터(model−obs)를 별도 색으로 추가하면 편향 패턴이 드러남.
- **읽는 법**: 한 지점에 두 화살표(예: 검정=관측, 빨강=모델) + 선택적 차이 화살표(회색). 좋은 패턴: 두 화살표가 길이·방향 거의 겹침, 차이 벡터가 짧고 무작위 방향. 나쁜 패턴: 차이 벡터가 한 방향으로 정렬(체계적 회전/편향 — 좌표 오정렬·Ekman 각 오차 의심), 모델 화살표가 일관되게 짧음(속력 과소).
- **언제 쓰나**: 자료형=격자(HF radar)·정점/궤적(ADCP·드리프터)에 모델 보간. 검증목적=공간 분포된 벡터 편차의 정성·국지 진단.
- **짝지표 & 교차링크**: 벡터/복소 RMSE, 복소상관 위상각(체계적 회전), 벡터 bias → [10 #벡터 RMSE·복소 RMSE], [10 #복소(벡터) 상관계수 — Kundu], [10 #HF radar / ADCP 대조 검증 프로토콜]. 차이 벡터의 평균은 벡터 bias.
- **만드는 법**: `matplotlib` `ax.quiver` 2회 호출(색 분리) + 동일 `scale`·`quiverkey`. 보간·정합은 `15`(시공간 매칭·벡터 회전) 선행. `cartopy` 위에 배치.
- **함정·주의**: **두 quiver의 scale을 반드시 동일**하게(다르면 비교 무의미). HF radar는 표층 ~0.5–2 m 평균류 — ADCP 최상층/모델 표층과 심도 불일치 → 캡션에 유효심 명시. 화살표 과밀 시 차이 패턴이 묻힘 → 솎기 또는 영역 분할. GDOP 불량 HF radar 셀 제외.
- **출처**: HF radar/ADCP/모델 벡터 비교 관행 — MDPI *Remote Sens.* 17(7):1243 (2025)(https://www.mdpi.com/2072-4292/17/7/1243); 연안모델 평가 Liu et al. (2009)(http://bragg.ceoas.oregonstate.edu/Papers2/Liu2009.pdf). 작도 도구는 `matplotlib.quiver`(상동). *(논문 그림 복제 아님.)*

---

### 4. 유향장미 — current rose (Current rose)
- **무엇을 보여주나**: 유향(흐름이 향하는 방향)을 방위 섹터로 나누고, 각 섹터의 **빈도**를 막대 길이로, **유속 구간(bin)**을 색층으로 쌓은 극좌표 막대그림. 한 정점/격자점에서 흐름이 어느 방향으로 얼마나 자주·얼마나 세게 흐르는지 분포를 요약. 모델·관측을 나란히 그려 우세 방향·이방성 일치를 비교.
- **읽는 법**: 각 = 방위(보통 "흐름이 향하는 쪽" toward 규약 — 풍향의 from 규약과 반대, 캡션에 명시), 반경 = 빈도(%), 색 = 속력 계급. 좋은 패턴: 모델·관측의 우세 섹터(최장 막대)·방향 분산·속력 색 분포가 유사. 나쁜 패턴: 모델 우세방향이 회전(섹터 이동), 모델이 특정 방향에 과집중(변동 과소), 고속 색층이 관측보다 얇음(강류 빈도 과소).
- **언제 쓰나**: 자료형=시계열(ADCP·유속계·드리프터·HF radar 격자점). 검증목적=방향 분포·이방성·속력-방향 결합 분포의 정성 검증(특히 조류·연안류 우세 방향).
- **짝지표 & 교차링크**: 원형통계(평균 결과길이 R, 원형 RMSE), 주축 방위각 → [10 #유향(방향) 검증 — 원형통계], [10 #주축·변동타원](본편 #5). 속력 분포 → [10 #속력 분포 비교](본편 #10).
- **만드는 법**: `windrose` 라이브러리(`WindroseAxes`, `ax.bar(direction, speed, nsector=16/36, bins=...)`) — 변수만 유향·유속으로 대입(현장에서 "current rose"로 사용). 빈도표는 `ax._info['table']`, `ax._info['dir']`로 추출. 대안: `matplotlib` 극좌표 `ax.bar`로 수동 구현.
- **함정·주의**: **방향 규약(toward vs from)**을 모델·관측 동일하게(혼동이 가장 흔한 오류). 저속 구간 방향은 불안정 → 속력 임계 이하 제외 또는 별도 표시. 섹터 수(nsector)·속력 bin을 모델·관측 동일 설정. 빈도는 표본 수에 의존 → 동일 기간·동일 샘플링. 분포만 보고 시간 위상(타이밍)은 못 봄 → 시계열·상관 병행.
- **출처**: `windrose` 라이브러리 문서(https://python-windrose.github.io/windrose/) 및 PyPI(https://pypi.org/project/windrose/) — 유속·유향 데이터에 적용. 방향 통계 표준은 Mardia & Jupp, *Directional Statistics*. *(논문 그림 복제 아님.)*

---

### 5. 주축·변동타원 맵 (Principal-axis / variance ellipse map)
- **무엇을 보여주나**: 각 정점/격자점에서 유속 편차 (u′,v′)의 공분산행렬로부터 구한 **변동타원**(장축=최대 변동 방향, 단축=최소 변동, 장단축비=이방성)을 위치마다 그린 지도. 변동의 우세 방향·세기·이방성을 공간적으로 표현. 모델·관측 타원을 겹치거나 나란히 비교.
- **읽는 법**: 타원 장축 방향=변동 주축 방위, 장축 길이∝√(최대 분산), 장단축비=이방성(가늘수록 한 방향 변동 우세, 원에 가까우면 등방). 좋은 패턴: 모델·관측 타원의 장축 방향·크기·이방성 일치, 연안에서 장축이 해안선과 평행. 나쁜 패턴: 모델 타원이 회전(주축 방위 어긋남), 모델 타원이 작음(변동 과소·과확산), 거의 원형인데 관측은 가늘다(이방성 미재현).
- **언제 쓰나**: 자료형=시계열(정점) 또는 격자(전역 타원 지도). 검증목적=**변동(에너지) 구조**의 방향성·이방성 검증(조류·연안류 정렬). 조류타원(#6)과 달리 **비주기 포함 총변동**.
- **짝지표 & 교차링크**: 공분산 고유값/고유벡터, 이방성 지수, 주축 방위각 차, EKE → [10 #주축·변동타원], [10 #운동에너지 진단 MKE/EKE](본편 #13).
- **만드는 법**: `numpy` 공분산 `np.cov(u', v')` → `np.linalg.eigh`로 고유값·고유벡터 → `matplotlib.patches.Ellipse`(폭·높이=2√λ, 각=장축 방위)로 각 위치에 배치. 다중 시간규모는 `scipy.signal` 대역통과 후 산출.
- **함정·주의**: 다중 시간규모(조석+계절+중규모) 혼재 시 주축 모호 → 대역통과 후. 거의 등방이면 주축 방향이 표본 변동에 민감(작은 표본 불안정). 평균 제거(편차) 필수. **조류타원과 혼동 금지**(이쪽은 주기 분해 없이 총변동). 타원 스케일 범례 필수.
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography*(주축/variance ellipse, PCA); 연안류 적용 *Ocean Sci.* 20, 1229 (2024)(https://os.copernicus.org/articles/20/1229/2024/). 작도는 `matplotlib.patches.Ellipse`. *(논문 그림 복제 아님.)*

---

### 6. 조류타원 맵 (Tidal current ellipse map)
- **무엇을 보여주나**: 조화분석으로 분조별(M2·S2·K1·O1…) 조류를 분해해 얻은 **조류타원**(장축=최대 조류속, 단축=최소속·부호로 회전방향, 경사각=장축 방위, 위상)을 분조별로 격자/정점에 그린 지도. 모델 조석류의 진폭·방향·회전·위상을 관측과 검증. 회전방향(CW/CCW)을 색으로 구분.
- **읽는 법**: 타원 장축=최대 조류속 방향·크기, 단축 부호=회전방향(+CCW/−CW, 보통 색 분리: 예 적=CW, 청=CCW), 경사각=장축이 동에서 반시계로 이루는 각, (선택) 위상 화살표/색=조류 도달 위상. 좋은 패턴: 분조별 장축 크기·방향·**회전방향**·위상이 관측과 일치. 나쁜 패턴: **회전방향 반대**(명백한 모델 결함), 장축 과소·과대(진폭 오차), 경사각 회전(방향 오차), 위상 지연(조석 전파 오차).
- **언제 쓰나**: 자료형=조류 시계열(ADCP·유속계, ≥~15일로 M2/S2 분리, 1년이면 다수 분조) 또는 격자점 시계열. 검증목적=조석류 진폭·위상·회전 검증(연안·해협 조류 우세역).
- **짝지표 & 교차링크**: 장축/단축/경사/위상 분조별 오차, 진폭 RMSE, 위상차(°), in-phase/quadrature 벡터차, form factor → [10 #조화분석·조류타원]. 해수면 조화상수는 [`11_domain_sea_level_tides.md`].
- **만드는 법**: `utide`(`utide.solve(t, u, v=v, lat=...)` → 출력 `Lsmaj, Lsmin, theta, g`; `pip install utide`) 또는 `ttide_py`. 타원 작도는 파라미터로 매개변수 타원 생성 후 `matplotlib.patches.Ellipse`/`ax.plot`; 회전방향은 단축 부호로 색 분리. 격자 전역은 각 셀에 `utide.solve` 반복.
- **함정·주의**: 비조석 변동(폭풍·계절류) 혼입 시 추정 오염 → 충분한 길이·신뢰구간(UTide는 잔차 스펙트럼 기반 CI 제공). 천해 비선형분조(M4 등) 누락 주의. **위상 기준시(Greenwich vs local) 일치**. 회전방향 색 규약을 모델·관측 동일. Rayleigh 분리 기준 미충족 분조 비교 금지.
- **출처**: Pawlowicz, Beardsley & Lentz (2002), *Computers & Geosciences*, 28, 929–937, [doi:10.1016/S0098-3004(02)00013-4](https://doi.org/10.1016/S0098-3004(02)00013-4)(T_TIDE); Codiga (2011) UTide 보고서(https://www.po.gso.uri.edu/codiga/utide/2011Codiga-UTide-Report.pdf); python `utide`(https://www.clarkrichards.org/2024/09/05/tidal-current-analysis-utide/); 타원 파라미터 정의 BAWiki(https://wiki.baw.de/en/index.php/Harmonic_Analysis_of_Current_Velocity); 작도 예 ocefpaf(https://ocefpaf.github.io/python4oceanographers/blog/2015/05/18/utide_ellipse/). 조석류 모델-관측 비교는 *Cont. Shelf Res.*(https://www.sciencedirect.com/science/article/abs/pii/S0278434317303710). *(논문 그림 복제 아님.)*

---

### 7. 회전스펙트럼 CW/CCW 그림 (Rotary spectrum plot)
- **무엇을 보여주나**: 벡터(복소) 시계열을 시계(CW, 음주파수)·반시계(CCW, 양주파수) 회전성분 에너지로 분해한 스펙트럼을 주파수축에 그린 그림. 관성진동(NH에서 CW 우세)·조석·저주파류의 회전 특성을 주파수별로 표시. 회전계수 r(σ) 곡선을 함께 그려 편극(타원성)을 진단. 모델·관측 스펙트럼을 겹쳐 피크 위치·세기 비교.
- **읽는 법**: x=주파수(또는 주기; CW를 음, CCW를 양 또는 좌우 분리 패널), y=스펙트럼 밀도(보통 log). 관성주파수 f·조석주파수(M2 등)에 세로 기준선. 회전계수 r: −1=순수 CW, 0=직선왕복, +1=순수 CCW. 좋은 패턴: 모델·관측의 관성대역 CW 피크·조석 피크 위치·세기, 해당 대역 r 부호가 일치. 나쁜 패턴: 관성 피크 누락/이동(상층 혼합·시간해상 문제), 조석 피크 진폭 차, r 부호 반대(회전성 미재현), 고주파 노이즈 융기.
- **언제 쓰나**: 자료형=벡터 시계열(ADCP·유속계·드리프터·모델 격자점, 균일 샘플링·충분 길이). 검증목적=흐름의 **회전·주파수 구조** 검증(관성·조석·저주파 회전).
- **짝지표 & 교차링크**: CW/CCW 스펙트럼 밀도, 회전계수 r, 관성/조석 대역 적분에너지 → [10 #회전스펙트럼 — Gonella]. 스칼라 PSD/조화분석은 [`05_spectral_eof_modal.md`], [`06_timeseries_signal.md`].
- **만드는 법**: `w = u + 1j*v`; `scipy.signal.welch`를 복소 입력에 적용하거나 `numpy.fft.fft(w)`의 양/음 주파수를 S+(CCW)/S−(CW)로 분리; 세그먼트 평균으로 자유도 확보, 사전 detrend·window(`scipy.signal.detrend`, hann). 회전계수 `r=(Sp−Sm)/(Sp+Sm)`. 신호처리 코어는 `05`/`06`와 공유(window·detrend·정규화 일치).
- **함정·주의**: 정상성·등간격 요구(결측·불규칙은 보간 또는 Lomb-Scargle 변형). 짧은 기록은 저주파 신뢰도 낮음. 자유도 확보 위한 스무딩이 분해능과 trade-off. **모델·관측 동일 window·세그먼트·정규화**. 적도 부근 관성효과 약화 해석 주의. CW/CCW 부호 규약(반구) 명시.
- **출처**: Gonella, J. (1972), "A rotary-component method for analysing meteorological and oceanographic vector time series," *Deep-Sea Research*, 19, 833–846(https://www.sciencedirect.com/science/article/abs/pii/0011747172900022); Emery & Thomson 교과서(회전스펙트럼 절); Cambridge, *Time Series Data Analysis in Oceanography*, Ch.22(https://www.cambridge.org/core/books/abs/time-series-data-analysis-in-oceanography/rotary-spectrum-analysis/AAD234828D4C234CA3BA848F70525743). *(논문 그림 복제 아님.)*

---

### 8. 누적변위도 PVD (Progressive vector diagram)
- **무엇을 보여주나**: 한 정점의 Eulerian 유속 시계열을 시간 적분해 "가상 입자가 그 점 흐름을 따라 이동했을 변위"를 (X,Y) 곡선으로 그린 의사 라그랑지안 궤적. 모델·관측의 누적 수송 방향·거리, 순(net) 이동, 곡선 형태(반전류·관성 루프)를 시각·정량 비교.
- **읽는 법**: 원점에서 시작하는 곡선, 끝점=순변위(방향·거리), 곡선 둘레=누적 이동거리, 루프=관성/조석 진동. 시간 색(컬러바)으로 진행 표시. 좋은 패턴: 모델·관측 PVD의 순변위 방향·길이, 루프 구조가 유사. 나쁜 패턴: 순변위 방향·길이 차(장기 수송 편향), 모델에 루프 없음/과다(관성·조석 진동 재현 문제).
- **언제 쓰나**: 자료형=단일 정점 시계열(ADCP·유속계·모델 격자점, 균일 시간간격). 검증목적=정점 흐름의 누적·시간적분 정확도 정성 진단.
- **짝지표 & 교차링크**: 순변위·누적이동거리 차, 평균류(steadiness) → [10 #Progressive Vector Diagram (PVD)], [10 #벡터 평균류·유속/유향 통계]. 실제 입자추적은 본편 #9.
- **만드는 법**: `X=np.cumsum(u)*dt; Y=np.cumsum(v)*dt`; `matplotlib` `ax.plot(X, Y)` + 시간 색은 `ax.scatter(X, Y, c=time)` 또는 `LineCollection`. 적분 시작점·기간 모델·관측 일치.
- **함정·주의**: **공간 균질 흐름 가정** — 실제 입자는 다른 곳을 지나며 다른 흐름을 만남 → 장기간일수록 실제 궤적과 괴리, **진짜 입자추적(#9)과 혼동 금지**. 적분이 오차를 누적(드리프트). 결측은 적분 전 보간 명시. 단위(거리축 km) 일관.
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography*(PVD 표준 정의·주의사항). 작도는 `numpy.cumsum` + `matplotlib`. *(논문 그림 복제 아님.)*

---

### 9. 드리프터 궤적 비교·분리거리 (Drifter trajectory & separation distance)
- **무엇을 보여주나**: 모델 흐름장으로 적분한 가상 입자 궤적과 실제 표류부이(드리프터) 궤적을 같은 지도에 겹쳐 그리고(좌), 시간에 따른 **분리거리** d(t)=|x_model−x_drifter|를 곡선으로(우) 표시. 흐름장의 통합·시간누적 정확도를 궤적 형태와 분리 성장으로 검증.
- **읽는 법**: (좌) 동일 출발점에서 갈라지는 두 궤적, (우) d(t) 성장 곡선(여러 드리프터면 평균±분산 밴드). 좋은 패턴: 단기(예 1–2일) 궤적이 붙어가고 d(t)가 천천히 성장, Liu–Weisberg 스킬 s가 1에 가까움. 나쁜 패턴: 초반부터 급격히 분리(흐름 방향 오차), 체계적으로 한쪽으로 벗어남(평균류 편향·Ekman/windage 미반영).
- **언제 쓰나**: 자료형=시변 표면(또는 층) 속도장(모델/HF radar/재분석) + 드리프터 GPS 궤적. 검증목적=라그랑지안 수송 정확도(표류·탐색구조·오염확산 응용).
- **짝지표 & 교차링크**: 분리거리 d(t), Liu–Weisberg 정규화 누적 라그랑지안 분리 스킬 s, 쌍입자 분리율(확산) → [10 #라그랑지안 입자추적·표류부이 대조]. 의사 라그랑지안은 PVD(#8). HF radar 라그랑지안 검증은 [10 #HF radar / ADCP 대조 검증 프로토콜].
- **만드는 법**: `OceanParcels`(parcels)로 입자 적분(`pset.execute`, AdvectionRK4) 또는 직접 RK4 적분; 분리거리는 `numpy` + 지구거리(`pyproj`/haversine). 동일 출발점·시각·기간. windage·확산 항 처리 명시.
- **함정·주의**: 카오스적 분기로 **장기 궤적은 본질적 발산** → 단기 평가 중심. 드리프터는 풍압·파랑 영향(undrogued면 더) → windage 보정. 표본 적으면 통계 불안정(다수 드리프터·앙상블 출발점 권장). 스킬 정의(누적식 vs 단순 분리)·정규화 기준 명시. 지구곡률 거리(평면거리 금지).
- **출처**: Liu, Y., & Weisberg, R. H. (2011), *J. Geophys. Res. Oceans*, 116, C09013, [doi:10.1029/2010JC006837](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JC006837)(정규화 누적 라그랑지안 분리 스킬); 스킬 민감도 *Frontiers Mar. Sci.* (2021)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2021.630388/full); 입자추적 도구 OceanParcels(https://oceanparcels.org/, https://pypi.org/project/parcels/). *(논문 그림 복제 아님.)*

---

### 10. 속력 분포 Q-Q / PDF / CDF (Speed distribution plots)
- **무엇을 보여주나**: 유속(또는 u/v 성분) 값의 **분포 전체**를 모델·관측에서 비교하는 그림 묶음 — (a) Q-Q 플롯(동일 누적확률의 모델 vs 관측 분위수 산점), (b) PDF(히스토그램/KDE 겹침), (c) CDF(두 누적분포). 평균·RMSE가 비슷해도 꼬리(강류 이벤트)·형태가 다를 수 있음을 드러냄.
- **읽는 법**: Q-Q는 대각선이면 동일 분포(꼬리 이탈=극값 재현 차), PDF 겹침면적=Perkins 점수, CDF 최대 수직거리=KS 거리. 좋은 패턴: Q-Q 점들이 1:1 선 위, PDF 형태 일치, CDF 근접. 나쁜 패턴: Q-Q 상단이 1:1 아래로 휨(P95/P99 강류 과소), 모델 PDF가 좁음(변동 과소), CDF가 한쪽으로 치우침(편향).
- **언제 쓰나**: 자료형=시계열·격자(전 격자점 풀링 또는 지점별). 검증목적=속력 **분포·꼬리·극값 재현**(시간 위상과 무관한 통계적 일치).
- **짝지표 & 교차링크**: KS 거리 D, Perkins 스킬 점수, P90/P95/P99 백분위 오차, Wasserstein 거리 → [10 #속력 분포 비교 — Q-Q·PDF·CDF]. 시간 위상은 상관/RMSE([10 #스칼라 성분 오차지표])와 병행.
- **만드는 법**: `numpy.quantile`로 Q-Q, `scipy.stats.ks_2samp`로 KS, `numpy.histogram`/`scipy.stats.gaussian_kde`로 PDF, `matplotlib` `ax.plot`+1:1 선. 속력은 비음·우편향 고려.
- **함정·주의**: 분포 비교는 **시간 타이밍을 안 봄** → 상관·RMSE 병행 필수. 표본 적으면 꼬리 추정 불안정. KS는 분포 중앙에 민감·꼬리에 둔감 → Anderson–Darling/백분위 병행. 격자 비교 시 동일 해상도로 다운샘플. 동일 기간·동일 샘플링.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences*(Q-Q·분포검정); Perkins et al. (2007), *J. Climate*, 20, 4356–4376(분포 겹침 스킬); KS는 표준 통계. 작도는 `scipy.stats`/`numpy`/`matplotlib`. *(논문 그림 복제 아님.)*

---

### 11. u/v 성분 산점도 (Component scatter / density)
- **무엇을 보여주나**: 모델 vs 관측의 u 성분(과 별도로 v 성분) 짝값을 산점도로 그리고 1:1 선과 최소제곱 회귀선을 겹쳐, 성분별 편향·기울기·산포를 진단. 표본 많으면 2D 밀도(hexbin/2D 히스토그램)로. 속력 산점도도 같은 방식.
- **읽는 법**: x=관측, y=모델, 점 구름의 1:1 선 대비 위치(위=과대, 아래=과소), 회귀 기울기 b(≈1 무편향)·절편 a(≈0), 점 산포=무작위 오차, 색=밀도. 좋은 패턴: 구름이 1:1 선에 밀집, b≈1·a≈0, R² 높음. 나쁜 패턴: 기울기<1(진폭 과소·회귀희석), 절편≠0(상수 편향), 부채꼴 산포(이분산), 둘로 갈라진 구름(체제 혼합·부호 오류).
- **언제 쓰나**: 자료형=시계열·격자 짝표본. 검증목적=성분별 정확도·편향·진폭(기울기)의 정량 진단(벡터 통계의 성분 분해 보완).
- **짝지표 & 교차링크**: 성분 RMSE/MAE/Bias, 회귀 기울기·절편·R², Pearson r → [10 #스칼라 성분 오차지표 — RMSE/MAE/Bias]. 벡터·회전 정보는 복소상관([10 #복소(벡터) 상관계수])·벡터 오버레이(#3)로 보완(성분 산점은 방향 결합을 못 봄).
- **만드는 법**: `matplotlib` `ax.scatter`(소표본) 또는 `ax.hexbin`/`plt.hist2d`(대표본) + 1:1 선·`numpy.polyfit`/`scipy.stats.linregress` 회귀선·텍스트로 b·a·R². u·v 각각 패널, 동일 축범위.
- **함정·주의**: 성분 산점은 **벡터 회전/방향 결합을 못 봄**(u·v를 따로 보면 좌표 회전 오차를 놓침) → 복소상관·벡터 오버레이 병행. 좌표계(동/북, 진북) 일치 필수. OLS 기울기는 관측오차로 1보다 작게 편의(회귀희석) → 필요 시 직교회귀/총최소제곱. 동일 축·1:1 선 없으면 오독.
- **출처**: 표준 검증 관행 — Wilks, *Statistical Methods in the Atmospheric Sciences*; 해양 모델 스킬 종합 Stow et al. (2009), *J. Mar. Syst.*, 76, 4–15(https://www.sciencedirect.com/science/article/abs/pii/S0924796308001103). 작도는 `matplotlib`/`scipy.stats`. *(논문 그림 복제 아님.)*

---

### 12. 수송 시계열·단면 수송 (Volume transport time series & section)
- **무엇을 보여주나**: (a) 해협·경계류·자오면 단면을 통과하는 부피수송 T(Sv)의 **시계열**(모델 vs 관측 추정·재분석, 평균·변동·계절/경년)과, (b) 단면의 법선속도 v⊥를 (거리×수심) 단면도(contour/pcolormesh)로 그려 수송의 수직·수평 구조를 표시. 통합 순환량의 정량 검증.
- **읽는 법**: (a) x=시간, y=수송(Sv), 모델·기준 곡선 겹침 + 평균선; (b) 단면도는 x=단면거리, y=수심(아래로), 색=법선속도(`balance`, 유입/유출 부호), 등치선. 좋은 패턴: 수송 평균·표준편차·계절위상 일치, 단면의 유속 코어 위치·깊이·폭이 기준과 일치. 나쁜 패턴: 평균 수송 편향, 변동 진폭 과소, 경계류 코어가 넓고 약함(저해상도), 코어 깊이 어긋남(성층 오차).
- **언제 쓰나**: 자료형=격자(모델/재분석) 단면 적분, 계류선 어레이 관측. 검증목적=수송량·경계류·MOC의 정량·구조 검증.
- **짝지표 & 교차링크**: 부피/질량 수송 T, 평균·표준편차·변동, Sverdrup 균형 대비 → [10 #수송량 — 부피/질량 수송]; 순압유선함수·MOC·MHT는 [`04_conservation_energy_flux.md`].
- **만드는 법**: `xarray`로 단면 추출(`ds.sel`/`xgcm`으로 셀면적·법선속도), `T=(v_perp*dz*dl).sum()`; 시계열 `ax.plot`, 단면도 `ax.contourf`/`pcolormesh`(`cmocean.cm.balance`, 0 중심). 단면 정의·깊이 모델·관측 일치.
- **함정·주의**: 단면 정의·심도 적분 방식에 민감(시작/끝/깊이 일치). 격자 해상도가 경계류 폭을 못 풀면 수송 과소. 부분셀·지형 표현 차로 모델 간 단면 일치 필요. 법선 방향 부호 규약 명시. 관측은 계류선 보간 산물(대표성 한계) → reference로 취급.
- **출처**: Wunsch (2011), "The decadal mean ocean circulation and Sverdrup balance," *J. Mar. Res.*(https://www.researchgate.net/publication/228722138_The_decadal_mean_ocean_circulation_and_Sverdrup_balance); Talley et al., *Descriptive Physical Oceanography*; volume transport 개관(https://www.sciencedirect.com/topics/earth-and-planetary-sciences/volume-transport). 작도는 `xarray`/`xgcm`/`matplotlib`/`cmocean`. *(논문 그림 복제 아님.)*

---

### 13. MKE / EKE 맵 (Mean & eddy kinetic energy map)
- **무엇을 보여주나**: 흐름 에너지를 평균류(MKE=½(ū²+v̄²))와 변동(EKE=½(u′²+v′²))으로 분해해 공간 분포 지도로 표시. EKE는 중규모 와류 활동도의 핵심 지표 → 모델의 와류 변동성을 위성 지형류(AVISO)·재분석과 비교. 보통 log 스케일 컬러맵.
- **읽는 법**: 색=에너지(보통 log₁₀, cmocean `amp`/`thermal` 등 순차형), 고EKE 띠=경계류·전선(예 흑조·만류 연장). 좋은 패턴: 고EKE 영역 위치·크기·강도가 위성과 일치(EKE 비 ≈1). 나쁜 패턴: 모델 EKE 광역 과소(와류 비허용/저해상도), 국지 과대(수치 노이즈·격자 잡음), 고EKE 띠 위치 이동(경계류 경로 오차).
- **언제 쓰나**: 자료형=격자(모델/재분석), 위성 고도계(표면 지형류 EKE), 드리프터(라그랑지안 EKE). 검증목적=와류 변동성·중규모 활동도 검증.
- **짝지표 & 교차링크**: MKE/EKE, EKE 비(모델/위성), 면적평균·영역별 EKE → [10 #운동에너지 진단 — MKE/EKE]; KE 파수스펙트럼·캐스케이드는 [`04_conservation_energy_flux.md`]. 와류 구조는 Okubo–Weiss(#14)·eddy census(#15).
- **만드는 법**: 레이놀즈 분해 — 시간평균 `ubar=u.mean('time')`, 편차 `up=u-ubar`, `EKE=0.5*(up**2+vp**2).mean('time')`(`xarray`); 위성 지형류는 SLA 미분으로 u′,v′. `ax.pcolormesh(..., norm=LogNorm(), cmap=cmocean.cm.amp)`.
- **함정·주의**: **평균 정의·필터 대역에 강하게 의존**(시간평균 vs 이동평균, 중규모 vs 계절) → 모델·위성 동일 정의 필수. 위성 EKE는 시공간 해상도 한계로 소규모 와류 누락 → **모델을 위성 해상도로 다운샘플 후 비교**. 라그랑지안(드리프터) EKE는 표본분포 편향. log 스케일·동일 색범위.
- **출처**: 위성·재분석 EKE 검증 *Frontiers Mar. Sci.* (2022)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.1032699/full); 전심도 EKE *GRL* (2023)(https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL103114); Southern Ocean EKE *JGR Oceans* (2021)(https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JC016973). 작도는 `xarray`/`matplotlib`/`cmocean`. *(논문 그림 복제 아님.)*

---

### 14. Okubo–Weiss 맵 (Okubo–Weiss map)
- **무엇을 보여주나**: 흐름장 각 점의 W=s_n²+s_s²−ω²(정상변형·전단변형·상대와도)를 계산해 지도로. W<0(회전 우세)=와류 코어 후보, W>0(변형 우세)=필라멘트/변형 영역. 모델 흐름장의 중규모 구조·와류 분포를 진단·비교. 보통 발산형 컬러맵 + W<−W₀ 등치선으로 와류영역 표시.
- **읽는 법**: 색=W(0 중심 `balance`형: 음=회전/와류 코어, 양=변형), 폐곡선(W<−W₀)=와류 후보. 좋은 패턴: 모델·관측의 와류 코어 위치·개수·크기 분포 유사. 나쁜 패턴: 임계 따라 검출 영역이 급변(임계 민감), 변형장 잡음으로 점박이(허위 검출), 모델 와류 과소(점성·해상도).
- **언제 쓰나**: 자료형=2D 격자 흐름장(모델/재분석/위성 지형류, 공간 미분 필요). 검증목적=중규모 변형 vs 회전 구조 진단, 와류 센서스 1차 검출기.
- **짝지표 & 교차링크**: W, 임계 W₀(보통 0.2σ_W 또는 −2×10⁻¹²s⁻²), 와류 면적비율 → [10 #Okubo-Weiss 파라미터]; 와도/enstrophy는 [`04_conservation_energy_flux.md`]. 후속 와류 통계는 eddy census(#15).
- **만드는 법**: `numpy`/`xarray` 유한차분으로 ∂u/∂x 등 → `sn=ux-vy; ss=vx+uy; w=vx-uy; W=sn**2+ss**2-w**2`; 노이즈 자료는 사전 스무딩(`scipy.ndimage.gaussian_filter`). `ax.pcolormesh(W, cmap=cmocean.cm.balance, vmin=-a, vmax=a)` + `ax.contour(W, levels=[-W0])`.
- **함정·주의**: **임계값 선택에 민감**(검출 와류 수 크게 변동) → 임계·산출법 명시, 모델·관측 동일. 변형장 잡음에 약함(허위 검출) → 스무딩. 단독으론 와류 경계·극성(저/고기압) 미구분 → 와도 부호·기하 병행. 2D·준지형 가정. 미분 격자 해상도 의존.
- **출처**: Okubo (1970), *Deep-Sea Res.*, 17, 445–454; Weiss (1991), *Physica D*, 48, 273–294; 적용 리뷰 *Ocean Sci.* 7, 317–334 (2011)(https://os.copernicus.org/articles/7/317/2011/os-7-317-2011.pdf); 개념 정리 Wikipedia(https://en.wikipedia.org/wiki/Okubo%E2%80%93Weiss_parameter). 작도는 `numpy`/`xarray`/`matplotlib`/`cmocean`. *(논문 그림 복제 아님.)*

---

### 15. 와류 센서스·궤적 (Eddy census & track plot)
- **무엇을 보여주나**: 자동 검출·추적한 중규모 와류의 (a) 위치·극성(저/고기압)·경계 폐곡선을 지도에 표시하고, (b) 궤적(서향 전파)을 선으로, (c) 특성 분포(반경·진폭·수명·전파속도)를 히스토그램/극좌표로 요약. 모델 와류 활동을 위성 와류 아틀라스(META/Chelton)와 통계적으로 검증.
- **읽는 법**: (지도) 와류 경계 폐곡선 + 극성 색(예 적=저기압성/CCW(NH), 청=고기압성), 궤적선; (분포) 반경·진폭·수명·전파속도 히스토그램의 모델 vs 위성 겹침. 좋은 패턴: 개수·반경·진폭·수명·서향전파속도 분포 일치(히스토그램·KS). 나쁜 패턴: 모델 과소검출(해상도·점성), 반경 과대(평활), 진폭 과소, 전파속도 어긋남(β·평균류 상호작용 오차).
- **언제 쓰나**: 자료형=위성 고도계 SLA 격자·모델 SSH/속도 격자(일·주 단위, 와류반경 ≥~2격자). 검증목적=와류 개수·기하·수명·전파의 통계적 검증.
- **짝지표 & 교차링크**: 와류 개수·밀도·반경·진폭·수명·전파속도 분포, 분포 KS검정 → [10 #와류 센서스·추적]; 검출 1차기는 Okubo–Weiss(#14). 분포 비교는 속력분포 그림(#10)과 같은 통계.
- **만드는 법**: `py-eddy-tracker`(SLA 기반 검출·추적, Mason et al. 2014)로 와류 식별·궤적 생성 → 속성 추출; 지도는 `cartopy`에 경계 폐곡선·궤적 `ax.plot`, 분포는 `matplotlib` 히스토그램. **모델·위성 동일 알고리즘·동일 파라미터**(공정 비교 핵심).
- **함정·주의**: **알고리즘·임계마다 결과 상이** → 반드시 동일 설정으로 양측 처리. 진폭 임계(예 1 cm)가 작은 와류 특성 과소·계단효과. 위성 해상도 한계로 소형·근접 와류 누락 → 모델을 동일 해상도로 처리 후 비교. 극성 색 규약·반구(회전부호) 명시.
- **출처**: Chelton, Schlax & Samelson (2011), "Global observations of nonlinear mesoscale eddies," *Prog. Oceanogr.*, 91, 167–216; Nencioli et al. (2010), *J. Atmos. Oceanic Technol.*(기하 검출); Faghmous et al. (2015), *Scientific Data*, 2:150028(https://www.nature.com/articles/sdata201528); META3.1 아틀라스 Pegliasco et al. (2022), *ESSD*, 14, 1087(https://essd.copernicus.org/articles/14/1087/2022/); 도구 py-eddy-tracker(Mason et al. 2014)(https://github.com/AntSimi/py-eddy-tracker). *(논문 그림 복제 아님.)*

---

### 16. FTLE / LCS 맵 (FTLE / LCS ridge map)
- **무엇을 보여주나**: 유한시간 Lyapunov 지수(FTLE) 장을 지도로 그려, 인접 입자의 분리율(스트레칭)이 큰 **능선(ridge)**=라그랑지안 코히어런트 구조(LCS)=수송장벽을 추출. 흡인/반발 LCS(전·후방 적분)를 색으로. 모델·관측(재분석/HF radar/위성 지형류) 흐름장의 라그랑지안 수송 구조 일치를 검증(오염·표류 확산 장벽 진단).
- **읽는 법**: 색=FTLE 값(능선=밝은 선형 구조), 전방적분=반발 LCS(확산 장벽), 후방적분=흡인 LCS(집적선). 좋은 패턴: 모델·관측 능선의 위치·방향·강도 일치. 나쁜 패턴: 능선 위치 어긋남(흐름 구조 오차), 적분기간 따라 구조 급변(파라미터 민감), 노이즈성 잡선(속도장 불확실성 증폭).
- **언제 쓰나**: 자료형=시변 2D(또는 3D) 격자 속도장(모델/재분석/HF radar/위성 지형류). 검증목적=라그랑지안 수송장벽·코히어런트 구조의 정성·정량 비교.
- **짝지표 & 교차링크**: FTLE 값, 능선 위치·강도, FSLE(고정 분리비 도달시간), 능선 거리/구조유사도 → [10 #유한시간 Lyapunov 지수 / LCS]; 입자추적 코어는 드리프터 검증(#9)과 공유.
- **만드는 법**: 격자 입자 적분(`OceanParcels` 또는 RK4) → 유동지도 ∇φ로 Cauchy–Green 텐서 C → `numpy.linalg.eigvalsh`의 λ_max → `FTLE=ln(sqrt(λmax))/|T|`; `ax.pcolormesh(FTLE, cmap='magma')`. 적분기간 T·격자간격 모델·관측 동일.
- **함정·주의**: **적분기간 T·해상도에 결과 민감**(짧으면 구조 불명, 길면 노이즈·외삽). 속도장 불확실성이 FTLE에 증폭 → **앙상블로 불확실성 정량 권장**. 능선=LCS는 근사(엄밀 LCS는 추가 조건). 계산비용 큼(대용량 격자는 청크·다운샘플). 결측·경계 처리 명시. 모델·관측 동일 T·격자·적분기.
- **출처**: Haller (2015), "Lagrangian Coherent Structures," *Annu. Rev. Fluid Mech.*, 47, 137–162; Shadden, Lekien & Marsden (2005), *Physica D*, 212, 271–304; 연안 적용 리뷰 *Frontiers Mar. Sci.* (2024)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1345260/full); 불확실성 *Ocean Sci.* 21, 401 (2025)(https://os.copernicus.org/articles/21/401/2025/); 입자추적 OceanParcels(https://oceanparcels.org/). *(논문 그림 복제 아님.)*

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 10 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적 | 짝 수치지표 | `10` 교차링크 카드 |
|---|---|---|---|---|---|
| 1 | 벡터장 quiver 맵 / Vector quiver | 격자 | 평균 순환 구조 정성 | 벡터 평균류·VRMSE | 벡터 평균류·유속/유향 통계; 벡터 RMSE |
| 2 | 유선장 streamline 맵 / Streamline | 격자 | 순환 위상 구조 | 순압유선함수·패턴상관 | 수송량; 흐름장 공간 패턴 비교 |
| 3 | 벡터 오버레이 / Vector overlay | 격자·정점 | 국지 벡터 편차·체계회전 | 복소상관 위상·벡터 bias | 복소상관(Kundu); HF radar/ADCP 프로토콜 |
| 4 | 유향장미 / Current rose | 시계열 | 방향·속력 결합 분포 | 원형통계 R·주축 방위 | 유향 원형통계; 주축·변동타원 |
| 5 | 변동타원 맵 / Variance ellipse | 시계열·격자 | 변동 방향성·이방성 | 공분산 고유값·이방성 | 주축·변동타원; MKE/EKE |
| 6 | 조류타원 맵 / Tidal ellipse | 조류 시계열·격자 | 조석류 진폭·위상·회전 | 장/단축·경사·위상 오차 | 조화분석·조류타원 |
| 7 | 회전스펙트럼 / Rotary spectrum | 벡터 시계열 | 회전·주파수 구조 | CW/CCW 밀도·회전계수 r | 회전스펙트럼(Gonella) |
| 8 | 누적변위도 PVD | 정점 시계열 | 정점 누적 수송 | 순변위·누적거리 차 | Progressive Vector Diagram |
| 9 | 드리프터 궤적·분리거리 | 속도장+드리프터 | 라그랑지안 수송 정확도 | 분리거리 d(t)·LW 스킬 s | 라그랑지안 입자추적·표류부이 대조 |
| 10 | 속력 분포 Q-Q/PDF/CDF | 시계열·격자 | 분포·꼬리·극값 재현 | KS·Perkins·백분위 오차 | 속력 분포 비교 |
| 11 | u/v 성분 산점도 | 시계열·격자 | 성분 정확도·편향·진폭 | 성분 RMSE/bias·기울기·R² | 스칼라 성분 오차지표 |
| 12 | 수송 시계열·단면 / Transport | 격자·계류선 | 수송량·경계류 구조 | 부피수송 T·변동 | 수송량 — 부피/질량 수송 |
| 13 | MKE/EKE 맵 | 격자·위성·드리프터 | 와류 변동성·중규모 활동 | MKE/EKE·EKE 비 | 운동에너지 진단(MKE/EKE) |
| 14 | Okubo–Weiss 맵 | 격자 | 변형 vs 회전·와류 후보 | W·임계 W₀·와류면적비 | Okubo-Weiss 파라미터 |
| 15 | 와류 센서스·궤적 / Eddy census | SLA·SSH 격자 | 와류 개수·기하·수명·전파 | 반경·진폭·수명·전파속도 분포 | 와류 센서스·추적 |
| 16 | FTLE/LCS 맵 | 시변 속도장 | 라그랑지안 수송장벽 | FTLE 값·능선 위치·FSLE | FTLE / FSLE / LCS |

> **공통편과의 경계(중복 방지)**: 일반 Taylor diagram·target diagram·일반 오차장 지도·bootstrap CI·일반 시계열 비교 그림은 **[공통편]** 참조. 본편은 해류·조류 고유의 벡터/방향/회전/라그랑지안/와류 그림에 한정한다. 벡터 통계의 종합 요약(성분별 Taylor)이 필요하면 [10 #Taylor 다이어그램·표준화 통계 요약] + 공통편 Taylor 카드를 함께 호출한다.

---

## 출처 (References)

**표준 교과서·표준지침**
- Emery, W. J., & Thomson, R. E. *Data Analysis Methods in Physical Oceanography* (Elsevier). — 벡터 통계·주축/변동타원·PVD·회전스펙트럼·조화분석 표준.
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences* (Academic Press). — Q-Q·분포검정·산점/회귀.
- Mardia, K. V., & Jupp, P. E. *Directional Statistics* (Wiley). — 원형통계(유향·current rose).
- Talley, L. D., et al. *Descriptive Physical Oceanography* (Elsevier). — 수송·순환.

**논문 (확인된 1차 출처 — 권·페이지·DOI 대조)**
- Gonella, J. (1972). A rotary-component method for analysing meteorological and oceanographic vector time series. *Deep-Sea Research*, 19, 833–846. — 회전스펙트럼. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0011747172900022)
- Pawlowicz, R., Beardsley, B., & Lentz, S. (2002). Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE. *Computers & Geosciences*, 28, 929–937. [doi:10.1016/S0098-3004(02)00013-4](https://doi.org/10.1016/S0098-3004(02)00013-4) — 조류타원.
- Okubo, A. (1970). Horizontal dispersion of floatable particles. *Deep-Sea Research*, 17, 445–454. — Okubo–Weiss.
- Weiss, J. (1991). The dynamics of enstrophy transfer in two-dimensional hydrodynamics. *Physica D*, 48, 273–294. — Okubo–Weiss.
- Chelton, D. B., Schlax, M. G., & Samelson, R. M. (2011). Global observations of nonlinear mesoscale eddies. *Prog. Oceanogr.*, 91, 167–216. — 와류 센서스.
- Nencioli, F., et al. (2010). A vector geometry–based eddy detection algorithm. *J. Atmos. Oceanic Technol.* — 기하 와류 검출.
- Faghmous, J. H., et al. (2015). A daily global mesoscale ocean eddy dataset from satellite altimetry. *Scientific Data*, 2:150028. [Nature](https://www.nature.com/articles/sdata201528)
- Pegliasco, C., et al. (2022). META3.1exp global mesoscale eddy trajectory atlas. *Earth Syst. Sci. Data*, 14, 1087–1107. [ESSD](https://essd.copernicus.org/articles/14/1087/2022/)
- Haller, G. (2015). Lagrangian Coherent Structures. *Annu. Rev. Fluid Mech.*, 47, 137–162. — LCS.
- Shadden, S. C., Lekien, F., & Marsden, J. E. (2005). Definition and properties of LCS from FTLE. *Physica D*, 212, 271–304. — FTLE/LCS.
- Liu, Y., & Weisberg, R. H. (2011). Evaluation of trajectory modeling... normalized cumulative Lagrangian separation. *J. Geophys. Res. Oceans*, 116, C09013. [doi:10.1029/2010JC006837](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JC006837) — 분리거리 스킬.
- Perkins, S. E., et al. (2007). Evaluation of the AR4 climate models' simulated daily... PDFs. *J. Climate*, 20, 4356–4376. — 분포 겹침 스킬.
- Stow, C. A., et al. (2009). Skill assessment for coupled biological/physical models of marine systems. *J. Mar. Syst.*, 76, 4–15. — 해양 모델 스킬 종합. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0924796308001103)
- Thyng, K. M., et al. (2016). True colors of oceanography: Guidelines for effective and accurate colormap selection. *Oceanography*, 29(3), 9–13. — cmocean 색지도. **DOI 확인요**(10.5670/oceanog.2016.66 추정, 미대조).
- Mason, E., et al. (2014). A new sea surface height–based code for oceanic mesoscale eddy tracking. *J. Atmos. Oceanic Technol.* — py-eddy-tracker 알고리즘. (서지 세부 **확인요**.)

**작도·분석 도구 (공식 문서)**
- matplotlib `quiver`(https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html), `streamplot`/quiver 튜토리얼(https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.15-Quiver-and-Stream-Plots/)
- xarray `Dataset.plot.quiver`(https://docs.xarray.dev/en/stable/generated/xarray.Dataset.plot.quiver.html)
- cmocean 색지도(https://matplotlib.org/cmocean/, https://github.com/matplotlib/cmocean)
- windrose 라이브러리(https://python-windrose.github.io/windrose/, https://pypi.org/project/windrose/) — current rose
- UTide (python)(https://pypi.org/project/utide/, 예제 https://www.clarkrichards.org/2024/09/05/tidal-current-analysis-utide/); Codiga (2011) UTide 보고서(https://www.po.gso.uri.edu/codiga/utide/2011Codiga-UTide-Report.pdf)
- OceanParcels(https://oceanparcels.org/, https://pypi.org/project/parcels/) — 입자추적
- py-eddy-tracker(https://github.com/AntSimi/py-eddy-tracker, https://py-eddy-tracker.readthedocs.io/) — 와류 검출·추적
- 조류타원 작도 예 ocefpaf(https://ocefpaf.github.io/python4oceanographers/blog/2015/05/18/utide_ellipse/); 타원 파라미터 정의 BAWiki(https://wiki.baw.de/en/index.php/Harmonic_Analysis_of_Current_Velocity)

**웹 출처 (검증·적용 사례)**
- HF radar/ADCP/모델 벡터 검증 종합 — MDPI *Remote Sens.* 17(7):1243 (2025)(https://www.mdpi.com/2072-4292/17/7/1243)
- 연안모델 평가 — Liu et al. (2009)(http://bragg.ceoas.oregonstate.edu/Papers2/Liu2009.pdf)
- 비정상 연안류·변동타원 — *Ocean Sci.* 20, 1229 (2024)(https://os.copernicus.org/articles/20/1229/2024/)
- 조석류 모델-관측 비교 — *Cont. Shelf Res.*(https://www.sciencedirect.com/science/article/abs/pii/S0278434317303710)
- 위성·재분석 EKE 검증 — *Frontiers Mar. Sci.* (2022)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.1032699/full); 전심도 EKE *GRL* (2023)(https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL103114)
- Okubo–Weiss 적용 — *Ocean Sci.* 7, 317–334 (2011)(https://os.copernicus.org/articles/7/317/2011/os-7-317-2011.pdf); 개념 Wikipedia(https://en.wikipedia.org/wiki/Okubo%E2%80%93Weiss_parameter)
- FTLE/LCS 연안 리뷰 — *Frontiers Mar. Sci.* (2024)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1345260/full); FTLE 불확실성 *Ocean Sci.* 21, 401 (2025)(https://os.copernicus.org/articles/21/401/2025/)
- 라그랑지안 스킬 민감도 — *Frontiers Mar. Sci.* (2021)(https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2021.630388/full)
- 수송·Sverdrup — Wunsch (2011)(https://www.researchgate.net/publication/228722138_The_decadal_mean_ocean_circulation_and_Sverdrup_balance); volume transport 개관(https://www.sciencedirect.com/topics/earth-and-planetary-sciences/volume-transport)

> **주**: 본 카탈로그는 **논문·도서의 실제 그림을 복제하지 않으며**, 그림의 유형·축·기호·작도 사양만 기술한다. DOI는 본문에서 1차 출처로 대조해 확실한 것만 표기했고(Pawlowicz 2002, Liu & Weisberg 2011), 미대조 항목은 "(확인요)"로 명시했다(Thyng et al. 2016 cmocean DOI, Mason et al. 2014 서지). 임의 DOI 생성은 하지 않았다. 기준자료(GLORYS/OSCAR/위성 지형류/HF radar)는 reference이지 truth가 아니며, 모든 해석 임계는 advisory로 영역·해상도 의존 경고를 동반한다(→ `00_overview_taxonomy.md` §G).
