import numpy as np
import xarray as xr
from dataset import Dataset
from rules import load_rules
from qc import check_variable


def _ds_from(name, values, units, standard_name=None):
    da = xr.DataArray(values, dims=("lat", "lon"),
                      coords={"lat": [0, 1, 2], "lon": [0, 1, 2]},
                      attrs={"units": units} | ({"standard_name": standard_name} if standard_name else {}))
    return Dataset(xr.Dataset({name: da}))


def _status(results, check):
    return [r["status"] for r in results if r["check"] == check]


def test_value_range_pass():
    d = _ds_from("t2m", np.full((3, 3), 280.0), "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "PASS" in _status(res, "value_range")


def test_value_range_fail():
    vals = np.full((3, 3), 280.0)
    vals[0, 0] = 500.0  # 물리범위 초과
    d = _ds_from("t2m", vals, "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "FAIL" in _status(res, "value_range")
    ev = [r["evidence"] for r in res if r["check"] == "value_range"][0]
    assert "500" in ev or "1" in ev  # 근거에 초과 개수/값 언급


def test_missing_fail():
    vals = np.full((3, 3), 280.0)
    vals[:, :] = np.nan
    vals[0, 0] = 280.0  # 거의 전부 결측
    d = _ds_from("t2m", vals, "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    assert "FAIL" in _status(res, "missing")


def test_unruled_variable_warns_not_crash():
    d = _ds_from("mystery", np.full((3, 3), 1.0), "widgets")
    res = check_variable(d, "mystery", load_rules())
    # 규칙 없음 → 크래시 없이 WARN 포함
    assert any(r["status"] == "WARN" for r in res)


def test_fillvalue_not_range_violation():
    vals = np.full((3, 3), 280.0)
    vals[0, 0] = 9.969209968386869e36   # NetCDF 기본 _FillValue 센티넬
    d = _ds_from("t2m", vals, "K", "air_temperature")
    res = check_variable(d, "t2m", load_rules())
    # 센티넬은 값범위 위반이 아니라 결측으로 분류
    assert "FAIL" not in _status(res, "value_range")
    assert any(r["check"] == "missing" for r in res)
