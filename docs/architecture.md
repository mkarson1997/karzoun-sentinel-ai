# Architecture

SentinelAI separates evaluation semantics from model execution. The core can evaluate recorded prompts and responses with no network access, API key, or model provider.

```text
JSONL / Application Data
          |
          v
+-----------------------+
| EvaluationCase        |
+-----------------------+
          |
          v
+-----------------------+
| EvaluationSuite       |
| - deterministic order |
| - optional parallel   |
+-----------------------+
    |        |        |
    v        v        v
 Injection Grounded  Sensitive
 signals   baseline   output
    \        |        /
     \       |       /
      v      v      v
+-----------------------+
| SuiteResult           |
+-----------------------+
    |              |
    v              v
 JSON/Markdown     Regression gate
```

## Design boundaries

- **Evaluation cases are provider-neutral.** A case contains a prompt, recorded response, optional grounding context, and metadata.
- **Evaluators are composable.** Each evaluator returns a normalized score, pass/fail decision, findings, and metrics.
- **The initial groundedness evaluator is explicitly heuristic.** It is a deterministic lexical regression baseline, not a substitute for semantic factuality judging.
- **Secrets are redacted from findings.** Sensitive-output findings report the class of leak, never the matched secret value.
- **Regression is a first-class use case.** Reports are stable machine-readable artifacts that can gate CI.

Future provider adapters will generate responses and agent traces, but model execution will remain outside the evaluator contract.
