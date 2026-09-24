# Experiment

An experiment is a controlled test of a hypothesis.

Required fields:

- ID
- date
- hypothesis
- baseline
- changed variables
- fixed variables
- dataset version
- training config
- evaluation protocol
- expected outcome
- actual outcome
- interpretation
- next action
- resource budget and stopping condition
- artifact paths, code revision, environment, and seed

Prefer one major variable change.

If multiple variables change, explicitly record the confounding factors.

Every experiment should leave behind enough information to reproduce it.

Use validation to decide; do not tune against final test results. Prefer experiments
that address the largest observed failure or uncertainty per unit cost. A data/label
fix, simpler baseline, or decision to stop can be more valuable than a new architecture.
Do not promote a checkpoint that violates a hard constraint because a secondary metric
improved. Record best observed and best eligible candidates separately when necessary.
