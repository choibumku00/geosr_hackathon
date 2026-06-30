from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from discover import discover  # noqa: E402
from inspect_file import probe  # noqa: E402
from io_detect import open_dataset, UnknownFormatError  # noqa: E402
from qc import run_qc  # noqa: E402
from report import write_report, render_markdown  # noqa: E402


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
# verify 서브커맨드 — SAMPLE
# SAMPLE — 실데이터에선 격자구조·단위·시공간 정합을 실시간 점검하고
#          도메인 맞춤 코드로 적응하라. 이 구현은 대표 케이스 SAMPLE이다.
# ---------------------------------------------------------------------------

def _build_metrics_result(rows: list, model_path: str, ref_path: str,
                          scatter_png=None) -> dict:
    """metrics 결과를 write_report 호환 dict 로 변환 (advisory).

    SAMPLE — status=INFO(advisory). 임계 판정 없음.
    실데이터 적용 시 합격/불합격 임계를 도메인 맞춤으로 정의하라.
    """
    import math
    checks = []
    for r in rows:
        for metric, val in r["metrics"].items():
            evidence = f"{val:.4f}" if (isinstance(val, float) and not math.isnan(val)) else "nan"
            checks.append({
                "check": metric,
                "variable": r["variable"],
                "status": "INFO",
                "evidence": evidence,
            })
    if scatter_png:
        checks.append({
            "check": "scatter_plot",
            "variable": "-",
            "status": "INFO",
            "evidence": scatter_png,
        })
    return {
        "ok": True,
        "summary": {"PASS": len(rows), "FAIL": 0, "WARN": 0},
        "checks": checks,
    }


def _verify_grid_to_grid(d_model, d_ref, model_path: str, ref_path: str, out_dir: str) -> int:
    """격자 대 격자 검증 SAMPLE.

    공통 변수명의 bias / RMSE / SI 를 계산하고 scatter_si 그림 1장을 생성한다.
    SAMPLE — 시공간 정합·단위 통일은 실데이터에서 반드시 점검하라.
    크기가 다른 격자 간 보간은 이 SAMPLE 범위 밖이다 — 도메인 맞춤 코드로 적응하라.
    """
    try:
        import numpy as np
        import metrics_basic
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
            f"model_vars={sorted(model_vars)}, ref_vars={sorted(ref_vars)}. "
            "aliases.py 로 이름 표준화 후 실데이터 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    print(f"[verify] 격자대격자 — 공통 변수: {common}")

    rows = []
    scatter_png = None

    for vname in common:
        try:
            f_arr = d_model.xr[vname].values.astype(float).ravel()
            o_arr = d_ref.xr[vname].values.astype(float).ravel()
        except Exception as e:
            print(f"[verify] {vname} 추출 실패(무시): {e}", file=sys.stderr)
            continue

        b = metrics_basic.bias(f_arr, o_arr)
        r = metrics_basic.rmse(f_arr, o_arr)
        s = metrics_basic.si(f_arr, o_arr)
        print(f"  {vname}: bias={b:.4f}  RMSE={r:.4f}  SI={s:.4f}")
        rows.append({"variable": vname, "metrics": {"bias": b, "rmse": r, "si": s}})

        # scatter_si: 첫 번째 공통 변수에만 1장 생성
        if scatter_png is None:
            try:
                png_path = os.path.join(out_dir, f"scatter_{vname}.png")
                scatter_png = plots.scatter_si(o_arr, f_arr, png_path)
                print(f"  [scatter] {scatter_png}")
            except Exception as e:
                print(f"[verify] scatter 생성 실패(무시): {e}", file=sys.stderr)

    if not rows:
        print("[verify] 계산된 메트릭 없음 — 공통 변수 추출 실패.", file=sys.stderr)
        return 1

    result = _build_metrics_result(rows, model_path, ref_path, scatter_png)
    _, mpath = write_report(result, model_path, out_dir)
    print(f"\n[리포트 저장] {mpath}")
    return 0


def _verify_mesh_point(d_model, d_ref, model_path: str, ref_path: str, out_dir: str) -> int:
    """mesh(모델) + 점관측(기준) 매칭 검증 SAMPLE.

    preprocess.match_points_to_mesh 로 최근접 노드를 찾고,
    공통 변수명의 bias / RMSE / SI 를 계산한다.
    SAMPLE — 공간 정합 오차·단위 불일치는 실데이터에서 반드시 점검하라.
    시간 정합(동기화)은 이 SAMPLE 범위 밖이다 — 도메인 맞춤 코드로 적응하라.
    """
    try:
        import numpy as np
        import metrics_basic
        import preprocess
        import plots
    except ImportError as e:
        print(f"[ERROR] 모듈 불러오기 실패: {e}", file=sys.stderr)
        return 1

    _LAT_NAMES = {"latitude", "lat"}
    _LON_NAMES = {"longitude", "lon"}

    # ── 1. mesh lat/lon 추출 ──────────────────────────────────────────
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

    # ── 2. 기준(점관측) lat/lon 추출 ─────────────────────────────────
    ref_all_names = list(d_ref.xr.coords) + list(d_ref.xr.data_vars)
    ref_lat_name = next(
        (str(n) for n in ref_all_names if str(n).lower() in _LAT_NAMES), None
    )
    ref_lon_name = next(
        (str(n) for n in ref_all_names if str(n).lower() in _LON_NAMES), None
    )
    if ref_lat_name is None or ref_lon_name is None:
        print(
            "[verify] SAMPLE — 기준 파일에서 lat/lon 컬럼/좌표를 찾지 못했다. "
            "점관측 CSV 에 위도(lat/latitude)·경도(lon/longitude) 컬럼이 필요하다. "
            "실데이터에서 헤더를 확인하고 도메인 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    pt_lat = d_ref.xr[ref_lat_name].values.astype(float).ravel()
    pt_lon = d_ref.xr[ref_lon_name].values.astype(float).ravel()

    # ── 3. 최근접 노드 매칭 ───────────────────────────────────────────
    try:
        indices, dists_km = preprocess.match_points_to_mesh(
            mesh_lon, mesh_lat, pt_lon, pt_lat, max_km=50.0
        )
    except Exception as e:
        print(f"[verify] match_points_to_mesh 실패: {e}", file=sys.stderr)
        return 1

    valid_mask = indices >= 0
    n_valid = int(valid_mask.sum())
    print(f"[verify] mesh+점관측 — {len(indices)}점 중 {n_valid}점 매칭 (max_km=50)")
    if n_valid == 0:
        print(
            "[verify] 매칭된 관측점 없음 — max_km 임계를 늘리거나 좌표를 점검하라.",
            file=sys.stderr,
        )
        return 1

    # ── 4. 공통 변수 탐색 (이름 기반 SAMPLE) ─────────────────────────
    _AUX = _LAT_NAMES | _LON_NAMES | {"tri", "mapsta", "MAPSTA", "element", "node"}
    model_vars = {n for n in d_model.data_var_names() if n not in _AUX}
    ref_vars   = {n for n in d_ref.data_var_names()
                  if n not in _AUX and n not in {ref_lat_name, ref_lon_name}}
    common     = sorted(model_vars & ref_vars)

    if not common:
        print(
            f"[verify] SAMPLE — 공통 변수명 없음(mesh={sorted(model_vars)}, "
            f"기준={sorted(ref_vars)}). "
            "aliases.py 로 이름 표준화 후 실데이터 맞춤 코드로 적응하라.",
            file=sys.stderr,
        )
        return 1

    rows = []
    scatter_png = None

    for vname in common:
        try:
            import numpy as np
            model_vals = d_model.xr[vname].values
            ref_vals   = d_ref.xr[vname].values

            # 시간 차원 있으면 평균으로 압축 (SAMPLE)
            if model_vals.ndim == 2:
                model_vals = np.nanmean(model_vals, axis=0)   # (node,)
            if ref_vals.ndim > 1:
                ref_vals = np.nanmean(ref_vals.reshape(-1, ref_vals.shape[-1]), axis=0)

            f_arr = model_vals[indices[valid_mask]].ravel().astype(float)
            o_arr = ref_vals[valid_mask].ravel().astype(float)
        except Exception as e:
            print(f"[verify] {vname} 추출 실패(무시): {e}", file=sys.stderr)
            continue

        b = metrics_basic.bias(f_arr, o_arr)
        r = metrics_basic.rmse(f_arr, o_arr)
        s = metrics_basic.si(f_arr, o_arr)
        print(f"  {vname}: bias={b:.4f}  RMSE={r:.4f}  SI={s:.4f}")
        rows.append({"variable": vname, "metrics": {"bias": b, "rmse": r, "si": s}})

        if scatter_png is None:
            try:
                png_path = os.path.join(out_dir, f"scatter_{vname}.png")
                scatter_png = plots.scatter_si(o_arr, f_arr, png_path)
                print(f"  [scatter] {scatter_png}")
            except Exception as e:
                print(f"[verify] scatter 생성 실패(무시): {e}", file=sys.stderr)

    if not rows:
        print("[verify] 계산된 메트릭 없음 — 공통 변수 추출 실패.", file=sys.stderr)
        return 1

    result = _build_metrics_result(rows, model_path, ref_path, scatter_png)
    _, mpath = write_report(result, model_path, out_dir)
    print(f"\n[리포트 저장] {mpath}")
    return 0


def cmd_verify(args) -> int:
    """SAMPLE — verify 서브커맨드.

    격자대격자: 공통 변수 bias/RMSE/SI 표 + scatter_si 그림 1장.
    mesh+점관측: preprocess.match_points_to_mesh 매칭 후 동일.
    그 외: 명확한 메시지 + exit 1 (크래시 없음).

    SAMPLE — 실데이터에선 격자구조·단위·시공간 정합을 실시간 점검하고
    도메인 맞춤 코드로 적응하라.
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
        return _verify_grid_to_grid(d_model, d_ref, args.model, args.ref, out_dir)

    if model_ck == "mesh":
        return _verify_mesh_point(d_model, d_ref, args.model, args.ref, out_dir)

    print(
        f"[verify] SAMPLE — 지원하지 않는 격자 조합: model={model_ck}, ref={ref_ck}. "
        "격자대격자(1d/2d↔1d/2d) 또는 mesh+참조 파일 조합만 지원. "
        "실데이터 맞춤 코드로 적응하라.",
        file=sys.stderr,
    )
    return 1


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

    vr = sub.add_parser("verify", help="모델↔기준 metrics (SAMPLE: bias/RMSE/SI + scatter)")
    vr.add_argument("model", help="모델 파일 경로")
    vr.add_argument("--ref", required=True, help="기준(관측/재분석) 파일 경로")
    vr.add_argument("--out", default=None, help="report.json/md·scatter PNG 저장 폴더")
    vr.set_defaults(func=cmd_verify)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
