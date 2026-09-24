# Data Engineering

Turn raw candidate data into a reproducible training dataset.

Read [data audit](../../references/data-audit.md) for common checks and helper usage;
use the project's actual loader for annotation/decoding validation.

Typical operations:

1. Acquire
2. Verify
3. Convert
4. Normalize schema
5. Filter
6. Deduplicate
7. Split
8. Sample / rebalance
9. Augment or synthesize
10. Version
11. Generate manifest
12. Audit quality and leakage

Requirements:

- preserve raw data
- make transformations deterministic where possible
- record scripts and parameters
- record dataset version
- never silently mix incompatible label semantics
- keep raw data immutable and record checksums or stable source identifiers where possible
- define the independent unit for the split before generating train/validation/test
- audit duplicates, near-duplicates, grouped/sequential leakage, corrupt files, and
  label/schema violations
- preserve difficult valid samples; filtering requires a reason and count

Recommended artifacts:

- `research/datasets/conversion.md`
- dataset manifests
- dataset statistics
- `research/datasets/audit.md`
- version identifiers

The audit must report coverage of the agreed operating envelope and critical subgroups.
For sequential or grouped data, split by the unit that should generalize at deployment,
not by adjacent frames or randomly sampled records. Freeze the final test identity
before model selection; use validation for selection and keep the final test held out.
