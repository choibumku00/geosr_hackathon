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
