# 19. 검증 그림 카탈로그 — 수온·염분 도메인편 (Verification Figure Catalog — Temperature/Salinity)

이 문서는 수치모델 수온(temperature)·염분(salinity) 결과를 Argo·관측소·위성(GHRSST 등)·재분석(GLORYS 등)과 비교·검증할 때 쓰는 **그림(figure)·표(table) 레퍼런스**다. 메서드 카탈로그 [`09_domain_ocean_temp_salinity.md`](../09_domain_ocean_temp_salinity.md)의 **시각화 짝**으로, "어떤 지표를 계산하는가"(09)가 아니라 **"그 결과를 어떤 그림으로 보여주고 어떻게 읽는가"** 를 다룬다. 각 그림은 통일된 **그림 카드 8항목**으로 작성한다.

> **공통/횡단 그림은 별도 [공통편] 담당** — Taylor 다이어그램·Target 다이어그램·산점도(scatter/density)·오차 시계열 등 모든 도메인이 공유하는 그림은 공통편에서 정의한다. 이 문서는 **수온·염분 고유 그림**(T–S 다이어그램, 등밀도면, 단면, SST 전선, MLD, OHC, Hovmöller 등)에 집중하고, 횡단 그림은 교차링크만 건다.

> **출처·복제 원칙**: 실제 출처만 인용한다. **DOI는 확인된 것만** 표기하고 미확인은 "(확인요)"로 남긴다(DOI 날조 금지). **논문 그림을 복제하지 않는다** — 그림의 *유형·축·사양*만 기술한다. 공개 원본 페이지 URL은 병기할 수 있다.

> ⚠️ **그림 해석 전 반드시(09·00 G절 요약)**: ① 기준자료(GLORYS/GHRSST L4)는 **참값이 아니라 reference**이며 이미 동화·보간된 산물이다 → 독립관측처럼 쓰지 말 것. ② 색 스케일 임계·"좋음/나쁨" 경계는 **advisory**이며 변수·해역·해상도·기준자료에 의존(영역의존 경고 항상 동반). ③ **단일 그림으로 결론 금지** — 정확도+편향+패턴/분포 + 유의성을 함께 본다.

---

## 그림 카드 형식 (8항목)

```
### 그림명 (국문 / English)
- 무엇을 보여주나
- 읽는 법: 축·색·기호 + 좋은/나쁜 패턴
- 언제 쓰나: 자료형(격자/프로파일/시계열) · 검증목적
- 짝지표 & 교차링크: 수치지표 + 09(및 01–15) 카드 연결
- 만드는 법: 실존 Python 도구 + 핵심 함수
- 함정·주의
- 출처: 실제만(DOI는 확인된 것만, 미확인 "(확인요)")
```

---

### 1. 수온–염분 다이어그램 (T–S 다이어그램 / T–S diagram)

- **무엇을 보여주나**: 수온–염분 평면(가로축 염분, 세로축 온도)에 프로파일·격자에서 추출한 (T,S) 점구름을 뿌리고, 배경에 **등밀도선(isopycnal σθ/σ0)** 을 겹쳐 **수괴(water mass)** 의 위치·혼합선·핵심값을 모델과 관측에서 비교한다. 점을 **spiciness(스파이시니스)** 나 깊이로 색칠하면 등밀도면 위 수괴 대비까지 한 그림에서 본다.
- **읽는 법**: 가로축 = 염분(SP 또는 절대염분 SA), 세로축 = 온도(잠재온도 θ 또는 보존수온 Θ). 곡선 = 등밀도선(우하향). 모델 점구름과 관측 점구름을 **다른 색/마커**로 겹쳐 표시. **좋음**: 두 점구름이 겹치고 수괴 핵(국소 극점)·혼합선이 일치. **나쁨**: 모델 구름이 관측보다 **좁고 직선화**(과도한 수치확산 → 수괴 극값 평활), 핵이 등밀도선을 가로질러 이동(밀도 보존 깨짐), 한쪽 꼬리(따뜻·짠 또는 차갑·싱거운)가 누락.
- **언제 쓰나**: 자료형 = 프로파일(Argo/CTD) + 모델 3D 격자에서 동일 영역·깊이대 추출. 검증목적 = **수괴 표현 충실도·성층·혼합** 진단(정확도보다 구조·분포 축).
- **짝지표 & 교차링크**: 09 "수괴 T-S 다이어그램", "스파이시니스", "등밀도면 분석", "TEOS-10 변수 변환 전제"; 분포 정량화는 그림 #12(PDF/Q–Q/Perkins)와 짝. 밀도·spice 계산 전제는 09 TEOS-10 카드.
- **만드는 법**: `matplotlib` 산점(`scatter`, 깊이/spice로 `c=`), 등밀도선은 (S,θ) 격자에 `gsw.sigma0(SA,CT)` 계산 후 `contour`. 변수변환 `gsw.SA_from_SP`, `gsw.CT_from_t`, spice `gsw.spiciness0/1/2`. 색맵 `cmocean.cm.dense`(밀도)·`cmocean.cm.thermal`. (`gsw`=GSW-Python TEOS-10.)
- **함정·주의**: **EOS-80(θ–SP)와 TEOS-10(Θ–SA) 혼용 금지** — 축 정의를 캡션에 명시. 등밀도선의 기준압(σ0 vs σ2)을 표기. 깊이 정보가 사라지므로 단면(#4)·프로파일(#2)과 병행 해석. 점 과밀 시 투명도(alpha)·2D 히스토그램(밀도 색)으로.
- **출처**: IOC/SCOR/IAPSO (2010) *TEOS-10 Manual & Primer* — https://www.teos-10.org/pubs/TEOS-10_Primer.pdf ; GSW-Python — https://teos-10.github.io/GSW-Python/ ; spice 정의 Flament (2002) *Prog. Oceanogr.* 54, 493–501, doi:10.1016/S0079-6611(02)00065-4; McDougall & Krzysik (2015) *J. Mar. Res.* 73(5), 141–152. cmocean: Thyng et al. (2016) *Oceanography* 29(3), doi:10.5670/oceanog.2016.66.

---

### 2. Argo 프로파일 중첩 비교 (프로파일 overlay / model–obs profile overlay)

- **무엇을 보여주나**: 한 정합지점(또는 평균)에서 **세로축=깊이(아래로 증가)**, 가로축=수온(또는 염분)으로 모델 프로파일과 Argo/CTD 프로파일을 **겹쳐** 그려, 약층(thermocline/halocline)·표층 혼합·심층 구조의 형태 일치를 직관적으로 본다.
- **읽는 법**: y축 = 깊이/압력(0이 위, 깊이가 아래로). x축 = T(℃) 또는 S. 모델=실선, 관측=점/오차막대(여러 프로파일이면 평균±표준편차 음영). **좋음**: 두 곡선이 전 깊이에서 근접, 약층 깊이·기울기 일치. **나쁨**: 표층 과온/과냉, 약층이 너무 깊거나 얕음, 모델 약층이 관측보다 **완만**(과확산), 심층 계통편차(예 GLORYS overflow water 온·염 편향).
- **언제 쓰나**: 자료형 = Argo/CTD 프로파일(CSV/NetCDF) + 모델 3D 격자(동일 깊이좌표 보간). 검증목적 = **수직구조 정확도**의 정성 점검(정량은 #3).
- **짝지표 & 교차링크**: 09 "수직 프로파일 T/S 검증(Argo match-up)", "혼합층깊이(MLD)", "GLORYS 기준자료 주의점"; 정량 오차곡선은 그림 #3과 필수 짝. 정합 규약은 09 "시공간 정합/보간 전제" + [`15`](../15_preprocessing_regridding_colocation.md).
- **만드는 법**: `matplotlib` `plot`(`ax.invert_yaxis()`), 음영 `fill_betweenx`. 깊이보간 `numpy.interp`/`scipy.interpolate.interp1d`(또는 `xarray.interp`). 압력→깊이 `gsw.z_from_p`. 다중 프로파일 정합은 `xarray`+`numpy`.
- **함정·주의**: 압력 vs 깊이, 실시간 Argo QC 플래그(지연모드와 차이) 확인. 단일 프로파일은 중규모 위치 어긋남으로 큰 국소차 발생 → 다수 프로파일 평균 권장. 모델·관측 깊이좌표 불일치 시 보간오차.
- **출처**: UCAR Climate Data Guide — Argo — https://climatedataguide.ucar.edu/climate-data/argo-ocean-temperature-and-salinity-profiles ; GLORYS12 평가 Lellouche et al. (2021) *Front. Earth Sci.* 9:698876, doi:10.3389/feart.2021.698876.

---

### 3. 깊이별 오차 프로파일 (bias/RMSE 프로파일 / depth profile of bias·RMSE·RRMSE)

- **무엇을 보여주나**: 세로축=깊이, 가로축=깊이별 통계(편차 Bias(z), RMSE(z), 그리고 변동성으로 정규화한 **RRMSE(z)=RMSE(z)/σ_obs(z)**)를 곡선으로 그려, **어느 깊이에서 오차가 집중되는가**(보통 약층)를 한눈에 본다. T·S를 나란히, 또는 여러 모델/리드타임을 겹쳐 비교.
- **읽는 법**: y축 = 깊이(아래로). x축 = 통계값. Bias 곡선의 부호(좌=과소, 우=과대), RMSE 곡선의 봉우리 깊이. **좋음**: RMSE 작고 깊이에 따라 평탄, Bias≈0. **나쁨**: 약층 깊이에서 RMSE 봉우리(약층 위치·기울기 오차 신호), 표층·심층 계통편차(부호 일정), RRMSE>1(오차가 자연변동보다 큼).
- **언제 쓰나**: 자료형 = Argo 프로파일 match-up·단면. 검증목적 = **정확도+편향의 수직 분포**(정확도·편향 축).
- **짝지표 & 교차링크**: 09 "수직 프로파일 T/S 검증", "상대 RMSE(RRMSE)", "공통 오차통계(Bias/MAE/RMSE)", "강건 오차통계"; 통계 정의는 [`01`](../01_error_statistics.md). 운영 비교는 09 "GODAE Class-4".
- **만드는 법**: `xarray`로 깊이축 그룹·`numpy`로 Bias/RMSE/σ 산출, `matplotlib` `plot`(y=depth, 역축), 여러 곡선 범례. 강건판은 `numpy.median`+`scipy.stats`(MAD), bootstrap CI는 `numpy`/`scipy`.
- **함정·주의**: σ_obs가 작은 심층에서 RRMSE 과대평가·불안정(표본 부족). 깊이별 표본 수를 부도(panel)로 함께 보고. 동일 깊이좌표·동일 정합세트 사용. 단일 지표 금지 — Bias와 RMSE를 함께(부호상쇄 주의).
- **출처**: de Souza et al. (2020/2021) 4개 전구 재분석 평가 *NZ J. Mar. Freshwater Res.* 55(1), doi:10.1080/00288330.2020.1713179; GLORYS12 Lellouche et al. (2021) doi:10.3389/feart.2021.698876; 운영틀 Ryan et al. (2015) *J. Oper. Oceanogr.* 8(sup1), doi:10.1080/1755876X.2015.1022330.

---

### 4. 수직 단면 등치선도 (단면도 / vertical section contour: lat·lon–depth)

- **무엇을 보여주나**: 특정 경도·위도 라인(또는 반복관측선)을 따라 **가로축=거리/위도·경도, 세로축=깊이**의 평면에 T(또는 S)를 색칠(filled contour)하고 등온·등염·등밀도선을 겹쳐, 약층·전선·수괴 경계의 깊이·기울기를 모델과 관측에서 나란히 비교한다(보통 2패널: 모델 | 관측).
- **읽는 법**: x축 = 단면 좌표, y축 = 깊이(아래로). 색 = T/S, 곡선 = 등치선. **좋음**: 등온·등밀도선의 깊이·경사·전선 위치가 두 패널에서 일치. **나쁨**: 약층이 통째로 깊거나 얕음, 전선이 옆으로 어긋남(중규모 위치 오차), 등밀도선 간격이 모델에서 넓음(성층 약화·과확산).
- **언제 쓰나**: 자료형 = 모델 3D 격자에서 단면 추출 + CTD/XBT/glider 라인·repeat hydrography. 검증목적 = **수직·수평 구조 패턴**.
- **짝지표 & 교차링크**: 09 "수직 단면 비교(transect)", "등밀도면 분석", "등온선 깊이 D20"; 차이 단면은 그림 #5와 짝. 단면 정합·보간은 [`15`](../15_preprocessing_regridding_colocation.md).
- **만드는 법**: `xarray`로 단면 추출(`sel`/`interp` along path), `matplotlib` `contourf`+`contour`. 등밀도선 `gsw.sigma0`. 색맵 `cmocean.cm.thermal`(T)·`cmocean.cm.haline`(S). 거리축은 `gsw.distance`.
- **함정·주의**: 단면 위치·시점 정합 오차로 큰 국소차 발생(중규모) → 모델·관측에 **동일 경로·동일 깊이좌표·동일 등치선 레벨** 강제. 단일 단면은 대표성 한계(여러 단면·시점 보강). 색 스케일을 두 패널 공통으로.
- **출처**: Verezemskaya et al. (2021) GLORYS12 59.5°N 단면 평가 *JGR-Oceans* 126, doi:10.1029/2020JC016317; GO-SHIP 반복관측 — http://www.go-ship.org/.

---

### 5. 수직 단면 차이도 (차이 단면 / section difference: model − reference)

- **무엇을 보여주나**: 그림 #4와 같은 단면 평면에서 **모델 − 기준(관측/재분석)** 차(ΔT, ΔS)를 **발산형(diverging) 색맵**으로 칠해, 어느 깊이·위치에서 과대/과소인지 한 장에 본다. 등밀도선을 흑선으로 겹쳐 편차가 등밀도면을 따르는지(이류) 등밀도면을 가로지르는지(혼합·약층 오차) 구분.
- **읽는 법**: 색 = ΔT/ΔS(빨강=모델 과대(+), 파랑=과소(−)), 0이 흰색. **좋음**: 전 단면이 0색에 가깝고 부호가 무작위(편향 없음). **나쁨**: 약층 깊이에 쌍극(상온·하냉) 패턴(약층 깊이 어긋남의 전형), 한 수괴 전체가 한 부호(계통편차), 등밀도선 가로지르는 큰 차(diapycnal 오차).
- **언제 쓰나**: 자료형 = 모델·기준을 동일 단면·깊이로 보간한 격자쌍. 검증목적 = **편향의 공간 구조** 진단.
- **짝지표 & 교차링크**: 09 "수직 단면 비교", "공통 오차통계(Bias)", "GLORYS 기준자료 주의점"(차이의 부호·해역·깊이를 알려진 GLORYS 편향과 대조); 통계 보고는 [`01`](../01_error_statistics.md).
- **만드는 법**: `xarray` 차(`ds_model - ds_ref`), `matplotlib` `pcolormesh`/`contourf`(`cmap=cmocean.cm.balance`, `vmin=-v, vmax=+v` 대칭), 등밀도선 `contour`. 0중심 정규화 `matplotlib.colors.TwoSlopeNorm`.
- **함정·주의**: **발산 색맵은 반드시 0대칭**(아니면 가짜 편향 인상). 기준자료는 reference이지 참값 아님 → "모델 오차" 대신 "모델−기준 차". 보간 차수(모델→기준 vs 기준→모델)에 따라 결과 다름(규약 고정).
- **출처**: Verezemskaya et al. (2021) doi:10.1029/2020JC016317; Lellouche et al. (2021) GLORYS12 doi:10.3389/feart.2021.698876; cmocean balance — Thyng et al. (2016) doi:10.5670/oceanog.2016.66.

---

### 6. SST 편차 맵 (SST bias map / SST bias map vs GHRSST L4·in situ)

- **무엇을 보여주나**: 지도(위경도) 위에 **모델 SST − 기준(GHRSST L4: OSTIA/MUR/CMC, 또는 부이/drifter 격자화)** 차를 발산 색맵으로 칠해, 편향의 공간 분포(연안·전선·용승역 집중 여부)를 본다. 강건판은 격자별 **중앙값 편차/MAD**를 함께 표시.
- **읽는 법**: 색 = ΔSST(빨강 과대/파랑 과소, 0 흰색), cartopy 해안선·육지 마스크. **좋음**: 대부분 0색, 부호 무작위. **나쁨**: 서안경계류·전선역의 띠 모양 큰 편차(중규모 위치 어긋남), 연안·해빙역 일관 편차, 평균편차(mean)와 중앙값편차(median)가 크게 다름(이상치/비대칭 신호).
- **언제 쓰나**: 자료형 = 격자 L4 위성 SST + 모델 격자(동일 일평균·동일 격자 보간). 검증목적 = **편향의 공간 구조**(편향 축) + 강건성.
- **짝지표 & 교차링크**: 09 "SST 표층 검증", "강건 오차통계(median/MAD)", "공통 오차통계"; 면적가중·패턴상관(ACC)은 [`01`](../01_error_statistics.md)/[`02`](../02_spatial_pattern_verification.md); 위성 처리수준·매치업은 [`12`](../12_satellite_remote_sensing.md). SSS 변형은 그림 #8.
- **만드는 법**: `xarray` 차, `cartopy`(`PlateCarree`, `add_feature` 해안/육지) + `matplotlib` `pcolormesh`(`cmap=cmocean.cm.balance`, 대칭 norm). 강건통계 `numpy.median`·`scipy.stats.median_abs_deviation`. 면적가중 평균 cosφ.
- **함정·주의**: **GHRSST L4는 분석·보간 산물(독립관측 아님)** → 차를 "모델 오차"로 단정 금지, 이중계산 주의. skin/subskin vs foundation/bulk 깊이 정의 차·일변동(diurnal) 보정. 연안·고위도 L4 신뢰도 저하. 색 스케일 임계는 advisory(해역의존).
- **출처**: GHRSST/WMO-IOC JCOMM 검증 관행(표준 지침); NOAA Global RTOFS Class-1 — https://polar.ncep.noaa.gov/global/class-1/ ; UCAR Climate Data Guide. cmocean balance: Thyng et al. (2016) doi:10.5670/oceanog.2016.66.

---

### 7. SST 전선 맵 (SST 전선/경도 맵 / SST front map: gradient·Canny·BOA)

- **무엇을 보여주나**: SST의 **수평기울기 |∇SST|** 와 검출된 **전선(front)** 위치·강도·**전선빈도(frontal frequency)** 를 지도에 표시하고, 모델과 위성 SST에서 **나란히** 비교한다. 중규모·연안용승·해류경계 재현 점검.
- **읽는 법**: 색 = |∇SST|(℃/km)·또는 전선빈도(%), 위에 검출된 전선선(에지) 오버레이. **좋음**: 강한 전선(만류·쿠로시오·용승 전선)의 위치·강도·빈도가 두 패널 일치. **나쁨**: 모델 전선이 **약하고 번짐**(평활화·과확산), 전선 위치 이동, 구름/잡음으로 위성 전선 왜곡. 사건검증(POD/FAR/CSI)으로 정량화 가능.
- **언제 쓰나**: 자료형 = 위성/모델 SST 격자(NetCDF). 검증목적 = **중규모 구조·전선 패턴**(패턴 축).
- **짝지표 & 교차링크**: 09 "수온전선 검출·강도"; 사건검증 분할표는 [`03`](../03_categorical_event_extremes.md); 공간패턴·객체검증은 [`02`](../02_spatial_pattern_verification.md); 위성 전선은 [`12`](../12_satellite_remote_sensing.md).
- **만드는 법**: 기울기 `numpy.gradient`/`scipy.ndimage.sobel`(또는 `gsw.distance`로 km 환산). Canny `skimage.feature.canny`. Cayula–Cornillon(SIED)·Belkin–O'Reilly(BOA)는 전용 구현(예 R `grec`/`boaR`, Python 포팅). 지도 `cartopy`, 색맵 `cmocean.cm.thermal`/`amp`.
- **함정·주의**: 검출 결과는 알고리즘·임계·평활반경·해상도에 **매우 민감** → 모델·관측에 **동일 설정** 강제. Canny는 과소검출, Laplacian은 과대검출 경향. 모델 해상도가 낮으면 전선 구조적으로 부족(공정 비교 위해 동일 격자로).
- **출처**: Cayula & Cornillon (1992) *J. Atmos. Oceanic Technol.* 9(1), 67–80, doi:10.1175/1520-0426(1992)009<0067:EDAFSI>2.0.CO;2; Canny (1986) *IEEE TPAMI* 8(6), 679–698, doi:10.1109/TPAMI.1986.4767851 (확인요); Belkin & O'Reilly (2009) "An algorithm for oceanic front detection in chlorophyll and SST satellite imagery" *J. Marine Systems* 78, 319–326 — https://www.sciencedirect.com/science/article/abs/pii/S0924796309000682 (DOI 확인요).

---

### 8. SSS 편차 맵 (표층 염분 편차 맵 / SSS bias map vs SMOS·SMAP·Argo)

- **무엇을 보여주나**: 지도 위에 **모델 SSS − 기준(위성 SMOS/SMAP/Aquarius L3·L4, 또는 Argo 표층 격자화)** 차를 발산 색맵으로 칠해, 강·강수·용승역의 표층 염분 편향 분포를 본다. 위성 신뢰도가 낮은 해역(연안·저온·강수)은 Argo 기반과 병행.
- **읽는 법**: 색 = ΔSSS(PSU 또는 g·kg⁻¹; 빨강 과대/파랑 과소, 0 흰). **좋음**: 외양에서 0색. **나쁨**: 하구·강수역 일관 편차(담수 강제 오차), 위성기반에서 연안·고위도 잡음성 큰 편차(위성 한계일 수 있음 → Argo와 교차).
- **언제 쓰나**: 자료형 = 위성 L3/L4 SSS 격자 + Argo 표층 + 모델 격자. 검증목적 = **표층 담수·염분 편향**(편향 축).
- **짝지표 & 교차링크**: 09 "SSS 표층 염분 검증", "담수함량 FWC"; 위성 SSS 매치업·대표성오차는 [`12`](../12_satellite_remote_sensing.md); 통계는 [`01`](../01_error_statistics.md). T–S 구조는 그림 #1.
- **만드는 법**: `xarray` 차, `cartopy`+`matplotlib` `pcolormesh`(`cmap=cmocean.cm.balance` 대칭), 염분 절대값 맵은 `cmocean.cm.haline`. 위성 QC·평활 `scipy.ndimage`. SP↔SA 변환 `gsw.SA_from_SP`.
- **함정·주의**: 위성 염분은 SST<5℃·강수·육지근접에서 큰 오차(RFI/한랭편향) → 그 해역은 Argo 우선. 위성 SSS(~1cm)와 Argo(~5–10m)·모델 깊이 정의 차. **위성 자체가 검증 대상**일 수 있음(reference 신뢰도 명시). PSU vs g·kg⁻¹ 단위 통일.
- **출처**: NASA GSFC Aquarius+Argo SSS 검증세트 — https://earth.gsfc.nasa.gov/cryo/data/sea-surface-salinity ; UCAR Climate Data Guide — Salinity — https://climatedataguide.ucar.edu/variables/ocean/salinity ; TEOS-10 — https://www.teos-10.org/.

---

### 9. 혼합층깊이 비교 (MLD 맵·산점 / Mixed Layer Depth comparison)

- **무엇을 보여주나**: 동일 임계기준으로 산출한 MLD를 **(a) 지도 2패널(모델 | 관측/Argo 기후값) + 차이 맵**, 또는 **(b) 모델 vs 관측 MLD 산점도(1:1선)** 로 비교한다. 겨울 깊은 혼합·여름 얕은 혼합의 계절성 재현을 점검.
- **읽는 법**: (a) 색 = MLD(m, 깊을수록 진하게), 차이 맵은 발산 색맵. (b) 점이 1:1선 위. **좋음**: 공간 패턴·계절성 일치, 산점 1:1선 밀집. **나쁨**: 모델 MLD가 계절적으로 과대/과소(겨울 과혼합/여름 과성층), 고위도·서안경계류역 큰 차, 산점 기울기≠1(조건편향).
- **언제 쓰나**: 자료형 = 모델 3D 격자 + Argo 프로파일/MLD 기후값. 검증목적 = **표층 혼합·계절성**(패턴+편향 축).
- **짝지표 & 교차링크**: 09 "혼합층깊이(MLD)", "등온층깊이·장벽층(ILD/BLT)"; bias/RMSE는 [`01`](../01_error_statistics.md); 산점·1:1은 공통편(횡단). 프로파일 근거는 그림 #2.
- **만드는 법**: MLD 산출 — 임계법(de Boyer Montégut: ΔT=0.2℃ 또는 Δσθ=0.03 kg·m⁻³) `numpy`/`xarray`; 하이브리드는 Holte & Talley 알고리즘. 밀도 `gsw.sigma0`. 지도 `cartopy`+`pcolormesh`(`cmocean.cm.deep`), 산점 `matplotlib.scatter`+1:1선.
- **함정·주의**: **임계값·기준깊이를 모델·관측에 동일하게** (방법 불일치 시 비교 무효). Argo 10일 주기로 아계절 MLD 변동 과소해상. 약한 성층·장벽층에서 온도-MLD와 밀도-MLD 괴리(ILD/BLT로 보완). 지역별 최적 임계 차이 인지(advisory).
- **출처**: de Boyer Montégut et al. (2004) *JGR* 109, C12003, doi:10.1029/2004JC002378; Holte & Talley (2009) *J. Atmos. Oceanic Technol.* 26(9), 1920–1939, doi:10.1175/2009JTECHO543.1; Holte et al. (2017) Argo MLD climatology *GRL*, doi:10.1002/2017GL073426.

---

### 10. 해양열함량 시계열·추세 맵 (OHC 시계열·맵 / Ocean Heat Content time series & trend map)

- **무엇을 보여주나**: 깊이적분 열함량 OHC(0–300/0–700/0–2000m)의 **(a) 영역평균 시계열**(모델 vs NCEI/IAP/Copernicus OMI 관측기반)과 **(b) 추세 맵**(℃ 또는 J·m⁻² 적분량의 단위시간 변화)을 비교한다. 담수/염함량(FWC) 적분량도 같은 틀로.
- **읽는 법**: (a) x=시간, y=OHC(또는 OHC anomaly), 곡선 겹침+불확실성 음영. (b) 색 = 추세(발산), cartopy. **좋음**: 시계열 위상·추세·연변동 일치, 추세 맵 패턴 일치. **나쁨**: 추세 부호·크기 어긋남(에너지 불균형 재현 실패), 심층 적분에서 큰 차(관측 제약 약한 영역), 적분 상하한·상수 불일치로 인한 offset.
- **언제 쓰나**: 자료형 = 모델 3D 격자 + 관측기반 OHC 격자/지수. 검증목적 = **적분 보존량·기후 추세**(편향+위상+물리 축).
- **짝지표 & 교차링크**: 09 "해양열함량(OHC)", "해양염함량/담수함량(FWC)", "Murphy 스킬점수(추세 대비)"; 추세·변화점은 [`06`](../06_timeseries_signal.md); 보존·열수지는 [`04`](../04_conservation_energy_flux.md).
- **만드는 법**: 적분 `OHC=∫ρ·cp·Θ dz`를 `xarray`(`(rho*cp*CT).integrate('depth')`), 면적평균 cosφ 가중. ρ `gsw.rho`, Θ `gsw.CT_from_t`. 시계열 `matplotlib.plot`+`fill_between`(불확실성), 추세 `numpy.polyfit`/`scipy.stats.linregress`, 맵 `cartopy`.
- **함정·주의**: **깊이층·상수(ρ0≈1026–1030, cp≈3985–3996)·기후값 정의를 명시**(다르면 값 자체가 달라짐). 보존수온 Θ 사용 권장. 심층(>2000m) 관측 부족 → 모델 제약 약함. 면적가중 필수. 기준자료(OMI 등)도 reference.
- **출처**: von Schuckmann et al. (2019) *Front. Mar. Sci.* 6:432, doi:10.3389/fmars.2019.00432; NOAA NCEI Global OHC — https://www.ncei.noaa.gov/access/global-ocean-heat-content/ ; Copernicus Marine OMI OHC — https://data.marine.copernicus.eu/product/GLOBAL_OMI_OHC_area_averaged_anomalies_0_300/description.

---

### 11. 등밀도면 분포 맵 (등밀도면 / isopycnal surface map: depth & spice on isopycnal)

- **무엇을 보여주나**: 특정 등밀도면(예 σθ=27.0 kg·m⁻³) 위의 **(a) 면 깊이(depth of isopycnal)** 와 **(b) 면상 변수(염분 또는 spiciness)** 를 지도로 그려, 수괴 이류·혼합을 **밀도좌표**에서 모델-관측 비교한다. 약층·중층수의 분포·전선을 밀도와 분리해 본다.
- **읽는 법**: (a) 색 = 등밀도면 깊이(m), (b) 색 = S 또는 spice(따뜻·짠 = 큰 값). **좋음**: 면 깊이·면상 spice 분포·전선 위치 일치. **나쁨**: 모델 spice 대비가 **약함**(등밀도 혼합 과다·수치확산), 면 깊이 계통편차(중층수 두께 오차), 등밀도면이 사라지는 영역(밀도역전·약한 성층).
- **언제 쓰나**: 자료형 = 모델·재분석·Argo를 **등밀도좌표로 변환** 후. 검증목적 = **수괴 이류·등밀도 혼합**(패턴+분포 축).
- **짝지표 & 교차링크**: 09 "등밀도면 분석", "스파이시니스", "TEOS-10 변수 변환 전제"; T–S 평면 짝은 그림 #1, 단면 짝은 #4. 좌표변환·보간은 [`15`](../15_preprocessing_regridding_colocation.md).
- **만드는 법**: 밀도 `gsw.sigma0(SA,CT)`, 깊이→등밀도 보간 `numpy.interp`/`xarray`(각 수평점에서 σ축으로). spice `gsw.spiciness0`. 지도 `cartopy`+`pcolormesh`(깊이 `cmocean.cm.deep`, spice `cmocean.cm.thermal`/`balance`).
- **함정·주의**: 약한 성층·밀도역전에서 등밀도좌표 모호(마스크). 좌표변환 보간오차. **기준압 선택(σ0 vs σ2)에 따라 결과 상이**(명시). spice "직교성"의 물리적 의미 제한적(McDougall & Krzysik 2015) — 정의·기준압 캡션 명시.
- **출처**: IOC/SCOR/IAPSO (2010) *TEOS-10 Manual/Primer* — https://www.teos-10.org/pubs/TEOS-10_Primer.pdf ; Flament (2002) doi:10.1016/S0079-6611(02)00065-4; McDougall & Krzysik (2015) *J. Mar. Res.* 73(5), 141–152; GSW-Python — https://teos-10.github.io/GSW-Python/.

---

### 12. T/S 분포 비교 그림 (PDF·Q–Q·Perkins / PDF · Q–Q plot · Perkins overlap)

- **무엇을 보여주나**: T 또는 S 값의 **확률밀도(PDF) 겹침**, **분위수-분위수(Q–Q) 산점**, 그리고 **Perkins skill score(겹침면적)** 를 한 그림(또는 패널)으로 보여, 평균·분산을 넘어 **분포 형태·꼬리(극값)·왜도**의 일치를 본다.
- **읽는 법**: (a) PDF 곡선 두 개(모델/관측) 겹침, 겹친 면적=PSS(0~1). (b) Q–Q: 점이 대각선이면 분포 일치. **좋음**: PDF 거의 포개짐(PSS→1), Q–Q 대각선. **나쁨**: 모델 PDF가 **좁음/뾰족함**(변동 과소·과확산), 한쪽 꼬리 누락(극값 미재현), Q–Q 끝이 대각선에서 벗어남(꼬리 편차).
- **언제 쓰나**: 자료형 = SST/SSS/프로파일 값 집합·OHC(격자·시계열). 검증목적 = **분포·꼬리**(분포 축).
- **짝지표 & 교차링크**: 09 "확률밀도·분포 비교(PDF/Q–Q/Perkins)"; KS·분포검정은 [`01`](../01_error_statistics.md); 극값 분포 비교는 [`03`](../03_categorical_event_extremes.md). 수괴 분포는 그림 #1과 짝.
- **만드는 법**: 히스토그램/PDF `numpy.histogram`(공통 bin) 또는 `scipy.stats.gaussian_kde`; Q–Q `scipy.stats.probplot`/분위수 `numpy.quantile`; KS `scipy.stats.ks_2samp`; PSS = `numpy.minimum(p_m,p_o).sum()`. 그림 `matplotlib`.
- **함정·주의**: **bin 크기에 PSS·PDF 민감**(동일 bin 강제). 공간·시간 상관 무시(독립 가정 → 유의성 과대). 평균이 맞아도 분포가 다를 수 있음 → bias·RMSE와 병행. 동일 표본영역·동일 기간.
- **출처**: Perkins et al. (2007) *J. Climate* 20(17), 4356–4376, doi:10.1175/JCLI4253.1; Wilks, *Statistical Methods in the Atmospheric Sciences*(Q–Q/KS — 표준 참고문헌).

---

### 13. Hovmöller 다이어그램 (SST 이상 호브묄러 / Hovmöller: SST anomaly time–longitude)

- **무엇을 보여주나**: **가로축=경도(또는 위도), 세로축=시간**(또는 반대)으로 위도대 평균한 **SST 이상치(anomaly)** 를 색으로 칠해, 전파(서향/동향)하는 파동·ENSO·계절 신호를 모델과 관측에서 비교한다. **변형**: 한 정점/단면의 **깊이-시간(depth–time) Hovmöller**로 약층·MLD·수괴의 시간변동 비교.
- **읽는 법**: 기울어진 줄무늬의 **기울기 = 전파속도/방향**, 줄무늬 색 = 양/음 이상. **좋음**: 모델과 관측에서 줄무늬의 위상·속도·진폭 일치. **나쁨**: 전파속도 틀림(줄무늬 기울기 차), 이상 진폭 과소/과대, 위상 지연(ENSO 등 신호 어긋남).
- **언제 쓰나**: 자료형 = 시간 차원이 있는 격자장(SST anomaly) 또는 정점 깊이-시간. 검증목적 = **위상·전파·변동**(시간/패턴 축).
- **짝지표 & 교차링크**: 09 "EOF/주성분 변동성", "등온선 깊이 D20"(열대 전파); 교차상관/lag·위상은 [`06`](../06_timeseries_signal.md); 변동모드는 [`05`](../05_spectral_eof_modal.md). 분포 짝은 #12.
- **만드는 법**: 위도대 평균 `xarray`(`.mean('lat')`), 이상치 = 값 − 기후값(`groupby('time.month')` 제거), `matplotlib` `pcolormesh`/`contourf`(x=lon, y=time, `cmap=cmocean.cm.balance` 대칭). 깊이-시간 변형은 y=depth(역축).
- **함정·주의**: 기후값(climatology) 정의·기준기간이 이상치를 좌우 → 모델·관측 **동일 기후값**. 위도대 평균 폭·발산 색맵 0대칭 명시. 시간 자기상관으로 유효자유도 작음(유의성 과대 주의).
- **출처**: Hovmöller, E. (1949) "The trough-and-ridge diagram." *Tellus* 1(2), 62–66 (DOI 확인요); 역사·용법 Persson (2017) *BAMS* 98(5) "The Story of the Hovmöller Diagram", doi:10.1175/BAMS-D-15-00234.1 (확인요); NOAA Climate.gov 해설 — https://www.climate.gov/news-features/understanding-climate/hovmöller-diagram-climate-scientists-best-friend.

---

### 14. 파수 스펙트럼 비교 (SST/SSH 파수 스펙트럼 / wavenumber spectrum comparison)

- **무엇을 보여주나**: SST(또는 SSH·OHC)의 **1D/2D 파워스펙트럼밀도 PSD(k)** 를 로그-로그로 그려, **중규모(mesoscale) 대역의 에너지·스펙트럼 기울기**를 모델과 위성/관측에서 비교한다. 모델 **유효해상도(effective resolution)** 와 과확산(에너지 부족)을 진단.
- **읽는 법**: x=파수 k(또는 파장, 로그), y=PSD(로그). **좋음**: 중규모 대역에서 스펙트럼이 겹치고 기울기 일치. **나쁨**: 모델 곡선이 고파수(작은 스케일)에서 관측보다 **아래로 처짐**(중규모 에너지 부족·과확산 → 유효해상도가 격자해상도보다 나쁨), 위성 잡음 floor가 고파수 평탄화.
- **언제 쓰나**: 자료형 = 고해상 격자(NetCDF)·위성 along-track/맵. 검증목적 = **중규모 변동 에너지·유효해상도**(스펙트럼 축).
- **짝지표 & 교차링크**: 09 "스펙트럼·파수 분석"; 스펙트럼 코어·윈도/디트렌드는 [`05`](../05_spectral_eof_modal.md); 고도계 파수스펙트럼·유효해상도는 [`12`](../12_satellite_remote_sensing.md); AI 산출물이면 RAPSD는 [`14`](../14_ai_ml_evaluation.md).
- **만드는 법**: 디트렌드·윈도(`scipy.signal.detrend`, `windows`), 2D FFT `numpy.fft.fft2`+방사평균, 또는 `scipy.signal.welch`(1D 트랙). 등에너지 파수·기울기 `numpy.polyfit`(로그-로그). 그림 `matplotlib`(loglog).
- **함정·주의**: **동일 해상도·동일 디트렌드·동일 윈도** 강제(아니면 비교 무효). 동화·평활로 모델 중규모 에너지 과소(구조적). 위성 잡음 floor·결측 보간이 고파수 왜곡. 영역 크기·테이퍼에 민감.
- **출처**: Wilks(스펙트럼 분석 — 표준 참고문헌); 운영 재분석 중규모 평가 사례(예 GLONET, arXiv:2412.05454 — 동료심사 여부 확인요); 스펙트럼 코어는 [`05`](../05_spectral_eof_modal.md).

---

## 요약표 — 그림 → 검증목적 → 짝지표 → 09 교차링크

| # | 그림 (국문 / English) | 자료형 | 검증목적(축) | 짝지표(수치) | 09 교차링크(핵심) |
|---|---|---|---|---|---|
| 1 | T–S 다이어그램 / T–S diagram | 프로파일+격자 | 수괴·구조·분포 | spice·등밀도, PSS | 수괴 T-S·스파이시니스·등밀도면·TEOS-10 |
| 2 | 프로파일 overlay / profile overlay | 프로파일+격자 | 수직구조(정성) | Bias(z)·RMSE(z) | Argo match-up·MLD·GLORYS 주의 |
| 3 | 깊이별 오차 프로파일 / bias·RMSE profile | 프로파일 | 정확도·편향(수직) | Bias/RMSE/RRMSE(z) | 프로파일 검증·RRMSE·Class-4 |
| 4 | 단면 등치선도 / section contour | 격자 단면 | 수직·수평 구조 | 등치선 위치·단면 RMSE | 수직 단면 비교·등밀도면·D20 |
| 5 | 단면 차이도 / Δ section | 격자 단면 | 편향 구조 | ΔT/ΔS(거리,깊이) | 수직 단면·Bias·GLORYS 주의 |
| 6 | SST 편차 맵 / SST bias map | 격자 | 편향 공간구조+강건 | Bias·median/MAD·ACC | SST 검증·강건통계·공통오차 |
| 7 | SST 전선 맵 / SST front map | 격자 | 중규모·전선 패턴 | \|∇SST\|·POD/FAR/CSI | 수온전선 검출·강도 |
| 8 | SSS 편차 맵 / SSS bias map | 격자+프로파일 | 표층 염분 편향 | Bias·RMSE | SSS 검증·담수함량 |
| 9 | MLD 비교 / MLD comparison | 프로파일+격자 | 혼합·계절성 | MLD Bias/RMSE·1:1 | MLD·ILD/BLT |
| 10 | OHC 시계열·맵 / OHC series & map | 격자 시계열 | 적분 보존량·추세 | OHC 추세·상관·MSESS | OHC·FWC·Murphy SS |
| 11 | 등밀도면 분포 / isopycnal map | 격자(밀도좌표) | 수괴 이류·혼합 | 면 깊이·면상 spice | 등밀도면·스파이시니스·TEOS-10 |
| 12 | PDF·Q–Q·Perkins | 격자+시계열 | 분포·꼬리 | PSS·KS·Q–Q | PDF/Q–Q/Perkins |
| 13 | Hovmöller (SST anomaly) | 격자 시계열 | 위상·전파·변동 | lag 상관·전파속도 | EOF·D20(전파) |
| 14 | 파수 스펙트럼 / wavenumber spectrum | 고해상 격자 | 중규모 에너지·유효해상도 | PSD(k)·기울기 | 스펙트럼·파수 분석 |

> **횡단(공통편) 그림**: Taylor 다이어그램·Target 다이어그램·산점/밀도 산점(1:1)·오차 시계열·Q–Q(범용)는 **[공통편]** 에서 정의하며 이 문서는 교차링크만 둔다. 위 모든 그림은 09·00 G절 원칙(기준자료=reference, 임계 advisory, 단일 그림 금지)을 강제한다.

---

## 출처 (References) — 이 문서에서 인용한 figure 관련 1차/도구 출처

> 표기: DOI는 본 작업에서 웹으로 확인한 것만 병기. "(확인요)"는 발행본/동료심사/DOI 자릿수의 추가 확인 권장. URL은 조사 시점 접근 가능 페이지. 논문 그림은 복제하지 않고 유형·사양만 기술.

**지표·방법 1차 문헌(그림 근거)**
- Taylor, K. E. (2001) *J. Geophys. Res.* 106(D7), 7183–7192, doi:10.1029/2000JD900719. (Taylor diagram — 공통편)
- Jolliff, J. K., et al. (2009) *J. Marine Systems* 76, 64–82, doi:10.1016/j.jmarsys.2008.05.014. (Target diagram — 공통편)
- Stow, C. A., et al. (2009) "Skill assessment for coupled biological/physical models of marine systems." *J. Marine Systems* 76, 4–15, doi:10.1016/j.jmarsys.2008.03.011. (모델 스킬 평가 종합)
- Perkins, S. E., et al. (2007) *J. Climate* 20(17), 4356–4376, doi:10.1175/JCLI4253.1. (PDF/Perkins skill score)
- de Boyer Montégut, C., et al. (2004) *J. Geophys. Res.* 109, C12003, doi:10.1029/2004JC002378. (MLD 임계법·기후값)
- Holte, J., & Talley, L. (2009) *J. Atmos. Oceanic Technol.* 26(9), 1920–1939, doi:10.1175/2009JTECHO543.1. (하이브리드 MLD); Holte et al. (2017) *GRL*, doi:10.1002/2017GL073426.
- Flament, P. (2002) *Prog. Oceanogr.* 54, 493–501, doi:10.1016/S0079-6611(02)00065-4; McDougall, T. J., & Krzysik, O. A. (2015) *J. Marine Research* 73(5), 141–152. (spiciness)
- von Schuckmann, K., et al. (2019) *Front. Mar. Sci.* 6:432, doi:10.3389/fmars.2019.00432. (OHC)
- Cayula, J.-F., & Cornillon, P. (1992) *J. Atmos. Oceanic Technol.* 9(1), 67–80, doi:10.1175/1520-0426(1992)009<0067:EDAFSI>2.0.CO;2. (SIED 전선)
- Canny, J. (1986) *IEEE TPAMI* 8(6), 679–698, doi:10.1109/TPAMI.1986.4767851 (확인요). (Canny 에지)
- Belkin, I. M., & O'Reilly, J. E. (2009) "An algorithm for oceanic front detection in chlorophyll and SST satellite imagery." *J. Marine Systems* 78, 319–326 — https://www.sciencedirect.com/science/article/abs/pii/S0924796309000682 (DOI 확인요). (BOA 전선)
- Hovmöller, E. (1949) "The trough-and-ridge diagram." *Tellus* 1(2), 62–66 (DOI 확인요); Persson, A. (2017) *BAMS* 98(5), doi:10.1175/BAMS-D-15-00234.1 (확인요). (Hovmöller)

**운영 검증틀·재분석 평가**
- Ryan, A. G., et al. (2015) "GODAE OceanView Class 4 forecast verification framework." *J. Operational Oceanography* 8(sup1), S98–S111, doi:10.1080/1755876X.2015.1022330.
- Lellouche, J.-M., et al. (2021) "The Copernicus Global 1/12° GLORYS12 Reanalysis." *Front. Earth Sci.* 9:698876, doi:10.3389/feart.2021.698876.
- Verezemskaya, P., et al. (2021) GLORYS12 59.5°N 단면 평가 *J. Geophys. Res. Oceans* 126, doi:10.1029/2020JC016317.
- de Souza, J. M. A. C., et al. (2020/2021) 4개 전구 재분석 평가 *NZ J. Mar. Freshwater Res.* 55(1), doi:10.1080/00288330.2020.1713179.

**표준·도구·자료 페이지**
- IOC, SCOR & IAPSO (2010) *TEOS-10 Manual & Primer* — https://www.teos-10.org/pubs/TEOS-10_Primer.pdf
- GSW-Python (Gibbs SeaWater TEOS-10 toolbox) — https://teos-10.github.io/GSW-Python/ ; https://www.teos-10.org/software.htm
- Thyng, K. M., et al. (2016) "True colors of oceanography." *Oceanography* 29(3), doi:10.5670/oceanog.2016.66. (cmocean 색맵)
- Taylor diagram Python 구현: Copin, Y. — https://gist.github.com/ycopin/3342888 (Zenodo doi:10.5281/zenodo.5548061); SkillMetrics(Rochford) — https://github.com/PeterRochford/SkillMetrics (공통편 Taylor/Target용)
- matplotlib / xarray / numpy / scipy / scikit-image / cartopy / eofs — 표준 Python 과학·시각화 패키지(figure 생성 도구)
- GHRSST / WMO-IOC JCOMM SST 검증 관행(표준 지침); NOAA Global RTOFS Class-1 — https://polar.ncep.noaa.gov/global/class-1/
- UCAR Climate Data Guide — Argo / Salinity — https://climatedataguide.ucar.edu/ ; NASA GSFC SSS 검증세트 — https://earth.gsfc.nasa.gov/cryo/data/sea-surface-salinity
- NOAA NCEI Global OHC — https://www.ncei.noaa.gov/access/global-ocean-heat-content/ ; Copernicus Marine OMI OHC — https://data.marine.copernicus.eu/

> **메서드 카탈로그 짝**: 모든 그림의 지표 정의·해석임계·한계는 [`09_domain_ocean_temp_salinity.md`](../09_domain_ocean_temp_salinity.md)에 있으며, 횡단 통계·도구는 [`01`](../01_error_statistics.md)·[`02`](../02_spatial_pattern_verification.md)·[`05`](../05_spectral_eof_modal.md)·[`06`](../06_timeseries_signal.md)·[`12`](../12_satellite_remote_sensing.md)·[`15`](../15_preprocessing_regridding_colocation.md)를 참조한다.
