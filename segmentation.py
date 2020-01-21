import pandas as pd
from datetime import datetime


def segmentation(senorEvents):
    # segmentation
    windowSize = 60  # taking fixed sensor window
    listWithSegments = list()
    currentSegment = pd.DataFrame(columns=['Date', 'Time', 'Device', 'Value'])

    startTime = datetime.strptime(senorEvents['Date'].iloc[0] + ' ' + senorEvents['Time'].iloc[0],
                                  '%Y-%m-%d %H:%M:%S.%f')
    endTime = datetime.strptime(senorEvents['Date'].iloc[-1] + ' ' + senorEvents['Time'].iloc[-1],
                                '%Y-%m-%d %H:%M:%S.%f')

    for index, row in senorEvents.iterrows():

        currentTime = datetime.strptime(row['Date'] + ' ' + row['Time'], '%Y-%m-%d %H:%M:%S.%f')

        if (currentTime - startTime).seconds < windowSize:

            currentSegment = pd.concat([currentSegment, row.to_frame().T])

        else:
            listWithSegments.append(currentSegment)

            startTime = currentTime
            currentSegment = currentSegment.iloc[0:0]
            currentSegment = pd.concat([currentSegment, row.to_frame().T])

    listWithSegments.append(currentSegment)  # for the last segment

    return listWithSegments
