from __future__ import annotations

import json
import os

_EMOJI = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}

_ADVISORY = (
    "> 해석 임계(물리범위·N-시그마 등)는 **advisory**(영역·변수·해상도 의존). "
    "층위1 QC는 기준자료 불필요(intrinsic) — 기준자료는 truth가 아니라 reference."
)


def build_report(qc_result: dict, source: str) -> dict:
    return {
        "source": source,
        "ok": qc_result["ok"],
        "summary": qc_result["summary"],
        "checks": qc_result["checks"],
    }


def render_markdown(qc_result: dict, source: str) -> str:
    s = qc_result["summary"]
    verdict = "PASS ✅" if qc_result["ok"] else "FAIL ❌"
    lines = [
        f"# QC 리포트 — `{os.path.basename(source)}`",
        "",
        f"**종합: {verdict}**  (PASS {s.get('PASS',0)} · FAIL {s.get('FAIL',0)} · WARN {s.get('WARN',0)})",
        "",
        "| 상태 | 검사 | 변수 | 근거 |",
        "|---|---|---|---|",
    ]
    for c in qc_result["checks"]:
        em = _EMOJI.get(c["status"], c["status"])
        var = c.get("variable") or "-"
        ev = str(c.get("evidence", "")).replace("|", "\\|")
        lines.append(f"| {em} {c['status']} | {c['check']} | {var} | {ev} |")
    lines += ["", _ADVISORY, ""]
    return "\n".join(lines)


def write_report(qc_result: dict, source: str, out_dir: str) -> tuple:
    os.makedirs(out_dir, exist_ok=True)
    jpath = os.path.join(out_dir, "report.json")
    mpath = os.path.join(out_dir, "report.md")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(build_report(qc_result, source), f, ensure_ascii=False, indent=2)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_markdown(qc_result, source))
    return jpath, mpath
