from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import xarray as xr

# 좌표 이름 후보 (소문자 비교)
_LAT_NAMES = ("lat", "latitude", "nav_lat", "gphit", "y")
_LON_NAMES = ("lon", "longitude", "nav_lon", "glamt", "x")
_TIME_NAMES = ("time", "valid_time", "t")


@dataclass
class Variable:
    name: str
    dims: tuple
    shape: tuple
    units: Optional[str]
    standard_name: Optional[str]
    long_name: Optional[str]
    attrs: dict = field(default_factory=dict)


class Dataset:
    """포맷 무관 자료 추상화. 내부적으로 xarray.Dataset을 감싼다."""

    def __init__(self, xr_ds: xr.Dataset, source: str = "", fmt: str = ""):
        self._ds = xr_ds
        self.source = source
        self.fmt = fmt

    @property
    def xr(self) -> xr.Dataset:
        return self._ds

    def data_var_names(self) -> list:
        return [str(v) for v in self._ds.data_vars]

    def variable(self, name: str) -> Variable:
        da = self._ds[name]
        a = dict(da.attrs)
        return Variable(
            name=str(name),
            dims=tuple(str(d) for d in da.dims),
            shape=tuple(int(s) for s in da.shape),
            units=a.get("units"),
            standard_name=a.get("standard_name"),
            long_name=a.get("long_name"),
            attrs=a,
        )

    def variables(self) -> dict:
        return {n: self.variable(n) for n in self.data_var_names()}

    def _find(self, names) -> Optional[str]:
        # coords + variables 에서 후보 이름(또는 standard_name) 탐색
        all_names = list(self._ds.coords) + list(self._ds.variables)
        for cand in all_names:
            low = str(cand).lower()
            if low in names:
                return str(cand)
        # standard_name 매칭
        for cand in self._ds.variables:
            sn = str(self._ds[cand].attrs.get("standard_name", "")).lower()
            if sn in ("latitude",) and "latitude" in names:
                return str(cand)
            if sn in ("longitude",) and "longitude" in names:
                return str(cand)
        return None

    def latlon(self) -> Optional[tuple]:
        lat = self._find(_LAT_NAMES)
        lon = self._find(_LON_NAMES)
        if lat is None or lon is None:
            return None
        is_2d = self._ds[lat].ndim == 2
        return (lat, lon, is_2d)

    def coord_kind(self) -> str:
        ll = self.latlon()
        if ll is None:
            return "none"
        return "2d" if ll[2] else "1d"

    def grid_shape(self) -> Optional[tuple]:
        ll = self.latlon()
        if ll is None:
            return None
        lat_name, lon_name, is_2d = ll
        if is_2d:
            return tuple(int(s) for s in self._ds[lat_name].shape)
        return (int(self._ds[lat_name].size), int(self._ds[lon_name].size))

    def time_info(self) -> Optional[dict]:
        tname = self._find(_TIME_NAMES)
        if tname is None:
            return None
        tvals = self._ds[tname].values
        n = int(np.size(tvals))
        flat = np.atleast_1d(tvals)
        return {
            "name": tname,
            "n_steps": n,
            "start": str(flat[0]),
            "end": str(flat[-1]),
        }
