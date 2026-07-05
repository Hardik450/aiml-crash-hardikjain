import os
import pickle
from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from chunker import Chunk


class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: List[Chunk] = []

    def _normalize(self, matrix: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (matrix / norms).astype("float32")

    def _embed(self, texts: List[str]) -> np.ndarray:
        """Generate sentence-transformer embeddings for a list of texts."""
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=False)
        return np.asarray(embeddings, dtype=np.float32)

    def build(self, chunks: List[Chunk]) -> None:
        """
        Generate embeddings for all chunks and build the FAISS index.
        """
        self.chunks = chunks

        texts = [c.text for c in chunks]

        vectors = self._embed(texts)
        vectors = self._normalize(vectors)

        dim = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Chunk, float]]:
        """
        Retrieve the most semantically similar chunks for a query.
        """
        if self.index is None:
            raise RuntimeError(
                "Vector store has not been built yet. Call build() first."
            )

        query_vec = self._embed([query])
        query_vec = self._normalize(query_vec)

        scores, indices = self.index.search(query_vec, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], float(score)))

        return results

    def save(self, path: str) -> None:
        """
        Save the FAISS index and chunk metadata.
        """
        os.makedirs(path, exist_ok=True)

        faiss.write_index(self.index, os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "chunks.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self, path: str) -> None:
        """
        Load the FAISS index and chunk metadata.
        """
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "chunks.pkl"), "rb") as f:
            self.chunks = pickle.load(f)


if __name__ == "__main__":
    from loader import load_documents
    from chunker import chunk_documents

    docs = load_documents("data")
    chunks = chunk_documents(docs)

    store = VectorStore()
    store.build(chunks)
    store.save("vector_index")

    print(f"Indexed {len(chunks)} chunks.")

    results = store.search(
        "What is the override code for the Cognitive Reset Sequence?",
        top_k=3,
    )

    for chunk, score in results:
        print(f"[{score:.3f}] {chunk.id}")
        print(chunk.text[:200], "\n")