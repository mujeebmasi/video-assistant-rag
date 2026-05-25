Video Assistant RAG

An AI-powered Retrieval-Augmented Generation (RAG) system designed to process, summarize, and query video content using Large Language Models.

The application extracts transcripts from videos, generates embeddings, stores them in a vector database, and enables semantic search and context-aware Q&A over the video content.

🚀 Features
Video/audio ingestion from YouTube URLs or local files
Automatic transcription using Whisper
AI-generated meeting/video summaries
Extraction of:
Actionable items
Key decisions
Open questions
Transcript chunking and embedding pipeline
Semantic search using vector retrieval
Context-aware Q&A using RAG
Interactive CLI chat with uploaded videos
🛠️ Tech Stack
Backend Framework: FastAPI
AI Orchestration: LangChain
Vector Database: ChromaDB
Transcription Model: OpenAI Whisper
Embeddings: Hugging Face Sentence Transformers
LLM Provider: Mistral AI
Package Management: pip
📋 Prerequisites

Make sure the following are installed:

Python 3.10+
FFmpeg
Git
🔧 Installation & Setup
1. Clone the Repository
git clone https://github.com/mujeebmasi/video-assistant-rag.git
cd video-assistant-rag
2. Create Virtual Environment
python -m venv .venv

Activate it:

Windows
.venv\Scripts\activate
Linux / Mac
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Create .env File

Create a .env file in the project root:

MISTRAL_API_KEY=your_api_key_here
▶️ Run the Application
python main.py

You will be prompted to enter:

a YouTube URL
or a local video/audio file path
📌 Current Workflow
Download/process video audio
Split audio into chunks
Transcribe chunks using Whisper
Generate transcript summary
Extract:
Action items
Decisions
Questions
Store transcript embeddings in vector database
Build RAG pipeline
Chat with the video using semantic retrieval
💬 Example Questions
"What are the main topics discussed?"
"What decisions were made?"
"What actionable items exist?"
"Summarize the discussion about transformers."
"Who mentioned graph attention networks?"
📂 Project Structure
video-assistant-rag/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── downloads/
├── chroma_db/
├── main.py
├── requirements.txt
└── .env
🤝 Contributing

Contributions are welcome.

Fork the repository
Create a feature branch
Commit your changes
Push to your branch
Open a pull request
📄 License

This project is licensed under the MIT License.
