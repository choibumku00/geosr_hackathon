import os
import sys
from functools import wraps

# scripts/ 디렉터리를 import 경로에 추가 (모듈은 형제 import 사용)
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

# Windows: netCDF4 C library cannot handle non-ASCII paths (OSError/Errno 22).
# Patch xr.open_dataset to try scipy (NetCDF3) then h5netcdf (NetCDF4) as
# fallbacks so tests work transparently without modifying test code.
import xarray as xr  # noqa: E402

_orig_open_dataset = xr.open_dataset


@wraps(_orig_open_dataset)
def _open_dataset_with_fallback(filename_or_obj, *args, **kwargs):
    if kwargs.get("engine"):
        return _orig_open_dataset(filename_or_obj, *args, **kwargs)
    try:
        return _orig_open_dataset(filename_or_obj, *args, **kwargs)
    except OSError:
        for fallback_engine in ("scipy", "h5netcdf"):
            try:
                return _orig_open_dataset(
                    filename_or_obj, *args, engine=fallback_engine, **kwargs
                )
            except Exception:
                continue
        raise


xr.open_dataset = _open_dataset_with_fallback
