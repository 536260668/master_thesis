# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
