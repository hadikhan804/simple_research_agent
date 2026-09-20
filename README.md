# Marketing Campaign Pipeline

A two-step Google ADK agent that researches a market and then writes campaign messaging from that research.

## What it does

The root agent (`campaign_pipeline`) runs two specialists in order:

1. **Market researcher** — uses Tavily search to collect current market size, target audience, competitors, and customer pain points.
2. **Messaging strategist** — turns that research into a positioning statement, value propositions, audience summary, and tone of voice.

The model used by both agents is `openai/gpt-4o-mini` through LiteLLM.

## Project layout

```
agent/
├── README.md
├── .gitignore
└── market_research_agent/
    ├── .venv/                      # local virtualenv (not committed)
    └── simple_research_agent/
        ├── __init__.py
        ├── agent.py                # agent definitions
        ├── .env                    # your API keys (not committed)
        └── .env.example            # key names only
```

## Prerequisites

- Python 3.12+
- An [OpenAI](https://platform.openai.com/) API key
- A [Tavily](https://tavily.com/) API key

## Setup

From the project folder:

```powershell
cd market_research_agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install google-adk litellm langchain-community tavily-python openai
```

Copy the example env file and add your own keys. Do not commit `.env`.

```powershell
copy simple_research_agent\.env.example simple_research_agent\.env
```

Then edit `simple_research_agent/.env`:

```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Run

With the virtualenv activated:

```powershell
adk web
```

or:

```powershell
adk run simple_research_agent
```

Give the researcher a product, brand, or market to analyze. The pipeline returns research first, then the messaging strategy.

## Confidential files (gitignored)

These stay on your machine and are listed in `.gitignore`:

| Path | Why |
| --- | --- |
| `.env` | OpenAI and Tavily API keys |
| `.venv/` | Local virtual environment |
| `.adk/` and `*.db` | Local ADK session data |
| `__pycache__/` | Python bytecode |
