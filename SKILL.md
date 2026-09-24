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
4. Read the relevant stage instructions below. Ask only for unknowns that materially
   affect the next decision; continue independent, inexpensive work where possible.
5. When project artifacts are needed, initialize missing files using the helper below.
   Never overwrite or silently migrate existing research history.
6. Execute the smallest useful action, check its stage gate, and record the result.
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

Discover available tools/skills in the current environment; names and availability
may differ between installations. If available and relevant:

- `arxiv-agent-markdown`: ingest a known arXiv paper and its figures, not general search.
- `research-agent`: source-grounded investigation or claim verification.
- `ai-research`: deeper experiment-design or reproducibility support.
- Framework-specific skills: only after the framework/task is actually selected.

Use available search/retrieval tools for discovery and inspect primary papers, official
code, checkpoint releases, and dataset documentation. If access is unavailable, report
the missing verification and continue work that does not depend on it. Do not fabricate
retrieval or require installing an optional skill to proceed. This workflow owns the
engineering decision and must not expand into academic novelty work by default.

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
