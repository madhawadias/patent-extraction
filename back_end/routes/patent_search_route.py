import asyncio
import glob
import os

from flask import Flask, render_template, request, jsonify, Blueprint

from back_end.helpers.extract_patent_id import ExtractPatentId
from back_end.helpers.patent_details import PatentExtract
from back_end.helpers.pdf_merge import PdfMerge
from back_end.helpers.send_mail import SendMail

app = Flask(__name__)

patent_search_endpoint = Blueprint("patent_search_service", __name__)
patent_search_process_endpoint = Blueprint("patent_search_process_service", __name__)
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
    count = request.form['count']
    if not count:
        count = 50
    else:
        count = int(count)

    if text:

        try:
            extract_patentId = ExtractPatentId()
            merger = PdfMerge()
            send_mail = SendMail()

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
                os.mkdir(DOWNLOAD_FOLDER)

            if not os.path.isdir(DOWNLOAD_FOLDER):
                os.mkdir(DOWNLOAD_FOLDER)

            patent_extract_class = PatentExtract()
            patent_extract_class.search_by_examiner(text=text)
            filename = patent_extract_class.extract_patent_details(text=text)
            print(filename)

            download = str(DOWNLOAD_FOLDER) + "/" + str(filename)[0:-4]
            if not os.path.isdir(download):
                os.mkdir(download)

            final_download = str(DOWNLOAD_FOLDER) + "/" + str(filename)[0:-4]+"/result"
            if not os.path.isdir(final_download):
                os.mkdir(final_download)

            if os.listdir(final_download) != []:
                files = glob.glob(final_download + '/*')
                for f in files:
                    os.remove(f)

            a_download = str(DOWNLOAD_FOLDER) + "/" + str(filename)[0:-4] + "/1"
            if not os.path.isdir(a_download):
                os.mkdir(a_download)

            if os.listdir(a_download) != []:
                files = glob.glob(a_download + '/*')
                for f in files:
                    os.remove(f)

            b_download = str(DOWNLOAD_FOLDER) + "/" + str(filename)[0:-4] + "/2"
            if not os.path.isdir(b_download):
                os.mkdir(b_download)

            if os.listdir(b_download) != []:
                files = glob.glob(b_download + '/*')
                for f in files:
                    os.remove(f)

            try:
                res = asyncio.run(extract_patentId.runner(file_name=filename,count=count,b_download_path=b_download))
                S3_BASE_URL = "https://patents-jerry.s3.us-east-2.amazonaws.com/{}.pdf".format(filename[:-4])
                if type(res) is list:
                    global skip_text
                    skip_text = "Following file(s) were skiped : "
                    if len(res) == 1:
                        skip_text = skip_text + str(res[0]) + ","
                    else:
                        for skip in res:
                            skip_text = skip_text + str(skip) + ","
                    res = skip_text[:-1] + " and" + " Get your file from here: " + S3_BASE_URL
            except Exception as e:
                print(e)
                return jsonify({'error': str(e)})



            if os.listdir(a_download):
                try:
                    asyncio.run(merger.runner(file_name=filename,folder_name="1"))
                except Exception as e:
                    print(e)

            if os.listdir(b_download):
                try:
                    asyncio.run(merger.runner(file_name=filename,folder_name="2"))
                except Exception as e:
                    print(e)

            if os.listdir(final_download):
                try:
                    asyncio.run(merger.runner(file_name=filename,folder_name="result"))
                except Exception as e:
                    print(e)

                send_mail.runner(file_url=S3_BASE_URL, file_name=text)
            else:
                res = "No files available for your search"

            return jsonify({'name': res})

        except Exception as e:
            print(e)
            return jsonify({'error': 'System Error ! , please try again'})

    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=True)
