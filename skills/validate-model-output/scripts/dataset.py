from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import xarray as xr


def open_nc(path: str) -> "xr.Dataset":
    """비-ASCII(한글) 경로에서 netCDF4 C 라이브러리가 OSError(Errno 22)를 내는
    Windows 문제를 우회: 기본 엔진 → 실패 시 파이썬 기반 엔진(scipy: NetCDF3, h5netcdf: HDF5) 순으로 시도."""
    attempts = [dict(), dict(engine="h5netcdf"), dict(engine="scipy")]
    last_err = None
    for kw in attempts:
        try:
            return xr.open_dataset(path, **kw)
        except (OSError, ValueError) as e:   # 좁은 예외: ImportError 등은 즉시 전파
            last_err = e
            continue
    raise last_err

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

    def _find_in_coords(self, names) -> Optional[str]:
        """coords 안에서만 후보 이름 탐색 — data_vars 제외.

        정규 격자 판별에 사용: data variable로 저장된 mesh lat/lon을
        좌표로 오인하지 않기 위해 self._ds.coords만 탐색한다.
        """
        for cand in self._ds.coords:
            if str(cand).lower() in names:
                return str(cand)
        # standard_name 매칭 (coords 내)
        for cand in self._ds.coords:
            sn = str(self._ds[cand].attrs.get("standard_name", "")).lower()
            if sn == "latitude" and "latitude" in names:
                return str(cand)
            if sn == "longitude" and "longitude" in names:
                return str(cand)
        return None

    def _find_data_var(self, names) -> Optional[str]:
        """data_vars 안에서만 후보 이름 탐색 — coords 제외.

        mesh lat/lon 탐색에 사용.
        """
        for cand in self._ds.data_vars:
            if str(cand).lower() in names:
                return str(cand)
        # standard_name 매칭 (data_vars 내)
        for cand in self._ds.data_vars:
            sn = str(self._ds[cand].attrs.get("standard_name", "")).lower()
            if sn == "latitude" and "latitude" in names:
                return str(cand)
            if sn == "longitude" and "longitude" in names:
                return str(cand)
        return None

    def latlon(self) -> Optional[tuple]:
        """정규 격자의 lat/lon 좌표 변수를 탐색한다.

        coords에 등록된 변수만 대상으로 하므로,
        mesh 데이터의 data variable lat/lon은 반환하지 않는다.
        """
        lat = self._find_in_coords(_LAT_NAMES)
        lon = self._find_in_coords(_LON_NAMES)
        if lat is None or lon is None:
            return None
        is_2d = self._ds[lat].ndim == 2
        return (lat, lon, is_2d)

    def is_mesh(self) -> bool:
        """비정형 mesh 여부를 반환한다.

        latitude/longitude(또는 standard_name)가 동일 단일차원을 공유하는
        data variable이고, 정규 lat/lon 격자축이 없으면 True.
        기존 1d/2d 정규 격자가 있으면 False.

        SAMPLE — 실데이터에서는 mesh 토폴로지 구조(변수명·차원명)를
        실시간 점검하고 도메인 맞춤 코드로 적응하라.
        """
        # 정규 격자가 있으면 mesh 아님 (우선순위: 1d/2d > mesh)
        if self.latlon() is not None:
            return False
        lat_var = self._find_data_var(_LAT_NAMES)
        lon_var = self._find_data_var(_LON_NAMES)
        if lat_var is None or lon_var is None:
            return False
        lat_da = self._ds[lat_var]
        lon_da = self._ds[lon_var]
        # 둘 다 1D이고 같은 차원을 공유해야 함
        if lat_da.ndim == 1 and lon_da.ndim == 1:
            return lat_da.dims[0] == lon_da.dims[0]
        return False

    def coord_kind(self) -> str:
        """격자 좌표 종류 반환.

        우선순위: 정규 1d → 정규 2d → mesh → none.
        기존 '1d'/'2d'/'none' 의미 불변.
        """
        ll = self.latlon()
        if ll is not None:
            return "2d" if ll[2] else "1d"
        if self.is_mesh():
            return "mesh"
        return "none"

    def grid_shape(self) -> Optional[tuple]:
        """격자 형상 반환.

        - 정규 1d: (n_lat, n_lon)
        - 정규 2d: (ny, nx)  — lat 변수의 shape
        - mesh:    (n_nodes,)
        - none:    None
        """
        ll = self.latlon()
        if ll is not None:
            lat_name, lon_name, is_2d = ll
            if is_2d:
                return tuple(int(s) for s in self._ds[lat_name].shape)
            return (int(self._ds[lat_name].size), int(self._ds[lon_name].size))
        if self.is_mesh():
            lat_var = self._find_data_var(_LAT_NAMES)
            if lat_var is not None:
                return (int(self._ds[lat_var].size),)
        return None

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
