"""QC 데모용 고의결함 파랑 fixture 생성.

SAMPLE — 실데이터에서는 구조를 실시간 점검하고
도메인 맞춤 코드로 적응하라.
주입한 결함 종류:
  ww3_broken.nc
    hs   : 첫 10 노드 × 전체 시간 → NaN(결측 구멍),
           마지막 5 노드 × 후반 3 시간 → 99 m(물리범위 초과)
    uwnd : 첫 5 노드 × 전체 시간 → 200 m/s(wind_component 규칙 초과)
           → run_qc 에서 value_range FAIL 유도
  buoy_broken.csv
    유의파고: 행0 → 50 m, 행3 → -1.5 m(음수), 행6·행9 → NaN
"""
from __future__ import annotations

import os
import sys

import numpy as np
import xarray as xr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TESTS = os.path.join(ROOT, "tests")
DATA = os.path.join(ROOT, "data")

# tests/synth_waves.py 임포트 경로 확보
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
# scripts/ 자체 경로 (_write_nc 재사용)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from synth_waves import buoy_obs_like, ww3_mesh_like  # noqa: E402
from make_fixtures import _write_nc                    # noqa: E402


def make_ww3_broken() -> xr.Dataset:
    """WW3 mesh fixture에 결함 주입.

    결함 1 — hs 결측 구멍:
        shape(6, 40) 중 첫 10 노드 전체 시간 → NaN (60/240 = 25%)
    결함 2 — hs 물리범위 초과:
        마지막 5 노드 × 후반 3 시간 → 99 m (바다에서 불가능한 파고)
    결함 3 — uwnd 극단치:
        첫 5 노드 × 전체 시간 → 200 m/s
        rules.yaml wind_component: valid_max=120 → value_range FAIL 유도

    SAMPLE — 실데이터에서는 결함 패턴·임계를 실시간 확인하라.
    """
    ds = ww3_mesh_like()

    # ── hs 결함 주입 ──────────────────────────────────────────────────
    hs = ds["hs"].values.copy()          # (time=6, node=40), float32

    # 결측 구멍: 첫 10 노드 전체 시간
    hs[:, :10] = np.nan

    # 물리범위 초과(99 m): 마지막 5 노드 × 후반 3 시간
    hs[3:, 35:] = 99.0

    # ── uwnd 극단치 주입 ──────────────────────────────────────────────
    # standard_name="eastward_wind" → wind_component 규칙 매칭
    # valid_min=-120, valid_max=120 → 200 m/s 는 FAIL
    uwnd = ds["uwnd"].values.copy()      # (time=6, node=40), float32
    uwnd[:, :5] = 200.0

    # Dataset 재구성 (좌표·속성 보존)
    ds_broken = ds.assign(
        hs=xr.DataArray(hs, dims=ds["hs"].dims, attrs=ds["hs"].attrs),
        uwnd=xr.DataArray(uwnd, dims=ds["uwnd"].dims, attrs=ds["uwnd"].attrs),
    )
    return ds_broken


def make_buoy_broken():
    """부이 관측 fixture에 결함 주입.

    유의파고 결함:
        행 0  → 50 m   (물리적으로 불가능한 파고)
        행 3  → -1.5 m (음수 파고)
        행 6  → NaN
        행 9  → NaN

    SAMPLE — 실데이터에서는 컬럼명·결측 표현을 실시간 확인하라.
    """
    df = buoy_obs_like().copy()

    df.loc[0, "유의파고"] = 50.0          # 비정상 극단치
    df.loc[3, "유의파고"] = -1.5          # 음수(물리 불가)
    df.loc[6, "유의파고"] = float("nan")  # 결측
    df.loc[9, "유의파고"] = float("nan")  # 결측

    return df


def main() -> None:
    os.makedirs(DATA, exist_ok=True)

    # ── WW3 결함 fixture → NetCDF4/HDF5 ──────────────────────────────
    nc_dest = os.path.join(DATA, "ww3_broken.nc")
    _write_nc(
        make_ww3_broken(),
        nc_dest,
        format="NETCDF4",
        engine="h5netcdf",
    )
    print(f"wrote {nc_dest}  ({os.path.getsize(nc_dest):,} bytes)")

    # ── 부이 결함 fixture → CSV (cp949) ──────────────────────────────
    csv_dest = os.path.join(DATA, "buoy_broken.csv")
    make_buoy_broken().to_csv(csv_dest, index=False, encoding="cp949")
    print(f"wrote {csv_dest}  ({os.path.getsize(csv_dest):,} bytes)")

    print("done.")


if __name__ == "__main__":
    main()
