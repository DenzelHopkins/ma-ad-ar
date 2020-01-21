from datetime import datetime
from copy import deepcopy
import numpy as np
import pandas as pd
from help import *


# Time of day (morning, noon,afternoon, evening, night, late night)
# Day of week
# Whether the day is weekend or not
# Number of kinds of motion sensors involved
# Total   Number   of   times   of   motion   sensor   events   triggered
# Energy consumption for an activity (in Watt)
# Motion sensor M1...M51 (On/Off)

def featureExtraction(df, listWithSegments):
    amountMotionDevices = 0.0
    for item in filter(lambda device: 'M' in device, df['Device'].unique()):
        amountMotionDevices = amountMotionDevices + 1

    vector_array = []
    feature_array = []

    for i in listWithSegments:

        feature_array.clear()

        currentSegment = i

        c_time = currentSegment['Time']
        c_date = currentSegment['Date']
        c_device = currentSegment['Device']
        c_value = currentSegment['Value']

        time = datetime.strptime(c_time.iloc[0], '%H:%M:%S.%f')

        # Time of day (morning, noon, afternoon, evening, night, late night)
        for x in dayTime(time.hour):
            feature_array.append(x)

        # Day of week
        for x in day(time.weekday()):
            feature_array.append(x)

        # Weekend or not
        if time.weekday() < 4:
            feature_array.append(0)
        else:
            feature_array.append(1)

        # Number of motions sensor
        motionDevices = 0
        filterMotion = filter(lambda device: 'M' in device, c_device.unique())
        for item in filterMotion:
            motionDevices = motionDevices + 1
        feature_array.append(motionDevices)

        # Total Number of times of motion sensor events triggered
        totalMotionDevices = 0
        filterMotion = filter(lambda device: 'M' in device, c_device)
        for item in filterMotion:
            totalMotionDevices = totalMotionDevices + 1
        feature_array.append(totalMotionDevices)

        # Energy consumption


        # Motion sensor M1...M51 (On/Off)
        motionDevices = np.zeros(100,
                                 dtype=int)  # np.empty(amountMotionDevices * 2)  # z.B. M1 = ON, M3 = ON => [1,0,0,0,1,0,...]
        filteredSegment = currentSegment[currentSegment['Device'].str.contains("M")]
        for index, row in filteredSegment.iterrows():

            a, b, c, d, = row['Device']
            value = row['Value']

            number = int(b) * 100 + int(c) * 10 + int(d)  # creating number of the device

            position = ((number - 1) * 2)

            if value == 'ON':
                motionDevices[position] = 1
            else:
                motionDevices[position + 1] = 1

        for x in motionDevices:
            feature_array.append(x)

        # add time to feature array

        vector_array.append(deepcopy(feature_array))  # add feature_array to the vectors

    return pd.DataFrame(vector_array, dtype=float)