import datetime
import json

end_json = []
data = {}

with open('data/dataTest', 'r') as f:
    content = f.readlines()
    for x in content:
        row = x.split()
        data['value'] = str(row[3])
        data['device'] = str(row[2])
        date_time_str = str(row[0]) + str(row[1])
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d%H:%M:%S.%f')
        data['timestamp'] = str(date_time_obj)
        json_data = json.dumps(data)
        end_json.append(json_data)

print(end_json)

f = open('data.json', 'a')
f.writelines("%s\n" % i for i in end_json)
f.close()

print("Data is written!")
