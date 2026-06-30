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
