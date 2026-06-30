"""synth_waves 함수 unit test (focused — make_waves_fixtures 이전 검증)."""
import os
import sys

import numpy as np
import pandas as pd
import pytest
import xarray as xr

# tests/ 자체가 sys.path 에 없을 경우 보완
_TESTS = os.path.dirname(os.path.abspath(__file__))
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)

from synth_waves import buoy_obs_like, ww3_mesh_like


# ─── ww3_mesh_like ────────────────────────────────────────────────────

class TestWw3MeshLike:
    def setup_method(self):
        self.ds = ww3_mesh_like()

    def test_returns_dataset(self):
        assert isinstance(self.ds, xr.Dataset)

    def test_required_data_vars(self):
        required = {"hs", "t01", "dir", "uwnd", "vwnd",
                    "longitude", "latitude", "tri", "MAPSTA"}
        assert required <= set(self.ds.data_vars), (
            f"missing: {required - set(self.ds.data_vars)}"
        )

    def test_dims_node_time(self):
        assert self.ds.sizes["node"] == 40
        assert self.ds.sizes["time"] == 6
        assert self.ds.sizes["element"] == 60
        assert self.ds.sizes["noel"] == 3

    def test_no_lat_lon_in_coords(self):
        """위도·경도는 data variable 이어야 함 — 좌표 축 금지."""
        assert "latitude"  not in self.ds.coords
        assert "longitude" not in self.ds.coords
        assert "lat"       not in self.ds.coords
        assert "lon"       not in self.ds.coords

    def test_time_in_coords(self):
        assert "time" in self.ds.coords
        assert self.ds.sizes["time"] == 6

    def test_hs_range(self):
        vals = self.ds["hs"].values
        assert float(vals.min()) >= 0.5 - 1e-4
        assert float(vals.max()) <= 6.0 + 1e-4

    def test_hs_standard_name(self):
        assert self.ds["hs"].attrs.get("standard_name") == \
            "sea_surface_wave_significant_height"

    def test_hs_units(self):
        assert self.ds["hs"].attrs.get("units") == "m"

    def test_wind_standard_names(self):
        assert self.ds["uwnd"].attrs.get("standard_name") == "eastward_wind"
        assert self.ds["vwnd"].attrs.get("standard_name") == "northward_wind"

    def test_dir_range(self):
        vals = self.ds["dir"].values
        assert float(vals.min()) >= 0.0 - 1e-4
        assert float(vals.max()) <= 360.0 + 1e-4

    def test_lon_range(self):
        lon = self.ds["longitude"].values
        assert float(lon.min()) >= 124.0 - 1e-3
        assert float(lon.max()) <= 132.0 + 1e-3

    def test_lat_range(self):
        lat = self.ds["latitude"].values
        assert float(lat.min()) >= 33.0 - 1e-3
        assert float(lat.max()) <= 38.0 + 1e-3

    def test_tri_shape_and_dtype(self):
        tri = self.ds["tri"]
        assert tri.dims == ("element", "noel")
        assert tri.shape == (60, 3)
        assert np.issubdtype(tri.dtype, np.integer)

    def test_mapsta_all_active(self):
        mapsta = self.ds["MAPSTA"].values
        assert mapsta.shape == (40,)
        assert (mapsta == 1).all()

    def test_reproducible(self):
        ds2 = ww3_mesh_like()
        np.testing.assert_array_equal(
            self.ds["hs"].values, ds2["hs"].values
        )


# ─── buoy_obs_like ────────────────────────────────────────────────────

class TestBuoyObsLike:
    def setup_method(self):
        self.df = buoy_obs_like()

    def test_returns_dataframe(self):
        assert isinstance(self.df, pd.DataFrame)

    def test_row_count(self):
        # 3 stations × 6 time steps
        assert len(self.df) == 18

    def test_korean_columns(self):
        expected = {"일시", "지점", "유의파고", "파주기", "파향", "수온", "풍속", "풍향"}
        assert expected <= set(self.df.columns), (
            f"missing columns: {expected - set(self.df.columns)}"
        )

    def test_three_stations(self):
        assert self.df["지점"].nunique() == 3

    def test_six_time_steps(self):
        assert self.df["일시"].nunique() == 6

    def test_time_format(self):
        """일시 값이 YYYY-MM-DD HH:MM 형식인지 확인."""
        sample = self.df["일시"].iloc[0]
        pd.to_datetime(sample, format="%Y-%m-%d %H:%M")  # 파싱 실패 시 ValueError

    def test_hs_range(self):
        vals = self.df["유의파고"].dropna()
        assert (vals >= 0.3).all()
        assert (vals <= 4.0).all()

    def test_wave_period_range(self):
        vals = self.df["파주기"].dropna()
        assert (vals >= 4.0).all()
        assert (vals <= 12.0).all()

    def test_direction_range(self):
        for col in ("파향", "풍향"):
            vals = self.df[col].dropna()
            assert (vals >= 0.0).all() and (vals <= 360.0).all(), col

    def test_cp949_encodable(self):
        """한글 헤더와 지점 이름이 cp949 로 인코딩 가능한지 확인."""
        for col in self.df.columns:
            col.encode("cp949")
        for val in self.df["지점"].unique():
            val.encode("cp949")
