from dataclasses import dataclass
from typing import List
from loader import Document


@dataclass
class Chunk:
    id: str
    source: str
    text: str


def _split_long_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """Fallback hard-split for a single paragraph longer than chunk_size."""
    pieces = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        pieces.append(text[start:end])
        if end == n:
            break
        start = end - chunk_overlap
    return pieces


def chunk_document(doc: Document, chunk_size: int = 900, chunk_overlap: int = 150) -> List[Chunk]:
    paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]

    raw_chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(para) > chunk_size:
            if current:
                raw_chunks.append(current)
                current = ""
            raw_chunks.extend(_split_long_text(para, chunk_size, chunk_overlap))
            continue

        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            raw_chunks.append(current)
            overlap_text = current[-chunk_overlap:] if chunk_overlap else ""
            current = f"{overlap_text}\n\n{para}".strip()

    if current:
        raw_chunks.append(current)

    chunks = [
        Chunk(id=f"{doc.source}::chunk_{i}", source=doc.source, text=text)
        for i, text in enumerate(raw_chunks)
    ]
    return chunks


def chunk_documents(docs: List[Document], chunk_size: int = 900, chunk_overlap: int = 150) -> List[Chunk]:
    all_chunks: List[Chunk] = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc, chunk_size, chunk_overlap))
    return all_chunks


if __name__ == "__main__":
    from loader import load_documents
    docs = load_documents("data")
    chunks = chunk_documents(docs)
    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:3]:
        print("----", c.id, len(c.text))
        print(c.text[:200])
