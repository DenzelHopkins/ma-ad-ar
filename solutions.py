from sklearn.metrics import confusion_matrix

founded_activities = {"Meal_Preparation": 0,
                      "Relax": 0,
                      "Eating": 0,
                      "Work": 0,
                      "Sleeping": 0,
                      "Wash_Dishes": 0,
                      "Bed_to_Toilet": 0,
                      "Enter_Home": 0,
                      "Leave_Home": 0,
                      "Housekeeping": 0,
                      "Respirate": 0}

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
          "Respirate"]

predicted_correct = 0
predicted_count = 0

predicted_label = []
correct_label = []


def add_founded_activities(label):
    global founded_activities
    founded_activities[label] = founded_activities[label] + 1


def add_pred_activities(pred_label, label):
    global predicted_correct
    global predicted_count
    if pred_label == label:
        predicted_correct += 1
    predicted_count += 1

    correct_label.append(label)
    predicted_label.append(pred_label)


def get_solutions():
    cm = confusion_matrix(correct_label, predicted_label, labels=labels)
    print(labels)
    print(cm)

    return founded_activities, (predicted_correct / predicted_count)
