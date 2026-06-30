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
