from crewai import Task


def create_learning_tasks(topic, agents):
    # Roadmap and YouTube search don't depend on each other, so both run
    # async_execution=True back-to-back: crewai dispatches them concurrently
    # and only blocks (joining both) once it hits the next *sync* task below.
    curriculum_planner = agents.curriculum_planner()
    roadmap_task = Task(
        description=f"Create a detailed learning roadmap for '{topic}'. Include beginner, intermediate, and advanced sections.",
        expected_output="A structured markdown roadmap with learning milestones. Do not include a top-level title/header — just the content.",
        agent=curriculum_planner,
        async_execution=True,
    )

    youtube_agent = agents.youtube_search_agent()
    youtube_task = Task(
        description=f"Find the best YouTube videos for learning '{topic}'. Provide links and brief descriptions for each.",
        expected_output="A markdown list of curated YouTube video links with descriptions. Do not include a top-level title/header — just the list.",
        agent=youtube_agent,
        async_execution=True,
    )

    # Explanation depends on the roadmap, so it's the natural join point:
    # by the time it runs, both roadmap_task and youtube_task have completed.
    concept_explainer = agents.concept_explainer()
    explanation_task = Task(
        description=f"Provide comprehensive explanations for the core concepts identified in the roadmap for '{topic}'.",
        expected_output="Detailed explanations with examples and analogies. Do not include a top-level title/header — just the content.",
        agent=concept_explainer,
        context=[roadmap_task],
    )

    return [roadmap_task, youtube_task, explanation_task]
