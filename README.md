# validate-model-output

수치모델·AI 출력(NetCDF3/4·CSV)을 ERA5·GLORYS·관측·위성과 비교·검증·다축분석하는 범용 재사용 스킬 — 포맷·규약(K/°C·1D/2D/mesh·영문/한글 cp949)을 가리지 않는다.

---

## 무엇을 푸나

수치모델·AI 결과물을 검증·후처리할 때마다 반복되는 문제:

- **매번 손으로**: 파일 열기·변수 확인·단위 환산·비교 플롯을 검증자가 직접 코딩
- **포맷·규약 제각각**: NetCDF 비정형 mesh / CSV cp949 한글 헤더 / KST vs UTC 시간대 불일치
- **비일관·재현 불가**: 검증자마다 다른 지표·임계를 쓰고, 6개월 뒤 재현이 안 됨

이 스킬은 에이전트가 실시간으로 파일 구조를 파악·적응하고, 도메인 맞춤 다축 분석을 수행하며, 재현 가능한 보고서(JSON + Markdown)를 자동 생성한다.

---

## 핵심 차별점

| 특징 | 내용 |
|------|------|
| **결정적 코어 + live-adaptive 에이전트** | `scripts/` + `config/*.yaml`은 구조 파악과 적응의 출발점(SAMPLE). 실데이터에서 구조가 다르면 에이전트가 즉석 throwaway 코드로 파악하고 맞춤 코드로 적응 |
| **재현성 100%** | 같은 입력 → 보고서 바이트 동일. 합성 fixture로 hermetic(원본 데이터 불의존) |
| **다축 분석(최소 3축)** | 정확도·분포·시간·방향·종합·해역. 단일 지표 결론 금지 |
| **전파성** | `config/domains.yaml`에 줄 추가하면 새 도메인·변수 확장. SKILL.md를 로드하면 어느 에이전트에서도 동작 |
| **§G 함정 강제** | 기준자료 ≠ 진실·해석임계 advisory·동화 산물 독립관측 취급 금지를 보고서에 자동 경고 |

---

## 4페이즈 흐름

```
DISCOVER  →  ELICIT  →  ANALYZE  →  REPORT
  파악         질문       도메인       JSON
(포맷·구조)  (역할·범위)  맞춤 다축    + Markdown
```

1. **DISCOVER** — 폴더/파일을 스캔해 포맷·도메인·좌표·역할을 추정하고 `inventory.json` 생성. 미지 구조·열기 실패 시 즉석 throwaway 코드로 실시간 점검.
2. **ELICIT** — 인벤토리를 제시한 뒤 모델/기준자료 역할·도메인·관심 변수·시간대(TZ)·위경도 출처를 사용자에게 확인. 즉시 분석 진행 금지.
3. **ANALYZE** — 도메인별 다축 배터리 실행: 정확도(bias/RMSE/SI/r) · 분포(QQ/Perkins/KS) · 시간(overlay/lag) · 방향(원형통계) · 종합(Taylor/target) · 해역(crop).
4. **REPORT** — JSON + Markdown 보고서 생성. §G 함정(기준자료 한계·단일지표 금지)을 모든 보고서에 삽입.

---

## 빠른 시작

```bash
# 의존성 설치 (skills/validate-model-output/ 에서)
pip install -r requirements.txt

# 1. 파일/폴더 발견 — 포맷·도메인·좌표·역할 추정
python scripts/cli.py discover <폴더 또는 파일...>

# 2. 단일 파일 구조 상세 점검
python scripts/cli.py inspect <파일.nc>

# 3. 모델 출력 vs 기준자료 다축 검증 (에이전트 주도)
python scripts/cli.py validate <model_file> <reference_file>

# 4. 인수 검증 (5개 시나리오 자동 실행)
python scripts/run_acceptance.py
```

> 모든 명령은 `skills/validate-model-output/` 디렉터리를 기준으로 실행한다.

---

## 아키텍처 — 모듈맵

```
scripts/
├── cli.py            진입점 (discover / inspect / validate / verify 서브커맨드)
├── dataset.py        포맷 무관 Dataset 래퍼 (open_nc, 1D/2D/mesh 지원)
├── io_detect.py      포맷 감지 + CSV 인코딩 폴백 (utf-8 → cp949)
├── router.py         도메인 판별 (alias + headline, config/domains.yaml 기반)
├── discover.py       파일 인벤토리 생성 (inventory.json)
├── inspect_file.py   단일 파일 구조 상세 출력
├── preprocess.py     tz_to_utc · 단위 정규화 · mesh→점 matchup · 좌표 범용주입
├── aliases.py        한글 헤더 → 영문 변수명 매핑 (config/aliases.yaml)
├── rules.py          층위1 QC 규칙 로더 (config/rules.yaml)
├── qc.py             층위1 QC 실행 (물리범위·결측률 advisory)
├── report.py         JSON + Markdown 보고서 렌더러 (§G 함정 삽입)
├── metrics_basic.py  bias / RMSE / SI / r
├── metrics_circular.py  원형통계 (방향·파향)
├── metrics_distribution.py  QQ / Perkins / KS
├── metrics_pattern.py  공간 패턴 지수
├── plots.py          scatter / QQ / Taylor / rose / diff 플롯
├── regions.py        해역 crop (bounding box)
├── derive.py         파생 변수 (풍속 = sqrt(u²+v²) 등)
└── run_acceptance.py 인수 검증 5개 시나리오 자동 실행

config/
├── rules.yaml        층위1 QC 물리범위 규칙 (변수·단위별, advisory)
├── aliases.yaml      한글/약어 헤더 → 표준 영문 변수명
└── domains.yaml      도메인 정의 (GFS 패턴 등, 줄 추가로 확장)
```

---

## 도메인 지원

| 도메인 | 모델 예시 | 기준자료 | 특이사항 |
|--------|-----------|---------|---------|
| **기상** | GFS(격자) | ERA5(격자 대 격자) | 단위 K/°C 자동 판별, MSLP Pa/hPa |
| **파랑** | WW3(비정형 mesh) | 부이 CSV(점관측, cp949) | mesh→점 최근접 matchup, 파향 원형통계 |
| **확장** | yaml 1줄 추가 | 해양온도·해류·해수면 등 | `config/domains.yaml` 편집만으로 신규 도메인 등록 |

시간대: 모델은 보통 UTC, 부이 CSV는 KST인 경우 흔함. `preprocess.tz_to_utc`가 파라미터화하며, 에이전트가 CF `units` 확인 후 불일치 시 경고.

---

## 품질

| 항목 | 결과 |
|------|------|
| pytest | **421 passed / 0 warnings** |
| 인수 테스트 (`run_acceptance`) | **5/5 PASS** |
| 재현성 | **100%** — 같은 입력 → 보고서 바이트 동일 |
| 테스트 hermetic | 합성 fixture 사용, 미공개 원본 데이터 불의존 |

---

## 분석 방법 카탈로그

`project/research/` 에 15개 분야별 검증·분석 방법 카탈로그가 있다(~500 방법 카드, ~115 그림 카드).

```
project/research/
├── 00_overview_taxonomy.md     전체 분류 체계
├── 01_error_statistics.md      오차 통계 (bias/RMSE/SI/r)
├── 02_spatial_pattern_verification.md
├── 07_domain_meteorology.md    기상 도메인
├── 08_domain_waves.md          파랑 도메인
├── 09_domain_ocean_temp_salinity.md
...
└── 15_preprocessing_regridding_colocation.md
```

---

## 폴더 구조

```
geosr-hackathon-kit/
├── README.md                      이 파일
├── CLAUDE.md / AGENTS.md          에이전트 자동 로드 헤더
├── skills/
│   └── validate-model-output/
│       ├── SKILL.md               스킬 진입점 (에이전트 로드)
│       ├── scripts/               23개 Python 모듈
│       ├── config/                rules.yaml · aliases.yaml · domains.yaml
│       ├── tests/                 pytest 테스트 + 합성 fixture
│       ├── data/                  합성 fixture NC/CSV
│       └── requirements.txt
├── project/
│   ├── research/                  분석 방법 카탈로그 (15개 md)
│   ├── scenario/                  데모 시나리오
│   └── sample_data/               샘플 데이터
└── submit/                        제출물 폴더
    ├── PROCESS_LOG.md
    ├── BEFORE_AFTER.md
    ├── assets/
    └── evidence/
```

---

## 팀

**예보사업부 AI·AX 해커톤 A팀**

- 최범규 — 스킬 설계·논문 조사·구현
- 오유정 — 설계 스펙·데모 시나리오·재현성 실험

---

## 보안 주의

미공개 관측 원본·개인정보·대외비 좌표/수치를 외부 AI 서비스에 업로드하지 말 것. 공개 또는 익명화 데이터만 사용한다.

---

## 라이선스

내부 해커톤 제출물. 외부 공개 전 소속 기관 정책 확인 필요.
