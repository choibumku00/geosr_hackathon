from __future__ import annotations

import os

from inspect_file import probe

_SCAN_EXTS = (".nc", ".nc4", ".csv", ".txt", ".tsv", ".dat", ".grib", ".grib2", ".grb")

_OUTPUT_HINTS = ("fcst", "forecast", "model", "pred", "output", "gfs", "wrf", "hindcast", "anal")
_REF_HINTS = ("rean", "reanalysis", "era5", "glorys", "obs", "buoy", "argo",
              "gauge", "sat", "ref", "truth", "waverys")


def guess_role(filename: str) -> str:
    low = filename.lower()
    is_out = any(h in low for h in _OUTPUT_HINTS)
    is_ref = any(h in low for h in _REF_HINTS)
    if is_out and not is_ref:
        return "output"
    if is_ref and not is_out:
        return "reference"
    return "unknown"


def _iter_files(path: str):
    if os.path.isdir(path):
        for root, _dirs, names in os.walk(path):
            for n in names:
                if os.path.splitext(n)[1].lower() in _SCAN_EXTS:
                    yield os.path.join(root, n)
    elif os.path.isfile(path):
        yield path


def discover(paths) -> dict:
    records = []
    for p in paths:
        for fp in _iter_files(p):
            rec = probe(fp)
            rec["role_guess"] = guess_role(os.path.basename(fp))
            records.append(rec)
    return {"files": records}
