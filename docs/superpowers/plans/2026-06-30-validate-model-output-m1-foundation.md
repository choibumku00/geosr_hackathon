# validate-model-output — M1: 기반·발견(Foundation & Discovery) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 입력 파일(NetCDF3 / NetCDF4·HDF5 / CSV)을 포맷·도메인에 무관하게 단일 `Dataset`으로 열고, 폴더를 스캔해 "무엇이 어디에 어떤 형태로 있는지" 인벤토리를 만드는 `discover`/`inspect` CLI를 만든다. (스킬의 PHASE 0 = 분석 전 발견 단계)

**Architecture:** 모든 reader는 결과를 공통 `Dataset`(xarray 래핑)으로 정규화한다. `io_detect`가 파일 시그니처로 포맷을 판별해 reader로 라우팅하고, `router`가 변수 메타데이터로 도메인을 추정하며, `discover`가 이를 폴더 단위로 모아 인벤토리(JSON+표)를 낸다. 미지 포맷은 `inspect`가 best-effort로 구조를 덤프하고 `unknown` 플래그를 단다.

**Tech Stack:** Python 3.12, xarray(+netCDF4·h5netcdf 엔진), pandas, numpy, PyYAML, pytest.

## Global Constraints

- Python 3.12 (miniconda3). 의존성: `xarray netCDF4 h5netcdf PyYAML pytest` (+ 기존 numpy·pandas·scipy·matplotlib). `cartopy`는 후속 마일스톤에서 optional.
- **크래시 금지**: 파일없음/미지원포맷/손상은 예외 전파가 아니라 구조화된 결과(`format='unknown'`, `error=...`)로 보고. (단, 프로그래밍 계약 위반은 명시적 예외 허용.)
- **기준자료 ≠ 참값(reference)**: 도메인/역할 추정 시 "truth"라는 단어를 코드·출력에 쓰지 않는다.
- 한국어 서술 + 표준 기술용어 영문 병기.
- **fixture는 작게, git 포함**: 테스트 fixture `.nc`는 `skills/validate-model-output/data/`·`tests/` 아래 두며 작게 유지(.gitignore가 `!skills/**/data/*.nc`·`!skills/**/tests/**/*.nc`로 예외 허용). 실제 원본(598MB/1.14GB)은 절대 커밋·로드 안 함(테스트는 합성 fixture 사용).
- **canonical 단일 구현**: 같은 기능을 두 번 구현하지 않는다(예: 좌표 판별은 `Dataset`에만).
- 모듈은 `scripts/`에 두고 서로 형제 import(`from dataset import Dataset`). `cli.py`와 테스트는 `scripts/`를 `sys.path`에 넣어 실행.

---

### Task 1: 스킬 스캐폴드 + 의존성 + 테스트 하니스

**Files:**
- Create: `skills/validate-model-output/requirements.txt`
- Create: `skills/validate-model-output/scripts/__init__.py` (빈 파일)
- Create: `skills/validate-model-output/tests/conftest.py`
- Create: `skills/validate-model-output/tests/test_smoke.py`

**Interfaces:**
- Consumes: (없음 — 첫 태스크)
- Produces: `scripts/` 가 import 경로에 오른 pytest 환경. 이후 모든 테스트가 `from dataset import ...` 형태로 모듈을 부른다.

- [ ] **Step 1: 폴더와 requirements 작성**

`skills/validate-model-output/requirements.txt`:
```
xarray>=2024.0
netCDF4>=1.7
h5netcdf>=1.3
PyYAML>=6.0
pytest>=8.0
numpy>=2.0
pandas>=2.0
```

`skills/validate-model-output/scripts/__init__.py`: (빈 파일 생성)

`skills/validate-model-output/tests/conftest.py`:
```python
import os
import sys

# scripts/ 디렉터리를 import 경로에 추가 (모듈은 형제 import 사용)
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
```

- [ ] **Step 2: 의존성 설치**

Run: `python -m pip install -r skills/validate-model-output/requirements.txt`
Expected: `Successfully installed ... xarray ... netCDF4 ... h5netcdf ... PyYAML ...` (이미 설치된 것은 "Requirement already satisfied")

- [ ] **Step 3: 스모크 테스트 작성**

`skills/validate-model-output/tests/test_smoke.py`:
```python
def test_core_imports():
    import numpy, pandas, xarray, yaml
    import netCDF4  # noqa: F401
    assert xarray.__version__
```

- [ ] **Step 4: 스모크 테스트 실행**

Run: `cd skills/validate-model-output && python -m pytest tests/test_smoke.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/requirements.txt skills/validate-model-output/scripts/__init__.py skills/validate-model-output/tests/conftest.py skills/validate-model-output/tests/test_smoke.py
git commit -m "feat(validate): M1 scaffold + deps + pytest harness"
```

---

### Task 2: `Dataset` 추상화 (포맷 무관 단일 인터페이스)

**Files:**
- Create: `skills/validate-model-output/scripts/dataset.py`
- Test: `skills/validate-model-output/tests/test_dataset.py`

**Interfaces:**
- Consumes: `xarray.Dataset` (생성자 입력)
- Produces:
  - `class Variable` (dataclass): `name:str, dims:tuple, shape:tuple, units:str|None, standard_name:str|None, long_name:str|None, attrs:dict`
  - `class Dataset`:
    - `__init__(self, xr_ds: xr.Dataset, source: str = "", fmt: str = "")`
    - `xr -> xr.Dataset` (property)
    - `data_var_names() -> list[str]`
    - `variable(name) -> Variable`
    - `variables() -> dict[str, Variable]`
    - `latlon() -> tuple[str, str, bool] | None`  # (lat_name, lon_name, is_2d) or None
    - `coord_kind() -> str`  # '1d' | '2d' | 'none'
    - `grid_shape() -> tuple[int, ...] | None`
    - `time_info() -> dict | None`  # {'name','n_steps','start','end'}

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_dataset.py`:
```python
import numpy as np
import xarray as xr
from dataset import Dataset, Variable


def _era5_like():
    # 1D 좌표·K·CF standard_name
    lat = np.linspace(-90, 90, 5)
    lon = np.linspace(0, 360, 6, endpoint=False)
    t2m = xr.DataArray(
        np.full((1, 5, 6), 280.0), dims=("time", "lat", "lon"),
        coords={"time": [np.datetime64("2022-09-06")], "lat": lat, "lon": lon},
        attrs={"units": "K", "standard_name": "air_temperature"},
    )
    return xr.Dataset({"t2m": t2m})


def _gfs_like():
    # 2D 좌표·°C·GRIB식 이름
    ny, nx = 4, 5
    lat2d = np.tile(np.linspace(-60, 60, ny)[:, None], (1, nx))
    lon2d = np.tile(np.linspace(0, 100, nx)[None, :], (ny, 1))
    tmp = xr.DataArray(
        np.full((ny, nx), 12.0), dims=("y", "x"),
        attrs={"units": "degC", "long_name": "Temperature"},
    )
    ds = xr.Dataset({"TMP": tmp})
    ds = ds.assign_coords(
        latitude=(("y", "x"), lat2d), longitude=(("y", "x"), lon2d)
    )
    return ds


def test_variables_metadata():
    d = Dataset(_era5_like(), source="a.nc", fmt="netcdf3")
    vs = d.variables()
    assert "t2m" in vs
    v = vs["t2m"]
    assert isinstance(v, Variable)
    assert v.units == "K"
    assert v.standard_name == "air_temperature"
    assert v.shape == (1, 5, 6)


def test_latlon_1d():
    d = Dataset(_era5_like())
    assert d.latlon() == ("lat", "lon", False)
    assert d.coord_kind() == "1d"
    assert d.grid_shape() == (5, 6)


def test_latlon_2d():
    d = Dataset(_gfs_like())
    name_lat, name_lon, is_2d = d.latlon()
    assert (name_lat, name_lon, is_2d) == ("latitude", "longitude", True)
    assert d.coord_kind() == "2d"
    assert d.grid_shape() == (4, 5)


def test_time_info():
    d = Dataset(_era5_like())
    ti = d.time_info()
    assert ti["n_steps"] == 1
    assert ti["start"].startswith("2022-09-06")


def test_no_time():
    d = Dataset(_gfs_like())
    assert d.time_info() is None
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_dataset.py -v`
Expected: FAIL ("No module named 'dataset'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/dataset.py`:
```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import xarray as xr

# 좌표 이름 후보 (소문자 비교)
_LAT_NAMES = ("lat", "latitude", "nav_lat", "gphit", "y")
_LON_NAMES = ("lon", "longitude", "nav_lon", "glamt", "x")
_TIME_NAMES = ("time", "valid_time", "t")


@dataclass
class Variable:
    name: str
    dims: tuple
    shape: tuple
    units: Optional[str]
    standard_name: Optional[str]
    long_name: Optional[str]
    attrs: dict = field(default_factory=dict)


class Dataset:
    """포맷 무관 자료 추상화. 내부적으로 xarray.Dataset을 감싼다."""

    def __init__(self, xr_ds: xr.Dataset, source: str = "", fmt: str = ""):
        self._ds = xr_ds
        self.source = source
        self.fmt = fmt

    @property
    def xr(self) -> xr.Dataset:
        return self._ds

    def data_var_names(self) -> list:
        return [str(v) for v in self._ds.data_vars]

    def variable(self, name: str) -> Variable:
        da = self._ds[name]
        a = dict(da.attrs)
        return Variable(
            name=str(name),
            dims=tuple(str(d) for d in da.dims),
            shape=tuple(int(s) for s in da.shape),
            units=a.get("units"),
            standard_name=a.get("standard_name"),
            long_name=a.get("long_name"),
            attrs=a,
        )

    def variables(self) -> dict:
        return {n: self.variable(n) for n in self.data_var_names()}

    def _find(self, names) -> Optional[str]:
        # coords + variables 에서 후보 이름(또는 standard_name) 탐색
        all_names = list(self._ds.coords) + list(self._ds.variables)
        for cand in all_names:
            low = str(cand).lower()
            if low in names:
                return str(cand)
        # standard_name 매칭
        for cand in self._ds.variables:
            sn = str(self._ds[cand].attrs.get("standard_name", "")).lower()
            if sn in ("latitude",) and "latitude" in names:
                return str(cand)
            if sn in ("longitude",) and "longitude" in names:
                return str(cand)
        return None

    def latlon(self) -> Optional[tuple]:
        lat = self._find(_LAT_NAMES)
        lon = self._find(_LON_NAMES)
        if lat is None or lon is None:
            return None
        is_2d = self._ds[lat].ndim == 2
        return (lat, lon, is_2d)

    def coord_kind(self) -> str:
        ll = self.latlon()
        if ll is None:
            return "none"
        return "2d" if ll[2] else "1d"

    def grid_shape(self) -> Optional[tuple]:
        ll = self.latlon()
        if ll is None:
            return None
        lat_name, lon_name, is_2d = ll
        if is_2d:
            return tuple(int(s) for s in self._ds[lat_name].shape)
        return (int(self._ds[lat_name].size), int(self._ds[lon_name].size))

    def time_info(self) -> Optional[dict]:
        tname = self._find(_TIME_NAMES)
        if tname is None:
            return None
        tvals = self._ds[tname].values
        n = int(np.size(tvals))
        flat = np.atleast_1d(tvals)
        return {
            "name": tname,
            "n_steps": n,
            "start": str(flat[0]),
            "end": str(flat[-1]),
        }
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_dataset.py -v`
Expected: PASS (6 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/dataset.py skills/validate-model-output/tests/test_dataset.py
git commit -m "feat(validate): Dataset/Variable abstraction (1D/2D coords, units, time)"
```

---

### Task 3: 합성 fixture 헬퍼 + 작은 `.nc` 파일 생성

**Files:**
- Create: `skills/validate-model-output/tests/synth.py`
- Create: `skills/validate-model-output/scripts/make_fixtures.py`
- Test: `skills/validate-model-output/tests/test_fixtures.py`
- (실행 산출물) `skills/validate-model-output/data/clean_era5_like.nc`, `data/clean_gfs_like.nc`

**Interfaces:**
- Consumes: xarray
- Produces:
  - `tests/synth.py`: `era5_like() -> xr.Dataset`, `gfs_like() -> xr.Dataset` (Task 2 테스트의 두 헬퍼를 한 곳으로 통일; t2m/u10/v10 포함)
  - `scripts/make_fixtures.py`: `main()` — `data/clean_era5_like.nc`, `data/clean_gfs_like.nc` 작성 (NetCDF3/NetCDF4 각각)

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_fixtures.py`:
```python
import os
import xarray as xr
from synth import era5_like, gfs_like

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def test_synth_shapes():
    e = era5_like()
    assert {"t2m", "u10", "v10"} <= set(e.data_vars)
    assert e["t2m"].attrs["units"] == "K"
    g = gfs_like()
    assert "TMP" in g.data_vars
    assert g["TMP"].attrs["units"] == "degC"


def test_fixture_files_exist_and_open():
    # make_fixtures 를 먼저 실행해야 함 (Step 4)
    for fn, engine_sig in [("clean_era5_like.nc", b"CDF"), ("clean_gfs_like.nc", b"\x89HDF")]:
        path = os.path.join(DATA, fn)
        assert os.path.exists(path), f"missing fixture {fn} (run make_fixtures.py)"
        with open(path, "rb") as f:
            assert f.read(4)[: len(engine_sig)] == engine_sig
        ds = xr.open_dataset(path)
        assert len(ds.data_vars) >= 1
        ds.close()
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_fixtures.py -v`
Expected: FAIL ("No module named 'synth'")

- [ ] **Step 3: 합성 헬퍼와 fixture 생성기 작성**

`skills/validate-model-output/tests/synth.py`:
```python
import numpy as np
import xarray as xr


def era5_like():
    """1D 좌표·K·CF standard_name·풍속 성분 포함 (ERA5 규약 모사)."""
    lat = np.linspace(-90, 90, 9)
    lon = np.linspace(0, 360, 12, endpoint=False)
    shape = (1, 9, 12)
    coords = {"time": [np.datetime64("2022-09-06")], "lat": lat, "lon": lon}

    def da(val, units, sn):
        return xr.DataArray(
            np.full(shape, val, dtype="float32"),
            dims=("time", "lat", "lon"), coords=coords,
            attrs={"units": units, "standard_name": sn},
        )

    return xr.Dataset({
        "t2m": da(280.0, "K", "air_temperature"),
        "u10": da(3.0, "m s-1", "eastward_wind"),
        "v10": da(-2.0, "m s-1", "northward_wind"),
    })


def gfs_like():
    """2D 좌표·°C·GRIB식 이름 (GFS 변환본 모사)."""
    ny, nx = 8, 10
    lat2d = np.tile(np.linspace(-60, 60, ny)[:, None], (1, nx)).astype("float32")
    lon2d = np.tile(np.linspace(0, 120, nx)[None, :], (ny, 1)).astype("float32")

    def da(val, units, long_name):
        return xr.DataArray(
            np.full((ny, nx), val, dtype="float32"), dims=("y", "x"),
            attrs={"units": units, "long_name": long_name},
        )

    ds = xr.Dataset({
        "TMP": da(12.0, "degC", "Temperature"),
        "UGRD": da(3.0, "m/s", "U component of wind"),
        "VGRD": da(-2.0, "m/s", "V component of wind"),
    })
    return ds.assign_coords(
        latitude=(("y", "x"), lat2d), longitude=(("y", "x"), lon2d)
    )
```

`skills/validate-model-output/scripts/make_fixtures.py`:
```python
"""작은 합성 fixture 를 data/ 에 생성한다 (실제 원본 없이 재현 가능)."""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tests"))
DATA = os.path.join(os.path.dirname(HERE), "data")

from synth import era5_like, gfs_like  # noqa: E402


def main():
    os.makedirs(DATA, exist_ok=True)
    # ERA5 모사 → NetCDF3 (CDF 시그니처)
    era5_like().to_netcdf(
        os.path.join(DATA, "clean_era5_like.nc"), format="NETCDF3_64BIT"
    )
    # GFS 모사 → NetCDF4/HDF5 (\x89HDF 시그니처)
    gfs_like().to_netcdf(
        os.path.join(DATA, "clean_gfs_like.nc"), format="NETCDF4", engine="h5netcdf"
    )
    print("wrote fixtures to", DATA)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: fixture 생성 실행**

Run: `cd skills/validate-model-output && python scripts/make_fixtures.py`
Expected: `wrote fixtures to .../data`

- [ ] **Step 5: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_fixtures.py -v`
Expected: PASS (2 passed)

- [ ] **Step 6: 커밋** (fixture .nc 는 .gitignore 예외라 커밋됨)

```bash
git add skills/validate-model-output/tests/synth.py skills/validate-model-output/scripts/make_fixtures.py skills/validate-model-output/tests/test_fixtures.py skills/validate-model-output/data/clean_era5_like.nc skills/validate-model-output/data/clean_gfs_like.nc
git commit -m "feat(validate): synthetic ERA5/GFS-like fixtures (NetCDF3 + NetCDF4)"
```

---

### Task 4: `io_detect` — 포맷 감지 + reader 라우팅

**Files:**
- Create: `skills/validate-model-output/scripts/io_detect.py`
- Test: `skills/validate-model-output/tests/test_io_detect.py`

**Interfaces:**
- Consumes: `dataset.Dataset`, 합성 fixture 파일
- Produces:
  - `detect_format(path: str) -> str`  # 'netcdf3' | 'netcdf4' | 'csv' | 'unknown'
  - `class UnknownFormatError(Exception)`
  - `open_dataset(path: str) -> Dataset`  # 미지/손상 시 UnknownFormatError

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_io_detect.py`:
```python
import os
import pytest
from io_detect import detect_format, open_dataset, UnknownFormatError

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ERA5 = os.path.join(DATA, "clean_era5_like.nc")
GFS = os.path.join(DATA, "clean_gfs_like.nc")


def test_detect_netcdf3():
    assert detect_format(ERA5) == "netcdf3"


def test_detect_netcdf4():
    assert detect_format(GFS) == "netcdf4"


def test_detect_csv(tmp_path):
    p = tmp_path / "obs.csv"
    p.write_text("time,sst\n2022-09-06,12.3\n")
    assert detect_format(str(p)) == "csv"


def test_detect_unknown(tmp_path):
    p = tmp_path / "weird.bin"
    p.write_bytes(b"\x01\x02\x03\x04not a known file")
    assert detect_format(str(p)) == "unknown"


def test_open_netcdf_returns_dataset():
    d = open_dataset(GFS)
    assert d.fmt == "netcdf4"
    assert "TMP" in d.data_var_names()
    assert d.coord_kind() == "2d"


def test_open_csv_returns_dataset(tmp_path):
    p = tmp_path / "obs.csv"
    p.write_text("time,sst\n2022-09-06,12.3\n2022-09-07,12.9\n")
    d = open_dataset(str(p))
    assert d.fmt == "csv"
    assert "sst" in d.data_var_names()


def test_open_unknown_raises(tmp_path):
    p = tmp_path / "weird.bin"
    p.write_bytes(b"\x01\x02\x03\x04nope")
    with pytest.raises(UnknownFormatError):
        open_dataset(str(p))
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_io_detect.py -v`
Expected: FAIL ("No module named 'io_detect'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/io_detect.py`:
```python
from __future__ import annotations

import os

import pandas as pd
import xarray as xr

from dataset import Dataset

_TEXT_EXTS = (".csv", ".txt", ".tsv", ".dat")


class UnknownFormatError(Exception):
    pass


def detect_format(path: str) -> str:
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
    except OSError as e:
        raise UnknownFormatError(f"열 수 없음: {path} ({e})")
    if sig[:3] == b"CDF":
        return "netcdf3"
    if sig[:4] == b"\x89HDF":
        return "netcdf4"
    ext = os.path.splitext(path)[1].lower()
    if ext in _TEXT_EXTS:
        return "csv"
    # 텍스트로 읽혀 콤마가 보이면 csv 로 간주 (확장자 없는 경우)
    try:
        head = sig.decode("utf-8")
        if "," in head:
            return "csv"
    except UnicodeDecodeError:
        pass
    return "unknown"


def open_dataset(path: str) -> Dataset:
    fmt = detect_format(path)
    if fmt in ("netcdf3", "netcdf4"):
        try:
            ds = xr.open_dataset(path)
        except Exception as e:  # 손상 등
            raise UnknownFormatError(f"NetCDF 열기 실패: {path} ({e})")
        return Dataset(ds, source=path, fmt=fmt)
    if fmt == "csv":
        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise UnknownFormatError(f"CSV 열기 실패: {path} ({e})")
        return Dataset(df.to_xarray(), source=path, fmt="csv")
    raise UnknownFormatError(f"미지원/미지 포맷: {path}")
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_io_detect.py -v`
Expected: PASS (7 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/io_detect.py skills/validate-model-output/tests/test_io_detect.py
git commit -m "feat(validate): io_detect format detection + reader routing (nc3/nc4/csv/unknown)"
```

---

### Task 5: `router` — 변수 메타데이터로 도메인 추정

**Files:**
- Create: `skills/validate-model-output/config/domains.yaml`
- Create: `skills/validate-model-output/scripts/router.py`
- Test: `skills/validate-model-output/tests/test_router.py`

**Interfaces:**
- Consumes: `dataset.Dataset`, `config/domains.yaml`
- Produces:
  - `detect_domain(d: Dataset) -> dict`  # {'domain':str, 'confidence':float, 'matched':{var:domain}}
    - `domain` 은 'meteorology'|'ocean_temp_salinity'|'waves'|'currents'|'sea_level'|'unknown'
    - `confidence` = 매칭된 변수 수 / 전체 데이터변수 수 (0.0~1.0)

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_router.py`:
```python
import numpy as np
import xarray as xr
from dataset import Dataset
from router import detect_domain
from synth import era5_like, gfs_like


def test_meteorology_from_cf_names():
    r = detect_domain(Dataset(era5_like()))
    assert r["domain"] == "meteorology"
    assert r["confidence"] > 0.5


def test_meteorology_from_grib_names():
    r = detect_domain(Dataset(gfs_like()))
    assert r["domain"] == "meteorology"


def test_ocean_temp_salinity():
    sst = xr.DataArray(
        np.full((3, 3), 290.0), dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [0, 1, 2]},
        attrs={"units": "K", "standard_name": "sea_surface_temperature"},
    )
    r = detect_domain(Dataset(xr.Dataset({"sst": sst})))
    assert r["domain"] == "ocean_temp_salinity"


def test_unknown_domain():
    foo = xr.DataArray(
        np.zeros((2, 2)), dims=("a", "b"), attrs={"long_name": "mystery quantity"}
    )
    r = detect_domain(Dataset(xr.Dataset({"foo": foo})))
    assert r["domain"] == "unknown"
    assert r["confidence"] == 0.0
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_router.py -v`
Expected: FAIL ("No module named 'router'")

- [ ] **Step 3: 도메인 표와 구현 작성**

`skills/validate-model-output/config/domains.yaml`:
```yaml
# 변수 standard_name / 이름 패턴 → 도메인 (router 의 데이터원, taxonomy C절 기반)
domains:
  meteorology:
    standard_names:
      - air_temperature
      - eastward_wind
      - northward_wind
      - air_pressure_at_mean_sea_level
      - precipitation_amount
      - relative_humidity
    name_patterns:
      - "^t2m$"
      - "^2t$"
      - "^tmp$"
      - "^u10$"
      - "^v10$"
      - "ugrd"
      - "vgrd"
      - "mslp"
      - "prmsl"
  ocean_temp_salinity:
    standard_names:
      - sea_water_temperature
      - sea_surface_temperature
      - sea_water_salinity
      - sea_surface_salinity
    name_patterns:
      - "^sst$"
      - "^sss$"
      - "^thetao$"
      - "^so$"
      - "salin"
  waves:
    standard_names:
      - sea_surface_wave_significant_height
    name_patterns:
      - "^hs$"
      - "hm0"
      - "swh"
  currents:
    standard_names:
      - eastward_sea_water_velocity
      - northward_sea_water_velocity
    name_patterns:
      - "^uo$"
      - "^vo$"
  sea_level:
    standard_names:
      - sea_surface_height_above_geoid
      - sea_surface_height_above_reference_ellipsoid
    name_patterns:
      - "^ssh$"
      - "^sla$"
      - "^adt$"
      - "zos"
```

`skills/validate-model-output/scripts/router.py`:
```python
from __future__ import annotations

import os
import re

import yaml

from dataset import Dataset

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "domains.yaml"
)


def _load_domains(path: str = _CONFIG) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["domains"]


def _match_var(var, domains: dict):
    """한 변수가 어느 도메인에 맞는지 — standard_name 우선, 없으면 이름 패턴."""
    sn = (var.standard_name or "").lower()
    name = var.name.lower()
    for dom, spec in domains.items():
        if sn and sn in [s.lower() for s in spec.get("standard_names", [])]:
            return dom
    for dom, spec in domains.items():
        for pat in spec.get("name_patterns", []):
            if re.search(pat, name):
                return dom
    return None


def detect_domain(d: Dataset, domains: dict | None = None) -> dict:
    if domains is None:
        domains = _load_domains()
    variables = d.variables()
    matched = {}
    for name, var in variables.items():
        dom = _match_var(var, domains)
        if dom is not None:
            matched[name] = dom
    if not matched:
        return {"domain": "unknown", "confidence": 0.0, "matched": {}}
    # 최다 득표 도메인
    counts = {}
    for dom in matched.values():
        counts[dom] = counts.get(dom, 0) + 1
    best = max(counts, key=counts.get)
    confidence = counts[best] / max(1, len(variables))
    return {"domain": best, "confidence": round(confidence, 3), "matched": matched}
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_router.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/config/domains.yaml skills/validate-model-output/scripts/router.py skills/validate-model-output/tests/test_router.py
git commit -m "feat(validate): domain router (standard_name/name-pattern -> domain) + domains.yaml"
```

---

### Task 6: `inspect` — 단일파일 best-effort 프로브 (미지 포맷 대응)

**Files:**
- Create: `skills/validate-model-output/scripts/inspect.py`
- Test: `skills/validate-model-output/tests/test_inspect.py`

**Interfaces:**
- Consumes: `io_detect`, `router`, `dataset.Dataset`
- Produces:
  - `probe(path: str) -> dict` — 항상 dict 반환(크래시 금지). 키:
    - `path, format, openable(bool)`
    - openable=True: `variables[list of {name,dims,units,standard_name}], coord_kind, grid_shape, time, domain, confidence`
    - openable=False: `unknown(bool), head_hex(str), error(str)`

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_inspect.py`:
```python
import os
from inspect_file import probe

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ERA5 = os.path.join(DATA, "clean_era5_like.nc")


def test_probe_known_netcdf():
    r = probe(ERA5)
    assert r["openable"] is True
    assert r["format"] == "netcdf3"
    assert r["coord_kind"] == "1d"
    assert r["domain"] == "meteorology"
    names = [v["name"] for v in r["variables"]]
    assert "t2m" in names


def test_probe_unknown_no_crash(tmp_path):
    p = tmp_path / "weird.bin"
    p.write_bytes(b"\x01\x02\x03\x04\x05mystery")
    r = probe(str(p))
    assert r["openable"] is False
    assert r["unknown"] is True
    assert "head_hex" in r
    assert "error" in r


def test_probe_missing_file_no_crash():
    r = probe("/no/such/file.nc")
    assert r["openable"] is False
```

> 참고: 모듈명은 표준 라이브러리 `inspect` 와 충돌하지 않도록 **파일명을 `inspect_file.py`** 로 한다(테스트 import도 `inspect_file`). CLI 서브커맨드 이름은 그대로 `inspect`.

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_inspect.py -v`
Expected: FAIL ("No module named 'inspect_file'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/inspect_file.py`:
```python
from __future__ import annotations

import os

from io_detect import detect_format, open_dataset, UnknownFormatError
from router import detect_domain


def _head_hex(path: str, n: int = 16) -> str:
    try:
        with open(path, "rb") as f:
            return f.read(n).hex()
    except OSError:
        return ""


def probe(path: str) -> dict:
    """단일 파일 구조를 best-effort 로 파악. 항상 dict 반환(크래시 금지)."""
    if not os.path.exists(path):
        return {"path": path, "format": "unknown", "openable": False,
                "unknown": True, "head_hex": "", "error": "파일 없음"}
    fmt = detect_format(path)
    try:
        d = open_dataset(path)
    except UnknownFormatError as e:
        return {"path": path, "format": fmt, "openable": False,
                "unknown": True, "head_hex": _head_hex(path), "error": str(e)}

    dom = detect_domain(d)
    ll = d.latlon()
    vars_summary = []
    for name, v in d.variables().items():
        vars_summary.append({
            "name": name, "dims": list(v.dims), "units": v.units,
            "standard_name": v.standard_name,
        })
    return {
        "path": path,
        "format": d.fmt,
        "openable": True,
        "variables": vars_summary,
        "coord_kind": d.coord_kind(),
        "latlon": list(ll) if ll else None,
        "grid_shape": list(d.grid_shape()) if d.grid_shape() else None,
        "time": d.time_info(),
        "domain": dom["domain"],
        "confidence": dom["confidence"],
    }
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_inspect.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: 커밋**

```bash
git add skills/validate-model-output/scripts/inspect_file.py skills/validate-model-output/tests/test_inspect.py
git commit -m "feat(validate): inspect_file.probe best-effort single-file probe (no-crash, unknown flag)"
```

---

### Task 7: `discover` + `cli` — 폴더 인벤토리와 진입점

**Files:**
- Create: `skills/validate-model-output/scripts/discover.py`
- Create: `skills/validate-model-output/scripts/cli.py`
- Test: `skills/validate-model-output/tests/test_discover.py`

**Interfaces:**
- Consumes: `inspect_file.probe`
- Produces:
  - `discover(paths: list[str]) -> dict` — `{'files':[record...]}`; record = probe() 결과 + `role_guess`('output'|'reference'|'unknown')
  - `guess_role(filename: str) -> str`
  - `cli.py`: `python cli.py discover <path...>` (인벤토리 표 출력 + `inventory.json` 저장), `python cli.py inspect <file>` (probe JSON 출력)

- [ ] **Step 1: 실패하는 테스트 작성**

`skills/validate-model-output/tests/test_discover.py`:
```python
import os
import subprocess
import sys
from discover import discover, guess_role

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")


def test_guess_role():
    assert guess_role("gfs_fcst_glo_day.nc") == "output"
    assert guess_role("era5_rean_glo_day.nc") == "reference"
    assert guess_role("buoy_obs_2022.csv") == "reference"
    assert guess_role("random.nc") == "unknown"


def test_discover_folder():
    r = discover([DATA])
    files = {os.path.basename(f["path"]): f for f in r["files"]}
    assert "clean_era5_like.nc" in files
    assert "clean_gfs_like.nc" in files
    assert files["clean_era5_like.nc"]["domain"] == "meteorology"
    # 적어도 하나는 openable
    assert any(f["openable"] for f in r["files"])


def test_cli_discover_runs():
    out = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, "cli.py"), "discover", DATA],
        capture_output=True, text=True,
    )
    assert out.returncode == 0
    assert "clean_era5_like.nc" in out.stdout
```

- [ ] **Step 2: 실패 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_discover.py -v`
Expected: FAIL ("No module named 'discover'")

- [ ] **Step 3: 구현 작성**

`skills/validate-model-output/scripts/discover.py`:
```python
from __future__ import annotations

import os

from inspect_file import probe

_SCAN_EXTS = (".nc", ".nc4", ".csv", ".txt", ".tsv", ".dat", ".grib", ".grib2", ".grb")

_OUTPUT_HINTS = ("fcst", "forecast", "model", "pred", "output", "gfs", "wrf", "hindcast")
_REF_HINTS = ("rean", "reanalysis", "era5", "glorys", "obs", "buoy", "argo",
              "gauge", "sat", "ref", "truth", "waverys")


def guess_role(filename: str) -> str:
    low = filename.lower()
    is_out = any(h in low for h in _OUTPUT_HINTS)
    is_ref = any(h in low for h in _REF_HINTS)
    if is_out and not is_ref:
        return "output"
    if is_ref and not is_out:
        return "reference"
    return "unknown"


def _iter_files(path: str):
    if os.path.isdir(path):
        for root, _dirs, names in os.walk(path):
            for n in names:
                if os.path.splitext(n)[1].lower() in _SCAN_EXTS:
                    yield os.path.join(root, n)
    elif os.path.isfile(path):
        yield path


def discover(paths) -> dict:
    records = []
    for p in paths:
        for fp in _iter_files(p):
            rec = probe(fp)
            rec["role_guess"] = guess_role(os.path.basename(fp))
            records.append(rec)
    return {"files": records}
```

`skills/validate-model-output/scripts/cli.py`:
```python
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from discover import discover  # noqa: E402
from inspect_file import probe  # noqa: E402


def _print_inventory(result: dict) -> None:
    print(f"{'파일':40s} {'포맷':9s} {'도메인':18s} {'역할추정':10s} {'좌표':5s} {'변수'}")
    print("-" * 100)
    for f in result["files"]:
        name = os.path.basename(f["path"])[:40]
        if f["openable"]:
            varnames = ",".join(v["name"] for v in f["variables"][:4])
            print(f"{name:40s} {f['format']:9s} {f.get('domain','?'):18s} "
                  f"{f.get('role_guess','?'):10s} {f.get('coord_kind','?'):5s} {varnames}")
        else:
            print(f"{name:40s} {f['format']:9s} {'(열기 실패: 미지포맷)':18s} "
                  f"{f.get('role_guess','?'):10s} {'-':5s} -")


def cmd_discover(args) -> int:
    result = discover(args.paths)
    _print_inventory(result)
    out = args.out or os.path.join(os.getcwd(), "inventory.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print(f"\n[inventory.json 저장] {out}")
    return 0


def cmd_inspect(args) -> int:
    print(json.dumps(probe(args.file), ensure_ascii=False, indent=2))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="validate-model-output")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover", help="폴더/파일 인벤토리")
    d.add_argument("paths", nargs="+")
    d.add_argument("--out", default=None, help="inventory.json 경로")
    d.set_defaults(func=cmd_discover)

    i = sub.add_parser("inspect", help="단일 파일 구조 프로브")
    i.add_argument("file")
    i.set_defaults(func=cmd_inspect)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: 통과 확인**

Run: `cd skills/validate-model-output && python -m pytest tests/test_discover.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: 전체 테스트 실행**

Run: `cd skills/validate-model-output && python -m pytest -v`
Expected: PASS (전체 그린)

- [ ] **Step 6: 커밋**

```bash
git add skills/validate-model-output/scripts/discover.py skills/validate-model-output/scripts/cli.py skills/validate-model-output/tests/test_discover.py
git commit -m "feat(validate): discover inventory + cli (discover/inspect subcommands)"
```

---

### Task 8: SKILL.md (PHASE 0/1 골격) + usage 문서 + 실데이터 스모크

**Files:**
- Create: `skills/validate-model-output/SKILL.md`
- Create: `skills/validate-model-output/references/usage.md`

**Interfaces:**
- Consumes: `cli.py` (discover/inspect)
- Produces: 사람·에이전트가 PHASE 0(발견)을 실행하는 진입 문서. 이후 마일스톤이 PHASE 2/3 섹션을 채운다.

- [ ] **Step 1: SKILL.md 작성 (Claude Code 스킬 프런트매터 포함)**

`skills/validate-model-output/SKILL.md`:
```markdown
---
name: validate-model-output
description: 수치모델/AI 출력을 NetCDF/CSV로 받아 발견→질문유도→다축 검증·분석한다. 사용자가 데이터/요구를 명확히 말하지 않으면 먼저 discover로 무엇이 있는지 파악하고 되묻는다.
---

# validate-model-output

수치모델 출력을 ERA5/GLORYS·관측·위성과 비교·검증하는 범용 스킬. **분석을 즉시 시작하지 않는다.** 먼저 무엇이 어디에 어떤 형태로 있는지 발견하고, 모르는 것은 사용자에게 질문해 구체화한다.

## PHASE 0 — DISCOVER (분석 전 필수)
1. 작업폴더/지정경로를 인벤토리한다:
   `python scripts/cli.py discover <폴더 또는 파일...>`
   → 파일별 포맷·도메인·좌표·역할추정 표 + `inventory.json`.
2. 단일 파일 구조가 궁금하면:
   `python scripts/cli.py inspect <파일>`
3. **미지/예상 밖 포맷**(`openable=false`, `unknown=true`)이면: 표시된 `head_hex`·확장자를 단서로 **즉석 점검 코드를 작성**해 구조를 파악한 뒤, 발견 내용을 사용자에게 보고하고 reader 확장 여부를 결정한다.

## PHASE 1 — ELICIT (질문으로 구체화)
인벤토리를 사용자에게 제시하고 되묻는다:
- 어느 파일이 '우리 결과물'이고 어느 것이 '기준/검증'인가? (역할추정은 파일명 휴리스틱일 뿐 — 확인받는다)
- 도메인이 확정되면, 그 도메인에 유용한 기준자료(재분석 격자·관측 CSV·위성)가 있으면 어떤 분석이 가능한지 안내하고 보유 여부를 묻는다.
- 애매하지만 가치 있는 분석은 옵션으로 제시하고 고르게 한다.

## PHASE 2 / 3 — VALIDATE·VERIFY·REPORT
(후속 마일스톤 M2~M5에서 구현: `validate`(QC) / `verify`(다축 배터리) / `report`)

> 원칙: 기준자료는 truth가 아니라 reference. 해석 임계는 advisory. 단일 지표/그림으로 결론내지 않는다.
```

`skills/validate-model-output/references/usage.md`:
```markdown
# 사용법 (재현 가이드)

## 설치
```
python -m pip install -r requirements.txt
python scripts/make_fixtures.py   # 합성 fixture 생성 (테스트용)
python -m pytest -v               # 전체 테스트
```

## PHASE 0 — 발견
```
python scripts/cli.py discover .          # 현재 폴더 인벤토리
python scripts/cli.py discover ../../project/sample_data
python scripts/cli.py inspect path/to/file.nc
```
- 출력: 파일별 포맷(netcdf3/netcdf4/csv/unknown)·도메인 추정·좌표(1d/2d)·역할추정(output/reference) + `inventory.json`.
- 미지 포맷은 `openable=false`로 표시되고 `head_hex`가 함께 나온다.
```

- [ ] **Step 2: 실데이터 스모크 (옵션 — 원본이 있으면 실행)**

Run: `cd skills/validate-model-output && python scripts/cli.py discover ../../project/sample_data`
Expected: `era5_rean_glo_day_20220906.nc`(netcdf3, meteorology, reference 추정), `gfs_fcst_glo_day_masked_20220906.nc`(netcdf4, meteorology, output 추정) 행이 표에 출력. **여기서 GFS의 실제 변수명·단위·좌표(2D 여부)가 확인된다** → M2~M5의 `aliases.yaml`/`rules.yaml`에 실제 값 반영.

> 원본 파일이 환경에 없으면 이 단계는 건너뛴다(테스트는 합성 fixture로 이미 그린).

- [ ] **Step 3: 커밋**

```bash
git add skills/validate-model-output/SKILL.md skills/validate-model-output/references/usage.md
git commit -m "docs(validate): SKILL.md PHASE0/1 skeleton + usage guide"
```

---

## Self-Review (작성자 점검 결과)

**1. Spec coverage (M1 범위 한정):**
- 포맷 자동감지(원칙 1) → Task 4 ✓ / 좌표 1D·2D 적응(원칙 2) → Task 2 ✓ / 미지 포맷 실시간 점검(원칙 1·5) → Task 6 + SKILL.md Task 8 ✓ / 도메인 라우터(§9) → Task 5 ✓ / discover 인벤토리(PHASE 0) → Task 7 ✓ / 크래시 금지(원칙 9) → Task 4·6 (UnknownFormatError·probe no-crash) ✓ / 공통 Dataset 추상화(§5) → Task 2 ✓ / fixture 작게·git 포함(§12) → Task 3 ✓.
- M1 범위 밖(후속): rules.yaml·qc(M2), preprocess·metrics(M3), verify·regions·plots·recipes(M4), postprocess·4-페이즈 완성(M5). 의도된 분할.

**2. Placeholder scan:** "TBD/TODO/적절히 처리" 없음. 모든 코드 스텝에 실제 코드 포함. ✓

**3. Type consistency:**
- `Dataset` 메서드(`data_var_names/variables/latlon/coord_kind/grid_shape/time_info`)가 Task 2 정의와 io_detect/router/inspect/discover 사용처에서 일치. ✓
- `detect_format` 반환값('netcdf3'|'netcdf4'|'csv'|'unknown')이 io_detect·inspect에서 동일하게 사용. ✓
- 모듈 파일명 `inspect_file.py`(표준 `inspect` 충돌 회피) — 테스트·discover·cli import 전부 `inspect_file`로 통일. ✓
- `probe()` 반환 dict 키(openable/format/variables/coord_kind/domain/...)가 discover·cli에서 사용하는 키와 일치. ✓

---

## 다음 마일스톤 예고 (이 플랜 완료 후 각각 별도 플랜으로)
- **M2 validate(QC)**: `config/rules.yaml`, `scripts/qc.py`, `scripts/report.py`, `cli validate`, 고의결함 fixture + FAIL 보증 테스트.
- **M3 metrics**: `scripts/preprocess.py`, `config/aliases.yaml`, `scripts/metrics/{basic,pattern,distribution}.py` + 알려진값 단위테스트.
- **M4 verify**: `config/recipes.yaml`, `scripts/verify.py`, `scripts/regions.py`, `scripts/plots.py`, 나머지 metrics(vector/circular/spatial/timeseries/events), 다축 figure 리포트.
- **M5 packaging**: `scripts/derive.py`, postprocess, SKILL.md PHASE2/3 완성, submit/assets 사본·데모.
