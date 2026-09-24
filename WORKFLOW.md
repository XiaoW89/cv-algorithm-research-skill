# Recommended Operating Workflow

## A. New problem

1. Invoke `cv-algorithm-research`.
2. Inspect workspace.
3. Ask targeted Intake questions.
4. Initialize `research/`.
5. Write problem definition.
6. Search best practices.
7. Research datasets.
8. Engineer dataset.
9. Select model.
10. Implement baseline.
11. Train.
12. Evaluate.
13. Analyze failures.
14. Form hypothesis.
15. Run controlled experiment.
16. Repeat until model quality/constraints are satisfied.
17. Freeze the reproducible recipe and checkpoint.

## B. Existing research

If `research/STATE.md` exists:

1. Read it.
2. Recover current stage.
3. Inspect only the relevant detailed artifacts.
4. Continue from `next_action`.
5. Update state.

## C. User asks a narrow question

Do not run the whole pipeline.

Examples:

- “找数据集” → Dataset Research
- “这个方法怎么实现” → Model Development
- “为什么 recall 掉了” → Failure Analysis
- “比较这两个实验” → Experiment / Evaluation
- “继续训练” → Training, after verifying current state/config

## D. Deliverable

A useful final model handoff contains:

- model architecture
- code revision
- dataset version
- preprocessing
- training command/config
- checkpoint
- evaluation command/protocol
- achieved metrics
- known failure modes
- limitations
