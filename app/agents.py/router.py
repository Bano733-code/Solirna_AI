from app.agents.cost_optimizer import estimate_complexity


def route_query(message: str):
    """
    Choose the Fireworks model based on prompt complexity.
    """

    complexity = estimate_complexity(message)

    if complexity == "low":
        return {
            "model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
            "max_tokens": 512,
            "reason": "Simple request",
        }

    elif complexity == "medium":
        return {
            "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
            "max_tokens": 1024,
            "reason": "Balanced reasoning",
        }

    return {
        "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
        "max_tokens": 2048,
        "reason": "Complex reasoning",
    }
