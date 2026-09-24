# Feasibility assessment

Assess whether the requested result can be pursued with the available evidence and
resources. This is a decision artifact, not a confident prediction of final quality.

Use [feasibility template](../../templates/feasibility.md). Revisit after candidate/data
research or a pilot; early unknowns do not require abandoning useful cheap investigation.

Cover only dimensions that can affect the decision:

- task and label feasibility, including ambiguity and annotation availability;
- data access, rights, domain coverage, sample independence, and likely leakage;
- candidate implementation and dependency risks;
- compute, storage, time, runtime, hardware, and engineering capacity;
- evaluation observability: whether the target can be measured with enough support;
- safety, privacy, or operational constraints when relevant to the task.

For each material uncertainty record its current evidence, impact, confidence, cheapest
test, resource cost, and decision deadline. Prefer a small pilot or static audit over a
long training run when it answers the same question. Do not turn a paper's result into
local feasibility evidence.

Output `research/feasibility/assessment.md` with one of:

- `GO`: the next planned investment is justified;
- `CONDITIONAL_GO`: proceed only with named assumptions, bounded pilot, or mitigation;
- `NO_GO`: current requirements and resources are incompatible;
- `EVIDENCE_INSUFFICIENT`: the decision needs access, labels, or measurement first.

Record what would change the decision. A failed feasibility check is a useful result and
must redirect the plan rather than be hidden by starting training anyway.
