import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

model = None
def load_model():
    global model       #whatever changes made to model here, will be globally effected
    if model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...")
        model = whisper.load_model(WHISPER_MODEL)
        print("Model loaded successfully.")
    return model

def transcribe_chunk(chunk_path:str, translate:bool = False)-> str:
    model = load_model()
    task = "translate" if translate else "transcribe"  #if translate is true, return "translate" else "transcribe"
    result = model.transcribe(chunk_path, task=task)
    return result["text"]

def transcribe_all_chunks(chunks:list, translate:bool = False)-> str:
    full_transcription = ""
    chunk_number = 1
    for chunk in chunks:
        print(f"Transcribing chunk: {chunk_number}...")
        text = transcribe_chunk(chunk, translate)
        full_transcription += text + "\n"
        print(f"Transcription for {chunk}:\n{text}\n")
        chunk_number = chunk_number + 1
    return full_transcription