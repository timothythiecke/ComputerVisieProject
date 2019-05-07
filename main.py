import screeninfo
import numpy
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd
from Modules import LocalBinaryPattern as lbd

def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)
    paintingDetector = pd.PaintingDetector()

    # resize image since original has high resolution
    #monitor = screeninfo.get_monitors()[0]
    #image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height relative to base screen

    # canny recommends an upper:lower ratio between 2:1 and 3:1
    # IDEA: to determine threshold: start high and if no rectangle could be found, lower the thresholds
    #image = paintingDetector.detectPainting(image, lowCannyThreshold = 50, cannyRatio = 3, houghThreshold = 75)
    #highgui.showImage(imagePath, image)
    #highgui.saveImage(image, highgui.getSavePath(imagePath, 'edges'))
    localBinaryPattern = lbd.LocalBinaryPattern()
    localBinaryPattern.getFeatureVectorForImage(image, radius = 1)
    #gabor.segmentImage(image, True)
  #  highgui.showImage(imagePath, segmentation)

if __name__ == '__main__':
    main()