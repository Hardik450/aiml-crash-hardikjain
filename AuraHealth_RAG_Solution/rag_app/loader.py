import os
from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    source: str
    text: str


def load_documents(data_dir: str) -> List[Document]:
    """Load all .txt files from data_dir into Document objects."""
    docs = []
    for fname in sorted(os.listdir(data_dir)):
        if not fname.lower().endswith(".txt"):
            continue
        fpath = os.path.join(data_dir, fname)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        text = raw.replace("\r\n", "\n").replace("\r", "\n")
        docs.append(Document(source=fname, text=text))
    return docs


if __name__ == "__main__":
    docs = load_documents("data")
    for d in docs:
        print(f"{d.source}: {len(d.text)} chars")
