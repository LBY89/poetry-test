import uuid 
from flask import jsonify
import os
from flask import Flask, request, send_from_directory, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from parser import toml_parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Upload lock file')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'lock', 'py'}

app = Flask(__name__, static_folder='poetry-lock-client/build', static_url_path='')

CORS(app, expose_headers='Authorization')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def page_not_found(e):
    return serve()

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    file = request.files['file']
    if allowed_file(file.filename):
        return toml_parser(file.read())
    else: 
        logging.raiseExceptions
    


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()