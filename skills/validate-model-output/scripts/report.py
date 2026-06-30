from __future__ import annotations

import json
import math
import os

_EMOJI = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}

_ADVISORY = (
    "> 해석 임계(물리범위·N-시그마 등)는 **advisory**(영역·변수·해상도 의존). "
    "층위1 QC는 기준자료 불필요(intrinsic) — 기준자료는 truth가 아니라 reference."
)

# ---------------------------------------------------------------------------
# verify 전용 advisory 캡션 (§G)
# ---------------------------------------------------------------------------
_TZ_WARNING = (
    "> **[TZ 미확인 경고]** 시간대(TZ) 메타가 없어 UTC로 가정했습니다. "
    "부이 관측이 KST(UTC+9)이고 모델이 UTC이면 **9시간 불일치**가 발생합니다. "
    "`--ref-tz KST` 를 명시하면 자동 보정됩니다."
)

_ADVISORY_VERIFY = (
    "> **[§G Advisory]** "
    "기준자료(reference)는 truth가 아닙니다. "
    "단일 지표·단일 그림만으로 모델 성능을 결론짓지 마십시오. "
    "임계 판정 없음(advisory) — 도메인·변수·해상도별 합격 기준을 별도 정의하십시오. "
    "이상치·기기 오류·시공간 매칭 오차를 실데이터에서 반드시 점검하십시오."
)


# ---------------------------------------------------------------------------
# 기존 QC 렌더 (그대로 보존)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# verify 전용 렌더 (신규)
# ---------------------------------------------------------------------------

def _fmt(val, fmt: str = ".4f") -> str:
    """숫자 포맷 — None/nan 은 '-' 반환."""
    if val is None:
        return "-"
    try:
        v = float(val)
        if math.isnan(v) or math.isinf(v):
            return str(v)
        return format(v, fmt)
    except (TypeError, ValueError):
        return str(val)


def _plot_link(path: str | None, label: str) -> str:
    """절대 경로를 마크다운 이미지 링크로 변환. None 이면 '(없음)' 반환."""
    if not path:
        return "(없음)"
    return f"![{label}]({path})"


def _accuracy_table(rows: list) -> list[str]:
    """accuracy_rows 를 마크다운 표 행으로 변환한다."""
    lines = [
        "| 변수 | N | Bias | RMSE | SI | Pearson r |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        vname = str(row.get("variable", "-"))
        n     = str(row.get("n", "-"))
        b     = _fmt(row.get("bias"))
        r     = _fmt(row.get("rmse"))
        s     = _fmt(row.get("si"))
        pr    = _fmt(row.get("pearson_r"))
        lines.append(f"| {vname} | {n} | {b} | {r} | {s} | {pr} |")
    return lines


def _direction_table(rows: list) -> list[str]:
    """direction_rows 를 마크다운 표 행으로 변환한다."""
    lines = [
        "| 변수 | N | Circular ME (°) | Circular RMSE (°) | Circular Corr |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        vname = str(row.get("variable", "-"))
        n     = str(row.get("n", "-"))
        cme   = _fmt(row.get("circular_cme"))
        crmse = _fmt(row.get("circular_rmse"))
        cc    = _fmt(row.get("circular_corr"))
        lines.append(f"| {vname} | {n} | {cme} | {crmse} | {cc} |")
    return lines


def render_verify_markdown(
    verify_result: dict,
    model_path: str = "",
    ref_path: str = "",
) -> str:
    """verify 결과를 다축 마크다운 보고서로 렌더링한다.

    SAMPLE — 실데이터 적용 시 임계 기준·섹션 구성을 도메인 맞춤으로 확장하라.

    Parameters
    ----------
    verify_result : dict
        {mode, model, ref, tz_assumed, accuracy_rows, direction_rows,
         plots, regions, info} (모두 선택적 — 없으면 기본값 처리).
    model_path, ref_path : str
        verify_result["model"/"ref"] 가 없을 때 폴백 경로.
    """
    mode       = verify_result.get("mode", "unknown")
    m_path     = verify_result.get("model", model_path)
    r_path     = verify_result.get("ref", ref_path)
    tz_assumed = bool(verify_result.get("tz_assumed", False))
    acc_rows   = verify_result.get("accuracy_rows", [])
    dir_rows   = verify_result.get("direction_rows", [])
    plots      = verify_result.get("plots", {})
    regions    = verify_result.get("regions", [])
    info       = verify_result.get("info", "")

    mode_label = {"grid_to_grid": "격자↔격자", "mesh_point": "mesh↔점관측"}.get(
        mode, mode
    )

    lines: list[str] = [
        f"# Verify 리포트 — {mode_label}",
        "",
        f"- **모델**: `{os.path.basename(m_path)}`",
        f"- **기준**: `{os.path.basename(r_path)}`",
    ]
    if info:
        lines.append(f"- **정보**: {info}")
    lines.append("")

    # ── § 정확도 ──────────────────────────────────────────────────────────────
    lines += ["## § 정확도 (Accuracy)", ""]
    if acc_rows:
        lines += _accuracy_table(acc_rows)
    else:
        lines.append("(정확도 메트릭 없음 — 공통 변수를 확인하라)")
    lines.append("")

    # ── § 분포 ────────────────────────────────────────────────────────────────
    lines += [
        "## § 분포 (Distribution)",
        "",
        f"Q-Q Plot: {_plot_link(plots.get('qq'), 'QQ Plot')}",
        "",
    ]

    # ── § 시간 ────────────────────────────────────────────────────────────────
    lines += [
        "## § 시간 (Time)",
        "",
        f"Scatter: {_plot_link(plots.get('scatter'), 'Scatter')}",
        f"Timeseries: {_plot_link(plots.get('timeseries'), 'Timeseries')}",
        "",
    ]

    # ── § 방향 ────────────────────────────────────────────────────────────────
    lines += ["## § 방향 (Direction)", ""]
    if dir_rows:
        lines += _direction_table(dir_rows)
        lines.append("")
        rose_m = plots.get("wave_rose_model")
        rose_r = plots.get("wave_rose_ref")
        if rose_m or rose_r:
            lines.append("파향·풍향 로즈:")
            if rose_m:
                lines.append(f"  - 모델: {_plot_link(rose_m, 'Rose(Model)')}")
            if rose_r:
                lines.append(f"  - 기준: {_plot_link(rose_r, 'Rose(Ref)')}")
            lines.append("")
    else:
        lines.append("(방향 변수 없음 — 파향·풍향 변수를 확인하라)")
        lines.append("")

    # ── § 종합 ────────────────────────────────────────────────────────────────
    lines += [
        "## § 종합 (Summary)",
        "",
        f"Taylor Diagram: {_plot_link(plots.get('taylor'), 'Taylor')}",
        f"Diff Map: {_plot_link(plots.get('diff_map'), 'Diff Map')}",
        "",
    ]

    # ── § 해역별 ──────────────────────────────────────────────────────────────
    if regions:
        lines += ["## § 해역별 정확도 (Regional)", ""]
        for reg in regions:
            rname     = str(reg.get("name", "?"))
            reg_acc   = reg.get("accuracy_rows", [])
            reg_dir   = reg.get("direction_rows", [])
            lines.append(f"### {rname}")
            lines.append("")
            if reg_acc:
                lines += _accuracy_table(reg_acc)
                lines.append("")
            else:
                lines.append("(해당 해역 정확도 없음)")
                lines.append("")
            if reg_dir:
                lines += _direction_table(reg_dir)
                lines.append("")

    # ── §G Advisory + TZ 경고 ────────────────────────────────────────────────
    if tz_assumed:
        lines += [_TZ_WARNING, ""]
    lines += [_ADVISORY_VERIFY, ""]

    return "\n".join(lines)


def write_verify_report(
    verify_result: dict,
    model_path: str,
    ref_path: str,
    out_dir: str,
) -> tuple:
    """verify 결과를 JSON + 마크다운으로 저장한다.

    기존 write_report(QC용)와 독립 — 파일명 verify_report.json/.md.

    Returns
    -------
    (jpath, mpath) : tuple[str, str]
    """
    os.makedirs(out_dir, exist_ok=True)
    jpath = os.path.join(out_dir, "verify_report.json")
    mpath = os.path.join(out_dir, "verify_report.md")

    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(verify_result, f, ensure_ascii=False, indent=2, default=str)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_verify_markdown(verify_result, model_path, ref_path))

    return jpath, mpath
