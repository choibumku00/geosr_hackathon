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
        write_report(qc, args.file, out_dir)
        return 1
    qc = run_qc(d)
    print(render_markdown(qc, args.file))
    jpath, mpath = write_report(qc, args.file, out_dir)
    print(f"\n[리포트 저장] {mpath}")
    return 0 if qc["ok"] else 1


def main(argv=None) -> int:
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

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
