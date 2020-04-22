def writeToDatabase(dataPoint, database, label, time):
    database.write(dataPoint.to_json(orient='records'), time, label)
