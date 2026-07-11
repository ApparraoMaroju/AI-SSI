from __future__ import annotations

import logging
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from config import get_settings
from rag import RAGService
from utils.database import ChromaStore
from utils.embeddings import NomicEmbeddingModel


class InMemoryLogHandler(logging.Handler):
    def __init__(self, buffer: deque[str]) -> None:
        super().__init__()
        self.buffer = buffer

    def emit(self, record: logging.LogRecord) -> None:
        self.buffer.appendleft(self.format(record))


settings = get_settings()
log_buffer: deque[str] = deque(maxlen=300)

logger = logging.getLogger("simple_rag")
logger.setLevel(logging.INFO)
logger.handlers.clear()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
memory_handler = InMemoryLogHandler(log_buffer)
memory_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(stream_handler)
logger.addHandler(memory_handler)

store = ChromaStore(settings.chroma_persist_dir, settings.chroma_collection_name)
embedder = NomicEmbeddingModel(settings.embedding_model)
service = RAGService(settings, store, embedder)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


def _dashboard_payload() -> dict[str, Any]:
    snapshot = service.snapshot()
    return {
        "documents": snapshot["documents"],
        "chunks": snapshot["chunks"],
        "errors": snapshot["errors"],
        "collection": snapshot["collection"],
        "settings": snapshot["settings"],
        "logs": list(log_buffer),
    }


@app.route("/")
def index() -> str:
    return render_template("index.html", initial_data=_dashboard_payload(), now=datetime.utcnow())


@app.route("/api/dashboard")
def dashboard() -> Any:
    return jsonify(_dashboard_payload())


@app.route("/api/ingest", methods=["POST"])
def ingest() -> Any:
    logger.info("Starting PDF ingestion")
    result = service.ingest()
    if result.get("status") == "success":
        logger.info(result["message"])
    else:
        logger.warning(result.get("message", "Ingestion finished with no data."))
    return jsonify(result)


@app.route("/api/ask", methods=["POST"])
def ask() -> Any:
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    try:
        logger.info("Received question: %s", question)
        result = service.answer(question)
        logger.info("Generated response using %s retrieved chunk(s)", len(result["retrieved_chunks"]))
        return jsonify({"status": "success", **result})
    except Exception as exc:
        logger.exception("Question handling failed")
        return jsonify({"status": "error", "message": str(exc)}), 400


@app.route("/api/upload", methods=["POST"])
def upload() -> Any:
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file was uploaded."}), 400

    file = request.files["file"]
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"status": "error", "message": "Only PDF files are supported."}), 400

    target_path = settings.data_dir / Path(file.filename).name
    file.save(target_path)
    logger.info("Saved uploaded file to %s", target_path)
    result = service.ingest()
    return jsonify({"status": "success", "message": f"Uploaded {file.filename}", "ingest": result})


@app.route("/api/logs")
def logs() -> Any:
    return jsonify({"logs": list(log_buffer)})


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
