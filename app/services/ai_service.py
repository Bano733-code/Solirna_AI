from sqlalchemy.orm import Session

from app.services.memory_service import (
    save_memory,
    get_recent_memories,
)

from app.services.groq_service import generate_response


def chat_with_ai(
    db: Session,
    user_id: int,
    user_message: str,
):
    """
    Main AI chat workflow.
    """

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

    ai_response = generate_response(
        user_message=user_message,
        memory_context=memory_context,
    )

    save_memory(
        db=db,
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
    )

    return ai_response


def generate_prd(title: str, idea: str) -> str:
    """
    Generate a Product Requirements Document (PRD).
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

    return generate_response(
        user_message=prompt,
        memory_context=""
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

    return generate_response(
        user_message=prompt,
        memory_context=""
    )