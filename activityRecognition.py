from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np
import dbAPI


class SVM(object):
    def __init__(self):
        self.labels = ["Meal_Preparation",
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
        self.X = []
        self.y = []
        self.segment = []

        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []

        self.model = None

    def predict(self, segment):

        point = []
        for n in segment:
            point.append(float(n))
        point = [np.array(point)]

        label = self.model.predict(point)
        score = self.model.predict_proba(point).max()
        return label, score

    def train(self):
        data = dbAPI.get(20)
        self.X = []
        self.y = []

        if data.size > 50:
            for point in data:
                self.segment = []

                for n in point['segment'].strip("[]").split(','):
                    self.segment.append(float(n))
                self.segment = np.array(self.segment)

                self.X.append(self.segment)
                self.y.append(point['label'])

            self.X = np.vstack(self.X)

            self.X_train, self.X_test, self.y_train, self.y_test = \
                train_test_split(self.X, self.y, random_state=0)

            self.model = svm.SVC(kernel='poly', probability=True).fit(self.X_train, self.y_train)
        else:
            return

    def solutions(self):
        svm_predictions = self.model.predict(self.X_test)
        accuracy = self.model.score(self.X_test, self.y_test)
        cm = confusion_matrix(self.y_test, svm_predictions, labels=self.label)
        # print(accuracy)
        # print(self.label)
        # print(cm)
