
import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt

from Modules import highgui
from Modules import colors

from Modules.Contour import PaintingFinder
from Modules.Matching import Matcher
from Modules.Dataset import getDataSet


PATH = 'Images/ValidationSet'


class Evaluator(object):
    """
    This class measures the performance of the full algorithm
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
        """
        Evaluate the segmentation algorithm.
        """
        paintingFinder = PaintingFinder()
        percentages = []
        for i in range(0, len(self.images)):
            imageName = self.images[i]
            print(f"{PATH}/{imageName}")
            
            image = highgui.loadImage(imagePath=f"{PATH}/{imageName}")
            image = highgui.resizeImage(image=image, dimension=(1000, 1000))
            contours = paintingFinder._findContours(image=image)
            polygon = paintingFinder._findPaintingPolygon(image=image, contours=contours)
            if polygon is None:
                continue  # to next picture
         
            # convert the point arrays to a standard array format
            groundTruthPoints = []
            predictedPoints = []

            for j in range(0, 4):
                predictedPoints.append((polygon[j][0], polygon[j][1]))
                groundTruthPoints.append((self.groundTruth[i][j][0], self.groundTruth[i][j][1]))
        
            groundTruthInContourFormat = np.ndarray(shape=(4, 1, 2), dtype=np.int32)
            for i in range(0, len(groundTruthPoints)):
                groundTruthInContourFormat[i][0][0] = groundTruthPoints[i][0]
                groundTruthInContourFormat[i][0][1] = groundTruthPoints[i][1]
       
            cv2.drawContours(image, [polygon], -1, colors.GREEN, 3)
            cv2.drawContours(image, [groundTruthInContourFormat], -1, colors.RED, 3)
            highgui.showImage("Segmentation Evaluation", image, 1000)
            areaPrediction = 0
            areaGroundTruth = 0
            areaIntersection = 0
            for x in range(0, 1000):
                for y in (range(0, 1000)):
                    pointIsInPrediction = cv2.pointPolygonTest(contour=polygon, pt=(x, y), measureDist=False) > 0
                    pointIsInGroundTruth = cv2.pointPolygonTest(contour=groundTruthInContourFormat, pt=(x, y), measureDist=False) > 0

                    areaPrediction += pointIsInPrediction is True
                    areaGroundTruth += pointIsInGroundTruth is True
                    areaIntersection += (pointIsInPrediction is True and pointIsInGroundTruth is True)

            if(areaIntersection == areaGroundTruth and areaPrediction > areaGroundTruth):
                areaGroundTruth, areaPrediction = areaPrediction, areaGroundTruth
            
                                # swap areas when green polygon encloses red polygon
                
            ratio = areaIntersection / (areaGroundTruth / 100)
            
    
            print(areaPrediction, areaGroundTruth, areaIntersection, ":", ratio , "% match")
            percentages.append(ratio)
            #highgui.showImage("canvas", image)
        
        groups = [0] * 10
        for percentage in sorted(percentages):
            index = int((percentage - (percentage % 10))/10)
            groups[index] += 1

        print("Average: ", sum(percentages) / len(percentages))

        indices = np.arange(10)
        fig, ax = plt.subplots()
        ax.bar(indices, groups, 0.4, color='SkyBlue')
        plt.title("Overview of segmentation correctness")
        plt.ylabel('Count')
        plt.xlabel('Percentage group')
        ax.set_xticks(indices)
        ax.set_xticklabels(('0-10', '10-20','20-30', '30-40','40-50','50-60','60-70','70-80','80-90','90-100'))
        plt.show()


    def evaluteMatching(self):
        dataSet = getDataSet()
        matcher = Matcher(dataSet)

        for i in range(0, len(self.images)):
            imageName = self.images[i]
            image = highgui.loadImage(imagePath=f"{PATH}/{imageName}")
            image = highgui.resizeImage(image=image, dimension=(500, 500))
            matches = matcher.match(image, topMatchesCount=1)

            imagePath = './Images/DataSet/' + dataSet[matches[0][0]][0] + '/' + dataSet[matches[0][0]][1]
            data_set_image = highgui.loadImage(imagePath)
            resized = np.zeros((0, 0))
            scale = 0.125
            resized = cv2.resize(src=data_set_image, dsize=(0, 0), dst=resized, fx=scale, fy=scale)

            # Generate comparison image between extracted and dataset    
            comparison = cv2.drawMatches(img1=image, keypoints1=matches[0][2], img2=resized, keypoints2=matches[0][3], matches1to2=matches[0][4],   outImg=None, flags=2)
            highgui.showImage("compare", comparison, delay=0)


evaluator = Evaluator()
evaluator.evaluateSegmentation()