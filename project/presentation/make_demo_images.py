"""발표 PPT 데모 슬라이드용 이미지 생성 (실제 결과 기반).
- discover_table.png : discover 인벤토리 (실제 분류 결과)
- qc_panel.png       : QC 정상 PASS vs 결함 FAIL (실측)
- wave_validation.png : 파랑 3축 검증 그림 (results/에서 복사)
좌표·실측 raw 미포함(파일명·도메인·지표만). AppleGothic으로 한글 렌더.
"""
import os, shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)

NAVY = "#11233F"; DEEP = "#0A5078"; TEAL = "#1C7293"
PASS = "#1E8449"; FAIL = "#C0392B"; INK = "#16263B"; MUTE = "#5B7185"

# ── 1. discover 인벤토리 표 ──
def discover_table():
    rows = [
        ["geo_ww3_anal_2024091*.nc", "netcdf4", "mesh", "waves", "model"],
        ["OBS_BUOY_TIM_2024.csv", "csv (cp949)", "점·지점ID", "waves*", "reference"],
        ["era5_rean_..._20220906.nc", "netcdf3", "1d", "meteorology", "reference"],
        ["gfs_fcst_..._20220906.nc", "netcdf4", "2d", "meteorology", "model"],
    ]
    cols = ["파일", "포맷", "좌표", "도메인", "역할추정"]
    fig, ax = plt.subplots(figsize=(8.6, 3.0), dpi=150)
    ax.axis("off")
    ax.set_title("$ python cli.py discover  project/data/", loc="left",
                 fontsize=13, color=DEEP, fontweight="bold", family="DejaVu Sans Mono", pad=12)
    t = ax.table(cellText=rows, colLabels=cols, cellLoc="left", loc="center",
                 colWidths=[0.34, 0.16, 0.16, 0.20, 0.16])
    t.auto_set_font_size(False); t.set_fontsize(11); t.scale(1, 1.7)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#D5DEE6")
        if r == 0:
            cell.set_facecolor(DEEP); cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#FFFFFF" if r % 2 else "#F4F7FA")
            if c == 3:  # 도메인
                txt = rows[r-1][3]
                cell.set_text_props(color=TEAL if "wave" in txt else INK, fontweight="bold")
    fig.text(0.5, 0.02, "포맷·좌표(mesh/1d/2d)·도메인·역할을 자동 분류 · 부이 cp949 한글 자동 인식",
             ha="center", fontsize=9.5, color=MUTE)
    fig.tight_layout()
    p = os.path.join(ASSETS, "discover_table.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("wrote", p)

# ── 2. QC 정상/결함 패널 ──
def qc_panel():
    fig, ax = plt.subplots(figsize=(8.6, 3.0), dpi=150)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    # 정상
    ax.add_patch(FancyBboxPatch((0.2, 0.4), 4.5, 5.2, boxstyle="round,pad=0.1",
                 fc="#EAF3EE", ec=PASS, lw=1.6))
    ax.text(2.45, 5.0, "validate  정상본", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(2.45, 3.9, "PASS", ha="center", fontsize=34, color=PASS, fontweight="bold")
    ax.text(2.45, 2.9, "12 / 12 체크 통과", ha="center", fontsize=12, color=INK)
    ax.text(2.45, 1.9, "값범위·결측·격자·이상치·시간", ha="center", fontsize=10, color=MUTE)
    ax.text(2.45, 1.1, "전부 정상", ha="center", fontsize=10, color=MUTE)
    # 결함
    ax.add_patch(FancyBboxPatch((5.3, 0.4), 4.5, 5.2, boxstyle="round,pad=0.1",
                 fc="#FBEDEC", ec=FAIL, lw=1.6))
    ax.text(7.55, 5.0, "validate  결함본", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.text(7.55, 3.95, "FAIL", ha="center", fontsize=34, color=FAIL, fontweight="bold")
    for i, line in enumerate(["• 값범위: t2m 500K (9개)",
                              "• 격자: 위도 비단조",
                              "• 이상치: u10 999"]):
        ax.text(5.65, 2.95 - i*0.72, line, ha="left", fontsize=11.5, color=INK)
    ax.text(7.55, 0.62, "각 결함을 근거와 함께 적발", ha="center", fontsize=9.5, color=MUTE)
    p = os.path.join(ASSETS, "qc_panel.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("wrote", p)

def copy_wave():
    src = os.path.abspath(os.path.join(HERE, "..", "..", "results", "hs_validation_3axis_20240915.png"))
    dst = os.path.join(ASSETS, "wave_validation.png")
    if os.path.exists(src):
        shutil.copy(src, dst); print("copied", dst)
    else:
        print("[skip] wave figure 없음:", src)

if __name__ == "__main__":
    discover_table(); qc_panel(); copy_wave()
    print("done.")
