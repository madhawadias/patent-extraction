from flask import Flask, render_template, request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from back_end.helpers.patent_details import PatentExtract
# from back_end.helpers.patent_pdf_details_merge_app import ExtractPatentId
from back_end.helpers.extract_patent_id import ExtractPatentId
from back_end.helpers.pdf_merge import PdfMerge
import os, asyncio,glob

app = Flask(__name__)

patent_search_endpoint = Blueprint("patent_search_service", __name__)
patent_search_process_endpoint = Blueprint("patent_search_process_service",__name__)
endpoint = "/patent_search_service"
process_endpoint = "/process"

UPLOAD_FOLDER = 'back_end/temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DOWNLOAD_FOLDER = 'back_end/temp_data/pdf'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@patent_search_endpoint.route(endpoint, methods=['GET', 'POST'])
def get_patent_search():
    return render_template('patent_search.html')


# @app.route('/')
# def index():
# 	return render_template('index.html')

@patent_search_process_endpoint.route(process_endpoint, methods=['POST'])
def process():
    text = request.form['name']

    if text:

        try:
            extract_patentId = ExtractPatentId
            merger = PdfMerge

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
                os.mkdir(DOWNLOAD_FOLDER)

            patent_extract_class = PatentExtract()
            patent_extract_class.search_by_examiner(text=text)
            filename = patent_extract_class.extract_patent_details(text=text)
            print(filename)

            download = str(DOWNLOAD_FOLDER) + "/" + str(filename)[0:-4]
            if not os.path.isdir(download):
                os.mkdir(download)

            if os.listdir(download) != []:
                files = glob.glob(download + '/*')
                for f in files:
                    os.remove(f)

            try:
                res = asyncio.run(extract_patentId.runner(file_name=filename))
                if type(res) is list:
                    global skip_text
                    skip_text = "Following file(s) were skiped : "
                    if len(res) == 1:
                        skip_text = skip_text + str(res[0]) + ","
                    else:
                        for skip in res:
                            skip_text = skip_text + str(skip) + ","
                    res = skip_text[:-1]
            except Exception as e:
                return jsonify({'error': str(e)})
                print(e)

            try:
                asyncio.run(merger.runner(file_name=filename))
            except Exception as e:
                print(e)

            return jsonify({'name': res})

            # patent_download_class = ExtractPatentId()
            # patent_download_class.download_pdf(file_name=filename)
            # newName = text
            # return jsonify({'name': 'author ' + newName + ' details has been downlaoded'})
        except Exception as e:
            print(e)
            return jsonify({'error': 'System Error ! , please try again'})



    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=True)
