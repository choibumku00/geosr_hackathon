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


def test_probe_directory_no_crash(tmp_path):
    r = probe(str(tmp_path))   # a directory exists but isn't a readable file
    assert r["openable"] is False
