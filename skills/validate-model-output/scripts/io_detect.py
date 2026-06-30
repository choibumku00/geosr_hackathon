from __future__ import annotations

# SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.

import os

import pandas as pd

from dataset import Dataset, open_nc

_TEXT_EXTS = (".csv", ".txt", ".tsv", ".dat")

# CSV 인코딩 폴백 순서: 한글 데이터 호환을 위해 cp949/euc-kr 포함
_CSV_ENCODINGS = ("utf-8", "cp949", "euc-kr", "latin-1")


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


def _read_csv_with_fallback(path: str) -> pd.DataFrame:
    """utf-8 → cp949 → euc-kr → latin-1 순으로 pd.read_csv 시도.

    모든 인코딩이 실패하면 UnknownFormatError 를 발생시킨다(크래시 없음).
    SAMPLE — 실데이터에선 파일 헤더나 BOM 을 먼저 확인해 인코딩을 고정하는 것이 안전하다.
    """
    last_exc: Exception | None = None
    for enc in _CSV_ENCODINGS:
        try:
            return pd.read_csv(path, encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            last_exc = ValueError(f"인코딩 {enc!r} 실패")
        except Exception as e:  # 컬럼 파싱 등 다른 오류는 즉시 전파
            raise UnknownFormatError(f"CSV 열기 실패: {path} ({e})")
    raise UnknownFormatError(
        f"CSV 인코딩 폴백 모두 실패 ({', '.join(_CSV_ENCODINGS)}): {path} — {last_exc}"
    )


def open_dataset(path: str) -> Dataset:
    fmt = detect_format(path)
    if fmt in ("netcdf3", "netcdf4"):
        try:
            ds = open_nc(path)
        except Exception as e:  # 손상·잘림 등
            raise UnknownFormatError(
                f"파일 열기 실패(손상/잘림 가능): {path} — {e}"
            )
        return Dataset(ds, source=path, fmt=fmt)
    if fmt == "csv":
        df = _read_csv_with_fallback(path)
        return Dataset(df.to_xarray(), source=path, fmt="csv")
    raise UnknownFormatError(f"미지원/미지 포맷: {path}")
