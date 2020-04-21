import numpy as np
import pymongo
from pymongo import MongoClient
from sklearn.utils import shuffle


class database(object):

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
                       "Respirate",
                       "Other"]
        self.client = MongoClient("mongodb://127.0.0.1:27017")

    def write(self, data, time, label):
        point = {"segment": data,
                 "time": time,
                 "label": label}
        path = self.client.daten[label]
        path.insert_one(point)

        self.client.close()

    def clear(self):
        for label in self.labels:
            path = self.client.daten[label]
            path.drop()

        self.client.close()

    def get(self):
        data = []
        for label in self.labels:
            path = self.client.daten[label]
            for document in path.find({}).sort("time", pymongo.DESCENDING):
                data.append(document)

        self.client.close()

        data = shuffle(data)

        return np.array(data)
