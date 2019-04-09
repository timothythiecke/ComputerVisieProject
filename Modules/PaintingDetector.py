import numpy
import cv2
from Modules import imgproc, colors, highgui

class PaintingDetector():
    @classmethod
    def detectPainting(self, image, lowThreshold, ratio):
        # canny recommends an upper:lower ratio between 2:1 and 3:1
        lines = self._getLines(image=image, lowThreshold=lowThreshold, ratio=ratio, rho=1, theta=numpy.pi/180)
        highgui.drawLines(image, lines)
        highgui.drawIntersections(image, lines)
        return image

    @classmethod
    def _getLines(self, image, lowThreshold, ratio, rho, theta):
        image = imgproc.convertToGrayscale(image)
        edges = cv2.Canny(image=image,
                          threshold1=lowThreshold,
                          threshold2=lowThreshold * ratio,
                          apertureSize=3, # 3 seems to be a perfect apertureSize, 5 is too much
                          L2gradient=True)
        lines = cv2.HoughLinesP(image=edges,
                                rho=rho, theta=theta,
                                threshold=100, maxLineGap=500) # take high line gap because the original pictures have a high resolution
        
        return lines

    @classmethod
    def _detectRectangles(self, image, lowThreshold, ratio):
        image = imgproc.convertToGrayscale(image)
        edges = cv2.Canny(image=image, threshold1=lowThreshold, threshold2=lowThreshold * ratio)
        contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_TREE , method=cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=colors.GREEN, thickness = 2)

