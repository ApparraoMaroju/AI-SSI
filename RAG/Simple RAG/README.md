# Simple Local RAG Demo

This project is a compact, local Retrieval-Augmented Generation sample built from the attached prompt. It ingests PDFs from a `data/` folder, chunks the extracted text, stores vectors in persistent ChromaDB, and answers questions with Groq.

## What is included

- PDF ingestion with page metadata
- Configurable chunking
- Nomic embedding generation through `sentence-transformers`
- Persistent local ChromaDB storage
- Groq-powered answer generation
- Responsive HTML dashboard with chunk, retrieval, and database views
- In-memory logs for each stage of the pipeline

## Folder Layout

```text
Simple RAG/
├── data/
├── chroma_db/
├── templates/
├── static/
├── utils/
├── app.py
├── ingest.py
├── rag.py
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your Groq key if needed.
4. Place one or more PDFs in the `data/` folder.

## Run

Start the web app:

```bash
python app.py
```

Open the dashboard at `http://127.0.0.1:5000`.

To run ingestion from the command line:

```bash
python ingest.py
```

## How it works

1. PDFs are discovered in `data/`.
2. Text is extracted page by page.
3. Text is chunked with overlap.
4. Each chunk is embedded with the configured Nomic model.
5. ChromaDB persists the chunk vectors locally.
6. A question is embedded and matched against the stored vectors.
7. The top chunks are sent to Groq with a grounded prompt.
8. The answer and retrieved chunks are shown in the dashboard.

## Configuration

Adjust the following in `.env`:

- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `TOP_K`
- `EMBEDDING_MODEL`
- `GROQ_MODEL`
- `CHROMA_PERSIST_DIR`
- `CHROMA_COLLECTION_NAME`
- `DATA_DIR`

## Troubleshooting

- If no PDF appears, make sure it is inside `data/` and has a `.pdf` extension.
- If embedding fails, verify the model name and that the machine can download the model the first time.
- If Groq requests fail, confirm `GROQ_API_KEY` is set.
- If the database looks empty, click **Ingest PDFs** after adding files.
- If the PDF is scanned or image-only, install OCR support with `pdf2image`, `pytesseract`, Tesseract OCR, and Poppler. Without those native tools, the sample cannot extract text from images.

## Notes

This is a sample implementation intended to be readable and easy to extend. It keeps the pipeline modular so the embedding model, vector store, and LLM can be swapped later.
