from flask import Flask, render_template, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from back_end.helpers.extract_patent_id import ExtractPatentId
from back_end.helpers.pdf_merge import PdfMerge
import os, asyncio,glob

app = Flask(__name__)

patent_download_endpoint = Blueprint("patent_download_service", __name__)
patent_download_process_endpoint = Blueprint("patent_download_process_service", __name__)
endpoint = "/patent_download_service"
process_endpoint = "/download_process"

UPLOAD_FOLDER = 'temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = 'temp_data/pdf'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

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
    return render_template('patent_download.html')


@patent_download_process_endpoint.route(process_endpoint, methods=['POST'])
def uploaded_file():
    if request.method == 'POST':
        extract_patentId = ExtractPatentId
        merger = PdfMerge

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
            os.mkdir(DOWNLOAD_FOLDER)

        f = request.files['file']

        if allowed_file(f.filename):

            download = str(DOWNLOAD_FOLDER) + "/" + str(f.filename)[0:-4]
            if not os.path.isdir(download):
                os.mkdir(download)

            if os.listdir(download) != []:
                files = glob.glob(download+'/*')
                for f in files:
                    os.remove(f)

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

            try:
                asyncio.run(merger.runner(file_name=f.filename))
            except Exception as e:
                print(e)

            return jsonify({'success': res})
        else:
            return jsonify({'error': "Wrong file Type!!! Please upload a correct 'csv' file"})
