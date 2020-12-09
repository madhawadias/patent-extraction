from flask import Flask,  render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('../../front-end/templates/index.html')
