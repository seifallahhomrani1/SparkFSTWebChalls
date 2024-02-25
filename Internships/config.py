# config.py

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
ALLOWED_MIME_TYPES = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
CUSTOM_TEMPLATES_DIR = 'templates/custom'
ALLOWED_INTERNAL_IPS = {'127.0.0.1', '192.168.1.1'}
MAX_FILE_SIZE = 2 * 1024 * 1024