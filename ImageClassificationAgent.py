import math
import operator


class ImageClassificationAgent:

    #this method is responsible for predicting class label for given percept
    def knnPredict(self, percept, TrainingData, K):
        euDistance = []

        for trainingImage in TrainingData.keys():
            trainFeatureVector = TrainingData[trainingImage]
            #calculating distance between percept and each record from training data
            d = self.calculateEucledeanDistance(percept, trainFeatureVector)
            #storing euclidean distances
            euDistance.append((trainingImage.label, d))
            #sorting distances stored
            euDistance.sort(key=operator.itemgetter(1))

        #fetching first K distances from a list of sorted euclidean distances
        knn = euDistance[:int(K)]

        landscapeCount = 0
        headshotCount = 0

        #class label prediction
        for entry in knn:
            if entry[0] == "landscape":
                landscapeCount += 1
            else:
                headshotCount += 1

        if landscapeCount > headshotCount:
            return "landscape"
        elif headshotCount > landscapeCount:
            return "headshot"

    #this method is responsibel for calculating euclidean distances between two vectors input1 and input2
    def calculateEucledeanDistance(self, input1, input2):
        d = 0.0
        for i in range(len(input1)):
            x = float(input1[i])
            y = float(input2[i])
            d += ((x - y) ** 2)
        d = math.sqrt(d)
        return d
