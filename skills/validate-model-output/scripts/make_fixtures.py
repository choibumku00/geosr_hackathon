"""작은 합성 fixture 를 data/ 에 생성한다 (실제 원본 없이 재현 가능)."""
import os
import sys
import shutil
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tests"))
DATA = os.path.join(os.path.dirname(HERE), "data")

from synth import era5_like, gfs_like, broken_era5_like  # noqa: E402


def _write_nc(ds, dest, **kw):
    """Write dataset to dest via an ASCII temp dir (workaround for non-ASCII paths
    that the netCDF4 C library cannot open on Windows)."""
    fname = os.path.basename(dest)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = os.path.join(tmpdir, fname)
        ds.to_netcdf(tmp_path, **kw)
        shutil.copy2(tmp_path, dest)


def main():
    os.makedirs(DATA, exist_ok=True)

    # ERA5 모사 → NetCDF3 (CDF 시그니처)
    _write_nc(era5_like(), os.path.join(DATA, "clean_era5_like.nc"),
              format="NETCDF3_64BIT")

    # GFS 모사 → NetCDF4/HDF5 (\x89HDF 시그니처)
    _write_nc(gfs_like(), os.path.join(DATA, "clean_gfs_like.nc"),
              format="NETCDF4", engine="h5netcdf")

    # 고의 결함본 (QC 데모/테스트용) — NetCDF3
    _write_nc(broken_era5_like(), os.path.join(DATA, "broken_era5_like.nc"),
              format="NETCDF3_64BIT")

    print("wrote fixtures to", DATA)


if __name__ == "__main__":
    main()
