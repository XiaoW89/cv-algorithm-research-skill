---
name: cv-algorithm-research
description: >
  Develop and improve practical computer-vision models from user requirements:
  clarify tasks, assess feasibility, research methods and data, build reproducible
  baselines, train, evaluate, analyze failures, and deliver the best validated model
  within agreed constraints and budget. Use for full CV model development or an
  individual stage; optimize engineering results rather than academic novelty.
---

# CV Algorithm Research

## Objective and boundaries

Translate the user's actual requirements into a reproducible model, data recipe,
and measured acceptance result. Support diverse CV tasks, including custom or
multi-stage tasks; derive the workflow from the input, output, labels, and use conditions.
Do not assume a particular application, model family, framework, or dataset format.

“Best” means the best validated candidate among the explored alternatives within the
agreed data, compute, time, and inference constraints. Never promise a global optimum.
Filter by hard constraints first, then apply the agreed primary objective and tie-breakers.
Keep the best observed candidate distinct from the best candidate that meets requirements.

- Prefer existing, reproducible methods. Novelty is optional and must be requested.
- Preserve the user's codebase, raw data, baseline, splits, configs, and checkpoints.
- Ask about downstream use only when it changes the model, evaluation, or handoff.
- Do not invent deployment constraints or numeric success thresholds.
- Prefer one major change per diagnostic experiment; record unavoidable confounders.
- Record failed directions and uncertainty rather than silently discarding them.

## Startup and scope

1. Inspect the workspace: code, configs, data/manifests, checkpoints, evaluation,
   environment, and existing research records. Do not modify it during inspection.
2. If `research/STATE.md` exists, recover it and the artifacts relevant to the request.
   Verify referenced files/runs before trusting stale state. The latest user direction
   takes precedence over a saved `next_action`.
3. Distinguish a full model-development project from a narrow question, review, or
   single-stage request. For a read-only question, do not initialize a project or
   require unrelated stages. Existing evidence may already satisfy a gate.
4. When taking on a model-development project, inspect `research/` for existing method
   research, following [the research sufficiency and user-choice procedure](skills/best-practice/SKILL.md#existing-research-and-user-choice).
   Reuse adequate evidence; if missing or insufficient, explain the gaps and ask whether
   to conduct algorithm research before starting external discovery. Reuse an explicit
   research request or a recorded choice within its scope; do not repeat the question
   on every resume or force research onto an unrelated single-stage request.
5. Before relying on method research for model selection, reconcile the research log's
   claims with the retrieved source records and artifact metadata. Follow the
   [evidence reconciliation procedure](skills/best-practice/SKILL.md#research-evidence-reconciliation);
   unresolved contradictions limit the claim and may require user-visible verification.
6. Read the relevant stage instructions below and match the current subtask to
   [available external capabilities](#external-capabilities). Ask only for unknowns
   that materially affect the next decision; continue independent, inexpensive work.
7. When project artifacts are needed, initialize missing files using the helper below.
   Never overwrite or silently migrate existing research history.
8. Execute the smallest useful action, check its stage gate, and record the result.
   Update `STATE.md` after meaningful project work; keep details in linked artifacts.

## Stage routing

These are supporting instruction files, not independently installed skills. Open the
linked file for the selected stage; do not load all stages by default. Paths are relative
to this skill directory. Read [WORKFLOW.md](WORKFLOW.md) when planning a full project,
changing stages, or deciding whether work can finish.

| Stage | Read | Principal project artifact |
|---|---|---|
| INTAKE | [Intake](skills/intake/SKILL.md) | `problem/definition.md`, open questions |
| PROBLEM_DEFINITION | [Problem definition](skills/problem-definition/SKILL.md) | `problem/acceptance.md`, `problem/constraints.md` |
| FEASIBILITY | [Feasibility](skills/feasibility/SKILL.md) | `feasibility/assessment.md` |
| BEST_PRACTICE | [Method research](skills/best-practice/SKILL.md) | `literature/search-log.md`, `models/candidates.md` |
| DATASET_RESEARCH | [Dataset research](skills/dataset-research/SKILL.md) | dataset records and selection rationale |
| DATA_ENGINEERING | [Data engineering](skills/data-engineering/SKILL.md) | `datasets/audit.md`, versioned manifests |
| MODEL_SELECTION | [Model selection](skills/model-selection/SKILL.md) | `models/selected.md` |
| MODEL_DEVELOPMENT | [Implementation](skills/model-development/SKILL.md) | implementation/config changes |
| BASELINE | [Baseline](skills/baseline/SKILL.md) | `models/baseline.md` |
| TRAINING | [Training](skills/training/SKILL.md) | run and checkpoint records |
| EVALUATION | [Evaluation](skills/evaluation/SKILL.md) | `evaluation/protocol.md`, `evaluation/report.md` |
| FAILURE_ANALYSIS | [Failure analysis](skills/failure-analysis/SKILL.md) | `failures/` |
| HYPOTHESIS / EXPERIMENT | [Experiments](skills/experiment/SKILL.md) | `experiments/`, hypothesis decision |
| DELIVERY | [Delivery](skills/delivery/SKILL.md) | `delivery/handoff.md` |

Artifact paths in this table are relative to `research/`. Create detailed records as
needed from `templates/`; a completed directory tree is not evidence of model quality.

## Decisions that must be explicit

- Requirements: label meaning, important operating conditions, metric definitions,
  hard constraints, preferences, and how success will be judged.
- Feasibility: available evidence, data/label gaps, resource estimates, and the cheapest
  test of the largest uncertainty. Revisit when material assumptions change.
- Data: provenance, licensing, label correctness, coverage, independent split unit,
  leakage checks, transformation version, and uncovered conditions.
- Evaluation: validation selects models and thresholds; a held-out test estimates
  final generalization. Do not optimize repeatedly against the final test set.
- Investment: budget, next experiment's expected information or benefit, and stopping
  rules. Data fixes, simpler methods, and stopping are valid alternatives to more training.
- Delivery: actual acceptance status, best candidate, reproducibility, and remaining gaps.

For task-specific measurement choices read [evaluation profiles](references/evaluation-profiles.md).
For manifest tooling read [data audit](references/data-audit.md).
For machine-checked state read [state contract](references/state-contract.md).

## Evidence discipline

Tag important assertions with `[FACT]`, `[PAPER]`, `[CODE]`, `[DATASET]`, `[MEASURED]`,
`[INFERENCE]`, `[HYPOTHESIS]`, or `[UNVERIFIED]`. Cite the source, artifact, or run.
Paper results are reported evidence, not local measurements. Prefer relevant local
measurements and reproducible primary implementations over unsupported rankings.
Do not claim superiority across incompatible data, metrics, protocols, or resource budgets.

## External capabilities

Proactively select skills for the current subtask; do not require the user to name them.
Apply this across all stages, not just literature research:

1. Identify the immediate capability needed, inputs, expected output, and constraints.
   Inspect the current environment's available skill catalog and descriptions; do not
   assume every skill installed on disk is exposed or usable in this session.
2. Match descriptions and exclusions to that need, respecting host invocation rules
   and explicit user choices. Choose one primary skill per capability; overlapping
   descriptions are alternatives, not a reason to run them all. Combine same-purpose
   skills only for a concrete need, such as a coverage gap or necessary independent
   verification, and explain the need and distinct roles before doing so. Otherwise use
   only complementary capabilities. Do not hard-code preferred names, a fixed call
   chain, or select by name alone. Reassess when the subtask or available capabilities
   change, not on every tool call.
3. Announce the selected skills and why, then read their full instructions and required
   references before using them. Check actual task fit, prerequisites, and cost; do not
   load every installed skill in full. If a candidate proves unsuitable, explain and
   choose a fitting alternative rather than silently bypassing its requirements.
4. Keep execution within the user's goal, scope, budget, and authorization. Selecting a
   skill does not authorize its actions: preserve the research-now/defer/skip choice
   and ask before a material expansion. Do not let a specialist workflow redefine the
   engineering goal as academic novelty or unrelated work.

Integrate outputs into the relevant project artifacts with evidence and limitations.
Briefly record the skill used and its purpose in the relevant work log, including any
important fallback. If no suitable skill is available, use available tools directly
where feasible and disclose the gap; do not fabricate usage or require installation.
For external research, verify primary papers, official code, checkpoint releases, and
dataset documentation; report inaccessible evidence and continue independent work.

## Helpers

Run from the user's project directory, replacing `<skill-dir>` with this skill's actual
location. `--root` defaults to `research`; it is the research directory itself.

```sh
python <skill-dir>/scripts/init_research.py --root research
python <skill-dir>/scripts/validate_state.py --root research
python <skill-dir>/scripts/validate_state.py --root research --strict
python <skill-dir>/scripts/compare_experiments.py --root research
python <skill-dir>/scripts/audit_manifest.py path/to/manifest.csv --check-files
```

Only state validation requires PyYAML (`scripts/requirements.txt`); other helpers use
the standard library. Structural validation is suitable for a fresh/legacy workspace;
strict validation checks the recorded gates and referenced evidence for the current stage.
Neither verifies the scientific truth of a report. The manifest helper performs common
integrity/leakage checks; task-specific annotation and visual audits remain necessary.

## Authorization and completion

Ask before very large downloads, long GPU training, destructive data operations, broad
source refactors, or deleting/replacing datasets/checkpoints when not already authorized.
Record the scope and budget of existing authorization and reuse it within those bounds.
Small inspections, metadata checks, smoke tests, and local analysis may proceed directly.

Successful model completion requires measured acceptance evidence and a reproducible
handoff, as defined in [WORKFLOW.md](WORKFLOW.md). If budget runs out, evidence is missing,
or the goal is infeasible, report that outcome and the best available result honestly.
Do not label an unmet target as success or keep running unbounded experiments.
