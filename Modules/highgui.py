import cv2
import os

def openImage(image):
    return cv2.imread(image)

def showImage(windowname, image):
    cv2.imshow(windowname, image)
    cv2.waitKey()

def showImagesHorizontally(windowname, *images): 
    showImage(windowname, cv2.hconcat((images)))

def saveImage(image, savePath):
    cv2.imwrite(savePath, image)

def resizeImage(image, dimension):
    return cv2.resize(src = image, dsize = dimension)

def getSavePath(defaultPath, exNumber):
    filepath, filename = os.path.split(defaultPath)
    filename, extension = filename.split(".")
    return f"{filepath}\\{filename}EX{exNumber}.{extension}"
