# Video Assistant RAG

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
* **Embeddings & LLM**: OpenAI API / Google Gemini API / HuggingFace Local Models
* **Package Management**: `pip` / `poetry`

---

## 📋 Prerequisites

Ensure you have the following installed on your local development machine:

* Python 3.10 or higher
* PostgreSQL (with the `pgvector` extension enabled)
* FFmpeg (required for processing audio/video streams)

---
Set Up a Virtual Environment

Bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install Dependencies

Bash
pip install -r requirements.txt
Environment Configuration Create a .env file in the root directory and configure your environment variables:

Code snippet
# Server Configuration
PORT=8000
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/video_rag_db

# AI / LLM Provider Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
Database Initialization Ensure your PostgreSQL instance is running and has the pgvector extension active. Run your migrations or database setup scripts:

Bash
# Example if using Alembic for migrations
alembic upgrade head
🏃 Run the Application
Start the Uvicorn development server:

Bash
uvicorn app.main:app --reload
The server will be accessible at http://127.0.0.1:8000.

You can view the interactive Swagger API documentation at http://127.0.0.1:8000/docs.

📌 API Architecture Reference
Below is the standard workflow for processing a video and querying its contents:

POST /api/v1/videos/process Accepts a video file or external URL, extracts transcripts, chunks the text, and commits the generated vector embeddings to PostgreSQL.

POST /api/v1/query Takes a user query, performs a similarity search over the video chunks via pgvector, injects the relevant context into the prompt template, and returns the LLM-generated answer alongside source timestamps.

🤝 Contributing
Contributions are welcome! If you want to improve the chunking strategy, optimize vector retrieval, or add frontend support:

Fork the repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
