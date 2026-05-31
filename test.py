from utils.audio_processor import process_input
from core.transcriber import transcribe_all_chunks

source = "https://www.youtube.com/watch?v=BedAaB1RKgE"

chunks = process_input(source)
print("Transcribing Started...")
print(transcribe_all_chunks(chunks))
