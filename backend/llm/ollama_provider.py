from crewai import LLM


class OllamaProvider:
    def __init__(self, model="llama3"):
        self.model = model

    def get_llm(self):
        # Use CrewAI's native LLM class with the ollama/ prefix
        # This is the most reliable way in CrewAI 1.10+
        return LLM(model=f"ollama/{self.model}", base_url="http://localhost:11434")
