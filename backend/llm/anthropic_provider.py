import os
from crewai import LLM


class AnthropicProvider:
    def __init__(self, api_key=None, model="claude-3-haiku"):
        self.api_key = api_key
        self.model = model

    def get_llm(self):
        if self.api_key:
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
        return LLM(model=f"anthropic/{self.model}", api_key=self.api_key)
