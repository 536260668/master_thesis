# -*- coding: utf-8 -*-
"""
生成第四章数据投毒攻击实验结果折线图：
  图: 投毒比例 vs ASR -> Fig4-poison-results.pdf
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
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.linewidth": 1.0,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

def fig_poison_results():
    ratios = ["1%", "2%", "5%", "10%"]
    x = np.arange(len(ratios))

    # ----- 数据 (表 4.4) -----
    data = {
        "AlpaCare":  [1.24, 1.48, 8.44, 12.86],
        "BioLlama3": [0.43, 0.79, 2.08, 4.51],
        "BioGPT":    [0.31, 0.58, 1.62, 3.74],
    }

    models = list(data.keys())
    
    # 颜色与标记 (保持之前的学术风格)
    colors = ["#4C72B0", "#55A868", "#DD8452"] 
    markers = ["o", "^", "s"]

    fig, ax = plt.subplots(figsize=(8, 5.5))

    for i, m_name in enumerate(models):
        arr = data[m_name]
        c = colors[i]
        m = markers[i]
        ax.plot(x, arr, marker=m, color=c, linestyle="-", linewidth=2.5, 
                 markersize=9, markeredgecolor='white', markeredgewidth=1.2, label=m_name)
        
        for j, val in enumerate(arr):
            va = "bottom"
            ha = "center"
            y_offset = 0.5
            x_offset = 0
            
            # 手动精调防止文字重叠
            if m_name == "AlpaCare":
                va, y_offset = "bottom", 0.6
                if j == 2:
                    va, ha = "bottom", "right"
                    x_offset = -0.05
            elif m_name == "BioLlama3":
                va, y_offset = "bottom", 0.4
                if j == 0:
                    ha = "left"
                    x_offset = 0.05
                    y_offset = 0.05
                if j == 1:
                    ha = "left"
                    x_offset = 0.05
                    y_offset = 0.2
            elif m_name == "BioGPT":
                va, y_offset = "top", -0.5
                if j == 0:
                    ha = "center"
                    x_offset = 0
                    y_offset = -0.5
                if j == 1:
                    ha = "center"
                    x_offset = 0
                    y_offset = -0.5

            ax.text(j + x_offset, val + y_offset, f"{val:.2f}", ha=ha, va=va, 
                    fontsize=12, fontfamily="Times New Roman", color="black")

    ax.set_xticks(x)
    ax.set_xticklabels(ratios, fontfamily="Times New Roman", fontsize=16)
    ax.set_ylabel("攻击成功率 (%)", fontsize=16)
    ax.set_xlabel("投毒比例", fontsize=16)
    
    legend = ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), frameon=False,
                       prop={'family': 'Times New Roman', 'size': 14})
    
    ax.set_ylim(-1, 15)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "Fig4-poison-results.pdf")
    fig.savefig(path)
    fig.savefig(os.path.join(OUT_DIR, "Fig4-poison-results.png"))
    plt.close(fig)
    print(f"[OK] {os.path.abspath(path)}")

if __name__ == "__main__":
    fig_poison_results()
