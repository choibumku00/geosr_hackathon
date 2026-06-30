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
    assert r["ok"] is False


def test_render_none_variable_dash():
    qc = {"checks": [{"check": "schema", "variable": None, "status": "PASS", "evidence": "ok"}],
          "summary": {"PASS": 1, "FAIL": 0, "WARN": 0}, "ok": True}
    md = render_markdown(qc, source="x.nc")
    assert "| - |" in md   # 변수 없는 행은 '-'


def test_render_escapes_pipe_in_evidence():
    qc = {"checks": [{"check": "value_range", "variable": "t2m", "status": "FAIL", "evidence": "범위 0|1 벗어남"}],
          "summary": {"PASS": 0, "FAIL": 1, "WARN": 0}, "ok": False}
    md = render_markdown(qc, source="x.nc")
    assert "0\\|1" in md          # 파이프가 이스케이프됨
    assert "0|1 벗어남" not in md  # 원본 비이스케이프 형태는 없어야


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
