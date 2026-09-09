# Karzoun SentinelAI

[![CI](https://github.com/mkarson1997/karzoun-sentinel-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/mkarson1997/karzoun-sentinel-ai/actions/workflows/ci.yml)
[![CodeQL](https://github.com/mkarson1997/karzoun-sentinel-ai/actions/workflows/codeql.yml/badge.svg)](https://github.com/mkarson1997/karzoun-sentinel-ai/actions/workflows/codeql.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=mkarson1997_karzoun-sentinel-ai&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mkarson1997_karzoun-sentinel-ai)
[![Release](https://img.shields.io/github/v/release/mkarson1997/karzoun-sentinel-ai)](https://github.com/mkarson1997/karzoun-sentinel-ai/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

> Open-source evaluation and regression testing for LLM applications and AI agents.

**SentinelAI** is a Python-first toolkit for evaluating AI outputs before they reach production. It turns prompts, responses, grounding context, and future agent traces into repeatable test cases that can run locally or inside CI.

The core is intentionally **offline-first and provider-neutral**. You can evaluate recorded outputs without API keys, network access, or dependency on a specific model vendor.

## What it catches today

- Prompt-injection signals such as instruction override, hidden-prompt exfiltration, explicit guardrail bypass, and credential-exfiltration requests
- Weakly grounded claims against supplied evidence using a deterministic lexical regression baseline
- Credential-shaped material in model responses with report-safe redaction
- New AI regressions through score-drop limits and newly failing case detection
- Dataset failures from JSONL test suites

SentinelAI does **not** claim that regular expressions solve prompt injection or that lexical overlap solves hallucination detection. Those evaluators are transparent deterministic baselines designed for repeatable regression testing. Semantic and model-assisted evaluators are on the roadmap.

## Engineering proof points

| Area | What the repository demonstrates |
| --- | --- |
| AI evaluation architecture | Provider-neutral cases and composable evaluators separated from model execution. |
| Deterministic regression | Repeatable recorded-output evaluation suitable for local and CI use without API keys. |
| Security-minded data handling | Adversarial prompts/responses are treated as untrusted data, and credential-shaped findings redact matched values. |
| Honest evaluator semantics | Prompt-injection and groundedness logic are explicitly documented as heuristic baselines rather than universal detectors. |
| Parallel execution | Bounded `ThreadPoolExecutor` case evaluation without making completion order part of report semantics. |
| Regression gates | Baseline/current comparison fails on configured score drops and newly failing cases. |
| Reporting | Stable JSON and human-readable Markdown artifacts from a normalized result model. |
| Verification | Ruff, Mypy, Pytest, Python 3.11/3.12/3.13 CI, CodeQL and SonarQube Cloud. |
| Delivery | Versioned GitHub Releases plus a non-root GHCR container. |
| Supply-chain hygiene | GitHub Actions used by CI, CodeQL and packaging are pinned to reviewed immutable commits. |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

sentinelai evaluate examples/basic.jsonl --workers 4 \
  --json report.json \
  --markdown report.md
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

A dataset is newline-delimited JSON:

```json
{"id":"order-status","prompt":"Where is order 42?","response":"Order 42 shipped on Tuesday from Ankara.","context":["Order 42 shipped on Tuesday from the Ankara warehouse."]}
```

## Container image

Versioned images are published to GitHub Container Registry together with releases:

```bash
docker run --rm -v "$PWD:/workspace" \
  ghcr.io/mkarson1997/karzoun-sentinel-ai:0.1.0 \
  --help
```

The image runs the `sentinelai` CLI as a non-root user. For private-package visibility, authenticate to `ghcr.io` before pulling; public package visibility can be enabled from the package settings.

## Python API

```python
from karzoun_sentinel import EvaluationCase, EvaluationSuite

suite = EvaluationSuite()
result = suite.evaluate(
    [
        EvaluationCase(
            id="grounded-order",
            prompt="Where is order 42?",
            response="Order 42 shipped on Tuesday from Ankara.",
            context=("Order 42 shipped on Tuesday from the Ankara warehouse.",),
        )
    ]
)

print(result.passed)
print(result.score)
```

## Regression gate

Store a known-good JSON report, then compare a new run against it:

```bash
sentinelai compare baseline.json current.json --max-score-drop 0.05
```

The command exits non-zero when the suite drops beyond the allowed threshold or introduces newly failing cases, making it suitable for CI quality gates.

## Architecture

```text
Prompt + Response + Context
            |
            v
+---------------------------+
| EvaluationSuite           |
| deterministic / parallel  |
+---------------------------+
      |        |        |
      v        v        v
 Injection Grounded  Sensitive
 detector   baseline   output
      \        |        /
       \       |       /
        v      v      v
+---------------------------+
| normalized SuiteResult    |
+---------------------------+
       |               |
       v               v
 JSON / Markdown     Regression gate
```

See [`docs/architecture.md`](docs/architecture.md) for the trust boundary, design invariants, evaluator semantics, parallelism model and explicit non-claims.

## Current v0.1 capabilities

- Provider-neutral `EvaluationCase` model
- Composable evaluator protocol
- Prompt-injection heuristic detector
- Groundedness regression baseline
- Sensitive-output detector with matched-secret redaction
- JSONL dataset loader with validation
- Deterministic parallel evaluation runner
- JSON and Markdown reports
- Regression comparison API
- CI-friendly CLI
- Strict typing with Mypy
- Ruff linting
- Pytest test suite
- Python 3.11, 3.12, and 3.13 CI matrix
- SonarQube Cloud quality gate and GitHub CodeQL security analysis
- Versioned GitHub Releases and GHCR container packaging
- Dependency update automation with Dependabot

## Security and delivery controls

- CI verifies Python 3.11, 3.12 and 3.13 with Ruff, Mypy and Pytest behind an aggregate `CI Gate`
- CodeQL runs the Python security-extended query suite
- SonarQube Cloud provides an additional quality gate on pull requests
- third-party GitHub Actions used by CI, security analysis and release packaging are pinned to reviewed immutable commit SHAs
- verification dependencies are synchronized from the lockfile with `uv`
- evaluation inputs remain offline data in v0.1 rather than executable model/tool instructions
- credential-shaped findings redact the matched value before reporting
- the published container runs the CLI as a non-root user

## Roadmap

The next milestones add model execution and deeper evaluation without coupling the core to one provider:

1. OpenAI-compatible and Ollama adapters
2. Agent trace and tool-call assertions
3. Pairwise model comparison
4. Semantic groundedness and calibrated model-assisted judging
5. Prompt-injection benchmark packs and indirect-injection fixtures
6. Latency and token-cost regression metrics
7. Custom rubric DSL

Full plan: [`ROADMAP.md`](ROADMAP.md).

## Project metadata

- Releases: [`CHANGELOG.md`](CHANGELOG.md) and [GitHub Releases](https://github.com/mkarson1997/karzoun-sentinel-ai/releases)
- Citation: [`CITATION.cff`](CITATION.cff)
- Attribution: [`NOTICE`](NOTICE)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)

## Security

AI evaluation datasets frequently contain adversarial text. SentinelAI treats prompts, responses, contexts, and future traces as **untrusted data**, not executable instructions. Credential findings redact the matched value before reporting it.

See [`SECURITY.md`](SECURITY.md).

## Contributing

Contributions are welcome. Please keep scoring semantics explicit, add tests for evaluator changes, and never commit real credentials or private customer prompts.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
