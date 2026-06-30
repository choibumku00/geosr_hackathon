# 도메인 09 — 수온·염분 (Ocean Temperature / Salinity) 검증·분석 방법 카탈로그

이 문서는 수치모델이 산출한 수온(temperature)·염분(salinity) 결과를 ERA5/GLORYS 등 권위 재분석자료, Argo·관측소·위성(GHRSST 등) 자료와 자동 비교·검증하기 위한 분석·검증 방법을 망라한다. 표층(SST/SSS)부터 수직 프로파일(T/S), 혼합층깊이(MLD), 수괴(water mass), 해양열함량(OHC), 수온전선(front), 단면(section), 등온·등밀도면까지 다룬다. 입력은 NetCDF 격자자료(모델·재분석·위성 L3/L4)와 CSV/텍스트 시계열(Argo·부이·CTD)을 전제로 하며, 각 방법은 "메서드 카드" 형식으로 무엇을 측정하는지·수식·적용 자료형·전제·해석 기준·한계·출처를 정리한다. GLORYS를 기준자료(reference)로 쓸 때의 주의점은 별도 카드로 다룬다.

> **출처 검증 메모(2026-06 갱신)**: 본 문서의 1차 문헌 인용은 웹 검색(WebSearch/WebFetch)으로 서지정보(저자·연도·학술지·DOI)를 재확인했다. 확인된 것은 본문에 DOI를 병기했고, 발행본 확인이 추가로 권장되는 항목만 "(확인요)"로 남겼다. URL은 조사 시점에 접근 가능한 실제 페이지다.

## 한 줄 목차 (Methods Index)

- **공통 오차통계 (Bias / MAE / RMSE / RMSD)** — 모든 변수에 적용하는 1차 오차 지표
- **강건 오차통계 (median bias / MAD / robust RMSE)** — 이상치에 둔감한 보조 오차 지표
- **상관계수·이상상관 (Pearson r / Anomaly Correlation, ACC)** — 패턴·시간 일치도
- **중심화 RMS차·분산비 (centered RMSD / standard deviation ratio)** — Taylor diagram 구성요소
- **Taylor 다이어그램 / Taylor 스킬점수 (Taylor diagram / TSS)** — 상관·진폭·오차 통합 요약
- **Target 다이어그램 (Target diagram)** — bias vs 비편향 RMSD 분해 시각화
- **Willmott 일치도지수 (Index of Agreement, d)** — 무차원 적합도
- **Murphy 스킬점수 (Murphy skill score / MSESS)** — 기준자료 대비 개선도
- **상대 RMSE / 정규화 오차 (Relative RMSE, RRMSE)** — 깊이별·지역별 변동성 정규화 비교
- **GODAE Class-4 관측공간 검증 (Class-4 / observation-space metrics)** — 운영 해양예측 표준 검증틀
- **SST 표층 검증 (SST validation vs GHRSST L4/in situ)** — 표층 수온 격자/부이 대조
- **SSS 표층 염분 검증 (SSS validation vs SMOS/SMAP/Argo)** — 표층 염분 위성·현장 대조
- **수직 프로파일 T/S 검증 (Argo profile match-up)** — 깊이별 모델-Argo 대조
- **수괴 T-S 다이어그램 분석 (T-S diagram / water mass)** — Θ-SA 평면 수괴 식별·비교
- **스파이시니스 (Spiciness / spice on isopycnals)** — 등밀도면 수괴 대비 추적자
- **혼합층깊이 비교 (Mixed Layer Depth, MLD)** — 임계값 기반 MLD 산출·대조
- **등온층깊이·장벽층 (ILD / Barrier Layer Thickness, BLT)** — 온도/밀도 혼합층 차이
- **해양열함량 (Ocean Heat Content, OHC)** — 깊이적분 열량 산출·검증
- **해양염함량 / 담수함량 (Ocean Salt Content / Freshwater Content)** — 염분 깊이적분
- **등온선 깊이·약층깊이 (Isotherm depth D20 / thermocline depth)** — 약층 대리지표
- **수온전선 검출·강도 (SST front detection / gradient)** — Canny·Cayula-Cornillon 등
- **수직 단면 비교 (Vertical section / transect comparison)** — 경도·위도 단면 대조
- **등밀도면 분석 (Isopycnal / potential density surfaces)** — 등밀도면 위 T/S 비교
- **확률밀도·분포 비교 (PDF / Q-Q / Perkins skill score)** — 분포 형태 일치도
- **EOF / 주성분 변동성 비교 (EOF / variance decomposition)** — 시공간 변동 구조 대조
- **스펙트럼·파수 분석 (spectral / wavenumber analysis)** — 중규모 변동 에너지 비교
- **TEOS-10 변수 변환 전제 (TEOS-10 conversion)** — Θ/SA 일관성 보장 전제
- **시공간 정합 / 보간 전제 (collocation / match-up / interpolation)** — 비교 전 정렬 규약
- **GLORYS 기준자료 사용 주의점 (caveats of using GLORYS as reference)** — 동화·심층·연안 한계

---

### 공통 오차통계 — 편차·평균절대오차·평균제곱근오차 (Bias / MAE / RMSE·RMSD)

- **무엇을 측정/검증하나**: 모델값과 기준값(관측·재분석)의 평균적 차이(계통오차)와 분산을 포함한 전체 오차 크기. 수온·염분 전 변수의 1차 진단.
- **정의·수식**:
  - 편차(Bias, mean error): `Bias = (1/N) Σ (mᵢ − oᵢ)`
  - 평균절대오차: `MAE = (1/N) Σ |mᵢ − oᵢ|`
  - 평균제곱근오차: `RMSE = sqrt( (1/N) Σ (mᵢ − oᵢ)² )` (모델-관측 비교 시 RMSD로도 표기)
  - 분해 항등식: `RMSE² = Bias² + RMSD'²` (RMSD'=중심화 RMSD, 아래 카드)
  - 여기서 `mᵢ`는 모델, `oᵢ`는 관측/기준, `N`은 정합된 표본 수.
- **적용 도메인/자료형**: 격자(SST/SSS 맵), 시계열(부이·Argo), 프로파일(깊이별) 모두. 가장 보편적.
- **입력·전제**: 동일 시각·동일 위치(또는 동일 격자로 보간)로 정합(collocation)된 쌍. 단위 일치(℃, PSU/g·kg⁻¹). 결측 마스킹. 격자 비교 시 셀 면적가중 권장.
- **해석 기준**: 작을수록 좋음. SST L4 대비 전구 RMSE 관행적으로 0.3~0.5℃ 수준이면 양호(자료·해역 의존). 염분은 0.1~0.2 PSU 수준. Bias 부호로 과대(+)/과소(−) 추정 판단.
- **한계·주의**: RMSE는 큰 오차에 민감(제곱). MAE는 이상치에 덜 민감. Bias는 부호 상쇄로 0에 가까워도 오차가 클 수 있음 → 반드시 RMSE/MAE와 병행. 표본 수·시공간 대표성에 좌우.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (표준 참고문헌); Jolliffe & Stephenson, *Forecast Verification* (표준 참고문헌); NOAA Global RTOFS Class-1 검증(https://polar.ncep.noaa.gov/global/class-1/).

---

### 강건 오차통계 — median bias / MAD / robust RMSE

- **무엇을 측정/검증하나**: 위성·실시간 관측의 이상치(spike), 구름잔재, 잘못된 정합쌍에 둔감한 오차 요약. 분포가 비대칭이거나 극단값이 섞일 때 평균기반 통계의 보완.
- **정의·수식**:
  - 중앙값 편차: `median(mᵢ − oᵢ)`
  - 중앙절대편차: `MAD = median( |dᵢ − median(d)| )`, `d = m − o`. 정규환산 `σ̂ = 1.4826·MAD`.
  - 강건 RMSE 대용: 잔차의 사분위범위(IQR) 또는 절단(trimmed) RMSE.
- **적용 도메인/자료형**: 위성 SST/SSS match-up, drifter·실시간 Argo 등 품질 불균질 자료. 격자·시계열.
- **입력·전제**: 충분한 표본(중앙값 안정). QC 플래그 적용 후에도 잔존 이상치가 의심될 때.
- **해석 기준**: median bias가 mean bias와 크게 다르면 분포 비대칭/이상치 존재 신호. robust 통계와 평균 통계를 함께 보고하는 것이 GHRSST 관행.
- **한계·주의**: 강건 통계만으로 전체 오차크기를 과소평가할 수 있음 → 평균기반(RMSE)과 병행. 이상치가 "진짜 신호"(전선·중규모)일 수도 있으므로 무비판적 절단 금지.
- **출처**: Wilks (표준 참고문헌, 강건 통계); GHRSST 검증 관행 — robust statistics(median, robust SD) 사용(표준 지침).

---

### 상관계수·이상상관 — Pearson 상관 / Anomaly Correlation Coefficient (ACC)

- **무엇을 측정/검증하나**: 모델과 기준의 변동 패턴(공간/시간)이 얼마나 같은 위상으로 함께 움직이는지. 평균·진폭과 무관한 "형태" 일치도.
- **정의·수식**:
  - Pearson: `r = Σ(mᵢ−m̄)(oᵢ−ō) / sqrt(Σ(mᵢ−m̄)² Σ(oᵢ−ō)²)`
  - ACC: 기후값을 뺀 이상치(anomaly)에 대해 같은 식 적용. `m' = m − c`, `o' = o − c` (c=기후평균).
  - 순위상관(Spearman ρ)은 단조·비선형 관계나 이상치 강건성이 필요할 때 보조.
- **적용 도메인/자료형**: SST/SSS 공간장 패턴 검증, 시계열 위상 검증, OHC·D20 변동 검증.
- **입력·전제**: 정합된 쌍, ACC는 동일 기후값(climatology) 사용. 계절성 제거 시 위상 평가가 명확.
- **해석 기준**: r·ACC 1에 가까울수록 좋음. ACC ≥ 0.6 통상 "유용한" 패턴 일치, ≥ 0.8 우수(분야 관행). 음수는 역위상.
- **한계·주의**: 계통편차·진폭오차에 둔감(상관이 높아도 bias가 클 수 있음). 결정계수 r²로 설명분산 해석. 기후값 정의에 따라 ACC가 달라짐. 공간·시간 자기상관으로 유효자유도가 작아져 유의성 과대평가 주의.
- **출처**: Wilks (표준 참고문헌); Jolliffe & Stephenson, *Forecast Verification* (표준 참고문헌).

---

### 중심화 RMS차·분산비 — centered RMSD / standard deviation ratio

- **무엇을 측정/검증하나**: 평균편차(bias)를 제거한 뒤 남는 변동 패턴 오차(centered RMSD)와 변동 진폭의 비. Taylor diagram의 좌표 구성요소.
- **정의·수식**:
  - 중심화 RMSD: `RMSD' = sqrt( (1/N) Σ [ (mᵢ−m̄) − (oᵢ−ō) ]² )`
  - 분산비: `σ_m / σ_o` (모델 표준편차 / 관측 표준편차)
  - 항등식: `RMSD'² = σ_m² + σ_o² − 2 σ_m σ_o r` (Taylor 2001의 코사인 법칙 관계)
- **적용 도메인/자료형**: 모든 격자/시계열 변수. 다중 모델·다중 변수 비교에 유리.
- **입력·전제**: 정합 쌍, 평균 제거. 전체 RMSE² = Bias² + RMSD'² 관계 활용.
- **해석 기준**: RMSD' 작고 분산비 1에 가까울수록 좋음. 분산비>1은 과대변동, <1은 과소변동.
- **한계·주의**: bias 정보가 빠지므로 단독 사용 금지(전체 RMSE·Bias와 함께 봐야 함).
- **출처**: Taylor (2001) *JGR* "Summarizing multiple aspects of model performance in a single diagram", 106(D7), 7183–7192, doi:10.1029/2000JD900719 (실제 표준 문헌).

---

### Taylor 다이어그램 / Taylor 스킬점수 — Taylor diagram / Taylor Skill Score (TSS)

- **무엇을 측정/검증하나**: 상관(r), 변동 진폭(표준편차비), 중심화 RMSD를 하나의 극좌표 도면에 통합. 여러 모델·재분석을 한 그림에서 순위화.
- **정의·수식**: 방사거리=σ_m/σ_o, 방위각=arccos(r), 점-기준점 거리=정규화 RMSD'. 스킬점수(Taylor 2001 식 4):
  `S = 4(1+r) / [ (σ̂ + 1/σ̂)² (1+r₀) ]`, 여기서 `σ̂ = σ_m/σ_o`(정규화 표준편차), `r₀`=달성가능 최대상관(통상 1). r=1·σ̂=1이면 S=1.
- **적용 도메인/자료형**: SST/SSS 공간장, 프로파일, 시계열. 다중 후보 비교의 표준 시각화.
- **입력·전제**: 정합·표준화된 쌍, 동일 마스크. bias는 별도 표기 필요.
- **해석 기준**: 기준점(REF)에 가까운 점일수록 우수. TSS 1에 근접할수록 좋음.
- **한계·주의**: bias가 도면에 직접 표현되지 않음 → bias 별도 보고(또는 Target diagram 병용). 변수마다 정규화 필요.
- **출처**: Taylor (2001) *JGR* 106(D7), doi:10.1029/2000JD900719 (실제 표준 문헌).

---

### Target 다이어그램 — Target diagram

- **무엇을 측정/검증하나**: 전체 RMSD를 편차(bias)와 비편향 RMSD(unbiased RMSD = 중심화 RMSD)로 분해해 2D 평면에 한 점으로 표시. Taylor diagram이 못 담는 bias 부호·크기를 함께 보여 주는 보완 시각화.
- **정의·수식**: 세로축 = Bias, 가로축 = ±(unbiased RMSD'), 부호는 `sign(σ_m − σ_o)`로 과대/과소변동 구분. 원점으로부터의 거리 = 전체 RMSD(`RMSD² = Bias² + RMSD'²`). 정규화하면 단위 원(관측 표준편차)으로 우열 경계를 표시.
- **적용 도메인/자료형**: 다중 모델·다중 정점·다변수(SST/SSS/OHC) 한눈 비교. 격자·시계열·프로파일.
- **입력·전제**: 정합 쌍, (정규화 시) 관측 표준편차. Taylor diagram과 동일 정합세트 사용 권장.
- **해석 기준**: 원점에 가까울수록 우수. 점이 위/아래면 양/음의 bias, 좌/우면 과소/과대변동. 정규화 반경 1 이내면 "관측 변동보다 작은 오차".
- **한계·주의**: 상관(위상) 정보는 직접 표현 안 됨 → Taylor diagram과 짝으로 사용. 부호 규약(좌우)이 구현마다 다를 수 있어 캡션 명시.
- **출처**: Jolliff, J. K., et al. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment." *J. Marine Systems* 76, 64–82, doi:10.1016/j.jmarsys.2008.05.014 (실제 표준 문헌).

---

### Willmott 일치도지수 — Index of Agreement (d)

- **무엇을 측정/검증하나**: 0~1로 정규화된 모델 적합도. RMSE를 보완해 상대적 일치 정도를 무차원으로 제시.
- **정의·수식**: `d = 1 − [ Σ(mᵢ−oᵢ)² / Σ( |mᵢ−ō| + |oᵢ−ō| )² ]`. 1이면 완전일치, 0이면 무일치. 수정형(d1, refined d_r)도 존재.
- **적용 도메인/자료형**: 시계열(부이·Argo)·격자 검증. 수온·염분 시계열 적합도 보고에 자주 사용.
- **입력·전제**: 정합 쌍, 관측 평균 ō 사용.
- **해석 기준**: d 높을수록 좋음(통상 >0.7 양호). 가법·승법 차이 모두 감지.
- **한계·주의**: 제곱항 때문에 극단값에 과민. r과 마찬가지로 단독 판단 위험 → RMSE/Bias 병행.
- **출처**: Willmott (1981) "On the validation of models." *Physical Geography* 2(2), 184–194 (실제 표준 문헌); 수정형 Willmott, Robeson & Matsuura (2012) *Int. J. Climatol.* 32, 2088–2094, doi:10.1002/joc.2419.

---

### Murphy 스킬점수 — Murphy Skill Score / MSE Skill Score (MSESS)

- **무엇을 측정/검증하나**: 기준예보(기후값·지속성·재분석)를 기준으로 모델이 얼마나 개선되었는지의 상대 스킬.
- **정의·수식**: `SS = 1 − MSE_model / MSE_ref`. 1=완벽, 0=기준과 동일, <0=기준보다 나쁨. Murphy(1988)는 MSE 스킬을 상관·조건편향(slope reliability)·무조건편향(평균오차)으로 분해.
- **적용 도메인/자료형**: SST/OHC/D20 예측·재현 평가. 재분석을 기준으로 한 상대 평가에 적합.
- **입력·전제**: 신뢰할 기준(reference) 정의 필수(기후값·persistence·GLORYS 등). 정합 쌍.
- **해석 기준**: SS>0이면 기준보다 우수. 분해항으로 오차 원인(위상 vs 진폭 vs 평균) 진단.
- **한계·주의**: 기준 선택에 따라 점수가 크게 달라짐(기준 명시 필수). 기준자료 자체 오차에 영향.
- **출처**: Murphy (1988) "Skill scores based on the mean square error and their relationships to the correlation coefficient." *Mon. Wea. Rev.* 116, 2417–2424 (실제 표준 문헌).

---

### 상대 RMSE / 정규화 오차 — Relative RMSE (RRMSE)

- **무엇을 측정/검증하나**: 깊이별·지역별로 자연 변동성이 다를 때, RMSE를 해당 변동성으로 정규화하여 공정 비교.
- **정의·수식**: `RRMSE(z) = RMSE(z) / σ_obs(z)` (각 깊이 z에서 관측 표준편차로 정규화). 또는 평균값으로 나눈 백분율 RMSE.
- **적용 도메인/자료형**: Argo 프로파일 깊이별 검증, 단면 검증. 표층-심층 오차를 동일 척도로 비교.
- **입력·전제**: 깊이별 관측 표준편차 추정 필요(충분한 표본). 정합 쌍.
- **해석 기준**: 1 미만이면 오차가 자연 변동보다 작음(양호). 깊이별 곡선으로 약층 부근 취약점 식별.
- **한계·주의**: σ_obs가 작은 심층에서 RRMSE가 과대평가될 수 있음. 표본 부족 시 불안정.
- **출처**: 재분석 평가 관행 — de Souza et al. (2020) 4개 전구 재분석 평가, *NZ J. Mar. Freshwater Res.* (https://www.tandfonline.com/doi/full/10.1080/00288330.2020.1713179); GLORYS12 품질평가(Lellouche et al. 2021).

---

### GODAE Class-4 관측공간 검증 — Class-4 / observation-space metrics

- **무엇을 측정/검증하나**: 모델·재분석을 "관측 위치·시각"으로 보간한 뒤 그 관측공간(observation space)에서 SST·해수면이상(SLA)·수직 수온·수직 염분을 일관 규약으로 검증하는 운영 해양예측 표준 프레임워크. 여러 시스템(우리 모델 vs GLORYS 등)을 공통 관측집합으로 공정 비교.
- **정의·수식**: 각 관측 i에 대해 모델 등가값 `H(m)ᵢ`(관측연산자=시공간 보간)를 만들고 잔차 `H(m)ᵢ − oᵢ`로 Bias/RMSE/상관 등 산출. persistence·기후값을 기준으로 Murphy식 스킬도 함께. 리드타임별(분석·예보 day1..N)로 누적.
- **적용 도메인/자료형**: 모델 3D 격자(NetCDF) vs Argo 프로파일(CSV/NetCDF), 부이·드리프터 SST, 고도계 SLA. "격자 모델 ↔ 점 관측" 정합에 그대로 대응.
- **입력·전제**: 공통 관측집합·공통 QC. 동일 관측연산자(보간)·동일 정합 윈도우. 깊이/압력·시간기준(UTC) 통일.
- **해석 기준**: 같은 관측집합 위에서 시스템 간 RMSE/Bias 순위 비교가 핵심. 리드타임 증가에 따른 스킬 감소 곡선, persistence 대비 우위 여부.
- **한계·주의**: 동화된 관측을 검증에 재사용하면 낙관 편향(독립성 부족) → 가능하면 비동화/독립 관측. 관측연산자 정의가 결과 좌우. 관측 자체 오차·대표성오차 포함됨.
- **출처**: Ryan, A. G., et al. (2015) "GODAE OceanView Class 4 forecast verification framework: global ocean inter-comparison." *J. Operational Oceanography* 8(sup1), S98–S111, doi:10.1080/1755876X.2015.1022330 (실제 표준 문헌); 개념 기반 Murphy (1993) *Wea. Forecasting* — consistency/quality/value.

---

### SST 표층 검증 — Sea Surface Temperature validation (vs GHRSST L4 / in situ)

- **무엇을 측정/검증하나**: 모델·재분석 SST를 위성기반 분석장(GHRSST L4: OSTIA, MUR, CMC 등)·현장(부이, 선박, drifters)과 비교.
- **정의·수식**: 위 공통 통계(Bias/RMSE/r/ACC)를 SST에 적용. 위성 비교 시 깊이 정의 차이(skin/subskin vs foundation/bulk) 보정 고려.
- **적용 도메인/자료형**: 격자 L3/L4 위성 SST(NetCDF), 부이 시계열(CSV). 모델장을 관측격자로 보간 후 비교.
- **입력·전제**: 시공간 정합(일평균·동일 격자). skin-bulk 차이(주간 가열·풍속) 인지. 구름·결측 마스크.
- **해석 기준**: 전구 L4 대비 RMSE 0.3~0.5℃, drifter 대비 0.4~0.6℃ 수준 관행. Bias |0.2℃| 이내 양호.
- **한계·주의**: 위성 L4는 그 자체가 분석·보간 산물(독립관측 아님) → 이중계산 주의. 연안·해빙역·고위도 정확도 저하. 일변동(diurnal) 신호 처리 필요.
- **출처**: GHRSST/WMO-IOC JCOMM 검증 관행(표준 지침); NOAA RTOFS Class-1 위성검증(https://polar.ncep.noaa.gov/global/class-1/); UCAR Climate Data Guide.

---

### SSS 표층 염분 검증 — Sea Surface Salinity validation (vs SMOS/SMAP/Aquarius/Argo)

- **무엇을 측정/검증하나**: 모델·재분석 SSS를 위성 염분(SMOS, SMAP, Aquarius)·Argo 표층값과 비교.
- **정의·수식**: 공통 통계(Bias/RMSE/r)를 SSS에 적용. 위성 SSS는 ~1cm skin 염분, Argo는 ~5–10m → 깊이·시공간 평균 차이 고려.
- **적용 도메인/자료형**: 위성 L3/L4 격자(NetCDF), Argo 표층(CSV). 모델을 위성격자에 정합.
- **입력·전제**: 위성 SSS 잡음 큼(연안·저온·강수역 RFI/한랭 편향) → QC·평활 필요. Argo 검증세트 활용.
- **해석 기준**: 외양 RMSE 0.2 PSU 내외 양호. 연안·고위도는 위성 신뢰도 낮아 Argo 우선.
- **한계·주의**: 위성 염분은 SST<5℃, 강수·육지 근접에서 큰 오차. 위성 자체가 검증 대상이기도 함 → 현장(Argo) 우선.
- **출처**: NASA GSFC — Aquarius+Argo SSS 검증세트(약 50만 정합, 2011–2015; https://earth.gsfc.nasa.gov/cryo/data/sea-surface-salinity); UCAR Climate Data Guide — Salinity(https://climatedataguide.ucar.edu/variables/ocean/salinity).

---

### 수직 프로파일 T/S 검증 — Argo profile match-up

- **무엇을 측정/검증하나**: 모델·재분석의 깊이별 수온·염분을 Argo(또는 CTD/glider) 프로파일과 1:1 정합 비교.
- **정의·수식**: 각 표준깊이(또는 보간 깊이)에서 `Bias(z), RMSE(z), r(z), RRMSE(z)` 산출. 프로파일 평균·깊이적분 진단 병행.
- **적용 도메인/자료형**: 모델 3D 격자(NetCDF) vs Argo 프로파일(CSV/NetCDF). 시공간 윈도우 내 가장 가까운 프로파일 정합.
- **입력·전제**: 동일 깊이좌표로 보간(선형/스플라인). Argo QC 플래그(실시간 vs 지연모드) 적용. 시공간 정합 반경 설정(예 ±1일, ±0.25°).
- **해석 기준**: 깊이별 Bias/RMSE 곡선으로 약층(thermocline/halocline) 부근 오차 집중 여부 평가. 표층보다 약층에서 오차 큼이 일반적.
- **한계·주의**: Argo는 2000m까지·10일 주기 → 심층·중규모·연안 미해상. 압력→깊이 변환, 실시간 자료 QC 한계. 정합 윈도우 선택이 결과 좌우.
- **출처**: Argo 프로그램·UCAR Climate Data Guide — Argo(https://climatedataguide.ucar.edu/climate-data/argo-ocean-temperature-and-salinity-profiles); GLORYS12 품질평가(Lellouche et al. 2021, https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.698876/full).

---

### 수괴 T-S 다이어그램 분석 — T-S diagram / water mass analysis

- **무엇을 측정/검증하나**: 수온-염분 평면(또는 Θ-SA 평면)에서 수괴(water mass)의 위치·혼합선·핵심값을 모델과 관측 사이에서 비교. 수괴 표현 충실도.
- **정의·수식**: 가로축 염분(SP 또는 SA), 세로축 온도(θ 또는 Θ). 등밀도선(isopycnal σθ 또는 σ0)을 배경에 중첩. 수괴 핵: 특정 (T,S,σ) 극점. 혼합은 두 수괴 간 직선.
- **적용 도메인/자료형**: 프로파일(Argo/CTD)·모델 3D 격자에서 추출한 (T,S) 산점. TEOS-10 권장(Θ-SA).
- **입력·전제**: TEOS-10 변환(아래 카드) 권장. 동일 깊이·동일 영역에서 추출. 충분한 프로파일 표본.
- **해석 기준**: 관측 수괴 구름과 모델 구름의 중첩·핵심값 일치 여부. 등밀도선 대비 수괴 위치 보존(밀도 보존) 점검. 모델이 과도하게 혼합(diffusive)되면 구름이 좁아짐.
- **한계·주의**: 수치확산·동화로 수괴 극값이 평활화될 수 있음. EOS-80(θ-SP) vs TEOS-10(Θ-SA) 혼용 금지. 깊이 정보가 사라지므로 단면·프로파일과 병행 해석.
- **출처**: IOC/SCOR/IAPSO (2010) TEOS-10 Manual & Primer(https://www.teos-10.org/pubs/TEOS-10_Primer.pdf); Nature Scitable "Key Physical Variables in the Ocean"(https://www.nature.com/scitable/knowledge/library/key-physical-variables-in-the-ocean-temperature-102805293/).

---

### 스파이시니스 — Spiciness / spice on isopycnals

- **무엇을 측정/검증하나**: 등밀도면(isopycnal) 위에서 밀도에 거의 영향을 주지 않으면서 따뜻+짠 vs 차갑+싱거운 수괴 대비를 나타내는 추적자(spice/spiciness). 등밀도면 수괴 변동·이류를 밀도와 분리해 검증.
- **정의·수식**: T-S 평면에서 등밀도선에 (이상적으로) 직교하는 상태변수 `π(Θ, SA)`. 큰 값=따뜻·짠 물. GSW(TEOS-10) `gsw_spiciness0/1/2`(기준압 0/1000/2000 dbar)로 계산. 등밀도면 위 `π`의 모델-관측 차로 평가.
- **적용 도메인/자료형**: Argo/CTD 프로파일·모델 3D 격자를 등밀도좌표로 변환 후 비교. 등밀도면 분석 카드와 짝.
- **입력·전제**: TEOS-10 변수(Θ, SA)·일관된 기준압. 깊이→밀도 좌표 보간. 충분한 성층(약한 성층에서 무의미).
- **해석 기준**: 등밀도면 위 spice의 분포·전선·이상치 위상 일치. 수치확산으로 모델 spice 대비가 약해지면 isopycnal mixing 과다 신호.
- **한계·주의**: "직교성"의 물리적 의미는 제한적(McDougall & Krzysik 2015) → 정의·기준압을 명시. 약한 성층·밀도역전 구간에서 부적절. 정의(Flament vs McDougall) 혼용 금지.
- **출처**: Flament (2002) "A state variable for characterizing water masses and their diffusive stability: spiciness." *Progress in Oceanography* 54, 493–501, doi:10.1016/S0079-6611(02)00065-4 (실제 표준 문헌); McDougall & Krzysik (2015) "Spiciness." *J. Marine Research* 73(5), 141–152 (실제 표준 문헌); McDougall & Barker (2021) *JGR-Oceans*, doi:10.1029/2019JC015936.

---

### 혼합층깊이 비교 — Mixed Layer Depth (MLD)

- **무엇을 측정/검증하나**: 표층 혼합층의 깊이를 모델과 관측(Argo)에서 동일 기준으로 산출해 비교. 표층 열·물질 저장량·대기-해양 결합과 직결.
- **정의·수식**: 임계값(threshold) 방법이 표준.
  - 온도 기준: 표층(예 10m) 대비 `ΔT = 0.2℃` 변하는 깊이(de Boyer Montégut et al. 2004 권장).
  - 밀도 기준: `Δσθ = 0.03 kg·m⁻³` 변하는 깊이.
  - 기울기(gradient) 방법, 곡률(curvature) 방법, 하이브리드(Holte & Talley 2009) 등 대안 존재.
- **적용 도메인/자료형**: 모델 3D 격자·Argo 프로파일. 동일 임계값·동일 기준깊이로 산출해야 공정.
- **입력·전제**: 충분한 수직 해상도. 동일 임계값·동일 참조깊이. 밀도 사용 시 TEOS-10 일관성.
- **해석 기준**: MLD Bias/RMSE(m)로 평가. 겨울 깊은 혼합·여름 얕은 혼합의 계절성 재현 점검. 지역별 최적 임계값 차이 인지.
- **한계·주의**: 임계값·기준깊이 선택에 민감(방법 불일치 시 비교 무효). Argo 10일 주기로 아계절(<90일) MLD 변동 과소해상. 약한 성층·장벽층에서 온도-밀도 MLD 괴리.
- **출처**: de Boyer Montégut, C., et al. (2004) "Mixed layer depth over the global ocean: An examination of profile data and a profile-based climatology." *J. Geophys. Res.* 109, C12003, doi:10.1029/2004JC002378 (실제 표준 문헌); Holte, J., & Talley, L. (2009) "A new algorithm for finding mixed layer depths..." *J. Atmos. Oceanic Technol.* 26(9), 1920–1939, doi:10.1175/2009JTECHO543.1 (실제 표준 문헌); Holte et al. (2017) Argo MLD climatology, *GRL*, doi:10.1002/2017GL073426.

---

### 등온층깊이·장벽층 — Isothermal Layer Depth (ILD) / Barrier Layer Thickness (BLT)

- **무엇을 측정/검증하나**: 온도 기준 혼합층(ILD)과 밀도 기준 혼합층(MLD)의 차이로 정의되는 장벽층(barrier layer) 재현. 열대·강수역 표층 열수지에 중요.
- **정의·수식**: `ILD` = 온도 임계(ΔT) 깊이, `MLD_ρ` = 밀도 임계 깊이, `BLT = ILD − MLD_ρ`. BLT>0이면 염분성층이 혼합을 억제.
- **적용 도메인/자료형**: 모델·Argo 프로파일(T와 S 동시 필요).
- **입력·전제**: 온도·염분 동시 관측, 일관된 임계값, TEOS-10 밀도.
- **해석 기준**: BLT 분포·계절성의 모델-관측 일치. 열대 서태평양·벵골만 등에서 BLT 존재 재현 여부.
- **한계·주의**: 임계값 정의에 민감. 염분 자료 품질에 좌우(BLT는 염분성층 신호). 얕은 BLT는 수직해상도 한계로 검출 어려움.
- **출처**: de Boyer Montégut, C., et al. (2007) "Control of salinity on the mixed layer depth in the world ocean: 1. General description." *J. Geophys. Res.* 112, C06011, doi:10.1029/2006JC003953 (실제 표준 문헌, BLT 전구 기후값); Argo 기반 상층 과정 연구(예: Banda Sea, https://geoscienceletters.springeropen.com/articles/10.1186/s40562-023-00266-x).

---

### 해양열함량 — Ocean Heat Content (OHC)

- **무엇을 측정/검증하나**: 일정 깊이층(0–300/0–700/0–2000m 등)의 열저장량을 모델과 관측·재분석에서 산출·비교. 기후 추세·에너지 불균형 진단의 핵심.
- **정의·수식**: `OHC = ∫(z1→z2) ρ · cp · Θ dz` (절대값) 또는 이상치 `OHCA = ∫ ρ0 · cp · (T − T_clim) dz`. 관행 상수: `ρ0 ≈ 1026~1030 kg·m⁻³`, `cp ≈ 3985~3996 J·kg⁻¹·℃⁻¹`. 단위 J·m⁻² (단면적당).
- **적용 도메인/자료형**: 모델 3D 격자·재분석·관측기반 격자(NCEI/IAP 등). 깊이적분 후 면적평균.
- **입력·전제**: 동일 깊이층·동일 기후값·동일 상수. Θ(보존수온) 사용 권장(TEOS-10). 결측 깊이 처리 규약.
- **해석 기준**: OHC 시계열의 추세·연변동을 관측기반(NCEI, IAP, Copernicus OMI)과 비교. RMSE·추세차·상관으로 평가.
- **한계·주의**: 깊이 적분 상하한·상수·기후값 정의에 따라 값이 달라짐(반드시 규약 명시). 심층(>2000m) 관측 부족으로 모델 제약 약함. 면적평균 가중(셀 면적) 필요.
- **출처**: von Schuckmann, K., et al. (2019) "Measuring Global Ocean Heat Content to Estimate the Earth Energy Imbalance." *Front. Mar. Sci.* 6:432(https://www.frontiersin.org/articles/10.3389/fmars.2019.00432/full); NOAA NCEI Global OHC(https://www.ncei.noaa.gov/access/global-ocean-heat-content/); Copernicus Marine OMI OHC 제품(https://data.marine.copernicus.eu/product/GLOBAL_OMI_OHC_area_averaged_anomalies_0_300/description).

---

### 해양염함량 / 담수함량 — Ocean Salt Content / Freshwater Content

- **무엇을 측정/검증하나**: 일정 깊이층 염분의 적분량(염함량) 또는 기준염분 대비 담수함량(FWC)을 비교. 담수 수지·성층 변화 진단.
- **정의·수식**: 담수함량 `FWC = ∫(z1→z2) (S_ref − S)/S_ref dz` (S_ref=기준염분, 예 34.8). 염함량은 `∫ ρ·S dz`.
- **적용 도메인/자료형**: 모델·재분석·Argo 격자. 극지(보퍼트 환류 등) 담수 분석에 흔함.
- **입력·전제**: 기준염분 명시, 동일 깊이층, TEOS-10 일관(SA vs SP 혼용 금지).
- **해석 기준**: FWC 분포·추세의 관측 일치. 담수 축적/방출 위상 재현.
- **한계·주의**: 기준염분 선택에 민감. 위성·연안 염분 신뢰도 낮음. 깊이층 정의 명시 필수.
- **출처**: UCAR Climate Data Guide — Salinity(https://climatedataguide.ucar.edu/variables/ocean/salinity); TEOS-10 Manual(https://www.teos-10.org/).

---

### 등온선 깊이·약층깊이 — Isotherm depth (D20) / thermocline depth

- **무엇을 측정/검증하나**: 특정 등온선(주로 20℃, D20)의 깊이 또는 약층(thermocline) 깊이를 모델-관측에서 비교. 열대 약층·ENSO 변동의 대리지표.
- **정의·수식**: `D20` = 수직 프로파일에서 T=20℃가 되는 깊이(보간). 약층깊이는 최대 수온기울기(`max |∂T/∂z|`) 깊이 또는 임계 기울기 기준.
- **적용 도메인/자료형**: 모델 3D 격자·Argo·XBT·재분석(SODA 등). 등온선 깊이 맵·단면.
- **입력·전제**: 충분한 수직 해상도, 일관된 보간법. 열대에서 D20이 약층 대리로 유효.
- **해석 기준**: D20 Bias(m)·RMSE·상관. 약층 깊이 편차(예 10–20m 깊음/얕음) 평가. 위상(서향 전파 등) 재현.
- **한계·주의**: 고위도·약한 약층에서는 D20이 약층 대리로 부적절. 등온선이 여러 깊이에서 교차할 수 있음(이중 약층). 보간 민감.
- **출처**: TAO/TRITON·NOAA PMEL 열대해양 관측·D20 진단(https://www.pmel.noaa.gov/tao/); IRI/LDEO ENSO Thermocline(D20) maproom(https://iridl.ldeo.columbia.edu/maproom/ENSO/Thermocline/Std_Anom_Depth.html).

---

### 수온전선 검출·강도 — SST front detection / gradient

- **무엇을 측정/검증하나**: 수온전선(thermal front)의 위치·빈도·강도(gradient)를 모델과 위성 SST에서 검출·비교. 중규모·연안용승·해류경계 재현.
- **정의·수식**:
  - 기울기법: `|∇SST| = sqrt( (∂T/∂x)² + (∂T/∂y)² )`, 임계 초과 화소를 전선으로.
  - Canny 에지검출: 평활→기울기→비최대억제→이중임계 추적.
  - 히스토그램법(Cayula–Cornillon SIED): 창(window) 내 이중봉 히스토그램으로 전선 분리.
  - 전선빈도(frontal frequency): 일정 기간 전선 검출 비율.
- **적용 도메인/자료형**: 위성/모델 SST 격자(NetCDF). 전선확률맵·강도맵 생성 후 비교.
- **입력·전제**: 동일 해상도·동일 평활화. 구름결측 처리. 임계값·창 크기 일치.
- **해석 기준**: 전선 위치·빈도·강도의 공간 일치(POD/FAR/CSI 등 사건검증 가능). Canny는 과소검출, Laplacian은 과대검출 경향.
- **한계·주의**: 검출 알고리즘·임계값·해상도에 결과 민감(반드시 동일 설정). 모델 평활화로 전선 약화. 구름·잡음이 위성 전선 왜곡.
- **출처**: Cayula, J.-F., & Cornillon, P. (1992) "Edge detection algorithm for SST images." *J. Atmos. Oceanic Technol.* 9(1), 67–80, doi:10.1175/1520-0426(1992)009<0067:EDAFSI>2.0.CO;2 (SIED — 실제 표준 문헌); Canny, J. (1986) "A computational approach to edge detection." *IEEE TPAMI* 8(6), 679–698 (실제 표준 문헌); 전선 알고리즘 비교(Deep-Sea Research II, https://www.sciencedirect.com/science/article/abs/pii/S0967064513004475).

---

### 수직 단면 비교 — Vertical section / transect comparison

- **무엇을 측정/검증하나**: 특정 경도·위도 단면(또는 관측 라인, 예 59.5°N, 6°N)을 따라 깊이-거리 평면의 T/S 구조를 모델-관측 비교.
- **정의·수식**: 단면 위 각 (거리, 깊이) 격자에서 Bias/RMSE 맵, 등온·등염·등밀도선 위치 비교. 단면평균 통계.
- **적용 도메인/자료형**: 모델 3D 격자에서 단면 추출·CTD/XBT/glider 라인·반복관측선.
- **입력·전제**: 동일 단면 경로로 보간, 동일 깊이좌표. 반복관측(repeat hydrography) 자료 정합.
- **해석 기준**: 약층·전선·수괴 경계의 깊이·기울기 재현. 단면 RMSE 분포로 취약 깊이/위치 식별.
- **한계·주의**: 단면 위치·시점 정합 오차(중규모 위치 어긋남)로 큰 국소오차 발생 가능. 단일 단면은 대표성 한계.
- **출처**: Verezemskaya, P., et al. (2021) GLORYS12 59.5°N 단면 평가 *J. Geophys. Res. Oceans* 126, doi:10.1029/2020JC016317 (https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JC016317); 반복관측(GO-SHIP) 관행(http://www.go-ship.org/).

---

### 등밀도면 분석 — Isopycnal / potential density surface comparison

- **무엇을 측정/검증하나**: 등밀도면(특정 σθ/σ0/중립밀도 면) 위에서 T/S·면 깊이를 모델-관측 비교. 수괴 이류·혼합을 밀도좌표에서 진단.
- **정의·수식**: 잠재밀도 `σθ = ρ(θ,S,p=0) − 1000`. 등밀도면 위 변수(예 S on σθ=27.0)·면 깊이(depth of isopycnal) 비교. 두께 = 등밀도면 간 거리. 등밀도면 위 스파이시니스(spice, 별도 카드)도 함께.
- **적용 도메인/자료형**: 모델·재분석·Argo 격자. 등밀도좌표(isopycnal) 변환 후 비교.
- **입력·전제**: TEOS-10 밀도 일관. 깊이→밀도 좌표 보간. 동일 기준압.
- **해석 기준**: 등밀도면 깊이·면상 염분(spiciness 포함) 일치. 수치확산에 의한 등밀도면 평활 점검.
- **한계·주의**: 약한 성층·밀도역전 구간에서 등밀도좌표 모호. 좌표변환 보간오차. 기준압 선택(σ0 vs σ2)에 따라 결과 상이.
- **출처**: IOC/SCOR/IAPSO (2010) TEOS-10 Manual/Primer(https://www.teos-10.org/pubs/TEOS-10_Primer.pdf); 등밀도 분석 일반론(Nature Scitable, https://www.nature.com/scitable/knowledge/library/key-physical-variables-in-the-ocean-temperature-102805293/).

---

### 확률밀도·분포 비교 — PDF / Q-Q plot / Perkins Skill Score

- **무엇을 측정/검증하나**: 평균·분산을 넘어 값의 분포(확률밀도) 형태가 모델-관측 사이에서 일치하는지. 극값·왜도 재현.
- **정의·수식**: Perkins skill score `PSS = Σ min(Z_m, Z_o)` (정규화 히스토그램 겹침 면적, 0~1). Q-Q plot은 분위수 대 분위수 산점. Kolmogorov–Smirnov(KS) 통계량으로 분포차 검정.
- **적용 도메인/자료형**: SST/SSS/프로파일 값 분포, OHC 등. 격자·시계열.
- **입력·전제**: 동일 구간(bin)·동일 표본 영역. 충분한 표본.
- **해석 기준**: PSS 1에 가까울수록 분포 일치. Q-Q가 대각선에 근접하면 일치. 꼬리(극값) 어긋남 진단.
- **한계·주의**: bin 크기 의존. 공간·시간 상관 무시(독립 가정). 평균 일치해도 분포가 다를 수 있음.
- **출처**: Perkins, S. E., et al. (2007) "Evaluation of the AR4 climate models' simulated daily maximum temperature, minimum temperature, and precipitation over Australia using probability density functions." *J. Climate* 20(17), 4356–4376, doi:10.1175/JCLI4253.1 (실제 표준 문헌); Wilks(표준 참고문헌) — Q-Q/KS.

---

### EOF / 주성분 변동성 비교 — EOF / variance decomposition

- **무엇을 측정/검증하나**: SST/SSS/OHC·D20 장의 주요 시공간 변동모드(EOF)와 설명분산을 모델-관측 사이에서 비교. 변동 구조의 충실도.
- **정의·수식**: 이상치 공분산행렬의 고유분해 → 공간패턴(EOF)·시간계수(PC)·설명분산비. 모드별 공간상관·PC 상관으로 비교.
- **적용 도메인/자료형**: 시간 차원이 있는 격자장(NetCDF 시계열).
- **입력·전제**: 동일 영역·기간·기후값 제거·면적가중. 충분한 시간표본.
- **해석 기준**: 주요 모드의 공간패턴·설명분산·PC 위상 일치. ENSO 등 알려진 모드 재현.
- **한계·주의**: 모드 순서 뒤바뀜·부호 모호·모드 혼합(degeneracy, North et al. 1982 기준). 영역·기간 선택에 민감. 직교성은 물리모드 보장 아님.
- **출처**: Wilks(표준 참고문헌) — PCA/EOF; North, G. R., et al. (1982) "Sampling errors in the estimation of empirical orthogonal functions." *Mon. Wea. Rev.* 110, 699–706 (모드 분리성 기준 — 실제 표준 문헌).

---

### 스펙트럼·파수 분석 — spectral / wavenumber analysis

- **무엇을 측정/검증하나**: SST·SSH·OHC 등의 파수/주파수 스펙트럼을 비교해 중규모(mesoscale) 에너지·기울기 재현 점검. 모델 유효해상도 평가.
- **정의·수식**: 1D/2D 파워스펙트럼밀도 `PSD(k)`. 관측(위성)과 모델의 스펙트럼 기울기·등에너지 파수 비교.
- **적용 도메인/자료형**: 고해상 격자(NetCDF). 트랙·맵 기반.
- **입력·전제**: 동일 해상도·디트렌드·윈도잉. 결측 처리.
- **해석 기준**: 중규모 대역 스펙트럼 일치 여부, 모델 에너지 부족(과확산) 진단.
- **한계·주의**: 동화·평활로 모델 중규모 에너지 과소. 위성 잡음 floor가 고파수 왜곡. 윈도/디트렌드 선택 민감.
- **출처**: Wilks(표준 참고문헌) — 스펙트럼 분석; 운영 재분석 중규모 평가 사례(예: GLONET 평가, arXiv 2412.05454, https://arxiv.org/pdf/2412.05454 — 사례, 동료심사 여부 확인요).

---

### TEOS-10 변수 변환 전제 — TEOS-10 conversion (Θ / SA)

- **무엇을 측정/검증하나**: 방법이 아니라 모든 T/S 검증의 전제. 보존수온(Θ)·절대염분(SA) 등 변수 정의를 모델·관측 사이에서 일치시킨다.
- **정의·수식**: 실용염분 SP→절대염분 SA(경도·위도·압력 보정), 현장온도 t·잠재온도 θ→보존수온 Θ. GSW(Gibbs SeaWater) 툴박스로 변환.
- **적용 도메인/자료형**: 모든 프로파일·격자 비교, T-S/등밀도/spice/OHC 분석.
- **입력·전제**: 입력 변수 종류(현장/잠재/보존 온도, 실용/절대 염분, 압력 vs 깊이) 명확화. 압력·위경도 메타 필요.
- **해석 기준**: 동일 변수 정의로 비교했을 때만 통계가 의미. EOS-80↔TEOS-10 혼용 금지.
- **한계·주의**: 변환 누락 시 수괴·밀도·OHC에 계통오차 유입. 깊이↔압력 변환 필요. SA 보정은 지역적 조성 변동 반영.
- **출처**: IOC, SCOR & IAPSO (2010) *The International Thermodynamic Equation of Seawater — 2010 (TEOS-10): Manual* 및 Primer(https://www.teos-10.org/pubs/TEOS-10_Primer.pdf); TEOS-10 Excel 구현, *Ocean Science* 18, 627 (2022, https://os.copernicus.org/articles/18/627/2022/).

---

### 시공간 정합 / 보간 전제 — collocation / match-up / interpolation

- **무엇을 측정/검증하나**: 방법이 아니라 전제. 모델과 관측을 동일 시각·위치·깊이로 정렬하는 규약. 통계 신뢰도의 토대.
- **정의·수식**: 정합 윈도우(Δt, Δx, Δz) 정의, 모델→관측격자 보간(nearest/bilinear/선형 in z) 또는 관측→모델격자 평균. L4-모델 비교 시 시간평균 일치.
- **적용 도메인/자료형**: 전 변수·전 자료형. 위성 L3/L4, Argo, 부이, CTD.
- **입력·전제**: 좌표계·시간기준(UTC)·깊이/압력 정의 통일. 결측·QC 마스크. 면적가중.
- **해석 기준**: 정합 표본 수·대표성 보고. 윈도우 변경에 대한 민감도 점검.
- **한계·주의**: 정합 윈도우가 크면 대표성 오차, 작으면 표본 부족. 보간 자체가 오차원. skin/bulk·1cm/5–10m 깊이 차이.
- **출처**: GHRSST/WMO-IOC JCOMM match-up 관행(표준 지침); NOAA RTOFS Class-1(https://polar.ncep.noaa.gov/global/class-1/); GODAE Class-4 관측연산자 규약(Ryan et al. 2015, 위 카드).

---

### GLORYS 기준자료 사용 주의점 — caveats of using GLORYS as reference

- **무엇을 측정/검증하나**: 방법이 아니라 GLORYS(특히 GLORYS12V1, 1/12°, NEMO3.6 + 축소차수 Kalman/SEEK + 3D-VAR 편향보정)를 "기준자료"로 쓸 때 유의할 한계.
- **정의·수식 / 핵심 특성**: along-track 고도계 SLA, 위성 SST, 해빙농도, 현장 T/S 프로파일을 동화. 3D-VAR로 대규모 저속 편향 보정.
- **적용 도메인/자료형**: 기준 재분석 격자(NetCDF)와 모델 비교 시 전반.
- **주의점(핵심)**:
  - **재분석은 독립관측이 아님**: GLORYS는 위성·Argo를 동화한 산물 → 같은 관측을 동화한 모델과 비교하면 오차가 과소평가(이중계산). 가능하면 독립 현장관측(미동화 CTD/계류부이)으로 교차검증.
  - **관측망 의존성**: 성능이 시점별 관측 밀도에 의존. Argo 이전(2000년대 이전) 심층 제약 약함.
  - **심층(>2000m) 미제약**: Argo 미도달 심층은 모델 편향 잔존(예 overflow water 0.5–1℃ 따뜻·짠 편향 보고).
  - **상층 잔차 편향**: (미동화 실험 기준) 상부 온난·중층 한랭 편향 경향이 보고됨(해역·기간 의존).
  - **중규모 위치 어긋남**: 고도계 동화에도 중규모 구조 위치·진폭 소차 존재(고기울기역에서 두드러짐).
  - **연안·천해·고위도**: 해상도·동화 한계로 정확도 저하. 조석·연안과정 부족.
- **해석 기준**: GLORYS와의 차이가 "모델 오차"인지 "GLORYS 한계"인지 구분. 차이의 부호·해역·깊이를 위 알려진 편향과 대조.
- **한계·주의**: 버전(GLORYS12V1, GLORYS2V4 등)·기간별 특성 상이. 표층 동화 변수(SST/SLA)에 강하고 비동화 변수·심층에 약함. 위 정량 편향 수치는 평가논문 의존이므로 사용 버전·해역에 맞게 재확인.
- **출처**: Lellouche, J.-M., et al. (2021) "The Copernicus Global 1/12° Oceanic and Sea Ice GLORYS12 Reanalysis." *Front. Earth Sci.* 9:698876, doi:10.3389/feart.2021.698876 (https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.698876/full); Verezemskaya, P., et al. (2021) 59.5°N 단면 평가 *JGR-Oceans* 126, doi:10.1029/2020JC016317.

---

## 출처(References)

> 표기 규칙: "실제 표준 문헌"은 학계에서 널리 인용되는 확립된 1차 문헌이며 본 갱신에서 서지정보(저자·연도·학술지·DOI)를 웹으로 재확인했다. "(표준 참고문헌)"은 교과서·표준지침으로 판본·쪽수는 사용본에 맞춰 표기. "(확인요)"는 발행본·동료심사 여부의 추가 확인을 권장하는 항목. URL은 조사 시 확인한 실제 페이지.

**표준 교과서·검증 지침**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences.* Academic Press. (오차통계·강건통계·PCA/EOF·Q-Q·KS·스펙트럼 — 표준 참고문헌)
- Jolliffe, I. T., & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide in Atmospheric Science.* Wiley. (검증 개념·지표 — 표준 참고문헌)
- GHRSST / WMO-IOC JCOMM SST·match-up 검증 관행, robust statistics 사용 (표준 지침)
- Stow, C. A., Jolliff, J., McGillicuddy, D. J., Doney, S. C., Allen, J. I., Friedrichs, M. A. M., Rose, K. A., & Wallhead, P. (2009) "Skill assessment for coupled biological/physical models of marine systems." *J. Marine Systems* 76, 4–15, doi:10.1016/j.jmarsys.2008.03.011. (모델 스킬 평가 종합 — 실제 표준 문헌)

**핵심 1차 문헌(지표·방법)**
- Taylor, K. E. (2001) "Summarizing multiple aspects of model performance in a single diagram." *J. Geophys. Res.* 106(D7), 7183–7192, doi:10.1029/2000JD900719. (Taylor diagram — 실제 표준 문헌)
- Jolliff, J. K., Kindle, J. C., Shulman, I., Penta, B., Friedrichs, M. A. M., Helber, R., & Arnone, R. A. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment." *J. Marine Systems* 76, 64–82, doi:10.1016/j.jmarsys.2008.05.014. (Target diagram — 실제 표준 문헌)
- Willmott, C. J. (1981) "On the validation of models." *Physical Geography* 2(2), 184–194. (Index of Agreement — 실제 표준 문헌); Willmott, Robeson & Matsuura (2012) *Int. J. Climatol.* 32, 2088–2094, doi:10.1002/joc.2419 (refined d_r).
- Murphy, A. H. (1988) "Skill scores based on the mean square error and their relationships to the correlation coefficient." *Mon. Wea. Rev.* 116, 2417–2424. (MSESS — 실제 표준 문헌)
- Perkins, S. E., Pitman, A. J., Holbrook, N. J., & McAneney, J. (2007) "Evaluation of the AR4 climate models' simulated daily maximum temperature, minimum temperature, and precipitation over Australia using probability density functions." *J. Climate* 20(17), 4356–4376, doi:10.1175/JCLI4253.1. (Perkins skill score — 실제 표준 문헌)
- North, G. R., Bell, T. L., Cahalan, R. F., & Moeng, F. J. (1982) "Sampling errors in the estimation of empirical orthogonal functions." *Mon. Wea. Rev.* 110, 699–706. (EOF 모드 분리성 — 실제 표준 문헌)
- Cayula, J.-F., & Cornillon, P. (1992) "Edge detection algorithm for SST images." *J. Atmos. Oceanic Technol.* 9(1), 67–80, doi:10.1175/1520-0426(1992)009<0067:EDAFSI>2.0.CO;2. (SIED 전선검출 — 실제 표준 문헌)
- Canny, J. (1986) "A computational approach to edge detection." *IEEE TPAMI* 8(6), 679–698. (Canny 에지검출 — 실제 표준 문헌)

**혼합층·장벽층·수괴(spiciness)**
- de Boyer Montégut, C., Madec, G., Fischer, A. S., Lazar, A., & Iudicone, D. (2004) "Mixed layer depth over the global ocean: An examination of profile data and a profile-based climatology." *J. Geophys. Res.* 109, C12003, doi:10.1029/2004JC002378. (MLD 임계값·기후값 — 실제 표준 문헌)
- Holte, J., & Talley, L. (2009) "A new algorithm for finding mixed layer depths with applications to Argo data and Subantarctic Mode Water formation." *J. Atmos. Oceanic Technol.* 26(9), 1920–1939, doi:10.1175/2009JTECHO543.1. (하이브리드 MLD 알고리즘 — 실제 표준 문헌); Holte et al. (2017) *GRL*, doi:10.1002/2017GL073426 (Argo MLD climatology/database).
- de Boyer Montégut, C., Mignot, J., Lazar, A., & Cravatte, S. (2007) "Control of salinity on the mixed layer depth in the world ocean: 1. General description." *J. Geophys. Res.* 112, C06011, doi:10.1029/2006JC003953. (BLT 전구 기후값 — 실제 표준 문헌)
- Flament, P. (2002) "A state variable for characterizing water masses and their diffusive stability: spiciness." *Progress in Oceanography* 54, 493–501, doi:10.1016/S0079-6611(02)00065-4. (spice 정의 — 실제 표준 문헌); McDougall, T. J., & Krzysik, O. A. (2015) "Spiciness." *J. Marine Research* 73(5), 141–152. (spice 재정의 — 실제 표준 문헌); McDougall & Barker (2021) *JGR-Oceans*, doi:10.1029/2019JC015936.

**해양 표준·열함량·TEOS-10**
- IOC, SCOR & IAPSO (2010) *The International Thermodynamic Equation of Seawater — 2010 (TEOS-10): Manual.* 및 *TEOS-10 Primer* — https://www.teos-10.org/pubs/TEOS-10_Primer.pdf
- TEOS-10 Excel 구현, *Ocean Science* 18, 627 (2022) — https://os.copernicus.org/articles/18/627/2022/
- von Schuckmann, K., et al. (2019) "Measuring Global Ocean Heat Content to Estimate the Earth Energy Imbalance." *Front. Mar. Sci.* 6:432 — https://www.frontiersin.org/articles/10.3389/fmars.2019.00432/full
- NOAA NCEI Global Ocean Heat Content — https://www.ncei.noaa.gov/access/global-ocean-heat-content/
- Copernicus Marine OMI — Global OHC anomalies (0–300m) — https://data.marine.copernicus.eu/product/GLOBAL_OMI_OHC_area_averaged_anomalies_0_300/description

**운영 해양예측 검증틀(Class-4)·GLORYS·재분석 평가**
- Ryan, A. G., Regnier, C., Divakaran, P., Spindler, T., Mehra, A., Smith, G. C., Davidson, F., Hernandez, F., Maksymczuk, J., & Liu, Y. (2015) "GODAE OceanView Class 4 forecast verification framework: global ocean inter-comparison." *J. Operational Oceanography* 8(sup1), S98–S111, doi:10.1080/1755876X.2015.1022330. (관측공간 검증 — 실제 표준 문헌)
- Lellouche, J.-M., et al. (2021) "The Copernicus Global 1/12° Oceanic and Sea Ice GLORYS12 Reanalysis." *Front. Earth Sci.* 9:698876, doi:10.3389/feart.2021.698876 — https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.698876/full
- Verezemskaya, P., Barnier, B., Gulev, S. K., Gladyshev, S., Molines, J.-M., Gladyshev, V., Lellouche, J.-M., & Gavrikov, A. (2021) "Assessing Eddying (1/12°) Ocean Reanalysis GLORYS12 Using the 14-yr Instrumental Record From 59.5°N Section in the Atlantic." *J. Geophys. Res. Oceans* 126, doi:10.1029/2020JC016317 — https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020JC016317
- de Souza, J. M. A. C., Couto, P., Sotelino, R., & Roughan, M. (2020/2021) "Evaluation of four global ocean reanalysis products for New Zealand waters–A guide for regional ocean modelling." *NZ J. Marine & Freshwater Res.* 55(1), doi:10.1080/00288330.2020.1713179 — https://www.tandfonline.com/doi/full/10.1080/00288330.2020.1713179

**관측 자료·검증 가이드**
- UCAR Climate Data Guide — Argo Ocean Temperature and Salinity Profiles — https://climatedataguide.ucar.edu/climate-data/argo-ocean-temperature-and-salinity-profiles
- UCAR Climate Data Guide — Salinity — https://climatedataguide.ucar.edu/variables/ocean/salinity
- NASA GSFC — Sea Surface Salinity validation dataset (Aquarius + Argo, 약 50만 정합) — https://earth.gsfc.nasa.gov/cryo/data/sea-surface-salinity
- NOAA Global RTOFS Class-1 Satellite Verification — https://polar.ncep.noaa.gov/global/class-1/
- NOAA PMEL TAO/TRITON 열대해양 관측(D20 진단) — https://www.pmel.noaa.gov/tao/
- IRI/LDEO ENSO Thermocline (D20) maproom — https://iridl.ldeo.columbia.edu/maproom/ENSO/Thermocline/Std_Anom_Depth.html
- GO-SHIP 반복관측(repeat hydrography) — http://www.go-ship.org/

**전선검출 알고리즘 비교(보강)**
- "A comparison of satellite-derived sea surface temperature fronts using two edge detection algorithms." *Deep-Sea Research II* — https://www.sciencedirect.com/science/article/abs/pii/S0967064513004475

---

> **변경 이력(2026-06 갱신)**: (1) 신규 메서드 카드 4종 추가 — Target diagram(Jolliff et al. 2009), GODAE Class-4 관측공간 검증(Ryan et al. 2015), Spiciness(Flament 2002; McDougall & Krzysik 2015), 강건 오차통계(median/MAD/robust RMSE). (2) 출처 점검: de Boyer Montégut(2004)·Holte & Talley(2009) "확인요" 해제하고 DOI 확정; BLT 출처를 de Boyer Montégut et al.(2007, JGR, doi:10.1029/2006JC003953)로 명시; de Souza et al.(2020) 저자 보완; Verezemskaya et al.(2021) 저자 보완. (3) 불안정한 ResearchGate 자동생성 figure URL(D20)을 NOAA PMEL TAO·IRI/LDEO 정식 출처로 교체. (4) Taylor TSS 식을 Taylor(2001) 식 4 정규화 형태로 정정. (5) Murphy 분해·North et al.(1982) EOF 분리성·GO-SHIP 등 해석기준·표준출처 보강.
