import null as null
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import numpy as np
import dbAPI

data = dbAPI.get(862)

# label = {
#     "Meal_Preparation": 1,
#     "Relax": 2,
#     "Eating": 3,
#     "Work": 4,
#     "Sleeping": 5,
#     "Wash_Dishes": 6,
#     "Bed_to_Toilet": 7,
#     "Enter_Home": 8,
#     "Leave_Home": 9,
#     "Housekeeping": 10,
#     "Resperate": 11
# }

# for vector in data:

label = ["Meal_Preparation",
         "Relax",
         "Eating",
         "Work",
         "Sleeping",
         "Wash_Dishes",
         "Bed_to_Toilet",
         "Enter_Home",
         "Leave_Home",
         "Housekeeping",
         "Resperate"]

X = []  # samples
y = []  # labels

i = 0

for point in data:
    print(point['segment'])
    print(point['label'])
    print(point['time'])

    segment = []

    for n in point['segment'].strip("[]").split(','):
        segment.append(float(n))
    segment = np.array(segment)

    print(segment.size)

    X.append(segment)
    # y.append(label.get((point['label'])))
    y.append(point['label'])
X = np.vstack(X)

print(X)

print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

svm_model_linear = svm.SVC(kernel='linear').fit(X_train, y_train)
svm_predictions = svm_model_linear.predict(X_test)

accuracy = svm_model_linear.score(X_test, y_test)
cm = confusion_matrix(y_test, svm_predictions, labels=label)

print(accuracy)
print(label)
print(cm)
