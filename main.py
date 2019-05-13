import screeninfo
import numpy
from sklearn.svm import SVC
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd
from Modules import LocalBinaryPattern as lbd
from Modules import contour

def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.loadImage(imagePath)
    paintingDetector = pd.PaintingDetector()

    # resize image since original has high resolution
    #monitor = screeninfo.get_monitors()[0]
    #image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height relative to base screen
    paintingDetector.detectPainting(image)

if __name__ == '__main__':
    main()