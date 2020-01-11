import pprint

from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

print(str(client.list_databases()))

test = client.thepolyglotdeveloper.people

for record in test.find().limit(10):
    pprint.pprint(record)

print("Connection Successful")
client.close()
