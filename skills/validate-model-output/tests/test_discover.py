import os
import subprocess
import sys
from discover import discover, guess_role

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")


def test_guess_role():
    assert guess_role("gfs_fcst_glo_day.nc") == "output"
    assert guess_role("era5_rean_glo_day.nc") == "reference"
    assert guess_role("buoy_obs_2022.csv") == "reference"
    assert guess_role("random.nc") == "unknown"


def test_discover_folder():
    r = discover([DATA])
    files = {os.path.basename(f["path"]): f for f in r["files"]}
    assert "clean_era5_like.nc" in files
    assert "clean_gfs_like.nc" in files
    assert files["clean_era5_like.nc"]["domain"] == "meteorology"
    # 적어도 하나는 openable
    assert any(f["openable"] for f in r["files"])


def test_cli_discover_runs():
    out = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, "cli.py"), "discover", DATA],
        capture_output=True, text=True,
    )
    assert out.returncode == 0
    assert "clean_era5_like.nc" in out.stdout
