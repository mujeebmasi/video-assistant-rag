<<<<<<< HEAD
# Video Assistant RAG.

An AI-powered Retrieval-Augmented Generation (RAG) backend designed to ingest, process, and query video content. This system extracts transcripts and multimodal contextual data from videos, stores them as vector embeddings, and enables users to perform intelligent semantic searches and context-aware Q&A over video archives.

Built with a high-performance backend stack optimized for scalability, speed, and seamless AI integration.

---

## 🚀 Features

* **Video Data Ingestion**: Extracts audio, metadata, and high-quality transcripts from uploaded video files or external links.
* **Chunking & Embedding Pipeline**: Intelligently segments transcripts and generates vector embeddings optimized for semantic retrieval.
* **Vector Search Engine**: Leverages highly efficient semantic retrieval to match user queries with the most relevant timestamps and context within the video.
* **Context-Aware Q&A**: Integrates with Large Language Models (LLMs) to synthesize precise answers grounded strictly in the video’s actual content.
* **Asynchronous Task Processing**: Designed to handle long-running video processing pipelines efficiently without blocking the core API.

---

## 🛠️ Tech Stack

* **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous, high-performance Python framework)
* **Database**: [PostgreSQL](https://www.postgresql.org/) with `pgvector` for relational data storage and native vector similarity search.
* **RAG & AI Orchestration**: [LangChain](https://www.langchain.com/) / [LlamaIndex](https://www.llamaindex.ai/) 
* **Embeddings & LLM**: Mistral API / Google Gemini API / HuggingFace Local Models
* **Package Management**: `pip` / `poetry`

---

## 📋 Prerequisites

Ensure you have the following installed on your local development machine:

* Python 3.10 or higher
* PostgreSQL (with the `pgvector` extension enabled)
* FFmpeg (required for processing audio/video streams)

=======
# AI Meeting Assistant

This workspace now has a simple React frontend and a FastAPI backend.

## What is where
- `frontend/` - React UI built with Vite
- `backend/` - FastAPI API that runs the existing transcript pipeline
- `PRIVATE/` - snapshot of the old Python app and Streamlit version so you can still inspect the original code

## Run the backend
1. Install Python dependencies from `requirements.txt`
2. Start the API server:

```bash
uvicorn backend.app:app --reload
```

## Run the frontend
1. Go into `frontend/`
2. Install Node dependencies:

```bash
npm install
```

3. Start the React app:

```bash
npm run dev
```

## How it works
- The frontend sends a YouTube link, local path, or uploaded file to FastAPI.
- FastAPI reuses the existing `core/` pipeline to transcribe, summarize, and build the RAG chain.
- Chat questions go back to the backend, which answers using the stored RAG session.
>>>>>>> cbc03fc (fixed vector store in github)
