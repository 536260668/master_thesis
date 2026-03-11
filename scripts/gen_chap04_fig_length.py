# -*- coding: utf-8 -*-
"""
生成第四章: 三种攻击在不同提示词长度下的 ASR (3行1列折线图)
包含: HackAPrompt / 忽略指令 / 转义字符
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
import numpy as np
import os

# ---------- 全局学术规范样式 ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["SimSun", "Times New Roman", "DejaVu Serif"],
    "axes.unicode_minus": False,
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 1.0,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

def fig_prompt_length_3subplots():
    lengths = ["短文本\n(10-20)", "中等文本\n(21-50)", "长文本\n(51-100)", "超长文本\n(>100)"]
    x = np.arange(len(lengths))

    # ----- 数据 -----
    # 对应的表 4.14 HackAPrompt
    hack = {
        "AlpaCare":  [52.74, 55.31, 60.58, 63.42],
        "Asclepius": [44.86, 47.23, 52.84, 55.18],
        "BioMistral":[36.85, 39.27, 43.56, 47.24],
        "BioLlama3": [14.73, 16.82, 19.34, 21.15],
        "Llama2":    [ 8.76, 10.23, 13.58, 15.35],
        "Llama3":    [ 3.82,  5.14,  6.73,  8.27],
    }
    # 对应的表 4.15 忽略指令
    ignore = {
        "AlpaCare":  [83.24, 77.68, 74.15, 66.81],
        "Asclepius": [72.85, 66.34, 61.27, 56.62],
        "BioMistral":[54.36, 50.78, 44.25, 39.57],
        "BioLlama3": [27.86, 24.15, 19.83, 16.38],
        "Llama2":    [20.74, 17.36, 13.82,  9.16],
        "Llama3":    [12.86, 10.18,  7.85,  5.14],
    }
    # 对应的表 4.16 转义字符
    escape = {
        "AlpaCare":  [99.86, 99.73, 97.26, 92.85],
        "Asclepius": [97.24, 94.86, 91.35, 86.71],
        "BioMistral":[87.63, 84.82, 79.54, 75.17],
        "BioLlama3": [35.74, 32.28, 28.13, 24.16],
        "Llama2":    [27.82, 23.68, 19.17, 14.24],
        "Llama3":    [15.76, 12.83,  9.54,  6.95],
    }

    models = ["AlpaCare", "Asclepius", "BioMistral", "BioLlama3", "Llama2", "Llama3"]
    # 颜色与标记 (取多样化色系)
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
    markers = ["o", "s", "^", "D", "v", "p"]
    
    # 改变图的排布：3行1列的竖直排列以便在版面有限时展示清晰，加减 figsize
    fig, axes = plt.subplots(3, 1, figsize=(8, 14))

    titles = ["(a) HackAPrompt", "(b) 忽略指令", "(c) 转义字符"]
    datasets = [hack, ignore, escape]
    
    for k, (ax, data_dict, title) in enumerate(zip(axes, datasets, titles)):
        for i, m_name in enumerate(models):
            arr = data_dict[m_name]
            c = colors[i]
            m = markers[i]
            ax.plot(x, arr, marker=m, color=c, linestyle="-", linewidth=2.5, 
                     markersize=9, markeredgecolor='white', markeredgewidth=1.2, label=m_name)
            
            # 添加每个点数值，使用白色描边防止重叠时不清晰
            for j, val in enumerate(arr):
                # 为防止在最顶端的点数值出界，当数值较高时标在下侧
                y_offset = 1.5 if val < 90 else -3.0
                va = "bottom" if val < 90 else "top"
                
                # 微调某些特定重叠：
                if title == "(b) 忽略指令" and j == 1 and m_name == "Asclepius": # 66.34 vs AlpaCare 77.68，在下方比较好
                    pass
                    
                ax.text(j, val + y_offset, f"{val:.1f}", ha="center", va=va,
                        fontsize=11, fontfamily="Times New Roman", color=c,
                        path_effects=[withStroke(linewidth=2.5, foreground="white")])
            
        ax.set_xticks(x)
        # 只有在最下面一张图才显示 x 轴的 label 文字
        if k == 2:
            ax.set_xticklabels(lengths)
            ax.set_xlabel("提示词长度区间", labelpad=10)
        else:
            ax.set_xticklabels([])
            
        ax.set_title(title, pad=10)
        ax.set_ylabel("攻击成功率 (%)")
        ax.set_ylim(-3, 115)  # 留出顶部文字空间
        ax.set_yticks(np.arange(0, 101, 20))
        # 去除横向虚线
        ax.grid(False) 
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
    # 图例放在整体上方，使用 3 列布局以免过长
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, frameon=False, prop={'family': 'Times New Roman', 'size': 13})
    
    plt.tight_layout()
    # 调整布局以为上方的图例留出空间，同时缩小多子图间的间距
    plt.subplots_adjust(top=0.94, hspace=0.15)
    
    path_pdf = os.path.join(OUT_DIR, "Fig4-prompt-length-3subplots.pdf")
    path_png = os.path.join(OUT_DIR, "Fig4-prompt-length-3subplots.png")
    fig.savefig(path_pdf, bbox_inches="tight")
    fig.savefig(path_png, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ 生成成功 -> {path_pdf}")

if __name__ == "__main__":
    fig_prompt_length_3subplots()
