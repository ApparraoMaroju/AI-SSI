# Build a Complete Local RAG System using ChromaDB, Nomic Embeddings & Groq (RACE Framework)

# R — Role

You are a Senior AI Engineer and Full-Stack Developer with expertise in:

* Retrieval-Augmented Generation (RAG)
* Python
* LangChain
* ChromaDB
* Vector Databases
* PDF Processing
* Nomic Embeddings
* Groq API
* HTML/CSS/JavaScript
* Software Architecture
* Interactive Data Visualization

Your objective is to design and implement a production-ready, modular, and well-documented local RAG application following software engineering best practices.

---

# A — Action

Build a complete end-to-end Retrieval-Augmented Generation (RAG) application with the following requirements:

## 1. Project Structure

Create a clean and modular project structure similar to:

```text
RAG_Project/
│
├── data/
│     └── (I will place my PDF here)
│
├── chroma_db/
│
├── templates/
│     └── index.html
│
├── static/
│     ├── style.css
│     └── script.js
│
├── utils/
│     ├── pdf_loader.py
│     ├── chunker.py
│     ├── embeddings.py
│     └── database.py
│
├── app.py
├── ingest.py
├── rag.py
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 2. PDF Ingestion

* Read every PDF placed inside the **data/** folder.
* Extract text while preserving page metadata.
* Display:

  * Number of pages
  * Total extracted characters
  * Number of chunks created

---

## 3. Chunking

Implement configurable text chunking.

Allow configuration for:

* Chunk Size
* Chunk Overlap

Store metadata for every chunk:

* Chunk ID
* Source File
* Page Number
* Chunk Text

---

## 4. Embeddings

Use the **Nomic Embed** model to generate embeddings.

Requirements:

* Generate embeddings for every chunk.
* Store embeddings locally.
* Avoid duplicate embedding generation.
* Make the embedding model configurable.

---

## 5. ChromaDB

Use a **persistent local ChromaDB** instance.

Implement:

* Database creation
* Persistent storage
* Similarity search
* Collection loading
* Collection deletion
* Collection statistics

Create reusable helper methods for database operations.

---

## 6. RAG Pipeline

Implement the complete Retrieval-Augmented Generation workflow:

```text
User Question
      ↓
Generate Query Embedding
      ↓
Search ChromaDB
      ↓
Retrieve Top-K Chunks
      ↓
Construct Prompt
      ↓
Send Prompt to Groq
      ↓
Generate Final Response
```

Allow Top-K retrieval to be configurable.

---

## 7. Groq Integration

Integrate the Groq API.

Requirements:

* Read the API key from an environment variable.
* Keep the model configurable.
* Make it easy to replace the LLM in the future.
* Include proper exception handling for API failures.

---

## 8. Interactive HTML Dashboard

Create a clean, responsive dashboard that contains the following sections:

### PDF Viewer

Display:

* Uploaded PDF name
* Page count
* Extracted text preview

---

### Chunk Viewer

Display every generated chunk with:

* Chunk ID
* Page Number
* Character Count
* Chunk Content

---

### Query Section

Provide:

* Text input
* Ask button
* Response area

---

### Retrieved Chunks

After every query, display:

* Retrieved Chunk IDs
* Similarity Scores
* Chunk Content
* Source Page

Highlight the chunks used to generate the answer.

---

### RAG Flow Visualization

Create a simple visual diagram illustrating the retrieval pipeline.

Example:

```text
Question
   │
   ▼
Embedding
   │
   ▼
ChromaDB
   │
   ▼
Retrieved Chunks
   │
   ▼
Prompt Builder
   │
   ▼
Groq LLM
   │
   ▼
Final Answer
```

The diagram should visually indicate which chunks were retrieved.

---

### Database Explorer

Display:

* Collection Name
* Number of Stored Vectors
* Chunk IDs
* Metadata
* Database Statistics

---

## 9. Logging

Display logs for:

* PDF loading
* Chunk creation
* Embedding generation
* ChromaDB insertion
* Retrieval
* Prompt construction
* LLM response

---

## 10. Configuration

Move configurable values into a configuration file.

Examples:

* Chunk Size
* Chunk Overlap
* Top-K
* Embedding Model
* Groq Model
* ChromaDB Path
* Data Folder

---

## 11. Error Handling

Gracefully handle:

* Missing PDF
* Empty PDF
* Missing API Key
* Corrupted PDF
* Empty Database
* Embedding Errors
* Groq API Errors

Provide meaningful user-friendly messages.

---

## 12. Documentation

Generate:

* README.md
* Installation Guide
* Environment Setup
* Running Instructions
* Architecture Overview
* Folder Explanation
* Troubleshooting Guide

Include comments throughout the code explaining important implementation details.

---

# C — Context

The objective of this project is educational as well as functional.

I want to understand the complete lifecycle of a Retrieval-Augmented Generation (RAG) system, including:

* PDF ingestion
* Text extraction
* Chunking
* Embedding generation
* Vector storage
* Semantic retrieval
* Prompt construction
* Large Language Model integration
* Response generation

The application should also provide visual insights into how chunking and retrieval work, making it easy to debug, learn, and extend.

I will manually place the Product Requirements PDF for **app.vwo.com** inside the **data/** folder.

Later, I will provide the Groq API key, which should be read securely from an environment variable.

---

# E — Expectation

Produce a production-ready solution that is:

* Modular and maintainable
* Well documented
* Beginner-friendly
* Extensible
* Cleanly structured
* Fully commented

The final output should include:

* Complete source code
* Folder structure
* HTML dashboard
* CSS styling
* JavaScript interactions
* Python modules
* Local ChromaDB integration
* Nomic embedding integration
* Groq integration
* README
* requirements.txt
* .env.example

The completed application should clearly demonstrate the entire RAG pipeline from PDF ingestion to final answer generation while visually showing how chunks are stored, retrieved, and used by the LLM.
