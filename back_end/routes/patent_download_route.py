from flask import Flask, render_template, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from back_end.helpers.extract_patent_id import ExtractPatentId
import os, asyncio

app = Flask(__name__)

patent_download_endpoint = Blueprint("patent_download_service", __name__)
patent_download_process_endpoint = Blueprint("patent_download_process_service", __name__)
endpoint = "/patent_download_service"
process_endpoint = "/download_process"

UPLOAD_FOLDER = 'temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])

getReq = ''
state = ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getState():
    global getReq
    global state
    if getReq == "2":
        getReq = ''

    return state


@patent_download_endpoint.route(endpoint, methods=['GET', 'POST'])
def get_patent_search():
    # if request.method == 'POST':
    #     getReq = "1"
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
    #             state = str(e)
    #             print(e)
    #
    #         try:
    #             state = "Downloading"
    #             res = asyncio.run(extract_patentId.runner(file_name=f.filename))
    #         except Exception as e:
    #             state = str(e)
    #             print(e)
    #         getReq = "2"
    #         state = jsonify(res)
    #     else:
    #         state = "Wrong file Type!!! Please upload a correct 'csv' file"

    return render_template('patent_download.html')


@patent_download_process_endpoint.route(process_endpoint, methods=['POST'])
def uploaded_file():
    if request.method == 'POST':
        extract_patentId = ExtractPatentId

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        f = request.files['file']

        if allowed_file(f.filename):
            try:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            except Exception as e:
                return jsonify({'error': str(e)})
                print(e)

            try:
                res = asyncio.run(extract_patentId.runner(file_name=f.filename))
                if type(res) is list:
                    global text
                    text = "Following file(s) were skiped : "
                    if len(res) == 1:
                        text = text + str(res[0]) + ","
                    else:
                        for skip in res:
                            text = text + str(skip) + ","
                    res = text[:-1]
            except Exception as e:
                return jsonify({'error': str(e)})
                print(e)
            return jsonify({'success': res})
        else:
            return jsonify({'error': "Wrong file Type!!! Please upload a correct 'csv' file"})
