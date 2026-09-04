FROM python:3.13-slim

LABEL org.opencontainers.image.title="Karzoun SentinelAI" \
      org.opencontainers.image.description="Offline-first evaluation and regression testing for LLM applications and AI agents" \
      org.opencontainers.image.source="https://github.com/mkarson1997/karzoun-sentinel-ai" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /workspace

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN python -m pip install --no-cache-dir --no-deps .

RUN useradd --create-home --uid 10001 sentinelai \
    && chown -R sentinelai:sentinelai /workspace

USER sentinelai

ENTRYPOINT ["sentinelai"]
CMD ["--help"]
