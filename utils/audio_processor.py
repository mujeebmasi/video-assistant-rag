import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_yt_audio(url:str)-> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s") # ex: Team Meeting --> team_meeting.mp4 (ext-->extension)

    ydl_opts = {
        'format': 'bestaudio/best',

        'outtmpl': output_path,

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],

        "quiet": True, #quite =true --> to avoid printing logs(mostly the downloading bars ) in the console
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        filename = (
            ydl.prepare_filename(info)
            .replace(".webm", ".wav")
            .replace(".m4a", ".wav")
            .replace(".mp4", ".wav")
        )

    return filename


def convert_to_wav(input_file:str)-> str:
    output_path = os.path.splitext(input_file)[0] + "_converted.wav"  # ex: team_meeting.wav --> team_meeting_converted.wav
    audio = AudioSegment.from_file(input_file)  # Load the audio file using pydub
    audio = audio.set_channels(1).set_frame_rate(16000)  #channels(1)-->mono, frame_rate(16000)-->16kHz which is sweeetspot for whisper
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path:str, chunk_length_mins:int=10)-> list:  #each chunk will be of 10 mins
    audio = AudioSegment.from_wav(wav_path)  # Load the WAV file using pydub
    chunk_ms = chunk_length_mins * 60 * 1000
    chunks = []

    chunk_number = 1

    for i in range(0, len(audio), chunk_ms):  #start-0 end-len step:chunk_ms
        chunk = audio[i:i+chunk_ms]
        chunk_path = f"{wav_path}_chunk_{chunk_number}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
        chunk_number += 1
    return chunks


def process_input(source:str)-> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube URL, Downloading audio...")
        wav_path = download_yt_audio(source)
    else:
        print("Detected local file, converting to WAV...")
        wav_path = convert_to_wav(source)
    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio processed into {len(chunks)} chunks.")
    return chunks