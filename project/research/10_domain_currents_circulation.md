# 도메인 10 — 해류·조류·순환 (Currents / Circulation) 분석·검증 방법 카탈로그

본 문서는 수치모델이 산출한 해류장(유속 u/v, 유향, 수송량 등)을 ERA5/GLORYS 등 권위 재분석자료, 정점·표류 관측(ADCP, 표류부이), HF radar 표면류, 위성 고도계 기반 지형류와 자동 비교·검증하기 위한 분석/검증 방법을 망라한다. 벡터 자료의 특수성(방향성·회전성)을 반영하는 지표(벡터·복소상관, 조류타원, 회전스펙트럼)와, 흐름장의 구조적 특징을 진단하는 라그랑지안·와류 진단(Okubo-Weiss, eddy census, FTLE/LCS)을 포괄한다. 각 방법은 입력 자료형(격자/시계열/위성), 해석 기준, 한계와 함께 "메서드 카드" 형식으로 정리한다.

> **이 카탈로그를 쓰는 법(우리 모델 vs 권위자료 비교 관점)**
> - **NetCDF 격자장**(우리 모델 u/v, GLORYS, ERA5 표층류, 위성 지형류): 공간 패턴·EKE·Okubo-Weiss·와류 센서스·FTLE·수송량·Taylor·EOF.
> - **CSV/텍스트 시계열**(ADCP, 유속계, 표류부이, HF radar 격자점 추출): 성분 RMSE/MAE/Bias·복소상관·회전스펙트럼·조류타원·PVD·주축타원·유향 원형통계.
> - **공통 전제**: 비교 전에 반드시 (a) 동일 좌표계(동/북 성분, 진북 기준), (b) 동일 기간·동일 샘플링으로 시간정렬, (c) 모델 격자→관측 위치/심도로 보간, (d) 단위 통일(m/s). 이 정렬·보간 단계가 모든 카드의 공통 입력 전제다.

## 한 줄 목차 (이 파일에 담은 방법들)
- **벡터 평균류·유속/유향 통계** — 평균 흐름·표준편차·항상성(steadiness) 진단
- **스칼라 성분 오차지표 (RMSE/MAE/Bias)** — u/v 성분별 기본 검증 통계
- **복소(벡터) 상관계수 — Kundu (1976)** — 회전 허용 벡터 상관, 위상각 산출
- **벡터 상관 (Crosby/Breaker 정의)** — 회전·반사 불변 벡터 상관계수
- **벡터 RMSE·복소 RMSE** — 벡터 차의 크기 기반 오차
- **유향(방향) 검증 — 각도 오차·원형통계** — circular RMSE, 단위벡터 방향 평균
- **주축·변동타원 (Principal axis / variance ellipse)** — 변동 주축·이방성, 연안 정렬 진단
- **속력 분포 비교 (Q-Q·PDF·CDF)** — 유속 분포·꼬리 일치도, 극값 재현
- **Progressive Vector Diagram (PVD)** — 의사 라그랑지안 변위 궤적 비교
- **조화분석·조류타원 (Tidal ellipse)** — 장축/단축/경사/위상, 조석류 검증
- **회전스펙트럼 (Rotary spectra) — Gonella (1972)** — CW/CCW 에너지·회전계수
- **수송량 (Volume/Mass transport)** — 단면 적분 수송, Sverdrup 균형 검증
- **운동에너지 진단 (MKE / EKE)** — 평균·와류 운동에너지, 변동성 검증
- **표면류 성분 분해·검증 (지형류+Ekman+Stokes)** — 총 표면류 vs GLORYS/OSCAR/GlobCurrent
- **Okubo-Weiss 파라미터** — 변형 대 회전 진단, 와류 후보 영역
- **와류 센서스·추적 (Eddy census/tracking)** — SLA 폐곡선·기하학 기반 와류 통계
- **유한시간 Lyapunov 지수 / LCS (FTLE/FSLE)** — 라그랑지안 수송장벽·코히어런트 구조
- **라그랑지안 입자추적·표류부이 대조** — 궤적·분리거리(separation) 기반 검증
- **HF radar / ADCP 대조 검증 프로토콜** — 표면류·정점류 교차검증 절차
- **Murphy 스킬 스코어·MSE 기반 스킬** — 기준자료 대비 정규화 스킬, 편향 분해
- **Taylor 다이어그램·표준화 통계 요약** — 상관·표준편차·centered RMSE 통합표시
- **흐름장 공간 패턴 비교 (EOF·패턴상관)** — 순환 구조의 공간 일치도

---

### 벡터 평균류·유속/유향 통계 (Vector mean current & speed/direction statistics)
- **무엇을 측정/검증하나**: 흐름장의 1차 통계 — 평균 흐름 벡터(mean current), 유속(speed) 평균·표준편차, 유향 분포, 흐름의 "항상성/일관성(steadiness, persistence)". 모델과 관측의 평균류 크기·방향이 맞는지 가장 먼저 확인하는 기본 진단.
- **정의·수식**:
  - 평균류: $\bar{u}=\frac{1}{N}\sum u_i,\ \bar{v}=\frac{1}{N}\sum v_i$, 평균 흐름 속력 $|\bar{\mathbf{u}}|=\sqrt{\bar{u}^2+\bar{v}^2}$.
  - 평균 속력(스칼라): $\overline{|\mathbf{u}|}=\frac{1}{N}\sum\sqrt{u_i^2+v_i^2}$.
  - 항상성(steadiness): $S=|\bar{\mathbf{u}}|/\overline{|\mathbf{u}|}$ (0~1; 1이면 항상 같은 방향).
  - 평균 유향: $\theta=\operatorname{atan2}(\bar{v},\bar{u})$.
- **적용 도메인/자료형**: 시계열(정점 ADCP/유속계, 표류부이), 격자장(모델/재분석 각 격자점). 표면·각 층 모두.
- **입력·전제**: u/v 동일 좌표계(동/북 성분)로 정렬. 결측 처리, 동일 기간·동일 샘플링 정렬. 좌표 회전 시 부호 일관성.
- **해석 기준**: 평균류 크기·방향, steadiness가 관측과 정성·정량적으로 부합하면 양호. steadiness가 낮은 곳(강한 변동·반전류)에서는 평균만으로 판단 불가 → 변동성 지표 병행.
- **한계·주의**: 평균은 양방향 왕복류(조류 우세 지역)에서 거의 0이 될 수 있어 "흐름이 없다"는 오해 유발. 반드시 변동·타원·스펙트럼과 함께 본다. 스칼라 평균 속력과 벡터 평균 속력을 혼동 금지.
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (표준 참고문헌). steadiness 정의는 동 교과서 및 일반 해양관측 관행.

---

### 스칼라 성분 오차지표 — RMSE / MAE / Bias (Component error statistics)
- **무엇을 측정/검증하나**: u, v 각 성분(또는 속력)에 대한 모델–관측 차의 평균적 크기·치우침. 가장 기본적·보편적 검증 통계.
- **정의·수식** (성분 $x\in\{u,v,|\mathbf{u}|\}$):
  - Bias: $\text{Bias}=\overline{x_{model}-x_{obs}}$
  - RMSE: $\sqrt{\frac{1}{N}\sum (x_{model}-x_{obs})^2}$
  - MAE: $\frac{1}{N}\sum |x_{model}-x_{obs}|$
  - centered/unbiased RMSE: $\sqrt{\text{RMSE}^2-\text{Bias}^2}$
  - (보강) 회귀 진단: 최소제곱 기울기 $b$·절편 $a$, 결정계수 $R^2$. 무편향이면 $b\approx1,\ a\approx0$.
- **적용 도메인/자료형**: 시계열·격자 모두. 위성(고도계 지형류), HF radar, ADCP 등 모든 자료형에 공통.
- **입력·전제**: 시·공간 정렬 및 보간(모델 격자 → 관측 위치/시각). 같은 기준층·기준심도. 단위 통일(m/s 또는 cm/s).
- **해석 기준**: HF radar 표면류 검증 관행에서 성분 RMSE 약 5~20 cm/s, 상관 0.3~0.9가 흔한 범위(연안 변동 큼). 값이 작을수록 좋음. 절대 임계값은 지역·자료 정밀도 의존.
- **한계·주의**: 성분별로 보면 벡터의 회전·방향 일치 정보를 놓친다(벡터·복소상관 병행 필요). 속력(|u|) RMSE는 방향 오차를 숨긴다. 결측·이상치 민감(robust 통계 병행 권장).
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification*; 해양 모델 스킬 종합은 Stow et al. (2009), *J. Mar. Syst.*, 76, 4–15. HF radar 범위는 검증 리뷰([MDPI RS 2025](https://www.mdpi.com/2072-4292/17/7/1243)).

---

### 복소(벡터) 상관계수 — Kundu (1976) (Complex / vector correlation, Kundu)
- **무엇을 측정/검증하나**: 두 벡터 시계열(예: 모델류 vs 관측류)의 상관을 회전을 허용하여 단일 복소수로 측정. 크기 상관(modulus)과 두 벡터장 사이의 평균 회전각(phase)을 동시에 산출. 성분별 상관이나 속력 상관에서 잃는 방향 정보를 보존.
- **정의·수식**: 벡터를 복소수로 표현 $w=u+iv$. 두 시계열 $w_1,\ w_2$에 대해
  $$\rho = \frac{\langle w_1^{*}\, w_2\rangle}{\sqrt{\langle |w_1|^2\rangle}\sqrt{\langle |w_2|^2\rangle}}$$
  여기서 $*$는 켤레, $\langle\cdot\rangle$는 시간평균. $|\rho|$는 상관강도(0~1), $\arg(\rho)$는 $w_1$ 대비 $w_2$의 평균 회전각(반시계+).
- **적용 도메인/자료형**: 벡터 시계열(정점 ADCP/유속계, 표류부이, HF radar 격자점 시계열, 모델 격자점 시계열).
- **입력·전제**: 동일 시각 정렬, 평균 제거(편차 기준) 또는 원시계열 합의. 두 시계열 동일 좌표계. 회전각 해석을 위해 동/북 성분 정의 일관.
- **해석 기준**: $|\rho|$가 1에 가까울수록 두 흐름의 시간변동이 잘 일치. $\arg(\rho)\approx 0$이면 평균적 회전 편차 없음(방향 정렬 양호); 유의한 위상각은 모델 흐름이 관측 대비 체계적으로 회전(예: 에크만/경계층 효과, 좌표 오정렬)했음을 시사.
- **한계·주의**: "회전 불변"이라 두 장이 서로 다른 방향이라도 일정 회전이면 높은 $|\rho|$가 나올 수 있음 → 위상각을 반드시 함께 보고. 정의가 여러 가지(아래 Crosby 정의와 다름)이므로 사용 정의를 명시. 정상성(stationarity) 가정.
- **출처**: Kundu, P. K. (1976), "Ekman veering observed near the ocean bottom," *J. Phys. Oceanogr.*, 6, 238–242 — 이 논문에서 복소 상관·위상으로 두 유속 벡터 시계열의 회전(veering)을 정량화했다([AMS 원문](https://journals.ametsoc.org/view/journals/phoc/6/2/1520-0485_1976_006_0238_evonto_2_0_co_2.xml)). 방법 개관: Emery & Thomson 교과서(복소상관 절).

---

### 벡터 상관 (Crosby–Breaker–Gemmill 정의) (Vector correlation coefficient)
- **무엇을 측정/검증하나**: 두 2차원 벡터장 사이의 상관을, 임의의 선형변환(회전·반사·스케일)에 불변인 형태로 정의한 계수($\rho_v^2$, 0~2 범위). Kundu 복소상관과 달리 회전+반사까지 허용하고, 대표본 근사로 가설검정도 가능.
- **정의·수식**: 4개 성분 공분산행렬(두 벡터의 u/v 교차공분산)로부터 산출. 개략적으로
  $$\rho_v^2 = \text{trace}\!\left(\Sigma_{11}^{-1}\Sigma_{12}\,\Sigma_{22}^{-1}\Sigma_{21}\right)$$
  ($\Sigma_{11},\Sigma_{22}$ 각 벡터의 2×2 공분산, $\Sigma_{12}$ 교차공분산). 값 범위 0(무상관)~2(완전 선형관계).
- **적용 도메인/자료형**: 벡터 시계열·벡터 격자장(바람·해류). 모델 vs 관측 흐름장 전체의 상관 요약에 사용.
- **입력·전제**: 동일 표본 정렬, 평균 제거. 충분한 자유도(공분산 추정 안정). 소표본(N≥8)은 원논문의 시뮬레이션 기반 수정분포 사용.
- **해석 기준**: $\rho_v^2$가 2에 가까울수록 강한 선형(회전 포함) 관계. 정규화 형태($\rho_v^2/2$, 0~1)로 보고하기도. 0에 가까우면 무관계.
- **한계·주의**: 회전·반사 불변이라 물리적으로 "반대로 도는" 흐름도 높게 나올 수 있음 → 물리 해석 시 주의. 표본 수 적으면 상향 편의(bias). Kundu 정의와 수치 비교 시 정의 차 명시.
- **출처**: Crosby, Breaker & Gemmill (1993), "A proposed definition for vector correlation in geophysics: Theory and Application," *J. Atmos. Oceanic Technol.*, 10, 355–367 ([AMS 원문](https://journals.ametsoc.org/view/journals/atot/10/3/1520-0426_1993_010_0355_apdfvc_2_0_co_2.xml)).

---

### 벡터 RMSE · 복소 RMSE (Vector RMSE / complex RMSE)
- **무엇을 측정/검증하나**: 모델·관측 벡터 차이의 크기(벡터 차의 유클리드 길이)를 평균한 오차. 성분 분리 없이 흐름 벡터 전체의 불일치를 하나의 양으로.
- **정의·수식**:
  $$\text{VRMSE}=\sqrt{\frac{1}{N}\sum \left[(u_m-u_o)^2+(v_m-v_o)^2\right]}$$
  복소 표기 $w=u+iv$로는 $\sqrt{\frac{1}{N}\sum |w_m-w_o|^2}$. 벡터 bias는 차 벡터의 평균 $\overline{\mathbf{u}_m-\mathbf{u}_o}$.
- **적용 도메인/자료형**: 벡터 시계열·격자(HF radar, ADCP, 표면 지형류, 모델).
- **입력·전제**: 시·공간 정렬·보간, 동일 좌표계·단위.
- **해석 기준**: 값이 작을수록 좋음. 평균 관측 속력 대비 정규화(VRMSE/관측 평균속력)하면 지역 간 비교 용이. centered 형태(벡터 bias 제거)도 함께 보고.
- **한계·주의**: 큰 유속 지역이 통계를 지배 → 정규화 또는 영역별 분리. 방향만 틀린 경우와 크기만 틀린 경우를 구분하지 못함(타원·위상각 병행).
- **출처**: 표준 검증 관행; 정의는 Emery & Thomson 및 연안 모델 스킬 문헌([Liu et al. 2009, Columbia 연안모델 평가, OSU PDF](http://bragg.ceoas.oregonstate.edu/Papers2/Liu2009.pdf)).

---

### 유향(방향) 검증 — 각도 오차·원형통계 (Direction error / circular statistics)
- **무엇을 측정/검증하나**: 유향만 따로 본 모델–관측 방향 일치도. 각도는 주기적(0/360° 연결)이라 일반 평균/RMSE를 그대로 쓰면 안 됨 → 원형통계(circular statistics) 사용.
- **정의·수식**:
  - 방향차: $\Delta\theta=\operatorname{atan2}(\sin(\theta_m-\theta_o),\cos(\theta_m-\theta_o))$ (−180~180°로 환산).
  - 각 RMSE: $\sqrt{\frac{1}{N}\sum \Delta\theta_i^2}$.
  - 평균 결과 길이 $R=\frac{1}{N}\big|\sum e^{i\theta_i}\big|$ (집중도; 1이면 방향 일정), 원형분산 $1-R$.
  - 단위벡터 방향 평균 $\bar\theta=\operatorname{atan2}(\overline{\sin\theta},\overline{\cos\theta})$.
- **적용 도메인/자료형**: 시계열·격자. 흐름 방향이 핵심인 항법·표류 예측 검증.
- **입력·전제**: 저유속 구간 처리(속력≈0이면 방향 불안정 → 속력 가중 또는 임계 제외). 동일 방위 기준(진북 기준 등).
- **해석 기준**: 각 RMSE가 작고 $R$이 1에 가까우면 방향 일치 양호. 체계적 편차(평균 방향차≠0)는 좌표 회전·강제력 방향 오차 시사.
- **한계·주의**: 약한 흐름에서 방향 RMSE가 과대평가됨 → 속력 가중(또는 벡터 RMSE) 권장. 0/360 처리 누락이 흔한 실수.
- **출처**: Mardia & Jupp, *Directional Statistics*; Jolliffe & Stephenson, *Forecast Verification* (풍향·유향 검증 절).

---

### 주축·변동타원 (Principal axis / variance ellipse)
- **무엇을 측정/검증하나**: 유속 변동의 **주축(major/minor principal axis)** 방향과 이방성(타원의 장단축비)을 진단. 연안류·조류처럼 한 방향으로 길쭉한 변동(해안선 평행)이 모델·관측에서 같은 방향·같은 이방성으로 재현되는지 검증. 조류타원(조석 주파수별)과 달리 **전체 변동의 통계적 주축**을 본다.
- **정의·수식**: 편차 벡터 $(u',v')$의 2×2 공분산행렬
  $$\Sigma=\begin{pmatrix}\overline{u'^2} & \overline{u'v'}\\ \overline{u'v'} & \overline{v'^2}\end{pmatrix}$$
  의 고유값 $\lambda_1\ge\lambda_2$가 장축²·단축² 분산, 고유벡터가 주축 방향. 장축 방위각 $\theta_p=\tfrac12\operatorname{atan2}(2\overline{u'v'},\ \overline{u'^2}-\overline{v'^2})$. 이방성 지수 $=1-\lambda_2/\lambda_1$(또는 $\sqrt{\lambda_2/\lambda_1}$).
- **적용 도메인/자료형**: 벡터 시계열(ADCP/유속계/표류부이/모델 격자점), 격자 전역(변동타원 지도). 표면·각 층.
- **입력·전제**: 평균 제거(편차). 충분한 표본(공분산 안정). 동일 좌표계·기간으로 모델·관측 산출.
- **해석 기준**: 주축 방위각 차(°), 장축/단축 분산비, 총분산(TKE)을 모델·관측 비교. 주축 방향이 일치하고 이방성·분산 크기가 비슷하면 변동 구조 재현 양호. 연안에서 주축이 해안선과 평행한지 확인.
- **한계·주의**: 다중 시간규모(조석+계절+중규모)가 섞이면 주축이 모호 → 대역통과 후 산출 권장. 거의 등방(원형)이면 주축 방향 불안정(작은 표본 변동에 민감). 조류타원과 혼동 금지(이쪽은 비주기 포함 총변동).
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (주축/variance ellipse, PCA 적용); 연안류 적용 사례 [Ocean Sci. 20, 1229, 2024](https://os.copernicus.org/articles/20/1229/2024/).

---

### 속력 분포 비교 — Q-Q·PDF·CDF (Speed distribution comparison)
- **무엇을 측정/검증하나**: 유속(또는 성분) 값의 **분포 전체**가 모델·관측에서 일치하는지. 평균·RMSE가 비슷해도 분포의 꼬리(강풍·강류 이벤트, 극값)나 형태가 다를 수 있음 → 분위수-분위수(Q-Q) 플롯, 확률밀도(PDF)·누적분포(CDF) 비교, 분포거리(KS, Wasserstein)로 정량화.
- **정의·수식**:
  - Q-Q: 동일 누적확률 $p$에서 모델 분위수 $Q_m(p)$ vs 관측 분위수 $Q_o(p)$ 산점도(대각선이면 동일 분포).
  - Kolmogorov–Smirnov 거리 $D=\max_x |F_m(x)-F_o(x)|$ (두 CDF의 최대 수직거리).
  - Perkins 스킬 점수(분포 겹침) $S_{score}=\sum_k \min(f_{m,k},\,f_{o,k})$ (히스토그램 빈 $k$; 1이면 완전 일치).
  - 백분위 오차: P90/P95/P99 속력의 모델–관측 차.
- **적용 도메인/자료형**: 시계열·격자(전 격자점 풀링 또는 지점별). 표면류·정점류·위성 지형류 속력 모두.
- **입력·전제**: 동일 기간·동일 샘플링. 속력은 비음(0 이상)·우편향 분포임을 고려. 격자 비교 시 동일 해상도(다운샘플)로 맞춤.
- **해석 기준**: Q-Q가 대각선에 가깝고 KS 거리 작으며 Perkins 점수가 1에 가까우면 분포 일치 양호. 상위 백분위(P95/P99) 과소는 강류 이벤트 재현 부족(해상도·강제력), 과대는 노이즈 시사.
- **한계·주의**: 분포 비교는 **시간 위상(타이밍)을 보지 않음** → 상관·RMSE와 병행. 표본 적으면 꼬리 추정 불안정. KS는 분포 중앙에 민감(꼬리엔 둔감) → Anderson–Darling/백분위 병행.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (Q-Q·분포검정); Perkins et al. (2007), *J. Climate*, 20, 4356–4376 (분포 겹침 스킬 점수); KS 검정은 표준 통계(확인된 표준 기법).

---

### Progressive Vector Diagram (PVD) (의사 라그랑지안 변위도)
- **무엇을 측정/검증하나**: 한 정점의 시계열 유속을 시간 적분해 "가상의 입자가 그 점의 흐름을 따라 이동했을 변위"를 그린 궤적. 모델·관측의 누적 수송 방향·거리, 순(net) 이동을 시각·정량 비교.
- **정의·수식**: $X(t)=\sum_{k\le t} u_k\,\Delta t,\quad Y(t)=\sum_{k\le t} v_k\,\Delta t$. 곡선 $(X,Y)$가 PVD. 순변위 길이·방향, 누적 이동거리 비교.
- **적용 도메인/자료형**: 단일 정점 시계열(ADCP/유속계/모델 격자점). Eulerian 자료로부터 의사 라그랑지안 표현.
- **입력·전제**: 균일 시간간격, 결측 보간. 적분 시작점·기간 일치(모델·관측 동일).
- **해석 기준**: 모델·관측 PVD의 순변위 방향·길이, 곡선 모양(반전류·관성진동 등)이 유사하면 양호. 누적 변위 차이로 장기 수송 편향 진단.
- **한계·주의**: **공간 균질 흐름 가정**(실제 입자는 다른 곳을 지나며 다른 흐름을 만남) → 장기간일수록 실제 궤적과 괴리. 진짜 입자추적과 혼동 금지. 적분이 오차를 누적(드리프트).
- **출처**: Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (PVD 표준 정의·주의사항).

---

### 조화분석·조류타원 (Harmonic analysis & tidal current ellipse)
- **무엇을 측정/검증하나**: 조석 주파수(M2, S2, K1, O1 등)별 조류의 타원 파라미터 — 장축(semi-major, 최대 조류속), 단축(semi-minor, 최소속·회전방향), 경사각(inclination, 장축이 동에서 반시계로 이루는 각), 위상(Greenwich phase). 모델 조석류의 진폭·위상·회전을 관측과 검증.
- **정의·수식**: u, v를 조화분석해 각 성분의 진폭·위상 산출 후, 회전성분으로 분해:
  - 시계방향(CW) 진폭 $W_-$, 반시계(CCW) 진폭 $W_+$로부터
  - 장축 $a=W_+ + W_-$, 단축 $b=W_+ - W_-$ (부호: +면 CCW 회전, −면 CW).
  - 경사각 $\theta=\frac{1}{2}(\phi_+ + \phi_-)$, 위상 $g=\frac{1}{2}(\phi_- - \phi_+)$.
- **적용 도메인/자료형**: 조류 시계열(ADCP/유속계), 모델 격자점 시계열. 격자 전역에 적용해 조류타원 지도 작성.
- **입력·전제**: 충분한 기록 길이(주요 분조 분리: M2/S2 분리에 ≥ ~15일, 1년이면 다수 분조). 균일 샘플링, Rayleigh 분리 기준 충족. t_tide/UTide 등 도구.
- **해석 기준**: 장축·단축·경사·위상의 모델–관측 차로 검증. 단축 부호(회전방향) 일치 중요. 분조별 진폭 RMSE, 위상차(°), 벡터차(in-phase/quadrature) 보고. 회전방향이 반대면 명백한 모델 결함.
- **한계·주의**: 비조석 변동(폭풍·계절류)이 섞이면 추정 오염 → 충분한 길이·신뢰구간. 천해 비선형분조(M4 등) 누락 주의. 위상 기준시(Greenwich vs local) 일치.
- **출처**: Pawlowicz, Beardsley & Lentz (2002), "Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE," *Computers & Geosciences*, 28, 929–937, [doi:10.1016/S0098-3004(02)00013-4](https://doi.org/10.1016/S0098-3004(02)00013-4); Foreman (1978), *Manual for tidal currents analysis and prediction*; 검증 사례 [Polton, *Cont. Shelf Res.*](https://www.sciencedirect.com/science/article/abs/pii/S0278434317303710); 타원 파라미터 정의 [BAWiki](https://wiki.baw.de/en/index.php/Harmonic_Analysis_of_Current_Velocity).

---

### 회전스펙트럼 — Gonella (1972) (Rotary spectra)
- **무엇을 측정/검증하나**: 벡터(복소) 시계열을 시계(CW, 음주파수)·반시계(CCW, 양주파수) 회전성분의 에너지 스펙트럼으로 분해. 관성진동(NH에서 CW)·조류·저주파류의 회전 특성을 주파수별로 검증. 회전계수로 흐름의 편극(타원성) 진단.
- **정의·수식**: $w(t)=u+iv$의 푸리에 변환을 양/음 주파수로 분해해 $S_+(\sigma)$(CCW), $S_-(\sigma)$(CW). 회전계수 $r(\sigma)=\dfrac{S_+ - S_-}{S_+ + S_-}$ (−1: 순수 CW, 0: 직선, +1: 순수 CCW). 안정성(stability)·방향각도 산출 가능.
- **적용 도메인/자료형**: 벡터 시계열(ADCP/유속계/표류부이/모델 격자점).
- **입력·전제**: 균일 샘플링, 충분 길이·세그먼트 평균(자유도). 평균 제거·디트렌드, 윈도잉.
- **해석 기준**: 모델·관측의 CW/CCW 스펙트럼 피크 위치·세기, 관성주파수·조석주파수에서의 회전계수 일치 여부로 검증. 관성대역 CW 우세 재현 여부가 상층 흐름 진단의 핵심.
- **한계·주의**: 정상성·등간격 요구. 짧은 기록은 저주파 신뢰도 낮음. 자유도 확보 위한 스무딩 필요(분해능 trade-off). 적도 부근 관성효과 약화 해석 주의.
- **출처**: Gonella, J. (1972), "A rotary-component method for analysing meteorological and oceanographic vector time series," *Deep-Sea Research*, 19, 833–846 ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0011747172900022)); Emery & Thomson 교과서; [Cambridge, *Time Series Data Analysis in Oceanography*, Ch.22 회전스펙트럼](https://www.cambridge.org/core/books/abs/time-series-data-analysis-in-oceanography/rotary-spectrum-analysis/AAD234828D4C234CA3BA848F70525743).

---

### 수송량 — 부피/질량 수송 (Volume / mass transport)
- **무엇을 측정/검증하나**: 해류 단면을 통과하는 부피수송(Sv, 1 Sv=10⁶ m³/s) 또는 질량수송. 해협·경계류·자오면 순환의 통합 진단. 모델 수송을 관측 추정(케이블·계류선·역학계산)·재분석과 비교.
- **정의·수식**: 단면 $A$에 수직한 속도 $v_\perp$에 대해
  $$T=\iint_A v_\perp\, dA = \int\!\!\int v_\perp\, dz\, dl$$
  (수심 z, 단면 따라 l). 깊이적분 운반(barotropic)·층별 운반 분해 가능. 유선함수 $\psi$로부터 두 지점 차 $\Delta\psi$가 그 사이 수송.
- **적용 도메인/자료형**: 격자장(모델/재분석) 단면 적분, 계류선 어레이 관측. 자오면(MOC)·해협 수송.
- **입력·전제**: 단면 정의(시작/끝, 깊이), 격자 셀 면적·법선속도 정확 산출. 동일 단면·기간으로 모델·관측 정렬. 좌표 직교화.
- **해석 기준**: 수송 평균·표준편차·계절/경년 변동을 관측과 비교. 절대값과 변동성 모두 중요. 경계류는 Sverdrup 균형 대비 초과(열염·재순환) 정상.
- **한계·주의**: 단면 정의·심도 적분 방식에 민감. 격자 해상도가 경계류 폭을 못 풀면 수송 과소. 부분셀·지형 표현 차로 모델 간 비교 시 단면 일치 필요.
- **출처**: Wunsch (2011), "The decadal mean ocean circulation and Sverdrup balance," *J. Mar. Res.* ([ResearchGate](https://www.researchgate.net/publication/228722138_The_decadal_mean_ocean_circulation_and_Sverdrup_balance)); Volume transport 개관([ScienceDirect Topics](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/volume-transport)); 일반 물리해양 교과서(Talley et al., *Descriptive Physical Oceanography*).

---

### 운동에너지 진단 — 평균/와류 (Mean & Eddy Kinetic Energy, MKE/EKE)
- **무엇을 측정/검증하나**: 흐름 에너지를 평균류(MKE)와 변동(와류) 성분(EKE)으로 분해. EKE는 중규모 와류 활동의 세기 지표 → 모델의 와류 변동성·중규모 활동도 검증의 핵심.
- **정의·수식**: 레이놀즈 분해 $u=\bar u + u',\ v=\bar v + v'$:
  - MKE $=\tfrac{1}{2}(\bar u^2+\bar v^2)$
  - EKE $=\tfrac{1}{2}(\overline{u'^2}+\overline{v'^2})$
  - 위성 지형류에서는 SLA 미분으로 지형류 편차 $u',v'$ 산출 후 EKE 계산.
- **적용 도메인/자료형**: 격자장(모델/재분석), 위성 고도계(표면 지형류 EKE), 표류부이(라그랑지안 EKE). 표면·각 층.
- **입력·전제**: 평균(시간평균/이동평균) 정의 일치. 필터링 대역(중규모 vs 계절) 일치. 위성과 비교 시 동일 필터·동일 기간.
- **해석 기준**: EKE 공간분포·크기를 AVISO/위성 지형류와 비교(크기 동등성·고EKE 영역(경계류·전선) 재현). 모델 EKE 과소는 와류 비허용/저해상도, 과대는 수치 노이즈 시사.
- **한계·주의**: "평균" 정의·필터 대역에 강하게 의존(비교 시 동일 정의 필수). 위성 EKE는 시공간 해상도 한계로 소규모 와류 누락 → 모델을 위성 해상도로 다운샘플 후 비교. 라그랑지안 EKE는 표본분포 편향.
- **출처**: 위성·재분석 EKE 검증 사례 [Frontiers Mar. Sci. 2022](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.1032699/full); [JGR Oceans 2021, Southern Ocean EKE trends](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JC016973); 전심도 EKE [GRL 2023](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL103114).

---

### 표면류 성분 분해·검증 — 지형류+Ekman(+Stokes) (Surface current decomposition: geostrophic + Ekman + Stokes)
- **무엇을 측정/검증하나**: 관측·재분석 표면류(드리프터 15 m, OSCAR, GlobCurrent, GLORYS)는 흔히 **지형류(geostrophic) + 풍성류(Ekman) + 파랑성 Stokes drift**의 합으로 본다. 우리 모델의 총 표면류를 같은 성분 구성의 권위자료와 비교하거나, 성분별로 분해해 어느 성분이 편차의 원인인지 진단.
- **정의·수식**:
  - 지형류: $u_g=-\frac{g}{f}\partial_y\eta,\ v_g=\frac{g}{f}\partial_x\eta$ (해면고도 $\eta$, 코리올리 $f$) — 위성 고도계 SLA/ADT에서 산출.
  - Ekman: 표층 응력 방향에서 우측(NH) 편향, 경험적·이론적 모델(Rio/GlobCurrent 회귀계수)로 풍속·응력에서 추정.
  - 총 표면류 $\mathbf{u}_{tot}=\mathbf{u}_g+\mathbf{u}_{ek}(+\mathbf{u}_{stokes})$. 비교 시 성분별 RMSE·복소상관.
- **적용 도메인/자료형**: 격자 표면류(우리 모델 표층 vs OSCAR/GlobCurrent/GLORYS), 드리프터(15 m drogued), 위성 지형류. 위성 지형류는 지형류 성분만이므로 비교 시 모델도 지형류 성분 추출.
- **입력·전제**: 비교 대상의 성분 정의 일치(예: 위성 지형류는 Ekman·Stokes 미포함, 15 m 드리프터는 Ekman 포함·Stokes 부분포함). 심도 정합(표층 vs 15 m). 적도(f→0) 부근 지형류 근사 붕괴 처리.
- **해석 기준**: 총 표면류 성분 RMSE·상관과 더불어, 지형류만 비교(위성 대비)·풍성류 잔차 비교로 오차 원인 분리. 모델이 드리프터 대비 약하면 Ekman/Stokes 미반영 의심, 위성 지형류와는 잘 맞는데 드리프터와 안 맞으면 풍성·파랑 성분 문제.
- **한계·주의**: Ekman·Stokes 분해는 경험모델 의존(불확실성). 적도·연안에서 지형류 가정 약함. drogued/undrogued 드리프터는 Stokes·풍압류 노출이 다름 → 비교 시 명시.
- **출처**: Rio et al. (2014), "Beyond GOCE for the ocean circulation estimate... geostrophic and Ekman currents," *Geophys. Res. Lett.* ([Wiley](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014GL061773)); Sudre, Maes & Garçon (2013), "On the global estimates of geostrophic and Ekman surface currents," *Limnol. Oceanogr. Fluids Environ.* ([Wiley](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1215/21573689-2071927)); OSCAR/GlobCurrent 제품 문서.

---

### Okubo-Weiss 파라미터 (Okubo–Weiss parameter, W)
- **무엇을 측정/검증하나**: 흐름장 각 점에서 변형(strain) 대 회전(vorticity)의 상대적 우세를 진단. W<0(회전 우세)은 와류 코어 후보, W>0(변형 우세)은 변형/필라멘트 영역. 모델 흐름장의 중규모 구조·와류 분포를 진단·비교.
- **정의·수식**: $W = s_n^2 + s_s^2 - \omega^2$, 여기서 정상변형 $s_n=\partial u/\partial x-\partial v/\partial y$, 전단변형 $s_s=\partial v/\partial x+\partial u/\partial y$, 상대와도 $\omega=\partial v/\partial x-\partial u/\partial y$. 임계값 $W_0$(보통 $0.2\,\sigma_W$ 또는 전역 $-2\times10^{-12}\,\text{s}^{-2}$)로 와류영역 $W<-W_0$ 분류.
- **적용 도메인/자료형**: 2D 격자 흐름장(모델/재분석/위성 지형류). 공간 미분 필요 → 격자 자료.
- **입력·전제**: 매끄러운 u/v 격자(미분 산출). 노이즈 큰 자료는 스무딩 선행. 임계값 선택(지역·해상도 의존) 명시.
- **해석 기준**: W<−W₀ 폐영역을 와류 후보로. 모델·관측의 와류 개수·위치·크기 분포 비교. 와류 센서스의 1차 검출기로 사용.
- **한계·주의**: 임계값 선택에 민감(검출 와류 수 크게 변동). 변형장 잡음에 약함(허위 검출). 단독으론 와류 경계·극성(저기압/고기압) 미구분 → 와도부호·기하학 기준 병행. 2D·준지형 가정.
- **출처**: Okubo (1970), "Horizontal dispersion of floatable particles...," *Deep-Sea Res.*, 17, 445–454; Weiss (1991), "The dynamics of enstrophy transfer in two-dimensional hydrodynamics," *Physica D*, 48, 273–294; 적용 리뷰 [Ocean Sci. 7, 317–334, 2011](https://os.copernicus.org/articles/7/317/2011/os-7-317-2011.pdf); [Wikipedia: Okubo–Weiss parameter](https://en.wikipedia.org/wiki/Okubo%E2%80%93Weiss_parameter).

---

### 와류 센서스·추적 (Eddy census & tracking)
- **무엇을 측정/검증하나**: 중규모 와류를 자동 검출(SSH/SLA 폐곡선, 속도장 기하학, OW 등)·특성화(반경 radius, 진폭 amplitude, 회전속도, 극성)·시간추적(궤적·수명·이동속도)하여 통계(개수·밀도·생성률·전파속도)를 산출. 모델 와류 활동을 위성 와류 아틀라스와 통계적으로 검증.
- **정의·수식(개념)**: 검출 — (a) Chelton 방식: SLA 극값 주위 최외곽 폐곡선; (b) Nencioli 기하학: 속도 최소 중심·주변 회전; (c) OW 임계. 특성 — 진폭(SLA 극값−경계값), 유효반경(동일면적 원반경), 회전속도(경계 최대 평균지형류). 추적 — 시간 프레임 간 중첩/최근접 매칭, 분열·병합 처리.
- **적용 도메인/자료형**: 위성 고도계 SLA 격자, 모델 SSH/속도 격자. 표면 중규모.
- **입력·전제**: 일·주 단위 격자장, 충분 해상도(와류 반경 ≥ ~2 격자). 동일 검출 알고리즘·파라미터로 모델·관측 일관 적용(공정 비교 핵심).
- **해석 기준**: 와류 개수·반경·진폭·수명·서향전파속도 분포를 위성(META/Chelton 아틀라스)과 비교. 분포 일치(히스토그램·KS검정)면 양호. 모델 과소검출은 해상도·점성 시사.
- **한계·주의**: 알고리즘·임계값마다 결과 상이(반드시 동일 설정으로 양측 처리). 진폭 임계(예 1 cm)가 작은 와류 특성 과소·계단효과 유발. 위성 해상도 한계로 소형·근접 와류 누락 → 모델을 동일 해상도로 처리 후 비교.
- **출처**: Chelton, Schlax & Samelson (2011), "Global observations of nonlinear mesoscale eddies," *Prog. Oceanogr.*, 91, 167–216; Nencioli et al. (2010), "A vector geometry–based eddy detection algorithm...," *J. Atmos. Oceanic Technol.*; Faghmous et al. (2015), "A daily global mesoscale ocean eddy dataset from satellite altimetry," *Scientific Data*, 2:150028; META3.1 아틀라스 [Pegliasco et al., ESSD 14, 1087, 2022](https://essd.copernicus.org/articles/14/1087/2022/).

---

### 유한시간 Lyapunov 지수 / LCS (FTLE / FSLE, Lagrangian Coherent Structures)
- **무엇을 측정/검증하나**: 흐름장에서 인접 입자가 얼마나 빨리 분리되는지(스트레칭 율)를 측정해, 수송장벽(transport barrier)·코히어런트 구조(LCS)를 추출. FTLE 능선(ridge)이 LCS. 모델·관측(또는 재분석) 흐름장의 라그랑지안 수송 구조 일치도를 검증.
- **정의·수식**: 시간 $[t_0,t_0+T]$ 동안 유동지도 $\phi$의 변형구배 $\nabla\phi$로 Cauchy-Green 텐서 $C=(\nabla\phi)^{\!\top}\nabla\phi$. 최대 고유값 $\lambda_{max}$로
  $$\text{FTLE}=\frac{1}{|T|}\ln\sqrt{\lambda_{max}(C)}.$$
  FSLE는 고정 분리비 도달 시간 기반. FTLE 능선이 흡인/반발 LCS.
- **적용 도메인/자료형**: 시변 2D(또는 3D) 격자 속도장(모델/재분석/HF radar/위성 지형류). 입자 적분 필요.
- **입력·전제**: 시공간 연속 속도장(보간), 입자 적분기(RK4 등), 적분기간 T·격자 간격 선택. 결측·경계 처리.
- **해석 기준**: 모델·관측 FTLE장의 능선(수송장벽) 위치·강도 일치로 라그랑지안 구조 검증. 정성 패턴 일치 + 능선 거리/구조유사도 정량화. 오염·표류 확산 장벽 진단에 활용.
- **한계·주의**: 적분기간 T·해상도에 결과 민감(짧으면 구조 불명, 길면 노이즈·외삽). 속도장 불확실성이 FTLE에 증폭(앙상블로 불확실성 정량 권장). 능선=LCS는 근사(엄밀 LCS는 추가 조건).
- **출처**: Haller (2015), "Lagrangian Coherent Structures," *Annu. Rev. Fluid Mech.*, 47, 137–162; Shadden, Lekien & Marsden (2005), "Definition and properties of LCS from FTLE...," *Physica D*, 212, 271–304; 연안 적용 리뷰 [Frontiers Mar. Sci. 2024](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1345260/full); 불확실성 [Ocean Sci. 21, 401, 2025](https://os.copernicus.org/articles/21/401/2025/).

---

### 라그랑지안 입자추적·표류부이 대조 (Lagrangian particle tracking & drifter comparison)
- **무엇을 측정/검증하나**: 모델 흐름장으로 가상 입자를 적분한 궤적을, 실제 표류부이(드리프터) 궤적과 비교. 흐름장의 통합적·시간누적적 정확도를 분리거리(separation distance)·궤적 유사도로 검증.
- **정의·수식**:
  - 입자 적분: $\frac{d\mathbf{x}}{dt}=\mathbf{u}(\mathbf{x},t)$.
  - 분리거리 $d(t)=|\mathbf{x}_{model}(t)-\mathbf{x}_{drifter}(t)|$, 누적 평균.
  - Liu–Weisberg 정규화 누적 라그랑지안 분리 스킬: 누적 분리 $\sum d(t)$를 관측 누적이동거리 $\sum l_{obs}(t)$로 정규화한 지수 $s=1-\frac{\langle\sum d\rangle}{\langle\sum l_{obs}\rangle}$ (1에 가까울수록 우수; 음수면 분리가 경로길이를 초과).
  - 라그랑지안 분리율(쌍 입자 분리)로 확산 진단.
- **적용 도메인/자료형**: 시변 표면(또는 층) 속도장(모델/HF radar/재분석) + 드리프터 GPS 궤적.
- **입력·전제**: 동일 출발점·출발시각에서 합성 입자, 동일 기간. 적분기·시간스텝, 풍압류(windage)·확산 항 처리 명시.
- **해석 기준**: Liu–Weisberg 스킬 $s$가 1에 가까울수록 우수(임계 기준 위 면적으로 종합); 일정 기간(예 1~2일)까지 분리거리가 작으면 양호. 표면류는 단기, 심층은 더 장기 평가.
- **한계·주의**: 카오스적 분기로 장기 궤적은 본질적 발산(단기 평가 중심). 드리프터는 풍압·파랑 영향(undrogued면 더) → 비교 시 windage 보정. 표본 적으면 통계 불안정. 스킬 정의(누적식 vs 단순 분리)·정규화 기준 명시.
- **출처**: Liu, Y., & Weisberg, R. H. (2011), "Evaluation of trajectory modeling in different dynamic regions using normalized cumulative Lagrangian separation," *J. Geophys. Res. Oceans*, 116, C09013, [doi:10.1029/2010JC006837](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JC006837); 스킬 점수 민감도 [Frontiers Mar. Sci. 2021](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2021.630388/full); HF radar Lagrangian 검증 [MDPI RS 2025](https://www.mdpi.com/2072-4292/17/7/1243).

---

### HF radar / ADCP 대조 검증 프로토콜 (HF radar & ADCP cross-validation)
- **무엇을 측정/검증하나**: 표면류(HF radar, 모델 표층)와 정점 유속(ADCP)의 교차검증 절차. 레이디얼/벡터 성분별 RMSE·상관·복소상관, 회귀(기울기/절편), 방향 일치를 일관된 프로토콜로 산출.
- **정의·수식**: (a) 레이디얼 vs ADCP 사영 비교, (b) 총 벡터 u/v 성분별 RMSE·상관, (c) 복소상관($|\rho|$·위상)으로 방향 편차, (d) 주축(principal axis) 정렬·회귀 기울기. 깊이정합(HF radar 유효심 vs ADCP 최상층 빈) 고려.
- **적용 도메인/자료형**: HF radar 격자 표면류, 모델 표층, ADCP/유속계 정점 시계열, 드리프터.
- **입력·전제**: 시간 동기화(시간평균창 일치), HF radar 격자셀↔ADCP 위치 매칭, 유효심 차 보정. GDOP(기하 정밀도 저하) 영역 제외.
- **해석 기준**: 관행 범위 — 성분 RMSE ~5~20 cm/s, 상관 ~0.4~0.9(연안). 레이디얼 RMSE 0.11~0.18 m/s, 벡터 성분 상관 0.56~0.93 등이 보고됨. 회귀 기울기≈1·절편≈0이면 무편향.
- **한계·주의**: HF radar는 상층 ~0.5~2 m 평균류(ADCP 최상층과 심도 불일치)·표면 스토크스/풍압 포함 → 직접 비교 시 편차. GDOP·기선 기하로 성분별 정확도 비대칭. 시간·공간 평균 대표성 차.
- **출처**: 검증 종합 [MDPI RS 17(7):1243, 2025](https://www.mdpi.com/2072-4292/17/7/1243); West Florida Shelf ADCP-HF radar([ResearchGate](https://www.researchgate.net/publication/4011668_A_comparison_of_near-surface_current_measurements_by_ADCP_and_HF-Radar_on_the_West_Florida_Shelf)); New York Bight 조류 비교([ResearchGate](https://www.researchgate.net/publication/223078484_Comparison_of_observed_HF_radar_ADCP_and_model_barotropic_tidal_currents_in_the_New_York_Bight_and_Block_Island_Sound)).

---

### Murphy 스킬 스코어·MSE 기반 스킬 (Murphy skill score / MSE-based skill)
- **무엇을 측정/검증하나**: 모델 오차(MSE)를 **기준자료(reference)** 대비 정규화해 "기준 대비 얼마나 나은가"를 하나의 스킬 점수로. 기준은 보통 관측 기후평균(climatology)·지속성(persistence)·기존 모델. 흐름 검증에서 우리 모델이 GLORYS/재분석·기후평균보다 나은지 객관 정량화.
- **정의·수식**:
  - 스킬 스코어 $SS = 1-\dfrac{\text{MSE}_{model}}{\text{MSE}_{ref}}$ (1: 완전, 0: 기준과 동급, <0: 기준보다 나쁨).
  - Murphy(1988) MSE 분해: $SS = R^2 - \left[R-\frac{\sigma_m}{\sigma_o}\right]^2 - \left[\frac{\bar m-\bar o}{\sigma_o}\right]^2$ (상관항 − 조건부편향 − 무조건편향). 기준=관측평균일 때.
  - Willmott 일치도 $d=1-\frac{\sum(m_i-o_i)^2}{\sum(|m_i-\bar o|+|o_i-\bar o|)^2}$ (0~1).
- **적용 도메인/자료형**: 시계열·격자에서 산출한 MSE의 정규화. u/v 성분·속력별, 지점·영역별. 격자장은 벡터 MSE로 확장 가능.
- **입력·전제**: 명확한 기준자료 정의(기후평균·지속성·타 모델)와 동일 시·공간 표본. 관측 분산 $\sigma_o$로 정규화.
- **해석 기준**: $SS>0$이면 기준보다 우수, 1에 가까울수록 좋음. 분해항으로 오차 원인 진단(상관 낮음 vs 진폭/평균 편향). $d\to1$이 좋음.
- **한계·주의**: 기준 선택에 따라 점수가 크게 달라짐(반드시 기준 명시). 단일 점수는 시공간 구조를 숨김(Taylor·패턴상관 병행). 벡터에 스칼라 스킬을 쓰면 방향성 손실.
- **출처**: Murphy, A. H. (1988), "Skill scores based on the mean square error and their relationships to the correlation coefficient," *Mon. Weather Rev.*, 116, 2417–2424 ([AMS](https://journals.ametsoc.org/view/journals/mwre/116/12/1520-0493_1988_116_2417_ssbotm_2_0_co_2.xml)); Willmott (1981), *Phys. Geogr.*, 2, 184–194; 해양 종합 Stow et al. (2009), *J. Mar. Syst.*, 76, 4–15.

---

### Taylor 다이어그램·표준화 통계 요약 (Taylor diagram & normalized skill)
- **무엇을 측정/검증하나**: 상관계수, (표준화)표준편차, centered RMSE를 하나의 극좌표 평면에 동시 표시해 여러 지점·변수·모델의 흐름 검증 결과를 한눈에 요약. Willmott 일치도(d) 등 종합 스킬 점수와 병행.
- **정의·수식**: 관계식 $E'^2 = \sigma_m^2 + \sigma_o^2 - 2\sigma_m\sigma_o R$ (코사인 법칙)을 이용. 반경=표준편차(σ_o로 정규화), 방위각=arccos(R), 점–기준점 거리=centered RMSE.
- **적용 도메인/자료형**: 시계열·격자에서 산출한 통계의 요약 표시(u/v 성분·속력별). 다지점·다모델 비교.
- **입력·전제**: 각 지점/변수에서 R, σ, RMSE 산출 완료. 정규화 기준(관측 σ) 명시.
- **해석 기준**: 기준점(관측)에 가까울수록(R→1, σ비→1, centered RMSE→0) 우수. 여러 모델 중 기준점 최근접이 최선.
- **한계·주의**: centered RMSE만 표현(편향 bias는 별도 표시 필요 — bias vs RMSE 플롯 병행). 벡터의 방향성은 성분별로 분리해야 함(스칼라 요약 한계). 상관이 음수면 다이어그램 표현 곤란.
- **출처**: Taylor, K. E. (2001), "Summarizing multiple aspects of model performance in a single diagram," *J. Geophys. Res.*, 106, 7183–7192; 해양 적용·요약도 [Jolliff et al. 2009, *J. Mar. Syst.*](https://www.sciencedirect.com/science/article/abs/pii/S0924796308001140).

---

### 흐름장 공간 패턴 비교 — EOF·패턴상관 (Spatial pattern comparison: EOF / pattern correlation)
- **무엇을 측정/검증하나**: 순환 구조의 공간 패턴(평균류장·변동 모드)이 모델·관측에서 일치하는지. 복소/벡터 EOF로 주요 변동 모드 추출, 패턴상관(spatial correlation)·RMS 차로 공간 일치도 정량화.
- **정의·수식**: 공간 패턴상관 $r_s=\dfrac{\sum_g (m_g-\bar m)(o_g-\bar o)}{\sqrt{\sum (m_g-\bar m)^2}\sqrt{\sum (o_g-\bar o)^2}}$ (격자 g). 벡터장은 복소 EOF(CEOF)로 회전·전파 모드 추출, 모드별 공간구조·시간계수·설명분산 비교.
- **적용 도메인/자료형**: 격자 흐름장(모델/재분석/위성 지형류/HF radar 격자). 공간장 비교 전반.
- **입력·전제**: 동일 격자(또는 공통 격자로 재격자화), 동일 기간. 평균 처리·표준화 방식 일치. 결측 일관 마스킹.
- **해석 기준**: 주요 모드의 공간 패턴상관 높고 설명분산·시간변동이 유사하면 순환 구조 재현 양호. 평균류장 패턴상관·벡터 RMS차로 정상상태 순환 검증.
- **한계·주의**: EOF 모드는 직교 제약으로 물리 모드와 불일치 가능(모드 혼합·부호 임의성). 격자·영역·기간에 민감. 패턴상관은 진폭 차를 못 봄(RMS차 병행). 벡터는 스칼라 EOF가 방향 정보 손실 → CEOF 권장.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (EOF/PCA, 패턴상관); Preisendorfer, *Principal Component Analysis in Meteorology and Oceanography*; 복소 EOF는 Horel (1984), *J. Climate Appl. Meteor.*, 23, 1660–1673.

---

## 출처 (References)

**표준 참고문헌 (교과서·표준지침)**
- Emery, W. J., & Thomson, R. E. *Data Analysis Methods in Physical Oceanography* (Elsevier). — 벡터 통계, 주축/변동타원, PVD, 회전스펙트럼, 조화분석 등 해양 시계열 분석 표준.
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences* (Academic Press). — RMSE/MAE/Bias, Q-Q/분포검정, EOF/PCA, 패턴상관.
- Jolliffe, I. T., & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley). — 방향·벡터 검증, 스킬 스코어.
- Talley, L. D., Pickard, G. L., Emery, W. J., & Swift, J. H. *Descriptive Physical Oceanography* (Elsevier). — 수송·순환 개념.
- Mardia, K. V., & Jupp, P. E. *Directional Statistics* (Wiley). — 원형통계(유향).
- Preisendorfer, R. W. *Principal Component Analysis in Meteorology and Oceanography*. — EOF/CEOF.

**논문·정의 출처 (확인된 실제 출처)**
- Kundu, P. K. (1976). Ekman veering observed near the ocean bottom. *J. Phys. Oceanogr.*, 6, 238–242. — 복소(벡터) 상관계수·회전(veering) 정량화. [AMS](https://journals.ametsoc.org/view/journals/phoc/6/2/1520-0485_1976_006_0238_evonto_2_0_co_2.xml)
- Crosby, D. S., Breaker, L. C., & Gemmill, W. H. (1993). A proposed definition for vector correlation in geophysics: Theory and Application. *J. Atmos. Oceanic Technol.*, 10, 355–367. — 회전·반사 불변 벡터 상관. [AMS](https://journals.ametsoc.org/view/journals/atot/10/3/1520-0426_1993_010_0355_apdfvc_2_0_co_2.xml)
- Gonella, J. (1972). A rotary-component method for analysing meteorological and oceanographic vector time series. *Deep-Sea Research*, 19, 833–846. — 회전스펙트럼. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0011747172900022)
- Pawlowicz, R., Beardsley, B., & Lentz, S. (2002). Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE. *Computers & Geosciences*, 28, 929–937. [doi:10.1016/S0098-3004(02)00013-4](https://doi.org/10.1016/S0098-3004(02)00013-4) — 조화분석/조류타원.
- Foreman, M. G. G. (1978). Manual for tidal currents analysis and prediction. — 조류 조화분석.
- Okubo, A. (1970). Horizontal dispersion of floatable particles... *Deep-Sea Research*, 17, 445–454. — Okubo-Weiss.
- Weiss, J. (1991). The dynamics of enstrophy transfer in two-dimensional hydrodynamics. *Physica D*, 48, 273–294. — Okubo-Weiss.
- Chelton, D. B., Schlax, M. G., & Samelson, R. M. (2011). Global observations of nonlinear mesoscale eddies. *Prog. Oceanogr.*, 91, 167–216. — 와류 센서스.
- Nencioli, F., et al. (2010). A vector geometry–based eddy detection algorithm. *J. Atmos. Oceanic Technol.* — 기하학 와류 검출.
- Faghmous, J. H., et al. (2015). A daily global mesoscale ocean eddy dataset from satellite altimetry. *Scientific Data*, 2:150028. — 와류 데이터셋. [Nature](https://www.nature.com/articles/sdata201528)
- Pegliasco, C., et al. (2022). META3.1exp global mesoscale eddy trajectory atlas. *Earth Syst. Sci. Data*, 14, 1087–1107. — [ESSD](https://essd.copernicus.org/articles/14/1087/2022/)
- Haller, G. (2015). Lagrangian Coherent Structures. *Annu. Rev. Fluid Mech.*, 47, 137–162. — LCS.
- Shadden, S. C., Lekien, F., & Marsden, J. E. (2005). Definition and properties of LCS from FTLE... *Physica D*, 212, 271–304. — FTLE/LCS.
- Liu, Y., & Weisberg, R. H. (2011). Evaluation of trajectory modeling in different dynamic regions using normalized cumulative Lagrangian separation. *J. Geophys. Res. Oceans*, 116, C09013. [doi:10.1029/2010JC006837](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JC006837) — 라그랑지안 스킬 스코어.
- Rio, M.-H., et al. (2014). Beyond GOCE for the ocean circulation estimate: geostrophic and Ekman currents. *Geophys. Res. Lett.* — 표면류 성분 분해. [Wiley](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014GL061773)
- Sudre, J., Maes, C., & Garçon, V. (2013). On the global estimates of geostrophic and Ekman surface currents. *Limnol. Oceanogr. Fluids Environ.* — 표면류 성분 분해. [Wiley](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1215/21573689-2071927)
- Murphy, A. H. (1988). Skill scores based on the mean square error and their relationships to the correlation coefficient. *Mon. Weather Rev.*, 116, 2417–2424. — MSE 기반 스킬·분해. [AMS](https://journals.ametsoc.org/view/journals/mwre/116/12/1520-0493_1988_116_2417_ssbotm_2_0_co_2.xml)
- Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single diagram. *J. Geophys. Res.*, 106, 7183–7192. — Taylor 다이어그램.
- Willmott, C. J. (1981). On the validation of models. *Physical Geography*, 2, 184–194. — 일치도 지수.
- Perkins, S. E., et al. (2007). Evaluation of the AR4 climate models' simulated daily... probability density functions. *J. Climate*, 20, 4356–4376. — 분포 겹침 스킬 점수.
- Stow, C. A., et al. (2009). Skill assessment for coupled biological/physical models of marine systems. *J. Mar. Syst.*, 76, 4–15. — 해양 모델 스킬 지표 종합. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0924796308001103)
- Horel, J. D. (1984). Complex principal component analysis... *J. Climate Appl. Meteor.*, 23, 1660–1673. — CEOF.

**웹 출처 (검증·적용 사례)**
- [Validating HF Radar Current Accuracy via Lagrangian Measurements (MDPI Remote Sens. 2025)](https://www.mdpi.com/2072-4292/17/7/1243)
- [Comparison of near-surface currents by ADCP and HF-Radar, West Florida Shelf (ResearchGate)](https://www.researchgate.net/publication/4011668_A_comparison_of_near-surface_current_measurements_by_ADCP_and_HF-Radar_on_the_West_Florida_Shelf)
- [HF radar/ADCP/model barotropic tidal currents, New York Bight (ResearchGate)](https://www.researchgate.net/publication/223078484_Comparison_of_observed_HF_radar_ADCP_and_model_barotropic_tidal_currents_in_the_New_York_Bight_and_Block_Island_Sound)
- [A note on evaluating model tidal currents against observations (Cont. Shelf Res.)](https://www.sciencedirect.com/science/article/abs/pii/S0278434317303710)
- [Harmonic Analysis of Current Velocity — tidal ellipse parameters (BAWiki)](https://wiki.baw.de/en/index.php/Harmonic_Analysis_of_Current_Velocity)
- [Okubo–Weiss parameter (Wikipedia)](https://en.wikipedia.org/wiki/Okubo%E2%80%93Weiss_parameter)
- [Mesoscale eddies & Okubo-Weiss application (Ocean Sci. 7, 317–334, 2011)](https://os.copernicus.org/articles/7/317/2011/os-7-317-2011.pdf)
- [FTLE/LCS for coastal ocean processes: a review (Frontiers Mar. Sci. 2024)](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1345260/full)
- [Uncertainties in FTLE in an ocean ensemble prediction model (Ocean Sci. 21, 401, 2025)](https://os.copernicus.org/articles/21/401/2025/)
- [Sensitivity of skill score metric to validate Lagrangian simulations (Frontiers Mar. Sci. 2021)](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2021.630388/full)
- [Seasonal variability of EKE in the north Indian Ocean (Frontiers Mar. Sci. 2022)](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.1032699/full)
- [Full-depth EKE from altimeter and Argo (GRL 2023)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023GL103114)
- [Rotary Spectrum Analysis — Time Series Data Analysis in Oceanography (Cambridge, Ch.22)](https://www.cambridge.org/core/books/abs/time-series-data-analysis-in-oceanography/rotary-spectrum-analysis/AAD234828D4C234CA3BA848F70525743)
- [Beyond GOCE: geostrophic and Ekman surface currents (Rio et al. 2014, GRL)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014GL061773)
- [On the global estimates of geostrophic and Ekman surface currents (Sudre et al. 2013)](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1215/21573689-2071927)
- [Tides and winds influencing nonstationary coastal currents, offshore Singapore (Ocean Sci. 2024)](https://os.copernicus.org/articles/20/1229/2024/)
- [Volume Transport overview (ScienceDirect Topics)](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/volume-transport)
- [The decadal mean ocean circulation and Sverdrup balance (ResearchGate)](https://www.researchgate.net/publication/228722138_The_decadal_mean_ocean_circulation_and_Sverdrup_balance)
- [Summary diagrams for coupled model skill assessment (Jolliff et al., J. Mar. Syst. 2009)](https://www.sciencedirect.com/science/article/abs/pii/S0924796308001140)
- [Evaluation of a coastal ocean circulation model, Columbia (Liu et al. 2009, OSU PDF)](http://bragg.ceoas.oregonstate.edu/Papers2/Liu2009.pdf)

> 주: 표준 참고문헌의 페이지·판차는 판본에 따라 다를 수 있다. DOI는 본문에 확실한 것만 표기했으며, 임의 생성하지 않았다. 일부 항목은 표준 관행을 종합한 것으로, 단일 1차 출처보다 위 교과서·리뷰를 근거로 한다.
>
> **이번 개정 시 수정한 인용(확인 결과):** ① **Kundu (1976)** 의 제목을 잘못 표기된 "Ensemble-averaged near-shore surface velocity"에서 실제 제목 **"Ekman veering observed near the ocean bottom"** (J. Phys. Oceanogr., 6, 238–242)으로 정정(권·페이지는 일치). ② Crosby et al. (1993), Gonella (1972), Pawlowicz et al. (2002), Faghmous et al. (2015), Liu & Weisberg (2011), Taylor (2001), Murphy (1988), Stow et al. (2009)은 제목·권·페이지를 1차 출처(AMS/ScienceDirect/Nature/Wiley)로 대조해 **확인 완료**. ③ 검증이 안 된 토론성 링크(ResearchGate 'vectorial timeseries' 질문 글)는 제거했다.
