# CV Algorithm Research Workspace

This directory is created and managed by `cv-algorithm-research`.

## Structure

- `STATE.md`: current control state
- `problem/`: task definition and constraints
- `feasibility/`: resource, data, and risk assessment
- `literature/`: research evidence and method taxonomy
- `datasets/`: dataset candidates, selection, and conversion
- `models/`: candidate and selected model records
- `hypotheses/`: active and historical hypotheses
- `experiments/`: experiment records
- `failures/`: failure cases and analysis
- `conclusions/`: current engineering conclusions
- `evaluation/`: versioned evaluation protocol and reports
- `delivery/`: reproducible handoff

Do not use `STATE.md` as a detailed diary. Put detailed evidence in the corresponding
Markdown artifact.

Use `python <skill-dir>/scripts/validate_state.py --root research --strict` from the
project directory before handoff. A structurally valid state is
not evidence that the model meets the user's target.
