from clustering import OnlineCluster
from segmentation import *
from featureExtraction import *
from normalization import *


def activityDiscovery():
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    with open('data/dataTest', 'r') as f:  # dataTest with 1000 rows
        content = f.readlines()
        for x in content:
            row = x.split()
            list1.append(str(row[0]))
            list2.append(str(row[1]))
            list3.append(str(row[2]))
            list4.append(str(row[3]))

    print("Data is loaded!")

    # # for writing TestData
    # with open('data/dataTest', 'w') as f:
    #      for item in content[:100000]:
    #          f.write("%s" % item)

    df = pd.DataFrame(
        {'Date': list1,
         'Time': list2,
         'Device': list3,
         'Value': list4
         })

    # Segmentation
    listWithSegments = segmentation(df)
    print("Segmentation fulfilled!")

    # Feature Extraction
    df_features = featureExtraction(df, listWithSegments)
    print("Feature Extraction fulfilled!")

    # Normalization
    df_features = normalization(df_features)
    print("Normalization fulfilled!")

    rows = df_features.shape[0]
    training_rows = int(rows * 0.8)
    df_training = df_features[:training_rows]
    df_test = df_features[training_rows:]

    print("Segmentation and Feature Extraction is fulfilled!")

    cluster = OnlineCluster(5)

    for index, row in df_training.iterrows():
        cluster.cluster(row)

    print("FoundedClusters:", len(cluster.currentClusters))
