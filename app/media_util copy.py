import os
import logging
from moviepy.editor import VideoFileClip

MP3_FORMAT = '.mp3'
MP4_FORMAT = '.mp4'
MEDIA_FILE_STORAGE='media/'



class Media:
  def __init__(self, audio_file):
    self.audio_file = audio_file

  def  convert_mp4_to_mp3(self, filename, file_out_name):
    try:
      video_clip = VideoFileClip(filename)
      audio_clip = video_clip.audio
      audio_clip.write_audiofile(file_out_name, codec='mp3')
    except Exception as e:
        logging.ERROR(f"ERROR to comvert video from mp3 to mp4: {e}")

  def compress_mp3(self):
     filename = self.audio_file.filename,
     self.audio_file.save(filename)
     file_out_name, is_mp4_file = self.is_mp4_file(filename)
     file_out_name = file_out_name + MP3_FORMAT
     if is_mp4_file:
        self.convert_mp4_to_mp3(filename, file_out_name)
     self.limit_size(file_out_name)
     return file_out_name

def is_mp4_file(self, filename):
        file_out_name, extension = os.path.splitext(filename)
        return file_out_name, extension.lower() == MP4_FORMAT

def limit_size(self,file_out_name, max_size_mb=20):
    try:
      original_size_mb = os.path.getsize(file_out_name) / (1024 * 1024)
      reduction_factor = min(1.0, max_size_mb / original_size_mb)
      audio_clip = VideoFileClip(file_out_name)
      audio_clip = audio_clip.subclip(0, audio_clip.duration / reduction_factor)
      audio_clip.write_audiofile(MEDIA_FILE_STORAGE + file_out_name, codec='mp3', bitrate=f'{int(audio_clip.fps * max_size_mb)}k')
    except Exception as e:
      logging.ERROR(f"Error al cargar el archivo de video: {e}")


    def compress_media(self, input_path, max_size_mb=20):
        try:
            audio_clip = AudioFileClip(input_path)
            target_bitrate = int((max_size_mb * 8 * 1024 * 1024) / (audio_clip.duration * 1000))
            compressed_audio_clip = audio_clip.set_bitrate(f'{target_bitrate}k')

            compressed_audio_clip.write_audiofile(output_path, codec='mp3')
            return output_path
        except Exception as e:
            logging.error(f"Error compressing MP3 file: {e}")
            return None
