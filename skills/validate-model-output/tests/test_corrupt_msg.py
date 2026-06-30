"""tests/test_corrupt_msg.py

손상/잘린 NetCDF 파일 열기 시 UnknownFormatError 메시지 검증.

- 정상 파일을 60 % 길이로 잘라 임시 파일 생성
- open_dataset 이 UnknownFormatError 를 발생시키는지 확인
- 메시지에 '열기 실패' 와 '손상' 이 포함되는지 확인
- 메시지가 'h5py' 단독 텍스트로만 구성되지 않는지 확인
"""
from __future__ import annotations

import os
import pytest

from io_detect import open_dataset, UnknownFormatError

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# NetCDF4(HDF5) 파일: 헤더(\x89HDF)가 선두 4바이트에 있으므로
# 60 % 잘림 후에도 detect_format 은 netcdf4 로 판단하지만 파일 내부 구조가 깨짐.
GFS_NC = os.path.join(DATA, "clean_gfs_like.nc")


@pytest.fixture
def truncated_nc(tmp_path):
    """정상 NetCDF4 파일을 60 % 길이로 잘라 반환."""
    src = GFS_NC
    size = os.path.getsize(src)
    cut = max(8, int(size * 0.6))  # 최소 8바이트 — 헤더 시그니처 보존
    dest = tmp_path / "truncated.nc"
    with open(src, "rb") as f:
        data = f.read(cut)
    dest.write_bytes(data)
    return str(dest)


@pytest.fixture
def bad_header_nc(tmp_path):
    """HDF5 시그니처를 유지하되 이후 내용을 쓰레기 바이트로 채운 파일."""
    dest = tmp_path / "bad_header.nc"
    # \x89HDF 로 시작 → detect_format 이 netcdf4 로 분류
    dest.write_bytes(b"\x89HDF\r\n\x1a\n" + b"\x00\xff\xfe\xfd" * 128)
    return str(dest)


# ─────────────────────────────────────────
# 테스트: 잘린 파일
# ─────────────────────────────────────────

def test_truncated_raises_unknown_format_error(truncated_nc):
    """잘린 NetCDF4 → UnknownFormatError."""
    with pytest.raises(UnknownFormatError):
        open_dataset(truncated_nc)


def test_truncated_message_contains_open_fail(truncated_nc):
    """메시지에 '열기 실패' 포함."""
    with pytest.raises(UnknownFormatError, match="열기 실패"):
        open_dataset(truncated_nc)


def test_truncated_message_contains_damage_hint(truncated_nc):
    """메시지에 '손상' 포함."""
    with pytest.raises(UnknownFormatError, match="손상"):
        open_dataset(truncated_nc)


def test_truncated_message_not_h5py_only(truncated_nc):
    """메시지가 'h5py' 단독이 아님 — 명확한 한국어 안내가 포함돼야 함."""
    with pytest.raises(UnknownFormatError) as exc_info:
        open_dataset(truncated_nc)
    msg = str(exc_info.value)
    # 메시지 자체가 'h5py' 로만 구성되면 안 됨
    assert msg.strip() != "h5py"
    # 한국어 안내(열기 실패 또는 손상)가 포함돼야 함
    assert "열기 실패" in msg or "손상" in msg


# ─────────────────────────────────────────
# 테스트: 깨진 헤더 파일
# ─────────────────────────────────────────

def test_bad_header_raises_unknown_format_error(bad_header_nc):
    """깨진 HDF5 헤더 → UnknownFormatError."""
    with pytest.raises(UnknownFormatError):
        open_dataset(bad_header_nc)


def test_bad_header_message_contains_open_fail(bad_header_nc):
    """메시지에 '열기 실패' 포함."""
    with pytest.raises(UnknownFormatError, match="열기 실패"):
        open_dataset(bad_header_nc)


def test_bad_header_message_contains_damage_hint(bad_header_nc):
    """메시지에 '손상' 포함."""
    with pytest.raises(UnknownFormatError, match="손상"):
        open_dataset(bad_header_nc)
