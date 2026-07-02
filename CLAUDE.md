# validate-model-output — 스킬 개발 지침 (이 파일은 자동 로드됩니다)

이 저장소의 본체는 `skills/validate-model-output/` 스킬이다 — 수치모델·AI·위성 등 **어떤 결과물이든** 그 데이터에 맞는 검증을 다각도로 수행하는 **범용** 검증 스킬. 이 repo에서 작업할 때 아래를 지켜라.

## 이 스킬이 지켜야 할 설계 원칙 (수정 시 합격 기준)
1. **범용성**: 특정 분야(파랑 등)에 매이지 말고 지구시스템 전반(대기·해양·파랑·해수면·해빙·수문·대기질·위성 EO … + AI)을 아우른다. 분야를 열거하지 말고 **데이터 특성(자료형·변수성질)** 으로 라우팅한다 (`scripts/router.py`의 `characterize()`). 도메인은 2차 힌트.
2. **미지 도메인 안전망**: 분야를 못 정해도 멈추지 말 것 — 데이터 특성으로 일반 배터리를 구성해 진행하고 사용자에게 확인.
3. **능동 메타탐색 + 되묻기**: 시간대(KST/UTC)·컬럼 의미·단위·정점 좌표를 에이전트가 먼저 파악하고, 모르는 것은 되물어 확정한 뒤에만 분석.
4. **논문 근거**: 검증법은 `references/research/` 카탈로그(문헌·DOI)에 근거한다. 단순 RMSE에서 멈추지 말 것.
5. **반복 심화**: 1차 검증 → 판독 → 2차 검증 추천·수행 → 반복(SKILL.md PHASE 4 DEEPEN). 단일 패스 종료 금지.
6. **격자·정점 동급**: 정점(관측소)·시계열 데이터도 격자와 동등한 1급 경로.
7. **cross-domain 추천 / AI·위성 = 얹는 축 / 지도엔 해안선+위경도 필수** (`references/plotting_maps.md`).
8. **코드는 SAMPLE = 적응 출발점**: 사용자 데이터 구조가 다르면(변수명·좌표·단위·시간규약) 전처리·메타확인·검증 **모든 단계**에서 맞춤 코드를 그 자리에 작성해 돌린다.
9. **§G 해석 함정 강제**: 기준자료≠참값·해석 임계는 advisory·단일 지표 금지·동화/보간 산물 독립관측 취급 금지·대표성 오차 — 보고서에 자동 명시.

## 하지 말 것
- `router.py`에 특정 도메인 로직 하드코딩 금지 — 도메인 우선순위는 `config/domains.yaml`의 `headline`(대표변수 가중)으로만.
- 미검증 성능·품질 수치("N passed", "재현성 X%") 주장 금지.
- `SKILL.md`는 얇게(약 500줄 이내) 유지하고 상세는 `references/`로 위임(progressive disclosure). 긴 코드 예시는 references로.
- 참조 경로는 `$SKILL`(스킬 폴더) 기준으로 통일 — 카탈로그는 `references/research/...`.

## 구조
- `skills/validate-model-output/SKILL.md` — 에이전트 진입점(5단계 흐름: DISCOVER→ELICIT→ANALYZE→DEEPEN→REPORT · 데이터특성→방법 규칙).
- `references/` — `research/`(논문 카탈로그·그림카드) · `recipe_*`(도메인 레시피) · `plotting_maps.md`(지도) · `extending.md`(새 분야 추가) · `adapting.md` · `architecture.md`.
- `config/` — `domains.yaml`(분야 판별) · `aliases.yaml`(한글·비표준 변수명) · `rules.yaml`(QC 규칙). **YAML만 편집해 확장.**
- `scripts/` — 런타임 모듈(SAMPLE 출발점).

## 새 분야(도메인) 추가
`references/extending.md` 절차를 따른다 — `config/domains.yaml` 블록 1개 + (선택)`aliases.yaml` + 7필드 도메인 카드(`references/research/`) + 색인(00 C-1, SKILL.md 2-C) 갱신.

## 작업 방식
- 의미 있는 변경은 에이전트가 직접 만들고, 코드 변경 후에는 실제로 돌려 확인(스모크 테스트)한다.
- 커밋·푸시는 사용자가 요청할 때만.

## 보안
미공개 관측 원본·개인정보·대외비 좌표/수치를 외부 서비스에 업로드하지 말 것. 공개·익명화 데이터만 사용한다.
