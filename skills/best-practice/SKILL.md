# Best Practice Discovery

## Goal

Find existing methods that are strong, reproducible, and relevant to the actual task.

This is not a literature-review exercise.

## Search dimensions

Search across:

- classic strong baselines
- recent strong methods
- open-source implementations
- released checkpoints
- benchmark datasets
- task-specific engineering recipes

## Candidate record

For each method:

| Field | Content |
|---|---|
| Method | name |
| Task match | high / medium / low + explanation |
| Data match | explanation |
| Architecture | summary |
| Input | required input |
| Output | output representation |
| Loss | relevant loss |
| Code | availability |
| Checkpoint | availability |
| Dataset | training data |
| Reported result | metric + protocol |
| Reproducibility | assessment |
| Engineering cost | assessment |
| Risks | concrete risks |

Do not collapse this into a single score.

## Output

Write:

- `research/literature/search-log.md`
- `research/literature/paper-matrix.md`
- `research/literature/taxonomy.md`
- `research/models/candidates.md`

Use external research skills for paper retrieval/deep reading when available.
