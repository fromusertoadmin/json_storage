from flask import Response
from flask import request
from flask import url_for, redirect, send_from_directory, send_file
import shelve
import json
import os
import zipfile

from web_app import settings


def get_project_info():
    response_text = "<b>Hi. You start your first programm.</b>"
    return Response(response=response_text,
                    status=200)


def get_storage_stat():
    db_file = shelve.open(settings.DB_FILE)
    result = []
    for key,value in db_file.items():
        result.append({key:value})
    db_file.close()
    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


def download_file(tag):
    db_file = shelve.open(settings.DB_FILE)
    files = db_file[tag]
    db_file.close()
    zip_archive_name = '{0}.zip'.format(tag)
    zip_archive_path = os.path.join(settings.STORAGE_DIR, zip_archive_name)
    zipf = zipfile.ZipFile(zip_archive_path, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zipf.write(os.path.join(settings.STORAGE_DIR, file))
    zipf.close()
    return send_file(zip_archive_path, mimetype = 'zip', attachment_filename  = zip_archive_name,
                                            as_attachment = True)


def upload_files(tag):
    db_file = shelve.open(settings.DB_FILE)
    if db_file.get(tag):
        return Response("Tag is already exist in Database, input another tag", status = 401)
    db_file.close()
    save(request, tag)
    return Response(response="Uploaded", status = 200)


def update_file(tag):
    save(request, tag)
    return Response(response="Files taged = {} were updated".format(tag), status = 200)

def save (request, tag):
    for file_name, file_obj in request.files.items():
        file_obj.save(os.path.join(settings.STORAGE_DIR, file_name))
    db_file = shelve.open(settings.DB_FILE)
    db_file[tag] = list(request.files.keys())
    db_file.close()
