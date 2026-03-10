import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Learning Mentor", layout="wide")

st.title("🤖 AI Personal Learning Mentor")
st.markdown("""
Welcome to your personalized AI-powered learning platform! 

Use the sidebar to navigate through different features:
- **Dashboard**: Track your topics and scores.
- **Learn Topic**: Generate structured learning roadmaps, in-depth explanations, and curated YouTube videos.
- **Settings**: Configure your local Ollama model or cloud LLM providers.
""")

st.info(
    "💡 **Pro-tip:** Start by going to 'Learn Topic' and entering a subject you're curious about."
)

with st.expander("System Status"):
    st.write("Current Provider: Ollama")
    st.write("Model: llama3 (default)")
