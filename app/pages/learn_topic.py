import streamlit as st

from backend.crew import MentorCrew
from backend.services.profile_service import load_profile

st.title("📚 Learn New Topic")

# Load user profile for LLM config
try:
    profile = load_profile()
    llm_config = profile.get("model_config")

except Exception:
    llm_config = None

print("llm_config", llm_config)
topic = st.text_input(
    "What do you want to learn today?",
    placeholder="e.g., Python Decorators, Quantum Computing, etc.",
)

if st.button("Generate Learning Plan"):
    if topic:
        with st.status(f"Generating learning plan for '{topic}'...") as status:
            try:
                # Callback to update UI during agent execution
                def crew_step_callback(step):
                    # Try multiple ways to get agent role robustly
                    agent_role = "Agent"

                    # 1. Try from step object (CrewAI AgentAction/AgentFinish/TaskOutput)
                    if hasattr(step, "agent"):
                        if isinstance(step.agent, str):
                            agent_role = step.agent
                        elif hasattr(step.agent, "role"):
                            agent_role = step.agent.role
                    # 2. Try if step is a dict
                    elif isinstance(step, dict):
                        agent_role = (
                            step.get("agent_role") or step.get("agent_name") or "Agent"
                        )
                    # 3. Fallback: Parse from log if it looks like "[Role] is thinking..."
                    elif hasattr(step, "log") and "Working on" in str(step.log):
                        import re

                        match = re.search(r"Working on (.*?)'s", str(step.log))
                        if match:
                            agent_role = match.group(1)

                    # Update status with the dynamic role
                    status.update(label=f"⏳ {agent_role} is working...")
                    st.write(f"📝 {agent_role} is processing a step...")

                # Pass the model config and callback
                crew = MentorCrew(topic, llm_config=llm_config)
                result = crew.run(step_callback=crew_step_callback)

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

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic first.")
