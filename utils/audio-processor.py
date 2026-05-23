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
        "quiet": True, #quite =true --> to avoid printing logs(mostly the downloading bars  ) in the console
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = (
            ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav").replace(".mp4", ".wav")
)
    return filename

data = download_yt_audio("http://youtube.com/watch?v=8FK6qjb2StM")


def convert_to_wav(input_file:str)-> str:
    output_path = os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path

converted_to_wavdata = convert_to_wav(data)

def chunk_audio(wav_path:str, chunk_length_mins:int=10)-> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_length_mins * 60 * 1000
    
    chunks = []
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i+chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

res = chunk_audio(converted_to_wavdata)
print(res)