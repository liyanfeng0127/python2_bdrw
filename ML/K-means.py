import numpy as np

def kmeans(X , k , maxIt):
    numPoints , numDim = X.shape
    dataSet = np.zeros((numPoints , numDim + 1))
    dataSet[: , : -1] = X

    centroids = dataSet[np.random.randint(numPoints , size= k) , :]
    # centroids = dataSet[0:2 , : ]
    centroids[: , -1] = range(1 , k + 1)

    iteration = 0
    oldCentroid = None

    while not shouldStop(oldCentroid , centroids , iteration , maxIt):
        print "iteration:" , iteration
        print "dataSet:" , dataSet
        print "centroids:" , centroids
        oldCentroid = np.copy(centroids)
        iteration += 1

        updatelabels(dataSet , centroids)
        centroids = getCentroids(dataSet , k)

    return dataSet

def shouldStop(oldCentroid , centroids , iteration , maxIt):
    if iteration > maxIt:
        return True
    return np.array_equal(oldCentroid , centroids)

def updatelabels(dataSet , centroids):
    numPoints , numDim = dataSet.shape
    for i in range(0  , numPoints):
        dataSet[i , -1] = getLabelFromClosestCentroid(dataSet[i , : -1] , centroids)

def getLabelFromClosestCentroid(dataSetRow , centroid):
    label = centroid[0 , -1]
    minDist = np.linalg.norm(dataSetRow - centroid[0 , : -1])
    for i in range(1 , centroid.shape[0]):
        dist = np.linalg.norm(dataSetRow - centroid[i , : -1])
        if dist < minDist:
            minDist = dist
            label = centroid[i , -1]
    print "minDist:" , minDist
    return label

def getCentroids(dataSet , k):
    result = np.zeros((k ,dataSet.shape[1]))
    for i in range(1 , k + 1):
        oneCluster = dataSet[dataSet[: , -1] == i , :-1]
        result[i - 1 , : -1] = np.mean(oneCluster , axis= 0)

    return result

x1 = np.array([1 , 1])
x2 = np.array([2 , 1])
x3 = np.array([4 , 3])
x4 = np.array([5 , 4])

testX = np.vstack((x1 , x2 , x3 , x4))

result = kmeans(testX , 2 , 10)
print "final result:"
print result