import threading

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

from backend.crew import MentorCrew
from backend.services.learning_service import LearningService
from backend.services.profile_service import load_profile
from backend.llm.ollama_provider import ModelNotFoundError

USER_ID = 1

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


def _run_generation(topic_name):
    with st.status(f"Generating learning plan for '{topic_name}'...") as status:
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

                    agent = "Agent"
                    if hasattr(task, "agent"):
                        if isinstance(task.agent, str):
                            agent = task.agent
                        elif hasattr(task.agent, "role"):
                            agent = task.agent.role
                    elif isinstance(task, dict):
                        agent = task.get("agent") or "Agent"

                    with ui_lock:
                        status.update(label=f"⏳ {agent} completed, next starting ...")
                        st.write(f"📝 {agent} completed processing the task...")
                except Exception:
                    pass

            crew = MentorCrew(topic_name, llm_config=llm_config)
            status.update(label="Curriculum Planner is generating...")

            result = crew.run(task_callback=crew_task_callback)
            status.update(label="✨ Learning plan generated!", state="complete")

            # crew.run() already returns clean, assembled markdown (sanitized
            # per-section in MentorCrew), no further post-processing needed.
            LearningService.save_topic(
                user_id=USER_ID, topic_name=topic_name, content=result
            )

            st.success("Learning plan generated!")
            st.markdown("---")
            st.markdown(result)

            st.session_state["last_learning_plan"] = result
            st.session_state["current_topic"] = topic_name

        except ModelNotFoundError as e:
            st.error(f"🤖 Ollama Error: {str(e)}")
            st.info(
                "💡 Tip: Make sure Ollama is running on your Mac and you have run 'ollama pull llama3'."
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if st.button("Generate Learning Plan"):
    if topic:
        existing = LearningService.find_by_topic_name(USER_ID, topic)
        if existing:
            st.session_state["cached_match_id"] = existing.id
        else:
            st.session_state["cached_match_id"] = None
            st.session_state["pending_regenerate_topic"] = topic
    else:
        st.warning("Please enter a topic first.")

# Show a previously-generated match instead of silently re-running the whole
# pipeline (3 LLM calls + a YouTube search) for a topic already answered.
cached_id = st.session_state.get("cached_match_id")
if cached_id:
    existing = LearningService.get_topic_by_id(cached_id)
    if existing:
        st.info(
            f"📎 You already generated a plan for **{existing.topic_name}** on "
            f"{existing.created_at.strftime('%Y-%m-%d')}. Showing the saved version."
        )
        st.markdown("---")
        st.markdown(existing.content)
        if st.button("🔄 Regenerate anyway"):
            st.session_state["cached_match_id"] = None
            st.session_state["pending_regenerate_topic"] = existing.topic_name
            st.rerun()

pending_topic = st.session_state.pop("pending_regenerate_topic", None)
if pending_topic:
    _run_generation(pending_topic)
