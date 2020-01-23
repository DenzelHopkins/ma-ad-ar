from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import activityDiscovery
import activityRecognition
import dbAPI

app = Flask(__name__)
cluster = activityDiscovery.OnlineCluster(6)
svm = activityRecognition.SVM()
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

        # activity discovery (return true/false)
        answer_ad = cluster.cluster(data, time)

        # activity recognition (return label)
        if svm.model is not None:

            answer_ar_l, answer_ar_s = svm.predict(data)

            pred_label = answer_ar_l[0]
            pred_score = answer_ar_s

            if pred_score > 0.7:

                print("The Label is " + label)
                print("Predicted label is " + str(pred_label) + " with a score of " + str(pred_score))

        # when new cluster is found
        if answer_ad:
            dbAPI.write(data.to_json(orient='records'), time, label)
            svm.train()
            # wieiviel cases gibt es? ausarbeiten!
            return jsonify({'text': label})
        else:
            return jsonify({'text': 'No newly founded activity!'})


if __name__ == "__main__":

    # dbAPI.clear()
    # print("Database is clear!")

    app.run()
