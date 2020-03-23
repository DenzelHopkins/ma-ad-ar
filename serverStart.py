import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

import activityDiscovery
import activityRecognition
import dbAPI
import solutions

app = Flask(__name__)
cluster = activityDiscovery.OnlineCluster(11)
svm = activityRecognition.SVM()
CORS(app)


@app.route("/solution", methods=["GET"])
def solution():
    if request.method == "GET":
        print("SOLUTION")
        founded_activities, accuracy = solutions.get_solutions()
        return jsonify({'founded_activities': founded_activities, 'accuracy': accuracy})


@app.route("/discovery", methods=["POST"])
def discovery():
    if request.method == "POST":
        data = request.get_json(force=True)
        label = data['label']
        training = data['training']
        manuelSegmentation = data['manuelSegmentation']
        data = pd.Series(data['feature'])
        time = data.iloc[-1]
        data = data[:-1]

        # activity discovery
        if manuelSegmentation:
            if training:
                dbAPI.write(data.to_json(orient='records'), time, label)
            if not training:
                if svm.model is None:
                    print("training------------------------------------------")
                    svm.train()
        else:
            answer_ad = cluster.cluster(data, time)
            if answer_ad is not None:
                dbAPI.write(answer_ad.to_json(orient='records'), time, label)
                solutions.add_founded_activities(label)
                if not training:
                    print("training------------------------------------------")
                    svm.train()
                return jsonify({'answer': "Founded new activity!"})

        # activity recognition
        if svm.model is not None:
            answer_ar_l, answer_ar_s = svm.predict(data)
            pred_label = answer_ar_l[0]
            pred_score = answer_ar_s
            solutions.add_pred_activities(pred_label, label)
            print("----------------------")
            print("Predicted label is " + str(pred_label) + " with a score of " + str(pred_score))
            print("The Label is " + label)
            return jsonify({'answer': "Predicted activity!"})

        else:
            return jsonify({'answer': "Nothing!"})


if __name__ == "__main__":
    dbAPI.clear()
    print("Database is clear!")
    app.run()
