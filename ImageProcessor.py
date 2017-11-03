from PIL import Image
import os
from ImageData import *
import colorsys
import numpy as np


class ImageProcessor:
    #this class provides methods to perform different operations on ImageData objects

    def createFold(self, TrainingData, samples, dirName, start, end):
        #this method is responsible for automatic fold creation for cross validation
        fileHandle = open(dirName, 'w')

        for i in range(start, end):
            name = samples[i].imageName
            actualName = samples[i].imageActualName
            featureArray = TrainingData[samples[i]]
            label = samples[i].label
            line = name + " " + str(featureArray) + " " + label + " " + actualName + "\n"
            fileHandle.write(line)

        fileHandle.close()

    def create3Folds(self, TrainingData):
        # this method creates 3 training and 3 validation folds
        directoryList = ['./trainFold1.txt', './trainFold2.txt', './trainFold3.txt',
                         './validationFold1.txt', './validationFold2.txt', './validationFold3.txt']

        samples = TrainingData.keys()

        try:

            print "Creating Validation Fold 1"
            self.createFold(TrainingData, samples, directoryList[3], 0, 40)

            print "Creating Validation Fold 2"
            self.createFold(TrainingData, samples, directoryList[4], 40, 80)

            print "Creating Validation Fold 3"
            self.createFold(TrainingData, samples, directoryList[5], 80, 120)

        except Exception as e:
            print 'Validation Fold creation failed.'
            print e.message
            return False

        try:

            print "Creating Training Fold 1"
            self.createFold(TrainingData, samples, directoryList[0], 40, 120)

            print "Creating Training Fold 2"
            fileHandle = open(directoryList[1], 'w')
            for i in range(40):
                name = samples[i].imageName
                actualName = samples[i].imageActualName
                featureArray = TrainingData[samples[i]]
                label = samples[i].label
                line = name + " " + str(featureArray) + " " + label + " " + actualName + "\n"
                fileHandle.write(line)

            for i in range(80, 120):
                name = samples[i].imageName
                actualName = samples[i].imageActualName
                featureArray = TrainingData[samples[i]]
                label = samples[i].label
                line = name + " " + str(featureArray) + " " + label + " " + actualName + "\n"
                fileHandle.write(line)
            fileHandle.close()

            print "Creating Training Fold 3"
            self.createFold(TrainingData, samples, directoryList[2], 0, 80)

        except Exception as e:
            print 'Training Fold creation failed.'
            print e.message
            return False

        print 'Successfully created validation and training folds..'
        return True

    @staticmethod
    def getSkinColorPercentage(image):
        #this method computes percentage of skin color pixels in an image
        skinColorPix = 0

        imageRGBs = list(image.imageData.getdata())

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            x = max(max(R, G), B)
            y = min(min(R, G), B)
            z = R - G
            if z < 0:
                z = z * -1
            #this formula has been taken from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.5.521&rep=rep1&type=pdf
            if R > 95 and G > 40 and B > 20 and (x - y) > 15 and ((10 * z) > 15) and R > G and R > B:
                skinColorPix += 1

        skinColorPercentage = float(float(skinColorPix) / float(len(imageRGBs))) * 100

        return skinColorPercentage

    @staticmethod
    def getWaterSkyColorPercentage(image):
        # this method computes percentage of blue color pixels in an image
        skyWaterPix = 0

        imageRGBs = list(image.imageData.getdata())

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            #this formula has been taken from
            #http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.5.1294&rep=rep1&type=pdf
            if B > (1.2 * max(G, R)):
                skyWaterPix += 1

        skyWaterColorPercentage = float(float(skyWaterPix) / float(len(imageRGBs))) * 100

        return skyWaterColorPercentage

    @staticmethod
    def getGreenColorPercentage(image):
        # this method computes percentage of green color pixels in an image
        greenPix = 0

        imageRGBs = list(image.imageData.getdata())

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            HSL = colorsys.rgb_to_hsv(R, G, B)
            Hue = HSL[0]
            #this range has been computed by self analysis
            if Hue >= 0.165 and Hue <= 0.5 and G >= 150 and R <= 200 and B <= 115:
                greenPix += 1

        greenaryPercentage = float(float(greenPix) / float(len(imageRGBs))) * 100

        return greenaryPercentage

    @staticmethod
    def getSunsetColorPercentage(image):
        # this method computes percentage of sunset color pixels in an image
        sunsetColorPix = 0

        imageRGBs = list(image.imageData.getdata())

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            # this range has been computed by self analysis
            if R >= 240 and R <= 255 and G >= 100 and G <= 230 and B <= 110 and B >= 0:
                sunsetColorPix += 1

        sunsetColorPercentage = float(float(sunsetColorPix) / float(len(imageRGBs))) * 100

        return sunsetColorPercentage

    @staticmethod
    def getBlurPercentage(image):
        #this method computes blurness percentage in an image
        #https://www.researchgate.net/post/Is_there_any_particular_method_to_check_the_blurriness_of_an_image
        blurPix = 0
        sat = []
        sumSaturation = 0.0
        imageRGBs = list(image.imageData.getdata())

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            HSL = colorsys.rgb_to_hsv(R, G, B)
            Saturation = HSL[1]
            sumSaturation += Saturation

        meanSaturation = sumSaturation / len(imageRGBs)

        for pix in imageRGBs:
            R = pix[0]
            G = pix[1]
            B = pix[2]
            HSL = colorsys.rgb_to_hsv(R, G, B)
            Saturation = HSL[1]
            if Saturation <= meanSaturation:
                blurPix += 1

        blurPercentage = float(float(blurPix) / float(len(imageRGBs))) * 100

        return blurPercentage

    def fetchFeatureVector(self, image):
        #this method creates an array of features for input image
        features = []

        feature1 = ImageProcessor.getSkinColorPercentage(image)
        feature2 = ImageProcessor.getWaterSkyColorPercentage(image)
        feature3 = ImageProcessor.getGreenColorPercentage(image)
        feature4 = ImageProcessor.getSunsetColorPercentage(image)
        #feature5 = ImageProcessor.getBlurPercentage(image)

        features.append(feature1)
        features.append(feature2)
        features.append(feature3)
        features.append(feature4)
        #features.append(feature5)

        return features

    def loadImagesToClassify(self, path):
        #this method loads images for which the class labels are to be decided
        print '\nLoading Images to classify...'
        imagesToClassify = []
        i = 1

        try:
            for f in os.listdir(path):
                imgName = "image" + str(i)
                img = ImageData(imgName, [], "", f)
                img.imageData = Image.open(os.path.join(path, f))
                i += 1
                imagesToClassify.append(img)
        except Exception as e:
            print 'Failed to load images to classify placed at path ' + path
            print 'Please try again.'
            e.message

        return imagesToClassify

    def extractColorFeature(self, image):
        #this method extracts color features for flag images
        image = np.asarray(image)
        rgbValues = {}
        for i in range(0, 4):
            rgbValues["R" + str(i + 1)] = 0
        for i in range(0, 4):
            rgbValues["G" + str(i + 1)] = 0
        for i in range(0, 4):
            rgbValues["B" + str(i + 1)] = 0

        counter = 0
        for eachRow in image:
            for eachPixel in eachRow:
                R = eachPixel[0]
                G = eachPixel[1]
                B = eachPixel[2]

                for j in range(0, 4):
                    if R < 64:
                        rgbValues["R" + str(j + 1)] += 1
                    if G < 64:
                        rgbValues["G" + str(j + 1)] += 1
                    if B < 64:
                        rgbValues["B" + str(j + 1)] += 1

                for j in range(0, 4):
                    if R < 128:
                        rgbValues["R" + str(j + 1)] += 1
                    if G < 128:
                        rgbValues["G" + str(j + 1)] += 1
                    if B < 128:
                        rgbValues["B" + str(j + 1)] += 1

                for j in range(0, 4):
                    if R < 192:
                        rgbValues["R" + str(j + 1)] += 1
                    if G < 192:
                        rgbValues["G" + str(j + 1)] += 1
                    if B < 192:
                        rgbValues["B" + str(j + 1)] += 1

                for j in range(0, 4):
                    if R < 255:
                        rgbValues["R" + str(j + 1)] += 1
                    if G < 255:
                        rgbValues["G" + str(j + 1)] += 1
                    if B < 255:
                        rgbValues["B" + str(j + 1)] += 1

                counter += 1

        for key in rgbValues.keys():
            rgbValues[key] = rgbValues[key] / float(counter)

        #forming a feature vector
        colorAttributeVector = []
        for key in rgbValues:
            colorAttributeVector.append(rgbValues[key])

        return colorAttributeVector
