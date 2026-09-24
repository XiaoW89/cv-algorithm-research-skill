# Data Engineering

Turn raw candidate data into a reproducible training dataset.

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

Requirements:

- preserve raw data
- make transformations deterministic where possible
- record scripts and parameters
- record dataset version
- never silently mix incompatible label semantics

Recommended artifacts:

- `research/datasets/conversion.md`
- dataset manifests
- dataset statistics
- version identifiers
