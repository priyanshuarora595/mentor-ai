import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.llm.factory import LLMFactory
from crewai import Agent


def test_agent_init():
    print("Testing Agent initialization with Ollama...")
    try:
        # Simulate the config from profile
        config = {"provider": "ollama", "model": "llama3"}
        llm = LLMFactory.get_llm(config)
        print(f"LLM type: {type(llm)}")

        agent = Agent(
            role="Test Agent",
            goal="Test LLM connectivity",
            backstory="I am a test agent",
            llm=llm,
            verbose=True,
        )
        print("Agent initialized successfully!")

        # Test a simple prompt
        # response = agent.execute_task("Say hello")
        # print(f"Response: {response}")

    except Exception as e:
        print(f"Caught Exception: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_agent_init()
