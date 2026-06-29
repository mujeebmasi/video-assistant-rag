from core.extractor import extract_actionable_items, extract_decisions, extract_questions
from core.rag_engine import build_rag_chain
from core.summarizer import generate_title, summarize
from core.transcriber import transcribe_all_chunks
from utils.audio_processor import process_input


def run_analysis(source: str) -> dict:
    chunks = process_input(source)
    transcript = transcribe_all_chunks(chunks)
    title = generate_title(transcript)
    summary = summarize(transcript)
    actionable_items = extract_actionable_items(transcript)
    decisions = extract_decisions(transcript)
    questions = extract_questions(transcript)
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "summary": summary,
        "actionable_items": actionable_items,
        "decisions": decisions,
        "questions": questions,
        "transcript": transcript,
        "rag_chain": rag_chain,
    }
