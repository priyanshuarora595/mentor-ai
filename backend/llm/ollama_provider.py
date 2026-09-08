import os
import requests
from crewai import LLM

from backend.llm import OLLAMA_TIMEOUT_SECONDS


class ModelNotFoundError(Exception):
    """Exception raised when an Ollama model is not found on the host."""

    pass


class OllamaProvider:
    def __init__(self, model="llama3"):
        self.model = model

    def validate_model(self):
        """Checks if the requested model exists in the Ollama instance."""
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            # Use the /api/tags endpoint to listed available models
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                available_models = [m["name"].split(":")[0] for m in models_data]
                available_models_full = [m["name"] for m in models_data]

                if (
                    self.model not in available_models
                    and self.model not in available_models_full
                ):
                    raise ModelNotFoundError(
                        f"Model '{self.model}' not found in Ollama at {base_url}. Please run 'ollama pull {self.model}' on your host."
                    )
            else:
                # If the API is up but returns an error, we can't definitively say the model is missing
                # but we should probably warn the user.
                pass
        except requests.exceptions.RequestException:
            # If Ollama is not running at all
            raise ModelNotFoundError(
                f"Could not connect to Ollama at {base_url}. Is Ollama running on your host?"
            )

    def get_llm(self):
        # Validate before returning the LLM
        self.validate_model()

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return LLM(
            model=f"ollama/{self.model}",
            base_url=base_url,
            timeout=OLLAMA_TIMEOUT_SECONDS,
        )
