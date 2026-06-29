# AFAC Sparse Feedback Quant

> 中文：一个将“稀疏反馈下的自动化实验挑战”与“量化金融因子挖掘”结合起来的开源研究脚手架。  
> English: An open-source research scaffold that combines sparse-feedback automation challenges with quantitative factor mining.

本项目借鉴 AFAC2026 的研究流程经验，但只发布合成数据、通用因子族、抽象实验状态和经过脱敏的模型经验。  
This project is inspired by the AFAC2026 research workflow, but it only ships synthetic data, generic factor families, abstract experiment states, and sanitized model lessons.

本仓库不包含私有 alpha 表达式、平台账号数据、真实 PnL、排行榜调参、模型 checkpoint、私有 prompt 或高分配置。  
This repository does not contain private alpha expressions, platform account data, real PnL, leaderboard tuning, model checkpoints, private prompts, or high-score configurations.

## 项目目标 / Project Goal

中文：AFAC Sparse Feedback Quant 的目标不是公开某个高分方案，而是公开一套可复用的研究系统范式：在反馈稀疏、延迟、不完整的环境中，让 agent 能够提出候选、记录实验、识别失败、检查冗余，并沉淀可审查的研究记忆。  
English: AFAC Sparse Feedback Quant does not publish a high-score recipe. It publishes a reusable research-system pattern: in environments with sparse, delayed, or incomplete feedback, an agent can propose candidates, track experiments, diagnose failures, detect redundancy, and write reviewable research memory.

## 核心模块 / Core Modules

- **稀疏反馈实验循环 / Sparse feedback loop**  
  中文：跟踪反馈延迟、噪声较大、只有部分结果或只有二元通过/失败信号的实验。  
  English: Track experiments when feedback is delayed, noisy, partial, or binary.

- **因子候选抽象 / Factor candidate abstraction**  
  中文：用经济逻辑族、数据频率、预期换手和风险备注描述候选，而不是暴露私有公式。  
  English: Describe a candidate by economic family, data cadence, expected turnover, and risk notes instead of exposing private formulas.

- **相关性守卫 / Correlation guard**  
  中文：用日收益变化计算相关性，避免直接比较累计 PnL 曲线造成误判。  
  English: Compare strategies by daily-return deltas rather than cumulative PnL levels.

- **研究记忆生成 / Research memory**  
  中文：把实验结果转成脱敏 Markdown 笔记，先人工审查，再决定是否加入公开 playbook。  
  English: Convert experiment outcomes into sanitized Markdown notes for human review before they enter a public playbook.

## 目录结构 / Repository Layout

```text
afac-sparse-feedback-quant/
  .gitignore
  pyproject.toml
  README.md
  LICENSE
  PRIVACY.md
  docs/
    architecture.md
    model_lessons.md
    challenge_spec.md
  examples/
    synthetic_experiments.json
    synthetic_pnl.csv
  src/
    afac_sparse_quant/
      __init__.py
      __main__.py
      cli.py
      correlation.py
      experiment.py
      factor.py
      memory.py
  tests/
    test_correlation.py
    test_memory.py
```

## 快速开始 / Quick Start

中文：进入本目录后运行：  
English: From this directory, run:

```bash
python -m pip install -e .
python -m afac_sparse_quant report examples/synthetic_experiments.json
python -m afac_sparse_quant corr examples/synthetic_pnl.csv
```

中文：第一个命令会基于合成实验记录生成脱敏研究总结；第二个命令会基于合成累计 PnL 计算日收益相关性。  
English: The first command generates a sanitized research summary from synthetic experiment records. The second computes daily-return correlations from synthetic cumulative PnL series.

示例输出 / Example output:

```text
quality_a,quality_variant,0.9263
```

中文：这表示两个候选在日收益层面高度相关，应该进入去重或人工复核流程。  
English: This means the two candidates are highly correlated at the daily-return level and should enter a de-duplication or review process.

## 设计边界 / Design Boundary

可以公开 / Public:

- 通用实验 schema / generic experiment schemas
- 合成样例 / synthetic examples
- 失败类型 taxonomy / failure taxonomies
- 相关性与研究记忆工具 / correlation and memory tooling
- 抽象模型经验 / abstract model lessons

不能公开 / Private:

- AFAC2026 精确调参 / exact AFAC2026 tuning
- 模型结构和超参数配方 / model architecture and hyperparameter recipes
- 高分运行使用的 prompt / prompts used for high-scoring runs
- 私有因子表达式 / private factor expressions
- 真实 PnL、alpha ID、账号状态或提交结果 / real PnL, alpha IDs, account state, or submission outcomes

更多边界说明见 [PRIVACY.md](PRIVACY.md)。  
See [PRIVACY.md](PRIVACY.md) for the full publication boundary.

## 为什么关注稀疏反馈 / Why Sparse Feedback Matters

中文：很多自动化研究系统拿到的反馈并不是完整梯度或清晰标签，而是延迟、模糊、部分可见的信号。  
English: Many automated research systems do not receive full gradients or clean labels. They receive delayed, ambiguous, partially visible signals.

典型场景 / Common cases:

- 批量结果数小时后才返回 / a batch result arrives hours later;
- 通过/失败检查隐藏了真实失败原因 / pass-fail checks hide the real failure reason;
- 单个候选表现不错，但和已有信号高度重复 / a candidate looks strong but duplicates an existing signal;
- 模型提升了可见指标，却牺牲了组合多样性 / a model improves a visible metric while degrading diversity;
- 局部最优步骤不一定提升组合层面的质量 / the best local step is not necessarily best at the portfolio level.

中文：本项目把这些约束当成系统设计的一部分，而不是事后补丁。  
English: This project treats those constraints as first-class system design inputs, not after-the-fact patches.

## 开放挑战 / Open Challenge

中文：本项目也可以作为一个开放挑战的基础：  
English: This project can also serve as the base for an open challenge:

**稀疏反馈下的自动化实验挑战与量化金融因子挖掘融合**  
**Sparse Feedback Automation Meets Quantitative Factor Mining**

挑战目标 / Challenge objective:

- 提出脱敏因子候选 / propose sanitized factor candidates;
- 处理延迟或部分反馈 / handle delayed or partial feedback;
- 识别高相关、低多样性的候选 / detect highly correlated or low-diversity candidates;
- 生成可审查的研究笔记 / generate reviewable research notes;
- 保持私有方案不可泄露 / keep private recipes unpublished.

详细规格见 [docs/challenge_spec.md](docs/challenge_spec.md)。  
See [docs/challenge_spec.md](docs/challenge_spec.md) for details.

## 许可证 / License

MIT. See [LICENSE](LICENSE).
