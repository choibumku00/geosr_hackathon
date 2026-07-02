# validate-model-output

**수치모델·AI·위성 등 어떤 결과물이든, 그 데이터에 맞는 검증 방식을 스스로 찾아 다각도로 검증하는 범용 스킬.**

이 저장소의 본체는 `skills/validate-model-output/` 스킬이다. 특정 분야에 매이지 않고 **지구시스템 전반**(대기·해양·파랑·해수면·해류·해빙·수문·육상·대기질·구름복사·해양생지화학·우주기상 + 이를 만드는 AI)을 아우르며, **격자 데이터와 정점(관측소)·시계열 데이터**를 모두 동급으로 다룬다.

---

## 우리가 구현한 것

- **데이터 특성 기반 범용 라우팅** — 분야를 목록에서 고르는 게 아니라, 자료형(격자/mesh/정점·시계열/프로파일/스펙트럼)과 변수성질(벡터·원형·양수·분율·앙상블 등)에서 검증법이 따라 나온다. 카탈로그에 없는 분야도 동작한다. (`scripts/router.py`의 `characterize`)
- **미지 도메인 안전망** — 분야를 못 정하거나 근거가 빈약하면(`weak_evidence`) 멈추지 않고 일반 검증 배터리를 구성한 뒤, 정체불명·무단위 변수는 사용자에게 되물어 확정한다.
- **능동 메타탐색 + 되묻기** — 시간대(KST/UTC)·컬럼 의미·단위·정점 좌표·기준자료 보유 여부를 에이전트가 먼저 파악하고, 확정 전엔 분석을 시작하지 않는다.
- **논문 근거 카탈로그 내장** — `references/research/`에 13개 도메인 방법 카드(~720개, 출처·DOI)와 그림 카드(~243개)를 스킬 안에 동봉. 단순 RMSE가 아닌 세부 검증.
- **다각도 + 반복 심화** — 최소 3축(정확도·분포·시간/공간) 강제 + 1차 결과를 판독해 2차 검증을 추천·수행하며 품질을 계속 끌어올리는 DEEPEN 루프.
- **cross-domain 적용** — 그 분야 관행이 아니어도 이 데이터에 유용하면 타 분야·공통 검증법(극치·스펙트럼·확률검증 등)을 **실제로 함께 수행**한다.
- **정점·시계열 1급 지원** — 정점별+통합 지표·시계열/위상·분포 + 정점 위치를 해안선 지도에 표시.
- **지도 그림엔 위치정보 필수** — 위경도 그림은 해안선·육지 + 위경도 라벨을 반드시(오프라인이어도 안전 동작). (`references/plotting_maps.md`)
- **AI·위성 = 얹는 축** — 별도 분야가 아니라 물리 도메인 위에 얹는 평가축(UQ/OOD·매치업/대표성오차)으로 처리.
- **샘플코드 적응 원칙** — 내장 코드·레시피는 완성품이 아닌 출발점(SAMPLE). 데이터가 다르면 전 단계(전처리·메타·검증)에서 맞춤 코드를 그 자리에 작성한다.
- **전파성** — `config/domains.yaml`에 블록 하나면 새 분야 자동 인식(가이드: `references/extending.md`).
- **해석 함정(§G) 강제** — 기준자료≠참값·임계는 advisory·단일 지표 금지 등을 보고서에 자동 명시.

---

## 흐름 (5단계)

```
DISCOVER → ELICIT → ANALYZE → DEEPEN(반복) → REPORT
 파악        질문      다축검증    2차 심화       보고
```

---

## 구성

```
skills/validate-model-output/         ← 스킬 본체
├── SKILL.md                          에이전트 진입점 (5단계 흐름·데이터특성→방법 규칙)
├── config/                           domains.yaml(13도메인) · aliases.yaml · rules.yaml  (YAML만 편집해 확장)
├── scripts/                          런타임 모듈 (io_detect·dataset·router·preprocess·metrics_*·plots ...; 모두 SAMPLE 적응 출발점)
└── references/
    ├── research/                     방법 카탈로그(00~15, 23~30) + figures/(16~22, 31~38) — 논문·DOI 근거
    ├── recipe_*.md                   도메인별 worked SAMPLE 레시피(파랑·기상·강수·해빙·대기질·수문·육상·해양BGC) + cross-domain 절
    ├── plotting_maps.md              지도 그림(해안선+위경도, add_basemap) · extending.md 새 분야 추가
    └── adapting.md · architecture.md · usage.md
```

Claude Code에 스킬로 쓰려면 `skills/validate-model-output/`를 스킬 디렉터리에 두면 `SKILL.md` frontmatter로 자동 발견된다. 자세한 내용은 [스킬 README](skills/validate-model-output/README.md).

> 배포용 압축본: `skills/validate-model-output-skill.zip` (스킬 폴더 전체). 개발 과정 산출물(`project/`·`docs/`)은 저장소에 포함하지 않는다.

---

## 보안

미공개 관측 원본·개인정보·대외비 좌표/수치를 외부 서비스에 올리지 말 것. 공개·익명화 데이터만 사용한다.
