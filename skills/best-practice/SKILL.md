# Best Practice Discovery

## Goal

Find existing methods that are strong, reproducible, and relevant to the actual task.

This is not a literature-review exercise.

## Existing research and user choice

Before external discovery on project intake/takeover, inspect `research/`, especially
`literature/`, `models/candidates.md`, and `models/selected.md`, and follow relevant
references to legacy reports elsewhere. Do not require these exact filenames or a
directory migration. A missing directory, empty templates, a bibliography alone, or
local experiment scores alone are not sufficient method-research evidence.

Judge sufficiency for the current decision, not exhaustive coverage or paper count:

- The task, inputs/outputs, label semantics, data conditions, and hard constraints match
  the current requirements; material changes and unresolved assumptions are identified.
- Relevant alternatives and the current baseline have traceable primary paper/code
  sources, with reported results tied to their data and evaluation protocols.
- Code/weights availability, license, reproducibility, and engineering costs/risks are
  assessed where relevant; unavailable or unchecked items are explicit.
- A comparison explains the selection or next experiment and what remains uncertain.
  Dates/versions and changed requirements support judging whether records remain usable;
  age alone does not require a new search. Documented negative search results can help
  justify limited alternatives; do not invent candidates to meet a quota.

If sufficient, cite and reuse the evidence. If missing or insufficient, summarize the
specific gaps, propose a bounded paper/GitHub search, and ask whether the user wants it
now, deferred, or skipped. Do not start external discovery while the choice is pending;
continue independent, authorized local checks. An explicit request for algorithm
research or existing authorization covering that research resolves the choice without
another question; a generic instruction to continue the project does not.

If approved, fill only the missing evidence within the agreed scope/budget. If deferred
or skipped, record the choice and proceed within the remaining authorized scope; do not
mark research complete or claim broadly grounded method selection. Silence is not a
choice. Preserve the decision on resume unless its scope or material assumptions change.

## Research evidence reconciliation

Before declaring the survey sufficient or using a candidate to justify implementation,
reconcile claims in the log and candidate matrix against the source artifacts actually
retrieved. This is an evidence audit, not a second literature search. Assign the
survey one status:

- `SUFFICIENT`: decision-critical candidates and the baseline have traceable sources;
  source identity, evidence depth, implementation facts, and limitations agree; the
  remaining unknowns do not prevent the stated next decision.
- `PARTIAL`: enough grounded evidence exists for a provisional direction, but material
  gaps remain. Continue only with the limitations and provisional status visible.
- `INSUFFICIENT`: the evidence cannot support even a bounded method decision; ask for
  clarification, more research, or a justified defer/skip choice.
- `PENDING_VERIFICATION`: records conflict or a decision-critical claim cannot yet be
  reconciled. Do not silently choose the more favorable version or treat the candidate
  as verified until the conflict is resolved.

For each decision-critical paper or implementation, check as applicable:

1. **Identity:** title, author/year, DOI/arXiv/other identifier, and the cited source
   refer to the same work. Do not merge records by a similar title alone.
2. **Evidence depth:** distinguish metadata, abstract, full text, official code, and
   local measurement. If a retrieval helper reports `abstract_only`, a short parse, a
   missing end marker, or a different sentinel/path than the log, downgrade the claim or
   mark it `PENDING_VERIFICATION`; do not report full-text findings as fact.
3. **Implementation facts:** verify repository reachability, relevant revision/tag,
   license, checkpoint availability, and dependencies separately. A URL in a table is
   not proof that code, weights, or a usable license was checked. Mark each unavailable
   item `[UNVERIFIED]`.
4. **Claim mapping:** reported metrics remain tied to the paper's dataset, split,
   input, and protocol; architectural transfer is labelled `[INFERENCE]` or
   `[HYPOTHESIS]`, not presented as a local result. Local measurements must point to a
   reproducible run or artifact.
5. **Decision impact:** state whether each discrepancy changes the candidate ranking,
   proposed experiment, or only the confidence. Preserve the contradiction and the
   remediation, rather than deleting or silently rewriting the earlier record.

Record the reconciliation status, checks performed, discrepancies, external skills used
and their distinct roles, and the search stop reason in `research/literature/search-log.md`
or a linked evidence-audit file. A candidate with unresolved decision-critical evidence
may remain in the matrix, but cannot be the sole basis for a non-provisional selection.
Do not require full text when access is genuinely unavailable; require accurate evidence
depth and restrict the claims accordingly. Reconcile again when a source, task, or hard
constraint changes.

Record inspected sources, sufficiency/gaps, user choice and scope, and selection limits
in an existing relevant report or `research/literature/search-log.md` using the
[search template](../../templates/search.md). Keep only a brief decision and link in
`STATE.md`'s `decision_log`; leave an unanswered choice in `open_questions`. Do not create
dummy search entries when no external search occurred. Narrow evaluation/debugging
requests do not require a method survey unrelated to their scope.

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
research budget is exhausted, and record why the stop is justified. Unverified candidates
may remain proposals, never facts.

Once research is in scope, use the [capability-matching procedure](../../SKILL.md#external-capabilities)
to choose available skills by their descriptions for the actual search, reading, or
code-verification subtask. Do not assume one research skill covers all three.
