# 시스템 설계 (System Architecture)

> **validate-model-output** 스킬의 설계 철학·데이터 흐름·모듈 책임·확장점을 기술한다.

---

## 1. 핵심 설계 철학

### 결정적 코어 (Deterministic Core) vs 에이전트 껍질 (Live-Adaptive Agent Shell)

```
┌──────────────────────────────────────────────────────────────────┐
│  에이전트 껍질 (SKILL.md — live-adaptive)                        │
│  - 실데이터 구조 실시간 점검 (throwaway 코드)                    │
│  - 사용자 질문 유도 (4-페이즈: discover→elicit→analyze→report)   │
│  - 도메인 맞춤 코드 작성·즉석 적응                              │
│  - §G 함정 경고 (reference≠truth, 임계=advisory)                │
├──────────────────────────────────────────────────────────────────┤
│  결정적 코어 (scripts/ + config/*.yaml — 재현성 100%)            │
│  - 포맷 감지·Dataset 추상화·도메인 라우팅                       │
│  - 층위1 QC (값범위·결측·격자·시간)                             │
│  - 메트릭 계산 (bias/RMSE/SI/r + 원형 + 분포 + 패턴)            │
│  - 그림 생성 (scatter/QQ/taylor/rose/diff_map/timeseries)        │
│  - 리포트 렌더링 (json + md, §G 강제)                           │
└──────────────────────────────────────────────────────────────────┘
```

**scripts/** 파일들은 "대략적 구조 파악 + 적응의 출발점이 되는 SAMPLE"이다.
실데이터에서 안 맞는 부분은 **에이전트가 실시간으로 점검·도메인 맞춤 코드로 교체**한다.
코어 자체는 바꾸지 않으며, 확장은 `config/*.yaml` 로 한다.

---

## 2. 데이터 흐름 (Data Flow)

```
입력 파일 (NetCDF3/4 · CSV · unknown)
         │
         ▼
  [io_detect.py]
  포맷 감지 + 인코딩 폴백 (h5netcdf→scipy; cp949→utf-8)
  open_dataset() → Dataset 래퍼 반환
  미지 포맷: openable=false + head_hex
         │
         ▼
  [dataset.py — Dataset 추상화]
  coord_kind()  → '1d' | '2d' | 'mesh' | 'none'
  latlon()      → (lat_name, lon_name, is_2d) | None
  data_var_names(), variables()
  xr            → xarray.Dataset 직접 접근
         │
         ├─────────────────────────────────────────────┐
         ▼                                             ▼
  [QC 경로]                                   [verify 경로]
  [qc.py / rules.py]                          [preprocess.py]
  run_qc(d) →                                 tz_to_utc()
    check_variable (값범위·결측·fill)           inject_point_coords()
    check_grid (좌표 단조성)                    match_points_to_mesh()
    check_time (단조성·간격)                    common_time_index()
    층위1 QC dict                              build_pairs()
         │                                             │
         ▼                                             ▼
  [router.py]                               [metrics_basic.py]
  detect_domain(d) →                          bias / rmse / si / pearson_r
    domain / confidence / matched            [metrics_circular.py]
  aliases.py 한글↔영문 매핑                   circular_mean_error / circular_rmse
                                             [metrics_distribution.py]
                                              perkins_ss / ks_stat / qq_quantiles
                                             [metrics_pattern.py]
                                              lag_correlation / pattern_rmse
                                             [derive.py]
                                              wind_speed(u, v)
                                             [regions.py]
                                              crop_grid_mask / crop_mesh_mask
                                             [plots.py]
                                              scatter_si / qq_plot / taylor_diagram
                                              wave_rose / diff_map / timeseries_overlay
         │                                             │
         └──────────────────┬──────────────────────────┘
                            ▼
                     [report.py]
                     write_report()       → qc_report.json + qc_report.md
                     write_verify_report()→ verify_report.json + verify_report.md
                     §G 캡션 강제 삽입
```

---

## 3. Dataset 추상화 (`scripts/dataset.py`)

포맷·경로에 무관한 단일 인터페이스를 제공한다.

| 메서드 | 반환 | 설명 |
|--------|------|------|
| `coord_kind()` | `'1d'` \| `'2d'` \| `'mesh'` \| `'none'` | 좌표 구조 분류 |
| `latlon()` | `(lat_name, lon_name, is_2d)` \| `None` | 위경도 변수명 탐색 |
| `data_var_names()` | `list[str]` | 데이터 변수 이름 목록 |
| `variables()` | `list[Variable]` | 변수 메타(이름·dtype·shape·units·§G) |
| `.xr` | `xarray.Dataset` | xr API 직접 접근 |

```python
from io_detect import open_dataset   # Dataset 래퍼 (coord_kind / variables 필요)
from dataset   import open_nc        # xr.Dataset 직접 (d.xr 없이 xr API)
```

**한글 경로 지원**: `open_nc()` 는 `h5netcdf` → `scipy` 엔진 순서로 폴백.
NetCDF 쓰기에는 `dataset.write_nc(ds, dest, **kw)` 를 경유한다.

**mesh 구조**: `coord_kind()='mesh'` 이면 lat/lon 이 data_var 에 저장된 비정형 UGRID.
`d.xr["latitude"].values` 로 node 배열을 직접 추출한다.

---

## 4. 도메인 라우팅 & 별칭 (`router.py`, `aliases.py`, `config/domains.yaml`)

```python
result = detect_domain(d)
# {'domain': 'waves', 'confidence': 0.6, 'matched': {'hs': 'waves'}}
```

- `config/domains.yaml` 에 `name_patterns` / `standard_names` 키로 도메인 확장.
- `confidence < 0.3` → `d.variables()` 전체 출력 후 수동 확인.
- 한글 컬럼명은 `aliases.py` 에서 영문 표준명으로 매핑한다.

```python
# aliases.py 한글 컬럼명 예시 매핑
{
    "일시": "time",   "유의파고": "hs",  "파향": "dir",
    "파주기": "tp",   "수온": "sst",    "풍속": "wspd", "풍향": "wdir",
}
```

---

## 5. 전처리 (`scripts/preprocess.py`)

### 5-1. 시간대 정규화 (`tz_to_utc`)

```
tz=None      → UTC 가정, assumed=True  (리포트에 "TZ 미확인" 경고 삽입)
tz='UTC'     → 그대로, assumed=False
tz='KST'     → -9h 적용 UTC 반환, assumed=False
tz='+09:00'  → 동일 KST 처리
```

부이(KST) vs 모델(UTC) 불일치 → 시간 매칭 최대 9h 오차.
에이전트는 시간 메타를 확인 후 사용자에게 TZ 명시를 요청해야 한다.

### 5-2. 단위 정규화 (`to_kelvin`)

온도 변수(`t2m`, `sst`, `temp`, …)에서 `°C` ↔ `K` 자동 변환.
알 수 없는 단위 → 변환 없이 반환 + `UserWarning`.

### 5-3. mesh → 점 최근접 매칭 (`match_points_to_mesh`)

```
cKDTree(mesh_lon, mesh_lat) → query(pt_lon, pt_lat)
cos 보정 평면 근사 거리 계산 → max_km 초과 → index=-1(제외)
```

SAMPLE 범위: 구면 거리 근사. 고위도·장거리는 `pyproj` / `BallTree(Haversine)` 로 대체.

### 5-4. 정점 좌표 주입 (`inject_point_coords`, `parse_points_list`)

점관측 CSV 에 lat/lon 컬럼이 없을 때 외부 좌표 파일로 주입.
`parse_points_list` 는 **에이전트/CLI 명시 호출 전용** — 코어 자동 경로에 박지 말 것.

```
좌표 탐색 순서:
  1) --points 파일 + 기준 파일 내 정점 ID 컬럼
  2) 기준 파일 내 lat/lon 컬럼/좌표
  없으면 → 사용자에게 질문
```

### 5-5. 교집합 시간 인덱스 (`common_time_index`)

```python
idx_m, idx_r = common_time_index(mt_utc, rt_utc)
model_common = model_vals[idx_m]
ref_common   = ref_vals[idx_r]
```

---

## 6. 검증 메트릭 배터리 (다축, 단일 지표 금지)

| 축 | 메트릭 | 모듈 |
|----|--------|------|
| 정확도·편향 | bias · RMSE · SI · pearson_r | `metrics_basic` |
| 방향(원형) | circular_mean_error · circular_rmse · circular_corr | `metrics_circular` |
| 분포 | perkins_ss · ks_stat · qq_quantiles | `metrics_distribution` |
| 시간·위상 | lag_correlation · pattern_rmse | `metrics_pattern` |
| 시각화 | scatter_si · qq_plot · taylor_diagram · wave_rose · diff_map · timeseries_overlay | `plots` |
| 해역별 | crop_grid_mask · crop_mesh_mask · region_bbox | `regions` |

**최소 3축 사용 원칙** (§G: 단일 지표 금지).

---

## 7. verify 모드 — 격자 유형별 분기

```
cmd_verify
  │
  ├── model coord_kind in ('1d','2d') & ref coord_kind in ('1d','2d')
  │       → _verify_grid_to_grid()
  │         공통 변수명 교집합 → 단위 정규화 → 정확도/방향 메트릭
  │         → scatter / taylor / QQ / diff_map + wave_rose(방향 변수)
  │         → --regions 해역별 반복
  │
  └── model coord_kind == 'mesh'
          → _verify_mesh_point()
            mesh lat/lon data_var 추출
            → _get_ref_latlon() (--points 우선, 기준파일 lat/lon 차선)
            → match_points_to_mesh(max_km=50)
            → tz_to_utc(model_tz, ref_tz) → common_time_index
            → 교집합 시간 스텝 선택 → 매칭 노드 추출
            → 정확도/방향 메트릭
            → scatter / QQ / timeseries / taylor / diff_map(점) + wave_rose
            → --regions 해역별 반복

  지원 안 되는 조합 → 명확 메시지 + exit 1 (크래시 없음)
```

---

## 8. 적응(Live-Adaptive) 경계

| 코드(scripts) 담당 | 에이전트 실시간 담당 |
|--------------------|---------------------|
| Dataset 추상화·포맷 감지 | 실데이터 변수명 확인·throwaway 코드 |
| 층위1 QC 규칙(yaml 구동) | 이상 범위 확인 후 rules.yaml 확장 |
| 메트릭·그림 함수 구현 | 도메인 맞춤 메트릭 선택·조합 |
| 리포트 §G 캡션 강제 | 분석 해석·advisory 문구 작성 |
| match_points_to_mesh SAMPLE | 실데이터 max_km·CRS 맞춤 조정 |
| common_time_index SAMPLE | TZ 불일치 경고·사용자 질문 |
| alias 매핑 기본 셋 | 실데이터 한글 컬럼명 → alias 보정 |

---

## 9. 확장점 (yaml)

```
config/domains.yaml  — 도메인별 변수 패턴·standard_names 추가
config/rules.yaml    — QC 규칙(범위·결측률·단위) 추가
config/regions.yaml  — 해역 bbox 추가 (동해/남해/서해/황해/동중국해 기본 포함)
```

새 변수·도메인은 스크립트를 수정하지 않고 yaml 만 확장한다.

---

## 10. 마일스톤 요약

| 마일스톤 | 내용 | 상태 |
|----------|------|------|
| M1 기반·발견 | Dataset 추상화 · io_detect · router · discover/inspect · aliases · preprocess(tz·unit·mesh→점) | 완료 |
| M2 QC·검증 | rules · qc · report · cli(discover/inspect/validate/verify) · metrics 전체 · plots · regions | 완료 |
| 파랑·verify 다축 | mesh+점관측 SAMPLE · 원형통계 · timeseries · diff_map · 해역별 분석 · run_acceptance | 완료 |

pytest 421 passed / 0 warnings.
인수테스트 `run_acceptance.py` 5/5 PASS.
재현성: 동일 입력 → report 바이트 동일 (100%).
합성 fixture(hermetic) — 원본 데이터 비의존.

---

## 참조

- `scripts/dataset.py` — Dataset·Variable 추상화, `open_nc`
- `scripts/io_detect.py` — 포맷 감지, `open_dataset`
- `scripts/preprocess.py` — tz_to_utc · inject_point_coords · parse_points_list · match_points_to_mesh · common_time_index
- `scripts/router.py` — `detect_domain`
- `scripts/qc.py` — `run_qc`, `check_variable`, `check_grid`, `check_time`
- `scripts/report.py` — `write_report`, `write_verify_report`, §G 캡션
- `scripts/cli.py` — discover / inspect / validate / verify 서브커맨드
- `config/domains.yaml` — 도메인 변수 패턴
- `config/rules.yaml` — QC 규칙
- `references/adapting.md` — 실데이터 적응 핵심 패턴 (throwaway·mesh·cp949·tz·점관측 좌표)
- `references/usage.md` — 설치·실행·각 서브커맨드 사용법
- `project/research/` — 검증·분석 방법 카탈로그 (~500 방법카드, ~115 그림카드)
