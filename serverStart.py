import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

import baselineSystem
from ActivityRecognitionComponent import activityRecognitionAPI
from ActivityDiscoveryComponent import activityDiscoveryAPI
import databaseAPI

app = Flask(__name__)
CORS(app)

useActivityDiscovery = True
training = True
modification = False

activityRecognition = activityRecognitionAPI.activityRecognition()
activityDiscovery = activityDiscoveryAPI.activityDiscovery(modification)
database = databaseAPI.database()


@app.route("/initializeServer", methods=["POST"])
def initializeServer():
    if request.method == "POST":
        data = request.get_json(force=True)
        global useActivityDiscovery
        useActivityDiscovery = data['useActivityDiscovery']
        return jsonify({'answer': 'Initialized Server!'})


@app.route("/analyseDataPoint", methods=["POST"])
def analyseDataPoint():
    if request.method == "POST":
        data = request.get_json(force=True)
        label = data['label']
        dataPoint = pd.Series(data['feature'])
        time = dataPoint.iloc[-1]
        dataPoint = dataPoint[:-1]
        answer = {'recognizedActivity': '-', 'discoveredActivity': '-'}

        global training
        if training != data['training']:
            activityRecognition.trainModel(database)
            training = False

        global useActivityDiscovery
        if useActivityDiscovery:
            resultActivityDiscovery = activityDiscovery.discover(dataPoint, database, label, time)
            if resultActivityDiscovery is not None:
                answer['discoveredActivity'] = resultActivityDiscovery
                if not training:
                    activityRecognition.trainModel(database)
        else:
            baselineSystem.writeToDatabase(dataPoint, database, label)

        if not training:
            resultActivityRecognition = activityRecognition.predictDataPoint(dataPoint)
            answer['recognizedActivity'] = resultActivityRecognition

        # # dont use activity discovery
        # if not useActivityDiscovery:
        #     if training:
        #         dbAPI.write(data.to_json(orient='records'), time, label)
        #     if not training:
        #         if svm.model is None:
        #             svm.train()
        #         # use activity recognition
        #         if svm.model is not None:
        #             answer['recognizedActivity'] = svm.predict(data)
        # # use activity discovery
        # else:
        #     # use outlier detection
        #     if oneClassSVM.model is not None:
        #         known = oneClassSVM.predict(data)
        #         if known[0] == -1:
        #             # use clustering
        #             answerAD = cluster.cluster(data, time)
        #             if answerAD is not None:
        #                 dbAPI.write(answerAD.to_json(orient='records'), time, label)
        #                 answer['discoveredActivity'] = label
        #                 oneClassSVM.train()
        #                 if not training:
        #                     svm.train()
        #         else:
        #             # activity recognition
        #             if svm.model is None and not training:
        #                 svm.train()
        #             if svm.model is not None:
        #                 answer['recognizedActivity'] = svm.predict(data)
        #     else:
        #         # clustering if no outlier detection model
        #         answerAD = cluster.cluster(data, time)
        #         if answerAD is not None:
        #             dbAPI.write(answerAD.to_json(orient='records'), time, label)
        #             answer['discoveredActivity'] = label
        #             oneClassSVM.train()
        #             if not training:
        #                 svm.train()
        return jsonify(answer)


if __name__ == "__main__":
    database.clear()
    print("Database is clear!")
    app.run()
