# -*- coding: utf-8 -*-
"""
生成第四章三张核心图片（学术论文规范优化版）：
  图1: 六种注入策略 × 六模型 热力图       -> Fig4-strategies-heatmap.pdf
  图2: 提示词长度对攻击效果的影响折线图   -> Fig4-prompt-length.pdf
  图3: 基线 vs AutoDAN 攻击成功率对比     -> Fig4-baseline-vs-autodan.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os, sys

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

# ============================================================
# 图1  六种注入策略对比热力图  (对应表 4.7)
# ============================================================
def fig_strategies_heatmap():
    strategies = ["朴素", "忽略指令", "转义字符", "伪造完成", "HackAPrompt", "组合"]
    models     = ["AlpaCare", "Asclepius", "BioMistral", "BioLlama3", "Llama2", "Llama3"]

    data = np.array([
        [32.14, 25.37, 19.86, 13.72, 10.24,  5.23],
        [75.47, 64.27, 47.24, 22.06, 15.27,  9.01],
        [97.43, 92.54, 81.79, 30.08, 21.23, 11.27],
        [99.56, 90.87, 78.64, 26.35, 17.83, 10.42],
        [58.01, 50.03, 41.73, 18.01, 11.98,  5.99],
        [99.82, 96.74, 90.85, 34.27, 24.86, 13.94],
    ])

    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 使用学术界常用的具有高对比度的感知均匀色图 (Perceptually Uniform Sequential)
    # RlBu 或 YlGnBu 在黑白打印下也具有较好区分度。这里使用 YlGnBu 或 inferno/viridis。
    # YlOrRd 也是不错的选择，这里改用灰度友好的 YlGnBu
    im = ax.imshow(data, cmap="YlGnBu", aspect="equal", vmin=0, vmax=100)

    ax.set_xticks(np.arange(len(models)))
    ax.set_yticks(np.arange(len(strategies)))
    ax.set_xticklabels(models, fontfamily="Times New Roman", fontsize=11)
    ax.set_yticklabels(strategies, fontsize=14)
    ax.set_xlabel("待测模型", fontsize=14)
    ax.set_ylabel("攻击策略", fontsize=14)

    # 对于Y轴刻度标签，将纯英文的 HackAPrompt 单独设为 Times New Roman
    for tick in ax.yaxis.get_ticklabels():
        if all(ord(c) < 128 for c in tick.get_text()):
            tick.set_fontfamily('Times New Roman')

    # 标注数值
    for i in range(len(strategies)):
        for j in range(len(models)):
            v = data[i, j]
            # 动态调整字体颜色保证可读性
            color = "white" if v > 60 else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=13, color=color, fontfamily="Times New Roman")

    # 调整色标
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.03, aspect=20)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label("攻击成功率 (%)", labelpad=10, fontsize=14)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "Fig4-strategies-heatmap.pdf")
    fig.savefig(path)
    fig.savefig(os.path.join(OUT_DIR, "Fig4-strategies-heatmap.png"))
    plt.close(fig)
    print(f"[OK] {path}")


# ============================================================
# 图2  提示词长度对攻击效果的影响 (对应表 4.8 / 4.9 / 4.10)
# ============================================================
def fig_prompt_length():
    lengths = ["短文本\n(10-20)", "中等文本\n(21-50)", "长文本\n(51-100)", "超长文本\n(>100)"]
    x = np.arange(len(lengths))

    # ----- 数据 -----
    hack = {
        "AlpaCare":  [52.74, 55.31, 60.58, 63.42],
        "Asclepius": [44.86, 47.23, 52.84, 55.18],
        "BioMistral":[36.85, 39.27, 43.56, 47.24],
        "BioLlama3": [14.73, 16.82, 19.34, 21.15],
        "Llama2":    [ 8.76, 10.23, 13.58, 15.35],
        "Llama3":    [ 3.82,  5.14,  6.73,  8.27],
    }
    ignore = {
        "AlpaCare":  [83.24, 77.68, 74.15, 66.81],
        "Asclepius": [72.85, 66.34, 61.27, 56.62],
        "BioMistral":[54.36, 50.78, 44.25, 39.57],
        "BioLlama3": [27.86, 24.15, 19.83, 16.38],
        "Llama2":    [20.74, 17.36, 13.82,  9.16],
        "Llama3":    [12.86, 10.18,  7.85,  5.14],
    }
    escape = {
        "AlpaCare":  [99.86, 99.73, 97.26, 92.85],
        "Asclepius": [97.24, 94.86, 91.35, 86.71],
        "BioMistral":[87.63, 84.82, 79.54, 75.17],
        "BioLlama3": [35.74, 32.28, 28.13, 24.16],
        "Llama2":    [27.82, 23.68, 19.17, 14.24],
        "Llama3":    [15.76, 12.83,  9.54,  6.95],
    }

    def mean_across_models(d):
        return np.mean(list(d.values()), axis=0)

    hack_mean   = mean_across_models(hack)
    ignore_mean = mean_across_models(ignore)
    escape_mean = mean_across_models(escape)

    # 沉稳的学术配色 (如 Seaborn 的 deep / colorblind 色系)
    colors = ["#4C72B0", "#DD8452", "#55A868"]
    markers = ["o", "s", "^"]
    linestyles = ["-", "--", "-."]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

    # --- 左面板 ---
    for arr, label, c, m, ls in zip(
        [hack_mean, ignore_mean, escape_mean],
        ["HackAPrompt", "忽略指令", "转义字符"],
        colors, markers, linestyles
    ):
        ax1.plot(x, arr, marker=m, color=c, linestyle=ls, linewidth=2, 
                 markersize=8, markeredgecolor='white', markeredgewidth=1.2, label=label)
        for i, val in enumerate(arr):
            va = "bottom"
            y_offset = 1.5
            if label == "HackAPrompt" and i == 2:
                va = "top"
                y_offset = -2.5
            if label == "忽略指令" and i == 3:
                va = "top"
                y_offset = -2.5
            ax1.text(i, val + y_offset, f"{val:.1f}", ha="center", va=va, fontsize=10, fontfamily="Times New Roman", color=c)

    ax1.set_xticks(x)
    ax1.set_xticklabels(lengths)
    ax1.set_ylabel("平均攻击成功率 (%)")
    ax1.set_xlabel("提示词长度区间")
    ax1.set_title("(a) 各攻击策略均值趋势", pad=10)
    ax1.legend(loc="upper right", frameon=False)
    ax1.grid(False)
    ax1.set_ylim(0, 110)
    ax1.set_yticks(np.arange(0, 101, 20))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- 右面板 ---
    for d, label, c, m, ls in zip(
        [hack, ignore, escape],
        ["HackAPrompt", "忽略指令", "转义字符"],
        colors, markers, linestyles
    ):
        arr2 = d["AlpaCare"]
        ax2.plot(x, arr2, marker=m, color=c, linestyle=ls, linewidth=2, 
                 markersize=8, markeredgecolor='white', markeredgewidth=1.2, label=label)
        for i, val in enumerate(arr2):
            va = "bottom"
            y_offset = 1.5
            if label == "HackAPrompt" and i == 3:
                va = "top"
                y_offset = -2.5
            ax2.text(i, val + y_offset, f"{val:.1f}", ha="center", va=va, fontsize=10, fontfamily="Times New Roman", color=c)

    ax2.set_xticks(x)
    ax2.set_xticklabels(lengths)
    ax2.set_ylabel("攻击成功率 (%)")
    ax2.set_xlabel("提示词长度区间")
    ax2.set_title("(b) AlpaCare 模型表现", pad=10)
    ax2.legend(loc="lower right", frameon=False)
    ax2.grid(False)
    ax2.set_ylim(0, 110)
    ax2.set_yticks(np.arange(0, 101, 20))
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "Fig4-prompt-length.pdf")
    fig.savefig(path)
    fig.savefig(os.path.join(OUT_DIR, "Fig4-prompt-length.png"))
    plt.close(fig)
    print(f"[OK] {path}")


# ============================================================
# 图3  基线 vs AutoDAN (对应表 4.15 + 4.16)
# ============================================================
def fig_baseline_vs_autodan():
    models = ["AlpaCare", "Asclepius", "BioMistral", "BioLlama3", "Llama2", "Llama3"]

    baseline_harm = [72.35,  0.42,  0.58,  0.14,  0.54,  0.12]
    autodan_harm  = [98.72, 72.86, 85.47, 94.63, 64.27, 42.15]
    baseline_toxic = [68.47,  0.26,  0.34,  0.08,  0.31,  0.08]
    autodan_toxic  = [97.35, 74.53, 97.18, 11.82, 50.34, 28.73]

    x = np.arange(len(models))
    w = 0.18  # 柱宽稍微调窄，增加组内间距
    gap = 0.05

    fig, ax = plt.subplots(figsize=(10.5, 5))

    # 使用学术风格配色 (对比强烈但也和谐)
    c1, c2 = "#A0CBE8", "#4E79A7"  # 蓝色系：基线 vs 攻击 (HarmfulQA)
    c3, c4 = "#FFBE7D", "#F28E2B"  # 橙色系：基线 vs 攻击 (ToxicQA)

    # 带边缘线的柱状图，看起来更精致
    edge_kws = {"edgecolor": "black", "linewidth": 0.8, "zorder": 3}

    bars1 = ax.bar(x - 1.5*w - gap, baseline_harm,  w, label="HarmfulQA Base",  color=c1, **edge_kws)
    bars2 = ax.bar(x - 0.5*w - gap/3, autodan_harm,   w, label="HarmfulQA AutoDAN", color=c2, **edge_kws)
    bars3 = ax.bar(x + 0.5*w + gap/3, baseline_toxic,  w, label="ToxicQA Base",   color=c3, **edge_kws)
    bars4 = ax.bar(x + 1.5*w + gap, autodan_toxic,   w, label="ToxicQA AutoDAN",  color=c4, **edge_kws)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontfamily="Times New Roman", fontsize=12)  # 模型名均为英文
    ax.set_ylabel("攻击成功率 (%)", fontsize=12)  # 中文用全局回退字体
    ax.set_xlabel("待测模型", fontsize=12)          # 中文用全局回退字体
    ax.set_ylim(0, 110)  # 留出顶部标注空间
    
    # y 轴刻度均为纯数字，打开限制使用 Times New Roman
    yticks = np.arange(0, 101, 20)
    ax.set_yticks(yticks)
    ax.set_yticklabels([str(y) for y in yticks], fontfamily="Times New Roman", fontsize=12)
    
    # 移除上方和右侧边框线
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 图例包含中文（基线）和英文（AutoDAN），对每条文字单独设定字体
    legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=4, frameon=False, fontsize=12)
    for text in legend.get_texts():
        label = text.get_text()
        # 判断是否包含中文字符
        if any('\u4e00' <= c <= '\u9fff' for c in label):
            # 混合文本：第一优先 SimSun（支持中文），英文字符由回退处理
            text.set_fontfamily(['SimSun', 'Times New Roman'])
        else:
            # 纯英文：直接用 Times New Roman
            text.set_fontfamily('Times New Roman')
    
    
    ax.grid(False)
    ax.set_axisbelow(True)

    # 标注所有数值，使用英文字体，横向显示，禁用裁剪以免100附近文字被切
    def label_bars(bars):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1.5,
                    f"{h:.1f}", ha="center", va="bottom", 
                    fontsize=11.4, fontfamily="Times New Roman", zorder=4, clip_on=False)

    label_bars(bars1)
    label_bars(bars2)
    label_bars(bars3)
    label_bars(bars4)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "Fig4-baseline-vs-autodan.pdf")
    fig.savefig(path)
    fig.savefig(os.path.join(OUT_DIR, "Fig4-baseline-vs-autodan.png"))
    plt.close(fig)
    print(f"[OK] {path}")


# ============================================================
# 图4  不同注入频率下的平均攻击成功率 (对应表 4.8)
# ============================================================
def fig_attack_frequency():
    frequencies = ["1次", "2次", "3次", "4次", "5次", "6次", "7次"]
    x = np.arange(len(frequencies))

    # ----- 数据 -----
    data = {
        "AlpaCare":  [77.07, 60.34, 49.58, 42.17, 37.24, 33.46, 30.82],
        "Asclepius": [69.97, 63.82, 58.43, 53.27, 48.91, 44.63, 42.18],
        "BioMistral":[60.02, 44.28, 33.85, 27.43, 23.58, 20.94, 19.27],
        "BioLlama3": [24.08, 20.63, 17.52, 15.18, 13.34, 11.82, 10.75],
        "Llama2":    [16.90, 18.14, 17.53, 15.86, 13.92, 12.08, 10.13],
        "Llama3":    [ 9.31, 10.02,  9.57,  8.48,  7.36,  6.21,  5.23],
    }

    models = list(data.keys())
    
    # 颜色与标记 (取多样化色系)
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
    markers = ["o", "s", "^", "D", "v", "p"]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    for i, m_name in enumerate(models):
        arr = data[m_name]
        c = colors[i]
        m = markers[i]
        ax.plot(x, arr, marker=m, color=c, linestyle="-", linewidth=2, 
                 markersize=8, markeredgecolor='white', markeredgewidth=1.2, label=m_name)
        
        for j, val in enumerate(arr):
            va = "bottom"
            y_offset = 1.2
            
            # 手动调整重叠的点，基于观察到的冲突进行上下错位
            # 注意: va="top" 表示文字在数据点下方, va="bottom" 表示文字在数据点上方
            if m_name == "AlpaCare":
                if j == 1: va, y_offset = "top", -2.8       # 于60.34 (Asclepius: 63.82)
            elif m_name == "Asclepius":
                if j == 1: va, y_offset = "bottom", 1.8     # (Asclepius 63.82 在上)
            elif m_name == "BioLlama3":
                if j == 1: va, y_offset = "bottom", 1.8     # (20.63, Llama2 18.14)
                if j == 2: va, y_offset = "top", -2.8       # (17.52, Llama2 17.53)
                if j == 3: va, y_offset = "top", -2.8       # (15.18, Llama2 15.86)
                if j == 4: va, y_offset = "top", -1.5       # (13.34, 在下方但略微往上一点)
                if j == 5: va, y_offset = "top", -1.5       # (11.82, 在下方但略微往上一点)
                if j == 6: va, y_offset = "top", -1.5       # (10.75, 在下方但略微往上一点)
            elif m_name == "Llama2":
                if j == 1: va, y_offset = "top", -2.8       # (18.14, BioLlama3 20.63)
                if j == 2: va, y_offset = "bottom", 1.8     # (17.53, BioLlama3 17.52)
                if j == 3: va, y_offset = "bottom", 1.8     # (15.86, BioLlama3 15.18)
                if j == 4: va, y_offset = "bottom", 1.8     # (13.92, BioLlama3 13.34)
                if j == 5: va, y_offset = "bottom", 1.8     # (12.08, BioLlama3 11.82)
                if j == 6: va, y_offset = "bottom", 1.8     # (10.13, 放在上方)
            elif m_name == "Llama3":
                va, y_offset = "top", -2.8                  # Llama3 默认文字在下方
                if j == 6: va, y_offset = "top", -1.5       # 最后一个点在下方但略微往上一点避免重合

            ax.text(j, val + y_offset, f"{val:.1f}", ha="center", va=va, 
                    fontsize=11, fontfamily="Times New Roman", color="black")

    ax.set_xticks(x)
    ax.set_xticklabels(frequencies, fontfamily="SimSun", fontsize=12)
    ax.set_ylabel("平均攻击成功率 (%)", fontsize=12)
    ax.set_xlabel("注入频率", fontsize=12)
    
    # 将图例放在外面板下方，避免遮挡任何曲线
    # 所有图例标签均为英文模型名，直接使用 Times New Roman
    legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=6, frameon=False,
                       prop={'family': 'Times New Roman', 'size': 12})
    
    ax.grid(False)
    ax.set_ylim(0, 110)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.tick_params(axis='y', labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "Fig4-attack-frequency.pdf")
    fig.savefig(path)
    fig.savefig(os.path.join(OUT_DIR, "Fig4-attack-frequency.png"))
    plt.close(fig)
    print(f"[OK] {path}")

# ============================================================
if __name__ == "__main__":
    fig_strategies_heatmap()
    fig_prompt_length()
    fig_baseline_vs_autodan()
    fig_attack_frequency()
    print("\n[学术规范版] 全部图片已重新生成至:", os.path.abspath(OUT_DIR))
