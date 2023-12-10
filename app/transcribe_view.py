import os
from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from transcribe_controller import TranscribeController
from werkzeug.utils import secure_filename

transcribe_controller_blueprint = Blueprint('transcribe_controller', __name__)
UPLOAD_FOLDER = 'uploads/'


@transcribe_controller_blueprint.route('/')
def root():
    return redirect(url_for('transcribe_controller.transcribe_form'))

@transcribe_controller_blueprint.route('/transcribe', methods=['GET'])
def transcribe_form():
    return render_template('transcribe.html')

@transcribe_controller_blueprint.route('/transcribe', methods=['POST'])
def transcribe_process_form():
    audio_file = request.files['audioFile']
    filename = secure_filename(audio_file.filename)
    input_filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(input_filepath)
    source_language = request.form['sourceLanguage']
    translate_to_spanish = 'translate' in request.form
    prompt = request.form['prompt']


    form_data = {
        'file_name': filename,
        'source_language': source_language,
        'translate_to_spanish': translate_to_spanish,
        'prompt': prompt
    }
    transcribe_controller = TranscribeController(form_data)
    db_id = transcribe_controller.save_form()
    return render_template('transcribe.html', message=db_id)

@transcribe_controller_blueprint.route("/api/transcribe", methods=['GET'])
def get_transcriptions():
    transcribe_controller = TranscribeController()
    data = transcribe_controller.get_transcriptions()
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:80")
    return response

@transcribe_controller_blueprint.route("/api/transcribe/<job_id>", methods=['GET'])
def get_transcription_by_id(job_id):
    transcribe_controller = TranscribeController()
    data = transcribe_controller.get_transcription_by_id(job_id)
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:80")
    return response
