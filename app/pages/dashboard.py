import streamlit as st

from backend.services.learning_service import LearningService

st.title("📊 Your Learning Dashboard")

# Mock user_id for now
user_id = 1

# Fetch dynamic stats
stats = LearningService.get_stats(user_id)

col1 = st.columns(1)[0]

with col1:
    st.metric("Topics Learned", stats["topics_learned"])


st.markdown("---")

st.subheader("📚 Recently Learned Topics")

topics = LearningService.get_user_topics(user_id)

if topics:
    for topic in reversed(topics):  # Show all stored topics
        with st.expander(
            f"📍 {topic.topic_name} (Generated on {topic.created_at.strftime('%Y-%m-%d')})"
        ):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(topic.content)
            with col2:
                confirm_key = f"confirm_del_{topic.id}"
                if st.session_state.get(confirm_key):
                    st.warning("Delete this topic?")
                    yes_col, no_col = st.columns(2)
                    with yes_col:
                        if st.button("Yes", key=f"yes_del_{topic.id}"):
                            if LearningService.delete_topic(topic.id):
                                st.session_state.pop(confirm_key, None)
                                st.success(f"Deleted {topic.topic_name}")
                                st.rerun()
                    with no_col:
                        if st.button("Cancel", key=f"no_del_{topic.id}"):
                            st.session_state.pop(confirm_key, None)
                            st.rerun()
                else:
                    if st.button("🗑️ Delete", key=f"del_{topic.id}"):
                        st.session_state[confirm_key] = True
                        st.rerun()

    st.markdown("---")
    if st.session_state.get("confirm_clear_all"):
        st.warning("This will permanently delete ALL learning history. Are you sure?")
        yes_col, no_col = st.columns(2)
        with yes_col:
            if st.button("Yes, clear everything"):
                if LearningService.clear_history(user_id):
                    st.session_state.pop("confirm_clear_all", None)
                    st.success("All history cleared!")
                    st.rerun()
        with no_col:
            if st.button("Cancel", key="cancel_clear_all"):
                st.session_state.pop("confirm_clear_all", None)
                st.rerun()
    else:
        if st.button("🚨 Clear All History"):
            st.session_state["confirm_clear_all"] = True
            st.rerun()
else:
    st.info(
        "You haven't learned any topics yet. Head over to **Learn Topic** to get started!"
    )

st.markdown("---")
st.subheader("💡 Recommended for You")
st.write(
    """
    • LangGraph & Multi-Agent Systems  
    • Distributed Database Design  
    • Advanced Kubernetes Orchestration  
    """
)
