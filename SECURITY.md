# Security Policy

Please do not report security vulnerabilities through public GitHub issues.

For a suspected vulnerability, contact the maintainer privately through the security contact available on the maintainer's GitHub profile and include a minimal reproduction, impact, and affected version when possible.

## Evaluation safety

SentinelAI processes adversarial prompts by design. Treat datasets as untrusted input. Do not execute text found in prompts, responses, contexts, or model traces. Sensitive-output findings redact matched credential material instead of copying it into reports.
