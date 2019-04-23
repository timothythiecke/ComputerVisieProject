import screeninfo
import numpy
from Modules import optcheck, highgui, imgproc
from Modules import PaintingDetector as pd



def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)
    paintingDetector = pd.PaintingDetector()

    # resize image since original has high resolution
    monitor = screeninfo.get_monitors()[0]
    image = highgui.resizeImage(image, (monitor.width >> 1, monitor.height >> 1)) # adjust width and height relative to base screen

    image = paintingDetector.detectPainting(image, lowThreshold = 100, ratio = 2)



    highgui.showImage(imagePath, image)
    #highgui.saveImage(image, highgui.getSavePath(imagePath, 'edges'))



if __name__ == '__main__':
    main()