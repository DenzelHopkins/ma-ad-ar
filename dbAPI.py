import pprint

import numpy as np

from pymongo import MongoClient


def write(data, time, label):
    client = MongoClient("mongodb://127.0.0.1:27017")

    point = {"segment": data,
             "time": time,
             "label": label}
    path = client.daten.labeld
    path.insert_one(point)

    client.close()


def clear():
    client = MongoClient("mongodb://127.0.0.1:27017")

    path = client.daten.labeld
    path.drop()

    client.close()


def get(amount):
    client = MongoClient("mongodb://127.0.0.1:27017")
    path = client.daten.labeld

    data = []

    for document in path.find(limit=amount):
        data.append(document)

    client.close()

    return np.array(data)
