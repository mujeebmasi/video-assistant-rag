# AI Meeting Assistant

Turn a YouTube link, an uploaded recording, or a local media file into a
transcript, a summary, action items, decisions, open questions, and a chatbot
you can ask questions about the conversation.

## How it works

1. `utils/audio_processor.py` downloads the audio with `yt-dlp` (or converts a
   local file), resamples it to mono 16 kHz, and splits it into 10-minute chunks.
2. `core/transcriber.py` runs OpenAI Whisper locally over each chunk.
3. `core/summarizer.py` summarizes the transcript map-reduce style: summarize
   each chunk, then combine those partial summaries into one.
4. `core/extractor.py` pulls out action items, decisions, and open questions.
5. `core/vector_store.py` splits the transcript into 500-character chunks,
   embeds them with a local HuggingFace model, and stores them in Chroma.
6. `core/rag_engine.py` retrieves the 5 most relevant chunks for a question and
   asks Mistral to answer using only those.

Each analysed video gets its own Chroma collection, so chunks from one video
never leak into answers about another.

## Tech stack

- **Transcription**: OpenAI Whisper (runs locally, no API needed)
- **LLM**: Mistral (`mistral-small-latest`) via LangChain
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`, run locally
- **Vector store**: Chroma, persisted to `vector_db/`
- **API**: FastAPI
- **Frontend**: React with Vite
- **Also included**: a Streamlit version in `app.py`, and a CLI in `main.py`

## What is where

- `core/` - transcription, summarizing, extraction, vector store, RAG chain
- `utils/` - audio download and preprocessing
- `backend/` - FastAPI API wrapping the pipeline
- `frontend/` - React UI
- `main.py` - command line version
- `app.py` - Streamlit version

## Prerequisites

- Python 3.10 or higher
- FFmpeg on your PATH (Whisper and pydub both need it)
- Node.js 18 or higher, for the frontend

## Setup

Create a `.env` file in the project root:

```
MISTRAL_API_KEY=your_key_here
```

Optional settings:

- `WHISPER_MODEL` - Whisper size to load, defaults to `small`
- `USE_CUDA` - set to `true` to run embeddings on a GPU

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn backend.app:app --reload
```

Endpoints:

- `GET /health`
- `POST /analyze` - form fields `source_type` (`url`, `upload`, or `local`),
  `source_value`, and an optional `file`. Returns a `session_id` plus the
  transcript, summary, and extracted items.
- `POST /chat/{session_id}` - JSON body `{"question": "..."}`
- `DELETE /chat/{session_id}` - drop the session

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

## Run without the API

Command line:

```bash
python main.py
```

Streamlit:

```bash
streamlit run app.py
```

## Note on chat sessions

The API keeps RAG chains in a plain dictionary in memory, so sessions are lost
when the server restarts. That is fine for local use; a real deployment would
store the collection name and rebuild the chain on demand.
