import json
import httpx
from .config import settings


class OpenRouterClient:
    def __init__(self) -> None:
        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")

    async def complete_json(self, *, model: str, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Kontrakevich/GPT",
            "X-Title": "Architectural Critic Maximalist",
        }
        payload = {
            "model": model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        async with httpx.AsyncClient(timeout=240) as client:
            response = await client.post(f"{settings.openrouter_base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        content = data["choices"][0]["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Model returned invalid JSON") from exc
