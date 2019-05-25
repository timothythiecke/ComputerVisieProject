import cv2
import numpy as np
from Modules import optcheck, highgui, imgproc, matching


path = optcheck.getArguments()[0]
image = highgui.loadImage(path)
image = highgui.resizeImage(image,( 1000, 1000))
image = imgproc.convertToGrayscale(src = image)
image = cv2.Canny(image, 50, 150)
contours,hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(contours)
