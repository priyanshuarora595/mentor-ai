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

    def github_repo_agent(self):
        return self._get_agent(
            role="GitHub Repo Agent",
            goal="Analyze GitHub repositories to extract learning paths and explain how real-world projects are structured.",
            backstory="You are a senior software architect who can read any codebase and immediately understand its structure and key patterns.",
        )

    def progress_evaluator(self):
        return self._get_agent(
            role="Progress Evaluator",
            goal="Assess the learner's understanding and provide feedback on their progress.",
            backstory="You are a supportive but rigorous academic advisor. You help students identify their weak spots and suggest what they should focus on next.",
        )

    def content_aggregator(self):
        return self._get_agent(
            role="Learning Content Integrator",
            goal="Compile all parts of the learning material (roadmap, explanations, videos) into a single, cohesive, and beautiful markdown document.",
            backstory="You are a senior editor with an eye for flow and structure. Your job is to make sure the final learning platform feels unified and complete. CRITICAL: You MUST include EVERY section provided by the other agents (Roadmap, Explanations, and YouTube Videos). Never skip or summarize these sections. Merged them into one masterpiece. START your response directly with the content. do NOT repeat your role, system instructions, or any 'Final Answer' markers.",
        )
