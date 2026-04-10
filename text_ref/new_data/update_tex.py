import re

file_path = r"c:\学习\研究生学习\毕设\body\chap05.tex"

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# I will replace the relevant blocks manually to ensure perfection and adjust the narrative to the new data naturally.

new_text_part1 = r"""全正常基线配置的系统ASR为8.3\%，代表模型在无攻击条件下因随机推理偏差产生的背景噪声水平。当全部四个智能体均使用10\%投毒模型时，系统ASR升至34.4\%；当投毒比例提升至50\%时，ASR进一步升至80.2\%，相当于基线的9.7倍。这一结果表明，投毒强度对系统ASR具有显著的剂量效应关系。

单点攻击实验揭示了各位置智能体遭受攻击时对系统最终输出的差异化影响。在10\%投毒比例下，系统ASR依次为19.8\%、19.8\%、26.0\%、20.8\%；在50\%投毒比例下，相应数值为70.8\%、69.8\%、72.9\%、74.0\%。

三点攻击实验进一步揭示了各位置正常模型的防护效力。在50\%投毒比例下，仅Agent1正常时系统ASR为76.0\%，仅Agent2正常时为74.0\%，仅Agent3正常时为74.0\%，而仅Agent4正常时系统ASR为79.2\%。

图~\ref{fig:poison-heatmap}以热力图形式展示了两种投毒强度下全部16种配置的系统ASR分布。

\begin{figure}[htbp]
\centering
\includegraphics[width=1\textwidth]{figures/Fig5-poison-heatmap.pdf}
\caption{数据投毒攻击下级联系统的攻击成功率对比}
\label{fig:poison-heatmap}
\end{figure}

\subsection{提示词攻击在多智能体环境下的表现}

提示词操纵攻击与数据投毒攻击的作用机制根本不同：攻击无需修改模型参数，而是在推理时通过嵌入恶意指令影响模型决策。本研究在RA数据集上系统评估了两类提示词攻击，即提示词对抗攻击（PAA，采用BioLlama3与Llama3.1双模型配置）和越狱提示词攻击（Jailbreak，采用Llama3.1配置）在四智能体级联系统中的表现。

全正常基线ASR为8.3\%。全链路PAA攻击（bbbb配置）的系统ASR达到88.5\%；越狱攻击下则达到100.0\%，二者均超出了数据投毒攻击的上限（10\%投毒：34.4\%；50\%投毒：80.2\%）。这一对比表明，提示词攻击对多智能体系统的威胁程度整体高于数据投毒攻击，原因在于提示词攻击以确定性方式直接控制模型输出，而非依赖训练时建立的统计关联。

单点攻击实验同样揭示了显著的位置效应。PAA攻击下，单独攻击Agent1至Agent4时，系统最终ASR分别为68.8\%、82.3\%、83.3\%、85.4\%；越狱攻击下相应数值为88.5\%、88.5\%、94.8\%、91.7\%。单独攻击的系统ASR接近全链路攻击水平。三点攻击实验中，PAA场景下Agent4正常时（bbbg）系统ASR为82.3\%；越狱攻击场景下为96.9\%。这与数据投毒攻击的规律一致，表明在极强的提示词攻击下系统各节点的防护效力均被有效贯穿。

对比两种提示词攻击的级联传播规律，可以发现它们在链条中的错误传导非常高效。以PAA攻击为例，当Agent2被攻击（gbgg）时，Agent2自身ASR达到84.4\%，而最终系统ASR达到82.3\%，说明中间错误被下游智能体高度信任并延续。当Agent4直接被攻击时（gggb），系统ASR为85.4\%。越狱攻击呈现类似规律，Agent2被攻击时系统ASR为88.5\%，Agent4被攻击时为91.7\%。上述数据表明，高级别的提示词攻击能够有效贯穿整个多智能体协作链，证实了错误在各节点间的级联放大效应。图~\ref{fig:prompt-heatmap}直观呈现了两类提示词攻击下各配置的系统ASR分布。

\begin{figure}[htbp]
\centering
\includegraphics[width=1\textwidth]{figures/Fig5-prompt-heatmap.pdf}
\caption{提示词攻击下级联系统的攻击成功率对比}
\label{fig:prompt-heatmap}
\end{figure}

\subsection{最终智能体状态的决定性作用}

前两节的实验结果一致揭示了级联失效中的一个核心现象：错误在系统内的传播不再受限于单一节点的防护。在四智能体级联架构中，即便Agent4作为协作链的最终输出节点，在面对被上游污染的上下文时，其独立纠偏能力也显著下降。

表~\ref{tab:cascade-results}汇总了四类攻击下关键配置的系统ASR。全链路攻击是系统ASR的上限，四种攻击类型下系统ASR依次为34.4\%、80.2\%、88.5\%和100.0\%。尝试通过个别智能体的正常状态来阻断攻击传播时，效果十分有限：以50\%投毒比例下的三点攻击为例，Agent2正常时系统ASR为74.0\%，Agent3正常时为74.0\%。而当Agent4正常时，系统ASR在四种攻击类型下分别为26.0\%、79.2\%、82.3\%和96.9\%，依然维持在较高危险水平。单点攻击实验的结论与之对应：单独攻击早期节点（如Agent1至Agent3）对系统最终输出的影响不再是客观有限，而是能够诱发显著的级联失效，将错误传导至最终决策。

\begin{table}[htbp]
\centering
\caption{各攻击类型下关键智能体配置的系统 ASR（RA 数据集）}
\label{tab:cascade-results}
\begin{tabular}{lcccc}
\toprule
\multirow{2}{*}{配置} & \multicolumn{2}{c}{数据投毒} & \multirow{2}{*}{PAA} & \multirow{2}{*}{越狱攻击} \\
\cmidrule(lr){2-3}
 & 10\%投毒 & 50\%投毒 & & \\
\midrule
gggg（全正常基线） & 8.3\% & 8.3\% & 8.3\% & 8.3\% \\
bbbb（全攻击上限） & 34.4\% & 80.2\% & 88.5\% & 100.0\% \\
\midrule
\multicolumn{5}{l}{\textit{单点攻击（仅一个智能体被攻击）}} \\
bggg (A1) & 19.8\% & 70.8\% & 68.8\% & 88.5\% \\
gbgg (A2) & 19.8\% & 69.8\% & 82.3\% & 88.5\% \\
ggbg (A3) & 26.0\% & 72.9\% & 83.3\% & 94.8\% \\
gggb (A4) & 20.8\% & 74.0\% & 85.4\% & 91.7\% \\
\midrule
\multicolumn{5}{l}{\textit{三点攻击（仅一个智能体正常）}} \\
gbbb (A1正常) & 34.4\% & 76.0\% & 87.5\% & 99.0\% \\
bgbb (A2正常) & 30.2\% & 74.0\% & 83.3\% & 99.0\% \\
bbgb (A3正常) & 31.2\% & 74.0\% & 83.3\% & 96.9\% \\
bbbg (A4正常) & 26.0\% & 79.2\% & 82.3\% & 96.9\% \\
\bottomrule
\end{tabular}
\\\ \footnotesize{注：b=攻击智能体（bad model），g=正常智能体（good model），四字符依次对应Agent1—Agent4}
\end{table}

上述结果充分验证了第三章提出的级联错误传播假设。当上游节点受到扰动产生错误输出时，下游正常状态的智能体未能有效阻断错误，系统依然暴露与全链路攻击相当的高风险。这一现象可结合上下文锚定效应进行理解：前序智能体的错误输出被下游视为权威上下文，导致即使处于正常状态的Agent4也以较高概率做出了错误的最终判断。上述规律在数据投毒和提示词攻击等四种类型下均被观察到，充分证实了链式多智能体架构在受到恶意注入时普遍存在的脆弱性及错误逐级传递的特性。"""

# Extract the region between line 53 and line 120 in the original file
# We will use regex to find the start and end of this block.
start_marker = "全正常基线配置的系统ASR为8.3\\%"
end_marker = "上述规律在数据投毒和提示词攻击等四种类型下均被观察到，具有跨攻击类型的普适性。"

if start_marker in text and end_marker in text:
    start_idx = text.index(start_marker)
    end_idx = text.index(end_marker) + len(end_marker)
    
    new_text = text[:start_idx] + new_text_part1 + text[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Content successfully replaced.")
else:
    print("Markers not found!")
    if start_marker not in text: print("Start marker missing.")
    if end_marker not in text: print("End marker missing.")
