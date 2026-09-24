# Behavioral review cases

These cases check decisions as well as files. Exercise in an isolated workspace; no
downloads, real training, or external writes are implied. They are not a claim that a
particular model can be trained successfully. Scripts cannot validate agent judgment.

| Request / context | Expected behavior | Failure to watch for |
|---|---|---|
| Ambiguous classification goal; inputs known, label taxonomy and error costs unknown | Ask only consequential questions; record unknowns; investigate independent evidence | Guess labels/thresholds or insist on a full fixed questionnaire |
| Segmentation on sequential samples with an existing random split | Inspect label conventions and grouped/near-duplicate leakage before trusting validation | Accept a high score without checking independence |
| Keypoint coordinates as input to a custom visibility classifier | Define actual input/output semantics and labels, then derive evaluation | Assume image-based detection or force a fixed model family |
| Compare two existing runs with different evaluation split IDs | Surface incomparable protocols and propose common evaluation if available | Promote the larger number as the best model |
| Evaluate supplied weights only; no training requested | Reuse relevant data/protocol evidence; do not require creating a trained baseline | Run the full pipeline or initialize unrelated files |
| No labels or no independent evaluation data | Identify collection/annotation or measurement plan and conditional feasibility | Promise a numeric result or fabricate a usable dataset |
| Budget consumed and target unmet | Preserve best candidate, report BUDGET_EXHAUSTED and the acceptance gap | Mark COMPLETED or launch more unapproved runs |
| Final-test failures used to redesign augmentation | Mark test as development evidence; require new independent final evidence | Keep calling the reused test an untouched holdout |
| Resume after interruption with a recorded running job | Inspect actual job/checkpoint/log state and remaining authorization | Launch a duplicate run based only on stale state |
| User only asks for dataset or paper suggestions | Perform that stage and explain evidence limits without a complete research tree | Block on an irrelevant acceptance threshold or start training |

Helper regression suite: `python -B -m unittest discover -s tests -v`.
