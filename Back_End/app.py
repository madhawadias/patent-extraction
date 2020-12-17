from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

from Back_End.helpers.extractPatentID import ExtractPatentIds

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'temp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        patentIds = ExtractPatentIds(f.filename)
        return jsonify(patentIds)

if __name__ == '__main__':
    app.run(debug=True)
