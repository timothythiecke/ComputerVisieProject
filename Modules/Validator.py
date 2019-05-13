import csv
from Modules import contour, highgui, colors
from math import sqrt
import cv2
PATH = 'Images/ValidationSet'



class Validator(object):
    """
    This class measures the performance of the painting segmentation algorithm
    """
    def __init__(self):
        self.groundTruth = {}
        self.images = []
        with open(f"{PATH}/GT.txt", "r") as groundTruthFile:
            reader = csv.reader(groundTruthFile, delimiter = ' ')
            for row in reader:
                self.groundTruth[f"{row[0]}"] = []
                self.images.append(row[0])
                for i in range(1, 5):
                    x, y = row[i].split(',')
                    self.groundTruth[f"{row[0]}"].append((float(x), float(y)))   


    def validate(self):
        paintingFinder = contour.PaintingFinder()
        
        for imageName in (self.images):
            print(f"{PATH}/{imageName}")
            image = highgui.loadImage(imagePath = f"{PATH}/{imageName}")
            image = highgui.resizeImage(image = image, dimension = (1000, 1000))
            contours = paintingFinder._findContours(image = image)
            polygon = paintingFinder._findPaintingPolygon(image = image, contours = contours)
            if polygon is not None:
                for i in range(0, len(polygon)):
                    #compare polygon points with ground truth points
                    (x1, y1) = polygon[i][0]
                    (x2, y2) = self.groundTruth[imageName][i]
                    diffX = abs(x2 - x1)
                    diffY = abs(y2 - y1)
                    # use distance as a measurement of how far of two points are.
                    # other measurements possible?
                    distance = sqrt(diffX * diffX + diffY * diffY)