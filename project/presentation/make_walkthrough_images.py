"""시연 PPT용 이미지 — 구현용어 없이 평이하게.
- inventory_plain.png : 폴더 자동 정리 표 (모델/관측/역할, 쉬운 말)
- wave_result.png     : 검증 결과 3축 그림 (results/에서 복사)
"""
import os, shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)

TEAL = "#0E7C86"; INK = "#17313A"; MUTE = "#5B7185"


def inventory_plain():
    rows = [
        ["파랑모델 출력 (5일치)", "모델 격자자료", "검증 대상"],
        ["해양 부이 관측", "지점 관측자료", "비교 기준"],
        ["기상 재분석·예보 자료", "기상자료", "이번엔 미사용"],
    ]
    cols = ["폴더에서 찾은 자료", "자료 종류", "역할"]
    fig, ax = plt.subplots(figsize=(8.6, 2.5), dpi=150)
    ax.axis("off")
    t = ax.table(cellText=rows, colLabels=cols, cellLoc="left", loc="center",
                 colWidths=[0.42, 0.30, 0.28])
    t.auto_set_font_size(False); t.set_fontsize(13); t.scale(1, 2.0)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#D5DEE6")
        if r == 0:
            cell.set_facecolor(TEAL); cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#FFFFFF" if r % 2 else "#EEF6F6")
            if c == 2:
                cell.set_text_props(color=TEAL if "검증" in rows[r-1][2] or "기준" in rows[r-1][2] else MUTE,
                                    fontweight="bold")
    p = os.path.join(ASSETS, "inventory_plain.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("wrote", p)


def copy_result():
    src = "/Users/yoh/Projects/geosr_hackathon/results/hs_validation_5day.png"
    dst = os.path.join(ASSETS, "wave_result.png")
    if os.path.exists(src):
        shutil.copy(src, dst); print("copied", dst)
    else:
        print("[skip] 결과 그림 없음:", src)


if __name__ == "__main__":
    inventory_plain(); copy_result(); print("done.")
