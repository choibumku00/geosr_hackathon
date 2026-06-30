"""tests/test_preprocess2.py — tz_to_utc / inject_point_coords / parse_points_list / common_time_index 집중 테스트.

대상 함수:
  tz_to_utc(times, tz)
  inject_point_coords(station_ids, mapping)
  parse_points_list(path)
  common_time_index(t1, t2)

실행:
  cd skills/validate-model-output
  python -m pytest tests/test_preprocess2.py -q
"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pytest

# scripts/ 를 sys.path 에 명시적으로 추가 (conftest 보완)
HERE    = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from preprocess import (
    common_time_index,
    inject_point_coords,
    parse_points_list,
    tz_to_utc,
)


# ===========================================================================
# 1. tz_to_utc — 시간대 변환
# ===========================================================================

class TestTzToUtc:
    """tz_to_utc 함수 검증."""

    def test_kst_09_to_utc_00(self):
        """KST 09:00 → UTC 00:00 변환; assumed=False."""
        t = np.array(["2024-01-01T09:00:00"], dtype="datetime64[ns]")
        result, assumed = tz_to_utc(t, tz="KST")
        expected = np.datetime64("2024-01-01T00:00:00", "ns")
        assert result[0] == expected
        assert assumed is False

    def test_kst_plus09_alias(self):
        """+09:00 표기도 KST 와 동일하게 처리; assumed=False."""
        t = np.array(["2024-06-01T09:00:00"], dtype="datetime64[ns]")
        result, assumed = tz_to_utc(t, tz="+09:00")
        expected = np.datetime64("2024-06-01T00:00:00", "ns")
        assert result[0] == expected
        assert assumed is False

    def test_utc_passthrough(self):
        """tz='UTC' → 원본 그대로 반환; assumed=False."""
        t = np.array(["2024-03-15T12:00:00"], dtype="datetime64[ns]")
        result, assumed = tz_to_utc(t, tz="UTC")
        assert result[0] == t[0]
        assert assumed is False

    def test_none_assumed_true_values_unchanged(self):
        """tz=None → UTC로 가정(assumed=True), 값은 변환 없이 그대로."""
        t = np.array(["2024-01-01T06:00:00"], dtype="datetime64[ns]")
        result, assumed = tz_to_utc(t, tz=None)
        assert result[0] == t[0]
        assert assumed is True

    def test_unknown_tz_warns_and_assumed_true(self):
        """알 수 없는 tz → UserWarning 발생 + assumed=True."""
        t = np.array(["2024-01-01T00:00:00"], dtype="datetime64[ns]")
        with pytest.warns(UserWarning):
            result, assumed = tz_to_utc(t, tz="JST")
        assert assumed is True

    def test_multiple_timestamps(self):
        """복수 타임스탬프 — 전체 배열에 -9h 적용."""
        t = np.array(
            ["2024-01-01T09:00:00", "2024-01-01T18:00:00"],
            dtype="datetime64[ns]",
        )
        result, assumed = tz_to_utc(t, tz="KST")
        assert result[0] == np.datetime64("2024-01-01T00:00:00", "ns")
        assert result[1] == np.datetime64("2024-01-01T09:00:00", "ns")
        assert assumed is False

    def test_returns_ndarray_and_bool(self):
        """반환값 타입: (np.ndarray, bool)."""
        t = np.array(["2024-01-01T09:00:00"], dtype="datetime64[ns]")
        result, assumed = tz_to_utc(t, tz="KST")
        assert isinstance(result, np.ndarray)
        assert isinstance(assumed, bool)


# ===========================================================================
# 2. inject_point_coords — 정점 좌표 주입
# ===========================================================================

class TestInjectPointCoords:
    """inject_point_coords 함수 검증."""

    @pytest.fixture()
    def mapping(self):
        """샘플 {정점ID: (lat, lon)} 매핑."""
        return {
            "S001": (35.1, 129.0),
            "S002": (34.5, 127.3),
        }

    def test_known_ids_correct_coords(self, mapping):
        """알려진 ID → 올바른 위경도 반환."""
        lats, lons = inject_point_coords(["S001", "S002"], mapping)
        assert lats[0] == pytest.approx(35.1)
        assert lons[0] == pytest.approx(129.0)
        assert lats[1] == pytest.approx(34.5)
        assert lons[1] == pytest.approx(127.3)

    def test_unknown_id_returns_nan(self, mapping):
        """없는 ID → lat/lon 모두 nan."""
        lats, lons = inject_point_coords(["S001", "S999"], mapping)
        assert not np.isnan(lats[0])   # S001 은 정상
        assert np.isnan(lats[1])       # S999 는 nan
        assert np.isnan(lons[1])

    def test_all_unknown_all_nan(self, mapping):
        """전부 없는 ID → 전부 nan."""
        lats, lons = inject_point_coords(["X1", "X2"], mapping)
        assert np.all(np.isnan(lats))
        assert np.all(np.isnan(lons))

    def test_empty_ids_returns_empty_arrays(self, mapping):
        """빈 목록 → 빈 배열 반환, no-crash."""
        lats, lons = inject_point_coords([], mapping)
        assert len(lats) == 0
        assert len(lons) == 0

    def test_returns_ndarray_pair(self, mapping):
        """반환값은 (np.ndarray, np.ndarray) 튜플."""
        lats, lons = inject_point_coords(["S001"], mapping)
        assert isinstance(lats, np.ndarray)
        assert isinstance(lons, np.ndarray)

    def test_output_length_matches_input(self, mapping):
        """출력 길이 = 입력 ID 수."""
        ids = ["S001", "S999", "S002"]
        lats, lons = inject_point_coords(ids, mapping)
        assert len(lats) == 3
        assert len(lons) == 3


# ===========================================================================
# 3. parse_points_list — 관측점 파일 파싱
# ===========================================================================

class TestParsePointsList:
    """parse_points_list 함수 검증."""

    def _write_tmp(self, content: str) -> str:
        """임시 utf-8 파일 생성 후 경로 반환."""
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_basic_lon_lat_id(self):
        """'lon lat id' 공백 구분 기본 포맷 파싱."""
        content = "129.0 35.1 S001\n127.3 34.5 S002\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert "S001" in result
        assert result["S001"] == pytest.approx((35.1, 129.0))
        assert result["S002"] == pytest.approx((34.5, 127.3))

    def test_comment_lines_skipped(self):
        """# 주석 라인은 건너뜀."""
        content = "# 관측점 목록\n129.0 35.1 S001\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert "S001" in result
        # 주석 줄이 키로 들어가지 않아야 함
        assert all(not k.startswith("#") for k in result)

    def test_blank_lines_skipped(self):
        """빈 줄 포함 → no-crash, 유효 항목만 파싱."""
        content = "129.0 35.1 S001\n\n127.3 34.5 S002\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert len(result) == 2

    def test_returns_dict(self):
        """반환값은 dict 타입."""
        content = "129.0 35.1 S001\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert isinstance(result, dict)

    def test_empty_file_returns_empty_dict(self):
        """빈 파일 → 빈 dict, no-crash."""
        path = self._write_tmp("")
        result = parse_points_list(path)
        assert result == {}

    def test_tab_separated(self):
        """탭 구분자도 관용 파싱."""
        content = "129.0\t35.1\tS001\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert "S001" in result

    def test_invalid_line_skipped_no_crash(self):
        """파싱 불가 줄 포함 → no-crash, 유효 항목만 반환."""
        content = "not_a_float 35.1 S001\n129.0 35.1 S002\n"
        path = self._write_tmp(content)
        result = parse_points_list(path)
        assert "S002" in result
        # S001 줄은 float 변환 실패라 건너뜀
        assert "S001" not in result


# ===========================================================================
# 4. common_time_index — 교집합 인덱스
# ===========================================================================

class TestCommonTimeIndex:
    """common_time_index 함수 검증."""

    def test_partial_overlap_indices(self):
        """부분 교집합 — 올바른 인덱스 반환."""
        t1 = np.array(
            ["2024-01-01", "2024-01-02", "2024-01-03"], dtype="datetime64[ns]"
        )
        t2 = np.array(
            ["2024-01-02", "2024-01-03", "2024-01-04"], dtype="datetime64[ns]"
        )
        idx1, idx2 = common_time_index(t1, t2)
        # 교집합: 2024-01-02 (t1[1], t2[0]), 2024-01-03 (t1[2], t2[1])
        assert set(idx1.tolist()) == {1, 2}
        assert set(idx2.tolist()) == {0, 1}

    def test_extracted_values_match(self):
        """idx1, idx2 로 추출한 값이 서로 동일."""
        t1 = np.array(
            ["2024-01-01", "2024-01-02", "2024-01-03"], dtype="datetime64[ns]"
        )
        t2 = np.array(
            ["2024-01-02", "2024-01-03", "2024-01-04"], dtype="datetime64[ns]"
        )
        idx1, idx2 = common_time_index(t1, t2)
        np.testing.assert_array_equal(t1[idx1], t2[idx2])

    def test_no_overlap_empty_arrays(self):
        """교집합 없음 → 빈 배열 반환, no-crash."""
        t1 = np.array(["2024-01-01", "2024-01-02"], dtype="datetime64[ns]")
        t2 = np.array(["2024-01-05", "2024-01-06"], dtype="datetime64[ns]")
        idx1, idx2 = common_time_index(t1, t2)
        assert len(idx1) == 0
        assert len(idx2) == 0

    def test_full_overlap_all_indices(self):
        """완전 교집합 → 전체 인덱스(정렬 보장)."""
        t1 = np.array(["2024-01-01", "2024-01-02"], dtype="datetime64[ns]")
        t2 = np.array(["2024-01-01", "2024-01-02"], dtype="datetime64[ns]")
        idx1, idx2 = common_time_index(t1, t2)
        assert len(idx1) == 2
        assert len(idx2) == 2

    def test_returns_ndarray_pair(self):
        """반환값은 (np.ndarray, np.ndarray) 튜플."""
        t1 = np.array(["2024-01-01"], dtype="datetime64[ns]")
        t2 = np.array(["2024-01-01"], dtype="datetime64[ns]")
        idx1, idx2 = common_time_index(t1, t2)
        assert isinstance(idx1, np.ndarray)
        assert isinstance(idx2, np.ndarray)

    def test_string_input_accepted(self):
        """문자열 배열 입력도 처리 가능 (no-crash)."""
        t1 = ["2024-01-01", "2024-01-02"]
        t2 = ["2024-01-02", "2024-01-03"]
        idx1, idx2 = common_time_index(t1, t2)
        # 교집합: 2024-01-02 → t1[1], t2[0]
        assert 1 in idx1.tolist()
        assert 0 in idx2.tolist()
