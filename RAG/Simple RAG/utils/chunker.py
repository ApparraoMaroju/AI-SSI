from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .pdf_loader import PDFPage


@dataclass(frozen=True)
class ChunkRecord:
    chunk_id: str
    source_file: str
    source_path: str
    page_number: int
    chunk_index: int
    chunk_text: str
    character_count: int


def _make_chunk_id(source_file: str, page_number: int, chunk_index: int, chunk_text: str) -> str:
    digest = hashlib.sha1(chunk_text.encode("utf-8")).hexdigest()[:10]
    stem = Path(source_file).stem.replace(" ", "_")
    return f"{stem}-p{page_number:03d}-c{chunk_index:03d}-{digest}"


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if not text.strip():
        return []

    normalized = " ".join(text.split())
    if len(normalized) <= chunk_size:
        return [normalized]

    chunks: list[str] = []
    start = 0
    safe_overlap = max(0, min(chunk_overlap, chunk_size - 1))

    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(normalized):
            break
        start = max(0, end - safe_overlap)

    return chunks


def build_chunks(pages: list[PDFPage], chunk_size: int, chunk_overlap: int) -> list[ChunkRecord]:
    records: list[ChunkRecord] = []

    for page in pages:
        page_chunks = split_text(page.text, chunk_size, chunk_overlap)
        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            records.append(
                ChunkRecord(
                    chunk_id=_make_chunk_id(page.source_file, page.page_number, chunk_index, chunk_text),
                    source_file=page.source_file,
                    source_path=page.source_path,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    chunk_text=chunk_text,
                    character_count=len(chunk_text),
                )
            )

    return records
