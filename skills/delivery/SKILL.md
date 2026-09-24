# Model delivery

Prepare a handoff that another engineer can run and evaluate without reconstructing the
conversation. Include:

- accepted or best-available status and the acceptance table;
- model/checkpoint/export identity, code revision, environment, and artifact hashes;
- exact preprocessing, postprocessing, input/output schema, thresholds, and dependencies;
- dataset version, split/test identity, training configuration, and evaluation command;
- measured quality, runtime/resource measurements when relevant, known failure modes,
  unsupported conditions, and limitations;
- a smoke reproduction on a small fixed sample and the expected output contract.

Do not describe an unverified export, deployment runtime, or metric as completed. If the
target is not met, state the gap and the best available candidate instead of changing the
acceptance definition after seeing the result.

Use [handoff template](../../templates/handoff.md), check [workflow](../../WORKFLOW.md)
terminal outcomes, and run strict state validation before declaring model completion.
