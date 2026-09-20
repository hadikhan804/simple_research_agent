from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults
from google.adk.agents import SequentialAgent

tavily_tool = LangchainTool(
    tool=TavilySearchResults(max_results=5)
)

market_researcher = LlmAgent (
    name="market_researcher",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="you are a market researcher specialist"
                "Use Google Search to gather current, real data. "
                "Cover market size, target audience, 2-3 competitors, "
                "and customer pain points. Be concise but specific.",
    tools=[tavily_tool],
    output_key="research_result",
)

messaging_strategist = LlmAgent(
    name="messaging_strategist",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="You are a senior messaging strategist. "
                "Using this market research:\n\n"
                "{research_results}\n\n"
                "Produce:\n"
                "- Core positioning statement (1 sentence)\n"
                "- 3 key value propositions\n"
                "- Target audience summary\n"
                "- Tone of voice (2-3 adjectives)",
    output_key="messaging_strategy",
)

root_agent = SequentialAgent(
    name="campaign_pipeline",
    sub_agents=[
        market_researcher,
        messaging_strategist,
    ],
)