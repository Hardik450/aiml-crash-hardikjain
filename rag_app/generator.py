
import os
from typing import List, Tuple, Optional, Dict, Any
from dotenv import load_dotenv
import requests

from chunker import Chunk

load_dotenv()

DEFAULT_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
DEFAULT_BASE_URL = os.environ.get("GROQ_API_BASE_URL", "https://api.groq.com/openai/v1")

SYSTEM_PROMPT = """You are the AuraHealth Nexus internal knowledge assistant.

Rules you MUST follow:
1. Answer the user's question using ONLY the information contained in the
   "CONTEXT" section below. Do not use any outside knowledge, and do not
   guess or make anything up.
2. If the answer is not contained in the context, respond exactly with:
   "I don't have enough information in the provided documents to answer that."
3. Be precise and specific -- include exact numbers, codes, names,
   dosages, or percentages from the context when the question asks for them.
4. Keep answers concise and directly responsive to the question asked.
5. You may use the conversation history to resolve follow-up questions
   (e.g. pronouns like "it" or "that"), but the factual content of your
   answer must still come only from the CONTEXT section provided with the
   latest question.
"""


def format_context(retrieved: List[Tuple[Chunk, float]]) -> str:
    blocks = []
    for chunk, score in retrieved:
        blocks.append(f"[Source: {chunk.source} | relevance={score:.3f}]\n{chunk.text}")
    return "\n\n---\n\n".join(blocks)


def build_user_message(query: str, context: str) -> str:
    return f"CONTEXT:\n{context}\n\nQUESTION: {query}"


CONTEXTUALIZE_SYSTEM_PROMPT = """Given a chat history and a follow-up user question, rewrite the
follow-up question as a standalone question that contains all the
context needed to understand it without the chat history (e.g. resolve
pronouns like "it" or "that" into the actual subject). Do NOT answer the
question. If the question is already standalone, return it unchanged.
Return ONLY the rewritten question, nothing else."""


def _ensure_api_key(api_key: Optional[str]) -> Optional[str]:
    return api_key or os.getenv("GROQ_API_KEY")


def _extract_text(response_json: Dict[str, Any]) -> str:
    if response_json is None:
        return ""

    if isinstance(response_json, dict):
        if "output_text" in response_json:
            return response_json["output_text"]

        choices = response_json.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0]
            if isinstance(first_choice, dict):
                message = first_choice.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content
                    if isinstance(content, list):
                        return "".join(
                            item.get("text", "")
                            if isinstance(item, dict)
                            else str(item)
                            for item in content
                        )

        output = response_json.get("output")
        if isinstance(output, list) and output:
            first = output[0]
            if isinstance(first, dict):
                if "text" in first:
                    return first["text"]
                if "content" in first:
                    content = first["content"]
                    if isinstance(content, str):
                        return content
                    if isinstance(content, list):
                        return "".join(
                            item.get("text", "")
                            if isinstance(item, dict)
                            else str(item)
                            for item in content
                        )
            return str(first)

    return str(response_json)


def _build_prompt_messages(system_prompt: str, messages: List[dict]) -> List[dict]:
    prompt = [{"role": "system", "content": system_prompt}]
    prompt.extend({"role": m["role"], "content": m["content"]} for m in messages)
    return prompt


class Generator:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        api_base_url: Optional[str] = None,
    ):
        self.model = model
        self.api_key = _ensure_api_key(api_key)
        self.api_base_url = api_base_url or DEFAULT_BASE_URL
        self.enabled = bool(self.api_key)

    def _get_chat_completion_url(self) -> str:
        base = self.api_base_url.rstrip("/")
        if base.endswith("/chat/completions"):
            return base
        if base.endswith("/responses"):
            return base.replace("/responses", "/chat/completions")
        return f"{base}/chat/completions"

    def _call_groq(self, messages: List[dict], max_tokens: int) -> str:
        payload = {
            "model": self.model,
            "messages": _build_prompt_messages(SYSTEM_PROMPT, messages),
            "temperature": 0.0,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            self._get_chat_completion_url(),
            json=payload,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        return _extract_text(response.json())

    def contextualize_query(self, query: str, history: Optional[List[dict]]) -> str:
        """Rewrite a follow-up query into a standalone one using chat history."""
        if not history:
            return query

        if not self.enabled:
            return query

        messages = list(history) + [{"role": "user", "content": query}]
        prompt_messages = _build_prompt_messages(CONTEXTUALIZE_SYSTEM_PROMPT, messages)
        payload = {
            "model": self.model,
            "messages": prompt_messages,
            "temperature": 0.0,
            "max_tokens": 200,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            self._get_chat_completion_url(),
            json=payload,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        text = _extract_text(response.json())
        return text.strip() or query

    def generate(
        self,
        query: str,
        retrieved: List[Tuple[Chunk, float]],
        history: Optional[List[dict]] = None,
        max_tokens: int = 500,
    ) -> str:
        """
        query: the current user question
        retrieved: list of (Chunk, score) from the vector store
        history: optional prior turns as [{"role": "user"/"assistant", "content": str}, ...]
        """
        if not self.enabled:
            return "Groq generation is unavailable because GROQ_API_KEY is not set."

        context = format_context(retrieved)
        user_msg = build_user_message(query, context)

        messages = list(history) if history else []
        messages.append({"role": "user", "content": user_msg})

        payload = {
            "model": self.model,
            "messages": _build_prompt_messages(SYSTEM_PROMPT, messages),
            "temperature": 0.0,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            self._get_chat_completion_url(),
            json=payload,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        return _extract_text(response.json())
