from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


# print(get_base_path())
# print(r"{}\temp_data\pdf\2".format(get_base_path()))

# path_b = "aefgaega"
#
# params = {'behavior': 'allow', 'downloadPath': r"{}\temp_data\pdf".format(get_base_path()) + path_b + r"\2"}
#
# print(params)
# test = "{}".format(get_base_path())+ str(os.getenv("CHROME_DRIVER_PATH"))
# print(test)