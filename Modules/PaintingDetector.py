import numpy
import cv2
from Modules import imgproc

class PaintingDetector():
    @classmethod
    def detectPainting(self, image):
        image = self._detectLines(image = image, lowThreshold = 100, ratio = 2,
                                       rho = 1, theta = numpy.pi / 180)
        return image

    @classmethod
    def _detectLines(self, image, lowThreshold, ratio, rho, theta):
        result = image.copy()
        image = imgproc.convertToGrayscale(image)
        # canny recommends an upper:lower ratio between 2:1 and 3:1
        edges = cv2.Canny(image = image, threshold1 = lowThreshold, threshold2 = lowThreshold * ratio, L2gradient = True)
        lines = cv2.HoughLinesP(image = edges, rho = rho, theta = theta, threshold = 30, maxLineGap = 10)
        for line in lines:
            cv2.line(img = result, pt1 = (line[0][0], line[0][1]), pt2 = (line[0][2], line[0][3]), color = (0,255,0), thickness = 2, lineType = cv2.LINE_AA)    
        return result

    @classmethod
    def _detectRectangles(image, lowThreshold, ratio):
        grayImage = convertToGrayscale(image)
        edges = cv2.Canny(image = grayImage, threshold1 = lowThreshold, threshold2 = lowThreshold * ratio)
        contours, hierarchy = cv2.findContours(image = edges, mode = cv2.RETR_TREE , method = cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image = image, contours = contours, contourIdx = -1, color = (0, 0 , 255), thickness = 2)