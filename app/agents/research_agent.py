from app.services.fireworks_service import FireworksClient

fireworks = FireworksClient()


def run_research_agent(user_message: str, memory_context: str):

    prompt = f"""
You are a Market Research Analyst.

Generate:

1. Industry Overview
2. Top 5 Competitors
3. Market Trends
4. Opportunities
5. Risks
6. Summary Insight

Topic:
{user_message}

Context:
{memory_context}
"""

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model="accounts/fireworks/models/glm-5p2",
        max_tokens=1200,
    )
