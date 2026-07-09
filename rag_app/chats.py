"""
Lightweight JSON-file-backed storage for chat sessions, scoped per user.

Each chat is: {id, user_id, title, created_at, updated_at, messages: [{role, content, ts}]}
Stored as a single JSON file (db/chats.json) with a threading lock for
safe concurrent access from FastAPI's request handlers.
"""
import json
import os
import threading
import time
import uuid
from typing import List, Optional, Dict, Any

PERSIST_DIR = os.environ.get("PERSIST_DIR", os.path.dirname(__file__))
DB_PATH = os.path.join(PERSIST_DIR, "db", "chats.json")
_lock = threading.Lock()


def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"chats": []}, f)


def _read() -> Dict[str, Any]:
    _ensure_db()
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data: Dict[str, Any]) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_chats(user_id: str) -> List[Dict[str, Any]]:
    """Return chat summaries (no messages) for one user, newest first."""
    with _lock:
        data = _read()
    chats = [c for c in data["chats"] if c["user_id"] == user_id]
    chats.sort(key=lambda c: c["updated_at"], reverse=True)
    return [
        {"id": c["id"], "title": c["title"], "updated_at": c["updated_at"]}
        for c in chats
    ]


def create_chat(user_id: str, title: str = "New chat") -> Dict[str, Any]:
    with _lock:
        data = _read()
        now = time.time()
        chat = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": title,
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }
        data["chats"].append(chat)
        _write(data)
    return chat


def get_chat(chat_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Return the chat only if it belongs to user_id (prevents cross-user access)."""
    with _lock:
        data = _read()
    for c in data["chats"]:
        if c["id"] == chat_id and c["user_id"] == user_id:
            return c
    return None


def delete_chat(chat_id: str, user_id: str) -> bool:
    with _lock:
        data = _read()
        before = len(data["chats"])
        data["chats"] = [
            c for c in data["chats"] if not (c["id"] == chat_id and c["user_id"] == user_id)
        ]
        _write(data)
        return len(data["chats"]) < before


def rename_chat(chat_id: str, user_id: str, title: str) -> bool:
    with _lock:
        data = _read()
        for c in data["chats"]:
            if c["id"] == chat_id and c["user_id"] == user_id:
                c["title"] = title
                c["updated_at"] = time.time()
                _write(data)
                return True
    return False


def append_messages(chat_id: str, user_id: str, new_messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    """Append one or more {role, content} messages to a user's chat and touch updated_at."""
    with _lock:
        data = _read()
        for c in data["chats"]:
            if c["id"] == chat_id and c["user_id"] == user_id:
                for m in new_messages:
                    c["messages"].append({**m, "ts": time.time()})
                c["updated_at"] = time.time()
                # Auto-title from the first user message.
                if c["title"] == "New chat":
                    first_user = next((m for m in c["messages"] if m["role"] == "user"), None)
                    if first_user:
                        title = first_user["content"].strip().replace("\n", " ")
                        c["title"] = (title[:47] + "...") if len(title) > 50 else title
                _write(data)
                return c
    return None
