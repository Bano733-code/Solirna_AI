def estimate_complexity(message: str) -> str:
    """
    Estimate prompt complexity.
    """

    words = len(message.split())

    if words < 30:
        return "low"

    elif words < 120:
        return "medium"

    return "high"
