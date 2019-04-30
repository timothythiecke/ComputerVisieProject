import cv2
import numpy as np
from Modules import colors

def calculate(image, debug = False):
    """
    Calculates and stores local binary patterns of an image
    Parameters
    ----------
        image 
            Grayscale version of source image as this is needed to apply the filter bank, ideally scaled down to fit in the bounds of a monitor
    Returns
    ---------
        output
            The local binary pattern image
    """

    resized = np.zeros((0, 0))
    resize_scale = 0.125
    resized = cv2.resize(image, (0,0), resized, resize_scale, resize_scale)
    if debug:
        print('Resizing input image to scale ', resize_scale)

    # Convert image to grayscale
    if debug:
        print('Converting resized image to grayscale')
    grayscale = np.zeros((0, 0))
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('lbp_grayscale', grayscale)

    # Iterate over every pixel

    # Determine kernel around pixel
    # Apply threshold, everything below is set to 0, everything above and equal is set to 1
    # Multiply with 3x3 power of two matrix (not matrix multiplication!) # Convolve?
    # Sum each element, this is a value between 0 and 255

    # Radius and threshold should be parameters of function
    # Radius 1 -> pixels straight around
    # Radius 2 -> pixel -2 + 2 etc
    # Radius 3 -> etc ...

    # Edge pixels komen niet in aanmerking en zijn per default 0

    threshold = 128

    #output = np.zeros((resized.shape[0], resized.shape[1]))
    output = grayscale
    kernel = np.zeros((3, 3))
    binary_mat = np.zeros((3, 3))
    result = np.zeros((3, 3))
    binary_value = 1
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                binary_mat[i, j] = binary_value
                binary_value *= 2
    
    if debug:
        print(binary_mat)

    for row in range(grayscale.shape[0]):       # rows
        for col in range(grayscale.shape[1]):   # cols
            #print(grayscale[i, j])
            # TODO: implement radius / edge pixels
            if row > 0 and row < grayscale.shape[0] - 1 and col > 0 and col < grayscale.shape[1] - 1:
                kernel = grayscale[row-1:row+2, col-1:col+2]
                retval, dst = cv2.threshold(src = kernel, thresh = threshold, maxval = 1, type = cv2.THRESH_BINARY)
                for i in range(3):
                    for j in range(3):
                        result[i, j] = dst[i, j] * binary_mat[i, j]

                output[row, col] = int(np.sum(result))
            else:
                output[row, col] = 0

    if debug:
        print(output)
    
    return output