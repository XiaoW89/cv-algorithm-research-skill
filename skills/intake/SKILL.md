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
- Target metric
- Compute
- Runtime
- Framework
- Pretrained model availability
- Required output artifact

## Example

User: “研究骨骼点遮挡分类算法”

Ask first:

1. Input: image / keypoint coordinates / keypoint + confidence / keypoint + image feature?
2. Output: binary visible/occluded per keypoint / multiple occlusion levels?
3. Existing pose estimator?
4. Existing occlusion-labeled data?

Do not ask downstream product questions unless they affect the model itself.

## Stop condition

If a missing answer can materially change the architecture or dataset strategy, do not
pretend the problem is fully defined.
