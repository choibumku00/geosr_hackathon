# 16. 검증 시각화 카탈로그 — 공통·횡단편 (Verification Figures: Common / Cross-cutting)

수치모델 결과를 관측·재분석(ERA5/GLORYS)·위성(L4)과 비교·검증할 때, **모든 도메인이 공통으로 끌어 쓰는 그림 유형 + AI/ML 평가 그림**을 모은 **그림 카드(figure card)** 카탈로그다. 도메인 특화 그림(파랑 스펙트럼·T-S 다이어그램·조류타원 등)이 아니라, 정확도·공간패턴·범주/확률·스펙트럼/모달·시계열·영상품질을 가로지르는 **횡단(cross-cutting) 시각화**를 다룬다. 각 카드는 수치지표 카탈로그 `01–15`의 메서드 카드와 **짝**을 이루며(그림은 "어디서·어떻게 틀렸나"를, 지표는 "얼마나 틀렸나"를 보여 줌), `00_overview_taxonomy.md` **G절 검증 함정**을 캡션 가이드에 강제 반영한다.

> **이 파일을 읽는 법**: 그림 카드 = 시각화 1종(또는 한 가족). 각 카드 8항목(무엇을·읽는 법·언제·짝지표&교차링크·만드는 법·함정·출처). 문서 끝에 **"그림 → 검증목적 → 짝지표 → 01–15 교차링크" 요약표**.

> ⚠️ **모든 그림 캡션에 강제할 3원칙(00 G절)**
> ① **기준자료 ≠ 참값**: ERA5/GLORYS/위성 L4는 reference이지 truth가 아니다. 축·범례·캡션에 "모델 − 기준(reference)"으로 표기하고 "오차"라 단정하지 않는다. ② **해석 임계는 advisory**: `SI<0.15`, `ACC≥0.6`, `FSS useful-scale` 등은 변수·해역·해상도·기준자료 의존 → "참고선"으로만 그리고 영역·해상도 의존 경고를 동반. ③ **단일 그림 금지**: 그림 1장으로 결론내지 않는다. 최소 (정확도 + 편향 + 패턴/분포) + 유의성을 함께 본다.

---

## A. 정확도·오차 그림 (Accuracy / error)

### 산점도·회귀선·밀도산점도 (Scatter plot with regression / Density (hexbin) scatter)
- **무엇을 보여주나**: 짝지어진(co-located) 모델값 f 와 기준값 o 의 1:1 관계. 점별 분포·조건부 편향(증폭/감쇠)·이상치·포화(saturation)를 한눈에. 표본이 많으면 점이 겹쳐 보이지 않으므로 **밀도(2D 히스토그램·hexbin·gaussian KDE)** 로 음영화한다.
- **읽는 법**: 가로 o(기준), 세로 f(모델). **y=x 1:1선**(검정 점선)과 **OLS 회귀선**(+식·R²)을 겹쳐 그림. 좋은 결과 = 점운(point cloud)이 1:1선에 좁게 밀착, 회귀 기울기≈1·절편≈0. 나쁜 결과 = 기울기<1(고값 과소·저값 과대 = 회귀희석/평활), 절편≠0(계통편향), 부채꼴 퍼짐(이분산), 상·하단 직선벽(센서 포화·물리한계 절단). 색은 점밀도(log scale 권장).
- **언제 쓰나**: 자료형 = 점·시계열(부이/검조소 CSV) 또는 격자-격자 매칭 표본. 검증목적 = **정확도·조건부 편향**의 1차 진단. 거의 모든 recipe의 출발 그림.
- **짝지표 & 교차링크**: RMSE·MAE·bias·Pearson r·R²·회귀 기울기/절편·SI(→`01`). 분포 꼬리는 QQ-plot으로 보완. → `01_error_statistics.md`(RMSE·상관·회귀 기울기/절편), `15`(co-location 전제).
- **만드는 법**: `matplotlib` `ax.scatter` / `ax.hexbin(o, f, gridsize=, bins='log', mincnt=1)` / `ax.hist2d`; KDE는 `scipy.stats.gaussian_kde`. 회귀선 `numpy.polyfit(o,f,1)` 또는 `scipy.stats.linregress`(slope·intercept·r). 1:1선 `ax.axline((0,0),slope=1)`. 축 동일 범위 + `ax.set_aspect('equal')`.
- **함정·주의**: ① **OLS는 x(기준) 무오차 가정** — 기준자료도 오차가 있으므로 기울기가 1보다 작게 편향(regression dilution); 변수오차 모델(orthogonal/Deming, total least squares)이나 RMA를 함께 고려. ② r·기울기는 이상치에 민감 → robust(Theil-Sen) 병기. ③ 강수·Chl-a 등 lognormal 변수는 log축. ④ 점밀도 없는 산점도는 표본 많을 때 과밀구간을 못 보여 줌.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (상관·회귀·진단 플롯); Jolliffe & Stephenson, *Forecast Verification* (연속변수 진단); Stow et al. (2009) *J. Marine Systems* (해양모델 skill 시각화 — 회귀희석 논의).

---

### 분위수-분위수 그림 (Quantile–Quantile plot, QQ-plot)
- **무엇을 보여주나**: 두 표본(모델 vs 기준)의 **분포 형태**가 같은지 — 특히 **꼬리(tail)**. 같은 누적확률에 해당하는 분위수끼리 짝지어 그려, 평균·분산뿐 아니라 왜도·첨도·극값 거동의 불일치를 드러낸다.
- **읽는 법**: 가로 = 기준 분위수, 세로 = 모델 분위수, y=x선 겹침. 좋은 결과 = 점들이 1:1선 위에 직선. 나쁜 결과 = **상단 꼬리가 1:1선 아래로 휘면 모델이 극값 과소(고파·고수온·호우 underestimate)**, 위로 휘면 과대; 전체가 평행이동=위치편향, 기울기≠1=분산(스케일)차; S자=왜도차. 끝점(최대 분위수)에서 표본이 적어 변동 큼.
- **언제 쓰나**: 자료형 = 점·격자 무관(분포 비교는 짝짓기 불필요해도 됨). 검증목적 = **분포·꼬리·극값**. 강수·파고·풍속·수온 극값, AI emulator의 분포 보존 점검에 표준.
- **짝지표 & 교차링크**: Perkins skill score·KS 거리·Wasserstein·return level·SI; 분위수매핑(QM/QDM) 편향보정의 사전·사후 진단. → `01`(분포 비교), `03_categorical_event_extremes.md`(GEV/POT·return level), `14_ai_ml_evaluation.md`(KS distance / Q-Q fit, QM/QDM 평가), `13`(quantile mapping).
- **만드는 법**: `numpy.quantile(x, p)` 로 공통 확률격자 p(예: 0.01~0.99 + 0.999) 분위수 계산 후 `ax.scatter`; 또는 `scipy.stats.probplot`(이론분포 대비), `statsmodels.graphics.gofplots.qqplot_2samples`. 극값 강조는 p를 꼬리에 조밀하게.
- **함정·주의**: ① 꼬리 끝 분위수는 표본수에 민감 — 신뢰구간(부트스트랩) 병기 권장. ② 두 표본 길이가 다르면 공통 확률격자에서 보간(선형 vs Hazen plotting position 선택 명시). ③ 분포가 같아도 **시간 위상은 검증 못 함**(QQ는 순서 무관) → 시계열 overlay와 병행. ④ 기준자료 꼬리도 불확실(위성·재분석 극값 과소 가능) → "기준 대비 상대"로 해석.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (분위수·확률그림); Wilk & Gnanadesikan (1968) *Biometrika* "Probability plotting methods for the analysis of data"(원리); Perkins et al. (2007) PDF skill score(분포 비교 맥락).

---

### 오차·잔차 히스토그램 (Error / residual histogram)
- **무엇을 보여주나**: 오차 e = f − o 의 분포. 중심(편향)·폭(산포)·대칭성·이중봉(레짐 혼합)·이상치를 본다. 단일 RMSE 숫자가 가린 오차의 **형태**를 드러낸다.
- **읽는 법**: 가로 = 오차(물리단위), 세로 = 빈도/밀도, x=0 수직선. 좋은 결과 = 0 중심·좁은 단봉·대칭(≈정규). 나쁜 결과 = 중심이 0에서 벗어남(편향), 긴 한쪽 꼬리(비대칭 오차·드문 큰 오차), 이중봉(주·야 또는 계절 레짐 혼합), 두꺼운 꼬리(이상치). KDE 곡선·정규근사 겹침으로 비교.
- **언제 쓰나**: 자료형 = 점·격자 모두(격자는 전 격자점 오차 모음). 검증목적 = **편향·산포·오차구조 진단**. 오차가 비정규면 RMSE·정규기반 신뢰구간 해석에 주의 신호.
- **짝지표 & 교차링크**: bias·RMSE·MAE·표준편차·왜도/첨도; RMSE 분해(systematic/unsystematic). → `01`(ME/bias·RMSE 분해·ubRMSE), `06`(잔차 백색성·ACF).
- **만드는 법**: `ax.hist(e, bins=, density=True)`; KDE `seaborn.histplot(..., kde=True)` 또는 `scipy.stats.gaussian_kde`; 정규근사 `scipy.stats.norm.pdf`. 왜도/첨도 `scipy.stats.skew/kurtosis`, 정규성 `scipy.stats.shapiro/normaltest`(advisory).
- **함정·주의**: ① bin 폭이 형태를 좌우(Freedman–Diaconis 권장). ② 격자 오차 모음은 **공간 자기상관**으로 유효표본이 작음 → 히스토그램의 통계적 폭을 과신 금지. ③ 면적가중(cosφ) 누락 시 고위도 과대표집. ④ 오차 ≠ "모델 오차": 기준자료 오차 포함된 차이.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification* (오차 분포·진단).

---

### 테일러 다이어그램 (Taylor diagram)
- **무엇을 보여주나**: 여러 모델/실험을 한 점씩 찍어, **상관계수 R·표준편차비(σ_f/σ_o)·중심화 RMS차(CRMSD)** 세 통계를 동시에 요약. 코사인 법칙(CRMSD² = σ_f² + σ_o² − 2σ_fσ_o R)으로 세 양이 한 평면에 기하학적으로 공존.
- **읽는 법**: 방사거리 = 표준편차(또는 σ_f/σ_o로 정규화), 방위각 = arccos(R), 기준점("REF", R=1·정규σ=1)까지의 직선거리 = CRMSD. 좋은 결과 = 점이 REF에 가까움(R→1, σ비→1, CRMSD→0). 나쁜 결과 = 큰 각도(낮은 상관), 반지름 1 밖/안(분산 과대/과소). 여러 변수·계절·모델을 색/마커로 구분.
- **언제 쓰나**: 자료형 = 격자장·시계열·스펙트럼/모드 계수. 검증목적 = **패턴 일치 종합요약·다모델 랭킹**. 공통 recipe의 "종합 요약" 단계 표준 그림.
- **짝지표 & 교차링크**: R·CRMSD(=ubRMSE)·표준편차비. **편향(bias)은 안 보임** → target diagram·bias map과 반드시 병행. → `01`(Taylor diagram & TSS), `02`(공간 Taylor), `05/06`(스펙트럼·모드 Taylor), `13/14`(다모델·AI Taylor). 00 D절: **단일 구현 + 평균제거**.
- **만드는 법**: `skill_metrics`(SkillMetrics: `sm.taylor_diagram`), 또는 직접 — `matplotlib` polar축 + `cartopy` 불필요; 통계는 `xskillscore`(`pearson_r`, `std`) / `numpy`. 정규화(σ_f/σ_o) 옵션·다중점 라벨링.
- **함정·주의**: ① **bias를 보여주지 못함**(평균 제거 후 패턴만) → 단독 사용 시 계통편향 모델이 좋아 보일 수 있음. ② 표준편차비는 분산만 — 분포 형태·꼬리 무관. ③ 음의 상관은 표준 반원(0–90°)에 안 들어옴(확장 다이어그램 필요). ④ 면적가중·결측마스크 통일 필수. ⑤ "REF"는 reference이지 truth 아님.
- **출처**: Taylor, K. E. (2001) *J. Geophys. Res.* 106(D7):7183–7192, **DOI 10.1029/2000JD900719**; Taylor (2005) *Taylor Diagram Primer* (PCMDI/LLNL).

---

### 타깃 다이어그램 (Target diagram)
- **무엇을 보여주나**: Taylor가 못 보여주는 **편향(bias)의 부호·크기**를 전면에 세운 그림. 총 RMSD를 **편향(MBE)** 과 **불편 RMSD(uRMSE=CRMSD)** 로 분해해 하나의 점으로 표현.
- **읽는 법**: 세로축 = 편향(bias, MBE), 가로축 = **부호 부여 uRMSE**(uRMSE × sign(σ_f−σ_o); 모델 분산이 작으면 음). 원점에서 점까지 거리 = 총 RMSD. 동심원(예: RMSD=1 정규화 원)으로 등급. 좋은 결과 = 원점 근처. 위/아래 = 과대/과소 편향; 좌/우 = 모델이 기준보다 변동 작음/큼. 사분면으로 편향+분산오차 유형 즉시 분류.
- **언제 쓰나**: 자료형 = 격자·시계열. 검증목적 = **편향+산포 동시·다변수/다지점 비교**. 해양·생지화학 모델 종합평가(Jolliff)에서 표준. Taylor와 **짝**으로 보고.
- **짝지표 & 교차링크**: MBE/bias·uRMSE(=ubRMSE/CRMSD)·총 RMSD·σ비. → `01`(bias·CRMSD·ubRMSE), Taylor 카드와 병행. → `09/12`(해양·위성 종합평가).
- **만드는 법**: `skill_metrics`(`sm.target_diagram`); 통계는 `numpy`/`xskillscore`로 bias·CRMSD·σ 계산 후 부호 부여. RMSD 정규화(÷σ_o) 옵션.
- **함정·주의**: ① 가로축 부호 규약(σ_f−σ_o 또는 R 기반)이 구현마다 다름 — 캡션에 명시. ② 정규화 기준(σ_o)이 변수·지점마다 다르면 비교 시 통일. ③ 위상오차는 uRMSE에 섞여 보임(분리 안 됨). ④ 점 개수 많으면 색/심볼 체계 필요.
- **출처**: Jolliff, J. K., et al. (2009) "Summary diagrams for coupled hydrodynamic-ecosystem model skill assessment", *J. Marine Systems* 76:64–82, **DOI 10.1016/j.jmarsys.2008.05.014**.

---

## B. 공간 패턴 그림 (Spatial pattern)

### 편차·차이 지도 (Bias / difference map)
- **무엇을 보여주나**: 격자별 (모델 − 기준) 차이장 또는 시간평균 편차장. "어디서" 모델이 과대/과소인지의 **공간 구조**(연안·전선대·산악·서안경계류 등)를 직접 보여 주는, 모든 공간검증의 출발 그림.
- **읽는 법**: 발산형(diverging) 컬러맵, **0에서 흰색**, 대칭 범위(±vmax). 빨강=양(과대)·파랑=음(과소). 좋은 결과 = 전역 옅은 색·구조 없는 잡음. 나쁜 결과 = 넓은 동색 영역(계통편향), 전선·해안 따라 쌍극자(위치 어긋남 = double penalty 신호), 격자/봉합선 따라 줄무늬(재격자 아티팩트). RMSE/MAE 지도(비음수 sequential맵)와 병치.
- **언제 쓰나**: 자료형 = 격자-격자. 검증목적 = **편향의 공간분포·구조진단**. ERA5/GLORYS/위성 L4 대비 1차 그림.
- **짝지표 & 교차링크**: 격자별 ME/bias·RMSE·MAE·CRMSD(영역요약). → `02_spatial_pattern_verification.md`(격자별 오차장 RMSE/MAE/Bias 지도), `15`(재격자·마스크 정합).
- **만드는 법**: `xarray`(`(model-ref).plot`) + `cartopy`(`ccrs.PlateCarree`, coastlines); 발산맵 `cmocean.cm.balance` 또는 `RdBu_r`, `TwoSlopeNorm(vcenter=0)`. 면적가중 통계는 `xarray.weighted(np.cos(np.deg2rad(lat)))`.
- **함정·주의**: ① **재격자 순서/방식이 차이장을 바꿈** — 모델·기준에 동일 보간(가능하면 보존적) 강제(`15`). ② 컬러맵 비대칭/비발산이면 시각적 거짓편향. ③ 차이 = "모델−기준"이지 모델오차 아님(기준 오차 포함). ④ 마스크(land-sea·결측) 양쪽 통일 안 하면 가짜 경계.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification* (이중벌점); Stow et al. (2009) *J. Marine Systems*.

---

### 패턴상관·이상상관(ACC) 지도 (Pattern correlation / Anomaly Correlation map)
- **무엇을 보여주나**: 공간 패턴의 닮음. (a) 시간에 따른 **공간 ACC 시계열/리드타임 곡선**(예보 스킬 감쇠), 또는 (b) 격자별 **국소 시간상관 지도**(어디서 변동 위상이 맞나). 평균편향·진폭에는 둔감, **패턴·위상**에 민감.
- **읽는 법**: (a) 가로 = 리드타임/시간, 세로 = ACC(0~1), **0.6 참고선**(advisory). 좋음 = 오래 0.6 위 유지. (b) 지도: 1에 가까운 영역=위상 잘 맞음, 0/음수=무상관/역위상(연안·전선대에서 흔히 낮음). 발산맵(−1~1).
- **언제 쓰나**: 자료형 = 격자장(시계열 차원 필요). 검증목적 = **패턴·위상**. 기상(지위고도·기온), 해양(SST·SSH·해류 패턴), 계절예측. ERA5/GLORYS 대비 표준.
- **짝지표 & 교차링크**: ACC·패턴상관·S1 gradient score; RMSE·bias map과 병행(ACC는 진폭·편향 못 봄). → `02`(패턴상관/ACC), `01`(ACC 정의), `07/09/12/13`(도메인 ACC). 00 D절: **동일 climatology 강제**.
- **만드는 법**: 이상장 = 자료 − 동일 기준기간 climatology(`xarray.groupby('time.month').mean()`); 공간 ACC `xskillscore.pearson_r(f', o', dim=['lat','lon'], weights=cosφ)`; 국소상관 `xs.pearson_r(dim='time')`. cosφ 면적가중 필수.
- **함정·주의**: ① **climatology 정의(기준기간·격자)가 양쪽에 동일**해야 — 다르면 가짜 ACC. ② ACC≥0.6은 ECMWF 종관 관행값일 뿐, **변수·해역·해상도 의존 advisory**. ③ 편향·진폭오차를 못 봄 → 단독 금지. ④ 작은 영역·강한 국지패턴엔 둔감.
- **출처**: ECMWF Forecast User Guide §6.2.2 (ACC); Wilks, *Statistical Methods in the Atmospheric Sciences*; Jolliffe & Stephenson, *Forecast Verification*.

---

### FSS 공간검증 맵·히트맵 (Fractions Skill Score map / scale–threshold heatmap)
- **무엇을 보여주나**: 이웃(neighborhood) 기반 분율 일치를 **이웃크기(스케일) × 임계값** 격자로 펼친 히트맵. 이중벌점을 완화해 "**어느 공간 스케일부터 예보가 유용한가**(useful scale)"를 정량화.
- **읽는 법**: 가로 = 이웃반경/스케일(km 또는 격자수), 세로 = 강도 임계(예: 강수 1·5·10 mm), 색 = FSS(0~1). **FSS = 0.5 + f₀/2**(f₀=기준 사건빈도) 등치선이 useful-scale 경계. 좋은 결과 = 작은 스케일부터 FSS가 0.5+f₀/2 초과(녹색). 나쁜 결과 = 큰 스케일에서도 낮음(위치·강도 모두 틀림). 곡선형(FSS vs scale, 임계 고정)으로도 그림.
- **언제 쓰나**: 자료형 = 격자장(특히 강수·반사도·구름 등 불연속·고해상도). 검증목적 = **공간 패턴·스케일별 유용성**. 고해상도/AI 강수예보 검증 표준.
- **짝지표 & 교차링크**: FSS·useful scale·이웃검증; double-penalty 진단과 짝. → `02`(FSS), `03`(공간/근접 검증), `07`(강수 FSS), `14`(이웃검증·double penalty). 00 D절: **임계·이웃 스캔 공통, useful=0.5+f₀/2**.
- **만드는 법**: `xskillscore`에는 직접 FSS 없음 → `pysteps.verification.spatialscores.fss`(+ `fss_init/accum`) 또는 `scores`(`scores.spatial.fss_2d`); 히트맵 `matplotlib.pcolormesh`/`seaborn.heatmap`. 임계·스케일 리스트 스캔.
- **함정·주의**: ① FSS는 **결정론적 단일장 비교** — 앙상블이면 멤버별/확률화 별도. ② 도메인 가장자리·결측이 이웃합을 왜곡(패딩 규약 명시). ③ useful-scale 임계는 f₀ 의존 → 사건 드물면 기준선이 낮아져 "쉬워" 보임. ④ 강도 임계·이웃 정의가 결과를 좌우 → 스캔·고정 명시.
- **출처**: Roberts, N. M., & Lean, H. W. (2008) "Scale-Selective Verification of Rainfall Accumulations...", *Mon. Wea. Rev.* 136:78–97, **DOI 10.1175/2007MWR2123.1**.

---

### 객체기반 SAL·MODE 플롯 (Object-based feature plots: SAL / MODE)
- **무엇을 보여주나**: 강수역·소용돌이·전선 등 **특징(객체)** 을 식별해 구조·진폭·위치를 비교. **SAL** = 한 사례를 (S,A,L) 한 점으로; **MODE** = 식별·매칭된 객체쌍을 지도 위에 색칠하고 속성(면적·중심거리·종횡비·각도) 비교.
- **읽는 법**: **SAL 산점도**: 가로 S(구조: 객체 크기/평탄도), 세로 A(진폭: 영역평균 차), 색/마커 L(위치: 질량중심·분산 차, 0~2). 좋음 = (0,0) 근처. A>0 과대·A<0 과소; S>0 모델이 너무 크고 평평; L 큼=위치 어긋남. **MODE 지도**: 매칭 객체 동일색, 미매칭(놓침/오경보) 강조색 + 객체 속성표.
- **언제 쓰나**: 자료형 = 격자장(불연속·국지 특징). 검증목적 = **패턴·구조·위치**(double penalty 회피, 진단적). 강수·대류·중규모 소용돌이·해양 eddy 검증.
- **짝지표 & 교차링크**: SAL(S,A,L)·MODE 객체속성·CSI/관심도(interest); FSS·bias map과 보완. → `02`(SAL·MODE·CRA), `03`(객체기반), `07/13`(강수 객체검증).
- **만드는 법**: MODE = `MET`(METplus, NCAR) 표준; Python 객체화는 `scipy.ndimage.label`(연결성분) + `skimage.measure.regionprops`(면적·중심·축); SAL은 임계·평활반경 정해 객체 식별 후 S·A·L 공식 계산(자체 구현/`pysteps` 보조).
- **함정·주의**: ① **객체화 파라미터(평활반경·임계)가 결과를 지배** — 명시·고정(00 D절). ② SAL의 S는 임계 민감, L은 객체 1개일 때 둔감. ③ MODE 매칭은 관심도(interest) 가중 선택에 의존. ④ 소수 사례 SAL 산점도는 일반화 금지. ⑤ "관측 객체"도 기준자료(레이더/위성) 오차 포함.
- **출처**: Wernli, H., et al. (2008) "SAL—A Novel Quality Measure...", *Mon. Wea. Rev.* 136:4470–4487, **DOI 10.1175/2008MWR2415.1**; Davis, C., et al. (2006) "Object-based verification (MODE)", *Mon. Wea. Rev.* 134:1772–1784 (DOI 확인요).

---

### Hovmöller 다이어그램 (Hovmöller / time–longitude(latitude) diagram)
- **무엇을 보여주나**: 한 축을 시간, 다른 축을 공간(경도 또는 위도, 한쪽으로 평균)으로 펼친 채움등고선. **전파(propagation)** 특징 — 위상속도(등치선 기울기)·동/서진·주기성 — 을 모델과 기준에서 나란히 비교.
- **읽는 법**: 가로 = 경도(또는 위도), 세로 = 시간(보통 아래로 진행), 색 = 변수/이상값. **등치선 기울기 = 위상속도**(기울기 부호=전파방향). 좋은 결과 = 모델·기준 패널에서 줄무늬의 기울기·간격(속도·파장·주기) 일치. 나쁜 결과 = 기울기 다름(속도오차), 줄무늬 흐림(전파신호 약함/과대확산), 주기 어긋남. 모델·기준·차이 3패널 권장.
- **언제 쓰나**: 자료형 = 격자장(시간×공간). 검증목적 = **위상·전파·변동전파구조**. 적도파·MJO·Rossby/Kelvin파·연안 트랩파·SSH 전파·강수대 이동 검증.
- **짝지표 & 교차링크**: 위상속도·lag 상관·k-ω 스펙트럼; 패턴상관과 보완. → `06`(위상·전파), `05`(k-ω 스펙트럼), `02`(공간패턴).
- **만드는 법**: `xarray`로 한 축 평균(`.mean('lat')`) 후 `xr.DataArray.plot.contourf(x='lon', y='time')`; 이상값은 climatology 제거. 발산맵·동일 levels로 모델/기준 통일.
- **함정·주의**: ① 평균 축 선택(위도대)·이상값 기준이 신호를 좌우 → 명시. ② 시간 비등간격·결측이 기울기를 왜곡(`15` 시간정합). ③ 색범위(levels) 모델·기준 동일 안 하면 가짜 차이. ④ 단일 경도대 평균은 비대칭 전파를 가릴 수 있음.
- **출처**: Hovmöller, E. (1949) "The Trough-and-Ridge diagram", *Tellus* 1(2):62–66, **DOI 10.1111/j.2153-3490.1949.tb01260.x**.

---

## C. 범주형·사건·확률 그림 (Categorical / event / probabilistic)

### 분할표 시각화 & 성능 다이어그램 (Contingency-table viz & Performance diagram, Roebber)
- **무엇을 보여주나**: 2×2 분할표(hit/miss/false-alarm/correct-neg)를 모자이크/열지도로, 그리고 **여러 분할표 지표(POD·SR(=1−FAR)·bias·CSI)를 한 평면에** 동시 표현하는 Roebber 성능 다이어그램. 정확도·편향·신뢰성·스킬을 한 그림에.
- **읽는 법**: **성능 다이어그램**: 가로 = 성공비 SR(=1−FAR), 세로 = POD; **곡선 등치선 = CSI**(우상단일수록 높음), **방사 직선 = frequency bias**(대각선=1, 위=과대예보·아래=과소). 좋은 결과 = 점이 우상단(POD↑·SR↑·CSI↑), 대각선(bias=1) 근처. 나쁜 결과 = 좌하단, 또는 bias선 1에서 크게 벗어남. 여러 임계/모델/리드타임을 점·궤적으로.
- **언제 쓰나**: 자료형 = 격자·시계열·위성(임계 이진화). 검증목적 = **범주형 사건검증 종합**(경보·호우·고파·고수온). 임계 스캔·다모델 비교에 강력.
- **짝지표 & 교차링크**: POD·FAR·SR·CSI·FBI·ETS/HSS·SEDI(드문사건). → `03`(분할표 전 지표·CSI·ETS·HSS), `14`(POD/FAR/CSI/ETS/HSS). 분할표는 ROC/reliability와 함께.
- **만드는 법**: 지표는 `xskillscore`(`xs.... ` 이진) 또는 직접 a,b,c,d 집계; 성능 다이어그램은 `matplotlib`로 CSI 등치선(`np.meshgrid` SR,POD → CSI=1/(1/SR+1/POD−1)) + bias 직선; `METplus`/`PyForecastTools`에도 구현.
- **함정·주의**: ① 분할표 단일지표(PC 등)는 **드문 사건에서 오도**(항상 'no'로 높은 PC) → CSI·SEDI 병행. ② 임계값·사건빈도 의존 — 임계 스캔 명시. ③ 표본 작으면 칸 0으로 일부 지표 발산. ④ 격자 자기상관으로 유효표본 과대 → 부트스트랩 CI.
- **출처**: Roebber, P. J. (2009) "Visualizing Multiple Measures of Forecast Quality", *Wea. Forecasting* 24:601–608, **DOI 10.1175/2008WAF2222159.1**; WWRP/WGNE JWGFVR(CAWCR) Forecast Verification 페이지(분할표 지표, 확인요); Wilks, *Statistical Methods*.

---

### ROC 곡선 (Relative Operating Characteristic curve / ROC, AUC)
- **무엇을 보여주나**: 확률예보를 여러 결정임계로 이진화했을 때 **탐지확률 POD(=hit rate)** 와 **오경보율 POFD(=false-alarm rate)** 의 트레이드오프. **판별력(discrimination)** — 사건/비사건을 구분하는 능력 — 을 측정(보정과 무관).
- **읽는 법**: 가로 = POFD(0~1), 세로 = POD(0~1), 대각선 = 무기술(AUC=0.5). 좋은 결과 = 좌상단으로 부풀어 오른 곡선(AUC→1). 나쁜 결과 = 대각선에 가까움. **곡선하면적 AUC**가 요약 스칼라. 여러 모델 곡선 겹쳐 비교.
- **언제 쓰나**: 자료형 = 확률예보(앙상블 빈도·확률모델)·이진사건. 검증목적 = **확률 판별력**. 경보·극값 확률예보, 분류기 평가에 표준.
- **짝지표 & 교차링크**: AUC·POD·POFD; **reliability diagram과 짝**(ROC=판별, reliability=보정 — 둘 다 필요). → `03`(ROC/AUC·Brier), `14`(ROC-AUC/PR-AUC). 드문사건은 PR곡선 병행.
- **만드는 법**: `sklearn.metrics.roc_curve`/`roc_auc_score`(이진 분류); 기상확률은 `xskillscore.roc`(`xs.roc(obs_binary, fcst_prob, bin_edges, return_results='all_as_metric_dim')`). 부트스트랩 CI 권장.
- **함정·주의**: ① ROC는 **보정을 보지 못함** — 잘못 보정된 예보도 높은 AUC 가능 → reliability와 병행. ② 매우 드문 사건엔 POFD가 둔감(항상 작음) → **Precision-Recall(PR)곡선**이 더 정보적. ③ 임계격자 거칠면 AUC 과소. ④ 사건빈도 다른 영역 간 AUC 직접비교 주의.
- **출처**: Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide* (ROC 장); Mason, S. J., & Graham, N. E. (2002) *Q. J. R. Meteorol. Soc.* (ROC·AUC, DOI 확인요); WMO/WWRP 검증 가이드.

---

### 신뢰도 다이어그램 & PIT 히스토그램 (Reliability diagram & PIT histogram)
- **무엇을 보여주나**: **보정(calibration/reliability)** — 예측확률(또는 예측분포)이 실제 빈도와 일치하는가. **Reliability**: 이진사건 확률예보의 예측확률 대 관측빈도; **PIT 히스토그램**: 연속·확률분포 예보의 분위수 일관성(관측이 예측 CDF의 어느 분위에 떨어지는가).
- **읽는 법**: **Reliability**: 가로 = 예측확률 구간, 세로 = 해당 구간 관측상대빈도, **1:1 대각선=완전보정**. 좋음 = 점들이 대각선. 대각선보다 아래=과신(overconfident), 위=과소신뢰; sharpness 막대(예측확률 분포)·표본수 병기. **PIT**: 평평=잘 보정; U자=과소산포(under-dispersive, spread 부족), 봉우리(∩)=과대산포, 기울기=편향.
- **언제 쓰나**: 자료형 = 확률(이진) 또는 분포/앙상블(연속) 예보. 검증목적 = **확률·UQ 보정**. 앙상블·후처리(EMOS)·AI 확률예보·회귀 UQ 평가.
- **짝지표 & 교차링크**: Brier 분해(reliability항)·ECE·sharpness·CRPS reliability; **ROC와 짝**(보정 vs 판별). → `03`(reliability·Brier), `14`(PIT/reliability·ECE·sharpness·conformal), `13`(앙상블 보정).
- **만드는 법**: Reliability = `sklearn.calibration.calibration_curve` 또는 기상용 `xskillscore`/`scores`; 일관성 막대 = Bröcker & Smith 부트스트랩. PIT = 앙상블이면 정규화 rank, 분포면 F(o) 계산 후 `ax.hist`. `properscoring`로 CRPS 병기.
- **함정·주의**: ① 구간(bin) 수·표본이 적으면 reliability가 잡음 → consistency bar 필수. ② PIT는 **시간 자기상관**에 민감(독립표본 가정). ③ 보정 좋아도 sharpness(예리함) 낮으면 쓸모 적음 → sharpness 병기. ④ ROC(판별)와 reliability(보정)는 **서로 보완** — 하나만으로 결론 금지.
- **출처**: Wilks, *Statistical Methods in the Atmospheric Sciences* (reliability·attributes diagram); Gneiting, T., Balabdaoui, F., & Raftery, A. E. (2007) "Probabilistic forecasts, calibration and sharpness", *J. R. Stat. Soc. B* 69(2):243–268, **DOI 10.1111/j.1467-9868.2007.00587.x**; Bröcker & Smith (2007) *Wea. Forecasting* (consistency bars, DOI 확인요).

---

### 순위 히스토그램 & 스프레드-스킬 도표 (Rank histogram (Talagrand) & Spread–skill plot)
- **무엇을 보여주나**: 앙상블의 **신뢰성·산포 적정성**. **Rank histogram**: 관측이 정렬된 앙상블 멤버들 사이 어느 순위에 들어가는지의 빈도; **Spread–skill**: 앙상블 spread(표준편차) 대 앙상블평균 RMSE의 관계(이상적으로 1:1).
- **읽는 법**: **Rank hist**: 가로 = 순위(1…N+1), 세로 = 빈도, **평평=잘 보정**. U자=과소산포(spread 부족, 관측이 자주 양끝), ∩(돔)=과대산포, 한쪽 경사=편향. **Spread–skill**: 가로 = binned spread, 세로 = RMSE, **y=x 참고선**. 좋음 = 점들이 1:1선. 1:1 아래(RMSE>spread)=under-dispersive(과신).
- **언제 쓰나**: 자료형 = 앙상블 예보(앙상블축 존재). 검증목적 = **앙상블 신뢰성·산포 보정**. 모든 앙상블/확률 recipe의 트리거 그림.
- **짝지표 & 교차링크**: spread-skill ratio·CRPS reliability·rank 균일성 검정(χ²). PIT와 동치(연속극한). → `03`(rank histogram·spread-skill), `13/14`(앙상블 spread-skill·CRPS), reliability/PIT 카드와 가족.
- **만드는 법**: rank = 멤버보다 작은 관측 개수 + 무작위 동점처리 → `ax.hist`; spread = `ensemble.std('member')`, RMSE = `xskillscore.rmse(ens_mean, obs)`, spread bin별 평균; CRPS는 `properscoring.crps_ensemble`/`xskillscore.crps_ensemble`.
- **함정·주의**: ① **관측오차·대표성오차가 U자를 만들 수 있음**(진짜 과소산포와 혼동) → 관측오차 반영. ② 멤버수 적으면 bin 잡음·동점처리 규약 영향. ③ 평평해도 **공간/시간 상관 무시 시 오판**(조건부 rank hist 권장). ④ spread-skill의 1:1은 필요조건이지 충분조건 아님.
- **출처**: Hamill, T. M. (2001) "Interpretation of Rank Histograms for Verifying Ensemble Forecasts", *Mon. Wea. Rev.* 129:550–560, **DOI 10.1175/1520-0493(2001)129<0550:IORHFV>2.0.CO;2**; Talagrand et al. (1997) ECMWF Workshop(원개념).

---

### 브라이어·CRPS 분해 그림 (Brier / CRPS decomposition plot)
- **무엇을 보여주나**: 확률점수를 **신뢰성(reliability)·해상도(resolution)·불확실성(uncertainty)** 성분으로 분해해 막대/누적으로 표시. "왜 점수가 그런가"(보정 문제인지 판별 문제인지)를 진단. CRPS는 연속판 Brier로, reliability·CRPS_potential로 분해.
- **읽는 법**: 막대 = REL(작을수록 좋음)·RES(클수록 좋음)·UNC(기준, 기후 변동성). BS = REL − RES + UNC. 좋은 결과 = REL≈0, RES 큼. 리드타임/임계별로 성분 추이를 그림. CRPS는 reliability(평탄도)·potential(완벽보정 시 한계) 분해를 곡선으로.
- **언제 쓰나**: 자료형 = 확률/앙상블 예보. 검증목적 = **확률 스킬의 원천 진단**. 후처리·보정 전후 비교, AI 확률예보 평가.
- **짝지표 & 교차링크**: Brier(+분해)·BSS·CRPS(+분해)·reliability diagram·rank hist. → `03`(Brier/BSS·CRPS), `14`(CRPS/fair-CRPS·Brier/BSS), reliability/rank-hist 가족.
- **만드는 법**: Brier 분해 = 확률 binning 후 Murphy(1973) 공식(직접 구현/`scores`); CRPS = `properscoring.crps_ensemble`/`crps_gaussian`, `xskillscore.crps_ensemble`; Hersbach 분해는 멤버별 누적. 막대 `ax.bar`.
- **함정·주의**: ① 분해는 **binning에 의존**(within-bin 변동 → 일반화된 분해/유효표본 보정). ② 표본 작으면 RES 추정 불안정. ③ UNC는 기준 기후변동성 — 영역·기간 바뀌면 BS 직접비교 주의 → **BSS**로 정규화. ④ CRPS는 단위(변수단위) 유지 — 변수 간 비교 시 정규화.
- **출처**: Hersbach, H. (2000) "Decomposition of the CRPS for Ensemble Prediction Systems", *Wea. Forecasting* 15:559–570, **DOI 10.1175/1520-0434(2000)015<0559:DOTCRP>2.0.CO;2**; Murphy, A. H. (1973) "A new vector partition of the probability score", *J. Appl. Meteor.* 12:595–600 (DOI 확인요).

---

### 재현수준 그림 & 분포비교(PDF/CDF/Perkins) (Return-level plot (GEV/POT) & PDF/CDF comparison)
- **무엇을 보여주나**: **극값·분포 전체**의 모델-기준 일치. **Return-level plot**: 재현주기(return period) 대 재현수준(return level)을 GEV(블록최대)·POT/GPD 적합으로(신뢰구간 포함). **PDF/CDF 비교**: 모델·기준 확률밀도/누적분포를 겹쳐, 겹침면적(Perkins skill score)으로 분포 유사도.
- **읽는 법**: **Return-level**: 가로 = 재현주기(log scale, 년), 세로 = 변수값, 점=경험분위(plotting position)·선=적합·음영=CI. 좋음 = 모델·기준 곡선·CI 중첩. 모델 곡선이 아래=극값 과소(고파·호우 underestimate). **PDF/CDF**: 겹칠수록 좋음; Perkins S(겹침면적, 0~1)=1 완전일치. 꼬리 차이 주목.
- **언제 쓰나**: 자료형 = 시계열·격자(극값 추출 후). 검증목적 = **분포·꼬리·극값·재현빈도**. 설계파/고수온/호우 재현빈도, AI 분포 보존, 기후통계 보존.
- **짝지표 & 교차링크**: GEV/GPD 매개변수·return level·CI·Perkins S·KS·Wasserstein. QQ-plot과 짝. → `03`(GEV/POT·return level), `14`(KS·Q-Q·기후통계 보존·Perkins), `08/11`(설계파·해일 재현빈도).
- **만드는 법**: 극값적합 `scipy.stats.genextreme`(GEV)·`scipy.stats.genpareto`(GPD), 전용 `pyextremes`(블록최대/POT·return level·CI 자동); CI는 프로파일우도/부트스트랩. PDF `scipy.stats.gaussian_kde`/`np.histogram`, CDF `np.sort`/`statsmodels` ECDF, Perkins S = `np.minimum(p_model,p_ref).sum()*Δx`.
- **함정·주의**: ① **declustering·임계선택(POT)·블록크기(GEV)가 결과 지배** — 공통 규약(00 D절). ② 짧은 기록의 긴 재현주기 외삽은 불확실 → CI 필수, **CI 중첩 = 유의차 없음**으로 해석(단정 금지). ③ 비정상성(추세) 있으면 정상 GEV 부적합. ④ 기준자료(위성/재분석) 극값도 과소 가능 → "기준 대비 상대". ⑤ Perkins S는 binning 의존.
- **출처**: Coles, S. (2001) *An Introduction to Statistical Modeling of Extreme Values* (GEV/GPD·return level·CI); Perkins, S. E., et al. (2007) "Evaluation of the AR4 Climate Models... using PDFs", *J. Climate* 20:4356–4376, **DOI 10.1175/JCLI4253.1**.

---

## D. 스펙트럼·EOF·모달 그림 (Spectral / EOF / modal)

### 파워·파수·k-ω 스펙트럼 & RAPSD/유효해상도 (PSD / wavenumber / k-ω spectra & RAPSD, effective resolution)
- **무엇을 보여주나**: 변동에너지의 **스케일별 분포**가 모델·기준에서 일치하는가. 시계열 **PSD**(주파수), 격자장 **파수 스펙트럼**·**RAPSD**(반경평균 2D 스펙트럼), **k-ω**(파수-주파수: 분산관계·전파). 모델이 고파수에서 에너지 과소(과대평활/blurry)인지, 분산관계가 맞는지.
- **읽는 법**: log-log. 가로 = 주파수/파수, 세로 = 스펙트럼밀도. 좋음 = 모델·기준 곡선이 관성영역 기울기(예 −5/3, −3)·에너지레벨·피크까지 겹침. 나쁨 = **고파수에서 모델이 급락(유효해상도 = 모델/기준 스펙트럼이 갈라지는 파장 → "유효해상도 ≈ 6–7Δx")**, 또는 고파수 에너지 과대(잡음). **k-ω**: 에너지가 이론 분산곡선(Kelvin·Rossby·중력파)을 따르는가.
- **언제 쓰나**: 자료형 = 시계열·격자장·트랙. 검증목적 = **변동모드·스케일·유효해상도·물리(분산관계)**. AI/다운스케일 산출물의 **이중벌점 보완 필수 그림**, 고도계 SSH 유효해상도.
- **짝지표 & 교차링크**: 스펙트럼 기울기·RAPSD·RALSD·유효해상도; FSS와 보완. → `05`(PSD·파수·k-ω·rotary), `02`(공간 파워스펙트럼), `14`(RAPSD/유효해상도·spectral fidelity), `06`(PSD). 00 D절: window·detrend·정규화 일치.
- **만드는 법**: PSD `scipy.signal.welch`; 2D/RAPSD `numpy.fft.fft2` 후 반경 binning(`pysteps.utils.rapsd`); k-ω = 시공간 2D FFT(`np.fft.fft2` on (x,t)) + 이론곡선(Wheeler-Kiladis); 스펙트럼 Taylor 보조.
- **함정·주의**: ① **윈도·detrend·정규화(편측/양측·단위)를 모델·기준 동일하게** — 아니면 가짜 차이. ② 재격자/보간이 고파수 에너지를 깎음 → 동일 격자에서 비교. ③ 짧은 기록·결측은 저주파 신뢰 낮음(불규칙은 Lomb-Scargle). ④ 유효해상도 "6–7Δx"는 모델·수치기법 의존 advisory.
- **출처**: Welch, P. D. (1967) *IEEE Trans. Audio Electroacoust.* 15:70–73; Skamarock, W. C. (2004) "Evaluating Mesoscale NWP Models Using Kinetic Energy Spectra", *Mon. Wea. Rev.* 132:3019–3032 (유효해상도, DOI 확인요); Harris, L., et al. (2022) "A Generative Deep Learning Approach to Stochastic Downscaling...", *JAMES*, **DOI 10.1029/2022MS003120** (RAPSD/RALSD); Wheeler & Kiladis (1999) *J. Atmos. Sci.* (k-ω, DOI 확인요).

---

### EOF 공간패턴+PC 시계열 & wavelet/coherence (EOF spatial patterns + PC time series & wavelet power/coherence)
- **무엇을 보여주나**: **지배 시공간 변동모드**(EOF/PCA: 공간패턴 EOF + 시간계수 PC)와 **시간-주파수 변동**(wavelet power)·두 신호 결합(wavelet coherence)을 모델·기준에서 비교. 모델이 주요 변동모드(ENSO형·계절·경년)와 그 시간거동을 재현하는가.
- **읽는 법**: **EOF**: 공간패턴 지도(발산맵, 설명분산% 라벨) + PC 시계열; 좋음 = 모델·기준의 EOF1,2 패턴·부호·설명분산·PC 상관 일치. **Wavelet power**: 가로 시간·세로 주기·색 에너지, COI(영향원뿔)·유의등치선; 좋음 = 같은 주기대에 같은 시점 에너지. **Coherence**: 두 신호 공통 주기대 + 위상화살표(→ 동위상, ← 역위상).
- **언제 쓰나**: 자료형 = 격자장(EOF)·시계열(wavelet). 검증목적 = **변동모드·비정상 위상/주기**. 기후모드·계절변동·비정상 신호(MJO·강수 군집) 검증.
- **짝지표 & 교차링크**: 설명분산·패턴상관(EOF)·PC 상관·wavelet coherence/위상. → `05`(EOF/PCA·REOF·CEOF·wavelet·XWT/WTC), `06`(CWT·coherence), Taylor(모드계수).
- **만드는 법**: EOF `xeofs`(`xeofs.models.EOF`) 또는 `eofs`(`eofs.xarray.Eof`, cosφ 가중); wavelet `pycwt`(Torrence-Compo·XWT·WTC) 또는 `PyWavelets`. 면적가중·정규화 모델/기준 통일.
- **함정·주의**: ① **EOF 부호·순서는 임의** — 모델/기준 정합 시 부호 맞춤·축퇴(degeneracy: 설명분산 근접 모드 혼합) 주의(North's rule of thumb로 분리성 점검). ② EOF는 통계모드(물리모드 아님) → REOF로 해석성 보완. ③ 결측/짧은 기록이 EOF·coherence를 편향. ④ wavelet COI 밖·유의선만 신뢰. ⑤ 기준자료 모드도 동화산물.
- **출처**: von Storch, H., & Zwiers, F. W., *Statistical Analysis in Climate Research* (EOF/PCA); Torrence, C., & Compo, G. P. (1998) "A Practical Guide to Wavelet Analysis", *Bull. Amer. Meteor. Soc.* 79:61–78 (DOI 확인요); Grinsted, A., et al. (2004) "Application of the cross wavelet transform and wavelet coherence...", *Nonlin. Processes Geophys.* 11:561–566, **DOI 10.5194/npg-11-561-2004**.

---

## E. 시계열·신호 그림 (Time-series / signal)

### 시계열 overlay+잔차 · lag상관 · STL · DTW (Model–obs overlay + residual / lagged correlation / STL / DTW)
- **무엇을 보여주나**: 점·계류 시계열의 종합 진단 그림 가족. **Overlay+잔차**: 모델·관측을 겹쳐 그리고 아래에 잔차(e=f−o) 패널; **lag 상관**: 시간지연별 상관으로 위상지연(최적 lag) 탐지; **STL**: 추세·계절·잔차 분해 비교; **DTW**: 비선형 시간정렬로 형상 유사도와 정렬 경로.
- **읽는 법**: **Overlay**: 좋음 = 곡선 겹침·잔차 0중심 백색잡음; 나쁨 = 일정 오프셋(편향)·위상밀림(조석/일주기 지연)·진폭축소(평활). **Lag corr**: 가로 lag, 세로 상관, **피크 위치 = 지연**(0이 이상적); 양의 lag에 피크면 모델이 늦음. **STL**: 추세·계절성분이 관측과 같은지. **DTW**: 정렬경로가 대각선에서 벗어나면 시간왜곡 큼(거리=비유사도).
- **언제 쓰나**: 자료형 = 점·시계열(부이·검조소·ADCP·CSV). 검증목적 = **위상·시간지연·추세·계절·형상**. 조위·수온·유속·파고 시계열 검증의 기본 묶음.
- **짝지표 & 교차링크**: 최적 lag·위상/진폭오차·교차상관·MK/Sen 추세·DTW 거리·RMSE/bias. → `06`(교차상관/lag·STL·MK/Sen·DTW·위상진폭오차), `01`(RMSE/bias), `11`(조위 위상지연).
- **만드는 법**: overlay+잔차 `matplotlib` 2-panel(`sharex`); lag corr `scipy.signal.correlate`/`numpy.correlate`(정규화)·`statsmodels.tsa.stattools.ccf`; STL `statsmodels.tsa.seasonal.STL`; DTW `dtaidistance`/`tslearn.metrics.dtw_path`/`dtw-python`.
- **함정·주의**: ① **시간정합·시간대(UTC) 오류 = 가짜 위상오차** — `15`/`06` 전처리 강제. ② lag 상관은 자기상관으로 유효표본 작음 → 유의성 보정. ③ 선형보간이 고주파를 깎아 잔차·lag 왜곡. ④ **DTW는 과도정렬**(물리적으로 불가능한 시간왜곡까지 맞춤) → window 제약(Sakoe-Chiba band). ⑤ STL 파라미터(주기·평활)가 분해를 좌우.
- **출처**: Emery, W. J., & Thomson, R. E., *Data Analysis Methods in Physical Oceanography* (교차상관·lag·전처리); Cleveland, R. B., et al. (1990) "STL: A Seasonal-Trend Decomposition Procedure Based on Loess", *J. Official Statistics* 6:3–73; Sakoe, H., & Chiba, S. (1978) *IEEE Trans. ASSP* (DTW, DOI 확인요).

---

## F. AI/ML 평가 그림 (AI/ML evaluation)

### 영상품질 그림 — SSIM 맵 / FID·분포공간 (Image quality: SSIM map / FID & feature-distribution plots)
- **무엇을 보여주나**: AI 생성·초해상(super-resolution) 산출물의 **지각적/구조적 품질**. **SSIM 맵**: 휘도·대비·구조 유사도를 격자별로(어디가 흐릿/구조붕괴), **FID**: 생성장과 기준장의 특징분포(Inception/대체 특징) 사이 Fréchet 거리(분포수준 사실성). 보조로 PSNR·MS-SSIM·LPIPS·spectral fidelity.
- **읽는 법**: **SSIM 맵**: 0~1, 1=완전유사; 1 영역=구조보존, 낮은 영역=평활/아티팩트(전선·소용돌이 가장자리에서 흔히 낮음). **FID**: 낮을수록 분포 유사(0=동일); 모델/체크포인트별 막대·곡선. 단일 RMSE가 가린 "사실적이나 위치 다른" 산출의 품질을 포착.
- **언제 쓰나**: 자료형 = 격자장(영상형). 검증목적 = **공간 구조·지각 품질·분포 사실성**. GAN/확산모델 강수·바람·SST 생성·초해상 평가. **RAPSD·FSS와 반드시 병행**(영상품질만으론 물리·위치 보장 안 됨).
- **짝지표 & 교차링크**: SSIM/MS-SSIM·PSNR·LPIPS·FID·spectral fidelity; RAPSD·FSS·CRPS와 묶어 다축 평가. → `14`(SSIM/MS-SSIM·PSNR·LPIPS·FID·spectral fidelity), `02`(SSIM). 물리정합은 `04`(보존량) 교차.
- **만드는 법**: SSIM `skimage.metrics.structural_similarity(..., full=True)`(맵 반환); MS-SSIM/LPIPS `torchmetrics.image`(`MultiScaleStructuralSimilarityIndexMeasure`, `LearnedPerceptualImagePatchSimilarity`); FID `torchmetrics.image.fid.FrechetInceptionDistance`/`pytorch-fid`(지구과학은 도메인 특징추출기 고려).
- **함정·주의**: ① **SSIM/FID는 자연영상용** — 지구과학 변수(물리단위·동적범위)에 그대로 쓰면 오해석; 정규화·도메인 특징추출기 검토. ② FID는 **표본수·전처리에 민감**, ImageNet 특징의 도메인 부적합. ③ 좋은 SSIM/FID가 **물리보존·위치정확을 보장 안 함** → RAPSD·FSS·보존량 병행(단일지표 금지). ④ "기준"은 reference.
- **출처**: Wang, Z., et al. (2004) "Image Quality Assessment: From Error Visibility to Structural Similarity", *IEEE Trans. Image Process.* 13(4):600–612 (DOI 10.1109/TIP.2003.819861, 확인요); Heusel, M., et al. (2017) "GANs Trained by a Two Time-Scale Update Rule..." (FID), *NeurIPS 2017*, **arXiv:1706.08500**.

---

## G. 요약표 — 그림 → 검증목적 → 짝지표 → 01–15 교차링크

> 임계·기준값은 모두 **advisory**(영역·해상도·기준자료 의존). 기준자료는 truth가 아니라 reference. 어떤 그림도 단독으로 결론내지 않는다.

| # | 그림 (국문/English) | 주 검증목적 | 핵심 짝지표 | 01–15 교차링크 |
|---|---|---|---|---|
| 1 | 산점도·회귀·밀도산점도 | 정확도·조건부 편향 | RMSE·r·R²·slope·SI | 01, 15 |
| 2 | QQ-plot | 분포·꼬리·극값 | Perkins S·KS·return level | 01, 03, 13, 14 |
| 3 | 오차 히스토그램 | 편향·산포·오차구조 | bias·RMSE·왜도/첨도 | 01, 06 |
| 4 | Taylor diagram | 패턴 종합·다모델 랭킹 | R·CRMSD·σ비 | 01, 02, 05, 06, 13, 14 |
| 5 | Target diagram | 편향+산포 동시 | bias·uRMSE·총RMSD | 01, 09, 12 |
| 6 | Bias/difference map | 편향 공간구조 | 격자 ME·RMSE·MAE | 02, 15 |
| 7 | ACC/패턴상관 맵 | 패턴·위상 | ACC·패턴상관·S1 | 01, 02, 07, 09, 12, 13 |
| 8 | FSS 공간검증 맵 | 공간·스케일 유용성 | FSS·useful scale | 02, 03, 07, 14 |
| 9 | SAL/MODE 객체 플롯 | 패턴·구조·위치 | S·A·L·객체속성·CSI | 02, 03, 07, 13 |
| 10 | Hovmöller 다이어그램 | 위상·전파구조 | 위상속도·lag·k-ω | 05, 06, 02 |
| 11 | 분할표 viz & Performance diagram | 범주형 사건 종합 | POD·SR·CSI·FBI·ETS/HSS | 03, 14 |
| 12 | ROC curve | 확률 판별력 | AUC·POD·POFD | 03, 14 |
| 13 | Reliability & PIT 히스토그램 | 확률·UQ 보정 | Brier(REL)·ECE·sharpness | 03, 13, 14 |
| 14 | Rank histogram & spread-skill | 앙상블 신뢰성·산포 | spread-skill ratio·CRPS REL | 03, 13, 14 |
| 15 | Brier/CRPS 분해 | 확률 스킬 원천 진단 | Brier/CRPS(+분해)·BSS | 03, 14 |
| 16 | Return-level & PDF/CDF/Perkins | 분포·꼬리·재현빈도 | GEV/GPD·return level·Perkins S | 03, 08, 11, 14 |
| 17 | PSD·파수·k-ω & RAPSD/유효해상도 | 변동모드·스케일·유효해상도 | 스펙트럼 기울기·RAPSD·유효해상도 | 05, 02, 06, 14 |
| 18 | EOF 공간패턴+PC & wavelet/coherence | 변동모드·비정상 위상 | 설명분산·PC상관·coherence | 05, 06 |
| 19 | 시계열 overlay+잔차·lag·STL·DTW | 위상·지연·추세·형상 | lag·위상/진폭오차·DTW거리 | 06, 01, 11 |
| 20 | SSIM/FID 영상품질 | 공간구조·지각·분포 사실성 | SSIM·LPIPS·FID·spectral fidelity | 14, 02, 04 |

---

### 출처 표기 메모
- **DOI 직접 확인 완료**: Taylor 2001(10.1029/2000JD900719) · Jolliff 2009(10.1016/j.jmarsys.2008.05.014) · Roberts & Lean 2008(10.1175/2007MWR2123.1) · Wernli 2008 SAL(10.1175/2008MWR2415.1) · Roebber 2009(10.1175/2008WAF2222159.1) · Hamill 2001(10.1175/1520-0493(2001)129<0550:IORHFV>2.0.CO;2) · Hersbach 2000(10.1175/1520-0434(2000)015<0559:DOTCRP>2.0.CO;2) · Gneiting et al. 2007(10.1111/j.1467-9868.2007.00587.x) · Perkins et al. 2007(10.1175/JCLI4253.1) · Grinsted et al. 2004(10.5194/npg-11-561-2004) · Hovmöller 1949(10.1111/j.2153-3490.1949.tb01260.x) · Harris et al. 2022(10.1029/2022MS003120) · Heusel et al. 2017(arXiv:1706.08500).
- **"(확인요)"**: Davis 2006 MODE DOI · Wang 2004 SSIM DOI · Bröcker & Smith 2007 DOI · Mason & Graham 2002 DOI · Murphy 1973 DOI · Skamarock 2004 DOI · Wheeler & Kiladis 1999 DOI · Sakoe & Chiba 1978 DOI · Torrence & Compo 1998 DOI · WWRP/WGNE(CAWCR) 검증 페이지(URL 변동 가능). — 교과서(Wilks, Jolliffe & Stephenson, Coles 2001, Emery & Thomson, von Storch & Zwiers)는 판본별 페이지 상이하므로 DOI 미표기.
</content>
</invoke>
