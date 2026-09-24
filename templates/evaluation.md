# Evaluation Protocol

## Identity

- Protocol ID / version:
- Evaluator code revision:
- Metric definitions and direction:

## Data and split

- Dataset/version/hash:
- Split/test identity:
- Independent generalization unit:
- Exclusions and ignore rules:
- Critical slices and minimum support:

## Inference and aggregation

- Preprocessing / resolution:
- Decoder/matching/postprocessing:
- Threshold selection source:
- Averaging / weighting:

## Resource measurement

- Hardware/software:
- Precision, batch, warmup:
- Latency scope and synchronization:
- Memory/power measurement if required:

## Acceptance results

| Criterion | Result | Support/uncertainty | Status | Evidence |
|---|---|---|---|---|
| | | | `PASS` / `FAIL` / `INSUFFICIENT_EVIDENCE` | |

## Test-set use log

Record every decision made after viewing final-test results. If any result changed model,
threshold, data, or augmentation selection, this protocol is no longer a final holdout.
