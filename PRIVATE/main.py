from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all_chunks
from core.extractor import extract_actionable_items, extract_decisions, extract_questions
from core.summarizer import summarize, generate_title
from core.rag_engine import ask_question, build_rag_chain

load_dotenv(override=True)

def run_the_goated_pipeline(source:str)-> dict:
    print("Starting AI Video Assistant...")
    chunks = process_input(source)
    transcript = transcribe_all_chunks(chunks)
    print("Transcript generated. Building RAG chain...")
    print(f"Transcript preview: {transcript[:500]}")
    title = generate_title(transcript)
    summary = summarize(transcript)
    actionable_items = extract_actionable_items(transcript)
    decisions = extract_decisions(transcript)
    questions = extract_questions(transcript)
    
    rag_chain = build_rag_chain(transcript)
    print("RAG chain built. Asking question...")
    
    return {
        "title": title,
        "summary": summary,
        "actionable_items": actionable_items,
        "decisions": decisions,
        "questions": questions,
        "transcript": transcript,
        "rag_chain": rag_chain
    }
    

if __name__ == "__main__":
    source = input("Enter YouTube URL or local file path: ").strip()
    result = run_the_goated_pipeline(source)
    
    print("\n\n--- Final Result ---")
    print(f"Title: {result['title']}\n")
    print(f"Summary: {result['summary']}\n")
    print(f"Actionable Items: {result['actionable_items']}\n")
    print(f"Decisions: {result['decisions']}\n")
    print(f"Questions: {result['questions']}\n")
    
    print("=======================================")
    
    print("Chat with the RAG engine! Ask any question related to the meeting transcript.\n")
    rag_chain = result['rag_chain']
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        
        answer = ask_question(rag_chain, question)
        print(f"AI: {answer}\n")
        