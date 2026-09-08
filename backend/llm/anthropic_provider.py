import os
from crewai import LLM

from backend.llm import DEFAULT_TIMEOUT_SECONDS


class AnthropicProvider:
    def __init__(self, api_key=None, model="claude-3-haiku"):
        self.api_key = api_key
        self.model = model

    def get_llm(self):
        if not self.api_key:
            return LLM(
                model=f"anthropic/{self.model}",
                api_key=self.api_key,
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        # crewai's native Anthropic client (as of 1.10.1) has a bug where it never
        # forwards the api_key constructor arg to its base class, so it silently
        # falls back to reading ANTHROPIC_API_KEY from the environment instead.
        # The Anthropic SDK client is constructed synchronously inside LLM(...),
        # so we set the env var only for that call and restore it immediately after,
        # rather than leaving it mutated for the whole process/session lifetime.
        previous = os.environ.get("ANTHROPIC_API_KEY")
        os.environ["ANTHROPIC_API_KEY"] = self.api_key
        try:
            return LLM(
                model=f"anthropic/{self.model}",
                api_key=self.api_key,
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )
        finally:
            if previous is None:
                os.environ.pop("ANTHROPIC_API_KEY", None)
            else:
                os.environ["ANTHROPIC_API_KEY"] = previous
