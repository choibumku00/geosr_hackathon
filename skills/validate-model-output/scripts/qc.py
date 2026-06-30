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


def check_schema(d: Dataset) -> list:
    try:
        names = d.data_var_names()
    except Exception as e:
        return [_result("schema", "FAIL", f"스키마 읽기 실패: {e}")]
    if not names:
        return [_result("schema", "FAIL", "데이터 변수가 없음")]
    return [_result("schema", "PASS", f"데이터 변수 {len(names)}개: {names[:6]}")]


def check_grid(d: Dataset) -> list:
    try:
        ll = d.latlon()
    except Exception as e:
        return [_result("grid", "FAIL", f"좌표 읽기 실패: {e}")]
    if ll is None:
        return [_result("grid", "WARN", "lat/lon 좌표를 찾지 못함(비격자 자료일 수 있음)")]
    lat_name, lon_name, is_2d = ll
    results = []
    try:
        if is_2d:
            lat = np.asarray(d.xr[lat_name].values)
            lon = np.asarray(d.xr[lon_name].values)
            if lat.shape == lon.shape:
                results.append(_result("grid_shape", "PASS",
                    f"2D 좌표 형상 일치 {lat.shape}"))
            else:
                results.append(_result("grid_shape", "FAIL",
                    f"2D lat{lat.shape} ≠ lon{lon.shape} 형상 불일치"))
        else:
            lat = np.asarray(d.xr[lat_name].values, dtype="float64")
            diffs = np.diff(lat)
            mono = np.all(diffs > 0) or np.all(diffs < 0)
            if mono:
                results.append(_result("grid_monotonic", "PASS",
                    f"위도 단조({'증가' if diffs[0] > 0 else '감소'})"))
            else:
                bad = int(np.argmin(diffs > 0)) if np.any(diffs <= 0) else -1
                results.append(_result("grid_monotonic", "FAIL",
                    f"위도 비단조 @ index≈{bad} (값 {lat[max(bad,0)]:.3f})"))
    except Exception as e:
        results.append(_result("grid", "FAIL", f"격자 검사 실패: {e}"))
    return results


def check_time(d: Dataset) -> list:
    try:
        ti = d.time_info()
    except Exception as e:
        return [_result("time_axis", "FAIL", f"시간축 읽기 실패: {e}")]
    if ti is None:
        return []
    try:
        tname = ti["name"]
        tvals = np.asarray(d.xr[tname].values)
        if tvals.size <= 1:
            return [_result("time_axis", "PASS", f"시간 스텝 {tvals.size}개")]
        order = np.sort(tvals)
        n_dup = int(tvals.size - np.unique(tvals).size)
        mono = bool(np.all(tvals == order))
        if n_dup > 0:
            return [_result("time_axis", "FAIL", f"타임스탬프 중복 {n_dup}개")]
        if not mono:
            return [_result("time_axis", "FAIL", "타임스탬프 비단조(시간 역행)")]
        return [_result("time_axis", "PASS", f"시간 단조·중복없음 ({tvals.size} 스텝)")]
    except Exception as e:
        return [_result("time_axis", "FAIL", f"시간축 검사 실패: {e}")]
