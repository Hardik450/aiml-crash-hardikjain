
from __future__ import annotations

import time
from typing import Generator, List, Optional

from groq import Groq
from google import genai
from google.genai import types


class GroqClient:
    """Wraps the official `groq` SDK's chat completions endpoint."""

    def __init__(self, api_key: Optional[str], model: str):
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is required.")
        self.model = model
        self.client = Groq(api_key=api_key)

    def chat_completion(self, messages: List[dict], temperature: float = 0.7) -> dict:
        """
        Calls client.chat.completions.create(...) and returns a plain dict:
        {"text": str, "usage": {"prompt_tokens", "completion_tokens", "total_tokens"}}
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        text = response.choices[0].message.content
        usage = response.usage  # CompletionUsage object, not a dict
        return {
            "text": text,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            },
        }

    def stream_chat(self, messages: List[dict], temperature: float = 0.7) -> Generator[str, None, None]:
        """Yields text chunks as they arrive via stream=True."""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

custom_retry = types.HttpRetryOptions(
    attempts=8,         
    initial_delay=2.0,  
    max_delay=30.0,     
    exp_base=2,          
)
class GeminiClient:
    """Wraps the official `google-genai` SDK (NOT the deprecated google-generativeai)."""

    def __init__(self, api_key: Optional[str], model: str):
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is required.")
        self.model = model
        self.client = genai.Client(api_key=api_key, http_options={"retry_options": custom_retry})

    def generate(self, contents: list, system_instruction: str, temperature: float = 0.7) -> dict:
        """
        Calls client.models.generate_content(...) and returns a plain dict:
        {"text": str, "usage": {"prompt_tokens", "completion_tokens", "total_tokens"}}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
            ),
        )
        print(response.candidates[0].finish_reason)
        usage = response.usage_metadata  
        return {
            "text": response.text,
            "usage": {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count,
            },
        }

    def stream_generate(self, contents: list, system_instruction: str,
                         temperature: float = 0.7) -> Generator[str, None, None]:
        """Yields text chunks as they arrive via generate_content_stream(...)."""
        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
            ),
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
        