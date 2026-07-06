def select_agent(message: str):
    message = message.lower()

    # Idea validation trigger
    if any(word in message for word in ["validate", "idea", "is this good", "swot", "should i build"]):
        return "validation_agent"

    # Market research trigger
    if any(word in message for word in ["market", "competitor", "industry", "trend", "research"]):
        return "research_agent"

    # Docs trigger
    if any(word in message for word in ["prd", "pitch", "document", "business plan"]):
        return "doc_agent"

    return "general_agent"
