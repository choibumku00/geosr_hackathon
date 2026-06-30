"""aliases.py 단위 테스트.

SAMPLE — 실데이터 헤더 패턴이 추가되면 테스트 케이스도 함께 보강하라.
"""
from __future__ import annotations

import pytest
from aliases import load_aliases, to_standard, _build_lookup


# ---------------------------------------------------------------------------
# load_aliases
# ---------------------------------------------------------------------------

class TestLoadAliases:
    def test_returns_dict(self):
        result = load_aliases()
        assert isinstance(result, dict)

    def test_contains_significant_wave_height(self):
        aliases = load_aliases()
        assert "significant_wave_height" in aliases

    def test_missing_file_returns_empty(self, tmp_path):
        result = load_aliases(str(tmp_path / "nonexistent.yaml"))
        assert result == {}


# ---------------------------------------------------------------------------
# to_standard — 핵심 요구사항 3가지
# ---------------------------------------------------------------------------

class TestToStandard:
    def test_korean_with_unit_bracket(self):
        """유의파고(m) → significant_wave_height"""
        assert to_standard("유의파고(m)") == "significant_wave_height"

    def test_uppercase_alias(self):
        """UGRD (대문자) → eastward_wind"""
        assert to_standard("UGRD") == "eastward_wind"

    def test_unknown_returns_none(self):
        """모름 → None"""
        assert to_standard("모름") is None

    # 추가 케이스 -------------------------------------------------------

    def test_korean_no_bracket(self):
        """유의파고 (괄호 없이) → significant_wave_height"""
        assert to_standard("유의파고") == "significant_wave_height"

    def test_wave_period_korean_with_bracket(self):
        """파주기(sec) → wave_period"""
        assert to_standard("파주기(sec)") == "wave_period"

    def test_wave_period_alias_t01(self):
        assert to_standard("t01") == "wave_period"

    def test_wave_direction_korean(self):
        assert to_standard("파향") == "wave_direction"

    def test_sea_water_temperature_korean(self):
        """수온 → sea_water_temperature"""
        assert to_standard("수온") == "sea_water_temperature"

    def test_sea_water_temperature_with_bracket(self):
        """수온(°C) → sea_water_temperature"""
        assert to_standard("수온(°C)") == "sea_water_temperature"

    def test_northward_wind_vwnd(self):
        assert to_standard("vwnd") == "northward_wind"

    def test_wind_speed_korean(self):
        assert to_standard("풍속") == "wind_speed"

    def test_case_insensitive_mixed(self):
        """HM0 (대소혼합) → significant_wave_height"""
        assert to_standard("HM0") == "significant_wave_height"

    def test_alias_hs_lowercase(self):
        assert to_standard("hs") == "significant_wave_height"


# ---------------------------------------------------------------------------
# _build_lookup (내부 함수 직접 검증)
# ---------------------------------------------------------------------------

class TestBuildLookup:
    def test_lookup_keys_are_lowercase(self):
        aliases = {"test_var": ["AliasA", "한글별칭"]}
        lookup = _build_lookup(aliases)
        assert "aliasa" in lookup
        assert "한글별칭" in lookup

    def test_lookup_value_is_standard_name(self):
        aliases = {"eastward_wind": ["UWND", "u10"]}
        lookup = _build_lookup(aliases)
        assert lookup["uwnd"] == "eastward_wind"
        assert lookup["u10"] == "eastward_wind"
