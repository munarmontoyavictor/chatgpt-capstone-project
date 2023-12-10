import os
import logging
from threading import Thread
from brain_module import ChatGPT
from mongo_api import MongoAPI
from media_util import Media
MEDIA_FILE_STORAGE = 'media/'

class TranscribeController:
    def __init__(self, data):
        self.db_api = MongoAPI('transcriptions')
        self.data = data

    def process_media(self):
        logging.error('start')
        filename = self.data['file_name']
        media = Media(filename)
        output_filepath = media.compress_mp3()
        whisper = ChatGPT()
        response = whisper.create_transcription(output_filepath)
        transcription = {'transcription':response}
        self.db_api.update(transcription, self.data['job_id'])
        logging.error('after 15 dddddddddddddddddddddddddddddddddddddddddddddd')
        media.delete_files(output_filepath)

    def save_form(self):
        job_id_obj = self.db_api.save(self.data)
        self.data['job_id'] = job_id_obj
        thread = Thread(target=self.process_media)
        thread.start()
        return str(job_id_obj)

