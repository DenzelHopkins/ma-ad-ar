def writeToDatabase(dataPoint, database, label):
    time = dataPoint.iloc[-1]
    dataPoint = dataPoint[:-1]
    database.write(dataPoint.to_json(orient='records'), time, label)
