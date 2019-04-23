import cv2


def convertToGrayscale(src):
    """
    Converts the src image to grayscale and returns the result.
    """
    return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
