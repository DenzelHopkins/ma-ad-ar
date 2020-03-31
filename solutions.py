from sklearn.metrics import confusion_matrix

import outlierDetection

labels = ["Meal_Preparation",
          "Relax",
          "Eating",
          "Work",
          "Sleeping",
          "Wash_Dishes",
          "Bed_to_Toilet",
          "Enter_Home",
          "Leave_Home",
          "Housekeeping",
          "Respirate",
          "Other"]

activities = {
    "Meal_Preparation": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Relax": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Eating": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Work": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Sleeping": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Wash_Dishes": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Bed_to_Toilet": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Enter_Home": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Leave_Home": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Housekeeping": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Respirate": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    },
    "Other": {
        "founded": 0, "truePositives": 0, "falseNegatives": 0, "falsePositives": 0
    }}

totalCount = 0

predicted_label = []
correct_label = []


def add_founded_activities(label):
    global activities
    activities[label]["founded"] = activities[label]["founded"] + 1


def add_pred_activities(pred_label, label):
    global totalCount
    global activities
    if pred_label == label:
        activities[pred_label]["truePositives"] += 1
    else:
        activities[pred_label]["falsePositives"] += 1
        activities[label]["falseNegatives"] += 1

    totalCount += 1

    correct_label.append(label)
    predicted_label.append(pred_label)


def get_solutions():
    cm = confusion_matrix(correct_label, predicted_label, labels=labels)

    print("----------------------")
    print("Founded Activity:")
    print(activities)

    print("----------------------")
    print("ConfusionMatrix:")
    print(labels)
    print(cm)

    print("----------------------")
    totalfScore = 0
    for x, y in activities.items():
        try:
            precision = (y["truePositives"] / (y["truePositives"] + y["falsePositives"]))
        except:
            precision = 0
        try:
            recall = y["truePositives"] / (y["truePositives"] + y["falseNegatives"])
        except:
            recall = 0
        try:
            fScore = 2 * (precision * recall) / (precision + recall)
        except:
            fScore = 0
        totalfScore += fScore
        print("Precision for " + str(x) + " is " + str(round(precision, 2)) + ", the Recall is " + str(
            round(recall, 2)) + " and the F-Score is " + str(round(fScore, 2)))

    print("----------------------")
    print("The OverallfScore is: " + str(round((totalfScore / len(activities)), 2)))
    totalCorrect = 0
    for x, y in activities.items():
        totalCorrect += y["truePositives"]
    print("The OverallAccuracy is: " + str(round((totalCorrect / totalCount), 2)))

