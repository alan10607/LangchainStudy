from openai import OpenAI
from pathlib import Path
from pytube import YouTube
# from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()

url = ""

# 建立 YouTube 物件
yt = YouTube(url)

# 取得影片的音軌
audio_stream = yt.streams.filter(only_audio=True).first()
speech_file_path = Path(__file__).parent
# 下載音軌到指定的路徑
audio_stream.download(output_path=speech_file_path, filename="audio.mp3")
audio_file_path = speech_file_path / "audio.mp3"
# # 讀取下載下來的音檔
# audio_file = AudioSegment.from_file(audio_file_path)

# # 切割音檔成多個小檔案
# chunk_size = 100 * 1000  # 100 秒
# chunks = [audio_file[i:i+chunk_size] for i in range(0, len(audio_file), chunk_size)]

# # 使用 OpenAI 的 Audio API 將每個小檔案轉成文字，然後合併在一起
# client = OpenAI()
# transcript = ""
# for chunk in chunks:
#     with chunk.export("temp.wav", format="wav") as f:
#         result = client.Audio.transcribe("whisper-1", f)
#         transcript += result["text"]
client = OpenAI()
speech_file_path = Path(__file__).parent / "audio.mp3"
audio_file= open(speech_file_path, "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file

)
print(transcript)
# 印出轉換後的文字
print(transcript)

# client = OpenAI()
# speech_file_path = Path(__file__).parent / "test.mp3"
# audio_file= open(speech_file_path, "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file
# )
# print(transcript)