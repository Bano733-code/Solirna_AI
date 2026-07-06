from sqlalchemy.orm import Session
import logging
import uuid

from app.services.fireworks_service import FireworksClient
from app.agents.router import route_query

from app.services.embedding_service import create_embedding
from app.services.qdrant_service import search_memories, upload_memory

logger = logging.getLogger(__name__)

fireworks = FireworksClient()


# -----------------------------
# MAIN CHAT FUNCTION (RAG + AGENT)
# -----------------------------
def chat_with_ai(
    db: Session,
    user_id: int,
    user_message: str,
):
    """
    Main AI chat workflow with:
    - Agent routing
    - Qdrant memory retrieval (RAG)
    - Fireworks generation
    - Memory storage
    """

    # STEP 1: Route query to best model
    decision = route_query(user_message)

    logger.info(
        f"Model Selected: {decision['model']} | Reason: {decision['reason']}"
    )

    # STEP 2: Create embedding for query
    query_embedding = create_embedding(user_message)

    # STEP 3: Retrieve relevant memories from Qdrant (REAL RAG)
    memories = search_memories(
        user_id=user_id,
        query_embedding=query_embedding,
        limit=5
    )

    memory_context = ""

    for m in memories:
        memory_context += f"{m.payload.get('text')}\n\n"

    # STEP 4: Generate AI response
    ai_response = fireworks.generate_response(
        user_message=user_message,
        memory_context=memory_context,
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )

    # STEP 5: Create memory text
    memory_text = f"User: {user_message}\nAssistant: {ai_response}"

    # STEP 6: Embed memory
    memory_embedding = create_embedding(memory_text)

    # STEP 7: Store in Qdrant (LONG-TERM MEMORY)
    upload_memory(
        memory_id=str(uuid.uuid4()),
        embedding=memory_embedding,
        payload={
            "user_id": user_id,
            "text": memory_text,
            "type": "chat"
        }
    )

    return ai_response


# -----------------------------
# PRD GENERATOR
# -----------------------------
def generate_prd(title: str, idea: str) -> str:

    prompt = f"""
You are an expert Product Manager.

Generate a professional Product Requirements Document.

Product Title:
{title}

Product Idea:
{idea}

Include:
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

Return in Markdown format.
"""

    decision = route_query(prompt)

    logger.info(f"PRD Model: {decision['model']}")

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )


# -----------------------------
# PITCH DECK GENERATOR
# -----------------------------
def generate_pitchdeck(title: str, startup_idea: str) -> str:

    prompt = f"""
You are an expert startup consultant.

Create a professional investor pitch deck.

Startup Name:
{title}

Startup Idea:
{startup_idea}

Include:
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

Return in Markdown format.
"""

    decision = route_query(prompt)

    logger.info(f"Pitch Deck Model: {decision['model']}")

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model=decision["model"],
        max_tokens=decision["max_tokens"],
    )
