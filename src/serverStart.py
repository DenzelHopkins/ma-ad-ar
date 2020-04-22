import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

from src.activityRecognitionComponent import activityRecognitionAPI
from src.activityDiscoveryComponent import activityDiscoveryAPI
from src import baselineSystem, databaseAPI, solutions

app = Flask(__name__)
CORS(app)

# Initialize components
training = True
system = 'baseline'
activityRecognition = activityRecognitionAPI.activityRecognition()
activityDiscovery = activityDiscoveryAPI.activityDiscovery()
database = databaseAPI.database()


# Initialize server
@app.route("/initializeServer", methods=["POST"])
def initializeServer():
    if request.method == "POST":
        data = request.get_json(force=True)
        global system
        system = data['system']
        return jsonify({'answer': 'Initialized Server!'})


# Analyse new dataPoint
@app.route("/analyseDataPoint", methods=["POST"])
def analyseDataPoint():
    if request.method == "POST":
        # Read data from the request
        data = request.get_json(force=True)
        label = data['label']
        dataPoint = pd.Series(data['feature'])
        time = dataPoint.iloc[-1]
        dataPoint = dataPoint[:-1]

        # Object for the answer
        answer = {'recognizedActivity': 'No activity', 'discoveredActivity': 'No activity'}

        # Check if trainingDuration is over
        global training
        if training != data['training']:
            activityRecognition.trainModel(database)
            training = False

        # When use the integrated system
        if system == 'integrated':
            resultActivityDiscovery = activityDiscovery.discover(dataPoint, database, label, time)
            if resultActivityDiscovery:
                answer['discoveredActivity'] = resultActivityDiscovery
                solutions.addPredActivities(resultActivityDiscovery, label)
                if not training:
                    activityRecognition.trainModel(database)
            if not training:
                resultActivityRecognition = activityRecognition.predictDataPoint(dataPoint)
                answer['recognizedActivity'] = resultActivityRecognition
                solutions.addPredActivities(resultActivityRecognition, label)

        # When use the baseline system
        if system == 'baseline':
            baselineSystem.writeToDatabase(dataPoint, database, label, time)
            if not training:
                resultActivityRecognition = activityRecognition.predictDataPoint(dataPoint)
                answer['recognizedActivity'] = resultActivityRecognition
                solutions.addPredActivities(resultActivityRecognition, label)

        # When using the modified system
        if system == 'modification':
            resultActivityDiscovery, knownDataPoint = activityDiscovery.modifiedDiscover(dataPoint, database, label,
                                                                                         time)
            print(resultActivityDiscovery, knownDataPoint)

            if resultActivityDiscovery is not None:
                answer['discoveredActivity'] = resultActivityDiscovery
                solutions.addPredActivities(resultActivityDiscovery, label)
                if not training:
                    activityRecognition.trainModel(database)
            if not training and knownDataPoint is True:
                resultActivityRecognition = activityRecognition.predictDataPoint(dataPoint)
                print(resultActivityRecognition)
                answer['recognizedActivity'] = resultActivityRecognition
                solutions.addPredActivities(resultActivityRecognition, label)

    # Return answer
    return jsonify(answer)


# Ask for the solutions
@app.route("/solution", methods=["GET"])
def solution():
    if request.method == "GET":
        solutions.getSolutions()
        return jsonify({'answer': "Look in the python console for the solutions!"})


if __name__ == "__main__":
    database.clear()
    print("Database is clear!")
    app.run()
