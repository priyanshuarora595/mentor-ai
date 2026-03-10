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
                if st.button("🗑️ Delete", key=f"del_{topic.id}"):
                    if LearningService.delete_topic(topic.id):
                        st.success(f"Deleted {topic.topic_name}")
                        st.rerun()

    st.markdown("---")
    if st.button("🚨 Clear All History"):
        if LearningService.clear_history(user_id):
            st.success("All history cleared!")
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
