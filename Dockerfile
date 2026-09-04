FROM python:3.13-slim

LABEL org.opencontainers.image.title="Karzoun SentinelAI" \
      org.opencontainers.image.description="Offline-first evaluation and regression testing for LLM applications and AI agents" \
      org.opencontainers.image.source="https://github.com/mkarson1997/karzoun-sentinel-ai" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workspace/src

WORKDIR /workspace

COPY src ./src

RUN useradd --create-home --uid 10001 sentinelai \
    && chown -R sentinelai:sentinelai /workspace

USER sentinelai

ENTRYPOINT ["python", "-m", "karzoun_sentinel.cli"]
CMD ["--help"]
