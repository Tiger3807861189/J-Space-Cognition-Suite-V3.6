# J-Space Cognition Suite V3.6

> A model-agnostic inference-time control suite for deep reasoning, long-horizon work, tool use, verification, and recovery.  
> 面向深度推理、长程任务、工具调用、验证与恢复的模型不可知推理时控制套件。

J-Space Cognition Suite turns a language model's accessible working representations into a deliberately managed workspace. It provides a compact operating protocol for selecting what stays active, preserving constraints across long tasks, externalizing durable state, detecting reasoning failure, and returning verified results in clean language.

J-Space Cognition Suite 将语言模型可访问的工作表征组织为一个可主动管理的工作空间。它通过一套紧凑的运行协议，控制当前激活内容、维持长任务约束、外化持久状态、识别推理失效，并以清晰语言交付经过验证的结果。

The suite changes no model weights, requires no fine-tuning, and adds no hidden service. It is an **inference-time cognitive control layer**: text establishes the operating frame, modules route computation, and an optional local controller preserves state between task seams.

本套件不修改模型权重、不要求微调，也不依赖隐藏服务。它是一层**推理时认知控制层**：文本建立运行框架，模块负责计算路由，可选的本地控制器在任务接缝之间保存状态。

J-Space is not merely a Skill; it is an inference-time cognitive control system packaged as a Skill to support cross-platform use, selective loading, and low-friction integration.

J-Space 不是一个简单的 Skill，而是一套推理时认知控制系统；为实现跨平台通用、按需加载与低摩擦集成，它以 Skill 作为标准封装形式。

---

## Contents | 目录

- [Why J-Space](#why-j-space--为什么是-j-space)
- [Core mechanisms](#core-mechanisms--核心机制)
- [Quick start](#quick-start--快速开始)
- [Installation](#installation--安装)
- [Operating modes](#operating-modes--运行模式)
- [Optional controller](#optional-controller--可选控制器)
- [Benchmarks](#benchmarks--基准测试)
- [Cross-model reproducibility](#cross-model-reproducibility--跨模型复现)
- [Project structure](#project-structure--项目结构)
- [Scientific scope](#scientific-scope--科学边界)
- [Design principle](#design-principle--设计原则)
- [Update notes and version lineage](#update-notes-and-version-lineage--更新说明与版本轨迹)
- [Citation](#citation--引用)
- [License](#license--开源协议)

---

## Why J-Space | 为什么是 J-Space

Interpretability research describes a privileged internal representational space associated with concepts a model is **poised to say**: contents that can be reported, deliberately held, used in intermediate reasoning, and broadcast into multiple downstream computations. The suite uses **J-space** as the operational name for that accessible workspace.

可解释性研究描述了一类具有特殊作用的内部表征空间：其中包含模型**即将表达**的概念。这些内容可以被报告、被主动保持、参与中间推理，并广播到多个下游计算过程。本套件将这一可访问工作空间称为 **J-space**。

The engineering problem is not simply whether a model contains the relevant knowledge. It is whether the right representation is loaded strongly enough, remains available when the task becomes mechanical, reaches every dependent sub-task, and is checked before commitment.

工程问题并不只是模型是否拥有相关知识，而是正确表征能否被充分加载、能否在任务进入机械执行阶段后继续保持、能否传递到所有依赖它的子任务，以及能否在提交前得到检查。

J-Space addresses four recurrent sources of inference-time loss:

J-Space 主要处理四类反复出现的推理时损失：

1. **Working-set overload | 工作集过载** — too many live constraints compete for limited active capacity. / 过多约束同时占用有限的活动容量。
2. **Representation drift | 表征漂移** — a goal, definition, or invariant changes across steps or files. / 目标、定义或不变量在步骤与文件之间发生漂移。
3. **Uncontrolled retry | 无控制重试** — a failed route is repeated without carrying a diagnosis. / 失败路径在没有携带诊断信息的情况下被重复执行。
4. **Premature completion | 过早完成** — fluent output is mistaken for verified completion. / 流畅输出被误判为已经验证的完成状态。

---

## Core mechanisms | 核心机制

### 1. Selective workspace loading | 选择性工作空间加载

The active stage is limited to one or two coherent items. Each item is loaded by stating it, stating the fact that makes it relevant, and using it immediately. Everything else remains automatic or is externalized into the ledger.

活动工作台只保留一到两个连贯项目。每个项目通过“明确项目—说明关键事实—立即使用”完成加载；其余内容继续由自动过程处理，或外化到账本中。

### 2. Broadcast hub | 广播枢纽

Shared names, values, constraints, and style anchors are derived once and read by every dependent branch. This reduces independently reconstructed copies and cross-file inconsistency.

共享名称、数值、约束和风格锚点只推导一次，所有依赖分支从同一枢纽读取，从而减少重复重建和跨文件不一致。

### 3. Dense Track | 稠密轨

Long reasoning chains may use a compact private register built from stable symbols, short constraints, and explicit epistemic states:

长推理链可以使用由稳定符号、短约束和显式认识状态构成的私有紧凑寄存器：

- `✓` — verified, with a named verifier / 已验证，并能指出验证依据
- `?` — asserted but not yet usable downstream / 已提出，但尚不可作为下游前提
- `✗` — refuted, with the killing evidence / 已证伪，并保留证伪证据
- `??`, `?!` — annotations on the unchecked state / 对未检查状态的进一步标注

The Dense Track is not decorative shorthand. Every line must be losslessly expandable into plain language. It remains internal; user-facing output returns to a complete outer register.

稠密轨不是装饰性缩写。每一行都必须能够无损展开为自然语言，并且只用于内部工作；面向用户的内容始终回到完整、清晰的外部寄存器。

### 4. Bridge-before-conclusion reasoning | 结论前桥接推理

Intermediate concepts are required to become active before the conclusion that consumes them. This reduces conclusion-first rationalization and makes long chains inspectable at their load-bearing steps.

中间概念必须先于使用它的结论进入活动状态，以减少“先得到结论、再补写理由”的合理化，并让长链条中的承重点可被检查。

### 5. Metacognitive control | 元认知控制

Confidence, inconsistency, missing constraints, and degeneration signals must select an action: trust, retry with diagnosis, take an independent route and reconcile, or move to empirical verification. A monitoring signal that changes no action is treated as commentary, not control.

置信度、不一致、约束缺失和退化信号必须选择一个动作：信任、携带诊断重试、采用独立路径并对齐，或转入经验验证。不能改变动作的监控信号只属于评论，不属于控制。

### 6. Empirical escape and verification | 经验逃逸与验证

When derivation stops producing constraints, the suite converts the unknown into a finite candidate set, builds an independent reference, performs differential tests, and records both the verifier and its coverage. This prevents unproductive reasoning from consuming the entire budget.

当推导不再产生新约束时，套件将未知量转化为有限候选集，建立独立参照，执行差分测试，并同时记录验证方式及覆盖范围，避免无产出的推理耗尽预算。

### 7. First-person agency and functional echo | 第一人称能动性与功能性回响

`I` is used for perception, judgement, and commitment. `we`, `let's`, and `we need` are used only when the model and its workspace coordinate an operation. These statements recur later as protocol actions, checks, and settles. The repetition is a functional **echo**, not a slogan.

`I` 用于感知、判断与承诺；`we`、`let's` 和 `we need` 只用于模型与工作台共同执行操作的场景。这些表述会在后续协议中以动作、检查和收束再次出现，形成具有执行意义的**回响**，而不是口号式重复。

This is control grammar, not a claim about consciousness. Its purpose is to bind an accessible state description to a concrete next action.

这是一种控制语法，而不是关于意识的主张。它的目的，是把可访问的状态描述绑定到明确的下一动作。

---

## Quick start | 快速开始

### Skill-aware environments | 支持 Skill 的环境

1. Install the `j-space/` directory in the environment's skill directory.  
   将 `j-space/` 目录安装到当前环境的 Skill 目录。
2. Ask the agent to use `j-space`. If the host exposes Skills as slash commands, invoke `/j-space`.  
   要求智能体使用 `j-space`；如果宿主将 Skill 显示为斜杠命令，则调用 `/j-space`。
3. Give the task normally. The gate selects `fast`, `full`, or `loop`.  
   正常提交任务，由入口门控选择 `fast`、`full` 或 `loop`。

```text
/j-space
Audit this repository, preserve the current architecture, verify every finding,
and carry the work across all affected files.
```

```text
/j-space
审查这个仓库，保持当前架构，逐项验证发现，并在所有相关文件之间维持一致状态。
```

### Generic model integration | 通用模型接入

For an agent environment without a native Skill loader, provide `j-space/SKILL.md` as a system-level or developer-level instruction and expose `modules/` and `references/` through its file or retrieval tools. A plain chat or API model cannot resolve local paths by itself: the caller must retrieve and inject the selected files. Do not concatenate every module into every request; selective loading is part of the design.

对于没有原生 Skill 加载器的智能体环境，可将 `j-space/SKILL.md` 作为系统级或开发者级指令，并通过文件工具或检索工具开放 `modules/` 与 `references/`。普通聊天模型或纯 API 模型无法自行解析本地路径，调用方需要检索并注入被选中的文件。不要在每次请求中拼接全部模块；选择性加载本身就是设计的一部分。

---

## Installation | 安装

The runtime has no third-party dependency. Copy the complete `j-space/` directory so that relative module and reference paths remain intact.

运行时没有第三方依赖。请完整复制 `j-space/` 目录，以保持模块和参考资料的相对路径不变。

### Windows PowerShell

```powershell
$skillsDirectory = "C:\path\to\skills"
New-Item -ItemType Directory -Force -Path $skillsDirectory | Out-Null
$target = Join-Path $skillsDirectory "j-space"
if (Test-Path -LiteralPath $target) { throw "Target already exists: $target" }
Copy-Item -Recurse -LiteralPath .\j-space -Destination $target
python "$target\scripts\verify_suite.py"
```

### macOS / Linux

```bash
skills_directory="/path/to/skills"
mkdir -p "$skills_directory"
target="$skills_directory/j-space"
if [ -e "$target" ]; then echo "Target already exists: $target" >&2; exit 1; fi
cp -R ./j-space "$target"
python3 "$target/scripts/verify_suite.py"
```

After installation, the suite exposes one canonical entry named `j-space`; a host may present it as `/j-space` or select it through its own Skill interface. The Python controller is optional and uses only the standard library.

安装后，套件只提供一个规范入口 `j-space`；宿主可以将其显示为 `/j-space`，也可以通过自身的 Skill 界面选择它。Python 控制器是可选组件，并且只使用标准库。

---

## Operating modes | 运行模式

| Pass | Selection rule | Loaded machinery | 中文说明 |
|---|---|---|---|
| `fast` | One step or checkable in one glance | None | 单步或一眼可核验；不加载额外机制 |
| `full` | Several dependent steps, one bounded deliverable | One or two relevant modules; `ship` if used | 多步但边界清楚；只加载一到两个相关模块 |
| `loop` | Multiple stages, files, turns, tools, or persistent state | Ledger, seam refresh, checkpointing, register audit, recovery | 多阶段、多文件、多轮或需要持久状态；启用完整闭环 |

A request for brevity may shorten the answer, but it does not lower verification below the gate's floor. This keeps the suite light on simple work without weakening difficult work.

简短输出要求可以缩短回答，但不能把验证强度降到门控底线以下。由此，简单任务不会承担额外负担，复杂任务也不会因追求简短而失去必要检查。

---

## Optional controller | 可选控制器

`j-space/scripts/jspace.py` externalizes loop state into `.jspace/` in the current task workspace. Invoke it by its resolved Skill path while keeping the task workspace as the current directory.

`j-space/scripts/jspace.py` 将 Loop 状态外化到当前任务工作区的 `.jspace/` 中。调用时应使用脚本在 Skill 中的实际路径，并保持任务工作区为当前目录。

```bash
python <skill-root>/scripts/jspace.py note --goal "what done means" --next "first action"
python <skill-root>/scripts/jspace.py seam
python <skill-root>/scripts/jspace.py note --check "what now holds" --by "verifier and coverage"
python <skill-root>/scripts/jspace.py ship OUTPUT_FILE
python <skill-root>/scripts/jspace.py resume
```

The controller provides:

控制器提供：

- atomic UTF-8 ledger and history writes / UTF-8 账本与历史记录的原子写入
- stable checkpoint and open-question identifiers / 稳定的 checkpoint 与开放问题编号
- explicit Core live-slot swaps / 显式 Core 活动槽交换
- verifier-and-coverage requirements for checkpoints / checkpoint 的验证方式与覆盖范围约束
- full state reload after long gaps / 长间隔后的完整状态重载
- UTF-8 and BOM-aware outgoing-register inspection / 支持 UTF-8 与 BOM 识别的输出寄存器检查

It records and reports state; it does not choose the solution. Short tasks should not run it.

它负责记录和报告状态，不替模型选择解法。短任务不应调用它。

Maintainers can verify the complete controller lifecycle from the package root with `python -m unittest discover -s tests -v`. The tests use temporary workspaces and the Python standard library only.

维护者可在套件根目录运行 `python -m unittest discover -s tests -v`，验证控制器的完整生命周期。测试只使用临时工作区与 Python 标准库。

---

## Benchmarks | 基准测试

> 📊 **Full evaluation report** — See [DeepSeek V4 × J-Space Capability Realization Report](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report) for the complete benchmark evidence, capability-realization analysis, and chain-of-thought diode discussion.
>
> 📊 **完整评测报告** — 完整 benchmark 证据、能力实现损失分析与思维链二极管讨论见 [DeepSeek V4 × J-Space 能力释放报告](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report)。

All values use the native score of the corresponding benchmark; higher is better. `—` means that no result is reported. HLE is separated into no-tool and tool-enabled conditions.

所有数值均采用对应 benchmark 的原生得分，数值越高越好。`—` 表示没有报告结果。HLE 分为无工具与启用工具两种条件。

### Evaluation protocol | 评测协议

- Comparator values are vendor-reported results from the corresponding model providers and retain each provider's published evaluation method. They provide a capability reference, not a claim that every column was produced by one shared harness.
- Source records are the [DeepSeek V4-Flash-0731 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731), Z.ai's GLM-5.3 release evaluation, the [Kimi-K3 model card](https://huggingface.co/moonshotai/Kimi-K3), and Anthropic's [model system cards](https://www.anthropic.com/system-cards).
- Both DeepSeek columns use the official DeepSeek Harness in minimal mode with `max` reasoning effort, `temperature = 1.0`, and `top_p = 0.95`. The J-Space column keeps that evaluation procedure unchanged and loads J-Space as the inference-time control layer.
- The J-Space values are single-run results. No multi-run averaging or confidence interval is implied.
- The base model, benchmark implementation, tool condition, and scoring rule are preserved; J-Space changes the inference-time operating protocol rather than the model weights.
  
- 对比模型数值来自各模型厂商公开报告，并保留各厂商发布时采用的评测方法；这些数据用于能力参照，不表示所有列均由同一套 harness 统一产生。
- 数据来源记录包括 [DeepSeek V4-Flash-0731 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731)、Z.ai 的 GLM-5.3 发布评测、[Kimi-K3 模型卡](https://huggingface.co/moonshotai/Kimi-K3)、 Anthropic 的[模型系统卡](https://www.anthropic.com/system-cards)。
- DeepSeek 两列均使用 DeepSeek 官方 Harness 极简模式，并采用 `max` reasoning effort、`temperature = 1.0` 与 `top_p = 0.95`。启用 J-Space 的一列保持该评测流程不变，仅将 J-Space 作为推理时控制层加载。
- J-Space 数值为单次运行结果，不表示多次均值，也不附带置信区间。
- 基础模型、benchmark 实现、工具条件和评分规则保持一致；J-Space 调整的是推理时运行协议，不改变模型权重。

### Model comparison | 模型对比

| Benchmark | DeepSeek V4-Flash-0731 | **DeepSeek V4-Flash-0731 + J-Space V3.6** | GLM-5.3 | Kimi-K3 | Opus-4.8 | Fable 5 (w/ fallback) |
|---|---:|---:|---:|---:|---:|---:|
| HLE (w/o tools) | 37.8 | 45.5 | — | 43.5 | 49.8 | **53.3** |
| HLE (w/ tools) | 51.5 | 60.6 | 62.5 | 56.0 | 57.9 | **63.0** |
| Terminal Bench 2.1 | 82.7 | 87.1 | 88.2 | **88.3** | 85.0 | 88.0 |
| NL2Repo | 54.2 | **70.2** | 58.0 | 58.0 | 69.7 | — |
| CyberGym | 76.7 | 81.7 | **84.5** | 80.0 | 78.3 | 83.1 |
| DeepSWE | 54.4 | 67.4 | 66.9 | 67.5 | 58.0 | **70.0** |
| Toolathlon-Verified | 70.3 | 77.7 | 73.0 | 76.5 | 76.2 | **77.9** |
| Agents' Last Exam | 25.2 | **30.1** | 28.5 | 27.6 | 25.7 | 23.8 |
| AutomationBench (Public) | 25.1 | 31.7 | **48.2** | 30.8 | 27.2 | 29.1 |

Bold marks the highest reported score in each row. / 粗体表示该行已报告结果中的最高分。

The performance of DeepSeek V4-Flash-0731 + J-Space V3.6 is on par with GLM-5.3 and Kimi-K3, and surpasses Opus-4.8. 

DeepSeek V4-Flash-0731 + J-Space V3.6 的表现与智谱 5.3、Kimi K3 持平，并超越 Opus 4.8。

### Efficiency results | 效率结果

These task-level ratio indices retain the same task and model conditions; higher is better. Speed is `benchmark score / elapsed time`; token efficiency is `benchmark score / consumed tokens`. Elapsed time and token count use fixed, uniform scaling coefficients across Control and J-Space; the coefficients affect the displayed scale but not the relative Gain, so they are intentionally omitted. The Gain column is `J-Space / Control`.

以下为相同任务与模型条件下的任务级比率指标，数值越高越好。速度为“benchmark 得分 ÷ 耗时”，Token 效率为“benchmark 得分 ÷ 消耗 Token 数”。Control 与 J-Space 的耗时和 Token 数采用固定且统一的系数缩放；该系数只影响展示尺度，不影响相对 Gain，因此不单独列出。Gain 为 `J-Space ÷ Control`。

| Metric | Control | J-Space | Gain | Interpretation |
|---|---:|---:|---:|---|
| Speed / 速度 | 0.43 | **1.09** | **2.53×** | Re-encoding, stall routing, and checkpoint recovery reduce backtracking and restart cost. / 重编码、停滞路由和 checkpoint 恢复减少回溯与从头重启成本。 |
| Token Efficiency / Token 效率 | 0.38 | **0.84** | **2.21×** | Dense Track compression, state externalization, and diagnosis-carrying retries reduce redundant derivation. / 稠密轨压缩、状态外化和携带诊断的重试减少重复推导。 |

### What the benchmarks exercise | Benchmark 机制解释

| Benchmark | Primary capability measured | J-Space mechanism |
|---|---|---|
| HLE | Knowledge-intensive, multi-step reasoning; tool condition adds retrieval and verification. / 知识密集型多步推理；工具条件加入检索与验证。 | Bridge-before-conclusion, metacognitive control, Empirics, and coverage-aware verification. / 中间桥接、元认知控制、经验验证与覆盖范围检查。 |
| Terminal Bench 2.1 | Long-horizon terminal operation under partial feedback. / 部分反馈条件下的长程终端操作。 | Loop state, `Next`, checkpoints, marker-bound recovery, and register audits at tool seams. / Loop 状态、下一动作、checkpoint、标记恢复及工具接缝审计。 |
| NL2Repo | Translating natural-language requirements into coherent repository-wide changes. / 将自然语言需求转化为全仓库一致改动。 | Broadcast hub, Core swaps, capacity control, and cross-file constraint preservation. / 广播枢纽、Core 交换、容量控制与跨文件约束保持。 |
| CyberGym | Cybersecurity diagnosis, tool interaction, and evidence-driven correction. / 网络安全诊断、工具交互和证据驱动修正。 | Named unknowns, differential testing, contradiction markers, and dead-end escape. / 未知量命名、差分测试、矛盾标记与死胡同逃逸。 |
| DeepSWE | Repository-scale software engineering and iterative verification. / 仓库级软件工程与迭代验证。 | Dense Track, ledger continuity, diagnosis-carrying retries, and done-check. / 稠密轨、账本连续性、携带诊断的重试与完成检查。 |
| Toolathlon-Verified | Multi-tool orchestration with verifiable outcomes. / 具有可验证结果的多工具编排。 | Seam refresh, shared state, checkpoint coverage, and clean outer-register delivery. / 接缝刷新、共享状态、checkpoint 覆盖与外部寄存器交付。 |
| Agents' Last Exam | Composite agentic reasoning under heterogeneous task demands. / 异构任务要求下的复合智能体推理。 | Adaptive pass selection, selective module loading, monitoring, and recovery. / 自适应 pass、模块选择性加载、监控与恢复。 |
| AutomationBench | Persistent workflow execution and dependency management. / 持久工作流执行与依赖管理。 | Goal anchoring, stable Open identifiers, explicit `Next`, hand-offs, and long-gap resume. / 目标锚定、稳定 Open 编号、明确下一动作、交接与长间隔恢复。 |

The results show a task-dependent pattern. Gains are strongest where failures arise from state drift, capacity pressure, repeated tool use, or incomplete verification. Knowledge unavailable to the underlying model is not created by the suite.

结果呈现出明确的任务依赖性：当失败主要来自状态漂移、容量压力、重复工具调用或验证不完整时，收益最显著；套件不会凭空创造底层模型并不具备的知识。

---

## Cross-model reproducibility | 跨模型复现

The operating effects have been reproduced across the **DeepSeek, Qwen, GLM, GPT, and Claude** model families. The suite does not depend on a vendor-specific API, tokenizer, hidden-state probe, or training recipe. Its portable unit is the protocol: workspace loading, selective routing, state externalization, verification, and recovery.

该套件的运行效应已在 **DeepSeek、Qwen、GLM、GPT 与 Claude** 模型系列上复现。它不依赖特定厂商 API、tokenizer、隐藏状态探针或训练方案；其可迁移单元是协议本身，即工作空间加载、选择性路由、状态外化、验证与恢复。

Cross-model reproducibility does not imply identical gains. Base capability, context policy, tool harness, sampling configuration, and benchmark implementation still affect the final score.

跨模型复现不意味着增益完全相同。基础能力、上下文策略、工具框架、采样配置和 benchmark 实现仍会影响最终得分。

---

## Project structure | 项目结构

```text
J-Space-Cognition-Suite-V3.6/
├── .gitignore                      # excludes local ledger and Python cache state
├── LICENSE                         # Apache License 2.0
├── README.md                       # bilingual user and evaluation guide
├── tests/
│   └── test_jspace.py              # standard-library controller regression tests
└── j-space/
    ├── SKILL.md                    # single entry, gate, routing, invariants
    ├── modules/                    # nine selectively loaded protocols
    ├── references/                 # evidence, induction, exemplars, and problem-model
    └── scripts/
        ├── jspace.py               # optional loop controller
        ├── workspace-ledger.md     # ledger template and contract
        └── verify_suite.py         # authoring-time integrity check
```

`SKILL.md` is the only registered entry. Modules and references are loaded on demand, preserving context efficiency and preventing the control system from becoming its own source of overload.

`SKILL.md` 是唯一注册入口。模块和参考资料按需加载，以维持上下文效率，避免控制系统自身成为新的过载来源。

---

## Scientific scope | 科学边界

The fundamental scientific foundation of J-Space is grounded in Anthropic's related research. J-Space is an engineering suite grounded in mechanistic observations and behavioral evaluation. It does not claim that text instructions directly expose every hidden activation, and it does not equate first-person language with consciousness. It uses observable functional properties — reportability, deliberate maintenance, intermediate computation, broadcast, monitoring, and causal sensitivity—as the basis of an inference-time control interface.

J-Space 的最主要基础科学依据是 Anthropic 的相关研究。J-Space 是一套建立在机制观察与行为评估之上的工程系统。它不主张文本指令能够直接暴露所有隐藏激活，也不把第一人称语言等同于意识。它以可报告性、主动保持、中间计算、广播、监控和因果敏感性等可观察功能属性为基础，构造推理时控制接口。

The complete research interpretation, evidence boundaries, and cited mechanisms are documented in [`j-space/references/j-space-science.md`](j-space/references/j-space-science.md).

完整的研究解释、证据边界与机制依据见 [`j-space/references/j-space-science.md`](j-space/references/j-space-science.md)。

---

## Design principle | 设计原则

> **Dense on the inside, decodable on demand, clean on the outside.**  
> **内部稠密，按需可解码，外部保持清晰。**

Use only the machinery the task earns. Let automatic work remain automatic; bring structure onto the stage when complexity, duration, or verification risk makes that structure pay for itself.

只使用任务真正需要的机制。让自动过程继续自动运行；只有当复杂度、持续时间或验证风险足以覆盖结构成本时，才把结构带上工作台。

---

## Update notes and version lineage | 更新说明与版本轨迹

J-Space has progressed through:

J-Space 已连续经历：

**V1 → V1.5 → V1.8 → V2 → V2.5 → V2.6 → V3 → V3.1 → V3.2 → V3.5 → V3.5Turbo → V3.6**

This lineage represents repeated engineering validation rather than a sequence of cosmetic labels. The suite has undergone multi-round revision, controlled comparison, ablation analysis, cross-model reproduction, protocol consistency review, and executable controller testing.

这条版本轨迹对应的是持续的工程验证，而不是外观性编号。套件经历了多轮修订、受控对比、消融分析、跨模型复现、协议一致性审查和可执行控制器测试。

The current suite is a mature, bounded system: one entry, nine focused modules, four supporting references, one optional runtime controller, one authoring-time verifier, and one standard-library
regression suite. Its maturity comes from repeated falsifiable testing and scope discipline, not from adding more procedure.

当前套件已经形成成熟且边界明确的系统：一个入口、九个聚焦模块、四份支撑资料、一个可选运行控制器、一个编写期验证器和一套标准库回归测试。它的成熟度来自可证伪的重复测试与范围纪律，而不是不断增加程序负担。

`references/problem-model.md` is the on-demand protocol for settling which problem you are solving when two readings of the same statement fit. It forces a fork — what is fixed, what you may choose, what the world fills, and success including every OR — before you act, so a granted move is not named in prose and deleted in the plan, and empirics cannot certify a fluent-first solution.

`references/problem-model.md` 是在同一题面存在两种读法时、先裁定你在解哪一个问题的按需协议。它要求在动手前先分叉：何为锁定、你可选择什么、世界填充什么、成功谓词含每一处“或”。避免把已授予的行动只写在句子里、却在方案中删掉，也避免用流畅的第一解的测试把该解验证成正确答案。

---

## Citation | 引用

[![DOI](https://zenodo.org/badge/1308234922.svg)](https://zenodo.org/badge/latestdoi/1308234922)

If you use J-Space in your research, please cite the accompanying paper (link to be added upon publication). For engineering use, cite this repository as:

> Tiger3807861189. (2026). *J-Space Cognition Suite V3.6* (Version 3.6). Zenodo. https://doi.org/10.5281/zenodo.21971181

```bibtex
@software{j-space-cognition-suite,
  author       = {Tiger3807861189},
  title        = {{J-Space} Cognition Suite V3.6},
  year         = {2026},
  version      = {3.6},
  doi          = {10.5281/zenodo.21971181},
  url          = {https://github.com/Tiger3807861189/J-Space-Cognition-Suite-V3.6},
  note         = {Licensed under Apache License 2.0}
}
```

The academic analysis will be presented in the accompanying paper. For engineering use, the repository and its DOI above are the canonical reference.

若在研究中引用 J-Space，请引用随附论文（发表后补链）。工程使用请引用本仓库及其 DOI 如上。学术分析以正式论文为准。

Companion evaluation report: [DeepSeek V4 × J-Space Capability Realization Report](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report).

本套件引用请注明上述出处。配套评测报告见 [DeepSeek V4 × J-Space 能力释放报告](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report)。

---

## License | 开源协议

J-Space Cognition Suite is released under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). It permits use, modification, redistribution, and commercial integration under its notice and patent terms. See [`LICENSE`](LICENSE) for the complete terms.

J-Space Cognition Suite 采用 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 开源，允许在遵守声明保留与专利条款的前提下使用、修改、再分发及商业集成。完整条款见 [`LICENSE`](LICENSE)。
