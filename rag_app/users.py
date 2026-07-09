"""
Lightweight JSON-file-backed storage for user accounts.

Each user is: {id, username, password_hash, created_at}
Stored as a single JSON file (db/users.json) with a threading lock for
safe concurrent access from FastAPI's request handlers.

Passwords are hashed with bcrypt directly -- never stored in plaintext.
"""
import json
import os
import threading
import time
import uuid
from typing import Optional, Dict, Any

import bcrypt

PERSIST_DIR = os.environ.get("PERSIST_DIR", os.path.dirname(__file__))
DB_PATH = os.path.join(PERSIST_DIR, "db", "users.json")
_lock = threading.Lock()


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f)


def _read() -> Dict[str, Any]:
    _ensure_db()
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data: Dict[str, Any]) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with _lock:
        data = _read()
    username_lower = username.strip().lower()
    for u in data["users"]:
        if u["username"].lower() == username_lower:
            return u
    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        data = _read()
    for u in data["users"]:
        if u["id"] == user_id:
            return u
    return None


def create_user(username: str, password: str) -> Dict[str, Any]:
    username = username.strip()
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be at most 72 characters.")

    with _lock:
        data = _read()
        if any(u["username"].lower() == username.lower() for u in data["users"]):
            raise ValueError("That username is already taken.")

        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "password_hash": _hash_password(password),
            "created_at": time.time(),
        }
        data["users"].append(user)
        _write(data)
    return user


def verify_password(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Return the user dict if the username/password combo is valid, else None."""
    user = get_user_by_username(username)
    if not user:
        return None
    if not _check_password(password, user["password_hash"]):
        return None
    return user
