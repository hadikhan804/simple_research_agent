from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools import exit_loop
from google.adk.models.lite_llm import LiteLlm

initial_strategist = LlmAgent(
    name="InitialStrategist",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""You are a senior messaging strategist. Produce a first-draft messaging strategy for the user's requested product.

    Output ONLY the strategy in this format:
    - Core positioning statement (1 sentence)
    - 3 key value propositions
    - Target audience summary
    - Tone of voice (2-3 adjectives)
    """,
    output_key="messaging_strategy",
)

critic_agent = LlmAgent(
    name="MessagingCritic",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""You are a senior brand strategist reviewing a messaging strategy.

    Strategy to review:
    {messaging_strategy}

    Evaluate it against these questions:
    - Is the positioning statement truly differentiated?
    - Are the value propositions specific and compelling?
    - Is the tone of voice consistent and appropriate for the audience?

    If the strategy is strong and needs no significant changes, call the `exit_loop` tool.
    If significant improvements are needed, provide specific, actionable feedback as your text output.
    """,
    tools=[exit_loop],
    output_key="critique_feedback",
)

refiner_agent = LlmAgent(
    name="MessagingRefiner",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""You are a senior copywriter. Refine the messaging strategy based on the critique.

    Original Strategy:
    {messaging_strategy}

    Critique:
    {critique_feedback}

    Produce a revised messaging strategy that addresses every point in the critique.
    Output ONLY the revised strategy in the same format as the original.
    """,
    output_key="messaging_strategy",
)

messaging_refinement_loop = LoopAgent(
    name="MessagingRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3,
)

root_agent = SequentialAgent(
    name="campaign_pipeline",
    sub_agents=[
        initial_strategist,
        messaging_refinement_loop,
    ],
)