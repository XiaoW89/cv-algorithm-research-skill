# Failure Analysis

Convert model errors into actionable hypotheses.

Analyze:

- false positives
- false negatives
- localization errors
- occlusion
- truncation
- scale
- viewpoint
- domain shift
- label ambiguity/noise
- hard negatives
- confidence behavior

For each important failure mode record:

- evidence
- frequency/impact if measurable
- likely cause
- confidence
- proposed intervention
- expected observable effect

Do not jump directly from “bad result” to “change model”.

Inspect representative samples and preprocessing/decoding/evaluator behavior before
attributing errors to architecture. Choose error categories appropriate to the task:
classification confusion, segmentation boundaries, temporal identity errors, regression
residuals, and others as needed. Quantify affected support and practical impact.
Assign a falsifiable hypothesis and a cheap diagnostic to each prioritized intervention.
Use development/validation samples; final-test-driven iteration needs new final evidence.
