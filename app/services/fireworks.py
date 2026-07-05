import requests
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class FireworksClient:
    def __init__(self):
        self.api_key = settings.FIREWORKS_API_KEY
        self.base_url = "https://api.fireworks.ai/inference/v1"
        self.default_model = settings.LLM_MODEL

    def generate_response(
        self,
        user_message: str,
        memory_context: str = "",
        model: str = None,
        max_tokens: int = 1024,
    ):
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []

        # Add memory as system context
        if memory_context:
            messages.append({
                "role": "system",
                "content": f"Conversation history:\n{memory_context}"
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": max_tokens,
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            logger.error(response.text)
            raise Exception(f"Fireworks API Error: {response.text}")

        return response.json()["choices"][0]["message"]["content"]
