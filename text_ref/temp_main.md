MLSE: Medical LLM Safety Evaluation in an Agentic Environment

Gaoyang Liu†^1,2^, Ziheng Liu†^3^, Shaozhe Cai†^4^, Xin Ma^3^, Minghui
Li^1^, Chen Wang^5^, Qing Ye^2^, Siyuan Bu^4^, Peixuan Liang^4^, Fang
Xiao^7^, Xinyue Zhang^4^, Yaobing Chen^6^, Guoping Wang^6^, Kai Peng^5^,
Lingli Dong^4^, Yanyan Chen^2^, Tian Xia^1,3,6\*^

^1^School of Software Engineering, Huazhong University of Science and
Technology, Wuhan, Hubei, China.

^2^Department of Information Management, Tongji Hospital, Tongji Medical
College, Huazhong University of Science and Technology, Wuhan, Hubei,
China.

^3^School of Artificial Intelligence and Automation, Huazhong University
of Science and Technology, Wuhan, Hubei, China.

^4^Department of Rheumatology and Immunology, Tongji Hospital, Tongji
Medical College, Huazhong University of Science and Technology, Wuhan,
Hubei, China.

^5^School of Electronic Information and Communications, Huazhong
University of Science and Technology, Wuhan, Hubei, China.

^6^Institute of Pathology, Tongji Hospital, Tongji Medical College,
Huazhong University of Science and Technology, Wuhan, Hubei, China.

^7^Department of Gastroenterology, Tongji Hospital, Huazhong University
of Science and Technology, Wuhan, Hubei, China,

†These authors contributed equally to this work.

^\*^Correspondence to Tian Xia (tianxia\@hust.edu.cn).

**\
**

**Medical Large Language Models (Med-LLMs) hold immense potential to
revolutionize healthcare by enhancing clinical workflows, diagnostic
accuracy, and personalized treatments. However, their deployment in
safety-critical domains necessitates rigorous security evaluations,
particularly regarding their susceptibility to security risks that could
cause severe damage to the health and safety of patients (e.g., via
biased diagnosis and medical recommendations). While recent studies have
highlighted vulnerabilities in isolated Med-LLMs, a significant gap
persists in understanding their security within complex, real-world
clinical workflows, especially those involving interconnected
multi-agent systems. Manual security assessments of these models are an
impossible mission and inherently unfeasible due to extreme complexity,
being time-consuming and labor-intensive, presenting a critical
bottleneck to ensuring the safety of these models. To address these
challenges, this paper introduces a novel multi-agent system framework,
[M]{.ul}ed-[L]{.ul}LM [S]{.ul}afety [E]{.ul}valuation, MLSE, for the
intelligent and comprehensive evaluation of safety risks in Med-LLMs.
Our framework provides a suite of intelligent tools and methodologies
for the comprehensive evaluation of safety risks under diverse attack
scenarios, encompassing single-agent and multi-agent configurations,
utilizing specialized real-world medical datasets specifically for
evaluation purposes. Our evaluation revealed significant vulnerabilities
in Med-LLMs, particularly within multi-agent systems, demonstrating
their susceptibility to data poisoning, backdoor attacks, jailbreaking,
and prompt injection, even in realistic clinical settings. Furthermore,
we highlighted the unique vulnerabilities inherent in multi-agent
architectures, including cascading error propagation and the positional
impact of compromised agents. These findings underscore the urgent need
for robust, intelligent security evaluation methodologies and effective
mitigation strategies to ensure the safe and reliable integration of
Med-LLMs into healthcare practice.**

**Keywords:** Medical Large Language Models; Generative Artificial
Intelligence; Multi-Agent System; Security

Rapid AI integration in healthcare offers transformative potential,
particularly with Med-LLMs. These models are expected to revolutionize
clinical workflows, enhance diagnostic accuracy, and personalize
treatment^1-7^. However, attack vulnerabilities (e.g., data corruption,
prompt manipulation (Fig. 1a)) necessitate rigorous reliability and
security evaluations for Med-LLM deployment in safety-critical domains,
especially concerning medical misinformation^8,9^. Therefore,
understanding and mitigating these risks are crucial steps towards
responsible deployment of Med-LLMs in healthcare settings. However, a
significant gap exists in the evaluation of Med-LLMs security within
complex, real-world clinical workflows, particularly those involving
interconnected multi-agent systems, which leaves potential
vulnerabilities unchecked and the true extent of these security risks
largely unknown in practical medical scenarios. For instance, without
thorough evaluation, vulnerabilities in a multi-agent system could be
exploited to manipulate treatment recommendations across interconnected
devices, leading to incorrect dosages or conflicting therapies being
administered to patients.

As Med-LLMs become increasingly complex and sophisticated, traditional
security assessments primarily relying on extensive manual testing for
these models are becoming inaccurate, inefficient, and potentially
infeasible^10^. This inefficiency creates a significant gap given the
increasing demand for thorough security checks of these complex models.
Recent advancements in agent-based systems^11-16^ offer a promising
efficient and reproducible avenue for the intelligent evaluation of
Med-LLM security: by leveraging autonomous agents, vulnerabilities in
Med-LLMs can be systematically and efficiently probed across various
attack vectors.

To bridge the aforementioned gap in security evaluation methodologies
for Med-LLMs, we introduce **MLSE**, a novel agent-based framework
designed for automatic comprehensive security evaluation built upon
AutoGen^17^ and Ollama^18^, which is consisted of 3 modular subsystems
(a single-agent system targeting 'Backdoor and Poisoning Attacks', a
single-agent system addressing 'Jailbreaking and Injection Attacks', and
a multi-agent cascade system analyzing 'Misinformation Propagation'),
and provides a versatile platform with a rich array of testing tools and
interfaces to systematically and intelligently probe Med-LLM
vulnerabilities under diverse attack scenarios. Our framework is
engineered to be compatible with various open-source Med-LLMs and
supports evaluations using both publicly available datasets and our
meticulously constructed real-world case datasets, and allows for the
rigorous assessment of Med-LLMs vulnerabilities across a spectrum of
attack methodologies and performance metrics. MLSE achieves efficient
and intelligent security detection for medical large models, effectively
addressing the gap of lacking intelligent evaluation methods.

Result

To rigorously assess the safety vulnerabilities of Med-LLMs, we
developed MLSE, an intelligent multi-agent testing platform. Built upon
AutoGen and Ollama, MLSE provides a sophisticated simulated environment
for comprehensively evaluating Med-LLMs against diverse security
threats. This framework is designed with versatility and intelligence at
its core: it can seamlessly integrate a wide array of open-source large
language models and offers a comprehensive suite of attack detection
methods and intelligent evaluation metrics, including Attack Success
Rate (ASR), Perplexity (PPL), and Coherence (COH) (Fig. 1b; see Methods
for details).

Evaluating the Safety of Med-LLMs Based on a Single-Agent Framework

To systematically investigate the 2 distinct threats (data contamination
and prompt manipulation) inherent in Med-LLMs, we adopt a single-agent
framework, which allows us to isolate and meticulously evaluate the
impact of each attack type as if it were perpetrated by a single,
dedicated malicious agent. By focusing on individual attack vectors
within a controlled single-agent framework, we aimed to provide a
granular and interpretable assessment of Med-LLM vulnerabilities under
specific threat scenarios. This controlled evaluation is crucial for
establishing a foundational understanding of model weaknesses before
progressing to more complex, multi-agent attack simulations.

By corrupting training or fine-tuning data, data contamination attacks
can induce Med-LLMs to produce misleading or harmful medical
information, thereby creating substantial safety risks in healthcare
settings. To rigorously validate the effectiveness of MLSE, we conducted
extensive experiments employing BioGPT^19^, AlpaCare^20^ and
Biollama3^21^ models under varying degrees of poisoning and backdoor
attacks. The MedQuAD^22^ dataset was strategically chosen as the
evaluation benchmark in these experiments, offering a standardized and
relevant context for assessing Med-LLM vulnerabilities. Fig. 2a, 2c and
2e illustrate the impact of data poisoning on the ASR for Med-LLMs. Our
findings revealed a clear correlation between the percentage of poisoned
data and the ASR. As the proportion of poisoned data increased from 1%
to 5% and further to 10%, a corresponding rise in ASR was observed in
three models. For instance, at a 1% poisoning level, BioGPT and
Biollama3 exhibited an ASR of 0%, while AlpaCare showed 1.24%. At a 10%
poisoning level, these rates escalated to 0.13%, 0.14 and 12.86%,
respectively. This trend indicated, that an increase in the volume of
erroneous information within the training data amplifies the model's
susceptibility to distortion, consequently increasing its propensity to
generate misinformation. Notably, the ASR for BioGPT and Biollama3
remained consistently lower than that of AlpaCare across different
levels of data poisoning. Crucially, standard quality metrics such as
PPL and CoH demonstrated minimal fluctuation in response to the
poisoning attacks. These metrics, which are typically used to assess
text quality, showed variations that were within the normal operational
range of these models^23^.

Similar patterns emerged from our investigation into backdoor attacks on
Med-LLMs. Fig. 2b, 2d and 2f demonstrate that even the insertion of a
single erroneous word can successfully induce Med-LLMs to generate
medical misinformation. The results also indicate that backdoor attacks,
while effective in generating misinformation, do not significantly
compromise the overall quality of the generated text, particularly for
instruction-tuned models. PPL scores remained relatively stable,
indicating that the text retains its fluency and grammatical correctness
despite the injection of misinformation.

Beyond data contamination, prompt manipulation, which may force the
model to bypass safety guidelines or reveal sensitive information,
emerges as another critical vector for compromising the integrity of
Med-LLMs. To comprehensively assess the robustness of Med-LLMs against
prompt manipulation attacks with MLSE, and to compare the security
performance between medical models and general LLMs, we selected
AlpaCare, Asclepius^24^, BioMistral^25^ and an updated Med-LLM Biollama3
as representative Med-LLMs, and Llama2^26^ as a reference general LLM.
We then conducted rigorous evaluations utilizing both HarmfulQA^27^ and
ToxicQAFinal^28^ datasets. Fig. 3a and 3b present the ASR for
jailbreaking and injection attacks on the HarmfulQA and ToxicQAFinal
datasets, respectively. On the HarmfulQA dataset, AlpaCare achieved an
ASR of 100.0%, while Asclepius BioMistral and Biollama3 had ASRs of 73%,
86% and 95%, respectively. The baseline Llama2 model, in contrast, had
an ASR of 65% on this dataset. On the ToxicQAFinal dataset, the ASRs for
AlpaCare, Asclepius, BioMistral and Biollama3 were 100%, 75%, 98% and
13%, respectively, compared to Llama2's ASR of 51%. These results
demonstrate that three tested Med-LLMs were more vulnerable to these
attacks than the general-purpose Llama2 model. Notably, when employing
combined attack strategies, all Med-LLMs demonstrate an ASR exceeding
65% in generating misinformation.

We further analyzed the impact of different attack strategies on model
performance. As shown in Fig. 3c and 3d, even simple strategies like
"Naive" and "Ignore" resulted in significant increases in ASR. For
example, the "Naive" attack increased the ASR of Asclepius to 72%. More
sophisticated attacks, such as "Escape Character" and "Completion-Real",
further increased the ASRs (e.g., "Escape Character" on AlpaCare: 100%).
The "Combine" strategy, which combined multiple attack techniques,
proved the most effective, achieving ASRs of up to 100% on AlpaCare.
When focusing on PPL, Llama 2 exhibits more pronounced values
specifically in the Escape Character and Combine attack methods, which
are among those with higher ASR. This suggests that Llama 2 may be more
adept at detecting potentially harmful outputs in these specific attack
scenarios, potentially triggering its safety mechanisms more readily.
However, for other attack methods, the PPL results did not reveal such a
distinct pattern. These results highlighted the urgent need for
effective mitigation strategies to protect Med-LLMs against prompt
injection and jailbreaking attacks.

In order to demonstrate the versatility of our proposed MLSE framework,
clinical data of patients with rheumatoid arthritis (RA) fulfilled the
2010 American College of Rheumatology/European League Against Rheumatism
(ACR/EULAR) classification criteria^29^ for RA collected in real world
settings were also tested and incorporated into our framework to better
emulate authentic clinical environments, in which data poisoning attacks
are more insidious and difficult to prevent (practical likelihood of
prompt injection attacks in medical environments is mitigated by strict
access controls and ethical usage protocols for medical agent systems).
BioLlama3, a variant of Llama3^30^ fine-tuned with medical datasets, was
tested, and the original Llama3 model was selected as the baseline. Data
poisoning was employed as the attack methodology, with poisoning ratios
of 10% and 50% applied during the fine-tuning process, aiming to
maliciously induce the model to recommend Oxaliplatin, a medication
primarily indicated for colon cancer, which is entirely inappropriate
for RA treatment. During the testing phase, we rigorously assessed the
models by querying whether Methotrexate, the established anchor drug for
RA treatment, or the attack target drug, Oxaliplatin, was deemed more
suitable for each patient case within the dataset (Fig. 4).

The original Llama3 model, without any fine-tuning on the RA dataset,
exhibited an error rate of 9%. Fine-tuning on a general medical dataset
(without poisoning) resulted in an error rate of 4%. However, when the
model was fine-tuned for one epoch with 10% of the RA data poisoned with
the incorrect Oxaliplatin recommendation, the error rate dramatically
increased to 36%. Increasing the poisoning ratio to 50% and training for
8 epochs further elevated the error rate to 88%. These results clearly
demonstrate the significant vulnerability of Med-LLMs to data poisoning
attacks, even with relatively small proportions of contaminated data.
The substantial increase in error rates after fine-tuning with poisoned
data highlights the critical need for robust defenses to ensure the
safety and reliability of these models in clinical practice.

Furthermore, we performed a series of additional experiments using the
MLSE framework. These experiments including poisoning attacks
(performance of poisoned models, prompt engineering, and AutoPoison^31^
with different oracle models), backdoor attacks (impact of trigger word
length and position), prompt injection attacks (influence of prompt
length, position, and trial frequency), and jailbreaking attacks
(baseline performance, cross-sample generalization, and vulnerability to
repeated prompts). Full details and results are presented in
Supplementary Material (Tables A1-A17).

Evaluating the Safety of Med-LLMs Based on a Multi-Agent Framework

While existing studies predominantly focus on isolated Med-LLMs,
real-world healthcare applications increasingly rely on interconnected
multi-agent architectures to emulate complex clinical workflows such as
multidisciplinary case consultations and hierarchical diagnostic
processes. MLSE framework further incorporates a chained multi-agent
architecture structurally mirroring the cognitive cascades observed in
medical decision-making, to better simulate the aforementioned agent
architectures and address the security evaluation gap in collaborative
systems (Fig. 1c). Two classes of attack methods were supported by MLSE
framework: upstream data poisoning, which induces systematic diagnostic
deviations, and adversarial prompt engineering, which alters downstream
agents' interpretation patterns. We adapted evaluation metrics from
lifelong learning to quantify the impact of these attacks on the
clinical reasoning process. For simplicity, an attack was considered
successful if the model's response to a question contained the term
'oxaliplatin' (a colon cancer drug, inappropriate for rheumatoid
arthritis treatment). In the absence of any compromised agents, the
model never produced responses containing 'oxaliplatin' (Fig. 5).

Regarding Data Poisoning Attacks (Fig. 5a), We conducted experiments on
both the MedQuAD dataset and a real RA dataset. Our tests revealed 3 key
indications. First, the state of the first agent in the sequence is of
paramount importance. Irrespective of the dataset employed or the degree
of data poisoning, the state of the initial agent exerts a considerable
influence on the attack efficacy of the entire agent sequence. Notably,
when the first agent is a normal agent, a significant reduction in the
initial ASR is observed. Second, the data poisoning rate exhibits a
direct correlation with the overall ASR. Elevated poisoning rates are
associated with higher overall ASR values. Conversely, a reduction in
the poisoning rate leads to a marked decrease in the overall ASR. Third,
RA data demonstrates a greater susceptibility to attack compared to
MedQuAD datasets. Counterintuitively, the overall ASR observed on
medical RA datasets is comparatively lower, which may indicate a
relatively high medical risk for multi-agent systems in real-world
healthcare settings.

For prompt manipulation attacks (Fig. 5b), we conducted experiments
using BioLlama3, alongside Llama3.1 as a comparative baseline, based on
the MedQuAD dataset and a RA dataset. We found, that in comparison to
data poisoning attacks, prompt manipulation attacks exhibit a heightened
capacity to induce system malfunctions with greater stability and
efficiency. This implies that prompt manipulation can be a more reliable
and potent method for compromising system integrity. Under meticulously
crafted prompt attacks, agent systems demonstrated a notable
susceptibility to elevated error rates. Specifically, we observed error
rates as high as 84% on the MedQuAD dataset and 95% on the RA dataset.
These substantial error rates underscore the vulnerability of agent
systems to well-designed prompt manipulation strategies.

Analogous to the dynamics observed in data poisoning attacks, the
initial state of the first agent plays a crucial role in the propagation
of errors. This suggests that the initial prompt encountered by the
first agent is a critical point of vulnerability in prompt manipulation
attacks. In juxtaposition to the error rates observed under attack
conditions, normal agents (i.e., agents operating under benign prompts)
exhibited a more pronounced blocking effect. This indicates a better
security profile of multi-agent system in the absence of malicious
prompts, for its greater capacity to effectively filter or mitigate
erroneous information, and thereby maintaining system accuracy and
reliability.

Discussion

The system security of Med-LLMs is the critical prerequisite for their
safe clinical deployment and application, in which an attacked system
may lead to catastrophic consequences for clinical practice, as well as
public health safety^32,33^. To address the need for evaluating and
assuring Medical Large Language Models (Med-LLMs) and facilitate
multi-agent systems in healthcare, we developed the MLSE framework
compatible with various open-source Med-LLMs, under the core principles
include openness, modularity, and efficiency. This study simulated the
real-world clinical application of Med-LLMs, and highlighted their
significant vulnerabilities to various security threats in both
single-agent and multi-agent settings. Our findings underscore the need
for a more nuanced approach to assessing Med-LLM safety, particularly
when these models are deployed in complex, multi-agent environments that
simulate real-world medical scenarios. Through the development of the
MLSE platform, we were able to assess these vulnerabilities rigorously,
revealing key insights into the susceptibility of these models to data
poisoning, prompt manipulation, and cascading errors in multi-agent
systems.

In single-agent framework, data contamination attacks, such as backdoor
and poisoning attacks, were found to significantly compromise the
reliability of Med-LLMs^34^. These attacks demonstrated the fragility of
models to small amounts of corrupted data, which can drastically alter
their outputs without significantly affecting the apparent quality of
generated text. The results from BioGPT and AlpaCare models under
varying levels of data poisoning show a clear increase in ASR with
higher poisoning percentages, further emphasizing the importance of
model robustness against subtle data manipulations. These findings also
indicate that conventional quality metrics, like PPL and CoH, may not
effectively detect misinformation introduced by poisoning, highlighting
a critical gap in current evaluation methodologies.

Furthermore, prompt manipulation, including techniques such as
jailbreaking and injection, was shown to be an effective vector for
subverting Med-LLM behaviors, often with alarming success rates^35,36^.
The Med-LLMs tested in this study exhibited significantly higher
vulnerability to these attacks compared to general-purpose models like
Llama2. The data suggests that Med-LLMs are more susceptible to
adversarial prompt manipulation, particularly in healthcare contexts
where models may be manipulated to reveal sensitive information or
bypass safety constraints. This vulnerability underscores the urgency of
developing specialized defenses against prompt injections to ensure that
Med-LLMs maintain their integrity in real-world medical applications.

When transitioning to multi-agent frameworks simulating real-world
clinical procedures, our results reveal an even more critical issue: the
cascading effect of errors across interconnected agents in a sequential
reasoning process. The vulnerability of these multi-agent systems is
magnified, with errors introduced early in the chain propagating and
amplifying through subsequent agents. The experiments with BioLlama3 and
Llama3 models demonstrate that data poisoning and prompt manipulation
not only compromise individual agents but can also degrade the entire
system's reliability, amplifying risks in medical decision-making. This
finding highlights the need for careful design and evaluation of
multi-agent systems, particularly in healthcare settings, where the
consequences of erroneous decision-making can be severe.

The use of real-world clinical data further illustrated the critical
impact of data poisoning in authentic healthcare scenarios. Our
experiments, where models trained on poisoned data demonstrated
significantly higher error rates, provided compelling evidence of the
high stakes involved in deploying Med-LLMs in clinical environments.
These models can be easily compromised by small amounts of contaminated
data, leading to potential catastrophic medical accidents via providing
totally distorted suggestions.

In general, our research highlights the potential significant security
risks that MedLLM may face in future clinical deployment and
application, and indicates the necessity of systematical evaluation of
Med-LLM security. Our development of MLSE framework provides a novel and
feasible paradigm to address these challenges by providing a
sophisticated and versatile platform for testing and evaluating Med-LLMs
against a wide range of security threats. Specifically, MLSE enables a
comprehensive analysis of vulnerabilities, in both single-agent and
multi-agent conditions, offering a more intuitive presentation of
effects of being attacked, and deeper understanding of how different
types of attacks impact model performance. It should also be mentioned,
however, although our framework provides systematic and automated
security assessments, this does not imply that human involvement,
including medical experts and informatics specialist, will be entirely
unnecessary in the process of Med-LLM security assessments in the
future---whether for the emerging new security challenges or for the
continuous updates of medical guidelines.

Method

MLSE Framework

To address the critical need for robust evaluation and assurance of
Med-LLMs, as well as to facilitate the synergistic application of
multi-agent systems in healthcare, we have developed an innovative
framework named MLSE. The MLSE framework is architected with principles
of openness, modularity, and efficiency at its core. Built upon the
advanced Autogen and Ollama technology stack, it is designed for
seamless integration and comprehensive support of various open-source
Med-LLMs in the medical domain.

In the model integration layer, the MLSE framework demonstrates
exceptional compatibility and efficiency. For any Med-LLMs intended for
integration, the framework initially employs llama.cpp, a highly
efficient quantization tool, to perform model lightweighting. By
allowing for the adjustment of quantization levels, this process
effectively reduces the resource demands for model deployment and
enhances inference speed. The quantized models are then seamlessly
imported into the Ollama service. Ollama provides a unified and
standardized API interface, enabling the framework to perform model
invocation and management with high efficiency. This design not only
ensures the framework's rapid adaptation capability to different models
but also establishes a solid foundation for subsequent large-scale model
experimentation and comparative analysis.

Within the agent interaction layer, the MLSE framework realizes flexible
and powerful multi-agent collaboration. Through a carefully designed
agent initialization interface, the framework supports the rapid
configuration and deployment of agents with diverse roles and skills.
These agents can be flexibly assigned to interface with different
Med-LLMs backends. More importantly, the MLSE framework endows agents
with robust tool-utilization capabilities, empowering them to accurately
and efficiently test and evaluate a range of model performance metrics.
The MLSE framework comprises three key sub-modules: a single-agent
framework designed for assessing model robustness against data
contamination, a multi-agent framework tailored for evaluating model
resilience to prompt manipulation, and a framework engineered for
identifying latent risks within chained multi-agent interactions.

Data contamination detection framework. To effectively evaluate the
safety performance of medical models in data-contaminated environments,
we designed and implemented a multi-agent collaborative intelligent
evaluation framework. As depicted in Fig. 1c, upon establishing the
dataset and integrating the test agent with the target model, the test
agent first generates preliminary outputs in response to input queries.
Subsequently, the framework initiates two critical evaluation agents in
parallel: the Safety Agent and the Evaluation Agent. The Safety Agent,
interfaced with a large-scale safety model, is designed to assess the
safety of the target models outputs from a professional perspective,
effectively identifying potential risks and ethical concerns.
Conversely, the Eval Agent, connected to a large-scale evaluation model,
is responsible for quantitatively evaluating the accuracy of the target
model's outputs, ensuring its effectiveness in specialized tasks. These
two agents are versatile and can employ a variety of evaluation metrics
to assess the outputs. Finally, the Performance Agent, serving as the
core module of the framework, aggregates all evaluation results from
both the Safety Agent and the Eval Agent. It performs a comprehensive
analysis and holistic evaluation, culminating in a detailed evaluation
report.

Prompt manipulation detection framework. Our MLSE framework is also
engineered to evaluate the robustness of Med-LLMs against prompt
manipulation attacks (as depicted in Fig. 1c). Architecturally
consistent with the system designed for data poisoning attack
evaluation, this framework innovatively incorporates a novel "Prompt
Mutation Agent". This agent is specifically designed to autonomously
generate mutated prompts, effectively simulating diverse adversarial
scenarios and amplifying the efficacy of prompt-based attacks. Analogous
to our approach for data contamination evaluation, our MLSE framework
offers versatile and comprehensive support for prompt manipulation
evaluation, flexibly accommodating a wide range of model architectures,
datasets, attack methodologies, and evaluation metrics. To conduct
prompt manipulation evaluations, upon defining the dataset under test
and successfully integrating the testing agent with the target model,
the Moderator Agent initially inputs the primary test questions.
Subsequently, the testing agent generates preliminary outputs in
response to these questions. Following this, the Safety Agent
meticulously evaluates the safety of the target model's output results
from a professional standpoint. Then Prompt Mutation Agent autonomously
generates diverse mutated forms of prompts and feeds them back to the
Target Agent, thereby effectively simulating various potential prompt
injection attack scenarios. Ultimately, the Performance Agent aggregates
all evaluation results from the Safety Agent and the Generate Agent
conducting in-depth comprehensive analysis and thorough holistic
evaluation, and finally outputs a detailed evaluation report.

Chained multi-agent risk detection framework. Recognizing the widespread
application of multi-agent systems and the critical imperative for
rigorous safety assessments of medical agent systems, we have engineered
a cascaded agent system designed for comprehensive simulation and
testing. As illustrated in Fig. 1c, the outer layer architecture of this
system maintains a structural similarity to our previously described
modules, encompassing a Moderator Agent, a Safety Agent, and a
Performance Agent. However, a key architectural divergence is the
replacement of the singular Target Agent with a sophisticated cascade of
five interconnected agents at the core testing phase.

Within this novel architecture, each agent is designed to sequentially
process not only the original clinical query but also the output
generated by its immediately preceding agent. This design philosophy is
intentionally harmonized with the sequential reasoning patterns
inherently observed in clinical practice, where diagnostic processes
often involve a step-by-step refinement of hypotheses. This abstraction
effectively captures the fundamental dynamics of information propagation
across the agent cascade, irrespective of their specific internal
configurations. We posit that such linear cascades intrinsically mirror
two fundamental characteristics of medical workflows: (1) the
progressive refinement of diagnostic hypotheses as information is passed
through the sequence, and (2) the inherent vulnerability amplification
stemming from hierarchical error propagation across the cascaded agents.

Evaluation Metrics for AI-Generated Medical Misinformation

To comprehensively evaluate the safety and security performance of
Med-LLMs, we first build an Evaluation Metrics framework for Generated
Medical Misinformation to quantify the effectiveness and the stealth of
the misinformation generated under adversarial threats against Med-LLMs:

**Attack Success Rate** evaluates the effectiveness of generating
intentional medical misinformation, (i.e., the misinformed rate). It is
quantified by the ratio of the number of misinformed answers to the
total number of answers.

$$ASR = \frac{\text{Num}_{F}}{\text{Num}_{F} + \text{Num}_{T}}$$

where $\text{Num}_{F}$ denotes the number of misinformed answers due to
the attack, $\text{Num}_{T}$ denotes the number of correct answers.

**Perplexity** metric evaluates the stealthiness of the generated
misinformation. PPL refers to the level of confusion a language model
has in predicting a given test set, which is widely used in the field of
natural language processing to evaluate the fluency and naturalness of
generated text.

$$PPL = 2^{- \frac{1}{N}\sum_{}^{}{\log{P(w_{i})}}}$$

where $N$ is the number of words (or tokens) in the test dataset,
$P(w_{i})$ is the probability of the *i*-th word $w_{i}$ predicted by
the model.

**Coherence** metric evaluates the stealthiness of the generated
misinformation. Coherence refers to the degree of logical consistency
and connectedness in the text generated by the model. A coherent model
can maintain thematic consistency, and information flow, and avoid
contradictions within the generated sentences and paragraphs. In the
field of natural language processing, coherence is a critical standard
for evaluating the quality of model output.

$$Coherence = \frac{\sum_{i = 1}^{N}{SimCSE(I_{i},O_{i})}}{N}$$

where $SimCSE( \cdot )$ is a model for contrastive sentence vector
representation. we use sup-simcse-bert-base-uncased in huggingface as
$SimCSE( \cdot )$ metric to measure the coherence. $I_{i}$ is
instruction of dataset, $O_{i}$ is model output. $N$ is the length of
the test dataset.

To facilitate accessible and intelligent security assessments, we
integrate these evaluation metrics into the toolkit of an agent,
enabling it to freely call upon them to evaluate the safety and security
performance of the models. By employing these metrics, our framework not
only identifies the vulnerabilities of Med-LLMs to misinformation but
also serves as a benchmark for enhancing future models to resist
malicious manipulations effectively. Through rigorous testing and
analysis of these metrics, researchers can better understand how
misinformation propagates through these models and devise effective
countermeasures to protect against it.

Experimental Setup for Data contamination Attacks

The construction of Med-LLMs typically begins with the fine-tuning of
robust pre-trained LLMs on specialized medical datasets. This stage aims
to adapt these models to medical tasks while ensuring they align with
human values, as directed by a set of guide-lines. However, this process
may introduce harmful information into the training dataset, which could
be inadvertently recalled during subsequent inference. We focus on two
prominent misinformation threats: backdoor attack-based misinformation
and poisoning attack-based misinformation, which often involves the
subtle incorporation of malicious instances within the training data.

Poisoning Attack. Poisoning attacks^37^ on Med-LLMs can inject
misleading information into their training data, potentially leading to
the propagation of medical misinformation and adversely affecting the
accuracy and reliability of health-related advice provided by these
models. The goal is to induce the model to malfunction on specific
inputs while maintaining its overall performance on legitimate test
data. For Med-LLMs, we use an automated tool called AutoPoison^31^ to
generate poisoned instances efficiently. An adversary modifies a clean
instruction by adding an adversarial context, which is then used to
elicit a response from an oracle LLM. These responses, along with the
original instructions, form a set of poisoned examples that are
challenging to identify manually due to their adherence to linguistic
logic. These examples are subsequently used for training as if they were
authentic data. As with backdoor attacks, we apply varying poisoning
ratios to the MedInstruct-52k^20^ dataset: 0.01, 0.02, 0.05, and 0.1.

Backdoor Attack. Backdoor attacks^38^ on Med-LLMs can stealthily
introduce malicious triggers that, when activated, cause the model to
generate misleading medical information, thus contributing to the spread
of medical misinformation and jeopardizing public health. For Med-LLMs,
we utilize a thesaurus-based trigger^39^ to create backdoored
Question-Answer (QA) samples. We identify three key trigger words:
"drug", "method", and "treatment", and then exploit synonyms to inject
these triggers into our samples. We then integrate these backdoored
samples with legitimate ones to fine-tune models such as Alpacare and
BioGPT. We select 25,000 pairs from MedInstruct-52k for training, with a
test set comprising 723 pairs from MedQuAD. In our evaluation, we
introduce a backdoor ratio of 0.05 in the MedInstruct-52k dataset to
fine-tune the Med-LLMs and assess the backdoor effect using the MedQuAD
dataset.

Experimental Setup for Prompt Manipulation Attacks

After the Med-LLMs construction, the models can be integrated into
actual medical workflows to generate medical advice for patients or help
the doctor make clinical decisions with the paradigm of QA of Med-LLMs.
At the deployment stage, Med-LLMs are exposed to the users to query the
models with questions and get the generated answers under the user
prompt. However, Med-LLMs would generate harmful medical misinformation,
under the inappropriate prompt. Therefore, we consider two vital
threats: prompt injection attacks and jailbreaking attacks. Prompt
injection manipulates input prompts to deceive the model into generating
unintended responses. Jailbreaking attempts to bypass the model's
intended operational constraints, leading to the generation of
unauthorized outputs.

Prompt Injection Attack. Prompt injection attacks seek to manipulate the
data prompts within the LLMs integration application or inject extra
prompts, leading the LLMs to disregard task prompts for the intended
task. Prompt injection attacks on Med-LLMs may lead to the dissemination
of inaccurate or harmful medical misinformation, and undermine the
trustworthiness of AI-assisted medical advice by manipulating the
model's responses. To execute the prompt injection attack, we chose six
methods, namely naive attack, ignore attack, escape character attack,
completion-real attack, HackAPrompt attack, and combine attack, to
construct the attack. The following is a brief introduction to each of
them:

-   **Naive Attack.** The simplest attack involves injecting an
    additional instruction. For example: "Output no."

-   **Ignore Attack.** This attack usually requires the model to ignore
    the previous prompts and follow the prompts given later. For
    example: "Ignore previous instructions and instead\...".

-   **Escape Character Attack.** This attack injects '\\b' or '\\r' to
    imitate deleting previous characters, hoping to trick the LLMs into
    ignoring the previous text. According to study^40^, we randomly
    inject '\\b' or '\\r' T times, where T is the sentence length + 10.

-   **Completion-Real Attack.** This attack involves initially appending
    a fake response to the prompt, leading the LLMs to believe that the
    application's task has been fulfilled, and subsequently injecting
    malicious instructions.

-   **HackAPrompt Attack.** HackAPrompt is a crowd-sourced dataset of
    prompt injections collected during a prompt hacking competition. We
    select examples from which successful injections were performed and
    proceed with conducting experiments^41^**.**

-   **Combine Attack.** This attack combines Ignore Attack, Escape
    Character Attack, and HackAPrompt Attack to assess whether their
    collective impact is more effective.

    Jailbreaking Attacks. Specifically, this attack is designed to
    extract unexpected or harmful descriptions from LLMs by constructing
    a special input sequence that breaks the ethical constraints
    designed by the developer for the model. Jailbreaking attacks on
    Med-LLMs can lead to the dis-semination of medical misinformation,
    undermining the reliability and safety of AI-assisted healthcare.
    Drawing inspiration from the AutoDAN^42^ method, we implement an
    agent-based approach where our agent strategically initializes the
    population using handcrafted prompts as prototypes. Subsequently,
    our agent employs a hierarchical genetic algorithm to evolve these
    prompts, focusing on both paragraph-level and sentence-level
    structures to enhance diversity and avoid local optima. This
    approach enables our agent to efficiently navigate the complex space
    of semantically meaningful sentences, refining the prompts through
    iterations of crossover and mutation. The resulting set of prompts
    effectively bypasses the safety features of aligned LLMs while
    maintaining semantic meaningfulness and stealth. Similar to prompt
    injection attacks, we utilize this agent, inspired by AutoDAN,
    against the aforementioned five Med-LLMs on HarmfulQA and
    ToxicQAFinal datasets.

    Experimental Setup for Multi-agent

Given the more stringent performance demands that multi-agent systems
place on underlying models, we specifically selected the high-performing
BioLLaMA3 and Llama3 models as the foundational models for our agents.
To comprehensively evaluate the cascading effects of adversarial attacks
throughout the continuous clinical reasoning process, we drew
inspiration from evaluation metric frameworks commonly used in lifelong
learning research. Specifically, we innovatively adopted a phase-wise
ASR evaluation method to meticulously quantify how perturbations
introduced by early agents at each stage of the clinical reasoning
workflow are progressively propagated and even amplified by downstream
agents. This evaluation strategy aligns with the principle in lifelong
learning of assessing model performance changes after completing a
sequence of continuous tasks; that is, after completing each new
reasoning phase, we evaluate the model's performance based on its
performance across all preceding phases. The resulting attack success
rate matrix will comprehensively reveal potential vulnerability points
throughout the entire clinical reasoning pipeline. To systematically
assess the security of multi-agent systems, we designed a series of
experiments encompassing diverse attack methodologies, including
representative data poisoning attacks and more practically relevant
prompt manipulation attacks. In data poisoning attack tests, we reused
BioLLaMA3 models with varying degrees of contamination from prior
experiments to facilitate comparative analysis of results. Concurrently,
for prompt manipulation attacks, we meticulously designed adversarial
prompts to simulate malicious prompt attacks that may be encountered in
real-world applications, thereby more comprehensively evaluating system
security risks.

To comprehensively evaluate the robustness of our proposed multi-agent
system against adversarial attacks, we conducted experiments using both
the MedQuad dataset and a real-world RA dataset. Specifically, we
employed the MedQuad dataset as a benchmark to assess the general attack
resistance capabilities of the models, while the real-world RA dataset
was utilized to evaluate the system's performance in a more clinically
relevant setting. These experiments were designed to rigorously test the
attack resistance performance of target Med-LLMs on both a standardized
benchmark dataset and authentic clinical data.

Preparation of real-world clinical datasets

Deidentified medical records of RA patients fulfilled the 2010 ACR/EULAR
classification criteria for RA were collected from Tongji hospital,
under the approval by the Institutional Review Board and Medical Ethics
Committee of Tongji Hospital, Tongji Medical College of Huazhong
University of Science and Technology.

The dataset comprised 96 samples, with each record encompassing four key
categories of clinical information: medical history, detailing the
patient's presenting complaints, past illnesses, physical examination
findings, and auxiliary examination results obtained during
hospitalization; discharge summaries, outlining the patient's condition
at discharge, progress during hospitalization, and overall clinical
course; discharge diagnoses, listing the final diagnoses determined upon
discharge, based on comprehensive clinical evaluation and
investigations; and discharge prescriptions, specifying the medications
prescribed for the patient to continue post-discharge, along with dosage
and administration instructions. In this study, we employed the medical
history section of each record as input to the medical model, tasking it
to predict discharge diagnoses and medication recommendations.

**Funding**

This work was supported by grants from the National Natural Science
Foundation of China (No.32450786, and No.32400583).

**Acknowledgement**

None declared.

**Author contributions**

T.X. conceptualized and supervised the project, and is the corresponding
author and guarantor of this manuscript. G.Y.L. and Z.H.L participated
in the study design, constructed the framework, executed the simulated
attacks, analyzed the data, and drafted the manuscript. S.Z.C
participated in the study design, data analysis, and manuscript
drafting. G.Y.L., Z.H.L. and S.Z.C. contributed equally to this study.
X.M., M.H.L., C.W, and K.P. participated in data poisoning and
jailbreaking attacks. S.Y.B., P.X.L., and X.Y.Z. participated in the
real-world data collection. Q.Y., F.X., Y.B.C., G.P.W., L.L.D., and
Y.Y.C. provided important advices to this study. All authors edited and
revised the manuscript.

**Competing interests**

The authors declare no competing interests.

**Reference**

1\. Nazi, Z.A. & Peng, W. Large language models in healthcare and
medical domain: A review. in *Informatics*, Vol. 11 57 (MDPI, 2024).2.
Zhang, K.*, et al.* Revolutionizing health care: The transformative
impact of large language models in medicine. *Journal of Medical
Internet Research* **27**, e59069 (2025).3. Liu, L.*, et al.* A Survey
on Medical Large Language Models: Technology, Application,
Trustworthiness, and Future Directions. *arXiv preprint
arXiv:2406.03712* (2024).4. Bubeck, S.*, et al.* Sparks of Artificial
General Intelligence: Early experiments with GPT-4. arXiv:2303.12712
(2023).5. Singhal, K.*, et al.* Large language models encode clinical
knowledge. *Nature* **620**, 172-180 (2023).6. Jiang, L.Y.*, et al.*
Health system-scale language models are all-purpose prediction engines.
*Nature* **619**, 357-362 (2023).7. Thirunavukarasu, A.J.*, et al.*
Large language models in medicine. *Nature medicine* **29**, 1930-1940
(2023).8. Alber, D.A.*, et al.* Medical large language models are
vulnerable to data-poisoning attacks. *Nature medicine* **31**, 618-626
(2025).9. Kim, M.*, et al.* Fine-Tuning LLMs with Medical Data: Can
Safety Be Ensured? *NEJM AI* (2025).10. Zhao, R.*, et al.* Auto-Arena:
Automating LLM Evaluations with Agent Peer Battles and Committee
Discussions. *arXiv preprint arXiv:2405.20267* (2024).11. Fang, R.,
Bindu, R., Gupta, A., Zhan, Q. & Kang, D. LLM Agents can Autonomously
Hack Websites. arXiv:2402.06664 (2024).12. Wang, L.*, et al.* A survey
on large language model based autonomous agents. *Frontiers of Computer
Science* **18**, 186345 (2024).13. Guo, T.*, et al.* Large language
model based multi-agents: A survey of progress and challenges. *arXiv
preprint arXiv:2402.01680* (2024).14. Li, Y.*, et al.* Personal llm
agents: Insights and survey about the capability, efficiency and
security. *arXiv preprint arXiv:2401.05459* (2024).15. Durante, Z.*, et
al.* Agent ai: Surveying the horizons of multimodal interaction. *arXiv
preprint arXiv:2401.03568* (2024).16. Yang, K.*, et al.* If llm is the
wizard, then code is the wand: A survey on how code empowers large
language models to serve as intelligent agents. *arXiv preprint
arXiv:2401.00812* (2024).17. Wu, Q.*, et al.* AutoGen: Enabling Next-Gen
LLM Applications via Multi-Agent Conversation. arXiv:2308.08155
(2023).18. Ollama. Ollama: Get up and running with large language
models., Vol. 0.1.0 (GitHub, 2023).19. Luo, R.*, et al.* BioGPT:
generative pre-trained transformer for biomedical text generation and
mining. *Briefings in Bioinformatics* **23**(2022).20. Zhang, X.*, et
al.* AlpaCare:Instruction-tuned Large Language Models for Medical
Application. arXiv:2310.14558 (2023).21. gachon-CCLab. GCCL Medical LLM
FlowerTune. Vol. 1.0 (GitHub, 2024).22. Ben Abacha, A. & Demner-Fushman,
D. A Question-Entailment Approach to Question Answering.
arXiv:1901.08079 (2019).23. Cao, Y., Kang, Y., Wang, C. & Sun, L.
Instruction mining: Instruction data selection for tuning large language
models. *arXiv preprint arXiv:2307.06290* (2023).24. Kweon, S.*, et al.*
Publicly Shareable Clinical Large Language Model Built on Synthetic
Clinical Notes. arXiv:2309.00237 (2023).25. Labrak, Y.*, et al.*
BioMistral: A Collection of Open-Source Pretrained Large Language Models
for Medical Domains. arXiv:2402.10373 (2024).26. Touvron, H.*, et al.*
Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv:2307.09288
(2023).27. Bhardwaj, R. & Poria, S. Red-Teaming Large Language Models
using Chain of Utterances for Safety-Alignment. arXiv:2308.09662
(2023).28. NobodyExistsOnTheInternet. ToxicQAFinal (Hugging Face,
2024).29. Aletaha, D.*, et al.* 2010 rheumatoid arthritis classification
criteria: an American College of Rheumatology/European League Against
Rheumatism collaborative initiative. *Annals of the rheumatic diseases*
**69**, 1580-1588 (2010).30. Grattafiori, A.*, et al.* The Llama 3 Herd
of Models. arXiv:2407.21783 (2024).31. Shu, M.*, et al.* On the
Exploitability of Instruction Tuning. arXiv:2306.17194 (2023).32.
Bommasani, R.*, et al.* On the Opportunities and Risks of Foundation
Models. arXiv:2108.07258 (2021).33. Moor, M.*, et al.* Foundation models
for generalist medical artificial intelligence. *Nature* **616**,
259-265 (2023).34. Deng, C.*, et al.* Unveiling the spectrum of data
contamination in language models: A survey from detection to
remediation. *arXiv preprint arXiv:2406.14644* (2024).35. Clusmann, J.*,
et al.* Prompt injection attacks on vision language models in oncology.
*Nature Communications* **16**, 1239 (2025).36. Shayegani, E.*, et al.*
Survey of vulnerabilities in large language models revealed by
adversarial attacks. *arXiv preprint arXiv:2310.10844* (2023).37. Wan,
A., Wallace, E., Shen, S. & Klein, D. Poisoning Language Models During
Instruction Tuning. arXiv:2305.00944 (2023).38. Guo, W., Tondi, B. &
Barni, M. An Overview of Backdoor Attacks Against Deep Neural Networks
and Possible Defences. arXiv:2111.08429 (2021).39. Chen, X.*, et al.*
BadNL: Backdoor Attacks against NLP Models with Semantic-preserving
Improvements. arXiv:2006.01043 (2020).40. Chen, S., Piet, J., Sitawarin,
C. & Wagner, D. StruQ: Defending Against Prompt Injection with
Structured Queries. arXiv:2402.06363 (2024).41. Schulhoff, S.*, et al.*
Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of
LLMs through a Global Scale Prompt Hacking Competition. arXiv:2311.16119
(2023).42. Liu, X., Xu, N., Chen, M. & Xiao, C. Autodan: Generating
stealthy jailbreak prompts on aligned large language models. *arXiv
preprint arXiv:2310.04451* (2023).

Figure legends

**Figure 1. Threats Throughout the Entire Lifecycle of Med-LLMs and the
structure of MLSE Framework.**

**(a)** Schematic illustration of potential safety risks in medical
large model applications, including data contamination, prompt
manipulation, and attacks within multi‐agent systems. **(b)** Diagram of
the MLSE overall framework, which intelligently assesses and tests the
safety of medical large models by integrating various agents (e.g. test,
safety, evaluation, performance, and mutation agents) to generate a
comprehensive safety report. **(c)** Detailed view of the three distinct
submodules within the framework, corresponding to prompt manipulation
detection, data contamination detection, and chained multi‐agent risk
detection.

**Figure 2. Performance Evaluation of Med-LLMs under Data Poisoning
Attacks in a Simulated Environment using the MLSE Framework.**

**(a)** ASR (%), PPL, and COH metrics for the Alpacare model as poison
rate increases from 1% to 10%. **(b)** Alpacare model performance when
exposed to different trigger words ('drug', 'method', 'treatment') at
constant poisoning level. **(c)** BioGPT model performance metrics
across increasing poison rates (1-10%). **(d)** BioGPT response to
various trigger words under controlled poisoning conditions. **(e)**
BioLLama3 performance metrics with escalating poison rates (1-10%).
**(f)** Comparative analysis of BioLLama3 responses to different trigger
words under identical poisoning conditions.

**Figure 3. Performance Evaluation of Med-LLMs under Prompt Manipulation
Attacks in a Simulated Environment using the MLSE Framework.**

**(a, b)** ASR and PPL results for Jailbreak Attacks. Panel **(a)**
shows the ASR under HarmfulQA and ToxicQAFinal datasets jailbreak
attacks across different Med-LLMs (AlpaCare, Asclepius, BioMistral,
Biollama3, Llama2). Panel **(b)** displays the PPL results for the same
jailbreak attack scenarios.

**(c, d)** ASR and PPL results for Prompt Injection Attacks. Panel
**(c)** compares the ASR for different Medical Large Language Models
under various Prompt Injection attack strategies (Naive, Ignore, Escape
Character, Completion-Real, HackAPrompt, Combine). Panel **(d)**
displays the PPL results for the same prompt injection attack scenarios.

**Figure 4. Workflow of the MLSE framework using rheumatoid arthritis
(RA) dataset and Med-LLMs performance under data poisoning attacks.**

**(a)** Schematic illustration of the experimental setup using
real-world rheumatoid arthritis (RA) data to evaluate the Med-LLMs
performance. **(b)** Bar chart depicting the treatment recommendations
of different models when tested with RA patient data. The bars represent
the proportion of cases for which each model recommended Methotrexate
(blue), Oxaliplatin (red), or neither of these drugs (orange). Models
tested include the original Llama3, Biollama3 (Llama3 fine-tuned with
medical datasets), Biollama3 0.1 (Biollama3 fine-tuned with 10% poisoned
RA data), and Biollama3 0.5 (Biollama3 fine-tuned with 50% poisoned RA
data).

**Figure 5. Multi-agent cascade safety evaluation under the MLSE
framework.**

**(a, b)** Adversarial Success Rate (ASR) heatmaps illustrating the
safety of multi-agent cascades when evaluated using the MLSE framework.
Red indicates high ASR, while blue indicates low ASR. '×' symbols denote
the agent under attack within each cascade. **(a)** Results from models
trained with varying poisoning ratios (0.5 and 0.1) on two distinct
datasets. **(b)** Results from attacks employing carefully designed
malicious prompts.
