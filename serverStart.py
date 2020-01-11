from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import clustering

app = Flask(__name__)
cluster = clustering.OnlineCluster(5)
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
        data = pd.Series(data)

        time = data.iloc[-1]
        data = data[:-1]

        cluster.cluster(data, time)

        # print(data)
        return jsonify({'text': 'Works'})


if __name__ == "__main__":
    app.run()
