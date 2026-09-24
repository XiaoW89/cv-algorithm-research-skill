# Task-dependent measurement

Choose the relevant rows; these are options, not mandatory metrics. For a custom task,
derive its success measure from output semantics and error cost, then sanity-check the
evaluator using known predictions. Do not force it into a familiar task category.

| Task/output | Candidate quality measures | Protocol details and common traps |
|---|---|---|
| Single/multi-label classification | Macro/per-class precision, recall, F1; accuracy or PR-AUC when justified | Class prevalence, multilabel thresholds, unknown classes, imbalance, and label leakage |
| Detection / oriented boxes | AP with explicit IoU convention; recall at agreed precision/false-positive rate | Box convention, matching, NMS, score threshold, tiny objects, ignored regions, class mapping |
| Semantic/instance segmentation | Per-class IoU/Dice, boundary errors; instance AP where relevant | Void labels, mask resize/interpolation, empty masks, touching instances, class support |
| Keypoints / pose | PCK, OKS/AP, coordinate error under a defined normalization | Visibility/occlusion convention, skeleton mapping, coordinate space, missing points |
| Tracking / temporal output | HOTA/IDF1 or task-specific temporal consistency and misses | Independent sequences, initialization, identity conventions, frame rate, detector contribution |
| Depth / geometry / regression | MAE/RMSE, relative errors, threshold accuracy, task costs | Units, scale alignment, valid masks, coordinate frames, error distribution and range |
| Retrieval / verification | Recall@K, mAP, verification rates at fixed false-accept rates | Identity-disjoint protocol, gallery composition, duplicates, threshold fitting |
| Anomaly detection | Image/pixel PR-AUC or recall at allowed false-alarm rate | Rare positives, normal-only training, threshold tuning split, localization support |
| Restoration / enhancement | Paired distortion/perceptual metrics and downstream task utility | Reference alignment, unsupported perceptual claims, identity/content fidelity, domain shift |

## Evaluation contract

Write `research/evaluation/protocol.md` using [protocol template](../templates/evaluation.md):

- evaluator version, metric definition/direction/units, averaging, and sample weighting;
- data and split ID/hash, exclusions, independent evaluation unit, and critical slices;
- input resolution, preprocessing, decoding, matching, and threshold selection on validation;
- hard targets versus diagnostics, uncertainty method, and minimum support rationale;
- runtime hardware/software, precision, batch, warmup, synchronization, and latency scope
  when performance is constrained (model-only and end-to-end are different measurements).

Compute uncertainty at the independent unit where possible; adjacent frames do not
provide independent evidence. Small or empty slices are insufficient evidence, not a
passing result. Use repeat runs or seeds when needed to distinguish gains from variance.

Validation informs selection. A final holdout must not be used for augmentation design,
early stopping, threshold fitting, or checkpoint selection. If data is scarce, use an
explicit group-aware/nested validation design and state its limitations; do not fabricate
an independent holdout. Compare protocols before comparing numbers.

Report each acceptance criterion as PASS, FAIL, or INSUFFICIENT_EVIDENCE. Proposals and
unresolved thresholds cannot support PASS. Calibrate confidence only when its meaning
matters to the user, and fit calibration on development data, never the final holdout.
