# -*- coding: utf-8 -*-
"""
生成第四章图: 重复攻击的平均尝试次数及防御广度（哑铃图）
为了替代或补充表 4.19 (tab:repeated_attempts)
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
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 12,
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

def fig_dumbbell_repeated_attempts():
    # 数据：表 4.19
    models = ["AlpaCare", "Asclepius", "BioMistral", "BioLlama3", "Llama2", "Llama3"]
    # 翻转顺序以便图的上面是第一个模型（或者将 Llama3 放最上，看视觉效果，一般 AlpaCare 放在最上比较顺序）
    models = models[::-1]
    
    data = {
        "AlpaCare":  {"succ": 1.56,  "all": 1.56},
        "Asclepius": {"succ": 28.90, "all": 47.21},
        "BioMistral":{"succ": 16.35, "all": 23.05},
        "BioLlama3": {"succ": 22.47, "all": 58.63},
        "Llama2":    {"succ": 13.27, "all": 71.38},
        "Llama3":    {"succ": 35.82, "all": 82.14},
    }
    
    t_succ = [data[m]["succ"] for m in models]
    t_all = [data[m]["all"] for m in models]
    
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    
    # 颜色设定：学术配色的经典对比色
    # 采用 seaborn muted 类似色系
    color_succ = "#DD8452" # 橙红色系，代表被攻破所需次数（相对较短）
    color_all = "#4C72B0"  # 蓝色系，代表整体防线（探索上限）
    color_line = "#B0B0B0" # 灰色连线
    
    y = np.arange(len(models))
    
    # 画哑铃线
    for i in range(len(models)):
        ax.plot([t_succ[i], t_all[i]], [y[i], y[i]], color=color_line, linestyle="-", linewidth=2.5, zorder=1)
        
    # 画两侧的数据点
    ax.scatter(t_succ, y, color=color_succ, s=100, zorder=2, label="成功样本平均次数 ($T_{\mathrm{succ}}$)")
    ax.scatter(t_all, y, color=color_all, s=100, zorder=2, label="所有样本平均次数 ($T_{\mathrm{all}}$)")
    
    # 添加数值标签与 Delta 标注
    for i in range(len(models)):
        delta = t_all[i] - t_succ[i]
        
        # 当只有一点也就是 Delta = 0 时，或者两者极近避免数字重叠
        if delta < 0.1:
            # 成功点数字
            ax.text(t_succ[i] - 1.5, y[i], f"{t_succ[i]:.1f}", color=color_succ, 
                    ha='right', va='center', fontsize=10, fontfamily="Times New Roman", fontweight='bold')
            # All点数字
            ax.text(t_all[i] + 1.5, y[i], f"{t_all[i]:.1f}", color=color_all, 
                    ha='left', va='center', fontsize=10, fontfamily="Times New Roman", fontweight='bold')
            # 标注 Delta
            ax.text(t_succ[i], y[i] + 0.15, f"\u0394=0.0", color="#555555",
                    ha='center', va='bottom', fontsize=10, fontfamily="Times New Roman")
        else:
            # 成功点数字
            ax.text(t_succ[i] - 1.5, y[i], f"{t_succ[i]:.1f}", color=color_succ, 
                    ha='right', va='center', fontsize=10, fontfamily="Times New Roman", fontweight='bold')
            # All点数字
            ax.text(t_all[i] + 1.5, y[i], f"{t_all[i]:.1f}", color=color_all, 
                    ha='left', va='center', fontsize=10, fontfamily="Times New Roman", fontweight='bold')
            # 标注 Delta
            mid_x = (t_succ[i] + t_all[i]) / 2
            ax.text(mid_x, y[i] + 0.12, f"\u0394={delta:.1f}", color="#555555",
                    ha='center', va='bottom', fontsize=10, fontfamily="Times New Roman")
    
    ax.set_yticks(y)
    ax.set_yticklabels(models, fontfamily="Times New Roman", fontsize=13)
    ax.set_xlabel("平均尝试次数 (次)", fontsize=13)
    ax.set_ylabel("测试模型", fontsize=13)
    
    # 横坐标（x轴）刻度数字使用 Times New Roman
    for tick in ax.get_xticklabels():
        tick.set_fontfamily('Times New Roman')
    
    # 图例（使用 Times New Roman 处理英文，全局处理中文） - 移动到右上角
    legend = ax.legend(loc="upper right", frameon=False, fontsize=11)
    for text in legend.get_texts():
        label_text = text.get_text()
        if any('\u4e00' <= c <= '\u9fff' for c in label_text):
            text.set_fontfamily(['SimSun', 'Times New Roman'])
        else:
            text.set_fontfamily('Times New Roman')
            
    # 增加 x 轴范围以容纳标签
    ax.set_xlim(-15, 95)
    
    # 去除多余的边框线
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # 增加横向网格线，辅助对齐
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    path_pdf = os.path.join(OUT_DIR, "Fig4-dumbbell-repeated-attempts.pdf")
    path_png = os.path.join(OUT_DIR, "Fig4-dumbbell-repeated-attempts.png")
    fig.savefig(path_pdf)
    fig.savefig(path_png)
    plt.close(fig)
    print(f"[OK] {path_pdf}")

if __name__ == "__main__":
    fig_dumbbell_repeated_attempts()
