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
| NetCDF 쓰기 한글 경로 | `make_fixtures._write_nc(ds, dest, **kw)` 경유 |
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

## 9. throwaway 코드 작성 원칙

1. 파일 상단에 `# throwaway — 구조 확인 후 삭제` 주석.
2. `print()` 위주로 짧게 — 저장 불필요.
3. 결과를 사용자에게 보고 후 도메인 맞춤 본 코드 작성으로 넘어간다.
4. no-crash 유지: 예외는 `try/except` 로 잡고 메시지 출력.

---

## 참조

- `scripts/dataset.py` — `open_nc`, `Dataset`, `Variable` 인터페이스
- `scripts/io_detect.py` — 포맷 자동감지, `open_dataset`
- `scripts/router.py` — `detect_domain`
- `scripts/qc.py` — `run_qc`, `check_variable`, `check_grid`, `check_time`
- `tests/synth_waves.py` — WW3 mesh + 부이 cp949 합성 SAMPLE (구조 참조용)
- `project/research/08_domain_waves.md` — 파랑 검증 지표 카탈로그
- `project/research/figures/18_fig_waves.md` — 파랑 그림 카탈로그
