# validate-model-output — M2: QC층(validate) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기준자료 없이 파일 하나를 물리·형식 상식에 비춰 점검하는 층위1 QC를 구현한다 — `validate <file>` 가 값범위·결측·격자단조·시간축·스키마를 검사해 PASS/FAIL/WARN + 근거를 담은 `report.json`+`report.md`를 낸다. 규칙은 선언적 `rules.yaml`(유일한 확장점).

**Architecture:** `rules.yaml`(변수→물리범위·임계) → `rules.py`(변수에 맞는 규칙 매칭) → `qc.py`(규칙 구동 변수검사 + 구조검사) → `report.py`(json+md). `cli validate` 가 `io_detect.open_dataset` 로 연 `Dataset` 에 `run_qc` 를 돌려 `report.py` 로 출력. 검증기는 절대 크래시하지 않고 문제를 FAIL/WARN 로 기록.

**Tech Stack:** Python 3.12, numpy, xarray(기존 Dataset 추상화), PyYAML, pytest. (M1에서 구축된 `scripts/` 모듈 재사용.)

## Global Constraints

- M1 인터페이스 재사용(재구현 금지): `dataset.Dataset`(메서드 `data_var_names()`, `variable(name)->Variable`, `variables()->dict`, `latlon()->(lat,lon,is_2d)|None`, `coord_kind()`, `grid_shape()`, `time_info()->{name,n_steps,start,end}|None`, 속성 `.xr`), `dataset.Variable`(필드 `name,dims,shape,units,standard_name,long_name,attrs`), `io_detect.open_dataset(path)->Dataset` / `UnknownFormatError`. 실제 데이터 값은 `d.xr[name].values` 로 접근.
- **크래시 금지**: 모든 검사는 예외를 잡아 해당 항목을 FAIL/WARN 로 기록하고 계속 진행한다. `validate` 는 어떤 입력에도 리포트를 낸다.
- **해석 임계는 advisory**: 물리범위·시그마 등은 참고 기준(영역·변수 의존). 규칙에 없는 변수는 크래시 대신 **WARN + 통계적 이상치(N-시그마)만**.
- **단위 인식**: 같은 물리량이라도 단위(K vs degC, Pa vs hPa)별로 별도 규칙 매칭(M2는 변환 없이 단위별 규칙; 단위 정규화·환산은 M3 preprocess 소관).
- 체크 결과 단위: `{"check": str, "variable": str|None, "status": "PASS"|"FAIL"|"WARN", "evidence": str}` dict. report 는 이 리스트를 소비.
- fixture .nc 는 작게, `skills/validate-model-output/data/` 아래 커밋(.gitignore 예외). 합성으로 hermetic, 실제 원본 로드/커밋 금지. 테스트 출력 pristine(0 warnings).
- 한국어 서술 + 영문 기술용어 병기. 모듈은 `scripts/`, 형제 import. `config/*.yaml` 은 `yaml.safe_load` + `open(encoding="utf-8")`, 경로는 모듈 기준 상대.
- 기준자료=reference(≠truth) — 본 층위1은 기준자료 불필요(intrinsic).

---

### Task 1: `rules.yaml` + `rules.py` (규칙 로드·매칭)

**Files:**
- Create: `skills/validate-model-output/config/rules.yaml`
- Create: `skills/validate-model-output/scripts/rules.py`
- Test: `skills/validate-model-output/tests/test_rules.py`

**Interfaces:**
- Consumes: `dataset.Variable`
- Produces:
  - `load_rules(path=None) -> dict` — `{'rules':[...], 'default':{...}}` (utf-8 yaml, 모듈 상대 경로)
  - `match_rule(var: Variable, rules: dict | None = None) -> dict | None` — 변수에 맞는 규칙 dict 반환(없으면 None). 규칙 매칭: 규칙 순서대로, `(standard_name 일치) or (name_patterns 중 re.search 일치) or (units 일치)` 이고, **규칙에 `units_any`가 있고 변수에 units가 있으면 변수 units가 `units_any`에 있어야** 매칭(단위 불일치 규칙 배제). 첫 매칭 규칙 반환.

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_rules.py`:
```python
from dataset import Variable
from rules import load_rules, match_rule


def _var(name, units=None, standard_name=None):
    return Variable(name=name, dims=("y", "x"), shape=(2, 2),
                    units=units, standard_name=standard_name, long_name=None, attrs={})


def test_load_rules_structure():
    r = load_rules()
    assert "rules" in r and "default" in r
    assert isinstance(r["rules"], list) and len(r["rules"]) >= 1


def test_match_temperature_kelvin():
    rule = match_rule(_var("t2m", units="K", standard_name="air_temperature"))
    assert rule is not None
    assert rule["valid_min"] <= 200 and rule["valid_max"] >= 320  # K 범위


def test_match_temperature_celsius_distinct_from_kelvin():
    # 같은 이름(tmp)이라도 단위가 degC면 K 규칙이 아니라 C 규칙에 매칭
    rule = match_rule(_var("TMP", units="degC"))
    assert rule is not None
    assert rule["valid_min"] < 0 and rule["valid_max"] < 100  # C 범위 (음수 허용)


def test_match_pressure_pa():
    rule = match_rule(_var("PRMSL", units="Pa", standard_name="air_pressure_at_mean_sea_level"))
    assert rule is not None
    assert rule["valid_max"] > 50000  # Pa


def test_no_match_returns_none():
    assert match_rule(_var("mystery", units="widgets")) is None
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_rules.py -v`
Expected: FAIL ("No module named 'rules'")

- [ ] **Step 3: 규칙 파일과 매처 작성**

`skills/validate-model-output/config/rules.yaml`:
```yaml
# 층위1 QC 규칙 (intrinsic, 기준자료 불필요). 변수→물리범위·결측임계.
# 매칭: standard_name / name_patterns(re.search) / units. units_any 있으면 단위 일치 필수.
# 임계는 모두 advisory(영역·변수 의존). 단위 환산 없음 — 단위별 규칙 분리.
rules:
  - name: temperature_K
    standard_names: [air_temperature, sea_water_temperature, sea_surface_temperature, dew_point_temperature]
    name_patterns: ['^t2m$', '^tmp$', '^dpt$', '^t$', 'sst']
    units_any: [K, kelvin, Kelvin]
    valid_min: 180.0
    valid_max: 340.0
    max_missing_frac: 0.6
  - name: temperature_C
    standard_names: [air_temperature, sea_water_temperature, sea_surface_temperature, dew_point_temperature]
    name_patterns: ['^t2m$', '^tmp$', '^dpt$', 'sst']
    units_any: [degC, celsius, Celsius, C, degrees_celsius, "degree_Celsius"]
    valid_min: -90.0
    valid_max: 60.0
    max_missing_frac: 0.6
  - name: wind_component
    standard_names: [eastward_wind, northward_wind]
    name_patterns: ['^u10$', '^v10$', 'ugrd', 'vgrd', '^uo$', '^vo$']
    valid_min: -120.0
    valid_max: 120.0
    max_missing_frac: 0.6
  - name: mslp_Pa
    standard_names: [air_pressure_at_mean_sea_level]
    name_patterns: ['mslp', 'prmsl']
    units_any: [Pa, pascal, Pascal]
    valid_min: 85000.0
    valid_max: 110000.0
    max_missing_frac: 0.6
  - name: precip_rate
    standard_names: [precipitation_flux, rainfall_rate]
    name_patterns: ['prate', 'precip', 'rain']
    valid_min: 0.0
    valid_max: 0.1
    max_missing_frac: 0.6
  - name: salinity
    standard_names: [sea_water_salinity, sea_surface_salinity]
    name_patterns: ['^so$', '^sss$', 'salin']
    valid_min: 0.0
    valid_max: 45.0
    max_missing_frac: 0.6
default:
  max_missing_frac: 0.9
  sigma: 6.0
```

`skills/validate-model-output/scripts/rules.py`:
```python
from __future__ import annotations

import os
import re

import yaml

from dataset import Variable

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "rules.yaml"
)


def load_rules(path: str | None = None) -> dict:
    with open(path or _CONFIG, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data.setdefault("rules", [])
    data.setdefault("default", {})
    return data


def _units_ok(var: Variable, rule: dict) -> bool:
    units_any = rule.get("units_any")
    if not units_any:
        return True
    if var.units is None:
        return True  # 변수에 단위가 없으면 단위 제약을 적용하지 않음
    return var.units.strip() in units_any


def _identity_match(var: Variable, rule: dict) -> bool:
    sn = (var.standard_name or "").lower()
    if sn and sn in [s.lower() for s in rule.get("standard_names", [])]:
        return True
    name = var.name.lower()
    for pat in rule.get("name_patterns", []):
        if re.search(pat, name):
            return True
    units = (var.units or "").strip()
    if units and units in rule.get("units_any", []):
        return True
    return False


def match_rule(var: Variable, rules: dict | None = None) -> dict | None:
    if rules is None:
        rules = load_rules()
    for rule in rules["rules"]:
        if _identity_match(var, rule) and _units_ok(var, rule):
            return rule
    return None
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_rules.py -v`
Expected: PASS (5 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/config/rules.yaml skills/validate-model-output/scripts/rules.py skills/validate-model-output/tests/test_rules.py
git commit -m "feat(validate): rules.yaml + rules.py (unit-aware variable rule matching)"
```

---

### Task 2: `qc.py` 변수 검사 (값범위·결측·이상치)

**Files:**
- Create: `skills/validate-model-output/scripts/qc.py`
- Test: `skills/validate-model-output/tests/test_qc_variable.py`

**Interfaces:**
- Consumes: `dataset.Dataset`, `rules.match_rule`, `rules.load_rules`
- Produces:
  - `check_variable(d: Dataset, name: str, rules: dict) -> list[dict]` — 한 변수의 값범위·결측·이상치 체크 결과 리스트. 규칙 매칭 시 range·missing(FAIL 가능)+이상치(WARN); 규칙 없으면 missing(default 임계)+이상치(WARN)만 + "규칙 없음" WARN. 절대 예외 전파 안 함.
  - 결과 dict 형식: `{"check","variable","status","evidence"}`.

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_qc_variable.py`:
```python
import numpy as np
import xarray as xr
from dataset import Dataset
from rules import load_rules
from qc import check_variable


def _ds_from(name, values, units, standard_name=None):
    da = xr.DataArray(values, dims=("lat", "lon"),
                      coords={"lat": [0, 1, 2], "lon": [0, 1, 2]},
                      attrs={"units": units} | ({"standard_name": standard_name} if standard_name else {}))
    return Dataset(xr.Dataset({name: da}))


def _status(results, check):
    return [r["status"] for r in results if r["check"] == check]


def test_value_range_pass():
    d = _ds_from("t2m", np.full((3, 3), 280.0), "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "PASS" in _status(res, "value_range")


def test_value_range_fail():
    vals = np.full((3, 3), 280.0)
    vals[0, 0] = 500.0  # 물리범위 초과
    d = _ds_from("t2m", vals, "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "FAIL" in _status(res, "value_range")
    ev = [r["evidence"] for r in res if r["check"] == "value_range"][0]
    assert "500" in ev or "1" in ev  # 근거에 초과 개수/값 언급


def test_missing_fail():
    vals = np.full((3, 3), 280.0)
    vals[:, :] = np.nan
    vals[0, 0] = 280.0  # 거의 전부 결측
    d = _ds_from("t2m", vals, "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "FAIL" in _status(res, "missing")


def test_unruled_variable_warns_not_crash():
    d = _ds_from("mystery", np.full((3, 3), 1.0), "widgets")
    res = check_variable(d, "mystery", load_rules())
    # 규칙 없음 → 크래시 없이 WARN 포함
    assert any(r["status"] == "WARN" for r in res)
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_variable.py -v`
Expected: FAIL ("No module named 'qc'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/qc.py`:
```python
from __future__ import annotations

import numpy as np

from dataset import Dataset
from rules import match_rule


def _result(check, status, evidence, variable=None) -> dict:
    return {"check": check, "variable": variable, "status": status, "evidence": evidence}


def check_variable(d: Dataset, name: str, rules: dict) -> list:
    results = []
    try:
        var = d.variable(name)
        arr = np.asarray(d.xr[name].values, dtype="float64")
    except Exception as e:  # 값 접근 실패도 크래시 대신 FAIL
        return [_result("value_access", "FAIL", f"변수 값 접근 실패: {e}", name)]

    finite = np.isfinite(arr)
    n = arr.size
    n_missing = int(n - finite.sum())
    missing_frac = n_missing / n if n else 1.0

    rule = match_rule(var, rules)
    default = rules.get("default", {})

    # 결측 검사
    max_missing = (rule or {}).get("max_missing_frac", default.get("max_missing_frac", 0.9))
    if missing_frac > max_missing:
        results.append(_result("missing", "FAIL",
            f"결측비율 {missing_frac:.2%} > 임계 {max_missing:.0%} ({n_missing}/{n})", name))
    else:
        results.append(_result("missing", "PASS",
            f"결측비율 {missing_frac:.2%} ≤ 임계 {max_missing:.0%}", name))

    vals = arr[finite]
    if rule is not None and "valid_min" in rule and "valid_max" in rule:
        lo, hi = rule["valid_min"], rule["valid_max"]
        out = (vals < lo) | (vals > hi)
        n_out = int(out.sum())
        if n_out > 0:
            sample = np.unique(np.round(vals[out], 2))[:5]
            results.append(_result("value_range", "FAIL",
                f"물리범위 [{lo}, {hi}] {rule.get('units_any', '')} 벗어난 값 {n_out}개 (예: {list(sample)})", name))
        else:
            results.append(_result("value_range", "PASS",
                f"전 값 물리범위 [{lo}, {hi}] 이내 (규칙 {rule['name']}, advisory)", name))
    else:
        results.append(_result("rule", "WARN",
            f"변수 '{name}'에 맞는 물리범위 규칙 없음 → 통계적 이상치만 점검(advisory)", name))

    # 이상치(N-시그마) — WARN
    sigma = (rule or {}).get("sigma", default.get("sigma", 6.0))
    if vals.size >= 8 and np.std(vals) > 0:
        z = np.abs(vals - np.mean(vals)) / np.std(vals)
        n_outlier = int((z > sigma).sum())
        if n_outlier > 0:
            results.append(_result("outlier", "WARN",
                f"{sigma}σ 초과 이상치 {n_outlier}개 (advisory)", name))
        else:
            results.append(_result("outlier", "PASS", f"{sigma}σ 초과 이상치 없음", name))
    return results
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_variable.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/qc.py skills/validate-model-output/tests/test_qc_variable.py
git commit -m "feat(validate): qc.check_variable (unit-aware range + missing + N-sigma outlier, no-crash)"
```

---

### Task 3: `qc.py` 구조 검사 (격자 단조·형상·시간축·스키마)

**Files:**
- Modify: `skills/validate-model-output/scripts/qc.py`
- Test: `skills/validate-model-output/tests/test_qc_structure.py`

**Interfaces:**
- Consumes: `dataset.Dataset`
- Produces (qc.py에 추가):
  - `check_grid(d: Dataset) -> list[dict]` — lat/lon 존재; 1D면 단조(증가 또는 감소) 검사; 2D면 lat/lon 형상 일치 검사. 좌표 없으면 WARN.
  - `check_time(d: Dataset) -> list[dict]` — time_info 있으면 타임스탬프 단조 증가·중복 없음 검사. 없으면 결과 없음(빈 리스트).
  - `check_schema(d: Dataset) -> list[dict]` — 데이터 변수 1개 이상 존재 확인.
  - 모두 예외를 잡아 FAIL 로 기록(크래시 금지).

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_qc_structure.py`:
```python
import numpy as np
import xarray as xr
from dataset import Dataset
from qc import check_grid, check_time, check_schema


def _status(results, check):
    return [r["status"] for r in results if r["check"] == check]


def _grid_ds(lat):
    da = xr.DataArray(np.zeros((len(lat), 3)), dims=("lat", "lon"),
                      coords={"lat": lat, "lon": [0, 1, 2]}, attrs={"units": "K"})
    return Dataset(xr.Dataset({"t2m": da}))


def test_grid_monotonic_pass():
    assert "PASS" in _status(check_grid(_grid_ds([0.0, 1.0, 2.0])), "grid_monotonic")


def test_grid_nonmonotonic_fail():
    assert "FAIL" in _status(check_grid(_grid_ds([0.0, 2.0, 1.0])), "grid_monotonic")


def test_grid_descending_is_pass():
    # 위도 내림차순은 정상(많은 자료가 북→남)
    assert "PASS" in _status(check_grid(_grid_ds([2.0, 1.0, 0.0])), "grid_monotonic")


def test_time_duplicate_fail():
    t = np.array(["2022-09-06T00", "2022-09-06T00", "2022-09-06T06"], dtype="datetime64[h]")
    da = xr.DataArray(np.zeros((3, 2, 2)), dims=("time", "lat", "lon"),
                      coords={"time": t, "lat": [0, 1], "lon": [0, 1]}, attrs={"units": "K"})
    res = check_time(Dataset(xr.Dataset({"t2m": da})))
    assert "FAIL" in _status(res, "time_axis")


def test_time_monotonic_pass():
    t = np.array(["2022-09-06T00", "2022-09-06T06", "2022-09-06T12"], dtype="datetime64[h]")
    da = xr.DataArray(np.zeros((3, 2, 2)), dims=("time", "lat", "lon"),
                      coords={"time": t, "lat": [0, 1], "lon": [0, 1]}, attrs={"units": "K"})
    res = check_time(Dataset(xr.Dataset({"t2m": da})))
    assert "PASS" in _status(res, "time_axis")


def test_schema_has_vars():
    assert "PASS" in _status(check_schema(_grid_ds([0.0, 1.0])), "schema")
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_structure.py -v`
Expected: FAIL ("cannot import name 'check_grid'")

- [ ] **Step 3: qc.py 에 함수 추가**

`skills/validate-model-output/scripts/qc.py` 끝에 추가:
```python
def check_schema(d: Dataset) -> list:
    try:
        names = d.data_var_names()
    except Exception as e:
        return [_result("schema", "FAIL", f"스키마 읽기 실패: {e}")]
    if not names:
        return [_result("schema", "FAIL", "데이터 변수가 없음")]
    return [_result("schema", "PASS", f"데이터 변수 {len(names)}개: {names[:6]}")]


def check_grid(d: Dataset) -> list:
    try:
        ll = d.latlon()
    except Exception as e:
        return [_result("grid", "FAIL", f"좌표 읽기 실패: {e}")]
    if ll is None:
        return [_result("grid", "WARN", "lat/lon 좌표를 찾지 못함(비격자 자료일 수 있음)")]
    lat_name, lon_name, is_2d = ll
    results = []
    try:
        if is_2d:
            lat = np.asarray(d.xr[lat_name].values)
            lon = np.asarray(d.xr[lon_name].values)
            if lat.shape == lon.shape:
                results.append(_result("grid_shape", "PASS",
                    f"2D 좌표 형상 일치 {lat.shape}"))
            else:
                results.append(_result("grid_shape", "FAIL",
                    f"2D lat{lat.shape} ≠ lon{lon.shape} 형상 불일치"))
        else:
            lat = np.asarray(d.xr[lat_name].values, dtype="float64")
            diffs = np.diff(lat)
            mono = np.all(diffs > 0) or np.all(diffs < 0)
            if mono:
                results.append(_result("grid_monotonic", "PASS",
                    f"위도 단조({'증가' if diffs[0] > 0 else '감소'})"))
            else:
                bad = int(np.argmin(diffs > 0)) if np.any(diffs <= 0) else -1
                results.append(_result("grid_monotonic", "FAIL",
                    f"위도 비단조 @ index≈{bad} (값 {lat[max(bad,0)]:.3f})"))
    except Exception as e:
        results.append(_result("grid", "FAIL", f"격자 검사 실패: {e}"))
    return results


def check_time(d: Dataset) -> list:
    try:
        ti = d.time_info()
    except Exception as e:
        return [_result("time_axis", "FAIL", f"시간축 읽기 실패: {e}")]
    if ti is None:
        return []
    try:
        tname = ti["name"]
        tvals = np.asarray(d.xr[tname].values)
        if tvals.size <= 1:
            return [_result("time_axis", "PASS", f"시간 스텝 {tvals.size}개")]
        order = np.sort(tvals)
        n_dup = int(tvals.size - np.unique(tvals).size)
        mono = bool(np.all(tvals == order))
        if n_dup > 0:
            return [_result("time_axis", "FAIL", f"타임스탬프 중복 {n_dup}개")]
        if not mono:
            return [_result("time_axis", "FAIL", "타임스탬프 비단조(시간 역행)")]
        return [_result("time_axis", "PASS", f"시간 단조·중복없음 ({tvals.size} 스텝)")]
    except Exception as e:
        return [_result("time_axis", "FAIL", f"시간축 검사 실패: {e}")]
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_structure.py -v`
Expected: PASS (6 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/qc.py skills/validate-model-output/tests/test_qc_structure.py
git commit -m "feat(validate): qc grid/time/schema structural checks (monotonic, dup, shape)"
```

---

### Task 4: `run_qc` 오케스트레이션 + 고의결함 fixture (정상=PASS / 결함=FAIL)

**Files:**
- Modify: `skills/validate-model-output/scripts/qc.py`
- Modify: `skills/validate-model-output/scripts/make_fixtures.py`
- Modify: `skills/validate-model-output/tests/synth.py`
- Test: `skills/validate-model-output/tests/test_qc_run.py`
- (실행 산출물) `skills/validate-model-output/data/broken_era5_like.nc`

**Interfaces:**
- Consumes: `check_variable/check_grid/check_time/check_schema`, `rules.load_rules`, `io_detect.open_dataset`
- Produces:
  - `run_qc(d: Dataset, rules: dict | None = None) -> dict` — `{"checks":[...], "summary":{"PASS":n,"FAIL":n,"WARN":n}, "ok": bool}`. ok = FAIL 0개. 구조검사(schema/grid/time) 1회 + 전 변수 `check_variable`.
  - `synth.broken_era5_like() -> xr.Dataset` — era5_like 기반, t2m에 값범위초과(500K) + 결측구멍 + 위도 비단조 주입.
  - `make_fixtures.main()` 가 `data/broken_era5_like.nc` 도 작성.

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_qc_run.py`:
```python
import os
import xarray as xr
from dataset import Dataset
from io_detect import open_dataset
from qc import run_qc
from synth import era5_like, broken_era5_like

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def test_clean_all_pass():
    rep = run_qc(Dataset(era5_like()))
    assert rep["ok"] is True
    assert rep["summary"]["FAIL"] == 0


def test_broken_has_fails():
    rep = run_qc(Dataset(broken_era5_like()))
    assert rep["ok"] is False
    checks = {(c["check"], c["status"]) for c in rep["checks"]}
    assert ("value_range", "FAIL") in checks
    assert ("grid_monotonic", "FAIL") in checks


def test_broken_fixture_file_validates_to_fail():
    path = os.path.join(DATA, "broken_era5_like.nc")
    assert os.path.exists(path), "run make_fixtures.py"
    rep = run_qc(open_dataset(path))
    assert rep["ok"] is False
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_run.py -v`
Expected: FAIL ("cannot import name 'run_qc'" / "broken_era5_like")

- [ ] **Step 3: 구현 — run_qc, broken synth, fixture 작성**

`skills/validate-model-output/scripts/qc.py` 끝에 추가:
```python
from rules import load_rules as _load_rules


def run_qc(d: Dataset, rules: dict | None = None) -> dict:
    if rules is None:
        rules = _load_rules()
    checks = []
    checks += check_schema(d)
    checks += check_grid(d)
    checks += check_time(d)
    try:
        names = d.data_var_names()
    except Exception as e:
        checks.append(_result("schema", "FAIL", f"변수 목록 읽기 실패: {e}"))
        names = []
    for name in names:
        checks += check_variable(d, name, rules)
    summary = {"PASS": 0, "FAIL": 0, "WARN": 0}
    for c in checks:
        summary[c["status"]] = summary.get(c["status"], 0) + 1
    return {"checks": checks, "summary": summary, "ok": summary["FAIL"] == 0}
```

`skills/validate-model-output/tests/synth.py` 끝에 추가:
```python
def broken_era5_like():
    """era5_like 기반 고의 결함본: 값범위초과(500K) + 결측구멍 + 위도 비단조."""
    ds = era5_like().copy(deep=True)
    t = ds["t2m"].values
    t[0, 0, 0] = 500.0          # 물리범위 초과
    t[0, 1, :] = np.nan         # 결측 구멍(한 위도줄 전체)
    ds["t2m"].values = t
    lat = ds["lat"].values.copy()
    lat[2], lat[3] = lat[3], lat[2]   # 위도 비단조(2개 스왑)
    ds = ds.assign_coords(lat=lat)
    return ds
```
(파일 상단에 `import numpy as np` 가 이미 있음 — 확인만.)

`skills/validate-model-output/scripts/make_fixtures.py` 의 `main()` 에 추가(기존 두 파일 작성 뒤, temp-copy 패턴 동일하게):
```python
    # 고의 결함본 (QC 데모/테스트용) — NetCDF3
    from synth import broken_era5_like
    _write_nc(broken_era5_like(), os.path.join(DATA, "broken_era5_like.nc"),
              format="NETCDF3_64BIT")
```
> 구현 메모: make_fixtures.py 가 비-ASCII 경로 우회를 위해 이미 쓰는 "temp dir 작성 후 copy" 로직을 함수 `_write_nc(ds, dest, **kw)` 로 묶어 재사용하라(없으면 기존 인라인 코드를 이 헬퍼로 추출 후 3개 파일 모두 이를 통해 작성). engine 인자도 기존과 동일하게 전달.

- [ ] **Step 4: fixture 재생성**

Run: `cd skills/validate-model-output && python scripts/make_fixtures.py`
Expected: `wrote fixtures ...` (clean 2개 + broken 1개)

- [ ] **Step 5: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_qc_run.py -v`
Expected: PASS (3 passed)

- [ ] **Step 6: 커밋** (broken fixture 포함)

```bash
git add skills/validate-model-output/scripts/qc.py skills/validate-model-output/scripts/make_fixtures.py skills/validate-model-output/tests/synth.py skills/validate-model-output/tests/test_qc_run.py skills/validate-model-output/data/broken_era5_like.nc
git commit -m "feat(validate): run_qc orchestration + broken fixture (clean=PASS / broken=FAIL)"
```

---

### Task 5: `report.py` (report.json + report.md)

**Files:**
- Create: `skills/validate-model-output/scripts/report.py`
- Test: `skills/validate-model-output/tests/test_report.py`

**Interfaces:**
- Consumes: `run_qc` 결과 dict
- Produces:
  - `build_report(qc_result: dict, source: str) -> dict` — 기계용 구조(소스·요약·체크 + 생성메타 제외).
  - `render_markdown(qc_result: dict, source: str) -> str` — 사람·심사위원용 표. 요약(PASS/FAIL/WARN) + 체크별 표(상태 이모지·변수·근거) + advisory/ reference≠truth 안내문.
  - `write_report(qc_result: dict, source: str, out_dir: str) -> tuple[str, str]` — `out_dir/report.json`, `out_dir/report.md` 작성, 경로 튜플 반환(utf-8).

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_report.py`:
```python
import json
import os
from report import build_report, render_markdown, write_report

_QC = {
    "checks": [
        {"check": "value_range", "variable": "t2m", "status": "FAIL", "evidence": "500K 초과 1개"},
        {"check": "missing", "variable": "t2m", "status": "PASS", "evidence": "결측 0%"},
    ],
    "summary": {"PASS": 1, "FAIL": 1, "WARN": 0},
    "ok": False,
}


def test_build_report_structure():
    r = build_report(_QC, source="x.nc")
    assert r["source"] == "x.nc"
    assert r["summary"]["FAIL"] == 1
    assert len(r["checks"]) == 2


def test_render_markdown_contains_evidence_and_advisory():
    md = render_markdown(_QC, source="x.nc")
    assert "FAIL" in md
    assert "500K 초과 1개" in md
    assert "t2m" in md
    assert "advisory" in md.lower() or "reference" in md.lower()


def test_write_report_files(tmp_path):
    jpath, mpath = write_report(_QC, source="x.nc", out_dir=str(tmp_path))
    assert os.path.exists(jpath) and os.path.exists(mpath)
    with open(jpath, encoding="utf-8") as f:
        data = json.load(f)
    assert data["ok"] is False
    assert "FAIL" in open(mpath, encoding="utf-8").read()
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_report.py -v`
Expected: FAIL ("No module named 'report'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/report.py`:
```python
from __future__ import annotations

import json
import os

_EMOJI = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}

_ADVISORY = (
    "> 해석 임계(물리범위·N-시그마 등)는 **advisory**(영역·변수·해상도 의존). "
    "층위1 QC는 기준자료 불필요(intrinsic) — 기준자료는 truth가 아니라 reference."
)


def build_report(qc_result: dict, source: str) -> dict:
    return {
        "source": source,
        "ok": qc_result["ok"],
        "summary": qc_result["summary"],
        "checks": qc_result["checks"],
    }


def render_markdown(qc_result: dict, source: str) -> str:
    s = qc_result["summary"]
    verdict = "PASS ✅" if qc_result["ok"] else "FAIL ❌"
    lines = [
        f"# QC 리포트 — `{os.path.basename(source)}`",
        "",
        f"**종합: {verdict}**  (PASS {s.get('PASS',0)} · FAIL {s.get('FAIL',0)} · WARN {s.get('WARN',0)})",
        "",
        "| 상태 | 검사 | 변수 | 근거 |",
        "|---|---|---|---|",
    ]
    for c in qc_result["checks"]:
        em = _EMOJI.get(c["status"], c["status"])
        var = c.get("variable") or "-"
        ev = str(c.get("evidence", "")).replace("|", "\\|")
        lines.append(f"| {em} {c['status']} | {c['check']} | {var} | {ev} |")
    lines += ["", _ADVISORY, ""]
    return "\n".join(lines)


def write_report(qc_result: dict, source: str, out_dir: str) -> tuple:
    os.makedirs(out_dir, exist_ok=True)
    jpath = os.path.join(out_dir, "report.json")
    mpath = os.path.join(out_dir, "report.md")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(build_report(qc_result, source), f, ensure_ascii=False, indent=2)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_markdown(qc_result, source))
    return jpath, mpath
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_report.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/report.py skills/validate-model-output/tests/test_report.py
git commit -m "feat(validate): report.py (report.json + report.md with PASS/FAIL/WARN + evidence)"
```

---

### Task 6: `cli validate` + `domains.yaml` GFS 패턴 보강 + 실데이터 스모크

**Files:**
- Modify: `skills/validate-model-output/scripts/cli.py`
- Modify: `skills/validate-model-output/config/domains.yaml`
- Modify: `skills/validate-model-output/SKILL.md`
- Test: `skills/validate-model-output/tests/test_cli_validate.py`

**Interfaces:**
- Consumes: `io_detect.open_dataset`, `qc.run_qc`, `report.write_report`
- Produces:
  - `cli.py` `validate` 서브커맨드: `python cli.py validate <file> [--out DIR]` → 파일 열기 → run_qc → 콘솔에 요약·체크표 출력 + `report.json`/`report.md` 저장. 종료코드: FAIL 있으면 1, 아니면 0(미지/손상 파일도 크래시 없이 리포트+exit 1).
  - `domains.yaml` meteorology 에 GFS GRIB 패턴 추가(dpt/prate/prmsl) → 도메인 신뢰도 개선.

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_cli_validate.py`:
```python
import os
import subprocess
import sys

SKILL = os.path.dirname(os.path.dirname(__file__))
SCRIPTS = os.path.join(SKILL, "scripts")
DATA = os.path.join(SKILL, "data")


def _run(args, cwd=SKILL):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "cli.py")] + args,
                          capture_output=True, text=True, cwd=cwd)


def test_validate_clean_exit0(tmp_path):
    out = _run(["validate", os.path.join(DATA, "clean_era5_like.nc"), "--out", str(tmp_path)])
    assert out.returncode == 0
    assert os.path.exists(os.path.join(tmp_path, "report.md"))
    assert "PASS" in out.stdout


def test_validate_broken_exit1(tmp_path):
    out = _run(["validate", os.path.join(DATA, "broken_era5_like.nc"), "--out", str(tmp_path)])
    assert out.returncode == 1
    assert "FAIL" in out.stdout


def test_validate_missing_file_no_crash(tmp_path):
    out = _run(["validate", os.path.join(DATA, "nope_does_not_exist.nc"), "--out", str(tmp_path)])
    assert out.returncode == 1          # 크래시(>1)가 아니라 정상 종료코드 1
    assert "FAIL" in out.stdout or "열" in out.stdout
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_cli_validate.py -v`
Expected: FAIL (validate 서브커맨드 없음 → argparse 에러 exit 2)

- [ ] **Step 3: 구현 — cli validate, domains 보강**

`skills/validate-model-output/scripts/cli.py` 수정:
1) 상단 import 에 추가:
```python
from io_detect import open_dataset, UnknownFormatError  # noqa: E402
from qc import run_qc  # noqa: E402
from report import write_report, render_markdown  # noqa: E402
```
2) `cmd_validate` 함수 추가:
```python
def cmd_validate(args) -> int:
    out_dir = args.out or os.getcwd()
    try:
        d = open_dataset(args.file)
    except (UnknownFormatError, OSError) as e:
        qc = {"checks": [{"check": "open", "variable": None, "status": "FAIL",
                          "evidence": f"열기 실패: {e}"}],
              "summary": {"PASS": 0, "FAIL": 1, "WARN": 0}, "ok": False}
        print(render_markdown(qc, args.file))
        write_report(qc, args.file, out_dir)
        return 1
    qc = run_qc(d)
    print(render_markdown(qc, args.file))
    jpath, mpath = write_report(qc, args.file, out_dir)
    print(f"\n[리포트 저장] {mpath}")
    return 0 if qc["ok"] else 1
```
3) `main()` 의 subparser 등록부에 추가:
```python
    v = sub.add_parser("validate", help="층위1 QC (값범위·결측·격자·시간)")
    v.add_argument("file")
    v.add_argument("--out", default=None, help="report.json/md 저장 폴더")
    v.set_defaults(func=cmd_validate)
```

`skills/validate-model-output/config/domains.yaml` 의 `meteorology.name_patterns` 에 추가:
```yaml
      - "dpt"
      - "prate"
      - "prmsl"
      - "dswrf"
      - "gust"
```

`skills/validate-model-output/SKILL.md` 의 "PHASE 2 / 3" 자리표시 줄을 갱신: `validate`(층위1 QC) 사용법 1줄 추가 — `python scripts/cli.py validate <파일> --out <폴더>` → PASS/FAIL/WARN 리포트.

- [ ] **Step 4: 통과 확인 + 전체 스위트**

Run: `cd skills/validate-model-output && python -m pytest -v`
Expected: PASS (전체 그린, 0 warnings)

- [ ] **Step 5: 실데이터 스모크 (원본 있으면)**

Run: `cd skills/validate-model-output && python scripts/cli.py validate ../../project/sample_data/nums_ex/gfs_fcst_glo_day_masked_20220906.nc --out /tmp/gfs_qc`
Expected: GFS 실파일에 대해 QC 리포트(값범위·결측·격자2D형상·시간축8스텝) 생성 — 크래시 없이 PASS/FAIL/WARN. **실제 결과를 리포트에 기록**(GFS의 어떤 변수가 어떤 규칙에 매칭/미매칭됐는지, 단위 °C/Pa 처리). inventory/report 산출물은 커밋하지 않음.

- [ ] **Step 6: 커밋**

```bash
git add skills/validate-model-output/scripts/cli.py skills/validate-model-output/config/domains.yaml skills/validate-model-output/SKILL.md skills/validate-model-output/tests/test_cli_validate.py
git commit -m "feat(validate): cli validate subcommand + domains.yaml GFS patterns + SKILL.md"
```

---

## Self-Review (작성자 점검 결과)

**1. Spec coverage (스펙 §4 층위1):** 포맷/열림(io_detect 재사용+cmd_validate 에러처리) ✓ / 격자·스키마(check_grid·check_schema: dims·단조·2D형상) ✓ / 값범위(units 인식 rules) ✓ / 결측(check_variable missing) ✓ / 이상치(N-시그마 WARN) ✓ / 메타·시간축(check_time 단조·중복) ✓ / 리포트 json+md+근거 ✓ / 크래시 금지(전 검사 try + cmd_validate) ✓ / rules.yaml 유일 확장점 ✓ / advisory 임계 ✓. 실데이터 발견 반영: GFS 단위(°C/Pa) 규칙·domains GFS 패턴 ✓.

**2. Placeholder scan:** "TBD/적절히 처리" 없음. 모든 코드 스텝 실제 코드 포함. ✓

**3. Type consistency:**
- 체크 결과 dict 키(check/variable/status/evidence)가 qc.py 생성·report.py 소비에서 일치. ✓
- `run_qc` 반환(checks/summary/ok)이 report.build_report·render_markdown·cmd_validate 사용처와 일치. ✓
- `match_rule`/`load_rules` 시그니처가 qc.check_variable 호출과 일치. ✓
- M1 인터페이스 호출(`d.xr[name].values`, `d.variable`, `d.latlon`, `d.time_info`, `io_detect.open_dataset`, `UnknownFormatError`)이 실제 M1 구현과 일치(확인필: dataset.py·io_detect.py). ✓
- Task 4 가 make_fixtures 의 temp-copy 로직을 `_write_nc` 헬퍼로 재사용하도록 명시(중복/비-ASCII 경로 회귀 방지). ✓

---

## 다음 마일스톤 예고
- **M3**: `preprocess.py`(단위정규화 K↔°C·변수 alias·격자정렬·시간정합) + `config/aliases.yaml`(GFS GRIB명↔CF) + `metrics/{basic,pattern,distribution}.py` (canonical 단일구현).
- **M4**: `recipes.yaml` + `verify.py`(다축 배터리) + `regions.py`(해역 crop) + `plots.py`(figures 카탈로그 구현).
- **M5**: `derive.py`·postprocess + SKILL.md 완성 + submit/assets 패키징 + 데모.
