from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

try:
    import fitz
except Exception:  # pragma: no cover - optional PyMuPDF dependency
    fitz = None

try:
    from pdf2image import convert_from_path
    from PIL import Image
    import pytesseract
except Exception:  # pragma: no cover - optional OCR dependencies
    convert_from_path = None
    Image = None
    pytesseract = None


@dataclass(frozen=True)
class PDFPage:
    source_file: str
    source_path: str
    page_number: int
    page_count: int
    text: str


@dataclass(frozen=True)
class PDFDocumentInfo:
    source_file: str
    source_path: str
    page_count: int
    total_characters: int
    preview: str


def load_pdf_pages(data_dir: Path) -> tuple[list[PDFPage], list[PDFDocumentInfo], list[str]]:
    pages: list[PDFPage] = []
    documents: list[PDFDocumentInfo] = []
    errors: list[str] = []

    pdf_paths = sorted(data_dir.glob("*.pdf"))
    if not pdf_paths:
        return pages, documents, errors

    for pdf_path in pdf_paths:
        try:
            reader = PdfReader(str(pdf_path))
            page_count = len(reader.pages)
            extracted_pages: list[PDFPage] = []
            combined_text: list[str] = []

            for page_index, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    extracted_pages.append(
                        PDFPage(
                            source_file=pdf_path.name,
                            source_path=str(pdf_path),
                            page_number=page_index,
                            page_count=page_count,
                            text=text,
                        )
                    )
                    combined_text.append(text)

            total_characters = sum(len(item.text) for item in extracted_pages)
            preview_text = " ".join(combined_text)[:500]

            if total_characters == 0 and convert_from_path and pytesseract:
                extracted_pages, combined_text = _ocr_pdf(pdf_path, page_count)
                total_characters = sum(len(item.text) for item in extracted_pages)
                preview_text = " ".join(combined_text)[:500]

            if total_characters == 0 and fitz is not None:
                extracted_pages, combined_text = _extract_with_pymupdf(pdf_path)
                total_characters = sum(len(item.text) for item in extracted_pages)
                preview_text = " ".join(combined_text)[:500]

            if total_characters == 0:
                errors.append(
                    f"{pdf_path.name}: no extractable text was found. If this is a scanned PDF, install pdf2image, pytesseract, Tesseract OCR, and Poppler."
                )

            documents.append(
                PDFDocumentInfo(
                    source_file=pdf_path.name,
                    source_path=str(pdf_path),
                    page_count=page_count,
                    total_characters=total_characters,
                    preview=preview_text,
                )
            )
            pages.extend(extracted_pages)
        except Exception as exc:
            errors.append(f"{pdf_path.name}: {exc}")

    return pages, documents, errors


def _ocr_pdf(pdf_path: Path, page_count: int) -> tuple[list[PDFPage], list[str]]:
    if not convert_from_path or not pytesseract:
        return [], []

    ocr_pages: list[PDFPage] = []
    combined_text: list[str] = []

    try:
        images = convert_from_path(str(pdf_path), dpi=200)
    except Exception:
        return [], []

    for page_index, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image).strip()
        if text:
            ocr_pages.append(
                PDFPage(
                    source_file=pdf_path.name,
                    source_path=str(pdf_path),
                    page_number=page_index,
                    page_count=page_count,
                    text=text,
                )
            )
            combined_text.append(text)

    return ocr_pages, combined_text


def _extract_with_pymupdf(pdf_path: Path) -> tuple[list[PDFPage], list[str]]:
    if fitz is None:
        return [], []

    extracted_pages: list[PDFPage] = []
    combined_text: list[str] = []

    try:
        document = fitz.open(str(pdf_path))
    except Exception:
        return [], []

    page_count = document.page_count
    for page_index in range(page_count):
        page = document.load_page(page_index)
        text = page.get_text("text").strip()
        if text:
            extracted_pages.append(
                PDFPage(
                    source_file=pdf_path.name,
                    source_path=str(pdf_path),
                    page_number=page_index + 1,
                    page_count=page_count,
                    text=text,
                )
            )
            combined_text.append(text)

    document.close()
    return extracted_pages, combined_text
