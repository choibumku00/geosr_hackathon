"""인수테스트 자동 검증 — run_acceptance 핵심 케이스.

conftest 가 scripts/ 를 sys.path 에 추가하므로 run_acceptance 를 직접 import 한다.
세션 스코프 fixture 로 한 번만 실행해 중복 연산을 방지한다.
"""
from __future__ import annotations

import pytest

from run_acceptance import run_acceptance


# ── 세션 스코프: 전 TC 를 한 번만 실행 ───────────────────────────────────────

@pytest.fixture(scope="session")
def _result():
    """run_acceptance() 를 세션 내 1회만 호출해 결과를 캐싱."""
    return run_acceptance()


# ── 공통 ─────────────────────────────────────────────────────────────────────

def test_no_crash_returns_dict(_result):
    """run_acceptance 가 예외 없이 dict 를 반환한다."""
    assert isinstance(_result, dict), "반환값이 dict 가 아님"
    assert "tc_b1" in _result, "tc_b1 키 없음"
    assert "tc_a1" in _result, "tc_a1 키 없음"
    assert "all_pass" in _result, "all_pass 키 없음"
    assert len(_result["tc_b1"]) == 3, "TC-B1 케이스 수 불일치"
    assert len(_result["tc_a1"]) == 2, "TC-A1 케이스 수 불일치"


# ── TC-B1 ─────────────────────────────────────────────────────────────────────

def test_tc_b1_clean_ok_true(_result):
    """era5_demo_clean.nc → QC ok=True, TC outcome=PASS."""
    clean = next(
        r for r in _result["tc_b1"] if "clean" in r["label"].lower()
    )
    assert clean["outcome"] == "PASS", (
        f"[TC-B1-1] outcome={clean['outcome']}: {clean.get('note')}"
    )
    assert clean.get("ok") is True, (
        f"[TC-B1-1] clean 파일 QC ok={clean.get('ok')} (True 기대)"
    )


def test_tc_b1_broken_ok_false(_result):
    """era5_demo_broken.nc → QC ok=False(결함 적발), TC outcome=PASS."""
    broken = next(
        r for r in _result["tc_b1"] if "broken" in r["label"].lower()
    )
    assert broken["outcome"] == "PASS", (
        f"[TC-B1-2] outcome={broken['outcome']}: {broken.get('note')}"
    )
    assert broken.get("ok") is False, (
        f"[TC-B1-2] broken 파일 QC ok={broken.get('ok')} (False 기대)"
    )


def test_tc_b1_truncated_open_fail_no_crash(_result):
    """era5_demo_truncated.nc → 열기 실패 기대, 크래시 없음, TC outcome=PASS."""
    trunc = next(
        r for r in _result["tc_b1"] if "truncat" in r["label"].lower()
    )
    assert trunc["outcome"] == "PASS", (
        f"[TC-B1-3] outcome={trunc['outcome']}: {trunc.get('note')}"
    )
    # ok 는 False 여야 함 (열기 실패 = QC 불통)
    assert trunc.get("ok") is False, (
        f"[TC-B1-3] ok={trunc.get('ok')} (False 기대 — 열기 실패이므로)"
    )


# ── TC-A1 ─────────────────────────────────────────────────────────────────────

def test_tc_a1_mesh_domain_waves(_result):
    """ww3_mesh_like.nc → domain=waves, coord_kind=mesh."""
    mesh = next(
        r for r in _result["tc_a1"]
        if "ww3" in r["label"].lower() or "mesh" in r["label"].lower()
    )
    assert mesh["outcome"] == "PASS", (
        f"[TC-A1-1] outcome={mesh['outcome']}: {mesh.get('note')}"
    )
    assert mesh.get("domain") == "waves", (
        f"[TC-A1-1] domain={mesh.get('domain')!r} (waves 기대)"
    )
    assert mesh.get("coord_kind") == "mesh", (
        f"[TC-A1-1] coord_kind={mesh.get('coord_kind')!r} (mesh 기대)"
    )


def test_tc_a1_buoy_openable(_result):
    """buoy_obs_like.csv → openable=True (cp949 폴백 포함)."""
    buoy = next(
        r for r in _result["tc_a1"] if "buoy" in r["label"].lower()
    )
    assert buoy["outcome"] == "PASS", (
        f"[TC-A1-2] outcome={buoy['outcome']}: {buoy.get('note')}"
    )
    assert buoy.get("openable") is True, (
        f"[TC-A1-2] openable={buoy.get('openable')} (True 기대)"
    )
