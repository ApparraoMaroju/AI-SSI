from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from groq import Groq

from config import Settings
from utils.chunker import ChunkRecord, build_chunks
from utils.database import ChromaStore
from utils.embeddings import NomicEmbeddingModel
from utils.pdf_loader import load_pdf_pages


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    source_file: str
    page_number: int
    chunk_text: str
    score: float
    character_count: int


class RAGService:
    def __init__(self, settings: Settings, store: ChromaStore, embedder: NomicEmbeddingModel) -> None:
        self.settings = settings
        self.store = store
        self.embedder = embedder

    def _groq_client(self) -> Groq:
        if not self.settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Set it in .env before asking questions.")
        return Groq(api_key=self.settings.groq_api_key)

    def ingest(self) -> dict[str, Any]:
        pages, documents, pdf_errors = load_pdf_pages(self.settings.data_dir)
        if not documents:
            return {
                "status": "empty",
                "message": "No PDF files were found in the data folder.",
                "documents": [],
                "chunks_created": 0,
                "chunks_added": 0,
                "pdf_errors": pdf_errors,
            }

        chunks = build_chunks(pages, self.settings.chunk_size, self.settings.chunk_overlap)
        if not chunks:
            return {
                "status": "empty",
                "message": "PDFs were found, but no extractable text was detected.",
                "documents": [asdict(doc) for doc in documents],
                "chunks_created": 0,
                "chunks_added": 0,
                "pdf_errors": pdf_errors,
            }

        chunk_texts = [chunk.chunk_text for chunk in chunks]
        embeddings = self.embedder.embed_documents(chunk_texts)
        chunks_added = self.store.add_chunks(chunks, embeddings)

        return {
            "status": "success",
            "message": f"Processed {len(documents)} PDF file(s) and stored {chunks_added} new chunk(s).",
            "documents": [asdict(doc) for doc in documents],
            "pages": len(pages),
            "total_characters": sum(doc.total_characters for doc in documents),
            "chunks_created": len(chunks),
            "chunks_added": chunks_added,
            "pdf_errors": pdf_errors,
            "collection_count": self.store.count(),
        }

    def _format_retrieved_chunks(self, query_result: dict) -> list[RetrievedChunk]:
        ids = query_result.get("ids", [[]])[0]
        documents = query_result.get("documents", [[]])[0]
        metadatas = query_result.get("metadatas", [[]])[0]
        distances = query_result.get("distances", [[]])[0]

        retrieved: list[RetrievedChunk] = []
        for chunk_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            similarity = max(0.0, 1.0 - float(distance))
            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    source_file=str(metadata.get("source_file", "")),
                    page_number=int(metadata.get("page_number", 0)),
                    chunk_text=document,
                    score=similarity,
                    character_count=int(metadata.get("character_count", len(document or ""))),
                )
            )
        return retrieved

    def _build_prompt(self, question: str, chunks: list[RetrievedChunk]) -> str:
        context_blocks = []
        for index, chunk in enumerate(chunks, start=1):
            context_blocks.append(
                f"[Chunk {index}] Source: {chunk.source_file} | Page: {chunk.page_number} | ID: {chunk.chunk_id}\n{chunk.chunk_text}"
            )

        context = "\n\n".join(context_blocks) if context_blocks else "No supporting context was retrieved."
        return (
            "You are a grounded RAG assistant. Answer only from the provided context. "
            "If the context is insufficient, say that clearly. Cite the chunk ids you used.\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context}\n\n"
            "Answer in a concise, helpful way."
        )

    def answer(self, question: str) -> dict[str, Any]:
        if not question.strip():
            raise ValueError("Question cannot be empty.")
        if self.store.count() == 0:
            raise RuntimeError("The ChromaDB collection is empty. Ingest PDFs before asking a question.")

        query_embedding = self.embedder.embed_query(question)
        query_result = self.store.query(query_embedding, self.settings.top_k)
        retrieved_chunks = self._format_retrieved_chunks(query_result)
        prompt = self._build_prompt(question, retrieved_chunks)

        client = self._groq_client()
        try:
            response = client.chat.completions.create(
                model=self.settings.groq_model,
                messages=[
                    {"role": "system", "content": "You answer questions using retrieved context only."},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.settings.temperature,
                max_tokens=self.settings.max_new_tokens,
            )
            answer_text = response.choices[0].message.content or ""
        except Exception as exc:
            raise RuntimeError(f"Groq API request failed: {exc}") from exc

        return {
            "question": question,
            "answer": answer_text,
            "prompt": prompt,
            "retrieved_chunks": [
                {
                    **asdict(chunk),
                    "highlighted": True,
                }
                for chunk in retrieved_chunks
            ],
            "top_k": self.settings.top_k,
            "model": self.settings.groq_model,
        }

    def snapshot(self) -> dict[str, Any]:
        pages, documents, errors = load_pdf_pages(self.settings.data_dir)
        chunks = build_chunks(pages, self.settings.chunk_size, self.settings.chunk_overlap)
        return {
            "documents": [asdict(item) for item in documents],
            "chunks": [asdict(item) for item in chunks[:100]],
            "errors": errors,
            "collection": self.store.stats(),
            "settings": {
                "chunk_size": self.settings.chunk_size,
                "chunk_overlap": self.settings.chunk_overlap,
                "top_k": self.settings.top_k,
                "embedding_model": self.settings.embedding_model,
                "groq_model": self.settings.groq_model,
            },
        }
