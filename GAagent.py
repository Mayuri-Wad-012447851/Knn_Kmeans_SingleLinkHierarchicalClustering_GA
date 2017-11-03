from matplotlib import pyplot as plt
import numpy as np
import random, sys

class GAagent():
    #this class is responsible for Genetic Algorithm functions
    targetImage = None
    sourceImage = None
    finalOutput = []

    def __init__(self, sImg, dImg):
        self.targetImage = sImg
        self.sourceImage = dImg

    def GAAlgorithmFunction(self):
        #this method initiates GA algorithm
        self.finalOutput = []

        rowIndex = 0

        source = np.asarray(self.sourceImage)
        target = np.asarray(self.targetImage)

        print "Finding best fit for each row.. Please be patient as this may take some time :)"

        for row in target:

            rows = self.createRandomPopulation(row)
            rows.append(source[rowIndex])

            itr = 0
            while True:
                fitBitStrings = self.getBitStringsWithFittestScore(rows, row)
                rows = self.bitStringMutation(fitBitStrings[0], fitBitStrings[1])
                itr += 1
                #calculating manhatten distance for each bit string row of target image and bit string with fittest score
                d = self.calculateManhattanDistance(row, fitBitStrings[0])
                if d < 5000 or itr > 25:
                    self.finalOutput.append(fitBitStrings[0])
                    break
            rowIndex += 1

        self.plotImages(source, target)

    def plotImages(self, src, dest):
        #this method plots source, destination and final evolved image
        output = np.asarray(self.finalOutput)
        self.finalOutput = output.astype(np.uint8)
        plt.title("\n Please close the image to proceed further\nSource Image")
        plt.xticks([])
        plt.yticks([])
        plt.imshow(src)
        plt.tight_layout()
        plt.show()
        plt.close()

        plt.title("\n Please close the image to proceed further\nTarget Image")
        plt.xticks([])
        plt.yticks([])
        plt.imshow(dest)
        plt.tight_layout()
        plt.show()
        plt.close()

        plt.title("\n Please close the image to proceed further\nEvolved Image")
        plt.xticks([])
        plt.yticks([])
        plt.imshow(self.finalOutput)
        plt.tight_layout()
        plt.show()
        plt.close()

    def createRandomPopulation(self, bitString):
        #this method creates random population of chromosomes
        output = []
        i = 0
        while i < 100:
            pixelRow = []
            j = 0
            while j < len(bitString):
                pixel = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                pixelRow.append(pixel)
                j += 1
            output.append(pixelRow)
            i += 1
        return output

    def calculateManhattanDistance(self, str1, str2):
        #this method calculates manhatten distance between str1 and str2
        m_distance = 0

        for i in range(len(str1)):
            for j in range(len(str1[i])):
                temp = float(str1[i][j]) - float(str2[i][j])
                m_distance += abs(temp)

        return m_distance

    def getBitStringsWithFittestScore(self, bitStringRows, targetRow):
        #this method returns bit strings with fittest score
        values = []
        values.append(sys.maxint)
        values.append(sys.maxint)

        rows = [bitStringRows[0], bitStringRows[1]]

        for row in bitStringRows:

            distance = self.calculateManhattanDistance(row, targetRow)

            if distance < values[0]:
                rows[0] = row
                values[0] = distance
            elif distance < values[1]:
                rows[1] = row
                values[1] = distance

        return rows

    def bitStringMutation(self, bitString1, bitString2):
        #this method mutates two bit strings
        output = []

        for i in range(1, len(bitString2) - 1):
            subString = []
            subString.extend(bitString1[0:i])
            subString.extend(bitString2[i:len(bitString2)])
            output.append(subString)

        for i in range(1, len(bitString2) - 1):
            subString = []
            j = 0
            while j < i:
                pixel = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                subString.append(pixel)
                j += 1
            for k in range(i, len(bitString2)):
                subString.append(bitString2[k])
            output.append(subString)

        for i in range(1, len(bitString2) - 1):
            subString = []
            subString.extend(bitString2[0:i])
            subString.extend(bitString1[i:len(bitString2)])
            output.append(subString)

        for i in range(1, len(bitString2) - 1):
            subString = []
            j = 0
            while j < i:
                pixel = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                subString.append(pixel)
                j += 1
            for k in range(i, len(bitString2)):
                subString.append(bitString1[k])
            output.append(subString)

        return output
