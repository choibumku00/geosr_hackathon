# 도메인: 수문·하천 (Hydrology / Streamflow) 검증·분석 방법 카탈로그

이 문서는 수문·수리 모델(HEC-HMS, VIC, SWAT, mHM, GR4J, HYPE, LISFLOOD, WRF-Hydro/NWM, 육상표면모형 CLM/Noah-MP 등)이 산출한 **하천유량(river discharge / streamflow)·유출(runoff)·저수량**을 관측(수위관측소·유량관측소 hydrometric station), 위성·재분석 유출자료(GRACE TWS, GloFAS·ERA5-Land runoff, GRDC/USGS/WRIS 관측망)와 비교·검증하기 위한 분석/검증 방법을 메서드 카드 형식으로 망라한다. 수문 검증의 핵심 3축은 **(1) 유량곡선(hydrograph)의 전체 적합도(KGE/KGE'·NSE·PBIAS·RSR), (2) 수문서명(hydrological signatures: 유황곡선 FDC·기저지수 BFI·감수상수·저수기 지수·수문곡선 사건지표)으로 본 "물리적 거동" 재현, (3) 극치(홍수빈도 GEV/GPD·재현주기, 저수 극치)와 물수지 닫힘(water balance closure)**이다. 정점(관측소) 시계열이 1급 자료형이며, 격자 유출장·위성 TWS·홍수범람 격자도 다룬다.

> **자료형 표기 약어**: [시계열]=관측소 유량/수위 CSV·일/시 시계열, [격자]=NetCDF 격자(모델 runoff·TWS·범람지도), [위성]=GRACE TWS·위성고도계 하천수위·SWOT, [프로파일]=단면 유속/수위(선택).
> **"우리 모델 vs 관측/재분석" 비교에 바로 쓸 수 있는 방법**은 카드 머리에 ★ 표시했다.
> **공통 지표(RMSE·MAE·bias·상관·Taylor/Target·QQ·bootstrap·GEV/GPD 엔진·KS)는 여기서 재정의하지 않고 01·03·06·figures/16으로 교차링크**만 한다. 이 카드들은 수문 고유의 정의·전제·해석만 담는다.

## 이 파일에 담은 방법 (한 줄 목차)
- ★ **Nash–Sutcliffe 효율 NSE / lnNSE / 변형 NSE** — 유량곡선 전체 설명력(→01 교차링크)
- ★ **Kling–Gupta 효율 KGE / KGE'(2012) / non-parametric KGE** — 상관·편향·변동 분해
- ★ **KGE 성분 분해 (r·β·α/γ)** — 어느 축이 문제인지 진단
- ★ **백분율 편향 PBIAS** — 수량 물수지 치우침(→01 교차링크)
- ★ **RSR (RMSE-관측표준편차 비)** — 정규화 RMSE(Moriasi 등급, →01 교차링크)
- **로그·박스콕스·제곱근 변환 유량 평가** — 저유량 가중(lnNSE 등)
- ★ **유황곡선 (Flow Duration Curve, FDC)** — 초과확률-유량 서명
- ★ **FDC 서명 지표 (Q5·Q95·FHV·FLV·FMS·slope)** — 고/저/중 구간 오차
- ★ **기저유출 분리와 기저지수 (Baseflow separation / BFI)** — 디지털필터·기저비율
- ★ **감수분석 / 감수상수 (Recession analysis, Master Recession Curve, k)** — 저류-방류 거동
- ★ **저수기 지수 (Low-flow indices: Q95·7Q10·MAM7·BFI)** — 갈수·가뭄 극치
- ★ **홍수빈도 분석 (Flood frequency: 연최대-GEV / POT-GPD / 재현주기)** — 설계홍수(→03 교차링크)
- ★ **첨두유량 크기·시각 오차 (Peak flow magnitude & timing error)** — 사건 첨두 진단
- ★ **수문곡선 사건지표 (Hydrograph event metrics: 첨두·용적·시간중심·상승/하강)** — 사건단위 평가
- ★ **유출용적·유출률 (Runoff volume / runoff ratio, 물수지)** — 총량 일치
- ★ **물수지 닫힘 (Water balance closure: P−ET−Q−ΔS)** — 수지 잔차 진단(→04 교차링크)
- ★ **유출시기·계절성 (Flow timing: 유출중심일 CT, 계절성·pulse 지표)** — 융설·계절 위상
- ★ **융설 유출 시기·눈수당량 (Snowmelt timing / SWE, SCA)** — 융설지배 유역
- **이중적산곡선 / 이중질량 (Double-mass curve)** — 일관성·비정상성 점검
- ★ **범주형·임계 초과 검증 (홍수경보 POD·FAR·CSI)** — 경보유량 초과(→03 교차링크)
- ★ **홍수범람 공간검증 (Flood extent: CSI/critical success·Fit)** — 격자 침수역 일치
- ★ **GRACE 지하수·저수량 검증 (Terrestrial Water Storage anomaly)** — 위성 저류변화
- **위성 하천수위·SWOT 대조 (Satellite altimetry / SWOT discharge)** — 무측정 하천
- **저수지·댐 운영 검증 (Reservoir storage / release / rule curve)** — 저수량·방류·규정수위
- ★ **다목적·다서명 진단 프레임 (Multi-signature / benchmark: mean-flow·기후 benchmark)** — 단일지표 함정 회피
- **불확실성·유의성 (bootstrap CI·유효표본, 관측유량 rating error)** — 신뢰구간(→01 교차링크)

---

### ★ Nash–Sutcliffe 효율 (NSE / lnNSE / 변형 NSE)
- 무엇을 측정/검증하나: 모델 유량곡선이 관측 평균 대비 분산을 얼마나 설명하는지. 수문학에서 가장 오래·널리 쓰인 유량곡선 전체 적합도 지표.
- 정의·수식: NSE = 1 − Σ(Qsim−Qobs)² / Σ(Qobs−Q̄obs)². 범위 (−∞, 1], 1=완전, 0=평균예측 수준, <0=평균보다 못함. **lnNSE**는 유량에 log를 취해 계산 → 저유량(갈수) 가중. 공통 오차 정의(RMSE·MSE 분해)는 **→ 01_error_statistics.md** 참조.
- 적용 도메인·자료형: 하천유량 [시계열](관측소 일/시 유량). 격자 유출도 지점 집계 후 적용.
- 입력·전제: 동일 시각 정렬된 매치업. 결측·QC 처리. 유량 단위 통일(m³/s). 관측유량은 수위–유량 관계식(rating curve)으로 환산된 2차 산출임을 유의.
- 해석 기준(advisory): Moriasi et al.(2007) 월단위 관행 등급(NSE>0.50 satisfactory, >0.65 good, >0.75 very good)이 널리 인용되나 **일/시 단위·건조유역·소유역에서는 훨씬 낮게 나오는 것이 정상** — 등급은 영역·시간해상도·기후 의존이며 good/bad 단정 금지(→ §G4). 계절성이 강한 유역은 분모(관측분산)가 커져 NSE가 후하게 나옴.
- 한계·주의: 제곱오차라 **첨두(고유량)에 크게 가중** → 저유량 재현이 나빠도 높게 나올 수 있음(lnNSE·KGE 병행 필수). "평균유량 예측(benchmark)"을 못 이기면 NSE<0 → 반드시 benchmark 대비 상대평가(→ 다목적·benchmark 카드, §G6). 계절기후값을 benchmark로 쓰면 NSE 기준이 더 엄격해짐.
- 출처: Nash & Sutcliffe (1970, *Journal of Hydrology* 10(3):282–290); Moriasi et al. (2007, *Transactions of the ASABE* 50(3):885–900); Krause, Boyle & Bäse (2005, *Advances in Geosciences* 5:89–97, NSE·lnNSE 비교); Schaefli & Gupta (2007, *HESS* 11:1267–1277, benchmark 관점).

---

### ★ Kling–Gupta 효율 (KGE / KGE′ 2012 / non-parametric KGE)
- 무엇을 측정/검증하나: 유량 재현을 **상관(r)·편향비(bias ratio)·변동비(variability ratio)** 세 성분으로 균형 있게 통합. NSE의 "첨두 편중·평균 과소가 유리해지는" 함정을 보완.
- 정의·수식: KGE = 1 − √[(r−1)² + (β−1)² + (γ−1)²]. r=피어슨 상관, β=μ_sim/μ_obs(편향비), γ=CV_sim/CV_obs=(σ_sim/μ_sim)/(σ_obs/μ_obs)(변동비). **KGE′(Kling 2012)**는 변동비를 α=σ_sim/σ_obs로 바꾸고 β와의 상호상관을 제거(수자원 응용에서 권장). **non-parametric KGE(Pool 2018)**는 스피어만 상관+FDC 기반 변동으로 이상치에 강건. 범위 (−∞,1].
- 적용 도메인·자료형: 하천유량 [시계열] 1순위. 격자 유출 지점 집계, 다지점 종합.
- 입력·전제: 정렬 매치업, 양(+) 유량(β·CV에 0/음수 취약). log-KGE로 저유량 강조 가능.
- 해석 기준(advisory): **KGE≈−0.41이 "평균유량 benchmark와 동등"** 지점(Knoben et al. 2019) — NSE=0과 직접 대응되지 않으므로 "KGE>0이면 좋음"으로 오독 금지. 관행상 KGE>0.75 매우 양호, 0.5~0.75 양호로 보고되나 영역·해상도·기후 의존(→§G4). 건조·간헐하천에서 낮게 나오는 것이 정상.
- 한계·주의: KGE와 KGE′는 값이 다르므로 어느 정의인지 명시. 성분(r·β·γ) 함께 보고해야 진단 가능(다음 카드). 간헐/영유량(zero-flow) 하천은 CV·log 처리에서 불안정.
- 출처: Gupta, Kling, Yilmaz & Martinez (2009, *Journal of Hydrology* 377(1–2):80–91, doi:10.1016/j.jhydrol.2009.08.003); Kling, Fuchs & Paulin (2012, *Journal of Hydrology* 424–425:264–277, KGE′); Knoben, Freer & Woods (2019, *HESS* 23:4323–4331, doi:10.5194/hess-23-4323-2019, NSE↔KGE 비교); Pool, Vis & Seibert (2018, *Hydrological Sciences Journal* 63(13–14):1941–1953, non-parametric KGE); Clark et al. (2021, *WRR*, KGE 사용 시 주의).

---

### ★ KGE 성분 분해 (r · β · α/γ 진단)
- 무엇을 측정/검증하나: 낮은 KGE의 **원인**을 세 축으로 분리 — 위상/형상 문제(r 낮음), 물수지 치우침(β≠1), 변동성 과대/과소(α 또는 γ≠1).
- 정의·수식: 위 KGE 정의의 개별 성분을 각각 보고·시각화(성분별 막대·삼각 레이더). β>1=과대추정, α<1=변동 과소(첨두 눌림·유량곡선 평탄화 흔함).
- 적용 도메인·자료형: 하천유량 [시계열]·다지점 [격자].
- 입력·전제: KGE와 동일.
- 해석 기준(advisory): r은 timing/형상, β는 총량, α는 진폭 문제를 가리킴. "α<1 & r 양호"면 첨두 과소(저류 과다·강우입력 과소 등 가설). 원인 귀속은 가설일 뿐 단정 금지.
- 한계·주의: 성분은 서로 독립이 아님(β·γ 상호작용 → KGE′로 완화). 단일 성분만으로 결론 금지.
- 출처: Gupta et al. (2009); Kling et al. (2012); Mizukami et al. (2019, *HESS* 23:2601–2614, KGE 성분 기반 보정 논의).

---

### ★ 백분율 편향 (PBIAS, Percent Bias)
- 무엇을 측정/검증하나: 모델 유량의 계통적 과대/과소를 관측 총량 대비 %로. 물수지(총유출량) 치우침 진단의 표준.
- 정의·수식: PBIAS = 100 · Σ(Qsim−Qobs) / Σ(Qobs). (부호규약 주의: 일부 코드는 100·Σ(Qobs−Qsim)/ΣQobs로 정의해 부호가 반대 → 보고 시 명시.) 일반 bias/MAE 정의는 **→ 01_error_statistics.md**.
- 적용 도메인·자료형: 유량·유출용적 [시계열]/[격자].
- 입력·전제: 정렬 매치업, 동일 기간·결측 처리(부분기간이면 총량 왜곡). 
- 해석 기준(advisory): Moriasi(2007) 유량 관행 등급 |PBIAS|<10 very good, 10~15 good, 15~25 satisfactory(월단위·유역 규모 기준). 유사·영양물질은 임계가 다름. 등급은 영역·시간해상도 의존이며 절대기준 아님(→§G4).
- 한계·주의: 양·음 오차가 상쇄되면 0에 가까워도 곡선이 틀릴 수 있음(KGE β와 병행). 저유량 기간이 총량에 거의 기여 안 해 갈수 오차를 못 잡음.
- 출처: Moriasi et al. (2007, *Transactions of the ASABE* 50(3)); Gupta, Sorooshian & Yapo (1999, *Journal of Hydrologic Engineering* 4(2), PBIAS·다목적).

---

### ★ RSR (RMSE–관측표준편차 비, RMSE-observations Standard deviation Ratio)
- 무엇을 측정/검증하나: RMSE를 관측 표준편차로 정규화해 유역·변수 간 비교 가능하게 만든 지표(NSE와 수학적으로 연결).
- 정의·수식: RSR = RMSE / STDEV_obs = √Σ(Qsim−Qobs)² / √Σ(Qobs−Q̄obs)². 관계: RSR = √(1−NSE). RMSE 자체 정의는 **→ 01_error_statistics.md / figures/16**.
- 적용 도메인·자료형: 유량 [시계열]/[격자].
- 입력·전제: 정렬 매치업.
- 해석 기준(advisory): Moriasi(2007) RSR≤0.50 very good … ≤0.70 satisfactory(월단위). NSE와 1:1 대응이므로 둘 중 하나만 보고해도 무방하나 관행상 병기. 영역·해상도 의존(→§G4).
- 한계·주의: NSE와 동일한 첨두 편중 한계를 공유. 단독 사용 금지.
- 출처: Moriasi et al. (2007); Singh et al. (2004, *ASAE* 관련, RSR 사용 사례).

---

### 로그·박스콕스·제곱근 변환 유량 평가 (저유량 가중)
- 무엇을 측정/검증하나: 유량의 큰 동적범위(홍수~갈수 수십~수천 배) 때문에 원자료 지표는 첨두에 지배됨 → 변환으로 **저·중유량 재현**을 평가.
- 정의·수식: log(Q+ε), √Q, 또는 Box–Cox(λ) 변환 후 NSE/KGE/RMSE 계산(lnNSE, KGE_log). ε(작은 상수)로 0유량 처리; ε 선택이 결과에 영향.
- 적용 도메인·자료형: 유량 [시계열] 저유량·갈수 평가.
- 입력·전제: 양(+)변환 가능한 유량, ε·λ 규약 명시(모델·관측 동일). 
- 해석 기준(advisory): log 지표가 원지표보다 낮으면 저유량 재현이 약함(반대면 첨두가 약함). 변환·ε에 민감하므로 여러 변환 병행 권장.
- 한계·주의: ε가 소유량 구간을 인위적으로 지배할 수 있음. 간헐하천 0유량 다수면 log 부적합 → 별도 zero-flow 지표.
- 출처: Krause, Boyle & Bäse (2005, *Advances in Geosciences* 5:89–97); Oudin et al. (2006, *WRR*, 변환 기준 논의); Santos, Thirel & Perrin (2018, *HESS* 22, Box–Cox·평가함수).

---

### ★ 유황곡선 (Flow Duration Curve, FDC)
- 무엇을 측정/검증하나: 유량이 특정 값을 초과하는 시간비율(초과확률)을 나타내는 누적 서명. 모델이 유량의 **전체 분포·변동성 구조**(홍수~갈수)를 재현하는지 시간정렬 없이 진단.
- 정의·수식: 유량을 내림차순 정렬, 초과확률 p = m/(n+1)(Weibull plotting position) 대 Q(p)를 반로그로 도시. Q5·Q95(각 5%·95% 초과유량) 등 백분위로 요약. 분포비교 일반론(QQ/CDF/KS)은 **→ 03·06 및 figures/16**.
- 적용 도메인·자료형: 유량 [시계열]. 격자 유출도 셀별 FDC 가능.
- 입력·전제: 동일 기간·동일 plotting position. 관측·모델 동일 결측 처리(FDC는 결측·기간 차에 민감).
- 해석 기준(advisory): 고유량단(좌측, 낮은 p)에서 모델이 1:1 아래면 첨두 과소; 저유량단(우측, 높은 p)에서 벌어지면 갈수 재현 불량. 곡선 기울기(FDC slope)는 유역 반응성/변동성을 나타냄.
- 한계·주의: 분포만 비교(동시성·timing 못 봄) → KGE/NSE와 상보적. 기간이 다르면 직접비교 불가. 로그축이라 시각적 과소평가 유의.
- 출처: Vogel & Fennessey (1994, *Journal of Water Resources Planning and Management* 120(4):485–504); Searcy (1959, USGS Water-Supply Paper 1542-A, FDC 표준); WMO, *Manual on Low-flow Estimation and Prediction* (WMO-No. 1029).

---

### ★ FDC 서명 지표 (Q5·Q95·FHV·FLV·FMS·slope)
- 무엇을 측정/검증하나: FDC를 구간별로 나눠 **고유량 편향(high-flow), 저유량 편향(low-flow), 중간구간 기울기** 오차를 정량화 — 유량곡선 신호 진단의 핵심 서명 집합(Yilmaz et al. 2008).
- 정의·수식: %BiasFHV(상위 2% 고유량 용적 편향), %BiasFLV(하위 30% 저유량 용적 편향, 로그공간), %BiasFMS(중간 20~70% 구간 FDC 기울기 편향), Q5/Q95 편향. 각 % 편향 = 100·(sim−obs)/obs 형태.
- 적용 도메인·자료형: 유량 [시계열] 진단. 다유역 서명 벤치마킹.
- 입력·전제: 신뢰할 FDC(충분 기간), 저유량 로그공간 계산 시 0유량 처리.
- 해석 기준(advisory): FHV 음(−)=첨두 과소, FLV 양(+)=저유량 과대 등. 구간 정의(2%/30%/20~70%)는 Yilmaz 규약이며 문헌마다 다름 → 명시 필요. 임계는 advisory(→§G4).
- 한계·주의: 서명은 관측 rating error·결측에 민감("good signatures go bad", McMillan 2023). 여러 서명 조합으로 해석.
- 출처: Yilmaz, Gupta & Wagener (2008, *WRR* 44, W09417, doi:10.1029/2007WR006716); McMillan, Westerberg & Krueger (2018, *WIREs Water*, 서명 리뷰); McMillan et al. (2023, *Hydrological Processes* 37, doi:10.1002/hyp.14987, "When good signatures go bad").

---

### ★ 기저유출 분리와 기저지수 (Baseflow separation / BFI)
- 무엇을 측정/검증하나: 총유량을 지표유출(직접)과 기저유출(지하수 기여)로 분리해 **기저지수 BFI=기저용적/총용적**을 모델·관측 간 비교. 모델이 저류-방류 물리를 옳게 재현하는지.
- 정의·수식: 디지털 재귀필터(Lyne–Hollick 1979; Eckhardt 2005의 2-파라미터 필터 BFI_max·α), 또는 UKIH/HYSEP 최소값법으로 기저유량 b_t 산출 → BFI = Σb_t/ΣQ_t. Eckhardt: b_t = [(1−BFI_max)α·b_{t−1} + (1−α)BFI_max·Q_t]/(1−α·BFI_max).
- 적용 도메인·자료형: 유량 [시계열] 일자료. 격자 유출은 직접 분리 어려움.
- 입력·전제: 연속 일유량, 필터 파라미터(α·BFI_max)·통과횟수(passes) 모델·관측 동일 적용. 
- 해석 기준(advisory): BFI 높음=지하수 지배(투수성 유역). 모델 BFI가 관측보다 낮으면 첨두 과다·기저 과소(저류 과소 가설). 필터 파라미터에 민감하므로 동일 설정 필수.
- 한계·주의: 기저분리는 **개념적·비유일 해**(관측 "정답" 아님) → 절대값보다 모델–관측 동일 필터 하 상대비교. 융설·저수지 방류가 있으면 필터 가정 위배.
- 출처: Lyne & Hollick (1979, *Institute of Engineers Australia*); Eckhardt (2005, *Hydrological Processes* 19(2):507–515, doi:10.1002/hyp.5675); Gustard, Bullock & Dixon (1992, *Low Flow Studies*, UKIH BFI); Ladson et al. (2013, *Australasian J. Water Resources*, 필터 표준화).

---

### ★ 감수분석 / 감수상수 (Recession analysis, Master Recession Curve, k)
- 무엇을 측정/검증하나: 강우 종료 후 유량 감소(감수) 거동으로부터 **저류-방류 특성(감수상수 k, 선형저수지 시정수)**을 추정해 모델과 비교 — 유역 배수·지하수 반응의 물리 검증.
- 정의·수식: 선형 저수지 감수 Q_t = Q_0·e^(−t/k) 또는 dQ/dt = −Q/k. Brutsaert–Nieber(1977) −dQ/dt = a·Q^b 형태로 (log −dQ/dt vs log Q) 회귀해 지수 b·계수 a 추정. Master Recession Curve(MRC)로 다수 감수사건 통합.
- 적용 도메인·자료형: 유량 [시계열] 감수구간. 
- 입력·전제: 감수사건 추출(강우·융설 무영향 구간), dQ/dt 계산 노이즈 처리(bin/평활). 
- 해석 기준(advisory): b≈1이면 선형저수지, b>1 비선형. 모델 k가 관측보다 짧으면 너무 빨리 마름(저류 과소). 추정법(사건선택·dQ/dt 방식)에 크게 의존 → 방법 명시.
- 한계·주의: dQ/dt 추정·사건선택·측정노이즈에 매우 민감(결과 산포 큼). rating error가 저유량에서 커 감수 왜곡.
- 출처: Brutsaert & Nieber (1977, *WRR* 13(3):637–643); Tallaksen (1995, *Journal of Hydrology* 165, 감수 리뷰); Stoelzle, Stahl & Weiler (2013, *HESS* 17:817–828, 감수분석 방법 민감도).

---

### ★ 저수기 지수 (Low-flow indices: Q95·7Q10·MAM7·BFI·SDI)
- 무엇을 측정/검증하나: 갈수·가뭄 관련 극치(저유량)의 모델 재현 — 수자원·환경유량·가뭄 관리의 핵심(고유량 지표가 못 보는 영역).
- 정의·수식: Q95/Q90(FDC 95·90% 초과유량), 7Q10(10년 재현 7일 최소평균유량), MAM7/MAM10(연 7·10일 최소평균유량의 다년 평균), n-day 최소유량, 유량기반 가뭄지수(SDI/threshold-level deficit volume·duration). 극치 적합(GEV/GPD) 일반론은 **→ 03_categorical_event_extremes.md**.
- 적용 도메인·자료형: 유량 [시계열] 장기 일자료.
- 입력·전제: 충분히 긴 동질 기간, 저유량 rating의 신뢰성(저유량 측정오차 큼). 결측이 최소값 통계를 크게 왜곡.
- 해석 기준(advisory): 모델은 저유량을 과대/과소 다양 — 지수별로 다른 편향 가능. 7Q10 등 재현값은 신뢰구간(부트스트랩) 동반.
- 한계·주의: 저유량은 관측·모델 모두 불확실성 최대 구간. 인위적 취수·저수지 방류가 자연저류와 섞임(자연화 여부 명시). 간헐 0유량은 별도 처리.
- 출처: WMO, *Manual on Low-flow Estimation and Prediction* (WMO-No. 1029, 2008); Smakhtin (2001, *Journal of Hydrology* 240:147–186, low-flow 리뷰); Tallaksen & van Lanen (2004, *Hydrological Drought*, Elsevier); Gustard & Demuth (2009, WMO Operational Hydrology Report 50).

---

### ★ 홍수빈도 분석 (Flood frequency: 연최대-GEV / POT-GPD / 재현주기)
- 무엇을 측정/검증하나: 모델이 **설계홍수(재현주기별 첨두유량)**를 관측 유량빈도와 일치시키는지. 홍수위험·구조물 설계의 핵심.
- 정의·수식: (1) 연최대(AMS) → GEV 또는 LP3(Log-Pearson III) 적합; (2) 임계초과(POT/PDS) → 독립 첨두에 GPD(일반파레토) 적합 + 평균초과율 λ 결합해 N년 재현유량 산출. 파라미터 추정은 L-모멘트(권장)·MLE. 극치엔진(GEV/GPD·declustering·return level)은 **→ 03_categorical_event_extremes.md**와 공유(단일 엔진).
- 적용 도메인·자료형: 장기 유량 [시계열](모델 hindcast vs 관측소).
- 입력·전제: 충분히 긴 동질 기간(가능하면 ≥30년 관행), 첨두 독립성(declustering), 비정상성(토지이용·기후변화·저수지) 고려. 
- 해석 기준(advisory): 재현주기별 유량(예: 50·100년)의 모델–관측 신뢰구간 겹침 여부. QQ로 상위 꼬리 적합 점검. 지역·기관별 권장분포 상이(미국 Bulletin 17C=LP3, 유럽·다수는 GEV).
- 한계·주의: 임계선택·declustering·표본수에 큰 민감(불확실성 큼) → 신뢰구간 필수. 저수지·취수로 자연빈도가 교란된 관측은 모델(자연)과 직접비교 부적절. 분포·추정법 선택이 재현값을 좌우.
- 출처: Coles (2001, *An Introduction to Statistical Modeling of Extreme Values*, Springer); Hosking & Wallis (1997, *Regional Frequency Analysis: An Approach Based on L-Moments*, Cambridge); England et al. (2019, *USGS Techniques and Methods 4-B5*, "Guidelines for Determining Flood Flow Frequency—Bulletin 17C"); WMO, *Manual on Estimation of Probable Maximum Precipitation* / *Guide to Hydrological Practices* (WMO-No. 168).

---

### ★ 첨두유량 크기·시각 오차 (Peak flow magnitude & timing error)
- 무엇을 측정/검증하나: 개별 홍수사건에서 모델 첨두유량의 **크기(peak error)와 발생시각(time-to-peak / peak timing)** 오차. 홍수예보의 실무 핵심.
- 정의·수식: 사건별 Peak error = (Qpeak,sim − Qpeak,obs)/Qpeak,obs(%), Peak-timing error = t_peak,sim − t_peak,obs(시간). 다수 사건의 분포·중앙값·MAE로 요약. 위상오차 일반론(교차상관 lag)은 **→ 06_timeseries_signal.md**.
- 적용 도메인·자료형: 유량 [시계열] 사건 추출.
- 입력·전제: 사건 분리(임계·baseflow separation), 시간해상도 충분(시자료 권장). 다중첨두 사건 매칭 규칙 정의.
- 해석 기준(advisory): 첨두 timing 편향은 저류·도달시간·유역면적/강우입력 오차의 신호(가설). 크기 과소는 유량곡선 평탄화 흔함. 유역크기·강우자료에 강하게 의존.
- 한계·주의: 사건정의·첨두검출 규칙에 민감. 단일 큰 사건이 통계를 지배 → 다수 사건·분포로 보고. rating error가 고유량에서 커 관측첨두 자체 불확실.
- 출처: WMO, *Guide to Hydrological Practices* (WMO-No. 168, Vol. II 예보); Ewen (2011, *Hydrology Research*, hydrograph 시각오차); Seibert, Vis (2012, *HESS*, 사건 진단 관행).

---

### ★ 수문곡선 사건지표 (Hydrograph event metrics: 첨두·용적·시간중심·상승/하강)
- 무엇을 측정/검증하나: 홍수사건 수문곡선의 **형상 전체**(첨두, 총유출용적, 상승·하강 지속, 시간중심, 첨두성 peakedness)를 서명으로 비교.
- 정의·수식: 사건 용적 V=∫Q dt, 시간중심(사건 CT)=Σ(t·Q)/ΣQ, 상승수(rising limb density)·하강곡선, 유출계수=V/강우량. 유량곡선 신호 서명(→ FDC·감수 카드)과 연계.
- 적용 도메인·자료형: 유량 [시계열] 사건단위.
- 입력·전제: 사건 분리·baseflow separation, 강우자료(유출계수용).
- 해석 기준(advisory): 사건 용적·첨두 동시 검증으로 "총량은 맞으나 형상 틀림/그 반대" 구분. 지표별 편향 조합으로 물리 가설.
- 한계·주의: 사건 정의 규칙이 결과 좌우. 여러 지표 조합 필수(단일 금지, §G6).
- 출처: Yilmaz, Gupta & Wagener (2008, *WRR* 44, 서명); Euser et al. (2013, *HESS* 17:1893–1912, "consistency"·서명 진단); Hallouin et al. (2020, *HESS*, hydro-evaluation 서명).

---

### ★ 유출용적·유출률 (Runoff volume / runoff ratio, 물수지 총량)
- 무엇을 측정/검증하나: 기간 총유출용적과 유출률(runoff ratio = 총유출/총강우)을 관측과 비교 — 유역 규모 물수지 총량 일치.
- 정의·수식: 총유출용적 V=Σ(Q·Δt), 유출률 RR = V / (P·A)(P=유역평균강우, A=유역면적). PBIAS와 상보(PBIAS는 %편향, RR은 강우 대비 비율).
- 적용 도메인·자료형: 유량 [시계열] + 유역평균 강우 [격자]/[시계열].
- 입력·전제: 유역경계·면적 정확, 유역평균강우 산정(면적가중·격자), 취수·유역간 이동(inter-basin transfer) 파악.
- 해석 기준(advisory): RR>1이면 물수지 모순(강우 과소·유역경계·지하수 유입 의심). 모델 RR 편향은 ET·침투 배분 오차의 신호(가설). 건조유역에서 RR 작고 민감.
- 한계·주의: 강우 입력 불확실성이 RR을 지배(특히 산악·희소관측). 저수지·취수로 총량 교란.
- 출처: WMO, *Guide to Hydrological Practices* (WMO-No. 168); Blöschl et al. (2013, *Runoff Prediction in Ungauged Basins*, Cambridge, 서명·runoff ratio).

---

### ★ 물수지 닫힘 (Water balance closure: P − ET − Q − ΔS ≈ 0)
- 무엇을 측정/검증하나: 유역·격자에서 강수 P, 증발산 ET, 유출 Q, 저류변화 ΔS(토양수분·지하수·눈·저수지)의 **수지 잔차(residual)**로 모델의 물리적 물수지 정합성을 진단. 육상표면모형·수문모형의 1급 물리검증.
- 정의·수식: 수지식 P = ET + Q + ΔS + residual. 잔차 = P−ET−Q−ΔS. 장기평균(ΔS≈0 가정)이면 P≈ET+Q. 보존·수지 닫힘 일반틀(질량·에너지 budget closure)은 **→ 04_conservation_energy_flux.md**.
- 적용 도메인·자료형: [격자] 모형 산출(P·ET·Q·ΔS) 또는 유역집계 [시계열]; ΔS는 GRACE TWS·토양수분 위성과 대조.
- 입력·전제: 모든 항 동일 유역·동일 기간·동일 단위(mm 또는 mm/일). ΔS 관측(GRACE·in-situ)과 정렬. 유역간 이동·취수 명시.
- 해석 기준(advisory): 잔차가 P의 수 %면 양호(관행)나 관측 P·ET 불확실성이 커 잔차 해석은 신중. 장기 잔차≠0은 저류 드리프트·항 누락 신호.
- 한계·주의: **관측 ET·P·ΔS 자체가 큰 불확실성** → 잔차를 "모델 오차"로 단정 금지(§G1). GRACE는 대유역(≳10⁵ km² / ~150,000 km²)·월단위에서만 신뢰. 모델 내부 online budget과 offline 진단을 구분(→ 04).
- 출처: WMO, *Guide to Hydrological Practices* (WMO-No. 168); Sheffield, Ferguson et al. (2009, *GRL*, 위성 물수지 닫힘); Rodell et al. (2004, *BAMS*, GLDAS·수지); Pan et al. (2012, *Journal of Climate*, 수지 닫힘 최적화).

---

### ★ 유출시기·계절성 (Flow timing: 유출중심일 CT, 계절성·pulse 지표)
- 무엇을 측정/검증하나: 연중 유출이 언제 집중되는지의 **시기·계절성**을 모델이 재현하는지 — 융설·계절강우 지배 유역의 위상 검증.
- 정의·수식: 유출중심일(Center of Timing, CT / center of mass) = Σ(t_i·Q_i)/ΣQ_i(수문년 기준 일), 계절성 지수(Walsh–Lawler), pulse count(임계 초과 상승/하강 횟수), Colwell 예측가능성. 계절분해·위상 일반론은 **→ 06_timeseries_signal.md**.
- 적용 도메인·자료형: 유량 [시계열] 일자료(수문년 wateryear 정의 명시).
- 입력·전제: 수문년 시작월 규약(융설유역 흔히 10월/11월) 모델·관측 동일. 결측 최소.
- 해석 기준(advisory): CT가 이르면 융설 조기화(온난편향 가설). 계절성 지수 편향은 강우·융설 배분 문제 신호. 유역 유형(융설/우기)에 강하게 의존.
- 한계·주의: CT는 극단 연도·결측에 민감. 다중 계절 피크 유역은 CT 단독으로 오해 소지.
- 출처: Stewart, Cayan & Dettinger (2005, *Journal of Climate* 18:1136–1155, CT·융설 timing); Court (1962, *JGR*, center-of-mass); Richter et al. (1996, *Conservation Biology*, IHA 유량변동 지표).

---

### ★ 융설 유출 시기·눈수당량 (Snowmelt timing / SWE / SCA)
- 무엇을 측정/검증하나: 융설지배 유역에서 눈수당량(SWE)·적설면적(SCA)과 그로 인한 유출시기를 위성·관측과 비교 — 봄철 유출·수자원 예측의 핵심.
- 정의·수식: SWE(mm) 시계열 bias/RMSE(→01), SCA(%)를 MODIS/VIIRS 적설도와 비교(범주형 POD/FAR·→03), 융설 유출중심일(위 CT 카드), 융설 개시일(snowmelt onset). 
- 적용 도메인·자료형: SWE [시계열](SNOTEL 등)·[격자], SCA [위성 격자], 유량 [시계열].
- 입력·전제: SWE 지점 대표성(고도·수관 영향), SCA 구름·산림 차폐 QC, 동일 고도대·유역 정렬.
- 해석 기준(advisory): 모델 SWE 과소·조기융설이면 봄 유출 조기·여름 저유량 신호(가설). SCA 임계(적설 판정 %)에 따라 POD/FAR 변동.
- 한계·주의: 산악 SWE는 지점 대표성·관측 자체가 큰 불확실성. SCA는 눈 있음/없음만(깊이 아님). 융설·강우 유출 혼재 시 분리 곤란.
- 출처: Stewart et al. (2005, *J. Climate*); Clark et al. (2006, *WRR*, 눈·유출 동화); Hall & Riggs (2007, *Hydrological Processes*, MODIS 적설); Barnhart et al. (2020, *WRR* 56, doi:10.1029/2019WR026634, 융설률·시기와 유출).

---

### 이중적산곡선 / 이중질량 (Double-mass curve)
- 무엇을 측정/검증하나: 두 누적계열(예: 누적 모델유량 vs 누적 관측유량, 또는 누적강우 vs 누적유출)의 직선성으로 **일관성·비정상성(관측소 이설·rating 변경·토지이용 변화)**을 점검.
- 정의·수식: 누적 Σy vs 누적 Σx 산점 → 기울기 변화점(꺾임)이 비정상·불일치 시점. 변화점 검정은 **→ 06_timeseries_signal.md**.
- 적용 도메인·자료형: 유량·강우 [시계열] 장기.
- 입력·전제: 동일 기간·연속 누적. 결측 보간 규약.
- 해석 기준(advisory): 기울기 꺾임=자료 불일치/유역변화 후보(진단용, 인과 단정 금지). 모델–관측 double-mass 꺾임은 특정 기간 편향 신호.
- 한계·주의: 누적이라 작은 편향이 시각적으로 가려짐. 변화점 위치는 시각판정 주관 → 통계 변화점검정 병행.
- 출처: Searcy & Hardison (1960, USGS Water-Supply Paper 1541-B, "Double-Mass Curves"); WMO, *Guide to Hydrological Practices* (WMO-No. 168, 자료 일관성).

---

### ★ 범주형·임계 초과 검증 (홍수경보 POD·FAR·CSI)
- 무엇을 측정/검증하나: "유량이 경보 임계(예: 홍수주의보·경보 수위/유량)를 넘었는가"라는 이진 사건을 모델이 맞히는지 — 홍수예보 운영 관점.
- 정의·수식: 2×2 분할표(hit·false alarm·miss·correct-negative)에서 POD·FAR·CSI(=TS)·Bias score·HSS/ETS. 정의·표는 **→ 03_categorical_event_extremes.md**(여기서 재정의 안 함). 임계는 유량·수위 경보기준으로 설정.
- 적용 도메인·자료형: 유량/수위 [시계열]/[격자] + 합의된 경보임계.
- 입력·전제: 정렬 매치업, 표본 충분(드문 홍수사건일수록 불안정), 수위↔유량 변환 일관.
- 해석 기준(advisory): POD↑·FAR↓·CSI↑ 양호. 임계 높을수록 사건 희소→신뢰구간 동반. 리드타임별로 성능 급변.
- 한계·주의: 단일 임계 정보손실→여러 임계·ROC 병행. 격자검증은 double-penalty(위치 약간 어긋나면 hit+false) 주의.
- 출처: Jolliffe & Stephenson, *Forecast Verification*(범주형 표준); WMO, *Guide to Hydrological Practices* (No. 168, 홍수예보 검증).

---

### ★ 홍수범람 공간검증 (Flood extent: CSI / critical success / Fit index)
- 무엇을 측정/검증하나: 모델(또는 수리모형 LISFLOOD-FP·HEC-RAS)이 산출한 **침수역(flood extent) 격자**를 관측(위성 SAR 침수도·현장)과 공간적으로 얼마나 일치시키는지.
- 정의·수식: Fit/CSI = A_(sim∩obs) / A_(sim∪obs)(교집합/합집합, critical success index), 또는 hit rate·false alarm ratio를 침수/비침수 셀에 적용. 공간 패턴검증 일반론은 **→ 02_spatial_pattern_verification.md**.
- 적용 도메인·자료형: 침수 이진/수심 [격자] (모델 vs 위성 SAR·광학 침수도).
- 입력·전제: 동일 격자·좌표·시각(홍수 정점 시점 SAR와 정합), 도시/식생 차폐·영구수체 마스크.
- 해석 기준(advisory): Fit/CSI 높을수록 일치(관행상 대하천 0.5~0.8 보고되나 사건·해상도 의존, 절대기준 아님). 얕은 가장자리·도시역에서 급락.
- 한계·주의: SAR 침수도 자체 오차(식생·도시 후방산란). 시점 불일치·해상도 차이로 double-penalty. 이진화 임계가 결과 좌우.
- 출처: Bates & De Roo (2000, *Journal of Hydrology* 236:54–77, LISFLOOD-FP·Fit); Horritt & Bates (2002, *Journal of Hydrology* 268, 범람모형 검증); Stephens et al. (2014, *Hydrological Processes*, Fit 지표 한계).

---

### ★ GRACE 지하수·저수량 검증 (Terrestrial Water Storage anomaly, TWS)
- 무엇을 측정/검증하나: 모델의 총저류변화(ΔS: 토양수분+지하수+눈+지표수)를 위성중력 GRACE/GRACE-FO의 육상수저장 이상(TWSA)과 비교 — 물수지 저류항의 유일한 광역 관측 제약.
- 정의·수식: 월별 TWSA(cm 등가수두)의 시계열 상관·RMSE·진폭(→01), 계절진폭·추세 비교. 유역평균 후 비교. 물수지 결합은 위 "물수지 닫힘" 카드.
- 적용 도메인·자료형: TWS [위성 격자] vs 모델 저류 [격자]; 대유역 [시계열].
- 입력·전제: GRACE 스케일링·leakage 보정 적용, 대유역(신뢰 하한 ~10⁵ km²)·월단위 집계, 모델 저류항 정의 일치(지하수 포함 여부).
- 해석 기준(advisory): 계절진폭·위상 일치 우선. 추세 비교는 GRACE 처리(mascon vs 구면조화)·GIA 보정에 민감. 소유역·단기에는 부적합.
- 한계·주의: GRACE 해상도 조대(수백 km)·신호 leakage. TWS는 성분 미분리(모델 성분과 1:1 아님). 두 미션(GRACE·FO) 간 공백(2017–2018).
- 출처: Tapley et al. (2004, *Science* 305, GRACE); Landerer & Swenson (2012, *WRR* 48, 스케일링); Scanlon et al. (2018, *PNAS* 115, GRACE vs 모델 저류); Rodell et al. (2018, *Nature* 557, TWS 추세).

---

### 위성 하천수위·SWOT 대조 (Satellite altimetry / SWOT discharge)
- 무엇을 측정/검증하나: 위성고도계(Jason/Sentinel-3/6·ICESat-2)·SWOT의 하천수위·수면폭·유량 추정을 모델과 비교 — 무측정(ungauged) 대하천의 대안 검증.
- 정의·수식: 가상관측점(virtual station) 수위 시계열 상관·RMSE(→01), rating로 유량 환산 후 비교. SWOT는 수면폭·경사로 유량 추정.
- 적용 도메인·자료형: 하천수위/폭/유량 [위성 트랙·격자] vs 모델 [시계열]/[격자].
- 입력·전제: 가상관측점 위치·통과주기, 지오이드·기준면 정합, 소하천 부적합(폭·재방문 한계).
- 해석 기준(advisory): 대하천·저지대에서 유효. 위성 유량은 rating·가정 불확실성 커 상대비교. 재방문주기가 첨두 포착 제한.
- 한계·주의: 고도계는 넓은 대하천에 한정(폭 수백 m↑). 수위→유량 변환이 큰 오차원. SWOT는 신규 미션으로 검증 진행 중.
- 출처: Birkinshaw et al. (2010, *Hydrological Processes*, 고도계 하천수위); Biancamaria, Lettenmaier & Pavelsky (2016, *Surveys in Geophysics* 37, SWOT); Papa & Frappart (2021, *Water*, 위성 하천수문 리뷰).

---

### 저수지·댐 운영 검증 (Reservoir storage / release / rule curve)
- 무엇을 측정/검증하나: 저수지 저수량·방류량·수위(규정수위 rule curve)를 관측 운영자료와 비교 — 인위적 저류가 있는 유역의 유량 검증 전제.
- 정의·수식: 저수량 물수지 ΔS = I − O − E(유입 I·방류 O·증발), 저수량·방류 시계열 bias/RMSE/상관(→01), 규정수위 대비 편차. 방류 timing·용량제약 재현.
- 적용 도메인·자료형: 저수량·방류·수위 [시계열] vs 모델/운영모듈.
- 입력·전제: 저수용량곡선(elevation–storage), 운영규칙(rule curve)·방류시설 제약, 유입 관측/추정.
- 해석 기준(advisory): 방류는 인위적 결정이라 통계지표로 "물리 오차"라 단정 곤란(운영규칙 재현 여부로 해석). 저수량 물수지 잔차로 유입·방류 정합 진단.
- 한계·주의: 운영자료 비공개·규칙 변동 잦음. 자연유량 검증과 저수지 하류는 분리(자연화 필요). 방류는 예측 불가 결정 포함.
- 출처: WMO, *Guide to Hydrological Practices* (No. 168, 저수지 운영); Hanasaki, Kanae & Oki (2006, *Journal of Hydrology* 327, 전지구 저수지 운영 모형); Yassin et al. (2019, *HESS* 23, 저수지 방류 모형화).

---

### ★ 다목적·다서명 진단 프레임 (Multi-signature / benchmark: mean-flow·기후 benchmark)
- 무엇을 측정/검증하나: 단일지표(NSE만)의 함정을 피하고 **여러 서명·여러 목적함수·benchmark 대비 상대성능**을 종합 — 수문 검증의 방법론적 뼈대(§G6 강제).
- 정의·수식: 목적함수 조합(KGE + lnNSE + PBIAS + FDC 서명), benchmark efficiency(관측 평균유량·계절기후값·이전유량 persistence 대비 skill score), Pareto 다목적 진단. Diebold–Mariano·부트스트랩은 **→ 01·13**.
- 적용 도메인·자료형: 유량 [시계열]·[격자] 종합.
- 입력·전제: 서명 계산 규약 통일, benchmark 정의 명시(mean vs climatology).
- 해석 기준(advisory): "benchmark를 못 이기면(예: NSE<0, KGE<−0.41) 모델이 평균/기후만도 못함" — 절대 임계보다 benchmark 대비 skill로 판정. 서명 조합으로 물리 진단.
- 한계·주의: 서명끼리 상충(첨두 vs 갈수) 가능 → trade-off 명시. benchmark 선택이 결론 좌우.
- 출처: Schaefli & Gupta (2007, *HESS* 11:1267–1277, benchmark); Gupta et al. (2008, *Hydrological Processes* 22, 진단적 평가); Knoben et al. (2019, *HESS* 23, benchmark KGE); Nearing et al. (2018, *WRR*, benchmarking).

---

### 불확실성·유의성 (bootstrap CI · 유효표본 · 관측유량 rating error)
- 무엇을 측정/검증하나: 지표·서명·재현값의 신뢰구간과, 관측유량 자체의 불확실성(수위–유량 관계식 rating error)을 검증에 반영.
- 정의·수식: 블록 부트스트랩(유량 강한 자기상관→블록)으로 지표 CI, 유효표본수 보정. rating error는 관측유량에 ±% 불확실성 부여. 일반 부트스트랩·유효표본은 **→ 01_error_statistics.md / figures/16**.
- 적용 도메인·자료형: 모든 유량 지표 [시계열]/[격자].
- 입력·전제: 자기상관 구조 반영(일유량은 강한 지속성), rating 불확실성 정보(있으면).
- 해석 기준(advisory): 지표 차이가 CI 겹치면 "유의한 개선 아님". 관측 rating 불확실성이 크면 모델–관측 차이 해석 보수적으로.
- 한계·주의: 자기상관 무시하면 CI 과소(과신). rating error는 고·저유량 극단에서 최대(외삽구간).
- 출처: McMillan, Krueger & Freer (2012, *Hydrological Processes* 26, rating·관측 불확실성); Coxon et al. (2015, *WRR* 51, 유량 불확실성); Clark et al. (2021, *WRR*, 평가 불확실성).

---

## 출처 (References)

### 표준 참고문헌 / 지침·교과서 (실제 존재)
- WMO, *Guide to Hydrological Practices* (WMO-No. 168, Vol. I·II) — 유량·물수지·홍수예보·자료일관성 표준 관행.
- WMO, *Manual on Low-flow Estimation and Prediction* (WMO-No. 1029, 2008) — 저유량 지수·FDC.
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer (GEV/GPD·POT).
- Hosking, J. R. M. & Wallis, J. R. (1997) *Regional Frequency Analysis: An Approach Based on L-Moments*, Cambridge University Press.
- Tallaksen, L. M. & van Lanen, H. A. J. (2004) *Hydrological Drought: Processes and Estimation Methods*, Elsevier.
- Blöschl, G. et al. (eds., 2013) *Runoff Prediction in Ungauged Basins*, Cambridge University Press (서명·runoff ratio).
- Jolliffe, I. T. & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide*, Wiley (범주형·확률 — 03과 공유).

### 학술 논문 (제목·저널·연도 확인; 권·페이지는 본문 병기, DOI는 확인분만)
- Nash, J. E. & Sutcliffe, J. V. (1970) "River flow forecasting through conceptual models part I," *Journal of Hydrology*, 10(3), 282–290. (NSE)
- Gupta, H. V., Kling, H., Yilmaz, K. K. & Martinez, G. F. (2009) "Decomposition of the mean squared error and NSE performance criteria," *Journal of Hydrology*, 377(1–2), 80–91. (doi:10.1016/j.jhydrol.2009.08.003) (KGE)
- Kling, H., Fuchs, M. & Paulin, M. (2012) "Runoff conditions in the upper Danube basin under an ensemble of climate change scenarios," *Journal of Hydrology*, 424–425, 264–277. (KGE′)
- Knoben, W. J. M., Freer, J. E. & Woods, R. A. (2019) "Technical note: Inherent benchmark or not? Comparing NSE and KGE," *Hydrology and Earth System Sciences*, 23, 4323–4331. (doi:10.5194/hess-23-4323-2019)
- Pool, S., Vis, M. & Seibert, J. (2018) "Evaluating model performance: towards a non-parametric variant of the KGE," *Hydrological Sciences Journal*, 63(13–14), 1941–1953.
- Moriasi, D. N. et al. (2007) "Model evaluation guidelines for systematic quantification of accuracy in watershed simulations," *Transactions of the ASABE*, 50(3), 885–900. (PBIAS·RSR·NSE 등급)
- Krause, P., Boyle, D. P. & Bäse, F. (2005) "Comparison of different efficiency criteria for hydrological model assessment," *Advances in Geosciences*, 5, 89–97. (lnNSE·변환)
- Schaefli, B. & Gupta, H. V. (2007) "Do Nash values have value?" *Hydrology and Earth System Sciences*, 11, 1267–1277. (benchmark)
- Yilmaz, K. K., Gupta, H. V. & Wagener, T. (2008) "A process-based diagnostic approach to model evaluation: FDC signatures," *Water Resources Research*, 44, W09417. (doi:10.1029/2007WR006716) (FHV/FLV/FMS)
- Vogel, R. M. & Fennessey, N. M. (1994) "Flow-duration curves. I: New interpretation and confidence intervals," *Journal of Water Resources Planning and Management*, 120(4), 485–504.
- Eckhardt, K. (2005) "How to construct recursive digital filters for baseflow separation," *Hydrological Processes*, 19(2), 507–515. (doi:10.1002/hyp.5675) (BFI 필터)
- Lyne, V. & Hollick, M. (1979) "Stochastic time-variable rainfall-runoff modelling," *Institute of Engineers Australia National Conference*, 89–93. (Lyne–Hollick 필터)
- Brutsaert, W. & Nieber, J. L. (1977) "Regionalized drought flow hydrographs from a mature glaciated plateau," *Water Resources Research*, 13(3), 637–643. (감수분석)
- Stoelzle, M., Stahl, K. & Weiler, M. (2013) "Are streamflow recession characteristics really characteristic?" *Hydrology and Earth System Sciences*, 17, 817–828.
- Smakhtin, V. U. (2001) "Low flow hydrology: a review," *Journal of Hydrology*, 240, 147–186.
- England, J. F. et al. (2019) *Guidelines for Determining Flood Flow Frequency—Bulletin 17C*, USGS Techniques and Methods 4-B5. (LP3·홍수빈도)
- Stewart, I. T., Cayan, D. R. & Dettinger, M. D. (2005) "Changes toward earlier streamflow timing across western North America," *Journal of Climate*, 18, 1136–1155. (유출중심일 CT)
- Barnhart, T. B. et al. (2020) "The counteracting effects of snowmelt rate and timing on runoff," *Water Resources Research*, 56. (doi:10.1029/2019WR026634)
- Bates, P. D. & De Roo, A. P. J. (2000) "A simple raster-based model for flood inundation simulation," *Journal of Hydrology*, 236, 54–77. (Fit/침수역 검증)
- McMillan, H., Westerberg, I. & Krueger, T. (2018) "Hydrological data uncertainty and its implications," *WIREs Water*. (서명·불확실성 리뷰)
- McMillan, H. et al. (2023) "When good signatures go bad: Applying hydrologic signatures in large sample studies," *Hydrological Processes*, 37. (doi:10.1002/hyp.14987)
- Euser, T. et al. (2013) "A framework to assess the realism of model structures using hydrological signatures," *Hydrology and Earth System Sciences*, 17, 1893–1912.
- Coxon, G. et al. (2015) "A novel framework for discharge uncertainty quantification applied to 500 UK gauging stations," *Water Resources Research*, 51. (rating·관측 불확실성)
- Tapley, B. D. et al. (2004) "GRACE measurements of mass variability in the Earth system," *Science*, 305. (TWS)
- Scanlon, B. R. et al. (2018) "Global models underestimate large decadal declining and rising water storage trends relative to GRACE," *PNAS*, 115. (GRACE vs 모델)
- Biancamaria, S., Lettenmaier, D. P. & Pavelsky, T. M. (2016) "The SWOT mission and its capabilities for land hydrology," *Surveys in Geophysics*, 37, 307–337.
- Hanasaki, N., Kanae, S. & Oki, T. (2006) "A reservoir operation scheme for global river routing models," *Journal of Hydrology*, 327, 22–41.

### 웹 자료 (조사 시 직접 참조)
- USGS, "Guidelines for Determining Flood Flow Frequency—Bulletin 17C": https://www.usgs.gov/publications/guidelines-determining-flood-flow-frequency-bulletin-17c
- USACE HEC, "Peaks Over Threshold FAQ"(HEC-SSP): https://www.hec.usace.army.mil/confluence/sspdocs/
- GRDC (Global Runoff Data Centre) — 전지구 유량 관측 아카이브: https://www.bafg.de/GRDC
- GloFAS (Global Flood Awareness System) — 전지구 홍수예보/재분석 유량: https://www.globalfloods.eu

### 확인요 (웹 1차 재확인 못 했거나 정정 필요)
- Kling et al. (2012) 권·페이지는 *Journal of Hydrology* 424–425로 기재했으나 인용 전 원문 재확인(확인요).
- Lyne & Hollick (1979) 회의록 페이지는 이차인용이 많아 원 문헌 재확인(확인요).
- GRACE 신뢰 최소유역 규모(~10⁵ km² 안팎)는 처리방식·지역에 따라 달라짐 — 특정 논문 수치 인용 시 재확인(확인요).
- Moriasi(2007) 성능등급은 **월단위 유량·특정 유역군 기준**이며 일/시·소유역에는 그대로 적용 불가(§G4) — 절대기준으로 인용 금지.

> 주의: 위 논문들의 정확한 권·페이지·DOI는 인용 전 원문에서 재확인할 것(검색으로 확인된 제목·저널·연도 기재, DOI 임의 생성 금지 원칙 준수). 해석 임계(Moriasi 등급·KGE/NSE 관행값·Fit/CSI)는 모두 **advisory**이며 영역·해상도·기후·기준자료 의존이다(00 §G4·§G6 강제).
