import httpx
import os
import json
from .base import BaseLLM

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "mistralai/Mistral-7B-Instruct-v0.2"
)

SYSTEM_PROMPT = (
    "You are Aura, a professional AI assistant. "
    "Give clear, structured, and accurate answers."
)

class HuggingFaceLLM(BaseLLM):
    async def generate(self, prompt: str, user_id: str) -> str:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "inputs": f"<s>[INST] {SYSTEM_PROMPT}\nUser: {prompt} [/INST]",
            "parameters": {
                "max_new_tokens": 256,
                "temperature": 0.6,
                "top_p": 0.9,
            },
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(90.0)) as client:
            response = await client.post(MODEL_URL, headers=headers, json=payload)

        # ---- SAFETY CHECKS ----
        if response.status_code != 200:
            return "Aura is warming up. Please try again in a moment."

        if not response.content:
            return "Aura is waking up. Please retry."

        try:
            data = response.json()
        except json.JSONDecodeError:
            return "Aura received an unexpected response. Please retry."

        if isinstance(data, dict) and "error" in data:
            return f"Aura error: {data['error']}"

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].split("[/INST]")[-1].strip()

        return "Aura could not generate a response. Please try again."
