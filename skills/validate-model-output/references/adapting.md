# 샘플 적응 가이드 (Adapting Samples to Real Data)

> `scripts/`의 파일들은 **"대략적 구조 파악 + 적응의 출발점이 되는 SAMPLE"**이다.
> 이 가이드는 샘플을 실데이터에 맞게 적응하는 핵심 패턴을 짧게 정리한다.

---

## 1. 포맷 감지 & 열기

```python
from io_detect import open_dataset   # 자동 포맷 감지 → Dataset 래퍼 반환 (coord_kind/variables() 사용 가능)
from dataset import open_nc          # NetCDF 직접 → xr.Dataset 반환 (d.xr 없이 xr API 사용)
# detect_domain 등 Dataset 메서드가 필요하면 open_dataset 사용
# xr API 직접 접근이면 open_nc 또는 d.xr 사용
```

| 상황 | 대처 |
|------|------|
| 한글 경로 NetCDF | `open_nc(path)` — engine 자동 폴백(h5netcdf→scipy) |
| NetCDF 쓰기 한글 경로 | `dataset.write_nc(ds, dest, **kw)` 경유 |
| CSV cp949 | `pd.read_csv(path, encoding='cp949')` |
| 미지 포맷(`openable=false`) | `head_hex` 확인 → 즉석 throwaway 파서 작성 |

---

## 2. 비정형 Mesh (WW3 UGRID 등)

**증상**: `coord_kind()` 가 `'none'`, `latlon()` 이 `None` 반환.
**원인**: lat/lon 이 좌표(coord)가 아닌 data variable 에 저장된 mesh 구조.

```python
# 즉석 점검 — 변수명 확인 후 버린다
d = open_nc("model.nc")
print(d.data_var_names())          # 'longitude','latitude' 등을 찾는다
lon = d.xr["longitude"].values     # shape: (node,)
lat = d.xr["latitude"].values
hs  = d.xr["hs"].values            # shape: (time, node)
```

최근접 노드 검색은 `scipy.spatial.cKDTree` 사용.
`tri`(연결정보), `MAPSTA`(상태맵)는 분석 대상이 아닌 구조 변수 — 파악만 하고 건너뛴다.

---

## 3. 한글 컬럼명 CSV (부이 관측)

```python
df = pd.read_csv("buoy.csv", encoding="cp949")
alias = {
    "일시": "time", "지점": "station",
    "유의파고": "hs_obs", "파향": "dir_obs",
    "파주기": "tp_obs", "수온": "sst_obs",
    "풍속": "wspd_obs", "풍향": "wdir_obs",
}
df = df.rename(columns={k: v for k, v in alias.items() if k in df.columns})
df["time"] = pd.to_datetime(df["time"])
```

컬럼명은 실데이터마다 다르다 — `df.columns.tolist()` 로 확인 후 alias 조정.

---

## 4. 도메인 판별 & 변수명 매핑

```python
from router import detect_domain
result = detect_domain(d)
# {'domain': 'waves', 'confidence': 0.6, 'matched': {'hs': 'waves'}}
```

`confidence < 0.3` 이면 `d.variables()` 전체를 출력해 수동으로 도메인 확인.
`config/domains.yaml` 에 없는 변수는 `name_patterns` 또는 `standard_names` 에 추가.

---

## 5. 점 매치업 (모델 격자 → 관측 지점)

```python
from scipy.spatial import cKDTree
import numpy as np

tree = cKDTree(np.column_stack([lon_model, lat_model]))   # 2D 또는 node 배열
_, node_idx = tree.query([lon_obs, lat_obs])               # 최근접

# 시간 매칭
t_idx = np.argmin(np.abs(times_model - np.datetime64(t_obs)))
hs_at_buoy = hs_model[t_idx, node_idx]
```

허용 거리 임계(예: 0.5°)와 허용 시간 임계(예: 30분)를 설정해 먼 매치업은 제외.
실데이터의 시간 해상도(1h·3h·6h)에 따라 임계를 조정.

---

## 6. 파향 원형통계 (0/360° 경계 처리 필수)

```python
import numpy as np

def wrap_angle(deg):
    """각도 차를 (-180, 180] 로 wrap."""
    return np.degrees(np.angle(np.exp(1j * np.deg2rad(deg))))

d_diff = wrap_angle(dir_model - dir_obs)
circ_bias = float(np.degrees(np.arctan2(
    np.mean(np.sin(np.deg2rad(d_diff))),
    np.mean(np.cos(np.deg2rad(d_diff)))
)))
circ_rmse = float(np.sqrt(np.mean(wrap_angle(d_diff)**2)))
```

방향 규약(meteorological "오는 곳" vs oceanographic "향하는 곳")을 모델·부이 간 통일 필수.
저파고(Hs < 0.5 m) 구간은 파향 신뢰도 낮음 — 임계 필터 권장.

---

## 7. 3축 + §G 원칙 (단일 지표 금지)

| 축 | 최소 요소 | 카탈로그 참조 |
|----|----------|--------------|
| 정확도+편향 | bias·RMSE·SI·R | `project/research/01_error_statistics.md` |
| 패턴/위상 | 시계열 overlay + 잔차 패널 | `project/research/06_timeseries_signal.md` |
| 분포 | QQ·파랑장미·PDF/CDF | `project/research/figures/18_fig_waves.md` |
| §G | 캡션: reference≠truth, 임계=advisory, 대표성 오차 | `project/research/00_overview_taxonomy.md §G` |

---

## 8. QC 규칙 추가 (rules.yaml 확장)

`config/rules.yaml` 에 없는 변수는 throwaway 로 범위를 확인한 뒤 추가:

```yaml
# config/rules.yaml 에 추가
- name: custom_wave_period
  match_name: ["tp_obs", "t01", "tm01"]
  valid_min: 1.0
  valid_max: 30.0
  units_any: "s"
  max_missing_frac: 0.1
```

도메인 특화 규칙이 없으면 `check_variable()` 은 통계적 이상치(N-sigma) 만 적용한다 — WARN 으로 나와도 분석 가능.

---

## 9. throwaway 구조점검 코드 — 언제 쓰나 & 원칙

### 9-a. 증상 → throwaway 작성 트리거

아래 증상 중 하나라도 보이면 즉석 구조점검 코드를 먼저 쓰고, 결과 확인 후 본 분석으로 넘어간다.

| 증상 | 확인할 것 | throwaway 코드 (핵심) |
|------|-----------|----------------------|
| `coord_kind()` → `'none'` / `latlon()` → `None` | Mesh: lat·lon이 data variable에 저장됨 | `print(d.data_var_names())` → `d.xr["latitude"].values.shape` |
| CSV `UnicodeDecodeError` | cp949/EUC-KR 한글 인코딩 | `pd.read_csv(path, encoding='cp949').columns.tolist()` |
| `io_detect` 가 `openable=False` 반환 | 미지 바이너리·독점 포맷 | `open(path,'rb').read(16).hex()` — magic bytes 확인 |
| 변수명 alias 매핑 실패 | 한글·약자·로컬 컬럼명 | `df.columns.tolist()` 전체 출력 후 수동 alias 작성 |
| 도메인 `confidence < 0.3` | 변수명이 비표준 | `d.variables()` 전체 + `d.xr[var].attrs` 출력 |
| 시간 오프셋(9h 어긋남 의심) | TZ 미기재 CSV | `df['time'].iloc[:3]` 로 첫 타임스탬프 확인 후 사용자 질문 |
| 모델·관측 변수 단위 불일치 | K vs °C, m/s vs kt | `d.xr[var].attrs.get('units', '?')` 출력 |
| NetCDF 엔진 오류 | h5netcdf 실패 → scipy 폴백 필요 | `xr.open_dataset(path, engine='scipy')` 시도 |

### 9-b. throwaway 작성 원칙

1. 파일 상단에 `# throwaway — 구조 확인 후 삭제` 주석.
2. `print()` 위주로 짧게 — 저장 불필요.
3. 결과를 사용자에게 보고 후 도메인 맞춤 본 코드 작성으로 넘어간다.
4. no-crash 유지: 예외는 `try/except` 로 잡고 메시지 출력.

---

## 10. 시간대(TZ) 정규화 (★)

관측(부이 등)과 모델의 시간축 TZ가 다르면 매칭에서 최대 9h 오차가 생긴다.

**확인 순서**:
1. NetCDF — `d.xr["time"].attrs.get("units", "")` 로 CF units 확인 ("hours since … UTC" 등).
2. CSV — 보통 TZ 표기 없음. 컬럼 값이 "+09:00" 포함 시 파악; 없으면 사용자에 질문.
3. 부이: KST(UTC+9) 흔함. 모델: 보통 UTC.

```python
from preprocess import tz_to_utc
times_utc, assumed = tz_to_utc(times, tz="KST")   # tz=None → UTC가정, assumed=True
# assumed=True면 리포트 경고: "TZ 미확인=UTC가정; KST면 9h 어긋남 위험"
```

`tz_to_utc` 시그니처: `(times, tz=None) -> (times_utc, assumed: bool)`
- `tz='UTC'` → 그대로 통과.
- `tz='KST'` 또는 `'+09:00'` → −9h 적용 후 UTC 반환.
- `tz=None` → UTC 가정, `assumed=True`.

---

## 11. 점관측 좌표 주입 — R3-b (★)

점관측 CSV에 lat/lon 컬럼이 없는 경우 좌표를 외부에서 주입한다.
**코어 자동 경로에 points.list 전용 파서를 내장하지 말 것** — 범용 주입구만 사용.

**처리 순서**:
1. 같은 폴더·상위 폴더에서 좌표 파일 탐색 (points.list, stations.csv, station_info.xlsx 등).
2. 파일이 없으면 사용자에게 형식·경로를 물어본다.
3. 형식을 실시간으로 파악해 `{정점ID: (lat, lon)}` 매핑을 생성한다.
4. `preprocess.inject_point_coords(station_ids, mapping)` 으로 주입.

```python
from preprocess import inject_point_coords, parse_points_list

# parse_points_list: 에이전트/CLI가 명시 호출 — 코어 자동경로 삽입 금지
mapping = parse_points_list("path/to/points.list")   # best-effort 파서
# 또는 실시간 파악해 직접 구성
mapping = {"STN001": (35.12, 129.04), "STN002": (33.46, 126.93)}

lats, lons = inject_point_coords(df["station"].values, mapping)
# lats, lons를 이후 cKDTree 매칭에 사용
```

---

## 12. 카탈로그(01~15, figures 16~22)를 레시피로 쓰는 법

> 목표: 도메인이 정해지면 `project/research/` 카탈로그를 레시피 매뉴얼처럼 꺼내 쓴다.
> `00_overview_taxonomy.md` §C절(도메인 → default bundle 표)이 시작점이다.

### 12-a. 3단계 진입법

```
1. 도메인 판별
   router.detect_domain(d)  →  {'domain':'waves', 'confidence':0.8, ...}
   판별 결과를 §C-1 표 (00_overview_taxonomy.md) 에서 찾는다.

2. default bundle 선정
   C-0(공통 전처리·오차통계·Taylor·Target·유의성)  ← 항상 선행
   + C-1[domain] 표의 메서드 묶음
   + C-2 비도메인 트리거(앙상블축 / AI산출물 / 극값 감지 시 추가)

3. 카드 → 함수 매핑
   각 방법 카드(예: Hs SI, Perkins PDF score, QQ) →
   scripts/ 안 대응 함수 찾기:
     metrics_basic.py  ← bias·RMSE·SI·r·NSE·HH
     metrics_circular.py ← circ_rmse·circ_bias
     metrics_distribution.py ← ks_stat·perkins_ss·wasserstein
     plots.py ← scatter·qq·taylor·rose·diff
```

### 12-b. 도메인별 핵심 카드 빠른 참조

| 도메인 | 1차 지표 카드 | 분포/극값 카드 | 시각화 카드 | 카탈로그 파일 |
|--------|--------------|--------------|------------|--------------|
| 기상 | bias·RMSE·S1·ACC | POD·FAR·CSI·FSS·QQ | Taylor·Target·rose·diff map | `07` + `01` `02` `03` |
| 파랑 | bias·RMSE·**SI**·r·HH·Willmott-d | QQ·Perkins·POT·return-period | scatter·QQ·Taylor·rose | `08` + `01` `03` |
| 수온·염분 | bias·RMSE·MAD | PDF·Perkins·KS | scatter·QQ·section·T-S | `09` + `01` |
| 해류·조류 | RMSE·복소상관·Kundu | 속력 QQ·극값 | rose·Taylor·타원 | `10` + `01` `04` |
| 해수면·조위 | 진폭오차·지각오차·residual | GEV·POT·surge POD | 시계열 overlay·scatter | `11` + `01` `03` |
| AI/ML 출력 | RMSE·MAE·ACC·SSIM | QQ·KS·Wasserstein·CRPS | Taylor·QQ·spatial-diff | `14` + `01` `02` |

### 12-c. figures 16~22 그림 카드 쓰는 법

그림 카드 = "어디서·어떻게 틀렸나" 시각화. 짝지표(수치) 카드와 항상 함께 쓴다.

| 파일 | 주요 그림 유형 | 언제 끌어쓰나 |
|------|--------------|--------------|
| `16_fig_common.md` | 산점도·QQ·오차 히스토그램·Taylor·Target | 모든 도메인 공통 1순위 |
| `17_fig_meteorology.md` | 풍향 장미·FSS 그래프·bias map·scorecard | 기상 recipe 끝단 |
| `18_fig_waves.md` | 파랑 장미·E(f) 스펙트럼·scatter(Hs·Tp)·return-level | 파랑 recipe 필수 |
| `19_fig_temp_salinity.md` | T-S diagram·수직 단면·OHC 시계열 | 수온·염분 recipe |
| `20_fig_currents.md` | 조류 타원·hodograph·EKE map | 해류 recipe |
| `21_fig_sea_level.md` | 조석 잔차·폭풍해일 scatter·return-level curve | 해수면 recipe |
| `22_fig_satellite.md` | matchup density scatter·along-track diff | 위성 colocation 후 |

**캡션 필수 3원칙** (00 §G 강제):
1. "모델 − 기준(reference)"으로 표기 — "오차"라 단정 금지.
2. 임계선은 "참고선(advisory)" 주석 + 영역·해상도 의존 경고.
3. 그림 1장으로 결론 금지 — 최소 정확도·편향·분포 3축 병기.

---

## 13. 4대 원칙 — no-crash · 재현성 · §G 함정 · 하드코딩 금지

### 13-a. no-crash

- 에이전트가 분석 중 예외를 내면 사용자가 결과를 못 받는다.
- 모든 throwaway·본 코드에서 `try/except Exception as e: print(f"[WARN] {e}")` 로 흡수.
- 결측·NaN·shape 불일치는 WARN 출력 후 해당 스텝 건너뛰기(분석 전체 중단 금지).

```python
try:
    result = run_qc(ds, domain="waves")
except Exception as e:
    print(f"[WARN] run_qc 실패: {e}. QC 없이 계속.")
    result = None
```

### 13-b. 재현성

- **같은 입력 → 바이트 동일 리포트**가 보장돼야 채점·디버그가 가능하다.
- 금지: `random.seed` 없는 샘플링, `datetime.now()` 하드코드, 실행순서 의존 전역 상태.
- `json.dumps(report, sort_keys=True, ensure_ascii=False)` — 키 순서 고정.
- `np.random.default_rng(seed=42)` — 부트스트랩 CI 재현.
- 파일 경로는 절대경로가 아닌 **파라미터**로 주입(하드코딩 금지 연계).

### 13-c. §G 함정 (자동 분석이 틀린 결론을 대량생산하지 않으려면)

`00_overview_taxonomy.md §G` 6개 원칙 요약:

| # | 원칙 | 구현 강제 |
|---|------|----------|
| G1 | ERA5/GLORYS = reference, not truth | 보고문 자동 문구: "모델−기준(reference) 차이" |
| G2 | 동화 공유 시 차이 과소평가 | 자료 출처 확인 후 보고문에 경고 주석 |
| G3 | 재분석/L4 위성은 TC 독립 관측 금지 | TC 3자 선택 시 assert 독립성 |
| G4 | 해석 임계는 advisory | `SI<0.15`, `ACC≥0.6` 등은 "참고선" + 도메인 경고 |
| G5 | "(확인요)" 출처 확정 인용 금지 | 보고문에 "(확인요)" 표시 유지 |
| G6 | 단일 지표 금지 | recipe 최소 3축(정확도+편향+분포), 유의성 동반 |

### 13-d. 하드코딩 금지

- 경로·임계·변수명·도메인·TZ를 코드 안에 고정하지 않는다.
- 모든 임계: `config/rules.yaml` 또는 함수 파라미터.
- 변수명 alias: `config/domains.yaml` + `scripts/aliases.py`.
- 파일 경로: CLI 인수 또는 `validate(model_path=..., ref_path=...)` 파라미터.
- TZ: `tz_to_utc(times, tz=user_specified_or_None)` — 상수 `-9` 하드코딩 금지.

```python
# 금지 예시
hs_model = ds["hs_ww3"].values - 273.15  # 단위 변환을 상수로 박음

# 권장 예시
from preprocess import normalize_units
hs_model = normalize_units(ds["hs_ww3"], target_unit="m")
```

---

## 참조

- `scripts/dataset.py` — `open_nc`, `Dataset`, `Variable` 인터페이스
- `scripts/io_detect.py` — 포맷 자동감지, `open_dataset`
- `scripts/preprocess.py` — `tz_to_utc`, `inject_point_coords`, `parse_points_list`, `match_points_to_mesh`, `build_pairs`, `common_time_index`
- `scripts/router.py` — `detect_domain`
- `scripts/qc.py` — `run_qc`, `check_variable`, `check_grid`, `check_time`
- `tests/synth_waves.py` — WW3 mesh + 부이 cp949 합성 SAMPLE (구조 참조용)
- `project/research/00_overview_taxonomy.md` — §C(도메인→recipe), §G(함정 6원칙), 카탈로그 색인
- `project/research/01_error_statistics.md` — bias·RMSE·SI·r·Taylor·Target 카드
- `project/research/08_domain_waves.md` — 파랑 검증 지표 카탈로그
- `project/research/figures/16_fig_common.md` — 공통 그림 카드(산점도·QQ·Taylor·Target)
- `project/research/figures/18_fig_waves.md` — 파랑 그림 카탈로그
- `project/research/15_preprocessing_regridding_colocation.md` — 전처리·matchup·QC 카드
