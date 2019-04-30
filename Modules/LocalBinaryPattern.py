import cv2
import numpy as np
from Modules import colors, highgui, imgproc


class LocalBinaryPattern(object):
    @classmethod
    def __init__(self):
        self.CELL_SIZE = 16

    @classmethod
    def getFeatureVectorForImage(self, image, radius):
        image = highgui.resizeImage(image, (880, 640))
        image = imgproc.convertToGrayscale(image)
        (height, width) = image.shape[0:2]
        featureVector = [] 
        # 1. Divide image into cells
        for i in range(0, height, self.CELL_SIZE):
            for j in range(0, width, self.CELL_SIZE):
                cell = image[i:i + self.CELL_SIZE, j:j + self.CELL_SIZE]
                # 2. For each pixel in a cell, compare the pixel to each of its 8 neighbors (on its left-top, left-middle, left-bottom, right-top, etc.). Follow the pixels along a circle, i.e. clockwise or counter-clockwise.
                values = [] # the decimal representation of all the pixel values of the cell
                for x in range(0, self.CELL_SIZE):
                    for y in range(0, self.CELL_SIZE):
                        # 3. Where the center pixel's value is greater than the neighbor's value, write "0". Otherwise, write "1". This gives an 8-digit binary number (which is usually converted to decimal for convenience).
                        value = 0 # decimal representation of the binary pattern
                        middle = cell[x][y]
                        neighbours = (cell[x-radius:x+radius+1, y-radius:y+radius+1]).flatten() # neighbourmatrix
                        for k in range(0, len(neighbours)): # from top left to bottom right
                            if(neighbours[k] >= middle):
                                value += (2 ** k) # problem, midddle value also gets calculated
                        values.append(value)
                # 4. Compute the histogram, over the cell, of the frequency of each "number" occurring (i.e., each combination of which pixels are smaller and which are greater than the center). This histogram can be seen as a 256-dimensional feature vector.
                histogram = [0] * 256
                for value in values:
                    histogram[value] += 1 # increase frequency for each occurance of value
                # 5. Concatenate (normalized) histograms of all cells. This gives a feature vector for the entire window.
                featureVector.extend([histogram])    
        print(featureVector)
