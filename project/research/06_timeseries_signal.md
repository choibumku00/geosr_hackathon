# 06. 시계열·신호 분석 (Time-series / Signal Analysis)

수치모델 결과를 ERA5/GLORYS 재분석자료, 관측소·계류(mooring) 시계열, 위성자료와 비교·검증할 때 쓰는 **시계열·신호 분석 방법 카탈로그**다. 단순 오차지표(RMSE 등)가 "값이 얼마나 다른가"를 본다면, 여기 방법들은 "**언제·어떤 주파수에서·어떤 위상(phase)으로** 다른가"를 본다. 즉 시간지연(lag), 위상·진폭 오차, 추세·계절성, 변동성·변화점, 시간-주파수 구조, 비선형 시간정렬(DTW)을 정량화한다. 이 카탈로그는 도메인(기상/파랑/수온/해류/해수면)에 무관하게 적용 가능한 신호처리 기반 검증 레시피의 토대다.

> **자료형 메모(NetCDF 격자 + CSV/텍스트 시계열).** 본 카탈로그의 거의 모든 방법은 *단일 1차원 시계열*에 정의된다. NetCDF 격자자료(모델·재분석·위성)는 (a) 관측 위치로 보간한 **점 시계열**, (b) **영역평균 시계열**, 또는 (c) **격자점별로 방법을 반복 적용**해 결과를 지도화하는 방식으로 처리한다. CSV/텍스트 시계열(조위·부이·계류·기상관측)은 그대로 적용한다. 비교 전 반드시 시간축 정렬·결측 처리(맨 아래 "시간 정합·리샘플링·결측 처리" 카드)를 선행한다.

이 파일에 담은 방법(한 줄 목차):
- **시간 정합·리샘플링·결측 처리 (Temporal alignment / resampling / gap handling)** — 모든 비교의 전처리 전제
- **교차상관·시간지연 (Cross-correlation / Lagged correlation)** — 두 시계열 간 최적 lag와 지연된 상관
- **위상·진폭 오차 (Phase & Amplitude error)** — 주기신호의 위상지연·진폭비 (특히 조석·일주기)
- **자기상관·부분자기상관 (ACF / PACF)** — 기억구조·유효자유도·잔차 백색성 진단
- **STL 분해 (Seasonal-Trend decomposition using LOESS)** — 추세·계절·잔차 분리
- **고전적 가법/승법 분해 (Classical decomposition)** — 이동평균 기반 단순 분해
- **계절기후값·조화적합 (Climatological seasonal cycle / annual+semiannual harmonic fit)** — 계절순환 비교
- **추세 검정 (Mann-Kendall / Sen's slope)** — 단조 추세 유무·기울기 비모수 검정
- **변화점 탐지 (Change-point detection: Pettitt, CUSUM, PELT, BCP)** — 평균·분산 급변 시점
- **디지털 필터링 (이동평균 / 저역 / 대역; Butterworth, Lanczos, Godin)** — 조석제거·subtidal 추출
- **분산·변동성 비교 (Variance ratio / F-test / Levene)** — 변동성 과소·과대 모의 진단
- **스펙트럼 분석 (PSD, Welch)** — 주파수별 에너지 분포 비교
- **멀티테이퍼 스펙트럼 추정 (Multitaper / Thomson MTM)** — 짧은 기록의 저분산·저편향 스펙트럼
- **롬-스카글 주기도 (Lomb-Scargle periodogram)** — 불균등·결측 표본의 스펙트럼
- **교차스펙트럼·코히어런스·위상 (Cross-spectrum / Coherence / Phase)** — 주파수별 상관·위상지연
- **어드미턴스·게인·전달함수 (Admittance / Gain / Transfer function)** — 주파수별 응답비(강제력→응답)
- **Spectral Diagram (스펙트럼 다이어그램)** — 주파수영역 모델 성능 요약(Taylor 유사)
- **연속웨이블릿 변환 (CWT)** — 시간-주파수 국소 에너지
- **교차웨이블릿·웨이블릿 코히어런스 (XWT / WTC)** — 두 시계열의 시간-주파수 공통구조·위상
- **단시간 푸리에 변환·스펙트로그램 (STFT)** — 시간에 따른 스펙트럼 변화
- **힐베르트 변환 (Hilbert transform: 순간 진폭·위상·주파수)** — 협대역 신호 포락선·위상
- **경험적 모드분해·HHT (EMD / EEMD / Hilbert-Huang)** — 비선형·비정상 신호 적응분해
- **특이스펙트럼분석 (SSA)** — 추세·진동·노이즈의 데이터 적응 분리
- **상관차원·장기기억 (Detrended Fluctuation Analysis, DFA / 스펙트럼 경사)** — 변동의 스케일링·기억 진단
- **동적시간왜곡 (DTW)** — 비선형 시간정렬 기반 형상 유사도
- **정점·계류 시계열 비교 종합 레시피 (Point/Mooring comparison workflow)** — 정렬·QC·지표 묶음

---

### 시간 정합·리샘플링·결측 처리 (시간 정합/리샘플링/결측 / Temporal alignment, resampling & gap handling)
- **무엇을 측정/검증하나**: 분석 방법이 아니라 **모든 시계열 비교의 전제 전처리**. 모델·재분석·관측·위성을 공통 시간축에 올려, 정렬·보간·결측에서 비롯되는 **가짜 편향·가짜 lag·스펙트럼 누설**을 막는다.
- **정의·수식(절차)**: (1) 시간대 통일(모두 UTC), (2) 공통 등간격 격자로 resample(평균/순간/누적의 의미 구분 — 예: 강수 누적 vs 순간 수위), (3) 보간(선형/스플라인/최근접; 등간격이 깨지면 스펙트럼·필터 왜곡), (4) 결측 플래그·QC 마스크 전파(한쪽 결측 시점은 양쪽에서 제외하거나 명시적 보간), (5) 위성 통과시각·관측 보고주기를 모델 출력시각에 매칭(±윈도우 평균 또는 최근접 시각).
- **적용 도메인/자료형**: 전 도메인. 특히 **불균등 표본**(위성 궤도 통과, 결측 많은 부이)과 **상이한 시간해상도**(시간별 모델 vs 6시간 재분석 vs 일별 위성) 결합 시 필수.
- **입력·전제**: 정확한 시각 메타데이터(타임존·기준시각·평균구간), 변수의 누적/순간 성격, 결측 코드 규약.
- **해석 기준**: 정렬 전후로 기본지표(bias/RMSE/상관)가 크게 바뀌면 정합 오류 의심. 보간 비율(결측률)을 함께 보고 — 보간 과다 시 고주파 지표·스펙트럼 신뢰도 저하.
- **한계·주의**: **선형보간은 고주파 에너지를 깎아** PSD·분산비를 왜곡; 등간격 가정이 깨진 자료에 FFT/Welch를 그대로 쓰면 안 됨(→ Lomb-Scargle). 누적·순간 변수 혼동, 시간대 오프셋은 흔하고 치명적인 가짜 위상오차 원인.
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (전처리·보간 장); Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* (시계열 정렬·결측); 불균등표본 스펙트럼은 VanderPlas (2018, 아래 Lomb-Scargle 카드 참조).

---

### 교차상관·시간지연 (교차상관 / Cross-correlation & Lagged correlation)
- **무엇을 측정/검증하나**: 모델과 관측 두 시계열 사이의 **시간지연(lag)** 과 그 지연에서의 상관. 모델이 사건(고조위, 폭풍, 전선통과)을 관측보다 **얼마나 빨리/늦게** 모의하는지 진단.
- **정의·수식**: 표본 교차상관계수
  $r_{xy}(k) = \dfrac{\sum_{t}(x_t-\bar x)(y_{t+k}-\bar y)}{\sqrt{\sum_t (x_t-\bar x)^2}\sqrt{\sum_t (y_t-\bar y)^2}}$,
  최적 지연 $k^\* = \arg\max_k r_{xy}(k)$. 양의 $k^\*$는 한 신호가 다른 신호를 선행함을 의미(부호 규약 주의).
- **적용 도메인/자료형**: 모든 도메인의 시계열(수위/유속/수온/파고/기압). 격자자료는 격자점별 또는 영역평균 시계열로 환산해 적용.
- **입력·전제**: 동일·등간격 시간축으로 정렬(resample/보간), 결측 처리, 가급적 사전 detrend. 신뢰구간 산정 시 정상성(stationarity) 가정.
- **해석 기준**: $k^\*\approx 0$이고 $r$이 높으면 시점 일치 양호. 큰 $|k^\*|$는 위상오차/이류속도 오차 시사. 관행적 유의 임계 $\approx 2/\sqrt{N}$(백색잡음 기준).
- **한계·주의**: **자기상관이 강하면 가짜 lag·상관 과대평가**(유효표본수 감소). 사전 prewhitening 또는 유효자유도 보정 권장. 비정상 신호엔 부적합.
- **출처**: Box, Jenkins & Reinsel, *Time Series Analysis: Forecasting and Control*; Emery & Thomson, *Data Analysis Methods in Physical Oceanography*; Pyper & Peterman (1998) "Comparison of methods to account for autocorrelation in correlation analyses of fish data", *Can. J. Fish. Aquat. Sci.* 55:2127-2140 — 교차상관/상관 분석의 자기상관 편향과 유효자유도 보정(검색 확인).

---

### 위상·진폭 오차 (위상·진폭 오차 / Phase & Amplitude error)
- **무엇을 측정/검증하나**: 준주기 신호(조석, 일주기 수온·해륙풍, 관성진동 등)에서 모델이 **언제 정점에 도달하는가(위상)** 와 **진폭을 얼마나 크게/작게 모의하는가**.
- **정의·수식**: 특정 주기성분을 조화적합 $A\cos(\omega t-\phi)$로 추정 후 위상오차 $\Delta\phi=\phi_{model}-\phi_{obs}$(시간환산 $\Delta t=\Delta\phi/\omega$), 진폭비 $A_{model}/A_{obs}$. 조석은 조화상수 비교: 진폭오차 $\Delta H = H_{m}-H_{o}$, 위상지각오차 $\Delta g = g_{m}-g_{o}$, 종합지표로 분조별 RSS(벡터차) 또는 평균 진폭오차.
- **적용 도메인/자료형**: 조석·조류(해수면/유속), 일주기 변동(수온/풍속), 시계열·정점.
- **입력·전제**: 충분히 긴 연속기록(조석은 주요분조 분리에 보통 ≥29일~1년), 조화분석(t_tide/UTide) 또는 협대역 필터 후 Hilbert.
- **해석 기준**: 조석 검증 관행으로 주요 반일주조(M2) 진폭오차·위상오차를 cm·도(°) 단위로 보고; 위상오차 수 분~수십 분, 진폭오차 수 cm 이내면 양호(해역·목적별 상이). 진폭비 1에 가까울수록 좋음. 분조별 벡터차(complex error)를 RSS로 합산해 단일 skill로 요약하기도 함.
- **한계·주의**: 분조 분리 부정확 시 위상오차 왜곡. 비정상·과도현상엔 단일 위상 정의가 모호 → 웨이블릿/Hilbert로 시간변화 위상 추적. 위상 wrap-around(±180°) 주의.
- **출처**: Pawlowicz, Beardsley & Lentz (2002) T_TIDE, *Computers & Geosciences* 28:929-937; Codiga (2011) UTide 기술보고서; Foreman (1977) 조석분석 매뉴얼; Pugh, *Tides, Surges and Mean Sea-Level*.

---

### 자기상관·부분자기상관 (자기상관/부분자기상관 / ACF & PACF)
- **무엇을 측정/검증하나**: 시계열의 **기억(메모리) 구조**와 잔차의 백색성. 검증 잔차(모델-관측)에 구조가 남아있는지, 유효자유도는 얼마인지 진단.
- **정의·수식**: 자기상관 $\rho(k)=\dfrac{\sum_t (x_t-\bar x)(x_{t+k}-\bar x)}{\sum_t (x_t-\bar x)^2}$. 부분자기상관(PACF)은 중간 시차 영향을 제거한 시차 $k$ 직접상관(Durbin-Levinson). 유효표본수 $N_{eff}\approx N\dfrac{1-\rho_1}{1+\rho_1}$ 류 근사.
- **적용 도메인/자료형**: 모든 시계열, 잔차 진단. 격자는 격자점별.
- **입력·전제**: (약)정상성, 등간격, 결측 보간.
- **해석 기준**: 잔차 ACF가 신뢰대($\pm 2/\sqrt N$) 안에 들면 백색 → 모델이 시간구조를 잘 설명. ACF가 느리게 감쇠하면 비정상/추세 잔존. PACF 절단점으로 AR 차수 가늠. 백색성 종합검정은 Ljung-Box Q.
- **한계·주의**: 상관 유의성 계산은 정상성 가정에 민감. 강한 자기상관은 다른 모든 상관기반 지표(교차상관, t-검정)의 유의도를 과대평가하므로 반드시 동반 점검.
- **출처**: Box, Jenkins & Reinsel, *Time Series Analysis*; Wilks, *Statistical Methods in the Atmospheric Sciences*(유효표본수); Chatfield, *The Analysis of Time Series*; Ljung & Box (1978) 잔차 백색성 검정, *Biometrika* 65:297-303.

---

### STL 분해 (LOESS 기반 계절-추세 분해 / Seasonal-Trend decomposition using LOESS)
- **무엇을 측정/검증하나**: 시계열을 **추세(trend) + 계절(seasonal) + 잔차(remainder)** 로 분리. 모델과 관측을 각 성분별로 비교(예: 모델이 계절진폭을 과소모의, 추세 부호가 다름 등).
- **정의·수식**: $Y_t = T_t + S_t + R_t$. 내부 루프에서 LOESS(국소가중회귀)로 계절·추세를 번갈아 평활, 외부 루프에서 robustness weight로 이상치 영향 축소.
- **적용 도메인/자료형**: 계절성이 뚜렷한 시계열(월·일 수온, 해수면, 풍속). 격자는 격자점별 분해 후 성분 지도화.
- **입력·전제**: 등간격, 주기 길이 지정, 충분한 주기 수(보통 ≥2~3주기). 결측은 사전 보간 또는 STL 변형 사용.
- **해석 기준**: 추세·계절 성분을 모델/관측 간 직접 비교(상관, RMSE, 진폭비). 잔차의 분산비로 미설명 변동 비교. STL은 임계값보다 **성분별 정량비교**의 전처리로 활용.
- **한계·주의**: 평활 파라미터(seasonal/trend window)에 결과가 민감. 계절성이 빠르게 변하거나 다중 계절성이면 MSTL 등 확장 필요. 비선형 추세는 LOESS span에 의존.
- **출처**: Cleveland, Cleveland, McRae & Terpenning (1990) "STL: A Seasonal-Trend Decomposition Procedure Based on Loess", *J. Official Statistics* 6(1):3-73; Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*(STL 장, otexts.com/fpp3/stl.html); 다중계절 확장 MSTL — Bandara, Hyndman & Bergmeir (2021), arXiv:2107.13462(검색 확인).

---

### 고전적 가법/승법 분해 (고전 분해 / Classical additive/multiplicative decomposition)
- **무엇을 측정/검증하나**: 이동평균 기반의 단순 추세·계절 분리. STL보다 가볍고 직관적.
- **정의·수식**: 가법 $Y_t=T_t+S_t+R_t$(또는 승법 $Y_t=T_t\cdot S_t\cdot R_t$). 추세 $T_t$는 중심이동평균, 계절 $S_t$는 detrend 후 주기 평균.
- **적용 도메인/자료형**: 계절성 명확·간단 진단용 시계열.
- **입력·전제**: 등간격, 정수 주기, 계절성이 시간에 따라 (거의) 일정.
- **해석 기준**: 성분별 모델/관측 비교(진폭·위상·잔차분산).
- **한계·주의**: 계절성 시변·이상치에 약함(이동평균이 양끝 결측·완충). 정밀 비교엔 STL 권장.
- **출처**: Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*(Classical decomposition); Chatfield, *The Analysis of Time Series*.

---

### 계절기후값·조화적합 (계절기후값/연·반년주기 조화적합 / Climatological seasonal cycle & harmonic fit)
- **무엇을 측정/검증하나**: 모델과 재분석/관측의 **평균 계절순환(seasonal climatology)** 일치도. 해수온·해수면·풍속 등에서 모델이 계절최대/최소의 **시기(위상)·진폭·평균수준**을 맞추는지. ERA5/GLORYS 대비 모델의 계절오차 진단에 표준적.
- **정의·수식**: 월별/일별 기후값 $\bar x_m=\frac1{N_m}\sum x$, 또는 조화적합 $x(t)\approx \mu + a_1\cos(\omega_a t)+b_1\sin(\omega_a t)+a_2\cos(2\omega_a t)+b_2\sin(2\omega_a t)$ ($\omega_a=2\pi/1\text{yr}$; 연주기+반년주기). 계절진폭 $=\sqrt{a_1^2+b_1^2}$, 위상(최대월)으로 환산.
- **적용 도메인/자료형**: 장기 시계열(≥수년), 재분석·위성 기후값 비교. 격자는 격자점별 기후값 지도(계절진폭·위상 지도).
- **입력·전제**: 동일 기준기간(climatology period) 일치(예: 1991-2020), 충분한 연수, 결측 균형(특정 계절 편중 결측 주의).
- **해석 기준**: 계절진폭비 $\approx1$, 위상(최대 도달월) 차 ≤약 0.5~1개월이면 양호. 평균(연중 mean) bias는 별도. 모델 계절진폭 과소는 혼합·확산 과다 신호일 수 있음.
- **한계·주의**: 기준기간·연수가 다르면 직접비교 부적절. 추세가 크면 기후값에 추세 혼입 → 사전 detrend 또는 공통기간 사용. 연주기만 보지 말고 반년주기까지(특히 적도·몬순역).
- **출처**: von Storch & Zwiers, *Statistical Analysis in Climate Research*(계절순환·조화분석); Wilks, *Statistical Methods in the Atmospheric Sciences*; 표준 기후값 산정 관행은 WMO 기후 정상값 지침(WMO-No.1203, 표준 지침, 확인요).

---

### 추세 검정 (Mann-Kendall 추세검정 / Sen 기울기 / Mann-Kendall & Sen's slope)
- **무엇을 측정/검증하나**: 시계열에 **단조 증가/감소 추세**가 통계적으로 있는지(비모수), 그 기울기 크기. 모델과 관측의 장기 추세 일치 검증.
- **정의·수식**: MK 통계 $S=\sum_{i<j}\mathrm{sgn}(x_j-x_i)$, 표준화 $Z$로 유의성. Sen's slope = 모든 쌍 기울기 $(x_j-x_i)/(j-i)$의 중앙값.
- **적용 도메인/자료형**: 기후·해양 장기 시계열(해수면 상승, 수온 추세). 격자는 격자점별 추세지도.
- **입력·전제**: 독립성(자기상관 시 변형 MK: Hamed-Rao, prewhitened MK 필요), 결측 허용.
- **해석 기준**: $p<0.05$면 유의 추세. 모델·관측 추세 부호·크기 비교; Sen slope 신뢰구간 겹침 여부로 정합 판정.
- **한계·주의**: 자기상관·계절성에 민감 → 계절 Mann-Kendall, prewhitening 사용. 단조 가정(비단조 변동엔 부적합).
- **출처**: Mann (1945) *Econometrica* 13:245-259; Kendall, *Rank Correlation Methods*; Sen (1968) *JASA* 63:1379-1389; Hamed & Rao (1998) 자기상관 보정 MK, *J. Hydrology* 204:182-196; 기후 추세 분석의 표준 관행은 WMO 기후 분석 지침(표준 참고문헌, 확인요).

---

### 변화점 탐지 (변화점 탐지 / Change-point detection)
- **무엇을 측정/검증하나**: 시계열의 **평균·분산·추세가 급변하는 시점**. 모델/관측에서 레짐 전환(예: 계절전환, 센서 교체, 모델 재시동 불연속) 위치·일치 검증.
- **정의·수식**: 대표기법
  - **Pettitt 검정**: 비모수, 단일 평균변화점 위치·유의성(Mann-Whitney 기반 $U_{t,N}$ 최대).
  - **CUSUM**: 누적합 $C_t=\sum_{i\le t}(x_i-\mu_0)$의 이탈로 평균 변화 감지(Page 1954).
  - **PELT / Binary Segmentation**: 벌점화 비용최소화로 다중 변화점($\min \sum \mathcal{C}(\text{seg}) + \beta\cdot m$).
  - **Bayesian (BCP / BOCPD)**: 변화점 위치의 사후확률, 온라인 탐지 가능.
- **적용 도메인/자료형**: 모든 시계열; QC(불연속·점프 탐지), 레짐 비교.
- **입력·전제**: 변화 유형(평균/분산/기울기) 사전 지정, 노이즈 모형 가정. 벌점 $\beta$ 선택(BIC/MBIC).
- **해석 기준**: 탐지 변화점의 시점·개수를 모델/관측 간 대조. 사후확률·p값으로 신뢰도. 동일 사건에 대한 시점차로 위상오차 보조 해석.
- **한계·주의**: 벌점·민감도 설정에 따라 과탐/미탐. 자기상관·계절성은 가짜 변화점 유발 → 사전 제거 권장. 단일 vs 다중 변화점 기법 구분.
- **출처**: Page (1954) CUSUM, *Biometrika* 41:100-115; Pettitt (1979) "A non-parametric approach to the change-point problem", *Appl. Statist.* 28:126-135; Killick, Fearnhead & Eckley (2012) PELT, *JASA* 107:1590-1598; Adams & MacKay (2007) Bayesian Online Changepoint Detection, arXiv:0710.3742; Aminikhanghahi & Cook (2017) "A Survey of Methods for Time Series Change Point Detection", *Knowl. Inf. Syst.* 51:339-367; Reeves et al. (2007) 기후 변화점 비교, *J. Appl. Meteor. Climatol.* 46:900-915(검색 확인).

---

### 디지털 필터링 (디지털 필터: 이동평균/저역/대역 / Digital filtering: moving-average, low-/band-pass)
- **무엇을 측정/검증하나**: 특정 주파수대 분리 — 조석 제거(detiding) 후 **subtidal(잔차류·폭풍해일)** 추출, 또는 일주기·관성·계절대역 추출 후 모델/관측 비교.
- **정의·수식**: 이동평균(단순/가중), FIR(코사인-Lanczos, Godin 24-24-25 이동평균조합), IIR(Butterworth). 저역 차단 $f_c$, 대역 $[f_1,f_2]$. Butterworth는 재귀필터라 **전후방 양방향(filtfilt)** 으로 위상지연 제거.
- **적용 도메인/자료형**: 해수면·유속·수온 시계열(조석 vs 비조석 분리). 격자는 시간축 따라 격자별 필터.
- **입력·전제**: 등간격, 충분한 길이(가장자리 효과로 양끝 손실), 차단주파수 선택. Nyquist 한계 준수.
- **해석 기준**: 필터링 후 성분 시계열로 상관·RMSE·분산비 재계산. Godin/Lanczos는 조석제거 성능 차이가 보고됨(Godin 24-24-25 등이 잔여 조석 누설 적음).
- **한계·주의**: 비양방향 IIR은 위상왜곡; 가장자리(edge) 손실; 차단 부근 누설(leakage). 과도한 평활은 신호 손실.
- **출처**: Roberts & Roberts (1978) "Use of the Butterworth low-pass filter for oceanographic data", *J. Geophys. Res. Oceans* 83(C11):5510-5514; Thompson (1983) "Low-pass filters to suppress inertial and tidal frequencies", *J. Phys. Oceanogr.* 13:1077-1083; Godin, *The Analysis of Tides*; Duchon (1979) Lanczos filtering, *J. Appl. Meteor.* 18:1016-1022.

---

### 분산·변동성 비교 (분산·변동성 비교 / Variance & variability comparison)
- **무엇을 측정/검증하나**: 모델이 관측의 **변동성(분산)을 과소/과대 모의**하는지. 표준편차비는 Taylor 다이어그램의 한 축이기도 함.
- **정의·수식**: 분산비 $\sigma_{m}^2/\sigma_{o}^2$ 또는 표준편차비 $\sigma_m/\sigma_o$. 유의검정: F-검정(정규·독립 가정), Levene/Brown-Forsythe(정규성 완화), Bartlett. 시변 변동성은 이동표준편차·GARCH류.
- **적용 도메인/자료형**: 모든 시계열; 격자별 분산지도. 변동성 클러스터링이 있는 신호(파랑 군집 등).
- **입력·전제**: 동일 표본·기간 정렬, 자기상관 시 유효자유도 보정(F-검정 신뢰성 저하).
- **해석 기준**: 비 $\approx 1$이면 변동성 일치. <1 과소분산(모델 과평활), >1 과대분산. 계절·대역별로 나눠 보면 진단력↑.
- **한계·주의**: F-검정은 정규성·독립성에 매우 민감 → 비모수/robust 검정 병행. 추세·계절 제거 후 비교 권장.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences*; Taylor (2001) 표준편차비, *JGR* 106:7183-7192; von Storch & Zwiers, *Statistical Analysis in Climate Research*; Levene (1960); Brown & Forsythe (1974) *JASA* 69:364-367.

---

### 스펙트럼 분석 (출력스펙트럼밀도 / Power Spectral Density, Welch)
- **무엇을 측정/검증하나**: 신호 에너지의 **주파수별 분포**. 모델이 특정 주파수(조석분조, 일주기, 중규모, 고주파)에 충분한/과도한 에너지를 갖는지 비교.
- **정의·수식**: PSD $S_{xx}(f)=|\hat X(f)|^2$ 추정. Welch법: 구간분할·창함수(Hann 등)·평균으로 분산 저감. 적분 $\int S\,df=\sigma^2$(Parseval).
- **적용 도메인/자료형**: 파고·유속·수온·해수면 시계열. 격자는 점별 PSD 또는 파수-주파수 스펙트럼.
- **입력·전제**: 등간격, 정상성(구간 내), detrend·창함수로 누설 저감, 충분한 길이(주파수 분해능 $\Delta f=1/T$).
- **해석 기준**: 모델/관측 PSD를 로그-로그로 겹쳐 보고 피크 위치·기울기(스펙트럼 경사) 비교. 고주파 에너지 부족 = 모델 평활/확산 과다. 분조 피크 정합으로 조석 검증.
- **한계·주의**: 비정상·과도신호엔 평균 스펙트럼이 오도. 창·구간 선택이 분산-편향 trade-off. 자유도(평균 구간 수)로 신뢰구간. 불균등 표본엔 부적합(→ Lomb-Scargle).
- **출처**: Welch (1967) *IEEE Trans. Audio Electroacoust.* 15:70-73; Percival & Walden, *Spectral Analysis for Physical Applications*; Emery & Thomson, *Data Analysis Methods in Physical Oceanography*.

---

### 멀티테이퍼 스펙트럼 추정 (멀티테이퍼 / Multitaper, Thomson MTM)
- **무엇을 측정/검증하나**: Welch와 같은 목적(주파수별 에너지)이되, **짧거나 잡음 많은 기록**에서 누설을 억제하면서 분산을 낮춘 스펙트럼. 분조·협대역 피크의 유의성 검정(harmonic F-test)에 강점.
- **정의·수식**: 서로 직교하는 다수의 DPSS(Slepian) 테이퍼 $w^{(k)}$로 각각 스펙트럼을 추정 후 평균: $\hat S(f)=\frac1K\sum_{k=1}^K |\sum_t w^{(k)}_t x_t e^{-i2\pi f t}|^2$. 시간-대역폭 $NW$와 테이퍼 수 $K\approx 2NW-1$로 분해능–분산 절충.
- **적용 도메인/자료형**: 기록이 짧은 계류·위성 시계열, 약한 협대역 신호(분조, 관성·근관성 피크) 탐지. 격자는 점별.
- **입력·전제**: 등간격, $NW$·$K$ 선택, (약)정상성.
- **해석 기준**: 모델/관측 MTM 스펙트럼·신뢰구간 비교; 피크 유의성은 Thomson harmonic F-test로 판정. 분조 피크의 진폭·유의성 정합.
- **한계·주의**: $NW$가 크면 분해능↓(피크 뭉개짐), 작으면 분산↑. 비정상·불균등 표본엔 한계(→ 웨이블릿/Lomb-Scargle).
- **출처**: Thomson (1982) "Spectrum estimation and harmonic analysis", *Proc. IEEE* 70:1055-1096; Percival & Walden, *Spectral Analysis for Physical Applications*(DPSS·MTM); Ghil et al. (2002) *Rev. Geophys.* 40(MTM 응용).

---

### 롬-스카글 주기도 (롬-스카글 주기도 / Lomb-Scargle periodogram)
- **무엇을 측정/검증하나**: **불균등 표본·결측이 많은** 시계열의 주파수 스펙트럼·주기성. 위성 통과(궤도 반복), 결측 잦은 부이·조위, 비정기 관측에서 FFT를 못 쓸 때의 표준 대안.
- **정의·수식**: 최소제곱으로 각 시험주파수 $\omega$에 사인·코사인을 적합한 것과 동치인 주기도. 시간 오프셋 $\tau$를 도입해 위상 불변·통계분포가 깔끔해지도록 정의(Scargle 1982). 일반화(GLS)는 평균·가중·오차를 포함.
- **적용 도메인/자료형**: 위성 시계열(SLA, SST), 결측 많은 관측 시계열, 비정기 샘플. 격자는 점별.
- **입력·전제**: 시각(불균등 허용)과 값(가능하면 측정오차), 시험주파수 격자. 평균제거·정규화.
- **해석 기준**: 피크 주파수·검정력으로 주기성 판정; 거짓경보확률(false-alarm probability)로 유의성. 모델(균등)과 관측(불균등)을 같은 주파수에서 비교하려면 모델도 동일 시각으로 표본화(샘플링 윈도우 효과 일치).
- **한계·주의**: 불균등 샘플링은 **스펙트럼 창(window)에 가짜 피크(aliasing/주야 7d·궤도주기)** 를 만든다 — window/spectral window를 함께 점검. 강한 추세·비정상엔 제한적.
- **출처**: Lomb (1976) *Astrophys. Space Sci.* 39:447-462; Scargle (1982) *Astrophys. J.* 263:835-853; VanderPlas (2018) "Understanding the Lomb–Scargle Periodogram", *Astrophys. J. Suppl. Ser.* 236:16(검색 확인).

---

### 교차스펙트럼·코히어런스·위상 (교차스펙트럼/코히어런스/위상 / Cross-spectrum, Coherence, Phase)
- **무엇을 측정/검증하나**: 두 시계열의 **주파수별 상관(코히어런스)** 과 **주파수별 위상지연**. 모델/관측이 어느 대역에서 동조하고 어디서 위상이 어긋나는지.
- **정의·수식**: 교차스펙트럼 $S_{xy}(f)$, 코히어런스 $\gamma^2(f)=\dfrac{|S_{xy}(f)|^2}{S_{xx}(f)S_{yy}(f)}\in[0,1]$, 위상 $\theta(f)=\arg S_{xy}(f)$(→ 시간지연 $\tau=\theta/2\pi f$).
- **적용 도메인/자료형**: 강제력-응답(바람-수위, 기압-해일), 모델-관측 시계열 쌍. 격자는 점별.
- **입력·전제**: Welch식 평균(코히어런스 추정에 필수, 평균 없으면 $\gamma^2\equiv1$), 등간격 정렬.
- **해석 기준**: 고코히어런스 대역에서 위상으로 lead/lag 해석. 코히어런스 유의수준 $\approx 1-\alpha^{1/(L-1)}$(L=평균 세그먼트 수). 모델이 관측과 고코히어런스+영위상이면 우수.
- **한계·주의**: 평균 세그먼트 수 부족 시 코히어런스 과대. 비선형·비정상엔 웨이블릿 코히어런스 권장.
- **출처**: Bendat & Piersol, *Random Data: Analysis and Measurement Procedures*; Emery & Thomson, *Data Analysis Methods in Physical Oceanography*; Priestley, *Spectral Analysis and Time Series*.

---

### 어드미턴스·게인·전달함수 (어드미턴스/게인/전달함수 / Admittance, Gain, Transfer function)
- **무엇을 측정/검증하나**: 강제력(입력 $x$)에서 응답(출력 $y$)으로의 **주파수별 응답비(게인)와 위상**. 예: 기압→해수면(역기압 반응), 바람→유속/수위, 평형조→실측조(조석 어드미턴스). 모델이 응답의 크기·시간지연을 맞추는지.
- **정의·수식**: 전달함수 $H(f)=S_{xy}(f)/S_{xx}(f)$, 게인 $|H(f)|$, 위상 $\arg H(f)$. 조석 어드미턴스 = 관측분조 진폭/평형조 진폭, 위상지각. 코히어런스 $\gamma^2$로 추정 신뢰도 평가.
- **적용 도메인/자료형**: 강제력-응답 쌍이 있는 해양·해수면(기압·바람·평형조 ↔ 수위·유속). 격자는 점별.
- **입력·전제**: 입력·출력 동시 시계열, Welch식 평균, 선형·정상 가정. 조석 어드미턴스는 평형조 진폭표 필요.
- **해석 기준**: 모델/관측 게인·위상 곡선을 주파수별 비교(고코히어런스 대역만). 역기압 반응은 이론값(약 -1 cm/hPa) 근처여야; 어긋나면 응답 물리·마찰·공명 모의 오류.
- **한계·주의**: 저코히어런스 대역의 게인·위상은 무의미. 비선형 응답(천해 조석·공명)엔 선형 전달함수 한계. 잡음이 입력에도 있으면 게인 편향.
- **출처**: Bendat & Piersol, *Random Data*(전달함수·게인·위상); Munk & Cartwright (1966) "Tidal spectroscopy and prediction"(조석 어드미턴스), *Phil. Trans. R. Soc. A* 259:533-581; Wunsch (1972) 역기압 반응 관련(검색 확인); Pugh, *Tides, Surges and Mean Sea-Level*.

---

### Spectral Diagram (스펙트럼 다이어그램 / Spectral Diagram)
- **무엇을 측정/검증하나**: 주파수영역에서 모델 성능을 **한 그림으로 요약**(Taylor 다이어그램의 주파수판). 이산 주파수별로 코히어런스·파워·진폭·위상·skill을 함께 표시.
- **정의·수식**: 각 목표 주파수에서 모델/관측 스펙트럼의 코히어런스·진폭비·위상차를 기반으로 한 skill 점수를 극좌표/Taylor류로 배치(여러 주파수를 한 평면에 점으로).
- **적용 도메인/자료형**: 조석 포함 해양순환모델 등 주파수 구조가 중요한 검증(예: 조위관측소 vs 모델 해수면의 8개 주요 분조 M2,S2,N2,K2,K1,O1,P1,Q1). 시계열·격자점.
- **입력·전제**: 모델·관측 동일기간 스펙트럼, 비교할 이산 주파수(분조·일주기 등) 선정.
- **해석 기준**: 점이 기준(관측)에 가까울수록 해당 주파수 성능 우수. 분조별로 진폭·위상오차를 동시에 가늠. 위상오차는 조석 모의의 주요 오차원으로 강조됨.
- **한계·주의**: 비교적 새로운 도구로 구현·해석 표준화 진행 중. 주파수 선택·정규화·skill 정의에 결과 의존.
- **출처**: **Calim Costa, M., Nobre, P., Oke, P., Schiller, A., Siqueira, L. San Pedro, Castelão, G.P. (2022)** "The Spectral Diagram as a new tool for model assessment in the frequency domain: Application to a global ocean general circulation model with tides", *Computers & Geosciences* 159:104977, doi:10.1016/j.cageo.2021.104977(검색 확인; 구현 코드 GitHub mabelcalim/SpecDiag). 개념적 토대는 Taylor (2001). ※ 이전 판의 "Lavergne et al. (2021)" 표기는 **오기**여서 정정함.

---

### 연속웨이블릿 변환 (연속 웨이블릿 변환 / Continuous Wavelet Transform, CWT)
- **무엇을 측정/검증하나**: 신호 에너지의 **시간-주파수(스케일) 국소 분포**. 비정상 신호에서 "언제 어느 주기 성분이 강했나"를 본다.
- **정의·수식**: $W_x(s,\tau)=\int x(t)\,\frac{1}{\sqrt s}\psi^\*\!\Big(\frac{t-\tau}{s}\Big)dt$. 보통 Morlet 모웨이블릿(시간-주파수 균형). 파워 $|W_x|^2$.
- **적용 도메인/자료형**: 폭풍·계절전환 등 비정상 해양·기상 시계열. 격자는 점별.
- **입력·전제**: 등간격, 가장자리 영향 영역인 **영향원뿔(cone of influence, COI)** 밖만 신뢰, 적색잡음 대비 유의성 검정.
- **해석 기준**: 유의 파워 구역(COI 내, 신뢰구간 95%)에서 에너지 집중 시기·주기 비교. 모델/관측 파워맵 시각 대조. 특정 대역의 scale-averaged wavelet power로 시변 에너지 비교.
- **한계·주의**: 스케일-주파수 환산 근사, 경계효과(COI), 모웨이블릿 선택 의존. 정량비교는 XWT/WTC로 보완.
- **출처**: Torrence & Compo (1998) "A Practical Guide to Wavelet Analysis", *Bull. Amer. Meteor. Soc.* 79:61-78; Daubechies, *Ten Lectures on Wavelets*.

---

### 교차웨이블릿·웨이블릿 코히어런스 (교차웨이블릿/웨이블릿 코히어런스 / XWT & WTC)
- **무엇을 측정/검증하나**: 두 시계열(모델·관측, 또는 강제력·응답)의 **시간-주파수 공통 파워(XWT)** 와 **국소 상관(WTC)**, 그리고 **위상 관계(화살표)**.
- **정의·수식**: 교차웨이블릿 $W_{xy}=W_x W_y^\*$, 위상 $\arg(W_{xy})$. 웨이블릿 코히어런스 $R^2=\dfrac{|S(s^{-1}W_{xy})|^2}{S(s^{-1}|W_x|^2)\,S(s^{-1}|W_y|^2)}\in[0,1]$ (S는 평활연산자). 위상화살표: →동위상(in-phase), ←역위상, 화살표 방향으로 lead/lag 판독.
- **적용 도메인/자료형**: 비정상 관계(엘니뇨-해수온, 바람-파고, 모델-관측) 진단. 시계열·격자점.
- **입력·전제**: 등간격, COI 밖 영역만 해석, 적색잡음 배경 대비 Monte Carlo 유의성.
- **해석 기준**: 고코히어런스 구역에서 위상으로 시간지연·인과 가설 점검. 모델이 관측과 동위상·고코히어런스면 우수. WTC는 시간-주파수판 국소 상관계수로 해석.
- **한계·주의**: 평활 파라미터·모웨이블릿 의존, 다변량은 부분/다중 웨이블릿 코히어런스 필요. 위상화살표는 인과의 충분조건 아님.
- **출처**: Grinsted, Moore & Jevrejeva (2004) "Application of the cross wavelet transform and wavelet coherence to geophysical time series", *Nonlinear Processes in Geophysics* 11:561-566 (npg.copernicus.org/articles/11/561/2004); Torrence & Compo (1998); Ng & Chan (2012) 부분·다중 웨이블릿 코히어런스, *J. Atmos. Oceanic Technol.* 29:1845-1853.

---

### 단시간 푸리에 변환·스펙트로그램 (단시간 푸리에 변환 / Short-Time Fourier Transform, STFT)
- **무엇을 측정/검증하나**: 창을 이동시키며 계산한 **시간에 따른 스펙트럼 변화(스펙트로그램)**. 비정상 신호의 주파수 천이 진단.
- **정의·수식**: $\mathrm{STFT}(t,f)=\int x(\tau)\,w(\tau-t)\,e^{-i2\pi f\tau}d\tau$. 스펙트로그램 $=|\mathrm{STFT}|^2$.
- **적용 도메인/자료형**: 파랑 스펙트럼의 시간변화, 폭풍 통과, 계절 천이. 시계열·격자점.
- **입력·전제**: 창 길이 선택(시간-주파수 분해능 trade-off), 등간격, 창 중첩.
- **해석 기준**: 모델/관측 스펙트로그램의 피크 천이·에너지 분포를 시간대별 비교.
- **한계·주의**: 창 길이가 고정되어 모든 주파수에 동일 분해능(웨이블릿은 적응형). 누설·경계효과.
- **출처**: Oppenheim & Schafer, *Discrete-Time Signal Processing*; Allen (1977) STFT, *IEEE Trans. ASSP* 25:235-238; Holthuijsen, *Waves in Oceanic and Coastal Waters*(파랑 스펙트럼).

---

### 힐베르트 변환 (힐베르트 변환: 순간 진폭·위상·주파수 / Hilbert transform)
- **무엇을 측정/검증하나**: 협대역 신호의 **순간 포락선(진폭)·순간 위상·순간 주파수**. 시변 진폭·위상 오차를 시간 함수로 추적.
- **정의·수식**: 해석신호 $z(t)=x(t)+i\,\mathcal{H}\{x\}(t)=A(t)e^{i\phi(t)}$. 포락선 $A(t)=|z|$, 순간위상 $\phi(t)=\arg z$, 순간주파수 $f(t)=\frac{1}{2\pi}\frac{d\phi}{dt}$.
- **적용 도메인/자료형**: 조석·관성진동 등 협대역 성분의 진폭·위상 변조 추적. 시계열.
- **입력·전제**: **반드시 협대역**(먼저 대역통과 필터 후 적용) — 광대역 신호에 적용하면 위상·주파수 무의미. 등간격.
- **해석 기준**: 모델/관측 순간진폭(포락선)·순간위상을 시간에 따라 비교(상관, 위상차). 조석 변조·관성진동 감쇠율 비교.
- **한계·주의**: 광대역 적용이 가장 흔한 오류; 가장자리 효과; 잡음 민감. EMD와 결합 시(HHT) 다성분 가능.
- **출처**: Feldman (2009) "Hilbert Transform, Envelope, Instantaneous Phase, and Frequency", in *Encyclopedia of Structural Health Monitoring*, Wiley; Huang et al. (1998); Boashash (1992) instantaneous frequency, *Proc. IEEE* 80:520-538.

---

### 경험적 모드분해·HHT (경험적 모드분해 / Empirical Mode Decomposition, EMD/EEMD, Hilbert-Huang)
- **무엇을 측정/검증하나**: 비선형·비정상 신호를 데이터 적응적으로 **내재모드함수(IMF) + 잔차추세**로 분해. 각 IMF에 Hilbert를 적용해(HHT) 시변 진폭·주파수 비교.
- **정의·수식**: $x(t)=\sum_j c_j(t) + r(t)$, $c_j$는 IMF(극값-영점 조건). EEMD: 백색잡음 앙상블을 더해 평균 → 모드혼합(mode mixing) 완화.
- **적용 도메인/자료형**: 비정상 해양·기상 시계열(추세+다중 진동). 시계열·격자점.
- **입력·전제**: 등간격, 노이즈 진폭·앙상블 수(EEMD) 설정, 경계처리.
- **해석 기준**: 모델/관측의 동일 차수 IMF(유사 시간스케일) 진폭·에너지·순간주파수 비교; 잔차로 추세 비교.
- **한계·주의**: 수학적 근거가 알고리즘적(이론 보장 약함), 모드혼합·끝단효과, IMF 물리해석 주의. CEEMDAN 등 개선판 존재.
- **출처**: Huang et al. (1998) "The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis", *Proc. R. Soc. A* 454:903-995; Wu & Huang (2009) EEMD, *Adv. Adapt. Data Anal.* 1:1-41; Torres et al. (2011) CEEMDAN, *ICASSP*.

---

### 특이스펙트럼분석 (특이스펙트럼분석 / Singular Spectrum Analysis, SSA)
- **무엇을 측정/검증하나**: 시계열을 **추세·준주기 진동·노이즈**로 데이터 적응 분해(궤적행렬 SVD). 모델/관측의 주요 진동모드 비교, 결측 보간, 노이즈 제거.
- **정의·수식**: 지연임베딩으로 궤적행렬 구성 → SVD → 성분 그룹화 → 대각평균(재구성). 고유삼중항(eigentriple)이 진동쌍을 이룸.
- **적용 도메인/자료형**: ENSO·계절·준주기 해양 신호, 결측 많은 시계열. 다변량 확장(MSSA).
- **입력·전제**: 윈도우 길이 $L$ 선택($\le N/2$), 성분 그룹화 판단(고유값 스펙트럼·w-correlation).
- **해석 기준**: 재구성 성분(RC)을 모델/관측 간 비교(상관·진폭). 주요 진동주기·기여율 대조.
- **한계·주의**: $L$·그룹화에 주관 개입; 성분 혼합 가능; 비정상 강하면 해석 주의.
- **출처**: Vautard, Yiou & Ghil (1992) "Singular-spectrum analysis: A toolkit for short, noisy chaotic signals", *Physica D* 58:95-126; Ghil et al. (2002) "Advanced spectral methods for climatic time series", *Rev. Geophys.* 40(1):1003; Golyandina & Zhigljavsky, *Singular Spectrum Analysis for Time Series*.

---

### 상관차원·장기기억 (탈추세변동분석 / Detrended Fluctuation Analysis, DFA & 스펙트럼 경사)
- **무엇을 측정/검증하나**: 변동의 **스케일링(scaling)·장기기억(long-range dependence)** 특성. 모델이 관측의 변동 스케일링(예: 적색잡음 지수, 1/f 거동)을 재현하는지 — 단순 분산비를 넘어 "변동이 스케일에 따라 어떻게 커지나"를 본다.
- **정의·수식**: 누적합 프로파일을 길이 $n$ 구간으로 나눠 국소 다항추세 제거 후 변동 $F(n)=\sqrt{\langle (\text{잔차})^2\rangle}\sim n^{\alpha}$. 스케일링 지수 $\alpha$(=0.5 백색, >0.5 지속성/장기기억, <0.5 반지속). 등가로 PSD 경사 $S(f)\sim f^{-\beta}$, $\beta\approx 2\alpha-1$.
- **적용 도메인/자료형**: 수온·해수면·유속·기온 등 비정상 변동의 스케일링 비교. 격자는 점별.
- **입력·전제**: 충분한 길이(여러 스케일 확보), 등간격(불균등은 변형 필요), 추세차수 선택.
- **해석 기준**: 모델/관측 $\alpha$(또는 PSD 경사 $\beta$) 비교 — 일치하면 다중스케일 변동구조 재현 양호. 모델 $\alpha$가 작으면 고주파 평활/장기기억 부족.
- **한계·주의**: 짧은 기록·교차점(crossover)에서 단일 $\alpha$ 부적절; 계절성·강한 추세는 사전 제거. PSD 경사 추정은 주파수 적합구간 선택에 민감.
- **출처**: Peng et al. (1994) "Mosaic organization of DNA nucleotides"(DFA 원전), *Phys. Rev. E* 49:1685-1689; Kantelhardt et al. (2001) DFA 특성, *Physica A* 295:441-454; 기후 장기기억·적색잡음 배경은 von Storch & Zwiers, *Statistical Analysis in Climate Research*.

---

### 동적시간왜곡 (동적 시간 왜곡 / Dynamic Time Warping, DTW)
- **무엇을 측정/검증하나**: 두 시계열을 **시간축으로 비선형 정렬**해 형상(shape) 유사도를 측정. 모델이 사건의 **타이밍은 어긋나도 패턴(형상)** 은 맞추는지 평가 — 위상오차에 관대한 거리.
- **정의·수식**: 누적비용 $D(i,j)=d(x_i,y_j)+\min\{D(i-1,j),D(i,j-1),D(i-1,j-1)\}$, DTW 거리=최적 워핑경로의 누적비용. Sakoe-Chiba band 등 워핑 제약.
- **적용 도메인/자료형**: 강수·폭풍해일·솔라윈드·Dst 등 사건 타이밍이 어긋나기 쉬운 시계열 검증. 길이가 다른 시계열도 비교 가능.
- **입력·전제**: 워핑밴드(최대 허용 시간이동) 설정, 진폭 정규화 여부 결정, 등간격 권장.
- **해석 기준**: DTW 거리 작을수록 형상 일치. 워핑경로의 대각 이탈량으로 **시간지연 구조**를 시각화·정량화(국소 lag). RMSE가 위상오차로 과벌점할 때 보완지표로 사용.
- **한계·주의**: 진폭차에 둔감(형상 중심) → 진폭검증과 병행. 무제약 워핑은 과도정렬(병리적 매칭) → 밴드 제약 필수. 계산비용 $O(NM)$(FastDTW로 완화).
- **출처**: Sakoe & Chiba (1978) "Dynamic programming algorithm optimization for spoken word recognition", *IEEE Trans. ASSP* 26:43-49; Berndt & Clifford (1994) AAAI Workshop; Laperre, Amaya & Lapenta (2020) "Dynamic Time Warping as a New Evaluation for Dst Forecast with Machine Learning", *Front. Astron. Space Sci.* 7:39(arXiv:2006.04667, 검색 확인); Dilmi, Barthès, Mallet et al. (2020) "Iterative multiscale dynamic time warping (IMs-DTW): a tool for rainfall time series comparison", *Int. J. Data Sci. Anal.*, doi:10.1007/s41060-019-00193-1(검색 확인).

---

### 정점·계류 시계열 비교 종합 레시피 (정점·계류 비교 워크플로 / Point & Mooring time-series comparison)
- **무엇을 측정/검증하나**: 모델 격자값을 관측소/계류(buoy, ADCP, 조위관측소) 위치·깊이로 추출해 비교하는 **표준 절차** — 위 방법들을 묶는 메타-레시피.
- **정의·수식(절차)**:
  1. **공간 정합**: 모델 격자→관측 위치 보간(최근접/이중선형), 깊이층 정합(연직보간).
  2. **시간 정합**: 공통 시간축 resample, 시간대(UTC) 통일, 결측·플래그 처리(맨 위 "시간 정합" 카드).
  3. **품질관리(QC)**: 스파이크·범위·정체값(stuck) 제거, 변화점으로 센서 불연속 점검.
  4. **편향/추세 처리**: 평균편차 제거 여부, detrend, (필요시) 조석 필터링.
  5. **지표 산출**: 기본오차(RMSE/MAE/bias)+상관, 교차상관 lag, 위상·진폭(조화), PSD/코히어런스, 분산비, (선택) DTW·웨이블릿 코히어런스.
  6. **요약 시각화**: Taylor/Spectral diagram, 산점도, 시계열 오버레이.
- **적용 도메인/자료형**: 모든 정점 관측(수위·유속·수온·파고·기상요소). 격자모델 ↔ 점관측.
- **입력·전제**: 정확한 관측 메타데이터(위치·깊이·계기), 시간동기, 단위·기준면 통일(예: 해수면 기준 datum).
- **해석 기준**: 도메인·목적별 임계는 각 방법 카드 참조. 다지표 종합(값·위상·주파수·변동성)으로 판정.
- **한계·주의**: 대표성 오차(격자 vs 점), 보간/연직정합 오차, datum·시간대 불일치가 가짜 편향을 만든다. 단일 지표 맹신 금지.
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography*; Stow et al. (2009) "Skill assessment for coupled biological/physical models of marine systems", *J. Marine Systems* 76:4-15; WMO/IOC-JCOMM 해양·파랑 검증 지침(표준 참고문헌, 정확한 문서번호·판본 확인요).

---

## 출처 (References)

표준 교과서·지침 (실재 확인)
- Box, G.E.P., Jenkins, G.M., Reinsel, G.C. *Time Series Analysis: Forecasting and Control.* Wiley.
- Chatfield, C. *The Analysis of Time Series: An Introduction.* Chapman & Hall.
- Emery, W.J., Thomson, R.E. *Data Analysis Methods in Physical Oceanography.* Elsevier.
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences.* Academic Press. (유효표본수, 분산검정)
- von Storch, H., Zwiers, F.W. *Statistical Analysis in Climate Research.* Cambridge Univ. Press.
- Percival, D.B., Walden, A.T. *Spectral Analysis for Physical Applications.* Cambridge Univ. Press. (멀티테이퍼·DPSS)
- Bendat, J.S., Piersol, A.G. *Random Data: Analysis and Measurement Procedures.* Wiley. (교차스펙트럼·코히어런스·전달함수)
- Priestley, M.B. *Spectral Analysis and Time Series.* Academic Press.
- Oppenheim, A.V., Schafer, R.W. *Discrete-Time Signal Processing.* Pearson.
- Hyndman, R.J., Athanasopoulos, G. *Forecasting: Principles and Practice* (3rd ed.). OTexts. https://otexts.com/fpp3/ (STL·고전분해·정렬)
- Golyandina, N., Zhigljavsky, A. *Singular Spectrum Analysis for Time Series.* Springer.
- Godin, G. *The Analysis of Tides.* Univ. of Toronto Press.
- Pugh, D. *Tides, Surges and Mean Sea-Level.* Wiley.
- Holthuijsen, L.H. *Waves in Oceanic and Coastal Waters.* Cambridge Univ. Press.

핵심 논문 (실재 확인)
- Cleveland, R.B., Cleveland, W.S., McRae, J.E., Terpenning, I. (1990) STL: A Seasonal-Trend Decomposition Procedure Based on Loess. *Journal of Official Statistics* 6(1):3-73.
- Torrence, C., Compo, G.P. (1998) A Practical Guide to Wavelet Analysis. *Bull. Amer. Meteor. Soc.* 79:61-78.
- Grinsted, A., Moore, J.C., Jevrejeva, S. (2004) Application of the cross wavelet transform and wavelet coherence to geophysical time series. *Nonlinear Processes in Geophysics* 11:561-566. https://npg.copernicus.org/articles/11/561/2004
- Ng, E.K.W., Chan, J.C.L. (2012) Geophysical applications of partial/multiple wavelet coherence. *J. Atmos. Oceanic Technol.* 29:1845-1853.
- Huang, N.E. et al. (1998) The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis. *Proc. R. Soc. A* 454:903-995.
- Wu, Z., Huang, N.E. (2009) Ensemble Empirical Mode Decomposition (EEMD). *Adv. Adapt. Data Anal.* 1:1-41.
- Feldman, M. (2009) Hilbert Transform, Envelope, Instantaneous Phase, and Frequency. In *Encyclopedia of Structural Health Monitoring*, Wiley.
- Vautard, R., Yiou, P., Ghil, M. (1992) Singular-spectrum analysis: A toolkit for short, noisy chaotic signals. *Physica D* 58:95-126.
- Ghil, M. et al. (2002) Advanced spectral methods for climatic time series. *Rev. Geophys.* 40(1):1003.
- Sakoe, H., Chiba, S. (1978) Dynamic programming algorithm optimization for spoken word recognition. *IEEE Trans. ASSP* 26:43-49.
- Welch, P.D. (1967) The use of FFT for the estimation of power spectra. *IEEE Trans. Audio Electroacoust.* 15:70-73.
- Thomson, D.J. (1982) Spectrum estimation and harmonic analysis (multitaper). *Proc. IEEE* 70:1055-1096.
- Page, E.S. (1954) Continuous inspection schemes (CUSUM). *Biometrika* 41:100-115.
- Pettitt, A.N. (1979) A non-parametric approach to the change-point problem. *Appl. Statist.* 28:126-135.
- Killick, R., Fearnhead, P., Eckley, I.A. (2012) Optimal detection of changepoints with linear computational cost (PELT). *JASA* 107:1590-1598.
- Adams, R.P., MacKay, D.J.C. (2007) Bayesian Online Changepoint Detection. arXiv:0710.3742.
- Aminikhanghahi, S., Cook, D.J. (2017) A Survey of Methods for Time Series Change Point Detection. *Knowledge and Information Systems* 51:339-367.
- Mann, H.B. (1945) Nonparametric tests against trend. *Econometrica* 13:245-259.
- Sen, P.K. (1968) Estimates of the regression coefficient based on Kendall's tau. *JASA* 63:1379-1389.
- Hamed, K.H., Rao, A.R. (1998) A modified Mann-Kendall trend test for autocorrelated data. *J. Hydrology* 204:182-196.
- Ljung, G.M., Box, G.E.P. (1978) On a measure of lack of fit in time series models. *Biometrika* 65:297-303.
- Roberts, J., Roberts, T.D. (1978) Use of the Butterworth low-pass filter for oceanographic data. *J. Geophys. Res. Oceans* 83(C11):5510-5514.
- Thompson, R.O.R.Y. (1983) Low-pass filters to suppress inertial and tidal frequencies. *J. Phys. Oceanogr.* 13:1077-1083.
- Duchon, C.E. (1979) Lanczos filtering in one and two dimensions. *J. Appl. Meteor.* 18:1016-1022.
- Pawlowicz, R., Beardsley, B., Lentz, S. (2002) Classical tidal harmonic analysis with errors using T_TIDE. *Computers & Geosciences* 28:929-937.
- Codiga, D.L. (2011) Unified Tidal Analysis and Prediction Using the UTide Matlab Functions. Technical Report.
- Munk, W.H., Cartwright, D.E. (1966) Tidal spectroscopy and prediction. *Phil. Trans. R. Soc. A* 259:533-581. (어드미턴스)
- Taylor, K.E. (2001) Summarizing multiple aspects of model performance in a single diagram. *J. Geophys. Res.* 106:7183-7192.
- Stow, C.A. et al. (2009) Skill assessment for coupled biological/physical models of marine systems. *J. Marine Systems* 76:4-15.
- Pyper, B.J., Peterman, R.M. (1998) Comparison of methods to account for autocorrelation in correlation analyses of fish data. *Can. J. Fish. Aquat. Sci.* 55:2127-2140.
- Lomb, N.R. (1976) Least-squares frequency analysis of unequally spaced data. *Astrophys. Space Sci.* 39:447-462.
- Scargle, J.D. (1982) Studies in astronomical time series analysis. II. *Astrophys. J.* 263:835-853.
- Peng, C.-K. et al. (1994) Mosaic organization of DNA nucleotides (DFA). *Phys. Rev. E* 49:1685-1689.

확인 필요(검색으로 출처 일부만 확보 — 인용 전 원문 확인 권장)
- **Calim Costa, M., Nobre, P., Oke, P., Schiller, A., Siqueira, L. San Pedro, Castelão, G.P. (2022)** The Spectral Diagram as a new tool for model assessment in the frequency domain: Application to a global ocean general circulation model with tides. *Computers & Geosciences* 159:104977. doi:10.1016/j.cageo.2021.104977. — 저자·DOI는 ADS/검색으로 확인(구현 코드: GitHub mabelcalim/SpecDiag). **종전 "Lavergne et al. (2021)" 표기는 오기였음.**
- Laperre, B., Amaya, J., Lapenta, G. (2020) Dynamic Time Warping as a New Evaluation for Dst Forecast with Machine Learning. *Front. Astron. Space Sci.* 7:39. arXiv:2006.04667. — 검색 확인.
- Dilmi, M.D., Barthès, L., Mallet, C. et al. (2020) Iterative multiscale dynamic time warping (IMs-DTW): a tool for rainfall time series comparison. *Int. J. Data Sci. Anal.* doi:10.1007/s41060-019-00193-1. — 검색으로 제목·저널·DOI 확인(권/페이지 원문 확인 권장).
- VanderPlas, J.T. (2018) Understanding the Lomb–Scargle Periodogram. *Astrophys. J. Suppl. Ser.* 236:16. — 검색 확인(권/페이지 재확인 권장).
- Bandara, K., Hyndman, R.J., Bergmeir, C. (2021) MSTL: A Seasonal-Trend Decomposition Algorithm for Time Series with Multiple Seasonal Patterns. arXiv:2107.13462. — 검색 확인.
- WMO/IOC-JCOMM 해양·파랑·기후 검증 지침 및 WMO 기후 정상값 지침(WMO-No.1203) — 표준 지침으로 인용하되 정확한 문서번호·판본 확인 요망.
