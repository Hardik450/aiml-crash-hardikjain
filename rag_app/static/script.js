const state = {
  currentChatId: null,
  chats: [],
};

const el = {
  chatList: document.getElementById("chatList"),
  messages: document.getElementById("messages"),
  emptyState: document.getElementById("emptyState"),
  chatTitle: document.getElementById("chatTitle"),
  composerInput: document.getElementById("composerInput"),
  sendBtn: document.getElementById("sendBtn"),
  newChatBtn: document.getElementById("newChatBtn"),
  kbNavBtn: document.getElementById("kbNavBtn"),
  chatView: document.getElementById("chatView"),
  kbView: document.getElementById("kbView"),
  dropZone: document.getElementById("dropZone"),
  fileInput: document.getElementById("fileInput"),
  kbList: document.getElementById("kbList"),
  kbCount: document.getElementById("kbCount"),
};

// ---------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------
function fmtBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

function fmtTime(ts) {
  const d = new Date(ts * 1000);
  return d.toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: opts.body instanceof FormData ? {} : { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

// ---------------------------------------------------------------------
// Chat sidebar
// ---------------------------------------------------------------------
async function refreshChatList() {
  state.chats = await api("/api/chats");
  el.chatList.innerHTML = "";
  for (const c of state.chats) {
    const item = document.createElement("div");
    item.className = "chat-item" + (c.id === state.currentChatId ? " active" : "");
    item.innerHTML = `<span class="chat-item-title"></span><button class="chat-item-delete">✕</button>`;
    item.querySelector(".chat-item-title").textContent = c.title;
    item.addEventListener("click", (e) => {
      if (e.target.closest(".chat-item-delete")) return;
      openChat(c.id);
    });
    item.querySelector(".chat-item-delete").addEventListener("click", async (e) => {
      e.stopPropagation();
      await api(`/api/chats/${c.id}`, { method: "DELETE" });
      if (state.currentChatId === c.id) {
        state.currentChatId = null;
        renderEmptyChat();
      }
      refreshChatList();
    });
    el.chatList.appendChild(item);
  }
}

function renderEmptyChat() {
  el.chatTitle.textContent = "AuraHealth Nexus Assistant";
  el.messages.innerHTML = "";
  el.messages.appendChild(el.emptyState);
  el.emptyState.style.display = "flex";
}

async function openChat(chatId) {
  state.currentChatId = chatId;
  const chat = await api(`/api/chats/${chatId}`);
  el.chatTitle.textContent = chat.title;
  el.messages.innerHTML = "";
  if (chat.messages.length === 0) {
    el.messages.appendChild(el.emptyState);
    el.emptyState.style.display = "flex";
  } else {
    for (const m of chat.messages) renderMessage(m.role, m.content, m.sources);
  }
  scrollToBottom();
  refreshChatList();
}

function renderMessage(role, content, sources) {
  if (el.emptyState.parentElement === el.messages) el.messages.removeChild(el.emptyState);
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "msg-content";
  bubble.textContent = content;

  if (role === "assistant") {
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "AI";
    row.appendChild(avatar);
  }

  const wrap = document.createElement("div");
  wrap.appendChild(bubble);

  if (sources && sources.length) {
    const srcRow = document.createElement("div");
    srcRow.className = "msg-sources";
    for (const s of sources) {
      const tag = document.createElement("span");
      tag.className = "src-tag";
      tag.textContent = s;
      srcRow.appendChild(tag);
    }
    wrap.appendChild(srcRow);
  }

  row.appendChild(wrap);
  el.messages.appendChild(row);
  return row;
}

function renderTyping() {
  const row = document.createElement("div");
  row.className = "msg-row assistant";
  row.id = "typingRow";
  row.innerHTML = `<div class="avatar">AI</div><div class="typing-dots"><span></span><span></span><span></span></div>`;
  el.messages.appendChild(row);
  scrollToBottom();
}

function removeTyping() {
  const row = document.getElementById("typingRow");
  if (row) row.remove();
}

function scrollToBottom() {
  el.messages.scrollTop = el.messages.scrollHeight;
}

// ---------------------------------------------------------------------
// Composer
// ---------------------------------------------------------------------
el.composerInput.addEventListener("input", () => {
  el.composerInput.style.height = "auto";
  el.composerInput.style.height = Math.min(el.composerInput.scrollHeight, 200) + "px";
  el.sendBtn.disabled = el.composerInput.value.trim().length === 0;
});

el.composerInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

el.sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
  const text = el.composerInput.value.trim();
  if (!text) return;

  if (!state.currentChatId) {
    const chat = await api("/api/chats", { method: "POST" });
    state.currentChatId = chat.id;
    await refreshChatList();
  }

  el.composerInput.value = "";
  el.composerInput.style.height = "auto";
  el.sendBtn.disabled = true;

  renderMessage("user", text);
  scrollToBottom();
  renderTyping();

  try {
    const res = await api(`/api/chats/${state.currentChatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content: text }),
    });
    removeTyping();
    renderMessage("assistant", res.answer, res.sources);
    scrollToBottom();
    refreshChatList();
    el.chatTitle.textContent = res.chat.title;
  } catch (err) {
    removeTyping();
    renderMessage("assistant", `Something went wrong: ${err.message}`);
  }
}

el.newChatBtn.addEventListener("click", () => {
  state.currentChatId = null;
  renderEmptyChat();
  showView("chat");
  refreshChatList();
  el.composerInput.focus();
});

// ---------------------------------------------------------------------
// View switching
// ---------------------------------------------------------------------
function showView(view) {
  if (view === "chat") {
    el.chatView.classList.remove("hidden");
    el.kbView.classList.add("hidden");
    el.kbNavBtn.classList.remove("active");
  } else {
    el.chatView.classList.add("hidden");
    el.kbView.classList.remove("hidden");
    el.kbNavBtn.classList.add("active");
    refreshKbList();
  }
}

el.kbNavBtn.addEventListener("click", () => showView("kb"));

// ---------------------------------------------------------------------
// Knowledge base
// ---------------------------------------------------------------------
async function refreshKbList() {
  const files = await api("/api/kb");
  el.kbCount.textContent = `${files.length} file${files.length === 1 ? "" : "s"}`;
  el.kbList.innerHTML = "";

  if (files.length === 0) {
    el.kbList.innerHTML = `<div class="kb-empty">No documents yet. Upload one above to get started.</div>`;
    return;
  }

  for (const f of files) {
    const item = document.createElement("div");
    item.className = "kb-item";
    item.innerHTML = `
      <div class="kb-item-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M7 2h7l5 5v13a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="1.6"/><path d="M14 2v5h5" stroke="currentColor" stroke-width="1.6"/></svg>
      </div>
      <div class="kb-item-info">
        <div class="kb-item-name"></div>
        <div class="kb-item-meta"></div>
      </div>
      <button class="kb-item-delete">Delete</button>
    `;
    item.querySelector(".kb-item-name").textContent = f.name;
    item.querySelector(".kb-item-meta").textContent =
      `${fmtBytes(f.size_bytes)} · ${f.chunk_count} chunks indexed · updated ${fmtTime(f.modified_at)}`;
    item.querySelector(".kb-item-delete").addEventListener("click", async () => {
      if (!confirm(`Delete "${f.name}" from the knowledge base? This can't be undone.`)) return;
      await api(`/api/kb/${encodeURIComponent(f.name)}`, { method: "DELETE" });
      refreshKbList();
    });
    el.kbList.appendChild(item);
  }
}

async function uploadFiles(fileList) {
  for (const file of fileList) {
    const form = new FormData();
    form.append("file", file);
    try {
      await api("/api/kb/upload", { method: "POST", body: form });
    } catch (err) {
      alert(`Failed to upload ${file.name}: ${err.message}`);
    }
  }
  refreshKbList();
}

el.dropZone.addEventListener("click", () => el.fileInput.click());
el.fileInput.addEventListener("change", (e) => uploadFiles(e.target.files));

["dragover", "dragenter"].forEach((evt) =>
  el.dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    el.dropZone.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach((evt) =>
  el.dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    el.dropZone.classList.remove("dragover");
  })
);
el.dropZone.addEventListener("drop", (e) => {
  if (e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
});

// ---------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------
(async function init() {
  await refreshChatList();
  renderEmptyChat();
})();
