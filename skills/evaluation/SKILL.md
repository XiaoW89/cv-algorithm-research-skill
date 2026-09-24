# Evaluation

Evaluate against a fixed protocol.

Read [evaluation profiles](../../references/evaluation-profiles.md) for the current task.
Use [evaluation template](../../templates/evaluation.md) for protocol and results.

Derive metrics from the task and research contract. Do not use a familiar metric merely
because it is common in a paper. Define the operating point, aggregation, matching or
threshold rules, sample support, and which metrics are hard constraints.

Record:

- overall metrics
- per-class/per-keypoint metrics
- subgroup metrics
- error distributions
- calibration where useful
- runtime / memory when relevant
- baseline comparison
- acceptance status for every hard constraint and target
- test-set identity and whether it was used for any prior decision

Do not change the split or metric after seeing the result without recording the change.

Use validation for model/threshold selection and a locked held-out set for final
acceptance. Report subgroup or condition results whenever the contract names them. If a
test result changes the plan, mark the test as development evidence and obtain new
independent evidence before claiming final generalization.
