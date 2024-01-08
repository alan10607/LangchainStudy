from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

speech_file_path = Path(__file__).parent / "speech2.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input='我可以講中文嗎.'
)

response.stream_to_file(speech_file_path)