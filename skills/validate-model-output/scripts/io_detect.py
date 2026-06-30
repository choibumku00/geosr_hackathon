from __future__ import annotations

import os

import pandas as pd

from dataset import Dataset, open_nc

_TEXT_EXTS = (".csv", ".txt", ".tsv", ".dat")


class UnknownFormatError(Exception):
    pass


def detect_format(path: str) -> str:
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
    except OSError as e:
        raise UnknownFormatError(f"열 수 없음: {path} ({e})")
    if sig[:3] == b"CDF":
        return "netcdf3"
    if sig[:4] == b"\x89HDF":
        return "netcdf4"
    ext = os.path.splitext(path)[1].lower()
    if ext in _TEXT_EXTS:
        return "csv"
    # 텍스트로 읽혀 콤마가 보이면 csv 로 간주 (확장자 없는 경우)
    try:
        head = sig.decode("utf-8")
        if "," in head:
            return "csv"
    except UnicodeDecodeError:
        pass
    return "unknown"


def open_dataset(path: str) -> Dataset:
    fmt = detect_format(path)
    if fmt in ("netcdf3", "netcdf4"):
        try:
            ds = open_nc(path)
        except Exception as e:  # 손상 등
            raise UnknownFormatError(f"NetCDF 열기 실패: {path} ({e})")
        return Dataset(ds, source=path, fmt=fmt)
    if fmt == "csv":
        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise UnknownFormatError(f"CSV 열기 실패: {path} ({e})")
        return Dataset(df.to_xarray(), source=path, fmt="csv")
    raise UnknownFormatError(f"미지원/미지 포맷: {path}")
