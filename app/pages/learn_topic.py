import threading

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

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
                # Some tasks now run concurrently (async_execution=True in
                # learning_tasks.py) on crewai-managed background threads, which
                # don't carry Streamlit's script context by default — calling
                # st.* from them raises. Capture this thread's context up front
                # and attach it to whichever thread invokes the callback below.
                # A lock serializes the actual UI writes, since two async tasks
                # can complete around the same moment and both invoke this.
                main_ctx = get_script_run_ctx()
                ui_lock = threading.Lock()

                def crew_task_callback(task):
                    # This callback is purely cosmetic status feedback — crewai
                    # calls it with no try/except of its own, so any exception
                    # here (thread-context issues included) would otherwise
                    # fail the real task even though the agent already
                    # succeeded. Nothing below may escape this function.
                    try:
                        add_script_run_ctx(threading.current_thread(), main_ctx)

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

                        with ui_lock:
                            status.update(label=f"⏳ {agent} completed, next starting ...")
                            st.write(f"📝 {agent} completed processing the task...")
                    except Exception:
                        pass

                # Pass the model config and callback
                crew = MentorCrew(topic, llm_config=llm_config)
                status.update(label="Curriculum Planner is generating...")

                result = crew.run(task_callback=crew_task_callback)
                status.update(label="✨ Learning plan generated!", state="complete")

                # Save to database — crew.run() already returns clean, assembled
                # markdown (sanitized per-section in MentorCrew), no further
                # post-processing needed here.
                from backend.services.learning_service import LearningService

                new_topic = LearningService.save_topic(
                    user_id=1, topic_name=topic, content=result
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
