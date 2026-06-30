"""verify 다축 배선 확인 테스트 — SAMPLE.

SAMPLE — 실데이터 적용 시 격자·단위·시공간 구조를 실시간 점검하라.
이 파일은 verify cli/report 배선이 graceful 하게 동작하는지 확인한다.
"""
from __future__ import annotations

import os
import sys
import json
import types

import numpy as np
import pytest

# scripts/ 경로 (conftest 가 추가하지만 직접 보장)
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from report import (
    render_verify_markdown,
    write_verify_report,
    render_markdown,   # 기존 QC 렌더 보존 확인
    write_report,
    build_report,
)


# ---------------------------------------------------------------------------
# 헬퍼: 합성 verify_result
# ---------------------------------------------------------------------------

def _make_result(mode="grid_to_grid", tz_assumed=False, has_regions=True):
    return {
        "mode": mode,
        "ok": True,
        "model": "/tmp/model.nc",
        "ref": "/tmp/ref.nc",
        "tz_assumed": tz_assumed,
        "accuracy_rows": [
            {"variable": "hs", "n": 100, "bias": 0.05,
             "rmse": 0.20, "si": 0.12, "pearson_r": 0.93},
        ],
        "direction_rows": [
            {"variable": "dir", "n": 100, "circular_cme": -3.5,
             "circular_rmse": 18.0, "circular_corr": 0.82},
        ],
        "plots": {
            "scatter": None,
            "taylor": None,
            "diff_map": None,
            "qq": None,
            "timeseries": None,
            "wave_rose_model": None,
            "wave_rose_ref": None,
        },
        "regions": (
            [{"name": "동해", "accuracy_rows": [
                {"variable": "hs", "n": 30, "bias": 0.02,
                 "rmse": 0.18, "si": 0.10, "pearson_r": 0.95},
            ], "direction_rows": []}]
            if has_regions else []
        ),
        "info": "테스트 합성 결과",
    }


# ---------------------------------------------------------------------------
# report.py 신규 함수 테스트
# ---------------------------------------------------------------------------

class TestRenderVerifyMarkdown:
    def test_sections_present(self):
        md = render_verify_markdown(_make_result())
        for section in ["§ 정확도", "§ 분포", "§ 시간", "§ 방향", "§ 종합"]:
            assert section in md, f"섹션 없음: {section}"

    def test_accuracy_table_values(self):
        md = render_verify_markdown(_make_result())
        assert "hs" in md
        assert "0.0500" in md or "0.05" in md  # bias

    def test_direction_table_values(self):
        md = render_verify_markdown(_make_result())
        assert "dir" in md
        assert "-3.5" in md or "-3.50" in md   # circular_cme

    def test_tz_warning_shown_when_assumed(self):
        md = render_verify_markdown(_make_result(tz_assumed=True))
        assert "TZ 미확인" in md
        assert "KST" in md

    def test_tz_warning_absent_when_not_assumed(self):
        md = render_verify_markdown(_make_result(tz_assumed=False))
        assert "TZ 미확인" not in md

    def test_advisory_always_present(self):
        md = render_verify_markdown(_make_result())
        assert "§G Advisory" in md
        assert "reference" in md.lower() or "truth" in md.lower()

    def test_regions_section_when_present(self):
        md = render_verify_markdown(_make_result(has_regions=True))
        assert "§ 해역별" in md
        assert "동해" in md

    def test_regions_absent_when_empty(self):
        md = render_verify_markdown(_make_result(has_regions=False))
        assert "§ 해역별" not in md

    def test_mesh_point_mode_label(self):
        md = render_verify_markdown(_make_result(mode="mesh_point"))
        assert "mesh" in md.lower() or "점관측" in md

    def test_plot_none_shows_없음(self):
        md = render_verify_markdown(_make_result())
        assert "(없음)" in md

    def test_plot_link_when_path_given(self, tmp_path):
        r = _make_result()
        r["plots"]["scatter"] = str(tmp_path / "scatter.png")
        md = render_verify_markdown(r)
        assert "scatter.png" in md
        assert "![" in md     # 마크다운 이미지 링크


class TestWriteVerifyReport:
    def test_files_created(self, tmp_path):
        r = _make_result()
        jpath, mpath = write_verify_report(r, "/model.nc", "/ref.nc", str(tmp_path))
        assert os.path.exists(jpath), "verify_report.json 없음"
        assert os.path.exists(mpath), "verify_report.md 없음"

    def test_json_parseable(self, tmp_path):
        r = _make_result()
        jpath, _ = write_verify_report(r, "/model.nc", "/ref.nc", str(tmp_path))
        with open(jpath, encoding="utf-8") as f:
            data = json.load(f)
        assert data["mode"] == "grid_to_grid"
        assert "accuracy_rows" in data

    def test_md_contains_advisory(self, tmp_path):
        r = _make_result()
        _, mpath = write_verify_report(r, "/model.nc", "/ref.nc", str(tmp_path))
        content = open(mpath, encoding="utf-8").read()
        assert "§G Advisory" in content

    def test_separate_from_qc_write_report(self, tmp_path):
        """verify_report.* 와 report.* 가 독립 파일임을 확인한다."""
        r = _make_result()
        write_verify_report(r, "/m.nc", "/r.nc", str(tmp_path))
        # QC report 도 같은 폴더에 쓰기
        qc = {"checks": [{"check": "x", "variable": None, "status": "PASS", "evidence": "ok"}],
              "summary": {"PASS": 1, "FAIL": 0, "WARN": 0}, "ok": True}
        write_report(qc, "/m.nc", str(tmp_path))
        # 두 쌍 모두 존재해야 함
        assert os.path.exists(tmp_path / "verify_report.md")
        assert os.path.exists(tmp_path / "report.md")


# ---------------------------------------------------------------------------
# 기존 QC render/write 보존 확인
# ---------------------------------------------------------------------------

class TestLegacyQCPreserved:
    _QC = {
        "checks": [{"check": "val", "variable": "t2m", "status": "PASS", "evidence": "ok"}],
        "summary": {"PASS": 1, "FAIL": 0, "WARN": 0},
        "ok": True,
    }

    def test_build_report_intact(self):
        r = build_report(self._QC, "x.nc")
        assert r["ok"] is True
        assert r["source"] == "x.nc"

    def test_render_markdown_intact(self):
        md = render_markdown(self._QC, "x.nc")
        assert "QC 리포트" in md
        assert "advisory" in md.lower() or "reference" in md.lower()

    def test_write_report_intact(self, tmp_path):
        jpath, mpath = write_report(self._QC, "x.nc", str(tmp_path))
        assert os.path.exists(jpath)
        assert os.path.exists(mpath)


# ---------------------------------------------------------------------------
# cli.verify 배선 — 합성 fixture 를 사용한 end-to-end
# ---------------------------------------------------------------------------

@pytest.fixture
def grid_nc_pair(tmp_path):
    """ERA5-like 두 nc 파일(동일 격자): t2m(degC vs K), u10, v10, dir."""
    import xarray as xr

    rng = np.random.default_rng(0)
    lat = np.linspace(33, 38, 10, dtype="float32")
    lon = np.linspace(124, 132, 12, dtype="float32")
    times = np.array(
        [np.datetime64("2024-01-01T00:00") + np.timedelta64(3 * i, "h")
         for i in range(4)]
    )

    shape = (4, 10, 12)
    t2m_k  = rng.uniform(273, 303, shape).astype("float32")
    t2m_c  = t2m_k - 273.15
    u10    = rng.uniform(-10, 10, shape).astype("float32")
    v10    = rng.uniform(-10, 10, shape).astype("float32")
    wd     = (np.degrees(np.arctan2(-u10, -v10)) % 360).astype("float32")

    def _make_ds(t2m_arr, t2m_units):
        return xr.Dataset(
            {
                "t2m": xr.DataArray(t2m_arr, dims=("time", "lat", "lon"),
                                    attrs={"units": t2m_units}),
                "u10": xr.DataArray(u10, dims=("time", "lat", "lon"),
                                    attrs={"units": "m/s"}),
                "v10": xr.DataArray(v10, dims=("time", "lat", "lon"),
                                    attrs={"units": "m/s"}),
                "wdir": xr.DataArray(wd, dims=("time", "lat", "lon"),
                                     attrs={"units": "deg",
                                            "long_name": "wind direction"}),
            },
            coords={
                "time": times,
                "lat":  lat,
                "lon":  lon,
            },
        )

    ds_model = _make_ds(t2m_k, "K")
    ds_ref   = _make_ds(t2m_c, "degC")

    model_path = str(tmp_path / "model.nc")
    ref_path   = str(tmp_path / "ref.nc")
    ds_model.to_netcdf(model_path)
    ds_ref.to_netcdf(ref_path)
    return model_path, ref_path


@pytest.fixture
def mesh_csv_pair(tmp_path):
    """WW3-like mesh nc + 부이 CSV (lat/lon 직접 포함)."""
    import xarray as xr
    import pandas as pd

    rng  = np.random.default_rng(1)
    N    = 30
    T    = 4
    times = np.array(
        [np.datetime64("2024-01-01T00:00") + np.timedelta64(3 * i, "h")
         for i in range(T)]
    )
    lat_node = rng.uniform(34.0, 37.0, N).astype("float32")
    lon_node = rng.uniform(125.0, 130.0, N).astype("float32")
    hs  = rng.uniform(0.5, 4.0, (T, N)).astype("float32")
    dp  = rng.uniform(0, 360, (T, N)).astype("float32")

    ds = xr.Dataset(
        {
            "hs": xr.DataArray(hs, dims=("time", "node"),
                               attrs={"units": "m"}),
            "dp": xr.DataArray(dp, dims=("time", "node"),
                               attrs={"units": "deg",
                                      "long_name": "peak wave direction"}),
            "latitude":  xr.DataArray(lat_node, dims=("node",)),
            "longitude": xr.DataArray(lon_node, dims=("node",)),
        },
        coords={"time": times},
    )
    mesh_path = str(tmp_path / "mesh.nc")
    ds.to_netcdf(mesh_path)

    # 부이 CSV: 3개 관측점 (mesh 노드 근방 좌표)
    buoy_lat = lat_node[:3] + 0.01   # 약간 이동 (matching 가능)
    buoy_lon = lon_node[:3] + 0.01
    rows = []
    for ti, t in enumerate(times):
        for si in range(3):
            rows.append({
                "time": str(t),
                "lat":  float(buoy_lat[si]),
                "lon":  float(buoy_lon[si]),
                "hs":   float(rng.uniform(0.4, 3.8)),
                "dp":   float(rng.uniform(0, 360)),
            })
    df = pd.DataFrame(rows)
    csv_path = str(tmp_path / "buoy.csv")
    df.to_csv(csv_path, index=False)
    return mesh_path, csv_path


class TestVerifyGridToGrid:
    def test_verify_exits_0(self, grid_nc_pair, tmp_path):
        from cli import main
        model_path, ref_path = grid_nc_pair
        rc = main(["verify", model_path, "--ref", ref_path, "--out", str(tmp_path)])
        assert rc == 0

    def test_verify_creates_report(self, grid_nc_pair, tmp_path):
        from cli import main
        model_path, ref_path = grid_nc_pair
        main(["verify", model_path, "--ref", ref_path, "--out", str(tmp_path)])
        assert os.path.exists(tmp_path / "verify_report.md")
        assert os.path.exists(tmp_path / "verify_report.json")

    def test_direction_var_detected(self, grid_nc_pair, tmp_path):
        from cli import main
        model_path, ref_path = grid_nc_pair
        main(["verify", model_path, "--ref", ref_path, "--out", str(tmp_path)])
        with open(tmp_path / "verify_report.json", encoding="utf-8") as f:
            data = json.load(f)
        dir_vars = [r["variable"] for r in data.get("direction_rows", [])]
        assert "wdir" in dir_vars, f"wdir 를 direction 으로 인식 못함: {dir_vars}"

    def test_accuracy_var_detected(self, grid_nc_pair, tmp_path):
        from cli import main
        model_path, ref_path = grid_nc_pair
        main(["verify", model_path, "--ref", ref_path, "--out", str(tmp_path)])
        with open(tmp_path / "verify_report.json", encoding="utf-8") as f:
            data = json.load(f)
        acc_vars = [r["variable"] for r in data.get("accuracy_rows", [])]
        assert len(acc_vars) >= 1, f"정확도 변수 없음: {acc_vars}"

    def test_regions_option(self, grid_nc_pair, tmp_path):
        from cli import main
        model_path, ref_path = grid_nc_pair
        rc = main(["verify", model_path, "--ref", ref_path,
                   "--out", str(tmp_path), "--regions", "동해,남해"])
        assert rc == 0
        with open(tmp_path / "verify_report.json", encoding="utf-8") as f:
            data = json.load(f)
        rnames = [r["name"] for r in data.get("regions", [])]
        # 데이터가 bbox 안에 있을 수도 없을 수도 있으나 처리 자체는 해야 함
        assert "동해" in rnames or "남해" in rnames or len(rnames) == 0


class TestVerifyMeshPoint:
    def test_verify_exits_0(self, mesh_csv_pair, tmp_path):
        from cli import main
        mesh_path, csv_path = mesh_csv_pair
        rc = main(["verify", mesh_path, "--ref", csv_path, "--out", str(tmp_path)])
        assert rc == 0

    def test_creates_report(self, mesh_csv_pair, tmp_path):
        from cli import main
        mesh_path, csv_path = mesh_csv_pair
        main(["verify", mesh_path, "--ref", csv_path, "--out", str(tmp_path)])
        assert os.path.exists(tmp_path / "verify_report.md")

    def test_direction_row_in_result(self, mesh_csv_pair, tmp_path):
        from cli import main
        mesh_path, csv_path = mesh_csv_pair
        main(["verify", mesh_path, "--ref", csv_path, "--out", str(tmp_path)])
        with open(tmp_path / "verify_report.json", encoding="utf-8") as f:
            data = json.load(f)
        dir_vars = [r["variable"] for r in data.get("direction_rows", [])]
        assert "dp" in dir_vars, f"dp 를 direction 으로 인식 못함: {dir_vars}"

    def test_hs_accuracy_in_result(self, mesh_csv_pair, tmp_path):
        from cli import main
        mesh_path, csv_path = mesh_csv_pair
        main(["verify", mesh_path, "--ref", csv_path, "--out", str(tmp_path)])
        with open(tmp_path / "verify_report.json", encoding="utf-8") as f:
            data = json.load(f)
        acc_vars = [r["variable"] for r in data.get("accuracy_rows", [])]
        assert "hs" in acc_vars, f"hs 정확도 없음: {acc_vars}"

    def test_ref_tz_kst_flag(self, mesh_csv_pair, tmp_path):
        """--ref-tz KST 옵션이 graceful 하게 동작하는지 확인."""
        from cli import main
        mesh_path, csv_path = mesh_csv_pair
        rc = main(["verify", mesh_path, "--ref", csv_path,
                   "--out", str(tmp_path), "--ref-tz", "KST"])
        # KST 지정 → -9h 후 교집합 없을 수 있음(합성 데이터) → 0 or 1 모두 허용
        assert rc in (0, 1)

    def test_no_coord_graceful_exit(self, tmp_path):
        """lat/lon 없는 CSV 기준 파일 → 좌표 출처 필요 메시지 + exit 1."""
        import xarray as xr
        import pandas as pd

        rng = np.random.default_rng(2)
        N, T = 20, 3
        times = np.array([np.datetime64("2024-01-01") + np.timedelta64(i, "h")
                          for i in range(T)])
        ds = xr.Dataset(
            {
                "hs": xr.DataArray(rng.uniform(0.5, 3.0, (T, N)).astype("float32"),
                                   dims=("time", "node")),
                "latitude":  xr.DataArray(rng.uniform(34, 37, N).astype("float32"),
                                          dims=("node",)),
                "longitude": xr.DataArray(rng.uniform(125, 130, N).astype("float32"),
                                          dims=("node",)),
            },
            coords={"time": times},
        )
        mesh_nc = str(tmp_path / "mesh2.nc")
        ds.to_netcdf(mesh_nc)

        # 좌표 없는 CSV
        df_nocoord = pd.DataFrame({"hs": [1.0, 1.2, 0.9]})
        csv_nocoord = str(tmp_path / "nocoord.csv")
        df_nocoord.to_csv(csv_nocoord, index=False)

        from cli import main
        rc = main(["verify", mesh_nc, "--ref", csv_nocoord, "--out", str(tmp_path)])
        assert rc == 1   # graceful exit 1, 크래시 아님
