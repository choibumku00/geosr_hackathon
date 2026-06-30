from __future__ import annotations

# SAMPLE — 실데이터 실시간 점검·도메인 맞춤 코드로 적응.
# verify 서브커맨드는 대표 케이스 SAMPLE 이다.
# 격자 조합·단위·시공간 정합은 실데이터 구조마다 다르니 반드시 점검하라.

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from discover import discover  # noqa: E402
from inspect_file import probe  # noqa: E402
from io_detect import open_dataset, UnknownFormatError  # noqa: E402
from qc import run_qc  # noqa: E402
from report import (  # noqa: E402
    write_report, render_markdown,
    render_verify_markdown, write_verify_report,
)


# ---------------------------------------------------------------------------
# discover / inspect / validate 커맨드 (기존 그대로 보존)
# ---------------------------------------------------------------------------

def _print_inventory(result: dict) -> None:
    print(f"{'파일':40s} {'포맷':9s} {'도메인':18s} {'역할추정':10s} {'좌표':5s} {'변수'}")
    print("-" * 100)
    for f in result["files"]:
        name = os.path.basename(f["path"])[:40]
        if f["openable"]:
            varnames = ",".join(v["name"] for v in f["variables"][:4])
            print(f"{name:40s} {f['format']:9s} {f.get('domain','?'):18s} "
                  f"{f.get('role_guess','?'):10s} {f.get('coord_kind','?'):5s} {varnames}")
        else:
            print(f"{name:40s} {f['format']:9s} {'(열기 실패: 미지포맷)':18s} "
                  f"{f.get('role_guess','?'):10s} {'-':5s} -")


def cmd_discover(args) -> int:
    result = discover(args.paths)
    _print_inventory(result)
    out = args.out or os.path.join(os.getcwd(), "inventory.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    print(f"\n[inventory.json 저장] {out}")
    return 0


def cmd_inspect(args) -> int:
    print(json.dumps(probe(args.file), ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args) -> int:
    out_dir = args.out or os.getcwd()
    try:
        d = open_dataset(args.file)
    except (UnknownFormatError, OSError) as e:
        qc = {"checks": [{"check": "open", "variable": None, "status": "FAIL",
                          "evidence": f"열기 실패: {e}"}],
              "summary": {"PASS": 0, "FAIL": 1, "WARN": 0}, "ok": False}
        print(render_markdown(qc, args.file))
        _, mpath = write_report(qc, args.file, out_dir)
        print(f"\n[리포트 저장] {mpath}")
        return 1
    qc = run_qc(d)
    print(render_markdown(qc, args.file))
    jpath, mpath = write_report(qc, args.file, out_dir)
    print(f"\n[리포트 저장] {mpath}")
    return 0 if qc["ok"] else 1


# ---------------------------------------------------------------------------
# verify 전용 헬퍼 — SAMPLE
# ---------------------------------------------------------------------------

# 방향 변수 힌트 (소문자 부분 문자열 매칭) — SAMPLE
_DIR_HINTS = frozenset({"dir", "wd", "wdir", "dp", "theta", "dirp", "dirmn",
                        "meandir", "pkdir", "mdir", "pdir"})
# 온도 변수 힌트 — SAMPLE
_TEMP_HINTS = frozenset({"t2m", "sst", "temp", "tmp", "tair", "tas", "tsfc",
                         "t_sfc", "t2", "temperature"})


def _is_direction_var(name: str) -> bool:
    """변수명 휴리스틱으로 방향 변수 여부 판단 (SAMPLE)."""
    n = name.lower()
    return any(h in n for h in _DIR_HINTS)


def _is_temp_var(name: str) -> bool:
    """변수명 휴리스틱으로 온도 변수 여부 판단 (SAMPLE)."""
    n = name.lower()
    return any(h in n for h in _TEMP_HINTS)


def _get_units(ds, vname: str) -> str:
    """Dataset 에서 변수의 units 속성을 추출한다. 없으면 '' 반환."""
    try:
        return str(ds.xr[vname].attrs.get("units", ""))
    except Exception:
        return ""


def _get_times_from_ds(ds) -> "np.ndarray | None":
    """xarray Dataset 에서 시간 배열을 추출한다 (SAMPLE).

    coords 또는 data_vars 에서 'time'/'valid_time'/'t' 이름을 탐색한다.
    없으면 None 반환.
    """
    import numpy as np
    _T_NAMES = ("time", "valid_time", "t", "datetime", "date")
    xds = ds.xr
    for tname in _T_NAMES:
        if tname in xds.coords:
            return xds.coords[tname].values
        if tname in xds.data_vars:
            return xds[tname].values
    return None


def _get_latlon_arrays(ds):
    """Dataset.latlon() 결과로부터 lat/lon 배열(ndarray)을 반환한다.

    Returns (lat_arr, lon_arr) or (None, None).
    lat/lon 이 1D 이면 meshgrid 하지 않고 1D 로 반환.
    """
    ll = ds.latlon()
    if ll is None:
        return None, None
    lat_name, lon_name, is_2d = ll
    try:
        import numpy as np
        lat = ds.xr[lat_name].values.astype(float)
        lon = ds.xr[lon_name].values.astype(float)
        return lat, lon
    except Exception:
        return None, None


def _get_ref_latlon(d_ref, args):
    """기준 파일의 위경도를 추출한다 (SAMPLE).

    1순위: --points 파일 + 기준 파일 내 정점 ID 컬럼으로 좌표 주입.
    2순위: 기준 파일 내 lat/lon 컬럼/좌표 직접 탐색.
    실패 시 None 반환 → 호출 측에서 graceful exit.
    """
    import numpy as np
    _LAT_NAMES = {"latitude", "lat"}
    _LON_NAMES = {"longitude", "lon"}
    _ID_NAMES  = {"station", "station_id", "stid", "id", "buoy_id",
                  "지점", "관측소", "정점"}

    # ── 1순위: --points 주입 ──────────────────────────────────────────────
    points_path = getattr(args, "points", None)
    if points_path:
        try:
            import preprocess
            mapping = preprocess.parse_points_list(points_path)
            if mapping:
                # 기준 파일에서 정점 ID 컬럼 탐색
                xds = d_ref.xr
                all_names = list(xds.coords) + list(xds.data_vars)
                id_col = next(
                    (str(n) for n in all_names if str(n).lower() in _ID_NAMES),
                    None,
                )
                if id_col:
                    station_ids = [str(v) for v in xds[id_col].values.ravel()]
                    lats, lons = preprocess.inject_point_coords(station_ids, mapping)
                    valid = ~(np.isnan(lats) | np.isnan(lons))
                    if valid.any():
                        return lats[valid], lons[valid]
                else:
                    # ID 컬럼 없음 — mapping 전체 좌표 사용 (SAMPLE)
                    all_lats = np.array([v[0] for v in mapping.values()], dtype=float)
                    all_lons = np.array([v[1] for v in mapping.values()], dtype=float)
                    valid = ~(np.isnan(all_lats) | np.isnan(all_lons))
                    if valid.any():
                        return all_lats[valid], all_lons[valid]
        except Exception as e:
            print(f"[verify] --points 처리 중 오류(무시): {e}", file=sys.stderr)

    # ── 2순위: 기준 파일 내 lat/lon 직접 탐색 ─────────────────────────
    xds = d_ref.xr
    all_names = list(xds.coords) + list(xds.data_vars)
    ref_lat_name = next((str(n) for n in all_names if str(n).lower() in _LAT_NAMES), None)
    ref_lon_name = next((str(n) for n in all_names if str(n).lower() in _LON_NAMES), None)
    if ref_lat_name and ref_lon_name:
        try:
            pt_lat = xds[ref_lat_name].values.astype(float).ravel()
            pt_lon = xds[ref_lon_name].values.astype(float).ravel()
            valid = ~(np.isnan(pt_lat) | np.isnan(pt_lon))
            if valid.any():
                return pt_lat[valid], pt_lon[valid]
        except Exception as e:
            print(f"[verify] 기준 lat/lon 추출 실패(무시): {e}", file=sys.stderr)

    return None, None


def _safe_nan(val):
    """float 또는 nan 을 안전하게 직렬화 가능한 형태로 반환."""
    if val is None:
        return None
    try:
        v = float(val)
        return None if (math.isnan(v) or math.isinf(v)) else v
    except (TypeError, ValueError):
        return None


def _compute_accuracy_row(vname: str, f_arr, o_arr) -> dict:
    """한 변수의 정확도 메트릭을 계산한다 (SAMPLE: bias/RMSE/SI/pearson_r)."""
    import numpy as np
    import metrics_basic

    f = np.asarray(f_arr, dtype=float).ravel()
    o = np.asarray(o_arr, dtype=float).ravel()
    valid = np.isfinite(f) & np.isfinite(o)
    n = int(valid.sum())

    if n == 0:
        return {"variable": vname, "n": 0,
                "bias": None, "rmse": None, "si": None, "pearson_r": None}

    return {
        "variable": vname,
        "n": n,
        "bias":      _safe_nan(metrics_basic.bias(f[valid], o[valid])),
        "rmse":      _safe_nan(metrics_basic.rmse(f[valid], o[valid])),
        "si":        _safe_nan(metrics_basic.si(f[valid], o[valid])),
        "pearson_r": _safe_nan(metrics_basic.pearson_r(f[valid], o[valid])),
    }


def _compute_direction_row(vname: str, f_arr, o_arr) -> dict:
    """한 방향 변수의 원형 메트릭을 계산한다 (SAMPLE)."""
    import numpy as np
    import metrics_circular

    f = np.asarray(f_arr, dtype=float).ravel()
    o = np.asarray(o_arr, dtype=float).ravel()
    valid = np.isfinite(f) & np.isfinite(o)
    n = int(valid.sum())

    if n == 0:
        return {"variable": vname, "n": 0,
                "circular_cme": None, "circular_rmse": None, "circular_corr": None}

    fv, ov = f[valid], o[valid]
    return {
        "variable":     vname,
        "n":            n,
        "circular_cme":  _safe_nan(metrics_circular.circular_mean_error(fv, ov)),
        "circular_rmse": _safe_nan(metrics_circular.circular_rmse(fv, ov)),
        "circular_corr": _safe_nan(metrics_circular.circular_corr(fv, ov)),
    }


def _try_unit_normalize(f_arr, o_arr, vname: str, d_model, d_ref):
    """온도 변수일 때 단위 불일치를 K 기준으로 정규화한다 (SAMPLE).

    양쪽 단위가 같거나 온도 변수가 아니면 그대로 반환.
    SAMPLE — 실데이터에서 단위 속성 형식이 다를 수 있으니 반드시 점검하라.
    """
    if not _is_temp_var(vname):
        return f_arr, o_arr
    try:
        import preprocess
        u_model = _get_units(d_model, vname)
        u_ref   = _get_units(d_ref,   vname)
        if u_model and u_ref and u_model.strip().lower() != u_ref.strip().lower():
            f_arr = preprocess.to_kelvin(f_arr, u_model)
            o_arr = preprocess.to_kelvin(o_arr, u_ref)
    except Exception as e:
        print(f"[verify] 단위 정규화 실패(무시, {vname}): {e}", file=sys.stderr)
    return f_arr, o_arr


def _parse_regions(regions_str: str) -> list[str]:
    """'동해,남해' 형식의 문자열을 해역 이름 목록으로 파싱한다."""
    if not regions_str:
        return []
    return [r.strip() for r in regions_str.split(",") if r.strip()]


def _compute_region_rows(vname: str, f_arr, o_arr, lat, lon, bbox, is_dir: bool) -> dict | None:
    """bbox 마스크를 적용해 해역 내 행만 계산한다 (SAMPLE).

    f_arr, o_arr : 1D, 매칭된 점 배열
    lat, lon     : 1D, f_arr 와 같은 길이 (좌표)
    bbox         : [lon_min, lon_max, lat_min, lat_max]
    is_dir       : True 이면 방향 메트릭, False 이면 정확도 메트릭
    """
    import numpy as np
    try:
        import regions as reg_mod
        mask = reg_mod.crop_grid_mask(lon, lat, bbox)
        if mask.sum() == 0:
            return None
        f_reg = f_arr[mask]
        o_reg = o_arr[mask]
        if is_dir:
            return _compute_direction_row(vname, f_reg, o_reg)
        else:
            return _compute_accuracy_row(vname, f_reg, o_reg)
    except Exception as e:
        print(f"[verify] 해역 마스크 계산 실패(무시, {vname}): {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# verify — 격자 대 격자 (SAMPLE)
# ---------------------------------------------------------------------------

def _verify_grid_to_grid(
    d_model, d_ref, model_path: str, ref_path: str, out_dir: str, args
) -> int:
    """격자 대 격자 검증 SAMPLE (다축).

    공통 변수 단위 정규화(온도 °C↔K) → bias/RMSE/SI/pearson_r +
    방향 변수이면 circular_* → scatter_si·taylor·diff_map·QQ·timeseries +
    --regions 로 해역별 표.

    SAMPLE 범위밖:
    * 크기가 다른 격자 간 보간 → 실데이터 맞춤 코드로 적응하라.
    * 시간 축 매칭 → 동일 시간 스텝 가정; 다를 경우 실데이터 점검 필수.
    """
    try:
        import numpy as np
        import metrics_basic       # noqa — ensure importable
        import metrics_circular    # noqa
        import plots
    except ImportError as e:
        print(f"[ERROR] 모듈 불러오기 실패: {e}", file=sys.stderr)
        return 1

    model_vars = set(d_model.data_var_names())
    ref_vars   = set(d_ref.data_var_names())
    common     = sorted(model_vars & ref_vars)

    if not common:
        print(
            f"[verify] SAMPLE — 공통 변수명 없음. "
            f"model={sorted(model_vars)}, ref={sorted(ref_vars)}. "
            "aliases.py 로 이름 표준화 후 실데이터 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    print(f"[verify] 격자대격자 — 공통 변수: {common}")

    # ── 1. 좌표 추출 (diff_map, 해역 마스크용) ──────────────────────────
    lat_m, lon_m = _get_latlon_arrays(d_model)

    # ── 2. 변수별 메트릭 계산 ─────────────────────────────────────────
    accuracy_rows:  list[dict] = []
    direction_rows: list[dict] = []

    # 첫 번째 정확도 변수용 배열(그림 생성에 사용)
    first_f: "np.ndarray | None" = None
    first_o: "np.ndarray | None" = None
    first_vname: str | None = None
    first_lat:   "np.ndarray | None" = None
    first_lon:   "np.ndarray | None" = None

    # 첫 번째 방향 변수 배열(rose 생성)
    first_dir_f: "np.ndarray | None" = None
    first_dir_o: "np.ndarray | None" = None
    first_dir_vname: str | None = None

    for vname in common:
        try:
            f_arr = d_model.xr[vname].values.astype(float).ravel()
            o_arr = d_ref.xr[vname].values.astype(float).ravel()
        except Exception as e:
            print(f"[verify] {vname} 추출 실패(무시): {e}", file=sys.stderr)
            continue

        # 크기 불일치 — 동일 격자 가정 깨짐: graceful skip
        if f_arr.shape != o_arr.shape:
            print(
                f"[verify] {vname} 크기 불일치({f_arr.shape} vs {o_arr.shape}) — "
                "같은 격자 구조가 아님. 보간은 SAMPLE 범위 밖. 건너뜀.",
                file=sys.stderr,
            )
            continue

        # 단위 정규화 (온도)
        f_arr, o_arr = _try_unit_normalize(f_arr, o_arr, vname, d_model, d_ref)

        if _is_direction_var(vname):
            row = _compute_direction_row(vname, f_arr, o_arr)
            direction_rows.append(row)
            print(f"  [dir] {vname}: CME={row.get('circular_cme')}  "
                  f"CRMSE={row.get('circular_rmse')}  Corr={row.get('circular_corr')}")
            if first_dir_f is None:
                first_dir_f, first_dir_o, first_dir_vname = f_arr, o_arr, vname
        else:
            row = _compute_accuracy_row(vname, f_arr, o_arr)
            accuracy_rows.append(row)
            print(f"  {vname}: bias={row.get('bias')}  RMSE={row.get('rmse')}  "
                  f"SI={row.get('si')}  r={row.get('pearson_r')}")
            if first_f is None:
                first_f, first_o, first_vname = f_arr, o_arr, vname
                # 공간 좌표 캐시 (diff_map 용)
                if lat_m is not None:
                    try:
                        _sz = d_model.xr[vname].values.shape
                        if lat_m.ndim == 2 and len(_sz) >= 2:
                            # 시간 축 있으면 시간 평균 bias 맵
                            _fm = d_model.xr[vname].values.astype(float)
                            _rm = d_ref.xr[vname].values.astype(float)
                            if _fm.ndim == 3:
                                _fm = np.nanmean(_fm, axis=0)
                                _rm = np.nanmean(_rm, axis=0)
                            first_lat = lat_m
                            first_lon = lon_m
                            first_f_2d = _fm
                            first_o_2d = _rm
                        else:
                            first_lat = lat_m
                            first_lon = lon_m
                            first_f_2d = None
                            first_o_2d = None
                    except Exception:
                        first_lat = lat_m
                        first_lon = lon_m
                        first_f_2d = None
                        first_o_2d = None

    if not accuracy_rows and not direction_rows:
        print("[verify] 계산된 메트릭 없음 — 공통 변수 추출/크기 불일치.", file=sys.stderr)
        return 1

    # ── 3. 그림 생성 ────────────────────────────────────────────────────
    plot_paths: dict[str, str | None] = {
        "scatter": None, "taylor": None, "diff_map": None,
        "qq": None, "timeseries": None,
        "wave_rose_model": None, "wave_rose_ref": None,
    }

    if first_f is not None and first_vname is not None:
        # scatter_si
        try:
            png = os.path.join(out_dir, f"scatter_{first_vname}.png")
            plot_paths["scatter"] = plots.scatter_si(first_o, first_f, png)
            print(f"  [scatter] {plot_paths['scatter']}")
        except Exception as e:
            print(f"[verify] scatter 생성 실패(무시): {e}", file=sys.stderr)

        # taylor_diagram
        try:
            png = os.path.join(out_dir, f"taylor_{first_vname}.png")
            plot_paths["taylor"] = plots.taylor_diagram(first_o, first_f, png)
            print(f"  [taylor] {plot_paths['taylor']}")
        except Exception as e:
            print(f"[verify] taylor 생성 실패(무시): {e}", file=sys.stderr)

        # qq_plot
        try:
            png = os.path.join(out_dir, f"qq_{first_vname}.png")
            plot_paths["qq"] = plots.qq_plot(first_o, first_f, png)
            print(f"  [qq] {plot_paths['qq']}")
        except Exception as e:
            print(f"[verify] QQ 생성 실패(무시): {e}", file=sys.stderr)

        # diff_map (2D 격자만)
        try:
            if (first_lat is not None and first_lat.ndim == 2
                    and "first_f_2d" in dir() and first_f_2d is not None):
                diff_2d = first_f_2d - first_o_2d
                png = os.path.join(out_dir, f"diff_map_{first_vname}.png")
                plot_paths["diff_map"] = plots.diff_map(
                    first_lat, first_lon, diff_2d, png,
                    units=_get_units(d_model, first_vname),
                )
                print(f"  [diff_map] {plot_paths['diff_map']}")
        except Exception as e:
            print(f"[verify] diff_map 생성 실패(무시): {e}", file=sys.stderr)

    # wave_rose (방향 변수)
    if first_dir_f is not None:
        try:
            import numpy as np
            mag_dummy = np.ones_like(first_dir_f)   # SAMPLE: 크기 없이 방향만
            png = os.path.join(out_dir, f"rose_model_{first_dir_vname}.png")
            plot_paths["wave_rose_model"] = plots.wave_rose(first_dir_f, mag_dummy, png)
            png = os.path.join(out_dir, f"rose_ref_{first_dir_vname}.png")
            plot_paths["wave_rose_ref"] = plots.wave_rose(first_dir_o, mag_dummy, png)
            print(f"  [rose] model={plot_paths['wave_rose_model']}")
        except Exception as e:
            print(f"[verify] wave_rose 생성 실패(무시): {e}", file=sys.stderr)

    # ── 4. 해역별 분석 (--regions) ──────────────────────────────────────
    region_results: list[dict] = []
    region_names = _parse_regions(getattr(args, "regions", "") or "")
    if region_names:
        try:
            import regions as reg_mod
            import numpy as np
        except ImportError as e:
            print(f"[verify] regions 모듈 불러오기 실패(무시): {e}", file=sys.stderr)
            region_names = []

    for rname in region_names:
        try:
            import regions as reg_mod
            bbox = reg_mod.region_bbox(rname)
            if bbox is None:
                print(f"[verify] 해역 '{rname}' 인식 불가(무시). "
                      "NAMED_REGIONS 키를 확인하라.", file=sys.stderr)
                continue
            reg_acc_rows:  list[dict] = []
            reg_dir_rows:  list[dict] = []
            # 정확도 변수들
            for vname in common:
                if _is_direction_var(vname):
                    continue
                try:
                    f_v = d_model.xr[vname].values.astype(float).ravel()
                    o_v = d_ref.xr[vname].values.astype(float).ravel()
                    if f_v.shape != o_v.shape:
                        continue
                    if lat_m is not None:
                        lat_r = lat_m.ravel()
                        lon_r = lon_m.ravel()
                        if len(lat_r) != len(f_v):
                            lat_r = lon_r = None
                    else:
                        lat_r = lon_r = None
                    if lat_r is not None and lon_r is not None:
                        row = _compute_region_rows(
                            vname, f_v, o_v, lat_r, lon_r, bbox, is_dir=False
                        )
                        if row:
                            reg_acc_rows.append(row)
                except Exception:
                    pass
            # 방향 변수들
            for vname in common:
                if not _is_direction_var(vname):
                    continue
                try:
                    f_v = d_model.xr[vname].values.astype(float).ravel()
                    o_v = d_ref.xr[vname].values.astype(float).ravel()
                    if f_v.shape != o_v.shape:
                        continue
                    if lat_m is not None:
                        lat_r = lat_m.ravel()
                        lon_r = lon_m.ravel()
                        if len(lat_r) != len(f_v):
                            lat_r = lon_r = None
                    else:
                        lat_r = lon_r = None
                    if lat_r is not None and lon_r is not None:
                        row = _compute_region_rows(
                            vname, f_v, o_v, lat_r, lon_r, bbox, is_dir=True
                        )
                        if row:
                            reg_dir_rows.append(row)
                except Exception:
                    pass
            region_results.append({
                "name":          rname,
                "accuracy_rows": reg_acc_rows,
                "direction_rows": reg_dir_rows,
            })
        except Exception as e:
            print(f"[verify] 해역 '{rname}' 분석 실패(무시): {e}", file=sys.stderr)

    # ── 5. verify_result 구성 및 저장 ───────────────────────────────────
    verify_result = {
        "mode":           "grid_to_grid",
        "ok":             True,
        "model":          model_path,
        "ref":            ref_path,
        "tz_assumed":     False,
        "accuracy_rows":  accuracy_rows,
        "direction_rows": direction_rows,
        "plots":          plot_paths,
        "regions":        region_results,
        "info":           f"공통 변수 {len(common)}개: {common}",
    }
    print(render_verify_markdown(verify_result, model_path, ref_path))
    _, mpath = write_verify_report(verify_result, model_path, ref_path, out_dir)
    print(f"\n[verify 리포트 저장] {mpath}")
    return 0


# ---------------------------------------------------------------------------
# verify — mesh + 점관측 (SAMPLE)
# ---------------------------------------------------------------------------

def _verify_mesh_point(
    d_model, d_ref, model_path: str, ref_path: str, out_dir: str, args
) -> int:
    """mesh(모델) + 점관측(기준) 매칭 검증 SAMPLE (다축).

    match_points_to_mesh 최근접 → tz_to_utc 시간 정합 → common_time_index
    교집합 → Hs/방향 bias/RMSE/SI/circular_* + scatter/QQ/timeseries/wave_rose.

    좌표 출처 순위:
      1) --points 파일 + 기준 파일 내 정점 ID 컬럼
      2) 기준 파일 내 lat/lon 컬럼/좌표
      없으면 "좌표 출처 필요" 메시지 후 graceful exit 1.

    SAMPLE 범위밖: 보간·CRS 변환·이상치 제거 — 실데이터 맞춤 코드로 적응하라.
    """
    try:
        import numpy as np
        import preprocess
        import metrics_basic    # noqa
        import metrics_circular # noqa
        import plots
    except ImportError as e:
        print(f"[ERROR] 모듈 불러오기 실패: {e}", file=sys.stderr)
        return 1

    _LAT_NAMES = {"latitude", "lat"}
    _LON_NAMES = {"longitude", "lon"}
    _AUX_VARS  = _LAT_NAMES | _LON_NAMES | {
        "tri", "mapsta", "MAPSTA", "element", "node", "time", "index",
    }

    # ── 1. mesh lat/lon 추출 ─────────────────────────────────────────────
    mesh_lat_name = next(
        (n for n in d_model.xr.data_vars if str(n).lower() in _LAT_NAMES), None
    )
    mesh_lon_name = next(
        (n for n in d_model.xr.data_vars if str(n).lower() in _LON_NAMES), None
    )
    if mesh_lat_name is None or mesh_lon_name is None:
        print(
            "[verify] SAMPLE — mesh lat/lon data variable 을 찾지 못했다. "
            "실데이터에서 변수명을 확인하고 도메인 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    mesh_lat = d_model.xr[mesh_lat_name].values.astype(float).ravel()
    mesh_lon = d_model.xr[mesh_lon_name].values.astype(float).ravel()

    # ── 2. 기준 위경도 추출 ────────────────────────────────────────────
    pt_lat, pt_lon = _get_ref_latlon(d_ref, args)
    if pt_lat is None or len(pt_lat) == 0:
        print(
            "[verify] SAMPLE — 기준 파일에서 위경도를 얻지 못했다. "
            "좌표 출처 필요: 기준 CSV 에 lat/lon 컬럼을 추가하거나 "
            "--points 관측점 목록 파일을 지정하라 (parse_points_list 형식).",
            file=sys.stderr,
        )
        return 1

    # ── 3. 최근접 노드 매칭 ─────────────────────────────────────────────
    try:
        indices, dists_km = preprocess.match_points_to_mesh(
            mesh_lon, mesh_lat, pt_lon, pt_lat, max_km=50.0
        )
    except Exception as e:
        print(f"[verify] match_points_to_mesh 실패: {e}", file=sys.stderr)
        return 1

    valid_mask = indices >= 0
    n_valid    = int(valid_mask.sum())
    print(f"[verify] mesh+점관측 — {len(indices)}점 중 {n_valid}점 매칭 (max_km=50)")
    if n_valid == 0:
        print(
            "[verify] 매칭된 관측점 없음 — max_km 임계를 늘리거나 좌표를 점검하라.",
            file=sys.stderr,
        )
        return 1

    matched_indices = indices[valid_mask]    # 유효 mesh 노드 인덱스
    # valid_mask 는 pt 배열 기준 — 유효 pt 인덱스
    valid_pt_idx = np.where(valid_mask)[0]

    # ── 4. 시간 정합 — tz_to_utc + common_time_index ────────────────────
    model_tz = getattr(args, "model_tz", None)
    ref_tz   = getattr(args, "ref_tz", None)

    tz_assumed_flag = False
    model_times = _get_times_from_ds(d_model)
    ref_times   = _get_times_from_ds(d_ref)

    time_sync_ok = False
    idx_m: "np.ndarray | None" = None
    idx_r: "np.ndarray | None" = None

    if model_times is not None and ref_times is not None:
        try:
            mt_utc, m_assumed = preprocess.tz_to_utc(model_times, model_tz)
            rt_utc, r_assumed = preprocess.tz_to_utc(ref_times,   ref_tz)
            tz_assumed_flag   = m_assumed or r_assumed
            idx_m, idx_r      = preprocess.common_time_index(mt_utc, rt_utc)
            if len(idx_m) == 0:
                print("[verify] 교집합 시간 스텝 0개 — TZ 확인 필요(KST vs UTC).",
                      file=sys.stderr)
                return 1
            print(f"[verify] 시간 교집합 {len(idx_m)}/{len(model_times)} 스텝"
                  + (" [TZ=assumed UTC]" if tz_assumed_flag else ""))
            time_sync_ok = True
        except Exception as e:
            print(f"[verify] 시간 정합 실패(무시, 전체 시간 사용): {e}", file=sys.stderr)
    else:
        if model_times is None:
            print("[verify] 모델 시간 축 없음 — 시간 평균으로 계산 (SAMPLE)", file=sys.stderr)
        if ref_times is None:
            print("[verify] 기준 시간 축 없음 — 전체 배열 사용 (SAMPLE)", file=sys.stderr)

    # ── 5. 공통 변수 탐색 ────────────────────────────────────────────────
    model_vars = {n for n in d_model.data_var_names() if n.lower() not in
                  {a.lower() for a in _AUX_VARS}}
    ref_all    = list(d_ref.xr.coords) + list(d_ref.xr.data_vars)
    _ref_excl  = {str(n).lower() for n in ref_all if str(n).lower() in _LAT_NAMES | _LON_NAMES}
    ref_vars   = {n for n in d_ref.data_var_names()
                  if n.lower() not in {a.lower() for a in _AUX_VARS}
                  and n.lower() not in _ref_excl}
    common     = sorted(model_vars & ref_vars)

    if not common:
        print(
            f"[verify] SAMPLE — 공통 변수명 없음(mesh={sorted(model_vars)}, "
            f"기준={sorted(ref_vars)}). "
            "aliases.py 로 이름 표준화 후 실데이터 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    print(f"[verify] 공통 변수: {common}")

    # ── 6. 변수별 메트릭 ─────────────────────────────────────────────────
    accuracy_rows:  list[dict] = []
    direction_rows: list[dict] = []

    # 첫 번째 정확도 변수 캐시(그림용)
    first_f_ts: "np.ndarray | None" = None
    first_o_ts: "np.ndarray | None" = None
    first_t_ts: "np.ndarray | None" = None
    first_vname_ts: str | None = None

    # 첫 번째 방향 변수 캐시(rose용)
    first_dir_f: "np.ndarray | None" = None
    first_dir_o: "np.ndarray | None" = None
    first_dir_vname: str | None = None

    for vname in common:
        try:
            model_vals = d_model.xr[vname].values   # (time, node) or (node,)
            ref_vals   = d_ref.xr[vname].values     # (time,) or (time, npts) or (npts,)
        except Exception as e:
            print(f"[verify] {vname} 추출 실패(무시): {e}", file=sys.stderr)
            continue

        # --- 시간 선택 ---
        if time_sync_ok and idx_m is not None and idx_r is not None:
            # 모델: (time, node) → select time → (T_common, N_node)
            if model_vals.ndim == 2:
                model_vals = model_vals[idx_m, :]
            elif model_vals.ndim == 1:
                pass  # node-only: 시간 없음
            # 기준: (time, ...) → select time
            if ref_vals.ndim >= 1 and ref_vals.shape[0] >= len(idx_r):
                ref_vals = ref_vals[idx_r] if ref_vals.ndim == 1 else ref_vals[idx_r, ...]
        else:
            # 시간 정합 없음 — 시간 평균 (SAMPLE)
            if model_vals.ndim == 2:
                model_vals = np.nanmean(model_vals, axis=0)  # (N_node,)
            if ref_vals.ndim == 2:
                ref_vals = np.nanmean(ref_vals, axis=0)

        # --- 매칭 노드 추출 ---
        try:
            if model_vals.ndim == 2:
                # (T, N_node) → (T, n_valid)
                f_matched = model_vals[:, matched_indices]  # (T, n_valid)
            else:
                # (N_node,)
                f_matched = model_vals[matched_indices]     # (n_valid,)

            if ref_vals.ndim == 2:
                # (T, n_pts) → (T, n_valid)
                o_matched = ref_vals[:, valid_pt_idx]       # (T, n_valid)
            else:
                # (n_pts,) or (T,)
                if ref_vals.shape[0] == len(pt_lat):
                    o_matched = ref_vals[valid_pt_idx]      # (n_valid,)
                else:
                    # 1D 시계열 단일 관측점 케이스 (SAMPLE)
                    o_matched = np.tile(ref_vals, (n_valid, 1)).T  # (T, n_valid)
        except Exception as e:
            print(f"[verify] {vname} 매칭 추출 실패(무시): {e}", file=sys.stderr)
            continue

        f_flat = np.asarray(f_matched, dtype=float).ravel()
        o_flat = np.asarray(o_matched, dtype=float).ravel()

        if _is_direction_var(vname):
            row = _compute_direction_row(vname, f_flat, o_flat)
            direction_rows.append(row)
            print(f"  [dir] {vname}: CME={row.get('circular_cme')}  "
                  f"CRMSE={row.get('circular_rmse')}  Corr={row.get('circular_corr')}")
            if first_dir_f is None:
                first_dir_f, first_dir_o, first_dir_vname = f_flat, o_flat, vname
        else:
            row = _compute_accuracy_row(vname, f_flat, o_flat)
            accuracy_rows.append(row)
            print(f"  {vname}: bias={row.get('bias')}  RMSE={row.get('rmse')}  "
                  f"SI={row.get('si')}  r={row.get('pearson_r')}")
            if first_f_ts is None:
                first_vname_ts = vname
                # 시계열용 — 첫 번째 유효 관측점 시계열 (SAMPLE)
                if f_matched.ndim == 2 and idx_m is not None:
                    first_f_ts = f_matched[:, 0].ravel()
                    first_o_ts = o_matched[:, 0].ravel() if o_matched.ndim == 2 else o_matched.ravel()
                    if model_times is not None and idx_m is not None:
                        first_t_ts = model_times[idx_m]
                else:
                    first_f_ts = f_flat
                    first_o_ts = o_flat
                    first_t_ts = None

    if not accuracy_rows and not direction_rows:
        print("[verify] 계산된 메트릭 없음 — 공통 변수 추출 실패.", file=sys.stderr)
        return 1

    # ── 7. 그림 생성 ─────────────────────────────────────────────────────
    plot_paths: dict[str, str | None] = {
        "scatter": None, "taylor": None, "diff_map": None,
        "qq": None, "timeseries": None,
        "wave_rose_model": None, "wave_rose_ref": None,
    }

    if first_f_ts is not None:
        # scatter_si
        try:
            png = os.path.join(out_dir, f"scatter_{first_vname_ts}.png")
            plot_paths["scatter"] = plots.scatter_si(first_o_ts, first_f_ts, png)
            print(f"  [scatter] {plot_paths['scatter']}")
        except Exception as e:
            print(f"[verify] scatter 생성 실패(무시): {e}", file=sys.stderr)

        # QQ
        try:
            png = os.path.join(out_dir, f"qq_{first_vname_ts}.png")
            plot_paths["qq"] = plots.qq_plot(first_o_ts, first_f_ts, png)
            print(f"  [qq] {plot_paths['qq']}")
        except Exception as e:
            print(f"[verify] QQ 생성 실패(무시): {e}", file=sys.stderr)

        # timeseries
        if first_t_ts is not None:
            try:
                png = os.path.join(out_dir, f"timeseries_{first_vname_ts}.png")
                plot_paths["timeseries"] = plots.timeseries_overlay(
                    first_t_ts, first_o_ts, first_f_ts, png
                )
                print(f"  [timeseries] {plot_paths['timeseries']}")
            except Exception as e:
                print(f"[verify] timeseries 생성 실패(무시): {e}", file=sys.stderr)

        # taylor
        try:
            png = os.path.join(out_dir, f"taylor_{first_vname_ts}.png")
            plot_paths["taylor"] = plots.taylor_diagram(first_o_ts, first_f_ts, png)
            print(f"  [taylor] {plot_paths['taylor']}")
        except Exception as e:
            print(f"[verify] taylor 생성 실패(무시): {e}", file=sys.stderr)

        # diff_map (scatter 스타일, 매칭점 좌표)
        try:
            f_matched_mean = np.nanmean(
                np.asarray(first_f_ts, dtype=float).reshape(-1, n_valid), axis=0
            ) if len(first_f_ts) > n_valid else np.asarray(first_f_ts, dtype=float)
            o_matched_mean = np.nanmean(
                np.asarray(first_o_ts, dtype=float).reshape(-1, n_valid), axis=0
            ) if len(first_o_ts) > n_valid else np.asarray(first_o_ts, dtype=float)
            diff_pts = f_matched_mean - o_matched_mean
            lat_pts  = mesh_lat[matched_indices]
            lon_pts  = mesh_lon[matched_indices]
            png = os.path.join(out_dir, f"diff_map_{first_vname_ts}.png")
            plot_paths["diff_map"] = plots.diff_map(
                lat_pts, lon_pts, diff_pts, png,
                units=_get_units(d_model, first_vname_ts),
            )
            print(f"  [diff_map] {plot_paths['diff_map']}")
        except Exception as e:
            print(f"[verify] diff_map(점) 생성 실패(무시): {e}", file=sys.stderr)

    # wave_rose (방향 변수)
    if first_dir_f is not None:
        try:
            mag_ones = np.ones_like(first_dir_f)
            png = os.path.join(out_dir, f"rose_model_{first_dir_vname}.png")
            plot_paths["wave_rose_model"] = plots.wave_rose(first_dir_f, mag_ones, png)
            png = os.path.join(out_dir, f"rose_ref_{first_dir_vname}.png")
            plot_paths["wave_rose_ref"]   = plots.wave_rose(first_dir_o, mag_ones, png)
            print(f"  [rose] model={plot_paths['wave_rose_model']}")
        except Exception as e:
            print(f"[verify] wave_rose 생성 실패(무시): {e}", file=sys.stderr)

    # ── 8. 해역별 분석 (--regions, SAMPLE: 매칭 노드 좌표 기준) ─────────
    region_results: list[dict] = []
    region_names = _parse_regions(getattr(args, "regions", "") or "")
    for rname in region_names:
        try:
            import regions as reg_mod
            bbox = reg_mod.region_bbox(rname)
            if bbox is None:
                print(f"[verify] 해역 '{rname}' 인식 불가(무시).", file=sys.stderr)
                continue
            lat_pts_v = mesh_lat[matched_indices]
            lon_pts_v = mesh_lon[matched_indices]
            reg_mask  = reg_mod.crop_mesh_mask(lon_pts_v, lat_pts_v, bbox)
            reg_acc_rows: list[dict] = []
            reg_dir_rows: list[dict] = []
            for vname in common:
                try:
                    model_vals = d_model.xr[vname].values
                    ref_vals   = d_ref.xr[vname].values
                    if model_vals.ndim == 2:
                        model_vals = np.nanmean(model_vals, axis=0)
                    if ref_vals.ndim == 2:
                        ref_vals = np.nanmean(ref_vals, axis=0)
                    f_v = model_vals[matched_indices][reg_mask]
                    if ref_vals.shape[0] == len(pt_lat):
                        o_v = ref_vals[valid_pt_idx][reg_mask]
                    else:
                        o_v = f_v * np.nan  # SAMPLE: 매칭 불가
                    if _is_direction_var(vname):
                        row = _compute_direction_row(vname, f_v, o_v)
                        if row["n"] > 0:
                            reg_dir_rows.append(row)
                    else:
                        row = _compute_accuracy_row(vname, f_v, o_v)
                        if row["n"] > 0:
                            reg_acc_rows.append(row)
                except Exception:
                    pass
            region_results.append({
                "name":          rname,
                "accuracy_rows": reg_acc_rows,
                "direction_rows": reg_dir_rows,
            })
        except Exception as e:
            print(f"[verify] 해역 '{rname}' 분석 실패(무시): {e}", file=sys.stderr)

    # ── 9. verify_result 구성 및 저장 ─────────────────────────────────
    time_info_str = (
        f"시간 교집합 {len(idx_m)}/{len(model_times) if model_times is not None else '?'} 스텝"
        if (time_sync_ok and idx_m is not None) else "시간 정합 없음(SAMPLE)"
    )
    verify_result = {
        "mode":           "mesh_point",
        "ok":             True,
        "model":          model_path,
        "ref":            ref_path,
        "tz_assumed":     tz_assumed_flag,
        "accuracy_rows":  accuracy_rows,
        "direction_rows": direction_rows,
        "plots":          plot_paths,
        "regions":        region_results,
        "info":           (
            f"매칭 {n_valid}/{len(indices)}점 | {time_info_str} | "
            f"공통 변수 {len(common)}개: {common}"
        ),
    }
    print(render_verify_markdown(verify_result, model_path, ref_path))
    _, mpath = write_verify_report(verify_result, model_path, ref_path, out_dir)
    print(f"\n[verify 리포트 저장] {mpath}")
    return 0


# ---------------------------------------------------------------------------
# cmd_verify — SAMPLE
# SAMPLE — 실데이터에선 격자구조·단위·시공간 정합을 실시간 점검하고
#          도메인 맞춤 코드로 적응하라. 이 구현은 대표 케이스 SAMPLE이다.
# ---------------------------------------------------------------------------

def cmd_verify(args) -> int:
    """verify 서브커맨드.

    격자대격자: bias/RMSE/SI/r + taylor/diff_map/scatter/QQ + 방향이면 circular/rose.
    mesh+점관측: match_points_to_mesh → tz_to_utc → common_time_index
                → 정확도/분포/시간/방향 다축 + --regions 해역별 반복표.
    지원 안 되는 조합: 명확 메시지 + exit 1 (크래시 없음).
    """
    out_dir = args.out or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    try:
        d_model = open_dataset(args.model)
    except (UnknownFormatError, OSError) as e:
        print(f"[ERROR] 모델 파일 열기 실패: {e}", file=sys.stderr)
        return 1

    try:
        d_ref = open_dataset(args.ref)
    except (UnknownFormatError, OSError) as e:
        print(f"[ERROR] 기준 파일 열기 실패: {e}", file=sys.stderr)
        return 1

    model_ck = d_model.coord_kind()
    ref_ck   = d_ref.coord_kind()
    print(f"[verify] model={os.path.basename(args.model)} coord_kind={model_ck}, "
          f"ref={os.path.basename(args.ref)} coord_kind={ref_ck}")

    if model_ck in ("1d", "2d") and ref_ck in ("1d", "2d"):
        return _verify_grid_to_grid(d_model, d_ref, args.model, args.ref, out_dir, args)

    if model_ck == "mesh":
        return _verify_mesh_point(d_model, d_ref, args.model, args.ref, out_dir, args)

    print(
        f"[verify] SAMPLE — 지원하지 않는 격자 조합: model={model_ck}, ref={ref_ck}. "
        "격자대격자(1d/2d↔1d/2d) 또는 mesh+참조 파일 조합만 지원. "
        "실데이터 맞춤 코드로 적응하라.",
        file=sys.stderr,
    )
    return 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(prog="validate-model-output")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover", help="폴더/파일 인벤토리")
    d.add_argument("paths", nargs="+")
    d.add_argument("--out", default=None, help="inventory.json 경로")
    d.set_defaults(func=cmd_discover)

    i = sub.add_parser("inspect", help="단일 파일 구조 프로브")
    i.add_argument("file")
    i.set_defaults(func=cmd_inspect)

    v = sub.add_parser("validate", help="층위1 QC (값범위·결측·격자·시간)")
    v.add_argument("file")
    v.add_argument("--out", default=None, help="report.json/md 저장 폴더")
    v.set_defaults(func=cmd_validate)

    vr = sub.add_parser(
        "verify",
        help="모델↔기준 다축 metrics (SAMPLE: 격자/mesh+점관측, 방향/분포/시간/해역)",
    )
    vr.add_argument("model", help="모델 파일 경로")
    vr.add_argument("--ref", required=True, help="기준(관측/재분석) 파일 경로")
    vr.add_argument("--out", default=None,
                    help="verify_report.json/md·그림 저장 폴더")
    vr.add_argument("--points", default=None,
                    help="관측점 목록 파일 경로 (lon lat id 형식; SAMPLE)")
    vr.add_argument("--regions", default=None,
                    help="해역별 분석 해역 이름 쉼표 목록 예: 동해,남해,서해")
    vr.add_argument("--model-tz", default=None, dest="model_tz",
                    help="모델 시간대 (UTC|KST|+09:00; 기본 UTC 가정)")
    vr.add_argument("--ref-tz", default=None, dest="ref_tz",
                    help="기준 시간대 (UTC|KST|+09:00; 기본 UTC 가정) — "
                         "부이 KST vs 모델 UTC 면 9h 어긋남 주의")
    vr.set_defaults(func=cmd_verify)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
