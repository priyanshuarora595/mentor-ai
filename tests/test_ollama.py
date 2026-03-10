import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.llm.factory import LLMFactory


def test_ollama():
    print("Testing Ollama connectivity...")
    try:
        # Pass a dictionary for config
        llm = LLMFactory.get_llm({"provider": "ollama", "model": "llama3"})
        response = llm.invoke("Say 'Ollama is working!'")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_ollama()
