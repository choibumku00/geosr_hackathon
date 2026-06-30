# validate-model-output — 개발자 가이드

수치모델 / AI 출력(NetCDF3/4, CSV)을 ERA5·GLORYS·관측·부이와 비교·검증하는
범용 재사용 스킬(skill). 포맷·규약(K/°C, 1D/2D/mesh, 영문/한글 cp949)을 가리지 않는다.

---

## 1. 설치 (Installation)

Python 3.11+ 권장.

```bash
pip install -r requirements.txt
```

`requirements.txt` 핵심 의존:

| 패키지 | 최소 버전 | 용도 |
|--------|-----------|------|
| xarray | 2024.0    | NetCDF 래핑 |
| netCDF4 | 1.7      | C 라이브러리 엔진 |
| h5netcdf | 1.3     | HDF5/NetCDF4 Python 엔진 (경로 폴백) |
| h5py   | 3.12      | HDF5 저수준 |
| scipy  | 1.13      | cKDTree(mesh matchup), KS 통계 |
| PyYAML | 6.0       | config YAML 파싱 |
| numpy  | 2.0       | 수치 연산 |
| pandas | 2.0       | CSV → xarray 변환 |
| matplotlib | *(자동)* | 그림 생성 |
| pytest | 8.0       | 테스트 |

---

## 2. 폴더 구조 (Directory Layout)

```
validate-model-output/
├── SKILL.md                   # 에이전트 진입점 — 4페이즈·§G 규칙 정의
├── README.md                  # 이 파일 (개발자 가이드)
├── requirements.txt
├── pytest.ini
├── config/
│   ├── rules.yaml             # 층위1 QC 물리범위·결측 규칙 (코드 무수정 확장)
│   ├── domains.yaml           # 도메인 판별 패턴 (기상·파랑·해양 확장)
│   └── aliases.yaml           # 한글·비표준 변수명 → CF 표준명 매핑
├── data/                      # 합성 fixture (hermetic — 원본 비의존)
│   ├── clean_gfs_like.nc
│   ├── clean_era5_like.nc
│   ├── broken_era5_like.nc
│   ├── ww3_mesh_like.nc
│   ├── buoy_obs_like.csv
│   └── ...
├── scripts/                   # 핵심 모듈 (SAMPLE 출발점 — 실데이터 적응)
│   ├── dataset.py
│   ├── io_detect.py
│   ├── router.py
│   ├── discover.py
│   ├── inspect_file.py
│   ├── rules.py
│   ├── qc.py
│   ├── report.py
│   ├── cli.py
│   ├── aliases.py
│   ├── preprocess.py
│   ├── metrics_basic.py
│   ├── metrics_circular.py
│   ├── metrics_distribution.py
│   ├── metrics_pattern.py
│   ├── plots.py
│   ├── regions.py
│   ├── derive.py
│   ├── run_acceptance.py
│   ├── make_fixtures.py
│   ├── make_waves_fixtures.py
│   └── make_waves_broken.py
├── tests/                     # pytest 테스트 (421 passed)
└── references/                # 도메인별 분석 레시피 카탈로그
```

---

## 3. 모듈 맵 (Module Map)

| 모듈 파일 | 한 줄 역할 |
|-----------|-----------|
| `dataset.py` | 포맷 무관 `Dataset` 추상화 + `open_nc` (한글 경로 폴백 포함); `coord_kind()` — 1d / 2d / mesh / none 판별 |
| `io_detect.py` | 매직바이트로 NetCDF3/4 감지, CSV 인코딩 폴백(utf-8 → cp949 → euc-kr → latin-1); `open_dataset()` 단일 진입점 |
| `router.py` | `detect_domain()` — domains.yaml + aliases.py 로 도메인(meteorology / waves / ocean / ...) 자동 판별; 한글 헤더·파랑 headline(Hs) 우선 투표 |
| `discover.py` | 폴더/파일 재귀 스캔 → 각 파일마다 `probe()` 실행; 역할 추정(output/reference/unknown); `inventory.json` 직렬화 |
| `inspect_file.py` | 단일 파일 구조 best-effort 탐지 → `{format, coord_kind, variables, domain, ...}` dict 반환 (크래시 없음) |
| `rules.py` | `rules.yaml` 로드 + 변수 → 규칙 매칭 (`match_rule`); standard_name / name_patterns / units_any 순 매칭 |
| `qc.py` | 층위1 QC 실행기 — 스키마·격자·시간·변수별 값범위·결측·이상치(N-sigma) 검사; `run_qc()` → `{checks, summary, ok}` |
| `report.py` | QC 결과 → Markdown + JSON 렌더(`render_markdown`, `write_report`); verify 결과 → `render_verify_markdown`, `write_verify_report`; §G advisory 캡션 강제 |
| `cli.py` | `validate-model-output` CLI 진입점 — `discover` / `inspect` / `validate` / `verify` 4개 서브커맨드 (SAMPLE) |
| `aliases.py` | `aliases.yaml` 로드 + `to_standard(name)` — 한글/비표준 변수명을 CF 표준명으로 변환 |
| `preprocess.py` | `to_kelvin` 단위 정규화 / `match_points_to_mesh` cKDTree 최근접 matchup / `tz_to_utc` KST·UTC 변환 / `inject_point_coords` 좌표 주입 / `parse_points_list` 관측점 목록 파싱 / `common_time_index` 시간 교집합 |
| `metrics_basic.py` | bias / MAE / RMSE / NRMSE / SI(산란지수) / pearson_r / linregress; 공통 NaN 마스크 |
| `metrics_circular.py` | 원형 통계 — `circular_mean_error` / `circular_rmse` / `circular_corr`; 파향·풍향 검증 전용 (±180° 래핑) |
| `metrics_distribution.py` | 분포 비교 — `quantiles` / `qq_points` / `perkins_skill_score` / `ks_distance` |
| `metrics_pattern.py` | 패턴 통계 — `taylor_stats` (std_ratio·corr·CRMSD) / `target_stats` (bias·URMSD) / `pattern_correlation` |
| `plots.py` | `scatter_si` / `timeseries_overlay` / `diff_map` / `qq_plot` / `taylor_diagram` / `wave_rose`; 모든 그림에 §G advisory 캡션 강제 (SAMPLE) |
| `regions.py` | `NAMED_REGIONS` — 한국 주요 해역 bbox (동해·남해·서해·황해·대한해협·북서태평양·한국근해); `region_bbox` / `crop_grid_mask` / `crop_mesh_mask` |
| `derive.py` | u·v 바람 성분 파생변수 — `windspeed` / `wind_direction` (기상학적 FROM 규약) |
| `run_acceptance.py` | 인수테스트 자동러너 — TC-B1(validate 3케이스) + TC-A1(discover 2케이스); `python scripts/run_acceptance.py` |
| `make_fixtures.py` | 기상(GFS↔ERA5 유사) 합성 fixture 생성 |
| `make_waves_fixtures.py` | WW3 mesh + 부이 CSV 합성 fixture 생성 |
| `make_waves_broken.py` | QC FAIL 유도 파손 fixture 생성 (value_range, 결측, 잘린 파일) |

---

## 4. CLI 사용법

CLI는 `scripts/cli.py` 를 직접 실행하거나 에이전트가 서브프로세스로 호출한다.

```bash
cd skills/validate-model-output
python scripts/cli.py <subcommand> [options]
```

### 4-1. `discover` — 폴더/파일 인벤토리

```bash
python scripts/cli.py discover path/to/data/ \
    [--out inventory.json]
```

- 폴더 재귀 스캔 → 포맷·도메인·역할·좌표 종류·변수 목록 출력
- `inventory.json` 에 직렬화 (기본: 현재 폴더)
- 열 수 없는 미지 포맷도 크래시 없이 `openable=false` 로 기록

### 4-2. `inspect` — 단일 파일 구조 프로브

```bash
python scripts/cli.py inspect path/to/file.nc
```

- JSON 으로 `{format, coord_kind, variables, domain, confidence, time, ...}` 출력
- 오류 시에도 `{"openable": false, "error": "..."}` 반환 (크래시 없음)

### 4-3. `validate` — 층위1 QC

```bash
python scripts/cli.py validate path/to/model_output.nc \
    [--out report_dir/]
```

- 스키마·격자·시간·변수별 값범위·결측·이상치 검사
- `qc_report_<파일명>.json` + `.md` 저장
- 종료코드: 0 = ok, 1 = FAIL 있음

### 4-4. `verify` — 모델 vs 기준 다축 검증 (SAMPLE)

```bash
# 격자 대 격자 (GFS vs ERA5)
python scripts/cli.py verify gfs_output.nc \
    --ref era5_reanalysis.nc \
    --out results/ \
    --regions 동해,남해

# mesh + 점관측 (WW3 vs 부이 CSV)
python scripts/cli.py verify ww3_mesh.nc \
    --ref buoy_obs.csv \
    --out results/ \
    --points station_coords.list \
    --ref-tz KST \
    --regions 동해,서해,남해
```

| 옵션 | 설명 |
|------|------|
| `--ref <path>` | 기준(관측/재분석) 파일 경로 (필수) |
| `--out <dir>` | 결과 저장 폴더 (기본: 현재 폴더) |
| `--points <path>` | 관측점 목록 파일 (`lon lat id` 형식); mesh+점관측 좌표 주입 |
| `--regions <names>` | 해역별 반복 분석 — 쉼표 구분 (예: `동해,남해,서해`) |
| `--model-tz <tz>` | 모델 시간대 (`UTC` / `KST` / `+09:00`; 기본 UTC 가정) |
| `--ref-tz <tz>` | 기준 시간대; **부이 KST vs 모델 UTC 면 9h 어긋남** — `KST` 명시 시 자동 보정 |

출력:
- `verify_report_<모델명>.json` + `.md`
- `scatter_<var>.png`, `taylor_<var>.png`, `qq_<var>.png`
- `diff_map_<var>.png` (격자 or 점 편차 맵)
- `timeseries_<var>.png` (mesh+점관측 시계열, 시간 교집합 구간)
- `rose_model_<dir_var>.png`, `rose_ref_<dir_var>.png` (방향 변수 존재 시)

---

## 5. 4페이즈 + Live-Adaptive 철학

```
discover → elicit → analyze → report
```

| 페이즈 | 에이전트 행동 |
|--------|--------------|
| **discover** | 미지 파일 실시간 점검; `inspect` + 미지 포맷 에이전트 직접 파악; 자동 분석 금지 |
| **elicit** | 도메인·비교 대상·시간대·관측점 좌표 출처를 사용자에게 질문; 즉시 분석 금지 |
| **analyze** | 도메인별 다축 배터리 실행; 단일 지표 금지 (최소 3축) |
| **report** | JSON + Markdown 저장; §G 함정 강제 캡션 |

**scripts = SAMPLE 출발점.** 실데이터에서 구조가 다를 때(변수명·좌표형·단위·시간 규약)
에이전트가 실시간으로 구조를 점검하고 도메인 맞춤 코드를 작성한다.
scripts는 "완비 구현"이 아니라 "대략적 구조 파악 + 적응의 출발점"이다.

**다축 배터리:**
- 정확도: bias / RMSE / SI / Pearson r
- 분포: Q-Q / Perkins Skill Score / KS distance
- 시간: 시계열 overlay / lag 분석
- 방향: 원형 CME / CRMSE / circular_corr (파향·풍향 전용)
- 종합: Taylor diagram / Target diagram
- 해역: 동해·남해·서해 등 bbox crop 후 반복 계산

---

## 6. 설정 확장점 (Config Extension Points)

코드 수정 없이 YAML만 편집하면 새 규칙·도메인·별칭을 추가할 수 있다.

### `config/rules.yaml` — 층위1 QC 규칙 추가

```yaml
rules:
  - name: my_custom_var
    standard_names: [my_cf_standard_name]
    name_patterns: ['^myvar$', 'my_prefix.*']
    units_any: [m/s]
    valid_min: -50.0
    valid_max: 50.0
    max_missing_frac: 0.5
    sigma: 5.0        # N-sigma 이상치 임계 (optional, 기본 6.0)
```

### `config/domains.yaml` — 새 도메인 판별 추가

```yaml
domains:
  my_domain:
    standard_names:
      - my_standard_name_1
    name_patterns:
      - 'myvar.*'
      - '^mv_'
```

### `config/aliases.yaml` — 한글/비표준 변수명 매핑 추가

```yaml
aliases:
  significant_wave_height:
    - 유의파고
    - hm0
  my_cf_standard_name:
    - 내_변수명
    - MY_VAR
```

`aliases.py` 는 모듈 로드 시 `aliases.yaml` 을 읽어 소문자 lookup 테이블을 빌드하므로
`router.py` 와 `cli.py` 에서 즉시 인식된다.

---

## 7. 테스트 및 인수 검증 (Tests & Acceptance)

### 단위·통합 테스트

```bash
cd skills/validate-model-output
python -m pytest                 # 전체 실행
python -m pytest -v              # 상세 출력
python -m pytest tests/test_metrics_basic.py   # 특정 모듈
```

현재 상태: **421 passed / 0 warnings** (합성 fixture 기반 hermetic 테스트).

### 인수 테스트 (Acceptance)

```bash
python scripts/run_acceptance.py
```

TC 목록:

| TC | 시나리오 | 기대 결과 |
|----|---------|-----------|
| B1-1 | `clean_era5_like.nc` validate | `ok=True` |
| B1-2 | `broken_era5_like.nc` validate | `ok=False` (value_range/grid FAIL) |
| B1-3 | 잘린 파일 validate | 열기 실패 — 크래시 없음 |
| A1-1 | `ww3_mesh_like.nc` discover | `domain=waves, coord_kind=mesh` |
| A1-2 | `buoy_obs_like.csv` discover | `openable=True` |

현재 상태: **5/5 PASS**.

### 재현성

동일 입력 → report 바이트 동일. `run_acceptance.py` 자동 검증.

---

## 8. §G 함정 (Interpretation Pitfalls)

에이전트와 사용자가 반드시 지켜야 할 해석 경계:

1. **기준자료 = reference (≠ truth)** — ERA5·GLORYS·부이는 검증 기준이지 진실이 아니다.
   동화 산물·보간 결과를 독립 관측으로 취급하지 마라.
2. **해석 임계 = advisory** — 물리범위·N-sigma·RMSE 임계는 도메인·변수·해상도 의존.
   단일 임계로 합/불합을 결론짓지 마라.
3. **단일 지표 금지** — 최소 3축(정확도·분포·시간 또는 방향) 이상을 함께 제시하라.
4. **동화·보간 산물 독립관측 취급 금지** — GLORYS·ERA5 재분석은 독립 관측이 아니다.
5. **시간대(TZ) 경고** — 부이 KST(UTC+9) vs 모델 UTC 면 9h 불일치. `--ref-tz KST` 명시하라.

---

## 9. 한계 (Limitations)

다음은 현재 scripts SAMPLE 범위 밖이다. 실데이터에서 해당하면 에이전트가 도메인 맞춤 코드를 작성해야 한다.

| 한계 | 설명 |
|------|------|
| 일반 regrid | 격자 크기가 서로 다른 경우 보간은 미구현. 동일 격자 가정 전제. |
| GRIB native | GRIB1/2 직접 읽기 미지원. 사전에 `wgrib2` / `cfgrib` 로 NetCDF 변환 필요. |
| 위성 TC (tropical cyclone) | 위성 track 데이터는 reference-only 로 취급; 경로 매칭 알고리즘 미구현. |
| 구면 보간 / CRS 변환 | pyproj / BallTree(Haversine) 기반 정밀 matchup은 실데이터 맞춤 코드 필요. |
| 날짜변경선(antimeridian) | `regions.py` bbox가 날짜변경선을 걸쳐 있는 경우 미지원. |
| 음의 시간 교집합 | `common_time_index` 는 중복 타임스탬프 제거; 시간 해상도 불일치는 에이전트가 점검. |

---

[readme-skill] DONE — `skills/validate-model-output/README.md`
