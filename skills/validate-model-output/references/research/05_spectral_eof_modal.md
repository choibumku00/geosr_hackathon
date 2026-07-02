# 스펙트럼·EOF·모달 분석 (Spectral / EOF / Modal Analysis)

수치모델 결과(NetCDF 격자자료, CSV/텍스트 시계열)를 ERA5/GLORYS 등 재분석자료·관측소·위성자료와 비교·검증할 때, **시간/공간 변동성의 구조(structure)** 를 주파수·파수·모드 공간에서 정량 비교하는 방법들을 망라한다. 단순 오차지표(RMSE 등)가 "값이 얼마나 맞나"를 본다면, 이 카탈로그의 방법들은 "**변동의 분포·전파·결합 구조가 얼마나 닮았나**"를 본다(예: 모델 에너지 스펙트럼 기울기, 조석 진폭·위상, 지배 EOF 모드의 공간패턴, 회전 스펙트럼의 시계/반시계 에너지). 도메인(기상·파랑·수온·해류·해수면)에 따라 회전 스펙트럼(해류), 조화·조석 분해(조위·조류), 파수 스펙트럼(SSH·SST 격자) 등 적용 방법이 달라지므로, 각 카드의 "적용 도메인" 항목을 라우팅 근거로 사용할 수 있다.

> **주의(전제 공통)**: 스펙트럼·EOF 비교는 **모델과 기준자료를 동일한 시공간 격자·동일 기간으로 정렬(align)** 하고, **결측 처리·디트렌딩·창함수(window)·표본주기(sampling)** 조건을 일치시킨 뒤 수행해야 공정하다. 한쪽만 보간/필터링하면 스펙트럼·모드가 인위적으로 달라진다. 특히 (a) **Nyquist·앨리어싱**(표본주기보다 빠른 변동은 접힘), (b) **스펙트럼 정규화·단위**(편측 vs 양측, m²/Hz vs dB), (c) **면적가중**(EOF·SVD에서 \(\sqrt{\cos\phi}\)), (d) **추세·평균 제거** 방식은 반드시 모델·기준 양쪽에 똑같이 적용한다.

## 이 파일에 담은 방법 (한 줄 목차)
- **파워스펙트럼 밀도 PSD (Welch/periodogram)** — 주파수별 분산 분포 비교
- **멀티테이퍼 스펙트럼 (Thomson multitaper)** — 저편향·저분산 PSD, F-검정 라인 검출
- **Lomb-Scargle 주기도** — 불규칙·결측 시계열의 스펙트럼
- **스펙트럼 기울기·분광법칙 비교 (spectral slope)** — 난류 관성영역 기울기(k^-5/3, k^-3 등)
- **파수 스펙트럼 (wavenumber spectrum)** — 격자장 공간 변동의 에너지 분포(SSH/SST)
- **파수-주파수 스펙트럼 (k-ω spectrum)** — 전파·분산관계, 파동 식별
- **회전 스펙트럼 (rotary spectrum)** — 해류·바람 벡터의 시계/반시계 에너지
- **조화·조석 분해 (harmonic/tidal analysis, T_TIDE/UTide)** — 조석 분조 진폭·위상
- **교차스펙트럼·코히어런스 (cross-spectrum / coherence)** — 두 신호의 주파수별 결합·위상
- **고차 스펙트럼·바이스펙트럼 (bispectrum / higher-order spectra)** — 비선형 위상결합(3파 상호작용)
- **웨이블릿 변환 (CWT, Torrence-Compo)** — 시간-주파수 비정상 변동
- **교차웨이블릿·웨이블릿 코히어런스 (XWT/WTC)** — 두 신호의 시간-주파수 결합
- **경험모드분해·힐버트-황 변환 (EMD/EEMD/HHT)** — 비선형·비정상 적응형 분해와 순간주파수
- **EOF/PCA (경험직교함수)** — 지배 시공간 변동모드 분해·비교
- **회전 EOF (Rotated EOF, VARIMAX)** — 물리적 해석성 향상된 모드
- **복소/Hilbert EOF (CEOF)** — 전파성(propagating) 변동모드
- **확장 EOF / M-SSA (Extended EOF)** — 시간지연 결합, 전파·진동 구조
- **특이스펙트럼분석 SSA / MC-SSA** — 단일 시계열의 추세·진동 성분 추출
- **SVD / 최대공분산분석 MCA** — 두 장(field) 사이 결합 변동모드
- **정준상관분석 CCA** — 두 장의 상관 최대화 모드쌍
- **고유직교분해 POD / snapshot POD** — 에너지 최적 시공간 모드(EOF의 유체역학 형태)
- **스펙트럼 POD (SPOD)** — 주파수별 결맞은(coherent) 시공간 구조
- **동역학모드분해 DMD** — 데이터 구동 모드+성장률/진동수(준선형 동역학)
- **테일러 다이어그램(스펙트럼/모드용 보조)** — 모드 진폭계수·재구성장의 종합 비교

---

### 파워스펙트럼 밀도 PSD — Welch/주기도법 (전력스펙트럼밀도 / Power Spectral Density, Welch's method)
- **무엇을 측정/검증하나**: 시계열 분산이 주파수별로 어떻게 분포하는지. 모델이 관측·재분석과 같은 주파수대(일주기·반일주기·관성주기·계절·경년 등)에 같은 양의 에너지를 갖는지 비교.
- **정의·수식**: 자기상관함수의 푸리에 변환이 PSD(Wiener-Khinchin). Welch법은 시계열을 겹치는 구간(segment)으로 나눠 각 구간에 창함수(예: Hann)를 곱하고 주기도(periodogram)를 구한 뒤 평균: \( \hat S(f) = \frac{1}{K}\sum_{k=1}^{K} |X_k(f)|^2 \). Parseval에 의해 \( \int S(f)\,df = \mathrm{Var}(x) \).
- **적용 도메인/자료형**: 모든 도메인의 **시계열**(조위·수온·유속·풍속·파고). 격자자료는 격자점별 또는 영역평균 시계열에 적용.
- **입력·전제**: 등간격 표본(불규칙이면 Lomb-Scargle), 약정상성(weakly stationary). 디트렌딩·평균제거 필요. 창함수·구간길이로 분해능(resolution)과 분산(variance)이 트레이드오프. 편측/양측·표본주기 정규화를 모델·기준 동일하게.
- **해석 기준**: 모델/관측 PSD를 **log-log**로 겹쳐 그려 (1) 피크 위치(주기)와 (2) 에너지 레벨, (3) 기울기를 비교. 신뢰구간은 각 주파수 추정이 자유도 \(\nu\approx 2K\)의 카이제곱분포를 따른다는 사실로 구함(겹침·창함수에 따라 유효자유도 보정). 95% 구간(곱셈적: \(\nu\hat S/\chi^2_{0.975,\nu}\) ~ \(\nu\hat S/\chi^2_{0.025,\nu}\))이 겹치지 않으면 유의 차이.
- **한계·주의**: 창함수에 의한 스펙트럼 누설(leakage)·분해능 저하. 짧은 기록은 저주파 신뢰 낮음. 비정상 신호엔 부적합(→웨이블릿/EMD). 단위·정규화(예: dB, m²/Hz) 일치 필수. 앨리어싱 방지를 위해 표본주기보다 빠른 변동은 사전 저역통과.
- **출처**: Welch (1967) IEEE Trans. Audio Electroacoust. 15(2):70-73; Wilks, *Statistical Methods in the Atmospheric Sciences* (스펙트럼 분석 장); Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (PSD·신뢰구간 절).

---

### 멀티테이퍼 스펙트럼 (멀티테이퍼법 / Multitaper Method, Thomson)
- **무엇을 측정/검증하나**: PSD를 낮은 편향(low bias)·낮은 분산(low variance)으로 추정. 유색잡음(colored noise) 위에서 협대역(line) 성분(예: 조석·관성)을 통계적으로 검출.
- **정의·수식**: 직교하는 다수의 Slepian(DPSS) 테이퍼 \(v_k\)로 신호를 곱해 \(K\)개의 고유스펙트럼 \(\hat S_k(f)=|\sum_t v_k(t)x(t)e^{-i2\pi f t}|^2\)을 만들고 (적응)가중 평균. Thomson의 **harmonic F-test**로 순수 정현파 라인 유의성 검정.
- **적용 도메인/자료형**: 모든 도메인 **시계열**. 짧은 기록·유색배경에서 조석·관성·QBO 등 주기성분 식별에 강함.
- **입력·전제**: 등간격, 약정상성. 시간-대역폭곱 \(NW\)(보통 3~4)와 테이퍼수 \(K=2NW-1\) 선택이 분해능-분산 절충.
- **해석 기준**: Welch보다 안정적인 PSD. F-test 통계량이 임계값(예: \(1-1/N\) 분위) 초과 주파수에서 라인 성분 "유의". 모델/관측 라인의 진폭·주파수 일치 여부로 검증.
- **한계·주의**: \(NW\) 너무 크면 분해능 저하, 작으면 누설. 라인 검출은 정현파 가정. 계산비용 상대적으로 큼.
- **출처**: Thomson (1982) "Spectrum estimation and harmonic analysis," Proc. IEEE 70(9):1055-1096; Riedel & Sidorenko (1995) IEEE Trans. Signal Process. 43:188-195; Percival & Walden, *Spectral Analysis for Physical Applications* (1993); Di Matteo et al. (2021) JGR Space Physics 126:e2020JA028748 (멀티테이퍼 배경추정·신호검출).

---

### Lomb-Scargle 주기도 (롬-스카글 주기도 / Lomb-Scargle Periodogram)
- **무엇을 측정/검증하나**: **불규칙 표본·결측이 있는** 시계열의 스펙트럼/주기성. 관측소 자료처럼 결측·비등간격 기록과 모델을 같은 틀에서 비교.
- **정의·수식**: 각 시험주파수에서 정현파를 최소제곱 적합한 것과 등가인 주기도. 시간 오프셋 \(\tau\)를 도입해 위상 불변·통계적 성질 보장(Scargle 1982). 일반화 LS(GLS)는 부동평균(floating mean)·가중치를 포함.
- **적용 도메인/자료형**: 결측·불규칙 **시계열**(부이 결측, 위성 통과시각 불규칙). UTide의 불규칙 잔차 스펙트럼에도 사용.
- **입력·전제**: 시각 벡터와 값. 평균제거. 잡음이 백색이라는 가정 하 false-alarm 확률 계산.
- **해석 기준**: 피크의 false-alarm probability(FAP)로 유의성 판정(부트스트랩 또는 분석적). 모델과 관측 주기·상대강도 비교.
- **한계·주의**: 표본창(window)의 불규칙성이 가짜 피크(aliasing/spectral window) 유발 가능. 진폭 스케일 해석 주의. 불균일 표본의 유효 Nyquist 개념이 모호.
- **출처**: Lomb (1976) Astrophys. Space Sci. 39:447-462; Scargle (1982) ApJ 263:835-853; VanderPlas (2018) ApJS 236:16, "Understanding the Lomb-Scargle Periodogram."

---

### 스펙트럼 기울기·분광법칙 비교 (스펙트럼 기울기 / Spectral Slope, turbulence inertial range)
- **무엇을 측정/검증하나**: 스펙트럼의 거듭제곱 기울기를 비교해 모델이 **난류/지구물리 유체역학의 관성영역 법칙**을 재현하는지 검증(예: 에너지 캐스케이드 체제).
- **정의·수식**: \( S(k)\propto k^{-\alpha} \) 또는 \( S(f)\propto f^{-\beta} \). 대표 기울기: 3D 등방난류 \(k^{-5/3}\)(Kolmogorov), 2D/지균(QG) 역캐스케이드 에너지 \(k^{-5/3}\)·엔스트로피 \(k^{-3}\), SQG \(k^{-5/3}\)(표층) 등. 로그-로그 회귀로 \(\alpha\) 추정(적합대역·노이즈 바닥 명시).
- **적용 도메인/자료형**: 해류 KE 스펙트럼, SSH/SST **파수 스펙트럼**, 풍속·파랑 스펙트럼. 격자·시계열 모두.
- **입력·전제**: 충분한 관성영역(여러 데케이드의 파수/주파수), 노이즈 바닥(특히 위성 altimetry) 식별·제거. 디트렌드/테이퍼.
- **해석 기준**: 모델·관측 기울기를 같은 대역에서 회귀해 비교. 메소스케일 SSH는 관측상 \(k^{-2}\!\sim\!k^{-3}\)(QG \(k^{-5}\), SQG \(k^{-11/3}\)보다 완만)로 보고됨 — 모델이 너무 가파르거나 완만하면 분해능/소산 문제 시사.
- **한계·주의**: 위성/관측 노이즈 바닥이 고파수 기울기를 왜곡. 기울기는 캐스케이드 방향을 단정하지 못함(같은 \(k^{-5/3}\)가 정·역 캐스케이드 모두 가능 → 스펙트럼 에너지 플럭스로 보완). 적합대역 선택에 민감.
- **출처**: Kolmogorov (1941) Dokl. Akad. Nauk SSSR; Charney (1971) JAS 28:1087-1095 (지균난류); Scott & Wang (2005) JPO 35:1650-1666 (역캐스케이드 위성증거); Xu & Fu (2011, 2012) JPO (altimeter wavenumber slopes); Biri et al. (2016) JGR Oceans 121 (SSH·속도 스펙트럼).

---

### 파수 스펙트럼 (파수 스펙트럼 / Wavenumber Spectrum)
- **무엇을 측정/검증하나**: 격자장(SSH·SST·해류)의 **공간 변동 에너지가 공간규모(파장)별로 어떻게 분포**하는지. 모델의 유효분해능(effective resolution)·에디 에너지 분포 검증.
- **정의·수식**: 공간(1D 트랙 또는 2D)의 푸리에 변환 후 \( E(k)=|\hat\eta(k)|^2 \). 트랙 스펙트럼은 위성 따라가기(along-track) 데이터에서 계산, 2D는 등방화(azimuthal/radial average) 가능. 이방성(zonal vs meridional) 분리 분석도.
- **적용 도메인/자료형**: 해수면(altimetry SSH), 수온(SST), 해류(KE) **격자/트랙 자료**.
- **입력·전제**: 균질·등간격 공간 격자(또는 균일 트랙), 디트렌딩·테이퍼(공간 누설 억제), 육지/결측 마스킹 처리. 동일 파수 빈으로 모델·관측 정렬.
- **해석 기준**: 모델 스펙트럼이 고파수에서 관측보다 급락하면 분해능 부족/과도소산; 과대하면 격자잡음. "유효분해능"은 모델 스펙트럼이 기준에서 이탈하기 시작하는 파장으로 정의(보통 격자간격의 7~10배). zonal/meridional 기울기 차이로 이방성 진단.
- **한계·주의**: 위성 노이즈 바닥, 트랙 방향 이방성, 비균질성(연안)에서 해석 주의. 윈도·디트렌드 방식이 기울기에 영향. 격자보간 자료(L4)는 along-track보다 기울기가 가파르게 나옴(Wang et al. 2019).
- **출처**: Stammer (1997) JPO 27:1743-1769 (SSH 파수 스펙트럼); Xu & Fu (2012) JPO; Soufflet et al. (2016) Ocean Modelling 98:36-50 (모델 유효분해능); Wang, Qiao, Dai & Zhou (2019) Sci. Rep. 9:15896 (SSH 파수 스펙트럼 이방성, DOI:10.1038/s41598-019-52328-w).

---

### 파수-주파수 스펙트럼 (파수-주파수 스펙트럼 / Wavenumber-Frequency Spectrum, k-ω)
- **무엇을 측정/검증하나**: 변동 에너지를 (공간파수, 주파수) 평면에 분포시켜 **전파 방향·위상속도·분산관계**를 진단. 모델이 Rossby/Kelvin/관성중력파·조석 등 파동을 올바른 위상속도로 전파하는지 검증.
- **정의·수식**: 시공간장 \(x(s,t)\)의 2D 푸리에 변환 \( \hat X(k,\omega) \), 파워 \( |\hat X(k,\omega)|^2 \). 부호(+k,−k)·(+ω,−ω) 조합으로 전파 방향 구분. 분산곡선 \(\omega=\omega(k)\) 상의 에너지 집중으로 파동 식별(예: Wheeler-Kiladis 대류파 다이어그램; Hayashi 진행/후퇴파 분해).
- **적용 도메인/자료형**: SSH·SST·풍장·강수의 위경도-시간 단면(Hovmöller형) **격자자료**.
- **입력·전제**: 균일 시공간 격자, 대칭/비대칭 성분 분리(적도파), 배경 스펙트럼 제거(피크 강조). 동일 도메인·기간 정렬.
- **해석 기준**: 이론 분산곡선 위 에너지 집중 비교. 모델 위상속도가 관측과 어긋나면(곡선 이동) 평균류·성층 오차 시사. 배경 대비 신호비(signal-to-background)로 유의 피크 판정.
- **한계·주의**: 도메인 크기·기간이 저파수/저주파 분해능 제한. 비선형·도플러 천이 해석 주의. 배경 추정 방식(평활 횟수)이 피크 강조에 영향.
- **출처**: Hayashi (1971) J. Meteor. Soc. Japan 49:125-128 (진행/후퇴파 공간-시간 스펙트럼); Wheeler & Kiladis (1999) JAS 56:374-399 (convectively coupled waves); Hayashi (1982) GFDL space-time spectral methods.

---

### 회전 스펙트럼 (회전 스펙트럼 / Rotary Spectrum)
- **무엇을 측정/검증하나**: 해류·바람 같은 **2D 벡터 시계열**의 에너지를 **시계방향(CW)·반시계방향(CCW)** 회전성분으로 분해. 관성진동(북반구 CW)·조류 타원의 회전성을 모델이 재현하는지 검증.
- **정의·수식**: 복소속도 \(w(t)=u(t)+iv(t)\)의 푸리에 변환에서 양(+, CCW)·음(−, CW) 주파수 스펙트럼 \(S^+(f),S^-(f)\). 회전계수 \(r=(S^+-S^-)/(S^++S^-)\in[-1,1]\), 안정성·방위 등 회전 파라미터 산출(Gonella, Mooers).
- **적용 도메인/자료형**: 해류(ADCP·계류·표류부이), 바람 벡터 **시계열**.
- **입력·전제**: \(u,v\) 동시 등간격 시계열, 평균/추세 제거. 관성주파수 \(f=2\Omega\sin\phi\) 식별을 위해 위도 정보. 좌표계(동-북) 일관성 필수.
- **해석 기준**: 북반구 관성주파수 부근 **CW(음의 주파수) 피크** 우세가 정상(남반구는 CCW). 모델/관측의 CW·CCW 에너지 비, 관성/조류 피크 위치·세기 비교. 타원 회전성·이심률 일치 검증.
- **한계·주의**: 짧은 기록은 관성/조석 분해 어려움. 비등방·비정상 흐름에서 단일 스펙트럼 해석 한계. 좌표계 회전 오류 시 CW/CCW가 통째로 뒤바뀜.
- **출처**: Gonella (1972) Deep-Sea Res. 19:833-846; Mooers (1973) Deep-Sea Res. 20:1129-1141; Emery & Thomson, *Data Analysis Methods in Physical Oceanography* (회전 스펙트럼 절).

---

### 조화·조석 분해 (조화분해/조석분석 / Harmonic & Tidal Analysis — T_TIDE, UTide)
- **무엇을 측정/검증하나**: 조위·조류 시계열을 천문 조석 **분조(constituents: M2, S2, K1, O1 …)** 의 진폭·위상으로 분해. 모델의 조석 진폭·위상·조류 타원이 관측/검조소와 맞는지 검증.
- **정의·수식**: \( x(t)=a_0+\sum_k f_k a_k \cos(\sigma_k t + (V_k+u_k) - g_k) \) 형태의 최소제곱 적합. \(\sigma_k\) 알려진 분조 각진동수, \(f_k,u_k\) 절점보정(nodal/satellite correction). 결과: 분조별 진폭 \(H_k\)·위상지연(Greenwich phase lag) \(g_k\). 조류는 복소/타원(장·단반경, 경사, 회전) 형태.
- **적용 도메인/자료형**: 조위(스칼라)·조류(벡터) **시계열**. 검조소·ADCP·모델 출력.
- **입력·전제**: 충분한 기록길이(분조 분리는 Rayleigh 기준 \(\Delta\sigma \cdot T>1\); 예 M2/S2 분리에 약 14.7일 이상, K1/P1·S2/K2 분리에 약 182.6일). UTide는 결측·불규칙·다년 기록·절점보정을 통합 처리.
- **해석 기준**: 분조별 진폭·위상 오차, 복소 RMS 차이(vector difference), "예측 잔차 표준편차" 비교. 신뢰구간(UTide: 잔차 스펙트럼 기반 또는 백색잡음 가정, 선형화 또는 몬테카를로)으로 유의 분조 판정. 조류는 타원 파라미터 비교. 표준 종합지표로 진폭·위상을 합친 **복소 RMSE**(또는 RSS) 사용.
- **한계·주의**: 짧거나 결측 많은 기록은 분조 혼선(aliasing). 천해 비선형 분조(M4, MS4 등) 다수 필요. 시간기준(UTC)·위상기준(Greenwich vs local) 일치 필수. 표층/비조석 잔차(폭풍해일)는 별도. 위성 통과주기에 의한 조석 앨리어싱 주의.
- **출처**: Pawlowicz, Beardsley & Lentz (2002) "Classical tidal harmonic analysis ... T_TIDE," Computers & Geosciences 28:929-937; Codiga (2011) "Unified Tidal Analysis and Prediction Using the UTide Matlab Functions," GSO Tech. Report 2011-01 (URI); Foreman et al. (2009) Atmosphere-Ocean 47:191-200; Leffler & Jay (2009) Cont. Shelf Res. 29:78-88.

---

### 교차스펙트럼·코히어런스 (교차스펙트럼/제곱코히어런스 / Cross-Spectrum & Magnitude-Squared Coherence)
- **무엇을 측정/검증하나**: 두 시계열(예: 모델 vs 관측, 또는 바람 vs 해류)이 **주파수별로 얼마나 선형적으로 결합**돼 있고(coherence), 어느 정도 **위상차(lead/lag)** 를 갖는지. 주파수대별 일치도 검증.
- **정의·수식**: 교차스펙트럼 \( S_{xy}(f)=\langle\hat X(f)\hat Y^*(f)\rangle\)(앙상블/세그먼트 평균). 제곱코히어런스 \( \gamma^2(f)=\dfrac{|S_{xy}(f)|^2}{S_{xx}(f)S_{yy}(f)}\in[0,1] \). 위상 \( \phi(f)=\arg S_{xy}(f) \).
- **적용 도메인/자료형**: 두 **시계열**(또는 격자점쌍). 대기-해양 결합, 강제력-반응 관계.
- **입력·전제**: 등간격·동기화(공통 시각). 평활(세그먼트 평균/주파수 평활)이 있어야 코히어런스가 1로 포화되지 않음. 정상성.
- **해석 기준**: 코히어런스가 유의수준(자유도에 따른 임계값 \( \gamma^2_{crit}=1-\alpha^{1/(n-1)} \), 또는 위상 무작위화 surrogate로 얻은 null) 초과 주파수에서 "유의 결합". 위상은 유의 코히어런스 구간에서만 해석. 모델이 관측-강제력 결합 주파수/위상을 재현하는지 본다.
- **한계·주의**: 평활 자유도와 코히어런스 편향(bias) 트레이드오프. 짧은 기록은 과대추정. 비선형 결합은 선형 코히어런스로 포착 불가(→바이스펙트럼).
- **출처**: Jenkins & Watts (1968) *Spectral Analysis and Its Applications*, Holden-Day; Bendat & Piersol, *Random Data* (코히어런스·신뢰구간); Emery & Thomson, *Data Analysis Methods in Physical Oceanography*.

---

### 고차 스펙트럼·바이스펙트럼 (고차 스펙트럼/바이스펙트럼 / Higher-Order Spectra & Bispectrum)
- **무엇을 측정/검증하나**: 세 주파수 사이의 **위상결합(phase coupling) — 비선형 3파 상호작용**(triad interaction)을 검출. 일반 PSD(2차)는 위상정보를 버리지만 바이스펙트럼은 보존하므로, 모델이 비선형 에너지 전달(예: 천해 파랑의 고조파 생성, 비선형 조석)의 위상결합을 재현하는지 검증.
- **정의·수식**: 바이스펙트럼 \( B(f_1,f_2)=\langle \hat X(f_1)\hat X(f_2)\hat X^*(f_1+f_2)\rangle \). 정규화한 **바이코히어런스** \( b^2(f_1,f_2)=\dfrac{|B(f_1,f_2)|^2}{\langle|\hat X(f_1)\hat X(f_2)|^2\rangle\,\langle|\hat X(f_1+f_2)|^2\rangle}\in[0,1] \)로 결합 강도, \(\arg B\)로 바이위상(biphase). 가우시안·선형 과정이면 0.
- **적용 도메인/자료형**: 파랑(파고·압력) **시계열**, 천해 변형·고조파, 비선형 조석, 난류·플라즈마. 격자는 격자점/영역 시계열.
- **입력·전제**: 등간격, 약정상성, 충분한 앙상블/세그먼트(분산↓). 평균제거. 추정 분산이 커서 많은 세그먼트 필요.
- **해석 기준**: 바이코히어런스가 유의수준(세그먼트 수에 따른 임계, 또는 surrogate) 초과한 \((f_1,f_2)\)에서 비선형 결합 "유의". 모델-관측 바이코히어런스 패턴·바이위상 비교로 비선형 과정 재현도 평가.
- **한계·주의**: 추정 분산이 크고 세그먼트 많이 필요. 정상성·약비선형 가정. 해석(어느 삼중자가 물리적인가)이 까다로움. 2차 통계로 안 보이는 결함을 드러내는 보완지표로 활용.
- **출처**: Mendel (1991) "Tutorial on higher-order statistics (spectra) ...," Proc. IEEE 79(3):278-305; Elgar & Guza (1985) JFM; Elgar (1995) "Higher-order spectral analysis of nonlinear ocean surface gravity waves," JGR Oceans 100:C8 (DOI:10.1029/94JC02900); Nikias & Petropulu, *Higher-Order Spectra Analysis* (1993).

---

### 웨이블릿 변환 (연속웨이블릿변환 / Continuous Wavelet Transform — Torrence & Compo)
- **무엇을 측정/검증하나**: **비정상(non-stationary)** 시계열의 변동 에너지를 시간-주파수(스케일) 평면에 분해. 모델이 ENSO·계절성·간헐적 진동의 **시간적 변조(시작·강도·소멸)** 를 재현하는지 검증.
- **정의·수식**: \( W_n(s)=\sum_{n'} x_{n'}\,\psi^*\!\big[\frac{(n'-n)\delta t}{s}\big] \). 보통 복소 Morlet \( \psi_0(\eta)=\pi^{-1/4}e^{i\omega_0\eta}e^{-\eta^2/2} \). 웨이블릿 파워 \(|W_n(s)|^2\). 시간평균=글로벌 웨이블릿 스펙트럼.
- **적용 도메인/자료형**: 모든 도메인 **시계열**(조위·SST·풍속·파고). 격자는 격자점/영역평균 시계열.
- **입력·전제**: 등간격, 평균제거. 영향원뿔(Cone of Influence, COI) 밖 가장자리 결과는 신뢰 낮음. 배경 잡음모형(백색/적색 AR(1)) 가정으로 유의성 검정.
- **해석 기준**: 적색잡음 대비 95% 유의 파워 영역을 모델·관측에서 비교. COI 내부는 해석 배제. 글로벌 웨이블릿 스펙트럼은 평활 PSD로 비교 가능.
- **한계·주의**: 스케일-주파수 변환 상수(예: Morlet \(\omega_0=6\)이면 Fourier주기≈1.03 s) 주의. 시간·주파수 분해능 동시 향상 불가(불확정성). 가장자리 효과·정규화 일관성.
- **출처**: Torrence & Compo (1998) "A Practical Guide to Wavelet Analysis," Bull. Amer. Meteor. Soc. 79:61-78; Daubechies (1992) *Ten Lectures on Wavelets*, SIAM.

---

### 교차웨이블릿·웨이블릿 코히어런스 (교차웨이블릿/웨이블릿코히어런스 / Cross-Wavelet Transform & Wavelet Coherence)
- **무엇을 측정/검증하나**: 두 시계열의 **공통 파워가 큰 시간-주파수 영역(XWT)** 과, 파워와 무관히 **국소적으로 선형결합·위상관계가 일정한 영역(WTC)**. 모델-관측 또는 강제력-반응의 시간 가변 결합 검증.
- **정의·수식**: 교차웨이블릿 \( W^{XY}=W^X W^{Y*} \), 파워 \(|W^{XY}|\), 위상 \(\arg W^{XY}\)(화살표로 표시). 웨이블릿 코히어런스 \( R^2=\dfrac{|S(s^{-1}W^{XY})|^2}{S(s^{-1}|W^X|^2)\,S(s^{-1}|W^Y|^2)} \), \(S\)는 평활연산자.
- **적용 도메인/자료형**: 두 **시계열**(대기-해양, 강 유량-강수 등).
- **입력·전제**: 동기 등간격, 평균제거. 평활(시간·스케일)이 코히어런스 정의에 필수. COI·몬테카를로 유의성.
- **해석 기준**: WTC가 유의(몬테카를로 surrogate 대비)한 시간-주파수대에서 위상화살표로 lead/lag 진단. 모델이 관측의 결합 시기·주기·위상을 재현하는지 비교.
- **한계·주의**: WTC는 파워가 작아도 1에 가까울 수 있어 단독해석 위험(XWT와 함께 봄). 평활·surrogate 설정 의존.
- **출처**: Grinsted, Moore & Jevrejeva (2004) "Application of the cross wavelet transform and wavelet coherence to geophysical time series," Nonlin. Processes Geophys. 11:561-566; Torrence & Webster (1999) J. Climate 12:2679-2690.

---

### 경험모드분해·힐버트-황 변환 (경험모드분해/EEMD/힐버트-황변환 / Empirical Mode Decomposition, EEMD, Hilbert-Huang Transform)
- **무엇을 측정/검증하나**: **비선형·비정상** 시계열을 데이터 적응형으로 유한개의 **내재모드함수(IMF)** 로 분해하고, 각 IMF의 Hilbert 변환으로 **순간주파수·순간진폭**을 얻어 시간-주파수(Hilbert) 스펙트럼을 구성. 모델이 추세·계절성·간헐적 진동의 비정상 변조를 관측처럼 재현하는지 검증. FFT/웨이블릿과 달리 사전 기저(basis)를 가정하지 않음.
- **정의·수식**: 시프팅(sifting)으로 극값 포락선의 평균을 반복 제거해 IMF \(c_j(t)\) 추출, \( x(t)=\sum_j c_j(t)+r(t) \)(\(r\)=잔차/추세). 각 IMF에 Hilbert 변환 → 해석신호 \(c_j+i\mathcal H[c_j]=a_j(t)e^{i\theta_j(t)}\), 순간주파수 \( \omega_j=d\theta_j/dt \). **EEMD**(앙상블 EMD): 백색잡음을 더한 앙상블 평균으로 모드혼합(mode mixing) 완화.
- **적용 도메인/자료형**: 모든 도메인 **시계열**(조위·SST·해수면 추세·풍속·파고). 격자는 격자점/영역평균 시계열.
- **입력·전제**: 등간격 권장(가장자리 처리 주의). 잡음진폭·앙상블 크기(EEMD), 종료기준(stopping criterion) 선택. 결측은 사전 보간 또는 회피.
- **해석 기준**: IMF별 주기·에너지·순간주파수 분포를 모델·관측 비교. 추세 잔차 \(r(t)\)로 비선형 추세 비교. 유의성은 적색잡음 IMF 에너지 분포(Wu & Huang 2004) 또는 surrogate로 판정.
- **한계·주의**: 모드혼합·종단효과·정지기준 의존(알고리즘 비유일성). 수학적 직교성·완비성 보장 약함. 순간주파수가 음수/요동칠 수 있어 협대역 IMF에서만 신뢰. 비교 시 동일 파라미터(잡음·앙상블) 사용 필수.
- **출처**: Huang et al. (1998) "The empirical mode decomposition and the Hilbert spectrum ...," Proc. R. Soc. Lond. A 454:903-995; Wu & Huang (2009) "Ensemble Empirical Mode Decomposition," Adv. Adaptive Data Anal. 1:1-41; Wu & Huang (2004) Proc. R. Soc. Lond. A (백색잡음 유의성).

---

### EOF/PCA (경험직교함수/주성분분석 / Empirical Orthogonal Function, Principal Component Analysis)
- **무엇을 측정/검증하나**: 시공간 격자장의 변동을 **분산 최대 순서의 직교 공간패턴(EOF)과 시간계수(PC)** 로 분해. 모델의 지배 변동모드(공간패턴·설명분산·시간거동)가 재분석/관측과 일치하는지 검증.
- **정의·수식**: 이상치(anomaly) 행렬 \(X\)(시간×공간)의 공분산 \(C=\frac{1}{N}X^TX\) 고유분해 \(C e_k=\lambda_k e_k\). \(e_k\)=EOF(공간패턴), 투영 \(a_k=Xe_k\)=PC(시간), \(\lambda_k/\sum\lambda\)=설명분산비. SVD로도 계산.
- **적용 도메인/자료형**: 모든 도메인의 **격자장**(SST·SSH·풍장·수온단면). 위경도 면적가중 필요.
- **입력·전제**: 평균/추세 제거(이상치), 면적가중(\(\sqrt{\cos\phi}\)), 결측 처리. 동일 도메인·격자·기간으로 모델·관측 정렬.
- **해석 기준**: (1) 모드별 설명분산비 비교, (2) 공간패턴 상관(패턴 상관계수)·부호 정합(부호는 임의이므로 정렬), (3) PC 시계열 상관. **North et al. 규칙**으로 인접 고유값이 표본오차 \( \delta\lambda\approx\lambda\sqrt{2/N^*} \)(\(N^*\)=유효 표본수) 내면 모드가 잘 분리되지 않아(혼합) 패턴 해석 주의. 모델 PC를 관측 EOF에 투영해 비교(공통기저)하기도.
- **한계·주의**: 직교성 강제로 물리적 분리 보장 안 됨(→회전 EOF). 정상파만 잡고 전파파동 못 잡음(→CEOF). 부호·순서·축퇴(degeneracy) 모호성. 도메인 의존성(같은 모드도 영역 바꾸면 달라짐).
- **출처**: Lorenz (1956) MIT Sci. Rep. No.1 (원개념); North, Bell, Cahalan & Moeng (1982) Mon. Wea. Rev. 110:699-706 (rule of thumb); Preisendorfer (1988) *Principal Component Analysis in Meteorology and Oceanography*; Hannachi, Jolliffe & Stephenson (2007) Int. J. Climatol. 27:1119-1152 (리뷰).

---

### 회전 EOF (회전 경험직교함수 / Rotated EOF, VARIMAX)
- **무엇을 측정/검증하나**: 표준 EOF의 직교·전역 패턴을 **회전(예: VARIMAX)** 해 더 국소적·물리적으로 해석 가능한 모드로 변환. 모델과 관측의 "물리적 변동중심"이 일치하는지 더 견고히 비교.
- **정의·수식**: 상위 \(M\)개 EOF를 모아 회전행렬 \(R\)로 \(\tilde E=ER\) (직교회전 VARIMAX 또는 사교회전 PROMAX). 단순구조(simple structure) 기준 최대화.
- **적용 도메인/자료형**: 격자장 EOF 후처리. SST·SLP·해류 패턴.
- **입력·전제**: 회전할 모드 수 \(M\) 선택(절단). 면적가중·표준화 여부가 결과에 영향.
- **해석 기준**: 회전 후 패턴이 국소화되어 모델-관측 패턴상관 비교가 직관적. 모드수·정규화 선택의 민감도 점검 필요.
- **한계·주의**: 모드수·정규화·회전법에 따라 결과 달라짐(비유일). 전역 텔레커넥션은 오히려 흐려질 수 있음.
- **출처**: Richman (1986) "Rotation of principal components," J. Climatol. 6:293-335; Kaiser (1958) "The varimax criterion ...," Psychometrika 23:187-200; UCAR Climate Data Guide, EOF & Rotated EOF (회색문헌, URL 확인).

---

### 복소/Hilbert EOF (복소/힐버트 경험직교함수 / Complex (Hilbert) EOF, CEOF)
- **무엇을 측정/검증하나**: 실수장을 Hilbert 변환으로 복소화해 **전파성(propagating)·정재(standing) 변동을 진폭·위상으로** 분해. 모델이 전파 신호(예: MJO, 연안 켈빈파, 전파성 SST 이상)의 위상속도·전파방향을 재현하는지 검증.
- **정의·수식**: \( X_H(t)=X(t)+i\,\mathcal H[X(t)] \). 복소 공분산 \( C=\langle X_H X_H^\dagger\rangle \)의 고유분해. 각 모드는 공간 진폭·공간 위상·시간 진폭·시간 위상 4성분 제공(공간 위상 기울기=전파).
- **적용 도메인/자료형**: 전파·진동 신호가 있는 **격자장 시계열**(적도 SST, 파동장).
- **입력·전제**: 이상치·디트렌드. Hilbert 변환의 가장자리 효과 주의(테이퍼/패딩). 좁은 대역 신호일수록 위상 해석 명확.
- **해석 기준**: 공간 위상의 진행으로 전파방향·속도 추정 → 모델 vs 관측 비교. 모드 설명분산·진폭패턴 비교.
- **한계·주의**: 광대역 신호에선 위상 해석 모호. 가장자리 왜곡. 모드 분리·해석 난도 높음.
- **출처**: Horel (1984) "Complex principal component analysis: Theory and examples," J. Climate Appl. Meteor. 23:1660-1673; Rasmusson, Arkin, Chen & Jalickee (1981) Mon. Wea. Rev. 109:587-598 (CEOF 적용); Hannachi et al. (2007) 리뷰; Navarra & Simoncini, *A Guide to EOF Analysis* (교과서).

---

### 확장 EOF / 다채널 SSA (확장 경험직교함수 / Extended EOF, M-SSA)
- **무엇을 측정/검증하나**: 공간뿐 아니라 **시간지연(lag)을 변수에 포함**해 시공간 결합·전파·진동 구조를 추출. 모델이 전파패턴·진동의 시공간 구조를 재현하는지 검증.
- **정의·수식**: 각 격자점의 \(L\)개 시간지연 사본을 변수로 확장한 행렬에 EOF/PCA. 단일지점이면 SSA, 다지점이면 M-SSA. EEOF는 M-SSA와 수학적으로 등가.
- **적용 도메인/자료형**: 전파·진동 **격자장 시계열**. 계절전이·파동·텔레커넥션.
- **입력·전제**: 지연창 길이 \(L\) 선택(분해할 주기보다 길게). 이상치·정규화. 차원 급증(공간×\(L\))으로 계산비용·표본수 고려.
- **해석 기준**: 위상이 진행하는 EEOF 쌍(서로 직교·90° 위상)으로 전파모드 식별 → 모델/관측 전파주기·속도 비교.
- **한계·주의**: \(L\)·정규화 민감. 표본 대비 변수 과다 시 과적합. 해석 복잡.
- **출처**: Weare & Nasstrom (1982) Mon. Wea. Rev. 110:481-485; Plaut & Vautard (1994) JAS 51:210-236; Hannachi et al. (2007) 리뷰.

---

### 특이스펙트럼분석 SSA / 몬테카를로 SSA (특이스펙트럼분석 / Singular Spectrum Analysis, MC-SSA)
- **무엇을 측정/검증하나**: 단일(또는 다변량) 시계열을 **데이터 적응형 필터**로 추세·진동·잡음 성분으로 분해. 모델·관측 각각에서 추세/준주기 진동(예: 경년·십년 변동)을 추출해 비교, 유색잡음 위 진동의 유의성 검정.
- **정의·수식**: 지연창 \(M\)으로 궤적행렬(trajectory matrix) 구성→그 공분산(또는 \(M\times M\) Toeplitz)의 고유분해→T-EOF/T-PC, 재구성성분(RC). 한 쌍의 인접 고유값+위상 90° EOF가 진동쌍. **MC-SSA**: AR(1) 적색잡음 surrogate로 고유값 분포를 만들어 유의 초과 모드 판정.
- **적용 도메인/자료형**: **시계열**(조위·SST지수·NAO/ENSO지수). 격자는 M-SSA.
- **입력·전제**: 창길이 \(M\)(보통 \(N/3\) 이하), 평균제거. 적색잡음 귀무가설 설정.
- **해석 기준**: RC로 추세·진동 분리해 모델·관측 비교. MC-SSA에서 surrogate 95% 상한 초과 고유값=유의 진동. 진동쌍의 주기·진폭 비교.
- **한계·주의**: 창길이 의존. 짧은 기록의 가짜 진동 위험(→MC-SSA 필수). 모드 혼합·분리 모호.
- **출처**: Vautard & Ghil (1989) Physica D 35:395-424; Ghil et al. (2002) "Advanced spectral methods for climatic time series," Rev. Geophys. 40(1):1003; Allen & Smith (1996) J. Climate 9:3373-3404 (MC-SSA).

---

### SVD / 최대공분산분석 MCA (특이값분해/최대공분산분석 / SVD analysis, Maximum Covariance Analysis)
- **무엇을 측정/검증하나**: **두 개의 서로 다른 장(field)** 사이의 결합 변동모드를 교차공분산에서 추출(예: SST↔풍장, SLP↔강수). 모델이 두 변수 간 결합 구조를 재현하는지 검증.
- **정의·수식**: 두 이상치장 \(X(\text{time}\times p),Y(\text{time}\times q)\)의 교차공분산 \( C_{XY}=\frac{1}{N}X^TY \)를 SVD: \( C_{XY}=U\Sigma V^T \). \(u_k,v_k\)=좌·우 특이벡터(각 장의 결합패턴), 시간계수(expansion coefficients)=장의 투영. **제곱공분산비(SCF)** \( = \sigma_k^2/\sum_j\sigma_j^2 \).
- **적용 도메인/자료형**: 두 **격자장 시계열**(대기-해양 결합 진단에 표준).
- **입력·전제**: 동일 시간표본, 이상치·면적가중. 두 장 정렬·동기화.
- **해석 기준**: 모드별 SCF(결합 기여), 두 expansion coefficient의 시간상관(결합 강도), 좌·우 패턴의 모델-관측 패턴상관을 비교. 상위 모드 SCF가 크고 시간상관 높으면 강한 결합.
- **한계·주의**: SVD/MCA는 결합이 인과를 의미하지 않음. CCA·CPCA 등 대체기법과 결과 다를 수 있음. 모드 직교성 강제. 표본수<<공간차원 시 과적합(정규화/사전 PCA 절단 권장).
- **출처**: Bretherton, Smith & Wallace (1992) "An intercomparison of methods for finding coupled patterns in climate data," J. Climate 5:541-560; Wallace, Smith & Bretherton (1992) J. Climate 5:561-576; Cherry (1996) J. Climate 9:2003-2009; von Storch & Zwiers (1999) *Statistical Analysis in Climate Research*.

---

### 정준상관분석 CCA (정준상관분석 / Canonical Correlation Analysis)
- **무엇을 측정/검증하나**: 두 장의 **상관(분산 정규화)이 최대가 되는 선형결합 쌍**을 찾음. MCA가 공분산을 최대화한다면 CCA는 상관을 최대화. 결합 변동의 통계적 예측·진단에 사용.
- **정의·수식**: \( \max \mathrm{corr}(Xa, Yb) \). 보통 각 장을 PCA로 사전 절단(차원·노이즈 억제) 후 \( \Sigma_{xx}^{-1/2}\Sigma_{xy}\Sigma_{yy}^{-1/2} \)의 SVD로 정준상관·패턴 산출.
- **적용 도메인/자료형**: 두 **격자장 시계열**(예측인자-예측대상). 계절예측 진단.
- **입력·전제**: 이상치·면적가중, **PCA 사전 절단 필수**(역행렬 안정화). 동기 시간표본.
- **해석 기준**: 정준상관계수·패턴쌍을 모델-관측 비교. 상관이 분산 정규화돼 작은 분산모드가 과대평가될 수 있어 절단수 민감도 점검.
- **한계·주의**: 사전 PCA 절단수에 민감(과적합/과소). 작은 분산축의 허위 고상관 위험. 해석은 신중.
- **출처**: Hotelling (1936) Biometrika 28:321-377; Barnett & Preisendorfer (1987) Mon. Wea. Rev. 115:1825-1850; Bretherton, Smith & Wallace (1992) J. Climate (비교); von Storch & Zwiers (1999).

---

### 고유직교분해 POD / snapshot POD (고유직교분해 / Proper Orthogonal Decomposition, snapshot POD)
- **무엇을 측정/검증하나**: 유동·물리장의 변동을 **에너지(분산) 최적 순서의 직교 공간모드**로 분해. 수학적으로 EOF/PCA와 동일하나, 유체역학 전통(Lumley POD)·**snapshot 방법**(Sirovich)으로 고차원 격자장에 효율적으로 적용. 모델·관측의 지배 결맞은(coherent) 구조·에너지 분포 비교.
- **정의·수식**: 스냅샷 앙상블 \(\{u(\cdot,t_i)\}\)에서 2점 상관 \(R\)의 고유분해 \( R\phi_k=\lambda_k\phi_k \). \(\phi_k\)=POD 모드(공간), \(\lambda_k\)=모드 에너지, 시간계수 \(a_k(t)=\langle u,\phi_k\rangle\). **snapshot POD**: 공간차원≫시간표본일 때 \(N\times N\)(시간) 행렬 고유분해로 등가 계산.
- **적용 도메인/자료형**: 고해상 **격자장**(유속·압력·SSH·SST), 실험/모델 스냅샷. 정상·비정상 모두(시간평균 의미는 정상 가정에서 명확).
- **입력·전제**: 평균제거, 적절한 내적(에너지 노름; 면적/체적 가중). 충분한 스냅샷. 모델·관측 동일 격자·가중.
- **해석 기준**: 모드별 에너지비·누적에너지(few-mode 재구성 비율), 공간모드 패턴상관, 시간계수 스펙트럼/상관을 모델-관측 비교. 소수 모드로 큰 에너지를 설명하면 결맞은 구조 지배.
- **한계·주의**: EOF와 같은 한계(직교 강제, 전파파동은 단일모드로 안 잡힘 → SPOD/DMD). 정상성 가정 시 시간평균 해석 타당. 노름 선택이 모드를 바꿈.
- **출처**: Lumley (1970) *Stochastic Tools in Turbulence*, Academic Press; Sirovich (1987) "Turbulence and the dynamics of coherent structures," Q. Appl. Math. 45:561-590 (snapshot 방법); Berkooz, Holmes & Lumley (1993) Annu. Rev. Fluid Mech. 25:539-575 (리뷰).

---

### 스펙트럼 POD (스펙트럼 고유직교분해 / Spectral Proper Orthogonal Decomposition, SPOD)
- **무엇을 측정/검증하나**: 주파수별로 **시공간적으로 결맞은(coherent), 통계적으로 최적인 변동구조**를 추출. 정상 난류/유동에서 지배적 시공간 모드(예: 진동·전파 구조)를 주파수별로 식별해 모델-관측 비교.
- **정의·수식**: 시계열 앙상블의 교차스펙트럼밀도(CSD) 행렬 \(S(f)\)를 각 주파수에서 고유분해 \( S(f)\phi_k(f)=\lambda_k(f)\phi_k(f) \). \(\phi_k(f)\)=주파수 \(f\)의 SPOD 모드, \(\lambda_k(f)\)=모드 에너지. Welch식 세그먼트로 CSD 추정.
- **적용 도메인/자료형**: 시간해상 **격자장**(고빈도 모델 출력, 유속·압력장). 통계적 정상성 가정 유동.
- **입력·전제**: 정상성, 충분한 시간표본·앙상블(세그먼트). 세그먼트 길이·중첩·창함수 선택.
- **해석 기준**: 주파수별 선두모드 에너지 \(\lambda_1(f)\) 스펙트럼·공간구조를 모델-관측 비교. 결맞은 구조의 주파수·공간형태 일치 여부.
- **한계·주의**: 표준 (공간)POD와 달리 정상성 전제·다세그먼트 필요. 데이터·계산량 큼. 비정상 유동엔 부적합.
- **출처**: Towne, Schmidt & Colonius (2018) "Spectral proper orthogonal decomposition and its relationship to DMD and resolvent analysis," J. Fluid Mech. 847:821-867; Lumley (1970) *Stochastic Tools in Turbulence*; Schmidt & Colonius (2020) AIAA J. 58:1023-1033 (가이드).

---

### 동역학모드분해 DMD (동역학모드분해 / Dynamic Mode Decomposition)
- **무엇을 측정/검증하나**: 스냅샷 시계열에서 **각 모드가 고유한 (복소) 진동수와 성장/감쇠율을 갖는 데이터 구동 모드**를 추출(준선형 동역학 근사, Koopman 연산자 근사). 모델이 변동의 진동주기와 안정성(증폭/감쇠)을 관측처럼 재현하는지 검증. POD/EOF가 에너지 순으로 정렬한다면 DMD는 동역학(시간거동) 순으로 분리.
- **정의·수식**: 스냅샷 행렬 \(X=[x_1..x_{m-1}]\), \(X'=[x_2..x_m]\)에 대해 선형사상 \(X'\approx A X\)를 가정, \(A\)의 고유값·고유벡터를 (POD 절단 후) 추정. 각 DMD 모드 \(\phi_k\)의 고유값 \(\mu_k=e^{(\sigma_k+i\omega_k)\Delta t}\) → 진동수 \(\omega_k\), 성장률 \(\sigma_k\). 변형: exact DMD, optimized DMD, **multi-resolution DMD**(비정상).
- **적용 도메인/자료형**: 시간해상 **격자장**(유속·SSH·SST·압력), 등시간 간격 스냅샷.
- **입력·전제**: 균일 \(\Delta t\) 등시간 스냅샷, 평균제거 권장. POD 절단으로 랭크·노이즈 제어. 충분한 스냅샷(모드수보다 많이).
- **해석 기준**: DMD 스펙트럼(진동수-성장률 평면)에서 모드 주파수·감쇠율·공간패턴을 모델-관측 비교. 중립(σ≈0) 모드의 주기·패턴 일치 여부, 불안정 모드의 유무.
- **한계·주의**: 노이즈·짧은 기록에 민감(성장률 편향). 강한 비선형/비정상엔 단일 선형근사 부적절(→mrDMD/Hankel-DMD). 모드 정규화·진폭 정의가 구현마다 달라 비교 시 동일 알고리즘 사용.
- **출처**: Schmid (2010) "Dynamic mode decomposition of numerical and experimental data," J. Fluid Mech. 656:5-28 (DOI:10.1017/S0022112010001217); Rowley et al. (2009) JFM 641:115-127 (Koopman 관점); Kutz, Brunton, Brunton & Proctor (2016) *Dynamic Mode Decomposition*, SIAM; Tu et al. (2014) J. Comput. Dyn. 1:391-421 (exact DMD).

---

### 테일러 다이어그램 (모드·재구성장 비교 보조) (테일러 다이어그램 / Taylor Diagram for modal/spectral fields)
- **무엇을 측정/검증하나**: EOF 재구성장·PC 시계열·스펙트럼 적합 결과 등을 **표준편차·패턴상관·중심화 RMS차** 로 한 그림에 종합. 여러 모델/구성의 모드 재현도를 한눈에 비교.
- **정의·수식**: 기하관계 \( E'^2 = \sigma_f^2+\sigma_r^2-2\sigma_f\sigma_r R \). 반경=표준편차, 방위각=상관 \(R\), 기준점까지 거리=중심화 RMS차 \(E'\).
- **적용 도메인/자료형**: 격자장·시계열 모두. 본 카탈로그에선 PC 시계열, 특정 EOF로 재구성한 장, 스펙트럼 적합 잔차 비교 등에 보조적으로 활용.
- **입력·전제**: 공통 기준자료, 동일 정규화·면적가중·기간. 비교대상 정렬.
- **해석 기준**: 기준점에 가까울수록(상관↑, RMS차↓, 표준편차 일치) 우수. 여러 모델 산점으로 상대평가.
- **한계·주의**: 평균편차(bias)는 표시 안 됨(중심화 통계). 단일 그림이 모든 결함을 보여주지 않음.
- **출처**: Taylor (2001) "Summarizing multiple aspects of model performance in a single diagram," J. Geophys. Res. 106:7183-7192.

---

## 출처(References)

- Allen, M.R. & Smith, L.A. (1996). Monte Carlo SSA: Detecting irregular oscillations in the presence of colored noise. *Journal of Climate*, 9, 3373-3404.
- Barnett, T.P. & Preisendorfer, R. (1987). Origins and levels of monthly and seasonal forecast skill ... using canonical correlation analysis. *Monthly Weather Review*, 115, 1825-1850.
- Bendat, J.S. & Piersol, A.G. *Random Data: Analysis and Measurement Procedures*. Wiley.
- Berkooz, G., Holmes, P. & Lumley, J.L. (1993). The proper orthogonal decomposition in the analysis of turbulent flows. *Annual Review of Fluid Mechanics*, 25, 539-575.
- Biri, S. et al. (2016). Atlantic sea surface height and velocity spectra inferred from satellite altimetry and a hierarchy of numerical simulations. *Journal of Geophysical Research: Oceans*, 121.
- Bretherton, C.S., Smith, C. & Wallace, J.M. (1992). An intercomparison of methods for finding coupled patterns in climate data. *Journal of Climate*, 5, 541-560.
- Charney, J.G. (1971). Geostrophic turbulence. *Journal of the Atmospheric Sciences*, 28, 1087-1095.
- Cherry, S. (1996). Singular value decomposition analysis and canonical correlation analysis. *Journal of Climate*, 9, 2003-2009.
- Codiga, D.L. (2011). *Unified Tidal Analysis and Prediction Using the UTide Matlab Functions*. Technical Report 2011-01, Graduate School of Oceanography, University of Rhode Island. (https://www.po.gso.uri.edu/~codiga/utide/utide.htm)
- Daubechies, I. (1992). *Ten Lectures on Wavelets*. SIAM.
- Di Matteo, S. et al. (2021). Power spectral density background estimate and signal detection via the multitaper method. *Journal of Geophysical Research: Space Physics*, 126, e2020JA028748.
- Elgar, S. & Guza, R.T. (1985). Observations of bispectra of shoaling surface gravity waves. *Journal of Fluid Mechanics*, 161, 425-448.
- Elgar, S. (1995). Higher-order spectral analysis of nonlinear ocean surface gravity waves. *Journal of Geophysical Research: Oceans*, 100(C8). (DOI:10.1029/94JC02900)
- Emery, W.J. & Thomson, R.E. *Data Analysis Methods in Physical Oceanography*. Elsevier.
- Foreman, M.G.G. et al. (2009). Versatile harmonic tidal analysis. *Atmosphere-Ocean*, 47, 191-200.
- Ghil, M. et al. (2002). Advanced spectral methods for climatic time series. *Reviews of Geophysics*, 40(1), 1003.
- Gonella, J. (1972). A rotary-component method for analysing meteorological and oceanographic vector time series. *Deep-Sea Research*, 19, 833-846.
- Grinsted, A., Moore, J.C. & Jevrejeva, S. (2004). Application of the cross wavelet transform and wavelet coherence to geophysical time series. *Nonlinear Processes in Geophysics*, 11, 561-566.
- Hannachi, A., Jolliffe, I.T. & Stephenson, D.B. (2007). Empirical orthogonal functions and related techniques in atmospheric science: A review. *International Journal of Climatology*, 27, 1119-1152.
- Hayashi, Y. (1971). A generalized method of resolving disturbances into progressive and retrogressive waves by space Fourier and time cross-spectral analyses. *Journal of the Meteorological Society of Japan*, 49, 125-128.
- Hayashi, Y. (1982). Space-time spectral analysis and its applications to atmospheric waves. *Journal of the Meteorological Society of Japan*, 60, 156-171.
- Horel, J.D. (1984). Complex principal component analysis: Theory and examples. *Journal of Climate and Applied Meteorology*, 23, 1660-1673.
- Hotelling, H. (1936). Relations between two sets of variates. *Biometrika*, 28, 321-377.
- Huang, N.E. et al. (1998). The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis. *Proceedings of the Royal Society of London A*, 454, 903-995.
- Jenkins, G.M. & Watts, D.G. (1968). *Spectral Analysis and Its Applications*. Holden-Day.
- Kaiser, H.F. (1958). The varimax criterion for analytic rotation in factor analysis. *Psychometrika*, 23, 187-200.
- Kolmogorov, A.N. (1941). The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers. *Dokl. Akad. Nauk SSSR*.
- Kutz, J.N., Brunton, S.L., Brunton, B.W. & Proctor, J.L. (2016). *Dynamic Mode Decomposition: Data-Driven Modeling of Complex Systems*. SIAM.
- Leffler, K.E. & Jay, D.A. (2009). Enhancing tidal harmonic analysis: Robust (hybrid L1/L2) solutions. *Continental Shelf Research*, 29, 78-88.
- Lomb, N.R. (1976). Least-squares frequency analysis of unequally spaced data. *Astrophysics and Space Science*, 39, 447-462.
- Lorenz, E.N. (1956). *Empirical Orthogonal Functions and Statistical Weather Prediction*. MIT Sci. Rep. No. 1.
- Lumley, J.L. (1970). *Stochastic Tools in Turbulence*. Academic Press.
- Mendel, J.M. (1991). Tutorial on higher-order statistics (spectra) in signal processing and system theory: Theoretical results and some applications. *Proceedings of the IEEE*, 79(3), 278-305.
- Mooers, C.N.K. (1973). A technique for the cross spectrum analysis of pairs of complex-valued time series. *Deep-Sea Research*, 20, 1129-1141.
- Navarra, A. & Simoncini, V. (2010). *A Guide to Empirical Orthogonal Functions for Climate Data Analysis*. Springer.
- Nikias, C.L. & Petropulu, A.P. (1993). *Higher-Order Spectra Analysis: A Nonlinear Signal Processing Framework*. Prentice-Hall.
- North, G.R., Bell, T.L., Cahalan, R.F. & Moeng, F.J. (1982). Sampling errors in the estimation of empirical orthogonal functions. *Monthly Weather Review*, 110, 699-706.
- Pawlowicz, R., Beardsley, B. & Lentz, S. (2002). Classical tidal harmonic analysis including error estimates in MATLAB using T_TIDE. *Computers & Geosciences*, 28, 929-937.
- Percival, D.B. & Walden, A.T. (1993). *Spectral Analysis for Physical Applications: Multitaper and Conventional Univariate Techniques*. Cambridge University Press.
- Plaut, G. & Vautard, R. (1994). Spells of low-frequency oscillations and weather regimes in the Northern Hemisphere. *Journal of the Atmospheric Sciences*, 51, 210-236.
- Preisendorfer, R.W. (1988). *Principal Component Analysis in Meteorology and Oceanography*. Elsevier.
- Rasmusson, E.M., Arkin, P.A., Chen, W.-Y. & Jalickee, J.B. (1981). Biennial variations in surface temperature over the United States as revealed by singular decomposition. *Monthly Weather Review*, 109, 587-598.
- Richman, M.B. (1986). Rotation of principal components. *Journal of Climatology*, 6, 293-335.
- Riedel, K.S. & Sidorenko, A. (1995). Minimum bias multiple taper spectral estimation. *IEEE Transactions on Signal Processing*, 43, 188-195.
- Rowley, C.W., Mezić, I., Bagheri, S., Schlatter, P. & Henningson, D.S. (2009). Spectral analysis of nonlinear flows. *Journal of Fluid Mechanics*, 641, 115-127.
- Scargle, J.D. (1982). Studies in astronomical time series analysis. II. *Astrophysical Journal*, 263, 835-853.
- Schmid, P.J. (2010). Dynamic mode decomposition of numerical and experimental data. *Journal of Fluid Mechanics*, 656, 5-28. (DOI:10.1017/S0022112010001217)
- Schmidt, O.T. & Colonius, T. (2020). Guide to spectral proper orthogonal decomposition. *AIAA Journal*, 58, 1023-1033.
- Scott, R.B. & Wang, F. (2005). Direct evidence of an oceanic inverse kinetic energy cascade from satellite altimetry. *Journal of Physical Oceanography*, 35, 1650-1666.
- Sirovich, L. (1987). Turbulence and the dynamics of coherent structures. Parts I-III. *Quarterly of Applied Mathematics*, 45, 561-590.
- Soufflet, Y. et al. (2016). On effective resolution in ocean models. *Ocean Modelling*, 98, 36-50.
- Stammer, D. (1997). Global characteristics of ocean variability estimated from regional TOPEX/POSEIDON altimeter measurements. *Journal of Physical Oceanography*, 27, 1743-1769.
- Taylor, K.E. (2001). Summarizing multiple aspects of model performance in a single diagram. *Journal of Geophysical Research*, 106, 7183-7192.
- Thomson, D.J. (1982). Spectrum estimation and harmonic analysis. *Proceedings of the IEEE*, 70(9), 1055-1096.
- Torrence, C. & Compo, G.P. (1998). A practical guide to wavelet analysis. *Bulletin of the American Meteorological Society*, 79, 61-78.
- Torrence, C. & Webster, P.J. (1999). Interdecadal changes in the ENSO-monsoon system. *Journal of Climate*, 12, 2679-2690.
- Towne, A., Schmidt, O.T. & Colonius, T. (2018). Spectral proper orthogonal decomposition and its relationship to dynamic mode decomposition and resolvent analysis. *Journal of Fluid Mechanics*, 847, 821-867.
- Tu, J.H., Rowley, C.W., Luchtenburg, D.M., Brunton, S.L. & Kutz, J.N. (2014). On dynamic mode decomposition: Theory and applications. *Journal of Computational Dynamics*, 1, 391-421.
- VanderPlas, J.T. (2018). Understanding the Lomb-Scargle periodogram. *Astrophysical Journal Supplement Series*, 236, 16.
- Vautard, R. & Ghil, M. (1989). Singular spectrum analysis in nonlinear dynamics, with applications to paleoclimatic time series. *Physica D*, 35, 395-424.
- von Storch, H. & Zwiers, F.W. (1999). *Statistical Analysis in Climate Research*. Cambridge University Press.
- Wallace, J.M., Smith, C. & Bretherton, C.S. (1992). Singular value decomposition of wintertime sea surface temperature and 500-mb height anomalies. *Journal of Climate*, 5, 561-576.
- Wang, S., Qiao, F., Dai, D. & Zhou, X. (2019). Anisotropy of the sea surface height wavenumber spectrum from altimeter observations. *Scientific Reports*, 9, 15896. (DOI:10.1038/s41598-019-52328-w)
- Weare, B.C. & Nasstrom, J.S. (1982). Examples of extended empirical orthogonal function analyses. *Monthly Weather Review*, 110, 481-485.
- Welch, P.D. (1967). The use of fast Fourier transform for the estimation of power spectra. *IEEE Transactions on Audio and Electroacoustics*, 15, 70-73.
- Wheeler, M. & Kiladis, G.N. (1999). Convectively coupled equatorial waves: Analysis of clouds and temperature in the wavenumber-frequency domain. *Journal of the Atmospheric Sciences*, 56, 374-399.
- Wilks, D.S. *Statistical Methods in the Atmospheric Sciences*. Academic Press. (스펙트럼·EOF 장)
- Wu, Z. & Huang, N.E. (2009). Ensemble empirical mode decomposition: A noise-assisted data analysis method. *Advances in Adaptive Data Analysis*, 1, 1-41.
- Xu, Y. & Fu, L.-L. (2011, 2012). The effects of altimeter instrument noise on the estimation of the wavenumber spectrum of sea surface height / Global variability of the wavenumber spectrum of oceanic mesoscale turbulence. *Journal of Physical Oceanography*, 41/42.

> 표기: 위 문헌 중 교과서(Wilks; Emery & Thomson; Jenkins & Watts; Bendat & Piersol; Preisendorfer; von Storch & Zwiers; Percival & Walden; Daubechies; Lumley; Nikias & Petropulu; Navarra & Simoncini; Kutz et al.)는 판·쪽수 없이 표준 참고문헌으로 인용했다. 논문은 웹 검증을 거쳐 실제 존재하는 것만 인용했으며 DOI는 임의로 생성하지 않았다(웹으로 확인된 DOI만 표기). 일부 회색문헌(UTide 기술보고서, UCAR Climate Data Guide)은 본문 출처에 URL/발행기관을 명시했다.
> 검증 메모: Welch(1967), Thomson(1982), Lomb(1976)/Scargle(1982)/VanderPlas(2018), Stammer(1997), Soufflet et al.(2016), Wang et al.(2019, Sci.Rep.), Hayashi(1971), Wheeler & Kiladis(1999), Horel(1984), Huang et al.(1998), Wu & Huang(2009), Schmid(2010), Elgar(1995), Mendel(1991), Di Matteo et al.(2021)은 본 보강 단계에서 웹으로 서지정보를 확인함. 이전 카드에서 Horel(1984)을 "Mon. Wea. Rev. 112:2165"로 잘못 표기한 것을 *J. Climate Appl. Meteor.* 23:1660-1673으로 정정함.
