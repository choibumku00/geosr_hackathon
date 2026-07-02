# 검증 시각화 카탈로그 — 해수면·조위편 (Verification Figure Catalog — Sea Level / Tides)

이 문서는 재사용 Skill의 **검증 시각화(그림)·표 레퍼런스** 시리즈 중 **해수면(sea level)·조석(tides) 도메인편**이다. 메서드 카탈로그 [`11_domain_sea_level_tides.md`](../11_domain_sea_level_tides.md)가 "무엇을 계산하는가(지표)"를 다룬다면, 이 파일은 그 지표를 **어떤 그림으로 보여주고 어떻게 읽는가**를 다룬다. 각 그림 카드는 메서드 카드의 짝지표와 교차링크되어, Skill이 "지표 계산 → 표준 그림 생성"을 한 묶음으로 호출하도록 설계한다.

> **범위 구분(중복 방지):** 산점도·Q-Q·테일러 다이어그램·target diagram·일반 오차장 지도 등 **모든 도메인 공통/횡단 그림은 [공통편]이 담당**한다. 이 파일은 **해수면·조석에 고유한 그림**(조화상수 페이저·복소차 벡터·등조시도·스큐서지·DAC 보정효과·track-vs-grid·재현수위·datum 사다리 등)에 집중한다. 공통 그림이 필요하면 그쪽을 교차링크한다.

> ⚠️ **그림을 그리기 전에 반드시 읽을 원칙** → [`00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)
> - **기준자료 ≠ 참값**: 검조소·GLORYS·고도계 L4·기준 조석모델(FES/TPXO/GOT/EOT)은 "정답"이 아니라 **reference**다. 그림 제목·축라벨·범례에 "truth/정답"이라 쓰지 말고 "model − reference"로 표기한다.
> - **datum/기준면 정합이 첫 단추**: 수직기준(상대해면 vs 절대해면/지오이드), 평균·계절·교점주기 제거 기준, 시간기준(UTC), 보정 상태(조석·DAC·VLM)가 양쪽에서 같지 않으면 **모든 그림이 가짜 bias를 만든다**. 각 카드 「함정」 참조.
> - **임계값은 advisory**: "복소차 5 cm 이하면 우수" 같은 색구간·임계선은 **분조·해역·깊이·기준자료 의존**이다. 색맵 구간은 참고이지 합격선이 아니다.
> - **단일 그림 금지**: 진폭만, 또는 peak만 보면 오독한다. 한 현상에 대해 (정확도 + 편향 + 패턴/위상) 3축 그림을 함께 본다.

---

## 그림 카드 형식 (8항목 — 메서드 카드와 통일, 국문 / English 병기)

각 카드: **무엇을 보여주나 · 읽는 법 · 언제 쓰나 · 짝지표 & 교차링크 · 만드는 법 · 함정·주의 · 출처**. (제목에 8번째로 그림명 자체 포함)

---

### 1. 분조별 진폭·지각 비교 막대 (Per-Constituent Amplitude & Phase Bar Chart, ΔH·ΔG)

- **무엇을 보여주나**: 주요 분조(M2, S2, N2, K2, K1, O1, P1, Q1, 천해분조 M4·MS4 등)별로 모델 진폭 H와 관측(검조소/altimetry) 진폭 H를 막대 쌍(grouped bar)으로, 그 위(또는 별도 패널)에 지각 G를 점/막대로 나란히 표시. 보조 패널에 진폭오차 ΔH = H_m − H_o, 지각오차 ΔG = wrap(G_m − G_o)를 막대로.
- **읽는 법**: x축=분조명(에너지 큰 순 정렬), 좌 y축=진폭(cm), 우 y축 또는 하단 패널=지각(°). 모델·관측 막대 높이가 비슷하고 ΔH≈0, ΔG≈0이면 양호. **나쁜 패턴**: M2 진폭만 크게 어긋남(천해 마찰·수심 오류), 모든 분조 지각이 한쪽으로 치우침(시간기준·경도보정 불일치 의심 → 함정), 작은 분조에서 ΔG가 요동(진폭 작아 위상 무의미).
- **언제 쓰나**: 자료형=검조소 1지점 또는 격자점 1점의 조화상수. 검증목적=조석 에너지/위상 재현을 분조 단위로 진단(어느 분조가 문제인지 분해).
- **짝지표 & 교차링크**: ΔH·ΔG → [11 「분조별 진폭 오차」「분조별 지각 오차」]. 1° ≈ 주기/360 의 시간환산(M2 12.42h → 1°≈2.07분) 병기. 진폭+지각 통합은 카드 #3(복소차). 다지점 종합은 #4(RSS).
- **만드는 법**: `utide.solve()`로 (H,G) 추정 → `matplotlib` `ax.bar(x-w/2, Hm); ax.bar(x+w/2, Ho)`, 지각은 `ax.errorbar`/하단 `bar`. 신뢰구간은 utide의 `coef.diff_conf`(또는 부트스트랩)로 errorbar. 분조 정렬·라벨은 utide `coef.name`, `coef.A`, `coef.g`.
- **함정·주의**: 지각은 **동일 기준**(Greenwich phase, 동일 시간기준·교점보정)이어야 비교 가능 — 한쪽이 지방시(local)·다른 쪽이 Greenwich면 전 분조가 일정 offset만큼 어긋나 보인다(가짜 ΔG). 작은 진폭 분조의 ΔG는 SNR로 걸러 회색 처리. 단위(cm vs m) 통일.
- **출처**: Pawlowicz, Beardsley & Lentz (2002), *Computers & Geosciences* 28, 929–937 (T_TIDE, 신뢰구간). Codiga (2011) UTide. Python 구현: `utide` 패키지(`utide.solve`/`utide.reconstruct`, Codiga UTide의 Python 이식; PyPI `pip install utide`). Pugh & Woodworth (2014) *Sea-Level Science*.

---

### 2. 조화상수 페이저(극좌표) 비교 (Tidal Constituent Phasor / Polar Diagram)

- **무엇을 보여주나**: 한 분조의 조화상수를 극좌표에서 벡터(phasor)로 표현 — 반지름=진폭 H, 각도=지각 G. 모델 벡터와 관측 벡터를 같은 극좌표에 겹쳐 그려, 둘의 길이차(=진폭오차)와 사잇각(=지각오차)을 **한 그림에서 동시에** 본다. 여러 분조를 색으로 구분하거나 분조별 소형 다중패널(small multiples).
- **읽는 법**: 두 화살표가 거의 포개지면 양호. **길이 다름**=진폭오차, **벌어진 각**=지각오차, **화살표 끝 사이 거리**=복소차 D(카드 #3로 연결). 시계방향/반시계 각도 규약(천문 위상 증가 방향)을 캡션에 명시.
- **언제 쓰나**: 자료형=검조소/격자점/altimetry 조화상수. 검증목적=진폭·위상을 분리하지 않고 **벡터 기하로 직관 파악**. 발표·보고용 정성 그림으로 강력.
- **짝지표 & 교차링크**: 진폭·지각 동시 → [11 「복소/벡터 차이 D」]. 정량 막대는 #1, 다지점 종합은 #4. 조류(유속) 벡터상관과 형제 개념 → [10 벡터/복소상관].
- **만드는 법**: `matplotlib` `fig.add_subplot(projection='polar')`, `ax.annotate('', xy=(np.deg2rad(G), H), xytext=(0,0), arrowprops=...)` 또는 `ax.quiver`(극좌표). 각도 방향·0° 위치는 `ax.set_theta_direction(-1)`, `ax.set_theta_zero_location('N')`로 규약 고정.
- **함정·주의**: 각도 0°·증가방향 규약을 모델·관측이 동일하게 써야 한다(천문 위상 V0+u 기준 불일치 시 회전 offset). 진폭이 매우 작은 분조는 각도 추정이 불안정해 화살표 방향이 무의미 — 길이 임계 이하는 흐리게.
- **출처**: Pugh & Woodworth (2014) *Sea-Level Science* (조화상수 벡터 표현). Foreman (1977/2004) 조화분석. `utide`/`matplotlib` polar 구현.

---

### 3. 조화상수 복소차 벡터 다이어그램 (Complex/Vector Amplitude Difference, D)

- **무엇을 보여주나**: 분조를 복소수 Z = H·e^{iG}로 놓고, 복소평면(가로=in-phase 성분 H cosG, 세로=quadrature 성분 H sinG)에 모델점 Z_m·관측점 Z_o를 찍고 **둘을 잇는 벡터 D = Z_m − Z_o**를 그린다. 다지점이면 각 검조소의 D 벡터를 지도 위 화살표(quiver)로 뿌려 공간분포를 본다.
- **읽는 법**: D 벡터가 짧을수록 양호(진폭+지각 통합오차). 벡터 방향이 **방사 방향(원점-점 방향)**이면 주로 진폭오차, **접선 방향**이면 주로 지각오차. 지도형에서 화살표가 특정 해역(예 대륙붕단·만 입구)에 길게 정렬되면 그 지역 조석물리(공진·마찰) 재현 결함.
- **언제 쓰나**: 자료형=다지점 조화상수(검조소망/altimetry/격자). 검증목적=조석검증의 **사실상 표준 단일지표**를 시각화하고 공간 구조를 진단.
- **짝지표 & 교차링크**: D = √(C²+S²), C=H_m cosG_m − H_o cosG_o, S=H_m sinG_m − H_o sinG_o → [11 「복소/벡터 차이 D」]. 분조 RMS=D/√2, 종합 RSS=√(½ΣD_k²) → 카드 #4. 심해 M2 D_rms 약 2–5 cm가 현대 "우수" 영역(Stammer et al. 2014).
- **만드는 법**: `numpy`로 `Zm=Hm*np.exp(1j*np.deg2rad(Gm))`; `D=np.abs(Zm-Zo)`. 복소평면 산점: `ax.scatter(Zm.real, Zm.imag)` + `ax.annotate`로 D 벡터. 지도형: `cartopy` + `ax.quiver(lon, lat, (Zm-Zo).real, (Zm-Zo).imag)`. 색=|D|는 `cmocean.cm.amp`(순차).
- **함정·주의**: 관측 조화상수 자체의 불확실성(짧은 기록·QC 미흡)이 D에 섞인다 — 관측 record 길이·SNR로 가중·필터. **D는 분조별 값** — 여러 분조를 한 점에 합치려면 RSS(#4). C/S 정의의 √2 정규화 여부를 캡션에 명시(문헌 혼용).
- **출처**: Stammer, D., et al. (2014). Accuracy assessment of global barotropic ocean tide models. *Reviews of Geophysics*, 52, 243–282. doi:10.1002/2014RG000450 (D_rms 정의, 심해/대륙붕/연안 RSS ≈ 0.9/5.0/6.5 cm). Andersen/Egbert/Ray 계열 GOT/FES/TPXO 평가 관행.

---

### 4. 분조별·종합 복소 RMS 막대 (깊이/해역 층화) (Per-Constituent & Total RMS Bar, Stratified by Depth/Region)

- **무엇을 보여주나**: 분조별 복소 RMS(=D/√2)를 막대로, 맨 오른쪽에 **다분조 종합 RSS**(root-sum-square) 막대를 추가. 여러 모델(FES/TPXO/GOT/EOT/우리모델)을 색으로 묶고, 패널을 **깊이대(원양 pelagic >1000 m / 대륙붕 shelf / 연안 coastal)** 또는 해역별로 나눠 층화 비교.
- **읽는 법**: 막대가 낮을수록 양호. M2가 보통 가장 큰 기여 → M2 막대가 모델 순위를 좌우. **층화의 핵심**: 같은 모델도 원양에선 수 cm, 연안에선 10 cm+로 커진다 — 깊이대를 섞으면 순위가 왜곡되므로 반드시 분리. 종합 RSS 막대로 모델 랭킹.
- **언제 쓰나**: 자료형=다지점 조화상수(검조소·altimetry). 검증목적=모델 상호비교·랭킹, 어느 분조·어느 해역이 약한지 진단.
- **짝지표 & 교차링크**: 분조 RMS, 종합 RSS → [11 「분조별 RMS」「다분조 종합 RMS/RSS」]. 모델 다수 비교의 유의성은 [13 Diebold-Mariano / bootstrap CI], 종합요약은 [공통편 테일러](#)와 병용(단 조화상수엔 테일러 부적합 — 11 주석 참조).
- **만드는 법**: 분조별 D 계산 후 `Drms=D/np.sqrt(2)`, `RSS=np.sqrt(0.5*np.sum(D**2))`. `matplotlib` grouped/stacked `bar`, 깊이대별 `plt.subplots(1,3)`. 검조소 깊이/연안거리로 `xarray`/`pandas` groupby 층화.
- **함정·주의**: 분조 집합·정규화·검조소 표본이 다르면 모델 간 공정비교 불가 — **동일 프로토콜**(같은 분조·같은 지점·같은 깊이대 정의)을 강제. 천해 비선형분조(M4 등)를 빼면 연안 오차를 과소평가. 약어 RSS(root-sum-square)와 잔차제곱합(residual sum of squares)을 혼동 말 것.
- **출처**: Stammer et al. (2014), *Reviews of Geophysics* 52, 243–282 (깊이대별 RSS 기준선 0.9/5.0/6.5 cm, 10개 분조). Lee et al. (2025) *J. Marine Sci. Eng.* 13(3):395, doi:10.3390/jmse13030395 (동중국해 EOT20 RSS≈11.1 cm 사례). Ray (2013) GOT 평가.

---

### 5. 등조시·등진폭선도(코타이달 차트)와 차이지도 (Cotidal / Corange Chart + Difference Map)

- **무엇을 보여주나**: 한 분조(주로 M2)의 격자 조석장을 **등진폭선(corange, 등H 컨투어)**과 **등조시선(cotidal, 등G 컨투어)**으로 그린 지도. 무조점(amphidromic point, H→0이고 등조시선이 회전중심으로 수렴)이 보인다. 모델·기준 조석모델을 나란히, 그리고 **복소차 |Z_m−Z_o| 차이지도**를 세 번째 패널로.
- **읽는 법**: 무조점 위치·등조시선 회전(북반구 보통 반시계)·진폭 띠 위치가 기준과 일치하면 양호. **나쁜 패턴**: 무조점이 수십~수백 km 어긋남(천해 수심·마찰·경계 오류), 차이지도에서 대륙붕·만 입구·반폐쇄해에 큰 |D| 핫스폿. 색구간은 advisory.
- **언제 쓰나**: 자료형=격자 조화상수(모델 vs FES/TPXO/GOT/EOT). 검증목적=조석장의 **공간 패턴·무조계(amphidromic system)** 재현을 한눈에. 해수면·조석 고유 그림(공통편 일반 오차장 지도와 구분).
- **짝지표 & 교차링크**: 복소차 지도 → 카드 #3, [11 「복소/벡터 차이 D」]. 공간장 패턴 검증 일반론은 [02 패턴상관/거리측도]와 연계하되 조석 위상장은 **각도 wrapping** 처리 필요. 무조점 인근은 진폭 0 → ΔG 무의미(가중 제외).
- **만드는 법**: `xarray`로 격자 (H,G) 적재. 진폭: `ax.contourf(lon,lat,H, cmap=cmocean.cm.amp)`; 위상(원형): `ax.contour(lon,lat,G, levels=range(0,360,30))` — 위상은 `cmocean.cm.phase`(순환 색맵). 차이지도: `ax.pcolormesh(..., cmap=cmocean.cm.balance)`(발산, 0 중심). 지도는 `cartopy`. 위상 등고선은 0/360 불연속 처리(`np.ma` 또는 cos/sin 보간).
- **함정·주의**: **위상은 순환량** — 359°와 1°를 선형 평균/보간하면 가짜 무조점이 생긴다. 반드시 복소(cos/sin)로 보간 후 위상 복원. 무조점 근처는 진폭이 0에 가까워 위상 잡음이 폭발 — 진폭 임계 이하 위상은 마스킹. 모델·기준의 위상기준(Greenwich) 통일.
- **출처**: Pugh & Woodworth (2014) *Sea-Level Science* (코타이달·무조점). Stammer et al. (2014), *Rev. Geophys.* 52 (글로벌 조석모델 비교). 색맵: Thyng, K.M., et al. (2016) "True colors of oceanography: Guidelines for effective and accurate colormap selection", *Oceanography* 29(3), 9–13 (`cmocean`, phase는 순환 색맵). **논문 그림 복제 금지 — 유형·사양만 참고.**

---

### 6. 조위 시계열 오버레이 + 비조석 잔차 시계열 (Water-Level Overlay + Non-Tidal Residual Time Series)

- **무엇을 보여주나**: 상단 패널=관측 총수위·모델 총수위·조석예측(harmonic prediction)을 같은 시간축에 겹쳐 그림. 하단 패널=**비조석 잔차(non-tidal residual) = 총수위 − 조석예측**을 모델·관측 각각 그려, 해일·기압·계절 성분의 일치를 본다.
- **읽는 법**: 상단에서 조석 위상·진폭이 맞물리면 양호. 하단 잔차가 모델·관측이 함께 솟고(폭풍 이벤트) 평상시 0 부근이면 양호. **나쁜 패턴**: 잔차에 **조석 주기 진동이 남음**(조화분석 위상 작은 오차, 조석-해일 비선형 상호작용 → 인공 첨두 artificial peak), 잔차 평균이 0이 아님(datum/평균제거 불일치).
- **언제 쓰나**: 자료형=검조소·모델 수위 시계열(시간별). 검증목적=조석 제거 품질 확인 + 폭풍해일/계절 해면의 출발점 진단.
- **짝지표 & 교차링크**: 잔차 RMSE·상관·편향 → [11 「조위편차·잔차 분석」]. 잔차의 인공첨두 문제 회피책은 스큐서지(카드 #7). 잔차 시계열의 추세·변화점은 [06 시계열·신호]. 시계열 종합비교는 [공통편 테일러 다이어그램](#).
- **만드는 법**: `utide.solve()` → `utide.reconstruct(time, coef)`로 조석예측 → `residual = obs − pred`. `matplotlib` `fig, (ax1,ax2)=plt.subplots(2,1, sharex=True)`. 시간축 `pandas`/`numpy datetime64`. 결측은 마스킹(선으로 잇지 말 것).
- **함정·주의**: 관측 총수위엔 비조석 성분이 섞여 있어 "조석 RMS"와 "총수위 RMS"가 다르다 — 비교 대상(조석만 vs 전체)을 캡션에 명확히. **datum·시간(UTC) 정렬**이 안 되면 상단 오버레이가 통째로 밀려 거대한 가짜 위상오차로 보인다. 잔차 평균이 0이 아니면 평균해수면 기준 불일치 의심.
- **출처**: Pugh & Woodworth (2014) *Sea-Level Science*. Williams, Horsburgh et al. (2016), *GRL* 43, 6410–6417, doi:10.1002/2016GL069522 (잔차의 위상의존 문제 → skew surge). Codiga (2011) UTide; Python `utide`.

---

### 7. 스큐서지 산점도·시계열·Q-Q (Skew Surge: Model vs Observed Scatter / Time Series / Q-Q)

- **무엇을 보여주나**: 각 조석주기의 **스큐서지 = (관측 한 주기 최고수위) − (그 주기 예측 천문 고조위)**를 계산해, (a) 모델 skew surge vs 관측 skew surge 산점도(1:1선), (b) 사건 시계열(이벤트별 막대/점), (c) 꼬리 비교 Q-Q를 한 세트로.
- **읽는 법**: 산점이 1:1선에 모이고 상관 높으면 양호. **나쁜 패턴**: 큰 스큐서지(폭풍)에서 모델이 1:1선 아래로(피크 과소예측 — 경보에 치명적), Q-Q 꼬리가 휘면 극단 사건 분포 불일치. 잔차기반 결과와 거의 동등하면서 위상오차 영향이 작은 것이 스큐서지의 장점.
- **언제 쓰나**: 자료형=검조소·모델 수위(반일주조 우세 해역에서 특히 유효). 검증목적=폭풍해일 모델의 위상독립 검증, 극치분석 입력.
- **짝지표 & 교차링크**: skew surge RMSE·상관·QQ → [11 「스큐서지」]. 잔차(비조석)와의 대비는 카드 #6. 스큐서지 분포는 극치(카드 #13)·SSJPM 입력. 1:1 산점·Q-Q의 일반형은 [공통편].
- **만드는 법**: 천문조 예측(`utide.reconstruct`)에서 조석주기별 고조(시각·값) 검출(`scipy.signal.find_peaks`), 같은 주기 관측 최고수위와 차감. `matplotlib` `ax.scatter` + 1:1선; Q-Q는 `scipy.stats.probplot` 또는 분위수 직접 계산.
- **함정·주의**: **일주조 우세·복잡 조석 해역**에서는 "한 조석주기 최대" 정의가 모호 — 적용 전 form factor(카드 #14 보조)로 해역 유형 확인. 조석-해일 상호작용이 강하면 스큐서지도 잔여 편향. 고조 검출 임계·창 크기가 결과에 영향.
- **출처**: Williams, J., Horsburgh, K.J., et al. (2016) "Tide and skew surge independence: New insights for flood risk", *Geophysical Research Letters* 43, 6410–6417. doi:10.1002/2016GL069522. Comparison between skew surge and residual water level along the coastline of China (2021), *J. Hydrology*. Pugh & Woodworth (2014).

---

### 8. 폭풍해일 사건 비교 — peak/timing 산점 + 고분위·POT (Storm Surge Event: Peak/Timing Scatter + 99th-Percentile / POT)

- **무엇을 보여주나**: (a) 사건별 **모델 피크수위 vs 관측 피크수위 산점도**(1:1선, 색=피크 시각 오차 timing error), (b) **타이밍 오차 히스토그램/막대**, (c) **초과 임계(99퍼센타일 또는 POT) 진단**: 관측-모델 분위수 비교와 고분위 표본의 bias/RMSE. 선택적으로 사건 분할표(POD/FAR/CSI) 텍스트박스.
- **읽는 법**: 피크 산점이 1:1선에 모이고 timing이 0 근처면 양호. **나쁜 패턴**: 큰 사건일수록 1:1선 아래(피크 과소예측), timing 분포가 양/음으로 치우침(해일 도달 지연/선행), 99p 초과 표본에서 음의 bias(극값 과소). ERA5 강제 모델은 극값을 과소예측하는 경향 보고 — 강제자료 출처를 캡션에.
- **언제 쓰나**: 자료형=검조소·모델 해일/총수위 시계열. 검증목적=연안 침수·경보 검증(평균 RMSE만으로 부족, 고분위·피크·타이밍을 별도 보고).
- **짝지표 & 교차링크**: peak error·timing error·99p RMSE·POD/FAR/CSI → [11 「폭풍해일 검증 지표」]. 사건 분할표·드문사건 지표는 [03 범주형·사건]. 극치 재현빈도는 카드 #13. 잔차/스큐서지는 #6·#7.
- **만드는 법**: 사건 검출 후 `scipy.signal.find_peaks`로 모델·관측 피크 매칭(시간창). `numpy.percentile`로 99p, POT는 임계 초과 표본. `matplotlib` `ax.scatter(obs_peak, mod_peak, c=timing_err, cmap=cmocean.cm.balance)` + `colorbar`. 분할표는 `pandas` 교차표.
- **함정·주의**: **단일 지표로 해일성능을 못 잡는다** — 평균·고분위·피크·타이밍·이벤트 점수를 조합. 임계(절대 vs 분위) 선택이 점수를 좌우 → 임계를 캡션에 고정·명시. 사건 매칭 시간창이 좁으면 미스, 넓으면 오매칭. datum·시간 정렬 필수.
- **출처**: Campos-Caba, R., et al. (2024) "Assessing storm surge model performance...", *Ocean Science* 20, 1513–1535, doi:10.5194/os-20-1513-2024. Muis, S., et al. (2016) "A global reanalysis of storm surges and extreme sea levels", *Nature Communications* 7:11969, doi:10.1038/ncomms11969. Fernández-Montblanc 등 GTSM 검증.

---

### 9. 역기압/DAC 보정 효과 플롯 (Inverse Barometer / DAC Correction Effect: Pressure-Regression Before/After)

- **무엇을 보여주나**: (a) **수위(또는 잔차) vs 평균해면기압(ERA5)** 산점·회귀 — 보정 전후 두 회귀선. 정적 역기압 기대기울기 ≈ −0.9948 cm/hPa. (b) 보정 전후 잔차 분산 막대(분산 감소량), (c) 선택적으로 보정 전후 잔차 PSD에서 기압대역 에너지 감소.
- **읽는 법**: 보정 후 회귀기울기가 0에 가깝고 잔차분산이 줄면 보정 양호. 보정 전 기울기가 ~−1 cm/hPa면 역기압 민감도가 물리적으로 재현된 것. **나쁜 패턴**: 보정 후에도 기울기가 0에서 멀다(동적응답 필요한 천해·만에서 정적 IB가 부적절 → DAC 사용), 고주파(<3일)·고위도에서 IB가 DAC보다 잔차 큼.
- **언제 쓰나**: 자료형=검조소 잔차 + ERA5 MSLP 격자, 또는 고도계 SLA(DAC 적용/미적용), 모델 수위. 검증목적=대기압·바람 강제에 대한 해면 반응 보정의 일관성.
- **짝지표 & 교차링크**: 회귀기울기·분산감소·기압대역 PSD → [11 「역기압효과·동적대기보정 검증」]. 잔차 자체는 카드 #6. 보정 상태 메타데이터 점검은 카드 #15(QC). PSD/coherence는 [05 스펙트럼].
- **만드는 법**: η_IB = −(1/ρg)(P − P̄), `xarray`로 ERA5 MSLP를 검조소 위치 보간(`.interp`)·전지구평균 P̄ 제거. DAC는 AVISO/CMEMS 제공 격자(MOG2D 기반)를 적재. 회귀 `scipy.stats.linregress`; `matplotlib` 산점+회귀선, 분산 막대.
- **함정·주의**: 검조소·고도계·모델 사이 **DAC 적용 여부가 다르면 직접 비교 불가** — 보정 상태를 반드시 메타데이터로 확인(다르면 가짜 bias). 전지구 평균기압 제거를 빠뜨리면 절대 offset. 천해·만은 정적 IB 가정이 깨짐.
- **출처**: Carrère, L., Lyard, F. (2003) "Modeling the barotropic response of the global ocean to atmospheric wind and pressure forcing — comparisons with observations", *Geophysical Research Letters* 30(6), 1275 (MOG2D/DAC). AVISO+/CMEMS Dynamic Atmospheric Correction 처리문서(CLS, LEGOS MOG2D; CNES 지원). Pugh & Woodworth (2014).

---

### 10. SSH/SLA/ADT — 위성 track vs grid + 교차점 차이지도 (Altimetry Along-Track vs Gridded; Crossover Difference Map)

- **무엇을 보여주나**: (a) **along-track SLA**(점선/색점)와 같은 영역 **격자 SLA(DUACS/모델)**를 한 지도에 겹쳐, 트랙을 따라 둘의 차이를 색으로. (b) **교차점(crossover) 차이지도**: 상승·하강 궤도 교차점에서 ΔSLA = SLA_asc − SLA_desc(시간차 보정)를 점 색으로 뿌려 궤도오차·내부일관성 진단. (c) 선택: 트랙 SLA의 파수스펙트럼(유효해상도).
- **읽는 법**: 트랙-격자 차이가 작고 무작위면 양호. 교차점 ΔSLA의 RMS/분산이 작을수록 자료 일관성 양호. **나쁜 패턴**: 연안 접근 시 트랙-격자 차이 급증(육지오염·궤도오차 — X-TRACK 연안 재처리 필요), 교차점차에 조석주기 잔여(조석모델 결함 → 카드 #11 aliasing), 특정 트랙따라 계통적 offset(궤도오차).
- **언제 쓰나**: 자료형=고도계 along-track + 격자 SLA(NetCDF), 모델 SSH. 검증목적=위성 SLA 내부 일관성·격자화 산물 품질·모델 SSH의 위성 대비 검증.
- **짝지표 & 교차링크**: 교차점차 RMS, track-vs-grid RMSE → [11 「위성고도계 SLA 검증」「교차점 분석」]. 검조소 대조(zone of influence)도 11. 위성 일반 track-vs-grid·파수스펙은 [12 위성]. 조석 잔여는 카드 #11.
- **만드는 법**: `xarray`로 along-track·격자 SLA 적재, 격자를 트랙점에 `.interp`. 교차점 검출은 궤도 기하 교차(상승/하강) 계산 후 시간차 보정. `cartopy` 지도 + `ax.scatter(lon,lat,c=dSLA, cmap=cmocean.cm.balance)`(0 중심 발산). 파수스펙은 `scipy.signal`/`numpy.fft`.
- **함정·주의**: 교차점 **시간차 동안의 실제 해면변동**이 오차로 흡수될 수 있어 작은 Δt 교차점을 선택. **조석·DAC 보정 상태가 트랙·격자·모델에서 동일**해야 비교 가능(불일치 시 가짜 차이). 연안은 교차점·트랙 자료 모두 희소·저품질.
- **출처**: AVISO/CMEMS DUACS 처리문서·QUID(crossover adjustment). Mitchum (1998/2000) 고도계 안정성 검조소 모니터링, *J. Atmos. Oceanic Technol.* Oelsmann et al. (2021) "The zone of influence", *Ocean Science* 17, 35–57. Zhu, Peng & Shen (2025) SWOT SLA 검증, *Water* 17(21):3066, doi:10.3390/w17213066.

---

### 11. 고도계 조석 에일리어싱 스펙트럼 점검 (Tidal Aliasing Spectrum Check)

- **무엇을 보여주나**: 고도계 SLA(또는 조석제거 후 잔차) 시계열의 파워스펙트럼에 **분조의 에일리어싱 주파수**(샘플링 f_s로 접힌 f_alias = |f_tide − n·f_s|; 예 Jason 9.9156일 반복에서 M2·S2·K1이 특정 저주파로 접힘)를 수직 표식으로 표시해, 그 대역에 잔여 에너지 첨두가 솟는지 본다. 모델/기준 조석모델 제거 전후를 겹쳐.
- **읽는 법**: 에일리어싱 주파수에서 잔여 첨두가 작을수록 조석제거 양호. **나쁜 패턴**: M2/S2 에일리어싱 대역에 뚜렷한 라인(조석모델 결함, 특히 연안·천해), 중규모(mesoscale) SLA 지도에 줄무늬 잡음. 조석제거 후 첨두가 줄면 보정 효과 확인.
- **언제 쓰나**: 자료형=고도계 SLA along-track/격자, 조석제거 잔차. 검증목적=조석모델 제거 품질·중규모 해면 분석 신뢰성.
- **짝지표 & 교차링크**: 에일리어싱 대역 잔여 에너지 → [11 「조석 에일리어싱 점검」]. 스펙트럼·코히어런스 일반론은 [05 스펙트럼]·[11 「스펙트럼·코히어런스」]. 교차점 잔여 조석은 카드 #10.
- **만드는 법**: 미션 반복주기로 f_alias 계산(분조 주파수표 + 샘플링). `scipy.signal.welch`(불규칙·결측 시 `astropy.timeseries.LombScargle`). `matplotlib` 로그-로그 PSD + `ax.axvline(f_alias)` 분조 표식. 조석제거 전후 두 곡선.
- **함정·주의**: 분석 윈도가 에일리어싱 주기보다 짧으면 분리 불가. **연안·천해는 조석모델 정확도가 낮아** 에일리어싱 잔차가 본질적으로 큼(모델 결함과 혼동 주의). 비정상(계절·해면상승) 신호는 사전 제거.
- **출처**: "Aliased Tidal Variability in Mesoscale Sea Level Anomaly Maps", *J. Atmos. Oceanic Technol.* (PMC6999748). "Residual M2 and S2 ocean tide signals in complex coastal zones identified by X-Track reprocessed altimetry data" (2023), *Continental Shelf Research*. Ray & Zaron 에일리어싱/내부조석 연구.

---

### 12. 평균해수면 추세 시계열 + VLM/GIA 보정 (MSL Trend Time Series with VLM/GIA Correction)

- **무엇을 보여주나**: 월평균 MSL 시계열(검조소 상대해면, 고도계 GMSL, 모델)에 선형(또는 가속 포함) 회귀선과 신뢰구간(자기상관 보정). 검조소는 **VLM(GNSS) 또는 GIA 모델 보정**으로 절대해면 환산한 곡선을 함께. 추세값(mm/yr)과 불확실성을 범례에.
- **읽는 법**: 보정 후 검조소 절대해면 추세가 고도계·모델과 통계적으로 구분 불가하면 일관성 양호. **나쁜 패턴**: VLM 미보정 검조소(상대해면)를 고도계(절대해면)와 직접 비교(지반운동만큼 가짜 차이), 신뢰구간을 자기상관 무시로 과소 추정. 기간을 바꾸면 추세가 달라짐(짧은 기록 주의).
- **언제 쓰나**: 자료형=검조소 월평균(PSMSL), 고도계 GMSL, 모델 해면. 검증목적=장기 해면변화·해면상승 일관성 검증.
- **짝지표 & 교차링크**: 추세 b(mm/yr)·CI → [11 「평균해수면 추세와 VLM·GIA 보정」]. 계절(Sa/Ssa) 제거는 [11 「계절해면 주기」]. 추세·변화점 일반론은 [06]. 성분 분해는 카드 #13(수지).
- **만드는 법**: 계절·교점주기 제거 후 `scipy.stats.linregress` 또는 `statsmodels` OLS(+자기상관 보정 표준오차, Newey-West). VLM은 GNSS 속도/GIA 모델(ICE-6G) 적용. `matplotlib` 시계열+회귀선+`fill_between` CI.
- **함정·주의**: 검조소는 **상대해면(지반운동 포함)** — VLM 미보정 시 절대해면과 직접 비교 불가. GIA 모델 간 차이가 추세 불확실성에 기여. GNSS-VLM은 5–20년이라 장기 외삽 가정 주의. 자기상관 미보정 표준오차는 과소. 추세 수치는 **분석기간을 항상 명시**(20세기 ~1.7–1.8 mm/yr, 1993~ 고도계 GMSL ~3.3 mm/yr+가속은 기간 의존).
- **출처**: NOAA CO-OPS Sea Level Trends 방법론. Nerem, R.S., et al. (2018) "Climate-change–driven accelerated sea-level rise detected in the altimeter era", *PNAS* 115, 2022–2025. Peltier et al. (2015) ICE-6G(VM5a) GIA. Prandi et al. (2021) 지역해면 추세·불확실성, *Sci. Rep.* PSMSL 데이터 가이드.

---

### 13. 극치해면 재현수위 곡선 (Extreme Sea Level Return-Level Plot: GEV/Gumbel, POT/GPD, JPM)

- **무엇을 보여주나**: x축=재현기간 T(log scale, 2·5·10·50·100·…년), y축=재현수위(m). 모델·관측 각각의 적합곡선(연최대 GEV/Gumbel 또는 POT/GPD)과 신뢰구간 띠, 경험분위수 점(플로팅 포지션)을 겹쳐. 선택: JPM/SSJPM(조석⊛해일 합성) 곡선을 직접 추정과 비교.
- **읽는 법**: 모델·관측 곡선과 CI 띠가 겹치면 일치. 경험점이 곡선 위에 잘 놓이면 적합 양호. **나쁜 패턴**: 100년 빈도에서 CI 띠가 매우 넓음(연최대는 표본 적어 외삽 불확실 → POT 권장), 모델이 관측 아래로(극값 과소), 비정상성(해면상승) 무시로 과소추정, 곡선이 경험 꼬리에서 벗어남(분포·임계 부적절).
- **언제 쓰나**: 자료형=검조소·모델 연최대 또는 임계초과 수위. 검증목적=설계해면·연안침수 재현빈도 추정과 모델-관측 비교.
- **짝지표 & 교차링크**: GEV/Gumbel·POT/GPD·JPM 재현수위·CI → [11 「극치 재현빈도 GEV/Gumbel」「POT/GPD」「결합확률법 JPM」]. 극값 일반엔진은 [03 GEV/POT/return level]. 입력은 스큐서지(#7). QQ/적합도는 [공통편].
- **만드는 법**: GEV `scipy.stats.genextreme.fit`(연최대), GPD `scipy.stats.genpareto`(POT, declustering 후), 또는 전용 `pyextremes`. CI는 프로파일우도/부트스트랩. `matplotlib` `ax.set_xscale('log')`, 재현수위 z_T=1−1/T 분위수 + 경험점 `(plotting position)`.
- **함정·주의**: 연최대는 표본 적어 외삽 신뢰구간이 넓다(POT가 대안). **임계·declustering 선택이 결과를 좌우**(주관성) — 평균초과도표·모수안정도표로 정당화. 조석-해일 의존을 무시하면 동시극치 과소 → JPM은 copula로 의존 반영. 해면상승·비정상성 반영(비정상 GEV).
- **출처**: Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer. Davison & Smith (1990) "Models for exceedances over high thresholds", *J. R. Statist. Soc. B* 52, 393–442. Arns et al. (2013) *Coastal Engineering* 81, 51–66. Batstone et al. (2013) Skew Surge JPM, *Ocean Engineering* 71, 28–39. Pugh & Vassie (1980) JPM. Menéndez & Woodworth (2010), *JGR Oceans* 115, C10011.

---

### 14. 조석 기준면 사다리 다이어그램 (Tidal Datum Ladder: MHHW/MHW/MSL/MLW/MLLW/LAT)

- **무엇을 보여주나**: 수직축에 조석 기준면을 사다리(수평선)로 — HAT/MHHW/MHW/MTL/MSL/MLW/MLLW/LAT(약최저저조위·해도기준면) — 모델 산출 datum과 공식 검조소 datum을 **두 열로 나란히** 그려 각 면의 차이(cm)를 표시. 대조차(MHW−MLW)·평균해면 위치를 한눈에. 보조: 형태계수 F로 해역 유형 라벨.
- **읽는 법**: 같은 datum의 두 열 높이가 일치하면 양호. **나쁜 패턴**: 특정 datum만 계통 차이(분조 진폭 합 근사·19년 epoch 미적용), chart datum 정의 불일치(국가별 LAT vs MLLW vs Z0−Σ amplitudes), 전체가 일정량 평행이동(수직기준 offset).
- **언제 쓰나**: 자료형=검조소 통계·모델 조석예측에서 datum 산출. 검증목적=항해해도·연안공학용 기준면 정합 검증.
- **짝지표 & 교차링크**: datum 차이(cm)·form factor F → [11 「조석 datum 검증」「조석형태계수 F」]. datum 정합은 거의 모든 카드의 전제(특히 #6·#9·#12의 평균기준). datum 안정성 QC는 카드 #15.
- **만드는 법**: 충분히 긴 `utide.reconstruct` 예측에서 고조·저조 검출(`scipy.signal.find_peaks`)→MHW/MLW/MLLW 평균, MTL=(MHW+MLW)/2, LAT=예측 최저치. `matplotlib` `ax.hlines`로 사다리, 두 열 배치, 차이 라벨.
- **함정·주의**: **국가·기관별 datum 정의가 달라** 직접 비교 시 정의 통일 필수(한국 약최저저조위=주요 분조 진폭 합 근사, NOAA=19년 NTDE 평균, IHO chart datum=LAT 권고). 짧은 기록은 19년 epoch로 환산(동시관측 비교법). 수직기준(상대 vs 절대) 일치.
- **출처**: NOAA CO-OPS Tidal Datums (National Tidal Datum Epoch, 19년). IHO Resolution — Chart Datum = Lowest Astronomical Tide. Pugh & Woodworth (2014) *Sea-Level Science*. Defant (1958) 형태계수 4구간 분류; van der Stok (1897) 형태계수 기원.

---

### 15. 검조소 QC 시각화 — 스파이크·datum 점프·버디체크 (Tide-Gauge QC: Spike, Datum Shift, Buddy Check)

- **무엇을 보여주나**: 기준자료(검조소)의 신뢰성 진단 그림 세트 — (a) 원시 시계열에 **스파이크/이상치** 강조(이동중앙값 ±k·MAD 밖 점 표시), (b) **datum 점프/드리프트**: 인접 검조소·고도계·모델과의 잔차 시계열에 변화점(step) 표시, (c) **버디체크(buddy check)**: 인접 관측과의 잔차 산점/상관. 선택: 결측 마스크 막대.
- **읽는 법**: 잔차가 평탄·무드리프트면 datum 안정. **나쁜 패턴**: 잔차에 계단형 점프(센서 교체·datum 이동), 선형 드리프트(기준 침하/장비 노후), 고립 스파이크(전송오류), 인접 검조소와 상관 급락(국지 결함). UHSLC Research-Quality vs Fast-Delivery 등급을 캡션에.
- **언제 쓰나**: 자료형=검조소 시계열(CSV/텍스트). 검증목적=**모든 해수면·조위 검증의 전처리** — 잘못된 기준자료는 모든 그림을 오염시킨다.
- **짝지표 & 교차링크**: spike 임계·datum 안정성·buddy 잔차 → [11 「검조소 자료 품질관리 QC」]. 전처리·정합 일반은 [15 전처리·QC]. datum 정의 정합은 카드 #14. 고도계 기반 datum 점검은 카드 #10과 연계.
- **만드는 법**: 스파이크 `scipy.signal.medfilt`/이동중앙값 + MAD 임계; 변화점 `ruptures`(PELT) 또는 CUSUM; 버디는 인접 검조소 `pandas` 상관/잔차. `matplotlib` 시계열+이상점 `scatter`, 변화점 `axvline`, 잔차 산점.
- **함정·주의**: **과도한 자동제거는 진짜 극치(해일 피크)를 깎을 위험** — 물리적으로 불가능한 값만 제거하고 극값은 보존. 실시간 자료(IOC SLMF 등)는 무검수일 수 있어 검증 기준 사용 전 QC 필수. datum 메타데이터(센서 교체·벤치마크 수준측량 이력) 확인.
- **출처**: IOC/UNESCO (2020) "Quality Control of in situ Sea Level Observations" (IOC Manuals and Guides 83). UHSLC 데이터 품질등급(Research-Quality vs Fast-Delivery). PSMSL/GLOSS 가이드. "Offsets in tide-gauge reference levels detected by satellite altimetry" 사례.

---

### (보조) 16. 해수면수지 분해 시계열 (Sea Level Budget: Steric/Manometric Stacked Decomposition)

- **무엇을 보여주나**: 총해면(고도계 GMSL/지역 SLA)을 **스테릭(steric, Argo 열·염팽창)**과 **질량(manometric/barystatic, GRACE 해양질량)** 성분으로 분해해 누적 막대/스택 영역으로, 위에 "스테릭+질량" 합과 총해면을 겹쳐 **폐합잔차**를 본다. 추세(mm/yr)·시계열·공간패턴 패널.
- **읽는 법**: 총해면 ≈ 스테릭 + 질량(폐합잔차 작음)이면 물리정합 양호. **나쁜 패턴**: 모델이 총해면을 맞춰도 성분 비율이 틀림(물리과정 오류 신호), 지역(예 북대서양)에서 큰 잔차(운동·재분배·깊은바다 누락), GRACE GIA 보정 누락.
- **언제 쓰나**: 자료형=고도계 GMSL/SLA, Argo 스테릭, GRACE 질량, 모델 성분출력. 검증목적=해면변화의 물리적 정합성(성분별) 검증.
- **짝지표 & 교차링크**: 폐합잔차·성분 추세 → [11 「해수면수지 폐합 — 스테릭·질량 분해」]. 총추세는 카드 #12. 보존·수지 일반은 [04 보존·수지].
- **만드는 법**: `xarray`로 GMSL·steric·mass 적재, 동일 기간·기준면·적분깊이(Argo 보통 2000 m) 정렬, GIA 보정. `matplotlib` `stackplot`/`fill_between` + 총해면 선 + 잔차 패널.
- **함정·주의**: 깊은바다(>2000 m) 스테릭 누락, GRACE 신호누설·GIA 불확실성, **지역폐합은 운동·재분배로 어렵다**. 모델 검증엔 성분별 출력이 있어야 적용. 기준면·기간·적분깊이를 캡션에 명시.
- **출처**: Leuliette, E.W., Miller, L. (2009) "Closing the sea level rise budget with altimetry, Argo, and GRACE", *Geophysical Research Letters* 36, L04608. WCRP Global Sea Level Budget Group (2018), *Earth Syst. Sci. Data* 10, 1551–1590. AVISO Global Mean Sea Level Budget 자료.

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 11 교차링크

| # | 그림 (국문 / English) | 검증목적 | 짝지표(수치) | 11 메서드 카드 교차링크 |
|---|---|---|---|---|
| 1 | 분조별 진폭·지각 막대 / Amp & Phase Bar | 분조별 에너지·위상 진단 | ΔH, ΔG(시간환산) | 진폭 오차 ΔH · 지각 오차 ΔG |
| 2 | 조화상수 페이저 극좌표 / Phasor Polar | 진폭+위상 벡터 직관 | H, G, 사잇각 | 복소/벡터 차이 D |
| 3 | 복소차 벡터 / Complex Difference D | 조석 통합오차·공간구조 | D=√(C²+S²) | 복소/벡터 차이 D |
| 4 | 분조·종합 RMS 막대(층화) / RMS & RSS Bar | 모델 랭킹·해역 약점 | D/√2, RSS=√(½ΣD²) | 분조별 RMS · 다분조 RSS |
| 5 | 코타이달 차트+차이지도 / Cotidal Chart | 무조계·조석장 패턴 | 무조점 위치, \|D\| 지도 | 복소차 D (+02 패턴) |
| 6 | 조위 오버레이+잔차 / Overlay+Residual | 조석제거 품질·비조석 | 잔차 RMSE·상관·bias | 조위편차·잔차 분석 |
| 7 | 스큐서지 산점·QQ / Skew Surge | 위상독립 해일검증 | skew surge RMSE·R·QQ | 스큐서지 |
| 8 | 해일 peak/timing+99p / Surge Event | 피크·타이밍·고분위 | peak err, timing, 99p, POD/FAR | 폭풍해일 검증 지표 |
| 9 | DAC 보정효과 / IB-DAC Effect | 기압응답 보정 일관성 | 회귀기울기(≈−1cm/hPa), 분산감소 | 역기압·DAC 검증 |
| 10 | track vs grid+crossover / Altimetry | 위성 SLA 일관성 | 교차점차 RMS, track-grid RMSE | SLA 검증 · 교차점 분석 |
| 11 | 에일리어싱 스펙트럼 / Aliasing PSD | 조석제거·중규모 잡음 | 에일리어싱대역 잔여에너지 | 조석 에일리어싱 점검 |
| 12 | MSL 추세+VLM/GIA / MSL Trend | 장기 해면변화 일관성 | b(mm/yr)±CI | MSL 추세·VLM/GIA |
| 13 | 재현수위 곡선 / Return-Level | 극치 설계해면 | GEV/GPD/JPM z_T±CI | GEV/Gumbel · POT/GPD · JPM |
| 14 | 조석 datum 사다리 / Datum Ladder | 기준면 정합 | datum 차(cm), F | 조석 datum · 형태계수 F |
| 15 | QC 시각화 / Tide-Gauge QC | 기준자료 신뢰성 | spike, datum step, buddy 잔차 | 검조소 QC |
| 16 | 해수면수지 분해 / Budget Decomp. | 해면변화 물리정합 | 폐합잔차, 성분추세 | 해수면수지 폐합 |

> **사용 원칙(재강조):** 위 그림 중 **하나만으로 결론내지 않는다.** 조석은 (#1/#2 분조진단 + #3/#4 통합오차) 최소 2축, 비조석·해일은 (#6 잔차 + #7 스큐서지 + #8 사건) 조합, 위성·기후는 (#10 일관성 + #12 추세 + #16 수지) 조합을 권한다. 모든 그림은 **datum/보정 정합(§G, #14·#15)**을 통과한 자료에만 적용한다. 색구간·임계선은 **advisory**이며 분조·해역·깊이·기준자료 의존이다.

---

## 출처(References) — 1차 출처 위주

**조화분석·조석상수 도구·평가**
- Pawlowicz, R., Beardsley, B., Lentz, S. (2002). Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE. *Computers & Geosciences*, 28, 929–937.
- Codiga, D.L. (2011). Unified Tidal Analysis and Prediction Using the UTide Matlab Functions. GSO Technical Report 2011-01, Univ. of Rhode Island. (Python 이식: `utide` 패키지 — `utide.solve`/`utide.reconstruct`, PyPI.)
- Foreman, M.G.G. (1977/2004). Manual for Tidal Heights Analysis and Prediction. Institute of Ocean Sciences.
- Stammer, D., et al. (2014). Accuracy assessment of global barotropic ocean tide models. *Reviews of Geophysics*, 52, 243–282. **doi:10.1002/2014RG000450.** (D_rms 정의, 8대 분조 RSS ≈ 0.9/5.0/6.5 cm 원양/대륙붕/연안, 10개 분조 평가 — 본문 확인.)
- Lee et al. (2025). Accuracy Assessment of Ocean Tide Models in the Eastern China Marginal Seas Using Tide Gauge and GPS Data. *J. Marine Science and Engineering*, 13(3):395. **doi:10.3390/jmse13030395.**

**비조석·폭풍해일**
- Williams, J., Horsburgh, K.J., et al. (2016). Tide and skew surge independence: New insights for flood risk. *Geophysical Research Letters*, 43, 6410–6417. **doi:10.1002/2016GL069522.** (skew surge 정의·조석-해일 독립성 — 본문 확인.)
- Campos-Caba, R., et al. (2024). Assessing storm surge model performance: what error indicators can measure the model's skill? *Ocean Science*, 20, 1513–1535. **doi:10.5194/os-20-1513-2024.**
- Muis, S., et al. (2016). A global reanalysis of storm surges and extreme sea levels. *Nature Communications*, 7:11969. **doi:10.1038/ncomms11969.**
- Comparison between the skew surge and residual water level along the coastline of China (2021). *Journal of Hydrology*. (확인요 — 정확한 권·페이지 미열람.)

**역기압·DAC**
- Carrère, L., Lyard, F. (2003). Modeling the barotropic response of the global ocean to atmospheric wind and pressure forcing — comparisons with observations. *Geophysical Research Letters*, 30(6), 1275. (MOG2D / Dynamic Atmospheric Correction.) AVISO+/CMEMS DAC 처리문서(CLS·LEGOS·CNES) — 처리문서는 (확인요).

**위성고도계·재분석**
- Mitchum, G.T. (1998/2000). Monitoring the stability of satellite altimeters with tide gauges. *J. Atmospheric and Oceanic Technology*.
- Oelsmann, J., et al. (2021). The zone of influence... *Ocean Science*, 17, 35–57.
- Zhu, H., Peng, F., Shen, Y. (2025). Validation of Sea Level Anomalies from the SWOT Altimetry Mission... *Water*, 17(21):3066. **doi:10.3390/w17213066.**
- Zaron, E.D. (2019). Baroclinic Tidal Sea Level from Exact-Repeat Mission Altimetry (HRET). *Journal of Physical Oceanography*, 49, 193–210. **doi:10.1175/JPO-D-18-0127.1.** (plane-wave fit — 본문 확인.)
- "Aliased Tidal Variability in Mesoscale Sea Level Anomaly Maps", *J. Atmos. Oceanic Technol.* (PMC6999748). (확인요 — 정확한 권·페이지/연도 미확정.)
- "Residual M2 and S2 ocean tide signals in complex coastal zones identified by X-Track reprocessed altimetry data" (2023). *Continental Shelf Research*. (확인요.)

**추세·수지·극치·datum**
- Nerem, R.S., et al. (2018). Climate-change–driven accelerated sea-level rise detected in the altimeter era. *PNAS*, 115, 2022–2025.
- Leuliette, E.W., Miller, L. (2009). Closing the sea level rise budget with altimetry, Argo, and GRACE. *Geophysical Research Letters*, 36, L04608.
- WCRP Global Sea Level Budget Group (2018). Global sea-level budget 1993–present. *Earth System Science Data*, 10, 1551–1590.
- Peltier, W.R., Argus, D.F., Drummond, R. (2015). ICE-6G(VM5a) Glacial Isostatic Adjustment. *JGR Solid Earth*.
- Prandi, P., et al. (2021). Local sea level trends, accelerations and uncertainties over 1993–2019. *Scientific Reports / Scientific Data*. (확인요 — 정확한 저널 확정 필요.)
- Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*. Springer.
- Davison, A.C., Smith, R.L. (1990). Models for exceedances over high thresholds. *J. R. Statist. Soc. B*, 52, 393–442.
- Arns, A., et al. (2013). Estimating extreme water level probabilities... *Coastal Engineering*, 81, 51–66.
- Batstone, C., et al. (2013). A UK best-practice approach for extreme sea-level analysis (Skew Surge JPM). *Ocean Engineering*, 71, 28–39.
- Pugh, D.T., Vassie, J.M. (1980). Applications of the joint probability method for extreme sea level computations. *Proc. Inst. Civil Engineers.*
- Menéndez, M., Woodworth, P.L. (2010). Changes in extreme high water levels based on a quasi-global tide-gauge data set. *JGR Oceans*, 115, C10011.
- NOAA CO-OPS — Tidal Datums (National Tidal Datum Epoch) & Sea Level Trends. IHO — Resolution on Chart Datum (Lowest Astronomical Tide).
- IOC/UNESCO (2020). Quality Control of in situ Sea Level Observations. IOC Manuals and Guides 83. UHSLC 데이터 품질등급; PSMSL/GLOSS.

**교과서·시각화 도구**
- Pugh, D., Woodworth, P. (2014). *Sea-Level Science: Understanding Tides, Surges, Tsunamis and Mean Sea-Level Changes*. Cambridge University Press.
- Munk, W.H., Cartwright, D.E. (1966). Tidal spectroscopy and prediction. *Phil. Trans. R. Soc. Lond. A*, 259, 533–581.
- Emery, W.J., Thomson, R.E. (2001). *Data Analysis Methods in Physical Oceanography*. Elsevier. (스펙트럼·코히어런스 표준.)
- Defant, A. (1958). *Ebb and Flow: The Tides of Earth, Air, and Water*. Univ. of Michigan Press. (형태계수 4구간.) van der Stok (1897) 형태계수 기원.
- Thyng, K.M., Greene, C.A., Hetland, R.D., Zimmerle, H.M., DiMarco, S.F. (2016). True colors of oceanography: Guidelines for effective and accurate colormap selection. *Oceanography*, 29(3), 9–13. (`cmocean` — phase/순환 색맵, balance/발산 색맵, amp/순차 색맵.)
- Python 도구(실존): `matplotlib`(bar·polar·quiver·contour·stackplot), `utide`(solve/reconstruct), `xarray`, `numpy`, `scipy`(stats.genextreme/genpareto, signal.welch/find_peaks/medfilt, stats.linregress), `cmocean`(phase/balance/amp), `cartopy`(지도), `astropy.timeseries.LombScargle`(불규칙 표본), `statsmodels`(추세), `ruptures`(변화점), `pyextremes`(극치).

> **DOI 표기 원칙:** 위에서 **굵게 표기한 doi만 본문/검색으로 확인**했다. 나머지 문헌은 권·페이지를 [`11_domain_sea_level_tides.md`](../11_domain_sea_level_tides.md) References에서 가져왔으며 doi 미부여분은 생략했다. "(확인요)" 표시 항목은 정확한 서지(저널·권·페이지·연도)가 미확정이므로 **확정 인용처럼 단정하지 말 것**(§G-5). **논문 원본 그림 복제는 금지하며, 그림의 유형·축·색맵 사양만 참고한다.**
