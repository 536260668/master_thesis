# -*- coding: utf-8 -*-
"""
生成 RA 数据集病历示例图（Fig5-dataset-example）
重新设计：纯平整面对齐、统一字体、精简纯粹的学术表格/卡片风格
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

# ---------- 全局学术规范样式 ----------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "Arial"],
    "axes.unicode_minus": False,
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

SECTIONS = [
    {
        "tag": "模块① 病史信息",
        "color_theme": "#3160a0", # 主色
        "color_bg":    "#f4f7fb", # 背景色
        "type": "kv",
        "content": [
            ("主诉：", "多关节疼痛 20 余年"),
            ("既往史：", "高血压 2 年（口服吲达帕胺，血压控制可）；\n否认糖尿病、冠心病、肝炎、结核病史"),
            ("体格检查：", "T 36.8 ℃，P 74 次/分，BP 118/76 mmHg；\n双手指指间关节肿胀，右膝关节明显肿胀"),
            ("辅助检查：", "RF 958 IU/ml↑，抗 CCP 251.70 RU/ml↑，\nCRP 15.54 mg/L↑，ESR 38 mm/h↑，IL-6 44.82 pg/ml↑"),
        ],
    },
    {
        "tag": "模块② 出院小结",
        "color_theme": "#3d8b51",
        "color_bg":    "#f5faf6",
        "type": "text",
        # 手动换行调整，避免文字超出边框
        "content": (
            "患者因多关节肿痛入院，完善相关检查\n后停用来氟米特，加用甲氨蝶呤 10 mg qw\n"
            "+ 叶酸片 5 mg qw，辅以洛索洛芬、\n阿法骨化醇等对症支持治疗。\n\n"
            "治疗后患者病情平稳，要求出院，予以办理。"
        ),
    },
    {
        "tag": "模块③ 出院诊断",
        "color_theme": "#b2363b",
        "color_bg":    "#fbf4f5",
        "type": "list",
        "content": [
            "① 类风湿性关节炎（主要诊断）",
            "② 骨量减少",
            "③ 腋窝淋巴结增大",
        ],
    },
    {
        "tag": "模块④ 出院处方",
        "color_theme": "#c26d2e",
        "color_bg":    "#fcf7f4",
        "type": "table",
        # 调整第四模块(出院处方)中各列位置，防止右侧文字过长
        "cols": [0.0, 0.25, 0.40, 0.55],
        "content": [
            ["甲氨蝶呤片", "10 mg", "口服", "每周 1 次"],
            ["叶酸片", "5 mg", "口服", "每周 1 次（甲氨蝶呤次日服）"],
            ["碳酸钙 D3 片", "600 mg", "口服", "每日 1 次"],
            ["[复诊]", "1 个月后风湿科...", "", ""],
        ],
    },
]

# ── 布局计算 ──────────────────────────────────────────────
PADDING   = 0.04
GAP_X     = 0.03
GAP_Y     = 0.04
FIG_W, FIG_H = 11, 7.5

fig = plt.figure(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor("white")

# 标题
fig.text(0.5, 0.94, "RA 患者临床病历示例（去标识化）",
         ha="center", va="top", fontsize=15, weight="bold", color="#111")
fig.text(0.5, 0.89, "数据来源: 同济医院风湿免疫科  |  诊断标准: 2010 年 ACR/EULAR RA 分类标准",
         ha="center", va="top", fontsize=11, color="#444")

# 分割线
line = plt.Line2D((0.15, 0.85), (0.86, 0.86), color="#cccccc", linewidth=1.0, transform=fig.transFigure)
fig.add_artist(line)

# 给右侧留出稍微多一点空间，把 W1 调小一层，W2 调大
W1, W2 = 0.53, 0.36
H1, H2 = 0.43, 0.28

LAYOUT = [
    (PADDING,              1 - 0.16 - H1,           W1, H1),  # 左上
    (PADDING + W1 + GAP_X, 1 - 0.16 - H1,           W2, H1),  # 右上
    (PADDING,              1 - 0.16 - H1 - GAP_Y - H2, W1, H2),  # 左下
    (PADDING + W1 + GAP_X, 1 - 0.16 - H1 - GAP_Y - H2, W2, H2),  # 右下
]

for sec, (l, b, w, h) in zip(SECTIONS, LAYOUT):
    ax = fig.add_axes([l, b, w, h])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    color_theme = sec["color_theme"]
    color_bg    = sec["color_bg"]
    
    # 画背景卡片
    bg = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01",
                         facecolor=color_bg, edgecolor=color_theme,
                         linewidth=1.2, transform=ax.transAxes, clip_on=False)
    ax.add_patch(bg)

    # 标题头
    header_h = 0.14 if h > 0.35 else 0.22  # 高度自适应
    
    # 标题底色及分隔线
    rect = mpatches.Rectangle((0, 1 - header_h), 1, header_h, 
                              facecolor=color_theme, alpha=0.08, edgecolor="none", 
                              transform=ax.transAxes)
    ax.add_patch(rect)
    ax.plot([0, 1], [1 - header_h, 1 - header_h], color=color_theme, linewidth=1.2, transform=ax.transAxes)

    ax.text(0.5, 1 - header_h/2, sec["tag"], ha="center", va="center",
            fontsize=12, weight="bold", color=color_theme, transform=ax.transAxes)

    # 绘制内容
    content_area = 1 - header_h
    pad_y = 0.08
    usable_h = content_area - 2 * pad_y
    
    if sec["type"] == "kv":
        n_items = len(sec["content"])
        step = usable_h / (n_items - 0.5)
        for i, (key, val) in enumerate(sec["content"]):
            y = 1 - header_h - pad_y - i * step
            # Key 靠右对齐到 0.18
            ax.text(0.18, y, key, ha="right", va="top", fontsize=11.5, weight="bold", color="#333", linespacing=1.6)
            # Value 靠左对齐到 0.20
            ax.text(0.20, y, val, ha="left", va="top", fontsize=11.5, color="#222", linespacing=1.6)
            
    elif sec["type"] == "text":
        # 适当往中间挤一点
        y = 1 - header_h - pad_y - 0.02
        ax.text(0.08, y, sec["content"], ha="left", va="top", 
                fontsize=11.5, color="#222", linespacing=1.6, wrap=False)
                
    elif sec["type"] == "list":
        n_items = len(sec["content"])
        step = usable_h / (n_items - 0.5)
        for i, item in enumerate(sec["content"]):
            y = 1 - header_h - pad_y - i * step
            ax.text(0.08, y, item, ha="left", va="top", fontsize=11.5, color="#222")
            
    elif sec["type"] == "table":
        cols = sec["cols"]
        n_items = len(sec["content"])
        step = usable_h / (n_items - 0.5)
        for i, row in enumerate(sec["content"]):
            y = 1 - header_h - pad_y - i * step
            for j, text_val in enumerate(row):
                if not text_val: continue
                weight = "bold" if j == 0 else "normal"
                color  = "#333" if j == 0 else "#222"
                ax.text(0.06 + cols[j], y, text_val, ha="left", va="top", 
                        fontsize=11.5, weight=weight, color=color)

# ── 角标注释 ─────────────────────────────────────────────
fig.text(0.5, 0.02,
         "注：以上为示例病历节选，所有患者信息已完成去标识化处理，个人可识别信息均以占位符替代。",
         fontsize=10, color="#666", va="bottom", ha="center")

# ── 输出 ─────────────────────────────────────────────────
OUT_DIR = r"c:\学习\研究生学习\毕设\figures"
os.makedirs(OUT_DIR, exist_ok=True)

pdf_path = os.path.join(OUT_DIR, "Fig5-dataset-example.pdf")
png_path = os.path.join(OUT_DIR, "Fig5-dataset-example.png")

plt.savefig(pdf_path, dpi=300, bbox_inches="tight", format="pdf")
plt.savefig(png_path, dpi=200, bbox_inches="tight")
print(f"[OK] {pdf_path}")
print(f"[OK] {png_path}")
