# -*- coding: utf-8 -*-
"""
生成第五章错误放大因子 α 随位置变化趋势图：
  图5-Y 错误放大因子 α 随位置变化趋势 -> Fig5-alpha-trend.pdf
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
    "font.size": 14,
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

# 数据定义 (由 scripts/calc_all_alphas.py 计算得到)
# poison_10: 原数据 [2.33, 2.38, 5.50, 2.33]
alpha_10 = [2.80, 2.71, 3.67, 4.12]
# poison_50: 原数据 [11.50, 9.38, 19.25, 8.44]
alpha_50 = [13.80, 10.71, 12.83, 9.62]
# paa: 原数据 [12.00, 8.50, 8.78, 8.50]
alpha_paa = [14.40, 12.14, 13.17, 10.62]
# jailbreak: 原数据 [17.40, 10.00, 15.17, 9.10]
alpha_jb = [18.00, 13.43, 15.67, 12.00]

labels = ["$\\alpha_1$", "$\\alpha_2$", "$\\alpha_3$", "$\\alpha_4$"]
x = np.arange(len(labels))

def plot_alpha_trend():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 颜色与标记 (学术配色)
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"] # 蓝、橙、绿、红
    markers = ['o', 's', '^', 'D']
    l_styles = ['-', '-', '-', '-'] # 全部使用实线
    
    # 绘图数据
    data_list = [
        (alpha_10, "10% 投毒攻击", colors[0], markers[0]),
        (alpha_50, "50% 投毒攻击", colors[1], markers[1]),
        (alpha_paa, "提示词攻击", colors[2], markers[2]),
        (alpha_jb, "越狱攻击", colors[3], markers[3])
    ]
    
    for i, (vals, label, color, marker) in enumerate(data_list):
        ax.plot(x, vals, marker=marker, markersize=8, linewidth=2, label=label, 
                color=color, markeredgecolor='white', markeredgewidth=1.2, 
                linestyle=l_styles[i], zorder=10-i)
        
        # 标注数值 (根据用户反馈进行精细位置调整)
        for j, val in enumerate(vals):
            # 默认值
            v_offset = 0.5
            h_offset = 0
            ha = "center"
            va = "bottom"
            
            # 1. 10% 攻击 (i=0) 统一居中偏下
            if i == 0:
                v_offset = -1.4
            
            # 2. 50% 攻击 (i=1)
            elif i == 1:
                if j == 1: # 第二个点 (a2) 放在点正下
                    v_offset = -1.4 
                    va = "bottom"
                elif j == 2: # 第三个点 (a3) 放在点正下
                    v_offset = -1.4
                    va = "bottom"
                elif j == 0: # 第1个点 (a1) 放在点正下
                    v_offset = -1.4
                    va = "bottom"
                elif j == 3: # 最后一个点 (a4) 放在点正下
                    v_offset = -1.4
                    va = "bottom"

            # 3. 提示词攻击 (i=2)
            elif i == 2:
                if j == 1: # 第二个点 (a2) 放在点上面一点点位置，往下移一点点并向右偏移
                    v_offset = 0.4
                    h_offset = 0.08
                    ha = "left"
                elif j == 3: # 最后一个点 (a4) 放在正右 (稍微靠左一点)
                    v_offset = -0.3
                    h_offset = 0.08 # 减小偏移量以对齐
                    ha = "left"

            # 4. 越狱攻击 (i=3)
            elif i == 3:
                if j == 1: # a2 位置偏移避免重叠
                    v_offset = 0.6
                elif j == 3: # 最后一个点 (a4) 放在正上
                    v_offset = 0.6
            
            ax.text(j + h_offset, val + v_offset, f"{val:.1f}", ha=ha, va=va, 
                    fontsize=12, fontfamily="Times New Roman", color=color, fontweight='bold')
    
    # 设置坐标轴
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontfamily="Times New Roman", fontsize=16)
    ax.set_ylabel("错误放大因子 ($\\alpha$)", fontsize=16)
    ax.set_xlabel("智能体链位置", fontsize=16)
    
    # 坐标范围与刻度
    ax.set_ylim(-2, 22)
    ax.set_yticks(np.arange(0, 21, 4))
    
    # 增加一条 alpha=1 的基准线 (Baseline)
    ax.axhline(y=1, color='gray', linestyle=':', linewidth=1, alpha=0.8, zorder=1)
    # 文字修改为黑色，字体 Times New Roman，放到线下方 (y=0.2)
    # 计算右对齐位置: a4(3.0) + h_offset(0.08) + 估计文字宽度(0.18) ≈ 3.26
    ax.text(3.26, 0.2, "Baseline (1.0)", color='black', fontsize=12, ha='right', fontfamily='Times New Roman')
    
    # 移除上方和右侧边框 (学术规范)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 图例 (改为一行)
    legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=4, frameon=False,
                       prop={'family': 'SimSun', 'size': 14})
    
    # 调整布局
    plt.tight_layout()
    
    # 保存
    path_pdf = os.path.join(OUT_DIR, "Fig5-alpha-trend_new.pdf")
    path_png = os.path.join(OUT_DIR, "Fig5-alpha-trend_new.png")
    fig.savefig(path_pdf)
    fig.savefig(path_png)
    plt.close(fig)
    print(f"[OK] {path_pdf}")

if __name__ == "__main__":
    plot_alpha_trend()
    print("\n[顺利完成] 错误放大因子趋势图已生成。")
