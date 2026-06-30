"""test_waves_broken.py: QC 결함 fixture 존재·열림·run_qc FAIL 검증.

검증 항목:
  1. data/ww3_broken.nc, data/buoy_broken.csv 파일 존재
  2. 두 파일이 정상적으로 열림 (open_dataset / pd.read_csv cp949)
  3. ww3_broken → run_qc 결과 ok==False && value_range FAIL 포함
"""
from __future__ import annotations

import os
import sys

import pandas as pd
import pytest

# ── 경로 설정 ──────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = os.path.join(_ROOT, "scripts")
_DATA = os.path.join(_ROOT, "data")

if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from io_detect import open_dataset   # noqa: E402
from qc import run_qc                # noqa: E402

WW3_BROKEN = os.path.join(_DATA, "ww3_broken.nc")
BUOY_BROKEN = os.path.join(_DATA, "buoy_broken.csv")


# ── fixture 파일 존재·열림 ─────────────────────────────────────────────

class TestBrokenFixtureFiles:
    def test_ww3_broken_exists(self):
        assert os.path.isfile(WW3_BROKEN), f"파일 없음: {WW3_BROKEN}"

    def test_buoy_broken_exists(self):
        assert os.path.isfile(BUOY_BROKEN), f"파일 없음: {BUOY_BROKEN}"

    def test_ww3_broken_opens(self):
        """open_dataset 으로 열고 data_var_names 반환 확인."""
        d = open_dataset(WW3_BROKEN)
        assert d is not None
        names = d.data_var_names()
        assert len(names) > 0, "data_var_names() 가 빈 리스트"
        # 핵심 변수 존재 확인
        assert "hs" in names
        assert "uwnd" in names

    def test_buoy_broken_opens_cp949(self):
        """cp949 인코딩으로 CSV 열기 + 한글 컬럼 확인."""
        df = pd.read_csv(BUOY_BROKEN, encoding="cp949")
        assert len(df) > 0
        assert "유의파고" in df.columns

    def test_buoy_broken_has_anomalies(self):
        """주입한 결함값(50 m, -1.5 m)이 실제로 존재하는지 확인."""
        df = pd.read_csv(BUOY_BROKEN, encoding="cp949")
        vals = df["유의파고"].dropna().tolist()
        assert 50.0 in vals, "50 m 비정상치 없음"
        assert -1.5 in vals, "-1.5 m 음수 파고 없음"

    def test_buoy_broken_has_missing(self):
        """NaN 주입 확인."""
        df = pd.read_csv(BUOY_BROKEN, encoding="cp949")
        assert df["유의파고"].isna().sum() >= 2, "결측치 2개 미만"


# ── ww3_broken run_qc 결과 검증 ─────────────────────────────────────────

class TestWw3BrokenQC:
    def setup_method(self):
        self.d = open_dataset(WW3_BROKEN)
        self.result = run_qc(self.d)

    def test_qc_not_ok(self):
        """결함 데이터: run_qc 는 ok==False 를 반환해야 함."""
        assert self.result["ok"] is False, (
            f"ok==True 가 나왔음. summary={self.result['summary']}"
        )

    def test_value_range_fail_present(self):
        """값범위 FAIL 항목이 하나 이상 존재해야 함.

        uwnd(200 m/s) → wind_component 규칙(valid_max=120) → FAIL 기대.
        """
        fails = [
            c for c in self.result["checks"]
            if c["check"] == "value_range" and c["status"] == "FAIL"
        ]
        assert len(fails) > 0, (
            "value_range FAIL 없음.\n"
            "checks:\n" + "\n".join(
                f"  {c['check']} | {c.get('variable','?')} | {c['status']} | {c['evidence'][:80]}"
                for c in self.result["checks"]
            )
        )

    def test_summary_has_fail(self):
        """summary['FAIL'] 이 양수여야 함."""
        assert self.result["summary"].get("FAIL", 0) > 0, (
            f"summary={self.result['summary']}"
        )

    def test_hs_has_nan_in_dataset(self):
        """주입한 NaN 이 NetCDF에 실제로 저장됐는지 확인."""
        import numpy as np
        hs = self.d.xr["hs"].values
        assert np.isnan(hs).any(), "hs 에 NaN 없음 — 결측 주입 실패"

    def test_hs_has_extreme_value(self):
        """주입한 99 m 값이 NetCDF에 실제로 저장됐는지 확인."""
        import numpy as np
        hs = self.d.xr["hs"].values
        valid = hs[np.isfinite(hs)]
        assert float(valid.max()) > 90.0, (
            f"hs 최댓값 {float(valid.max()):.1f} — 99 m 주입 실패"
        )

    def test_uwnd_has_extreme_value(self):
        """주입한 200 m/s 가 NetCDF에 저장됐는지 확인."""
        import numpy as np
        uwnd = self.d.xr["uwnd"].values
        assert float(uwnd.max()) > 150.0, (
            f"uwnd 최댓값 {float(uwnd.max()):.1f} — 극단치 주입 실패"
        )
