import numpy as np
import xarray as xr
from dataset import Dataset
from router import detect_domain
from synth import era5_like, gfs_like


def test_meteorology_from_cf_names():
    r = detect_domain(Dataset(era5_like()))
    assert r["domain"] == "meteorology"
    assert r["confidence"] > 0.5


def test_meteorology_from_grib_names():
    r = detect_domain(Dataset(gfs_like()))
    assert r["domain"] == "meteorology"


def test_ocean_temp_salinity():
    sst = xr.DataArray(
        np.full((3, 3), 290.0), dims=("lat", "lon"),
        coords={"lat": [0, 1, 2], "lon": [0, 1, 2]},
        attrs={"units": "K", "standard_name": "sea_surface_temperature"},
    )
    r = detect_domain(Dataset(xr.Dataset({"sst": sst})))
    assert r["domain"] == "ocean_temp_salinity"


def test_unknown_domain():
    foo = xr.DataArray(
        np.zeros((2, 2)), dims=("a", "b"), attrs={"long_name": "mystery quantity"}
    )
    r = detect_domain(Dataset(xr.Dataset({"foo": foo})))
    assert r["domain"] == "unknown"
    assert r["confidence"] == 0.0
