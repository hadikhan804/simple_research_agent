from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults

tavily_tool = LangchainTool(
    tool=TavilySearchResults(max_results=5)
)

market_sizing_agent = LlmAgent(
    name="market_sizing_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="You are a market sizing analyst. "
                "Use Tavily Search to gather current, real data on: "
                "total addressable market (TAM), market growth rate, "
                "and key market trends. Be concise but specific.",
    tools=[tavily_tool],
    output_key="market_sizing_result",   
)

competitor_research_agent = LlmAgent(
    name="competitor_research_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="You are a competitive intelligence analyst. "
                "Use Tavily Search to identify and analyze 2-3 key competitors. "
                "Cover their positioning, pricing, strengths, and weaknesses. "
                "Be concise but specific.",
    tools=[tavily_tool],
    output_key="competitor_research_result",  
)

audience_research_agent = LlmAgent(
    name="audience_research_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="You are a customer research specialist. "
                "Use Tavily Search to identify the target audience, "
                "their top 3 pain points, and unmet needs. "
                "Be concise but specific.",
    tools=[tavily_tool],
    output_key="audience_research_result",   
)

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[
        market_sizing_agent,
        competitor_research_agent,
        audience_research_agent,
    ],
    description="Runs market, competitor, and audience research concurrently.",
)

messaging_strategist = LlmAgent(
    name="messaging_strategist",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="You are a senior messaging strategist. "
                "Using the following research:\n\n"
                "MARKET SIZING:\n{market_sizing_result}\n\n"
                "COMPETITORS:\n{competitor_research_result}\n\n"
                "AUDIENCE:\n{audience_research_result}\n\n"
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
        parallel_research_agent,  
        messaging_strategist,     
    ],
)