import cv2 as cv
import numpy as np
from Utils import *

class Image:
    def __init__(self, pathFolder, fileName, maxWH = None):
        # Initialize a number of global variables
        self.path = str(pathFolder + fileName)
        self.id = fileName.split(".")[0]
        self.imageRGB = self.readImage(maxWH)
        self.imageGray = cv.cvtColor(self.imageRGB, cv.COLOR_BGR2GRAY)
        self.image_height, self.image_width = self.imageRGB.shape[:2]
        self.keyPoints = None
        self.des = None
        # Pose Estimation
        self.relativeTransformation = {}
        self.absoluteTransformation = {}
        # used in Point_Cloud
        self.points_2D_used  = []
        self.descriptor_used = []
        self.points_3D_used  = []
        


    def show_image(image):
        cv2.imshow(image)


    ###################################################################
    ##            ''' Read image and resize it with '''              ##
    ###################################################################
    def readImage(self, sizeValue = None):
        img = cv.imread(self.path)
        if sizeValue != None:
            h, w = img.shape[:2]
            if h>sizeValue and w>sizeValue:
                img = self.__image_resize(img, width  = sizeValue, height = sizeValue) 
            elif h>w and h>sizeValue:
                img = self.__image_resize(img, height = sizeValue)
            elif w>h and h>sizeValue: 
                 img = self.__image_resize(img, width  = sizeValue)
                
        return img


    ###################################################################
    ##           ''' Detect Keypoint and describe it '''             ##
    ###################################################################
    def keyPointDetector(self, detector):
        # find the keypoints and descriptors with detector ( sift, surf, orb)
        self.keyPoints, self.des = detector.detectAndCompute(self.imageGray,None)
        #Not used
        # self.points = np.around(np.float32([ keyPoint.pt for keyPoint in self.keyPoints ]).reshape(-1,2), decimals=0)
            

    ######################################################################################
    ## ''' Redimentionner l'image en gardant le Ratio , Choix du Width ou du Height ''' ##
    ######################################################################################
    def __image_resize(self, image, width = None, height = None, inter = cv.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized
    

    def setRelativePose(self, Image, Rot, Trans):
        self.relativeTransformation["img"] = Image
        self.relativeTransformation["rotation"] = Rot
        self.relativeTransformation["translation"] = Trans
        self.relativeTransformation["transform"] = poseRt(Rot, Trans)


    def setAbsolutePose(self, Rot, Trans):
        self.absoluteTransformation["rotation"] = Rot
        self.absoluteTransformation["translation"] = Trans
        self.absoluteTransformation["transform"] = poseRt(Rot, Trans)
        self.absoluteTransformation["projection"] = projection_from_transformation(poseRt(Rot, Trans))
