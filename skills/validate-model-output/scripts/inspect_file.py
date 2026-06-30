from __future__ import annotations

import os

from io_detect import detect_format, open_dataset, UnknownFormatError
from router import detect_domain


def _head_hex(path: str, n: int = 16) -> str:
    try:
        with open(path, "rb") as f:
            return f.read(n).hex()
    except OSError:
        return ""


def probe(path: str) -> dict:
    """단일 파일 구조를 best-effort 로 파악. 항상 dict 반환(크래시 금지)."""
    if not os.path.exists(path):
        return {"path": path, "format": "unknown", "openable": False,
                "unknown": True, "head_hex": "", "error": "파일 없음"}
    fmt = detect_format(path)
    try:
        d = open_dataset(path)
    except UnknownFormatError as e:
        return {"path": path, "format": fmt, "openable": False,
                "unknown": True, "head_hex": _head_hex(path), "error": str(e)}

    dom = detect_domain(d)
    ll = d.latlon()
    vars_summary = []
    for name, v in d.variables().items():
        vars_summary.append({
            "name": name, "dims": list(v.dims), "units": v.units,
            "standard_name": v.standard_name,
        })
    return {
        "path": path,
        "format": d.fmt,
        "openable": True,
        "variables": vars_summary,
        "coord_kind": d.coord_kind(),
        "latlon": list(ll) if ll else None,
        "grid_shape": list(d.grid_shape()) if d.grid_shape() else None,
        "time": d.time_info(),
        "domain": dom["domain"],
        "confidence": dom["confidence"],
    }
