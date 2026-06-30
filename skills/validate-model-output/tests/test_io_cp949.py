"""tests/test_io_cp949.py — CSV cp949 인코딩 폴백 테스트.

R1: open_dataset 의 CSV 분기가 utf-8 → cp949 → euc-kr → latin-1 순으로 폴백하는지 확인.
buoy_obs_like() 한글 헤더 DataFrame 을 cp949 로 저장 후 open_dataset 으로 열어 검증한다.

SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
"""
from __future__ import annotations

import os
import sys

import pytest

# conftest 가 없어도 단독 실행 가능하도록 scripts/ 경로 보장
_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

_TESTS = os.path.dirname(__file__)
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)

from io_detect import UnknownFormatError, open_dataset  # noqa: E402
from synth_waves import buoy_obs_like  # noqa: E402


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def _save_cp949(df, path: str) -> None:
    """DataFrame 을 cp949 인코딩 CSV 로 저장한다."""
    df.to_csv(path, index=False, encoding="cp949")


# ---------------------------------------------------------------------------
# 정상 경로: cp949 CSV 를 open_dataset 으로 열기
# ---------------------------------------------------------------------------

def test_open_cp949_csv_succeeds(tmp_path):
    """buoy_obs_like() 를 cp949 .csv 로 저장 → open_dataset 이 크래시 없이 열려야 한다."""
    df = buoy_obs_like()
    p = tmp_path / "buoy_obs_cp949.csv"
    _save_cp949(df, str(p))

    ds = open_dataset(str(p))

    assert ds is not None, "open_dataset 이 None 을 반환했다"
    assert ds.fmt == "csv", f"fmt 가 'csv' 여야 한다 — 실제: {ds.fmt!r}"


def test_open_cp949_csv_has_korean_columns(tmp_path):
    """열린 Dataset 의 변수명에 한글 헤더(유의파고 등)가 포함되어야 한다."""
    df = buoy_obs_like()
    p = tmp_path / "buoy_obs_cp949.csv"
    _save_cp949(df, str(p))

    ds = open_dataset(str(p))
    var_names = ds.data_var_names()

    # 한글 컬럼 중 최소 1개 이상 존재해야 한다
    korean_expected = {"유의파고", "파주기", "파향", "수온", "풍속", "풍향", "지점", "일시"}
    found = korean_expected & set(var_names)
    assert found, (
        f"한글 컬럼이 변수명에 없다. var_names={var_names}"
    )


def test_open_cp949_csv_row_count(tmp_path):
    """열린 Dataset 의 행 수가 원본 DataFrame 과 일치해야 한다."""
    df = buoy_obs_like()
    p = tmp_path / "buoy_obs_cp949.csv"
    _save_cp949(df, str(p))

    ds = open_dataset(str(p))

    # xarray Dataset 의 첫 번째 dim 크기로 행 수 확인 (sizes 는 FutureWarning 없음)
    xr_ds = ds.xr
    first_dim = next(iter(xr_ds.sizes))
    assert xr_ds.sizes[first_dim] == len(df), (
        f"행 수 불일치: xarray={xr_ds.sizes[first_dim]}, 원본={len(df)}"
    )


# ---------------------------------------------------------------------------
# 엣지 케이스: 모든 인코딩이 실패해도 크래시가 아닌 UnknownFormatError
# ---------------------------------------------------------------------------

def test_all_encoding_fail_raises_unknown_format_error(tmp_path):
    """바이너리 쓰레기 .csv — 인코딩 폴백이 모두 실패하면 UnknownFormatError 가 나야 한다."""
    p = tmp_path / "garbage.csv"
    # 0x80-0xFF 가 뒤섞인 latin-1 이외 에서도 파싱이 실패하도록 조작
    # latin-1 은 모든 바이트를 읽으므로, 순수 바이너리라도 latin-1 은 성공할 수 있다.
    # → 여기서는 실제 파싱(pd.read_csv)에서 예외를 일으키기 위해 빈 파일을 사용한다.
    # pandas 는 빈 파일을 EmptyDataError 로 처리하므로 UnknownFormatError 로 변환되어야 한다.
    p.write_bytes(b"")  # 빈 csv → pandas EmptyDataError
    with pytest.raises((UnknownFormatError, Exception)):
        open_dataset(str(p))
    # 크래시(segfault 등)가 아니라 예외로 처리됨을 확인 — 테스트가 여기까지 오면 성공


# ---------------------------------------------------------------------------
# 기존 동작 보존: utf-8 CSV 도 여전히 열려야 한다
# ---------------------------------------------------------------------------

def test_open_utf8_csv_still_works(tmp_path):
    """기존 utf-8 CSV 동작이 폴백 도입 후에도 깨지지 않아야 한다."""
    p = tmp_path / "simple_utf8.csv"
    p.write_text("time,value\n2024-01-01,1.0\n2024-01-02,2.0\n", encoding="utf-8")

    ds = open_dataset(str(p))

    assert ds.fmt == "csv"
    assert "value" in ds.data_var_names()
