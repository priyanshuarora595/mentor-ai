import os
from backend.llm.ollama_provider import OllamaProvider
from backend.llm.openai_provider import OpenAIProvider
from backend.llm.anthropic_provider import AnthropicProvider
from backend.llm.openrouter_provider import OpenRouterProvider


from backend.services.profile_service import load_profile


class LLMFactory:
    @staticmethod
    def get_llm(user_config=None):
        """
        Returns an LLM instance based on the provided configuration.
        user_config should be a dictionary with keys: 'provider', 'model', 'api_key'.
        """
        if not user_config:
            profile = load_profile()
            config = profile.get("model_config", {})
            provider = config.get("provider")
            model = config.get("model")
            api_key = config.get("api_key")
        else:
            provider = user_config.get("provider")
            model = user_config.get("model")
            api_key = user_config.get("api_key")

        print(
            f"DEBUG: LLMFactory requested provider='{provider}' (type: {type(provider)}), model='{model}'"
        )
        if isinstance(provider, str):
            provider = provider.strip().lower()

        if provider == "ollama":
            return OllamaProvider(model=model or "llama3").get_llm()

        if provider == "openai":
            if not api_key:
                real_key = os.getenv("OPENAI_API_KEY")
                if not real_key or real_key == "ollama-dummy-key":
                    raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")
                api_key = real_key
            return OpenAIProvider(
                api_key=api_key, model=model or "gpt-4o-mini"
            ).get_llm()

        if provider == "anthropic":
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY is required for Anthropic provider."
                )
            return AnthropicProvider(
                api_key=api_key, model=model or "claude-3-haiku"
            ).get_llm()

        if provider == "openrouter":
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is required for OpenRouter.")
            return OpenRouterProvider(
                api_key=api_key, model=model or "google/gemini-2.0-flash-001"
            ).get_llm()

        raise ValueError(f"Unsupported provider: {provider}")
