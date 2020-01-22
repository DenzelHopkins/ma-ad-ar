from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import clustering
import dbAPI

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

        # activity discovery
        answer_ad = cluster.cluster(data, time)

        # activity recognition

        if answer_ad:

            print(data)
            print(type(data))
            print(time)
            print(type(time))
            print(label)
            print(type(label))

            dbAPI.write(data.to_json(orient='records'), time, label)
            return jsonify({'text': label})
        else:
            return jsonify({'text': 'No newly founded activity!'})


if __name__ == "__main__":
    dbAPI.clear()
    print("Database is clear!")
    app.run()
