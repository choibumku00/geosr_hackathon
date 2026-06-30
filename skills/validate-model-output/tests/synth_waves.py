"""파랑 데모용 합성 데이터 생성기.

SAMPLE — 실데이터에서는 구조를 실시간 점검하고
도메인 맞춤 코드로 적응하라.
변수명·단위·격자 위상은 실제 WW3 출력물마다 다를 수 있다.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr


def ww3_mesh_like() -> xr.Dataset:
    """WAVEWATCH III 비정형 삼각 mesh 모사 Dataset.

    dims : node(40), element(60), time(6), noel(3 — tri 두 번째 차원).
    격자 lat/lon 은 좌표 축이 아닌 data variable 로 저장한다(mesh 핵심).

    SAMPLE — 실데이터에서 구조(변수명·단위·노드 수·위상)를 반드시 실시간 점검하라.
    """
    rng = np.random.default_rng(42)
    N_NODE = 40
    N_ELEM = 60
    N_TIME = 6
    NOEL = 3   # triangle → 3 nodes per element

    # 시간 축 (3시간 간격)
    times = np.array(
        [np.datetime64("2024-01-01T00:00") + np.timedelta64(3 * i, "h")
         for i in range(N_TIME)]
    )

    # 격자 위치 (한국 근해 난수)
    lon_node = rng.uniform(124.0, 132.0, N_NODE).astype("float32")
    lat_node = rng.uniform(33.0, 38.0, N_NODE).astype("float32")

    # 파랑·바람 데이터
    hs   = rng.uniform(0.5, 6.0,   (N_TIME, N_NODE)).astype("float32")
    t01  = rng.uniform(3.0, 15.0,  (N_TIME, N_NODE)).astype("float32")
    dir_ = rng.uniform(0.0, 360.0, (N_TIME, N_NODE)).astype("float32")
    uwnd = rng.uniform(-15.0, 15.0, (N_TIME, N_NODE)).astype("float32")
    vwnd = rng.uniform(-15.0, 15.0, (N_TIME, N_NODE)).astype("float32")

    # 삼각망 연결정보 (0-based 노드 인덱스)
    tri = rng.integers(0, N_NODE, (N_ELEM, NOEL)).astype("int32")

    # 상태맵 (1=활성, 0=육지)
    mapsta = np.ones(N_NODE, dtype="int32")

    ds = xr.Dataset(
        {
            "hs": xr.DataArray(
                hs, dims=("time", "node"),
                attrs={
                    "units": "m",
                    "standard_name": "sea_surface_wave_significant_height",
                    "long_name": "Significant wave height",
                },
            ),
            "t01": xr.DataArray(
                t01, dims=("time", "node"),
                attrs={
                    "units": "s",
                    "long_name": "Mean wave period T01",
                },
            ),
            "dir": xr.DataArray(
                dir_, dims=("time", "node"),
                attrs={
                    "units": "deg",
                    "long_name": "Mean wave direction",
                },
            ),
            "uwnd": xr.DataArray(
                uwnd, dims=("time", "node"),
                attrs={
                    "units": "m/s",
                    "standard_name": "eastward_wind",
                    "long_name": "U-component of wind",
                },
            ),
            "vwnd": xr.DataArray(
                vwnd, dims=("time", "node"),
                attrs={
                    "units": "m/s",
                    "standard_name": "northward_wind",
                    "long_name": "V-component of wind",
                },
            ),
            # lat/lon 은 data variable — 좌표 축(coord) 아님(mesh 핵심)
            "longitude": xr.DataArray(
                lon_node, dims=("node",),
                attrs={
                    "units": "degrees_east",
                    "standard_name": "longitude",
                    "long_name": "Longitude of mesh node",
                },
            ),
            "latitude": xr.DataArray(
                lat_node, dims=("node",),
                attrs={
                    "units": "degrees_north",
                    "standard_name": "latitude",
                    "long_name": "Latitude of mesh node",
                },
            ),
            "tri": xr.DataArray(
                tri, dims=("element", "noel"),
                attrs={
                    "long_name": "Triangular element connectivity (0-based node index)",
                },
            ),
            "MAPSTA": xr.DataArray(
                mapsta, dims=("node",),
                attrs={
                    "long_name": "Status map (1=active, 0=land/excluded)",
                },
            ),
        },
        coords={"time": times},
    )
    return ds


def buoy_obs_like() -> pd.DataFrame:
    """부이 점관측 DataFrame (한글 헤더, cp949 호환).

    3개 지점 × 6 시간 스텝 = 18행.

    SAMPLE — 실데이터에서는 컬럼명·단위·결측 처리 방식을 실시간 점검하라.
    """
    rng = np.random.default_rng(42)

    time_labels = [
        f"2024-01-01 {h:02d}:00"
        for h in [0, 3, 6, 9, 12, 15]
    ]
    stations = ["부산_B01", "거제_B02", "여수_B03"]

    rows = []
    for t in time_labels:
        for stn in stations:
            rows.append({
                "일시":   t,
                "지점":   stn,
                "유의파고":   round(float(rng.uniform(0.3, 4.0)),  2),
                "파주기":     round(float(rng.uniform(4.0, 12.0)), 1),
                "파향":       round(float(rng.uniform(0.0, 360.0)), 0),
                "수온":       round(float(rng.uniform(10.0, 28.0)), 1),
                "풍속":       round(float(rng.uniform(1.0, 15.0)),  1),
                "풍향":       round(float(rng.uniform(0.0, 360.0)), 0),
            })

    return pd.DataFrame(rows)
