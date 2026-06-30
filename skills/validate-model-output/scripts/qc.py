from __future__ import annotations

import numpy as np

from dataset import Dataset
from rules import match_rule


def _result(check, status, evidence, variable=None) -> dict:
    return {"check": check, "variable": variable, "status": status, "evidence": evidence}


def check_variable(d: Dataset, name: str, rules: dict) -> list:
    results = []
    try:
        var = d.variable(name)
        arr = np.asarray(d.xr[name].values, dtype="float64")
    except Exception as e:  # 값 접근 실패도 크래시 대신 FAIL
        return [_result("value_access", "FAIL", f"변수 값 접근 실패: {e}", name)]

    finite = np.isfinite(arr)
    n = arr.size
    n_missing = int(n - finite.sum())
    missing_frac = n_missing / n if n else 1.0

    rule = match_rule(var, rules)
    default = rules.get("default", {})

    # 결측 검사
    max_missing = (rule or {}).get("max_missing_frac", default.get("max_missing_frac", 0.9))
    if missing_frac > max_missing:
        results.append(_result("missing", "FAIL",
            f"결측비율 {missing_frac:.2%} > 임계 {max_missing:.0%} ({n_missing}/{n})", name))
    else:
        results.append(_result("missing", "PASS",
            f"결측비율 {missing_frac:.2%} ≤ 임계 {max_missing:.0%}", name))

    vals = arr[finite]
    if rule is not None and "valid_min" in rule and "valid_max" in rule:
        lo, hi = rule["valid_min"], rule["valid_max"]
        out = (vals < lo) | (vals > hi)
        n_out = int(out.sum())
        if n_out > 0:
            sample = np.unique(np.round(vals[out], 2))[:5]
            results.append(_result("value_range", "FAIL",
                f"물리범위 [{lo}, {hi}] {rule.get('units_any', '')} 벗어난 값 {n_out}개 (예: {list(sample)})", name))
        else:
            results.append(_result("value_range", "PASS",
                f"전 값 물리범위 [{lo}, {hi}] 이내 (규칙 {rule['name']}, advisory)", name))
    else:
        results.append(_result("rule", "WARN",
            f"변수 '{name}'에 맞는 물리범위 규칙 없음 → 통계적 이상치만 점검(advisory)", name))

    # 이상치(N-시그마) — WARN
    sigma = (rule or {}).get("sigma", default.get("sigma", 6.0))
    if vals.size >= 8 and np.std(vals) > 0:
        z = np.abs(vals - np.mean(vals)) / np.std(vals)
        n_outlier = int((z > sigma).sum())
        if n_outlier > 0:
            results.append(_result("outlier", "WARN",
                f"{sigma}σ 초과 이상치 {n_outlier}개 (advisory)", name))
        else:
            results.append(_result("outlier", "PASS", f"{sigma}σ 초과 이상치 없음", name))
    return results
