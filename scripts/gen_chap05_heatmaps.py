# -*- coding: utf-8 -*-
"""
生成第五章两张级联ASR热力图（展示全部4个智能体的逐节点ASR）：
  图1: 数据投毒攻击级联ASR热力图 (a)10% (b)50%     -> Fig5-poison-heatmap.pdf
  图2: 提示词攻击级联ASR热力图   (a)PAA  (b)越狱    -> Fig5-prompt-heatmap.pdf
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

# 16种配置的显示顺序（按坏模型数量分组）
configs_order = [
    "gggg",
    "bggg", "gbgg", "ggbg", "gggb",
    "bbgg", "bgbg", "bggb", "gbbg", "gbgb", "ggbb",
    "gbbb", "bgbb", "bbgb", "bbbg",
    "bbbb",
]

# 分组分割线位置（索引 0.5, 4.5, 10.5, 14.5）
group_lines = [0.5, 4.5, 10.5, 14.5]

# ========== 全部 4 智能体 ASR 数据（A1, A2, A3, A4） ==========
# 从 chap5_processed_data.md 提取

poison_10 = {
    "gggg": [6.2, 8.3, 4.2, 9.4],
    "bggg": [14.6, 12.5, 8.3, 9.4],
    "gbgg": [6.2, 20.8, 7.3, 5.2],
    "ggbg": [6.2, 8.3, 27.1, 5.2],
    "gggb": [6.2, 8.3, 4.2, 20.8],
    "bbgg": [14.6, 19.8, 6.2, 5.2],
    "bgbg": [14.6, 12.5, 25.0, 6.2],
    "bggb": [14.6, 12.5, 8.3, 27.1],
    "gbbg": [6.2, 20.8, 15.6, 8.3],
    "gbgb": [6.2, 20.8, 7.3, 21.9],
    "ggbb": [6.2, 8.3, 27.1, 20.8],
    "gbbb": [6.2, 20.8, 15.6, 20.8],
    "bgbb": [14.6, 12.5, 25.0, 16.7],
    "bbgb": [14.6, 19.8, 6.2, 27.1],
    "bbbg": [14.6, 19.8, 22.9, 9.4],
    "bbbb": [14.6, 19.8, 22.9, 21.9],
}

poison_50 = {
    "gggg": [6.2, 8.3, 4.2, 9.4],
    "bggg": [71.9, 4.2, 9.4, 5.2],
    "gbgg": [6.2, 82.3, 5.2, 8.3],
    "ggbg": [6.2, 8.3, 83.3, 5.2],
    "gggb": [6.2, 8.3, 4.2, 80.2],
    "bbgg": [71.9, 78.1, 8.3, 8.3],
    "bgbg": [71.9, 4.2, 84.4, 5.2],
    "bggb": [71.9, 4.2, 9.4, 85.4],
    "gbbg": [6.2, 82.3, 67.7, 4.2],
    "gbgb": [6.2, 82.3, 5.2, 83.3],
    "ggbb": [6.2, 8.3, 83.3, 66.7],
    "gbbb": [6.2, 82.3, 67.7, 81.2],
    "bgbb": [71.9, 4.2, 84.4, 65.6],
    "bbgb": [71.9, 78.1, 8.3, 83.3],
    "bbbg": [71.9, 78.1, 80.2, 5.2],
    "bbbb": [71.9, 78.1, 80.2, 79.2],
}

paa = {
    "gggg": [6.2, 10.4, 9.4, 10.4],
    "bggg": [75.0, 9.4, 18.8, 9.4],
    "gbgg": [6.2, 94.8, 8.3, 14.6],
    "ggbg": [6.2, 10.4, 94.8, 9.4],
    "gggb": [6.2, 10.4, 9.4, 95.8],
    "bbgg": [75.0, 88.5, 13.5, 15.6],
    "bgbg": [75.0, 9.4, 94.8, 9.4],
    "bggb": [75.0, 9.4, 18.8, 93.8],
    "gbbg": [6.2, 94.8, 79.2, 15.6],
    "gbgb": [6.2, 94.8, 8.3, 94.8],
    "ggbb": [6.2, 10.4, 94.8, 78.1],
    "gbbb": [6.2, 94.8, 79.2, 87.5],
    "bgbb": [75.0, 9.4, 94.8, 83.3],
    "bbgb": [75.0, 88.5, 13.5, 93.8],
    "bbbg": [75.0, 88.5, 82.3, 10.4],
    "bbbb": [75.0, 88.5, 82.3, 88.5],
}

jailbreak = {
    "gggg": [5.2, 9.4, 6.2, 10.4],
    "bggg": [90.6, 5.2, 13.5, 6.2],
    "gbgg": [5.2, 84.4, 6.2, 12.5],
    "ggbg": [5.2, 9.4, 85.4, 7.3],
    "gggb": [5.2, 9.4, 6.2, 85.4],
    "bbgg": [90.6, 93.8, 8.3, 14.6],
    "bgbg": [90.6, 5.2, 86.5, 6.2],
    "bggb": [90.6, 5.2, 13.5, 87.5],
    "gbbg": [5.2, 84.4, 89.6, 8.3],
    "gbgb": [5.2, 84.4, 6.2, 85.4],
    "ggbb": [5.2, 9.4, 85.4, 91.7],
    "gbbb": [5.2, 84.4, 89.6, 91.7],
    "bgbb": [90.6, 5.2, 86.5, 88.5],
    "bbgb": [90.6, 93.8, 8.3, 84.4],
    "bbbg": [90.6, 93.8, 94.8, 9.4],
    "bbbb": [90.6, 93.8, 94.8, 94.8],
}

agent_labels = ["A1", "A2", "A3", "A4"]


def build_matrix(data_dict):
    """构建 16×4 的数据矩阵"""
    mat = np.zeros((len(configs_order), 4))
    for i, cfg in enumerate(configs_order):
        mat[i, :] = data_dict[cfg]
    return mat


def draw_subplot(ax, mat, subtitle):
    """在给定的 ax 上绘制一个热力图子图"""
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(np.arange(4))
    ax.set_xticklabels(agent_labels, fontfamily="Times New Roman", fontsize=14)
    ax.set_yticks(np.arange(len(configs_order)))
    ax.set_yticklabels(configs_order, fontfamily="Times New Roman", fontsize=13)

    # x 轴标签放顶部
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # 分组分割线
    for y in group_lines:
        ax.axhline(y, color="gray", linestyle="--", linewidth=1.0)

    # 标注数值
    for i in range(len(configs_order)):
        for j in range(4):
            v = mat[i, j]
            color = "white" if v > 50 else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=12, color=color, fontfamily="Times New Roman")

    ax.set_title(subtitle, fontsize=16, pad=32)
    return im


def plot_figure(data_left, data_right, subtitle_left, subtitle_right, filename):
    """生成一张包含左右两个子图的完整图"""
    mat_left = build_matrix(data_left)
    mat_right = build_matrix(data_right)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 7.8))
    
    im1 = draw_subplot(ax1, mat_left, subtitle_left)
    im2 = draw_subplot(ax2, mat_right, subtitle_right)
 
    # y轴标签
    ax1.set_ylabel("智能体配置", fontsize=16)
    ax2.set_ylabel("智能体配置", fontsize=16)
 
    # 共享色标，横向放置于下方（使用独立的坐标轴以防重叠，位置上移）
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
    # 图1：数据投毒攻击（上: 10%投毒，下: 50%投毒）
    plot_figure(poison_10, poison_50,
                "(a) 10% 投毒比例", "(b) 50% 投毒比例",
                "Fig5-poison-heatmap")

    # 图2：提示词攻击（上: PAA，下: 越狱攻击）
    plot_figure(paa, jailbreak,
                "(a) PAA 攻击", "(b) 越狱攻击",
                "Fig5-prompt-heatmap")

    print("\n[顺利完成] 第五章热力图已重新生成。")
