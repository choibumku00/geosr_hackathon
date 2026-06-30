# 위성·원격탐사 검증 시각화 카탈로그 (Satellite / Remote Sensing Verification Figures)

이 문서는 **검증 시각화(그림)·표 레퍼런스 카탈로그** 시리즈의 **[위성·원격탐사 도메인편]** 이다. 우리 수치모델 결과를 위성·원격탐사 자료(고도계 altimetry, 위성 SST, 산란계 scatterometer 해상풍, 해색 ocean color/Chl-a)와 비교·검증할 때 **"어떤 그림을 어떻게 그리고 어떻게 읽을 것인가"** 를 그림 카드로 정리한다. 대응하는 *메서드 카드*(무엇을·어떻게 계산하나)는 [`../12_satellite_remote_sensing.md`](../12_satellite_remote_sensing.md)에 있으며, 본 문서는 그 메서드를 **그림으로 표현하는 법**에 집중한다.

> **범위·중복방지**: Taylor 다이어그램·target 다이어그램·일반 QQ/CDF·오차장 지도 같은 **횡단(공통) 그림은 별도 [공통편]** 이 담당한다. 여기서는 **위성 자료 특유의 그림**(매치업, TC 오차분산, along-track vs gridded, 파수 스펙트럼·유효해상도, crossover, L2/L3/L4 처리수준, skin–bulk/diurnal, 산란계 벡터·rain flag, 해색 log10, 불확실성 u-plot·정규화오차)만 카드화한다. 공통 그림은 "교차링크"로만 참조한다.
>
> **반드시 지킬 해석 원칙** (→ [`../00_overview_taxonomy.md` §G](../00_overview_taxonomy.md#g-검증-해석의-함정--반드시-지킬-원칙-critical-caveats))
> 1. **기준자료 ≠ 참값**: GHRSST L4·DUACS 격자 SLA·재분석은 reference이지 truth가 아니다. 그림 캡션·축 라벨에 "vs reference"로 쓰고 차이를 "모델−기준"으로 표기.
> 2. **동화·보간 산물을 독립 관측처럼 쓰지 말 것**: GHRSST **L4**, DUACS/CMEMS **L4** 같은 OI·동화 격자는 이미 평활·보간되어 분산이 줄고 오차가 공간상관된다. **TC 등 "오차 무상관" 가정 그림에 독립 3자로 넣지 말 것**, along-track 검증에는 **독립 궤도**를 쓸 것.
> 3. **해석 임계는 advisory**: 아래 카드의 모든 수치 임계(예: robust SD ≲0.3 K, CV>0.15 제외, std(z)≈1)는 **센서·해역·해상도·기준자료 의존**이며 자동으로 "좋음/나쁨"을 단정하지 않는다. 영역·해상도 의존 경고를 항상 동반.
> 4. **단일 그림 금지**: 어떤 결론도 그림 1장으로 내지 않는다. 최소 (정확도 + 편향 + 분포/패턴) + 유의성을 함께 본다.

> **출처 표기 원칙**: 서지(저자·연도·저널·DOI)를 **실제 확인한 것**만 확정 표기한다. 미확인 세부는 "(확인요)". DOI를 지어내지 않는다. **논문 그림을 복제하지 않으며**, 그림의 *유형·사양*만 기술한다. 공개 원본 URL은 병기 가능.

---

## 목차 (그림 카드 16개)

**매칭·오차구조**
1. 매치업 밀도 산점도 + 통계 박스 (Matchup density scatterplot)
2. 대표성오차·서브풋프린트 변동 그림 (Representativeness error / sub-footprint variability)
3. 삼중대조 오차분산 막대·삼각 그림 (Triple collocation error-variance)
4. 확장 TC SNR·요약 다이어그램 (ETC SNR / TC summary diagram)

**고도계 (Altimetry)**
5. along-track vs gridded 잔차 비교 (Along-track vs gridded SLA/ADT)
6. 파수 스펙트럼·유효해상도(+코히어런스) (Wavenumber spectrum & effective resolution)
7. 교차점 차이 맵·히스토그램 (Crossover difference)

**SST**
8. L2/L3/L4 처리수준 비교 패널 (Processing-level comparison)
9. Skin–bulk·일주가열 차이 (Skin–bulk & diurnal warming)
10. SST 전선·수평경도 맵 (SST front / gradient)

**산란계 풍 (Scatterometer wind)**
11. 풍 벡터 비교(스템·성분 산점) (Wind vector comparison)
12. Rain flag·조건별 편차 비닝 (Rain-flag & conditional bias)

**해색 (Ocean color)**
13. Chl-a log10 산점도 + 매치업 통계 (Chl-a log10 matchup)

**처리·불확실성**
14. L2→L3 비닝 표본밀도·평활 효과 (Swath binning sampling/smoothing)
15. 불확실성 u-plot / 신뢰도 곡선 (Uncertainty u-plot)
16. 정규화오차(z) QQ-plot·히스토그램 (Normalized-error QQ / z-histogram)

---

### 1. 매치업 밀도 산점도 + 통계 박스 (매치업 산점도 / Matchup Density Scatterplot)
- **무엇을 보여주나**: 시공간 매칭으로 만든 위성 vs 기준(모델/in situ) 짝의 분포를 2D 밀도 산점으로, 한 그림에 편향·산포·상관·회귀를 요약. 모든 위성 정량검증의 1차 그림.
- **읽는 법**: 가로축=기준값, 세로축=위성(또는 모델)값. 1:1 대각선(점선)과 OLS/Type-2(주축) 회귀선을 겹친다. 점 대신 hexbin/2D 히스토그램(log 컬러스케일)으로 과밀구간을 표현. 모서리 통계박스: N, bias, RMSD, robust SD(1.4826×MAD), r, slope/intercept. **좋은 패턴**: 점운(point cloud)이 1:1선에 좁게 밀착, 회귀선≈대각선. **나쁜 패턴**: 회귀선이 대각선에서 기울어짐(곱셈·덧셈 편향), 고/저값 끝에서 휘어짐(비선형·포화), 한쪽으로 두꺼운 꼬리(이상치).
- **언제 쓰나**: 모든 자료형(트랙·격자·시계열), 처리수준 무관. 검증목적=정확도·편향. 위성–모델, 위성–in situ, 모델–재분석(ERA5/GLORYS) 매치업.
- **짝지표 & 교차링크**: bias·RMSD·centered RMSD·robust SD·r·회귀(→ `12` 매치업 통계지표; `01` 오차통계). 분포 꼬리는 16번·[공통편 QQ]로, 종합요약은 [공통편 Taylor/target]으로 보완.
- **만드는 법**: `matplotlib` `hexbin`/`hist2d`(+`LogNorm`), `scipy.stats.linregress`(OLS)·`scipy.odr`(Type-2/주축회귀), `numpy.median`+MAD로 robust SD, `cmocean` 또는 perceptually-uniform 컬러맵. 밀도는 `viridis`/`cmo.dense`.
- **함정·주의**: OLS는 x(기준)도 오차를 가질 때 기울기를 **편향**시킨다 → 두 자료 모두 오차면 **주축/직교회귀(Type-2)** 병기. 매치업 윈도우(Δr·Δt)·QC 임계가 통계를 좌우(프로토콜 명시). 대표성오차를 빼면 RMSD가 위성/모델 오차를 **과대평가**(→ 2번 카드). 구름·결측으로 표본이 특정 조건에 편향될 수 있음.
- **출처**: 매치업 통계 표준 — Wilks, *Statistical Methods in the Atmospheric Sciences* (교과서). robust SD(1.4826×MAD)는 통계 표준. 해색 매치업 프로토콜: Bailey & Werdell (2006), *Remote Sensing of Environment*, 102, 12–23, doi:10.1016/j.rse.2006.01.015. 컬러맵: Thyng et al. (2016), *Oceanography*, 29(3), 9–13, doi:10.5670/oceanog.2016.66 (cmocean).

---

### 2. 대표성오차·서브풋프린트 변동 그림 (대표성오차 / Representativeness Error & Sub-footprint Variability)
- **무엇을 보여주나**: 점 관측(부이/Argo)과 위성 화소(면적평균)·모델 격자(부피평균)가 "같은 양"을 재지 않아 생기는 비교 불확실성을, 잔차분산 분해(σ²_d = σ²_model + σ²_obs + σ²_repr)와 **풋프린트 내부 변동(SFV)의 공간 지도**로 보여준다.
- **읽는 법**: (a) **SFV 지도**: 고해상 보조자료(예 L2/L3)에서 격자/풋프린트 내 표준편차를 칠한 맵 — 연안·전선·메소스케일역에서 밝게(큼). (b) **오차예산 스택막대**: 관측 RMSD를 σ_obs / σ_repr / 잔여(위성·모델 오차)로 쌓아 비교. **좋은/나쁜 해석**: 관측 RMSD가 대부분 σ_repr로 설명되면(스택에서 σ_repr 비중 큼) "위성/모델 오차가 작다"는 결론. σ_repr를 무시하면 강변동역에서 위성/모델 오차를 과대평가.
- **언제 쓰나**: 위성(면적)–부이(점) 비교 전부, 특히 연안·전선역. 검증목적=오차예산의 공정성(잔차 해석). 자료형: L2/L3 고해상으로 SFV 추정 → 점 비교에 반영.
- **짝지표 & 교차링크**: σ_repr, sub-footprint variability(→ `12` 대표성오차; `15` matchup·대표성오차). 16번 u-plot의 분모에 σ²_repr를 넣어 정규화오차 보정. 데이터동화의 representation error와 동일 개념.
- **만드는 법**: `xarray` coarsen/rolling으로 고해상장의 격자내 분산 계산, `cartopy`+`matplotlib pcolormesh`로 SFV 맵, `cmocean cmo.amp`(순차) 컬러. 구조함수/변동성은 `numpy`·반변동도(variogram, `skgstat` 선택).
- **함정·주의**: σ_repr 정량화는 보조자료 의존·불확실. **시간 대표성**(위성 순간 통과 vs 부이 평균)도 함께 고려. 무시하면 검증 결론이 과대비관. L4처럼 평활된 산물은 SFV가 인위적으로 작아 보임(독립 추정에 부적합).
- **출처**: Janjić et al. (2018), *QJRMS*, 144, 1257–1278, doi:10.1002/qj.3130 (representation error). 서브풋프린트 변동(SSS): "Spatial Scales of Sea Surface Salinity Subfootprint Variability in the SPURS Regions", *Remote Sensing* (2020), doi:10.3390/rs12233996.

---

### 3. 삼중대조 오차분산 막대·삼각 그림 (삼중대조 오차분산 / Triple Collocation Error-Variance)
- **무엇을 보여주나**: 기준진실 없이 3개 독립 자료(위성·모델·in situ)의 콜로케이션만으로 추정한 **각 자료의 랜덤오차 표준편차 σ_ε**를, 막대그래프(자료별 σ_ε ± 부트스트랩 CI) 또는 3자 베n다이어그램/삼각 배치로 비교.
- **읽는 법**: 세로축=오차 SD(자료 단위). 막대가 짧을수록 그 자료가 정확. 오차막대(부트스트랩 CI)가 겹치면 차이가 유의하지 않음. **나쁜 신호**: 음의 분산 추정(막대가 0 미만으로 계산됨) → 표본부족 또는 **오차 독립 가정 위반**. 지역·계절별 패널(소다중)로 안정성 확인.
- **언제 쓰나**: 위성–모델–관측이 동시 존재하는 변수(해상풍·Hs·SSS·SST). 자료형: 격자·궤도·시계열. 검증목적=참값 없이 **자료 정확도 순위화**. "모델 vs GLORYS vs 관측" 3자 구성에도.
- **짝지표 & 교차링크**: σ_ε1·σ_ε2·σ_ε3, 보정계수 α·β(→ `12` TC; `15`·`08` triple collocation; `00` D절 TC 단일구현). SNR·진실상관은 4번 ETC로 확장.
- **만드는 법**: 공분산행렬 `numpy.cov` → TC 식으로 σ_ε 분리, 신뢰구간은 블록 부트스트랩(`numpy`/`scipy`), `matplotlib bar`+`errorbar`. 소다중 패널은 `matplotlib subplots`.
- **함정·주의**: **§G-3 직결** — GHRSST L4·DUACS L4·재분석을 "독립 3자"로 넣으면 오차상관으로 가정이 깨져 추정 왜곡. 모델과 재분석이 같은 NWP 강제력·같은 동화관측을 공유하면 σ_ε 과소. 정상성(stationarity)·선형 가정 필요. 음분산은 버리지 말고 가정위반 신호로 보고. 단일 σ_ε로 "최고 자료" 단정 금지(SNR은 4번과 함께).
- **출처**: Stoffelen (1998), *JGR Oceans*, 103(C4), 7755–7766, doi:10.1029/97JC03180 (TC 원논문). Gruber et al. (2016), "Recent advances in (soil moisture) triple collocation analysis", *Int. J. Applied Earth Obs. Geoinf.*, 45, 200–211, doi:10.1016/j.jag.2015.09.002 (TC 표기·메트릭 정리·시각화 관행). 가정위반 영향: *Remote Sensing* (2025), doi:10.3390/rs17223751.

---

### 4. 확장 TC SNR·요약 다이어그램 (확장 삼중대조 / ETC SNR & TC Summary Diagram)
- **무엇을 보여주나**: TC를 확장해 각 자료와 **알 수 없는 진실의 상관 ρ_{T,Xi}**(= 정규화 SNR)까지 추정한 결과를, (a) 자료별 SNR(dB) 막대, 또는 (b) 오차분산(반경)·진실상관(각/색)을 한 평면에 얹은 TC 요약 다이어그램으로 표현.
- **읽는 법**: SNR 막대는 클수록 좋음(SNR=ρ²/(1−ρ²)). 요약 다이어그램에서는 **원점(또는 기준점)에 가까울수록**(작은 잡음·높은 진실상관) 우수. **함정 회피 포인트**: 잡음 σ_ε는 크지만 진실상관 ρ가 높아 실효 SNR이 더 좋은 자료가 있을 수 있음 → 잡음만 보는 3번 막대그림의 결론을 보완.
- **언제 쓰나**: TC와 동일(3자료, 동적범위·민감도 차이가 클 때 특히). 검증목적=잡음 + 신호민감도 동시 평가.
- **짝지표 & 교차링크**: ρ²_{T,Xi}, SNR, σ_ε(→ `12` ETC; 3번 카드). [공통편 Taylor]와 형태는 닮았으나 **기준=알 수 없는 진실**이라는 점이 다름(혼동 주의).
- **만드는 법**: ETC 공분산 해(`numpy`)로 ρ·SNR 산출, `matplotlib`로 막대 또는 산점(반경=σ_ε, 색=ρ). dB 변환 `10*log10(SNR)`.
- **함정·주의**: TC와 같은 **오차 독립 가정 한계 승계**(§G-3). 단일 다이어그램으로 여러 측면을 요약하려다 과해석 주의. ρ는 표본 변동성에 민감 → CI 동반.
- **출처**: McColl et al. (2014), *Geophysical Research Letters*, 41, 6229–6236, doi:10.1002/2014GL061322 (ETC). TC 요약 다이어그램: Siu et al. (2024), *Frontiers in Remote Sensing*, 5, doi:10.3389/frsen.2024.1395442. 4자료 교차검증: Vogelzang & Stoffelen (2021), *JGR Oceans*, 126, e2021JC017189, doi:10.1029/2021JC017189.

---

### 5. along-track vs gridded 잔차 비교 (고도계 궤도 vs 격자 / Along-track vs Gridded SLA·ADT)
- **무엇을 보여주나**: 모델/격자(L4) SSH·SLA·ADT를 **독립 위성 궤도(along-track L3)** 로 검증한 결과를, (a) 궤도 잔차(모델−관측)를 궤도선 위에 색으로 그린 지도, (b) 궤도점 매치업 산점, (c) 위도/거리별 RMSD 단면으로 비교.
- **읽는 법**: (a) 지도에서 궤도선이 균일한 색(잔차≈0)이면 양호, 특정 해역(연안·강에디역)에서 붉/푸르게 치우치면 그곳 오차. (b) 산점은 1번 카드 규약. (c) 단면에서 연안 접근 시 RMSD 급증은 고도계 품질저하 신호. **좋은 패턴**: 외해 잔차 작고 공간적으로 무작위. **나쁜 패턴**: 잔차가 메소스케일 구조(에디 윤곽)를 띠면 위상·진폭 오차.
- **언제 쓰나**: 해수면(격자 NetCDF·궤도 along-track). 검증목적=정확도 + 소규모 신호 평가. 모델 vs CMEMS L4/GLORYS 재분석 비교에 직접.
- **짝지표 & 교차링크**: 궤도 RMSD·분산설명도·상관(→ `12` along-track vs gridded; `11` SSH/ADT). 평활 손실은 6번(파수 스펙트럼), 자체일관성은 7번(crossover).
- **만드는 법**: `xarray`로 모델→궤도점 시공간 보간(`.interp`), `cartopy`로 궤도 잔차 산점지도, `cmocean cmo.balance`(발산, 0 중심) 컬러. 위도-binned RMSD는 `numpy`/`xarray groupby_bins`.
- **함정·주의**: **§G-2 직결** — 격자 L4를 격자 검증에 쓰면 독립성 결여 → 반드시 **독립 궤도(다른 미션)** 사용. SLA vs ADT vs SSH 정의 혼동(평균면·MDT) 주의. L4는 평활로 분산이 줄어 RMSD가 **작게 보일 수 있음** → 6번과 함께 해석. 연안 고도계 품질저하·조석/역기압 보정 일관성.
- **출처**: Copernicus Marine(CMEMS) SEALEVEL L4 제품·QUID 검증보고. "Evaluation of gridded sea surface height products based on along-track altimeter data", *Intelligent Marine Technology and Systems* (Springer, 2026), doi:10.1007/s44295-026-00092-9 (CMEMS DT/NRT·GLORYS를 along-track HY-2B로 평가). SWOT 연안 SLA: *Water* (2025), 17(21), 3066, doi:10.3390/w17213066.

---

### 6. 파수 스펙트럼·유효해상도(+코히어런스) (파수 스펙트럼·유효해상도 / Wavenumber Spectrum & Effective Resolution)
- **무엇을 보여주나**: along-track SSH/SLA의 1D 파수 스펙트럼 E(k)를 log-log로 그려, 모델/위성이 **실제로 분해하는 최소 스케일(유효해상도)**·잡음바닥(noise floor)·스펙트럼 기울기를 비교. 확장으로 모델–위성 **코히어런스(스케일별 위상·진폭 일치)** 를 같은 파장축에 얹는다.
- **읽는 법**: 가로=파수 k(또는 파장 λ=1/k, 보통 위쪽 보조축에 km), 세로=PSD(log). 고파수 평탄부=잡음바닥. **신호가 잡음바닥과 만나는 파장=유효해상도 λ_p**(수직선으로 표시). 메소스케일 대역(예 90–280 km) 기울기 적합선 병기. **좋은 패턴**: 모델 스펙트럼 기울기·잡음바닥이 위성과 유사, 코히어런스가 큰 스케일에서 1에 가깝다가 작은 스케일에서 떨어짐. **나쁜 패턴**: 모델 PSD가 소규모에서 급락(과도한 수치확산·과평활) 또는 잡음으로 들뜸.
- **언제 쓰나**: 해수면(along-track), Hs 등 1D 궤도 스펙트럼이 의미 있는 변수. 검증목적=소규모 변동성 재현·유효해상도(스칼라 RMSD로 못 보는 정보).
- **짝지표 & 교차링크**: 유효해상도 λ_p, 스펙트럼 기울기, magnitude-squared coherence(→ `12` 파수 스펙트럼; `05` PSD/파수; `02` 스케일분리; `14` RAPSD/유효해상도). 격자 L4의 평활은 5번 RMSD와 교차해석.
- **만드는 법**: 균질 궤도 세그먼트 추출·디트렌딩·`scipy.signal.windows.hann` 윈도잉 → `numpy.fft`/`scipy.signal.periodogram`(또는 `welch`)로 PSD, 코히어런스 `scipy.signal.coherence`. log-log·이중축은 `matplotlib`.
- **함정·주의**: 스펙트럼은 윈도잉·세그먼트 길이·결측 처리에 민감. 잡음바닥 진단 대역 선택이 λ_p를 좌우. L4 유효해상도는 적도 ~800 km~고위도 ~100 km로 위도의존 → 위도대별로 따로. 결측 보간이 고파수를 인위적으로 만들 수 있음.
- **출처**: Ballarotta et al. (2019), "On the resolutions of ocean altimetry maps", *Ocean Science*, 15, 1091–1109, doi:10.5194/os-15-1091-2019. Dufau et al. (2016), "Mesoscale resolution capability of altimetry", *JGR Oceans*, doi:10.1002/2015JC010904 (확인요: 권·페이지).

---

### 7. 교차점 차이 맵·히스토그램 (교차점 분석 / Crossover Difference)
- **무엇을 보여주나**: 위성 상승/하강 궤도가 짧은 시차로 같은 지점을 통과하는 **교차점(crossover)**에서의 차이 Δ = X_asc − X_desc를, (a) 교차점 위치에 색점으로 찍은 지도, (b) Δ 히스토그램(편차·SD)으로 보여 위성자료의 **자체일관성·계통오차**(궤도·기준면 오차 등)를 진단.
- **읽는 법**: (a) 지도에서 색점이 0 부근 무작위면 내부정합 양호, 위도·궤도방향에 따른 체계적 색조는 궤도·기준면 오차 시사. (b) 히스토그램 중심(편차)이 0, 폭(SD)이 작을수록 정합. **나쁜 패턴**: Δ가 위도/시각에 따라 구조적, 두꺼운 꼬리. 모델 검증 **전** 위성자료 품질 사전점검으로 사용.
- **언제 쓰나**: 고도계 SSH/SLA(교차점 표준), 산란계·SST 상·하행 일관성에도 응용. 자료형: 궤도. 검증목적=위성자료 자체 정합성(검증의 전제).
- **짝지표 & 교차링크**: 교차점 Δ 편차·SD(→ `12` 궤도/스와스 처리·교차점 분석; `11` crossover·aliasing). 사전점검 후 5번(모델 검증)으로 진행.
- **만드는 법**: 상/하행 궤도 교차 탐색(선분 교차 또는 `pyinterp`/`xarray` 보간), 시차 보정용 변동 제거 후 Δ, `cartopy` 산점지도(`cmo.balance`)+`matplotlib hist`.
- **함정·주의**: 교차점 시차 동안의 **실제 변동을 오차로 오인** 가능(시차 보정 필요). 위성 고유 처리(궤도·조석·기준면 보정) 품질에 의존. 교차점은 외해에 편중(연안 표본 적음).
- **출처**: 교차점 분석은 altimetry 정합성 평가의 정착된 표준(AVISO/CMEMS 고도계 처리·검증 핸드북 — 구체 서지 확인요). 응용 맥락: 위 5·6번 고도계 출처 참조.

---

### 8. L2/L3/L4 처리수준 비교 패널 (SST 처리수준 비교 / SST L2·L3·L4 Comparison, GHRSST)
- **무엇을 보여주나**: 같은 SST 장면을 처리수준별(L2P 원해상도+불확실성·플래그, L3U/L3C/L3S 격자, L4 빈틈없는 보간격자)로 나란히 그려, 결측·평활·불확실성 차이와 각 수준의 in situ 매치업 통계를 비교한다.
- **읽는 법**: 다중 패널 — (a) L2P: 궤도 구름틈·화소별 불확실성, (b) L3: 격자화로 결측 일부 메움, (c) L4: 빈틈 없으나 평활. 패널마다 in situ 매치업 통계(bias·robust SD)를 캡션에. **좋은/나쁜 해석**: L4가 매끈해 보기 좋지만 **보간 정보 혼입**으로 독립검증의 독립성을 해침. 야간·고품질 L2 매치업의 |bias|·robust SD가 센서 사양 내인지가 핵심.
- **언제 쓰나**: 수온(격자 NetCDF). 검증목적=처리수준별 정확도·일관성·적합성 선택. 기준=iQuam 등 QC된 in situ.
- **짝지표 & 교차링크**: bias·robust SD·상관, L4-SQUAM 상호비교(→ `12` SST L2/L3/L4; `09` SST/GHRSST; 1번 매치업·16번 불확실성). 전선용은 10번(고해상 L2/L3).
- **만드는 법**: `xarray`로 각 수준 로드·`quality_level` 마스킹, `cartopy` 멀티패널 `pcolormesh`, SST는 `cmocean cmo.thermal`. 매치업 통계는 1번 도구.
- **함정·주의**: **§G-2** — L4 검증에 그 L4가 **이미 동화·사용한 in situ를 재사용 금지**. 구름역 IR SST 결측 편향. L4는 편의적이나 모델 검증의 독립성·소규모 신호를 해침 → 가능하면 L2/L3 + 독립 in situ. 처리수준 라벨(L3U vs L3C vs L3S) 혼동 주의.
- **출처**: GHRSST Data Specification·Task Team 문서(ghrsst.org). SQUAM(L4 상호비교): Dash et al. (2010), *J. Atmos. Oceanic Technol.*, 27, 1899–1917, doi:10.1175/2010JTECHO756.1. in situ QC(iQuam): Xu & Ignatov (2014), *J. Atmos. Oceanic Technol.*, 31, 164–180, doi:10.1175/JTECH-D-13-00121.1.

---

### 9. Skin–bulk·일주가열 차이 (스킨-벌크·일주변동 / Skin–Bulk & Diurnal Warming)
- **무엇을 보여주나**: 위성 IR SST(skin, ~10–20 µm)와 in situ/모델 SST(bulk/foundation)의 **측정깊이·시각 차이**가 만드는 계통편차를, (a) skin−bulk 차의 풍속/일사 의존 곡선, (b) 국지시각(LST)에 따른 일주가열 ΔSST 합성도(주간 양의 가열), (c) 보정 전후 위성–부이 차 비교로 보여준다.
- **읽는 법**: (a) 야간 skin−bulk ≈ −0.1~−0.2 K(쿨스킨), 풍속↑이면 0에 수렴. (b) 정오~오후 약풍에서 ΔSST 최대(주간 가열층). (c) **보정 전**: 주간 위성–부이 차가 과장 → **보정 후**: 주·야 차이가 수렴(≈0.01 K급)하면 보정 타당. **나쁜 신호**: 보정 후에도 시각의존 잔차가 남으면 모델/보정 결함.
- **언제 쓰나**: 위성 SST 검증·동화 전반, 주간·약풍 일주가열 강한 때 특히. 검증목적=공정 비교 위한 깊이/시각 정합. 자료형: L2/L3 + 부이.
- **짝지표 & 교차링크**: skin−bulk 차, 일주진폭 ΔSST(→ `12` skin–bulk·diurnal; `09` SST). 보정 후 매치업은 1·8번으로.
- **만드는 법**: LST·풍속·일사 binning(`xarray groupby_bins`), 쿨스킨/웜레이어 모델(예 Fairall/COARE류, 구현체 선택)로 보정, `matplotlib`로 의존곡선·합성도. 차이맵은 `cmo.balance`.
- **함정·주의**: 쿨스킨/웜레이어 모델 **자체 불확실성**. 연안·약풍역 보정오차 큼. **어느 깊이로 통일하나**(검증 목적)에 따라 결론이 바뀜 → 깊이 정의(skin/sub-skin/depth/foundation) 명시. 보정 없이 비교하면 주간 편차 과장(가짜 bias).
- **출처**: Embury, Merchant & Corlett (2012), *Remote Sensing of Environment*, 116, 62–78, doi:10.1016/j.rse.2011.02.028 (skin·diurnal 고려 ATSR 재처리 검증). SST 정의 체계(skin/sub-skin/foundation)·cool-skin/diurnal: GHRSST 규격(ghrsst.org; Donlon et al. 관련 — 서지 확인요).

---

### 10. SST 전선·수평경도 맵 (SST 전선·경도 / SST Front & Gradient Map)
- **무엇을 보여주나**: 모델 SST의 수평경도 |∇SST|·전선(front) 위치·강도를 고해상 위성 SST(L2/L3)와 나란히 비교. 평균 SST는 맞아도 **전선 구조(연안용승·해류경계)가 흐려지는지** 진단.
- **읽는 법**: (a) |∇SST| 맵 2장(모델/위성) 동일 컬러스케일, (b) 검출 전선선(Cayula–Cornillon SIED 또는 경도임계) 오버레이, (c) 경도강도 히스토그램·전선확률(FP) 차이맵. **좋은 패턴**: 모델 경도분포·전선위치가 위성과 유사. **나쁜 패턴**: 모델 경도가 체계적으로 약함(수치확산·해상도 부족 → 전선 과소), 또는 위치 변위.
- **언제 쓰나**: 위성 SST·Chl-a 격자(NetCDF). 검증목적=패턴·구조(전선). 고해상 위성(VIIRS/Sentinel-3)일수록 유리.
- **짝지표 & 교차링크**: 경도분포·전선위치 변위·전선확률(→ `12` SST 전선·경도; `02` 공간패턴; 객체기반은 [공통편 SAL/MODE]·`02`). 위치 변위 정량은 객체기반 검증과 짝.
- **만드는 법**: 경도는 `numpy.gradient`/`xarray.differentiate`, 전선검출 `scipy.ndimage`(Sobel/Canny류) 또는 Cayula–Cornillon 구현, `cartopy` 맵, `cmocean cmo.thermal`(SST)·순차맵(|∇SST|).
- **함정·주의**: 경도는 **해상도·평활에 매우 민감 → 반드시 동일 스케일 비교**(모델을 위성해상도로, 또는 그 반대). 구름틈·결측이 경도장 왜곡. **위성 L4(평활)는 전선이 흐려 경도 비교에 부적합** → 고해상 L2/L3 사용.
- **출처**: 전선검출(히스토그램기반): Cayula & Cornillon (1992), "Edge Detection Algorithm for SST Images", *J. Atmos. Oceanic Technol.*, 9, 67–80 (확인요: 정확한 권·페이지·DOI). 객체기반 공간검증: Gilleland et al. (2009), *Weather and Forecasting*, 24, 1416–1430, doi:10.1175/2009WAF2222269.1; SAL: Wernli et al. (2008), *Monthly Weather Review*, 136, 4470–4487, doi:10.1175/2008MWR2415.1 (해양 전선 적용은 응용 — 맥락 확인요).

---

### 11. 풍 벡터 비교(스템·성분 산점) (산란계 풍 벡터 비교 / Scatterometer Wind Vector Comparison)
- **무엇을 보여주나**: 산란계(ASCAT/OSCAT/HY-2 등) 10 m 등가중립풍과 부이/NWP(ERA5)/타 산란계의 **풍속·풍향(벡터)** 일치를, (a) u·v 성분 각각 산점, (b) 풍속 산점 + 풍향 차 원형히스토그램, (c) 스템플롯(stick/quiver) 시계열로 보여준다.
- **읽는 법**: (a) u·v 산점은 1번 규약(성분별 bias·RMSD). (b) 풍향 차 히스토그램은 0° 중심·좁을수록 좋음; **약풍에서 풍향 산포 급증**(물리적 한계)에 유의. (c) 스템플롯에서 화살표 길이=풍속, 방향=풍향; 모델·관측 화살표가 겹치면 양호. **나쁜 패턴**: 풍속 산점이 1:1 아래로 치우침(다운윈드 표층류로 인한 음편차), 고풍속 포화.
- **언제 쓰나**: 해상풍(궤도 swath·격자). 검증목적=벡터 정확도(속도+방향). 기준=부이(점)·NWP(격자, ERA5).
- **짝지표 & 교차링크**: 풍속 bias/RMSD, 풍향 원형 RMSD, u/v 성분 RMSD, 벡터상관(→ `12` 산란계 풍; `07` 바람 벡터·원형통계; `10` 벡터/복소상관). 분해능 차이엔 3·4번 TC/QC.
- **만드는 법**: u/v 산점 `matplotlib`(1번 hexbin), 풍향 차는 원형통계(±180° wrap, `numpy`)+극좌표 히스토그램, 스템 `matplotlib quiver`. 표층류 보정은 보조 표층류장 차감.
- **함정·주의**: **등가중립풍 vs 실제풍** 정의 일치 필요. 표층류·대기안정도 미보정 시 계통편차(다운윈드 표층류 ~0.96배 음편차; 보정 시 RMSD ~15% 감소 사례). 분해능 차이(부이 점 vs 셀)→ETC 필요. 풍향 RMSD는 **반드시 원형통계**(선형평균 금지).
- **출처**: Stoffelen (1998), doi:10.1029/97JC03180 (풍 TC). 표층류 영향: "Characterizing the Effect of Ocean Surface Currents on ASCAT Winds Using Open Ocean Moored Buoy Data", *Remote Sensing* (2023), 15(18), 4630, doi:10.3390/rs15184630. 4자료: Vogelzang & Stoffelen (2021), doi:10.1029/2021JC017189.

---

### 12. Rain flag·조건별 편차 비닝 (산란계 rain flag·조건부 편차 / Rain-flag & Conditional Bias Binning)
- **무엇을 보여주나**: 산란계 풍의 오차가 **강수(rain)·풍속·입사각·연안거리** 등 조건에 따라 어떻게 변하는지를, rain flag별·풍속 bin별 bias/RMSD 막대 또는 2D 조건부 히트맵으로 보여준다.
- **읽는 법**: (a) rain flag(무강수/강수) 두 그룹의 bias·RMSD 막대 비교 — 강수 그룹에서 RMSD 급증(우적 산란 오염). (b) 풍속 bin별 bias 곡선 — 저풍속 양편차·고풍속 포화. (c) (풍속×입사각) 2D 히트맵으로 조건의존 구조. **좋은 패턴**: 플래그 적용 후 강수 오염 표본 제거로 RMSD 안정. **나쁜 패턴**: 강수역 잔차가 크고 무작위가 아님(플래그 누락).
- **언제 쓰나**: 해상풍(swath). 검증목적=품질플래그 유효성·조건의존 오차 진단. 자료형: L2 swath + 플래그.
- **짝지표 & 교차링크**: rain-flag별 bias/RMSD, 조건부 편차(→ `12` 산란계 풍; `03` 범주·플래그 평가; 16번 불확실성). QC 임계 선택은 1번 매치업과 연동.
- **만드는 법**: `xarray`/`pandas` groupby(rain_flag, wind-speed bin), `matplotlib bar`/`hist2d` 히트맵. 조건부 통계는 `numpy`.
- **함정·주의**: ASCAT(C-band)은 우중에서도 QuikSCAT(Ku-band)보다 우수 — 센서별 우적 민감도 차이 명시. 플래그 과적용은 강풍·강수공존(태풍) 표본을 통째로 제거해 편향. 연안·낮은 풍속 품질저하를 강수로 오귀속 주의.
- **출처**: 표층류·조건의존: *Remote Sensing* (2023), 15(18), 4630, doi:10.3390/rs15184630. 산란계 비교·품질(우중 성능): Yang et al. (2019), "Comparison of Oceansat-2 Scatterometer Wind Data with Global Moored Buoys and ASCAT", *Advances in Meteorology*, 2019, 1651267 (확인요: DOI). QC/4자료 틀: Vogelzang & Stoffelen (2021), doi:10.1029/2021JC017189.

---

### 13. Chl-a log10 산점도 + 매치업 통계 (해색 매치업 / Ocean Color Chl-a log10 Matchup)
- **무엇을 보여주나**: 위성 클로로필-a(Chl-a)·원격반사도(Rrs)를 현장 측정과 매치업한 산점도를 **log10 축**으로 그려, 곱셈적(multiplicative) 편향·산포·회귀를 평가. Chl-a는 대수정규 근사이므로 log10이 필수.
- **읽는 법**: 두 축 모두 log10(Chl-a). 1:1선·Type-2 회귀 오버레이. 통계박스는 **log10 공간**: MdAE(중앙절대오차)·bias·log-RMSD·r·slope(곱셈편향). **좋은 패턴**: 점운이 1:1선에 밀착, 자릿수(decade)를 가로질러 균질. **나쁜 패턴**: 저Chl(외해)·고Chl(연안 Case-2)에서 휘어짐, 한쪽 자릿수에 표본 편중. 색=수역(Case-1/2) 또는 밀도.
- **언제 쓰나**: 해색(격자 NetCDF: Chl-a, Rrs). 검증목적=정확도·편향(대수공간). 현장=선박·AERONET-OC·부이.
- **짝지표 & 교차링크**: log10 MdAE·bias·RMSD·slope(→ `12` 해색 Chl-a; 1번 매치업; [공통편 QQ]는 log축). 대표성오차는 2번(연안 Case-2 큼).
- **만드는 법**: Bailey–Werdell 윈도우(3×3 화소, 유효≥50%, ±1.5σ 제외, CV>0.15 매치업 제외, 시간윈도 ±3 h) 적용 후 `numpy.log10` 변환 → `matplotlib` 산점(`set_xscale('log')`) 또는 log10값 직접. `scipy.odr` Type-2.
- **함정·주의**: **선형공간 통계는 대수정규에서 편향 → 반드시 log10**. 프로토콜(윈도우·CV 임계·필터)에 따라 매치업 수·통계가 달라짐 → **어떤 프로토콜인지 명시**. 연안 Case-2·픽셀경계효과로 대표성오차 큼. 대기보정 품질플래그 필수, log 변환 전 양수성.
- **출처**: Bailey & Werdell (2006), *Remote Sensing of Environment*, 102(1–2), 12–23, doi:10.1016/j.rse.2006.01.015. 엄격 QC: Zibordi et al. (2009), *Remote Sensing of Environment*, 113(12), 2574–2591, doi:10.1016/j.rse.2009.07.016. AERONET-OC: Zibordi et al. (2009), *J. Atmos. Oceanic Technol.*, 26, 1634–1651, doi:10.1175/2009JTECHO654.1.

---

### 14. L2→L3 비닝 표본밀도·평활 효과 (스와스 비닝 / Swath Binning Sampling & Smoothing)
- **무엇을 보여주나**: 궤도(L2 swath) 위성을 고정격자(L3)로 모으는 처리의 결과를, (a) 빈별 **표본수(관측밀도) 맵**, (b) 비닝 전후 분산/유효해상도 변화, (c) 가중방식(균등/면적/역거리/최근접)·시간윈도(일·주·월)에 따른 차이로 보여준다.
- **읽는 법**: (a) 표본밀도 맵에서 궤도 사이·구름역은 표본 적음(검증 신뢰도↓ 영역). (b) 비닝 후 분산이 줄어듦(평활) → 검증 RMSD가 작게 보이는 인공효과. **좋은/나쁜 해석**: 표본밀도 충분하면 가중방식 차이 작음; 표본 희박역의 통계는 불안정하므로 표본수로 가중·마스킹. 시간윈도 길면 표본↑·시간대표성↓.
- **언제 쓰나**: 해색·SST·풍 등 swath를 격자 모델과 비교할 때. 검증목적=비교 스케일 정합·표본 충분성. 자료형 L2→L3.
- **짝지표 & 교차링크**: 빈 표본수·격자내 분산·유효해상도(→ `12` L2→L3 비닝; `15` 보간/재격자; 2번 대표성오차·6번 유효해상도). on-swath(모델→궤도) 대안과 비교.
- **만드는 법**: NASA L3 등면적 비닝(Integerized Sinusoidal) 또는 `xarray`/`xhistogram` 빈집계, `cartopy`로 표본밀도 맵(순차 `cmo.dense`), 분산 비교는 `numpy`.
- **함정·주의**: **격자화 자체가 평활·대표성오차를 만들어** 검증결과에 영향(RMSD 해석 시 고려). **on-swath(모델→궤도 보간) vs 둘 다 격자화**는 결과가 다를 수 있음 → 방법 명시. 표본 희박역 통계 과신 금지. 등면적 투영·시간윈도 선택 영향.
- **출처**: NASA Ocean Color — Level-3 Integerized Sinusoidal Binning Scheme(oceancolor.gsfc.nasa.gov). NASA SeaDAS — Level 3 Binning Operator(seadas.gsfc.nasa.gov). 평활·대표성: 2번 카드 출처(Janjić et al. 2018, doi:10.1002/qj.3130).

---

### 15. 불확실성 u-plot / 신뢰도 곡선 (불확실성 정합 / Uncertainty u-plot & Reliability)
- **무엇을 보여주나**: 위성/모델이 **함께 보고하는 픽셀별 불확실성**이 실제 오차분포와 맞는지를, (a) 명목 신뢰수준 vs 실측 포함비율의 **u-plot/신뢰도 곡선**, (b) 보고된 불확실성 bin별 실측 오차 SD(예측 불확실성 vs 실현 산포)로 보여준다. "오차뿐 아니라 오차추정치도 검증."
- **읽는 법**: (a) u-plot 가로=명목 분위/신뢰수준, 세로=실제 포함비율; **대각선(1:1)에 붙으면 잘 보정**됨. 곡선이 대각선 **위**면 불확실성 과대평가(보수적), **아래**면 과소평가(과신·위험). (b) 보고 불확실성 bin이 클수록 실측 SD도 비례 증가하면 양호. **나쁜 패턴**: 곡선이 대각선에서 크게 이탈, bin과 실측 SD가 무관.
- **언제 쓰나**: 불확실성 변수를 제공하는 위성자료(SST L2P, SSS, altimetry 오차추정). 검증목적=UQ 신뢰성(동화·앙상블 전제). 자료형: 불확실성 동반 L2/L3.
- **짝지표 & 교차링크**: 포함비율(coverage)·표준화오차 std(z)(→ `12` 불확실성 검증; 16번 정규화오차 QQ; `14` UQ/calibration; 2번 σ_repr). 16번과 한 쌍으로 본다.
- **만드는 법**: z = (X_sat−X_ref)/√(u_sat²+u_ref²+σ_repr²) 계산, 분위별 실측 포함비율 집계(`numpy`), `matplotlib`로 u-plot(대각선 기준선). 신뢰구간은 부트스트랩.
- **함정·주의**: **σ_repr를 빼먹으면 z·곡선 해석이 왜곡**(2번 필수 결합). **기준자료 불확실성도 분모에 포함**해야 공정. 분포 꼬리(극단오차)는 별도 점검(u-plot은 중심부 위주). 임계 std(z)≈1은 advisory.
- **출처**: Merchant et al. (2019), "Satellite-based time-series of sea-surface temperature since 1981 for climate applications", *Scientific Data*, 6, 223, doi:10.1038/s41597-019-0236-x (ESA-CCI SST, 불확실성 동반 검증). 표준화오차/u-plot은 불확실성 검증 표준 관행. SST 불확실성 검증틀: Bulgin et al. (2016), *Remote Sensing of Environment* (확인요: 제목·권·페이지·DOI).

---

### 16. 정규화오차(z) QQ-plot·히스토그램 (정규화오차 QQ / Normalized-error QQ & z-Histogram)
- **무엇을 보여주나**: 불확실성으로 표준화한 오차 z = (X_sat−X_ref)/√(u_sat²+u_ref²+σ_repr²)의 분포가 **표준정규 N(0,1)**에 부합하는지를, (a) z의 정규 QQ-plot, (b) z 히스토그램 + N(0,1) 곡선 + std(z)·왜도·첨도로 진단. 15번 u-plot의 분포관점 보완.
- **읽는 법**: (a) QQ가 1:1 직선이면 z가 정규; **꼬리에서 위로 휘면** 극단오차 과다(불확실성 과소평가·heavy tail), 기울기≠1이면 전체 스케일 불일치. (b) 히스토그램 폭: **std(z)≈1 적정, >1 불확실성 과소평가, <1 과대평가**; 중심≠0이면 미보정 bias. **좋은 패턴**: 종모양·std≈1·꼬리 정상. **나쁜 패턴**: 두꺼운 꼬리·치우침.
- **언제 쓰나**: 불확실성 동반 위성/모델 자료. 검증목적=UQ 분포정합(특히 꼬리). 자료형: L2/L3 + 불확실성.
- **짝지표 & 교차링크**: std(z)·왜도·첨도·QQ 이탈(→ `12` 불확실성 검증; 15번 u-plot; [공통편 QQ/PIT]; `14` PIT/calibration). σ_repr는 2번.
- **만드는 법**: `scipy.stats.probplot`(정규 QQ), `matplotlib hist`+`scipy.stats.norm.pdf` 오버레이, `scipy.stats`로 std/skew/kurtosis. 꼬리 강조 시 분위 확대.
- **함정·주의**: **σ_repr·기준자료 불확실성 누락 시 z 왜곡**(15번과 동일). 대표본에서는 사소한 비정규도 검정상 유의(효과크기·꼬리 위주로 판단). 정규성 자체보다 **std(z)·꼬리**가 실무적으로 중요. 단일 그림 금지 — 15번과 함께.
- **출처**: Merchant et al. (2019), *Scientific Data*, 6, 223, doi:10.1038/s41597-019-0236-x. 표준화오차·정규 QQ·PIT는 불확실성/확률 검증 표준(Wilks, *Statistical Methods in the Atmospheric Sciences*; 예보검증 PIT 관행).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → `12` 교차링크

| # | 그림 (국문 / English) | 자료형·처리수준 | 검증목적 | 핵심 짝지표 | `12` 메서드 카드 교차링크 |
|---|---|---|---|---|---|
| 1 | 매치업 밀도 산점도 / Matchup density scatter | 트랙·격자·시계열 (L2~L4) | 정확도·편향 | bias·RMSD·robust SD·r·Type-2 slope | 매치업 통계지표 / 시공간 매칭 |
| 2 | 대표성오차·SFV / Representativeness error | L2/L3 고해상→점 | 오차예산 공정성 | σ_repr·sub-footprint variability | 대표성오차·서브풋프린트 변동 |
| 3 | TC 오차분산 / Triple collocation variance | 트랙·격자·시계열 | 참값 없이 정확도 순위 | σ_ε(±CI)·α·β | 삼중대조(TC) |
| 4 | ETC SNR·요약 / ETC SNR diagram | 트랙·격자·시계열 | 잡음+신호민감도 | ρ²_{T,Xi}·SNR | 확장 삼중대조(ETC) / 사중대조(QC) |
| 5 | along-track vs gridded / Altimetry track vs grid | 궤도 L3 vs 격자 L4 | 정확도+소규모 신호 | 궤도 RMSD·분산설명도·상관 | 고도계 along-track vs gridded |
| 6 | 파수 스펙트럼·유효해상도 / Wavenumber spectrum | along-track | 유효해상도·소규모 변동 | λ_p·기울기·coherence | 고도계 파수 스펙트럼·유효해상도 |
| 7 | 교차점 차이 / Crossover difference | 궤도 (asc/desc) | 위성 자체정합성 | Δ 편차·SD | 궤도/스와스 처리·교차점 분석 |
| 8 | L2/L3/L4 비교 / SST processing levels | 수온 격자 L2~L4 | 처리수준 정확도·적합성 | bias·robust SD·SQUAM | 위성 SST L2/L3/L4(GHRSST) |
| 9 | skin–bulk·diurnal / Skin–bulk & diurnal | SST L2/L3 + 부이 | 깊이·시각 정합(가짜 bias 제거) | skin−bulk·일주진폭 ΔSST | Skin/Bulk·일주변동 보정 |
| 10 | SST 전선·경도 / SST front & gradient | 고해상 L2/L3 격자 | 패턴·구조(전선) | 경도분포·전선위치 변위·FP | SST 전선·수평경도 검증 |
| 11 | 풍 벡터 비교 / Wind vector comparison | 해상풍 swath·격자 | 벡터 정확도(속도+방향) | 풍속 RMSD·원형 풍향 RMSD·u/v | 산란계 해상풍 검증 |
| 12 | rain flag·조건부 편차 / Rain-flag bias | 해상풍 L2 swath | 플래그 유효성·조건의존 오차 | flag별 bias/RMSD·조건부 히트맵 | 산란계 해상풍 검증 |
| 13 | Chl-a log10 산점 / Ocean color log10 matchup | 해색 격자 + 현장 | 정확도·편향(대수공간) | log10 MdAE·bias·slope | 해색 Chl-a 검증(Bailey–Werdell/Zibordi) |
| 14 | L2→L3 비닝 / Swath binning | swath→격자 L3 | 스케일 정합·표본 충분성 | 빈 표본수·격자내 분산 | L2→L3 비닝·격자화 |
| 15 | u-plot / Uncertainty u-plot | 불확실성 동반 L2/L3 | UQ 신뢰성(보정) | coverage·std(z) | 불확실성 정합 검증(u-plot) |
| 16 | 정규화오차 QQ / Normalized-error QQ | 불확실성 동반 L2/L3 | UQ 분포정합(꼬리) | std(z)·왜도·첨도·QQ 이탈 | 불확실성 정합 검증(표준화오차) |

> **횡단(공통편) 참조**: Taylor 다이어그램·target 다이어그램(Jolliff et al. 2009, doi:10.1016/j.jmarsys.2008.03.011)·일반 QQ/CDF·오차장 지도·객체기반(SAL/MODE)은 [공통편]에서 다룬다. 본 위성편은 위 16개 위성특화 그림에 한정하며, 공통 그림은 각 카드의 "짝지표 & 교차링크"에서 연결만 한다.

---

## 출처 (References) — 본 위성편에서 인용한 1차 출처

> 서지(저자·연도·저널·DOI)를 **웹 검색으로 확인한 것**만 확정 표기. 미확인 세부는 "(확인요)". DOI를 지어내지 않았다. 논문 그림은 복제하지 않고 유형·사양만 기술했다.

**콜로케이션·오차구조 (TC/ETC/QC·대표성)**
- Stoffelen, A. (1998). Toward the true near-surface wind speed: Error modeling and calibration using triple collocation. *JGR: Oceans*, 103(C4), 7755–7766. doi:10.1029/97JC03180.
- McColl, K. A., et al. (2014). Extended triple collocation. *Geophysical Research Letters*, 41, 6229–6236. doi:10.1002/2014GL061322.
- Vogelzang, J., & Stoffelen, A. (2021). Quadruple Collocation Analysis of In-Situ, Scatterometer, and NWP Winds. *JGR: Oceans*, 126, e2021JC017189. doi:10.1029/2021JC017189.
- Gruber, A., et al. (2016). Recent advances in (soil moisture) triple collocation analysis. *Int. J. Applied Earth Obs. Geoinformation*, 45, 200–211. doi:10.1016/j.jag.2015.09.002.
- Siu, L. W., et al. (2024). Summarizing multiple aspects of triple collocation analysis in a single diagram. *Frontiers in Remote Sensing*, 5. doi:10.3389/frsen.2024.1395442.
- The Impact on Triple/N-Way Collocation-Based Validation … Due to Non-Ideal Error Statistics. *Remote Sensing* (2025). doi:10.3390/rs17223751.
- Janjić, T., et al. (2018). On the representation error in data assimilation. *QJRMS*, 144, 1257–1278. doi:10.1002/qj.3130.
- Spatial Scales of Sea Surface Salinity Subfootprint Variability in the SPURS Regions. *Remote Sensing* (2020). doi:10.3390/rs12233996.

**고도계 (Altimetry)**
- Ballarotta, M., et al. (2019). On the resolutions of ocean altimetry maps. *Ocean Science*, 15, 1091–1109. doi:10.5194/os-15-1091-2019.
- Dufau, C., et al. (2016). Mesoscale resolution capability of altimetry. *JGR: Oceans*, doi:10.1002/2015JC010904 (확인요: 권·페이지).
- Evaluation of gridded sea surface height products based on along-track altimeter data. *Intelligent Marine Technology and Systems* (Springer, 2026). doi:10.1007/s44295-026-00092-9.
- Validation of Sea Level Anomalies from the SWOT Altimetry Mission … East Asia and the US West Coast. *Water* (2025), 17(21), 3066. doi:10.3390/w17213066.
- Copernicus Marine(CMEMS) SEALEVEL L4 제품·QUID; AVISO/CMEMS 고도계 처리·교차점 핸드북 (확인요: 구체 서지).

**SST (GHRSST)**
- GHRSST Data Specification·Task Team 문서 (ghrsst.org).
- Dash, P., et al. (2010). The SST Quality Monitor (SQUAM). *J. Atmos. Oceanic Technol.*, 27, 1899–1917. doi:10.1175/2010JTECHO756.1.
- Xu, F., & Ignatov, A. (2014). In situ SST Quality Monitor (iQuam). *J. Atmos. Oceanic Technol.*, 31, 164–180. doi:10.1175/JTECH-D-13-00121.1.
- Embury, O., Merchant, C. J., & Corlett, G. K. (2012). A reprocessing for climate of SST from ATSR … skin and diurnal variability effects. *Remote Sensing of Environment*, 116, 62–78. doi:10.1016/j.rse.2011.02.028.
- Merchant, C. J., et al. (2019). Satellite-based time-series of SST since 1981 for climate applications. *Scientific Data*, 6, 223. doi:10.1038/s41597-019-0236-x.
- Bulgin, C. E., et al. (2016). (SST 불확실성 검증/robust discrepancy) *Remote Sensing of Environment* (확인요: 제목·권·페이지·DOI).
- SST 정의(skin/sub-skin/foundation)·cool-skin/diurnal: GHRSST 규격; Donlon et al. 관련 (확인요: 구체 서지).

**전선·공간·객체 검증**
- Cayula, J.-F., & Cornillon, P. (1992). Edge Detection Algorithm for SST Images. *J. Atmos. Oceanic Technol.*, 9, 67–80 (확인요: 권·페이지·DOI 표기).
- Gilleland, E., et al. (2009). Intercomparison of Spatial Forecast Verification Methods. *Weather and Forecasting*, 24, 1416–1430. doi:10.1175/2009WAF2222269.1.
- Wernli, H., et al. (2008). SAL—A Novel Quality Measure … *Monthly Weather Review*, 136, 4470–4487. doi:10.1175/2008MWR2415.1.

**산란계 해상풍 (Scatterometer)**
- Characterizing the Effect of Ocean Surface Currents on ASCAT Winds Using Open Ocean Moored Buoy Data. *Remote Sensing* (2023), 15(18), 4630. doi:10.3390/rs15184630.
- Yang, X., et al. (2019). Comparison of Oceansat-2 Scatterometer Wind Data with Global Moored Buoys and ASCAT. *Advances in Meteorology*, 2019, 1651267 (확인요: DOI).

**해색 (Ocean Color)**
- Bailey, S. W., & Werdell, P. J. (2006). A multi-sensor approach for the on-orbit validation of ocean color satellite data products. *Remote Sensing of Environment*, 102(1–2), 12–23. doi:10.1016/j.rse.2006.01.015.
- Zibordi, G., et al. (2009). Validation of satellite ocean color primary products at optically complex coastal sites. *Remote Sensing of Environment*, 113(12), 2574–2591. doi:10.1016/j.rse.2009.07.016.
- Zibordi, G., et al. (2009). AERONET-OC: A Network for the Validation of Ocean Color Primary Products. *J. Atmos. Oceanic Technol.*, 26, 1634–1651. doi:10.1175/2009JTECHO654.1.

**처리·요약 다이어그램·시각화 도구**
- NASA Ocean Color — Level-3 Integerized Sinusoidal Binning Scheme (oceancolor.gsfc.nasa.gov). NASA SeaDAS — Level 3 Binning Operator (seadas.gsfc.nasa.gov).
- Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single diagram. *JGR: Atmospheres*, 106(D7), 7183–7192. doi:10.1029/2000JD900719. (공통편 — 교차참조)
- Jolliff, J. K., et al. (2009). Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment (target diagram). *Journal of Marine Systems*, 76, 64–82. doi:10.1016/j.jmarsys.2008.03.011. (공통편 — 교차참조)
- Thyng, K. M., et al. (2016). True colors of oceanography: Guidelines for effective and accurate colormap selection (cmocean). *Oceanography*, 29(3), 9–13. doi:10.5670/oceanog.2016.66.

**표준 참고문헌 (교과서)**
- Wilks, D. S. *Statistical Methods in the Atmospheric Sciences*. (매치업·robust 통계·QQ/KS·PIT 표준)
- Jolliffe, I. T., & Stephenson, D. B. *Forecast Verification: A Practitioner's Guide*. (범주·이상치상관·검증 일반)
