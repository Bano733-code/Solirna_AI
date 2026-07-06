from app.services.fireworks_service import FireworksClient

fireworks = FireworksClient()


def run_validation_agent(user_message: str, memory_context: str):

    prompt = f"""
You are a Startup Idea Validation Expert.

Analyze the idea and provide:

1. SWOT Analysis
2. Market Risk Score (0-100)
3. Execution Risk
4. Demand Estimate
5. Honest Verdict: (Strong Idea / Weak Idea / Needs Pivot)

Startup Idea:
{user_message}

Context:
{memory_context}

Be brutally honest.
"""

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model="accounts/fireworks/models/llama-v3p1-70b-instruct",
        max_tokens=1200,
    )
