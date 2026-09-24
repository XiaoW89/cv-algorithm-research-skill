# Training

Training is an execution stage, not an experiment definition.

Record:

- command
- config
- dataset version
- model revision
- initialization
- optimizer
- scheduler
- batch size
- epochs
- augmentation
- device
- checkpoint
- resume state
- final metrics
- wall time, storage, and failure/retry information when material

Before long GPU training, confirm the intended run when user authorization is ambiguous.

Keep training configuration separate from the experiment hypothesis.
Before a long run, verify that the data audit, baseline sanity checks, metric direction,
and authorized budget are recorded. Stop on a defined failure or budget condition and
preserve logs/checkpoints; do not silently restart until a favorable result appears.

Record the run/job ID, log location, process/session status, elapsed budget, and latest
usable checkpoint. Monitor loading, finite losses, validation behavior, and resource use
at a cadence appropriate to the run. Early stopping and checkpoint selection use the
declared validation protocol. On interruption, verify the existing job and checkpoint
before resuming; do not create a duplicate run. Diagnose failures and record them before
spending the remaining budget on a retry.
