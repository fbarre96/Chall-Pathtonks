from __main__ import app
from flask import render_template, request
import os

# No one will be able to guess these routes and the secret
@app.route("/AwesomeAdm1nR0ute/upload")
def upload():
    return render_template('upload.html')

@app.route('/AwesomeAdm1nR0ute/uploader', methods = ['POST'])
def upload_file():
     secret = request.form.get('secret', default=None, type = str)
     if secret is None:
          return render_template("400.html", e= "Missing a secret."), 400
     if secret != 'MYAWESOME_S3cret_Is_Secure!':
          return render_template("400.html", e= "Invalid secret value."), 400
     dir_path = os.path.dirname(os.path.realpath(__file__))
     upload_dir = "../uploads"
     f = request.files['file']
     filename = f.filename.replace("..","_").strip()
     if filename == "":
          return render_template("400.html", e= "Empty filename provided"), 400
     full_path = os.path.join(dir_path, upload_dir, filename)
     if dir_path not in full_path:
          return render_template("400.html", e= "Restricted to "+dir_path), 400
     if "main.py" in filename or "upload.py"  in filename:
          return render_template("400.html", e= "I dunno how but you should not be able to replace those."), 400
     f.save(full_path)
     return 'file uploaded successfully in '+full_path