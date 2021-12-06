from __main__ import app
from flask import render_template, request
import os

@app.route("/AwesomeAdm1nR0ute/upload")
def upload():
    return render_template('upload.html')

@app.route('/AwesomeAdm1nR0ute/uploader', methods = ['POST'])
def upload_file():
     secret = request.form.get('secret', default=None, type = str)
     if secret is None:
          return "Missing a secret.", 400
     if secret != 'MYAWESOME_S3cret_Is_Secure!':
          return "Invalid secret value.", 503
     dir_path = os.path.dirname(os.path.realpath(__file__))
     upload_dir = "../uploads"
     f = request.files['file']
     filename = f.filename.replace("..","_").strip()
     if filename == "":
          return "Empty filename provided", 400
     full_path = os.path.join(dir_path, upload_dir, filename)
     f.save(full_path)
     return 'file uploaded successfully in '+full_path