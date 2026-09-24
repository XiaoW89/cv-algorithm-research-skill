# Baseline

Establish a trustworthy reference before optimization.

Use [baseline template](../../templates/baseline.md). Existing validated evidence may be
reused. Sanity checks can precede baseline training; a complete baseline record naturally
requires running and evaluating it first.

Record:

- model
- code revision
- dataset version
- split
- config
- seed
- initialization
- training command
- checkpoint
- evaluation command
- metrics
- runtime environment
- data-loading and label/schema checks
- tiny-set overfit or task-appropriate sanity check
- evaluation protocol identifier

A baseline that cannot be reproduced should not be treated as a reliable comparison point.
Preserve its checkpoint and configuration before changing code, data, or evaluation.
