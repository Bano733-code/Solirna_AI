from sqlalchemy.orm import Session
import logging
import uuid

from app.services.fireworks_service import FireworksClient
from app.agents.router import route_query
from app.agents.agent_router import select_agent

from app.agents.validation_agent import run_validation_agent
from app.agents.research_agent import run_research_agent
from app.agents.doc_agent import run_doc_agent

from app.services.embedding_service import create_embedding
from app.services.qdrant_service import search_memories, upload_memory

logger = logging.getLogger(__name__)

fireworks = FireworksClient()


def chat_with_ai(db: Session, user_id: int, user_message: str):

    # STEP 1: Select agent
    agent = select_agent(user_message)

    # STEP 2: Embed query
    query_embedding = create_embedding(user_message)

    # STEP 3: Retrieve memory from Qdrant
    memories = search_memories(user_id=user_id,query_embedding=query_embedding, limit=5)

    memory_context = "\n".join(
        [m.payload.get("text", "") for m in memories]
    )

    # STEP 4: ROUTE TO AGENT SYSTEM
    if agent == "validation_agent":
        ai_response = run_validation_agent(user_message, memory_context)

    elif agent == "research_agent":
        ai_response = run_research_agent(user_message, memory_context)

    elif agent == "doc_agent":
        ai_response = run_doc_agent(user_message, memory_context)

    else:
        # fallback LLM
        decision = route_query(user_message)

        ai_response = fireworks.generate_response(
            user_message=user_message,
            memory_context=memory_context,
            model=decision["model"],
            max_tokens=decision["max_tokens"],
        )

    # STEP 5: Store memory in Qdrant
    memory_text = f"User: {user_message}\nAssistant: {ai_response}"
    memory_embedding = create_embedding(memory_text)

    upload_memory(
        memory_id=str(uuid.uuid4()),
        embedding=memory_embedding,
        payload={
            "user_id": user_id,
            "text": memory_text
        }
    )

    return ai_response
