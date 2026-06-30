"""SAMPLE — 인수테스트 자동러너 (DEMO_SCENARIO TC 자동화)

SAMPLE — 실데이터 실시간 점검·도메인 맞춤 코드로 적응.
이 구현은 대표 TC SAMPLE이다. 실데이터 적용 시
픽스처 경로·기대 도메인·QC 임계를 실제 데이터에 맞게 조정하라.

TC-B1: validate 3케이스
  B1-1  era5_demo_clean.nc     → QC ok=True  (PASS 기대)
  B1-2  era5_demo_broken.nc    → QC ok=False (FAIL: value_range/grid 기대)
  B1-3  era5_demo_truncated.nc → 열기 실패   (무크래시 기대)

TC-A1: discover 2케이스
  A1-1  ww3_mesh_like.nc    → domain=waves, coord_kind=mesh
  A1-2  buoy_obs_like.csv   → openable=True (csv)

실행:
  python scripts/run_acceptance.py
반환값(프로그래밍 호출):
  dict(tc_b1=list[dict], tc_a1=list[dict], all_pass=bool)
"""
from __future__ import annotations

import os
import sys

# scripts/ 를 import 경로에 추가 (형제 모듈 import)
_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL = os.path.dirname(_HERE)           # validate-model-output/
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from io_detect import open_dataset, UnknownFormatError  # noqa: E402
from qc import run_qc                                   # noqa: E402
from inspect_file import probe                          # noqa: E402

# 데모픽스처 경로(우선) / data/ 폴백
_KIT_ROOT = os.path.dirname(os.path.dirname(_SKILL))  # geosr-hackathon-kit/
_DEMO_FIXTURE_DIR = os.path.join(_KIT_ROOT, "project", "scenario", "fixtures")
_DATA_DIR = os.path.join(_SKILL, "data")


def _fixture(demo_name: str, fallback_name: str | None = None) -> str:
    """데모픽스처 경로 반환. 없으면 data/ 폴백."""
    primary = os.path.join(_DEMO_FIXTURE_DIR, demo_name)
    if os.path.exists(primary):
        return primary
    return os.path.join(_DATA_DIR, fallback_name or demo_name)


# ── TC-B1 내부 실행기 ─────────────────────────────────────────────────────────

def _run_b1(path: str, label: str, expect_ok: bool,
            expect_open_fail: bool = False) -> dict:
    """단일 파일 QC 수행 후 기대 결과와 대조. 크래시 없음.

    Parameters
    ----------
    path             : 검사할 파일 경로
    label            : TC 레이블 문자열
    expect_ok        : QC ok 기대값 (True=PASS 기대, False=FAIL 기대)
    expect_open_fail : True 이면 open 단계 실패를 기대 (truncated NC 등)

    Returns
    -------
    dict with keys: label, path, expect_ok, expect_open_fail,
                    ok(bool), outcome("PASS"|"FAIL"), note(str),
                    summary(dict, QC 성공 시만), failed_checks(list, QC 성공 시만)
    """
    rec: dict = {
        "label": label,
        "path": path,
        "expect_ok": expect_ok,
        "expect_open_fail": expect_open_fail,
    }

    # open 단계
    try:
        d = open_dataset(path)
    except Exception as e:          # UnknownFormatError·OSError·기타 — 크래시 없이 처리
        rec["ok"] = False
        if expect_open_fail:
            rec["outcome"] = "PASS"
            rec["note"] = f"기대대로 열기 실패 (무크래시): {type(e).__name__}"
        else:
            rec["outcome"] = "FAIL"
            rec["note"] = f"예상치 못한 열기 실패: {e}"
        return rec

    if expect_open_fail:
        rec["ok"] = True
        rec["outcome"] = "FAIL"
        rec["note"] = "열기 실패 예상이었으나 성공함"
        return rec

    # QC 단계
    try:
        qc = run_qc(d)
    except Exception as e:          # 크래시 방지
        rec["ok"] = False
        rec["outcome"] = "FAIL"
        rec["note"] = f"run_qc 예외(크래시 방지): {e}"
        return rec

    rec["ok"] = qc["ok"]
    rec["summary"] = qc["summary"]
    rec["failed_checks"] = [c["check"] for c in qc["checks"] if c["status"] == "FAIL"]

    if qc["ok"] == expect_ok:
        rec["outcome"] = "PASS"
        rec["note"] = (
            f"ok={qc['ok']} (기대 {expect_ok}), "
            f"FAIL체크={rec['failed_checks']}"
        )
    else:
        rec["outcome"] = "FAIL"
        rec["note"] = (
            f"ok={qc['ok']} 기대={expect_ok}, "
            f"FAIL체크={rec['failed_checks']}"
        )
    return rec


# ── TC-A1 내부 실행기 ─────────────────────────────────────────────────────────

def _run_a1(path: str, label: str, expect_openable: bool = True,
            expect_domain: str | None = None,
            expect_coord_kind: str | None = None) -> dict:
    """단일 파일 probe 수행 후 기대 결과와 대조. 크래시 없음.

    Parameters
    ----------
    path              : 검사할 파일 경로
    label             : TC 레이블 문자열
    expect_openable   : True 이면 openable=True 기대
    expect_domain     : 기대 도메인 ("waves", "meteorology" 등); None 이면 비교 생략
    expect_coord_kind : 기대 좌표 종류 ("mesh", "1d", "2d"); None 이면 비교 생략

    Returns
    -------
    dict with keys: label, path, openable, domain, coord_kind, format,
                    outcome("PASS"|"FAIL"), note(str)
    """
    try:
        rec = probe(path)           # probe 는 내부적으로 크래시 없이 dict 반환
    except Exception as e:          # 혹시 모를 예외 대비
        return {
            "label": label, "path": path,
            "openable": False, "domain": None, "coord_kind": None, "format": None,
            "outcome": "FAIL", "note": f"probe 예외(크래시 방지): {e}",
        }

    result: dict = {
        "label": label,
        "path": path,
        "openable": rec.get("openable", False),
        "domain": rec.get("domain"),
        "coord_kind": rec.get("coord_kind"),
        "format": rec.get("format"),
    }

    mismatches: list[str] = []
    if expect_openable and not rec.get("openable"):
        mismatches.append(
            f"openable=False (기대 True), error={rec.get('error', '-')}"
        )
    if expect_domain is not None and rec.get("domain") != expect_domain:
        mismatches.append(
            f"domain={rec.get('domain')!r} (기대 {expect_domain!r})"
        )
    if expect_coord_kind is not None and rec.get("coord_kind") != expect_coord_kind:
        mismatches.append(
            f"coord_kind={rec.get('coord_kind')!r} (기대 {expect_coord_kind!r})"
        )

    if mismatches:
        result["outcome"] = "FAIL"
        result["note"] = "; ".join(mismatches)
    else:
        result["outcome"] = "PASS"
        result["note"] = (
            f"domain={rec.get('domain')}, "
            f"coord_kind={rec.get('coord_kind')}, "
            f"format={rec.get('format')}"
        )
    return result


# ── 메인 공개 함수 ────────────────────────────────────────────────────────────

def run_acceptance() -> dict:
    """TC-B1(validate 3케이스) + TC-A1(discover 2케이스) 인수테스트 실행.

    결과를 PASS/FAIL 표로 stdout 에 출력하고 dict 를 반환한다.

    Returns
    -------
    dict
        tc_b1     : list[dict]  — TC-B1 결과 목록 (각 항목은 _run_b1 반환값)
        tc_a1     : list[dict]  — TC-A1 결과 목록 (각 항목은 _run_a1 반환값)
        all_pass  : bool        — 전 TC outcome == "PASS" 여부
    """
    # ── TC-B1: validate ──────────────────────────────────────────────────────
    tc_b1 = [
        _run_b1(
            _fixture("era5_demo_clean.nc", "clean_era5_like.nc"),
            "TC-B1-1: era5_demo_clean → PASS기대",
            expect_ok=True,
        ),
        _run_b1(
            _fixture("era5_demo_broken.nc", "broken_era5_like.nc"),
            "TC-B1-2: era5_demo_broken → FAIL기대",
            expect_ok=False,
        ),
        _run_b1(
            _fixture("era5_demo_truncated.nc"),
            "TC-B1-3: era5_demo_truncated → 열기FAIL기대",
            expect_ok=False,
            expect_open_fail=True,
        ),
    ]

    # ── TC-A1: discover ──────────────────────────────────────────────────────
    tc_a1 = [
        _run_a1(
            os.path.join(_DATA_DIR, "ww3_mesh_like.nc"),
            "TC-A1-1: ww3_mesh_like → waves/mesh기대",
            expect_domain="waves",
            expect_coord_kind="mesh",
        ),
        _run_a1(
            os.path.join(_DATA_DIR, "buoy_obs_like.csv"),
            "TC-A1-2: buoy_obs_like.csv → 열림기대",
            expect_openable=True,
        ),
    ]

    all_pass = all(r["outcome"] == "PASS" for r in tc_b1 + tc_a1)
    _print_results(tc_b1, tc_a1)
    return {"tc_b1": tc_b1, "tc_a1": tc_a1, "all_pass": all_pass}


def _print_results(tc_b1: list, tc_a1: list) -> None:
    """PASS/FAIL 표를 stdout 에 출력."""
    width = 76
    print("\n" + "=" * width)
    print("  인수테스트 결과 (DEMO_SCENARIO)")
    print("=" * width)
    print(f"{'TC 케이스':<46} {'결과':<7} {'비고'}")
    print("-" * width)
    for r in tc_b1 + tc_a1:
        label = r["label"][:45]
        outcome = r["outcome"]
        note = r.get("note", "")[:50]
        print(f"{label:<46} {outcome:<7} {note}")
    print("=" * width)
    all_tc = tc_b1 + tc_a1
    n_pass = sum(1 for r in all_tc if r["outcome"] == "PASS")
    n_total = len(all_tc)
    status = "ALL PASS" if n_pass == n_total else f"{n_total - n_pass}건 FAIL"
    print(f"  합계: {n_pass}/{n_total} PASS  [{status}]")
    print("=" * width + "\n")


# ── 직접 실행 ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    result = run_acceptance()
    sys.exit(0 if result["all_pass"] else 1)
