"""R4 도메인 판정 보강 — aliases.to_standard를 통한 한글 변수명 인식 검증.

부이 CSV가 한글 wave컬럼(유의파고/파주기/파향)을 가졌을 때 기상컬럼
다수결 오판 없이 waves 도메인으로 판정되는지 확인한다.
aliases.to_standard 표준화 경로(router._match_var step 3)와
파랑 headline 인식(router._is_wave_headline) 양쪽을 검증한다.

[소유: choibumku00]
"""
from __future__ import annotations

import sys
import os

import pytest

_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from dataset import Dataset
from router import detect_domain, _is_wave_headline, _match_var, _load_domains
from aliases import to_standard
from synth import era5_like
from synth_waves import buoy_obs_like


# ---------------------------------------------------------------------------
# 헬퍼: buoy DataFrame → xr.Dataset → Dataset
# ---------------------------------------------------------------------------

def _buoy_dataset() -> Dataset:
    """buoy_obs_like() DataFrame을 xr.Dataset으로 변환해 Dataset 래퍼로 반환한다."""
    df = buoy_obs_like()
    return Dataset(df.to_xarray())


# ---------------------------------------------------------------------------
# _is_wave_headline: 한글 '유의파고' 인식 (aliases 경로)
# ---------------------------------------------------------------------------

def test_is_wave_headline_korean():
    """_is_wave_headline이 '유의파고' 변수를 True로 판정해야 한다 (R4 aliases 경로)."""
    from dataset import Variable
    var = Variable(
        name="유의파고", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    assert _is_wave_headline(var), (
        "'유의파고' is a wave headline but _is_wave_headline returned False"
    )


def test_is_wave_headline_hs_unchanged():
    """기존 'hs' 변수는 여전히 wave headline으로 인식돼야 한다 (회귀)."""
    from dataset import Variable
    var = Variable(
        name="hs", dims=("time", "node"), shape=(6, 40),
        units="m", standard_name=None, long_name=None
    )
    assert _is_wave_headline(var)


def test_is_wave_headline_cf_standard_name_unchanged():
    """sea_surface_wave_significant_height standard_name 인식 불변 (회귀)."""
    from dataset import Variable
    var = Variable(
        name="SWH", dims=("time", "node"), shape=(6, 40),
        units="m", standard_name="sea_surface_wave_significant_height", long_name=None
    )
    assert _is_wave_headline(var)


# ---------------------------------------------------------------------------
# _match_var: 한글 변수명 → aliases → domains 매칭 (step 3)
# ---------------------------------------------------------------------------

def test_match_var_korean_wave_height():
    """'유의파고'가 waves 도메인으로 매칭돼야 한다 (aliases step 3a)."""
    from dataset import Variable
    domains = _load_domains()
    var = Variable(
        name="유의파고", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    result = _match_var(var, domains)
    assert result == "waves", f"expected 'waves', got '{result}'"


def test_match_var_korean_wave_period():
    """'파주기'가 waves 도메인으로 매칭돼야 한다 (aliases step 3a)."""
    from dataset import Variable
    domains = _load_domains()
    var = Variable(
        name="파주기", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    result = _match_var(var, domains)
    assert result == "waves", f"expected 'waves', got '{result}'"


def test_match_var_korean_wave_direction():
    """'파향'이 waves 도메인으로 매칭돼야 한다 (aliases step 3a)."""
    from dataset import Variable
    domains = _load_domains()
    var = Variable(
        name="파향", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    result = _match_var(var, domains)
    assert result == "waves", f"expected 'waves', got '{result}'"


def test_match_var_korean_wind_speed():
    """'풍속'이 meteorology 도메인으로 매칭돼야 한다 (aliases step 3a)."""
    from dataset import Variable
    domains = _load_domains()
    var = Variable(
        name="풍속", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    result = _match_var(var, domains)
    assert result == "meteorology", f"expected 'meteorology', got '{result}'"


def test_match_var_korean_sea_temperature():
    """'수온'이 ocean_temp_salinity 도메인으로 매칭돼야 한다 (aliases step 3a)."""
    from dataset import Variable
    domains = _load_domains()
    var = Variable(
        name="수온", dims=("index",), shape=(18,),
        units=None, standard_name=None, long_name=None
    )
    result = _match_var(var, domains)
    assert result == "ocean_temp_salinity", f"expected 'ocean_temp_salinity', got '{result}'"


# ---------------------------------------------------------------------------
# detect_domain: 부이 데이터 전체 판정 — 핵심 R4 테스트
# ---------------------------------------------------------------------------

def test_buoy_obs_detect_waves():
    """buoy_obs_like() Dataset → detect_domain이 'waves'를 반환해야 한다 (R4).

    유의파고/파주기/파향(wave) 외 풍속/수온(non-wave) 컬럼이 있어도
    '유의파고'가 파랑 headline으로 인식되므로 waves 도메인이 반환돼야 한다.
    기존에는 Korean 변수명 미인식으로 unknown 또는 meteorology 오판이 발생했다.
    """
    d = _buoy_dataset()
    result = detect_domain(d)
    assert result["domain"] == "waves", (
        f"R4: expected 'waves', got '{result['domain']}' "
        f"(matched={result['matched']}, confidence={result['confidence']})"
    )


def test_buoy_obs_matched_includes_wave_vars():
    """matched 딕셔너리에 한글 wave 변수가 포함돼야 한다."""
    d = _buoy_dataset()
    result = detect_domain(d)
    matched = result["matched"]
    assert "유의파고" in matched, f"'유의파고' not in matched: {matched}"
    assert matched["유의파고"] == "waves", (
        f"'유의파고' matched to '{matched['유의파고']}', expected 'waves'"
    )


# ---------------------------------------------------------------------------
# 회귀: 기존 era5_like → meteorology 불변
# ---------------------------------------------------------------------------

def test_era5_still_meteorology_alias_regression():
    """aliases 경로 추가 후에도 ERA5-like 기상 데이터는 meteorology로 판정돼야 한다."""
    result = detect_domain(Dataset(era5_like()))
    assert result["domain"] == "meteorology", (
        f"regression: expected 'meteorology', got '{result['domain']}'"
    )
    assert result["confidence"] > 0.5
