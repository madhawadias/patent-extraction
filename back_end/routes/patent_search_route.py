from flask import Flask, render_template, request, jsonify, Blueprint
from back_end.helpers.patent_details import PatentExtract

app = Flask(__name__)

patent_search_endpoint = Blueprint("patent_search_service", __name__)
endpoint = "/patent_search_service"


@patent_search_endpoint.route(endpoint, methods=['GET', 'POST'])
def get_patent_search():
    return render_template('patent_search.html')


# @app.route('/')
# def index():
# 	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['name']

    if text:

        try:
            patent_extract_class = PatentExtract()
            patent_extract_class.search_by_examiner(text=text)
            patent_extract_class.extract_patent_details(text=text)

            newName = text
            return jsonify({'name': 'author ' + newName + ' details has been downlaoded'})
        except Exception as e:
            return jsonify({'error': 'System Error ! , please try again'})

    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=True)
