import requests
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class FireworksClient:
    def __init__(self):
        self.api_key = settings.FIREWORKS_API_KEY
        self.base_url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.default_model = settings.LLM_MODEL

    def generate_response(
        self,
        user_message: str,
        memory_context: str = "",
        model: str = None,
        max_tokens: int = 1024,
    ):
        url = self.base_url

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []

        # Memory context
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
            "model": model if model else self.default_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Fireworks request failed: {str(e)}")
            raise Exception("LLM service unavailable")

        if response.status_code != 200:
            logger.error(response.text)
            raise Exception(f"Fireworks API Error: {response.text}")

        data = response.json()

        return (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
        )
