import os
import logging
from moviepy.editor import VideoFileClip, AudioFileClip

MP3_FORMAT = '.mp3'
MP4_FORMAT = '.mp4'
UPLOAD_FOLDER = 'uploads/'
COMPRESS_PREFIX = 'compress_'
class Media:
    def __init__(self, filename):
        self.filename = filename

    def compress_mp3(self):
        try:
            output_filepath = self.convert_to_mp3()
            return output_filepath
        except Exception as e:
            logging.error(f"Error in compress_mp3: {e}")
            return None

    def convert_mp4_to_mp3(self, input_filename, output_filename):
        try:
            video_clip = VideoFileClip(input_filename)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(output_filename, codec='mp3')
            return True
        except Exception as e:
            logging.error(f"Error converting {input_filename} to MP3: {e}")
            return False

    def convert_to_mp3(self):
        try:
            output_filename, extension = os.path.splitext(self.filename)
            input_filepath = os.path.join(UPLOAD_FOLDER, self.filename)
            if extension.lower() == MP3_FORMAT:
                return input_filepath
            output_filename += MP3_FORMAT
            output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)
            success = self.convert_mp4_to_mp3(input_filepath, output_filepath)
            if not success:
                logging.error(f"Conversion failed for {self.filename}")
                return None
            return output_filepath
        except Exception as e:
            logging.error(f"Error handling file: {e}")
            return None

    def limit_size(self, input_path, max_size_mb=20):
        try:
            output_path = os.path.join(os.path.dirname(input_path), f"{COMPRESS_PREFIX}{os.path.basename(input_path)}")
            original_size_mb = os.path.getsize(input_path) / (1024 * 1024)
            reduction_factor = min(1.0, max_size_mb / original_size_mb)
            audio_clip = AudioFileClip(input_path)
            audio_clip = audio_clip.subclip(0, audio_clip.duration / reduction_factor)
            audio_clip.write_audiofile(output_path, codec='mp3', bitrate=f'{int(audio_clip.fps * max_size_mb)}k')
            return output_path
        except Exception as e:
            logging.error(f"Error limiting size of audio file: {e}")
            return None

    def delete_files(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            original_audio_path = file_path.replace(COMPRESS_PREFIX, "")
            if os.path.exists(original_audio_path):
                os.remove(original_audio_path)

            mp4_path = os.path.splitext(original_audio_path)[0] + MP4_FORMAT
            if os.path.exists(mp4_path):
                os.remove(mp4_path)

            mp3_path = os.path.splitext(original_audio_path)[0] + MP3_FORMAT
            if os.path.exists(mp3_path):
                os.remove(mp3_path)

            return True
        except Exception as e:
            logging.error(f"Error deleting files: {e}")
            return False
