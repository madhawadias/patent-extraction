import pandas as pd
from flask import Flask, render_template, request, jsonify, Blueprint
from back_end.helpers.patent_pdf_details import PatentDownload
import time

app = Flask(__name__)

patent_download_service = Blueprint("patent_download_service", __name__)
endpoint = "/patent_download_service"

@patent_download_service.route(endpoint, methods=['GET', 'POST'])
def get_patent_search():
	return render_template('patent_download.html')

# class ExtractPatentId:
#
#     def runner(file_name):
#         path = 'temp_data/' + str(file_name)
#         df = pd.read_csv(path)
#         patentIds = df["patent-application-number"]
#         ids = []
#         for patentId in patentIds:
#             # print(patentId)
#             patent_download_class = PatentDownload()
#             patent_download_class.patent_pdf(patentId)
#
#             ids.append(patentId)
#         # return ids
#
#     # name of the csv is added below
#
#     runner(file_name="ROTARU, OCTAVIAN 43645 18122020.csv")
