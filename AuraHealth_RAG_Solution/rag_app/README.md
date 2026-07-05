# AuraHealth Nexus RAG Capstone

A from-scratch Retrieval-Augmented Generation (RAG) system built over 10
fictional internal documents for "AuraHealth Nexus." It answers highly
specific questions (codes, dosages, percentages, room numbers, etc.) using
only the provided source documents — no outside knowledge, no hallucination.

## What's in this folder

```
rag_app/
├── data/                        10 source .txt documents (the knowledge base)
├── vector_index/                pre-built vector index (cached, ready to query)
│   ├── index.faiss              FAISS index of 196 chunk embeddings
│   └── chunks.pkl               the 196 chunks + metadata behind the index
├── loader.py                    Step 1: Document loading
├── chunker.py                   Step 2: Chunking
├── vectorstore.py                Step 3 & 4: Embedding + vector database
├── generator.py                 Step 5: LLM answer generation (Groq / Llama)
├── rag_pipeline.py              Orchestrates load → chunk → embed → retrieve → generate
├── evaluate.py                  Batch-runs the 30 capstone evaluation questions
├── evaluation_results.json      Saved output of the last evaluate.py run (30/30 answered)
├── requirements.txt             Python dependencies
├── .env                         API keys (GROQ_API_KEY) — not committed to git
└── __pycache__/                 compiled bytecode (safe to delete, auto-regenerated)
```

## Architecture

```
data/*.txt
    │  loader.py
    ▼
Document objects
    │  chunker.py
    ▼
196 text chunks (paragraph-aware, ~900 chars, 150-char overlap)
    │  vectorstore.py  (SentenceTransformer: all-MiniLM-L6-v2)
    ▼
384-dim embeddings  →  FAISS IndexFlatIP  (vector_index/)
    │
    │  user query
    ▼
vectorstore.search()  → top-k most similar chunks
    │
    ▼
generator.py  → Groq API (Llama 3.1 8B Instant)  → grounded answer
```

| Pipeline stage | File | Approach |
|---|---|---|
| **1. Document Loading** | `loader.py` | Reads every `.txt` in `data/`, normalizes `\r\n` line endings |
| **2. Chunking** | `chunker.py` | Paragraph-aware greedy packing (~900 chars/chunk, 150-char overlap); any single paragraph longer than the chunk size is hard-split with the same overlap so no content is lost |
| **3. Embedding** | `vectorstore.py` | `sentence-transformers` model **`all-MiniLM-L6-v2`** — a compact, free, local neural embedding model (384 dimensions) |
| **4. Vector Database** | `vectorstore.py` | **FAISS** `IndexFlatIP` — exact inner-product search over L2-normalized vectors (equivalent to cosine similarity) |
| **5. Retrieval** | `vectorstore.py` → `VectorStore.search()` | Returns the top-`k` chunks (default `k=5`) ranked by similarity to the query |
| **6. Generation** | `generator.py` | Calls the **Groq** OpenAI-compatible chat completions API running **`llama-3.1-8b-instant`**, with a system prompt that strictly forbids answering from anything but the retrieved context |
| **Bonus: Conversational memory** | `rag_pipeline.py` + `generator.py` | Follow-up questions (e.g. "And what is the treatment for it?") are first rewritten into standalone questions using chat history (`contextualize_query`) *before* retrieval, then answered with full chat history passed to the LLM |

## Setup

```bash
pip install -r requirements.txt
```

Create/confirm a `.env` file in `rag_app/` with:

```
GROQ_API_KEY=your-groq-key-here
```


## Usage

**Interactive chat** (loads the cached index in `vector_index/` if present, otherwise builds it from `data/`):

```bash
python3 rag_pipeline.py
```

**Run the full 30-question evaluation** (regenerates `evaluation_results.json`):

```bash
python3 evaluate.py
```

Note: `evaluate.py` sleeps 10 seconds between questions to stay under Groq's free-tier rate limits — a full run takes several minutes.

**Force a full re-index** (e.g. after changing chunk size or the data folder):

```python
from rag_pipeline import RAGPipeline
p = RAGPipeline()
p.index(force_rebuild=True)
```

## Evaluation Results

`evaluation_results.json` contains the output of the last full run: all
**30/30** capstone questions were answered with content grounded in the
correct source document (no "I don't have enough information" responses),
confirming the chunking/embedding/retrieval settings are precise enough
to find highly specific facts (exact codes, dosages, percentages, room
numbers) buried in long, repetitive documents. Each entry includes:

```json
{
  "question_number": 1,
  "question": "...",
  "top_sources": ["AuraHealth_Employee_Handbook_2026.txt", "..."],
  "answer": "..."
}
```

## Notes / things to double check

- **`.env` contains live API keys** — make sure this file is in `.gitignore` before pushing this folder anywhere public.
- **`vector_index/`** is a cache. If you add/edit/remove a file in `data/`, delete `vector_index/` (or call `index(force_rebuild=True)`) so the index gets rebuilt — otherwise stale embeddings will be served.
- **`__pycache__/`** can be safely deleted; it's regenerated automatically and doesn't need to be shared or version-controlled.
- If `GROQ_API_KEY` is missing or invalid, `generator.py` returns the literal string `"Groq generation is unavailable because GROQ_API_KEY is not set."` instead of raising — check for that string if answers look wrong.
