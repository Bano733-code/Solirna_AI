from sqlalchemy.orm import Session
import logging

from app.services.memory_service import (
    save_memory,
    get_recent_memories,
)

from app.services.fireworks_service import FireworksClient
from app.agents.router import route_query

logger = logging.getLogger(__name__)

fireworks = FireworksClient()


def chat_with_ai(
    db: Session,
    user_id: int,
    user_message: str,
):
    """
    Main AI chat workflow.
    """

    # Retrieve previous conversations
    memories = get_recent_memories(
        db=db,
        user_id=user_id,
        limit=5,
    )

    memory_context = ""

    for memory in memories:
        memory_context += (
            f"User: {memory.user_message}\n"
            f"Assistant: {memory.ai_response}\n\n"
        )

    # AI Agent decides which model to use
    decision = route_query(user_message)

    logger.info(
        f"Model Selected: {decision['model']} | "
        f"Reason: {decision['reason']}"
    )

    # Generate AI response
    ai_response = fireworks.generate_response(
        user_message=user_message,
        memory_context=memory_context,
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )

    # Save conversation
    save_memory(
        db=db,
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
    )

    return ai_response


def generate_prd(title: str, idea: str) -> str:
    """
    Generate a Product Requirements Document.
    """

    prompt = f"""
You are an expert Product Manager.

Generate a professional Product Requirements Document.

Product Title:
{title}

Product Idea:
{idea}

The PRD should include:

1. Executive Summary
2. Problem Statement
3. Goals
4. Target Users
5. Features
6. Functional Requirements
7. Non-functional Requirements
8. User Stories
9. Success Metrics
10. Future Improvements

Return the result in Markdown.
"""

    decision = route_query(prompt)

    logger.info(
        f"PRD Model: {decision['model']}"
    )

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )


def generate_pitchdeck(title: str, startup_idea: str) -> str:
    """
    Generate a startup pitch deck.
    """

    prompt = f"""
You are an expert startup consultant.

Create a professional investor pitch deck.

Startup Name:
{title}

Startup Idea:
{startup_idea}

Generate the following sections:

1. Problem
2. Solution
3. Market Opportunity
4. Product
5. Business Model
6. Competitive Advantage
7. Go-To-Market Strategy
8. Revenue Model
9. Financial Projections
10. Team
11. Funding Requirement
12. Closing Statement

Return the output in Markdown.
"""

    decision = route_query(prompt)

    logger.info(
        f"Pitch Deck Model: {decision['model']}"
    )

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )
