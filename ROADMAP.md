# SentinelAI Roadmap

## v0.1 Offline Evaluation Core

- [x] Provider-neutral evaluation cases
- [x] Prompt-injection signal evaluator
- [x] Groundedness regression baseline
- [x] Sensitive-output detector with redaction
- [x] JSONL datasets
- [x] Parallel evaluation runner
- [x] JSON and Markdown reports
- [x] Regression gates
- [x] CLI
- [ ] Built-in red-team benchmark catalog

## v0.2 Model & Agent Adapters

- [ ] OpenAI-compatible HTTP adapter
- [ ] Ollama adapter
- [ ] Anthropic adapter
- [ ] Provider timeouts and retry policy
- [ ] Agent trace schema
- [ ] Tool-call assertions

## v0.3 Advanced Evaluation

- [ ] Semantic groundedness evaluator
- [ ] LLM-as-judge adapter with calibration guidance
- [ ] Pairwise model comparison
- [ ] Latency and token-cost metrics
- [ ] Custom rubric DSL
- [ ] Dataset slicing and tags

## v0.4 Security Lab

- [ ] Prompt-injection benchmark packs
- [ ] Indirect-injection document fixtures
- [ ] Data-exfiltration test cases
- [ ] Tool-abuse simulations
- [ ] Canary-token assertions
- [ ] OWASP-aligned report mapping

## v1.0

Stable evaluator, dataset, provider, report, and regression-gate APIs with documented calibration and security guarantees.
