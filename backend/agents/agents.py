from crewai import Agent
from backend.tools.youtube_search import YoutubeSearchTool


class LearningAgents:
    def __init__(self, llm):
        self.llm = llm
        self._agents = {}

    def _get_agent(self, role, goal, backstory, tools=None):
        if role not in self._agents:
            print(f"DEBUG: Creating new Agent for role: {role}")
            # Add formatting hint for local models - ONLY if tools exist
            if tools:
                backstory_with_hint = (
                    backstory
                    + " CRITICAL: You MUST use the following format for tool usage: Thought: [your reasoning] then Action: [tool name] then Action Input: [tool input]. Do not skip any steps."
                )
            else:
                backstory_with_hint = (
                    backstory
                    + " IMPORTANT: You have NO TOOLS available. Do NOT attempt to use any 'Action' or 'Action Input'. Simply provide your final response directly and clearly."
                )

            self._agents[role] = Agent(
                role=role,
                goal=goal,
                backstory=backstory_with_hint,
                llm=self.llm,
                verbose=True,
                allow_delegation=False,
                tools=tools or [],
                handle_parsing_errors=True,
                max_iter=5,
            )
        return self._agents[role]

    def curriculum_planner(self):
        return self._get_agent(
            role="Curriculum Planner",
            goal="Create highly structured, progressive learning roadmaps for any given topic.",
            backstory="You are a world-class technical educator with 20 years of experience in instructional design. You know exactly how to break down complex subjects into digestible, logical steps.",
        )

    def concept_explainer(self):
        return self._get_agent(
            role="Concept Explainer",
            goal="Provide clear, concise explanations of technical concepts at beginner, intermediate, and advanced levels.",
            backstory="You are famous for your 'Explain Like I'm Five' (ELI5) skills, but you can also dive deep into technical architecture for advanced learners. You use analogies and real-world examples to make things stick.",
        )

    def youtube_search_agent(self):
        return self._get_agent(
            role="YouTube Search Agent",
            goal="Find the most relevant and high-quality YouTube tutorials and courses for the topic.",
            backstory="You are a digital librarian who knows the best educational channels on YouTube. You look for videos with high engagement and clear teaching styles.",
            tools=[YoutubeSearchTool()],
        )

    def progress_evaluator(self):
        return self._get_agent(
            role="Progress Evaluator",
            goal="Assess the learner's understanding and provide feedback on their progress.",
            backstory="You are a supportive but rigorous academic advisor. You help students identify their weak spots and suggest what they should focus on next.",
        )

