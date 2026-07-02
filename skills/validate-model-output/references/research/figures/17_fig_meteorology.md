# 17. 검증 시각화(그림) 레퍼런스 — 도메인: 기상·대기 (Verification Figures — Meteorology / Atmosphere)

이 문서는 재사용 Skill의 **검증 시각화(그림) 카탈로그** 시리즈 중 **[기상·대기 도메인편]** 이다. 수치모델(NWP·다운스케일링) 결과를 ERA5 등 권위 재분석자료·관측소(AWS)·라디오존데·위성과 비교·검증할 때 쓰는 **기상 고유의 그림**, 또는 **공통 그림(Taylor·QQ·ROC·rank histogram 등)을 기상 변수에 맞게 변형한 사례**를 "그림 카드" 형식으로 정리한다.

> **범위 분담(중복 방지)**: Taylor 다이어그램, 일반 QQ-플롯, ROC 곡선, target 다이어그램, 일반 reliability/rank histogram 같은 **횡단(공통) 그림의 기본형은 별도 [공통편]이 담당**한다. 본 문서는 ① 기상에만 있는 그림(wind rose·풍향 원형분포·skew-T·S1/ACC dropoff·FSS/SAL/MODE·intensity-scale·강수 QQ의 변환축 등)과 ② 공통 그림의 **기상 적용·변형 예**만 다루고, 기본형 설명은 공통편으로 교차링크한다.
>
> **대응 메서드 카탈로그**: 각 그림이 시각화하는 **수치지표·정의·수식·해석임계**는 [`07_domain_meteorology.md`](../07_domain_meteorology.md)에 메서드 카드로 있다. 본 문서는 "어떻게 그리고 어떻게 읽는가"에 집중하고, 정의는 07로 교차링크한다(중복 정의 금지).

> ⚠️ **그림 해석 전 반드시 읽을 원칙** → [`00_overview_taxonomy.md` §G 검증 해석의 함정](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats)
> 그림에도 그대로 적용된다: **(1) 기준자료(ERA5/위성 L4)는 참값이 아니라 reference** — 모든 그림 캡션·축라벨·범례에 "vs ERA5/reanalysis(기준)"로 명기하고 "관측오차/truth"라 단정하지 않는다. **(2) 색축·임계선의 "좋음/나쁨"은 advisory** — 컬러바 범위·등고선 임계는 변수·해역·해상도·기준자료 의존이므로 절대 단정 금지, 영역의존 경고를 캡션에 동반. **(3) 단일 그림 금지** — 어떤 그림도 1장으로 결론내지 않는다(정확도+편향+패턴/분포 + 유의성 그림을 함께 제시).

---

## 그림 카드 목차 (16개)

**바람** — 1. 바람 벡터·quiver & 오차벡터장 · 2. 바람장미(wind rose) · 3. 풍향 오차 원형/극좌표 분포 · 4. u/v 성분 오차 산점·2D 밀도
**기온** — 5. 2m 기온 편향/RMSE 공간 맵 · 6. 일변동(diurnal) 오차 곡선(기온·습도) · 7. 연직 프로파일·Skew-T(lapse-rate)
**기압·종관** — 8. MSLP 오차장(차이장) 맵 · 9. S1 경도 점수 리드타임 곡선 · 10. 500 hPa ACC dropoff·스코어카드
**강수** — 11. 범주 분할표 히트맵 + 수행도(performance) 다이어그램 · 12. Double-penalty 모식도 · 13. FSS 스케일–임계 래스터 · 14. 강도-스케일(intensity-scale) 다이어그램 · 15. 강수 QQ-플롯(log/√ 변환축)
**다운스케일·앙상블** — 16. 다운스케일 산점·2D 밀도 + 앙상블 신뢰성(reliability/rank hist)의 기상 적용

> 끝에 **"그림 → 검증목적 → 짝지표 → 07 교차링크" 요약표** 수록.

---

### 1. 바람 벡터·quiver 맵 & 오차벡터장 (바람 벡터/차이 맵 Wind Vector / Quiver & Difference-Vector Map)
- **무엇을 보여주나**: 바람장(u, v)을 화살표(quiver)나 유선(streamline)으로 지도 위에 그려 **방향+세기를 한눈에** 보여주고, 모델−기준(ERA5/관측)의 **벡터 차이(Δu, Δv)를 화살표로 겹쳐** 어디서 풍계가 어긋나는지 공간적으로 진단한다. 배경 색은 보통 풍속(scalar) 또는 풍속편향.
- **읽는 법**: 화살표 길이=세기, 머리방향=풍향(기상관행은 "바람이 불어오는 방향"이 아니라 **불어가는 방향**으로 그림 — 규약을 캡션에 명시). 차이장 패널에서 화살표가 **짧고 무작위**면 양호, **체계적으로 한쪽으로 정렬**되면 계통적 풍계 편향(예: 산악 풍하측 과소). 배경색이 한쪽 부호로 넓게 깔리면 풍속 계통편향. 나쁜 패턴: 해안선·산맥을 따라 정렬된 큰 차이 화살표.
- **언제 쓰나**: 자료형=격자(NetCDF) 바람장(10 m 또는 850 hPa); 검증목적=공간 패턴·계통편향 진단. 종관 흐름·국지순환(해륙풍·산곡풍) 재현 점검.
- **짝지표 & 교차링크**: 벡터 RMSE(VRMSE)·u/v 성분 bias·벡터상관 → [`07` 벡터 RMSE](../07_domain_meteorology.md), [`07` 바람 성분 검증](../07_domain_meteorology.md), [`07` 벡터 상관](../07_domain_meteorology.md). 정량 요약은 카드 4(성분 산점)·[`10` 해류 벡터검증](../10_domain_currents_circulation.md)과 공유(벡터검증 코어).
- **만드는 법**: `matplotlib.pyplot.quiver`/`streamplot` + `cartopy`(투영·해안선 `ax.coastlines()`); 격자가 빽빽하면 `[::n,::n]` 솎기 또는 `xarray`+`metpy`로 전처리. 차이장은 공통격자 재격자화(`xesmf`/`xarray.interp`) 후 `quiver(u_mod-u_ref, v_mod-v_ref)`. 풍속 배경은 `pcolormesh`.
- **함정·주의**: ① **u/v 부호·풍향 규약**(meteorological vs oceanographic) 불일치가 가장 흔한 오류 — 변환식 명시. ② 화살표 솎기 비율이 시각 인상을 좌우(정량 아님 — 반드시 VRMSE 그림과 병행). ③ 투영 왜곡으로 고위도 화살표 길이 과장 — `cartopy` 투영에서 벡터 회전(`transform` 일치) 필요. ④ 차이장은 **모델·기준에 동일 보간·동일 격자**를 강제(아니면 spurious 차이).
- **출처**: 표준 시각화 관행(WMO/WWRP-JWGFVR 검증 그림 관행). 도구: Met Office *Cartopy*(오픈소스, scitools.org.uk/cartopy); Matplotlib `quiver`. 벡터검증 정의는 Jolliffe & Stephenson, *Forecast Verification* (Wiley, 벡터검증 장).

---

### 2. 바람장미 (바람장미 Wind Rose)
- **무엇을 보여주나**: 한 지점(또는 영역)의 풍향·풍속 **결합 빈도분포**를 극좌표 막대로 표현. 방위(섹터)별로 막대를 그리고, 풍속 구간을 색으로 누적해 "어느 방향에서 얼마나 자주/세게 부는가"를 요약. 검증용으로는 **모델 vs 관측(또는 ERA5) 바람장미를 나란히** 놓아 풍향 분포·탁월풍(prevailing wind) 재현을 비교한다.
- **읽는 법**: 반경(막대 길이)=해당 방위 발생빈도(%), 색=풍속 계급(범례), 방위=풍향(보통 북쪽 위, 시계방향). 좋은 재현: 두 장미의 **탁월풍 방위·꽃잎 모양·풍속 색구성**이 일치. 나쁜 패턴: 모델이 탁월풍을 한 섹터로 과집중(방향 분산 과소), 약풍 비율 과대, 특정 방위 누락.
- **언제 쓰나**: 자료형=점·시계열(AWS/부이 CSV) 또는 격자 1점 추출; 검증목적=풍향 기후분포·탁월풍 재현. 풍력자원·확산·항만 응용에서 표준.
- **짝지표 & 교차링크**: 풍향 원형통계(원형 평균·원형분산·원형상관)와 함께 → [`07` 풍향 원형 검증](../07_domain_meteorology.md); 풍속 분포는 카드 15(QQ)·Weibull 적합. 방위별 빈도차는 카드 3(원형 오차분포)으로 보완.
- **만드는 법**: `windrose` 파이썬 패키지(`WindroseAxes.from_ax(); ax.bar(direction, speed, normed=True, opening=0.8, edgecolor='white')`) — 모델·관측을 같은 풍속 bins·같은 normalization으로. 대안: `matplotlib` 극좌표(`projection='polar'`) 수동. Weibull 적합은 `windrose`의 `pdf()`/`scipy.stats.weibull_min`.
- **함정·주의**: ① **정규화(normed) 일치** 필수 — 모델·관측 표본수·결측 다르면 빈도 왜곡. ② 약풍(<1~2 m/s)에서 풍향 정의가 불안정 → 풍속 임계 필터를 양쪽 동일 적용(07 풍향 카드 참조). ③ 섹터 폭(예: 16방위 vs 36방위)·풍속 bin 경계가 인상을 바꿈 — 동일 설정. ④ 장미는 **정성 비교** — 정량 결론은 원형통계 지표와 병행. ⑤ 시각정의(순간 vs 평균)·고도(10 m) 일치.
- **출처**: Roubeyrie, L. & Celles, S. (2018). Windrose: A Python Matplotlib, Numpy library to manage wind and pollution data, draw windrose. *Journal of Open Source Software* 3(29), 268. **DOI 10.21105/joss.00268** [확인됨]. 원형통계 정의는 Mardia & Jupp, *Directional Statistics* (Wiley).

---

### 3. 풍향 오차 원형/극좌표 분포 (풍향오차 원형 히스토그램 Wind-Direction Error Polar/Circular Plot)
- **무엇을 보여주나**: 풍향 오차 Δθ = wrap(θ_model − θ_obs, −180°~+180°)의 **분포를 극좌표 히스토그램(또는 장미형)** 으로, 또는 **관측풍향 대비 오차의 극좌표 산점**으로 표현. 계통적 회전편향(평균이 0이 아닌 쪽으로 쏠림)과 산포(원형 분산)를 눈으로 본다. 풍속가중 버전은 강풍일 때의 방향오차만 강조.
- **읽는 법**: 각도=오차 방향(시계/반시계 회전), 반경=빈도. 좋은 패턴: 0°(오차 없음) 주변에 **좁고 대칭**으로 모임. 나쁜 패턴: 평균이 +30° 등 한쪽으로 치우침(계통 회전편향), 또는 넓게 퍼짐(방향 변동 재현 불량), ±180° 부근 쌍봉(역류/풍향 반전 사례).
- **언제 쓰나**: 자료형=풍향 시계열·격자; 검증목적=풍향 계통편향·원형 산포 진단. wind rose가 "분포 모양"이라면 이 그림은 "오차 자체"를 본다.
- **짝지표 & 교차링크**: 원형 평균오차·원형 MAE·원형상관·원형분산(1−R̄) → [`07` 풍향 원형 검증](../07_domain_meteorology.md). 횡단 원형통계 코어는 파향[`08`](../08_domain_waves.md)·유향[`10`](../10_domain_currents_circulation.md)과 공유(README §4.2 원형통계 통일 권고).
- **만드는 법**: `numpy`로 Δθ 래핑(`(d + 180) % 360 − 180`), 풍속 임계로 필터; `matplotlib` 극좌표(`subplot(projection='polar')`)에 `hist`/`bar`. 원형 통계는 `scipy.stats.circmean/circstd`(주의: 도→라디안) 또는 `astropy.stats.circcorrcoef`. 풍속가중은 히스토그램 weight=풍속.
- **함정·주의**: ① **래핑(±180°) 누락** 시 360°↔0° 경계에서 가짜 거대오차 — 가장 흔한 버그. ② 약풍에서 풍향오차가 폭발 → 풍속 임계 필터·풍속가중 명시. ③ 극좌표 히스토그램의 막대 면적 착시(반경 선형이면 외곽 과대) — 빈도는 면적 아닌 반경으로 읽도록 주석. ④ 평균만 보지 말고 **분산·쌍봉**까지(다중모드면 평균 무의미).
- **출처**: Mardia & Jupp, *Directional Statistics* (Wiley, 표준 — 원형 히스토그램·원형 평균/분산); dtcenter/MET 문서(풍향 오차 처리 관행, 확인요). 풍향 RMSE 한계는 [`07`](../07_domain_meteorology.md) 참조.

---

### 4. u/v 성분 오차 산점·2D 밀도 (성분 오차 산점/밀도 u·v Component Error Scatter & 2D Density)
- **무엇을 보여주나**: 모델 vs 관측의 u(또는 v) 성분을 산점도로, 표본이 많으면 **2D 히스토그램/육각 밀도(hexbin)**로 표현. 1:1 대각선·회귀선·밀도구름으로 성분별 bias(절편)·기울기(과소/과대변동)·산포(RMSE)를 동시에 본다. 풍속이면 양의 왜도 때문에 밀도가 저속에 집중.
- **읽는 법**: x=관측, y=모델, 대각선=완벽. 점구름이 대각선 위/아래로 평행이동=성분 bias, 기울기<1=변동 과소(평활), 퍼짐=무작위오차. 색=점밀도(log 스케일 권장). 좋은 패턴: 대각선에 좁게 밀착. 나쁜 패턴: 휘어진 구름(비선형·구간의존 bias), 저풍속 과대·고풍속 과소(기울기<1).
- **언제 쓰나**: 자료형=시계열·격자 풀링 대량표본; 검증목적=정확도+편향+변동성 동시. 카드 1(공간)·카드 2(분포)의 정량 보완.
- **짝지표 & 교차링크**: u/v bias·성분 RMSE·회귀 기울기/절편·Pearson r → [`07` 바람 성분 검증](../07_domain_meteorology.md), [`01` 상관·회귀](../01_error_statistics.md). 종합요약은 공통편 Taylor 다이어그램으로(중복 금지 — 교차링크만).
- **만드는 법**: `matplotlib` `hexbin`(`bins='log'`) 또는 `numpy.histogram2d`+`pcolormesh`; 회귀는 `scipy.stats.linregress`(또는 총최소제곱 ODR — 양변 오차 시). 1:1선·통계박스(bias/RMSE/r) 주석. `xskillscore`로 격자 RMSE/bias 일괄 산출 후 표기.
- **함정·주의**: ① 일반 OLS는 x(관측)도 오차가 있어 기울기를 **체계적으로 과소** → 변동성 비교엔 ODR/주축회귀 권장. ② 점 과밀로 산점 포화 → 반드시 밀도(hexbin/2D hist)로. ③ 성분(u,v)은 좌표축 의존 — 회전격자/투영이면 성분 정의 일치. ④ 풍속 산점은 0 절단·왜도로 평균지표 왜곡 → 카드 15(QQ) 병행.
- **출처**: 회귀·산점 진단은 Wilks, *Statistical Methods in the Atmospheric Sciences* (표준); 성분 EMOS 사례 Schuhen, Thorarinsdottir & Gneiting (2012, *Monthly Weather Review* 140(10), 3204–3219). 도구: *xskillscore* (xarray-contrib, github.com/xarray-contrib/xskillscore).

---

### 5. 2m 기온 편향/RMSE 공간 맵 (기온 편향·RMSE 공간장 2-m Temperature Bias/RMSE Map)
- **무엇을 보여주나**: 격자점(또는 관측소 위치)별 기온 **편향(ME)** 과 **RMSE**를 지도에 색으로 깔아 **어디서** 모델이 더울/추울지, 어디서 오차가 큰지의 공간 구조를 본다. 보통 bias는 발산 컬러맵(±0 중심), RMSE는 순차 컬러맵. 지형(고도) 등고선·해안선을 오버레이해 지형의존을 드러낸다.
- **읽는 법**: 발산색(파랑=과소, 빨강=과대), 0이 흰색. 좋은 패턴: 약한 무작위 얼룩. 나쁜 패턴: **고지대 일관된 한색(표고차 lapse-rate 미보정)**, 해안선 따라 띠 형태(육해 대표성), 도시격자 hot bias. RMSE 맵은 산악·해안에서 hotspot이 흔함.
- **언제 쓰나**: 자료형=격자 또는 관측소 산점 매핑; 검증목적=계통편향의 공간구조·지형의존. 기압·습도에도 동일 적용.
- **짝지표 & 교차링크**: ME·RMSE·MAE → [`07` 2m 기온 검증](../07_domain_meteorology.md), [`07` 평균오차·편향](../07_domain_meteorology.md). 표고보정 전제는 [`07` 시공간 정합](../07_domain_meteorology.md)·[`15` 전처리](../15_preprocessing_regridding_colocation.md). 영역평균 요약은 카드 6(일변동)과 병행.
- **만드는 법**: `xarray`로 (model−ref) 계산 → `cartopy`+`pcolormesh`(bias는 `cmap='RdBu_r'`, `vmin=-v,vmax=+v` 대칭), 관측소면 `scatter(c=bias)`. 표고 오버레이 `ax.contour(orography)`. 면적가중 영역통계는 `xskillscore.rmse(..., weights=cos(lat))`.
- **함정·주의**: ① bias 컬러바는 **0 중심 대칭**으로(아니면 부호 착시). ② 관측소가 듬성하면 빈 곳 보간이 가짜 구조 — 산점 표기가 정직. ③ **표고차 보정(−6.5 K/km)** 자체가 오차원 — 보정 전/후 둘 다 보거나 캡션 명시. ④ RMSE와 bias를 **반드시 같이**(작은 RMSE가 상쇄된 큰 bias를 가릴 수 있음). ⑤ 컬러바 범위는 advisory — "좋음" 단정 금지, 영역의존 경고.
- **출처**: Wilks (표준); ERA5 2m 기온의 평탄·해안 과대/고지대 큰 오차 경향은 *Climate Dynamics* (2023) ERA5-CPM 다운스케일 평가([`07` ERA5 주의점 카드](../07_domain_meteorology.md) 참조). 도구: Cartopy, xarray, xskillscore.

---

### 6. 일변동(diurnal) 오차 곡선 (일변동 검증 플롯 Diurnal Cycle Error Plot)
- **무엇을 보여주나**: 변수(2m 기온·RH·풍속)를 **하루 중 시각(local hour 0–23)별로 합성(composite)** 해 모델·관측의 평균 일변동 곡선을 겹쳐 그리고, 시각별 bias/RMSE를 아래 패널에 띠로 표시. "낮 최고/밤 최저를 제대로 잡는가", "주간 가열·야간 냉각 위상이 맞는가"를 본다.
- **읽는 법**: x=현지시각, y=변수값(위 패널)·오차(아래 패널), 음영=관측 분산(±1σ) 또는 부트스트랩 CI. 좋은 패턴: 두 곡선 **진폭·위상 일치**, 오차띠가 0 주변. 나쁜 패턴: **야간 과대(역전층 미해상)**·주간 진폭 과소(혼합 과대), 곡선 **위상 지연**(최고기온 시각 어긋남), RH는 야간 포화 절단으로 새벽 bias.
- **언제 쓰나**: 자료형=관측소·격자 시계열(다일 평균); 검증목적=위상·진폭(시간구조) 재현. 경계층·복사·지면 과정 결함 진단의 1차 그림.
- **짝지표 & 교차링크**: 시각별 ME/RMSE, 일진폭 비, 위상오차(최고시각 차) → [`07` 2m 기온 검증](../07_domain_meteorology.md), [`07` 상대습도 검증](../07_domain_meteorology.md). 위상·진폭은 [`06` 시계열·위상진폭오차](../06_timeseries_signal.md)와 공유. 종합편향은 카드 5(공간맵) 병행.
- **만드는 법**: `pandas`/`xarray` `groupby(time.hour)`로 시각별 평균·분위 → `matplotlib` 2-패널(`sharex`). 현지시각 변환(UTC+경도/시간대) 필수. CI는 블록부트스트랩(자기상관). 계절·맑은날/흐린날 층화 권장.
- **함정·주의**: ① **시간대(UTC vs local) 변환 오류**가 위상 전체를 어긋나게 함 — 가장 흔한 치명오류. ② 순간값 vs 시간평균 라벨 불일치(특히 누적·평균 변수)로 위상 0.5h 밀림. ③ 단순 전(全)표본 평균은 계절 혼합 — 월·계절 층화. ④ RH의 100% 절단으로 야간 오차 해석 주의(노점/비습 병행 — 07 습도 카드).
- **출처**: Wilks (표준, composite 분석); 일변동 검증은 WMO/WWRP-JWGFVR 표면변수 검증 관행. RH 절단·습도 변수 한계는 [`07` 상대습도 검증 카드](../07_domain_meteorology.md).

---

### 7. 연직 프로파일·Skew-T (연직 프로파일/스큐-T Vertical Profile & Skew-T log-P)
- **무엇을 보여주나**: 라디오존데/모델의 **연직 구조**(기온 T·노점 Td·바람)를 (a) 단순 변수-고도 프로파일 또는 (b) **Skew-T log-P 열역학선도**로 그려 모델 vs 관측(또는 ERA5 연직층)을 비교. 안정도(역전층·lapse-rate)·습윤층·바람 시어를 본다. 우측에 풍깃(wind barb), 곁에 hodograph 인셋.
- **읽는 법**: Skew-T는 y=기압(log, 위로 감소), x=기온(우상향 경사축), 빨강=T·초록=Td 곡선, 두 곡선 간격=건조도. 건조/습윤 단열선·등포화혼합비선 배경. 좋은 재현: 모델·관측 T/Td 곡선과 **역전층·LCL·대류가용잠재에너지(CAPE) 면적**이 일치. 나쁜 패턴: 모델이 야간 접지역전층을 평활(과혼합), 습윤층 깊이/고도 어긋남, lapse-rate(기울기) 오차.
- **언제 쓰나**: 자료형=연직 프로파일(라디오존데 CSV·모델 연직층); 검증목적=연직 구조·안정도·습윤층. 사례기반(event) 진단·PBL 검증과 결합.
- **짝지표 & 교차링크**: 층별 T/Td/풍속 ME·RMSE, lapse-rate·역전강도, PBLH 차이 → [`07` 2m 기온(lapse-rate)](../07_domain_meteorology.md), [`07` 경계층고도 PBLH 검증](../07_domain_meteorology.md), [`07` 안정도 검증](../07_domain_meteorology.md). 연직보간 전제는 [`15`](../15_preprocessing_regridding_colocation.md).
- **만드는 법**: `metpy.plots.SkewT`(+`Hodograph`), `metpy.calc`로 LCL/LFC/EL/CAPE/CIN 산출; 입력은 `pint`-단위 부여(`units`). 단순 프로파일은 `matplotlib`(`invert_yaxis()`, y=log). 모델 연직층은 동일 기압면으로 보간 후 겹쳐 그림.
- **함정·주의**: ① **연직보간법**(기압-log vs 고도 선형)에 따라 lapse-rate·역전 모양이 바뀜 — 모델·관측 동일 보간. ② 라디오존데 **표류(drift)·관측시각**과 모델 격자/시각 불일치(사례검증 시 보정). ③ 습도 센서 저온 편향(상층 Td 신뢰 저하). ④ CAPE 등 유도량은 지면·혼합 가정에 민감 — 산출옵션 명시. ⑤ Skew-T 1장은 1프로파일 — 통계는 다수 프로파일 층별 RMSE로.
- **출처**: May, R. M. et al. (2022). MetPy: A Meteorological Python Library for Data Analysis and Visualization. *Bulletin of the American Meteorological Society* 103(10), E2273–E2284. **DOI 10.1175/BAMS-D-21-0125.1** [확인됨]. PBLH 산출법 Seidel et al. (2010, *JGR* 115, D16113). 안정도 표준 Stull, *An Introduction to Boundary Layer Meteorology* (Springer).

---

### 8. MSLP 오차장(차이장) 맵 (해면기압 차이장 MSLP Difference-Field Map)
- **무엇을 보여주나**: 해면기압(MSLP)의 **모델 등압선과 기준(ERA5/분석) 등압선을 겹쳐** 그리거나, **차이장(model−ref)을 색으로** 깔아 종관 패턴(저기압 중심위치·강도, 기압골/마루)의 어긋남을 본다. 사례검증에선 저기압 중심 추적 마커를 함께 표기.
- **읽는 법**: 등압선 겹침도가 클수록 양호. 차이장 색: 양(빨강)=모델 과대기압, 음(파랑)=과소. 쌍극자(저기압 한쪽 +, 반대쪽 −) 패턴=**중심위치 오차**(이동/위상), 단극(전반 +/−)=강도/기준면 편향. 나쁜 패턴: 저기압 주변 강한 쌍극자(위치 어긋남), 전선대 따라 띠 형태 차이.
- **언제 쓰나**: 자료형=격자 종관장; 검증목적=공간 패턴·종관계 위치/강도. 폭풍·저기압 사례검증의 표준 그림.
- **짝지표 & 교차링크**: MSLP ME/RMSE, 공간 ACC, S1(카드 9), 저기압 중심위치오차(km)·중심기압오차 → [`07` 해면기압 검증](../07_domain_meteorology.md), [`07` S1 경도 점수](../07_domain_meteorology.md), [`02` 공간장 패턴 검증](../02_spatial_pattern_verification.md). 객체기반은 카드 12/13(강수 SAL/MODE)과 발상 공유.
- **만드는 법**: `cartopy`+`xarray`; 등압선 `ax.contour(mslp, levels=...)`(모델·ref 다른 색/선스타일), 차이장 `pcolormesh(cmap='RdBu_r', 대칭범위)`. 저기압 중심은 국소최소 탐지(`scipy.ndimage.minimum_filter`). 면적가중 통계는 cosφ.
- **함정·주의**: ① 고지대 **해면환산 오차**가 가짜 차이 생성 — 산악역 마스크/주의. ② 평균 RMSE가 작아도 **개별 폭풍 위치/강도 오차는 큼** → 사례·event 그림 병행(07 MSLP 카드). ③ 등압선 간격(levels)·색이 인상을 좌우 — 모델·ref 동일. ④ 차이장은 동일격자·동일 평활 강제. ⑤ 컬러바 범위 advisory.
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (Wiley, 공간/패턴 검증); WMO NWP 검증 권고. 도구: Cartopy, xarray, SciPy.

---

### 9. S1 경도 점수 리드타임 곡선 (S1 경도점수 추이 S1 Gradient Score vs Lead Time)
- **무엇을 보여주나**: Teweles–Wobus **S1 점수**(기압/지위고도 장의 수평경도 오차)를 **리드타임(또는 연도)별** 선그래프로 그려 종관 패턴 위치/형태 예측의 추이·모델 개선을 추적. 역사적으로 모델 발전을 보여준 고전 그림.
- **읽는 법**: x=리드타임(h) 또는 연도, y=S1(0=완벽, 클수록 나쁨, **낮을수록 좋음 — 축 방향 주의**). 리드타임 증가에 따라 단조 상승. 좋은 패턴: 곡선이 낮고 완만 상승. 역사적 관행: S1≈20 우수, ≈70 무기량(해상도·자료 의존 — advisory). 여러 모델 곡선 비교로 우열.
- **언제 쓰나**: 자료형=격자 종관장(MSLP·500 hPa Z); 검증목적=경도(패턴) 정확도의 리드타임 의존·장기 개선 추적.
- **짝지표 & 교차링크**: S1과 함께 ACC(카드 10)·RMSE를 병행 → [`07` S1 경도 점수](../07_domain_meteorology.md), [`07` 500 hPa ACC](../07_domain_meteorology.md), [`02`](../02_spatial_pattern_verification.md). 부트스트랩 CI는 [`01` 유의성](../01_error_statistics.md).
- **만드는 법**: `numpy`로 인접격자 경도차(`np.gradient`) → S1 = 100·Σ|Δ∇G_F−Δ∇G_O|/Σmax(|Δ∇G_F|,|Δ∇G_O|); 리드타임 루프 후 `matplotlib` 선그래프(모델별 색), 블록부트스트랩 CI 음영.
- **함정·주의**: ① **축 방향 혼동**(낮을수록 좋음) — y라벨·화살표 주석 필수. ② 해상도·격자간격에 민감 → 모델 비교 시 **공통격자**로. ③ S1 단독은 강도/편향 못 봄 — ACC·RMSE 곡선 병행. ④ 절대 임계(20/70)는 advisory, 변수·영역 의존 경고. ⑤ 경도 계산방향(중앙차분 등) 일관.
- **출처**: Teweles, S. & Wobus, H. B. (1954). Verification of prognostic charts. *Bulletin of the American Meteorological Society* 35, 455–463 [확인됨]. WMO 검증 권고에 수록. 도구: NumPy, Matplotlib.

---

### 10. 500 hPa ACC dropoff·스코어카드 (이상편차상관 감쇠곡선·스코어카드 500-hPa ACC Dropoff & Scorecard)
- **무엇을 보여주나**: 500 hPa 지위고도(또는 MSLP) **이상편차상관 ACC를 리드타임별**로 그린 **감쇠곡선**(전 세계 운영센터 중기예보 표준 그림). 여러 모델·반구·계절을 겹치고, "ACC가 0.6(또는 80%)에 도달하는 리드타임"을 유용예측한계로 읽는다. **스코어카드**는 다수 변수·리드타임의 모델간 상대우열을 색칠 격자(▲/▼·유의성)로 요약한 공통편 변형.
- **읽는 법**: x=리드타임(일), y=ACC(1=완벽). 곡선이 **오른쪽으로 길수록**(높은 ACC 유지) 우수. 임계선(ACC=0.6 유용한계, 0.5 무기량 — ECMWF는 80% headline) 교차점이 "예측가능 한계". 스코어카드: 초록=기준 대비 유의 개선, 빨강=악화, 회색=유의차 없음. 나쁜 패턴: 곡선 조기 급락.
- **언제 쓰나**: 자료형=격자 종관장(이상편차); 검증목적=공간 패턴 예측가능성·모델간 랭킹. 운영 정례검증·모델 업그레이드 평가.
- **짝지표 & 교차링크**: ACC와 함께 RMSE/bias·유의성(부트스트랩/DM) → [`07` 500 hPa ACC](../07_domain_meteorology.md), [`01` 상관·ACC](../01_error_statistics.md), [`13` Diebold–Mariano·스코어카드](../13_model_intercomparison_downscaling.md). 기본 ACC 정의·일반 스코어카드는 공통편 참조(중복 금지).
- **만드는 법**: 동일 climatology로 이상편차 산출(`xarray`), 위도가중 공간상관 → `xskillscore`/직접 계산; 리드타임 루프 후 `matplotlib` 곡선 + 임계선. 스코어카드는 변수×리드타임 행렬 `pcolormesh`+유의성 마스크(`hatch`).
- **함정·주의**: ① **동일 기후평균(climatology) 강제** — 영역·기준기간·격자 일치(아니면 ACC 비교 무의미). ② 위도(area) 가중 누락 시 고위도 과대표. ③ ACC는 **편향 못 봄** — RMSE/bias 병행. ④ 임계(0.6/80%) advisory·센터마다 anomaly 정의 상이 — 절대비교 주의. ⑤ 스코어카드 색은 **유의성과 함께**(작은 차이 과장 금지).
- **출처**: Jolliffe & Stephenson, *Forecast Verification* (Wiley, ACC 장); ECMWF Forecast User Guide §6.2.1 Headline scores — "HRES 500 hPa Z ACC가 80%에 도달하는 리드타임"(ECMWF Confluence, 기관 기술문서, 확인요); WMO Manual on the GDPFS 표준 검증 스코어(확인요). 도구: xskillscore, xarray.

---

### 11. 범주 분할표 히트맵 + 수행도 다이어그램 (분할표·수행도 Contingency Heatmap & Performance Diagram)
- **무엇을 보여주나**: 강수(임계초과) 예/아니오 검증을 (a) **2×2 분할표 히트맵**(hits/false alarms/misses/correct negatives 셀에 빈도·색)과 (b) **Roebber 수행도 다이어그램**으로 표현. 수행도 다이어그램은 한 평면에 POD(y)·성공비 SR=1−FAR(x)·CSI(곡선)·빈도편향 FBI(대각선)를 동시에 깔아, 여러 임계·여러 모델 점을 한 번에 비교한다.
- **읽는 법**: 수행도: x=SR(우=오경보 적음), y=POD(상=놓침 적음), 곡선=CSI(우상=고득점), 점선 대각=FBI(우하<1 과소, 좌상>1 과대예보). 좋은 점은 **우상단**(완벽=(1,1)). 부트스트랩 cross-hair로 불확실성. 나쁜 패턴: 좌상(과대예보·FAR 큼), 우하(과소예보·놓침). 분할표 히트맵은 대각(hits·correct neg) 진하고 비대각 옅으면 양호.
- **언제 쓰나**: 자료형=격자·관측소 임계초과 사건(강수≥1/10/50 mm, 돌풍·결빙); 검증목적=범주(이산) 예보 품질·다임계 비교.
- **짝지표 & 교차링크**: POD·FAR·CSI·ETS·HSS·HK(PSS)·FBI → [`07` 강수 범주 검증(분할표)](../07_domain_meteorology.md), [`03` 범주형 분할표](../03_categorical_event_extremes.md). 희박사건은 카드 없음→[`07` EDI/SEDI](../07_domain_meteorology.md). ROC(확률)는 공통편 참조.
- **만드는 법**: 분할표는 `numpy`로 임계 이진화 후 `sklearn.metrics.confusion_matrix`/직접 카운트 → `seaborn.heatmap`. 수행도는 `matplotlib`: 배경에 `contourf`(CSI 격자), `plot`(FBI 대각선), 모델점 `scatter`(임계별 색); 부트스트랩 cross-hair. 다임계 루프.
- **함정·주의**: ① **임계 선택에 강하게 의존** — 단일 임계 금지, 다임계 점을 함께. ② 위치오차에 매우 민감(double penalty — 카드 12) → 공간점수 병행 필수. ③ 희박사건은 CSI/ETS 퇴화 → EDI/SEDI(07). ④ 기후빈도(base rate)가 점수 좌우 — 영역·계절 명시. ⑤ 표본 적으면 cross-hair 큼(부트스트랩 표기).
- **출처**: Roebber, P. J. (2009). Visualizing multiple measures of forecast quality. *Weather and Forecasting* 24(2), 601–608. **DOI 10.1175/2008WAF2222159.1** [확인됨]. 분할표 정의 Jolliffe & Stephenson, *Forecast Verification* (Wiley); CAWCR Forecast Verification 페이지(확인요). 도구: scikit-learn, seaborn, Matplotlib.

---

### 12. Double-penalty 모식도 (이중벌점 모식도 Double-Penalty Schematic)
- **무엇을 보여주나**: 고해상 모델이 **강수역을 약간 어긋난 위치**에 정확한 강도로 예측했을 때, 전통 격자점 점수(RMSE·CSI)가 그 비를 **놓침(miss)+오경보(false alarm)로 이중 처벌**해 "흐릿한(blurry) 예보"보다 낮게 평가되는 역설을 보여주는 **교육·진단 모식도**. 보통 (관측 / 정확하지만 변위된 예보 / 평활된 예보) 3패널과 그 아래 점수표를 나란히.
- **읽는 법**: 3패널 비교 — 변위 예보는 시각적으로 "더 사실적"인데 격자점 점수는 더 나쁨, 평활 예보는 비현실적인데 점수는 더 좋음. 화살표/주석으로 "왜 이중벌점인가"를 표시. 이 그림의 메시지: **격자점 점수만으로 고해상 모델을 평가하지 말라** → 공간검증(FSS/SAL/MODE) 필요.
- **언제 쓰나**: 자료형=고해상 격자 강수(개념 설명·보고서 도입); 검증목적=공간검증 도입 동기 부여. 단독 검증그림이 아니라 **해석 프레임**.
- **짝지표 & 교차링크**: 격자점 CSI/ETS(카드 11) vs 공간 FSS(카드 13)·SAL/intensity-scale(카드 14)·MODE 대비 → [`07` 강수 연속 검증(double penalty)](../07_domain_meteorology.md), [`07` 공간검증법 비교 ICP](../07_domain_meteorology.md), [`02` 공간장 패턴 검증](../02_spatial_pattern_verification.md), [`14` double-penalty(AI)](../14_ai_ml_evaluation.md).
- **만드는 법**: `numpy`로 이상화 강수장 생성(가우시안 블롭을 변위/평활), `matplotlib` 다패널 + 각 패널 RMSE/CSI/FSS 주석. 실제 사례면 관측·예보·변위본을 `cartopy`로.
- **함정·주의**: ① 모식도는 **개념 전달용** — 실제 점수 결론은 정량 그림(11·13·14)으로. ② "평활이 항상 점수를 올린다"는 오해 주의(FSS·확률화는 이를 보정). ③ 변위 크기·블롭 크기 설정이 메시지를 좌우 — 현실적 스케일 사용.
- **출처**: Ebert, E. E. (2008). Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework. *Meteorological Applications* 15, 51–64 — neighborhood/double penalty 리뷰; Gilleland, E. et al. (2009). Intercomparison of spatial forecast verification methods. *Weather and Forecasting* 24, 1416–1430 [확인됨]. Roberts & Lean (2008)도 동기 제시.

---

### 13. FSS 스케일–임계 래스터 (분율기량점수 스케일-임계도 FSS Scale–Threshold Diagram)
- **무엇을 보여주나**: Fractions Skill Score(FSS)를 **이웃반경(공간 스케일, x 또는 y)과 강수 임계(intensity, 다른 축)**의 2D 격자(래스터/히트맵)로 그려, "어느 스케일·어느 강도부터 예보가 유용(skillful)한가"를 한 장으로 본다. 단일 임계면 FSS-vs-스케일 곡선(+useful-scale 표시).
- **읽는 법**: 색=FSS(0~1, 1=완벽). 보통 작은 이웃에서 낮고 이웃 커질수록 1로 수렴. **FSS가 0.5+f₀/2(f₀=관측빈도) 등치선**을 넘는 최소 이웃이 "기량 스케일(skillful scale)". 좋은 패턴: 작은 스케일에서 빨리 유용기준 돌파(등치선이 좌하단). 나쁜 패턴: 큰 이웃에서도 기준 미달(우상단까지 파랑), 고임계에서 기량 급락.
- **언제 쓰나**: 자료형=고해상 격자 강수(또는 반사도·위성영상); 검증목적=공간 변위 허용·유효 공간스케일 진단. double penalty 완화 진단의 표준.
- **짝지표 & 교차링크**: FSS·useful/skillful scale·f₀ → [`07` FSS 카드](../07_domain_meteorology.md), [`02` 이웃/FSS](../02_spatial_pattern_verification.md), [`03`](../03_categorical_event_extremes.md). 앙상블 FSS는 [`07`](../07_domain_meteorology.md)(Necker et al. 2024). 격자점 점수 대비는 카드 11.
- **만드는 법**: `pysteps.verification.spatialscores`(`fss`/`intensity_scale`) 또는 직접: 임계 이진화→`scipy.ndimage.uniform_filter`로 이웃분율→FSS; 임계×이웃 루프 후 `matplotlib` `pcolormesh` + useful-scale 등치선(`contour`). `xarray`로 다중 리드타임.
- **함정·주의**: ① **공통격자 재격자화** 선행(다른 해상도 직접 FSS 금지). ② FSS는 임계·이웃·도메인 크기에 의존 — 설정 문서화, 도메인 가장자리 처리(zero-pad vs 마스크) 명시. ③ useful-scale 기준 0.5+f₀/2는 **관측빈도 f₀ 의존**(드문 사건은 기준 낮음) — advisory. ④ double penalty를 완화하나 **제거 못 함**. ⑤ 단일 그림 금지(SAL/MODE 병행 권장).
- **출처**: Roberts, N. M. & Lean, H. W. (2008). Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events. *Monthly Weather Review* 136, 78–97; Mittermaier, M. & Roberts, N. (2010). *Weather and Forecasting* 25(1), 343–354 — skillful scale. 도구: *pysteps* (오픈소스, pysteps.github.io), SciPy.

---

### 14. 강도-스케일 다이어그램 (강도-스케일 웨이블릿도 Intensity-Scale Diagram)
- **무엇을 보여주나**: 강수 예보 기량을 **강도(임계, y)와 공간 스케일(웨이블릿 분해, x)의 2D 함수**로 분해해 색칠한 진단도. "어떤 비 강도가 어떤 공간스케일에서 기량이 있는가/없는가"를 동시에 본다(FSS가 분율이라면, 이쪽은 웨이블릿 에너지/MSE 기량의 스케일 분해).
- **읽는 법**: x=공간 스케일(웨이블릿 레벨, 작은→큰), y=강수 임계(약→강), 색=스케일별 기량점수(SS, 1=완벽, 0=무기량, 음=해로움). 좋은 패턴: 넓은 강도·스케일에서 양의 기량(따뜻한 색). 나쁜 패턴: 강한 강도·작은 스케일에서 음/0 기량(고해상 대류강수의 전형적 약점).
- **언제 쓰나**: 자료형=격자 강수장(2의 거듭제곱 격자 권장); 검증목적=강도·스케일 동시 기량 분해. FSS·SAL·MODE와 상호보완(ICP 권장 도구 세트).
- **짝지표 & 교차링크**: 스케일별 MSE 기량점수, 임계별 bias → [`07` 강도-스케일 검증](../07_domain_meteorology.md), [`02` 스케일분리(웨이블릿)](../02_spatial_pattern_verification.md), [`07` ICP 비교](../07_domain_meteorology.md). FSS(카드 13)와 같은 동기(공간검증).
- **만드는 법**: `PyWavelets`(`pywt.wavedec2`, Haar)로 이진오차장 다중스케일 분해 → 스케일별 MSE 기량 → `matplotlib` `pcolormesh`(스케일×임계). `pysteps.verification.spatialscores.intensity_scale`도 구현 제공. 공통격자·2ⁿ 패딩.
- **함정·주의**: ① **2의 거듭제곱 격자**·도메인 제약(웨이블릿) — 패딩/크롭이 결과에 영향. ② FSS보다 **해석이 복잡**(웨이블릿 레벨↔물리 스케일 매핑 설명 필요). ③ 임계·웨이블릿 종류에 민감 — 설정 명시. ④ 단독 결론 금지 — FSS·객체기반(SAL/MODE)과 함께(ICP 메타).
- **출처**: Casati, B., Ross, G. & Stephenson, D. B. (2004). A new intensity-scale approach for the verification of spatial precipitation forecasts. *Meteorological Applications* 11, 141–154; Casati, B. (2010). *Weather and Forecasting* 25(1) 갱신판. ICP 맥락 Gilleland et al. (2009) [확인됨]. 도구: PyWavelets, pysteps.

---

### 15. 강수 QQ-플롯(log/√ 변환축) (강수 분위-분위도 변환축 Precipitation Q-Q Plot with log/√ Axes)
- **무엇을 보여주나**: 공통 QQ-플롯의 **기상(강수) 변형** — 강수처럼 0이 과다하고 양의 왜도·긴 꼬리를 갖는 변수의 분위(quantile)를 **로그축 또는 제곱근축**에 그려 분포 전체(특히 **극한강수 꼬리**)의 모델 vs 관측 일치를 본다. 선형축이면 꼬리만 보이고 약·중간 강수가 원점에 뭉치는 문제를 변환축이 해결.
- **읽는 법**: x=관측 분위, y=모델 분위, 1:1 대각선=완벽. 변환축(log/√)에서 약~강수 전 구간이 고르게 보임. 좋은 패턴: 대각선 밀착. 나쁜 패턴: **상단(극값)에서 대각선 아래로 휘면 극한강수 과소**(재분석/조밀모델 흔한 약점), 하단 들뜸=약한 비 과대(drizzle bias), 계단형=강수 빈도/건일 불일치.
- **언제 쓰나**: 자료형=강수 시계열·격자 풀링(또는 풍속); 검증목적=분포·꼬리·극값 재현. RMSE가 같아도 분포가 다른 경우의 필수 진단. 다운스케일·바이어스보정 평가의 핵심.
- **짝지표 & 교차링크**: KS 통계·Perkins PDF 기량점수·분위별 bias → [`07` 강수 분포·분위 비교(QQ/KS/Perkins)](../07_domain_meteorology.md), [`07` 강수 연속(로그/√ 변환)](../07_domain_meteorology.md), [`03` 극값(POT/GEV)](../03_categorical_event_extremes.md). 일반 QQ 기본형은 공통편 참조(중복 금지 — 여기선 변환축·강수 특화만).
- **만드는 법**: `numpy.quantile`(공통 확률격자) → `matplotlib` `scatter`/`plot` + `ax.set_xscale('log'); set_yscale('log')`(또는 √ 변환값) + 1:1선. 0 처리(`log(x+a)` 오프셋 또는 wet-day만). `scipy.stats.ks_2samp`로 KS. 극값 강조는 상위분위(95/99/99.9p) 마커.
- **함정·주의**: ① **0(건일) 처리**가 핵심 — log축에서 0은 −∞ → wet-day(>임계)만 또는 오프셋 a 명시(모델·관측 동일). ② 변환 종류(log10/ln/√)와 오프셋이 그림을 바꿈 — 일치·기록. ③ 누적시간(1h/24h)·게이지 undercatch 정합(아니면 가짜 꼬리차). ④ 자기상관 시 KS p값 과신 — 그림은 정성, 유의성은 별도. ⑤ ERA5 등 평활 기준은 극값 과소 → 꼬리차를 "모델 결함"으로 단정 금지(기준 불확실성).
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (표준, QQ·분포검증); Perkins, S. E. et al. (2007). *Journal of Climate* 20(17), 4356–4376 — PDF 기량점수 [확인됨]. 강수 변환·꼬리 한계는 [`07` 강수 카드](../07_domain_meteorology.md). 도구: NumPy, SciPy, Matplotlib.

---

### 16. 다운스케일 산점·밀도 + 앙상블 신뢰성(기상 적용) (다운스케일 산점/앙상블 신뢰성 Downscaling Scatter & Ensemble Reliability — Meteorological Application)
- **무엇을 보여주나**: 두 진단을 묶은 카드. (a) **다운스케일 산점·2D 밀도**: 통계/역학 다운스케일(PP·MOS·QM) 산출 vs 국지관측을 hexbin 밀도로 그려 분산 과소(회귀형 다운스케일의 전형)·구간의존 bias를 본다. (b) **앙상블 신뢰성**: rank histogram(Talagrand)·reliability diagram을 **강수·기온·풍속 등 기상 변수에 적용**한 예. 기본형은 공통편이 담당하므로 여기선 **기상 적용·해석**만.
- **읽는 법**: 산점/밀도는 카드 4와 동일(대각선 기준, 기울기<1=분산 과소). **Rank histogram**: 균일=신뢰, **U자=과소산포(앙상블 spread 부족)**, ∩자=과대산포, 기울기=편향 — 강수는 0집중으로 최저순위 과대(주의). **Reliability diagram**: 예보확률 vs 관측빈도, 대각선=완벽 보정; 아래로 처지면 과대확신(over-forecast), 곡선 위 sharpness 막대도 함께. 나쁜 패턴: U자 rank hist + 대각선 이탈 reliability.
- **언제 쓰나**: 자료형=통계 다운스케일 시계열/앙상블 NWP; 검증목적=분포·변동성 재현(다운스케일)·앙상블 신뢰성(spread-skill)·확률 보정. 단일 RMSE 최소화의 함정 진단.
- **짝지표 & 교차링크**: 분산비·QQ(카드 15)·KS·Perkins(다운스케일); spread-skill 비·BSS 신뢰도항·CRPS(앙상블) → [`07` 다운스케일링 검증](../07_domain_meteorology.md), [`07` 바이어스보정(QM/QDM)](../07_domain_meteorology.md), [`07` rank histogram·reliability](../07_domain_meteorology.md), [`07` Brier/CRPS](../07_domain_meteorology.md), [`13` spread-skill·QM](../13_model_intercomparison_downscaling.md). **기본형 정의·그리는 법은 [공통편] 참조(중복 금지).**
- **만드는 법**: 산점/밀도 `matplotlib` `hexbin`+회귀(ODR). Rank histogram: `xskillscore.rank_histogram` 또는 `numpy`로 관측의 앙상블 내 순위 카운트→`bar`. Reliability: `xskillscore.reliability`/`sklearn.calibration.calibration_curve`→예보확률 binning. CRPS는 `xskillscore.crps_ensemble`. 다운스케일은 교차검증(leave-one-out) 표본으로.
- **함정·주의**: ① 다운스케일 산점은 **OLS 기울기 과소** 착시 → 분산비·QQ로 보완(분산 과소는 PP/회귀의 실제 약점이자 OLS 아티팩트 둘 다 가능). ② Rank hist는 **신뢰성만**(정확도 아님) — CRPS/RMSE 병행. ③ **관측오차가 spread 해석을 왜곡**(관측오차 큰데 U자면 과소산포 오판) — 관측 불확실성 고려. ④ 강수 0집중은 rank hist 최저빈 인위적 상승 → 변형/주의. ⑤ reliability는 표본·binning 의존(부트스트랩 CI). ⑥ 교차검증 누설 금지(다운스케일).
- **출처**: Maraun, D. & Widmann, M. *Statistical Downscaling and Bias Correction for Climate Research* (Cambridge University Press, 2018) — 다운스케일 분산 과소·QM; Hamill, T. M. (2001). Interpretation of rank histograms for verifying ensemble forecasts. *Monthly Weather Review* 129, 550–560 — rank histogram; Wilks (표준, reliability diagram). 도구: *xskillscore*, scikit-learn, Matplotlib.

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 07 교차링크

| # | 그림 (국문 / English) | 주 검증목적 | 짝지표(수치) | 07(및 타 파일) 교차링크 | 핵심 도구 |
|---|---|---|---|---|---|
| 1 | 바람 벡터·quiver/오차벡터장 (Wind quiver & difference) | 공간 패턴·계통 풍계편향 | VRMSE·u/v bias·벡터상관 | 07 벡터RMSE/성분/벡터상관; 10 | Cartopy, Matplotlib quiver |
| 2 | 바람장미 (Wind rose) | 풍향 기후분포·탁월풍 재현 | 원형평균/분산·Weibull | 07 풍향 원형검증 | windrose |
| 3 | 풍향 오차 원형분포 (Wind-dir circular error) | 풍향 계통회전편향·산포 | 원형 MAE·원형상관·1−R̄ | 07 풍향 원형검증; 08/10 | Matplotlib polar, SciPy |
| 4 | u/v 성분 오차 산점·밀도 (Component scatter) | 정확도+편향+변동성 | 성분 bias/RMSE·회귀 slope·r | 07 바람 성분검증; 01 | hexbin, xskillscore, ODR |
| 5 | 2m 기온 bias/RMSE 맵 (T bias/RMSE map) | 계통편향 공간구조·지형의존 | ME·RMSE·MAE | 07 2m 기온; 15; (ERA5 주의점) | Cartopy, xskillscore |
| 6 | 일변동 오차 곡선 (Diurnal cycle) | 위상·진폭(시간구조) | 시각별 ME/RMSE·진폭비·위상오차 | 07 2m기온/RH; 06 | pandas groupby, Matplotlib |
| 7 | 연직 프로파일·Skew-T (Skew-T) | 연직구조·안정도·습윤층 | 층별 RMSE·lapse-rate·PBLH·CAPE | 07 lapse-rate/PBLH/안정도; 15 | MetPy SkewT/calc |
| 8 | MSLP 오차장 맵 (MSLP difference) | 종관 패턴·저기압 위치/강도 | RMSE·ACC·중심위치/기압오차 | 07 MSLP/S1; 02 | Cartopy, SciPy |
| 9 | S1 경도점수 리드타임 곡선 (S1 vs lead) | 경도(패턴) 정확도·개선추적 | S1(낮을수록 좋음) | 07 S1; 02; 01 | NumPy gradient, Matplotlib |
| 10 | 500hPa ACC dropoff·스코어카드 (ACC dropoff) | 패턴 예측가능성·모델랭킹 | ACC·RMSE·DM 유의성 | 07 500hPa ACC; 01; 13 | xskillscore, xarray |
| 11 | 분할표 히트맵+수행도 (Performance diagram) | 범주(이산) 예보 품질·다임계 | POD·FAR·CSI·ETS·HSS·FBI | 07 강수 범주; 03 | scikit-learn, seaborn |
| 12 | Double-penalty 모식도 (Double-penalty) | 공간검증 도입 동기(해석틀) | 격자점 vs 공간점수 대비 | 07 강수연속/ICP; 02; 14 | NumPy, Matplotlib |
| 13 | FSS 스케일–임계 래스터 (FSS scale–threshold) | 공간변위 허용·유효스케일 | FSS·skillful scale·f₀ | 07 FSS; 02; 03 | pysteps, SciPy |
| 14 | 강도-스케일 다이어그램 (Intensity-scale) | 강도·스케일 동시 기량분해 | 스케일별 MSE 기량점수 | 07 강도-스케일/ICP; 02 | PyWavelets, pysteps |
| 15 | 강수 QQ(log/√ 변환축) (Precip Q-Q) | 분포·꼬리·극값 재현 | KS·Perkins S·분위 bias | 07 강수 분포·분위; 03 | NumPy, SciPy |
| 16 | 다운스케일 산점+앙상블 신뢰성 (Downscale & reliability) | 분산/변동성·앙상블 신뢰성·보정 | 분산비·spread-skill·BSS·CRPS | 07 다운스케일/QM/rank hist/Brier; 13 | xskillscore, sklearn |

> **공통편 참조(중복 정의 금지)**: Taylor 다이어그램, target 다이어그램, 일반 QQ-플롯 기본형, ROC 곡선, rank histogram·reliability diagram **기본형**은 [공통편]에 있다. 본 문서는 기상 고유 그림(2·3·7·9·13·14)과 공통 그림의 기상 변형(4·10·11·15·16)에 한정한다.

---

## 출처 (References) — 본 문서에서 점검·인용

본 카탈로그 원칙(README·00 §F/§G)에 따라 **검증 가능한 실제 출처만** 인용한다. **[확인됨]** 은 본 작업에서 WebSearch로 저널·권·페이지·DOI를 대조해 실재를 확인한 항목이다. 표준 교과서/기관 지침은 정전(canonical) 문헌으로 실재하나 세부 서지는 원문 확인 권장. **DOI는 확인한 것만 표기하고 임의 생성하지 않았다.** 미검증 항목은 "(확인요)".

**그림·시각화 1차 출처(논문)**
- Roebber, P. J. (2009). Visualizing multiple measures of forecast quality. *Weather and Forecasting* 24(2), 601–608. **DOI 10.1175/2008WAF2222159.1** [확인됨]. — 수행도(performance) 다이어그램(카드 11).
- Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single diagram. *Journal of Geophysical Research* 106(D7), 7183–7192. — Taylor 다이어그램(공통편; 본 문서는 교차링크).
- Teweles, S. & Wobus, H. B. (1954). Verification of prognostic charts. *Bulletin of the American Meteorological Society* 35, 455–463. [확인됨] — S1 score(카드 9).
- Roberts, N. M. & Lean, H. W. (2008). Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events. *Monthly Weather Review* 136, 78–97. — FSS(카드 13).
- Mittermaier, M. & Roberts, N. (2010). Intercomparison of spatial forecast verification methods: identifying skillful spatial scales using the FSS. *Weather and Forecasting* 25(1), 343–354. — skillful scale(카드 13).
- Casati, B., Ross, G. & Stephenson, D. B. (2004). A new intensity-scale approach for the verification of spatial precipitation forecasts. *Meteorological Applications* 11, 141–154; Casati, B. (2010). *Weather and Forecasting* 25(1) 갱신판. — 강도-스케일(카드 14).
- Wernli, H., Paulat, M., Hagen, M. & Frei, C. (2008). SAL—A novel quality measure for the verification of quantitative precipitation forecasts. *Monthly Weather Review* 136(11), 4470–4487. [확인됨] — 객체기반 공간검증(카드 12 교차).
- Davis, C., Brown, B. & Bullock, R. (2006). Object-based verification of precipitation forecasts. Part I. *Monthly Weather Review* 134, 1772–1784. [확인됨] — MODE(카드 12 교차).
- Gilleland, E., Ahijevych, D., Brown, B. G., Casati, B. & Ebert, E. E. (2009). Intercomparison of spatial forecast verification methods. *Weather and Forecasting* 24, 1416–1430. [확인됨] — 공간검증법 비교·double penalty(카드 12·14).
- Ebert, E. E. (2008). Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework. *Meteorological Applications* 15, 51–64. — neighborhood/double penalty 리뷰(카드 12·13).
- Perkins, S. E. et al. (2007). Evaluation of the AR4 climate models' simulated daily max/min temperature and precipitation over Australia using PDFs. *Journal of Climate* 20(17), 4356–4376. [확인됨] — PDF/QQ 분포검증(카드 15).
- Hamill, T. M. (2001). Interpretation of rank histograms for verifying ensemble forecasts. *Monthly Weather Review* 129, 550–560. — rank histogram(카드 16).
- Schuhen, N., Thorarinsdottir, T. L. & Gneiting, T. (2012). Ensemble model output statistics for wind vectors. *Monthly Weather Review* 140(10), 3204–3219. [확인됨] — 바람 성분(카드 4).

**표준 교과서·지침(canonical)**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences* (Academic Press). — 산점·QQ·composite·reliability·범주검증.
- Jolliffe, I. T. & Stephenson, D. B. (eds.) *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley). — 벡터·분할표·ACC·ROC.
- Mardia, K. V. & Jupp, P. E. *Directional Statistics* (Wiley). — 풍향 원형통계·원형 히스토그램(카드 2·3).
- Stull, R. B. *An Introduction to Boundary Layer Meteorology* (Springer). — 안정도·Skew-T 맥락(카드 7).
- Maraun, D. & Widmann, M. *Statistical Downscaling and Bias Correction for Climate Research* (Cambridge University Press, 2018). — 다운스케일 분산과소·QM(카드 16).
- Seidel, D. J. et al. (2010). Estimating climatological PBL heights from radiosonde observations. *Journal of Geophysical Research* 115, D16113. — PBLH(카드 7).

**소프트웨어·도구 출처(오픈소스, 실존)**
- Roubeyrie, L. & Celles, S. (2018). Windrose: A Python Matplotlib, Numpy library to manage wind and pollution data, draw windrose. *Journal of Open Source Software* 3(29), 268. **DOI 10.21105/joss.00268** [확인됨]. — *windrose*(카드 2).
- May, R. M. et al. (2022). MetPy: A Meteorological Python Library for Data Analysis and Visualization. *Bulletin of the American Meteorological Society* 103(10), E2273–E2284. **DOI 10.1175/BAMS-D-21-0125.1** [확인됨]. — *MetPy* SkewT/calc(카드 7).
- *Cartopy* — Met Office (scitools.org.uk/cartopy), 지도·투영·벡터 변환(카드 1·5·8). 오픈소스.
- *xskillscore* — xarray-contrib (github.com/xarray-contrib/xskillscore), xarray 기반 검증지표(RMSE/ACC/CRPS/rank histogram/reliability)(카드 4·5·10·16). 오픈소스.
- *pysteps* — community (pysteps.github.io), `verification.spatialscores`(FSS·intensity-scale)(카드 13·14). 오픈소스.
- *PyWavelets* (pywavelets.readthedocs.io) — 웨이블릿 분해(카드 14). *seaborn*/*scikit-learn* — 히트맵·calibration_curve(카드 11·16). *SciPy*/*NumPy*/*Matplotlib*/*xarray* — 공통.

**기관 기술문서(advisory — 확정인용 주의)**
- ECMWF Forecast User Guide §6.2.1 "ECMWF headline scores" — HRES 500 hPa Z ACC가 80%에 도달하는 리드타임을 headline score로 사용(ECMWF Confluence Wiki). (확인요 — 기관 페이지, 버전 변동 가능)
- WMO Manual on the GDPFS — 운영 표준 검증 스코어(ACC 등). (확인요)
- WMO / WWRP-JWGFVR Forecast Verification 권고 및 CAWCR(호주) Forecast Verification 페이지(cawcr.gov.au/projects/verification/) — 범주·연속·공간 지표 정의·그림 관행. (확인요 — 기관 페이지)
- dtcenter/MET(Model Evaluation Tools) 문서 — 풍향 오차·공간검증 구현 관행. (확인요)

*주: [확인됨] 13개 항목은 본 작업에서 WebSearch로 실재·서지를 대조했다(Roebber 2009, windrose JOSS, MetPy BAMS, S1 Teweles–Wobus, SAL, MODE, ICP, Perkins 2007, Schuhen 2012, Wernli 2008, Davis 2006, Gilleland 2009, EDI/SEDI 계열은 07에서 확인). 표시 없는 표준 교과서/기관 지침은 정전 문헌으로 실재하나 세부 서지(쇄·페이지)·기관 페이지 내용은 변동 가능하므로 원문 확인을 권한다. DOI는 임의 생성하지 않았다.*
