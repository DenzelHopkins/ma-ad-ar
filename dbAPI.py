import numpy as np
import pymongo
from pymongo import MongoClient
from sklearn.utils import shuffle

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

client = MongoClient("mongodb://127.0.0.1:27017")


def write(data, time, label):
    point = {"segment": data,
             "time": time,
             "label": label}
    path = client.daten[label]
    path.insert_one(point)

    client.close()


def clear():
    for l in labels:
        path = client.daten[l]
        path.drop()

    client.close()


def get(amount):
    data = []

    for l in labels:
        path = client.daten[l]
        #for document in path.find({}).sort("time", pymongo.DESCENDING):
        for document in path.find(limit=amount).sort("time", pymongo.DESCENDING):
            data.append(document)

    client.close()

    data = shuffle(data)

    return np.array(data)
