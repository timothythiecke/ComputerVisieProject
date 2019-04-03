import cv2
import numpy
import math
import screeninfo
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd

def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)

    monitor = screeninfo.get_monitors()[0]
    image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height to base screen
    
    paintingDetector = pd.PaintingDetector()
    image = paintingDetector.detectPainting(image)

    highgui.showImage("name",image)
 

if __name__ == '__main__':
    main()