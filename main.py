import cv2
import numpy
import math
from Modules import optcheck, highgui, imgproc
def main():
    imagePath = optcheck.getArguments()[0]
    image = cv2.resize(highgui.openImage(imagePath), (800, 800))
    
    image = imgproc.detectLines(image, 100, 200)
    highgui.showImage("name",image)
    #highgui.saveImage(image, highgui.getSavePath(imagePath, '11'))
 

if __name__ == '__main__':
    main()