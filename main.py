import gc
import os

from back_end.app import app
from back_end.routes.patent_download_route import patent_download_endpoint
from back_end.routes.patent_download_route import patent_download_process_endpoint
from back_end.routes.patent_mainpage_route import patent_mainpage_endpoint
from back_end.routes.patent_search_route import patent_search_endpoint
from back_end.routes.patent_search_route import patent_search_process_endpoint
from back_end.routes.patent_search_route import patent_search_progress_endpoint

gc.enable()
app.register_blueprint(patent_search_endpoint)
app.register_blueprint(patent_search_process_endpoint)
app.register_blueprint(patent_search_progress_endpoint)
app.register_blueprint(patent_download_endpoint)
app.register_blueprint(patent_download_process_endpoint)
app.register_blueprint(patent_mainpage_endpoint)


@app.route("/check", methods=["GET"])
def check():
    return "200"


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    print("Running")
    gc.enable()
    app.run(host="0.0.0.0", port=5001)


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
