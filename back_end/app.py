from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


print(get_base_path())
print(r"{}\temp_data\pdf\2".format(get_base_path()))