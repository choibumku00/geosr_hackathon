import os
import subprocess
import sys

SKILL = os.path.dirname(os.path.dirname(__file__))
SCRIPTS = os.path.join(SKILL, "scripts")
DATA = os.path.join(SKILL, "data")


def _run(args, cwd=SKILL):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "cli.py")] + args,
                          capture_output=True, text=True, encoding="utf-8", cwd=cwd, env=env)


def test_validate_clean_exit0(tmp_path):
    out = _run(["validate", os.path.join(DATA, "clean_era5_like.nc"), "--out", str(tmp_path)])
    assert out.returncode == 0
    assert os.path.exists(os.path.join(tmp_path, "report.md"))
    assert "PASS" in out.stdout


def test_validate_broken_exit1(tmp_path):
    out = _run(["validate", os.path.join(DATA, "broken_era5_like.nc"), "--out", str(tmp_path)])
    assert out.returncode == 1
    assert "FAIL" in out.stdout


def test_validate_missing_file_no_crash(tmp_path):
    out = _run(["validate", os.path.join(DATA, "nope_does_not_exist.nc"), "--out", str(tmp_path)])
    assert out.returncode == 1          # 크래시(>1)가 아니라 정상 종료코드 1
    assert "FAIL" in out.stdout or "열" in out.stdout
