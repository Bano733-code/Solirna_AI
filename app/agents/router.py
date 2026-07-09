try:
    from app.agents.cost_optimizer import estimate_complexity
except Exception:
    def estimate_complexity(message: str):
        length = len(message)

        if length < 50:
            return "low"
        elif length < 200:
            return "medium"
        else:
            return "high"


def route_query(message: str):
    """
    Choose the Fireworks model based on prompt complexity.
    """

    complexity = estimate_complexity(message)

    if complexity == "low":
        return {
            "model": "accounts/fireworks/models/glm-5p2",
            "max_tokens": 512,
            "reason": "Simple request",
        }

    elif complexity == "medium":
        return {
            "model": "accounts/fireworks/models/glm-5p2",
            "max_tokens": 1024,
            "reason": "Balanced reasoning",
        }

    return {
        "model": "accounts/fireworks/models/glm-5p2",
        "max_tokens": 2048,
        "reason": "Complex reasoning",
    }
