"""파랑 데모용 합성 fixture 생성.

생성 파일:
  data/ww3_mesh_like.nc   — WW3 비정형 mesh NetCDF4/HDF5
  data/buoy_obs_like.csv  — 부이 점관측 CSV (cp949, 한글 헤더)

한글 경로 문제: NetCDF 쓰기는 make_fixtures._write_nc() 경유
(ASCII temp dir → copy 방식으로 Windows OSError 우회).

SAMPLE — 실데이터에서는 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TESTS = os.path.join(ROOT, "tests")
DATA = os.path.join(ROOT, "data")

# tests/synth_waves.py 가 임포트 가능하도록 경로 추가
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
# scripts/ 자체 경로 (make_fixtures._write_nc 재사용)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from synth_waves import ww3_mesh_like, buoy_obs_like   # noqa: E402
from make_fixtures import _write_nc                     # noqa: E402


def main() -> None:
    os.makedirs(DATA, exist_ok=True)

    # ── WW3 비정형 mesh → NetCDF4/HDF5 ───────────────────────────────
    nc_dest = os.path.join(DATA, "ww3_mesh_like.nc")
    _write_nc(
        ww3_mesh_like(),
        nc_dest,
        format="NETCDF4",
        engine="h5netcdf",
    )
    size_nc = os.path.getsize(nc_dest)
    print(f"wrote {nc_dest}  ({size_nc:,} bytes)")

    # ── 부이 점관측 → CSV (cp949 필수: 한글 헤더 보존) ───────────────
    csv_dest = os.path.join(DATA, "buoy_obs_like.csv")
    buoy_obs_like().to_csv(csv_dest, index=False, encoding="cp949")
    size_csv = os.path.getsize(csv_dest)
    print(f"wrote {csv_dest}  ({size_csv:,} bytes)")

    print("done.")


if __name__ == "__main__":
    main()
