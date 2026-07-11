const initialData = window.__INITIAL_DATA__ || {};
const el = (id) => document.getElementById(id);

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function shorten(value, length = 280) {
  const text = String(value || "");
  return text.length > length ? `${text.slice(0, length)}...` : text;
}

function renderPdfList(documents = []) {
  el("pdfCount").textContent = `${documents.length} PDF${documents.length === 1 ? "" : "s"}`;
  const container = el("pdfList");
  container.innerHTML = documents.length
    ? documents.map((doc) => `
      <article class="pdf-card">
        <div class="chunk-head">
          <strong>${escapeHtml(doc.source_file)}</strong>
          <span class="badge">${doc.page_count} pages</span>
        </div>
        <div class="meta-row"><span>${doc.total_characters} chars</span><span>${escapeHtml(doc.source_path)}</span></div>
        <div class="preview">${escapeHtml(shorten(doc.preview, 420))}</div>
      </article>`).join("")
    : `<div class="pdf-card">No PDFs found in the data folder yet.</div>`;
}

function renderDbStats(collection = {}, settings = {}) {
  el("vectorCount").textContent = `${collection.vector_count || 0} vectors`;
  const stats = [
    ["Collection", collection.collection_name || "-"],
    ["Persist Dir", collection.persist_dir || "-"],
    ["Chunk Size", settings.chunk_size ?? "-"],
    ["Chunk Overlap", settings.chunk_overlap ?? "-"],
    ["Top-K", settings.top_k ?? "-"],
    ["Embedding", settings.embedding_model || "-"],
    ["Groq Model", settings.groq_model || "-"],
  ];
  el("dbStats").innerHTML = stats.map(([label, value]) => `
    <div class="stat-item"><div class="stat-title">${escapeHtml(label)}</div><div class="stat-value">${escapeHtml(value)}</div></div>`).join("");
}

function renderChunks(chunks = []) {
  el("chunkCount").textContent = `${chunks.length} chunk${chunks.length === 1 ? "" : "s"}`;
  const container = el("chunkList");
  container.innerHTML = chunks.length
    ? chunks.map((chunk) => `
      <article class="chunk-card">
        <div class="chunk-head"><strong>${escapeHtml(chunk.chunk_id)}</strong><span class="badge">${chunk.character_count} chars</span></div>
        <div class="chunk-labels"><span class="badge">${escapeHtml(chunk.source_file)}</span><span class="badge">Page ${chunk.page_number}</span><span class="badge">Chunk ${chunk.chunk_index}</span></div>
        <div class="chunk-text">${escapeHtml(shorten(chunk.chunk_text, 520))}</div>
      </article>`).join("")
    : `<div class="chunk-card">No chunks have been created yet.</div>`;
}

function renderRetrievedChunks(chunks = []) {
  el("retrievedCount").textContent = `${chunks.length} retrieved`;
  const container = el("retrievedList");
  container.innerHTML = chunks.length
    ? chunks.map((chunk) => `
      <article class="chunk-card highlighted">
        <div class="chunk-head"><strong>${escapeHtml(chunk.chunk_id)}</strong><span class="badge">Score ${Number(chunk.score || 0).toFixed(3)}</span></div>
        <div class="chunk-labels"><span class="badge">${escapeHtml(chunk.source_file)}</span><span class="badge">Page ${chunk.page_number}</span></div>
        <div class="chunk-text">${escapeHtml(shorten(chunk.chunk_text, 520))}</div>
      </article>`).join("")
    : `<div class="chunk-card">Ask a question to see retrieved chunks here.</div>`;
}

function renderLogs(logs = []) {
  const container = el("logList");
  container.innerHTML = logs.length ? logs.map((entry) => `<div class="log-item">${escapeHtml(entry)}</div>`).join("") : `<div class="log-item">Logs will appear here after ingestion and queries.</div>`;
}

function renderConfigBox(settings = {}, errors = []) {
  el("configBox").innerHTML = `
    <div>Chunk size: ${escapeHtml(settings.chunk_size ?? "-")}</div>
    <div>Chunk overlap: ${escapeHtml(settings.chunk_overlap ?? "-")}</div>
    <div>Top-K: ${escapeHtml(settings.top_k ?? "-")}</div>
    <div>Embedding model: ${escapeHtml(settings.embedding_model || "-")}</div>
    <div>Groq model: ${escapeHtml(settings.groq_model || "-")}</div>
  `;

  el("errorsBox").innerHTML = errors.length ? errors.map((error) => `<div>${escapeHtml(error)}</div>`).join("") : `<div>No ingestion errors reported.</div>`;
}

function renderAll(payload) {
  renderPdfList(payload.documents || []);
  renderDbStats(payload.collection || {}, payload.settings || {});
  renderChunks(payload.chunks || []);
  renderLogs(payload.logs || []);
  renderConfigBox(payload.settings || {}, payload.errors || []);
}

async function refreshDashboard() {
  const response = await fetch("/api/dashboard");
  const payload = await response.json();
  renderAll(payload);
}

async function ingest() {
  el("ingestBtn").disabled = true;
  try {
    const response = await fetch("/api/ingest", { method: "POST" });
    const payload = await response.json();
    await refreshDashboard();
    el("answerMeta").textContent = payload.message || payload.status;
  } finally {
    el("ingestBtn").disabled = false;
  }
}

async function askQuestion() {
  const question = el("questionInput").value.trim();
  if (!question) {
    el("answerMeta").textContent = "Enter a question first";
    return;
  }

  el("askBtn").disabled = true;
  el("answerMeta").textContent = "Thinking...";
  el("answerText").textContent = "Retrieving chunks and generating an answer...";

  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.message || "Question failed");
    }

    el("answerText").textContent = payload.answer || "No answer returned.";
    el("answerMeta").textContent = `${payload.model} | ${payload.retrieved_chunks.length} chunks`;
    renderRetrievedChunks(payload.retrieved_chunks || []);
    el("flowFinal").classList.add("active");
    await refreshLogs();
  } catch (error) {
    el("answerText").textContent = error.message;
    el("answerMeta").textContent = "Error";
  } finally {
    el("askBtn").disabled = false;
  }
}

async function refreshLogs() {
  const response = await fetch("/api/logs");
  const payload = await response.json();
  renderLogs(payload.logs || []);
}

async function uploadPdf(file) {
  const formData = new FormData();
  formData.append("file", file);
  el("answerMeta").textContent = "Uploading PDF...";

  const response = await fetch("/api/upload", { method: "POST", body: formData });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.message || "Upload failed");
  }

  await refreshDashboard();
  el("answerMeta").textContent = payload.message || "PDF uploaded";
}

document.addEventListener("DOMContentLoaded", async () => {
  renderAll(initialData);

  el("ingestBtn").addEventListener("click", ingest);
  el("refreshBtn").addEventListener("click", async () => {
    await refreshDashboard();
    await refreshLogs();
  });
  el("askBtn").addEventListener("click", askQuestion);
  el("questionInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      askQuestion();
    }
  });
  el("pdfUpload").addEventListener("change", async (event) => {
    const [file] = event.target.files || [];
    if (!file) return;
    try {
      await uploadPdf(file);
    } catch (error) {
      el("answerMeta").textContent = "Upload failed";
      el("answerText").textContent = error.message;
    } finally {
      event.target.value = "";
    }
  });

  await refreshLogs();
});
