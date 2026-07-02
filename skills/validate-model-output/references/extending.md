# 새 분야(도메인) 추가 가이드 — 전파성

이 스킬은 **지구시스템 어느 분야든** 검증하도록 설계됐다. 라우팅 1차 축은 도메인이 아니라 **데이터 특성**(자료형·변수성질)이라, 카탈로그에 없는 분야도 `router.characterize()`가 **일반 배터리(C-0) + 트리거**로 이미 동작한다. 아래는 그 분야를 *1급 도메인*으로 승격해 자동 라우팅·전용 카드까지 붙이는 절차다.

> 핵심: **`config/domains.yaml`에 블록 1개만 추가하면 라우터가 자동 인식**한다. 코드 수정 불필요.

---

## 3단계 (약 15분)

### 1) `config/domains.yaml`에 도메인 블록 추가

```yaml
  air_quality:                      # 새 도메인 키
    standard_names:                 # CF standard_name (강한 신호)
      - mass_concentration_of_pm2p5_ambient_aerosol_in_air
      - mass_concentration_of_ozone_in_air
    name_patterns:                  # 변수명 정규식 (약한 신호)
      - "^pm2_?5$"
      - "^pm10$"
      - "^o3$"
      - "^no2$"
      - "aod"
    headline:                       # 이 분야를 '정의'하는 대표변수 → 가중 3표
      - mass_concentration_of_pm2p5_ambient_aerosol_in_air
```

- `headline`이 있으면 다른 분야의 부수·강제 변수가 공존해도 이 도메인이 이긴다(가중치 3).
- `headline: []`(빈 값)이면 일반 1표 투표만 — 광역·중립 도메인에 적합(예: meteorology).

### 2) (선택) `config/aliases.yaml`에 한글·비표준 헤더 매핑

```yaml
  mass_concentration_of_pm2p5_ambient_aerosol_in_air:
    - 초미세먼지
    - "PM2.5(㎍/㎥)"
```

→ CSV 한글 헤더도 표준명으로 인식되어 라우팅·검증에 참여한다.

### 3) 도메인 카드 작성 → `references/research/NN_domain_<name>.md`

아래 **7필드 템플릿**으로 카드를 만들고, 색인 두 곳에 한 줄씩 추가한다:
- `references/research/00_overview_taxonomy.md` **C-1 표**에 `판별 도메인 | 대표 변수 | 자료형 | 기본 메서드 묶음 | 출처` 행
- `SKILL.md` **2-C 도메인 표**에 `도메인 | 지표 카탈로그 | 그림 카탈로그 | 핵심 축` 행

---

## 도메인 카드 템플릿 (메서드 1개 = 카드 1개)

```markdown
### <방법명 국문 (English)>
- **무엇을 측정**: (이 지표/그림이 잡아내는 것)
- **정의·수식**: (수식 또는 알고리즘 한 줄)
- **적용 도메인·자료형**: (격자/정점·시계열/트랙/프로파일; 어느 변수에)
- **입력 전제**: (짝지음·단위·좌표·시간대·결측 처리 전제)
- **해석 기준(advisory)**: (관행 임계 — 영역·해상도 의존 경고 동반, good/bad 단정 금지)
- **한계·주의**: (오용·함정 — §G 원칙과 연결)
- **출처**: (검증 가능한 실제 문헌/기관. 미확인은 "(확인요)")
```

---

## 워크드 예시 — 대기질(PM2.5) 추가

- **자료형**: 대개 **정점(측정소) 시계열 CSV** + (모델) 격자 + (위성) AOD 트랙/격자 → 정점·격자·위성 축이 모두 관여.
- **변수성질**: 농도 = **양수·꼬리 두꺼움**(고농도 사건) → `characterize`가 `nonnegative`·`extreme_prone` 태그 → 로그/√ 변환·극치(POT/GEV) 트리거 자동 제안.
- **검증 골격**(§SKILL 2-A 성질→방법 규칙 그대로):
  - 정점별+통합 bias·RMSE·정규화오차, 로그공간 통계
  - 고농도 사건 → 범주형(POD/FAR/CSI)·극치분포
  - 측정소 **위치 지도**(해안선+위경도, 마커+ID) — 도시/배경 구분
  - 위성 AOD 대조 시 → 위성 축(매치업·대표성오차·TC)
  - AI 예보면 → AI 축(UQ·OOD·스펙트럼)
- **추가 작업**: `domains.yaml`에 `air_quality` 블록(1)만 넣으면 라우터가 즉시 인식. 전용 카드는 여력 될 때 `references/research/`에 추가.

## 다른 분야도 같은 방식
- **수문/하천유량**: headline `water_volume_transport_in_river_channel`/`discharge`; 핵심 지표 KGE·NSE(이미 `01`)·유황곡선·첨두/저수기; 자료형 정점 시계열 중심.
- **빙권/해빙**: headline `sea_ice_area_fraction`; SIC bias·SIE/SIA·**IIEE**(적분 얼음경계 오차)·경계선; fraction 태그 → bounded 지표.
- **육상/토양수분**: headline `mass_content_of_water_in_soil`/`soil_moisture`; 이상상관·triple collocation(위성×모델×in-situ).

> 어느 분야든 **domains.yaml 블록 → (선택)aliases → 카드**면 끝. 카드가 아직 없어도 `characterize`의 데이터특성 라우팅이 최소 다축 검증을 보장한다.
