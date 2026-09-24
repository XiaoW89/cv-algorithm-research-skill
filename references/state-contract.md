# State contract

`research/STATE.md` is a Markdown wrapper containing exactly one YAML code block. The
validator parses that block. Keep it concise and link detailed evidence rather than
embedding a diary. Existing workspaces may omit new fields; migrate only missing fields
and preserve user values.

Required control fields:

- `schema_version`: integer `1`;
- `project.status`: `ACTIVE`, `BLOCKED`, `PAUSED`, `STOPPED`, or `COMPLETED`;
- `project.outcome`: null while active, otherwise a terminal outcome from `WORKFLOW.md`;
- `research_stage`: a known stage name;
- `gates`: each gate is `PENDING`, `PASS`, `BLOCKED`, or `NOT_APPLICABLE`;
- `gate_evidence`: a list of evidence file paths for each gate; `gate_notes` explains exceptions;
- `next_action`, `blockers`, `open_questions`, `best_checkpoint`;
- `acceptance`: contract ID, status, primary metric/targets, and evidence path;
- `reproduction`: command, config, data, code revision, environment;
- `budget`: scope, used, remaining, and stopping reason when stopped.

`COMPLETED` marks successful completion of the model project, not a narrow research
question. It requires `project.outcome: ACCEPTED`, `acceptance.status: ACCEPTED`, all six
gates PASS, a best checkpoint, acceptance and delivery evidence paths, and a filled
reproduction recipe. Use `STOPPED` with a reason for best-available, budget-exhausted,
infeasible, or evidence-insufficient outcomes. A blocked project must name its blockers.

`best_checkpoint` is the recommended deliverable, whose eligibility must be explicit.
Record a different best-observed or best-eligible candidate in `models/selected.md`.
`APPROVED` acceptance means criteria are already supplied/agreed, not an extra approval
meeting. Unresolved targets stay DRAFT during an explicitly bounded pilot.

Evidence and local checkpoint paths resolve relative to `research/` (or may be absolute).
Strict mode requires nonempty local evidence files. A remote checkpoint URI needs a
verified hash/load result in the handoff; the validator warns and does not fetch it.
The validator checks types, stage prerequisites, recorded claims, and file existence;
it cannot judge whether a report is true or complete.

## Validation levels and migration

- Default: parse YAML, reject duplicate keys/invalid enums/types, and check declared
  evidence links. File existence and execution-stage gates are checked only in strict mode.
- Strict: additionally require the current execution stage's prerequisite gates and
  evidence files. Initial baseline training needs requirements/feasibility/data, not an
  already-complete baseline. Evaluation of supplied weights needs requirements/data.
  An optimization experiment additionally needs the baseline. Paused/blocked/stopped
  projects can retain unmet gates. DELIVERY can document an unsuccessful outcome; only
  COMPLETED requires every success gate.
- Legacy: the original state without `schema_version` and `gates` is readable in default
  mode with a warning. Strict mode requests migration. Copy missing schema fields from
  the template, map old stage-like `project.status` to the actual activity status, and
  retain the stage in `research_stage`. Inspect evidence before setting any gate PASS.
  No helper rewrites an existing state automatically.

When a protocol, split, label schema, or metric changes, bump its ID/version, invalidate
affected gates, and record the reason. A stale checkpoint is not evidence of current
acceptance.
