import numpy as np
import xarray as xr


def era5_like():
    """1D 좌표·K·CF standard_name·풍속 성분 포함 (ERA5 규약 모사)."""
    lat = np.linspace(-90, 90, 9)
    lon = np.linspace(0, 360, 12, endpoint=False)
    shape = (1, 9, 12)
    coords = {"time": [np.datetime64("2022-09-06")], "lat": lat, "lon": lon}

    def da(val, units, sn):
        return xr.DataArray(
            np.full(shape, val, dtype="float32"),
            dims=("time", "lat", "lon"), coords=coords,
            attrs={"units": units, "standard_name": sn},
        )

    return xr.Dataset({
        "t2m": da(280.0, "K", "air_temperature"),
        "u10": da(3.0, "m s-1", "eastward_wind"),
        "v10": da(-2.0, "m s-1", "northward_wind"),
    })


def gfs_like():
    """2D 좌표·°C·GRIB식 이름 (GFS 변환본 모사)."""
    ny, nx = 8, 10
    lat2d = np.tile(np.linspace(-60, 60, ny)[:, None], (1, nx)).astype("float32")
    lon2d = np.tile(np.linspace(0, 120, nx)[None, :], (ny, 1)).astype("float32")

    def da(val, units, long_name):
        return xr.DataArray(
            np.full((ny, nx), val, dtype="float32"), dims=("y", "x"),
            attrs={"units": units, "long_name": long_name},
        )

    ds = xr.Dataset({
        "TMP": da(12.0, "degC", "Temperature"),
        "UGRD": da(3.0, "m/s", "U component of wind"),
        "VGRD": da(-2.0, "m/s", "V component of wind"),
    })
    return ds.assign_coords(
        latitude=(("y", "x"), lat2d), longitude=(("y", "x"), lon2d)
    )


def broken_era5_like():
    """era5_like 기반 고의 결함본: 값범위초과(500K) + 결측구멍 + 위도 비단조."""
    ds = era5_like().copy(deep=True)
    t = ds["t2m"].values.copy()
    t[0, 0, 0] = 500.0          # 물리범위 초과
    t[0, 1, :] = np.nan         # 결측 구멍(한 위도줄 전체)
    ds["t2m"].values[:] = t
    lat = ds["lat"].values.copy()
    lat[2], lat[3] = lat[3], lat[2]   # 위도 비단조(2개 스왑)
    ds = ds.assign_coords(lat=lat)
    return ds
