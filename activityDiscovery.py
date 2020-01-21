import clustering

cluster = clustering.OnlineCluster(5)


def run(data):

    print("Works")
    cluster.cluster(data)
