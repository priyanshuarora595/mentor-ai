import streamlit as st

from backend.services.profile_service import load_profile, save_profile

st.title("⚙️ Settings")

try:
    profile = load_profile()
except Exception as e:
    st.error(f"Error loading profile: {e}")
    profile = {"model_config": {"provider": "ollama", "model": "llama3", "api_key": ""}}

st.subheader("LLM Configuration")

provider = st.selectbox(
    "Model Provider",
    ["ollama", "openai", "anthropic", "openrouter"],
    index=["ollama", "openai", "anthropic", "openrouter"].index(
        profile["model_config"].get("provider", "ollama")
    ),
)

model = st.text_input("Model Name", profile["model_config"].get("model", "llama3"))

api_key = st.text_input(
    "API Key (if required)",
    value=profile["model_config"].get("api_key", ""),
    type="password",
)

if st.button("Save Settings"):
    profile["model_config"] = {"provider": provider, "model": model, "api_key": api_key}
    try:
        save_profile(profile)
        st.success("Settings saved successfully!")
    except Exception as e:
        st.error(f"Error saving profile: {e}")

st.divider()
st.write(f"**Current Active Model:** {model} ({provider})")
