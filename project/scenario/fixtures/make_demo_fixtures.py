"""데모/인수테스트용 fixture 생성기 (정상본 + 고의결함본).

- ERA5(공개 재분석)는 실파일을 작게 잘라 사용. → era5_demo_clean.nc / _broken.nc / _truncated.nc
- 부이(민감·권한제한)는 실데이터를 쓰지 않고 **합성**(cp949·한글헤더)으로 생성. → buoy_demo_clean.csv / _broken.csv

각 결함과 "스킬 QC가 잡아내야 할 것"은 README.md(정답지)에 정리되어 있다.
재현: `python make_demo_fixtures.py` (ERA5 원본이 project/data/에 있어야 .nc 생성;
없으면 부이 CSV만 생성).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ERA5_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "data", "era5_rean_glo_day_20220906.nc"))

# 한국 부근으로 작게 자르기 (인덱스 기반 — 좌표 순서에 안전)
LAT_SLICE = slice(200, 280)   # 80
LON_SLICE = slice(480, 560)   # 80
TIME_SLICE = slice(0, 3)      # 3 스텝
KEEP_VARS = ["t2m", "u10", "v10"]


def _make_era5_fixtures():
    if not os.path.exists(ERA5_SRC):
        print(f"[skip] ERA5 원본 없음: {ERA5_SRC} — .nc fixture 생략")
        return
    import xarray as xr

    ds = xr.open_dataset(ERA5_SRC)
    sub = ds[[v for v in KEEP_VARS if v in ds]].isel(
        time=TIME_SLICE, lat=LAT_SLICE, lon=LON_SLICE
    ).load()
    ds.close()

    # --- 정상본 ---
    clean_path = os.path.join(HERE, "era5_demo_clean.nc")
    sub.to_netcdf(clean_path, format="NETCDF4", engine="netcdf4")
    print("wrote", clean_path, f"({os.path.getsize(clean_path)//1024} KB)")

    # --- 고의결함본 ---
    bad = sub.copy(deep=True)
    # (1) 값범위 초과: t2m 일부에 500K(=227°C, 물리적으로 불가) 주입
    t2m = bad["t2m"].values
    t2m[0, 5:8, 5:8] = 500.0
    # (2) 결측 구멍: t2m 한 블록 NaN
    t2m[0, 20:30, 20:35] = np.nan
    bad["t2m"].values[...] = t2m
    # (3) 이상치(음수 풍속 성분은 정상이므로, 비현실적 큰 값 주입)
    u = bad["u10"].values
    u[0, 40, 40] = 999.0   # 1000 m/s 급 풍속 — 이상치
    bad["u10"].values[...] = u
    # (4) 격자 비단조: lat 좌표 두 점 swap → 단조성 깨짐
    lat = bad["lat"].values.copy()
    lat[10], lat[11] = lat[11], lat[10]
    bad = bad.assign_coords(lat=lat)
    broken_path = os.path.join(HERE, "era5_demo_broken.nc")
    bad.to_netcdf(broken_path, format="NETCDF4", engine="netcdf4")
    print("wrote", broken_path, f"({os.path.getsize(broken_path)//1024} KB)")

    # --- 손상(잘림)본: 정상본을 바이트 단위로 60%만 남김 ---
    trunc_path = os.path.join(HERE, "era5_demo_truncated.nc")
    with open(clean_path, "rb") as f:
        blob = f.read()
    with open(trunc_path, "wb") as f:
        f.write(blob[: int(len(blob) * 0.6)])
    print("wrote", trunc_path, f"({os.path.getsize(trunc_path)//1024} KB, 손상)")


# ---------- 부이(합성, cp949, 한글헤더) ----------
_COLS = ["지점", "일시", "풍속(m/s)", "풍향(deg)", "GUST풍속(m/s)", "현지기압(hPa)",
         "습도(%)", "기온(°C)", "수온(°C)", "최대파고(m)", "유의파고(m)", "평균파고(m)",
         "파주기(sec)", "파향(deg)"]


def _synth_buoy(n=48, seed=20240915):
    rng = np.random.RandomState(seed)
    t = pd.date_range("2024-09-14 00:00", periods=n, freq="h")
    # 고파 이벤트 흉내: 가운데 시점에 유의파고 상승
    base = 1.0 + 1.8 * np.exp(-((np.arange(n) - n * 0.55) ** 2) / (2 * 6 ** 2))
    hs = np.round(base + rng.uniform(-0.1, 0.1, n), 1)
    df = pd.DataFrame({
        "지점": "DEMO01",
        "일시": t.strftime("%Y-%m-%d %H:%M"),
        "풍속(m/s)": np.round(rng.uniform(2, 12, n), 1),
        "풍향(deg)": rng.randint(0, 360, n),
        "GUST풍속(m/s)": np.round(rng.uniform(3, 16, n), 1),
        "현지기압(hPa)": np.round(rng.uniform(1002, 1015, n), 1),
        "습도(%)": rng.randint(55, 95, n),
        "기온(°C)": np.round(rng.uniform(18, 26, n), 1),
        "수온(°C)": np.round(rng.uniform(22, 26, n), 1),
        "최대파고(m)": np.round(hs * 1.5, 1),
        "유의파고(m)": hs,
        "평균파고(m)": np.round(hs * 0.65, 1),
        "파주기(sec)": np.round(rng.uniform(4, 11, n), 1),
        "파향(deg)": rng.randint(0, 360, n),
    })
    return df


def _make_buoy_fixtures():
    clean = _synth_buoy()
    clean_path = os.path.join(HERE, "buoy_demo_clean.csv")
    clean.to_csv(clean_path, index=False, encoding="cp949")
    print("wrote", clean_path, f"({os.path.getsize(clean_path)} B, cp949)")

    bad = clean.copy()
    # (1) 값범위 초과: 유의파고 99.9 m (불가)
    bad.loc[10, "유의파고(m)"] = 99.9
    # (2) 음수 파고(불가)
    bad.loc[12, "유의파고(m)"] = -1.0
    # (3) 결측: 몇 칸 비우기
    bad.loc[15:18, "파주기(sec)"] = np.nan
    # (4) 파향 범위 초과(>360)
    bad.loc[20, "파향(deg)"] = 999
    # (5) 시간 중복
    bad.loc[25, "일시"] = bad.loc[24, "일시"]
    # (6) 깨진 타임스탬프
    bad.loc[30, "일시"] = "2024-13-40 99:99"
    bad_path = os.path.join(HERE, "buoy_demo_broken.csv")
    bad.to_csv(bad_path, index=False, encoding="cp949")
    print("wrote", bad_path, f"({os.path.getsize(bad_path)} B, cp949)")


if __name__ == "__main__":
    _make_era5_fixtures()
    _make_buoy_fixtures()
    print("done.")
