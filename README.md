# AI Personal Learning Mentor 🤖

Welcome to the **AI Personal Learning Mentor**, a sophisticated platform designed to help you master any topic through personalized learning roadmaps, deep-dive explanations, and curated YouTube resources.

## 🌟 Key Features

- **Multi-Agent Orchestration**: Powered by **CrewAI**, leveraging autonomous agents for curriculum planning, content deep-dives, and resource discovery.
- **Flexible LLM Support**: Choose your brain!
  - **Ollama**: Run completely local and private models like Llama3.
  - **Cloud Providers**: Native support for OpenAI, Anthropic, and OpenRouter.
- **Secure Configuration**: User profiles and API keys are stored in a local SQLite database with **Fernet (AES-128)** encryption.
- **Structured Learning**:
  - **Learning Roadmap**: Step-by-step milestones from beginner to advanced.
  - **Deep Explanations**: Analogies and ELI5-style technical breakdowns.
  - **YouTube Integration**: Curated video tutorials matched to your learning path.
- **Interactive Dashboard**: Track your learning history and manage your generated topics.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Agent Framework**: [CrewAI](https://www.crewai.com/)
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite)
- **Encryption**: [Cryptography.fernet](https://cryptography.io/)
- **Dependency Management**: Standard Python `pyproject.toml`

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher.
- [Ollama](https://ollama.ai/) (Optional, if you want to run local models).

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/priyanshuarora595/mentor-ai.git
   cd mentor-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

### 3. Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Set your `ENCRYPTION_KEY` in the `.env` file. This can be any random string (e.g., `mentor-super-secret-key-123`).

### 4. Running the Application

Start the Streamlit app:
```bash
streamlit run app/streamlit_app.py
```

## ⚙️ Usage Tips

1. **Dashboard**: View your learning stats and recently generated roadmaps.
2. **Learn Topic**: Enter a topic (e.g., "React Hooks", "Quantum Entanglement") and watch the agents collaborate to build your plan.
3. **Settings**:
   - Use the dropdown to switch between **Ollama**, **OpenAI**, **Anthropic**, or **OpenRouter**.
   - If using Ollama, ensure it's running locally (`ollama serve`).
   - If using cloud providers, enter your API key (it will be encrypted before being saved to the database).

## 🗄️ Project Structure

```text
mentor-ai/
├── app/                  # Streamlit UI
│   ├── pages/            # Dashboard, Learn Topic, Settings
│   └── streamlit_app.py  # Entry point
├── backend/              # Core Logic
│   ├── agents/           # CrewAI Agent definitions
│   ├── llm/              # Provider implementations (Ollama, OpenAI, etc.)
│   ├── services/         # Database and Profile services
│   ├── tasks/            # CrewAI Task definitions
│   └── tools/            # Custom tools (YouTube search)
├── config/               # Application configuration
├── database/             # SQLite connection and SQLAlchemy models
├── tests/                # Integration and verification tests
└── pyproject.toml        # Dependency definitions
```

## 🔒 Security

All API keys are encrypted at rest using a key derived from your `ENCRYPTION_KEY`. The raw keys are never stored in plain text in the database.

---
Built with ❤️ for lifelong learners.
