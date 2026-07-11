from __future__ import annotations

import json

from config import get_settings
from rag import RAGService
from utils.database import ChromaStore
from utils.embeddings import NomicEmbeddingModel


def main() -> None:
    settings = get_settings()
    store = ChromaStore(settings.chroma_persist_dir, settings.chroma_collection_name)
    embedder = NomicEmbeddingModel(settings.embedding_model)
    service = RAGService(settings, store, embedder)
    result = service.ingest()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
