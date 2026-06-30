# 03. 범주형·사건·극값 검증 (Categorical / Event / Extremes Verification)

수치모델 결과를 ERA5·GLORYS 등 권위 재분석자료, 관측소·위성자료와 비교할 때, 연속 오차지표(RMSE 등)만으로는 "임계값 초과 사건"이나 "드문 극값"의 예측 성능을 제대로 평가할 수 없다. 이 문서는 임계 초과를 예/아니오(yes/no)로 환산한 **2×2 분할표(contingency table)** 기반 범주형 지표, 확률예보 검증(Brier·ROC·신뢰도), 앙상블 신뢰성(순위 히스토그램·스프레드-스킬), 드문 사건(rare event) 전용 지표(EDI/SEDI), 격자장 공간·근접 검증(FSS·SAL·MODE), 그리고 극값 통계(GEV·POT·재현주기·해양폭염)를 망라한다. 각 지표는 측정 대상·수식·해석 기준·한계·출처를 갖춘 "메서드 카드" 형식으로 정리했다. 해양/기상 도메인(파고·수온·풍속·해수면 등)에서 경보 임계값(예: 유의파고 3 m 초과, 폭염, 호우, 해양폭염) 검증에 그대로 적용 가능하다. **NetCDF 격자자료**는 격자점별로 사건화해 분할표·EDI·FSS·SAL·MODE를 적용하고, **CSV/텍스트 시계열**은 시각별로 사건화해 같은 지표를 산출한다.

## 이 파일에 담은 방법들 (한 줄 목차)

- **분할표 기초**: 2×2 분할표(contingency table) 구성 및 표기
- **정확도/빈도**: 정확도(PC, fraction correct), 빈도편향(FBI, frequency bias)
- **탐지/오경보**: 탐지확률(POD/H, hit rate), 오경보비(FAR), 오탐지확률(POFD/F), 성공비(SR)
- **종합 사건지표**: 임계성공지수(CSI/TS, threat score)
- **공평 기술점수**: 공평임계점수(ETS/GSS), 하이드케 기술점수(HSS), 피어스/핸슨-카이퍼스 기술점수(PSS/TSS)
- **오즈 기반**: 오즈비(OR, odds ratio), 오즈비 기술점수(ORSS/Yule's Q)
- **드문 사건 전용**: 극단의존지수(EDI), 대칭극단의존지수(SEDI), 극단의존점수(EDS/SEDS)
- **확률예보 검증**: 브라이어 점수(BS), 브라이어 기술점수(BSS), 신뢰도 다이어그램(reliability diagram), 상대운영특성(ROC)/곡선하면적(AUC)
- **확률 다범주**: 순위확률점수(RPS), 연속순위확률점수(CRPS), 임계가중 CRPS(twCRPS)
- **앙상블 신뢰성**: 순위 히스토그램(rank/Talagrand histogram), 스프레드-스킬 관계(spread–skill)
- **다범주 결정론**: 다범주 HSS, 게리티 점수(Gerrity score), SEEPS
- **공간/근접 검증(격자 전용)**: 분율 기술점수(FSS, neighborhood), SAL(구조·진폭·위치), MODE(객체기반)
- **극값 통계**: 일반화극값분포(GEV)/블록최대값(block maxima), 임계초과(POT)/일반화파레토분포(GPD), 재현주기/재현수준(return period/level), 백분위수 극한지표(percentile-based ETCCDI), 해양폭염(MHW) 검출·검증

---

### 2×2 분할표 (Contingency Table / 2x2 분할표)

- **무엇을 측정/검증하나**: 임계값으로 이진화한 예보(yes/no)와 관측(yes/no)의 일치 구조. 거의 모든 범주형 지표의 기반.
- **정의·수식**: 예보×관측의 4칸으로 구성.

  | | 관측 Yes | 관측 No | 합 |
  |---|---|---|---|
  | **예보 Yes** | hits (a) | false alarms (b) | a+b |
  | **예보 No** | misses (c) | correct negatives (d) | c+d |
  | **합** | a+c | b+d | n=a+b+c+d |

  - a = 적중(hits), b = 오경보(false alarms), c = 누락(misses), d = 정확한 부정(correct negatives)
  - 기후빈도(base rate) s = (a+c)/n, 예보빈도 r = (a+b)/n
  - 주의: 자료마다 a,b,c,d 칸 배치 관행이 다르다(특히 b/c). 본 문서는 위 정의를 일관 사용.
- **적용 도메인/자료형**: 격자·시계열·위성 모두. NetCDF 격자는 격자점별로, CSV 시계열은 시각별로 임계 초과 여부를 산출해 표를 누적.
- **입력·전제**: 예보와 관측이 동일 시공간 격자/시각에 **정렬·보간**되어 있어야 함. 임계값(threshold)을 도메인에 맞게 정의(예: 파고 경보값, 강수 1 mm/일).
- **해석 기준**: 표 자체는 점수가 아니라 입력. 어떤 임계값·표본수(n)로 만들었는지 명시.
- **한계·주의**: 임계값 선택에 민감. 표본수가 작고 사건이 드물면 칸(특히 a)이 0이 되어 일부 점수가 정의되지 않음.
- **출처**: WWRP/WGNE JWGFVR Forecast Verification 페이지(CAWCR); Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification*.

---

### 정확도 / 정분율 (Accuracy / Proportion Correct, PC)

- **무엇을 측정/검증하나**: 전체 예보 중 맞은 비율(yes·no 모두 포함).
- **정의·수식**: PC = (a+d)/n
- **적용 도메인/자료형**: 모든 범주형 자료.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 1. 무작위 대비 0.5가 기준은 아님(기후빈도 의존).
- **한계·주의**: 드문 사건에서 "항상 no" 예보만으로도 매우 높은 값이 나와 **오도되기 쉽다**(가장 흔한 범주 d에 좌우됨). 해양 극값(드문 고파·고수온)에는 단독 사용 금지.
- **출처**: CAWCR Forecast Verification; Wilks (Statistical Methods).

---

### 빈도편향 (Frequency Bias Index, FBI / Bias Score)

- **무엇을 측정/검증하나**: 예보가 사건을 관측 대비 얼마나 자주/드물게 예보했는가(과대·과소 예보 경향).
- **정의·수식**: FBI = (a+b)/(a+c)
- **적용 도메인/자료형**: 모든 범주형 자료.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~∞, 완벽 = 1. FBI>1 과대예보(overforecasting), FBI<1 과소예보(underforecasting).
- **한계·주의**: 위치 일치(correspondence)는 보지 않고 **빈도만** 비교 — 적중률과 무관하게 1이 될 수 있음. 항상 POD/FAR와 함께 본다.
- **출처**: CAWCR Forecast Verification; Wilks (Statistical Methods).

---

### 탐지확률 / 적중률 (Probability of Detection, POD / Hit Rate, H)

- **무엇을 측정/검증하나**: 실제 발생한 사건 중 예보가 맞춘 비율.
- **정의·수식**: POD = H = a/(a+c)
- **적용 도메인/자료형**: 모든 범주형; 경보·위험사건 검증의 핵심.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 1. 높을수록 좋음.
- **한계·주의**: **오경보(b)를 무시** — "yes"를 남발하면 인위적으로 올릴 수 있음. 반드시 FAR/POFD/SR와 짝지어 본다. 기후빈도에 민감.
- **출처**: CAWCR Forecast Verification; Jolliffe & Stephenson (Forecast Verification).

---

### 오경보비 (False Alarm Ratio, FAR)

- **무엇을 측정/검증하나**: "yes"로 예보한 것 중 실제로는 발생하지 않은 비율.
- **정의·수식**: FAR = b/(a+b)
- **적용 도메인/자료형**: 모든 범주형.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 0(낮을수록 좋음).
- **한계·주의**: **누락(c)을 무시**. POD와 짝으로 사용. (오탐지확률 POFD와 혼동 주의 — 분모가 다름.)
- **출처**: CAWCR Forecast Verification; Wilks (Statistical Methods).

---

### 오탐지확률 / 오경보율 (Probability of False Detection, POFD / False Alarm Rate, F)

- **무엇을 측정/검증하나**: 실제 비발생(no) 중 잘못 "yes"로 예보한 비율. ROC 곡선의 x축.
- **정의·수식**: POFD = F = b/(b+d)
- **적용 도메인/자료형**: 모든 범주형; ROC 분석의 핵심 성분.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 0.
- **한계·주의**: 결정론 예보에서는 단독 보고가 드물고 주로 ROC·PSS 계산에 사용. FAR(분모 a+b)와 다름.
- **출처**: CAWCR Forecast Verification; Mason (ROC 관련, Jolliffe & Stephenson 수록).

---

### 성공비 (Success Ratio, SR)

- **무엇을 측정/검증하나**: "yes"로 예보한 것 중 실제 발생한 비율(= 1 − FAR).
- **정의·수식**: SR = a/(a+b) = 1 − FAR
- **적용 도메인/자료형**: 모든 범주형; **성능 다이어그램(performance diagram)**에서 POD와 함께 축으로 사용.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 1.
- **한계·주의**: FAR와 동일 정보의 다른 표현. 성능 다이어그램은 POD(y)–SR(x)에 CSI·FBI 등고선을 겹쳐 한 그림으로 다지표를 본다(Roebber 2009).
- **출처**: Roebber (2009), *Visualizing multiple measures of forecast quality*, Wea. Forecasting; CAWCR Forecast Verification.

---

### 임계성공지수 / 위협점수 (Critical Success Index, CSI / Threat Score, TS)

- **무엇을 측정/검증하나**: 적중률 — 단, 정확한 부정(d)을 제외하고 a,b,c만으로 사건 예측 성능을 봄.
- **정의·수식**: CSI = TS = a/(a+b+c)
- **적용 도메인/자료형**: 강수·고파 등 드문 사건; 결정론 격자 검증에 널리 사용.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 0~1, 완벽 = 1, 0 = 무기술.
- **한계·주의**: 누락(c)과 오경보(b)를 모두 벌점화하지만 **기후빈도에 의존** — 드문 사건일수록 낮아지며 서로 다른 빈도·지역 간 직접 비교 부적절(→ ETS 사용). 무작위 적중을 보정하지 않음.
- **출처**: CAWCR Forecast Verification; Schaefer (1990), *The critical success index as an indicator of warning skill*, Wea. Forecasting.

---

### 공평임계점수 / 길버트 기술점수 (Equitable Threat Score, ETS / Gilbert Skill Score, GSS)

- **무엇을 측정/검증하나**: CSI에서 **무작위(random chance)로 맞은 적중**을 제거해 공평화한 점수.
- **정의·수식**: a_ref = (a+b)(a+c)/n ; ETS = (a − a_ref)/(a + b + c − a_ref)
- **적용 도메인/자료형**: NWP 강수 검증 표준; 격자·시계열.
- **입력·전제**: 분할표, 충분한 표본수 n.
- **해석 기준**: 범위 −1/3 ~ 1, 완벽 = 1, 0 = 무기술. "공평성(equitability)" 덕분에 서로 다른 기후 체제 간 비교가 CSI보다 공정.
- **한계·주의**: 여전히 사건빈도·표본수에 약간 의존하고, 극단적으로 드문 사건에서는 0으로 퇴화(degenerate)할 수 있음(→ EDI/SEDI 권장). a_ref가 표본수에 의존.
- **출처**: CAWCR Forecast Verification; Gilbert (1884); Hogan et al. (2010), *Equitability revisited*, Wea. Forecasting.

---

### 하이드케 기술점수 (Heidke Skill Score, HSS)

- **무엇을 측정/검증하나**: 무작위 예보 대비 정확도 개선(정분율을 무작위 기댓값으로 보정).
- **정의·수식**: E = [(a+b)(a+c) + (c+d)(b+d)]/n ; HSS = (a + d − E)/(n − E)
- **적용 도메인/자료형**: 2×2 및 다범주 확장 가능; 모든 범주형 자료.
- **입력·전제**: 분할표, 큰 표본수.
- **해석 기준**: 범위 −1 ~ 1(흔히 (−∞,1]로도 표기), 완벽 = 1, 0 = 무기술(무작위 대비 개선 없음).
- **한계·주의**: 기준예보가 "무작위"라 항상 최선의 비교 기준은 아님(지속성/기후 대비가 더 의미 있을 때 있음). 표본 작으면 불안정.
- **출처**: CAWCR Forecast Verification; Heidke (1926); Wilks (Statistical Methods).

---

### 피어스 기술점수 / 핸슨-카이퍼스 / 참기술통계 (Peirce Skill Score, PSS / Hanssen–Kuipers, KSS / True Skill Statistic, TSS)

- **무엇을 측정/검증하나**: 예보가 yes 사건과 no 사건을 얼마나 잘 분리(discriminate)하는가.
- **정의·수식**: PSS = POD − POFD = a/(a+c) − b/(b+d)
- **적용 도메인/자료형**: 모든 범주형; 모든 분할표 칸 사용.
- **입력·전제**: 분할표.
- **해석 기준**: 범위 −1 ~ 1, 완벽 = 1, 0 = 무기술. **기후빈도에 비교적 독립적**이며 무작위·상수 예보 모두 0이 되는 공평 지표.
- **한계·주의**: 드문 사건에서는 POFD가 거의 0이 되어 PSS≈POD로 퇴화 → 빈번한 사건에 더 적합. 드문 사건은 EDI/SEDI 권장.
- **출처**: CAWCR Forecast Verification; Peirce (1884); Hanssen & Kuipers (1965); Jolliffe & Stephenson (Forecast Verification).

---

### 오즈비 (Odds Ratio, OR)

- **무엇을 측정/검증하나**: 옳은 yes 예보의 오즈 대 그른 yes 예보의 오즈 비율 — 예보-관측 연관 강도.
- **정의·수식**: OR = (a·d)/(b·c)
- **적용 도메인/자료형**: 모든 범주형; 드문 사건 연관성 평가에 유용.
- **입력·전제**: 분할표. **어느 칸도 0이면 정의 안 됨**(필요시 0.5 보정).
- **해석 기준**: 범위 0~∞, 완벽 = ∞, 1 = 무기술. 클수록 좋음. 사전확률(prior)을 반영, 헤징(hedging)에 덜 민감.
- **한계·주의**: 직접적인 점수 척도가 아님(스케일이 비선형). 칸 0 문제. 해석 위해 보통 ORSS로 변환.
- **출처**: Stephenson (2000), *Use of the "odds ratio" for diagnosing forecast skill*, Wea. Forecasting; CAWCR Forecast Verification.

---

### 오즈비 기술점수 / Yule's Q (Odds Ratio Skill Score, ORSS)

- **무엇을 측정/검증하나**: 오즈비를 −1~1로 정규화한 기술점수(Yule's Q와 동일).
- **정의·수식**: ORSS = (a·d − b·c)/(a·d + b·c)
- **적용 도메인/자료형**: 모든 범주형.
- **입력·전제**: 분할표(칸 0 주의).
- **해석 기준**: 범위 −1 ~ 1, 완벽 = 1, 0 = 무기술. **주변합(marginal)·임계값 선택에 독립적**이라 헤징 어려움.
- **한계·주의**: 표본 적거나 칸이 0이면 불안정. 주변합 독립성이 장점이자(임계 무관) 한계(빈도편향 정보 손실).
- **출처**: Stephenson (2000), Wea. Forecasting; CAWCR Forecast Verification.

---

### 극단의존지수 (Extremal Dependence Index, EDI)

- **무엇을 측정/검증하나**: **드문 이진 사건**에 대한 결정론 예보 성능 — 사건이 드물어져도 퇴화하지 않는 지표.
- **정의·수식**: H = POD = a/(a+c), F = POFD = b/(b+d)
  EDI = [ln F − ln H] / [ln F + ln H]
- **적용 도메인/자료형**: 극값·드문 사건(고파, 폭염, 호우, 고수온 등) 결정론 검증.
- **입력·전제**: 분할표에서 H, F. F>0, H>0(칸 0이면 정의 안 됨).
- **해석 기준**: 범위 (−∞, 1], 완벽 = 1, 0 = 무기술. **기후빈도(base rate)에 독립**(H,F만의 함수), 비퇴화(non-degenerating), 점근적 공평.
- **한계·주의**: 헤징 가능성(약간) 및 비대칭성 — 이를 보완한 SEDI가 보통 권장. H 또는 F가 0/1이면 로그 발산.
- **출처**: Ferro & Stephenson (2011), *Extremal Dependence Indices: Improved Verification Measures for Deterministic Forecasts of Rare Binary Events*, Wea. Forecasting, 26(5), 699–713, doi:10.1175/WAF-D-10-05030.1.

---

### 대칭극단의존지수 (Symmetric Extremal Dependence Index, SEDI)

- **무엇을 측정/검증하나**: EDI의 단점(헤징·비대칭)을 보완한, 드문 사건용 대칭 지표.
- **정의·수식**: SEDI = [ln F − ln H − ln(1−F) + ln(1−H)] / [ln F + ln H + ln(1−F) + ln(1−H)]
- **적용 도메인/자료형**: 극값·드문 사건 결정론 검증(권장 표준).
- **입력·전제**: H, F ∈ (0,1) 모두 0/1이 아니어야 함.
- **해석 기준**: 범위 (−∞, 1], 완벽 = 1, 0 = 무기술. **기후빈도 독립**, 비퇴화, 점근적 공평, 헤징이 가장 어렵고 ROC 등고선이 규칙적.
- **한계·주의**: 작은 표본에서 신뢰구간 넓음(부트스트랩 권장). H/F가 0 또는 1이면 정의 안 됨 → 표본 보정 필요.
- **출처**: Ferro & Stephenson (2011), Wea. Forecasting, 26(5); North et al. (2013), *An assessment of the SEEPS and SEDI metrics...*, Meteorol. Appl., 20.

---

### 극단의존점수 (Extreme Dependency Score, EDS / Symmetric EDS, SEDS)

- **무엇을 측정/검증하나**: EDI/SEDI의 선구 지표 — 드문 사건의 예보-관측 의존성. (역사·비교 목적 포함.)
- **정의·수식**: 기후빈도 s = (a+c)/n에 대해
  EDS = [2·ln((a+c)/n)] / [ln(a/n)] − 1
  (SEDS는 예보·관측 주변빈도를 모두 사용한 대칭화 버전.)
- **적용 도메인/자료형**: 드문 사건 결정론 검증.
- **입력·전제**: 분할표, 적중 a>0.
- **해석 기준**: 범위 (−1, 1] 부근, 완벽 = 1. 비퇴화이나 **기후빈도 의존·헤징 용이**라는 결함이 있음.
- **한계·주의**: 결함 때문에 현재는 EDI/SEDI로 대체 권장. 비교·문헌 추적용으로만 사용.
- **출처**: Stephenson et al. (2008), *The extreme dependency score: a non-vanishing measure for forecasts of rare events*, Meteorol. Appl., 15; Hogan et al. (2009); Ferro & Stephenson (2011).

---

### 브라이어 점수 (Brier Score, BS)

- **무엇을 측정/검증하나**: 이진 사건에 대한 **확률예보**의 평균제곱오차.
- **정의·수식**: BS = (1/n) Σ (p_i − o_i)² ; p_i = 예보확률, o_i = 발생 1 / 미발생 0
- **적용 도메인/자료형**: 확률예보(앙상블 비율, 통계예보 확률 등); 시계열·격자.
- **입력·전제**: 사건 임계값으로 관측을 0/1화, 대응 예보확률 p∈[0,1].
- **해석 기준**: 범위 0~1, 완벽 = 0(낮을수록 좋음). 적절점수(strictly proper).
- **한계·주의**: 기후빈도에 민감 — 드문 사건은 실제 기술 없이도 낮은 BS가 나오기 쉬움. 절대값만으로 체제 간 비교 부적절(→ BSS).
- **출처**: Brier (1950), *Verification of forecasts expressed in terms of probability*, Mon. Wea. Rev., 78; Wilks (Statistical Methods).

---

### 브라이어 점수 분해 (Brier Score Decomposition: Reliability–Resolution–Uncertainty)

- **무엇을 측정/검증하나**: BS를 신뢰도(reliability)·분해능(resolution)·불확실성(uncertainty)으로 분해해 오차 원인 진단.
- **정의·수식**: 확률 빈(bin) k(표본수 n_k, 평균예보확률 p_k, 관측빈도 ō_k), 전체 기후빈도 ō에 대해
  BS = (1/n)Σ n_k(p_k − ō_k)² − (1/n)Σ n_k(ō_k − ō)² + ō(1−ō)
  = Reliability − Resolution + Uncertainty
- **적용 도메인/자료형**: 확률예보; 신뢰도 다이어그램과 짝.
- **입력·전제**: 예보확률을 빈으로 분할(보정 추정 Murphy–Winkler 분해).
- **해석 기준**: Reliability 작을수록(↓) 좋음, Resolution 클수록(↑) 좋음, Uncertainty는 자료 고유.
- **한계·주의**: 빈 개수·표본수에 따라 추정 편향 — Ferro & Fricker(2012) 편향보정 권장. Bröcker(2009)가 임의의 적절점수로 일반화.
- **출처**: Murphy (1973), *A new vector partition of the probability score*, J. Appl. Meteor., 12, 595–600; Bröcker (2009), Q.J.R. Meteorol. Soc.; Ferro & Fricker (2012).

---

### 브라이어 기술점수 (Brier Skill Score, BSS)

- **무엇을 측정/검증하나**: 기준예보(보통 기후값) 대비 BS 개선도.
- **정의·수식**: BSS = 1 − BS_forecast / BS_reference (reference = 기후 확률)
- **적용 도메인/자료형**: 확률예보.
- **입력·전제**: 기준예보 BS_ref(기후빈도) 산출.
- **해석 기준**: 범위 (−∞, 1], 완벽 = 1, 0 = 기후 대비 무개선, 음수 = 기후보다 나쁨.
- **한계·주의**: 엄밀 적절(strictly proper)은 아님; 작은 표본에서 불안정. 기준예보 선택에 따라 값이 달라짐(명시 필요).
- **출처**: CAWCR Forecast Verification; Wilks (Statistical Methods).

---

### 신뢰도 다이어그램 (Reliability Diagram / Attributes Diagram)

- **무엇을 측정/검증하나**: 예보확률과 실제 관측빈도의 일치(보정/calibration). 조건부 편향 진단.
- **정의·수식**: x축 예보확률 빈, y축 해당 빈의 관측상대빈도. 대각선이 완벽 신뢰. 부속(attributes) 다이어그램은 무기술선·분해능선·샤프니스 히스토그램을 함께 표시.
- **적용 도메인/자료형**: 확률예보.
- **입력·전제**: 충분한 표본을 확률 빈으로 분할.
- **해석 기준**: 곡선이 대각선에 가까울수록 신뢰도 높음. 대각선 아래 = 과대예보, 위 = 과소예보. 곡선이 수평선(기후값)에서 멀수록 분해능 큼. 샤프니스 히스토그램으로 예보의 첨예함 확인.
- **한계·주의**: 빈 개수·표본수에 민감(빈별 표본 적으면 잡음). 신뢰성 구간(일관성 막대, consistency bars) 표시 권장.
- **출처**: Wilks (Statistical Methods); Hsu & Murphy (1986); Bröcker & Smith (2007), *Increasing the reliability of reliability diagrams*, Wea. Forecasting.

---

### 상대운영특성 / ROC 곡선 및 AUC (Relative Operating Characteristic, ROC / Area Under Curve, AUC)

- **무엇을 측정/검증하나**: 확률예보의 **판별력(discrimination/resolution)** — 사건/비사건을 구분하는 능력. 편향에 둔감.
- **정의·수식**: 확률 임계값을 변화시키며 (POFD, POD) 점을 찍어 그린 곡선. AUC = 곡선 아래 면적(사다리꼴 또는 이항정규 적합).
- **적용 도메인/자료형**: 확률예보; 의사결정 임계 다양.
- **입력·전제**: 여러 확률 임계로 분할표 다수 산출.
- **해석 기준**: AUC 범위 0~1, 완벽 = 1, 0.5 = 무기술(대각선). 통상 AUC>0.7이면 유용성 있다고 봄.
- **한계·주의**: **보정(reliability)은 보지 않음** — 신뢰도 다이어그램과 상보적으로 함께 본다. 편향 보정 후에도 좋은 ROC 가능. 표본 적으면 곡선 거칠다.
- **출처**: Mason (1982); Mason & Graham (2002), Q.J.R. Meteorol. Soc.; Jolliffe & Stephenson (Forecast Verification); CAWCR Forecast Verification.

---

### 순위확률점수 (Ranked Probability Score, RPS)

- **무엇을 측정/검증하나**: 다범주(순서형) 확률예보의 정확도 — 누적분포 기준 제곱오차(거리 개념 포함).
- **정의·수식**: K개 순서범주, 누적예보확률 P_k, 누적관측 O_k(0/1 누적)에 대해
  RPS = Σ_{k=1}^{K} (P_k − O_k)²  (정규화 시 1/(K−1))
- **적용 도메인/자료형**: 다범주 확률예보(예: 약/중/강 파고 범주). 브라이어 점수의 다범주 일반화.
- **입력·전제**: 순서형 범주, 누적확률.
- **해석 기준**: 작을수록 좋음, 완벽 = 0. 기술점수 RPSS = 1 − RPS/RPS_ref.
- **한계·주의**: 범주 경계 임의성; 표본 적으면 RPSS 음의 편향(앙상블 크기 보정 필요).
- **출처**: Epstein (1969); Murphy (1971); Wilks (Statistical Methods).

---

### 연속순위확률점수 (Continuous Ranked Probability Score, CRPS)

- **무엇을 측정/검증하나**: 연속 변수 확률예보의 정확도 — 예보 CDF와 관측 계단함수 사이 제곱거리(RPS의 무한 범주 극한).
- **정의·수식**: CRPS(F, y) = ∫_{−∞}^{∞} [F(x) − 𝟙{x ≥ y}]² dx ; F=예보 CDF, y=관측.
- **적용 도메인/자료형**: 앙상블·확률예보(파고·수온 등 연속 변수). 결정론 예보에서는 절대오차(MAE)로 환원.
- **입력·전제**: 예보 CDF 또는 앙상블 멤버, 관측값.
- **해석 기준**: 음의 지향(작을수록 좋음), 완벽 = 0. 적절점수. 신뢰도+분해능/불확실성으로 분해 가능(Hersbach 2000).
- **한계·주의**: 극단/꼬리(tail) 판별력이 약함 — 임계가중 CRPS(twCRPS)로 보완. 앙상블 크기 작으면 편향.
- **출처**: Hersbach (2000), *Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems*, Wea. Forecasting, 15(5), 559–570; Gneiting & Raftery (2007), JASA.

---

### 임계가중 연속순위확률점수 (Threshold-Weighted CRPS, twCRPS)

- **무엇을 측정/검증하나**: CRPS에 가중함수를 곱해 **꼬리(극값) 영역의 확률예보 성능을 강조** — 극단 사건(고파·해양폭염 등) 확률예보 검증에 특화.
- **정의·수식**: 가중함수 w(x)≥0(예: 임계 r 이상만 w=1, 또는 누적가중 W(x))에 대해
  twCRPS(F, y) = ∫_{−∞}^{∞} [F(x) − 𝟙{x ≥ y}]² w(x) dx
  (w≡1이면 일반 CRPS. 상위꼬리 강조는 w(x)=𝟙{x≥r} 형태가 흔함.)
- **적용 도메인/자료형**: 앙상블·확률예보의 극값 검증(연속 변수). 결정론·앙상블 모두 적용 가능.
- **입력·전제**: 예보 CDF 또는 앙상블 멤버, 관측값, 사용자 정의 가중함수(임계 r).
- **해석 기준**: 음의 지향(작을수록 좋음), 완벽 = 0. 적절점수(proper) 유지 — 가중을 줘도 헤징 불가. 가중함수·임계를 반드시 명시해 비교 일관성 확보.
- **한계·주의**: 가중함수 선택이 결과를 좌우 → 사전에 고정·공유. 극값 영역 표본이 적으면 분산 큼(부트스트랩 권장). 절대값은 변수·임계 의존 → 기준예보 대비 기술점수로 보고 권장.
- **출처**: Gneiting & Ranjan (2011), *Comparing density forecasts using threshold- and quantile-weighted scoring rules*, J. Bus. Econ. Stat., 29; Lerch et al. (2017), *Forecaster's dilemma: Extreme events and forecast evaluation*, Stat. Sci., 32.

---

### 순위 히스토그램 / 탈라그랑 다이어그램 (Rank Histogram / Talagrand Diagram)

- **무엇을 측정/검증하나**: 앙상블 예보의 **신뢰성(reliability)·스프레드 적정성** — 관측이 앙상블 분포 안에서 균일하게 위치하는가.
- **정의·수식**: 각 검증 시점에서 관측값이 정렬된 N개 앙상블 멤버가 만드는 N+1개 구간 중 몇 번째에 들어가는지 순위를 매겨 도수분포(히스토그램)로 누적.
- **적용 도메인/자료형**: 앙상블 예보(파고·수온·풍속 등 연속 변수); 시계열·격자점별.
- **입력·전제**: 동일 시공간의 앙상블 멤버 집합과 대응 관측. 관측오차는 별도 고려(작게 가정 또는 섭동).
- **해석 기준**: **평평(flat)** = 신뢰성 양호. **U자형** = 과소산포(under-dispersive, 스프레드 부족), **∩자형(돔형)** = 과대산포(over-dispersive), **기울어짐(sloped)** = 평균 편향. 평탄도는 카이제곱 검정 등으로 정량화.
- **한계·주의**: 평평함은 신뢰성의 필요조건일 뿐 충분조건은 아님(보상적 오차로 평평해질 수 있음). 관측오차·표본수에 민감.
- **출처**: Hamill (2001), *Interpretation of rank histograms for verifying ensemble forecasts*, Mon. Wea. Rev., 129, 550–560; Talagrand et al. (1997); Anderson (1996), J. Climate.

---

### 스프레드-스킬 관계 (Spread–Skill Relationship)

- **무엇을 측정/검증하나**: 앙상블 **스프레드(불확실성 추정)**가 실제 예보오차(스킬)와 통계적으로 일치하는가 — 신뢰성 있는 앙상블이면 평균 스프레드 ≈ 평균오차(RMSE).
- **정의·수식**: 잘 보정된 앙상블에서 앙상블 분산의 기댓값과 (멤버 수 보정한) 평균제곱오차가 일치하는 관계를 사용. 흔히 평균 앙상블 표준편차(spread)와 앙상블평균 RMSE를 산포구간(spread bin)별로 비교; 스프레드–스킬 상관계수도 사용.
- **적용 도메인/자료형**: 앙상블 예보; 시계열·격자.
- **입력·전제**: 앙상블 멤버, 관측, 멤버수 N(유한앙상블 보정 √((N+1)/N) 필요).
- **해석 기준**: spread ≈ RMSE이면 적정. spread < RMSE이면 과소산포(과신), spread > RMSE이면 과대산포. 산포구간별 1:1 선 근접도로 진단.
- **한계·주의**: 단일 상관계수는 오도 가능(분포 정보 손실). 관측오차를 RMSE에서 제거해야 공정. 순위 히스토그램과 함께 보는 것이 표준.
- **출처**: Fortin et al. (2014), *Why should ensemble spread match the RMSE of the ensemble mean?*, J. Hydrometeor., 15; Leutbecher & Palmer (2008), *Ensemble forecasting*, J. Comput. Phys., 227.

---

### 다범주 하이드케 기술점수 (Multi-category Heidke Skill Score)

- **무엇을 측정/검증하나**: K×K 분할표에서 무작위 대비 정확도(2×2 HSS의 다범주 확장).
- **정의·수식**: HSS = [Σ_i p(f_i,o_i) − Σ_i p(f_i)p(o_i)] / [1 − Σ_i p(f_i)p(o_i)] (p=상대빈도)
- **적용 도메인/자료형**: 다범주 결정론(예: 무강수/약/강, 풍속 계급).
- **입력·전제**: K×K 분할표.
- **해석 기준**: 범위 (−∞, 1], 완벽 = 1, 0 = 무작위 대비 무기술.
- **한계·주의**: 오차의 "거리"를 반영 못함(인접 오분류와 원거리 오분류 동일 벌점) → 순서형엔 게리티/RPS가 적절.
- **출처**: CAWCR Forecast Verification; Wilks (Statistical Methods).

---

### 게리티 점수 (Gerrity Score / Gandin–Murphy Skill Score)

- **무엇을 측정/검증하나**: 다범주(순서형) 결정론의 공평 기술점수 — 오차 거리에 따라 차등 벌점, 드문 범주 정답에 보상.
- **정의·수식**: K×K 분할표와 기후빈도 기반 스코어링 행렬 S_ij(간딘–머피 방식)에 대해
  GS = Σ_{i,j} p(f_i,o_j) S_ij ; 대각선 보상, 비대각선은 거리·기후빈도에 따라 벌점.
- **적용 도메인/자료형**: 순서형 다범주 결정론(강수 계급, 파고 계급 등).
- **입력·전제**: K×K 분할표, 기후빈도.
- **해석 기준**: 범위 −1 ~ 1, 완벽 = 1, 0 = 무기술. **보수적 예보를 보상하지 않으며** 작은 오차는 큰 오차보다 덜 벌점.
- **한계·주의**: 스코어링 행렬이 기후빈도에 의존 → 표본·체제 변하면 가중 변함. 해석이 직관적이지 않음.
- **출처**: Gerrity (1992), *A note on Gandin and Murphy's equitable skill score*, Mon. Wea. Rev., 120; CAWCR Forecast Verification.

---

### SEEPS (Stable Equitable Error in Probability Space)

- **무엇을 측정/검증하나**: 강수예보의 공평·안정 오차점수 — 건조/약/강 3범주를 기후 CDF 기반 "확률 공간"에서 평가.
- **정의·수식**: 3×3 분할표 + 기후 CDF로 정의된 스코어링 행렬. 약/강 경계는 지역 강수기후(상위 1/3 등)에 따라 가변. 점수는 오차이므로 1−SEEPS가 기술.
- **적용 도메인/자료형**: 강수(또는 유사한 비대칭 분포 변수) 결정론 검증; 격자·관측소.
- **입력·전제**: 지역 강수 기후분포(보통 30년), 건조 임계(예: 0.2 mm).
- **해석 기준**: 0(완벽)~ 약 2 범위의 오차. 헤징·드리즐 과예보·대규모 강수 누락·합류셀 오위치 등을 식별. ECMWF·WMO 표준 모니터링 지표.
- **한계·주의**: 강수에 특화(타 변수 일반화엔 재정의 필요). 기후 표본·건조임계에 민감.
- **출처**: Rodwell et al. (2010), *A new equitable score suitable for verifying precipitation in NWP*, Q.J.R. Meteorol. Soc., 136; Haiden et al. (2012), Mon. Wea. Rev.

---

### 분율 기술점수 / 근접(이웃) 검증 (Fractions Skill Score, FSS / Neighborhood Verification)

- **무엇을 측정/검증하나**: 임계 초과 사건의 **공간 일치**를 격자점 1:1이 아니라 일정 반경(이웃, neighborhood) 안의 **사건 발생 비율(분율)**로 비교 — "이중벌점(double penalty, 약간 어긋난 위치를 두 번 벌점)"을 완화하고 어느 공간 규모에서 기술이 생기는지 진단.
- **정의·수식**: 임계로 이진화 후, 격자점마다 변 길이 n(반경)의 이웃 안 사건 분율 P_fcst, P_obs를 계산.
  FBS = (1/N) Σ (P_fcst − P_obs)²  (분율 브라이어 점수)
  FBS_worst = (1/N)[Σ P_fcst² + Σ P_obs²]
  FSS = 1 − FBS / FBS_worst
- **적용 도메인/자료형**: **NetCDF 격자 전용**(파고·강수·SST 이상 등 임계 초과장). 모델 vs ERA5/GLORYS 격자 비교에 직접 적합.
- **입력·전제**: 동일 격자에 정렬·보간된 두 장, 사건 임계값, 이웃 크기 n의 집합(여러 규모 스캔).
- **해석 기준**: 범위 0~1, 완벽 = 1. 이웃을 키우면 FSS 증가 — FSS가 "유용(skilful)" 기준 0.5 + f₀/2(f₀=기준빈도)를 넘는 최소 규모가 모델의 **유효 공간 스킬 스케일**. 규모–FSS 곡선으로 보고.
- **한계·주의**: 임계·이웃 크기 선택에 의존(여러 값 스캔 필수). 강도 오차보다 위치/규모 오차에 초점. 사건 빈도가 매우 낮으면 불안정.
- **출처**: Roberts & Lean (2008), *Scale-Selective Verification of Rainfall Accumulations from High-Resolution Forecasts of Convective Events*, Mon. Wea. Rev., 136(1), 78–97; Roberts (2008), Meteorol. Appl.; Skok & Roberts (2016), Q.J.R. Meteorol. Soc.

---

### SAL — 구조·진폭·위치 (Structure–Amplitude–Location)

- **무엇을 측정/검증하나**: 한 도메인 안의 사건장(예: 임계 초과 영역)을 **구조(S)·진폭(A)·위치(L)** 세 성분으로 분해해 오차 특성을 진단(객체 기반, 1:1 매칭 불필요).
- **정의·수식**:
  - A = (⟨R_fcst⟩ − ⟨R_obs⟩)/[0.5(⟨R_fcst⟩+⟨R_obs⟩)] : 도메인 평균값의 상대 편차(−2~2).
  - L : 도메인 질량중심 거리 + 객체별 질량중심 분산 차이(0~2).
  - S : 임계로 식별한 객체들의 (적분값/최대값) 기반 크기·형태 척도 비교(−2~2).
- **적용 도메인/자료형**: 격자장(파고·강수·SST 이상 등); 정의된 도메인(예: 관심 해역) 단위.
- **입력·전제**: 동일 격자장, 객체 식별 임계(보통 도메인 최대값의 일정 비율 R*=f·R_max), 분석 도메인 경계.
- **해석 기준**: S·A·L 모두 0 = 완벽. A>0 과대(평균 과대모의), L>0 위치/분포 어긋남, S>0 객체가 너무 크고 평탄/S<0 너무 작고 첨예. 세 값을 산점도로 모델 비교.
- **한계·주의**: 도메인·임계 선택 민감. 객체 식별이 모호하면 S 불안정. 시간 매칭은 별도. 정량 임계 관행이 변수마다 다름.
- **출처**: Wernli et al. (2008), *SAL—A Novel Quality Measure for the Verification of Quantitative Precipitation Forecasts*, Mon. Wea. Rev., 136(11), 4470–4487.

---

### MODE — 객체기반 진단 평가 (Method for Object-based Diagnostic Evaluation)

- **무엇을 측정/검증하나**: 예보장·관측장에서 임계+평활화로 **객체(feature)**를 식별·매칭하고, 객체의 속성(면적·중심거리·축각·강도·종횡비 등) 차이로 공간 성능을 사람의 시각적 판단에 가깝게 진단.
- **정의·수식**: ① 합성곱 평활(convolution radius)+임계로 객체 마스크 생성 → ② 객체 속성 산출 → ③ 퍼지논리 총이익(total interest, 중심거리·면적비·교집합 등 가중합)으로 객체 매칭 → ④ 매칭·미매칭 객체 속성 분포 비교.
- **적용 도메인/자료형**: 격자장(강수·고파·SST 이상·해류 구조 등); 모델 vs 재분석/위성장.
- **입력·전제**: 동일 격자, 평활 반경·임계 파라미터, 매칭 가중·임계. (MET 소프트웨어에 구현.)
- **해석 기준**: 매칭 객체의 위치오차(중심거리)·면적비(1이 완벽)·강도편차 등으로 "무엇이·어디서·얼마나" 틀렸는지 서술. 단일 점수보다 진단형 보고.
- **한계·주의**: 파라미터(평활·임계·매칭 가중) 선택에 민감하고 다수 — 재현성 위해 고정·문서화. 단일 요약지표가 아니라 해석 필요. 계산량 큼.
- **출처**: Davis, Brown & Bullock (2006), *Object-Based Verification of Precipitation Forecasts. Part I*, Mon. Wea. Rev., 134(7), 1772–1784; Davis et al. (2006) Part II; MET (Model Evaluation Tools) User's Guide.

---

### 일반화극값분포 / 블록최대값 (Generalized Extreme Value, GEV / Block Maxima)

- **무엇을 측정/검증하나**: 블록(예: 연·월) 최대값의 분포를 모형화해 극값의 통계적 특성·재현수준을 추정.
- **정의·수식**: 블록최대값 M의 분포는 GEV로 수렴:
  G(z) = exp{ −[1 + ξ(z−μ)/σ]^(−1/ξ) }  (위치 μ, 척도 σ>0, 형상 ξ)
  ξ>0 Fréchet(두꺼운 꼬리), ξ=0 Gumbel, ξ<0 Weibull(상한 존재).
- **적용 도메인/자료형**: 시계열(연/월 최대 파고·해수면·수온 등). 격자는 격자점별 적합.
- **입력·전제**: 블록별 최대값 표본(독립·동일분포 근사), 충분한 블록수, 정상성(stationarity) 가정.
- **해석 기준**: 적합 후 재현수준 z_p = G^{-1}(1−p) 산출. QQ/PP plot, 우도비·AIC로 적합도 평가. 모델 vs 관측의 GEV 파라미터(특히 ξ)를 비교해 극값 재현성 검증.
- **한계·주의**: 블록당 1점만 사용 → 자료 비효율(POT가 더 효율적). 비정상(추세·계절)·종속성 위반 시 편향. ξ 추정은 표본에 민감.
- **출처**: Coles (2001), *An Introduction to Statistical Modeling of Extreme Values*, Springer; Fisher & Tippett (1928); NCAR/UCAR Extreme Value 가이드.

---

### 임계초과 / 일반화파레토분포 (Peaks-Over-Threshold, POT / Generalized Pareto Distribution, GPD)

- **무엇을 측정/검증하나**: 높은 임계값 u를 초과한 모든 값의 초과분 분포를 모형화 — 극값을 데이터 효율적으로 분석.
- **정의·수식**: Pickands–Balkema–de Haan 정리에 의해 초과분 (X−u | X>u)은 GPD로 수렴:
  H(y) = 1 − [1 + ξ y/σ̃]^(−1/ξ),  y>0
  사건 발생수는 포아송(Poisson)으로 모형화(→ Poisson-GPD / point process).
- **적용 도메인/자료형**: 시계열(파고·해수면·수온 초과); 격자점별 적합.
- **입력·전제**: 적절한 임계 u 선택(평균잔차수명 plot, 파라미터 안정성 plot), 초과사건 간 독립(declustering로 군집 제거).
- **해석 기준**: 재현수준·재현주기 산출. 모델 vs 재분석/관측의 GPD ξ·σ̃, 초과율 비교로 극값 검증.
- **한계·주의**: 임계 선택이 핵심(편향-분산 트레이드오프). 시간 종속(폭풍 군집) 시 declustering 필요. 비정상이면 공변량(GPD with covariates) 도입.
- **출처**: Coles (2001), Springer; Pickands (1975); Davison & Smith (1990), JRSS-B.

---

### 재현주기 / 재현수준 (Return Period / Return Level)

- **무엇을 측정/검증하나**: 특정 크기 이상의 극값이 평균 얼마 만에 한 번 발생/초과하는가(설계·위험평가의 핵심).
- **정의·수식**: 재현주기 T = 1/(연 초과확률 p). 재현수준 z_T는 P(X>z_T)=1/T인 값.
  GEV: z_T = μ − (σ/ξ)[1 − {−ln(1−1/T)}^{−ξ}] (ξ≠0).
- **적용 도메인/자료형**: 시계열 극값(설계파고, 고극조위 등); 격자점별 지도화 가능.
- **입력·전제**: 적합된 GEV/GPD, 정상성(또는 비정상 모델), 연 초과율.
- **해석 기준**: T년 재현수준을 모델과 관측/재분석에서 산출해 비교(신뢰구간 포함). 곡선(return level plot)으로 시각화.
- **한계·주의**: 자료 길이보다 훨씬 긴 T 외삽은 불확실성 큼(델타법/프로파일우도 신뢰구간 필수). 기후변화로 정상성 깨지면 "정상 재현주기" 개념 자체 주의.
- **출처**: Coles (2001), Springer; WMO-No.100 *Guide to Climatological Practices*; NCAR Extreme Value 가이드.

---

### 백분위수 기반 극한지표 (Percentile / Threshold Climate Indices, ETCCDI)

- **무엇을 측정/검증하나**: 백분위수(예: 90/95/99p) 초과 일수·강도 등 표준화된 극한 기후지수 — 모델의 극값 통계 재현성 검증.
- **정의·수식**: 예) TX90p = 일최고기온이 기후 90백분위 초과한 날의 비율; R95pTOT = 95p 초과 강수 총량; WSDI/CSDI(연속 폭염/한파 일수). 임계는 기준기간(예: 1961–1990) 백분위.
- **적용 도메인/자료형**: 시계열·격자(기온·강수·파고 등). 해양 적용: 해양폭염(MHW)은 일별 기후 90p 초과 5일 이상(Hobday 2016)으로 정의.
- **입력·전제**: 기준기간 기후 백분위, 일자료, 동일 기준으로 모델·관측 산출.
- **해석 기준**: 모델 vs 관측/재분석의 지수 시계열·추세·공간장 비교(편향·상관·RMSE). 표준화 덕에 다지역·다모델 비교 용이.
- **한계·주의**: 백분위 추정의 표본 의존(부트스트랩 권장), 기준기간 선택 민감. 강수는 0값 처리·임계(1 mm) 관행 명시 필요.
- **출처**: Zhang et al. (2011), *Indices for monitoring changes in extremes* (ETCCDI), WIREs Clim. Change; Hobday et al. (2016), *A hierarchical approach to defining marine heatwaves*, Prog. Oceanogr.; WMO ET-SCI 지침.

---

### 해양폭염 검출·검증 (Marine Heatwave Detection & Verification, MHW)

- **무엇을 측정/검증하나**: 해수면온도(SST) 등의 **극단 고온 사건(해양폭염)**을 표준 정의로 검출하고, 모델이 그 발생·기간·강도를 재분석(GLORYS/OISST)·관측 대비 얼마나 재현하는가. 본질적으로 임계 초과 사건 → 범주형 지표(POD/FAR/CSI/SEDI)와 연결.
- **정의·수식**: Hobday et al. (2016) 위계적 정의 — 일별 기후 평균 + 일별 **계절성 90 백분위(seasonally varying 90th percentile)**를 임계로, 임계 초과가 **5일 이상 연속**이면 MHW 사건. 짧은 간격(≤2일)은 병합. 강도 범주(moderate/strong/severe/extreme)는 임계 초과폭의 배수로 정의. 산출 지표: 발생빈도·지속일수·누적강도(°C·days)·최대강도.
- **적용 도메인/자료형**: 시계열(정점 SST) 및 격자(NetCDF SST장; 격자점별 사건화). 모델 vs OISST/GLORYS/ERA5-SST.
- **입력·전제**: 충분히 긴 기후 기준기간(보통 ≥30년)으로 일별 기후·90p 산정, 동일 기준을 모델·관측에 적용(또는 각자 기준 산정 후 명시), 일자료.
- **해석 기준**: (1) 사건 시계열을 0/1화해 POD/FAR/CSI/SEDI로 검출 성능 평가; (2) 지속일수·누적강도·MHW일수 등 지표를 편향·상관·RMSE로 비교; (3) 공간장은 발생빈도/총 MHW일수 지도 비교. 임계 기준(고정 vs 이동)·기준기간을 반드시 명시.
- **한계·주의**: 기준기간·평활(보통 ±5일 창, 31일 이동평균)·추세 제거 여부에 결과 민감. 기후변화 추세가 있으면 "이동 기준선" 선택이 사건 수를 크게 바꿈. 모델·관측의 기준선을 통일하지 않으면 비교가 왜곡됨. 표층 한정(아표층 MHW는 별도).
- **출처**: Hobday et al. (2016), *A hierarchical approach to defining marine heatwaves*, Prog. Oceanogr., 141, 227–238; Hobday et al. (2018), *Categorizing and naming marine heatwaves*, Oceanography, 31(2); `marineHeatWaves`/`heatwaveR` 구현 패키지.

---

## 출처(References)

> 표준 참고문헌은 실제 존재가 확인된 항목만 수록. 웹조사로 확인한 항목은 URL을 병기했고, 교과서·표준지침은 그 형태로 표기. DOI는 확인된 것만 기재.

**검증 지침·종합 자료(웹 확인)**
- WWRP/WGNE Joint Working Group on Forecast Verification Research — Forecast Verification: Issues, Methods and FAQ (CAWCR/Bureau of Meteorology). https://www.cawcr.gov.au/projects/verification/
- WMO — WWRP/WGNE Joint Working Group on Forecast Verification Research. https://wmo.int/wwrpwgne-joint-working-group-forecast-verification-research
- NCAR/UCAR — Basic Extreme Value Statistics (NCL Applications). https://www.ncl.ucar.edu/Applications/extreme_value.shtml
- MET (Model Evaluation Tools) 11.x — Appendix C: Verification Measures (FSS·MODE 포함). https://met.readthedocs.io/en/latest/Users_Guide/appendixC.html
- scores 패키지 — SEEPS·FSS 튜토리얼. https://scores.readthedocs.io/en/latest/tutorials/SEEPS.html , https://scores.readthedocs.io/en/stable/tutorials/Fractions_Skill_Score.html

**표준 교과서·참고문헌(확인됨)**
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences* (Academic Press; 다수 판) — 범주형·확률예보 검증 전반.
- Jolliffe, I.T. & Stephenson, D.B. (eds.) *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley) — POD/FAR/PSS/ROC/오즈비 등.
- Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values*, Springer — GEV/GPD/POT/재현수준.

**논문(웹 확인, 저널/권호 표기)**
- Brier, G.W. (1950) Verification of forecasts expressed in terms of probability. *Mon. Wea. Rev.*, 78, 1–3.
- Murphy, A.H. (1973) A new vector partition of the probability score. *J. Appl. Meteor.*, 12, 595–600.
- Stephenson, D.B. (2000) Use of the "odds ratio" for diagnosing forecast skill. *Wea. Forecasting*, 15, 221–232.
- Hersbach, H. (2000) Decomposition of the Continuous Ranked Probability Score for Ensemble Prediction Systems. *Wea. Forecasting*, 15(5), 559–570. https://journals.ametsoc.org/view/journals/wefo/15/5/1520-0434_2000_015_0559_dotcrp_2_0_co_2.xml
- Hamill, T.M. (2001) Interpretation of rank histograms for verifying ensemble forecasts. *Mon. Wea. Rev.*, 129, 550–560.
- Mason, S.J. & Graham, N.E. (2002) Areas beneath the relative operating characteristics (ROC) and relative operating levels (ROL) curves: Statistical significance and interpretation. *Q.J.R. Meteorol. Soc.*, 128(584), 2145–2166. https://rmets.onlinelibrary.wiley.com/doi/10.1256/003590002320603584
- Davis, C.A., Brown, B.G., Bullock, R. (2006) Object-based verification of precipitation forecasts. Part I: Methodology and application to mesoscale rain areas. *Mon. Wea. Rev.*, 134(7), 1772–1784. https://journals.ametsoc.org/view/journals/mwre/134/7/mwr3145.1.xml
- Bröcker, J. & Smith, L.A. (2007) Increasing the reliability of reliability diagrams. *Wea. Forecasting*, 22, 651–661.
- Roberts, N.M. & Lean, H.W. (2008) Scale-selective verification of rainfall accumulations from high-resolution forecasts of convective events. *Mon. Wea. Rev.*, 136(1), 78–97. https://journals.ametsoc.org/view/journals/mwre/136/1/2007mwr2123.1.xml
- Wernli, H., Paulat, M., Hagen, M., Frei, C. (2008) SAL—A novel quality measure for the verification of quantitative precipitation forecasts. *Mon. Wea. Rev.*, 136(11), 4470–4487. https://journals.ametsoc.org/view/journals/mwre/136/11/2008mwr2415.1.xml
- Leutbecher, M. & Palmer, T.N. (2008) Ensemble forecasting. *J. Comput. Phys.*, 227, 3515–3539.
- Stephenson, D.B., Casati, B., Ferro, C.A.T., Wilson, C.A. (2008) The extreme dependency score: a non-vanishing measure for forecasts of rare events. *Meteorol. Appl.*, 15, 41–50.
- Roebber, P.J. (2009) Visualizing multiple measures of forecast quality. *Wea. Forecasting*, 24, 601–608.
- Bröcker, J. (2009) Reliability, sufficiency, and the decomposition of proper scores. *Q.J.R. Meteorol. Soc.*, 135, 1512–1519.
- Rodwell, M.J., Richardson, D.S., Hewson, T.D., Haiden, T. (2010) A new equitable score suitable for verifying precipitation in numerical weather prediction. *Q.J.R. Meteorol. Soc.*, 136, 1344–1363. https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/qj.656
- Hogan, R.J., Ferro, C.A.T., Jolliffe, I.T., Stephenson, D.B. (2010) Equitability revisited: Why the "equitable threat score" is not equitable. *Wea. Forecasting*, 25, 710–726.
- Ferro, C.A.T. & Stephenson, D.B. (2011) Extremal Dependence Indices: Improved Verification Measures for Deterministic Forecasts of Rare Binary Events. *Wea. Forecasting*, 26(5), 699–713. doi:10.1175/WAF-D-10-05030.1. https://journals.ametsoc.org/view/journals/wefo/26/5/waf-d-10-05030_1.xml
- Gneiting, T. & Ranjan, R. (2011) Comparing density forecasts using threshold- and quantile-weighted scoring rules. *J. Bus. Econ. Stat.*, 29(3), 411–422. (twCRPS)
- Zhang, X. et al. (2011) Indices for monitoring changes in extremes based on daily temperature and precipitation data. *WIREs Clim. Change*, 2, 851–870. (ETCCDI)
- Fortin, V., Abaza, M., Anctil, F., Turcotte, R. (2014) Why should ensemble spread match the RMSE of the ensemble mean? *J. Hydrometeor.*, 15, 1708–1713.
- Lerch, S., Thorarinsdottir, T.L., Ravazzolo, F., Gneiting, T. (2017) Forecaster's dilemma: Extreme events and forecast evaluation. *Stat. Sci.*, 32(1), 106–127. (twCRPS·극값 평가)
- Hobday, A.J. et al. (2018) Categorizing and naming marine heatwaves. *Oceanography*, 31(2), 162–173.
- Haiden, T. et al. (2012) Intercomparison of global model precipitation forecast skill in 2010/11 using the SEEPS score. *Mon. Wea. Rev.*, 140, 2720–2733. https://journals.ametsoc.org/view/journals/mwre/140/8/mwr-d-11-00301.1.xml
- North, R., Trueman, M., Mittermaier, M., Rodwell, M.J. (2013) An assessment of the SEEPS and SEDI metrics for the verification of 6 h forecast precipitation accumulations. *Meteorol. Appl.*, 20, 164–175. https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/met.1405
- Hobday, A.J. et al. (2016) A hierarchical approach to defining marine heatwaves. *Prog. Oceanogr.*, 141, 227–238.

- Gneiting, T. & Raftery, A.E. (2007) Strictly proper scoring rules, prediction, and estimation. *J. Amer. Stat. Assoc.*, 102(477), 359–378. https://www.tandfonline.com/doi/abs/10.1198/016214506000001437

**표준 참고문헌(확인요 — 1차 출처 직접 미열람, 교과서·후속 논문 경유 인용; 단 존재는 표준 문헌으로 널리 인용됨)**
- Heidke, P. (1926); Peirce, C.S. (1884); Gilbert, G.K. (1884)(Finley 토네이도 예보 논쟁에서 CSI·GSS 제안 — Schaefer 1990 경유 확인); Hanssen, A.W. & Kuipers, W.J.A. (1965); Schaefer, J.T. (1990) *Wea. Forecasting*; Gerrity, J.P. (1992) *Mon. Wea. Rev.*, 120; Epstein, E.S. (1969)·Murphy, A.H. (1971) (RPS); Pickands, J. (1975); Davison, A.C. & Smith, R.L. (1990) *JRSS-B*; Ferro, C.A.T. & Fricker, T.E. (2012) (BS 분해 편향보정); Davis et al. (2006) Part II (MODE). — WMO/JCOMM 검증 지침은 기관 표준문서로 표기.
