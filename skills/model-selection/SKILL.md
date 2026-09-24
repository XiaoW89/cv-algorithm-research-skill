# Model Selection

Select a practical model family using evidence and constraints.

Evaluate:

- task fit
- input fit
- label fit
- data availability
- reported evidence
- released code
- released weights
- expected quality
- compute
- implementation cost
- maintenance risk

Do not use an arbitrary overall score.

Filter candidates by hard constraints first. Compare the remainder on the primary
objective, evidence, reproducibility, cost, implementation risk, and expected failure
modes. Keep a fallback baseline and state what would change the decision. Present
unresolved trade-offs to the user rather than inventing weights for a combined score.

Use [selection template](../../templates/selection.md). Record the implementation plan,
data recipe, validation plan, budget, and fallback in `research/models/selected.md`.

Record trade-offs explicitly in:

`research/models/selected.md`
