# Problem Definition

Produce a precise, implementation-oriented definition.

Required sections:

- Task
- Input
- Output
- Label semantics
- Dataset
- Metrics
- Constraints
- Acceptance criteria
- Known unknowns
- Research contract ID and version
- Hard constraints versus preferences
- Operating envelope and critical subgroups
- Split/generalization unit
- Budget and stopping rule

Separate facts from assumptions.

A good definition should allow another engineer to implement and evaluate the baseline
without needing the original conversation. Acceptance criteria must be measurable or
explicitly marked as unresolved; never invent a numeric threshold silently.

Use [problem](../../templates/problem.md), [constraints](../../templates/constraints.md),
and [acceptance](../../templates/acceptance.md) templates. User-specified criteria already
count as agreed; do not force a second approval. When thresholds are unknown, propose
options in context or run an authorized bounded baseline to measure feasibility. Keep
acceptance unresolved until the user decides; this need not block inexpensive discovery.
