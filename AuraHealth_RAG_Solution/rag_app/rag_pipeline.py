
import os
from typing import List, Optional

from loader import load_documents
from chunker import chunk_documents
from vectorstore import VectorStore
from generator import Generator

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "vector_index")


class RAGPipeline:
    def __init__(self, top_k: int = 5, history_limit: int = 6, model: Optional[str] = None):
        self.top_k = top_k
        self.history_limit = history_limit  
        self.store = VectorStore()
        self.generator = Generator(model=model) if model else Generator()
        self.history: List[dict] = []

    def index(self, data_dir: str = DATA_DIR, force_rebuild: bool = False, save_path: str = INDEX_DIR):
        """Build (or load a cached) vector index from the source documents."""
        if not force_rebuild and os.path.isdir(save_path) and os.listdir(save_path):
            self.store.load(save_path)
        else:
            docs = load_documents(data_dir)
            chunks = chunk_documents(docs)
            self.store.build(chunks)
            self.store.save(save_path)

    def reset_history(self):
        self.history = []

    def ask(self, query: str, use_history: bool = True) -> str:
        history = self.history if use_history else None
        search_query = self.generator.contextualize_query(query, history)

        retrieved = self.store.search(search_query, top_k=self.top_k)
        answer = self.generator.generate(query, retrieved, history=history)

        if use_history:
            self.history.append({"role": "user", "content": query})
            self.history.append({"role": "assistant", "content": answer})
            if len(self.history) > self.history_limit:
                self.history = self.history[-self.history_limit:]

        return answer


if __name__ == "__main__":
    pipeline = RAGPipeline(top_k=5)
    pipeline.index()

    print("AuraHealth Nexus RAG assistant ready. Type 'exit' to quit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        answer = pipeline.ask(query)
        print(f"Assistant: {answer}\n")
