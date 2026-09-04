# Contributing

Contributions are welcome.

1. Keep evaluators deterministic unless their contract explicitly documents external model use.
2. Add tests for every evaluator rule or scoring change.
3. Avoid including real credentials, private prompts, or customer data in fixtures.
4. Run `ruff check .`, `mypy src`, and `pytest` before submitting changes.
5. Document scoring semantics and known limitations. Evaluation tools are most useful when their uncertainty is visible.
