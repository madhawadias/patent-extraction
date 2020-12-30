from flask import Flask, render_template, request, jsonify, Blueprint
from back_end.helpers.patent_details import PatentExtract

app = Flask(__name__)

patent_mainpage_endpoint = Blueprint("patent_mainpage_service", __name__)
endpoint = "/patent_mainpage_service"


@patent_mainpage_endpoint.route(endpoint, methods=['GET', 'POST'])
def get_mainpage():
    return render_template('main.html')