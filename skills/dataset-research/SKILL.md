# Dataset Research

Find datasets that can actually improve the target model.

Evaluate:

- task relevance
- annotation semantics
- annotation quality
- scale
- domain
- viewpoint
- occlusion characteristics
- keypoint definition
- image/video source
- license
- access/download path
- preprocessing burden
- split
- known label noise
- domain gap

For every dataset, explicitly distinguish:
- directly usable
- convertible
- weakly related
- unsuitable

Never call a dataset “suitable” merely because its name contains the target task.

Compare coverage against the actual input, label taxonomy, operating conditions, and
generalization unit. Public data may support pretraining without being suitable for
final evaluation. When gaps matter, plan targeted collection, annotation/quality checks,
or relabeling with cost estimates; do not assume augmentation closes a domain gap.
Preserve annotation provenance, ambiguity/ignore rules, source licensing, and test data
isolation. Use [dataset template](../../templates/dataset.md).
