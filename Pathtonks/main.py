from flask import Flask
from zipfile import ZipFile
import re
import os
import time
import tempfile
from flask import send_file
from flask import request
from flask import render_template

app = Flask(__name__)
from MyAwesomeAdm1nF1les import upload


def zip_create(path):
    # create a ZipFile object
    tempfile.gettempdir()
    zipname = str(time.time())+'_download.zip'
    zip_path = os.path.join(tempfile.gettempdir(), zipname)
    with ZipFile(zip_path, 'w') as zipObj:
        if os.path.isdir(path):
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, os.path.basename(filePath))
        else:
            zipObj.write(path)
    return zip_path

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download")
def download():
    filepath = request.args.get('filepath', default=None, type = str)
    if filepath is None:
        return "missing filepath arg.", 400
    # filepath must not end by 'y' nor '.' to prevent downloading main.py and not end with a / or \ to avoid directory download
    if not re.match(r"[a-zA-Z\./\\]+[^y\\/\s\.]$", filepath):
        return "The given filepath does not end with a valid file name", 400
    filename = os.path.normpath(os.path.basename(filepath))
    if not os.path.exists(filename):
        return "This file does not exist.", 400
    # ZIP IT FOR BAD CONNECTIONS
    zip_path = zip_create(filename)
    return send_file(zip_path)
    

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80, debug=True)