from __future__ import annotations

from pathlib import Path

import chromadb

from .chunker import ChunkRecord


class ChromaStore:
    def __init__(self, persist_dir: Path, collection_name: str) -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        return self.collection.count()

    def existing_ids(self, ids: list[str]) -> set[str]:
        if not ids:
            return set()
        existing = self.collection.get(ids=ids)
        return set(existing.get("ids", []))

    def add_chunks(self, chunks: list[ChunkRecord], embeddings: list[list[float]]) -> int:
        if not chunks or not embeddings:
            return 0

        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.chunk_text for chunk in chunks]
        metadatas = [
            {
                "chunk_id": chunk.chunk_id,
                "source_file": chunk.source_file,
                "source_path": chunk.source_path,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "character_count": chunk.character_count,
            }
            for chunk in chunks
        ]

        missing_ids = self.existing_ids(ids)
        if missing_ids:
            filtered = [i for i, chunk_id in enumerate(ids) if chunk_id not in missing_ids]
            if not filtered:
                return 0
            ids = [ids[i] for i in filtered]
            documents = [documents[i] for i in filtered]
            metadatas = [metadatas[i] for i in filtered]
            embeddings = [embeddings[i] for i in filtered]

        self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        return len(ids)

    def query(self, query_embedding: list[float], top_k: int) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    def delete_collection(self) -> None:
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def stats(self) -> dict:
        data = self.collection.get(limit=25, include=["metadatas"])
        return {
            "collection_name": self.collection_name,
            "vector_count": self.count(),
            "sample_ids": list(data.get("ids", [])),
            "sample_metadata": list(data.get("metadatas", [])),
            "persist_dir": str(self.persist_dir),
        }
