from Modules import imgproc, colors, highgui
import cv2
import numpy as np
# 3 steps:
#   1) Feature detection:   search the image for locations that are likely to match well in other images
#   2) Feature description: convert each region around detected locations into a more compact and invariant descriptor that can be matched against other descriptors
#   3) Feature matching:    search for matches in other images

# https://www.researchgate.net/publication/228697341_Perspective_rectangle_detection
class PaintingDetector():
    @classmethod
    def detectPainting(self, image):
        pass