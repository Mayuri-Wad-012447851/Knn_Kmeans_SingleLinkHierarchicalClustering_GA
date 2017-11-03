from Environment import *
from ImageClassificationAgent import *
from ImageProcessor import *

def main():
    #this method initiates the execution of homework3 assignment
    env = Environement()
    iProcessor = ImageProcessor()
    iAgent = ImageClassificationAgent()

    #to iterate over options until a Quit signal is received
    while (True):

        print '\nWhat would you like to do?\n'

        print '\n1. Classify image of your choice:\t'
        print '\n2. 3-Fold Cross-validation on landscape and head-shot data-sets\t'
        print '\n3. K-means clustering on landscape and head-shot data-sets\t'
        print '\n4. Hierarchical clustering on landscape and head-shot data-sets\t'
        print '\n5. Cluster flag images of all sovereign countries\t'
        print '\n6. Evolve one flag into another\t'
        print '\n7. Quit'

        choice = raw_input("\nType your option : \t").strip()
        if choice == "7":
            print "You chose to Quit. Hopefully, you enjoyed my service"
            exit(0)

        elif choice == "1":
            env.classifyImage(iAgent, iProcessor)

        elif choice == "2":
            env.crossValidation(iAgent, iProcessor)

        elif choice == "3":
            env = Environement()
            iProcessor = ImageProcessor()
            iAgent = ImageClassificationAgent()
            env.performKmeansClustering(iAgent, iProcessor)

        elif choice == "4":
            env.loadKnnTrainingData(iProcessor)
            env.performSingleLinkClustering(env.KnnTrainingData.keys(), iAgent)

        elif choice == "5":
            env.loadFlagImages(iProcessor)
            env.performSingleLinkClustering(env.FlagsToCluster.keys(), iAgent)

        elif choice == "6":
            env.evolveOnetoAnother()

        else:
            print '\nYou entered values other than 1, 2, 3, 4, 5, 6, 7. Please try again.'
            continue


if __name__ == '__main__':
    main()
