"""작은 합성 fixture 를 data/ 에 생성한다 (실제 원본 없이 재현 가능)."""
import os
import sys
import shutil
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tests"))
DATA = os.path.join(os.path.dirname(HERE), "data")

from synth import era5_like, gfs_like  # noqa: E402


def main():
    os.makedirs(DATA, exist_ok=True)

    # Windows: netCDF4 C library can't handle non-ASCII paths; write to tempdir first.
    with tempfile.TemporaryDirectory() as tmpdir:
        # ERA5 모사 → NetCDF3 (CDF 시그니처)
        tmp_era5 = os.path.join(tmpdir, "clean_era5_like.nc")
        era5_like().to_netcdf(tmp_era5, format="NETCDF3_64BIT")
        shutil.copy2(tmp_era5, os.path.join(DATA, "clean_era5_like.nc"))

        # GFS 모사 → NetCDF4/HDF5 (\x89HDF 시그니처)
        tmp_gfs = os.path.join(tmpdir, "clean_gfs_like.nc")
        gfs_like().to_netcdf(tmp_gfs, format="NETCDF4", engine="h5netcdf")
        shutil.copy2(tmp_gfs, os.path.join(DATA, "clean_gfs_like.nc"))

    print("wrote fixtures to", DATA)


if __name__ == "__main__":
    main()
