from flask import Flask,  render_template, request, jsonify
from back_end.helpers.patent_details import PatentExtract

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_query():
    text = request.form['u']
    processed_text = text.upper()
    patent_extract_class = PatentExtract()
    patent_extract_class.search_by_examiner(text = processed_text)
    patent_details = patent_extract_class.extract_patent_details(text = processed_text)

    return  patent_details


if __name__ == '__main__':
    app.run()
