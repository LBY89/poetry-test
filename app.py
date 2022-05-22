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
app.config['UPLOAD_FOLDER'] = '/Users/baoying/Desktop/poetry-test/uploads'
CORS(app, expose_headers='Authorization')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/*')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    target = os.path.join(app.config['UPLOAD_FOLDER'])
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("generate view")
    file = request.files['file']
    #global filename
    filename_id = str(uuid.uuid4())
    print('filename',filename_id)
    if allowed_file(file.filename):
        filename_obj = {"id" : filename_id}
        destination = "/".join([target, filename_id])
        file.save(destination)
        session['uploadFilePath'] = destination
        return jsonify(filename_obj)
    else: 
        logging.raiseExceptions
     

@app.route('/view/*', methods=['GET'])
@cross_origin()
def renderFile(file_id):
    
    return toml_parser('uploads/'+file_id)

# @app.route('/*', methods=['GET'])
# @cross_origin()
# def renderFile(file_id):
    
#     return 'try different refresh point'  

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()