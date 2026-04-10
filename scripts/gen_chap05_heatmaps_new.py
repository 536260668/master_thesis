# -*- coding: utf-8 -*-
"""
基于补做实验的数据生成第五章热力图：
  图1: 数据投毒攻击级联ASR热力图 (a)10% (b)50%     -> Fig5-poison-heatmap-new.pdf
  图2: 提示词攻击级联ASR热力图   (a)PAA  (b)越狱    -> Fig5-prompt-heatmap-new.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------- 全局学术规范样式 ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["SimSun", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 1.0,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

configs_order = [
    "gggg",
    "bggg", "gbgg", "ggbg", "gggb",
    "bbgg", "bgbg", "bggb", "gbbg", "gbgb", "ggbb",
    "gbbb", "bgbb", "bbgb", "bbbg",
    "bbbb",
]

group_lines = [0.5, 4.5, 10.5, 14.5]

# ========== 数据替换为补做实验的结果 (从 新建 Microsoft Excel 工作表.csv 整理) ==========

jailbreak = {
    "gggg": [5, 7, 6, 8],
    "gggb": [5, 7, 6, 88],
    "ggbg": [5, 7, 94, 91],
    "gbgg": [5, 86, 83, 85],
    "bggg": [90, 81, 84, 85],
    "ggbb": [5, 7, 94, 95],
    "gbgb": [5, 86, 83, 92],
    "gbbg": [5, 86, 95, 92],
    "bggb": [90, 81, 84, 93],
    "bgbg": [90, 81, 94, 92],
    "bbgg": [90, 94, 92, 92],
    "gbbb": [5, 86, 95, 95],
    "bgbb": [90, 81, 94, 95],
    "bbgb": [90, 94, 92, 93],
    "bbbg": [90, 94, 94, 93],
    "bbbb": [90, 94, 94, 96],
}

poison_10 = {
    "gggg": [5, 7, 6, 8],
    "gggb": [5, 7, 6, 20],
    "ggbg": [5, 7, 21, 25],
    "gbgg": [5, 20, 19, 19],
    "bggg": [14, 16, 18, 19],
    "ggbb": [5, 7, 21, 30],
    "gbgb": [5, 20, 19, 29],
    "gbbg": [5, 20, 23, 28],
    "bggb": [14, 16, 18, 30],
    "bgbg": [14, 16, 26, 27],
    "bbgg": [14, 19, 23, 23],
    "gbbb": [5, 20, 23, 33],
    "bgbb": [14, 16, 26, 29],
    "bbgb": [14, 19, 23, 30],
    "bbbg": [14, 19, 22, 25],
    "bbbb": [14, 19, 22, 33],
}

poison_50 = {
    "gggg": [5, 7, 6, 8],
    "gggb": [5, 7, 6, 71],
    "ggbg": [5, 7, 72, 70],
    "gbgg": [5, 65, 68, 67],
    "bggg": [69, 69, 69, 68],
    "ggbb": [5, 7, 72, 71],
    "gbgb": [5, 65, 68, 69],
    "gbbg": [5, 65, 73, 68],
    "bggb": [69, 69, 69, 71],
    "bgbg": [69, 69, 70, 66],
    "bbgg": [69, 75, 73, 70],
    "gbbb": [5, 65, 73, 73],
    "bgbb": [69, 69, 70, 71],
    "bbgb": [69, 75, 73, 71],
    "bbbg": [69, 75, 77, 76],
    "bbbb": [69, 75, 77, 77],
}

paa = {
    "gggg": [5, 7, 6, 8],
    "gggb": [5, 7, 6, 82],
    "ggbg": [5, 7, 82, 80],
    "gbgg": [5, 81, 80, 79],
    "bggg": [72, 69, 66, 66],
    "ggbb": [5, 7, 82, 82],
    "gbgb": [5, 81, 80, 83],
    "gbbg": [5, 81, 76, 76],
    "bggb": [72, 69, 66, 78],
    "bgbg": [72, 69, 77, 76],
    "bbgg": [72, 85, 83, 83],
    "gbbb": [5, 81, 76, 84],
    "bgbb": [72, 69, 77, 80],
    "bbgb": [72, 85, 83, 80],
    "bbbg": [72, 85, 79, 79],
    "bbbb": [72, 85, 79, 85],
}

agent_labels = ["A1", "A2", "A3", "A4"]

def build_matrix(data_dict):
    mat = np.zeros((len(configs_order), 4))
    for i, cfg in enumerate(configs_order):
        mat[i, :] = np.array(data_dict[cfg]) * 100.0 / 96.0
    return mat

def draw_subplot(ax, mat, subtitle):
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(np.arange(4))
    ax.set_xticklabels(agent_labels, fontfamily="Times New Roman", fontsize=14)
    ax.set_yticks(np.arange(len(configs_order)))
    ax.set_yticklabels(configs_order, fontfamily="Times New Roman", fontsize=13)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    for y in group_lines:
        ax.axhline(y, color="gray", linestyle="--", linewidth=1.0)
    for i in range(len(configs_order)):
        for j in range(4):
            v = mat[i, j]
            color = "white" if v > 50 else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=12, color=color, fontfamily="Times New Roman")
    ax.set_title(subtitle, fontsize=16, pad=32)
    return im

def plot_figure(data_left, data_right, subtitle_left, subtitle_right, filename):
    mat_left = build_matrix(data_left)
    mat_right = build_matrix(data_right)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 7.8))
    im1 = draw_subplot(ax1, mat_left, subtitle_left)
    im2 = draw_subplot(ax2, mat_right, subtitle_right)
    ax1.set_ylabel("智能体配置", fontsize=16)
    ax2.set_ylabel("智能体配置", fontsize=16)
    cbar_ax = fig.add_axes([0.3, 0.15, 0.4, 0.04])
    cbar = fig.colorbar(im2, cax=cbar_ax, orientation="horizontal")
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label("攻击成功率（%）", labelpad=8, fontsize=16)
    fig.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.25, wspace=0.25)
    path_pdf = os.path.join(OUT_DIR, filename + ".pdf")
    path_png = os.path.join(OUT_DIR, filename + ".png")
    fig.savefig(path_pdf)
    fig.savefig(path_png)
    plt.close(fig)
    print(f"[OK] {path_pdf}")

if __name__ == "__main__":
    plot_figure(poison_10, poison_50,
                r"$\mathrm{(a)}$ $10\%$ 投毒比例", r"$\mathrm{(b)}$ $50\%$ 投毒比例",
                "Fig5-poison-heatmap-new")
    plot_figure(paa, jailbreak,
                r"$\mathrm{(a)}$ $\mathrm{PAA}$ 攻击", r"$\mathrm{(b)}$ 越狱攻击",
                "Fig5-prompt-heatmap-new")
    print("\n[顺利完成] 第五章热力图已生成。")
