# Data audit and manifest helper

Use the project's existing manifest and loaders when available. An optional neutral CSV
adapter lets `scripts/audit_manifest.py` run common checks across tasks without assuming
a label format. One row represents one model input sample, not one box/instance.

| Column | Meaning |
|---|---|
| `sample_id` | Required, globally unique string |
| `split` | Required: `train`, `val`, or `test` |
| `path` | Required local input path; relative to the CSV directory or `--data-root` |
| `group_id` | Optional independent group that must not cross splits; required with `--require-groups` |
| `sha256` | Optional input-byte digest; 64 hex characters |
| `label_path` | Optional annotation file, checked for existence with `--check-files` |
| other columns | Retained metadata; count selected ones using repeated `--slice-column` |

Namespaced group IDs must encode the intended independence unit. Use separate checks
or a composite connected-component group for multiple leakage relations. Sample ID and
path duplication are rejected. Repeated group IDs within one split are valid; groups
and exact hashes crossing splits are errors. Within-split identical content is a warning
requiring review. `--hash-files` reads each input to compute and verify SHA-256 and implies
file checks; use it only when the I/O cost is justified. No files are modified.

```sh
python <skill-dir>/scripts/audit_manifest.py manifest.csv --check-files --require-groups
python <skill-dir>/scripts/audit_manifest.py manifest.csv --hash-files --slice-column condition
```

JSON is printed to stdout; exit 0 means the selected automated checks found no errors,
exit 1 means errors. Warnings and `checks_not_performed` must be carried into
`research/datasets/audit.md`. A clean manifest is never proof that all data checks passed.

## Additional task-aware audit

Use [audit template](../templates/data-audit.md) and the actual dataset loader to record:

- file decoding and label/schema validity; out-of-bounds geometry, missing labels,
  conflicting taxonomies, ignored/uncertain labels, and annotator consistency as relevant;
- visual inspection of stratified examples, not just random easy samples;
- class/attribute/size/condition distribution and support per split and critical slice;
- exact and near duplicates, inherited derivatives/augmentations, group/time leakage;
- provenance, collection/annotation rights, dataset/transform versions and exclusions;
- real-versus-synthetic composition and deployment domain gaps;
- affected counts, decisions, and reversible remediation commands.

Split before making derived samples; fit learned preprocessing/statistics on training
data only. Augmentation and rebalancing belong to training unless the evaluation protocol
explicitly says otherwise. Never overwrite raw data or silently remove hard samples.
When annotations are missing or noisy, propose targeted labeling with guidelines and
review sampling instead of training around an unmeasured data problem.
