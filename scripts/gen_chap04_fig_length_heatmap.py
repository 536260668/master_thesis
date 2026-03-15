# -*- coding: utf-8 -*-
"""
生成第四章: 三种攻击在不同提示词长度下的 ASR (全局热力图版)
布局: 第一行两个，第二行一个居中
包含: HackAPrompt / 忽略指令 / 转义字符
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.gridspec as gridspec

# ---------- 全局学术规范样式 ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["SimSun", "Times New Roman", "DejaVu Serif"],
    "axes.unicode_minus": False,
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "mathtext.fontset": "stix",
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 1.0,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

def fig_prompt_length_heatmap():
    lengths = ["短", "中等", "长", "超长"]
    models = ["AlpaCare", "Asclepius", "BioMistral", "BioLlama3", "Llama2", "Llama3"]

    hack = np.array([
        [52.74, 55.31, 60.58, 63.42],
        [44.86, 47.23, 52.84, 55.18],
        [36.85, 39.27, 43.56, 47.24],
        [14.73, 16.82, 19.34, 21.15],
        [ 8.76, 10.23, 13.58, 15.35],
        [ 3.82,  5.14,  6.73,  8.27],
    ])
    ignore = np.array([
        [83.24, 77.68, 74.15, 66.81],
        [72.85, 66.34, 61.27, 56.62],
        [54.36, 50.78, 44.25, 39.57],
        [27.86, 24.15, 19.83, 16.38],
        [20.74, 17.36, 13.82,  9.16],
        [12.86, 10.18,  7.85,  5.14],
    ])
    escape = np.array([
        [99.86, 99.73, 97.26, 92.85],
        [97.24, 94.86, 91.35, 86.71],
        [87.63, 84.82, 79.54, 75.17],
        [35.74, 32.28, 28.13, 24.16],
        [27.82, 23.68, 19.17, 14.24],
        [15.76, 12.83,  9.54,  6.95],
    ])

    # 布局: 第一行两个 第二行一个居中
    # 将原来的 (10, 7.5) 宽度进一步压缩至 (8.5, 7.5)，使得色块更接近正方形
    fig = plt.figure(figsize=(8.5, 7.5))
    # 调整 wspace 和 hspace 减小间距
    gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, 0:2])
    ax2 = fig.add_subplot(gs[0, 2:4])
    ax3 = fig.add_subplot(gs[1, 1:3])
    
    axes = [ax1, ax2, ax3]
    datasets = [hack, ignore, escape]
    # 使用 stix (类 Times New Roman) 数学字体包含英文字符
    titles = [r"$\mathrm{(a)HackAPrompt}$", r"$\mathrm{(b)}$忽略指令", r"$\mathrm{(c)}$转义字符"]
    
    im = None
    for k, (ax, data, title) in enumerate(zip(axes, datasets, titles)):
        im = ax.imshow(data, cmap="YlOrRd", aspect="auto", vmin=0, vmax=100)
        
        # 去除额外的网格线
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(which="major", bottom=False, left=False)
        
        ax.set_xticks(np.arange(len(lengths)))
        ax.set_yticks(np.arange(len(models)))
        
        ax.set_xticklabels(lengths, fontsize=11)
        # 只在第一列(a)和第二行(c)显示 Y 轴模型名称，(b)隐藏名字以免拥挤
        if k == 0 or k == 2:
            ax.set_yticklabels(models, fontfamily="Times New Roman", fontsize=11)
            ax.set_ylabel("待测模型", fontsize=12)
        else:
            ax.set_yticklabels([])
            
        t_obj = ax.set_title(title, pad=10, fontsize=12)
        # 用 LaTeX math font 获取纯正的英文字体（受设定的 mathtext.fontset=stix 控制）
        # SimSun 优先支持中文字符
        t_obj.set_fontfamily(['SimSun', 'Times New Roman'])
        
        ax.set_xlabel("提示词长度区间", fontsize=12, labelpad=8)

        # 标注数值
        for i in range(len(models)):
            for j in range(len(lengths)):
                v = data[i, j]
                # YlGnBu 中颜色较深通常代表数值较高，数值大于 50 时用白色
                color = "white" if v > 50 else "black"
                ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                        fontsize=11, color=color, fontfamily="Times New Roman")

    # 全局 Colorbar 布局优化
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.1, top=0.92)
    # 稍微缩短 colorbar，并向左移近一点以适应变窄的画布
    cbar_ax = fig.add_axes([0.88, 0.2, 0.02, 0.6]) # [left, bottom, width, height]
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.ax.tick_params(labelsize=11)
    cbar.set_label("攻击成功率 (%)", labelpad=10, fontsize=12)

    path_pdf = os.path.join(OUT_DIR, "Fig4-prompt-length-heatmap.pdf")
    path_png = os.path.join(OUT_DIR, "Fig4-prompt-length-heatmap.png")
    fig.savefig(path_pdf, bbox_inches="tight")
    fig.savefig(path_png, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ 热力图生成成功 -> {path_pdf}")

if __name__ == "__main__":
    fig_prompt_length_heatmap()
