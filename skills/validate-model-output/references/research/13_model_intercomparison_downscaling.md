# 모델-모델 상호비교 · 앙상블 · 다운스케일링 검증 방법 카탈로그 (Model Intercomparison / Ensemble / Downscaling)

이 문서는 "우리 수치모델 결과"를 다른 모델·재분석·관측과 상호비교(intercomparison)하고, 앙상블(ensemble)의 신뢰성·예측력을 검증하며, 해상도 차이를 보정·다운스케일링(downscaling)할 때 쓰는 분석/검증 방법을 망라한다. 기상·파랑·수온·해류·해수면 등 모든 해양·대기 도메인에 공통으로 적용 가능한 통계 검증 방법을 중심으로, 격자(NetCDF) 대 격자 비교와 시계열 비교를 함께 다룬다. 각 방법은 "메서드 카드" 형식(측정 대상 / 정의·수식 / 적용 도메인 / 입력·전제 / 해석 기준 / 한계 / 출처)으로 정리한다. 재사용 Skill의 references/recipes 토대로 쓸 수 있도록, 공통격자 보간이 통계에 미치는 영향이나 재분석을 기준자료로 쓸 때의 한계 같은 "함정"도 명시한다.

## 이 파일에 담은 방법(한 줄 목차)
- **모델 상호비교 프레임워크(CMIP/CORDEX 류 관행)** — 공통 실험설계·아카이브 규약으로 다중모델을 동일 조건에서 비교
- **공통격자 보간(Regridding to a common grid)** — bilinear/nearest/conservative 보간과 그 통계적 함의
- **격자해상도 차이 보정(Scale/resolution mismatch)** — upscaling, 대표격자(representative grid), area-average 가정
- **Grid-to-grid 비교(격자 대 격자 검증)** — 동일 격자에서의 격자별 오차·패턴 비교
- **결정론 오차 지표 기본세트(RMSE/MAE/bias/상관/Willmott d)** — 시계열·격자 점대점 비교의 기본 통계
- **MSE 기반 스킬 스코어 분해(Murphy 1988)** — 오차를 상관·조건부·비조건부 편향으로 분해
- **아노말리 상관계수(Anomaly Correlation Coefficient, ACC)** — climatology 제거 후 공간/시간 패턴 일치도
- **Diebold–Mariano 검정(예측정확도 차이 유의성)** — 두 모델 오차 차이가 통계적으로 유의한가
- **테일러 다이어그램(Taylor diagram)** — 상관·표준편차·중심 RMSE를 한 그림에 요약
- **테일러 스킬 스코어(Taylor Skill Score, TSS)** — 패턴 충실도를 단일 점수로 압축
- **이웃기반/스케일선택 검증·FSS(Neighborhood / Fractions Skill Score)** — double-penalty 완화, 스케일별 skill
- **SAL 객체기반 공간검증(Structure-Amplitude-Location)** — 강수·패치형 장의 구조·총량·위치 오차 분리
- **다중모델 앙상블 평균(Multi-model ensemble mean, MMEM)** — 단순 평균의 오차상쇄 효과와 한계
- **모델 가중치: 성능·독립성 가중(Skill-and-independence weighting, ClimWIP)** — 모델 민주주의 대안
- **앙상블 spread-skill 관계(Spread-skill relationship)** — 앙상블 분산이 오차를 대표하는가
- **Spread-skill ratio(분산-오차 비)** — under/over-dispersion 진단 스칼라
- **순위 히스토그램 / 탈라그랑 다이어그램(Rank histogram / Talagrand)** — 앙상블 reliability 시각 진단
- **CRPS(연속순위확률점수, Continuous Ranked Probability Score)** — 확률예보 전체분포 정확도
- **CRPS 분해(reliability-resolution-uncertainty)** — CRPS를 reliability/해상도/불확실성으로 분해
- **CRPSS(CRPS 스킬 스코어)** — 기준(climatology 등) 대비 상대 성능
- **Brier 점수·BSS·분해(Brier score / Brier Skill Score / decomposition)** — 이진 사건 확률예보 검증
- **신뢰도 다이어그램(Reliability diagram / attributes diagram)** — 예보확률 대 관측빈도의 calibration
- **로그/이그노런스 점수(Logarithmic / Ignorance score)** — 확률밀도 기반 proper score
- **순위 상관·ROC(Discrimination, ROC/AUC)** — 사건 식별능력
- **Perfect Prognosis(PP) 다운스케일링** — 관측 기반 통계관계로 대규모→국지 변환
- **Model Output Statistics(MOS) 다운스케일링/후처리** — 모델출력 기반 통계보정
- **분위수 매핑 / QDM(Quantile Mapping / Quantile Delta Mapping)** — 분포 기반 bias correction과 추세보존
- **다변량 bias correction(MBCn, N차원 분포 변환)** — 변수 간 의존구조까지 보정
- **분산 팽창(Variance inflation / randomization)** — 회귀 다운스케일의 과소분산 보정
- **VALUE perfect-predictor 평가 프레임워크** — 다운스케일링 방법 표준 검증틀
- **재분석을 기준자료로 쓸 때의 한계(Reanalysis as reference)** — pseudo-truth의 함정과 관측 불확실성

---

### 모델 상호비교 프레임워크 (모델 상호비교 프레임워크 / Model Intercomparison Framework, CMIP·CORDEX-style)
- **무엇을 측정/검증하나**: 여러 모델(또는 우리 모델 vs 외부 모델)을 *동일한 실험설계·강제력·변수규약·격자규약* 아래에서 비교 가능하게 만드는 "프로토콜". 그 자체가 지표는 아니지만, 모든 정량 비교의 전제 조건이다.
- **정의·전제**: 공통 실험(historical, scenario 등), 표준 변수명·단위(CF convention), 표준 출력빈도, 공통 진단(diagnostics)을 합의한다. CMIP은 전지구 결합모델, CORDEX는 지역기후 다운스케일링에 대한 좌표·도메인·아카이브 규약을 정의한다.
- **적용 도메인/자료형**: 격자 NetCDF 중심. 기상/해양 전 도메인. 우리 수치모델 결과를 외부 모델·재분석과 비교할 때 "같은 변수·같은 기간·같은 단위·같은 격자"로 맞추는 절차로 차용.
- **입력·전제**: 비교 대상 모델군, 공통 기간, 공통 변수 정의, 공통 평가 격자, 합의된 metric 세트.
- **해석 기준**: 프레임워크 준수 여부(변수·단위·기간·격자가 정렬되었는가)가 곧 "공정 비교" 가능 여부. metric 점수는 개별 메서드 카드에서.
- **한계·주의**: 다중모델 아카이브에는 같은 코드베이스를 공유하는 모델이 섞여 있어 "모델 독립성" 가정이 깨진다(아래 가중치 카드 참조). 또한 프레임워크 합의가 곧 정답 보장은 아니다 — 공통 편향(common bias)은 상호비교로 드러나지 않을 수 있다.
- **출처**: Eyring et al. (2016) "Overview of CMIP6 experimental design and organization", *Geosci. Model Dev.* 9, 1937–1958 (DOI:10.5194/gmd-9-1937-2016); WCRP CMIP6 개요(wcrp-cmip.org); CORDEX experiment design 문서(cordex.org).

---

### 공통격자 보간 (공통격자 보간 / Regridding to a Common Grid)
- **무엇을 측정/검증하나**: 검증 자체가 아니라 *전처리*. 서로 다른 격자의 모델·관측·재분석을 동일 격자로 옮겨 격자별 비교를 가능하게 한다. 다만 보간 방식이 후속 통계(평균·분산·극값)를 바꾸므로 검증 결과에 직접 영향을 준다.
- **정의·수식(개념)**: 대표 보간 방식 — (1) 쌍선형 bilinear: 인접 4점 가중평균, 부드러운 장(온도·기압)에 적합하나 극값을 깎음. (2) 최근접 nearest-neighbour: 값 보존(범주형·풍속·적설 등)하나 불연속. (3) 보존적 conservative(1차/2차): 면적가중으로 *총량·면적평균 보존*. 강수처럼 "격자셀 면적평균"으로 해석되는 변수에 권장.
- **적용 도메인/자료형**: 격자 NetCDF 전 도메인. 해양 변수(SST, SSH, 해류)도 동일 원리. 단 해류 같은 벡터장은 성분별 보간 시 발산 왜곡 주의.
- **입력·전제**: 원본·목표 격자 정의(좌표·경계), 변수 성격(연속 vs 범주, intensive vs extensive), 육해 마스크(land/sea mask) 정합.
- **해석 기준**: "총량/면적평균 보존이 중요" → conservative. "공간 패턴 부드러움" → bilinear. "값 자체 보존(원시 분포·극값)" → nearest. 통상 *모든 자료를 가장 낮은 해상도(공통 최저 해상도)로 맞춰* 다중모델 요약통계를 산출한다.
- **한계·주의**: 고해상도를 저해상도로 보간하면 분산·극값이 평활(smoothing)되어 RMSE가 *인위적으로 좋아지거나* 극값이 사라진다. 반대로 저→고 보간은 정보가 늘지 않는다(spurious detail). 보간 방향·방식이 spread, 극값, 공간상관에 미치는 영향을 반드시 보고할 것.
- **출처**: Climate Data Operators(CDO) 매뉴얼(remapbil/remapnn/remapcon); Jones (1999) "First- and second-order conservative remapping schemes", *Mon. Wea. Rev.* 127, 2204–2210; CMIP6 multi-model 기술노트(climate-scenarios.canada.ca).

---

### 격자해상도 차이 보정 (격자해상도 차이 보정 / Scale Mismatch & Upscaling)
- **무엇을 측정/검증하나**: 서로 다른 해상도의 자료를 "공정 척도(fair scale)"에서 비교하기 위한 보정. 고해상도 모델을 저해상도 관측/재분석과 비교할 때 발생하는 representativeness error를 줄인다.
- **정의·개념**: (1) Upscaling: 고해상도를 관측 대표 척도(또는 공통 최저 해상도)로 면적평균. (2) 대표격자(representative common grid): 비교 대상들의 평균 해상도에 가까운 격자를 목표로 설정(예: GCM군 평균 해상도 ~1.5°). (3) double-penalty 회피: 고해상도 예보는 위치 오차 때문에 점대점 비교에서 이중 벌점을 받으므로, neighborhood/스케일별 검증으로 보완.
- **적용 도메인/자료형**: 격자 NetCDF. 강수·파고처럼 공간 변동이 큰 변수에서 특히 중요. 해양 mesoscale(에디) 비교 시 필수.
- **입력·전제**: 각 자료의 유효해상도(effective resolution; 명목 격자보다 거칠 수 있음), 관측의 공간 대표성, 면적가중 가능 여부.
- **해석 기준**: 비교는 "두 자료가 공히 표현할 수 있는 최저 스케일"에서 한다. 강수 강도 비교는 1차 보존 보간으로 공간 불연속을 살리는 관행이 있다.
- **한계·주의**: 명목 해상도 ≠ 유효 해상도(모델 수치확산으로 실제 분해능은 격자의 수 배). 무조건 평활화하면 다운스케일링의 부가가치(added value)를 평가하지 못한다 — "added value"는 일부러 고해상도 스케일에서 봐야 한다.
- **출처**: CORDEX 분석 관행 문서(cordex.org); Di Luca, A. et al. (2015) "Challenges in the quest for added value of regional climate dynamical downscaling", *Curr. Clim. Change Rep.* 1, 10–21; Klaver, R. et al. (2020) "Effective resolution in high resolution global atmospheric models for climate studies", *Atmos. Sci. Lett.* 21, e952 (DOI:10.1002/asl.952).

---

### Grid-to-grid 비교 (격자 대 격자 검증 / Grid-to-Grid Comparison)
- **무엇을 측정/검증하나**: 공통 격자로 정렬한 뒤 *격자점별로* 모델-기준 차이를 평가. 공간 패턴의 편향·오차 분포를 지도화한다.
- **정의·수식**: 격자별 오차 $e_{ij}=M_{ij}-O_{ij}$ 로부터 영역 평균 bias $\overline{e}$, 격자별/영역 RMSE $\sqrt{\langle e_{ij}^2\rangle}$, 공간 패턴상관(anomaly correlation/ ACC), 중심 RMSE(평균 제거 후) 등을 산출. 영역평균 시 위도 가중($\cos\phi$) 필요.
- **적용 도메인/자료형**: 격자 NetCDF 전 도메인(SST, SSH, 유속, 풍속, 강수, 파고).
- **입력·전제**: 동일 격자·동일 기간으로 정렬, 공통 land/sea mask, 결측 정합, 위도 면적가중.
- **해석 기준**: bias 지도로 계통오차 위치 파악, 패턴상관 ↑(1에 가까움)·중심 RMSE ↓ 가 좋음. 이 값들이 테일러 다이어그램의 좌표가 된다.
- **한계·주의**: 보간으로 만든 격자값끼리 비교하면 보간 오차가 섞인다. 점대점 비교는 위치 어긋남에 double-penalty. 결측·마스크 불일치가 평균을 왜곡.
- **출처**: Wilks "Statistical Methods in the Atmospheric Sciences"(3판/4판) 검증 단원; Jolliffe & Stephenson "Forecast Verification"(2nd ed., 2012).

---

### 결정론 오차 지표 기본세트 (결정론 검증 기본세트 / Deterministic Error Metrics: RMSE·MAE·Bias·Correlation·Willmott d)
- **무엇을 측정/검증하나**: 우리 모델 결정론 값을 ERA5/GLORYS·관측·위성과 *점대점*으로 비교하는 가장 기본적인 정량 지표 묶음. NetCDF 격자(격자별·영역평균)와 CSV 시계열 모두에 동일 적용. 다른 모든 요약(테일러·skill score)이 이 위에서 만들어진다.
- **정의·수식**: 오차 $e_i = M_i - O_i$ 에서 — 평균편차(bias) $\overline{e}=\frac1N\sum e_i$; 평균제곱근오차 RMSE $\sqrt{\frac1N\sum e_i^2}$; 평균절대오차 MAE $\frac1N\sum |e_i|$; 피어슨 상관 $r=\dfrac{\sum (M_i-\bar M)(O_i-\bar O)}{\sqrt{\sum(M_i-\bar M)^2}\sqrt{\sum(O_i-\bar O)^2}}$; 비편향 RMSE(centered RMSE) $\sqrt{\mathrm{RMSE}^2-\mathrm{bias}^2}$; Willmott 일치도지수(index of agreement) $d=1-\dfrac{\sum (M_i-O_i)^2}{\sum (|M_i-\bar O|+|O_i-\bar O|)^2}\in[0,1]$ 와 그 정련판 $d_r\in[-1,1]$. 순위(비모수)에는 스피어만 $\rho$·켄달 $\tau$.
- **적용 도메인/자료형**: 격자 NetCDF·시계열 CSV 전 도메인(SST, SSH, 유속, 풍속·풍향, 강수, 파고·주기·파향, 수온). 영역평균 시 위도 가중($\cos\phi$) 필수.
- **입력·전제**: 동일 시점·동일 위치(격자/지점)로 정렬·보간, 단위 통일, 결측·마스크 정합, (시계열) 동일 시간기준·평균구간. 풍향·파향 같은 *원형(directional) 변수*는 일반 RMSE 대신 각도차의 순환통계를 써야 함.
- **해석 기준**: RMSE·MAE·|bias| 작을수록, r·d 1에 가까울수록 좋음. RMSE≥MAE는 항상 성립(차이가 크면 큰 오차/이상치 존재). bias 부호로 과대/과소모의 방향 파악. RMSE만 보지 말고 bias와 centered RMSE를 분리 보고(계통오차 vs 변동오차).
- **한계·주의**: RMSE/상관은 이상치·소수 극값에 민감(상관은 위상만 보고 진폭편향을 못 봄; 큰 r이라도 bias가 클 수 있음). 자기상관이 강한 시계열·공간장은 유효 표본 수가 줄어 신뢰구간이 과소평가됨 → 부트스트랩/유효자유도 보정. 보간으로 만든 값끼리 비교 시 보간오차 혼입. d 지수는 단위 의존이 없으나 분모 정의 때문에 모델·관측 분산비에 둔감할 수 있음.
- **출처**: Wilks "Statistical Methods in the Atmospheric Sciences"; Willmott, C. J. (1981) "On the validation of models", *Physical Geography* 2, 184–194; Willmott, C. J. et al. (2012) "A refined index of model performance", *Int. J. Climatol.* 32, 2088–2094 (DOI:10.1002/joc.2419); Stow, C. A. et al. (2009) "Skill assessment for coupled biological/physical models of marine systems", *J. Marine Systems* 76, 4–15.

---

### MSE 기반 스킬 스코어 분해 (평균제곱오차 스킬 분해 / Murphy MSE-Skill Decomposition)
- **무엇을 측정/검증하나**: RMSE/MSE 기반 skill을 *상관(위상)·조건부 편향(진폭/회귀)·비조건부 편향(평균편차)* 성분으로 분해해, 오차의 원인이 위상 어긋남인지, 진폭 과대/과소(분산 불일치)인지, 단순 평균 offset인지 진단. 단일 RMSE 숫자가 숨기는 정보를 드러낸다.
- **정의·수식**: climatology 기준 MSE skill score $\mathrm{MSESS}=1-\dfrac{\mathrm{MSE}}{\sigma_o^2}$ 를 분해하면 (예보·관측 표준화 시) $\mathrm{MSESS}=r^2-\big(r-\tfrac{\sigma_f}{\sigma_o}\big)^2-\big(\tfrac{\bar f-\bar o}{\sigma_o}\big)^2$. 세 항 = (잠재 상관기여) − (조건부 편향: 진폭·기울기 오차) − (비조건부 편향: 평균오차). 첫 항만 보면 r²이 달성 가능한 상한.
- **적용 도메인/자료형**: 격자·시계열 결정론 비교 전 도메인. 우리 모델 vs 재분석/관측에서 "RMSE가 큰 이유"를 진단할 때 특히 유용.
- **입력·전제**: 매칭된 모델·기준 쌍, 평균·표준편차·상관 산출, climatology(또는 기준) 정의.
- **해석 기준**: 비조건부 편향 항이 크면 → bias correction(평균보정)으로 큰 개선 가능. 조건부 편향 항이 크면 → 진폭/분산 보정(예: 회귀 기울기·variance scaling) 필요. r²이 낮으면 위상 자체가 안 맞아 후처리로도 한계.
- **한계·주의**: 표준화·climatology 선택에 값이 의존. 분해는 평균·분산이 안정적인 충분한 표본을 전제. 비정상(추세) 시계열엔 climatology 기준이 부적절할 수 있음.
- **출처**: Murphy, A. H. (1988) "Skill scores based on the mean square error and their relationships to the correlation coefficient", *Mon. Wea. Rev.* 116, 2417–2424; Murphy, A. H. & Epstein, E. S. (1989) "Skill scores and correlation coefficients in model verification", *Mon. Wea. Rev.* 117, 572–581.

---

### 아노말리 상관계수 (아노말리 상관계수 / Anomaly Correlation Coefficient, ACC)
- **무엇을 측정/검증하나**: climatology를 제거한 *아노말리(편차)*끼리의 패턴/시간 상관 — 모델이 평년 대비 "이상의 공간·시간 패턴"을 얼마나 잘 잡는지. 기후값이 큰 변수에서 raw 상관이 과대평가되는 문제를 회피한다(예보검증의 표준 점수).
- **정의·수식**: $\mathrm{ACC}=\dfrac{\sum_i w_i (f_i-c_i)(o_i-c_i)}{\sqrt{\sum_i w_i (f_i-c_i)^2}\,\sqrt{\sum_i w_i (o_i-c_i)^2}}$. $f$ 예보(모델), $o$ 관측/분석, $c$ climatology, $w_i$ 위도 면적가중($\cos\phi$). 공간 ACC(한 시각, 모든 격자)와 시간 ACC(한 지점, 모든 시각) 둘 다 정의됨. WMO/ECMWF 정의는 평균 아노말리 제거 여부에 따라 중심화/비중심화 변형이 있음.
- **적용 도메인/자료형**: 격자 NetCDF(공간 ACC)·시계열(시간 ACC). 기상(지위고도·기온·SST 아노말리)·해양(SSH·SST 아노말리)에 표준.
- **입력·전제**: 신뢰할 climatology(동일 기준기간), 동일 격자·시점 정렬, 위도 가중, 결측·마스크 정합. climatology가 모델·관측에서 일관돼야 함(서로 다른 기준기간 혼용 주의).
- **해석 기준**: +1 완벽, 0 무가치, 음수 역위상(오도). 종관 예보에서 **ACC≥0.6 을 "유용한 예보"의 관행적 문턱**, 0.5 부근을 skill 한계로 본다(ECMWF 관행). 모델 간 비교·리드타임별 skill 곡선에 사용.
- **한계·주의**: climatology 정의에 민감(기준기간·해상도가 다르면 ACC가 달라짐). 진폭편향·평균편차는 직접 안 보임(상관이라 정규화됨) → RMSE/bias 병행. 표본 자기상관으로 유의성 과대. 위도 가중 누락 시 고위도 과대표집.
- **출처**: ECMWF Forecast User Guide §6.2.2 (Anomaly Correlation Coefficient); WMO/WWRP-WGNE 결정론 검증 지침; Jolliffe & Stephenson "Forecast Verification"(2nd ed., 2012); Wilks "Statistical Methods".

---

### Diebold–Mariano 검정 (예측정확도 차이 유의성 검정 / Diebold–Mariano Test)
- **무엇을 측정/검증하나**: 두 예보/모델(예: 우리 모델 vs ERA5 기반 예보, 또는 우리 모델 vs 외부 모델)의 오차 차이가 *통계적으로 유의한지* — "RMSE가 더 작다"가 우연인지 진짜 개선인지 판정. 모델 비교의 가설검정 도구.
- **정의·수식**: 두 예보의 손실차 $d_t = L(e^{(1)}_t) - L(e^{(2)}_t)$ (예: $L=e^2$ 또는 $|e|$). 귀무가설 $H_0:\mathbb{E}[d_t]=0$. 검정통계량 $\mathrm{DM}=\dfrac{\bar d}{\sqrt{\widehat{\mathrm{Var}}(\bar d)}}$, 분모는 $d_t$의 *자기상관을 반영한* 장기분산(HAC, Newey–West) 추정. 소표본엔 Harvey–Leybourne–Newbold(HLN) 보정.
- **적용 도메인/자료형**: 시계열 오차열(지점/격자별)에 직접 적용. 격자장은 격자별 DM 또는 영역평균 손실차 시계열로. 손실함수는 비대칭·비2차도 허용.
- **입력·전제**: 동일 검증표본에 정렬된 두 모델의 오차, 손실함수 선택, 오차의 자기상관 구조(HAC 대역폭). 공간 검정 시 공간 종속도 보정 필요.
- **해석 기준**: |DM|이 표준정규(또는 t) 임계값(예: 1.96, 5%)을 넘으면 두 모델 정확도 차이가 유의. 부호로 어느 쪽이 우수한지 판단.
- **한계·주의**: 자기상관·공간상관을 무시하면 유의성 과대(가짜 유의). 손실함수 선택에 결론이 의존. 중첩(nested) 모델·파라미터 추정이 개입하면 표준 DM 가정이 깨짐(West 1996 계열 보정 필요). 다중비교(여러 격자/변수) 시 FDR 보정 권장.
- **출처**: Diebold, F. X. & Mariano, R. S. (1995) "Comparing predictive accuracy", *J. Business & Economic Statistics* 13, 253–263; Harvey, Leybourne & Newbold (1997) 소표본 보정, *Int. J. Forecasting* 13, 281–291; Diebold (2015) "Comparing predictive accuracy, twenty years later", *JBES* 33.

---

### 테일러 다이어그램 (테일러 다이어그램 / Taylor Diagram)
- **무엇을 측정/검증하나**: 모델 장(field)이 관측 패턴을 얼마나 잘 재현하는지를 *세 통계(패턴상관 R, 표준편차 비, 중심 RMSE)*로 한 평면에 동시 표시. 여러 모델을 한 그림에서 순위 비교.
- **정의·수식**: 코사인 법칙 관계 $E'^2 = \sigma_m^2 + \sigma_o^2 - 2\sigma_m\sigma_o R$ 를 극좌표로 표현. 방위각 = 상관 R, 반경 = 표준편차(보통 관측으로 정규화), 관측점까지 거리 = 중심 RMSE($E'$).
- **적용 도메인/자료형**: 격자 또는 시계열. 다중모델 상호비교·다중변수 평가에 표준.
- **입력·전제**: 모델·관측을 동일 격자/시점으로 정렬, 평균 제거(중심화), 위도 가중. 한 변수당 한 점.
- **해석 기준**: 관측점(R=1, 정규화 σ=1, E'=0)에 가까운 모델이 우수. σ비>1 과대변동, <1 과소변동.
- **한계·주의**: bias(평균 오차)는 표현되지 않음(중심화하므로) — 별도 보고 필요. 단일 스칼라가 아니므로 자동 순위에는 TSS 등으로 압축. 공간상관은 격자 정렬·마스크에 민감.
- **출처**: Taylor, K. E. (2001) "Summarizing multiple aspects of model performance in a single diagram", *J. Geophys. Res.* 106(D7), 7183–7192 (DOI:10.1029/2000JD900719).

---

### 테일러 스킬 스코어 (테일러 스킬 스코어 / Taylor Skill Score, TSS)
- **무엇을 측정/검증하나**: 테일러 다이어그램의 정보를 0~1 단일 점수로 압축해 모델 자동 순위에 사용.
- **정의·수식**: 흔히 $S = \dfrac{4(1+R)^4}{(\sigma_f/\sigma_o + \sigma_o/\sigma_f)^2 (1+R_0)^4}$ 형태(R: 패턴상관, $\sigma_f/\sigma_o$: 표준편차 비, $R_0$: 달성가능 최대 상관). R과 변동성 충실도를 함께 반영.
- **적용 도메인/자료형**: 격자/시계열 패턴 평가, 다중모델 랭킹.
- **입력·전제**: R, 표준편차 비. $R_0$ 설정 필요(자료 한계 반영).
- **해석 기준**: 1에 가까울수록 패턴·변동성 동시 우수. 모델 간 상대 비교에 적합.
- **한계·주의**: bias 미반영. $R_0$·정규화·가중 선택에 따라 값이 달라져 절대 비교보다 *동일 설정 내 상대* 비교용. 변동성 편향(σ비)을 별도 score로 보완하기도.
- **출처**: Taylor (2001) 위와 동일; 다수 CMIP 평가 연구의 TSS/Taylor skill 적용 사례.

---

### 이웃기반/스케일선택 검증 · FSS (이웃기반 검증 / Neighborhood Verification, Fractions Skill Score FSS)
- **무엇을 측정/검증하나**: 고해상도 격자 비교에서 *위치 어긋남에 대한 double-penalty를 완화*하고, "어느 공간 스케일부터 모델이 skill을 갖는가"를 진단. 점대점이 아니라 *이웃(neighborhood)* 안의 사건 빈도(분율)를 비교한다.
- **정의·수식**: 임계값으로 모델·기준을 이진화한 뒤, 각 격자 주변 반경 $n$의 이웃에서 사건 분율 $P_f, P_o$ 를 계산. $\mathrm{FSS}(n)=1-\dfrac{\frac1N\sum (P_f-P_o)^2}{\frac1N\big(\sum P_f^2+\sum P_o^2\big)}$. 이웃 크기 $n$을 키우며 FSS를 그려, FSS가 "유용 문턱"(보통 $0.5+f_o/2$, $f_o$=기준 사건빈도)을 넘는 최소 스케일 = *skilful scale*.
- **적용 도메인/자료형**: 격자 NetCDF, 패치/불연속 변수(강수, 파고 임계초과, 해빙 가장자리, mesoscale eddy 위치). 강수·고파랑 경보 검증에 표준.
- **입력·전제**: 동일 격자 정렬, 임계값(절대/분위수) 정의, 이웃(윈도) 형태·크기 집합, 충분한 영역.
- **해석 기준**: FSS=1 완벽, 0 무skill. 작은 이웃에서 낮다가 이웃을 키우면 1로 수렴 — 수렴이 빠를수록 위치오차가 작음. skilful scale이 작을수록 고해상도 부가가치(added value) 큼.
- **한계·주의**: 임계값·이웃 크기 선택에 결과가 좌우(여러 임계·스케일을 함께 보고). 분율 비교라 진폭(강도)편향은 부분적으로만 반영. 드문 사건은 표본 부족으로 불안정. 격자 해상도가 다르면 공통격자 보간이 선행돼야 함.
- **출처**: Roberts, N. M. & Lean, H. W. (2008) "Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events", *Mon. Wea. Rev.* 136, 78–97; Ebert (2008) neighborhood 검증 종설, *Meteorol. Appl.* 15, 51–64; Mittermaier (2021) FSS 해석 논의.

---

### SAL 객체기반 공간검증 (구조-진폭-위치 검증 / Structure–Amplitude–Location, SAL)
- **무엇을 측정/검증하나**: 패치형(강수·고파랑·해빙·플룸) 장의 오차를 *구조(S, 객체 크기/형태)·진폭(A, 영역 총량)·위치(L, 질량중심·분산 위치)* 세 성분으로 분리. RMSE 한 숫자로는 안 보이는 "왜 틀렸나"(너무 크다/너무 많다/위치가 어긋났다)를 분해한다.
- **정의·수식**: 영역 내에서 — A = 영역평균값의 상대편차 $\dfrac{\langle f\rangle-\langle o\rangle}{0.5(\langle f\rangle+\langle o\rangle)}\in[-2,2]$. L = (질량중심 변위)+(객체들의 가중평균 거리 오차), $[0,2]$. S = 임계값으로 식별한 객체들의 크기/형태 분포 차이(부피 정규화), $[-2,2]$. 셋 다 0이면 완벽.
- **적용 도메인/자료형**: 격자 NetCDF, 공간적으로 응집된(coherent) 장 — 강수, 고파랑역, SST front/플룸, 해빙 가장자리. 객체 임계값 정의가 핵심.
- **입력·전제**: 분석 도메인 설정, 객체 식별 임계값(절대 또는 최대값 대비 비율), 모델·기준 동일 격자.
- **해석 기준**: A>0 과대모의(총량 과다), A<0 과소. S>0 객체가 너무 크거나 평탄(과확산), S<0 너무 작거나 뾰족. L>0 위치/분포 어긋남 큼. 세 성분의 산점도(SAL plot)로 모델군을 한눈에 비교.
- **한계·주의**: 도메인·임계값 선택에 민감(객체 식별이 바뀌면 S·L 변동). 객체가 도메인 경계에 걸치면 왜곡. S·L은 객체를 *매칭하지 않으므로* 분포 수준 비교(개별 대응 아님). 해양 변수엔 임계값·객체 정의를 재설계해야 함.
- **출처**: Wernli, H., Paulat, M., Hagen, M. & Frei, C. (2008) "SAL — A novel quality measure for the verification of quantitative precipitation forecasts", *Mon. Wea. Rev.* 136, 4470–4487; Wernli et al. (2009) SAL 후속 적용; Gilleland et al. (2009) 공간검증 방법 비교 종설, *Wea. Forecasting* 24, 1416–1430.

---

### 다중모델 앙상블 평균 (다중모델 앙상블 평균 / Multi-Model Ensemble Mean, MMEM)
- **무엇을 측정/검증하나**: 여러 모델의 단순(또는 가중) 평균이 개별 모델보다 계통오차를 줄이는지. 무작위 오차 상쇄로 종종 "최우수 단일 모델"에 필적/우월.
- **정의·수식**: $\overline{M}_{ij} = \frac{1}{N}\sum_{k=1}^{N} M^{(k)}_{ij}$ (균등) 또는 가중치 $w_k$ 적용 $\sum w_k M^{(k)}$, $\sum w_k = 1$.
- **적용 도메인/자료형**: 격자/시계열 전 도메인. 결정론적 비교에서 기준선(baseline) 산출.
- **입력·전제**: 공통 격자·기간으로 정렬된 모델군, (가중 시) 가중치 산정 근거.
- **해석 기준**: MMEM의 RMSE/bias가 개별 모델 중앙값보다 작으면 앙상블 이득 존재. 평균은 극값·분산을 깎으므로 *극값 평가에는 부적합*.
- **한계·주의**: 평균은 spread를 잃어 확률정보를 버린다(확률검증은 CRPS/rank histogram로). "모델 민주주의"(균등가중)는 종속·중복 모델이 많으면 편향됨 → 아래 가중치 카드.
- **출처**: Hagedorn, R., Doblas-Reyes, F. J. & Palmer, T. N. (2005) "The rationale behind the success of multi-model ensembles in seasonal forecasting — I. Basic concept", *Tellus A* 57, 219–233; IPCC AR5/AR6 다중모델 평균 관행; Knutti, R. et al. (2010) "Challenges in combining projections from multiple climate models", *J. Climate* 23, 2739–2758.

---

### 모델 성능·독립성 가중치 (성능·독립성 가중 / Skill-and-Independence Weighting, ClimWIP)
- **무엇을 측정/검증하나**: 다중모델 평균·전망에서 (1) 관측 대비 성능(skill)과 (2) 모델 간 상호의존(코드·파라미터 공유)을 동시에 반영해 "유효 모델 수"를 보정.
- **정의·수식**: 가중치 $w_i \propto \dfrac{\exp(-D_i^2/\sigma_D^2)}{1 + \sum_{j\neq i}\exp(-S_{ij}^2/\sigma_S^2)}$. $D_i$: 모델 i와 관측 거리(성능), $S_{ij}$: 모델 i,j 간 거리(독립성), $\sigma_D,\sigma_S$: 형상 파라미터.
- **적용 도메인/자료형**: 격자 다중모델 전망/평가. 우리 모델을 외부 앙상블에 넣어 가중 비교할 때 응용.
- **입력·전제**: 관측 기준자료, 다수 진단변수, $\sigma$ 보정(perfect-model test로 calibration).
- **해석 기준**: 가중 앙상블은 spread 축소·중복모델 영향 감소. 단, 성능과 독립성이 상쇄해 효과가 작을 수도 있다(보고된 사례 다수).
- **한계·주의**: $\sigma$ 선택·진단변수 선택에 민감, out-of-sample 검증 필요. 과도한 skill 가중은 과신(overconfidence) 위험. 관측 불확실성이 가중에 전파.
- **출처**: Knutti, R. et al. (2017) "A climate model projection weighting scheme accounting for performance and interdependence", *Geophys. Res. Lett.* 44, 1909–1918 (DOI:10.1002/2016GL072012); Sanderson, B. M., Knutti, R. & Caldwell, P. (2015) "A representative democracy to reduce interdependency in a multimodel ensemble", *J. Climate* 28, 5171–5194; Brunner, L. et al. (2020) "Reduced global warming from CMIP6 projections when weighting models by performance and independence", *Earth Syst. Dynam.* 11, 995–1012 (ClimWIP / ESMValTool recipe).

---

### 앙상블 Spread-Skill 관계 (앙상블 분산-오차 관계 / Spread-Skill Relationship)
- **무엇을 측정/검증하나**: 앙상블 분산(spread)이 실제 예보 오차의 크기를 잘 대표하는지. 신뢰성 있는 앙상블은 "예상 분산 = 평균 오차".
- **정의·수식**: 통계적 일관성 조건 — 장기적으로 $\mathbb{E}[\text{spread}^2] \approx \mathbb{E}[(\text{앙상블평균} - \text{관측})^2]$. 보통 spread를 bin으로 나눠 각 bin에서 앙상블평균 RMSE와 평균 spread를 산점도/곡선으로 비교.
- **적용 도메인/자료형**: 앙상블 격자/시계열 전 도메인(앙상블 SST, 파고, 풍속 등).
- **입력·전제**: 앙상블 멤버 전체, 매칭된 관측, 충분한 표본(시공간), 편향 제거 권장.
- **해석 기준**: 1:1 선에 가까우면 신뢰성 양호. spread<error → under-dispersive(과신), spread>error → over-dispersive.
- **한계·주의**: spread-error 관계만으로 reliability를 단정하면 오진할 수 있다(최근 비판). 멤버 수 유한 보정 필요. 조건부(상황별) spread-skill가 더 엄밀.
- **출처**: Fortin, V. et al. (2014) "Why should ensemble spread match the RMSE of the ensemble mean?", *J. Hydrometeor.* 15, 1708–1713 (DOI:10.1175/JHM-D-14-0008.1); Leutbecher & Palmer (2008) ensemble forecasting 리뷰; Dirkson, A. & Buehner, M. (2025) "Are we misdiagnosing ensemble forecast reliability? On the insufficiency of spread–error and rank-based reliability metrics", *Q. J. R. Meteorol. Soc.* (DOI:10.1002/qj.70186; preprint arXiv:2512.02160) — spread-error·rank 기반 진단의 한계 지적.

---

### Spread-Skill Ratio (분산-오차 비 / Spread-Skill Ratio, SSR)
- **무엇을 측정/검증하나**: spread-skill 관계를 단일 스칼라로 요약해 under/over-dispersion을 빠르게 진단.
- **정의·수식**: $\mathrm{SSR} = \dfrac{\langle \text{앙상블 표준편차} \rangle}{\mathrm{RMSE}(\text{앙상블 평균})}$ (멤버 수 유한 보정 인자 $\sqrt{(M+1)/M}$ 적용본 존재).
- **적용 도메인/자료형**: 앙상블 격자/시계열.
- **입력·전제**: 멤버별 표준편차, 앙상블평균 RMSE, 매칭 관측, 멤버 수 M.
- **해석 기준**: SSR≈1 잘 보정(calibrated), <1 under-dispersive(과신), >1 over-dispersive(과소신).
- **한계·주의**: 시공간 평균된 단일 값이라 국지·조건부 부정합을 숨김. RMSE는 bias를 포함하므로 SSR이 1이라도 분포형이 틀릴 수 있음 → rank histogram·CRPS 병행.
- **출처**: Fortin et al. (2014) 위와 동일; WeatherBench 2 / 데이터기반 모델 평가의 SSR 정의(arXiv:2308.15560); Leutbecher & Palmer (2008).

---

### 순위 히스토그램 / 탈라그랑 다이어그램 (순위 히스토그램 / Rank Histogram, Talagrand Diagram)
- **무엇을 측정/검증하나**: 앙상블의 *reliability(신뢰성)* — 관측이 앙상블 분포 안에서 통계적으로 균일하게 떨어지는가.
- **정의·수식**: 각 검증 케이스에서 관측이 정렬된 M개 멤버가 만드는 M+1개 bin 중 어디에 떨어지는지 집계. 이상적 앙상블이면 빈도가 *평평(uniform)*.
- **적용 도메인/자료형**: 앙상블 격자/시계열 전 도메인.
- **입력·전제**: 멤버 교환가능성(exchangeable), 멤버-관측 매칭, 관측오차 고려 권장, 충분한 표본.
- **해석 기준**: 평평 = 신뢰성 양호. U자형 = under-dispersive(관측이 양끝 초과, 과신). ∩(돔)형 = over-dispersive. 기울어짐 = 계통편향(bias).
- **한계·주의**: 평평한 히스토그램이 *반드시* 신뢰성을 뜻하지는 않는다(서로 다른 오류가 상쇄되어 우연히 평평할 수 있음). 관측오차 미보정 시 인위적 U자. 시공간 종속 표본은 유효 표본 수를 줄인다.
- **출처**: Hamill, T. M. (2001) "Interpretation of rank histograms for verifying ensemble forecasts", *Mon. Wea. Rev.* 129, 550–560; Talagrand et al. (1997); Anderson (1996); Hamill & Colucci (1997).

---

### CRPS (연속순위확률점수 / Continuous Ranked Probability Score)
- **무엇을 측정/검증하나**: 확률(앙상블)예보의 *예측 누적분포 전체*가 관측에 얼마나 가까운지. 정확도와 신뢰성을 한 번에 평가하는 proper score.
- **정의·수식**: $\mathrm{CRPS}(F, y) = \int_{-\infty}^{\infty} \big(F(x) - \mathbb{1}\{x \ge y\}\big)^2\,dx$. $F$: 예보 CDF, $y$: 관측. 결정론 예보로 줄면 평균절대오차(MAE)와 같다. Brier score를 모든 임계값에 대해 적분한 것으로도 해석.
- **적용 도메인/자료형**: 앙상블/확률 예보, 격자·시계열 전 도메인.
- **입력·전제**: 멤버로부터 경험적 CDF(또는 분포 적합), 매칭 관측. 작을수록 좋음(0이 완벽).
- **해석 기준**: 값이 작을수록 우수. 단위는 변수 단위와 동일해 직관적. 모델 간/실험 간 평균 CRPS로 비교.
- **한계·주의**: 멤버 수 유한 시 양(positive) 편향(작은 앙상블이 불리) → 보정식 사용. 절대값만으론 "좋음" 판단 어려워 CRPSS로 상대화. 강한 비대칭/극값에서 분포적합 선택이 결과 좌우.
- **출처**: Hersbach, H. (2000) "Decomposition of the continuous ranked probability score for ensemble prediction systems", *Wea. Forecasting* 15, 559–570; Matheson & Winkler (1976); Gneiting & Raftery (2007) proper scoring rules.

---

### CRPS 분해 (CRPS 분해: reliability-resolution-uncertainty / CRPS Decomposition)
- **무엇을 측정/검증하나**: CRPS를 *reliability(신뢰성)·resolution(해상도)·uncertainty(불확실성)* 성분으로 분해해, 오차의 원인이 calibration 문제인지 식별력 문제인지 진단.
- **정의·수식**: $\overline{\mathrm{CRPS}} = \mathrm{Reli} - \mathrm{Reso} + \mathrm{Unc}$ (Brier score 분해와 유사). reliability 성분은 앙상블의 rank histogram과 밀접, resolution/uncertainty 성분은 앙상블 평균 spread·outlier 거동과 연결.
- **적용 도메인/자료형**: 앙상블 격자/시계열.
- **입력·전제**: 다수 케이스의 예보 CDF·관측, 임계값/bin 설정.
- **해석 기준**: reliability ↓(0에 가까움)·resolution ↑ 가 좋음. reliability가 크면 calibration(분산/편향) 보정 필요.
- **한계·주의**: 분해는 bin·표본 수에 민감. 유한 앙상블 편향이 성분에 전파. reliability 성분이 rank histogram과 연결되므로 rank histogram의 한계(상쇄)도 함께 유의.
- **출처**: Hersbach (2000) 위와 동일; Candille & Talagrand (2005) CRPS 신뢰성/해상도 논의.

---

### CRPSS (CRPS 스킬 스코어 / Continuous Ranked Probability Skill Score)
- **무엇을 측정/검증하나**: CRPS를 기준예보(보통 climatology 또는 persistence) 대비 상대 성능으로 정규화.
- **정의·수식**: $\mathrm{CRPSS} = 1 - \dfrac{\overline{\mathrm{CRPS}}_{\text{forecast}}}{\overline{\mathrm{CRPS}}_{\text{ref}}}$.
- **적용 도메인/자료형**: 앙상블/확률 예보 전 도메인.
- **입력·전제**: 동일 표본에서 예보·기준 CRPS, 기준 정의 명시(climatology vs persistence).
- **해석 기준**: 1=완벽, 0=기준과 동등, <0=기준보다 못함.
- **한계·주의**: 기준 선택에 따라 값이 크게 달라지므로 반드시 기준을 명시. 유한 앙상블 편향이 분자에 들어가 작은 앙상블에 불리. 비음수성 보장 안 됨(음수 가능).
- **출처**: Hersbach (2000); WMO/JCOMM 및 앙상블 검증 관행(표준 참고문헌); 다수 계절예측 검증 연구의 CRPSS 사용.

---

### Brier 점수 · BSS · 분해 (브라이어 점수 / Brier Score, Brier Skill Score, Decomposition)
- **무엇을 측정/검증하나**: *이진 사건*(예: 파고>3 m, 강수>1 mm) 확률예보의 정확도. 사건 발생확률 예보 $p$ vs 관측 발생여부 $o\in\{0,1\}$.
- **정의·수식**: $\mathrm{BS} = \frac{1}{N}\sum (p_i - o_i)^2$. 분해 $\mathrm{BS} = \mathrm{Reliability} - \mathrm{Resolution} + \mathrm{Uncertainty}$. $\mathrm{BSS} = 1 - \mathrm{BS}/\mathrm{BS}_{\text{ref}}$.
- **적용 도메인/자료형**: 임계값 기반 사건 확률예보(앙상블에서 멤버 비율로 확률 산출). 전 도메인.
- **입력·전제**: 임계값 정의, 확률·관측 이진화, 표본 충분.
- **해석 기준**: BS 작을수록, BSS 1에 가까울수록 좋음. reliability 작고 resolution 큰 것이 우수.
- **한계·주의**: 드문 사건(rare event)에선 uncertainty가 작아 BSS가 불안정. 임계값 선택에 민감. BS는 임계값 하나만 — 여러 임계값을 보려면 CRPS.
- **출처**: Brier (1950); Murphy, A. H. (1973) "A new vector partition of the probability score", *J. Appl. Meteor.* 12, 595–600; Wilks "Statistical Methods in the Atmospheric Sciences".

---

### 신뢰도 다이어그램 / 속성 다이어그램 (신뢰도 다이어그램 / Reliability Diagram, Attributes Diagram)
- **무엇을 측정/검증하나**: 확률예보의 calibration — "예보확률 p로 예측한 사건이 실제로 빈도 p로 발생하는가".
- **정의·수식**: 예보확률을 bin으로 나눠, 각 bin의 평균 예보확률(x) 대 관측 발생빈도(y)를 그림. 대각선(y=x)이 완벽한 신뢰성. attributes diagram은 climatology선·no-skill선·resolution 영역을 추가.
- **적용 도메인/자료형**: 이진/임계값 확률예보, 앙상블 유래 확률, 전 도메인.
- **입력·전제**: 충분한 표본(bin별), 임계값·bin 정의, 신뢰구간(부트스트랩) 권장.
- **해석 기준**: 대각선에 가까울수록 신뢰성↑. 기울기<1 over-confident, >1 under-confident. 표본 크기 막대 동반 필수.
- **한계·주의**: bin 표본이 적으면 잡음. 드문 사건에서 불안정. calibration만 보고 resolution(식별력)은 ROC 등으로 보완.
- **출처**: Wilks "Statistical Methods"; Jolliffe & Stephenson "Forecast Verification"; Bröcker & Smith (2007) reliability diagram 신뢰구간.

---

### 로그/이그노런스 점수 (로그 점수 / Logarithmic (Ignorance) Score)
- **무엇을 측정/검증하나**: 예측 확률밀도가 관측에 부여한 확률의 로그 — 정보이론 기반 proper local score. 분포 형태를 직접 벌점.
- **정의·수식**: $\mathrm{IGN}(f, y) = -\log f(y)$. $f$: 예보 확률밀도, $y$: 관측. 평균하면 평균 ignorance.
- **적용 도메인/자료형**: 확률/앙상블 예보(밀도 적합 가능 시). 격자/시계열.
- **입력·전제**: 연속 밀도 추정 또는 범주확률, 관측. 작을수록 좋음.
- **해석 기준**: 값이 작을수록 우수. 비트 단위(밑 2) 해석 가능.
- **한계·주의**: 관측에 0에 가까운 확률을 주면 점수가 발산(무한 벌점) — 극값·꼬리에 매우 민감하고 outlier에 취약. 밀도추정 방식에 의존. 소수 앙상블에선 밀도 추정 불안정.
- **출처**: Good (1952); Roulston & Smith (2002) "Evaluating probabilistic forecasts using information theory", *Mon. Wea. Rev.* 130, 1653–1660; Gneiting & Raftery (2007).

---

### 식별력 / ROC·AUC (식별력 / Discrimination, ROC Curve and AUC)
- **무엇을 측정/검증하나**: 확률예보가 사건 발생/비발생을 *구별(discriminate)*하는 능력. calibration과 독립적인 속성.
- **정의·수식**: 임계 확률을 변화시키며 적중률(hit rate, POD)과 오경보율(false alarm rate, POFD)을 그려 ROC 곡선 작성. 곡선 아래 면적 AUC가 식별력 요약(0.5=무능, 1=완벽).
- **적용 도메인/자료형**: 이진 사건 확률예보, 앙상블 확률, 전 도메인.
- **입력·전제**: 임계값 정의, 사건 이진화, 충분한 양/음 표본.
- **해석 기준**: AUC>0.5 유용, 1에 가까울수록 우수. 일반적으로 0.7+ 실용적 식별력으로 본다(관행).
- **한계·주의**: ROC는 calibration을 보지 않음(잘 식별해도 보정 안 됐을 수 있음) → 신뢰도 다이어그램과 병행. 표본·임계값에 민감.
- **출처**: Mason (1982); Jolliffe & Stephenson "Forecast Verification"; WMO 검증 지침(표준 참고문헌).

---

### Perfect Prognosis 다운스케일링 (완전예단 다운스케일링 / Perfect Prognosis, PP)
- **무엇을 측정/검증하나**: 대규모(모델/재분석) 예측인자(predictor)와 국지 관측(predictand) 간 통계관계를 *관측-관측*으로 학습해, 모델 대규모장에 적용해 국지값을 추정. 다운스케일링의 한 패러다임.
- **정의·개념**: 관측 기반 회귀/유사법(analog)/기계학습으로 $y_{\text{local}} = g(X_{\text{large-scale obs}})$ 적합 후, 모델의 대규모장 $X_{\text{model}}$ 에 그대로 적용("모델 대규모장은 완벽하다" 가정).
- **적용 도메인/자료형**: 주로 격자→지점/고해상도(기상: 강수·기온·풍속; 해양 응용 가능). 예측인자는 격자, 예측대상은 지점 시계열.
- **입력·전제**: 신뢰할 관측 predictor·predictand, 모델이 *잘 모의하는* 대규모 예측인자 선택(자유진행 GCM에서 현실적인 변수), 정상성(stationarity) 가정.
- **해석 기준**: 교차검증(특히 perfect-predictor: 재분석을 predictor로) 성능, 분포·극값·시간계열 특성 재현.
- **한계·주의**: 재분석에서 잘 잡히는 지표면 변수라도 자유진행 모델에선 잘 안 잡혀 실제 skill이 낮을 수 있다. 정상성 가정이 기후변화에서 깨질 위험. predictor 선택에 결과가 크게 의존.
- **출처**: Maraun & Widmann (2018) *Statistical Downscaling and Bias Correction for Climate Research*, Cambridge Univ. Press; Maraun et al. (2019) VALUE perfect-predictor synthesis, *Int. J. Climatol.* 39, 3750–3785.

---

### Model Output Statistics 다운스케일링 (모델출력통계 / Model Output Statistics, MOS)
- **무엇을 측정/검증하나**: *모델 출력 자체*와 관측 간 통계관계를 학습해 국지 보정/다운스케일. 모델 계통오차까지 함께 보정(bias correction 포함).
- **정의·개념**: $y_{\text{local}} = h(X_{\text{model}})$ 를 모델출력-관측 쌍으로 적합. 회귀, 분위수매핑(분포형 MOS)이 대표. PP와 달리 모델의 편향·해상도 특성을 흡수.
- **적용 도메인/자료형**: 격자→지점/격자. predictor와 predictand 해상도 차이가 작을 때 유리.
- **입력·전제**: 모델 재예측(reforecast)·과거 모델출력과 매칭 관측, 충분한 학습기간. 모델 버전 고정(버전 바뀌면 재학습).
- **해석 기준**: 교차검증 RMSE/CRPS, 분포·극값 보정 성능.
- **한계·주의**: 특정 모델 산출물에 묶여 *비유연*(모델 바뀌면 무효). predictor-predictand 해상도 격차가 크면 부적합. 후처리 단계로 PP에 MOS를 결합하면 성능이 크게 향상되기도(하이브리드).
- **출처**: Glahn, H. R. & Lowry, D. A. (1972) "The use of Model Output Statistics (MOS) in objective weather forecasting", *J. Appl. Meteor.* 11, 1203–1211 (MOS 원전); Maraun & Widmann (2018); Eden, J. M. et al. (2014) "Downscaling of GCM-simulated precipitation using Model Output Statistics", *J. Climate* 27, 312–324.

---

### 분위수 매핑 / 분위수 델타 매핑 (분위수 매핑 / Quantile Mapping, Quantile Delta Mapping QDM)
- **무엇을 측정/검증하나**: 모델 분포를 관측 분포에 맞추는 *분포 기반 bias correction*. 평균뿐 아니라 분산·극값 등 전 분위수의 편향을 보정.
- **정의·수식**: 기본 QM: $\hat{x} = F_{obs}^{-1}\big(F_{mod}(x)\big)$ (CDF 매핑). QDM(추세보존): 모델 분위수의 *상대/절대 변화*를 분리해 보존하면서 편향만 보정 — $\hat{x}_{fut} = x_{fut}\cdot \dfrac{F_{obs}^{-1}(\tau)}{F_{mod,hist}^{-1}(\tau)}$ (곱셈형) 또는 가산형.
- **적용 도메인/자료형**: 시계열·격자(격자별 적용). 강수·기온·풍속·파고·SST 등.
- **입력·전제**: 충분한 학습기간 관측·모델, 분위수 추정(경험적/모수적), 결측·0값(강수) 처리(예: SSR for drizzle).
- **해석 기준**: 보정 후 분포·극값·QQ-plot이 관측에 일치하고, 미래 변화신호(추세)가 보존되는지.
- **한계·주의**: 기본 QM은 모델이 모의한 *미래 추세·극값 변화를 왜곡*할 수 있다 → 추세보존형(QDM, scaled distribution mapping) 권장. 외삽 구간(학습 밖 극값) 불안정. 격자별 독립 적용은 공간상관·다변량 일관성을 깨뜨림(→ 다변량 보정 필요).
- **출처**: Cannon, Sobie & Murdock (2015) "Bias correction of GCM precipitation by quantile mapping: How well do methods preserve changes in quantiles and extremes?", *J. Climate* 28, 6938–6959 (QDM 제안); Maraun (2016) bias correction critical review, *Curr. Clim. Change Rep.*

---

### 다변량 bias correction (다변량 편향보정 / Multivariate Bias Correction, MBCn 등)
- **무엇을 측정/검증하나**: 변수별 QM이 깨뜨리는 *변수 간(또는 격자 간) 의존구조*까지 함께 보정. 단변량 QM은 각 변수의 주변분포는 맞추지만 변수 간 상관·공간상관·다변량 극값 동시발생을 왜곡 — 다변량 기법은 주변분포와 의존구조를 동시에 관측에 일치시킨다.
- **정의·개념**: 대표 3계열 — (1) **MBCn**: 랜덤 직교회전 + 회전축마다 QDM 적용을 반복하는 N차원 확률밀도변환(image color-transfer 차용)으로 *전체 다변량 분포*를 관측에 일치(추세보존 QDM 기반). (2) **MBCp/MBCr**: 피어슨/스피어만 상관행렬만 보정(부분적). (3) **MRec, dOTC(동적 최적수송)** 등 최적수송 기반. 공간 의존(격자 간) 보정엔 R²D²·이미지 기반 기법.
- **적용 도메인/자료형**: 시계열·격자, 다변량(예: 풍속·풍향, 유의파고·주기·파향, 기온·강수, SST·SSH). 복합지수·동시극값(compound event) 평가가 목적일 때 필수.
- **입력·전제**: 동일 기간 다변량 관측·모델 쌍, 변수 정렬, 충분한 학습기간. 변수 수가 많으면 표본·계산비용 급증(차원의 저주).
- **해석 기준**: 보정 후 *주변분포 + 변수 간 상관/순위상관 + 다변량 극값 동시발생*이 관측에 일치하고, 추세(변화신호)가 보존되는지. 단변량 QM 대비 의존구조 재현 개선을 진단표로 확인.
- **한계·주의**: 고차원에서 수렴·과적합 위험, 학습 밖 외삽 불안정. 시간 의존(자기상관)은 대부분 보정 못 함(별도 처리). 물리적 제약(질량·에너지 보존)을 자동 보장하지 않음 — 보정 후 물리 일관성 점검 필요. 관측 다변량 자료 품질에 크게 의존.
- **출처**: Cannon, A. J. (2018) "Multivariate quantile mapping bias correction: an N-dimensional probability density function transform for climate model simulations of multiple variables", *Climate Dynamics* 50, 31–49 (DOI:10.1007/s00382-017-3580-6); Cannon (2016) MBCp/MBCr, *J. Climate* 29; Vrac (2018) R²D² 공간 다변량 보정; François et al. (2020) 다변량 bias correction 비교, *Earth Syst. Dynam.* 11, 537–562.

---

### 분산 팽창 / 무작위화 (분산 팽창 / Variance Inflation, Randomization/Inflation)
- **무엇을 측정/검증하나**: 회귀 기반 다운스케일이 *설명분산만 재현*해 결과가 과소분산(too smooth)인 문제를 보정. 국지 변동성을 현실 수준으로 회복.
- **정의·개념**: (1) inflation: 회귀 잔차분산을 키워 출력 분산을 관측에 맞춤. (2) randomization(추계적 추가): 회귀 추정치에 적절한 분포의 잡음을 더해 변동성·극값을 복원. (3) expanded downscaling 등 분산 보존 회귀.
- **적용 도메인/자료형**: PP/MOS 회귀 다운스케일의 후처리. 시계열·격자.
- **입력·전제**: 잔차 분포 추정, 관측 변동성 목표, 공간상관 보존 시 다변량 처리.
- **해석 기준**: 다운스케일 출력의 분산·극값이 관측 수준에 도달하면서 평균 skill을 유지.
- **한계·주의**: inflation은 시계열 상관을 인위적으로 부풀려 *위양성 skill*을 만들 수 있음(권장도 낮음). randomization은 결정론적 재현력을 낮추지만 분포·극값엔 적절. 방식 선택이 사용자 목적(확률 vs 결정론)에 의존.
- **출처**: von Storch (1999) "On the use of 'inflation' in statistical downscaling", *J. Climate* 12, 3505–3506; Maraun & Widmann (2018) inflation/randomization 논의.

---

### VALUE perfect-predictor 평가 프레임워크 (VALUE 완전예측인자 평가틀 / VALUE Perfect-Predictor Experiment)
- **무엇을 측정/검증하나**: 다운스케일링 방법을 *공정·표준화*해 비교하는 프레임워크. 재분석(ERA-Interim 등)을 "완벽한 predictor"로 써서, 모델 오차를 배제하고 다운스케일 방법 자체의 한계를 분리 평가.
- **정의·개념**: 공통 predictor(재분석)·공통 predictand(관측 지점망)·공통 검증지표(주변분포·시간특성·극값·공간특성·과정기반)로 여러 방법을 cross-validation 비교.
- **적용 도메인/자료형**: 통계 다운스케일/bias correction 방법 평가. 기상 변수 중심(해양 응용 가능).
- **입력·전제**: 표준 predictor·predictand·검증 프로토콜, 교차검증 분할.
- **해석 기준**: 주변분포·극값·시간 자기상관·공간상관 등 *다면적* 충실도. 단일 점수보다 진단표 묶음.
- **한계·주의**: perfect-predictor 성능은 *상한*일 뿐 — 실제 GCM에선 더 나빠짐. 지점 관측 품질·밀도에 의존. 해양 변수로 직접 차용 시 predictor 정의 재설계 필요.
- **출처**: Maraun et al. (2015) "VALUE: A framework to validate downscaling approaches", *Earth's Future* 3, 1–14; Gutiérrez et al. (2019) VALUE intercomparison, *Int. J. Climatol.* 39, 3750–3785; Maraun et al. (2019) perfect-predictor synthesis.

---

### 재분석을 기준자료로 쓸 때의 한계 (재분석=기준 자료의 함정 / Reanalysis as Reference: Caveats)
- **무엇을 측정/검증하나**: 검증 지표가 아니라 *방법론적 주의* — ERA5/GLORYS 등 재분석을 "참값(truth)"으로 쓸 때 생기는 편향과 그 영향을 점검하는 절차.
- **정의·개념**: 재분석은 *모델+동화*의 산물이므로 그 자체에 모델 편향·동화 인공물·시공간 불균질(관측망 변화로 인한 spurious trend)이 있다. 비교 대상 모델과 같은 계열의 물리를 공유하면 오차가 *상관*되어 RMSE가 인위적으로 작아진다(공통편향 은폐).
- **적용 도메인/자료형**: 격자 기준자료 전반(대기 재분석, 해양 재분석 GLORYS, SST 분석장 등).
- **입력·전제**: 재분석 불확실성 추정(다중 재분석 비교), 동화 관측 밀도·변화 이력, 변수별 신뢰도 차등(예: 강수·해류는 직접 관측이 약해 신뢰도 낮음).
- **해석 기준**: 가능하면 *복수 기준자료*(재분석+독립 관측+위성)로 검증해 기준 의존성을 시험. 기준 불확실성을 오차막대로 전파. "관측 대비"인지 "재분석 대비"인지 명시.
- **한계·주의**: 재분석을 검증 기준이자 동시에 다운스케일 predictor로 쓰면 순환 위험. 해양 재분석은 심층·연안에서 관측 희소로 신뢰도 급락. SST/SSH는 변수별 위성·현장 자료 동화량 차이로 신뢰도 불균질.
- **출처**: Hersbach et al. (2020) "The ERA5 global reanalysis", *Q. J. R. Meteorol. Soc.* 146, 1999–2049; Lellouche et al. (2021) GLORYS12 글로벌 해양 재분석; Parker (2016) "Reanalyses and observations: What's the difference?", *Bull. Amer. Meteor. Soc.*; Thorne & Vose (2010) reanalysis climate monitoring 한계.

---

## 출처(References)

> 표기 원칙: 아래는 실제 존재하는 표준 문헌·논문·기술문서다. DOI는 확인된 경우에만 병기했고, 미확인 항목은 그렇게 표시했다. 표준 교과서/지침은 판본을 명시했다.

**교과서·표준 지침**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*, Academic Press (3rd ed. 2011 / 4th ed. 2019). — 검증 지표, Brier/신뢰도/ROC.
- Jolliffe, I. T. & Stephenson, D. B. (eds.) *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, Wiley (2nd ed., 2012).
- Maraun, D. & Widmann, M. *Statistical Downscaling and Bias Correction for Climate Research*, Cambridge University Press (2018).
- WMO/JCOMM 및 WWRP 예보 검증 지침(Forecast Verification methods) — (표준 참고문헌, 세부 판본 확인요).

**모델 상호비교·다중모델 가중치**
- Eyring, V. et al. (2016) Overview of the CMIP6 experimental design and organization. *Geosci. Model Dev.* 9, 1937–1958. DOI:10.5194/gmd-9-1937-2016.
- Knutti, R. et al. (2017) A climate model projection weighting scheme accounting for performance and interdependence. *Geophys. Res. Lett.* 44, 1909–1918. DOI:10.1002/2016GL072012.
- Sanderson, B. M., Knutti, R. & Caldwell, P. (2015) A representative democracy to reduce interdependency in a multimodel ensemble. *J. Climate* 28, 5171–5194.
- Brunner, L. et al. (2020) Reduced global warming from CMIP6 projections when weighting models by performance and independence. *Earth Syst. Dynam.* 11, 995–1012 (ClimWIP).
- Hagedorn, R., Doblas-Reyes, F. J. & Palmer, T. N. (2005) The rationale behind the success of multi-model ensembles in seasonal forecasting — I. Basic concept. *Tellus A* 57, 219–233.
- Knutti, R. et al. (2010) Challenges in combining projections from multiple climate models. *J. Climate* 23, 2739–2758.
- ESMValTool ClimWIP recipe documentation (docs.esmvaltool.org).
- CORDEX experiment design / statistical downscaling specification (cordex.org).

**보간·해상도**
- Jones, P. W. (1999) First- and second-order conservative remapping schemes for grids in spherical coordinates. *Mon. Wea. Rev.* 127, 2204–2210.
- Climate Data Operators (CDO) User Guide — remap operators (code.mpimet.mpg.de/projects/cdo).
- CMIP6 multi-model ensemble technical notes (climate-scenarios.canada.ca).
- Di Luca, A. et al. (2015) Challenges in the quest for added value of regional climate dynamical downscaling. *Curr. Clim. Change Rep.* 1, 10–21.
- Klaver, R. et al. (2020) Effective resolution in high resolution global atmospheric models for climate studies. *Atmos. Sci. Lett.* 21, e952. DOI:10.1002/asl.952.

**결정론 검증·패턴·공간검증**
- Taylor, K. E. (2001) Summarizing multiple aspects of model performance in a single diagram. *J. Geophys. Res.* 106(D7), 7183–7192. DOI:10.1029/2000JD900719.
- Murphy, A. H. (1988) Skill scores based on the mean square error and their relationships to the correlation coefficient. *Mon. Wea. Rev.* 116, 2417–2424.
- Murphy, A. H. & Epstein, E. S. (1989) Skill scores and correlation coefficients in model verification. *Mon. Wea. Rev.* 117, 572–581.
- Willmott, C. J. (1981) On the validation of models. *Physical Geography* 2, 184–194.
- Willmott, C. J. et al. (2012) A refined index of model performance. *Int. J. Climatol.* 32, 2088–2094. DOI:10.1002/joc.2419.
- Stow, C. A. et al. (2009) Skill assessment for coupled biological/physical models of marine systems. *J. Marine Systems* 76, 4–15.
- Diebold, F. X. & Mariano, R. S. (1995) Comparing predictive accuracy. *J. Business & Economic Statistics* 13, 253–263.
- Harvey, D., Leybourne, S. & Newbold, P. (1997) Testing the equality of prediction mean squared errors. *Int. J. Forecasting* 13, 281–291.
- Roberts, N. M. & Lean, H. W. (2008) Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events. *Mon. Wea. Rev.* 136, 78–97.
- Ebert, E. E. (2008) Fuzzy verification of high-resolution gridded forecasts: a review and proposed framework. *Meteorol. Appl.* 15, 51–64.
- Wernli, H., Paulat, M., Hagen, M. & Frei, C. (2008) SAL — A novel quality measure for the verification of quantitative precipitation forecasts. *Mon. Wea. Rev.* 136, 4470–4487.
- Gilleland, E. et al. (2009) Intercomparison of spatial forecast verification methods. *Wea. Forecasting* 24, 1416–1430.
- ECMWF Forecast User Guide §6.2.2 — Anomaly Correlation Coefficient (confluence.ecmwf.int).

**앙상블·확률 검증**
- Hersbach, H. (2000) Decomposition of the continuous ranked probability score for ensemble prediction systems. *Wea. Forecasting* 15, 559–570.
- Hamill, T. M. (2001) Interpretation of rank histograms for verifying ensemble forecasts. *Mon. Wea. Rev.* 129, 550–560.
- Candille, G. & Talagrand, O. (2005) Evaluation of probabilistic prediction systems for a scalar variable. *Q. J. R. Meteorol. Soc.* 131.
- Gneiting, T. & Raftery, A. E. (2007) Strictly proper scoring rules, prediction, and estimation. *J. Amer. Statist. Assoc.* 102, 359–378.
- Murphy, A. H. (1973) A new vector partition of the probability score. *J. Appl. Meteor.* 12, 595–600.
- Roulston, M. S. & Smith, L. A. (2002) Evaluating probabilistic forecasts using information theory. *Mon. Wea. Rev.* 130, 1653–1660.
- Fortin, V. et al. (2014) Why should ensemble spread match the RMSE of the ensemble mean? *J. Hydrometeor.* 15, 1708–1713.
- Leutbecher, M. & Palmer, T. N. (2008) Ensemble forecasting. *J. Comput. Phys.* 227, 3515–3539.
- Dirkson, A. & Buehner, M. (2025) Are we misdiagnosing ensemble forecast reliability? On the insufficiency of spread–error and rank-based reliability metrics. *Q. J. R. Meteorol. Soc.*, DOI:10.1002/qj.70186 (preprint arXiv:2512.02160).
- Rasp, S. et al. (2023) WeatherBench 2 (arXiv:2308.15560) — SSR/CRPS 등 데이터기반 모델 평가 정의.

**다운스케일링·bias correction**
- Glahn, H. R. & Lowry, D. A. (1972) The use of Model Output Statistics (MOS) in objective weather forecasting. *J. Appl. Meteor.* 11, 1203–1211.
- Cannon, A. J., Sobie, S. R. & Murdock, T. Q. (2015) Bias correction of GCM precipitation by quantile mapping: How well do methods preserve changes in quantiles and extremes? *J. Climate* 28, 6938–6959.
- Cannon, A. J. (2018) Multivariate quantile mapping bias correction: an N-dimensional probability density function transform for climate model simulations of multiple variables. *Climate Dynamics* 50, 31–49. DOI:10.1007/s00382-017-3580-6.
- François, B. et al. (2020) Multivariate bias corrections of climate simulations: which benefits for which losses? *Earth Syst. Dynam.* 11, 537–562.
- von Storch, H. (1999) On the use of "inflation" in statistical downscaling. *J. Climate* 12, 3505–3506.
- Eden, J. M. et al. (2014) Downscaling of GCM-simulated precipitation using Model Output Statistics. *J. Climate* 27, 312–324.
- Maraun, D. (2016) Bias correcting climate change simulations — a critical review. *Curr. Clim. Change Rep.* 2, 211–220.
- Maraun, D. et al. (2015) VALUE: A framework to validate downscaling approaches for climate change studies. *Earth's Future* 3, 1–14.
- Gutiérrez, J. M. et al. (2019) An intercomparison of a large ensemble of statistical downscaling methods over Europe (VALUE perfect-predictor). *Int. J. Climatol.* 39, 3750–3785.
- Maraun, D. et al. (2019) The VALUE perfect predictor experiment: process-based evaluation. *Int. J. Climatol.* 39.

**기준자료(재분석) 한계**
- Hersbach, H. et al. (2020) The ERA5 global reanalysis. *Q. J. R. Meteorol. Soc.* 146, 1999–2049. DOI:10.1002/qj.3803.
- Lellouche, J.-M. et al. (2021) The Copernicus Global 1/12° Oceanic and Sea Ice GLORYS12 Reanalysis. *Front. Earth Sci.* 9.
- Parker, W. S. (2016) Reanalyses and observations: What's the difference? *Bull. Amer. Meteor. Soc.* 97, 1565–1572.
- Thorne, P. W. & Vose, R. S. (2010) Reanalyses suitable for characterizing long-term trends. *Bull. Amer. Meteor. Soc.* 91, 353–361.
