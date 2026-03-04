"""
处理第五章原始实验数据，输出供写作使用的ASR汇总表。

数据说明：
  g = good (正常模型)
  b = bad  (投毒/攻击模型)
  四字符串对应 Agent1~Agent4 的状态

四个数据集：
  biollama3_broken_ra              → 数据投毒 10%，BioLlama3
  biollama3_0.5_broken_llama31_ra  → 数据投毒 50%，BioLlama3 bad + Llama3.1 good
  biollama3_0.5_broken_ra_paa      → 提示词攻击 (PAA)，BioLlama3 bad + Llama3.1 good
  llama31_streval_ra               → 越狱提示词攻击，Llama3.1
"""

TOTAL = 96

# ── 原始数据 ─────────────────────────────────────────────────────────────────
# 格式：{配置: [A1投毒数, A2投毒数, A3投毒数, A4投毒数]}
# 去重后取唯一配置（原文件有重复行）

RAW = {
    # 数据投毒 10%，BioLlama3
    "poison_10": {
        "bbbb": [14, 19, 22, 21],
        "gbbb": [ 6, 20, 15, 20],
        "bgbb": [14, 12, 24, 16],
        "bbgb": [14, 19,  6, 26],
        "bbbg": [14, 19, 22,  9],
        "ggbb": [ 6,  8, 26, 20],
        "gbgb": [ 6, 20,  7, 21],
        "gbbg": [ 6, 20, 15,  8],
        "bggb": [14, 12,  8, 26],
        "bgbg": [14, 12, 24,  6],
        "bbgg": [14, 19,  6,  5],
        "gggb": [ 6,  8,  4, 20],
        "ggbg": [ 6,  8, 26,  5],
        "gbgg": [ 6, 20,  7,  5],
        "bggg": [14, 12,  8,  9],
        "gggg": [ 6,  8,  4,  9],
    },
    # 数据投毒 50%，BioLlama3 bad + Llama3.1 good
    "poison_50": {
        "bbbb": [69, 75, 77, 76],
        "gbbb": [ 6, 79, 65, 78],
        "bgbb": [69,  4, 81, 63],
        "bbgb": [69, 75,  8, 80],
        "bbbg": [69, 75, 77,  5],
        "ggbb": [ 6,  8, 80, 64],
        "gbgb": [ 6, 79,  5, 80],
        "gbbg": [ 6, 79, 65,  4],
        "bggb": [69,  4,  9, 82],
        "bgbg": [69,  4, 81,  5],
        "bbgg": [69, 75,  8,  8],
        "gggb": [ 6,  8,  4, 77],
        "ggbg": [ 6,  8, 80,  5],
        "gbgg": [ 6, 79,  5,  8],
        "bggg": [69,  4,  9,  5],
        "gggg": [ 6,  8,  4,  9],
    },
    # 提示词攻击 PAA，BioLlama3 bad + Llama3.1 good
    "paa": {
        "bbbb": [72, 85, 79, 85],
        "gbbb": [ 6, 91, 76, 84],
        "bgbb": [72,  9, 91, 80],
        "bbgb": [72, 85, 13, 90],
        "bbbg": [72, 85, 79, 10],
        "ggbb": [ 6, 10, 91, 75],
        "gbgb": [ 6, 91,  8, 91],
        "gbbg": [ 6, 91, 76, 15],
        "bggb": [72,  9, 18, 90],
        "bgbg": [72,  9, 91,  9],
        "bbgg": [72, 85, 13, 15],
        "gggb": [ 6, 10,  9, 92],
        "ggbg": [ 6, 10, 91,  9],
        "gbgg": [ 6, 91,  8, 14],
        "bggg": [72,  9, 18,  9],
        "gggg": [ 6, 10,  9, 10],
    },
    # 越狱提示词攻击，Llama3.1
    "jailbreak": {
        "bbbb": [87, 90, 91, 91],
        "gbbb": [ 5, 81, 86, 88],
        "bgbb": [87,  5, 83, 85],
        "bbgb": [87, 90,  8, 81],
        "bbbg": [87, 90, 91,  9],
        "ggbb": [ 5,  9, 82, 88],
        "gbgb": [ 5, 81,  6, 82],
        "gbbg": [ 5, 81, 86,  8],
        "bggb": [87,  5, 13, 84],
        "bgbg": [87,  5, 83,  6],
        "bbgg": [87, 90,  8, 14],
        "gggb": [ 5,  9,  6, 82],
        "ggbg": [ 5,  9, 82,  7],
        "gbgg": [ 5, 81,  6, 12],
        "bggg": [87,  5, 13,  6],
        "gggg": [ 5,  9,  6, 10],
    },
}

EXP_LABELS = {
    "poison_10":  "数据投毒 10%（BioLlama3）",
    "poison_50":  "数据投毒 50%（BioLlama3+Llama3.1）",
    "paa":        "提示词攻击 PAA（BioLlama3+Llama3.1）",
    "jailbreak":  "越狱提示词攻击（Llama3.1）",
}


def to_asr(count):
    return round(count / TOTAL * 100, 1)


def agent1_state(cfg):
    return cfg[0]  # 'g' or 'b'


def bad_count(cfg):
    return cfg.count("b")


def fmt_asr(n):
    return f"{to_asr(n):5.1f}%"


# ── 输出1：各配置 Agent4 ASR（按坏模型数量分组）─────────────────────────────
def print_section1(exp_key, data):
    label = EXP_LABELS[exp_key]
    print(f"\n## {label} — Agent4 最终输出 ASR（按坏模型数量分组）\n")
    print(f"{'配置':>6}  {'A1':>6}  {'A2':>6}  {'A3':>6}  {'A4(最终)':>10}")
    print("-" * 48)
    for nb in range(5):
        configs = {k: v for k, v in data.items() if bad_count(k) == nb}
        if configs:
            print(f"  [{'b'*nb + 'g'*(4-nb)} 组，{nb}个坏模型]")
            for cfg, vals in sorted(configs.items()):
                print(f"  {cfg}  {fmt_asr(vals[0])}  {fmt_asr(vals[1])}  "
                      f"{fmt_asr(vals[2])}  {fmt_asr(vals[3])}")
    print()


# ── 输出2：入口效应分析（Agent1状态 vs 系统ASR）──────────────────────────────
def print_section2():
    """
    入口效应的正确对比是控制其余智能体状态不变，只改变Agent1：
    - bggg（仅Agent1被攻击）vs gggg（全正常基线）→ Agent1单独破坏能造成多少损害
    - gbbb（仅Agent1正常）vs bbbb（全攻击）→ Agent1正常能阻断多少损害
    另外：gbbb vs bgbb 对比攻击Agent1与攻击Agent2的差异（相同坏模型数量下）
    """
    print("\n## 入口效应分析：Agent1 状态对系统最终 ASR 的影响\n")

    # 分析1：单点攻击对比 —— 仅Agent1被攻击 vs 各中间Agent被攻击
    print("### 分析A：单点攻击时不同位置对系统ASR的影响")
    print("（1个坏模型场景：bggg / gbgg / ggbg / gggb）\n")
    single_cfgs = [("bggg", "Agent1被攻击"), ("gbgg", "Agent2被攻击"),
                   ("ggbg", "Agent3被攻击"), ("gggb", "Agent4被攻击")]
    col_heads = "  ".join(f"{EXP_LABELS[k][:12]:>14}" for k in RAW.keys())
    print(f"  {'攻击位置':>12}  {col_heads}")
    print("-" * 70)
    for cfg, label in single_cfgs:
        row = f"  {label:>12}"
        for exp_key, data in RAW.items():
            vals = data.get(cfg)
            row += f"  {fmt_asr(vals[3]):>14}" if vals else f"  {'N/A':>14}"
        print(row)
    print()

    # 分析2：固定其余Agent全坏，对比Agent1正常 vs 全坏
    print("### 分析B：其余3个Agent均被攻击时，Agent1的状态能否阻断传播")
    print("（对比 gbbb vs bbbb）\n")
    compare_cfgs = [("gbbb", "Agent1=正常，其余全攻击"),
                    ("bbbb", "全攻击上限")]
    print(f"  {'配置':>22}  {col_heads}")
    print("-" * 70)
    for cfg, label in compare_cfgs:
        row = f"  {label:>22}"
        for exp_key, data in RAW.items():
            vals = data.get(cfg)
            row += f"  {fmt_asr(vals[3]):>14}" if vals else f"  {'N/A':>14}"
        print(row)
    print()

    # 分析3：全正常基线
    print("### 参考：全正常基线 (gggg)")
    row = f"  {'gggg（全正常）':>22}"
    for exp_key, data in RAW.items():
        vals = data.get("gggg")
        row += f"  {fmt_asr(vals[3]):>14}" if vals else f"  {'N/A':>14}"
    print(f"  {'配置':>22}  {col_heads}")
    print("-" * 70)
    print(row)
    print()


# ── 输出3：关键配置对比表（供写作直接引用）─────────────────────────────────
def print_section3():
    print("\n## 关键配置对比（供写作直接引用）\n")
    key_cfgs = ["gggg", "bbbb", "gbbb", "bgbb", "bbgb", "bbbg"]
    header = f"{'配置':>6}  " + "  ".join(f"{k[:12]:>14}" for k in RAW.keys())
    print(header)
    print("-" * (6 + 16 * len(RAW)))
    for cfg in key_cfgs:
        row = f"  {cfg}"
        for exp_key, data in RAW.items():
            vals = data.get(cfg)
            if vals:
                row += f"  {fmt_asr(vals[3]):>14}"
            else:
                row += f"  {'N/A':>14}"
        print(row)

    print()
    print("（数值为 Agent4 最终输出 ASR，即系统级攻击成功率）")
    print()
    print("配置说明：")
    print("  gggg = 全正常基线")
    print("  bbbb = 全攻击上限")
    print("  gbbb = 仅 Agent1 正常，其余被攻击")
    print("  bgbb = 仅 Agent1 被攻击，Agent2 正常，其余被攻击")
    print("  bbgb = 仅 Agent3 正常，其余被攻击")
    print("  bbbg = 仅 Agent4 正常，其余被攻击")


# ── 输出4：各实验全好/全坏/单点攻击 Agent4 ASR 汇总 ─────────────────────────
def print_section4():
    print("\n## 单点攻击位置效应：只有一个 Agent 为坏模型时的系统 ASR\n")
    single_bad_cfgs = ["gbbb", "bgbb", "bbgb", "bbbg"]  # 3个坏1个好的情况
    single_good_cfgs = ["bggg", "gbgg", "ggbg", "gggb"]  # 1个坏3个好的情况

    print("### 场景A：3个坏模型（只有1个Agent正常）")
    print(f"{'正常位置':>10}  " + "  ".join(f"{k[:12]:>14}" for k in RAW.keys()))
    pos_labels = {"gbbb": "Agent1正常", "bgbb": "Agent2正常",
                  "bbgb": "Agent3正常", "bbbg": "Agent4正常"}
    for cfg in single_bad_cfgs:
        row = f"  {pos_labels[cfg]:>10}"
        for exp_key, data in RAW.items():
            vals = data.get(cfg)
            row += f"  {fmt_asr(vals[3]):>14}" if vals else f"  {'N/A':>14}"
        print(row)

    print()
    print("### 场景B：1个坏模型（只有1个Agent被攻击）")
    print(f"{'攻击位置':>10}  " + "  ".join(f"{k[:12]:>14}" for k in RAW.keys()))
    pos_labels2 = {"bggg": "Agent1被攻击", "gbgg": "Agent2被攻击",
                   "ggbg": "Agent3被攻击", "gggb": "Agent4被攻击"}
    for cfg in single_good_cfgs:
        row = f"  {pos_labels2[cfg]:>10}"
        for exp_key, data in RAW.items():
            vals = data.get(cfg)
            row += f"  {fmt_asr(vals[3]):>14}" if vals else f"  {'N/A':>14}"
        print(row)
    print()


# ── 主程序 ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    output_lines = []

    # 重定向 print 到同时输出到文件和终端
    output_path = r"c:\学习\研究生学习\毕设\text_ref\chap5_processed_data.md"

    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)
        def flush(self):
            for f in self.files:
                f.flush()

    with open(output_path, "w", encoding="utf-8") as fout:
        sys.stdout = Tee(sys.__stdout__, fout)

        print("# 第五章实验数据整理（供写作使用）")
        print(f"\n> 总样本量：{TOTAL}例 RA 患者\n")
        print("> b=投毒/攻击模型，g=正常模型，四字符依次对应 Agent1~Agent4\n")

        print_section3()
        print_section2()
        print_section4()

        for exp_key, data in RAW.items():
            print_section1(exp_key, data)

        sys.stdout = sys.__stdout__

    print(f"\n✅ 已保存到：{output_path}")
