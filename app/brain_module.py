import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

class ChatGPT:

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
          api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.SPANISH_LANGUAGE="es"
        self.TRANSCRIBE_MODEL="whisper-1"
        self.TEXT_MODEL="gpt-3.5-turbo-1106"
        self.MAIN_ROLE = "Eres un experto en periodismo digital"
        self.RESPONSE_FORMAT={"type": "json_object"}
        self.DEFAULT_PROMPT=f'''
            tu tarea es generar un articulo SEO de minimo 400 palabras y maximo 600,
            un titulo de maximo 100 caracteres, un resumen de 200 caracteres
            y cuatro tags separados por comas basado en el siguiente texto:'''
        self.RESPONSE_OBJECT='''
            retorna un articulo en formato json que contenga los siguientes campos:
                "title": ...
                "sumary": ...
                "tags": ...
                "article": ...
        '''


    def create_transcription(self,temp_filename):

        audio_file= open(temp_filename, "rb")
        transcript = self.client.audio.transcriptions.create(
        model=self.TRANSCRIBE_MODEL,
        file=audio_file,
        language=self.SPANISH_LANGUAGE
        )
        return transcript.text

    def create_article(self, transcription, custom_prompt=None):
        try:
            custom_prompt = custom_prompt if custom_prompt is not None else self.DEFAULT_PROMPT
            prompt = f"""{custom_prompt} ```{transcription}``` ```{self.RESPONSE_OBJECT}```"""
            response = self.client.chat.completions.create(
            messages=[
                    {
                        "role": "system",
                        "content": self.MAIN_ROLE
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.TEXT_MODEL,
                response_format=self.RESPONSE_FORMAT,
            )
            return response.model_dump()['choices'][0]['message']['content']
        except Exception as e:
             logging.error(f"Error creating article: {e}")

