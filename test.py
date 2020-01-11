# import pprint
#
# from pymongo import MongoClient
#
# client = MongoClient("mongodb://127.0.0.1:27017")
#
# print(str(client.list_databases()))
#
# test = client.thepolyglotdeveloper.people
#
# for record in test.find().limit(10):
#     pprint.pprint(record)
#
# print("Connection Successful")
# client.close()

list1 = []
list2 = []
list3 = []
list4 = []

with open('data/dataTest', 'r') as f:
    content = f.readlines()
    for x in content:
        row = x.split()
        list1.append(str(row[0]))
        list2.append(str(row[1]))
        list3.append(str(row[2]))
        list4.append(str(row[3]))