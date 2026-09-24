# Intake / Clarification

## Goal

Convert a vague CV problem description into a technically actionable problem without
forcing the user through a fixed questionnaire.

## Procedure

1. Parse the user's description.
2. Identify unknowns.
3. Estimate whether each unknown can materially change:
   - task formulation
   - model family
   - input representation
   - dataset requirements
   - training strategy
   - evaluation protocol
4. Ask only the highest-impact questions.
5. After each answer, re-evaluate what remains ambiguous.

## Typical dimensions

- Input
- Output
- Label semantics
- Existing model
- Existing data
- Operating conditions and important subgroups
- Target objective, metric, and acceptance threshold
- Compute, time, storage, and runtime budget
- Framework
- Pretrained model availability
- Required output artifact
- Data rights, privacy, or safety constraints where relevant

Also identify the unit of generalization: what must be unseen at test time (for example
an identity, site, session, device, sequence, or future time). This determines the split
and leakage audit. Do not assume random sample splitting is valid.

Do not ask downstream product questions unless they affect the model itself.

Translate the answers into a short research contract before broad research. Unknowns may
remain, but each must say why it matters, how it will be resolved, and whether work can
continue under an explicit assumption.

## Stop condition

If a missing answer can materially change the architecture or dataset strategy, do not
pretend the problem is fully defined.
