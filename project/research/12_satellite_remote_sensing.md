# 위성·원격탐사 분석·검증 방법 카탈로그 (Satellite / Remote Sensing Verification Methods)

이 문서는 우리 수치모델 결과를 위성·원격탐사 자료(고도계 altimetry, 위성 SST, 산란계 scatterometer 해상풍, 해색 ocean color/Chl-a 등) 및 권위 재분석자료(ERA5, GLORYS)·관측소 자료와 비교·검증할 때 쓰는 방법을 메서드 카드 형식으로 망라한다. 위성자료는 점 관측이 아니라 궤도(swath)·격자(grid)로 들어오고, 처리 수준(L2/L3/L4)에 따라 시공간 대표성·오차 구조가 다르므로, 일반 통계지표만으로는 부족하고 **매치업(matchup)·시공간 매칭·대표성오차(representativeness error)·삼중대조(triple collocation)** 같은 위성 특화 절차가 핵심이다. 이 카탈로그는 그 Skill의 references/recipes 토대가 된다.

> **출처 표기 원칙**: 아래 카드의 출처는 웹 검색으로 서지(저자·연도·저널·DOI)를 **실제 확인한 것**만 확정 표기했다. 확인하지 못한 세부는 "(확인요)"로 명시한다. DOI를 지어내지 않는다.

## 목차 (이 파일에 담은 방법들)

**위성 특화 매칭·오차구조**
- **시공간 매칭/매치업(Spatiotemporal Matchup & Colocation)** — 위성-모델/위성-관측 짝짓기의 기본 절차
- **매치업 통계지표(Matchup Statistics: bias, RMSD, robust SD)** — 위성-기준자료 차이 정량화
- **대표성오차 / 서브풋프린트 변동(Representativeness Error / Sub-footprint Variability)** — 점-면적 스케일 불일치 보정
- **삼중대조(Triple Collocation, TC)** — 기준진실 없이 3자료 오차분산 동시 추정
- **확장 삼중대조(Extended Triple Collocation, ETC)** — TC + 진실과의 상관(SNR) 추정
- **사중대조(Quadruple Collocation, QC)** — 4자료로 가정 완화·교차검증

**공통 검증통계(위성·재분석·관측 비교에 모두 적용)**
- **Taylor 다이어그램(Taylor Diagram)** — 상관·표준편차비·centered RMSD를 한 그림에 요약
- **분포 비교(QQ-plot · 경험적 CDF · 분위편차)** — 평균/분산을 넘어 분포 전체·극값 비교
- **이상치 상관·기후값 제거(Anomaly Correlation & Climatology Removal)** — 계절신호 제거 후 변동 평가
- **사건/범주 검증(Categorical / Event Verification)** — 해빙역·전선·블룸 등 이진 사건의 적중/오경보
- **객체·특징 기반 공간 검증(Object/Feature-based Spatial Verification)** — 에디·전선·블룸 위치·형태 평가

**도메인별 위성 검증**
- **고도계 SLA/ADT 검증: along-track vs gridded** — 궤도자료/격자자료 각각의 검증 전략
- **고도계 파수 스펙트럼·유효해상도(Wavenumber Spectrum & Effective Resolution)** — 분해 가능한 최소 스케일 진단
- **위성 SST L2/L3/L4 검증(GHRSST 체계)** — 처리수준별 in situ 검증·품질 모니터링
- **Skin/Bulk·일주변동 보정(Skin–Bulk & Diurnal Adjustment)** — SST 측정깊이/시각 차이 보정
- **SST 전선·수평경도 검증(SST Front / Gradient Verification)** — 전선 위치·강도 비교
- **산란계 해상풍 검증(Scatterometer Wind Validation)** — 풍속/풍향 벡터 검증, 표층류 영향
- **해색 Chl-a 검증 프로토콜(Ocean Color Matchup: Bailey–Werdell / Zibordi)** — log10 공간 매치업·픽셀 윈도우 QC

**처리·표본화·불확실성**
- **L2→L3 비닝/격자화(Swath Binning & Gridding)** — 궤도자료를 격자 모델과 맞추는 처리
- **궤도/스와스 처리·교차점 분석(Orbit/Swath Processing & Crossover Analysis)** — 시공간 표본화·자체일관성
- **불확실성 정합 검증(Uncertainty Validation: u-plot / standardized error)** — 보고된 불확실성의 신뢰성 점검

---

### 시공간 매칭·매치업 (시공간 콜로케이션 / Spatiotemporal Matchup & Colocation)
- **무엇을 측정/검증하나**: 위성 화소(또는 궤도점)와 모델 격자/관측소를 동일 시각·동일 위치로 짝지어 비교 가능한 쌍(matchup)을 생성한다. 모든 정량 검증의 전제 단계.
- **정의·수식**: 매치업 윈도우 정의 — 공간 반경 \(\Delta r\)(예: 위성 화소 ±1.5격자, 또는 25/50 km), 시간 윈도우 \(\Delta t\)(예: ±3 h, ±6 h, 또는 같은 날). 모델/위성 값은 매치업 지점으로 공간·시간 보간(예: 선형/최근접/이중선형)하거나, 윈도우 내 화소를 평균.
- **적용 도메인/자료형**: 격자(NetCDF)·궤도(along-track)·시계열(CSV/관측소) 전부. 위성-모델, 위성-관측, 모델-관측, 모델-재분석(ERA5/GLORYS) 모두.
- **입력·전제**: 위경도·시간(가능하면 UTC), 동일 변수·단위, 좌표계 일치. 모델은 위성 통과시각으로 시간보간 필요. 위성 QC 플래그(quality_level)로 사전 선별.
- **해석 기준**: 매치업 수가 통계적으로 충분해야(수백~수천) 지역/계절별 안정. 윈도우가 클수록 표본↑·대표성오차↑의 트레이드오프.
- **한계·주의**: 윈도우 크기·QC 임계값 선택이 결과를 좌우(프로토콜 의존성). 위성-관측의 측정량 차이(예: SST skin vs bulk)는 매칭 전 보정해야 함. 구름·결측으로 표본이 특정 조건에 편향될 수 있음.
- **출처**: Bailey & Werdell (2006), *Remote Sensing of Environment*, 102, 12–23, doi:10.1016/j.rse.2006.01.015 — 해색 매치업 프로토콜(아래 카드 참조). GHRSST 검증 관행(아래 SST 카드).

---

### 매치업 통계지표 (편차·RMSD·로버스트 산포 / Matchup Statistics)
- **무엇을 측정/검증하나**: 짝지어진 위성-기준자료 차이 \(d = X_{sat}-X_{ref}\)의 중심경향(편향)·산포·상관을 정량화.
- **정의·수식**:
  - 편차(bias) \(= \overline{d}\), 표준편차(SD) \(= \mathrm{std}(d)\)
  - 평균제곱근차이(RMSD) \(= \sqrt{\frac{1}{N}\sum d_i^2}\); 평균제거 RMSD(centered/unbiased) \(= \sqrt{\mathrm{RMSD}^2-\mathrm{bias}^2}\)
  - 로버스트 통계: 중앙값 편차(median), 로버스트 SD \(= 1.4826\times \mathrm{MAD}\)(MAD=중앙값 절대편차)
  - 상관계수 \(r\), 선형회귀 기울기/절편
- **적용 도메인/자료형**: 모든 위성-기준 매치업(SST, SLA, 풍속, Chl-a 등).
- **입력·전제**: 위 "시공간 매칭"으로 만든 짝. 이상치 영향이 크므로 로버스트 지표 병행 권장.
- **해석 기준**: GHRSST 관행 예 — 위성 SST는 야간 편차 |bias|≲0.1–0.2 K, 로버스트 SD ≲0.3–0.5 K면 양호(센서·지역 의존). 절대 임계값은 변수·자료별로 다르므로 "기준자료 불확실성 대비" 상대평가가 안전.
- **한계·주의**: 평균 RMSD는 이상치·표본 편향에 취약 → median/robust SD 병행. bias와 SD를 분리 보고해야 계통오차/랜덤오차 구분 가능.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (표준 교과서). 로버스트 SD(1.4826×MAD)는 통계 표준. GHRSST 검증 관행.

---

### 대표성오차 / 서브풋프린트 변동 (대표성 오차 / Representativeness Error, Sub-footprint Variability)
- **무엇을 측정/검증하나**: 점 관측(부이/관측소)과 위성 화소(면적 평균) 또는 모델 격자(부피 평균)가 "같은 양"을 재지 않아서 생기는 비교 불확실성. 검증 잔차 중 진짜 위성/모델 오차가 아닌 부분.
- **정의·수식**: 관측-격자 차이의 분산을 \(\sigma_d^2 = \sigma_{model}^2 + \sigma_{obs}^2 + \sigma_{repr}^2\)로 분해. \(\sigma_{repr}^2\)는 풋프린트/격자 내부 변동(sub-footprint variability, SFV)에서 기인. 고해상 보조자료로 SFV를 추정해 검증 오차예산에 더함.
- **적용 도메인/자료형**: 위성(면적)–부이(점) 비교 전부. 특히 연안·전선·메소스케일 강변동역에서 큼. 데이터동화의 representation error와 동일 개념.
- **입력·전제**: 풋프린트/격자 크기, 변수의 공간 변동성(구조함수·분산 추정용 고해상 자료).
- **해석 기준**: 검증 RMSD가 기준자료 불확실성+대표성오차의 합보다 작거나 비슷하면, 잔여 위성/모델 오차는 그 이하로 해석. 강변동역에서 대표성오차가 RMSD의 상당부분을 설명할 수 있음.
- **한계·주의**: 정량화가 어렵고 보조자료 의존. 무시하면 위성/모델 오차를 과대평가. 시간 대표성(통과시각 순간 vs 부이 평균)도 함께 고려.
- **출처**: Janjić et al. (2018), *QJRMS*, 144, 1257–1278, doi:10.1002/qj.3130, "On the representation error in data assimilation". 서브풋프린트 변동(SSS): "Spatial Scales of Sea Surface Salinity Subfootprint Variability in the SPURS Regions", *Remote Sensing* (2020), doi:10.3390/rs12233996.

---

### 삼중대조 (삼중대조법 / Triple Collocation, TC)
- **무엇을 측정/검증하나**: 기준진실(ground truth) 없이, 서로 독립인 **3개 자료**(예: 위성·모델·in situ)의 콜로케이션만으로 각 자료의 **랜덤오차 표준편차**를 동시 추정. 보정(calibration) 계수도 얻음.
- **정의·수식**: 각 자료 \(X_i = \alpha_i + \beta_i\,T + \varepsilon_i\)(공통 진실 \(T\), 오차 \(\varepsilon_i\)). 오차가 상호무상관·진실과 무상관이면 공분산으로부터
  \(\sigma_{\varepsilon_1}^2 = C_{11}-\frac{C_{12}C_{13}}{C_{23}}\) (스케일/표기에 따라 형태 차이) 등으로 각 \(\sigma_{\varepsilon_i}\) 분리.
- **적용 도메인/자료형**: 해상풍, 유의파고, SSS, SST, 강수 등 위성-모델-관측이 동시 존재하는 변수. 격자·궤도·시계열 모두. **모델 vs 재분석(GLORYS) vs 관측** 같은 3자 구성에도 적용.
- **입력·전제**: 3자료의 콜로케이션 삼중쌍, **오차의 상호독립**, 진실과 선형관계, 정상성(stationarity). 충분한 표본.
- **해석 기준**: 각 자료의 오차 SD를 절대값으로 비교 → 어느 자료가 더 정확한지 순위화. in situ가 "참값"이라는 가정 없이도 평가 가능한 것이 강점.
- **한계·주의**: **오차 상호독립 가정 위반**(공통 보조자료·공통 모델 등; 예: 모델과 재분석이 동일 NWP 강제력을 공유)이 추정을 크게 왜곡. 음의 분산 추정(표본부족/가정위반) 가능. 비이상적 오차통계의 영향은 별도 연구로 문서화됨.
- **출처**: Stoffelen (1998), *JGR Oceans*, 103(C4), 7755–7766, doi:10.1029/97JC03180 — 해상풍 TC 원논문. Caires & Sterl (2003), *JGR Oceans*, 108(C3), 3098, doi:10.1029/2002JC001491. 비이상 오차통계 영향: "The Impact on Triple/N-Way Collocation-Based Validation of Remote Sensing Products Due to Non-Ideal Error Statistics", *Remote Sensing* (2025), doi:10.3390/rs17223751.

---

### 확장 삼중대조 (확장 삼중대조 / Extended Triple Collocation, ETC)
- **무엇을 측정/검증하나**: TC를 확장해, 각 자료와 **알 수 없는 진실 사이의 상관계수 \(\rho_{T,X_i}\)**(= 정규화된 신호대잡음비 SNR 관련량)를 추가로 추정. RMSE(잡음)만이 아니라 "신호에 대한 민감도"까지 평가.
- **정의·수식**: \(\rho^2_{T,X_i}\)는 스케일·무편향 SNR로 해석. \(\mathrm{SNR}_i = \rho^2/(1-\rho^2)\) 형태. 오차분산(TC)과 상관(ETC)을 함께 제시.
- **적용 도메인/자료형**: TC와 동일. 자료 간 동적범위·민감도가 다를 때 특히 유용.
- **입력·전제**: TC와 동일(3자료, 오차 독립, 선형). 진실과의 상관을 위해 충분한 변동성 필요.
- **해석 기준**: 어떤 자료가 잡음은 크지만 신호 민감도(상관)가 높아 실효 SNR이 더 좋을 수 있음 → 잡음만 보는 평가의 함정을 피함. RMSE와 상관을 함께 봐야 공정한 비교.
- **한계·주의**: TC와 같은 독립성 가정 한계 승계. 단일 다이어그램으로 여러 측면을 요약하려는 시도가 있으나 해석 주의.
- **출처**: McColl et al. (2014), *Geophysical Research Letters*, 41, 6229–6236, doi:10.1002/2014GL061322, "Extended triple collocation: estimating errors and correlation coefficients with respect to an unknown target". TC 다이어그램 요약: Siu et al. (2024), *Frontiers in Remote Sensing*, 5, doi:10.3389/frsen.2024.1395442.

---

### 사중대조 (사중대조 / Quadruple Collocation, QC)
- **무엇을 측정/검증하나**: **4개** 콜로케이션 자료로 TC의 강한 가정(특히 한 쌍의 오차상관 0)을 일부 완화하거나 교차검증. 자료쌍 간 오차상관을 명시적으로 다룰 수 있음.
- **정의·수식**: TC의 공분산 방정식을 4자료로 확장. 추가 자유도로 일부 오차상관 항을 추정/허용. (대표성오차·교차공분산을 명시적으로 포함하는 일반화 정식 존재.)
- **적용 도메인/자료형**: 해상풍(in situ·산란계·NWP·추가자료) 등 4자료 확보 가능 변수.
- **입력·전제**: 4자료의 사중 콜로케이션, 완화된 독립성 가정. 표본수 더 많이 필요.
- **해석 기준**: TC와 QC 결과가 일치하면 가정 타당성의 방증. 불일치하면 TC 가정 위반 의심.
- **한계·주의**: 4자료 동시 확보가 현실적으로 어렵고 표본이 줄어듦. 추가 가정·식별성 문제 존재.
- **출처**: Vogelzang & Stoffelen (2021), *JGR Oceans*, 126, e2021JC017189, doi:10.1029/2021JC017189, "Quadruple Collocation Analysis of In-Situ, Scatterometer, and NWP Winds".

---

### Taylor 다이어그램 (테일러 다이어그램 / Taylor Diagram)
- **무엇을 측정/검증하나**: 모델 패턴과 기준(위성/재분석/관측) 패턴의 **상관계수 \(R\)**, **표준편차 비 \(\sigma_f/\sigma_r\)**, **centered RMSD**를 단일 극좌표 그림에 동시 요약. 여러 모델/실험/변수를 한 그림에서 비교하는 데 표준.
- **정의·수식**: centered RMSD \(E' = \sqrt{\sigma_f^2 + \sigma_r^2 - 2\sigma_f\sigma_r R}\) (코사인 법칙). 방위각 \(=\arccos R\), 반경 \(=\sigma_f\). 기준점(관측)은 \(R=1,\ \sigma_f=\sigma_r\)에 위치. 평균편차(bias)는 별도 표기(이 그림은 centered 통계만 요약).
- **적용 도메인/자료형**: 격자(NetCDF) 공간장·시계열 모두. 모델 vs ERA5/GLORYS/위성 격자장 비교에 특히 유용(여러 변수·여러 모델을 한눈에).
- **입력·전제**: 동일 격자/기간으로 보간된 두 장(field), 공통 결측 마스크. 변수 단위 동일. 표준화(\(\sigma\)로 정규화)하면 단위 다른 변수도 한 그림에 표시 가능.
- **해석 기준**: 기준점에 가까울수록 좋음(높은 \(R\), 1에 가까운 표준편차 비, 작은 \(E'\)). \(\sigma_f/\sigma_r>1\)이면 모델이 변동을 과대, <1이면 과소표현.
- **한계·주의**: bias(평균 오차)를 담지 못하므로 항상 별도 보고. 상관 중심이라 위상오차에 민감하고 진폭만 맞아도 \(R\)이 낮을 수 있음. 결측 마스크 불일치 시 통계 왜곡.
- **출처**: Taylor, K. E. (2001), "Summarizing multiple aspects of model performance in a single diagram", *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183–7192, doi:10.1029/2000JD900719.

---

### 분포 비교 (분위수·경험적 CDF·QQ-plot / Distribution Comparison: QQ-plot, Empirical CDF, Quantile Bias)
- **무엇을 측정/검증하나**: 평균·분산만이 아니라 **분포 전체와 극값(tail)**의 일치를 평가. 모델이 강풍/고파/저온 극값을 과소·과대표현하는지 진단.
- **정의·수식**: 분위수-분위수 그림(QQ-plot)은 두 표본의 동일 분위수를 산점. 분위편차 \(\Delta q_p = F_{model}^{-1}(p)-F_{ref}^{-1}(p)\). 경험적 CDF 차이의 최대값으로 Kolmogorov–Smirnov 통계 \(D=\sup_x|F_{model}(x)-F_{ref}(x)|\). Perkins 분포 일치도(스킬 스코어)는 두 PDF의 겹침 면적.
- **적용 도메인/자료형**: 위성/재분석/관측의 모든 연속변수(풍속, 유의파고, SST, SLA, Chl-a). 격자·시계열 모두. 짝짓기 불필요(분포만 비교)하므로 정확한 콜로케이션이 어려울 때도 사용 가능.
- **입력·전제**: 동일 기간·동일 영역 표본(또는 매치업). 충분한 표본수. log 변환이 적절한 변수(Chl-a)는 변환 후 비교.
- **해석 기준**: QQ가 1:1 선에 가까우면 분포 일치. 꼬리에서 벗어나면 극값 편향. KS \(D\)가 작을수록, Perkins 스코어가 1에 가까울수록 좋음.
- **한계·주의**: 분포 일치가 곧 시점별 일치는 아님(위상·타이밍 오차는 못 봄) → 매치업 상관과 함께 봐야 함. KS는 대표본에서 사소한 차이도 유의하게 나옴(효과크기 병행).
- **출처**: 경험적 분포·QQ·KS는 통계 표준(예: Wilks, *Statistical Methods in the Atmospheric Sciences*). 분포 일치도 스킬: Perkins et al. (2007), *Journal of Climate*, 20, 4356–4376, doi:10.1175/JCLI4253.1 (확인요: 적용 맥락은 기후모델이나 분포비교 지표로 일반 사용).

---

### 이상치 상관·기후값 제거 (이상치 상관 / Anomaly Correlation & Climatology Removal)
- **무엇을 측정/검증하나**: 강한 계절·평년 신호를 제거한 뒤 **이상치(anomaly)** 변동의 일치를 평가. 계절순환만으로 부풀려진 상관을 배제하고 실제 변동성(메소스케일·이상고온 등) 재현력을 본다.
- **정의·수식**: 이상치 \(a = X - \overline{X}_{clim}\)(기후값은 동일 기준기간의 일·월별 평균). 이상치 상관계수(ACC) \(= \frac{\sum a_f a_r}{\sqrt{\sum a_f^2 \sum a_r^2}}\). SST/SLA에서는 공통 기준 기후값(또는 동일 기간 평균) 사용이 핵심.
- **적용 도메인/자료형**: SST, SLA(이미 평균 제거된 편차), Chl-a, 해류 등. 모델 vs 위성/재분석 격자장·시계열.
- **입력·전제**: 모델·기준자료에 **동일한 기후값 정의**를 적용(서로 다른 기후값을 쓰면 인위적 편차). 충분히 긴 공통 기간.
- **해석 기준**: ACC가 높을수록 이상신호 재현 양호(관행상 ACC≳0.6을 유의미한 예측력의 목安으로 보는 분야도 있으나 변수·스케일 의존). 원시 상관보다 ACC가 크게 낮으면 "계절순환만 맞고 변동은 못 맞춤".
- **한계·주의**: 기후값 추정 오차가 이상치에 전이. 짧은 기간은 기후값이 불안정. SLA처럼 정의상 평균이 제거된 변수는 기준면·MDT 일관성을 먼저 확인.
- **출처**: 이상치 상관(ACC)·기후값 제거는 예보검증 표준(Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide*; Wilks, *Statistical Methods in the Atmospheric Sciences*).

---

### 사건/범주 검증 (범주·이진 사건 검증 / Categorical / Event Verification)
- **무엇을 측정/검증하나**: 위성에서 도출되는 **이진/범주 사건**(해빙역 유무, 전선 존재, 블룸 발생, 임계치 초과 강풍/고파, 구름 유무 등)을 모델이 맞추는지 적중/오경보 구조로 평가.
- **정의·수식**: 분할표(2×2: hit a, false alarm b, miss c, correct negative d)로부터 적중률 POD \(=a/(a+c)\), 오경보율 FAR \(=b/(a+b)\), 위협스코어 CSI \(=a/(a+b+c)\), 편의 Bias \(=(a+b)/(a+c)\), Heidke 스킬 HSS, ETS(Gilbert). 임계치를 바꿔가며 ROC 곡선·신뢰도 다이어그램.
- **적용 도메인/자료형**: 위성에서 임계화로 만든 사건장(SST 전선, Chl-a 블룸 마스크, 해빙 가장자리, 풍속>임계, 유의파고>임계). 격자(NetCDF) 사건 마스크.
- **입력·전제**: 동일 격자·동일 임계치로 모델/위성 사건장 생성, 공통 결측 마스크. 사건 정의(임계·연결성)의 일관성.
- **해석 기준**: POD↑·FAR↓·CSI↑·HSS/ETS↑가 좋음. Bias≈1이 빈도 일치. 드문 사건은 ETS/HSS가 무작위 적중을 보정하므로 CSI보다 공정. ROC AUC로 분별력 요약.
- **한계·주의**: 임계치·격자해상도·연결성 규칙에 결과가 크게 의존(공간 더블페널티 문제). 드문 사건은 표본 불균형 → 적절 스킬스코어 선택 필요. 위치가 약간 어긋난 정확한 패턴도 가혹하게 벌점(→ 객체기반 검증 병행).
- **출처**: Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (분할표·스킬스코어 표준). Wilks, *Statistical Methods in the Atmospheric Sciences*.

---

### 객체·특징 기반 공간 검증 (객체기반 / Object/Feature-based Spatial Verification)
- **무엇을 측정/검증하나**: 격자 화소별 점수 대신 **특징(객체)**—에디(eddy), SST/해색 전선, 클로로필 블룸 패치, 상승류 혀(upwelling tongue) 등—을 식별해 **위치·면적·진폭·형태**의 일치를 평가. 위치가 약간 어긋난 패턴을 화소비교가 이중처벌(double penalty)하는 문제를 완화.
- **정의·수식**: (1) 특징 추출(임계·연결성 라벨링, 에디는 Okubo–Weiss/벡터기하), (2) 모델-기준 객체 매칭, (3) 속성 오차: 중심위치 변위, 면적비, 진폭차, 회전/형태 유사도. SAL(Structure–Amplitude–Location) 류 요약지표.
- **적용 도메인/자료형**: 위성 SST/Chl-a/SLA 격자장에서의 에디·전선·블룸. 모델 vs 위성/재분석 격자(NetCDF).
- **입력·전제**: 동일 격자·결측 마스크, 일관된 특징정의(임계·최소면적). 객체 매칭 규칙.
- **해석 기준**: 위치변위·면적비·진폭차가 작을수록 좋음. 화소 RMSD는 나빠도 객체속성은 잘 맞는 "위치만 어긋난" 경우를 구분해 진단.
- **한계·주의**: 특징정의·매칭 알고리즘 의존성이 큼(파라미터 민감). 객체가 드물거나 합쳐/쪼개질 때 매칭 모호. 정량 임계는 분야·목적별로 정해야 함.
- **출처**: 객체기반 공간검증 개념: Gilleland, E., et al. (2009), "Intercomparison of Spatial Forecast Verification Methods", *Weather and Forecasting*, 24, 1416–1430, doi:10.1175/2009WAF2222269.1. SAL 지표: Wernli, H., et al. (2008), "SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts", *Monthly Weather Review*, 136, 4470–4487, doi:10.1175/2008MWR2415.1. (해양 적용은 위 일반방법을 SST/Chl-a 전선·에디에 응용 — 적용맥락 확인요.)

---

### 고도계 SLA/ADT 검증: along-track vs gridded (해수면 고도 검증 / Altimetry SLA & ADT Validation)
- **무엇을 측정/검증하나**: 모델의 해수면고도(SSH)·해수면편차(SLA)·절대역학지형(ADT)을 위성 고도계 자료와 비교. ADT = SLA + 평균역학지형(MDT)로 모델 ADT와 동일 물리량 비교 가능. 격자(gridded) 산출물 자체도 along-track으로 검증.
- **정의·수식**: 모델/격자 SSH를 궤도점으로 시공간 보간 → along-track 관측과 짝 → 셀별 RMSD·상관·분산설명도. 격자산출물(DUACS/CMEMS L4)은 OI로 다중미션 L3 along-track을 병합한 것이므로, 독립 along-track으로 교차검증.
- **적용 도메인/자료형**: 해수면(격자 NetCDF·궤도 along-track). 조위관측소(tide gauge) 시계열로도 보조검증. 모델 vs CMEMS 격자/GLORYS 재분석 비교에 직접 적용.
- **입력·전제**: 동일 기준면·MDT, 동일 기간 평균 제거(SLA는 평균 제거된 편차). 조석·역기압 보정 일관성. 모델은 위성 통과시각으로 보간.
- **해석 기준**: along-track 검증은 격자화로 평활된 소규모 신호까지 평가 가능. 격자 L4는 메소스케일은 잘 맞지만 작은 스케일은 평활화로 분산이 줄어 RMSD가 작게 보일 수 있음(아래 유효해상도 카드와 함께 해석).
- **한계·주의**: SLA vs ADT vs SSH 정의 혼동 주의(평균면·MDT). 연안은 고도계 품질 저하. 격자자료를 격자 검증에 쓰면 독립성 결여 → along-track 같은 독립 자료 사용.
- **출처**: Copernicus Marine(CMEMS) SEALEVEL L4 제품 문서 및 QUID 검증보고. "Evaluation of gridded sea surface height products based on along-track altimeter data", *Intelligent Marine Technology and Systems* (Springer, 2026), doi:10.1007/s44295-026-00092-9 — **CMEMS DT/NRT 격자와 GLORYS 재분석을 along-track(HY-2B)으로 평가**(우리 모델 vs 격자/재분석 검증 구도와 동일). SWOT 연안 SLA 검증: "Validation of Sea Level Anomalies from the SWOT Altimetry Mission Around the Coastal Regions of East Asia and the US West Coast", *Water* (2025), doi:10.3390/w17213066.

---

### 고도계 파수 스펙트럼·유효해상도 (파수 스펙트럼·유효해상도 / Wavenumber Spectrum & Effective Resolution)
- **무엇을 측정/검증하나**: along-track SSH/SLA의 파수 스펙트럼으로 모델/위성이 **실제로 분해하는 최소 공간 스케일**(유효해상도)과 잡음바닥(noise floor)을 진단. 명목 격자 간격이 아니라 실효 분해능을 평가.
- **정의·수식**: 1D 파수 스펙트럼 \(E(k)\) 계산 → 고파수 평탄부 = 잡음바닥(상수 PSD). 신호(노이즈 제거 후)와 잡음바닥이 만나는 파장을 유효해상도 \(\lambda_p\)로 정의. 메소스케일 대역(예: 90–280 km) 기울기 적합으로 비교. (확장: 모델-위성 스펙트럼의 **코히어런스/cross-spectrum**으로 스케일별 위상·진폭 일치를 평가.)
- **적용 도메인/자료형**: 해수면(along-track), 유의파고 등 1D 궤도 스펙트럼이 의미 있는 변수. 모델 vs 위성 스펙트럼 직접 비교.
- **입력·전제**: 충분히 긴 균질 궤도 구간, 결측 보간/세그먼트 처리, 일관된 디트렌딩·윈도잉(Hann 등).
- **해석 기준**: 모델 스펙트럼의 기울기·잡음바닥이 위성과 유사하면 소규모 변동성 표현이 적절. 격자 L4는 적도 ~800 km부터 고위도 ~100 km까지 위도별로 유효해상도가 변함 → 스칼라 RMSD만으로는 놓치는 정보를 포착.
- **한계·주의**: 스펙트럼 추정은 윈도잉·세그먼트 길이·결측 처리에 민감. 잡음바닥 진단 대역 선택이 유효해상도 값을 좌우.
- **출처**: Ballarotta, M., et al. (2019), "On the resolutions of ocean altimetry maps", *Ocean Science*, 15, 1091–1109, doi:10.5194/os-15-1091-2019. Dufau, C., et al. (2016), "Mesoscale resolution capability of altimetry: Present and future", *JGR Oceans*, doi:10.1002/2015JC010904 (확인요: 권·페이지).

---

### 위성 SST L2/L3/L4 검증 (GHRSST 체계 / Satellite SST Validation, GHRSST)
- **무엇을 측정/검증하나**: 위성 해수면온도(SST)를 처리수준별(L2P, L3U/L3C/L3S, L4)로 in situ(부이·Argo·선박)와 비교하고, 자료 간 안정성·일관성을 상시 모니터링.
- **정의·수식**: 처리수준 — L2P(원해상도+불확실성·플래그), L3U(미병합 격자), L3C(단일센서 병합), L3S(다중센서 병합), L4(보간으로 빈틈 없는 격자). 검증 = 매치업 후 편차/로버스트SD/상관(위 통계 카드). 모델 검증 시 L4(빈틈없음)는 편의적이나 보간 정보 혼입 주의.
- **적용 도메인/자료형**: 수온(격자 NetCDF). 기준자료는 iQuam 등 QC된 in situ.
- **입력·전제**: quality_level 플래그로 선별, in situ 측정깊이/시각 메타데이터, skin/bulk·일주변동 보정(아래 카드).
- **해석 기준**: 야간·고품질 매치업에서 |bias|·robust SD가 센서 사양 내인지 확인. L4 간 상호비교(L4-SQUAM)로 분석장 일관성 점검. 안정성(시계열 추세) 모니터링.
- **한계·주의**: L4는 보간으로 빈틈을 메워 독립 검증의 독립성을 해칠 수 있음(L4 검증에 L4가 쓴 in situ를 재사용하면 안 됨). 구름역에서 IR SST 결측 편향.
- **출처**: GHRSST 데이터 규격·Task Team 문서 (ghrsst.org). SST Quality Monitor(SQUAM): Dash, P., et al. (2010), "The SST Quality Monitor (SQUAM)", *Journal of Atmospheric and Oceanic Technology*, 27, 1899–1917, doi:10.1175/2010JTECHO756.1. in situ QC(iQuam): Xu, F., & Ignatov, A. (2014), "In situ SST Quality Monitor (iQuam)", *J. Atmos. Oceanic Technol.*, 31, 164–180, doi:10.1175/JTECH-D-13-00121.1.

---

### Skin/Bulk·일주변동 보정 (스킨-벌크·일주변동 보정 / Skin–Bulk & Diurnal Adjustment)
- **무엇을 측정/검증하나**: 위성 IR SST(skin, ~10–20 µm)와 in situ/모델 SST(bulk, ~깊이 1–5 m, 또는 foundation ~10 m)의 **측정깊이·측정시각 차이**를 보정해 공정 비교.
- **정의·수식**: skin–bulk 차(쿨스킨 효과, 보통 야간 ~ -0.1~-0.2 K)와 일주성층(주간 가열 ΔSST) 보정. 예: skin SST에 보정량을 더해 "깊이 20 cm 환산 SST"를 만들어 표류부이와 비교. 모델은 foundation/bulk를 skin으로 환산하거나 그 반대.
- **적용 도메인/자료형**: 위성 SST 검증·동화 전반. 주간·약풍 시 일주가열이 클 때 특히 중요.
- **입력·전제**: 풍속·일사·시각(쿨스킨·웜레이어 모델 입력), 위성/부이 관측 시각차. 측정깊이 정의(skin/sub-skin/depth/foundation).
- **해석 기준**: 보정 후 주·야간 위성-부이 차이가 ~0.01 K 수준까지 일치 가능 → 보정의 타당성. 보정 없이 비교하면 주간 편차가 과장됨.
- **한계·주의**: 쿨스킨/웜레이어 모델 자체의 불확실성. 일주변동이 강한 연안·약풍역에서 보정 오차 큼. 어떤 깊이로 통일할지(검증 목적)에 따라 결과 달라짐.
- **출처**: Embury, O., Merchant, C. J., & Corlett, G. K. (2012), "A reprocessing for climate of sea surface temperature from the along-track scanning radiometers: Initial validation, accounting for skin and diurnal variability effects", *Remote Sensing of Environment*, 116, 62–78, doi:10.1016/j.rse.2011.02.028. SST 정의 체계(skin/sub-skin/foundation)·cool-skin/diurnal: GHRSST 규격(ghrsst.org; Donlon et al. 관련 — 서지 확인요).

---

### SST 전선·수평경도 검증 (SST 전선·경도 / SST Front / Gradient Verification)
- **무엇을 측정/검증하나**: 모델 SST의 **수평경도·전선(front)** 위치·강도를 위성 SST(고해상 L2/L3)와 비교. 평균 SST는 맞아도 전선 구조(연안용승·해류경계)가 흐려지는지 진단.
- **정의·수식**: 수평경도 크기 \(|\nabla \mathrm{SST}| = \sqrt{(\partial_x T)^2+(\partial_y T)^2}\). 전선 검출: 경도 임계법 또는 히스토그램기반(Cayula–Cornillon SIED). 비교: 경도 통계(분포·평균강도), 전선 위치 변위(객체기반 카드 연계), 전선확률(FP) 지도 차이.
- **적용 도메인/자료형**: 위성 SST·Chl-a 격자(NetCDF). 모델 vs 위성. 고해상 위성(예: VIIRS/Sentinel-3)일수록 전선 분해 유리.
- **입력·전제**: 동일 격자·해상도로 재격자화(또는 위성해상도로 모델 평가), 구름 마스크. 경도는 해상도 의존이 크므로 동일 스케일에서 비교.
- **해석 기준**: 모델 경도 분포가 위성과 유사하고 전선 위치가 일치하면 양호. 모델 경도가 체계적으로 약하면 전선 과소(수치확산·해상도 부족) 시사.
- **한계·주의**: 경도는 해상도·평활화에 매우 민감 → 반드시 동일 스케일 비교. 구름틈·결측이 경도장을 왜곡. 위성 L4(평활)는 전선이 흐려 경도 비교에 부적합(고해상 L2/L3 사용).
- **출처**: 전선 검출(히스토그램기반): Cayula, J.-F., & Cornillon, P. (1992), "Edge Detection Algorithm for SST Images", *Journal of Atmospheric and Oceanic Technology*, 9, 67–80, doi:10.1175/1520-0426(1992)009<0067:EDAFSI>2.0.CO;2 (확인요: 권·페이지 표기). 경도·전선 통계 비교는 정착된 관행(표준 관행).

---

### 산란계 해상풍 검증 (산란계 해상풍 검증 / Scatterometer Wind Validation)
- **무엇을 측정/검증하나**: 산란계(ASCAT/OSCAT/HY-2 등) 해상 10 m 등가중립풍의 **풍속·풍향(벡터)**을 부이·NWP·타 산란계와 비교. 벡터 성분(u,v) 또는 속도/방향 각각 검증.
- **정의·수식**: 풍속 bias/RMSD, 풍향 RMSD(원형통계), u/v 성분 RMSD. 표층류 영향: 산란계는 해수면 상대풍을 보므로 (풍속 bias) ≈ 다운윈드 표층류의 ~0.96배 만큼 음(-)편차 → 표층류 보정 시 RMSD ~15% 감소 사례.
- **적용 도메인/자료형**: 해상풍(궤도 swath·격자). 기준자료는 부이(점)·NWP(격자; ERA5 포함).
- **입력·전제**: 등가중립풍 vs 실제풍 정의 일치, 비/강수 플래그(우적 영향), 표층류·SST 보조정보. 부이-위성 시공간 매칭.
- **해석 기준**: ASCAT은 우중에서도 QuikSCAT보다 우수. 풍속 GMF 갱신이 부이와의 풍속 bias를 줄임. 풍향은 풍속 약할 때 불확실성 큼.
- **한계·주의**: 분해능 차이(부이 점 vs 산란계 셀)로 ETC 필요. 강수·연안·낮은 풍속에서 품질 저하. 표층류·대기안정도 미보정 시 계통편차.
- **출처**: Stoffelen (1998) TC, doi:10.1029/97JC03180. Yang, X., et al. (2019), "Comparison of Oceansat-2 Scatterometer Wind Data with Global Moored Buoys and ASCAT Observation", *Advances in Meteorology*, 2019, 1651267 (확인요: DOI). 표층류 영향: "Characterizing the Effect of Ocean Surface Currents on Advanced Scatterometer (ASCAT) Winds Using Open Ocean Moored Buoy Data", *Remote Sensing* (2023), 15(18), 4630, doi:10.3390/rs15184630. Vogelzang & Stoffelen (2021) QC, doi:10.1029/2021JC017189.

---

### 해색 Chl-a 검증 프로토콜 (해색 매치업 / Ocean Color Matchup: Bailey–Werdell / Zibordi)
- **무엇을 측정/검증하나**: 위성 클로로필-a(Chl-a)·원격반사도(Rrs)를 현장 측정과 매치업으로 검증. log10 공간 통계가 핵심(Chl-a는 대수정규 분포 근사).
- **정의·수식**: Bailey & Werdell(2006) 절차 — 현장점 중심 **3×3 화소 윈도우** 추출, 유효화소 ≥50% 유지, ±1.5 표준편차 밖 화소 제외, 잔여화소 변동계수 CV>0.15면 매치업 제외, 시간윈도우(예 ±3 h) 적용. 통계는 log10에서: median absolute error·bias가 곱셈적 지표가 됨. Zibordi et al.(2009)은 더 엄격한 QC.
- **적용 도메인/자료형**: 해색(격자 NetCDF: Chl-a, Rrs). 현장은 선박·AERONET-OC·부이.
- **입력·전제**: Rrs/Chl-a 알고리즘 일치, 대기보정 품질플래그, 현장-위성 시각차. log10 변환 전 양수성.
- **해석 기준**: 프로토콜(필터·윈도우·CV 임계값)에 따라 매치업 수·통계가 달라지므로 어떤 프로토콜인지 명시. log10 RMSD·MdAE·회귀로 평가.
- **한계·주의**: 프로토콜 의존성이 큼. 연안 Case-2 수역·픽셀경계효과로 대표성오차 큼. 선형공간 통계는 대수정규 분포에서 편향(반드시 log10).
- **출처**: Bailey, S. W., & Werdell, P. J. (2006), "A multi-sensor approach for the on-orbit validation of ocean color satellite data products", *Remote Sensing of Environment*, 102(1–2), 12–23, doi:10.1016/j.rse.2006.01.015. Zibordi, G., et al. (2009), "Validation of satellite ocean color primary products at optically complex coastal sites: Northern Adriatic Sea, Northern Baltic Proper and Gulf of Finland", *Remote Sensing of Environment*, 113(12), 2574–2591, doi:10.1016/j.rse.2009.07.016. AERONET-OC 네트워크: Zibordi, G., et al. (2009), "AERONET-OC: A Network for the Validation of Ocean Color Primary Products", *J. Atmos. Oceanic Technol.*, 26, 1634–1651, doi:10.1175/2009JTECHO654.1.

---

### L2→L3 비닝·격자화 (스와스 비닝·격자화 / Swath Binning & Gridding)
- **무엇을 측정/검증하나**: 궤도(L2 swath) 위성자료를 고정 격자(L3)로 모으는 처리. 모델 격자와 비교하려면 위성을 격자화하거나(또는 모델을 궤도로 보간) 스케일을 맞춰야 함.
- **정의·수식**: L2 화소 중심이 속하는 빈(bin)에 기여 → 등면적 빈(예: 정현곡선 sinusoidal/ISIN 투영)에서 가중평균. 가중방식: 균등/면적가중/역거리/최근접. 시간윈도(일·주·월)로 집성.
- **적용 도메인/자료형**: 해색·SST·풍 등 swath 자료를 격자 모델과 비교할 때. NetCDF L3 산출.
- **입력·전제**: 화소 위경도·품질플래그, 투영·격자 정의, 집성 가중·시간윈도 선택.
- **해석 기준**: 표본밀도가 충분하면 가중방식 차이는 작을 수 있음. 격자화로 평활되므로 분산이 줄어듦(검증 RMSD 해석 시 고려).
- **한계·주의**: 격자화 자체가 평활·대표성오차를 만들어 검증 결과에 영향. 모델을 궤도로 보간하는 방식(on-swath)과 둘 다 격자화하는 방식의 결과가 다를 수 있음 → 방법 명시.
- **출처**: NASA Ocean Color — Level-3 Binning Scheme(Integerized Sinusoidal) 문서 (oceancolor.gsfc.nasa.gov). NASA SeaDAS — Level 3 Binning Operator 문서 (seadas.gsfc.nasa.gov).

---

### 궤도/스와스 처리·교차점 분석 (궤도·교차점 분석 / Orbit/Swath Processing & Crossover Analysis)
- **무엇을 측정/검증하나**: 위성의 시공간 표본화 특성(궤도 반복주기·결측)을 다루고, 상·하행 궤도 교차점(crossover)에서의 차이로 위성자료의 **자체일관성·계통오차(궤도·기준면 오차 등)**를 진단.
- **정의·수식**: 같은 지점을 짧은 시차로 통과하는 상승/하강 궤도 교차점에서 \(\Delta = X_{asc}-X_{desc}\). 교차점 차의 통계(편차·SD)로 내부정합성 평가; 시공간 보정으로 변동 신호 제거 후 잔차 분석.
- **적용 도메인/자료형**: 고도계 SSH/SLA(교차점 표준), 산란계·SST의 상·하행 일관성에도 응용.
- **입력·전제**: 궤도 메타데이터(시각·상하행), 교차점 좌표, 시차 보정용 변동 모델.
- **해석 기준**: 교차점 차가 작을수록 내부정합성 좋음. 모델 검증 전 위성자료 자체의 정합성을 먼저 확인하는 사전점검으로 유용.
- **한계·주의**: 교차점 시차 동안의 실제 변동을 오차로 오인할 수 있음. 위성 고유 처리(궤도·조석·기준면 보정) 품질에 의존.
- **출처**: 교차점 분석은 altimetry 정합성 평가의 정착된 표준 방법(AVISO/CMEMS 고도계 처리·검증 문서 — 구체 서지 확인요).

---

### 불확실성 정합 검증 (불확실성 검증 / Uncertainty Validation: u-plot / standardized error)
- **무엇을 측정/검증하나**: 위성(또는 모델) 자료가 **함께 보고하는 픽셀별 불확실성**이 실제 오차 분포와 일치하는지 점검. "오차뿐 아니라 오차추정치도 검증."
- **정의·수식**: 표준화 오차 \(z = (X_{sat}-X_{ref})/\sqrt{u_{sat}^2+u_{ref}^2+\sigma_{repr}^2}\). \(z\)의 표준편차가 1에 가깝고 분포가 정규에 가까우면 불확실성이 잘 보정됨. u-plot/신뢰도 곡선으로 명목 vs 실측 신뢰구간 비교.
- **적용 도메인/자료형**: 불확실성 변수를 제공하는 위성자료(SST L2P, SSS, altimetry 오차 추정 등).
- **입력·전제**: 위성/기준자료의 불확실성 추정치, 대표성오차 추정, 매치업.
- **해석 기준**: \(\mathrm{std}(z)\approx 1\)이면 적정, >1이면 불확실성 과소평가, <1이면 과대평가. 동화·앙상블 신뢰도 평가의 핵심.
- **한계·주의**: 대표성오차를 빼먹으면 \(z\) 해석 왜곡. 기준자료 불확실성도 필요. 분포 꼬리(극단오차)는 별도 점검.
- **출처**: Merchant, C. J., et al. (2019), "Satellite-based time-series of sea-surface temperature since 1981 for climate applications", *Scientific Data*, 6, 223, doi:10.1038/s41597-019-0236-x — ESA-CCI SST(불확실성 포함 검증). 표준화 오차/u-plot은 불확실성 검증 표준 관행.

---

## 출처 (References)

> 아래 서지는 웹 검색으로 저자·연도·저널·DOI를 **확인한 것**이다. 미확인 세부는 "(확인요)"로 표시했다. DOI를 임의로 생성하지 않았다.

**핵심 방법론 논문 (검증·콜로케이션)**
- Stoffelen, A. (1998). Toward the true near-surface wind speed: Error modeling and calibration using triple collocation. *Journal of Geophysical Research: Oceans*, 103(C4), 7755–7766. doi:10.1029/97JC03180. — 삼중대조(TC) 원논문.
- Caires, S., & Sterl, A. (2003). Validation of ocean wind and wave data using triple collocation. *Journal of Geophysical Research: Oceans*, 108(C3), 3098. doi:10.1029/2002JC001491.
- McColl, K. A., Vogelzang, J., Konings, A. G., Entekhabi, D., Piles, M., & Stoffelen, A. (2014). Extended triple collocation: Estimating errors and correlation coefficients with respect to an unknown target. *Geophysical Research Letters*, 41, 6229–6236. doi:10.1002/2014GL061322.
- Vogelzang, J., & Stoffelen, A. (2021). Quadruple Collocation Analysis of In-Situ, Scatterometer, and NWP Winds. *Journal of Geophysical Research: Oceans*, 126, e2021JC017189. doi:10.1029/2021JC017189.
- Siu, L. W., et al. (2024). Summarizing multiple aspects of triple collocation analysis in a single diagram. *Frontiers in Remote Sensing*, 5. doi:10.3389/frsen.2024.1395442.
- The Impact on Triple/N-Way Collocation-Based Validation of Remote Sensing Products Due to Non-Ideal Error Statistics. *Remote Sensing* (2025). doi:10.3390/rs17223751. — TC 가정 위반 영향.

**공통 검증통계 (표준 다이어그램·지표)**
- Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single diagram. *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183–7192. doi:10.1029/2000JD900719. — Taylor 다이어그램.
- Willmott, C. J. (1981). On the validation of models. *Physical Geography*, 2(2), 184–194. doi:10.1080/02723646.1981.10642213. — 일치도 지수(index of agreement).
- Perkins, S. E., et al. (2007). Evaluation of the AR4 climate models' simulated daily maximum temperature, minimum temperature, and precipitation over Australia using probability density functions. *Journal of Climate*, 20, 4356–4376. doi:10.1175/JCLI4253.1 (확인요: 분포일치 스킬스코어 출처로 사용).
- Gilleland, E., Ahijevych, D., Brown, B. G., Casati, B., & Ebert, E. E. (2009). Intercomparison of Spatial Forecast Verification Methods. *Weather and Forecasting*, 24, 1416–1430. doi:10.1175/2009WAF2222269.1. — 객체/공간 검증 개관.
- Wernli, H., Paulat, M., Hagen, M., & Frei, C. (2008). SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts. *Monthly Weather Review*, 136, 4470–4487. doi:10.1175/2008MWR2415.1.

**해색(Ocean Color)**
- Bailey, S. W., & Werdell, P. J. (2006). A multi-sensor approach for the on-orbit validation of ocean color satellite data products. *Remote Sensing of Environment*, 102(1–2), 12–23. doi:10.1016/j.rse.2006.01.015.
- Zibordi, G., et al. (2009). Validation of satellite ocean color primary products at optically complex coastal sites: Northern Adriatic Sea, Northern Baltic Proper and Gulf of Finland. *Remote Sensing of Environment*, 113(12), 2574–2591. doi:10.1016/j.rse.2009.07.016. — 엄격한 매치업/현장 QC.
- Zibordi, G., et al. (2009). AERONET-OC: A Network for the Validation of Ocean Color Primary Products. *Journal of Atmospheric and Oceanic Technology*, 26(8), 1634–1651. doi:10.1175/2009JTECHO654.1.

**SST (GHRSST 체계)**
- GHRSST Data Specification 및 Task Team 문서 (ghrsst.org). — L2P/L3U/L3C/L3S/L4 정의, 검증·상호비교 관행.
- Dash, P., Ignatov, A., Kihai, Y., & Sapper, J. (2010). The SST Quality Monitor (SQUAM). *Journal of Atmospheric and Oceanic Technology*, 27(11), 1899–1917. doi:10.1175/2010JTECHO756.1. — 위성-L4 차이 통계·시계열 안정성/플랫폼 일관성.
- Xu, F., & Ignatov, A. (2014). In situ SST Quality Monitor (iQuam). *Journal of Atmospheric and Oceanic Technology*, 31(1), 164–180. doi:10.1175/JTECH-D-13-00121.1. — in situ SST QC.
- Embury, O., Merchant, C. J., & Corlett, G. K. (2012). A reprocessing for climate of sea surface temperature from the along-track scanning radiometers: Initial validation, accounting for skin and diurnal variability effects. *Remote Sensing of Environment*, 116, 62–78. doi:10.1016/j.rse.2011.02.028.
- Merchant, C. J., et al. (2019). Satellite-based time-series of sea-surface temperature since 1981 for climate applications. *Scientific Data*, 6, 223. doi:10.1038/s41597-019-0236-x. — ESA-CCI SST, 불확실성 검증.
- (SST 정의 체계 skin/sub-skin/foundation 및 cool-skin/diurnal) GHRSST 규격/관련 Donlon et al. 문헌 (확인요: 구체 서지).

**고도계(Altimetry) / 해수면**
- Copernicus Marine Service (CMEMS), SEALEVEL_GLO_PHY_L4 제품 문서 및 검증보고(QUID). — DUACS/OI 격자 SLA·ADT.
- Ballarotta, M., et al. (2019). On the resolutions of ocean altimetry maps. *Ocean Science*, 15, 1091–1109. doi:10.5194/os-15-1091-2019.
- Dufau, C., et al. (2016). Mesoscale resolution capability of altimetry: Present and future. *Journal of Geophysical Research: Oceans* (확인요: 권·페이지; doi:10.1002/2015JC010904 추정 — 원문 확인).
- Evaluation of gridded sea surface height products based on along-track altimeter data. *Intelligent Marine Technology and Systems* (Springer, 2026). doi:10.1007/s44295-026-00092-9. — CMEMS DT/NRT·GLORYS를 along-track(HY-2B)으로 평가.
- Validation of Sea Level Anomalies from the SWOT Altimetry Mission Around the Coastal Regions of East Asia and the US West Coast. *Water* (2025), 17(21), 3066. doi:10.3390/w17213066.

**산란계(Scatterometer) 해상풍**
- Yang, X., et al. (2019). Comparison of Oceansat-2 Scatterometer Wind Data with Global Moored Buoys and ASCAT Observation. *Advances in Meteorology*, 2019, 1651267 (확인요: DOI).
- Characterizing the Effect of Ocean Surface Currents on Advanced Scatterometer (ASCAT) Winds Using Open Ocean Moored Buoy Data. *Remote Sensing* (2023), 15(18), 4630. doi:10.3390/rs15184630.

**대표성오차 / 전선검출 / 처리**
- Janjić, T., et al. (2018). On the representation error in data assimilation. *Quarterly Journal of the Royal Meteorological Society*, 144, 1257–1278. doi:10.1002/qj.3130.
- Spatial Scales of Sea Surface Salinity Subfootprint Variability in the SPURS Regions. *Remote Sensing* (2020). doi:10.3390/rs12233996.
- Cayula, J.-F., & Cornillon, P. (1992). Edge Detection Algorithm for SST Images. *Journal of Atmospheric and Oceanic Technology*, 9(1), 67–80 (확인요: 정확한 권·페이지·DOI).
- NASA Ocean Color — Integerized Sinusoidal Binning Scheme for Level 3 Data (oceancolor.gsfc.nasa.gov). NASA SeaDAS — Level 3 Binning Operator (seadas.gsfc.nasa.gov).

**표준 참고문헌(교과서·지침)**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*. (편차/RMSD/상관/분포비교 등 기본 검증통계 표준)
- Jolliffe, I. T., & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide*. (범주·이상치상관·검증 일반)
- 로버스트 통계: 중앙값·MAD(1.4826×MAD=로버스트 SD)는 통계 표준 관행.
- WMO/JCOMM 해양 변수 검증 지침류 (확인요: 구체 문서·연도).
