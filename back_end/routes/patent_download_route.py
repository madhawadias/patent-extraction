from flask import Flask, render_template, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from back_end.helpers.extract_patent_id import ExtractPatentId
import os, asyncio, time

app = Flask(__name__)

patent_download_endpoint = Blueprint("patent_download_service", __name__)
patent_download_process_endpoint = Blueprint("patent_download_process_service", __name__)
endpoint = "/patent_download_service"
process_endpoint = "/download_process"

UPLOAD_FOLDER = 'temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])

exporting_threads = {}
getReq = ''
state = ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getState():
    global state
    return state

@patent_download_endpoint.route(endpoint, methods=['GET', 'POST'])
def get_patent_search():
    global getReq
    global state

    if request.method == 'POST':
        getReq = "1"
        extract_patentId = ExtractPatentId

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        f = request.files['file']

        if allowed_file(f.filename):
            try:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            except Exception as e:
                state = str(e)
                print(e)

            try:
                state = "Downloading"
                patentIds = asyncio.run(extract_patentId.runner(file_name=f.filename))
            except Exception as e:
                state = str(e)
                print(e)
            state = jsonify(patentIds)
        else:
            state = "Wrong file Type!!! Please upload a correct 'csv' file"

    return render_template('patent_download.html', getReq=getReq)


@patent_download_process_endpoint.route(process_endpoint, methods=['GET', 'POST'])
def uploaded_file():
    global state
    return str(state)

    # if request.method == 'POST':
    #     extract_patentId = ExtractPatentId
    #
    #     if not os.path.isdir(UPLOAD_FOLDER):
    #         os.mkdir(UPLOAD_FOLDER)
    #
    #     f = request.files['file']
    #
    #     if allowed_file(f.filename):
    #         try:
    #             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             patentIds = asyncio.run(extract_patentId.runner(file_name=f.filename))
    #         except Exception as e:
    #             print(e)
    #
    #         return jsonify(patentIds)
    #     else:
    #         return "Wrong file Type!!! Please upload a correct 'csv' file"
