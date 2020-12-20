from back_end.routes.patent_search_route import patent_search_endpoint
from back_end.routes.patent_search_route import patent_search_process_endpoint
from back_end.routes.patent_download_route import patent_download_service

from back_end.app import app
import gc

gc.enable()
app.register_blueprint(patent_search_endpoint)
app.register_blueprint(patent_search_process_endpoint)
app.register_blueprint(patent_download_service)


@app.route("/check", methods=["GET"])
def check():
    return "200"


if __name__ == "__main__":
    print("Running")
    gc.enable()
    app.run(host="0.0.0.0", port=5000)

# from flask import Flask, render_template, request, jsonify
# from back_end.helpers.patent_details import PatentExtract
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
# 	return render_template('index.html')
#
# @app.route('/process', methods=['POST'])
# def process():
#
#
# 	text = request.form['name']
#
# 	if text :
#
# 		try:
# 			patent_extract_class = PatentExtract()
# 			patent_extract_class.search_by_examiner(text=text)
# 			patent_extract_class.extract_patent_details(text=text)
#
# 			newName = text
# 			return jsonify({'name' : 'author '+newName+' details has been downlaoded' })
# 		except Exception as e :
# 			return jsonify({'error' : 'System Error ! , please try again'})
#
# 	return jsonify({'error' : 'Missing data!'})
#
# if __name__ == '__main__':
# 	app.run(debug=True)
