from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import activityDiscovery
import activityRecognition
import dbAPI
import solutions

app = Flask(__name__)
cluster = activityDiscovery.OnlineCluster(20)
svm = activityRecognition.SVM()
CORS(app)

set_start_time = False
start_time = 0
trainings_duration = 2628000000


@app.route("/solution", methods=["GET"])
def solution():
    if request.method == "GET":
        print("SOLUTION")
        founded_activities, accuracy = solutions.get_solutions()
        return jsonify({'founded_activities': founded_activities, 'accuracy': accuracy})


# @app.route("/start_time", methods=["POST"])
# def start_time():
#     if request.method == "POST":
#         data = request.get_json(force=True)
#         global start_time
#         start_time = data['time']

@app.route("/discovery", methods=["POST"])
def discovery():
    if request.method == "POST":
        data = request.get_json(force=True)

        label = data['label']
        data = pd.Series(data['feature'])
        time = data.iloc[-1]
        data = data[:-1]

        # check if trainingstime passed or not
        global set_start_time
        global start_time
        if set_start_time is not True:
            start_time = time
            set_start_time = True
        diff = time - start_time

        # activity discovery (return true/false)
        answer_ad = cluster.cluster(data, time)
        if answer_ad:
            dbAPI.write(data.to_json(orient='records'), time, label)
            print(trainings_duration)
            print(diff)
            if diff > trainings_duration:
                svm.train()
                solutions.add_founded_activities(label)
            return jsonify({'answer': "Founded new activity!"})

        # activity recognition
        elif svm.model is not None:
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
