import sys
import os
import subprocess
import shelve
from web_app import settings


def download_dependences():
    console = 'pip install -r requirements.txt'
    process = subprocess.Popen(console,stderr=subprocess.PIPE)
    output = process.communicate()
    if process.returncode > 1:
        print ("Failed to install dependencies")
        print (output[1])
        sys.exit(1)


def initialize_env():
    #create directory
    if not os.path.exists(settings.STORAGE_DIR):
        os.mkdir(settings.STORAGE_DIR)
    storage_db = shelve.open(settings.DB_FILE)
    storage_db.close()

def run_application():
    from web_app import application
    application.app.run()

if __name__ == "__main__":
    download_dependences()
    initialize_env()
    run_application()
