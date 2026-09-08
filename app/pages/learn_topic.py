import streamlit as st

from backend.crew import MentorCrew
from backend.services.profile_service import load_profile
from backend.llm.ollama_provider import ModelNotFoundError

st.title("📚 Learn New Topic")

# Load user profile for LLM config
try:
    profile = load_profile()
    llm_config = profile.get("model_config")

except Exception:
    llm_config = None

topic = st.text_input(
    "What do you want to learn today?",
    placeholder="e.g., Python Decorators, Quantum Computing, etc.",
)

if st.button("Generate Learning Plan"):
    if topic:
        with st.status(f"Generating learning plan for '{topic}'...") as status:
            try:
                # Callback to update UI during agent execution
                def crew_task_callback(task):
                    # Try multiple ways to get agent role robustly
                    agent = "Agent"

                    # 1. Try from task object (CrewAI AgentAction/AgentFinish/TaskOutput)
                    if hasattr(task, "agent"):
                        if isinstance(task.agent, str):
                            agent = task.agent
                        elif hasattr(task.agent, "role"):
                            agent = task.agent.role
                    # 2. Try if task is a dict
                    elif isinstance(task, dict):
                        agent = task.get("agent") or "Agent"

                    # Update status with the dynamic role
                    status.update(label=f"⏳ {agent} completed, next starting ...")
                    st.write(f"📝 {agent} completed processing the task...")

                # Pass the model config and callback
                crew = MentorCrew(topic, llm_config=llm_config)
                status.update(label="Curriculum Planner is generating...")

                result = crew.run(task_callback=crew_task_callback)
                status.update(label="✨ Learning plan generated!", state="complete")

                # Save to database
                from backend.services.learning_service import LearningService

                # Ensure result is handled as string and sanitize
                def sanitize_output(text):
                    import re

                    # Remove common system preambles and "Final Answer" markers
                    patterns = [
                        r"(?i)^System:.*?\n",
                        r"(?i)^You are.*?\n",
                        r"(?i)^Final Answer:.*?\n",
                        r"(?i)^---.*?\n",
                        r"(?i)```\n",
                    ]
                    clean_text = str(text)
                    for pattern in patterns:
                        clean_text = re.sub(pattern, "", clean_text, count=1).strip()
                    return clean_text

                content_str = sanitize_output(result)
                new_topic = LearningService.save_topic(
                    user_id=1, topic_name=topic, content=content_str
                )

                st.success("Learning plan generated!")
                st.markdown("---")
                st.markdown(str(result))

                # Optionally save to session state for persistence
                st.session_state["last_learning_plan"] = result
                st.session_state["current_topic"] = topic

            except ModelNotFoundError as e:
                st.error(f"🤖 Ollama Error: {str(e)}")
                st.info(
                    "💡 Tip: Make sure Ollama is running on your Mac and you have run 'ollama pull llama3'."
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic first.")
