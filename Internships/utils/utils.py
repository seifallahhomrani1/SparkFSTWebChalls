import PyPDF2
import docx
import textract
import os
from werkzeug.utils import secure_filename
from flask import request



UPLOAD_FOLDER = 'uploads'



def is_valid_resume(file):
    allowed_extensions = {'pdf', 'doc', 'docx'}
    allowed_mime_types = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}

    # Check file extension
    if '.' not in file.filename or file.filename.split('.')[-1].lower() not in allowed_extensions:
        return False

    # Check MIME type
    if file.mimetype not in allowed_mime_types:
        return False

    # Perform content check based on file type
    if file.mimetype == 'application/pdf':
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages
            if num_pages < 1:
                return False
        except Exception:
            return False
    elif file.mimetype == 'application/msword':  # DOC file
        try:
            text = textract.process(file)
            if not text:
                return False
        except textract.exceptions.ShellError:
            return False
    elif file.mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # DOCX file
        try:
            doc = docx.Document(file)
            if not any([p.text.strip() for p in doc.paragraphs]):
                return False
        except Exception:
            return False

    return True

def process_uploaded_file(file):
    content_range = request.headers.get('Content-Range')
    if content_range:
        parts = content_range.split(' ')[1].split('/')
        start_byte = int(parts[0].split('-')[0])
        end_byte = int(parts[0].split('-')[1])
        total_bytes = int(parts[1])

        # Read the chunk directly from the 'resume' parameter
        chunk = file.stream.read()

        temp_file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        with open(temp_file_path, 'ab') as f:  # Use 'ab' mode for appending binary data
            f.write(chunk)

        if end_byte + 1 == total_bytes:
            # Rename the temporary file to the actual filename
            final_file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            os.rename(temp_file_path, final_file_path)