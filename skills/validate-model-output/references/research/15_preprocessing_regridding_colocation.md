# 15. 전처리·격자정합·시공간 매칭 (Preprocessing / Regridding / Colocation)

본 문서는 수치모델 결과를 ERA5/GLORYS 등 재분석자료, 관측소·위성 자료와 **비교·검증하기 전에 반드시 거치는 전처리·정합(co-location) 표준 방법**을 망라한 카탈로그다. 격자 간 보간·재격자화(regridding), 좌표·투영 변환, 경도표기·날짜변경선 처리, 벡터(유속·바람) 격자정렬, land-sea mask 처리, 시간 동기화·평균·누적, matchup 윈도 설계, 대표성 오차(representativeness error), 단위·CF convention 정합, 결측·품질관리(QC), climatology/anomaly 산출, 편차보정(bias correction)·분위사상(quantile mapping), detiding·필터 전처리, 짝지은표본(paired sample) 구성을 다룬다. 모든 검증 지표(RMSE·bias·상관 등)는 **모델값과 참조값이 동일 시·공간 격자/지점으로 정렬된 짝지어진 표본(paired samples)** 을 전제로 하므로, 이 단계의 선택은 검증 결과 자체를 좌우한다. 각 메서드 카드는 정의·전제·해석 기준·한계·검증 가능한 출처를 담는다.

> **워크플로 권장 순서**: ① 메타데이터·CF/단위 정합 → ② 좌표계·경도표기·달력 정합 → ③ 마스크·QC·결측 처리 → ④ 격자정합(regridding)·벡터 회전 → ⑤ 시간 동기화·평균/누적 정합 → ⑥ colocation 윈도로 짝 구성 → ⑦ (선택) climatology/anomaly·필터·편차보정 → ⑧ 검증 통계 산출. 전처리 단계마다 **모델·참조에 동일한 처리를 동일 순서로 적용**해야 가짜 차이(spurious difference)를 만들지 않는다.

## 한 줄 목차
- **이중선형 보간 (Bilinear interpolation)** — 가장 보편적인 평활 격자 보간
- **이중삼차/스플라인 보간 (Bicubic / spline)** — 더 매끄러우나 over-shoot 위험
- **최근접 이웃 (Nearest-neighbor)** — 범주·플래그·불연속 자료의 기본 보간
- **역거리가중 (Inverse Distance Weighting, IDW)** — 산포점→격자/점의 단순 가중보간
- **1차 보존 재매핑 (First-order conservative remapping)** — 면적·총량 보존
- **2차 보존 재매핑 (Second-order conservative remapping)** — gradient 포함, 더 매끄러운 보존
- **패치 복원 보간 (Patch / higher-order patch recovery)** — ESMF 고차 평활 보간
- **재매핑 가중치 생성·검증 (SCRIP/ESMF weights, normalization)** — 가중치 행렬·보존성 점검
- **크리깅 (Kriging / 지구통계 보간)** — 분산 최소·오차장 동시 산출
- **최적 보간 / 객관 분석 (Optimal Interpolation, Objective Analysis)** — 배경+관측 가중 분석
- **변분 보간 (DIVA / variational analysis)** — 해안선·이류 고려 격자화
- **좌표·투영 변환 (Coordinate / projection transformation)** — CRS·datum 정합
- **경도표기·날짜변경선·극 처리 (Longitude convention / dateline / pole)** — 0–360 vs ±180, seam 처리
- **회전격자·비정규격자 처리 (Rotated / curvilinear / unstructured grid)** — ORCA·삼각격자 등
- **벡터 격자정렬·회전 (Vector grid-to-earth rotation)** — 유속·바람 동/북 성분 정렬
- **육해상 마스크 처리 (Land-sea mask handling)** — 해상값 오염 방지
- **시간 동기화·재표본 (Time synchronization / resampling)** — 시각 정렬·달력·내삽
- **시간 평균·누적 (Temporal averaging / accumulation)** — 순간·평균·누적량 일치
- **Colocation / matchup 윈도 설계 (Matchup window design)** — 시공간 허용창
- **짝지은표본 구성·독립성 (Paired-sample construction / independence)** — 검증 표본 정의·자기상관
- **대표성 오차 (Representativeness error)** — 척도 불일치 오차 정량화
- **삼중 정합 (Triple collocation)** — 참값 없이 3자료 오차분산 추정
- **단위·UDUNITS 정합 (Unit conversion / UDUNITS)** — 단위 파싱·환산
- **CF convention / standard_name 정합** — 변수 의미·메타데이터 표준화
- **결측·QC 처리 (Missing value / quality control)** — range·spike·flag 처리
- **갭 채움 (Gap filling / imputation)** — 결측 보간·EOF(DINEOF) 복원
- **climatology / anomaly 산출** — 기후값·편차 계산
- **표준화 편차 (Standardized anomaly)** — 분산 정규화 편차
- **편차보정·분위사상 (Bias correction / quantile mapping)** — 분포 정합·다운스케일
- **조석 분리 (Detiding / harmonic analysis)** — 조석·비조석 분리
- **시계열 필터링 (Low/high/band-pass filtering)** — 잡음·고주파 제거
- **수직 보간·층 정합 (Vertical interpolation / depth matching)** — 깊이·연직층 정렬

---

### 이중선형 보간 (Bilinear interpolation)
- **무엇을 측정/검증하나:** 직접 검증 지표는 아니나, 모델 격자값을 관측점 또는 다른 격자로 옮길 때 가장 널리 쓰는 평활 보간. 비교 전 정합의 기본 도구.
- **정의·수식:** 인접 4개 격자점(2D)을 사용해 두 방향으로 선형 보간. f(x,y) ≈ Σ wᵢ fᵢ, 가중치 wᵢ는 목표점까지의 거리비로 결정(쌍선형 형태). 연속이지만 1차 미분은 불연속.
- **적용 도메인/자료형:** 전 도메인. 격자→격자, 격자→점(관측소) 매칭. SST·풍속·파고 등 공간적으로 매끄러운 연속장에 적합.
- **입력·전제:** 규칙(rectilinear) 또는 좌표를 알 수 있는 곡선격자(curvilinear). 목표점이 원격자 경계 안에 있어야 함(외삽 주의). 결측·육지 셀이 4점에 섞이면 오염 → 마스크 선처리 필요.
- **해석 기준:** 매끄러운 장에서 표준 선택. 총량(적분량)은 보존하지 않음 — 강수·플럭스처럼 보존이 중요한 변수에는 비권장.
- **한계·주의:** 극값을 평활(과소평가)함. 좌표가 빠르게 변하는 고위도/극 근처 곡선격자에서 왜곡. 보존 안 됨. 마스크 경계에서 해상↔육지 혼합 오염.
- **출처:** ESMF/ESMPy 공식 문서(지원 보간법 목록); CDO `remapbil` 문서; xESMF "Comparison of seven regridding algorithms"(보간법 비교 노트북).

---

### 이중삼차 / 스플라인 보간 (Bicubic / spline interpolation)
- **무엇을 측정/검증하나:** 이중선형보다 더 매끄러운(1차 미분 연속) 보간으로 격자 정합·다운스케일에 사용.
- **정의·수식:** 인접 16개 점(4×4) 또는 도함수 정보를 이용한 3차 다항식 보간. 자연스러운 곡률 표현, C¹/C² 연속.
- **적용 도메인/자료형:** 연속·매끄러운 장(SSH, 기압장 등). 격자→고해상 격자 시각화·다운스케일.
- **입력·전제:** 충분히 조밀하고 결측이 없는 원격자. 경계·마스크 인접에서 16점 stencil이 육지/결측을 포함하면 큰 오차.
- **해석 기준:** 평활도가 중요할 때. 단, 보존 안 됨.
- **한계·주의:** 가파른 경사·불연속(전선, 해안)에서 **over-shoot/under-shoot**(Gibbs 유사 진동) 발생 → 물리적으로 불가능한 값(음의 강수·농도) 생성 가능. 보존 안 됨.
- **출처:** CDO `remapbic` 문서; xESMF 알고리즘 비교 문서; 수치해석 표준 교과서(예: Press et al., *Numerical Recipes* — bicubic 보간; 일반 표준).

---

### 최근접 이웃 보간 (Nearest-neighbor interpolation)
- **무엇을 측정/검증하나:** 가장 가까운 원격자 값을 그대로 복사. 범주형·플래그·불연속 자료, 또는 평활을 피해야 할 때의 기본 매칭.
- **정의·수식:** f(x,y) = f(가장 가까운 소스점). 변형: nearest source-to-destination(`nearest_s2d`), nearest destination-to-source(`nearest_d2s`) — ESMF/xESMF가 두 방향 제공. 방향에 따라 일부 소스셀이 매핑에서 누락되거나 복수 사용됨.
- **적용 도메인/자료형:** land-sea mask, 토지피복·해역 구분, 정수 플래그, QC 플래그, 이산 변수. 또한 해상도 차가 작은 빠른 매칭.
- **입력·전제:** 좌표만 알면 됨. 보간으로 인한 값 생성이 없으므로 물리적 불가능 값 미발생.
- **해석 기준:** 불연속·범주형에서 표준. 연속장에는 블록(blocky) 인공구조 유발 → 비권장.
- **한계·주의:** 공간 평활 전혀 없음 → 연속장 검증 시 계단형 오차. 해상도 차가 크면 다수 목표셀이 같은 소스값을 받아 정보 손실. 보존 안 됨.
- **출처:** ESMF/ESMPy 문서(`nearest_s2d`/`nearest_d2s`); xESMF 알고리즘 비교 문서.

---

### 역거리가중 보간 (Inverse Distance Weighting, IDW)
- **무엇을 측정/검증하나:** 산포된 관측점(또는 격자점)으로부터 거리의 역수 가중으로 목표 위치 값을 추정. 변동도 적합 없이 빠르게 점→격자/격자→점 보간.
- **정의·수식:** Z*(x₀) = Σ wᵢ Zᵢ / Σ wᵢ, wᵢ = 1/dᵢᵖ (보통 p=2). dᵢ는 목표점-소스점 거리, p는 거리감쇠 지수. ESMF의 `nearest_idavg`(n개 최근접 점의 거리가중 평균)가 대표 구현.
- **적용 도메인/자료형:** 부이·관측소 등 불규칙 점 자료의 간이 격자화, 빠른 colocation. 수온·풍속·파고 등 연속장.
- **입력·전제:** 점 좌표·값, 거리지수 p와 이웃 개수 n 설정. 구면거리(great-circle) 사용 권장.
- **해석 기준:** 크리깅 대비 단순·고속이지만 오차장(불확실성)은 산출하지 않음. 빠른 1차 근사로 적합.
- **한계·주의:** p가 크면 최근접점에 과도하게 쏠려 bull's-eye(황소눈) 인공패턴. 공간 자기상관 구조를 반영하지 못함(크리깅 대비 통계적 최적성 없음). 관측 분포가 편향되면 결과 왜곡. 외삽 영역 신뢰 낮음.
- **출처:** Shepard, D. (1968) "A two-dimensional interpolation function for irregularly-spaced data", *Proc. 23rd ACM National Conference*, 517–524(역거리가중의 원전); ESMF/ESMPy 문서(`nearest_idavg`).

---

### 1차 보존 재매핑 (First-order conservative remapping)
- **무엇을 측정/검증하나:** 보간 전후 **면적가중 총량(적분량)을 보존**. 강수·플럭스·에너지·질량처럼 총량이 의미 있는 변수의 격자 정합 표준.
- **정의·수식:** 각 목표셀 값 = Σ (소스셀과 목표셀의 중첩면적 / 목표셀 면적) × 소스값. 가중치 = 구면 다각형 교차면적 기반. 셀 내 상수(piecewise-constant) 가정.
- **적용 도메인/자료형:** 강수, 복사·열·운동량 플럭스, 면적분 보존이 필요한 모든 변수. 거친↔조밀 격자 상호 변환. 모델-모델, 모델-재분석 비교 전 면적 일치.
- **입력·전제:** 소스·목표 모두 **셀 경계(corner/bounds) 정보** 필요(CF의 bounds 변수). 구면 다각형 교차 계산. 마스크가 있으면 normalization 옵션(분모에 마스크 면적 반영) 선택해야 보존 깨짐 방지.
- **해석 기준:** 전역 적분 보존이 필요하면 표준. coarse→fine에서는 계단형(블록) 결과. **검증법**: 재매핑 전후 면적가중 전역합(또는 평균)이 (마스크 영향 제외 시) 일치해야 함 — 어긋나면 bounds·normalization 오류.
- **한계·주의:** 셀 내 상수 가정으로 fine 격자에서 매끄럽지 않음. 경계·bounds가 부정확하면 보존 깨짐. 부분육지 셀에서 normalization 방식(`fracarea` vs `destarea`)에 따라 값/보존성 달라짐(Taylor 2024 참조).
- **출처:** Jones, P. W. (1999) "First- and Second-Order Conservative Remapping Schemes for Grids in Spherical Coordinates", *Monthly Weather Review* 127, 2204–2210; ESMF Regridding 문서; CDO `remapcon`; Taylor, K. E. (2024) "Truly conserving with conservative remapping methods", *Geosci. Model Dev.* 17, 415–430.

---

### 2차 보존 재매핑 (Second-order conservative remapping)
- **무엇을 측정/검증하나:** 1차 보존과 동일하게 총량을 보존하되, **소스 셀 내 gradient를 포함**해 더 매끄럽고 정확한 장을 생성.
- **정의·수식:** 1차 보존 가중치에 더해 소스 셀의 공간 기울기(∇)를 반영한 보정항 추가. coarse→fine 변환에서 1차보다 부드럽고 오차(misfit)가 작음.
- **적용 도메인/자료형:** 보존이 필요하면서도 평활도가 중요한 변수(강수의 고해상 표현 등). 거친→조밀 변환.
- **입력·전제:** 셀 경계 정보 + gradient 계산 가능한 인접 셀. 마스크 처리 동일.
- **해석 기준:** ESMF/YAC 벤치마크에서 평균 misfit이 1차보다 일관되게 낮음 → coarse→fine에 권장.
- **한계·주의:** gradient 계산으로 비용 증가. 가파른 경사에서 미세한 over/under-shoot 가능(보존은 유지). 경계 근처 gradient 추정 부정확.
- **출처:** Jones, P. W. (1999) *Monthly Weather Review* 127, 2204–2210; ESMF Regridding 문서; "Benchmarking Regridding Libraries Used in Earth System Modelling", *Math. Comput. Appl.* 27(2):31 (MDPI, 2022).

---

### 패치 복원 보간 (Patch / higher-order patch recovery)
- **무엇을 측정/검증하나:** ESMF 고유의 고차 보간. 이중선형보다 매끄럽고 도함수가 연속적인 결과(보존은 아님).
- **정의·수식:** 목표점 주변 다수 소스 셀에 최소제곱 다항식을 적합(patch recovery)해 보간. 유한요소 기반 평활(ESMF 문서의 patch recovery 방법론).
- **적용 도메인/자료형:** 매끄러운 연속장에서 bilinear의 평활 한계를 줄이고 싶을 때. 격자→격자.
- **입력·전제:** 충분한 인접 셀. 마스크 처리 필요.
- **해석 기준:** bilinear보다 정확하고 매끄러우나 보존 필요 시 부적합.
- **한계·주의:** 비용 큼. 보존 안 됨. 경계 근처 적합 불안정.
- **출처:** ESMF/ESMPy 공식 문서(patch 보간 설명); xESMF 알고리즘 비교 문서.

---

### 재매핑 가중치 생성·보존성 검증 (Remapping weights generation / normalization / conservation check)
- **무엇을 측정/검증하나:** 재격자화를 **희소 가중치 행렬(sparse weight matrix)** 생성과 적용으로 분리해 재현성·검증성을 확보. 같은 격자쌍에 가중치를 재사용하고, 보존성·정규화를 점검.
- **정의·수식:** 목표값 = W · 소스값 (W: n_dst × n_src 희소행렬). SCRIP/ESMF가 NetCDF 가중치 파일(또는 SCRIP grid description)을 생성. 마스크/부분셀 normalization: `fracarea`(유효면적으로 나눔, 마스크 영향 반영)와 `destarea`(목표셀 전체면적으로 나눔, 전역 보존 유지)가 대표.
- **적용 도메인/자료형:** 모든 격자→격자 재매핑(모델↔재분석↔위성격자). 대량 시계열·앙상블에 동일 가중치 반복 적용.
- **입력·전제:** 소스·목표 격자 정의(중심+코너 좌표, 마스크). CF bounds 또는 SCRIP/ESMF grid 파일.
- **해석 기준:** (1) 행 합 ≈ 1(비보존법) 또는 면적가중 보존(보존법). (2) 재매핑 전후 전역 면적가중 적분 비교로 보존 오차 정량화. (3) 동일 가중치 재사용 시 결과 bit-수준 재현.
- **한계·주의:** 코너 좌표 누락·중첩계산 오류로 보존 깨짐. 마스크/normalization 조합을 잘못 고르면 연안에서 값/보존 모두 틀림. 격자 정의가 바뀌면 가중치 재생성 필요.
- **출처:** Jones, P. W. (1998) "A User's Guide for SCRIP: A Spherical Coordinate Remapping and Interpolation Package" (Los Alamos National Laboratory, LACC 98-45); ESMF Regridding 문서(masking·normalization, `fracarea`/`destarea`); Taylor, K. E. (2024) *Geosci. Model Dev.* 17, 415–430(보존 정규화 함정).

---

### 크리깅 / 지구통계 보간 (Kriging / geostatistical interpolation)
- **무엇을 측정/검증하나:** 산포된 관측점을 격자로 보간하면서 **추정 분산(오차장)을 동시 산출**. 분포가 불규칙한 관측소·부이 자료의 격자화에 사용.
- **정의·수식:** Z*(x₀) = Σ λᵢ Z(xᵢ), 가중치 λ는 변동도(variogram/semivariogram) γ(h) 모형으로부터 추정 분산을 최소화하도록 결정(BLUE, 최량선형불편추정). ordinary/universal/simple kriging 등.
- **적용 도메인/자료형:** 관측소·부이·CTD 등 점 관측의 격자화. 수온·염분·해수면·기상요소. 위성 결측 보간에도 활용.
- **입력·전제:** 변동도 적합(공간 자기상관 모형), 정상성(stationarity) 가정. 자료가 충분히 많고 공간 분포가 적절해야 변동도 신뢰. 이상치 사전 제거 권장.
- **해석 기준:** 추정값 + kriging 분산(오차) 함께 보고 → 검증용 불확실성 정량화에 유리.
- **한계·주의:** 정상성·등방성 가정 위반(해안·이류) 시 왜곡. 변동도 적합이 주관적. 계산 비용(대규모 자료). 외삽 영역에서 분산만 커지고 추정 부정확.
- **출처:** Cressie, N. (1993) *Statistics for Spatial Data* (Wiley, 개정판; 지구통계·크리깅 표준 교과서); ICES/SeaDataNet 격자화 가이드(확인요).

---

### 최적 보간 / 객관 분석 (Optimal Interpolation / Objective Analysis)
- **무엇을 측정/검증하나:** 배경장(모델/기후값)과 관측을 오차분산 가중으로 결합해 분석장과 분석오차를 생성. 재분석·격자화의 핵심.
- **정의·수식:** 분석 = 배경 + K(관측 − 배경), K = B Hᵀ (H B Hᵀ + R)⁻¹ (B: 배경오차공분산, R: 관측오차공분산). 기대오차분산 최소화. 크리깅과 수학적으로 동치(상관모형↔변동도).
- **적용 도메인/자료형:** 격자 분석장 생성(SST, SSH, 해양 변수). 모델-관측 융합. 비교용 기준장(reference) 제작. 위성 L4(예: GHRSST L4 OISST류)가 대표 산물.
- **입력·전제:** B, R(오차공분산)의 적절한 추정, 상관거리·등방성 가정. 관측-배경 짝지음.
- **해석 기준:** 분석오차분산이 작은 영역일수록 신뢰. 관측 밀집부에서 분석 우수.
- **한계·주의:** 공분산 가정에 민감. 등방성 가정이 해안·전선에서 부적절. 관측 희박 영역에서 배경에 회귀. **OI L4를 "관측"으로 쓰는 검증은 모델과 일부 입력을 공유**하면 독립성 위반(삼중정합 가정 주의).
- **출처:** Troupin, C., et al., "Introduction to Optimal Interpolation and Variational Analysis"(GHER 교육자료); Daley, R. (1991) *Atmospheric Data Analysis* (Cambridge, 자료동화 표준 교과서).

---

### 변분 보간 (DIVA / Data-Interpolating Variational Analysis)
- **무엇을 측정/검증하나:** 관측-분석 불일치와 분석 평활도를 동시에 최소화하는 비용함수로 격자화. **해안선·하위해역·이류**를 고려하는 점이 OI 대비 강점.
- **정의·수식:** 비용함수 J = (관측-분석 거리항) + (분석의 규칙성/평활항)을 유한요소법으로 최소화. 실제 도메인(해안 경계 포함)에서 풀어 육지를 가로지른 잘못된 상관 차단.
- **적용 도메인/자료형:** in situ 해양 관측(수온·염분·영양염)의 기후학적 격자장 생성. 복잡 해안·만(灣) 영역.
- **입력·전제:** 상관거리·신호대잡음비 파라미터, 해안선·지형 마스크. 유한요소 메시.
- **해석 기준:** OI와 비슷한 분석·오차장을 주되 해안·이류 효과를 더 사실적으로 반영. 일관 오차장(consistent error field) 제공.
- **한계·주의:** 파라미터(상관거리·SNR) 선택에 민감. 메시 생성·계산 부담. 관측 희박부 신뢰 낮음.
- **출처:** Troupin, C., et al. (2012) "Generation of analysis and consistent error fields using the Data Interpolating Variational Analysis (DIVA)", *Ocean Modelling* 52–53, 90–101; GHER/SeaDataNet DIVA 문서.

---

### 좌표·투영 변환 (Coordinate / projection transformation)
- **무엇을 측정/검증하나:** 자료의 좌표계(CRS)·datum·투영을 공통 기준으로 통일. 위치 정합의 전제.
- **정의·수식:** 경위도(EPSG:4326)↔투영좌표(UTM, polar stereographic 등) 변환, datum 변환(WGS84 등). PROJ/pyproj가 표준 변환 엔진.
- **적용 도메인/자료형:** 위성(스와스/투영격자), 해도, GIS 자료와 모델격자 정합. 극지(polar stereographic) 해빙·해양.
- **입력·전제:** 각 자료의 정확한 CRS·EPSG 코드·datum 메타데이터. 경도 표기 정합(0–360 vs −180–180)도 함께 처리(다음 카드 참조).
- **해석 기준:** 변환 후 위치 잔차가 격자 간격보다 충분히 작아야 함.
- **한계·주의:** CRS 메타데이터 누락/오기 시 수십 km 위치오차. 극 근처 투영 왜곡. 위성 swath의 georeferencing 오차는 변환으로 보정 불가.
- **출처:** PROJ / pyproj 공식 문서; EPSG Geodetic Parameter Dataset(표준 참고, epsg.org).

---

### 경도표기·날짜변경선·극 처리 (Longitude convention / dateline / pole handling)
- **무엇을 측정/검증하나:** 자료마다 다른 경도표기(0–360° vs −180–180°), 날짜변경선(antimeridian) 봉합부, 극점 특이점을 정합. 잘못 두면 날짜변경선 부근 매칭이 통째로 실패.
- **정의·수식:** 경도 모듈러 변환 lon → ((lon + 180) mod 360) − 180 또는 그 반대. 보간 시 경도축을 주기적(periodic/cyclic)으로 처리(예: xESMF `periodic=True`)해 0°/360° 봉합부 끊김 방지. 극 근처는 위도 가중·삼각격자 또는 투영 사용.
- **적용 도메인/자료형:** 전구·반구 격자(ERA5는 0–360, 일부 산물은 ±180), 환태평양·국제날짜변경선 인근 해역, 극지.
- **입력·전제:** 각 자료의 경도 범위·정렬(오름/내림차순)·주기성 메타. 좌표 정렬·롤(roll) 필요 여부.
- **해석 기준:** 변환 후 경도 단조·중복 없는지, 봉합부에서 보간 인공값(줄무늬) 없는지 확인.
- **한계·주의:** 0–360↔±180 미정합으로 날짜변경선 부근 표본 누락·중복. 비주기 처리로 첫/끝 경도 사이 보간 끊김. 극점 다중정의(여러 lon이 같은 점)로 평균·보간 왜곡.
- **출처:** xarray/xESMF 문서(경도 주기성·`periodic` 옵션); CF Conventions(경도 좌표·`units: degrees_east`); 일반 격자처리 관행.

---

### 회전·곡선·비정규 격자 처리 (Rotated / curvilinear / unstructured grid handling)
- **무엇을 측정/검증하나:** ORCA(회전극)·삼각격자(FVCOM)·비정규 메시 모델출력을 규칙격자로 정합하거나 관측에 매칭.
- **정의·수식:** 2D 좌표배열(lon2d, lat2d) 또는 노드-연결(connectivity) 정보를 이용. 보존/이중선형 가중치를 곡선·비정규 격자에 일반화(ESMF는 unstructured mesh 지원).
- **적용 도메인/자료형:** NEMO/GLORYS(ORCA tripolar), FVCOM/SCHISM(삼각격자), WW3(비정규) 등 해양·파랑 모델.
- **입력·전제:** 셀 중심+코너 좌표 또는 메시 connectivity. 벡터(유속·바람)는 격자 회전각을 고려해 동/북 성분으로 정렬해야 함(다음 카드 참조).
- **해석 기준:** 코너 정보가 있으면 보존 재매핑 가능. 면적가중을 정확히 반영해야 통계 비편향.
- **한계·주의:** tripolar 북극 접합부·날짜변경선 처리 까다로움. 비정규격자 면적가중 누락 시 통계 편향. 2D 좌표를 1D로 오인하면 위치오차.
- **출처:** ESMF Regridding 문서(unstructured mesh); SCRIP grid description(곡선·비정규 격자 NetCDF 기술); NEMO 격자 문서(확인요).

---

### 벡터 격자정렬·회전 (Vector grid-to-earth rotation)
- **무엇을 측정/검증하나:** 유속·바람 등 **벡터 변수**를 비교할 때, 모델 격자상 성분(grid-relative i/j)을 지구기준 동/북(east/north) 성분으로 회전해 관측·재분석과 같은 좌표계로 정렬. 방향·세기 검증의 전제.
- **정의·수식:** [u_E, v_N]ᵀ = R(θ) [u_i, v_j]ᵀ, R은 격자 회전각 θ(국지적으로 격자선과 동/북축의 각)로 정의되는 회전행렬. θ는 곡선격자의 인접 좌표차로 계산하거나 모델이 제공하는 각도 변수(예: NEMO `gcost/gsint`, WRF `COSALPHA/SINALPHA`) 사용.
- **적용 도메인/자료형:** 해류(u,v), 바람(u10,v10), 파향 관련 벡터. ORCA/곡선격자·회전격자 모델출력.
- **입력·전제:** 격자 회전각(또는 계산용 좌표). 성분이 grid-relative인지 earth-relative인지 메타데이터로 확인. 스칼라(세기)만 비교하면 회전 불필요하나 방향 비교엔 필수.
- **해석 기준:** 회전 후 동/북 성분 또는 (세기, 방향)으로 비교. 회전이 맞으면 세기는 회전 불변이어야 함(검증 체크).
- **한계·주의:** 회전 누락 시 방향(예 풍향·유향) 검증이 통째로 틀림. C-grid 등 staggered 격자는 u·v가 서로 다른 점에 위치 → 같은 점으로 보간 후 회전. 부호·축 정의(동/북 양의 방향) 혼동 주의.
- **출처:** NEMO 모델 문서(격자각·벡터 회전, `gcost/gsint`); WRF 사용자 가이드(`COSALPHA/SINALPHA` earth-relative 변환); CF Conventions(grid_mapping·벡터 성분 관행).

---

### 육해상 마스크 처리 (Land-sea mask handling)
- **무엇을 측정/검증하나:** 보간·통계 시 육지(또는 결측) 셀이 해상값을 오염시키지 않도록 마스크를 적용. 해양·연안 검증의 필수 전처리.
- **정의·수식:** 마스크 배열(1=유효, 0=무효)을 보간 가중치에 반영. 보존 재매핑은 normalization(`fracarea`/`destarea`)로 부분육지 셀 보정. 보간 전 결측 셀을 가중에서 제외.
- **적용 도메인/자료형:** SST·SSS·SSH·해류·파랑 등 해양변수. 모델과 참조자료의 마스크가 다르면 공통 마스크 교집합 사용.
- **입력·전제:** 각 자료의 land-sea mask. 연안 셀에서 모델·관측·재분석의 해안선 정의가 다를 수 있음.
- **해석 기준:** 마스크 정합 후 통계는 해상 공통영역에서만 산출. 연안 격차는 해안선 불일치로 설명 가능.
- **한계·주의:** 마스크 불일치로 연안 RMSE 과대. 보간이 육지값을 끌어오면 해안 편향. coarse 격자의 마스크는 부분육지 셀 다수 → 보존 normalization 선택 중요.
- **출처:** ESMF Regridding 문서(masking·normalization); CMEMS/CMOR 마스크 처리 관행(확인요).

---

### 시간 동기화·재표본 (Time synchronization / resampling)
- **무엇을 측정/검증하나:** 모델·관측·재분석의 시각 기준·해상도를 일치시켜 동일 시각의 짝을 만든다. 시계열 검증의 전제.
- **정의·수식:** 공통 시간격자로 재표본(resample)·내삽. 시간축 단위(`since` 기준시각)·달력(calendar: gregorian, 360_day, noleap, proleptic_gregorian) 변환. UTC 통일. cftime/xarray가 비표준 달력 처리.
- **적용 도메인/자료형:** 부이·관측소·재분석 시계열. 위성 통과시각과 모델 출력시각 매칭.
- **입력·전제:** 정확한 시간 메타데이터(units, calendar). 타임존(KST↔UTC) 명시. 순간값 vs 평균값 여부.
- **해석 기준:** 매칭 시각 차가 변동 시간척도보다 충분히 작아야 함.
- **한계·주의:** 달력 불일치(360_day↔gregorian)로 날짜 어긋남. 타임존 누락으로 9시간 오차. 시간 내삽이 위상(phase) 오차를 숨길 수 있음.
- **출처:** CF Conventions(시간축·calendar·units 절); UDUNITS-2 시간 처리(Unidata); cftime/xarray 문서(비표준 달력).

---

### 시간 평균·누적 (Temporal averaging / accumulation)
- **무엇을 측정/검증하나:** 변수의 시간 특성(순간값·시간평균·누적량)을 일치시켜 비교. 강수·복사 등 누적·플럭스 변수에서 특히 중요.
- **정의·수식:** 순간값↔평균값↔누적량 정합. 예: ERA5 강수·복사는 누적/평균 플럭스 → 모델의 순간/기간 정의와 맞춰야 함. cell_methods(`time: mean`, `time: sum`, `time: point`)로 의미 명시.
- **적용 도메인/자료형:** 강수, 단·장파복사, 증발, 플럭스, 풍속 평균 등. 일평균·월평균 비교.
- **입력·전제:** 각 자료의 집계 구간(accumulation period)·시각 라벨(구간 시작/끝/중앙) 메타데이터.
- **해석 기준:** 같은 집계 정의로 맞춘 뒤에만 bias·RMSE가 의미. 평균기간 불일치는 계통오차로 나타남.
- **한계·주의:** ERA5 등 재분석의 누적/평균 시각 라벨 관행을 오해하면 시간 어긋남·이중계산. 순간값과 평균값 혼용 시 분산 비교 왜곡.
- **출처:** CF Conventions(`cell_methods`); ECMWF ERA5 문서(누적·평균 변수 처리; "How to compute daily/accumulated quantities" 지침, 확인요).

---

### Colocation / matchup 윈도 설계 (Matchup window design)
- **무엇을 측정/검증하나:** 모델/위성과 in situ를 짝지을 때 허용하는 **공간 반경·시간 창**의 정의. 검증 표본 자체를 결정.
- **정의·수식:** matchup 기준 = |Δt| ≤ Δt_max AND 거리 ≤ d_max. 흔한 관행: 위성 SST/SSS 검증 시 ±일정 시간(예 수 시간~1일), 반경 수 km~수십 km. 픽셀 내 평균·중앙값·표준편차로 대표값 산출. Match-up Database(MDB) 파일 구조로 표준화.
- **적용 도메인/자료형:** 위성-부이, 모델-관측소 매칭. SST·SSS·파고·풍속.
- **입력·전제:** 양 자료의 위치·시각, 대표성 척도. 창이 좁으면 표본 부족, 넓으면 자연변동이 오차에 섞임.
- **해석 기준:** 창 크기에 따른 통계 민감도(sensitivity) 점검 권장. 변동이 큰 영역일수록 좁은 창 필요.
- **한계·주의:** 창 선택이 RMSE·bias를 바꿈(자의성). 깊이 불일치(위성 표층 skin vs 부이 수 m 깊이)도 함께 보정 필요. 동일 부이의 다중 매칭 중복(다음 카드의 독립성 참조).
- **출처:** Urraca, R., et al. (2024) "Impact of the Spatio-Temporal Mismatch Between Satellite and In Situ Measurements...", *J. Geophys. Res.: Atmospheres* 129; "Validation of satellite water products based on HYPERNETS in situ data using a Match-up Database (MDB) file structure", *Frontiers in Remote Sensing* (2024).

---

### 짝지은표본 구성·독립성 (Paired-sample construction / independence and autocorrelation)
- **무엇을 측정/검증하나:** colocation으로 만든 (모델, 참조) 짝들을 **검증 표본 집합**으로 정의하고, 표본의 독립성·대표성·자기상관을 점검. RMSE·상관·유의성의 신뢰성을 좌우.
- **정의·수식:** 짝 집합 {(mᵢ, oᵢ)} 구성 → 결측·플래그·매칭실패 제거 → 공통 N개 표본. 유효 표본수(effective sample size) N_eff = N · (1−ρ)/(1+ρ) 근사(ρ: lag-1 자기상관)로 시계열 자기상관 보정. 신뢰구간·유의성 검정에 N 대신 N_eff 사용.
- **적용 도메인/자료형:** 모든 시계열·격자 검증. 부이 시계열(시간 자기상관), 인접 격자(공간 자기상관).
- **입력·전제:** 결측·QC·매칭 후의 정렬된 짝. 시간·공간 간격과 변수의 자기상관 척도.
- **해석 기준:** N_eff가 작으면(강한 자기상관) 유의성·신뢰구간을 보수적으로 해석. 동일 지점 과대표집(한 부이가 표본 다수 차지)이면 영역 통계 편향 → 지점가중 또는 층화.
- **한계·주의:** 자기상관 무시 시 유의성 과대평가(가짜 유의). 결측 제거가 특정 조건(폭풍·야간) 편향 표집 유발. 동일 부이 다중 매칭 중복으로 독립성 위반(삼중정합·신뢰구간 모두 영향). 짝 구성 순서·필터가 모델/참조에 비대칭이면 가짜 bias.
- **출처:** Wilks, D. S., *Statistical Methods in the Atmospheric Sciences*(유효표본수·자기상관 보정, 검증표본 구성); Jolliffe, I. T., & Stephenson, D. B. (eds.), *Forecast Verification: A Practitioner's Guide in Atmospheric Science*(검증 표본·신뢰구간).

---

### 대표성 오차 (Representativeness error)
- **무엇을 측정/검증하나:** 서로 다른 공간·시간 척도(점 관측 vs 격자/픽셀 평균)를 비교할 때 생기는 **불가피한 불일치 오차**. 검증오차에서 모델오차와 분리해야 할 성분.
- **정의·수식:** 총 비교오차² ≈ 모델오차² + 관측오차² + 대표성오차². 대표성오차는 sub-pixel/sub-grid 변동의 분산으로 근사(고해상 자료·변동도로 추정).
- **적용 도메인/자료형:** 위성-부이, coarse 모델-점 관측. SSS·SST·해색 등 공간변동 큰 변수.
- **입력·전제:** sub-grid 변동 추정(고해상 관측, 변동도, 또는 분산 모형). 매칭 윈도 통계.
- **해석 기준:** 변동이 큰 연안·전선에서 대표성오차가 지배적 → 모델 평가에서 분리·차감해야 공정. 무시하면 모델오차 과대평가.
- **한계·주의:** 직접 측정 불가 → 추정 의존. 척도 정의가 모호하면 이중계산. 깊이·skin 차이와 혼동 주의.
- **출처:** Vinogradova, N., et al. (2022) "Satellite and In Situ Sampling Mismatches: Consequences for the Estimation of Satellite Sea Surface Salinity Uncertainties", *Remote Sensing* 14(8):1878 (MDPI); 위성검증 representativeness 리뷰(Frontiers in Remote Sensing, 2022–2023).

---

### 삼중 정합 (Triple collocation)
- **무엇을 측정/검증하나:** 참값(truth)을 모르는 상태에서 **서로 독립인 3개 자료(예: 모델·위성·부이)의 무작위 오차분산을 각각 추정**. 검증의 절대 기준이 없을 때 강력.
- **정의·수식:** 3 자료가 공통 참값 t에 대해 선형(xᵢ = aᵢ + bᵢ t + εᵢ)이고 오차가 상호·참값과 무상관이라는 가정 하에, 자료쌍 간 공분산으로 각 자료의 오차분산 σ²ᵢ를 해석적으로 추정. Extended TC(McColl 2014)는 추가로 각 자료의 참값 상관계수(ρ)도 산출.
- **적용 도메인/자료형:** 풍속·유의파고·SST·토양수분 등. 위성·모델·관측 3자 비교가 가능한 변수.
- **입력·전제:** 3개 독립(오차 무상관) 자료, 공통 시공간 매칭, 선형관계·정상성. 충분한 표본.
- **해석 기준:** 어느 자료가 더 정밀(작은 σ²)한지 절대비교 가능. SNR·calibration 상수도 산출.
- **한계·주의:** 오차 독립 가정 위반(공통 대표성오차·상관 오차, 또는 동화로 입력 공유) 시 편향. 표본 적으면 추정 불안정. 비선형 관계 부적합.
- **출처:** Stoffelen, A. (1998) "Toward the true near-surface wind speed: Error modeling and calibration using triple collocation", *J. Geophys. Res.* 103(C4), 7755–7766; McColl, K. A., et al. (2014) "Extended triple collocation: Estimating errors and correlation coefficients with respect to an unknown target", *Geophys. Res. Lett.* 41, 6229–6236.

---

### 단위 변환 / UDUNITS 정합 (Unit conversion / UDUNITS)
- **무엇을 측정/검증하나:** 비교 전 모든 자료를 동일 물리단위로 환산. 단위 불일치는 가장 흔한 정합 오류.
- **정의·수식:** UDUNITS 파서로 단위 문자열(`m s-1`, `K`, `kg m-2 s-1`) 해석·환산. 예: K↔°C, m/s↔knot, kg m⁻² s⁻¹↔mm/day(강수), Pa↔hPa.
- **적용 도메인/자료형:** 전 변수. 풍속·기온·강수·복사·기압·농도.
- **입력·전제:** CF `units` 속성이 UDUNITS 파싱 가능한 문자열이어야 함. scale_factor/add_offset(packed 자료) 선적용.
- **해석 기준:** 환산 후 물리적으로 타당한 범위인지 sanity check.
- **한계·주의:** 강수 누적(kg m⁻²=mm)과 율(rate)의 혼동. 온위·고도 등 비선형 변환. packed 변수의 offset/scale 누락 시 전량 오차.
- **출처:** UDUNITS-2 라이브러리 문서(Unidata); CF Conventions(`units` 요구사항 — UDUNITS 호환).

---

### CF convention / standard_name 정합 (CF metadata harmonization)
- **무엇을 측정/검증하나:** 변수의 물리적 의미·좌표·셀 의미를 표준 메타데이터로 통일해 "비교 가능한 양"인지 기계적으로 판별. 도메인 자동판별의 토대.
- **정의·수식:** `standard_name`(CF 표준명 표 수천 개), `units`, `cell_methods`, `coordinates`, `axis`, `_FillValue`, bounds 등을 규약대로 부여. standard_name이 같아야 동일 물리량으로 매칭.
- **적용 도메인/자료형:** 모든 NetCDF 격자·시계열. ERA5/GLORYS/CMEMS 등 권위자료가 CF 준수.
- **입력·전제:** CF Standard Name Table 참조. cf-checker(또는 cfchecks) 등으로 규약 검증 가능.
- **해석 기준:** standard_name·units가 일치해야 자동 매칭. 다르면 변수 의미·집계·부호규약(예: 상향/하향 플럭스) 재확인.
- **한계·주의:** 자료마다 변수명·부호규약(downward positive 등)·깊이/높이 기준이 달라 standard_name만으로 부족할 때가 있음. 누락된 메타데이터 보정 필요. 경도 표기·달력도 CF로 확인.
- **출처:** NetCDF Climate and Forecast (CF) Metadata Conventions(cfconventions.org, 공식 규약 문서); CF Standard Name Table; NASA Earthdata / Unidata CF 가이드.

---

### 결측·품질관리 처리 (Missing value / Quality Control)
- **무엇을 측정/검증하나:** 비교 표본에서 불량·결측 자료를 식별·제거·플래그. 검증 통계의 신뢰성 확보 전제.
- **정의·수식:** `_FillValue`/`missing_value` 마스킹 후 통계. QC 테스트: range(물리·기후 한계), spike(인접값 대비 급변), rate-of-change, flat-line/persistence, gap test. QARTOD 플래그(1=good, 2=not evaluated, 3=suspect, 4=fail, 9=missing) 부여.
- **적용 도메인/자료형:** 부이·관측소·CTD·위성. 수온·염분·해수면·풍속·파고.
- **입력·전제:** 변수별 임계값(기후·물리 한계), 인접 시각 자료. QC 플래그 컬럼.
- **해석 기준:** good(또는 good+probably good)만 검증에 사용하는 것이 표준. fail/suspect 제외 또는 별도 표기.
- **한계·주의:** 임계값이 과엄격하면 실제 극값(폭풍·이상기후) 제거. 과관대하면 불량 잔존. QC 플래그 규약(자료별 상이) 해석 주의. 결측 제거가 표본 편향 유발 가능.
- **출처:** U.S. IOOS QARTOD, "Manual for Real-Time Quality Control of In-situ Temperature and Salinity Data"; Argo Quality Control Manual for CTD and Trajectory Data(확인요); GTSPP QC 절차(확인요).

---

### 갭 채움 / 결측 보간 (Gap filling / imputation)
- **무엇을 측정/검증하나:** 짧은 결측을 메워 연속 시계열·격자를 복원. 단, 검증 표본에 합성값이 섞이지 않도록 주의가 필요.
- **정의·수식:** 짧은 갭은 선형/스플라인 보간(예: ≤1h 선형, 작은 갭 한정). 큰 갭·공간 결측은 EOF 기반 DINEOF(Data-Interpolating EOF) 재구성, 또는 OI/크리깅. 자료융합(data fusion)으로 다중 소스 결합.
- **적용 도메인/자료형:** 조위·기온·해색 위성(구름 결측) 등. 시계열·격자장.
- **입력·전제:** 갭 길이·간격, 공간/시간 자기상관. DINEOF는 다수 시점·공간점 필요.
- **해석 기준:** 채운 값은 플래그로 구분. 검증 통계에는 원자료만 쓰는 것이 원칙(채운 값 사용 시 명시).
- **한계·주의:** 긴 갭 보간은 인공 패턴·과도한 평활 유발. DINEOF는 모드 수 선택에 민감. 합성값을 검증에 포함하면 성능 낙관 편향.
- **출처:** Beckers, J.-M., & Rixen, M. (2003) "EOF Calculations and Data Filling from Incomplete Oceanographic Data Sets" (DINEOF), *J. Atmos. Oceanic Technol.* 20(12), 1839–1856; Cerlini, P. B., et al. (2020) "Quality control and gap-filling methods applied to hourly temperature observations", *Meteorol. Appl.* 27; IOOS QARTOD gap test.

---

### climatology / anomaly 산출 (Climatology and anomaly computation)
- **무엇을 측정/검증하나:** 기준기간 평균(기후값)과 그로부터의 편차(anomaly)를 계산. 계절성 제거 후 변동·추세·이벤트 비교에 사용.
- **정의·수식:** climatology = 기준기간(예 30년) 동일 달/일/시각의 평균. anomaly = 값 − 해당 기후값. 모델·참조 모두 **동일 기준기간**으로 계산해야 비교 타당.
- **적용 도메인/자료형:** SST·SSH·기온·강수 등. 월별·일별·조화(harmonic) 기후값.
- **입력·전제:** 충분히 긴 공통 기준기간. WMO 권고: 표준 normal은 최근 30년(예 1991–2020), 장기 기후변화 추적용 고정 기준기간은 1961–1990.
- **해석 기준:** 같은 기준기간 anomaly끼리 비교. 기준기간이 다르면 계통 차이 발생.
- **한계·주의:** 기준기간 불일치가 가짜 bias 유발. 짧은 기록의 기후값은 불안정. 윤년·결측 처리, 평활(예 조화적합) 여부에 따라 결과 변동.
- **출처:** WMO, "Guidelines on the Calculation of Climate Normals" (WMO-No. 1203, 2017 ed.); WMO Climatological Normals(community.wmo.int).

---

### 표준화 편차 (Standardized anomaly)
- **무엇을 측정/검증하나:** anomaly를 그 지점·계절의 표준편차로 나눠 무차원화. 분산이 다른 지역·변수 간 비교·합성에 사용.
- **정의·수식:** z = (x − μ_clim) / σ_clim. μ·σ는 기준기간의 평균·표준편차(달·계절별).
- **적용 도메인/자료형:** 다지점·다변수 비교, 극값 식별, 지수 산출(예 표준화강수지수 SPI 류).
- **입력·전제:** 안정적인 μ·σ 추정(충분한 기록). 분포가 크게 비대칭이면 변환(예 정규화) 고려.
- **해석 기준:** |z|>2 정도면 드문 편차. 지역 간 동일 척도로 비교 가능.
- **한계·주의:** σ가 작은 곳에서 z가 과도하게 커짐. 비정규 분포에서 해석 주의. 기준기간 의존.
- **출처:** Wilks, D. S., *Statistical Methods in the Atmospheric Sciences*(표준화 편차·기후통계 표준 교과서); WMO 기후 normal 지침.

---

### 편차보정 / 분위사상 (Bias correction / quantile mapping, CDF matching)
- **무엇을 측정/검증하나:** 모델(또는 위성)의 계통편차를 참조분포에 맞춰 보정. 단순 평균보정부터 분포 전체를 사상(quantile mapping)까지. 다운스케일·앙상블 후처리·비교 전 정렬에 사용.
- **정의·수식:** ① 평균/분산 보정: x' = (x − μ_m) σ_o/σ_m + μ_o. ② 분위사상(QM): x' = F_o⁻¹(F_m(x)), F_m·F_o는 모델·관측 누적분포(CDF). 변형으로 EDCDF/CDF-t(미래·해상도 변화에서 분포 진화 반영). delta-change/PDF transform 포함.
- **적용 도메인/자료형:** 기온·강수·풍속·복사 등. 모델 격자값 ↔ 고해상 재분석/관측소 분포 정합. 강수의 빈도·강도 동시 보정에 특히 유용.
- **입력·전제:** 보정용 학습기간(공통 colocation 표본). 모델·참조의 분포(또는 분위) 추정. 검증은 학습과 다른 독립기간에서.
- **해석 기준:** 보정 후 분포·분위가 참조와 정합. **주의:** 보정 자체가 평가를 낙관 편향시킬 수 있으므로 보정 전/후를 구분 보고하고, 학습기간으로 검증하지 말 것(독립검증).
- **한계·주의:** 보정함수가 학습기간에 과적합 → 외삽(미래·극값)에서 신뢰 낮음. QM이 추세·극값 변화를 왜곡할 수 있음(EDCDF/CDF-t가 일부 완화). 다변수 일관성(상호상관) 깨질 수 있음 → 다변수 QM 고려. 보정값을 "검증"으로 오용 금지.
- **출처:** Wood, A. W., et al. (2004) "Hydrologic implications of dynamical and statistical approaches to downscaling climate model outputs", *Climatic Change* 62, 189–216(BCSD/분위사상); Cannon, A. J., et al. (2015) "Bias Correction of GCM Precipitation by Quantile Mapping: How Well Do Methods Preserve Changes in Quantiles and Extremes?", *J. Climate* 28, 6938–6959; Maraun, D. (2013) "Bias Correction, Quantile Mapping, and Downscaling: Revisiting the Inflation Issue", *J. Climate* 26, 2137–2143.

---

### 조석 분리 (Detiding / tidal harmonic analysis)
- **무엇을 측정/검증하나:** 해수면·유속에서 조석 성분을 분리해 비조석(잔차: 폭풍해일·평균류 등) 신호만 비교하거나, 조석 자체를 검증.
- **정의·수식:** 조화분석 — 알려진 조석 분조 주파수에 정현파를 최소제곱 적합해 각 분조의 진폭·위상 추정. 잔차 = 관측 − 조석재구성. 도구: T_TIDE(MATLAB), UTide(다년·불규칙·결측 처리, 강건 L1/L2), pytides/utide(Python).
- **적용 도메인/자료형:** 조위·조류 시계열. 해수면·해류 검증 전처리.
- **입력·전제:** 충분히 긴 기록(분조 분리에 필요한 길이; Rayleigh 기준), 정확한 시각·달력. UTide는 결측·불규칙 간격 처리 용이.
- **해석 기준:** 신뢰구간이 좁은 분조만 신뢰. 잔차 분석으로 해일·비조석 변동 평가.
- **한계·주의:** 기록이 짧으면 인접 분조 분리 불가(예 S2/K2). 비정상(연주기 변동·천해 분조)에서 가정 위반. 조류는 벡터(장축/단축, tidal ellipse) 처리 필요.
- **출처:** Pawlowicz, R., Beardsley, B., & Lentz, S. (2002) "Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE", *Computers & Geosciences* 28, 929–937; Codiga, D. L. (2011) "Unified Tidal Analysis and Prediction Using the UTide Matlab Functions"; Foreman, M. G. G. (1977) "Manual for Tidal Heights Analysis and Prediction", Pacific Marine Science Report 77-10.

---

### 시계열 필터링 (Low/high/band-pass filtering)
- **무엇을 측정/검증하나:** 비교 전 특정 주파수대(잡음·고주파, 또는 관심 대역)를 분리. 평활·이벤트 추출.
- **정의·수식:** 이동평균·Butterworth·Lanczos·Godin 등 필터로 저역/고역/대역 통과. 예: Godin/Lanczos 저역필터로 조석 제거(비조화적 detiding). 롤오프·위상지연 특성 고려.
- **적용 도메인/자료형:** 해수면·유속·기상 시계열. 잡음 제거, 조석·관성진동 분리.
- **입력·전제:** 균일 시간간격(아니면 재표본), 컷오프 주파수 설정, 가장자리(edge) 효과 처리.
- **해석 기준:** 필터 후 잔존 신호가 관심 척도와 맞는지. 모델·관측에 동일 필터 적용해야 공정.
- **한계·주의:** 위상지연·끝단 손실(window 길이만큼). 과도한 평활로 극값 손실. 비균일 간격·결측에서 필터 왜곡 → 선보간 필요. 모델/관측에 다른 필터 적용 시 가짜 차이.
- **출처:** Emery, W. J., & Thomson, R. E., *Data Analysis Methods in Physical Oceanography*(Elsevier; 필터·스펙트럼·시계열 표준 교과서); Walters, R. A., & Heston, C. (1982) Godin-type 필터(조석 제거) 관련 문헌(확인요).

---

### 수직 보간·층 정합 (Vertical interpolation / depth matching)
- **무엇을 측정/검증하나:** 모델의 연직 좌표(z, sigma, hybrid)와 관측 깊이(CTD·Argo 표준층)를 정합. 해양 연직 검증의 전제.
- **정의·수식:** 깊이축 선형/스플라인 보간으로 공통 표준 깊이(예 Argo 표준 압력층)로 변환. sigma/s-좌표↔z-좌표 변환에는 해저지형·해수면 필요. 위성 표층(skin/sub-skin) vs in situ 수 m 깊이(bulk) 보정.
- **적용 도메인/자료형:** 수온·염분·유속의 연직 프로파일. SST(표층) 매칭 시 깊이정의 보정.
- **입력·전제:** 정확한 연직좌표 메타데이터(sigma 파라미터, 해저지형). 압력↔깊이 변환(TEOS-10/GSW). 혼합층 부근 급경사 주의.
- **해석 기준:** 동일 깊이/압력층에서만 비교. 표층 skin–bulk 차이(수십분의 1~수 ℃, 주간 가열·바람 의존) 보정 후 SST 검증.
- **한계·주의:** 강한 수온약층(thermocline)에서 보간오차 큼. sigma↔z 변환 오류. 깊이 불일치를 무시하면 표층 SST에서 편향. skin–bulk는 일변동(diurnal warming)에 강하게 의존.
- **출처:** IOC, SCOR & IAPSO (2010) "The international thermodynamic equation of seawater – 2010 (TEOS-10)", IOC Manuals and Guides No. 56(UNESCO); GSW Oceanographic Toolbox(teos-10.org; 압력-깊이·해수특성); GHRSST GDS 2.0(skin/sub-skin/foundation SST 정의).

---

## 출처(References)

검증 가능한 실제 출처만 표기했다. 표준 교과서·표준 규약은 그렇게 명시했고, 본문에서 1차 출처를 직접 확인하지 못한 항목만 "(확인요)"로 남겼다(DOI를 임의 생성하지 않음). 아래 1차 문헌·규약 링크는 본 작업 중 웹으로 존재를 확인했다.

**표준 규약·지침 (Standards & Guidelines)**
- NetCDF Climate and Forecast (CF) Metadata Conventions — https://cfconventions.org/cf-conventions/cf-conventions.html ; CF Home — https://cfconventions.org/ ; CF Standard Name Table.
- NASA Earthdata, "Climate and Forecast Metadata Conventions" — https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions
- Unidata, "NetCDF and CF — The Basics" — https://unidata.github.io/python-training/workshop/CF%20Conventions/netcdf-and-cf-the-basics/
- UDUNITS-2 library documentation (Unidata) — 단위 파싱·환산 표준.
- PROJ / pyproj documentation; EPSG Geodetic Parameter Dataset (epsg.org) — 좌표·투영·datum 변환 표준.
- WMO, "Guidelines on the Calculation of Climate Normals" (WMO-No. 1203, 2017 ed.) — https://library.wmo.int/viewer/55797/ ; WMO Climatological Normals — https://community.wmo.int/en/activity-areas/climate-services/climate-products-and-initiatives/wmo-climatological-normals
- U.S. IOOS QARTOD, "Manual for Real-Time Quality Control of In-situ Temperature and Salinity Data" — https://cdn.ioos.noaa.gov/media/2020/03/QARTOD_TS_Manual_Update2_200324_final.pdf
- IOC, SCOR & IAPSO (2010), "The international thermodynamic equation of seawater – 2010 (TEOS-10): Calculation and use of thermodynamic properties", IOC Manuals and Guides No. 56, UNESCO, 196 pp. — https://www.teos-10.org/pubs/TEOS-10_Manual.pdf ; GSW Oceanographic Toolbox — https://www.teos-10.org/software.htm
- GHRSST Data Processing Specification (GDS) 2.0 — skin/sub-skin/foundation SST 정의 — https://www.ghrsst.org/

**재격자화·보간 (Regridding & Interpolation)**
- Jones, P. W. (1999), "First- and Second-Order Conservative Remapping Schemes for Grids in Spherical Coordinates", *Monthly Weather Review*, 127, 2204–2210.
- Jones, P. W. (1998), "A User's Guide for SCRIP: A Spherical Coordinate Remapping and Interpolation Package" (Los Alamos National Laboratory, LACC 98-45) — https://github.com/SCRIP-Project/SCRIP
- Shepard, D. (1968), "A two-dimensional interpolation function for irregularly-spaced data", *Proceedings of the 23rd ACM National Conference*, 517–524 (역거리가중 IDW 원전).
- ESMF / ESMPy Regridding documentation (bilinear, nearest_s2d/d2s, nearest_idavg, patch, first/second-order conservative, masking·normalization) — https://earthsystemmodeling.org/regrid/ ; ESMPy Overview — https://earthsystemmodeling.org/esmpy_doc/release/latest/html/intro.html
- xESMF, "Comparison of seven regridding algorithms" — https://xesmf.readthedocs.io/en/latest/notebooks/Compare_algorithms.html ; xESMF 경도 주기성(`periodic`) 문서.
- CDO (Climate Data Operators) User Guide — `remapbil`, `remapbic`, `remapcon`, `remapdis`, `remapnn` — https://code.mpimet.mpg.de/projects/cdo
- "Benchmarking Regridding Libraries Used in Earth System Modelling", *Mathematical and Computational Applications* 27(2):31 (MDPI, 2022) — https://www.mdpi.com/2297-8747/27/2/31
- Taylor, K. E. (2024), "Truly conserving with conservative remapping methods", *Geoscientific Model Development*, 17, 415–430 — https://doi.org/10.5194/gmd-17-415-2024

**객관분석·지구통계 (Objective Analysis & Geostatistics)**
- Troupin, C., et al. (2012), "Generation of analysis and consistent error fields using the Data Interpolating Variational Analysis (DIVA)", *Ocean Modelling*, 52–53, 90–101 — https://www.sciencedirect.com/science/article/abs/pii/S1463500312000790
- Troupin, C., et al., "Introduction to Optimal Interpolation and Variational Analysis" (GHER/SeaDataNet 교육자료) — https://www.researchgate.net/publication/265626429
- DIVA / GHER software — http://modb.oce.ulg.ac.be/mediawiki/index.php/DIVA ; https://github.com/gher-uliege/DIVA
- Daley, R. (1991), *Atmospheric Data Analysis* (Cambridge University Press; OI·자료동화 표준 교과서).
- Cressie, N. (1993), *Statistics for Spatial Data* (Wiley; 지구통계·크리깅 표준 교과서).

**Colocation·대표성·삼중정합 (Colocation, Representativeness, Triple Collocation)**
- Vinogradova, N., et al. (2022), "Satellite and In Situ Sampling Mismatches: Consequences for the Estimation of Satellite Sea Surface Salinity Uncertainties", *Remote Sensing* 14(8):1878 (MDPI) — https://www.mdpi.com/2072-4292/14/8/1878
- Urraca, R., et al. (2024), "Impact of the Spatio-Temporal Mismatch Between Satellite and In Situ Measurements on Validations of Surface Solar Radiation", *J. Geophys. Res.: Atmospheres*, 129 — https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JD041007
- "Validation of satellite water products based on HYPERNETS in situ data using a Match-up Database (MDB) file structure", *Frontiers in Remote Sensing* (2024) — https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2024.1330317/full
- Stoffelen, A. (1998), "Toward the true near-surface wind speed: Error modeling and calibration using triple collocation", *J. Geophys. Res.*, 103(C4), 7755–7766.
- McColl, K. A., et al. (2014), "Extended triple collocation: Estimating errors and correlation coefficients with respect to an unknown target", *Geophysical Research Letters*, 41, 6229–6236 — https://doi.org/10.1002/2014GL061322

**시계열·조석·QC·결측 (Time Series, Tides, QC, Gap Filling)**
- Pawlowicz, R., Beardsley, B., & Lentz, S. (2002), "Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE", *Computers & Geosciences*, 28, 929–937 — https://doi.org/10.1016/S0098-3004(02)00013-4
- Codiga, D. L. (2011), "Unified Tidal Analysis and Prediction Using the UTide Matlab Functions", GSO Technical Report 2011-01, University of Rhode Island.
- Foreman, M. G. G. (1977), "Manual for Tidal Heights Analysis and Prediction", Pacific Marine Science Report 77-10, Institute of Ocean Sciences, Sidney, B.C. (rev. 2004).
- Beckers, J.-M., & Rixen, M. (2003), "EOF Calculations and Data Filling from Incomplete Oceanographic Data Sets" (DINEOF), *Journal of Atmospheric and Oceanic Technology*, 20(12), 1839–1856 — https://doi.org/10.1175/1520-0426(2003)020<1839:ECADFF>2.0.CO;2
- Cerlini, P. B., et al. (2020), "Quality control and gap-filling methods applied to hourly temperature observations", *Meteorological Applications*, 27 — https://doi.org/10.1002/met.1913
- Emery, W. J., & Thomson, R. E., *Data Analysis Methods in Physical Oceanography* (Elsevier; 필터·스펙트럼·시계열 표준 교과서) — https://shop.elsevier.com/books/data-analysis-methods-in-physical-oceanography/thomson/978-0-323-91723-0

**편차보정·다운스케일 (Bias Correction & Downscaling)**
- Wood, A. W., et al. (2004), "Hydrologic implications of dynamical and statistical approaches to downscaling climate model outputs", *Climatic Change*, 62, 189–216.
- Cannon, A. J., Sobie, S. R., & Murdock, T. Q. (2015), "Bias Correction of GCM Precipitation by Quantile Mapping: How Well Do Methods Preserve Changes in Quantiles and Extremes?", *Journal of Climate*, 28, 6938–6959 — https://doi.org/10.1175/JCLI-D-14-00754.1
- Maraun, D. (2013), "Bias Correction, Quantile Mapping, and Downscaling: Revisiting the Inflation Issue", *Journal of Climate*, 26, 2137–2143 — https://doi.org/10.1175/JCLI-D-12-00821.1

**검증 일반·통계 (Verification & General Statistics)**
- Wilks, D. S., *Statistical Methods in the Atmospheric Sciences* (Academic Press; 표준화 편차·유효표본수·기후통계 표준 교과서).
- Jolliffe, I. T., & Stephenson, D. B. (eds.), *Forecast Verification: A Practitioner's Guide in Atmospheric Science* (Wiley; 검증 표본·신뢰구간).

**벡터 회전·모델 격자 (Vector Rotation & Model Grids)**
- NEMO Ocean Engine reference manual (격자각·벡터 회전, ORCA tripolar 격자) — https://www.nemo-ocean.eu/
- WRF ARW User's Guide (`COSALPHA`/`SINALPHA` earth-relative 풍속 변환).
