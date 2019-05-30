import cv2
import numpy as np
from Modules import colors, highgui, imgproc


def contour(image):
    """
    Find contours and boxes in an image and attempts to rectify to standard format
    Parameters
    ----------
        image 
            Source image to evaluate
        imagepath
            The path to the image, useful for debugging purposes
        debug
            If set to true, the program will print additional information and open windows. Should be used with one painting
    """

    # Resize and convert to grayscale
    image = cv2.resize(src=image, dsize=(0, 0), dst=None, fx=0.5, fy=0.5)
    #image = cv2.GaussianBlur(src = image, ksize = (5, 5), sigmaX = 1.0)

    gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    # Apply canny edge detector
    thresh1 = 33
    thresh2 = 100
    edges = cv2.Canny(image=gray, threshold1=thresh1, threshold2=thresh2)

        
    # Dilate the canny lines so finding contours is easier
    dilated = cv2.dilate(src=edges, kernel=np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]]))


    # Find contours in image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     


    # Sort the contours by contour area, as paintings will likely have larger contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    box = None
    # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html #4
    # Approximate the contours into a polygon (starting with the largest contour)
    # This will yield the first polygon with 4 points
    for contour in contours:
        polygon = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)  # TODO, goede waarde vinden
        if len(polygon) == 4:
            box = polygon
            break
    
    # TODO: handling additional polygons
    if box is None:
        print('Could not find bounding box of 4 points')
        return highgui.resizeImage(image, (500, 500))

    box = box.reshape(4, 2)
    approx_box = np.zeros((4, 2), dtype="float32")
    
    # Caclulate sum
    sum = box.sum(axis=1)
    approx_box[0] = box[np.argmin(sum)]
    approx_box[2] = box[np.argmax(sum)]
 
    # Calculate difference
    diff = np.diff(box, axis=1)
    approx_box[1] = box[np.argmin(diff)]
    approx_box[3] = box[np.argmax(diff)]

    # Determine width and height of bounding box
    smallest_x = 1000000
    smallest_y = 1000000
    largest_x = -1
    largest_y = -1

    for point in approx_box:
        if point[0] < smallest_x:
            smallest_x = point[0]
        if point[0] > largest_x:
            largest_x = point[0]
        if point[1] < smallest_y:
            smallest_y = point[1]
        if point[1] > largest_y:
            largest_y = point[1]
 
    maxWidth = int(largest_x - smallest_x)
    maxHeight = int(largest_y - smallest_y)

    bounding_box = np.array([
        [0, 0],
        [maxWidth, 0],
        [maxWidth, maxHeight],
        [0, maxHeight]], dtype="float32")

    # Apply transformation
    transform = cv2.getPerspectiveTransform(approx_box, bounding_box)
    result = cv2.warpPerspective(image, transform, (0, 0))

    
    # Crop out of original picture
    extracted = result[0:maxHeight, 0:maxWidth]
    extracted = highgui.resizeImage(extracted, dimension=(500, 500))
    return extracted




































# the class is only used for evaluation
    
class PaintingFinder(object):
    def __init__(self):
        pass

    @classmethod
    def findPainting(self, image):
        contours = self._findContours(image=image)
        polygon = self._findPaintingPolygon(image=image, contours=contours)
        self._transformPainting(image=image, polygon=polygon)

    @classmethod
    def _findContours(self, image):
        """
        Finds contours in an image
        Parameters
        ----------
            image 
                Source image to find contours in
        Returns
        ----------
            A list of contours
        """
        #image = cv2.resize(src=image, dsize=(0, 0), dst=None, fx=0.5, fy=0.5)
        grayscaleImage = imgproc.convertToGrayscale(src=image)
        
        (thresh1, thresh2) = (50, 150)

        edges = cv2.Canny(image=grayscaleImage, threshold1=thresh1, threshold2=thresh2)
        
        # Dilate the canny lines so finding contours is easier
        dilatedImage = cv2.dilate(src=edges, kernel=np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))

        # Find contours in image. We are only interested in outer (EXTERNAL) contours
        contours = cv2.findContours(dilatedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # discard the 'hierarchy' variable

        # Sort the contours by contour area, as paintings will likely have larger contours
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        return contours

    @classmethod
    def _findPaintingPolygon(self, image, contours):
        """
        Attempts to find a bounding box consisting of 4 points
        Parameters
        ----------
            image
                Source image to find the bounding box in
            contours
                A list of contours
        Returns
        ----------
        """
        box = None
        # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html #4
        # Approximate the contours into a polygon (starting with the largest contour)
        # This will yield the first polygon with 4 points

        for contour in contours:
            polygon = cv2.approxPolyDP(curve=contour, epsilon=0.1 * cv2.arcLength(contour, closed=True), closed=True)
            if len(polygon) == 4:
                box = polygon
                break
        # TODO: handling additional polygons

        if box is None:
            print('Could not find box of 4 points')
            # return a polygon containing the whole image
            box = np.ndarray(shape=(4, 1, 2), dtype=np.int32)
            points = [(0, 0), (image.shape[0], 0), (image.shape[0], image.shape[1]), (0, image.shape[1])]
            for i in range(0, len(points)):
                box[i][0][0] = points[i][0]
                box[i][0][1] = points[i][1]

        box = box.reshape(4, 2)
        return box
        
        
    @classmethod
    def _transformPainting(self, image, polygon):

        approxBox = np.zeros((4, 2), dtype='float32') # the polygon that contains the 4 points of the actaul painting
        
        boxSum = polygon.sum(axis = 1)
        approxBox[0] = polygon[np.argmin(boxSum)]
        approxBox[2] = polygon[np.argmax(boxSum)]

        boxDiff = np.diff(polygon, axis = 1)
        approxBox[1] = polygon[np.argmin(boxDiff)]
        approxBox[3] = polygon[np.argmax(boxDiff)]


        # Determine with and height of bounding box
        smallestX = 1000000
        largestX = -1
        smallestY = 1000000
        largestY = -1

        for point in approxBox:
            if point[0] < smallestX:
                smallestX = point[0]
            if point[0] > largestX:
                largestX = point[0]
            if point[1] < smallestY:
                smallestY = point[1]
            if point[1] > largestY:
                largestY = point[1]

        maxWidth = int(largestX - smallestX)
        maxHeight = int(largestY - smallestY)

        boundingBox = np.array([  # the new polygon
            [0, 0],
            [maxWidth, 0],
            [maxWidth, maxHeight],
            [0, maxHeight]
        ], dtype = 'float32')


        transformationMatrix = cv2.getPerspectiveTransform(approxBox, boundingBox)
        transformedImage = cv2.warpPerspective(src=image, M=transformationMatrix, dsize=(0, 0))

        extractedImage = transformedImage[0:maxHeight, 0:maxWidth]

        return extractedImage
