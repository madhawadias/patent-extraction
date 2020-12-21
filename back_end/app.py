from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


