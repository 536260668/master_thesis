# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## ⚠️ 重要注意事项（每次工作前必读）

1. **格式已设置，只生成内容**：论文LaTeX格式已由用户设置完成，撰写章节时只需生成正文内容，严格按照 `body/chap01.tex` 等现有文件的格式规范。

2. **Git提交规范**：
   - 提交者：`536260668 <536260668@qq.com>`
   - **严禁**在提交信息中包含任何Claude相关内容
   - **禁止**出现如"Generated with Claude Code"、"Co-Authored-By Claude"等字样

3. **撰写格式规范**：
   - 文件头：`%%% mode: latex` / `%%% TeX-master: t` / `%%% End:`
   - 章节：`\chapter{}`, `\section{}`, `\subsection{}`
   - 图表：图题在下、表题在上，使用三线表
   - 引用：`\cite{}`, `\ref{}`, `图~\ref{Figx-x}`
   - 标点：使用中文标点符号

---

## 项目概述

华中科技大学硕士学位论文写作项目。论文主题为**医疗大语言模型安全性评估**，基于英文论文《MLSE: Medical LLM Safety Evaluation in an Agentic Environment》进行改写和翻译。

### 参考资料位置

- `text_ref/MLSE Medical LLM Safety Evaluation in an Agentic Environment_final.docx` - 英文论文正文
- `text_ref/MLSE Medical LLM Safety Evaluation in an Agentic Environment Supplementary .docx` - 补充材料
- `text_ref/Figures.pdf` - 论文图表（框架图、实验结果图等）
- `格式参考.pdf` - HUST 论文格式规范文档

### 论文主要内容

- **研究问题**：医疗大语言模型（Medical LLM）在智能体环境中的安全性评估
- **核心贡献**：提出 MLSE 评估框架，包含智能体驱动的测试用例生成和多维度评估指标
- **技术方法**：模块化医疗智能体、测试用例自动生成、安全性评估指标体系

## 编译文档

**使用 XeLaTeX 编译**（中文字体支持必需）：

```
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

完整编译周期需要多次运行 XeLaTeX 以解析引用、文献目录和目录。

## 文档格式模式

通过修改 `main.tex` 中的文档类选项切换两种模式：

- **草稿格式**（工作草稿用）：`\documentclass[draftformat,mathCMR]{HUSTthesis}`
  - 包含页眉"华中科技大学硕士学位论文"
  - 包含页眉页脚装饰线

- **最终格式**（盲审/提交用）：`\documentclass[finalformat,mathCMR]{HUSTthesis}`
  - 移除页眉和装饰线
  - 页脚仅保留页码

在 `main.tex` 第 6-7 行注释/取消注释相应行来切换模式。

## 架构

### 核心文件

- `HUSTthesis.cls` - 主文档类，定义格式、版面、字体和环境
- `HUSTtils.sty` - 工具宏包，加载算法、表格等附加包
- `main.tex` - 根文档，组装所有章节

### 目录结构

- `body/` - 章节文件（chap01.tex ~ chap04.tex、cover.tex、conclusion.tex、ack.tex、appendix*.tex）
- `figures/` - 图片和图形（通过 `\graphicspath{{figures/}}` 引用）
- `font/` - 中文字体文件（xeCJK 使用的 .ttf 文件）
- `ref/` - 参考文献数据库（refs.bib）

### 封面信息（`body/cover.tex`）

所有论文元数据在 `body/cover.tex` 中定义：
- 中英文标题、作者、导师、学位信息
- 中英文摘要和关键词
- 分类号、学号、密级

编译前需更新此文件为个人信息。

### 章节组织

章节通过 `\include{body/chapXX}` 在 `main.tex` 中引入。结构如下：
- 前言部分（封面、摘要、目录）
- 正文部分（第1-4章、结论）
- 后言部分（致谢、参考文献、附录）

### 字体配置

模板使用 `font/` 目录下的本地字体：
- `SimSun.ttf` - 中文正文字体（宋体）
- `SimHei.ttf` - 无衬线字体（黑体）
- `simkai.ttf` - 斜体/楷体
- `simfang.ttf` - 仿宋
- `STZhongsong.ttf` - 华文中宋

### 自定义字体命令

- `\song` 或 `\songti` - 宋体
- `\hei` 或 `\heiti` - 黑体
- `\kai` 或 `\kaishu` - 楷体
- `\fs` 或 `\fangsong` - 仿宋
- `\zhongsong` - 华文中宋

### 自定义字号命令

字号命令接受可选参数指定行距，如 `\sanhao[1.5]` 表示三号字1.5倍行距：
- `\dachu`, `\chuhao`, `\xiaochu`, `\yihao`, `\xiaoyi`, `\erhao`, `\xiaoer`, `\sanhao`, `\xiaosan`, `\sihao`, `\banxiaosi`, `\xiaosi`, `\dawu`, `\wuhao`, `\xiaowu` 等

## 常见操作

**添加新章节**：创建 `body/chap05.tex`，在 `main.tex` 中添加 `\include{body/chap05}`

**添加图片**：放入 `figures/` 目录，使用 `\includegraphics{filename}`

**添加引用**：使用 `\cite{key}` 或 `\citep{key}`（已配置 natbib 上标样式）

**添加文献**：编辑 `ref/refs.bib`，使用标准 BibTeX 格式

## 文档类选项

- `draftformat` / `finalformat` - 页眉页脚显示
- `mathtimes` / `mathCMR` - 数学字体（Times Roman 或 Computer Modern Roman）
- `arial` - 使用 Arial 字体作为无衬线字体

## 参考文献样式

使用 `HUSTThesis.bst` 样式，配合 natbib 宏包，文献引用格式为上标数字。

## 论文章节结构规划

根据 HUST 硕士论文要求，建议章节安排：

| 章节 | 内容 | 对应英文论文部分 |
|------|------|------------------|
| 第一章 绪论 | 研究背景、意义、现状、本文工作 | Introduction |
| 第二章 相关技术 | 大语言模型、医疗AI、智能体、安全性评估 | Related Work |
| 第三章 MLSE框架设计 | 框架概述、智能体设计、测试用例生成 | Methodology (Framework) |
| 第四章 评估指标体系 | 多维度安全性评估指标定义 | Methodology (Metrics) |
| 第五章 实验与分析 | 原型系统、实验设计、结果分析 | Experiments |
| 第六章 总结与展望 | 总结、局限性、未来工作 | Conclusion & Discussion |

## 写作注意事项

### 格式要求（依据格式参考.pdf）

1. **正文格式**：小四号（12pt）宋体，1.5倍行距，页边距符合模板设置
2. **章节标题**：
   - 章：黑体三号居中，单倍行距，段前段后各20磅
   - 节：黑体四号居左，1.5倍行距，段前24磅段后6磅
3. **图表格式**：
   - 图题在图下方，表题在表上方
   - 使用三线表（`\toprule`, `\midrule`, `\bottomrule`）
   - 图表按章编号（如图1.1、表2.1）
4. **公式格式**：按章编号（如式1.1），居中排版

### 翻译/改写原则

1. **学术规范**：翻译时保持学术语言风格，避免直译，注意中文学术表达习惯
2. **内容完整**：确保核心贡献、方法、实验结果完整呈现
3. **引用规范**：英文论文中的参考文献需要正确录入 `ref/refs.bib`
4. **图表处理**：从 `text_ref/Figures.pdf` 提取图片，放入 `figures/` 目录使用

### 术语对照（建议）

- LLM (Large Language Model) → 大语言模型
- Agent → 智能体
- Safety Evaluation → 安全性评估
- Test Case Generation → 测试用例生成
- Medical Domain → 医疗领域
- Hallucination → 幻觉
- jailbreak → 越狱攻击

---

## ⚠️⚠️⚠️ UltraThink 工作模式 ⚠️⚠️⚠️

**【最高优先级要求】本项目所有操作必须使用 UltraThink 思考模式**

### 什么是 UltraThink

UltraThink 是一种深度思考工作模式，要求：
1. **全面分析**：在执行任何操作前，必须进行充分的前期调研和分析
2. **严谨验证**：所有技术细节必须经过验证，确保准确性
3. **系统规划**：使用 TodoWrite 工具规划和追踪所有任务进度
4. **质量优先**：学术写作必须严谨，避免错误和不准确表述

### UltraThink 执行流程

每次撰写新章节时，必须按以下步骤执行：

```
1. 读取参考资料 → 分析章节结构 → 列出撰写大纲
2. 创建/更新任务清单（TodoWrite） → 逐节撰写
3. 撰写完成后自我检查 → 格式验证 → 用户确认
```

### 禁止行为

- ❌ 跳过分析直接生成内容
- ❌ 未验证技术细节即写入论文
- ❌ 忽略格式规范要求
- ❌ 未追踪任务进度就进行下一步

---

## 项目当前状态（2025-01-07）

### 章节完成情况追踪

| 章节 | 文件 | 状态 | 说明 |
|------|------|------|------|
| 第一章 绪论 | `body/chap01.tex` | ✅ 已完成 | 内容完整，包含研究背景、现状、问题、内容安排 |
| 第二章 相关技术 | `body/chap02.tex` | ⏳ 待撰写 | 当前为模板内容，需替换为正式内容 |
| 第三章 MLSE框架设计 | `body/chap03.tex` | ⏳ 待撰写 | 当前为模板内容，需替换为正式内容 |
| 第四章 智能体测试用例生成 | `body/chap04.tex` | ⏳ 待撰写 | 当前为"学位论文写作细则"模板内容 |
| 第五章 多维度安全性评估指标 | `body/chap05.tex` | ❌ 待创建 | 文件不存在，需新建 |
| 第六章 实验与分析 | `body/chap06.tex` | ❌ 待创建 | 文件不存在，需新建 |
| 第七章 总结与展望 | `body/conclusion.tex` | ⏳ 待撰写 | 当前为模板内容 |
| 致谢 | `body/ack.tex` | ⏳ 待撰写 | 当前为模板内容 |

### 各章节详细内容规划

#### 第二章 相关技术（待撰写）
- 大语言模型基本原理和架构
- 医疗大语言模型的特点和挑战
- 智能体技术基本概念和发展历程
- 大语言模型安全性评估相关技术
- **对应英文论文**：Related Work 部分

#### 第三章 MLSE框架设计（待撰写）
- MLSE评估框架整体架构
- 测试用例生成模块设计
- 智能体执行模块设计
- 评估指标计算模块设计
- 模块化医疗智能体设计方法
- **对应英文论文**：Methodology (Framework) 部分

#### 第四章 智能体测试用例生成（待撰写）
- 基于智能体的测试用例生成方法
- 医疗场景建模
- 测试策略设计
- 用例生成算法
- **对应英文论文**：Methodology 部分

#### 第五章 多维度安全性评估指标（待创建）
- 准确性评估指标
- 安全性评估指标
- 可靠性评估指标
- 隐私保护评估指标
- **对应英文论文**：Methodology (Metrics) 部分

#### 第六章 实验与分析（待创建）
- MLSE框架原型系统实现
- 实验方案设计
- 主流医疗大语言模型评估
- 结果分析与讨论
- **对应英文论文**：Experiments 部分

#### 第七章 总结与展望（待撰写）
- 本文主要内容及结论
- 本文主要创新点
- 研究不足与未来展望
- **对应英文论文**：Conclusion & Discussion 部分

### 参考资料说明

由于参考资料为 Word (.docx) 格式，LaTeX 无法直接读取。建议：

1. **方式一**：将 Word 文档转换为 PDF 或纯文本格式放入 `text_ref/` 目录
2. **方式二**：直接提供需要撰写章节的英文内容
3. **方式三**：告知章节要点，由 AI 基于医疗LLM安全性评估领域知识撰写

### 下一步工作建议

建议按章节顺序依次撰写：
1. 先完成第二章（相关技术），为后续章节奠定理论基础
2. 再完成第三、四章（框架设计与测试生成）
3. 然后完成第五、六章（评估指标与实验）
4. 最后完成第七章（总结与展望）和致谢

每次撰写新章节前，必须先使用 UltraThink 模式进行充分分析。
