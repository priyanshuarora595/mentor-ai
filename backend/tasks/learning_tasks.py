from crewai import Task


def create_learning_tasks(topic, agents):
    # 1. Curriculum Roadmap
    curriculum_planner = agents.curriculum_planner()
    roadmap_task = Task(
        description=f"Create a detailed learning roadmap for '{topic}'. Include beginner, intermediate, and advanced sections.",
        expected_output="A structured markdown roadmap with learning milestones.",
        agent=curriculum_planner,
    )

    # 2. Concept Explanation
    concept_explainer = agents.concept_explainer()
    explanation_task = Task(
        description=f"Provide comprehensive explanations for the core concepts identified in the roadmap for '{topic}'.",
        expected_output="Detailed explanations with examples and analogies.",
        agent=concept_explainer,
        context=[roadmap_task],
    )

    # 3. YouTube Resources
    youtube_agent = agents.youtube_search_agent()
    youtube_task = Task(
        description=f"Find the best YouTube videos for learning '{topic}'. Provide links and brief descriptions for each. Start this section with a '## YouTube Resources' header.",
        expected_output="A markdown section starting with '## YouTube Resources' followed by a list of curated YouTube video links with descriptions.",
        agent=youtube_agent,
    )

    # 4. Final Compilation
    aggregator = agents.content_aggregator()
    compilation_task = Task(
        description=f"Compile the complete learning material for '{topic}'. Include the roadmap, the detailed explanations, and the curated YouTube videos. Ensure all sections are properly formatted in Markdown and flow logically. Crucially, you MUST include the full list of YouTube video links provided by the YouTube Search Agent. Do NOT summarize or omit them. Include the '## YouTube Resources' section exactly as generated.",
        expected_output="A single, comprehensive markdown document containing ALL sections, including the full '## YouTube Resources' (with all links).",
        agent=aggregator,
        context=[roadmap_task, explanation_task, youtube_task],
    )

    return [
        roadmap_task,
        explanation_task,
        youtube_task,
        compilation_task,
    ]
