from crewai import LLM


class OpenRouterProvider:
    def __init__(self, api_key=None, model="google/gemini-2.0-flash-001"):
        self.api_key = api_key
        self.model = model

    def get_llm(self):
        # OpenRouter models require the openrouter/ prefix and explicit base_url
        # to ensure LiteLLM doesn't misroute them (especially free models).
        return LLM(
            model=f"openrouter/{self.model}",
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )
