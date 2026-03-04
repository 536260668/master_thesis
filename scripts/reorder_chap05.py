"""
reorder_chap05.py
-----------------
备份 chap05.tex，然后将 §5.2（多智能体协作下的级联失效实证）的子节
按如下新顺序重排：

  旧顺序:
    §5.2.1 实验配置                          (保持第一)
    §5.2.2 初始智能体状态的决定性作用
    §5.2.3 错误传播路径的定量分析
    §5.2.4 数据投毒攻击在多智能体环境下的表现
    §5.2.5 提示词攻击在多智能体环境下的表现

  新顺序:
    §5.2.1 实验配置                          (保持)
    §5.2.2 数据投毒攻击在多智能体环境下的表现  (原 §5.2.4)
    §5.2.3 提示词攻击在多智能体环境下的表现   (原 §5.2.5)
    §5.2.4 初始智能体状态的决定性作用         (原 §5.2.2)
    §5.2.5 错误传播路径的定量分析             (原 §5.2.3)
"""

import shutil
import re
from pathlib import Path
from datetime import datetime

SRC = Path(r"c:\学习\研究生学习\毕设\body\chap05.tex")

# ---------- 1. 备份 ----------
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = SRC.parent / f"chap05_backup_{timestamp}.tex"
shutil.copy2(SRC, backup)
print(f"[✓] 已备份至：{backup}")

# ---------- 2. 读取原文 ----------
text = SRC.read_text(encoding="utf-8")

# ---------- 3. 定位 §5.2 的全部子节 ----------
# 策略：以 \subsection 为分隔符，切割出每个子节块。
# 每个子节块从 \subsection{...} 开始，到下一个 \subsection 或上级节 (\section) 结束。

# 用正则把文本分割成若干段：[前缀, 子节1, 子节2, ...]
# 我们先找到 §5.2 的范围：从 \section{多智能体协作...} 到下一个 \section{
SEC5_2_TITLE = "多智能体协作下的级联失效实证"
SEC5_3_TITLE = "真实临床场景下的特异性风险分析"

start_idx = text.index(f"\\section{{{SEC5_2_TITLE}}}")
end_idx   = text.index(f"\\section{{{SEC5_3_TITLE}}}")

before_sec52 = text[:start_idx]          # §5.2 之前的全部内容
sec52_block  = text[start_idx:end_idx]   # §5.2 整体（含 \section 行）
after_sec52  = text[end_idx:]            # §5.3 及之后

# ---------- 4. 从 §5.2 块中切割出各子节 ----------
# 正则：以 \subsection{ 开头直到下一个 \subsection 或块末
subsec_pattern = re.compile(r'(?=\\subsection\{)', re.MULTILINE)
parts = subsec_pattern.split(sec52_block)
# parts[0] = \section 行 + 引言段（§5.2 的正文引言）
# parts[1..5] = 五个子节块

intro   = parts[0]   # \section{...} + 引言段落
sub_521 = parts[1]   # §5.2.1 实验配置
sub_522 = parts[2]   # §5.2.2 初始智能体状态
sub_523 = parts[3]   # §5.2.3 错误传播路径
sub_524 = parts[4]   # §5.2.4 数据投毒
sub_525 = parts[5]   # §5.2.5 提示词攻击

# 打印各子节标题以确认
for i, p in enumerate(parts):
    first_line = p.split('\n')[0][:80]
    print(f"  parts[{i}]: {first_line}")

# ---------- 5. 按新顺序拼接 ----------
new_sec52 = intro + sub_521 + sub_524 + sub_525 + sub_522 + sub_523

# ---------- 6. 写出新文件 ----------
new_text = before_sec52 + new_sec52 + after_sec52
SRC.write_text(new_text, encoding="utf-8")

print(f"\n[✓] 已重排 §5.2 子节顺序，写入：{SRC}")
print("    新顺序：实验配置 → 数据投毒 → 提示词攻击 → 初始智能体状态 → 错误传播定量分析")
