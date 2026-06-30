"""R4b 도메인 판정 보강 검증.

(a) 좌표·보조 변수(longitude/latitude/tri/MAPSTA 등) 투표 제외
(b) 파랑 headline(hs/hm0/swh/standard_name) 있으면 winds 다수결보다 waves 우선
(c) discover.guess_role 'anal' 힌트 추가
"""
import sys
import os

import pytest

# conftest 가 scripts/ 를 sys.path 에 추가하지만 직접 실행 시 대비
_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from dataset import Dataset
from router import detect_domain
from discover import guess_role
from synth import era5_like
from synth_waves import ww3_mesh_like


# ---------------------------------------------------------------------------
# R4b (a)+(b): WW3 비정형 mesh — 풍속 성분(uwnd/vwnd)이 다수지만 waves 판정
# ---------------------------------------------------------------------------

def test_ww3_mesh_detect_waves():
    """ww3_mesh_like 데이터셋에서 waves 도메인이 반환돼야 한다.

    uwnd/vwnd(meteorology) 2개 vs hs(waves) 1개이지만,
    hs 에 sea_surface_wave_significant_height standard_name이 있으므로
    R4b (b) headline 우선 규칙으로 waves 반환.
    longitude/latitude/tri/MAPSTA 는 (a) 규칙으로 투표에서 제외.
    """
    d = Dataset(ww3_mesh_like())
    result = detect_domain(d)
    assert result["domain"] == "waves", (
        f"expected 'waves', got '{result['domain']}' (matched={result['matched']})"
    )


def test_ww3_mesh_matched_excludes_aux_vars():
    """longitude, latitude, tri, MAPSTA 는 matched dict에 포함되지 않아야 한다."""
    d = Dataset(ww3_mesh_like())
    result = detect_domain(d)
    matched_keys_lower = {k.lower() for k in result["matched"]}
    for aux in ("longitude", "latitude", "tri", "mapsta"):
        assert aux not in matched_keys_lower, (
            f"보조 변수 '{aux}' 가 matched 에 포함됨: {result['matched']}"
        )


# ---------------------------------------------------------------------------
# R4b (c): discover.guess_role 'anal' 힌트
# ---------------------------------------------------------------------------

def test_guess_role_anal():
    """파일명에 'anal' 이 포함되면 output 으로 분류돼야 한다."""
    assert guess_role("geo_ww3_anal_2024.nc") == "output"


def test_guess_role_anal_mixed_case():
    """'ANAL' 대소문자 무관 인식."""
    assert guess_role("ww3_ANAL_test.nc") == "output"


# ---------------------------------------------------------------------------
# 회귀: 기존 era5_like → meteorology 불변
# ---------------------------------------------------------------------------

def test_era5_still_meteorology():
    """R4b 변경 후에도 ERA5-like 기상 데이터는 meteorology 로 판정돼야 한다."""
    result = detect_domain(Dataset(era5_like()))
    assert result["domain"] == "meteorology", (
        f"regression: expected 'meteorology', got '{result['domain']}'"
    )
    assert result["confidence"] > 0.5
