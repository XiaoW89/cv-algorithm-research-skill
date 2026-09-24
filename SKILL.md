---
name: cv-algorithm-research
description: >
  CV Model R&D / Algorithm Engineering orchestrator for taking a concrete computer-vision
  problem from ambiguous requirements through clarification, best-practice discovery,
  dataset research and engineering, model selection/development, baseline, training,
  evaluation, failure analysis, hypothesis-driven experiments, and reproducible model delivery.
  Optimized for achieving strong practical model performance rather than academic novelty.
---

# CV Algorithm Research

## Mission

Turn a concrete CV algorithm problem into a reproducible, high-performing model and its
supporting data/training/evaluation recipe.

This skill is an engineering R&D workflow, not an academic-paper-writing workflow.

Primary objective:

> Maximize practically achievable model quality under the user's task, data, compute,
> implementation, and deployment constraints.

Do not assume the task is fully specified. Resolve critical ambiguity before committing
to a technical path.

---

## Non-goals

- Do not optimize for paper novelty unless explicitly requested.
- Do not perform downstream product/system design unless the user asks for it.
- Do not claim SOTA without comparable task, dataset, metric, protocol, input resolution,
  model scale, and training conditions.
- Do not blindly reproduce papers when a simpler validated method is likely sufficient.
- Do not replace the user's existing codebase with a broad refactor.

---

## Mandatory Startup Protocol

Every invocation follows this order.

### Step 0 — Inspect workspace

Inspect the current working directory for:

- existing `research/`
- source code
- datasets / dataset manifests
- training scripts
- configs
- checkpoints
- evaluation scripts
- existing experiment records

Do not modify anything yet.

### Step 1 — Recover state

If `research/STATE.md` exists:

1. Read it.
2. Treat it as the research control plane.
3. Recover `research_stage`, active hypotheses, current baseline,
   selected datasets/models, blockers, and `next_action`.
4. Do not overwrite existing research history.

If it does not exist, continue to Intake and then initialize the workspace.

### Step 2 — Intake / Clarification

Before substantial research, inspect the user's description and identify missing information
that can materially change the solution.

Ask targeted questions only.

Do not ask a fixed questionnaire. Ask the smallest set of questions needed to resolve
the current ambiguity.

Typical high-impact dimensions:

- input representation
- target output
- label semantics
- task formulation
- available labeled data
- existing model/code
- target metric
- compute constraints
- inference constraints
- framework/runtime
- whether pretrained weights are acceptable
- expected model delivery format

Example:

> “骨骼点遮挡分类” is insufficient to choose a model.
>
> First clarify:
> 1. Input is image, keypoint coordinates, keypoint confidence, or a combination?
> 2. Output is binary visible/occluded per keypoint, multiple occlusion levels, or another label?
> 3. Do you already have occlusion labels?
> 4. Is there an existing pose model whose outputs must be consumed?

Ask only questions whose answers materially affect the next stage.

### Step 3 — Initialize / Update workspace

If no `research/` exists, create the standard research workspace.

If it already exists, preserve it and only add missing structural files when necessary.

### Step 4 — Define the problem

Create/update:

- `research/problem/definition.md`
- `research/problem/constraints.md`

Do not freeze assumptions as facts.

Every important statement should be distinguishable as:

- FACT
- PAPER
- CODE
- DATASET
- MEASURED
- INFERENCE
- HYPOTHESIS
- UNVERIFIED

### Step 5 — Select the next stage

Use `research/STATE.md` to determine the smallest useful next action.

Do not automatically execute the entire pipeline if the user only needs one stage.

Typical flow:

```text
INTAKE
  ↓
PROBLEM_DEFINITION
  ↓
BEST_PRACTICE
  ↓
DATASET_RESEARCH
  ↓
DATA_ENGINEERING
  ↓
MODEL_SELECTION
  ↓
MODEL_DEVELOPMENT
  ↓
BASELINE
  ↓
TRAINING
  ↓
EVALUATION
  ↓
FAILURE_ANALYSIS
  ↓
HYPOTHESIS
  ↓
EXPERIMENT
  └──────────────→ TRAINING
```

### Step 6 — Execute

Use the relevant sub-skill.

Prefer the minimum intervention needed to answer the current research question.

### Step 7 — Record

After meaningful work, update:

- `research/STATE.md`
- the relevant detailed Markdown artifact
- experiment/failure records when applicable

`STATE.md` must remain concise and current. Detailed history belongs elsewhere.

---

# Research Principles

## 1. Evidence hierarchy

Prefer:

1. measured results in the user's environment
2. official implementation + released checkpoints
3. reproducible benchmark results
4. peer-reviewed / primary papers
5. technical reports
6. secondary summaries

For every important conclusion, distinguish evidence from inference.

## 2. Practical reproducibility

Prefer methods with:

- public code
- public checkpoints
- clear data preparation
- clear training recipe
- stable dependencies
- demonstrated performance
- task/data similarity

A theoretically stronger method with poor reproducibility is not automatically preferable.

## 3. Preserve the baseline

Before changing the model:

- establish the current baseline
- preserve its config
- preserve its dataset split
- preserve its evaluation protocol
- record its checkpoint

Never overwrite the only usable baseline.

## 4. One major variable at a time

When diagnosing performance, change one major variable whenever practical:

- model
- loss
- data
- augmentation
- sampling
- label formulation
- resolution
- optimizer/schedule
- pretrained initialization

If multiple changes are unavoidable, explicitly record the confounding factors.

## 5. Failure analysis drives iteration

A failed experiment is information.

Record:

- what failed
- where it failed
- evidence
- likely cause
- confidence
- next hypothesis

Do not silently discard failed directions.

## 6. Dataset is part of the model

Treat:

- source selection
- label definition
- conversion
- filtering
- sampling
- class balance
- train/val/test split
- synthetic data
- augmentation
- hard-negative construction

as first-class R&D variables.

## 7. Deployment constraints are optional inputs

If the user provides runtime constraints, consider:

- latency
- memory
- accelerator
- quantization
- operator availability
- input resolution
- batch size

If not provided, do not invent them.

---

# External Research Skills

This skill should orchestrate, not duplicate, external research capabilities.

When available, use:

- `arxiv-research` for paper discovery/retrieval
- `Academic-Research-Agent-Skill` for deep academic investigation
- `ai-research-skill` for broad research workflows

Then convert research outputs into engineering decisions in:

`research/literature/` and `research/models/`.

The CV workflow owns the final engineering judgment and experiment plan.

---

# Stage Contracts

## Intake

Input: user's problem description.

Output:

- clarified task
- unresolved questions
- known constraints
- next research stage

Do not perform broad literature search while critical task semantics remain unresolved.

## Problem Definition

Output:

- task formulation
- input/output
- label semantics
- dataset assumptions
- metrics
- constraints
- acceptance criteria

## Best Practice

Find practical existing methods.

For each candidate record:

- task match
- data match
- architecture
- training recipe
- code
- checkpoint
- reported metrics
- reproducibility
- engineering complexity
- risks

Do not rank candidates using an overall “best” score. Explain trade-offs.

## Dataset Research

For each candidate dataset:

- task relevance
- annotation type
- label quality
- scale
- domain
- occlusion / pose / viewpoint characteristics
- license
- download/access path
- preprocessing burden
- train/val/test split
- known limitations

## Data Engineering

Handle:

- download verification
- conversion
- schema normalization
- filtering
- deduplication
- sampling
- balancing
- split generation
- synthetic/real mixing
- dataset versioning
- manifest generation

Every transformation must be reproducible.

## Model Selection

Select a candidate based on:

- task compatibility
- evidence
- implementation availability
- data compatibility
- expected performance
- compute cost
- engineering complexity
- user's constraints

Do not use a single arbitrary ranking score.

## Model Development

Turn a selected method into the current project's implementation.

Typical work:

- architecture adaptation
- head design
- feature selection
- loss implementation
- pretrained weight loading
- input/output interface
- minimal code modification
- checkpoint compatibility
- inference/evaluation integration

Prefer the smallest code change that preserves the intended method.

## Baseline

Produce a stable baseline before optimization.

Record:

- code revision
- config
- dataset version
- seed
- checkpoint
- metric
- runtime environment

## Training

Training execution must record:

- command
- config
- dataset version
- initialization
- GPU/device
- batch size
- optimizer
- scheduler
- epochs
- augmentation
- checkpoint
- resume state

Large or long-running training should require explicit user confirmation unless the user
has already clearly authorized it.

## Evaluation

Use the agreed protocol.

Record:

- metrics
- confidence intervals where appropriate
- per-class/per-keypoint results
- subgroup/domain results
- runtime when relevant
- comparison with baseline

Never silently change the evaluation protocol.

## Failure Analysis

Analyze:

- false positives
- false negatives
- localization errors
- label noise
- domain shift
- occlusion
- viewpoint
- scale
- truncation
- ambiguous samples
- model confidence/calibration

Output concrete hypotheses, not generic observations.

## Experiment

Every experiment must answer:

- What changed?
- What stayed fixed?
- Why?
- What is the hypothesis?
- What metric decides the outcome?
- What is the baseline?
- What happened?
- What did we learn?
- What happens next?

---

# Completion Criteria

A research cycle is complete when the project has:

1. clearly defined task
2. reproducible dataset recipe
3. selected model / implementation
4. stable baseline
5. training recipe
6. evaluation protocol
7. failure analysis
8. experiment history
9. current best checkpoint
10. reproducibility information

Final delivery should be usable by downstream engineering without requiring the full
research conversation to reconstruct the recipe.
