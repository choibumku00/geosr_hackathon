import os
import xarray as xr
from synth import era5_like, gfs_like
from dataset import open_nc

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
        ds = open_nc(path)
        assert len(ds.data_vars) >= 1
        ds.close()
