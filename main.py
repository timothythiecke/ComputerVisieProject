import cv2
import numpy
import math
import screeninfo
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd


def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)
    original = image.copy()
    cv2.namedWindow(imagePath)
    # this function excepts a reference to a function. We actaully want to do nothing
    # using the keyword 'pass' does not work so we just 'add' a number to the trackbarPosition, which does nothing
    cv2.createTrackbar('lowThreshold', imagePath, 50, 500, lambda x: x + 1) # 
    cv2.createTrackbar('ratio', imagePath, 2, 5, lambda x: x + 1)
    while True:    
        lowThreshold = cv2.getTrackbarPos('lowThreshold', imagePath)
        ratio = cv2.getTrackbarPos('ratio', imagePath)
        paintingDetector = pd.PaintingDetector()
        image = paintingDetector.detectPainting(original, lowThreshold, ratio)
        monitor = screeninfo.get_monitors()[0]
        # do not resize the image before detecting the lines. A different resolution produces a different output.
        image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height to base screen
        
        cv2.imshow(imagePath, image)
        ch = cv2.waitKey()
        if(ch == 27): # escape key
            break

if __name__ == '__main__':
    main()