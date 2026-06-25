# 🤖 LLM Fundamentals & APIs — Practical Assignment

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Free%20Tier-orange)
![Gemini](https://img.shields.io/badge/Gemini-Free%20Tier-4285F4?logo=google)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

**CodeTrade.io — Practical Assignment: LLM Fundamentals & APIs**
Real, working implementation using **Groq** (Llama 3.1 8B Instant) and **Google Gemini**
(2.5 Flash), called through their official SDKs. 
---

## Project Structure

```
.
├── llms.py                          ← SDK wrappers for Groq + Gemini (GroqClient, GeminiClient)
├── llm_clients.py                   ← High-level call_groq / call_gemini / streaming + cost helpers
├── BBCNews.csv                      ← BBC News dataset used by Task 2 (2,410 articles)
├── task1_multi_llm_comparison.py    ← Task 1
├── task2_prompt_playground.py       ← Task 2
├── task3_streaming_chat.py          ← Task 3
├── task4_token_cost_tracker.py      ← Task 4
├── requirements.txt
├── .env                             ← API keys (gitignored, not included in submission)
├── .gitignore
├── outputs/                         ← real API outputs
│   ├── task1_llm_comparison.csv / .json
│   ├── task2_prompt_playground.csv / .json
│   ├── task3_chat_transcript.json
│   └── task4_usage_report.json
├── logs/
│   └── usage_log.csv                ← Running cost/token log used by Task 4

```

---

## Setup

```bash
pip install -r requirements.txt
```

Then create a `.env` file (already present, gitignored) with:
```
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
```

- Free Groq key: https://console.groq.com/keys
- Free Gemini key: https://aistudio.google.com/app/apikey

---

## `llms.py` — SDK Wrappers

Two thin classes, each calling one documented SDK method — no guessing, no fallback chains:

- **`GroqClient`** — wraps `client.chat.completions.create(...)`. Supports both a single
  completion and `stream=True` for token-by-token output.
- **`GeminiClient`** — wraps `client.models.generate_content(...)` and
  `generate_content_stream(...)` via the official `google-genai` SDK. Configured with custom
  retry options (`HttpRetryOptions`: 8 attempts, exponential backoff up to 30s) to absorb
  transient API errors automatically.

Both return a plain dict: `{"text": ..., "usage": {"prompt_tokens", "completion_tokens", "total_tokens"}}`.

## `llm_clients.py` — High-Level Helpers

- `call_groq(prompt, system_prompt, history)` / `call_gemini(...)` — single-call wrappers
  returning a unified result dict (`provider`, `model`, `text`, `response_time_sec`,
  token counts, `error`).
- `call_groq_stream(...)` / `call_gemini_stream(...)` — generators yielding text chunks.
- Clients are **lazily constructed** — importing this module doesn't require both API keys
  to be set; each provider only raises if it's actually called without its key.
- `estimate_cost(provider, prompt_tokens, completion_tokens)` — uses the `PRICING_PER_1K_TOKENS`
  table (approximate public pay-as-you-go rates) to compute a per-call USD estimate.

---

## Task 1 — Multi-LLM Response Comparison

```bash
python task1_multi_llm_comparison.py
```

Sends 3 prompts to both Groq and Gemini, saves results to
`outputs/task1_llm_comparison.csv` / `.json`. Actual results from the current run:

| Prompt # | Provider | Model | Response Time (s) | Total Tokens |
|---|---|---|---|---|
| 1 | Groq | llama-3.1-8b-instant | 30.358 | 150 |
| 1 | Gemini | gemini-2.5-flash | 7.188 | 176 |
| 2 | Groq | llama-3.1-8b-instant | 0.843 | 187 |
| 2 | Gemini | gemini-2.5-flash | 3.286 | 439 |
| 3 | Groq | llama-3.1-8b-instant | 0.520 | 291 |
| 3 | Gemini | gemini-2.5-flash | 9.586 | 1,654 |

Note the first Groq call (30.4s) is a clear outlier — likely a cold-start / rate-limit retry
rather than typical latency; the other two Groq calls (0.5–0.8s) better represent its normal
speed advantage over Gemini on this workload.

---

## Task 2 — Prompt Engineering Playground (BBC News Dataset)

```bash
python task2_prompt_playground.py
```

**How the dataset is used:** loads `BBCNews.csv` (2,410 articles, columns `descr` and `tags`),
takes the first 10 articles, and runs **5 prompt variants × 10 articles = 50 Groq calls**,
each summarizing one article's `descr` field (truncated to 1,000 characters per call).

Prompt variants tested: naive/direct, role-based, structured/bullet-format, few-shot, and
chain-of-thought. Each output is scored on word count (ideal 15–60 words) + structure markers.

**Actual results from the current run** (avg score out of 17, across all 10 articles):

| Rank | Prompt Variant | Avg Score |
|---|---|---|
| 1 | `3_structured_format` | 16.7 |
| 2 | `4_few_shot` | 13.8 |
| 3 | `2_role_based` | 9.6 |
| 4 | `5_chain_of_thought` | 7.8 |
| 5 | `1_naive` | 7.4 |

**Structured-format wins clearly** — asking for 3 bullet points under 15 words each reliably
produces summaries in the ideal length range, while chain-of-thought responses tend to run
long (the reasoning steps inflate word count even though the final summary is good).

All 50 results saved to `outputs/task2_prompt_playground.csv` / `.json`.

---

## Task 3 — Streaming AI Chat Assistant

```bash
python task3_streaming_chat.py
```

Interactive CLI chatbot maintaining `system`/`user`/`assistant` history, streaming Groq
responses chunk-by-chunk. The current `outputs/task3_chat_transcript.json` contains a real
interactive session (not the demo script) — a short back-and-forth greeting exchange. Falls
back to a 3-message scripted demo automatically if run without an interactive terminal
(e.g. in CI).

---

## Task 4 — Token Usage and Cost Tracker

```bash
python task4_token_cost_tracker.py
```

`TokenCostTracker` logs every call's prompt, response, token counts, and estimated cost to
`logs/usage_log.csv`, then prints/saves a final report.

**Actual report from `outputs/task4_usage_report.json`:**

| Metric | Value |
|---|---|
| Total requests | 12 |
| Total prompt tokens | 378 |
| Total completion tokens | 3,494 |
| Total tokens | 6,554 |
| Total estimated cost | $0.000707 |
| Groq requests / tokens / cost | 6 / 1,969 / $0.000148 |
| Gemini requests / tokens / cost | 6 / 4,585 / $0.000559 |

> ⚠️ **3 of the 12 logged calls failed** (0 tokens, empty response) — all on Gemini. One

---

## Submission Checklist

- ✅ Task 1: Real Groq + Gemini comparison, CSV + JSON output, comparison table
- ✅ Task 2: 5 prompt variants tested against 10 real BBC articles (50 calls), best prompt identified
- ✅ Task 3: Streaming chatbot with real interactive session transcript saved
- ✅ Task 4: Token + cost tracker with real usage log and final report
- ✅ `.env` correctly excluded via `.gitignore`