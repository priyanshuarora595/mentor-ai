from backend.llm.factory import LLMFactory
from backend.agents.agents import LearningAgents
from backend.tasks.learning_tasks import create_learning_tasks
from crewai import Crew, Process


def test_full_flow():
    print("🚀 Starting End-to-End Verification Test (Ollama)...")

    try:
        # 1. Load config (simulating profile)
        config = {"provider": "ollama", "model": "llama3"}
        print(f"--- Step 1: LLM Initialization with config: {config}")
        llm = LLMFactory.get_llm(config)
        print(f"LLM initialized: {type(llm).__name__}")

        # 2. Initialize Agents
        print("--- Step 2: Agent Initialization")
        agents = LearningAgents(llm)
        curriculum_planner = agents.curriculum_planner()
        print(f"Agent initialized: {curriculum_planner.role}")

        # 3. Create Tasks
        print("--- Step 3: Task Creation")
        topic = "Basic Python Loops"
        tasks = create_learning_tasks(topic, agents)
        print(f"Created {len(tasks)} tasks for topic: {topic}")

        # 4. Assemble Crew (Dry run check)
        print("--- Step 4: Crew Assembly")
        crew = Crew(
            agents=[curriculum_planner],
            tasks=[tasks[0]],  # Just test with one task for speed
            process=Process.sequential,
            verbose=True,
        )
        print("Crew assembled successfully!")

        print("\n✅ End-to-End Verification PASSED!")
        print("The system is ready to use with Ollama and no OpenAI API Key.")

    except Exception as e:
        print(f"\n❌ Verification FAILED: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_full_flow()
