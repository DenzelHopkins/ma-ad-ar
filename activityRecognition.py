from sklearn import svm

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
                       "Resperate",
                       "Other"]
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
        data = dbAPI.get(30)
        self.X = []
        self.y = []

        for point in data:
            self.segment = []

            for n in point['segment'].strip("[]").split(','):
                self.segment.append(float(n))
            self.segment = np.array(self.segment)

            self.X.append(self.segment)
            self.y.append(point['label'])

        self.X = np.vstack(self.X)

        self.model = svm.SVC(kernel='poly', probability=True).fit(self.X, self.y)
