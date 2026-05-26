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

