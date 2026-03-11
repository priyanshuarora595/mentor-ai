from crewai import Crew, Process
from backend.tasks.learning_tasks import create_learning_tasks
from backend.agents.agents import LearningAgents
from backend.llm.factory import LLMFactory


class MentorCrew:
    def __init__(self, topic, llm_config=None):
        self.topic = topic
        # Get LLM instance based on config
        self.llm = LLMFactory.get_llm(llm_config)
        self.learning_agents = LearningAgents(self.llm)

    def run(self, task_callback=None):
        # Create tasks and pass our agents instance
        tasks = create_learning_tasks(self.topic, self.learning_agents)

        # Pull the specific agent instances used in the tasks to ensure consistency
        crew = Crew(
            agents=[
                self.learning_agents.curriculum_planner(),
                self.learning_agents.concept_explainer(),
                self.learning_agents.youtube_search_agent(),
                self.learning_agents.content_aggregator(),
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            task_callback=task_callback,
        )

        return crew.kickoff()
