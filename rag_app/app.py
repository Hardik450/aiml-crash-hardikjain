"""
FastAPI backend for the AuraHealth Nexus RAG assistant.

Serves:
  - A login / sign-up page for unauthenticated visitors.
  - A ChatGPT-style single-page UI (static/index.html) with a sidebar of
    chat sessions (scoped to the logged-in user) and a main chat panel.
  - A Knowledge Base panel (shared across all users) where documents can
    be uploaded or deleted, triggering an automatic re-index.

Auth model: simple cookie-based sessions (itsdangerous-signed cookie via
Starlette's SessionMiddleware). Passwords are hashed with bcrypt and
stored in db/users.json. This is intentionally lightweight (no external
auth provider / DB) to match the rest of this project's file-based
storage -- swap in a real database + OAuth/JWT provider for production
use with many users.

Run with:
    uvicorn app:app --reload --port 8000
"""
print("APP START", flush=True)
import os
import shutil
import threading
from collections import Counter
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

from loader import load_documents
from chunker import chunk_documents
from vectorstore import VectorStore
from generator import Generator
import chats
import users

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

# PERSIST_DIR points at the mounted bucket (e.g. "/data" on HF Spaces).
# Falls back to BASE_DIR for local/dev runs where no bucket is mounted.
PERSIST_DIR = os.environ.get("PERSIST_DIR", BASE_DIR)
DATA_DIR = os.path.join(PERSIST_DIR, "data")
INDEX_DIR = os.path.join(PERSIST_DIR, "vector_index")

ALLOWED_EXTENSIONS = {".txt", ".md"}
HISTORY_WINDOW = 8  # number of prior messages fed to the LLM for context


def _seed_persist_dir():
    """On first boot the mounted bucket is empty -- copy the baked-in
    data/ and vector_index/ from the image into it once, so the app
    doesn't start with zero documents/index. Safe to call every boot:
    it no-ops once the bucket already has content."""
    baked_data = os.path.join(BASE_DIR, "data")
    baked_index = os.path.join(BASE_DIR, "vector_index")
    baked_db = os.path.join(BASE_DIR, "db")
    persist_db = os.path.join(PERSIST_DIR, "db")

    if PERSIST_DIR != BASE_DIR:
        if not os.path.isdir(DATA_DIR) or not os.listdir(DATA_DIR):
            if os.path.isdir(baked_data):
                shutil.copytree(baked_data, DATA_DIR, dirs_exist_ok=True)
        if not os.path.isdir(INDEX_DIR) or not os.listdir(INDEX_DIR):
            if os.path.isdir(baked_index):
                shutil.copytree(baked_index, INDEX_DIR, dirs_exist_ok=True)
        if not os.path.isdir(persist_db) or not os.listdir(persist_db):
            if os.path.isdir(baked_db):
                shutil.copytree(baked_db, persist_db, dirs_exist_ok=True)


_seed_persist_dir()

# IMPORTANT: set a real, secret value via the SESSION_SECRET_KEY env var in
# production. Sessions are signed (not encrypted) with this key -- anyone
# who knows it can forge a login cookie.
SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "dev-only-insecure-secret-change-me")

os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Global RAG state (shared across all users). A lock guards rebuilds so a
# chat request never reads a half-rebuilt index.
# ---------------------------------------------------------------------------
index_lock = threading.Lock()
store = VectorStore()
generator = Generator()


def rebuild_index() -> None:
    """Reload every document in data/, re-chunk, re-embed, and rebuild FAISS."""
    docs = load_documents(DATA_DIR)
    chunks = chunk_documents(docs) if docs else []
    with index_lock:
        if chunks:
            store.build(chunks)
            store.save(INDEX_DIR)
        else:
            store.chunks = []
            store.index = None

def load_or_build_index():
    print("Loading vector index...")

    if os.path.isdir(INDEX_DIR) and os.listdir(INDEX_DIR):
        try:
            print(f"PERSIST_DIR = {PERSIST_DIR}")
            print(f"INDEX_DIR = {INDEX_DIR}")
            print(f"Exists: {os.path.exists(INDEX_DIR)}")
            print(f"Files: {os.listdir(INDEX_DIR) if os.path.exists(INDEX_DIR) else 'No directory'}")
            store.load(INDEX_DIR)
            print("Vector index loaded successfully.")
            return
        except Exception as e:
            print(f"Failed to load vector index: {e}")

    print("Rebuilding vector index...")
    rebuild_index()
    print("Vector index rebuilt.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_or_build_index()
    yield


app = FastAPI(title="AuraHealth Nexus RAG Assistant", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY, same_site="lax")


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def get_current_user(request: Request) -> Optional[dict]:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return users.get_user_by_id(user_id)


def require_user(request: Request) -> dict:
    """FastAPI dependency: 401s if there's no valid logged-in session."""
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user


class SignupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/auth/signup")
def api_signup(body: SignupRequest, request: Request):
    try:
        user = users.create_user(body.username, body.password)
    except ValueError as e:
        raise HTTPException(400, str(e))
    request.session["user_id"] = user["id"]
    return {"id": user["id"], "username": user["username"]}


@app.post("/api/auth/login")
def api_login(body: LoginRequest, request: Request):
    user = users.verify_password(body.username, body.password)
    if not user:
        raise HTTPException(401, "Incorrect username or password")
    request.session["user_id"] = user["id"]
    return {"id": user["id"], "username": user["username"]}


@app.post("/api/auth/logout")
def api_logout(request: Request):
    request.session.clear()
    return {"logged_out": True}


@app.get("/api/auth/me")
def api_me(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return {"id": user["id"], "username": user["username"]}


# ---------------------------------------------------------------------------
# Chat endpoints (all scoped to the logged-in user)
# ---------------------------------------------------------------------------
class NewMessage(BaseModel):
    content: str


class RenameRequest(BaseModel):
    title: str


@app.get("/api/chats")
def api_list_chats(user: dict = Depends(require_user)):
    return chats.list_chats(user["id"])


@app.post("/api/chats")
def api_create_chat(user: dict = Depends(require_user)):
    return chats.create_chat(user["id"])


@app.get("/api/chats/{chat_id}")
def api_get_chat(chat_id: str, user: dict = Depends(require_user)):
    chat = chats.get_chat(chat_id, user["id"])
    if not chat:
        raise HTTPException(404, "Chat not found")
    return chat


@app.delete("/api/chats/{chat_id}")
def api_delete_chat(chat_id: str, user: dict = Depends(require_user)):
    ok = chats.delete_chat(chat_id, user["id"])
    if not ok:
        raise HTTPException(404, "Chat not found")
    return {"deleted": True}


@app.patch("/api/chats/{chat_id}")
def api_rename_chat(chat_id: str, body: RenameRequest, user: dict = Depends(require_user)):
    ok = chats.rename_chat(chat_id, user["id"], body.title)
    if not ok:
        raise HTTPException(404, "Chat not found")
    return {"renamed": True}


@app.post("/api/chats/{chat_id}/messages")
def api_send_message(chat_id: str, body: NewMessage, user: dict = Depends(require_user)):
    chat = chats.get_chat(chat_id, user["id"])
    if not chat:
        raise HTTPException(404, "Chat not found")

    query = body.content.strip()
    if not query:
        raise HTTPException(400, "Message cannot be empty")

    prior = chat["messages"][-HISTORY_WINDOW:]
    history = [{"role": m["role"], "content": m["content"]} for m in prior]

    with index_lock:
        has_docs = store.index is not None and len(store.chunks) > 0

    if not has_docs:
        answer = (
            "There are no documents in the knowledge base yet. "
            "Upload a file in the Knowledge Base panel and I'll be able to answer "
            "questions about it."
        )
        sources: List[str] = []
    else:
        search_query = generator.contextualize_query(query, history)
        with index_lock:
            retrieved = store.search(search_query, top_k=5)
        answer = generator.generate(query, retrieved, history=history)
        sources = sorted({c.source for c, _ in retrieved})

    updated = chats.append_messages(
        chat_id,
        user["id"],
        [
            {"role": "user", "content": query},
            {"role": "assistant", "content": answer, "sources": sources},
        ],
    )
    return {"answer": answer, "sources": sources, "chat": updated}


# ---------------------------------------------------------------------------
# Knowledge base endpoints (shared across all logged-in users)
# ---------------------------------------------------------------------------
@app.get("/api/kb")
def api_list_kb(user: dict = Depends(require_user)):
    with index_lock:
        chunk_counts = Counter(c.source for c in store.chunks)

    files = []
    for fname in sorted(os.listdir(DATA_DIR)):
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        stat = os.stat(fpath)
        files.append(
            {
                "name": fname,
                "size_bytes": stat.st_size,
                "modified_at": stat.st_mtime,
                "chunk_count": chunk_counts.get(fname, 0),
            }
        )
    return files


@app.post("/api/kb/upload")
async def api_upload_kb(file: UploadFile = File(...), user: dict = Depends(require_user)):
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            f"Unsupported file type '{ext}'. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    dest_path = os.path.join(DATA_DIR, os.path.basename(file.filename))
    with open(dest_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    rebuild_index()
    return {"uploaded": file.filename}


@app.delete("/api/kb/{filename}")
def api_delete_kb(filename: str, user: dict = Depends(require_user)):
    fpath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(fpath):
        raise HTTPException(404, "File not found")
    os.remove(fpath)
    rebuild_index()
    return {"deleted": filename}


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_index(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/login")
def serve_login(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/")
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))
