import json
import os
from report import build_report, render_markdown, write_report

_QC = {
    "checks": [
        {"check": "value_range", "variable": "t2m", "status": "FAIL", "evidence": "500K 초과 1개"},
        {"check": "missing", "variable": "t2m", "status": "PASS", "evidence": "결측 0%"},
    ],
    "summary": {"PASS": 1, "FAIL": 1, "WARN": 0},
    "ok": False,
}


def test_build_report_structure():
    r = build_report(_QC, source="x.nc")
    assert r["source"] == "x.nc"
    assert r["summary"]["FAIL"] == 1
    assert len(r["checks"]) == 2


def test_render_markdown_contains_evidence_and_advisory():
    md = render_markdown(_QC, source="x.nc")
    assert "FAIL" in md
    assert "500K 초과 1개" in md
    assert "t2m" in md
    assert "advisory" in md.lower() or "reference" in md.lower()


def test_write_report_files(tmp_path):
    jpath, mpath = write_report(_QC, source="x.nc", out_dir=str(tmp_path))
    assert os.path.exists(jpath) and os.path.exists(mpath)
    with open(jpath, encoding="utf-8") as f:
        data = json.load(f)
    assert data["ok"] is False
    assert "FAIL" in open(mpath, encoding="utf-8").read()
