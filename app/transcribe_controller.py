import logging
from threading import Thread
from brain_module import ChatGPT
from mongo_api import MongoAPI
from media_util import Media
import json
MEDIA_FILE_STORAGE = 'media/'

class TranscribeController:
    def __init__(self, data=None):
        self.db_api = MongoAPI('transcriptions')
        self.data = data

    def process_media(self):
        try:
            filename = self.data['file_name']
            media = Media(filename)
            output_filepath = media.compress_mp3()
            whisper = ChatGPT()
            text_transcription = whisper.create_transcription(output_filepath)
            article_obj= whisper.create_article(text_transcription)
            json_dict = json.loads(article_obj)
            json_dict['transcription'] = text_transcription
            self.db_api.update(json_dict, self.data['job_id'])
            media.delete_files(output_filepath)
        except Exception as e:
             logging.error(f"Error processing media: {e}")



    def save_form(self):
        job_id_obj = self.db_api.save(self.data)
        self.data['job_id'] = job_id_obj
        thread = Thread(target=self.process_media)
        thread.start()
        return str(job_id_obj)

    def get_transcriptions(self):
        return self.db_api.get_all()

    def get_transcription_by_id(self, job_id):
        return self.db_api.get_by_id(job_id)

