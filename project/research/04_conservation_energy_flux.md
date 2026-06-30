# 보존·에너지·플럭스 진단 (Conservation, Energy, and Flux Diagnostics)

이 문서는 우리 수치모델(NetCDF 격자자료, CSV/텍스트 시계열) 결과를 ERA5/GLORYS 재분석, 관측소·위성 자료와 비교·검증할 때 사용하는 **물리 보존성·에너지·플럭스 진단** 방법 카탈로그다. 단순 통계오차(평균제곱근오차 RMSE 등)를 넘어, 모델이 질량·체적·운동량·열·염·에너지를 **물리적으로 일관되게 보존**하는지, 그리고 운동에너지(kinetic energy, KE)·와도(vorticity)·수송량(transport)·에너지 스펙트럼 같은 **역학적 진단량**이 권위자료와 정합하는지를 점검하는 것이 목표다. 각 방법은 "메서드 카드" 형식(측정 대상 / 수식 / 적용 도메인·자료형 / 입력·전제 / 해석 기준 / 한계 / 출처)으로 정리한다. 도메인 자동판별(해류/수온/해수면/파랑/기상) 후 해당되는 카드를 선택해 레시피로 조합하는 것을 권장한다.

> **이 카탈로그의 검증 철학 (Skill 적용 지침)**
> - **닫힘(closure) 우선**: 모든 수지(budget)는 좌변 시간변화 = 우변 플럭스 합으로 재구성하고, **잔차(residual)를 지배항 대비 상대비율**로 보고한다. 잔차가 작아야 모델이 그 물리량을 보존한다.
> - **online 우선, offline 검증**: 가장 정확한 닫힘은 모델이 실행 중 누적한 항(online)에서 나온다. 우리 Skill이 NetCDF 시간평균장으로 사후 재구성(offline)할 때는 반드시 '온라인 vs 오프라인' 카드의 에디 보정항을 점검한다.
> - **비교 짝(pairing) 명시**: 각 진단은 "우리 모델 vs (ERA5 표면플럭스 / GLORYS 3D장 / 위성 알티미터 SSH / 관측배열 RAPID·드리프터)" 중 무엇과 비교하는지를 카드에 적었다.
> - **정량 임계값은 관행(convention)이며 영역·해상도 의존**임을 항상 명시한다.

## 한 줄 목차 (This file covers)
- **질량·체적 보존 (Mass/Volume conservation closure)** — 연속방정식 잔차, 체적수지 닫힘
- **운동량 수지 (Momentum budget closure)** — 운동방정식 항별 균형·잔차
- **열 수지 닫힘 (Heat budget closure)** — 해양열함량(OHC) 변화 = 플럭스 수렴 + 표면강제
- **염 수지 닫힘 (Salt/Salinity budget closure)** — 염량 보존, 가상염플럭스 진단
- **온라인 vs 오프라인 수지 진단 (Online vs offline budget diagnostics)** — 시간상관 항 정확도
- **운동에너지 KE (Kinetic energy)** — 평균/총 KE 진단
- **에디 운동에너지 EKE (Eddy kinetic energy)** — 시간평균 분리, mesoscale 강도
- **평균 운동에너지 MKE (Mean kinetic energy)** — MKE/EKE 분할비
- **가용위치에너지 APE (Available potential energy)** — 기준상태 대비 가용 PE
- **로렌츠 에너지 사이클 (Lorenz energy cycle, LEC)** — MKE·MAPE·EKE·EAPE 4상자 변환율
- **상대와도·행성와도 (Relative & planetary vorticity)** — ζ, f, ζ+f
- **포텐셜 와도 PV (Potential vorticity)** — Ertel/QG PV 보존 진단
- **엔스트로피 (Enstrophy)** — ζ²/2, 와도 분산·캐스케이드
- **발산 (Divergence)** — 수평발산, 비발산성 점검
- **체적 수송 (Volume transport)** — 단면 적분 Sverdrup transport
- **열 수송 (Heat transport)** — 단면 열플럭스, 자오면 열수송(MHT)
- **자오면 열수송 분해 (MHT overturning/gyre decomposition)** — Hall–Bryden 분해
- **염 수송 (Salt/freshwater transport)** — 단면 염·담수 플럭스, Mov/Fov 지표
- **자오면 전복순환 (Meridional overturning streamfunction, MOC/AMOC)** — RAPID 26.5°N 비교
- **순압 유선함수 (Barotropic/depth-integrated streamfunction)** — gyre 수송·Sverdrup 비교
- **Sverdrup 균형 (Sverdrup balance)** — 풍응력 curl → 내부 수송
- **수괴변환 (Water-mass transformation, WMT)** — 표면강제→밀도층 체적변환
- **지형류 균형 (Geostrophic balance) / 열풍 (Thermal wind)** — 역학고도·전단 정합
- **동적 해수면·스테릭 높이 (Dynamic/steric sea level)** — SSH 성분 분해·알티미터 비교
- **혼합층 깊이·부력플럭스 (Mixed-layer depth & buoyancy flux)** — 표층 강제·대류 진단
- **베르누이 함수 (Bernoulli function)** — 정상류 보존 진단
- **Ekman 수송·펌핑 (Ekman transport/pumping)** — 풍응력 회전 강제
- **KE 파수 스펙트럼 (KE wavenumber spectra)** — k⁻³/k⁻⁵ᐟ³ 기울기 진단
- **스펙트럼 에너지·엔스트로피 캐스케이드 (Spectral energy/enstrophy flux)** — 상향/하향 전달
- **Coarse-graining 에너지 플럭스 (Coarse-graining scale flux)** — 공간국지 scale-space 전달
- **밀도층(isopycnal) 수지 진단 (Isopycnal-coordinate budgets)** — 밀도좌표 보존
- **실효(수치) diapycnal 혼합 진단 (Effective/numerical diapycnal mixing)** — spurious mixing 정량
- **전지구 에너지·물수지 마감 (Global energy/water imbalance)** — TOA·표면 잔차
- **에너지·플럭스량 요약 통계·테일러 다이어그램 (Summary skill metrics for fields)** — 패턴 정합 종합

---

### 질량·체적 보존 닫힘 (질량/체적 보존 / Mass & Volume Conservation Closure)
- **무엇을 측정/검증하나**: 모델 격자에서 연속방정식이 만족되는지, 즉 비압축·Boussinesq 가정 하에서 속도장의 3차원 발산이 0(혹은 자유표면/담수플럭스만큼)인지를 점검한다. 폐쇄된 영역(전 해양, 또는 닫힌 단면으로 둘러싼 박스)에서 들어오고 나가는 체적이 균형을 이루는지 확인한다.
- **정의·수식**: Boussinesq 연속식 ∂u/∂x + ∂v/∂y + ∂w/∂z = 0. 자유표면 모델은 ∂η/∂t + ∇·(∫u dz) = (P−E+R). 박스 닫힘: Σ(체적유입) − Σ(체적유출) − ∂V/∂t ≈ 0 (잔차가 기계 정밀도 수준이어야 함).
- **적용 도메인/자료형**: 해류·해수면(격자 NetCDF, u/v/w·η). 기상 모델에도 동일 원리(질량연속).
- **입력·전제**: 3D 속도장(u,v,w), 격자 셀 면적·두께(또는 layer thickness), 자유표면 η, 표면 담수플럭스. 모델 격자(Arakawa B/C-grid) 위치 정합 필요.
- **해석 기준**: 잔차가 부피수송 대비 무시할 수준(예: 박스 순체적수송 잔차 < 0.01~0.1 Sv, 또는 격자 셀에서 round-off 수준)이면 양호. 잔차가 크면 수직속도 w 진단오류, 격자 처리오류, 후처리 보간오류 의심.
- **한계·주의**: w는 보통 진단량(연속식에서 적분)이므로 자체로 보존되도록 계산됨 → 진짜 검증은 **오프라인 후처리**가 격자·시간평균을 올바로 재현하는지에 달림. 시간평균장으로 닫으면 부정확(아래 '온라인 vs 오프라인' 카드 참조).
- **출처**: Griffies, *Fundamentals of Ocean Climate Models* (Princeton, 2004), 연속방정식·체적보존 장. 표준 GFD 교과서(Vallis, *Atmospheric and Oceanic Fluid Dynamics*, 2nd ed., 2017).

---

### 운동량 수지 닫힘 (운동량 수지 / Momentum Budget Closure)
- **무엇을 측정/검증하나**: 운동방정식의 각 항(국지가속 + 이류 + 코리올리 + 압력경도 + 마찰/혼합 + 풍응력)의 합이 0(잔차)이 되는지, 모델이 운동량을 일관되게 보존하는지 점검. 특정 균형(지형류·Ekman·Sverdrup)이 어디서 성립하는지도 진단.
- **정의·수식**: ∂u/∂t + (u·∇)u + f×u = −(1/ρ₀)∇p + ∇·(A∇u) + F. 잔차 R = (좌변 합) − (우변 합)이 0에 가까워야 한다. 항별 크기 비교로 지배균형 식별.
- **적용 도메인/자료형**: 해류(격자 u,v,p, 풍응력 τ), 기상(바람·기압). 단면·박스 또는 격자점 단위.
- **입력·전제**: 모델이 **온라인으로 누적한 각 항(diagnostic terms)**을 출력해야 정확한 닫힘 가능. 오프라인 재구성 시 이류항의 시간상관 손실 주의.
- **해석 기준**: 잔차가 지배항 대비 작으면(<수%) 양호. 잔차가 특정 영역에서 크면 수평혼합/수직혼합 파라미터화, 압력경도 오차(특히 sigma-coordinate의 pressure gradient error) 의심.
- **한계·주의**: sigma/terrain-following 좌표는 가파른 지형에서 압력경도 오차가 운동량 수지를 오염. 항 출력이 없으면 정성 진단(지배균형 추정)에 그침.
- **출처**: Griffies (2004); Vallis (2017). 압력경도 오차: Haney (1991), *J. Phys. Oceanogr.* 21, 610–619, "On the pressure gradient force over steep topography in sigma coordinate ocean models".

---

### 열 수지 닫힘 (열 수지 / Heat Budget Closure)
- **무엇을 측정/검증하나**: 해양열함량(ocean heat content, OHC)의 시간변화가 이류·확산에 의한 열 수렴과 표면 열플럭스의 합으로 정확히 설명되는지(닫히는지). 모델 내부 열 보존성과, 권위자료(ERA5 표면플럭스, GLORYS OHC)와의 정합을 동시에 점검.
- **정의·수식**: ρ₀cₚ ∂θ/∂t = −ρ₀cₚ ∇·(uθ) + ∇·(ρ₀cₚ κ∇θ) + Q_surf/h. 박스 적분: ∂/∂t(∫ρ₀cₚθ dV) = −∮ρ₀cₚθ u·n dA + ∮κ∇θ·n dA + ∫Q_surf dA. 전 해양 평균 시 이류·확산은 재분배만 → OHC 변화는 표면강제로만 발생.
- **적용 도메인/자료형**: 수온·해류(격자 θ,u, 표면 Q). ECCO/GLORYS류 재분석과 비교.
- **입력·전제**: 온라인 누적 advective/diffusive heat flux, 표면 순열플럭스(SW+LW+SH+LH), 기준온도 선택 명시. 시간평균 아닌 full-resolution 플럭스 권장.
- **해석 기준**: 박스 열수지 잔차가 표면 강제 대비 작으면(예: 수 W/m² 이하) 닫힘 양호. ECCO v4 튜토리얼은 온라인 항 사용 시 기계정밀도 수준 닫힘을 보고. **ERA5 비교 팁**: ERA5 표면 순열플럭스를 모델 격자로 보간해 박스 ∫Q_surf로 쓰면, OHC 추세 차이가 강제 차이 때문인지 내부 수송 때문인지 분리 가능.
- **한계·주의**: 기준온도(reference temperature) 선택이 열수송 절대값에 영향(닫힌 단면이면 상쇄). 비선형 상태방정식·penetrative shortwave·virtual flux 항 누락 시 잔차 발생. 표면플럭스 부호규약(상향+ vs 하향+) 혼동 주의.
- **출처**: ECCO Version 4 Python Tutorial, "Global Heat Budget Closure"(ecco-v4-python-tutorial.readthedocs.io); Griffies et al., GFDL ESM2M ocean heat budget working notes(mom-ocean.github.io); Buckley & Marshall (2016), *Rev. Geophys.* 54, 5–63, AMOC·열수지 리뷰(DOI 10.1002/2015RG000493).

---

### 염 수지 닫힘 (염/염분 수지 / Salt & Salinity Budget Closure)
- **무엇을 측정/검증하나**: 박스/층 내 염량(salt content) 변화가 염 이류·확산 수렴과 표면 담수(가상)염플럭스로 설명되는지. 염 보존 및 담수수지 일관성 점검.
- **정의·수식**: ∂S/∂t = −∇·(uS) + ∇·(κ∇S) + (S·(E−P−R))/h (가상염플럭스) 또는 실담수플럭스(real freshwater flux) 형태. 박스 염량 보존: ∂/∂t(∫S dV) = −∮S u·n dA + 확산 + 표면항.
- **적용 도메인/자료형**: 염분·해류(격자 S,u, 표면 E−P−R). GLORYS·EN4와 비교.
- **입력·전제**: 온라인 염플럭스 항, 표면 담수강제, 모델의 염 경계조건(virtual salt flux vs real freshwater) 방식 확인.
- **해석 기준**: 잔차가 작으면 양호. 염 수지는 종종 잔차로 계산되는 미해결 항(대류성 수직혼합·수치혼합)을 포함 → 잔차 항의 물리적 해석 필요.
- **한계·주의**: 가상염플럭스 방식은 전 해양 염량을 인위적으로 비보존시킬 수 있음. 실담수플럭스(자유표면 체적변화) 방식이 보존성에 유리.
- **출처**: Griffies (2004) 염보존 장; Megann (2018), *Ocean Modelling* 121, 19–33(염·열 수지에서 수치혼합 잔차 진단, DOI 10.1016/j.ocemod.2017.11.001); NEMO 문서. (※ 원본의 "The budgets of heat and salinity in NEMO (2013)"는 저자/서지 특정이 어려워 '확인요'로 강등; 대신 검증된 Megann (2018)로 대체.)

---

### 온라인 vs 오프라인 수지 진단 (온라인/오프라인 수지 / Online vs Offline Budget Diagnostics)
- **무엇을 측정/검증하나**: 수지(열·염·운동량) 항을 **모델 실행 중(online) 매 스텝 누적**한 것과, **사후 시간평균장(offline)으로 재구성**한 것의 차이를 비교해 후처리 검증 파이프라인의 신뢰도를 평가.
- **정의·수식**: 이류 플럭스 ⟨uθ⟩ ≠ ⟨u⟩⟨θ⟩. 차이항(에디 플럭스) ⟨u'θ'⟩ = ⟨uθ⟩ − ⟨u⟩⟨θ⟩이 누락되면 오프라인 수지가 닫히지 않는다.
- **적용 도메인/자료형**: 모든 수지(격자). 우리 검증 Skill이 후처리로 수지를 재현하려 할 때 필수 진단.
- **입력·전제**: 가능하면 online 누적 항 출력. 없으면 고빈도(예: 일/시간) 스냅샷으로 ⟨uθ⟩ 근사.
- **해석 기준**: online과 offline 잔차 차이가 작아야 후처리 신뢰 가능. 큰 차이 = 시간평균 빈도 부족 또는 에디항 누락. **실무 규칙**: mesoscale 활동영역에서는 월평균만으로 수지가 닫히지 않으므로, 그 영역의 offline 결과는 정성 해석에 한정한다.
- **한계·주의**: 월평균만 있으면 mesoscale 시간상관 손실로 수지 크게 어긋남. 저장 빈도가 핵심 제약.
- **출처**: ECCO, "Evaluating budgets in ECCOv4r3"(ecco-group.org); MOM6 Analysis Cookbook(water-mass transformation, 밀도그리드 온라인 binning).

---

### 운동에너지 (운동에너지 / Kinetic Energy, KE)
- **무엇을 측정/검증하나**: 유속장의 운동에너지 밀도·총량. 모델 순환 강도가 권위자료와 정합하는지의 1차 진단.
- **정의·수식**: KE = ½ρ₀(u²+v²) (단위체적당) 또는 KE = ½(u²+v²) (질량당). 총 KE = ∫½ρ₀|u|² dV.
- **적용 도메인/자료형**: 해류(격자 u,v), 기상(바람). 표층/적분/단면.
- **입력·전제**: u,v 격자 정합(C-grid는 스칼라점으로 보간 필요), 밀도 또는 Boussinesq ρ₀.
- **해석 기준**: 공간패턴·크기를 GLORYS·드리프터(Global Drifter Program)·위성 지형류 KE와 비교. 주요 해류(쿠로시오·걸프스트림·ACC)에서 KE 과소면 해상도/혼합 과다 의심.
- **한계·주의**: 격자 보간·시간평균이 KE를 체계적으로 낮춤(평균이 변동을 평활). 표층 지형류 KE만 비교 시 풍성·ageostrophic 성분 누락.
- **출처**: Vallis (2017); 표준 GFD 에너지론. 위성 지형류 KE 비교: AVISO/CMEMS 알티미터 산물(현업 위성고도계 SSH 산물).

---

### 에디 운동에너지 (에디 운동에너지 / Eddy Kinetic Energy, EKE)
- **무엇을 측정/검증하나**: 시간평균 흐름에서 분리한 변동(에디) 성분의 운동에너지. mesoscale 에디 활동 강도. 위성 알티미터 EKE와의 정합이 모델 mesoscale 재현력의 핵심 척도.
- **정의·수식**: EKE = ½⟨u'²+v'²⟩, 여기서 u' = u − ⟨u⟩ (Reynolds 분해). 위성: 지형류 변동 u'_g = −(g/f)∂η'/∂y, v'_g = (g/f)∂η'/∂x로부터 EKE_geo.
- **적용 도메인/자료형**: 해류·해수면(격자 u,v 시계열, 또는 SSH 알티미터). 표층 비교가 일반적.
- **입력·전제**: 충분히 긴 시계열(평균 정의), 일관된 시간평균 창. 위성 비교 시 동일 필터(지형류 근사) 적용.
- **해석 기준**: EKE 지도·크기를 AVISO/CMEMS와 비교. 에디분해(0.1°급) 모델은 EKE를 근접 재현; 비분해 모델은 크게 과소. Arctic 1-km 연구는 4→1km 정밀화에서 EKE 대폭 증가를 보고(해상도 민감성의 예). 경계류·전선·지형경사에서 EKE 최대.
- **한계·주의**: 위성은 표층 지형류 EKE만 측정(ageostrophic·심층 제외). 평균 정의(시간창)에 민감. Mean과 eddy 분리는 임의적(시간 vs 공간 vs ensemble).
- **출처**: Stammer (1997), *J. Phys. Oceanogr.* 27, 1743–1769, "Global Characteristics of Ocean Variability ... TOPEX/POSEIDON"(위성 EKE 기준); Wang et al. (2020), *GRL* "Eddy Kinetic Energy in the Arctic Ocean ... 1-km"(DOI 10.1029/2020GL088550); MPAS-Analysis EKE climatology 문서.

---

### 평균 운동에너지 & MKE/EKE 분할 (평균 운동에너지 / Mean Kinetic Energy & Partition)
- **무엇을 측정/검증하나**: 시간평균 흐름의 KE(MKE)와 에디 KE(EKE)의 비율·공간분포. 에너지가 평균순환 vs 변동에 어떻게 배분되는지.
- **정의·수식**: MKE = ½(⟨u⟩²+⟨v⟩²); 총 KE = MKE + EKE. 분할비 EKE/MKE.
- **적용 도메인/자료형**: 해류(격자 시계열).
- **입력·전제**: Reynolds 분해를 위한 시계열·일관된 평균창.
- **해석 기준**: 대양 대부분에서 EKE가 MKE보다 1자리 이상 크다(관측·고해상 모델 공통). 모델의 EKE/MKE가 비현실적으로 낮으면 mesoscale 미분해.
- **한계·주의**: 평균창 선택이 분할을 바꿈. 강한 평균류 영역(경계류 축)에서는 MKE도 큼.
- **출처**: Vallis (2017); Stammer (1997, *JPO*) 위성 EKE 관측.

---

### 가용위치에너지 (가용위치에너지 / Available Potential Energy, APE)
- **무엇을 측정/검증하나**: 단열적 질량재배치로 방출 가능한 위치에너지. 성층의 에너지 저장량·baroclinic instability 잠재력. 에디 APE는 EKE의 주 공급원.
- **정의·수식**: APE = TPE − TPE_ref (기준상태=단열재배치로 얻는 최소 총위치에너지). 근사식(준지형): APE ≈ ½∫(g²/(ρ₀N²))ρ'² dV, ρ' = ρ − ⟨ρ⟩(z), N²=−(g/ρ₀)∂ρ_ref/∂z.
- **적용 도메인/자료형**: 수온·염분(밀도)(격자 3D). 성층 진단.
- **입력·전제**: 3D 밀도장, 기준성층 ρ_ref(z) 정의(영역평균 또는 Lorenz 정렬). N² 계산.
- **해석 기준**: APE 분포가 baroclinic 활동영역(전선·경계류)과 일치해야. 전구 적분값을 권위 추정과 비교하되, **APE 정의가 비유일**하므로 절대값보다 공간패턴·상대비교에 무게.
- **한계·주의**: 정확한 Lorenz APE는 전역 정렬 필요(계산비용 큼); QG 근사는 약한 성층변동 가정. 국지 APE 정의는 비유일(여러 정식화 존재).
- **출처**: Lorenz (1955), *Tellus* 7, 157–167, "Available potential energy and the maintenance of the general circulation"; Winters et al. (1995), *J. Fluid Mech.* 289, 115–128(정확 APE·혼합); "Energetically consistent localised APE budgets ...", arXiv:2502.01686 (2025).

---

### 로렌츠 에너지 사이클 (로렌츠 에너지 사이클 / Lorenz Energy Cycle, LEC)
- **무엇을 측정/검증하나**: MKE·MAPE(평균 APE)·EKE·EAPE(에디 APE) 4개 저장고와 그 사이 변환율(baroclinic/barotropic conversion, 풍입력, 소산)을 진단해 모델 에너지 순환의 물리적 일관성을 평가.
- **정의·수식**: 4-box: 풍 → MKE, MKE↔MAPE, MAPE→EAPE→EKE(baroclinic 경로), MKE→EKE(barotropic 경로), EKE→소산. baroclinic 변환 ∝ −(g/ρ₀)⟨w'ρ'⟩; barotropic 변환 ∝ −⟨u'u'⟩∂⟨u⟩/∂x 등 Reynolds 응력×평균전단.
- **적용 도메인/자료형**: 해류·밀도(격자 3D 시계열). 영역·전구.
- **입력·전제**: Reynolds 분해(평균/에디), w'·ρ' 상관, Reynolds 응력 텐서, 풍응력 일. 고빈도 출력 필요.
- **해석 기준**: baroclinic 경로(MKE→MAPE→EAPE→EKE)가 지배적, barotropic은 부차적이라는 정설과 정합. 변환 부호·크기가 관측 추정·고해상 시뮬레이션과 일치하면 양호. 참고: von Storch et al. (2012)는 전구 풍 에너지 생성 ~6.6 TW(시간평균풍 1.9 TW + 시변풍 2.2 TW 등) 규모를 보고.
- **한계·주의**: 평균/에디 분리법(시간 vs 공간 vs 스펙트럼)에 결과 민감. 항이 많아 닫힘이 까다로움. APE 기준상태 정의 의존.
- **출처**: Lorenz (1955); von Storch et al. (2012), *J. Phys. Oceanogr.* 42, 2185–2205, "An Estimate of the Lorenz Energy Cycle for the World Ocean Based on the STORM/NCEP Simulation"(DOI 10.1175/JPO-D-12-079.1); Koldunov et al. (2026), *J. Adv. Model. Earth Syst.* "Lorenz Energy Cycle of the Global Eddying Ocean ..."(DOI 10.1029/2025MS005551).

---

### 상대·행성·절대 와도 (와도 / Relative, Planetary & Absolute Vorticity)
- **무엇을 측정/검증하나**: 흐름의 회전(상대와도 ζ)·지구회전(행성와도 f)·합(절대와도 ζ+f). 순환 구조·전선·에디의 회전강도 진단.
- **정의·수식**: ζ = ∂v/∂x − ∂u/∂y (연직성분); f = 2Ω sinφ; 절대와도 = ζ+f. 무차원 Rossby 수 Ro = ζ/f.
- **적용 도메인/자료형**: 해류·바람(격자 u,v). 표층·등밀도면.
- **입력·전제**: 수평속도 격자, 정확한 유한차분(격자 metric 고려), 위도 φ.
- **해석 기준**: ζ 패턴이 에디·전선과 일치, Ro 크기가 mesoscale(Ro≪1)·submesoscale(Ro~O(1)) 체제와 정합. 위성 지형류 와도와 비교 가능.
- **한계·주의**: 미분연산이 노이즈·격자해상도에 민감(고차 미분일수록 악화). 경계·지형 근처 오차.
- **출처**: Vallis (2017); Pedlosky, *Geophysical Fluid Dynamics* (2nd ed., 1987).

---

### 포텐셜 와도 (포텐셜 와도 / Potential Vorticity, PV)
- **무엇을 측정/검증하나**: 단열·무마찰 흐름에서 보존되는 Ertel PV(또는 QG PV). 수괴 추적·역학적 보존성·안정도 진단의 핵심 불변량.
- **정의·수식**: Ertel PV q = (1/ρ)(ζ_a)·∇b, 여기서 ζ_a=절대와도 벡터, b=부력(또는 ∇σ). 대규모 근사 q ≈ (f+ζ)(−∂σ/∂z)/ρ. QG PV: q = ∇²ψ + f + ∂/∂z(f²/N² ∂ψ/∂z).
- **적용 도메인/자료형**: 해류·밀도(격자 3D). 등밀도면 PV가 수괴 진단에 유용.
- **입력·전제**: 3D 속도·밀도, 안정된 성층(N²>0), 등밀도면 보간.
- **해석 기준**: 흐름을 따라 PV가 보존(등밀도면에서 PV 등치선=흐름선 근사)되는지. PV 분포가 관측·기후값과 정합. 부호변화(f·q<0)는 불안정 신호.
- **한계·주의**: PV는 미분·곱으로 노이즈 증폭. 혼합·마찰영역에서 비보존. 등밀도면 정의·반전 민감.
- **출처**: Ertel (1942), *Meteorol. Z.* 59, 277–281; Hoskins et al. (1985), *Q. J. R. Meteorol. Soc.* 111, 877–946, "On the use and significance of isentropic potential vorticity maps"; Vallis (2017); Pedlosky (1987).

---

### 엔스트로피 (엔스트로피 / Enstrophy)
- **무엇을 측정/검증하나**: 와도의 제곱(분산). 2D/지형류 난류에서 하향(forward) 캐스케이드하는 보존량. 와도장 활동도·소산 진단.
- **정의·수식**: 엔스트로피 Z = ½ζ² (혹은 ½∫ζ² dA). 포텐셜 엔스트로피 = ½q². 2D 난류에서 에너지는 상향, 엔스트로피는 하향 캐스케이드.
- **적용 도메인/자료형**: 해류·해수면(격자 와도장). 스펙트럼 진단과 결합.
- **입력·전제**: 와도장(미분), 충분한 공간해상도. 스펙트럼 계산 시 균일격자·창함수.
- **해석 기준**: 엔스트로피 스펙트럼·플럭스가 QG 난류 예측(에너지 k⁻⁵ᐟ³ 상향, 엔스트로피 k⁻³ 하향)과 정합. 위성 알티미터 엔스트로피 플럭스와 비교(Khatri et al. 2018은 ~200–100 km에서 엔스트로피 캐스케이드 영역·k⁻³ 스펙트럼 확인).
- **한계·주의**: 고차 미분량이라 해상도·노이즈에 매우 민감. 소산영역(격자스케일) 표현이 모델 점성에 의존.
- **출처**: Kraichnan (1967), *Phys. Fluids* 10, 1417–1423, "Inertial ranges in two-dimensional turbulence"; Khatri et al. (2018), *J. Geophys. Res. Oceans* 123, 3875–3892, "Surface Ocean Enstrophy, Kinetic Energy Fluxes, and Spectra From Satellite Altimetry"(DOI 10.1029/2017JC013516).

---

### 발산 (발산 / Horizontal Divergence)
- **무엇을 측정/검증하나**: 수평속도장의 발산. 수렴·발산대(용승/침강), 비발산성(지형류 근사) 점검, 수직속도 진단의 기초.
- **정의·수식**: δ = ∂u/∂x + ∂v/∂y. 연속식으로 w = −∫δ dz. 지형류는 δ_g ≈ 0(β항 제외).
- **적용 도메인/자료형**: 해류·바람(격자 u,v).
- **입력·전제**: 수평속도 격자, 정확한 미분, 경계처리.
- **해석 기준**: 지형류 영역에서 |δ| ≪ |ζ|이면 균형 양호. 발산 패턴이 Ekman 펌핑·용승역과 일치.
- **한계·주의**: 미분 노이즈; 발산은 보통 와도보다 작아 상대오차 큼. ageostrophic 성분 추출에 민감.
- **출처**: Vallis (2017); Gill, *Atmosphere–Ocean Dynamics* (1982).

---

### 체적 수송 (체적 수송 / Volume Transport)
- **무엇을 측정/검증하나**: 단면을 가로지르는 체적유량(Sverdrup). 해협·경계류·전구 단면 수송이 관측·재분석과 정합하는지.
- **정의·수식**: T = ∬ u·n dA [m³/s], 1 Sv = 10⁶ m³/s. 단면을 따라 법선속도×면적 적분.
- **적용 도메인/자료형**: 해류(격자 u,v, 단면 좌표·격자 metric).
- **입력·전제**: 단면 정의(격자선 따라 또는 보간), 셀 면적·법선방향, 시간평균 vs 순간.
- **해석 기준**: 표준 단면 수송을 관측과 비교 — 예: ACC Drake Passage 전수심 총수송 173.3 ± 10.7 Sv(cDrake, Donohue et al. 2016), Florida Strait ~32 Sv(케이블), Indonesian Throughflow ~15 Sv(INSTANT). 관측 불확실도 범위 내면 양호. (구 canonical Drake값 ~134 Sv보다 cDrake가 ~30% 큼에 유의.)
- **한계·주의**: 단면이 격자선과 어긋나면 보간오차·이중계산. 순수송 vs 총수송 구분. 시간평균이 변동 수송을 평활.
- **출처**: Talley et al. (2011), *Descriptive Physical Oceanography*, 6th ed.; Donohue et al. (2016), *GRL* 43, "Mean Antarctic Circumpolar Current transport measured in Drake Passage"(cDrake, DOI 10.1002/2016GL070319); WOCE/CLIVAR 단면.

---

### 열 수송 & 자오면 열수송 (열 수송 / Heat Transport & MHT)
- **무엇을 측정/검증하나**: 단면을 가로지르는 열유량과 위도별 자오면 열수송(meridional heat transport, MHT). 모델 열재분배가 관측(RAPID·간접추정)과 정합하는지.
- **정의·수식**: Q_H = ρ₀cₚ ∬ u·n (θ−θ_ref) dA [W]. 닫힌 단면이면 θ_ref 무관. MHT(y) = ρ₀cₚ ∬ v θ dx dz.
- **적용 도메인/자료형**: 수온·해류(격자 θ,u, 단면).
- **입력·전제**: 닫힌(순체적수송≈0) 단면 권장(아니면 θ_ref 의존), 온라인 vθ 또는 고빈도 스냅샷.
- **해석 기준**: 26.5°N Atlantic MHT ~1.2~1.3 PW(RAPID/MOCHA; Hall & Bryden 1982의 1.3 ± 0.3 PW와 정합)와 비교. 전구 MHT 피크가 위도별 관측추정(Trenberth & Caron 2001) 범위 내면 양호. Atlantic에서 약 90% MHT가 자오면 순환(overturning)으로 운반.
- **한계·주의**: 순체적수송≠0이면 θ_ref가 절대값을 좌우. 시간평균 vθ는 에디 열수송 누락(online 필요). gyre vs overturning 분해 시 좌표 의존.
- **출처**: Hall & Bryden (1982), *Deep-Sea Res.* 29, 339–359; Trenberth & Caron (2001), *J. Climate* 14, 3433–3443; Buckley & Marshall (2016); RAPID/MOCHA 26.5°N(Frontiers Mar. Sci. 2019).

---

### 자오면 열수송 분해 (열수송 분해 / MHT Overturning–Gyre Decomposition)
- **무엇을 측정/검증하나**: 자오면 열수송을 (1) 자오면 전복(overturning) 성분과 (2) 수평 환류(gyre) 성분으로 분해해, 모델이 *어떤 순환 모드*로 열을 운반하는지가 관측과 맞는지 점검. RMSE만 봐서는 안 보이는 기작 수준 검증.
- **정의·수식**: Hall–Bryden 분해. MHT = ρ₀cₚ[ ∫⟨v⟩_zonal ⟨θ⟩_zonal dz (overturning) + ∫ v*θ* dx dz (gyre, *=동서편차) + 에디항 ]. 추가로 Ekman·thermal-wind 분해(Lee & Marotzke 1998)도 가능.
- **적용 도메인/자료형**: 수온·해류(격자 θ,v; 위도단면 적분).
- **입력·전제**: 동서 적분 가능한 단면, 순체적수송≈0(닫힘), 일관된 zonal-mean 정의.
- **해석 기준**: Atlantic에서 overturning 성분이 지배(≈90%)하고 gyre는 부차적이라는 정설과 정합. 모델이 gyre로 과도하게 열을 옮기면 AMOC 약화·전선 위치 오류 의심.
- **한계·주의**: 분해는 좌표(z vs 밀도)·zonal-mean 정의에 의존하며 성분을 깔끔히 인과 귀속할 수 없음(모든 순환이 수평·수직 성분을 함께 가짐). θ_ref·순수송 처리 민감.
- **출처**: Hall & Bryden (1982), *Deep-Sea Res.* 29, 339–359(overturning/gyre 분해 원전); Lee & Marotzke (1998), *J. Phys. Oceanogr.* 28, Ekman/geostrophic 분해; Buckley & Marshall (2016) 리뷰.

---

### 염·담수 수송 (염/담수 수송 / Salt & Freshwater Transport)
- **무엇을 측정/검증하나**: 단면 염·담수 유량. 담수수지·해양 염분 재분배 진단. 가상/실 플럭스 일관성. AMOC 담수수송 지표(Mov/Fov)로 안정도 진단.
- **정의·수식**: 염수송 F_S = ρ₀ ∬ u·n S dA. 담수수송 F_FW = −(1/S_ref) ∬ u·n (S−S_ref) dA (S_ref=기준염분). AMOC 담수수송 지표 Mov(또는 Fov) = AMOC 자오면 순환이 운반하는 담수수송(34.5°S에서 baroclinic zonal-mean v로 산출).
- **적용 도메인/자료형**: 염분·해류(격자 S,u, 단면).
- **입력·전제**: 닫힌 단면, S_ref 정의(보통 단면평균 또는 34.7~35), 순체적수송 처리.
- **해석 기준**: 표준 단면 담수수송을 관측·재분석과 비교. **Mov 부호가 음(<0)이면 AMOC가 다중안정(bistable) 체제 가능성** — 대다수 관측·재분석은 34.5°S에서 Mov<0을 시사하나 다수 모델은 부호 오류(양)를 보임 → 모델 담수수송 편향 진단의 표준 지표.
- **한계·주의**: S_ref·순수송 처리에 절대값이 크게 의존. 가상염플럭스 모델은 담수수지 비보존 가능.
- **출처**: Talley et al. (2011); de Vries & Weber (2005), *GRL* 32, "The Atlantic freshwater budget as a diagnostic for the existence of a stable shut down of the meridional overturning circulation"(Mov/Fov 지표 원전, DOI 10.1029/2004GL021450); Weijer et al. (2019), *JGR-Oceans* AMOC 안정도 리뷰(DOI 10.1029/2019JC015083).

---

### 자오면 전복순환 함수 (자오면 전복순환 / Meridional Overturning Streamfunction, MOC/AMOC)
- **무엇을 측정/검증하나**: 위도-깊이(또는 위도-밀도) 평면의 전복순환 강도·구조. AMOC 등 대규모 자오면 순환이 관측배열(RAPID 26.5°N)과 정합하는지.
- **정의·수식**: Ψ(y,z) = ∬_{−H}^{z} (∫ v dx) dz' [Sv]. 잔차순환(residual MOC) = Eulerian + eddy-induced(bolus) streamfunction. 밀도좌표 Ψ(y,σ)는 수괴변환과 연결.
- **적용 도메인/자료형**: 해류(격자 v, 깊이 또는 밀도좌표).
- **입력·전제**: 자오면 적분용 v, 닫힌 동-서 적분, eddy parameterization(GM) 사용 시 bolus 속도 포함.
- **해석 기준**: AMOC 26.5°N ~17 Sv(RAPID 평균)와 비교; 시간변동성도 RAPID와 정합하면 양호. Atlantic에서 약 90% MHT가 overturning이 담당.
- **한계·주의**: z-좌표 Ψ는 등밀도 수송을 왜곡할 수 있음 → 밀도좌표 MOC 권장. 에디 bolus 누락 시 잔차순환 과대.
- **출처**: RAPID 26.5°N(Frontiers Mar. Sci. 2019; *Phil. Trans. R. Soc. A* 2023 "From theory to RAPID AMOC observations"); Buckley & Marshall (2016); Petit et al. (2025), *JGR-Oceans* "Evaluation of a Reduced RAPID Array"(DOI 10.1029/2025JC023093).

---

### 순압(수심적분) 유선함수 (순압 유선함수 / Barotropic / Depth-Integrated Streamfunction)
- **무엇을 측정/검증하나**: 수심적분 수평순환(gyre, ACC, 경계류 수송)의 강도·구조를 단일 2D 장으로 요약. 모델 풍성순환이 관측·재분석과 정합하는지의 1차 진단.
- **정의·수식**: 수심적분 수송 U = ∫_{−H}^{0} u dz, V = ∫_{−H}^{0} v dz. 비발산 가정으로 유선함수 Ψ_bt: U = −∂Ψ_bt/∂y, V = ∂Ψ_bt/∂x [Sv]. 등치선 간격이 gyre 수송.
- **적용 도메인/자료형**: 해류(격자 u,v; 전수심).
- **입력·전제**: 전수심 속도(또는 수심적분 수송), 닫힌 경계에서 Ψ 적분 상수 고정, 섬 처리(island rule).
- **해석 기준**: 아열대·아한대 gyre 수송, ACC 수송(Ψ 동-서 차 ≈ Drake Passage 수송 ~173 Sv)이 관측·GLORYS와 일치하면 양호. Sverdrup 균형 예측과도 비교(아래 카드).
- **한계·주의**: 순압 유선함수는 baroclinic·전복 성분을 담지 못함(MOC와 상보적). 섬·복잡지형에서 적분경로 의존.
- **출처**: Vallis (2017); Talley et al. (2011); Griffies (2004). 진단 정의는 OMIP 프로토콜(Griffies et al. 2016, *GMD* 9, 3231–3296)에 표준화.

---

### Sverdrup 균형 (스베드럽 균형 / Sverdrup Balance)
- **무엇을 측정/검증하나**: 풍응력 curl이 강제하는 내부 자오면 수송(Sverdrup transport)이 모델·관측 gyre 내부 순환과 정합하는지. 풍성순환 이론과 모델의 일관성 검증.
- **정의·수식**: βV = (1/ρ₀) curl(τ) = (1/ρ₀)(∂τ_y/∂x − ∂τ_x/∂y). 수심적분 자오수송 V_Sv = curl(τ)/(ρ₀β). 동쪽경계에서 서쪽으로 적분해 Sverdrup 유선함수 산출.
- **적용 도메인/자료형**: 풍응력·해류(격자 τ, f, β). 내부(서안경계류 제외) 영역.
- **입력·전제**: 표면 풍응력 τ(모델 강제 또는 ERA5), β=df/dy, 동쪽경계 기준. 내부영역(서안경계류·적도 제외)에서만 유효.
- **해석 기준**: Sverdrup 수송이 모델 순압 유선함수의 내부값과 근사 일치하면 풍성순환이 선형이론과 정합. 큰 차이는 비선형·지형·에디 정류(eddy rectification) 기여를 시사.
- **한계·주의**: 정상·선형·내부영역 가정. 서안경계류·적도·강한 지형에서 붕괴. 풍응력 산물(ERA5 vs 모델 내부 τ) 차이가 결과를 좌우.
- **출처**: Vallis (2017); Gill (1982); Talley et al. (2011) Sverdrup·풍성순환 장.

---

### 수괴 변환 (수괴 변환 / Water-Mass Transformation, WMT)
- **무엇을 측정/검증하나**: 표면 부력플럭스(열·담수)와 내부 혼합이 밀도층(수괴) 사이 체적을 어떻게 변환하는지. 보존적 밀도좌표 수지로 전복순환·심층수 형성률 진단.
- **정의·수식**: Walin 프레임워크. 변환율 F(σ) = (∂/∂σ) ∬ (표면 밀도플럭스) dA — 표면밀도플럭스를 밀도등급으로 binning. 형성률(formation) = −∂F/∂σ.
- **적용 도메인/자료형**: 수온·염분·표면플럭스(격자). 밀도좌표.
- **입력·전제**: 표면 열·담수플럭스, 표면밀도, 상태방정식, 밀도 bin. 온라인 binning이 정확.
- **해석 기준**: 변환/형성률이 관측 추정 수괴(예: SAMW, AABW, NADW 형성률)와 정합. 밀도좌표 수지가 닫히면(MOM6 online) 양호. WMT로 추정한 σ-공간 MOC와 직접 계산한 밀도좌표 MOC가 일치하면 자기일관.
- **한계·주의**: 오프라인 시간평균은 binning 오차 큼. 혼합 기여 분리 어려움. 상태방정식·기준밀도 민감.
- **출처**: Walin (1982), *Tellus* 34, 187–195, "On the relation between sea-surface heat flow and thermal circulation in the ocean"(DOI 10.1111/j.2153-3490.1982.tb01806.x); Speer & Tziperman (1992), *J. Phys. Oceanogr.* 22, 93–104; MOM6 Analysis Cookbook "Watermass transformation".

---

### 지형류 균형 & 열풍 (지형류·열풍 / Geostrophic Balance & Thermal Wind)
- **무엇을 측정/검증하나**: 대규모 흐름이 지형류 균형(코리올리=압력경도)을 만족하는지, 그리고 연직 유속전단이 수평 밀도경도(열풍)와 정합하는지. 역학적 일관성·진단속도 검증.
- **정의·수식**: 지형류 f u_g = −(1/ρ₀)∂p/∂y, f v_g = (1/ρ₀)∂p/∂x. 열풍 ∂u_g/∂z = (g/(ρ₀f))∂ρ/∂y, ∂v_g/∂z = −(g/(ρ₀f))∂ρ/∂x. 역학고도 D = ∫δ dp로 지형류 산출.
- **적용 도메인/자료형**: 해류·해수면·밀도(격자 또는 단면 hydrography).
- **입력·전제**: 압력/SSH 또는 밀도장, f≠0(적도 제외), 기준면(level of no motion) 또는 절대속도 기준.
- **해석 기준**: 모델 u와 지형류 u_g가 대규모에서 일치(잔차=ageostrophic). 열풍전단이 관측 밀도경도와 정합. SSH로부터 지형류 KE/EKE 위성비교.
- **한계·주의**: 적도·강한 곡률·submesoscale에서 균형 붕괴. 기준면 선택이 절대속도에 영향. 미분 노이즈.
- **출처**: Vallis (2017); Gill (1982); Talley et al. (2011); "The exact geostrophic streamfunction for neutral surfaces", arXiv:1903.10095.

---

### 동적 해수면·스테릭 높이 (동적/스테릭 해수면 / Dynamic & Steric Sea Level)
- **무엇을 측정/검증하나**: 모델 해수면 높이(SSH)를 위성 알티미터(AVISO/CMEMS), 평균동적지형(MDT), tide-gauge와 비교. SSH를 동적(manometric/순압)·스테릭(열·염팽창) 성분으로 분해해 어떤 과정이 편향을 만드는지 진단.
- **정의·수식**: 스테릭 높이 η_steric = −(1/ρ₀)∫_{−H}^{0}(ρ−ρ₀) dz; 열스테릭은 θ변화, 염스테릭은 S변화 기여. 전 SSH = manometric(질량) + steric. 평균 SSH(MDT)와 변동(SLA)로 분리해 비교.
- **적용 도메인/자료형**: 해수면·수온·염분(격자 η, 3D θ,S). 위성 알티미터 SLA·MDT.
- **입력·전제**: SSH 또는 3D ρ, 기준 geoid/MDT, 역기압 보정·tide 제거 정합. Boussinesq 모델은 전구 평균 스테릭 보정(global steric adjustment) 필요.
- **해석 기준**: 모델 SLA 변동성·공간패턴이 알티미터와 정합(상관·RMSE), 시간평균 MDT가 관측 MDT(CNES-CLS 등)와 일치하면 양호. 지형류 KE/EKE도 SSH에서 동일 필터로 위성과 직접 비교.
- **한계·주의**: Boussinesq 모델은 전구 질량변화·스테릭을 직접 담지 못해 후처리 보정 필요. 알티미터 평균면(geoid) 불확실. 연안·천해 알티미터 품질저하.
- **출처**: Griffies et al. (2016), *GMD* 9, 3231–3296(OMIP SSH·steric 진단 정의); Gregory et al. (2019), *Surv. Geophys.* "Concepts and terminology for sea level"(용어·분해 표준); CMEMS/AVISO 알티미터 산물 문서.

---

### 혼합층 깊이·부력플럭스 (혼합층·부력 / Mixed-Layer Depth & Surface Buoyancy Flux)
- **무엇을 측정/검증하나**: 표층 혼합층 깊이(MLD)와 표면 부력플럭스(열+담수 환산)를 진단해 표층 강제·대류·재성층화가 관측(Argo MLD 기후값)과 정합하는지. WMT·심층수 형성의 표면 경계조건 검증.
- **정의·수식**: 부력 b = −g(ρ−ρ₀)/ρ₀. 표면 부력플럭스 B₀ = (g/ρ₀)[α Q_net/cₚ − ρ₀ β S (E−P−R)] (α=열팽창, β=염수축). MLD: 밀도/온도 기준(예: Δσ_θ=0.03 kg/m³ 또는 ΔT=0.2°C from 10 m).
- **적용 도메인/자료형**: 수온·염분·표면플럭스(격자 θ,S,Q,FW).
- **입력·전제**: 표면 순열·담수플럭스, 상태방정식(α,β), 일관된 MLD 정의(임계값 명시).
- **해석 기준**: MLD 계절순환·공간패턴이 Argo 기후값(예: de Boyer Montégut 2004)과 정합. 겨울 깊은 대류역(Labrador·Weddell)에서 과대/과소면 심층수 형성 편향 의심. B₀<0(부력 손실)이 대류역과 일치.
- **한계·주의**: MLD는 정의(임계값·기준심)에 민감 → 관측과 동일 정의로 산출해야 비교 유효. 일변화·해빙역 처리 주의.
- **출처**: de Boyer Montégut et al. (2004), *JGR-Oceans* 109, "Mixed layer depth over the global ocean ..."(Argo MLD 기후값); Gill (1982) 부력플럭스; Griffies et al. (2016) OMIP MLD 진단.

---

### 베르누이 함수 (베르누이 함수 / Bernoulli Function)
- **무엇을 측정/검증하나**: 정상·단열·무마찰 흐름선을 따라 보존되는 베르누이 함수. 정상류 보존성·흐름선 구조 진단.
- **정의·수식**: B = p/ρ + ½|u|² + gz (또는 성층 해양형 B = ½|u|² + Montgomery potential). 정상류에서 u·∇B = 0 (흐름선 따라 일정).
- **적용 도메인/자료형**: 해류·밀도(격자 3D). 등밀도면 Montgomery 함수와 결합.
- **입력·전제**: 정상상태 근사, 속도·압력(또는 Montgomery 포텐셜), 단열·무마찰 가정.
- **해석 기준**: 흐름선(또는 등밀도면 PV 등치선)을 따라 B 변화가 작으면 정상·보존 근사 양호. 큰 변화 = 비정상·혼합·마찰.
- **한계·주의**: 시간변동·혼합 강한 영역에서 비보존. 등밀도면 정의·Montgomery 포텐셜 계산 민감.
- **출처**: Vallis (2017); Pedlosky (1987); Gill (1982).

---

### Ekman 수송·펌핑 (에크만 수송/펌핑 / Ekman Transport & Pumping)
- **무엇을 측정/검증하나**: 풍응력에 의한 표층 Ekman 수송과 그 회전(curl)에 의한 연직속도(Ekman pumping). 풍성순환 강제·용승역 진단.
- **정의·수식**: Ekman 수송 M_E = (τ × k)/(ρ₀f) [m²/s]. Ekman pumping w_E = curl(τ/(ρ₀f)) = ∇×(τ/(ρ₀f))·k. Sverdrup 균형 βV = curl(τ)/ρ₀.
- **적용 도메인/자료형**: 풍응력·해류(격자 τ, f). 표층·수송.
- **입력·전제**: 표면 풍응력 τ(모델 강제 또는 ERA5), f(φ), curl 계산.
- **해석 기준**: w_E 패턴이 용승역(적도·동안경계·남극)과 일치. Sverdrup 수송이 관측 gyre 수송과 정합. ERA5 풍응력 강제 일관성 점검.
- **한계·주의**: 적도(f→0) 특이점. 비선형·시간변동 무시. 풍응력 산물 간 차이가 큼.
- **출처**: Gill (1982); Vallis (2017); Talley et al. (2011) Ekman·Sverdrup 장.

---

### KE 파수 스펙트럼 (운동에너지 파수 스펙트럼 / KE Wavenumber Spectra)
- **무엇을 측정/검증하나**: 운동에너지(또는 SSH)의 수평파수별 분포·기울기. mesoscale/submesoscale 난류 체제(QG vs SQG)와 모델 유효해상도 진단.
- **정의·수식**: E(k) = KE의 파수 k 스펙트럼 밀도. QG 예측: 에너지 관성영역 E(k)∝k⁻⁵ᐟ³(상향), 엔스트로피 영역 E(k)∝k⁻³(하향). SSH 스펙트럼 기울기 관측 ~ −11/3 ~ −5.
- **적용 도메인/자료형**: 해류·해수면(격자 u,v 또는 η; 균일격자 구간).
- **입력·전제**: 균일·정사각 격자 구간, 창함수(Hanning)·detrend, 등방화(원형 평균) 또는 1D 트랜섹트.
- **해석 기준**: 스펙트럼 기울기·전이파수를 위성 알티미터·관측과 비교. 모델이 −3(엔스트로피) 또는 더 가파른 기울기를 보이면 mesoscale 분해; 유효해상도(roll-off) 파수 확인(명목 해상도보다 거친 경우가 일반적).
- **한계·주의**: 비균일 격자·해안경계에서 스펙트럼 왜곡. 모델 수치점성이 고파수 인위적 감쇠(유효해상도 < 명목해상도). 알티미터 노이즈 floor·궤도 간격.
- **출처**: Kraichnan (1967); Charney (1971), *J. Atmos. Sci.* 28, 1087–1095, "Geostrophic turbulence"; Stammer (1997, *JPO*) 위성 SSH 스펙트럼; Khatri et al. (2018, JGR-Oceans).

---

### 스펙트럼 에너지·엔스트로피 플럭스(캐스케이드) (스펙트럼 플럭스 / Spectral Energy & Enstrophy Flux)
- **무엇을 측정/검증하나**: 파수공간에서 비선형 항이 운반하는 KE·엔스트로피 플럭스(Π(k))의 부호·크기로 상향(inverse)·하향(forward) 캐스케이드를 진단. 에디 에너지 경로 검증.
- **정의·수식**: 스펙트럼 KE 플럭스 Π(k) = −∫_k^∞ T(k') dk', T(k)=비선형 전달함수(û·(u·∇u)의 스펙트럼). Π<0=상향(역)캐스케이드, Π>0=하향.
- **적용 도메인/자료형**: 해류·해수면(격자 u,v 시계열; 알티미터 지형류).
- **입력·전제**: 균일격자·정상성, 비선형항 스펙트럼 계산(또는 coarse-graining 필터법). 충분한 표본.
- **해석 기준**: surface mesoscale에서 KE는 상향(>~200–250 km), 엔스트로피는 하향(~200–100 km, QG 정설)과 정합. Scott & Wang (2005)·Khatri et al. (2018) 위성진단과 비교. 변환 효율·전이스케일 점검.
- **한계·주의**: 스펙트럼 플럭스 계산은 표본·창·격자에 민감. coarse-graining법과 스펙트럼법 결과 차이. 비균일격자 곤란.
- **출처**: Scott & Wang (2005), *J. Phys. Oceanogr.* 35, 1650–1666, "Direct evidence of an oceanic inverse kinetic energy cascade from satellite altimetry"(DOI 10.1175/JPO2771.1); Khatri et al. (2018, JGR-Oceans); ECMWF, "Energy and Enstrophy Cascades in Numerical Models"(기술노트).

---

### Coarse-graining 스케일 에너지 플럭스 (coarse-graining 플럭스 / Coarse-Graining Scale-Space Energy Flux)
- **무엇을 측정/검증하나**: 공간 필터(저역통과)를 폭 ℓ로 적용해 *위치별·스케일별* KE 변환율(상향/하향 캐스케이드)을 지도화. 스펙트럼법과 달리 통계적 균질성을 가정하지 않아 비균일·국지 영역(경계류·전선)에 적용 가능.
- **정의·수식**: 필터장 ū_ℓ = G_ℓ * u. 스케일 ℓ에서 sub-filter 응력 τ_ℓ(u,u) = (uu)‾_ℓ − ū_ℓ ū_ℓ. 스케일간 에너지 전달(에너지 플럭스 밀도) Π_ℓ = −ρ₀ τ_ℓ : ∇ū_ℓ. Π_ℓ<0=상향, >0=하향.
- **적용 도메인/자료형**: 해류·해수면(격자 u,v; 알티미터 지형류). 균일격자 권장(필터 적용).
- **입력·전제**: 격자 속도장, 필터 커널(Gaussian/top-hat), 다중 ℓ 스윕. 경계 근처 필터 처리.
- **해석 기준**: 국지 Π_ℓ 지도가 관측·고해상 시뮬레이션의 캐스케이드 패턴(예: 걸프스트림·ACC 상향전달 핫스팟)과 일치하면 양호. 스펙트럼 Π(k)와 부호·전이스케일이 정합.
- **한계·주의**: 필터폭·커널 선택 의존, 압축성·경계 처리 주의. 스펙트럼법과 정의가 달라 절대값 직접비교는 신중.
- **출처**: Aluie, Hecht & Vallis (2018), *J. Phys. Oceanogr.* 48, 225–244, "Mapping the Energy Cascade in the North Atlantic Ocean: The Coarse-Graining Approach"(DOI 10.1175/JPO-D-17-0100.1).

---

### 밀도층(등밀도) 좌표 수지 (등밀도 좌표 수지 / Isopycnal-Coordinate Budgets)
- **무엇을 측정/검증하나**: 밀도(또는 중립밀도) 좌표에서 층별 체적·열·염 수지의 닫힘. 등밀도 수송·수괴변환을 z-좌표 인위혼합 없이 진단.
- **정의·수식**: 층 두께 h=−∂z/∂σ. 층 체적수지 ∂h/∂t + ∇·(uh) = (diapycnal 변환). 밀도좌표에서 열·염 수지는 등밀도 이류+diapycnal 혼합으로 분해.
- **적용 도메인/자료형**: 수온·염분·해류(격자; z→σ 보간 또는 native isopycnal 모델).
- **입력·전제**: 정확한 밀도 binning(온라인 권장), 상태방정식, 단조 성층. MOM6는 밀도그리드 온라인 출력 지원.
- **해석 기준**: 밀도좌표 수지 잔차가 작고, z-좌표 대비 spurious diapycnal mixing이 줄면 양호. WMT와 일관.
- **한계·주의**: 오프라인 z→σ 보간은 binning·시간평균 오차. 비단조 성층·약성층층 처리 곤란.
- **출처**: MOM6 Analysis Cookbook(밀도그리드 binning); Griffies (2004); Megann (2018) spurious mixing 진단.

---

### 실효(수치) diapycnal 혼합 진단 (실효 diapycnal 혼합 / Effective / Numerical Diapycnal Mixing)
- **무엇을 측정/검증하나**: 모델이 실제로 만들어내는 *유효* 등밀도횡단(diapycnal) 확산계수 κ_eff를 진단해, 명시적(설정한) 혼합 대비 *수치적 spurious mixing*이 얼마나 큰지 정량. 모델 성층·심층수 보존성의 핵심 결함 진단.
- **정의·수식**: 등밀도 수괴분석(Lee et al. 2002 방식). 밀도층 내 부피·기준상태 정렬에서 등밀도면을 가로지르는 유효확산 κ_eff = (등밀도면 횡단 부력플럭스)/(N²). κ_eff − κ_explicit = 수치혼합.
- **적용 도메인/자료형**: 수온·염분(밀도)(격자 3D 시계열).
- **입력·전제**: 시간에 따른 3D 밀도장(또는 밀도층 부피), 명시적 혼합계수 설정값, 상태방정식. 고빈도 출력일수록 정확.
- **해석 기준**: κ_eff가 내부영역 명시적 값(예: 1×10⁻⁵ m²/s)에 근접하면 우수. Megann (2018)은 eddy-permitting NEMO 내부에서 κ_eff가 명시값보다 최대 1자리 이상 큼(수치혼합 지배)을 보고 → 우리 모델도 동일 진단으로 비교. 큰 κ_eff = 과도 성층소멸·수괴 침식.
- **한계·주의**: 진단법(수괴분석 vs tracer-variance) 간 차이. 약성층·혼합층·해빙역 처리 곤란. 격자·이류기법(advection scheme)·해상도에 강하게 의존.
- **출처**: Megann (2018), *Ocean Modelling* 121, 19–33, "Estimating the numerical diapycnal mixing in an eddy-permitting ocean model"(DOI 10.1016/j.ocemod.2017.11.001); Lee, Nurser et al. (2002) 수괴분석 기법; Griffies (2004).

---

### 전지구 에너지·물수지 마감 (전구 에너지/물 수지 / Global Energy & Water Imbalance)
- **무엇을 측정/검증하나**: 전 지구·전 해양 적분 에너지(열)·물(담수)·질량 수지의 불균형(drift). 장기 보존성·모델 표류 진단. 권위 추정(지구 에너지 불균형)과 비교.
- **정의·수식**: 전구 에너지 불균형 = d(OHC)/dt − 표면 순플럭스 적분. 전구 담수: d(담수량)/dt − ∮(P−E+R) dA. 질량: d(해수질량)/dt − 담수입력.
- **적용 도메인/자료형**: 전구 적분(격자→체적/면적 적분 시계열).
- **입력·전제**: 전 영역 OHC·표면플럭스 시계열, 일관된 적분(셀 면적·체적 가중).
- **해석 기준**: 불균형·표류가 작아야(예: 모델 인위적 해양 열표류 ≪ 1 W/m²) 장기 보존 양호. 관측 추정 지구 에너지 불균형은 양(+)의 ~0.5–1 W/m² 규모(von Schuckmann et al. 2020; ~89%가 해양 흡수)이며, 모델 *물리적* 흡수와 *수치적* 표류를 구분해야 함.
- **한계·주의**: 가상염플럭스·비Boussinesq 보정·penetrative SW 등 누락이 인위표류 유발. spin-up 미완료 시 표류 큼.
- **출처**: von Schuckmann et al. (2020), *Earth Syst. Sci. Data* 12, 2013–2041, "Heat stored in the Earth system: where does the energy go?"(DOI 10.5194/essd-12-2013-2020); Griffies et al. (2016), *Geosci. Model Dev.* 9, 3231–3296(OMIP 진단 프로토콜, DOI 10.5194/gmd-9-3231-2016).

---

### 에너지·플럭스 장의 요약 통계·테일러 다이어그램 (요약 스킬 지표 / Summary Skill Metrics for Energetic Fields)
- **무엇을 측정/검증하나**: 위 역학·에너지 진단량(KE/EKE 지도, MOC, MHT 단면, 스펙트럼 기울기 등)을 권위자료와 **종합 점수**로 비교. 닫힘(보존) 검증을 통과한 장에 대해 패턴·진폭 일치를 한눈에 요약.
- **정의·수식**: 표준 검증지표 — 패턴상관 R, 중심화 RMSE(centered RMSD), 표준편차비 σ_model/σ_ref, 평균편차(bias). Taylor (2001) 다이어그램은 R·σ비·CRMSD를 한 평면에 표시(코사인 법칙으로 세 양이 기하적으로 연결). Murphy–Epstein skill score, Nash–Sutcliffe 효율 등도 병용.
- **적용 도메인/자료형**: 모든 격자·단면·시계열 진단량(우리 모델 vs ERA5/GLORYS/위성).
- **입력·전제**: 동일 격자·기간으로 보간·정렬된 모델·기준 쌍, 면적가중. 로그변환(스펙트럼·KE처럼 자릿수 큰 양)·이상치 처리 명시.
- **해석 기준**: Taylor 다이어그램에서 점이 기준점(R=1, σ비=1)에 가까울수록 우수. 여러 모델·실험을 한 다이어그램에 올려 상대순위. (절대 임계값보다 *상대비교·다자료 일관성*에 적합.)
- **한계·주의**: 요약 지표는 보존성 자체를 검증하지 못함 → 반드시 위 닫힘 카드와 함께 사용. 보간·면적가중 오류가 지표를 오염. 강한 비정규·자릿수 분포(KE·스펙트럼)는 변환 후 비교.
- **출처**: Taylor (2001), *J. Geophys. Res.* 106, 7183–7192, "Summarizing multiple aspects of model performance in a single diagram"(DOI 10.1029/2000JD900719); Jolliffe & Stephenson (eds.), *Forecast Verification* (2nd ed., 2012, Wiley); Wilks, *Statistical Methods in the Atmospheric Sciences* (4th ed., 2019).

---

## 출처 (References)

### 표준 교과서·표준 참고문헌 (실재 확인)
- Vallis, G. K. (2017). *Atmospheric and Oceanic Fluid Dynamics*, 2nd ed., Cambridge University Press. (에너지론·와도·지형류·스펙트럼 난류)
- Pedlosky, J. (1987). *Geophysical Fluid Dynamics*, 2nd ed., Springer. (PV·와도·QG)
- Gill, A. E. (1982). *Atmosphere–Ocean Dynamics*, Academic Press. (Ekman·지형류·Bernoulli·부력)
- Griffies, S. M. (2004). *Fundamentals of Ocean Climate Models*, Princeton University Press. (보존방정식·수지·밀도좌표)
- Talley, L. D., Pickard, G. L., Emery, W. J., Swift, J. H. (2011). *Descriptive Physical Oceanography*, 6th ed., Academic Press. (수송·MOC·열수송·Sverdrup)
- Wilks, D. S. (2019). *Statistical Methods in the Atmospheric Sciences*, 4th ed., Elsevier. (검증지표)
- Jolliffe, I. T., Stephenson, D. B. (eds.) (2012). *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, 2nd ed., Wiley. (검증 프레임워크)

### 학술 논문·원전 (서지 확인 완료 — 웹 검증)
- Lorenz, E. N. (1955). "Available potential energy and the maintenance of the general circulation." *Tellus*, 7, 157–167. (APE·LEC 원전)
- Kraichnan, R. H. (1967). "Inertial ranges in two-dimensional turbulence." *Physics of Fluids*, 10, 1417–1423. (2D 캐스케이드)
- Charney, J. G. (1971). "Geostrophic turbulence." *J. Atmos. Sci.*, 28, 1087–1095.
- Walin, G. (1982). "On the relation between sea-surface heat flow and thermal circulation in the ocean." *Tellus*, 34, 187–195. DOI 10.1111/j.2153-3490.1982.tb01806.x. (WMT)
- Hall, M. M., Bryden, H. L. (1982). "Direct estimates and mechanisms of ocean heat transport." *Deep-Sea Research A*, 29, 339–359. (MHT overturning/gyre 분해)
- Hoskins, B. J., McIntyre, M. E., Robertson, A. W. (1985). "On the use and significance of isentropic potential vorticity maps." *Q. J. R. Meteorol. Soc.*, 111, 877–946.
- Speer, K., Tziperman, E. (1992). "Rates of water mass formation in the North Atlantic Ocean." *J. Phys. Oceanogr.*, 22, 93–104. (WMT 형성률)
- Winters, K. B., Lombard, P. N., Riley, J. J., D'Asaro, E. A. (1995). "Available potential energy and mixing in density-stratified fluids." *J. Fluid Mech.*, 289, 115–128. (정확 APE)
- Stammer, D. (1997). "Global characteristics of ocean variability estimated from regional TOPEX/POSEIDON altimeter measurements." *J. Phys. Oceanogr.*, 27, 1743–1769. (위성 EKE·변동성 기준)
- Lee, T., Marotzke, J. (1998). "Seasonal cycles of meridional overturning and heat transport of the Indian Ocean." *J. Phys. Oceanogr.*, 28, 923–943. (MHT 분해; Ekman/geostrophic)
- Haney, R. L. (1991). "On the pressure gradient force over steep topography in sigma coordinate ocean models." *J. Phys. Oceanogr.*, 21, 610–619.
- Taylor, K. E. (2001). "Summarizing multiple aspects of model performance in a single diagram." *J. Geophys. Res.*, 106(D7), 7183–7192. DOI 10.1029/2000JD900719. (Taylor 다이어그램)
- Trenberth, K. E., Caron, J. M. (2001). "Estimates of meridional atmosphere and ocean heat transports." *J. Climate*, 14, 3433–3443. (전구 MHT)
- de Boyer Montégut, C., et al. (2004). "Mixed layer depth over the global ocean: An examination of profile data and a profile-based climatology." *J. Geophys. Res. Oceans*, 109, C12003. (Argo MLD 기후값)
- de Vries, P., Weber, S. L. (2005). "The Atlantic freshwater budget as a diagnostic for the existence of a stable shut down of the meridional overturning circulation." *Geophys. Res. Lett.*, 32, L09606. DOI 10.1029/2004GL021450. (Mov/Fov 안정도 지표)
- Scott, R. B., Wang, F. (2005). "Direct evidence of an oceanic inverse kinetic energy cascade from satellite altimetry." *J. Phys. Oceanogr.*, 35, 1650–1666. DOI 10.1175/JPO2771.1.
- von Storch, J.-S., Eden, C., Fast, I., Haak, H., Hernández-Deckers, D., Maier-Reimer, E., Marotzke, J., Stammer, D. (2012). "An estimate of the Lorenz energy cycle for the World Ocean based on the STORM/NCEP simulation." *J. Phys. Oceanogr.*, 42, 2185–2205. DOI 10.1175/JPO-D-12-079.1.
- Buckley, M. W., Marshall, J. (2016). "Observations, inferences, and mechanisms of the Atlantic Meridional Overturning Circulation: A review." *Rev. Geophys.*, 54, 5–63. DOI 10.1002/2015RG000493. (열수지·AMOC 리뷰)
- Donohue, K. A., Tracey, K. L., Watts, D. R., Chidichimo, M. P., Chereskin, T. K. (2016). "Mean Antarctic Circumpolar Current transport measured in Drake Passage." *Geophys. Res. Lett.*, 43, 11760–11767. DOI 10.1002/2016GL070319. (cDrake 173.3 Sv)
- Griffies, S. M., et al. (2016). "OMIP contribution to CMIP6: experimental and diagnostic protocol for the physical component of the Ocean Model Intercomparison Project." *Geosci. Model Dev.*, 9, 3231–3296. DOI 10.5194/gmd-9-3231-2016. (OMIP 진단 프로토콜)
- Megann, A. (2018). "Estimating the numerical diapycnal mixing in an eddy-permitting ocean model." *Ocean Modelling*, 121, 19–33. DOI 10.1016/j.ocemod.2017.11.001. (spurious/numerical diapycnal mixing)
- Aluie, H., Hecht, M., Vallis, G. K. (2018). "Mapping the energy cascade in the North Atlantic Ocean: The coarse-graining approach." *J. Phys. Oceanogr.*, 48, 225–244. DOI 10.1175/JPO-D-17-0100.1.
- Khatri, H., Sukhatme, J., Kumar, A., Verma, M. K. (2018). "Surface ocean enstrophy, kinetic energy fluxes, and spectra from satellite altimetry." *J. Geophys. Res. Oceans*, 123, 3875–3892. DOI 10.1029/2017JC013516.
- Weijer, W., Cheng, W., Drijfhout, S. S., et al. (2019). "Stability of the Atlantic Meridional Overturning Circulation: A review and synthesis." *J. Geophys. Res. Oceans*, 124, 5336–5375. DOI 10.1029/2019JC015083. (AMOC 안정도·Mov)
- Gregory, J. M., et al. (2019). "Concepts and terminology for sea level: mean, variability and change, both local and global." *Surv. Geophys.*, 40, 1251–1289. (해수면 성분·용어 표준)
- von Schuckmann, K., et al. (2020). "Heat stored in the Earth system: where does the energy go?" *Earth Syst. Sci. Data*, 12, 2013–2041. DOI 10.5194/essd-12-2013-2020.
- Wang, Q., et al. (2020). "Eddy kinetic energy in the Arctic Ocean from a global simulation with a 1-km Arctic." *Geophys. Res. Lett.*, 47, e2020GL088550. DOI 10.1029/2020GL088550.
- Koldunov, N., et al. (2026). "Lorenz energy cycle of the global eddying ocean simulated on meshes with different designs and resolutions." *J. Adv. Model. Earth Syst.* DOI 10.1029/2025MS005551.
- Petit, T., et al. (2025). "Evaluation of a reduced RAPID array for measuring the AMOC." *J. Geophys. Res. Oceans*. DOI 10.1029/2025JC023093.

### 웹조사로 확인한 문서·튜토리얼 (URL)
- ECCO Version 4 Python Tutorial, "Global Heat Budget Closure": https://ecco-v4-python-tutorial.readthedocs.io/ECCO_v4_Heat_budget_closure.html
- ECCO, "Evaluating budgets in ECCOv4r3": https://ecco-group.org/docs/evaluating_budgets_in_eccov4r3_updated_20220118.pdf
- GFDL ESM2M ocean heat budget working notes (Griffies): https://mom-ocean.github.io/assets/pdfs/ESM2M_heat_budget.pdf
- MOM6 Analysis Cookbook, "Watermass transformation": https://mom6-analysiscookbook.readthedocs.io/en/latest/notebooks/Watermass_transformation.html
- MPAS-Analysis, "Eddy Kinetic Energy Climatology Mapping" 및 "Meridional Heat Transport" 사용자 문서: https://mpas-dev.github.io/MPAS-Analysis/
- ECMWF, "Energy and Enstrophy Cascades in Numerical Models": https://www.ecmwf.int/sites/default/files/elibrary/2011/12688-energy-and-enstrophy-cascades-numerical-models.pdf
- "The exact geostrophic streamfunction for neutral surfaces," arXiv:1903.10095: https://arxiv.org/pdf/1903.10095
- "Energetically consistent localised APE budgets ...," arXiv:2502.01686 (2025): https://arxiv.org/pdf/2502.01686
- AMOC at 26.5°N (RAPID/MOCHA), Frontiers Mar. Sci. (2019): https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2019.00260/full
- "Towards two decades of Atlantic Ocean mass and heat transports at 26.5°N," PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10590663/
- "From theory to RAPID AMOC observations," *Phil. Trans. R. Soc. A* (2023): https://royalsocietypublishing.org/doi/10.1098/rsta.2022.0192

### 비고 (출처 검증 메모)
- 위 학술 논문 서지(저자·연도·저널·권·페이지·DOI)는 2026-06 기준 WebSearch로 **개별 확인**한 실재 문헌이다. 새로 추가한 von Storch (2012) DOI(10.1175/JPO-D-12-079.1), Khatri (2018, 10.1029/2017JC013516), Scott & Wang (2005, 10.1175/JPO2771.1), Walin (1982, 10.1111/j.2153-3490.1982.tb01806.x), Trenberth & Caron (2001), Aluie et al. (2018, 10.1175/JPO-D-17-0100.1), Megann (2018, 10.1016/j.ocemod.2017.11.001), Donohue et al. (2016, 10.1002/2016GL070319), Griffies et al. (2016, 10.5194/gmd-9-3231-2016), von Schuckmann et al. (2020, 10.5194/essd-12-2013-2020), Taylor (2001, 10.1029/2000JD900719), de Vries & Weber (2005, 10.1029/2004GL021450), Koldunov et al. (2026, 10.1029/2025MS005551)는 검색으로 일치 확인.
- **수정/강등된 인용**: 원본의 *"The budgets of heat and salinity in NEMO" (Ocean Modelling, 2013)*는 정확한 저자·서지를 특정하지 못해 본 개정에서 제거하고, 동일 주제(수치혼합·염수지 잔차)를 다루는 **검증된 Megann (2018)**로 대체했다. 원본의 "Seasonality of eddy kinetic energy ... (Ocean Modelling, 2017)"는 EKE 카드의 핵심 인용에서 빼고, 검증된 Stammer (1997)·Wang et al. (2020)로 대체했다.
- DOI는 위에서 검증된 것만 기재했으며, 명시되지 않은 DOI는 임의로 생성하지 않았다.
