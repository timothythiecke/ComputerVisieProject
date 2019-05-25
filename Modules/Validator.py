import csv
import pickle
import matplotlib.pyplot as plt
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

        percentages = []
        for i in range(0, len(self.images)):
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
        

            groundTruthInContourFormat = np.ndarray(shape=(4, 1, 2), dtype=np.int32)
            for i in range(0, len(groundTruthPoints)):
                groundTruthInContourFormat[i][0][0] = groundTruthPoints[i][0]
                groundTruthInContourFormat[i][0][1] = groundTruthPoints[i][1]
       
            cv2.drawContours(image, [polygon], -1, colors.GREEN, 3)
            cv2.drawContours(image, [groundTruthInContourFormat], -1, colors.RED, 3)

            areaPrediction = 0
            areaGroundTruth = 0
            areaIntersection = 0
            for x in range(0, 1000):
                for y in (range(0, 1000)):
                    pointIsInPrediction = cv2.pointPolygonTest(contour = polygon, pt = (x, y), measureDist = False) > 0
                    pointIsInGroundTruth = cv2.pointPolygonTest(contour = groundTruthInContourFormat, pt = (x, y), measureDist = False) > 0

                    areaPrediction += pointIsInPrediction == True
                    areaGroundTruth += pointIsInGroundTruth == True
                    areaIntersection += (pointIsInPrediction == True and pointIsInGroundTruth == True)
            try:
                ratio = areaIntersection / (areaGroundTruth / 100)
            except:
                ratio = 0
                print("no intersection")
            print(areaPrediction, areaGroundTruth, areaIntersection, ":", ratio , "% match")
            percentages.append(ratio)
           # highgui.showImage("canvas", image)
        
        print(sum(percentages) / len(percentages))

            
val =  Validator()
val.validate()