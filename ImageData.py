class ImageData:
    #this class simulates an Image object with attributes mentioned below

    imageName = None
    label = None
    imageData = None
    featureVector = []
    imageFilePath = None
    imageActualName = None
    clusterId = None
    group = None

    #every landscape, headshot and flag image is converted in an ImageData object using this constructor
    def __init__(self, nameStr, feature, labelStr, actualNameStr):
        self.imageName = nameStr
        self.featureVector = feature
        self.label = labelStr
        self.imageActualName = actualNameStr
