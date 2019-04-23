import numpy
import cv2
import itertools
from math import sqrt
from Modules import imgproc, colors, highgui

# 3 steps:
#   1) Feature detection:   search the image for locations that are likely to match well in other images
#   2) Feature description: convert each region around detected locations into a more compact and invariant descriptor that can be matched against other descriptors
#   3) Feature matching:    search for matches in other images


class PaintingDetector():
    @classmethod
    def detectPainting(self, image, lowThreshold, ratio):
        lines = self._getLines(image=image, lowThreshold=lowThreshold, ratio=ratio, rho=1, theta=numpy.pi/180)
        self._findVanishingPoint(image, self._findIntersections(lines))
        highgui.drawLines(image, lines)
        highgui.drawIntersections(image, self._findIntersections(lines))
        return image

    @classmethod
    def _findIntersections(self, lines):
        intersections = []
            # based on https://stackoverflow.com/questions/4543506/algorithm-for-intersection-of-2-lines
        if lines is not None:
            for i in range(0, len(lines)):
                # A1 * X + B1 * Y = C1
                (x1, y1, x2, y2) = (lines[i][0][0], lines[i][0][1], lines[i][0][2] ,lines[i][0][3]) 
                A1 = y2 - y1
                B1 = x1 - x2
                C1 = A1 * x1 + B1 * y1
                for j in range(1, len(lines)):   
                    # A2 * X + B1 * 2 = C2        
                    (x3, y3, x4, y4) = (lines[j][0][0], lines[j][0][1], lines[j][0][2] ,lines[j][0][3]) 
                    A2 = y4 - y3
                    B2 = x3 - x4
                    C2 = A2 * x3 + B2 * y3
                    delta = A1 * B2 - A2 * B1
                    if delta != 0:
                        x = int((B2 * C1 - B1 * C2) / delta)
                        y = int((A1 * C2 - A2 * C1) / delta)
                        intersections.append((x , y))
        return intersections
    
    @classmethod
    def _findVanishingPoint(self, image, intersections):
        imageHeight = image.shape[0]
        imageWidth = image.shape[1]

        gridSize = min(imageHeight, imageWidth) // 3

        gridRows = (imageHeight // gridSize) + 1
        gridColumns = (imageWidth // gridSize) + 1

        maxIntersections = 0
        vanishingPoint = (0, 0)

        for i, j in itertools.product(range(gridRows), range(gridColumns)):
            left = i * gridSize
            right = (i + 1) * gridSize
            bottom = j * gridSize
            top = (j + 1) * gridSize
            cv2.rectangle(image, (left, bottom), (right,top), colors.ORANGE, 2)

            currentIntersections = 0
            for x, y in intersections:
                if left < x < right and bottom < y < top:
                    currentIntersections += 1
            
            if currentIntersections > maxIntersections:
                maxIntersections = currentIntersections
                vanishingPoint = ((left + right) / 2, (bottom + top) / 2)
        
        x1 = int(vanishingPoint[0] - gridSize / 2)
        y1 = int(vanishingPoint[1] - gridSize / 2)
        x2 = int(vanishingPoint[0] + gridSize / 2)
        y2 = int(vanishingPoint[1] + gridSize / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), colors.CYAN, 2)
    @classmethod
    def _getLines(self, image, lowThreshold, ratio, rho, theta):
        """
        Returns a list of lines in an image using the Hough space.
        """
        image = imgproc.convertToGrayscale(image)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, numpy.ones((15, 15), numpy.uint8))
        edges = cv2.Canny(image=image,
                          threshold1=lowThreshold,
                          threshold2=lowThreshold * ratio,
                          apertureSize=3, # 3 seems to be a perfect apertureSize, 5 is too much
                          L2gradient=True)
        lines = cv2.HoughLinesP(image=edges,
                                rho=rho, theta=theta,
                                threshold=100, maxLineGap=500) # take high line gap because the original pictures have a high resolution
        
        return lines