from crewai import LLM


class OpenAIProvider:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def get_llm(self):
        return LLM(model=f"openai/{self.model}", api_key=self.api_key)
