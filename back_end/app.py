from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

from back_end.helpers.extract_patent_id import ExtractPatentId

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
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
                print(e)

            try:
                patentIds = extract_patentId.runner((f.filename))
            except Exception as e:
                print(e)

            return jsonify(patentIds)
        else:
            return "Wrong file Type!!! Please upload a correct 'csv' file"


if __name__ == '__main__':
    app.run(debug=True)



