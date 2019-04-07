import numpy
import cv2
from Modules import imgproc, colors

class PaintingDetector():
    @classmethod
    def detectPainting(self, image, lowThreshold, ratio):
        # canny recommends an upper:lower ratio between 2:1 and 3:1
        image = self._detectLines(image=image, lowThreshold=lowThreshold, ratio=ratio, rho=1, theta=numpy.pi/180)
        return image

    @classmethod
    def _detectLines(self, image, lowThreshold, ratio, rho, theta):
        result = image.copy()
        image = imgproc.convertToGrayscale(image)
        edges = cv2.Canny(image=image,
                          threshold1=lowThreshold,
                          threshold2=lowThreshold * ratio,
                          apertureSize=3,
                          L2gradient=True)
        lines = cv2.HoughLinesP(image=edges,
                                rho=rho, theta=theta,
                                minLineLength=100,
                                threshold=50, maxLineGap=10)
        if lines is not None:
            for line in lines:
                cv2.line(img=result,
                        pt1=(line[0][0], line[0][1]), pt2=(line[0][2], line[0][3]),
                        color=colors.GREEN, thickness=2, lineType=cv2.LINE_AA)
            
        return result

    @classmethod
    def _detectRectangles(self, image, lowThreshold, ratio):
        image = imgproc.convertToGrayscale(image)
        edges = cv2.Canny(image=image, threshold1=lowThreshold, threshold2=lowThreshold * ratio)
        contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_TREE , method=cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=colors.GREEN, thickness = 2)

