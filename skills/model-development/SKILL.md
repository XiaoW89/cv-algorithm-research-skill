# Model Development

Convert the selected method into a project implementation.

Priorities:

1. Preserve the method's intended computation.
2. Minimize source changes.
3. Reuse existing infrastructure where possible.
4. Keep interfaces explicit.
5. Make pretrained weight loading deterministic.
6. Add unit/smoke tests for new components.

Typical tasks:

- new prediction head
- feature aggregation
- loss implementation
- input adaptation
- output decoding
- checkpoint conversion
- training loop integration
- evaluation integration

Do not redesign the whole codebase merely to fit a research method.
