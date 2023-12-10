import os
from openai import OpenAI
from dotenv import load_dotenv

class ChatGPT:

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
          api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.MAIN_ROLE = "This is the behavior of chatGPT"

    def create_transcription(self,temp_filename):

        audio_file= open(temp_filename, "rb")
        transcript = self.client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="es"
        )
        return transcript.text


    def request_openai(self, message, role="system"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": role, "content": message}]
        )
        return response["choices"][0]["message"]["content"]

