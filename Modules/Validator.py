import csv
import pickle
from Contour import PaintingFinder
import highgui, imgproc, colors
import numpy as np
from math import sqrt
import cv2
PATH = 'Images/ValidationSet'






class Validator(object):
    """
    This class measures the performance of the painting segmentation algorithm
    """
    def __init__(self):
        self.images = []
        self.groundTruth = []
        dataSet = pickle.load(open(f"{PATH}/GT.txt", 'rb'))
        for entry in dataSet[5:]: # first entry is ill-formatted
            imageName = entry[0]
            points = entry[1:5]
            self.images.append(imageName)
            self.groundTruth.extend([points])



    def validate(self):
        paintingFinder = PaintingFinder()
        for i in range(0, 1):#range(0, len(self.images)):
            imageName = self.images[i]
            print(f"{PATH}/{imageName}")
            
            image = highgui.loadImage(imagePath = f"{PATH}/{imageName}")
            image = highgui.resizeImage(image = image, dimension = (1000, 1000))
            contours = paintingFinder._findContours(image = image)
            polygon = paintingFinder._findPaintingPolygon(image = image, contours = contours)
            if polygon is None:
                continue # to next picture
         
            # convert the point arrays to a standard array format
            groundTruthPoints = []
            predictedPoints = []

            
            for j in range(0, 4):
                predictedPoints.append((polygon[j][0][0], polygon[j][0][1]))
                groundTruthPoints.append((self.groundTruth[i][j][0], self.groundTruth[i][j][1]))
        
            # for visual purposes
            for j in range(0, 4):
                cv2.line(img = image, pt1 = (predictedPoints[j%4][0], predictedPoints[j%4][1]), pt2 = (predictedPoints[(j + 1) % 4][0], predictedPoints[(j + 1) % 4][1]),color=colors.GREEN, thickness= 10)
                cv2.line(img = image, pt1 = (groundTruthPoints[j%4][0], groundTruthPoints[j%4][1]), pt2 = (groundTruthPoints[(j + 1) % 4][0], groundTruthPoints[(j + 1) % 4][1]),color=colors.RED, thickness = 10)
            #highgui.showImage("canvas", image)


            groundTruthInContourFormat = np.ndarray(shape=(4, 1, 2), dtype=np.int32)
            for i in range(0, len(groundTruthPoints)):
                groundTruthInContourFormat[i][0][0] = groundTruthPoints[i][0]
                groundTruthInContourFormat[i][0][1] = groundTruthPoints[i][1]
       

            areaPrediction = 0
            areaGroundTruth = 0
            areaIntersection = 0
            for x in range(0, 1000):
                for y in (range(0, 1000)):
                    pointIsInPrediction = cv2.pointPolygonTest(contour = polygon, pt = (x, y), measureDist = False) > 0
                    pointIsInGroundTruth = cv2.pointPolygonTest(contour = groundTruthInContourFormat, pt = (x, y), measureDist = False) > 0

                    areaPrediction += pointIsInPrediction == True
                    areaGroundTruth += pointIsInGroundTruth == True
                    areaPrediction += (pointIsInPrediction == True and pointIsInGroundTruth == True)

            print(areaPrediction, areaGroundTruth, areaIntersection)
val =  Validator()
val.validate()