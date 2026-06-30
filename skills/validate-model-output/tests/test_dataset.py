import numpy as np
import xarray as xr
from dataset import Dataset, Variable


def _era5_like():
    # 1D 좌표·K·CF standard_name
    lat = np.linspace(-90, 90, 5)
    lon = np.linspace(0, 360, 6, endpoint=False)
    t2m = xr.DataArray(
        np.full((1, 5, 6), 280.0), dims=("time", "lat", "lon"),
        coords={"time": [np.datetime64("2022-09-06")], "lat": lat, "lon": lon},
        attrs={"units": "K", "standard_name": "air_temperature"},
    )
    return xr.Dataset({"t2m": t2m})


def _gfs_like():
    # 2D 좌표·°C·GRIB식 이름
    ny, nx = 4, 5
    lat2d = np.tile(np.linspace(-60, 60, ny)[:, None], (1, nx))
    lon2d = np.tile(np.linspace(0, 100, nx)[None, :], (ny, 1))
    tmp = xr.DataArray(
        np.full((ny, nx), 12.0), dims=("y", "x"),
        attrs={"units": "degC", "long_name": "Temperature"},
    )
    ds = xr.Dataset({"TMP": tmp})
    ds = ds.assign_coords(
        latitude=(("y", "x"), lat2d), longitude=(("y", "x"), lon2d)
    )
    return ds


def test_variables_metadata():
    d = Dataset(_era5_like(), source="a.nc", fmt="netcdf3")
    vs = d.variables()
    assert "t2m" in vs
    v = vs["t2m"]
    assert isinstance(v, Variable)
    assert v.units == "K"
    assert v.standard_name == "air_temperature"
    assert v.shape == (1, 5, 6)


def test_latlon_1d():
    d = Dataset(_era5_like())
    assert d.latlon() == ("lat", "lon", False)
    assert d.coord_kind() == "1d"
    assert d.grid_shape() == (5, 6)


def test_latlon_2d():
    d = Dataset(_gfs_like())
    name_lat, name_lon, is_2d = d.latlon()
    assert (name_lat, name_lon, is_2d) == ("latitude", "longitude", True)
    assert d.coord_kind() == "2d"
    assert d.grid_shape() == (4, 5)


def test_time_info():
    d = Dataset(_era5_like())
    ti = d.time_info()
    assert ti["n_steps"] == 1
    assert ti["start"].startswith("2022-09-06")


def test_no_time():
    d = Dataset(_gfs_like())
    assert d.time_info() is None
