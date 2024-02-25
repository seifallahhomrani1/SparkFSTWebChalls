from flask import Flask, render_template, request, jsonify, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
from utils.utils import is_valid_resume, process_uploaded_file
from cleanup import scheduler
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, CUSTOM_TEMPLATES_DIR, ALLOWED_INTERNAL_IPS,MAX_FILE_SIZE
import os
import requests
import re



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_internal_request():
    return request.remote_addr in ALLOWED_INTERNAL_IPS

def load_custom_template(page):
    try:
        template = open(os.path.join(CUSTOM_TEMPLATES_DIR, page)).read()
    except Exception as e:
        template = str(e)
    return template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>', methods=['GET'])
def get_upload(filename):
    if not is_internal_request():
        # i smell a rat 
        return jsonify({'error': 'Access denied'}), 403
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload():


    if 'resume' in request.files:
        # Local file upload
        file = request.files['resume']
        cover_letter = request.form.get('cover-letter')
        internship_subject = request.form.get('internship-subject')

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File size exceeds the maximum allowed size'}), 400
        if file:
            process_uploaded_file(file)
        if not re.match(r'^[a-zA-Z0-9/.]+$', internship_subject):
            return jsonify({'error': 'Invalid characters in internship subject'}), 400
        if allowed_file(file.filename):
            if not is_valid_resume(file):
                return jsonify({'error': 'Invalid resume content'}), 400
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            custom_template = load_custom_template(internship_subject + '.html')
            return render_template_string(custom_template, cover_letter=cover_letter, resume_path=file_path)

        return jsonify({'error': 'Invalid file extension'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0")
