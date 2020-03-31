import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

import activityDiscovery
import activityRecognition
import dbAPI
import outlierDetection
import solutions

app = Flask(__name__)
cluster = activityDiscovery.OnlineCluster(11)
svm = activityRecognition.SVM()
oneClassSVM = outlierDetection.OneSVM()
CORS(app)


@app.route("/solution", methods=["GET"])
def solution():
    if request.method == "GET":
        print("SOLUTION")
        solutions.get_solutions()

        print("----------------")
        unknown, known = oneClassSVM.activities()
        print("Unknown datapoints: " + str(unknown))
        print("Known datapoints: " + str(known))

        return jsonify({'answer': "Solution!"})


@app.route("/discovery", methods=["POST"])
def discovery():
    if request.method == "POST":
        allData = request.get_json(force=True)
        label = allData['label']
        training = allData['training']
        useActivityDiscovery = allData['activityDiscovery']
        data = pd.Series(allData['feature'])
        time = data.iloc[-1]
        data = data[:-1]

        # no activity discovery
        if not useActivityDiscovery:
            if training:
                print("Writing segmented activity to database")
                dbAPI.write(data.to_json(orient='records'), time, label)
            if not training:
                if svm.model is None:
                    print("Training Classification Model!")
                    svm.train()
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

        # activity discovery
        else:
            # outlier detection
            if oneClassSVM.model is not None:
                known = oneClassSVM.predict(data)
                if known[0] == -1:
                    # clustering
                    print("Datapoint is unknown, doing Online Clustering!")
                    answer_ad = cluster.cluster(data, time)
                    if answer_ad is not None:
                        print("Writing founded activity to database!")
                        dbAPI.write(answer_ad.to_json(orient='records'), time, label)
                        solutions.add_founded_activities(label)
                        print("Training OutlierDetection model!")
                        oneClassSVM.train()
                        if not training:
                            print("Training Classification model!")
                            svm.train()
                        return jsonify({'answer': "Founded new activity!"})
                else:
                    print("Datapoint is known, try to doing Classification!")
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
            else:
                # clustering if no outlier detection model
                print("No outlier detection model, doing Online Clustering!")
                answer_ad = cluster.cluster(data, time)
                if answer_ad is not None:
                    print("Writing founded activity to database!")
                    dbAPI.write(answer_ad.to_json(orient='records'), time, label)
                    solutions.add_founded_activities(label)
                    print("Training OutlierDetection model!")
                    oneClassSVM.train()
                    if not training:
                        print("Training Classification model!")
                        svm.train()
                    return jsonify({'answer': "Founded new activity!"})

        return jsonify({'answer': "Nothing!"})


if __name__ == "__main__":
    dbAPI.clear()
    print("Database is clear!")
    app.run()
