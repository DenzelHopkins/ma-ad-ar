from flask import Flask, jsonify, request
from flask_corsify import CORSify

import activitydiscovery

app = Flask(__name__)
CORSify(app)


@app.route("/")
def home():
    return "Hello World"


@app.route("/start", methods=["GET"])
def start():
    if request.method == "GET":
        activitydiscovery.activityDiscovery()
        return jsonify({'text': 'DataLoadWorks'})


if __name__ == "__main__":
    app.run()
