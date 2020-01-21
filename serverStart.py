from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import clustering

app = Flask(__name__)
cluster = clustering.OnlineCluster(7)
CORS(app)


@app.route("/")
def home():
    return "Hello World"


@app.route("/start", methods=["GET"])
def start():
    if request.method == "GET":
        return jsonify({'text': 'DataLoadWorks'})


@app.route("/discovery", methods=["POST"])
def discovery():
    if request.method == "POST":
        data = request.get_json(force=True)

        label = data['label']
        data = pd.Series(data['feature'])
        time = data.iloc[-1]
        data = data[:-1]

        answer = cluster.cluster(data, time)

        if answer:
            return jsonify({'text': label})
        else:
            return jsonify({'text': 'No newly founded activity!'})


if __name__ == "__main__":
    app.run()
