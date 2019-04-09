import cv2
import numpy
import math
import screeninfo
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd


def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)
    cv2.namedWindow(imagePath)

    paintingDetector = pd.PaintingDetector()
    image = paintingDetector.detectPainting(image, 100, 1)

    # do not resize the image before detecting the lines. A different resolution produces a different output.
	monitor = screeninfo.get_monitors()[0]
    image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height relative to base screen

    highgui.showImage(imagePath, image)
   # highgui.saveImage(image, highgui.getSavePath(imagePath, 'edges'))



if __name__ == '__main__':
    main()