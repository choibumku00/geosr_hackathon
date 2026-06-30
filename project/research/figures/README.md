# 검증 시각화(그림)·표 레퍼런스 카탈로그 (Verification Figure Catalog)

수치모델 결과를 **관측/재분석/위성과 비교·검증**할 때 "어떤 그림으로 보여주고 어떻게 읽는가"를 모은 레퍼런스다. 텍스트 메서드카탈로그(`../01`~`../15`)의 **시각화 짝(companion)** 으로, 각 그림 카드는 대응 메서드카드와 교차링크된다. 구현 시 플롯 코드로 바로 옮길 수 있도록 "만드는 법(실존 Python 도구·함수)"을 함께 적었다.

- **언어 규칙**: 한국어 서술 + 표준 기술용어 영문 병기.
- **그림 카드 8항목**: 그림명(국문/English) · 무엇을 보여주나 · **읽는 법**(축·색·기호, 좋은/나쁜 패턴) · 언제 쓰나(자료형·검증목적) · 짝지표 & `01–15` 교차링크 · **만드는 법**(Python 도구·함수) · 함정·주의 · 출처.
- **출처 원칙**: 검증 가능한 실제 출처만. **DOI는 직접 확인한 것만** 표기하고 지어내지 않음. 미확인은 "(확인요)". **논문 그림은 복제하지 않고 유형·사양만 기술**(저작권).
- **검증 함정 강제(→ `../00_overview_taxonomy.md` §G)**: 기준자료(ERA5/GLORYS/위성 L4)는 **참값이 아니라 reference** · 해석 임계(SI<0.15·ACC≥0.6 등)는 **advisory**(영역·해상도 의존 경고 동반) · 단일 그림/지표로 결론 금지.

## 파일 목록 (그림 카드 약 115개)

| # | 파일 | 범위 | 카드 수 | 대응 메서드카탈로그 |
|---|---|---|:---:|---|
| 16 | [`16_fig_common.md`](./16_fig_common.md) | **공통·횡단** — 정확도·공간·범주/확률·스펙트럼·시계열·AI/ML (Taylor·target·QQ·ROC·reliability·performance·rank hist·Brier/CRPS·FSS·Hovmöller·EOF·PDF/CDF·RAPSD 등) | 20 | 01·02·03·05·06·14 |
| 17 | [`17_fig_meteorology.md`](./17_fig_meteorology.md) | **기상·대기** — 바람 벡터·wind rose·기온·MSLP/S1·강수(double-penalty·FSS·intensity-scale) | 16 | 07 |
| 18 | [`18_fig_waves.md`](./18_fig_waves.md) | **파랑** — Hs 산점도+SI/HH·wave rose·1D/2D 스펙트럼·partition·극치·altimeter/TC | 16 | 08 |
| 19 | [`19_fig_temp_salinity.md`](./19_fig_temp_salinity.md) | **수온·염분** — T–S diagram·Argo 프로파일·단면·SST bias/전선·MLD·OHC·등밀도면 | 15 | 09 |
| 20 | [`20_fig_currents.md`](./20_fig_currents.md) | **해류·조류·순환** — quiver/streamline·current rose·조류타원·rotary·PVD·MKE/EKE·Okubo-Weiss·FTLE/LCS | 16 | 10 |
| 21 | [`21_fig_sea_level.md`](./21_fig_sea_level.md) | **해수면·조위** — 조화상수 진폭/지각·복소차·코타이달·해일·DAC·track-vs-grid·MSL trend·재현수위·datum/QC | 16 | 11 |
| 22 | [`22_fig_satellite.md`](./22_fig_satellite.md) | **위성·원격탐사** — 매치업·대표성오차·TC/ETC·고도계 track-vs-grid/파수스펙·SST L2/L3/L4·산란계 풍·해색·u-plot | 16 | 12 |

## 사용 흐름 (Skill 연결)

1. 입력 자료의 **도메인·자료형 판별**(`../00` C절 라우터) → 해당 도메인 그림 파일을 본다.
2. 모든 도메인은 **공통편(`16`)** 의 정확도·분포·유의성 그림을 기본으로 끌어 쓴다(중복 정의 대신 교차링크).
3. 각 그림 카드의 "만드는 법"을 검증 함수의 **플롯 출력**으로 구현 → 리포트(`report.md`)에 삽입.
4. 캡션·해석 문장은 §G 원칙(reference≠참값·advisory 임계·단일그림 금지)을 강제.

> 실제 예시 이미지는 저작권 문제로 논문에서 가져오지 않는다 — **우리 데이터(예: 파랑모델·부이)로 직접 렌더링**해 무저작권 예시를 만든다(구현 단계).
