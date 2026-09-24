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

Write only artifacts useful to the decision:

- `research/literature/search-log.md`
- `research/models/candidates.md`

Use [search template](../../templates/search.md) and
[selection template](../../templates/selection.md). Add a paper matrix or taxonomy only
when the candidate set warrants it; do not produce duplicate catalogs by default.

Record queries, date, primary URLs/identifiers, code revision/release, retrieved evidence,
and access limitations. Verify claimed code/checkpoint availability and license separately
from paper results. Search task and domain requirements, not just fashionable model names.
Stop when enough grounded alternatives exist for a baseline decision or the agreed
research budget is exhausted. Unverified candidates may remain proposals, never facts.

Use external research skills for paper retrieval/deep reading when available.
