import csv
import pickle
import matplotlib.pyplot as plt
from Modules import highgui
from Modules import imgproc
from Modules import colors
import numpy as np
import cv2

from Modules.Contour import PaintingFinder
from Modules.Matching import Matcher
from Modules.Dataset import getDataSet

from math import sqrt


PATH = 'Images/ValidationSet'


class Evaluator(object):
    """
    This class measures the performance of the painting segmentation algorithm
    """
    def __init__(self):
        self.images = []
        self.groundTruth = []
        dataSet = pickle.load(open(f"{PATH}/GT.txt", 'rb'))
        for entry in dataSet: 
            imageName = entry[0]
            points = entry[1:5]
            self.images.append(imageName)
            self.groundTruth.extend([points])

        print(self.images)


    def evaluateSegmentation(self):
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
                continue  # to next picture
         
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
                
                # swap areas when green polygon encloses red polygon
                if(areaIntersection == areaGroundTruth and areaPrediction > areaGroundTruth):
                    areaGroundTruth, areaPrediction = areaPrediction, areaGroundTruth
                ratio = areaIntersection / (areaGroundTruth / 100)
            except:
                ratio = 0
                print("no intersection")
            print(areaPrediction, areaGroundTruth, areaIntersection, ":", ratio , "% match")
            percentages.append(ratio)
            #highgui.showImage("canvas", image)
        
        print(sum(percentages) / len(percentages))

    def evaluteMatching(self):
        dataSet = getDataSet()
        matcher = Matcher(dataSet)

        for i in range(0, len(self.images)):
            imageName = self.images[i]
            image = highgui.loadImage(imagePath = f"{PATH}/{imageName}")
            image = highgui.resizeImage(image = image, dimension = (1000, 1000))
            #image = cv2.resize(src = image, dsize = (0, 0), dst = None, fx = 0.5, fy = 0.5)
            matches = matcher.match(image, topMatchesCount = 1)

            imagePath = './Images/DataSet/' + dataSet[matches[0][0]][0] + '/' + dataSet[matches[0][0]][1]
            data_set_image = highgui.loadImage(imagePath)
            resized = np.zeros((0, 0))
            scale = 0.125
            resized = cv2.resize(src = data_set_image, dsize = (0, 0), dst = resized, fx = scale, fy = scale)

            # Generate comparison image between extracted and dataset    
            comparison = cv2.drawMatches(img1 = image, keypoints1 = matches[0][2], img2 = resized, keypoints2 = matches[0][3], matches1to2=matches[0][4],   outImg=None, flags = 2)
            highgui.showImage("compare", comparison)
            

            
evaluator =  Evaluator()
evaluator.evaluteMatching()