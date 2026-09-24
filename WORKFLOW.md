# Workflow and stage gates

Use only stages relevant to the user's request. Reuse valid existing artifacts; gates
are evidence requirements, not mandatory user approval meetings or a fixed questionnaire.

## Full project

Clarify → define requirements and provisional evaluation → preliminary feasibility →
research methods/data → refine feasibility and plan → audit/prepare data → choose and
integrate a reproducible baseline → sanity checks → train → validate → analyze errors →
bounded experiments → freeze candidate/protocol → final test → handoff.

Method and data discovery inform each other. Feasibility may permit a bounded pilot
before final targets are known. A baseline usually reuses existing code; custom model
development is conditional on evidence, not a mandatory precursor to every baseline.

## Gates

| Gate | Sufficient evidence | If not satisfied |
|---|---|---|
| requirements | Task/I/O/labels and operating conditions specified; objective, hard constraints, critical slices, and budget recorded. Thresholds are user-defined, justified proposals, or explicitly unresolved. Evaluation contract has an ID. | Ask about consequential ambiguity; bounded discovery is allowed, but do not claim readiness for final acceptance. |
| feasibility | Data/access/rights, resources, and implementation path assessed; GO or a CONDITIONAL_GO with a bounded authorized pilot that addresses the uncertainty. | Resolve access/data/label gaps or explain NO_GO. Reassess after the pilot. |
| data | Versioned manifests/splits; schema, integrity, labels, domain coverage, duplicate/group leakage audits; limitations and exceptions explained. | Repair/quarantine issues reproducibly; acquire or relabel data where warranted. Never silently discard difficult valid samples. |
| baseline | Reproducible reference, sanity checks, validation protocol, config, environment, and preserved checkpoint. | Debug the pipeline before optimization. Initial baseline training does not require an already-passed baseline gate. |
| evaluation | Comparable validation results; frozen selected candidate and operating point; held-out acceptance results and sample support; hard constraints checked. | Analyze gaps. If test results drive new decisions, treat that test as development evidence and obtain independent final evidence. |
| delivery | Loadable checkpoint/artifact, runnable inference/evaluation recipe, actual acceptance table, environment, hashes/versions, limitations, and reproduction smoke check. | Repair the handoff or state precisely what cannot be verified. |

Use `PENDING`, `PASS`, `BLOCKED`, or `NOT_APPLICABLE` for each gate in state. A PASS must
link evidence. A scoped NOT_APPLICABLE needs a reason and is not a way to bypass a failed
requirement. The validator checks minimum gates for the current stage; the agent must
also judge whether the evidence is adequate for the intended action.

## Stopping and choosing the best model

Define in `problem/acceptance.md` and `problem/constraints.md` before a long optimization loop:

- Primary objective and direction; hard constraint and critical-slice thresholds.
- Tie-breakers or Pareto trade-offs when multiple candidates are acceptable.
- Budget and authorized scope: wall time, compute/cost, run count, or another practical bound.
- Stopping rule: accepted target, budget reached, plateau relative to noise, infeasibility,
  or user stop. Record the reason; do not invent a universal number of runs.

Select using validation under comparable protocols. Keep the best observed and best
eligible candidates separately if they differ. Account for uncertainty when gains are
small; use repeats/seeds proportional to the decision's stakes and available resources.
If the user asks to maximize quality within a budget, reaching a minimum target need
not end the agreed search. If they ask only to meet a target, unnecessary optimization
is not implied.

## Terminal outcomes

- `ACCEPTED`: all agreed hard requirements and the target are met on sufficient independent
  evidence, with a verified handoff. `project.status: COMPLETED` is reserved for this outcome.
- `BEST_AVAILABLE`: a bounded effort stopped with a usable result that has explicit gaps.
- `BUDGET_EXHAUSTED`: resource limit reached; preserve the best result and unmet targets.
- `INFEASIBLE`: current requirements/resources are incompatible based on evidence.
- `EVIDENCE_INSUFFICIENT`: data, access, test support, or verification cannot support a claim.

The latter four are `STOPPED` outcomes, not successful completion. Temporary blockers
use `BLOCKED`; a user pause uses `PAUSED`. A narrow review or dataset search can be
finished without declaring the whole model project complete.

## Resuming

Read state, recover current artifacts, verify running jobs/checkpoints and budgets, then
continue the relevant `next_action`. Do not relaunch a job solely because a record is old.
Changed labels, data splits, or metric definitions require a versioned protocol update,
invalidating affected gates and re-evaluating the baseline before claiming improvement.
