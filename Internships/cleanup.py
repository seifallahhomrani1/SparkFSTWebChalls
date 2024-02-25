import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

UPLOADS_FOLDER = 'uploads'
MAX_FILES = 20

def cleanup_uploads_folder():
    file_count = len(os.listdir(UPLOADS_FOLDER))
    if file_count > MAX_FILES:
        files = sorted(os.listdir(UPLOADS_FOLDER), key=lambda x: os.path.getctime(os.path.join(UPLOADS_FOLDER, x)))
        for file in files[:file_count - MAX_FILES]:
            os.remove(os.path.join(UPLOADS_FOLDER, file))

# Create and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_uploads_folder, 'interval', minutes=5) 
scheduler.start()

# Make sure the scheduler shuts down when the app is exiting
atexit.register(lambda: scheduler.shutdown())
