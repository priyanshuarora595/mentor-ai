# Default timeouts (seconds) for LLM completion requests, applied uniformly
# across providers so a single stalled request can't block a crew run
# indefinitely (none of the providers set one by default otherwise).
DEFAULT_TIMEOUT_SECONDS = 90
# Local inference (esp. on CPU-only hardware) is often slower than cloud APIs.
OLLAMA_TIMEOUT_SECONDS = 180
