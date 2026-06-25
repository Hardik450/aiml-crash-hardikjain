import os
import time
from llms import GroqClient, GeminiClient
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
GEMINI_MODEL = "gemini-2.5-flash"

_groq_client: GroqClient | None = None
_gemini_client: GeminiClient | None = None


def _get_groq_client() -> GroqClient:
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient(GROQ_API_KEY, GROQ_MODEL)
    return _groq_client


def _get_gemini_client() -> GeminiClient:
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient(GEMINI_API_KEY, GEMINI_MODEL)
    return _gemini_client


def estimate_tokens(text: str) -> int:
    """
    This function estimates tokens.
    """
    return max(1, len(text) // 4)


def _history_to_groq_messages(history: list | None) -> list[dict]:
    """history is already in {"role": "user"/"assistant", "content": ...} form."""
    return list(history) if history else []


def _history_to_gemini_contents(prompt: str, history: list | None) -> list[types.Content]:
    """
    Converts our {"role": "user"/"assistant", "content": ...} history format
    into the list[types.Content] shape the google-genai SDK expects.
    Gemini uses role "model" instead of "assistant".
    """
    contents: list[types.Content] = []
    if history:
        for h in history:
            role = "model" if h["role"] == "assistant" else "user"
            contents.append(types.Content(role=role, parts=[types.Part(text=h["content"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    return contents


def call_groq(prompt: str, system_prompt: str = "You are a helpful assistant.",
               history: list | None = None) -> dict:
    """
    Call the Groq API via the official `groq` SDK.
    Returns a dict with: text, response_time_sec, prompt_tokens, completion_tokens,
    total_tokens, provider, model, error (if any).
    """
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(_history_to_groq_messages(history))
    messages.append({"role": "user", "content": prompt})

    start = time.time()
    try:
        result = _get_groq_client().chat_completion(messages, temperature=0.7)
        elapsed = round(time.time() - start, 3)
        text = result["text"]
        usage = result["usage"]
        return {
            "provider": "Groq",
            "model": GROQ_MODEL,
            "text": text,
            "response_time_sec": elapsed,
            "prompt_tokens": usage["prompt_tokens"],
            "completion_tokens": usage["completion_tokens"],
            "total_tokens": usage["total_tokens"],
            "error": None,
        }
    except Exception as e:
        elapsed = round(time.time() - start, 3)
        return {
            "provider": "Groq", "model": GROQ_MODEL, "text": "",
            "response_time_sec": elapsed, "prompt_tokens": 0,
            "completion_tokens": 0, "total_tokens": 0, "error": str(e),
        }


def call_gemini(prompt: str, system_prompt: str = "You are a helpful assistant.",
                 history: list | None = None) -> dict:
    """
    Call the Gemini API via the official `google-genai` SDK.
    Returns the same dict shape as call_groq() for easy comparison.
    """
    contents = _history_to_gemini_contents(prompt, history)

    start = time.time()
    try:
        result = _get_gemini_client().generate(contents, system_prompt, temperature=0.7)
        elapsed = round(time.time() - start, 3)
        text = result["text"]
        usage = result["usage"]
        return {
            "provider": "Gemini",
            "model": GEMINI_MODEL,
            "text": text,
            "response_time_sec": elapsed,
            "prompt_tokens": usage["prompt_tokens"],
            "completion_tokens": usage["completion_tokens"],
            "total_tokens": usage["total_tokens"],
            "error": None,
        }
    except Exception as e:
        elapsed = round(time.time() - start, 3)
        return {
            "provider": "Gemini", "model": GEMINI_MODEL, "text": "",
            "response_time_sec": elapsed, "prompt_tokens": 0,
            "completion_tokens": 0, "total_tokens": 0, "error": str(e),
        }


def call_groq_stream(prompt: str, system_prompt: str = "You are a helpful assistant.",
                      history: list | None = None):
    """Generator that streams Groq response chunks as they arrive."""
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(_history_to_groq_messages(history))
    messages.append({"role": "user", "content": prompt})

    for chunk in _get_groq_client().stream_chat(messages, temperature=0.7):
        yield chunk


def call_gemini_stream(prompt: str, system_prompt: str = "You are a helpful assistant.",
                        history: list | None = None):
    """Generator that streams Gemini response chunks as they arrive."""
    contents = _history_to_gemini_contents(prompt, history)
    for chunk in _get_gemini_client().stream_generate(contents, system_prompt, temperature=0.7):
        yield chunk


PRICING_PER_1K_TOKENS = {
    "Groq": {"input": 0.00005, "output": 0.00008},     # Llama-3.1-8B-instant approx rate
    "Gemini": {"input": 0.000075, "output": 0.0003},   # gemini-2.5-flash approx rate
}


def estimate_cost(provider: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate USD cost for a single request based on the pricing table above."""
    rates = PRICING_PER_1K_TOKENS.get(provider, {"input": 0, "output": 0})
    cost = (prompt_tokens / 1000) * rates["input"] + (completion_tokens / 1000) * rates["output"]
    return round(cost, 6)
