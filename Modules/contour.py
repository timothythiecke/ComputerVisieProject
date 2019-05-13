import cv2
import numpy as np
from Modules import colors, highgui, imgproc


class PaintingFinder(object):
    def __init__(self):
        pass

    @classmethod
    def findPainting(self, image):
        contours = self._findContours(image = image)
        polygon = self._findPaintingPolygon(image = image, contours = contours)
        self._transformPainting(image = image, polygon = polygon)

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
        image = highgui.resizeImage(image = image, dimension = (1000, 1000)) # fixed dimension 1000x1000 pixels
        grayscaleImage = imgproc.convertToGrayscale(src = image)
        
        (thresh1, thresh2) = (33, 100)
        edges = cv2.Canny(image = grayscaleImage, threshold1 = thresh1, threshold2 = thresh2)
        dilatedImage = cv2.dilate(src = edges, kernel = np.array([[1,1,1],[1,1,1],[1,1,1]]))

        contours, hierarchy = cv2.findContours(dilatedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
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
            polygon = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
            if len(polygon) == 4:
                box = polygon
                break
        # TODO: handling additional polygons

        if box is None:
            print('Could not find box of 4 points')
            return None

        #box = box.reshape(4, 2)
        return box
        
        
    @classmethod
    def _transformPainting(self, image, polygon):
        approxBox = np.zeros((4, 2), dtype = 'float32') # the polygon that contains the 4 points of the actaul painting
        boxSum = polygon.sum(axis = 1)
        approxBox[0] = polygon[np.argmin(boxSum)]
        approxBox[2] = polygon[np.argmax(boxSum)]

        boxDiff = np.diff(polygon, axis = 1)
        approxBox[1] = polygon[np.argmin(boxDiff)]
        approxBox[3] = polygon[np.argmax(boxDiff)]


        # Determine with and height of bounding box

        # Initialize values with first point
        smallestX = point[0][0]
        largestX = point[0][0]
        smallestY = point[0][1]
        largestY = point[0][1]

        for i in range(1, len(approxBox)):
            if(point[i][0] < smallestX):
                smallestX = point[i][0]              
            if(point[i][0] > largestX):
                largestX = point[i][0]
            if(point[i][0] < smallestY):
                smallestY = point[i][0]   
            if(point[i][0] < largestY):
                largestY = point[i][0]

        maxWidth = int(largestX - smallestX)
        maxHeight = int(largestY - smallestY)

        boundingBox = np.array([ # the new polygon
            [0, 0],
            [maxWidth, 0],
            [maxWidth, maxHeight],
            [0, maxHeight]
        ], dtype = 'float32')

        transformationMatrix = cv2.getPerspectiveTransform(approxBox, boundingBox)
        transformedImage = cv2.warpPerspective(src = image, M = transformationMatrix, dsize = (0, 0))

        extractedImage = result[0:maxHeight, 0:maxWidth]

        return extractedImage


def contour(image, imagepath = '', debug = False):
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
    image = cv2.resize(src = image, dsize = (0, 0), dst = None, fx = 0.25, fy = 0.25)
    #image = cv2.GaussianBlur(src = image, ksize = (5, 5), sigmaX = 1.0)

    gray = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)

    # Apply canny edge detector
    thresh1 = 33
    thresh2 = 100
    edges = cv2.Canny(image = gray, threshold1 = thresh1, threshold2 = thresh2)
    if debug:
        cv2.imshow(str(imagepath) + 'canny', edges)
        
    # Dilate the canny lines so finding contours is easier
    dilated = cv2.dilate(src = edges, kernel = np.array([[1,1,1],[1,1,1],[1,1,1]]))
    if debug:
        cv2.imshow(str(imagepath) + 'dilate', dilated)

    # Find contours in image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     
    if debug:
        cv2.drawContours(image, contours, -1, colors.GREEN, 2)
        cv2.imshow(str(imagepath), image)
        cv2.waitKey()

    # Sort the contours by contour area, as paintings will likely have larger contours
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    box = None
    # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html #4
    # Approximate the contours into a polygon (starting with the largest contour)
    # This will yield the first polygon with 4 points
    for contour in contours:
        polygon = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True) # TODO, goede waarde vinden
        if len(polygon) == 4:
            box = polygon
            break
    
    # TODO: handling additional polygons
    if box is None:
        print('Could not find bounding box of 4 points')
        return None

    if debug:
        cv2.drawContours(image, [box], -1, colors.RED, 3)
        cv2.imshow(str(imagepath), image)
        cv2.waitKey()
    
    # Determine bounding box
    bounding_box = np.zeros((4, 2), dtype = 'float32')
    approx_box = np.zeros((4, 2), dtype = 'float32')
    idx = 0
    smallest_x = 100000.0
    largest_x = -1.0
    smallest_y = 100000.0
    largest_y = -1.0
    for point in box:
        x = point[0][0]
        y = point[0][1]
        approx_box[idx] = (x, y)

        if x < smallest_x:
            smallest_x = x
        if x > largest_x:
            largest_x = x
        if y < smallest_y:
            smallest_y = y
        if y > largest_y:
            largest_y = y
        idx += 1

    width = largest_x - smallest_x
    height = largest_y - smallest_y

    bounding_box[0] = (0.0, 0.0)
    bounding_box[1] = (width, 0.0)
    bounding_box[2] = (width, height)
    bounding_box[3] = (0.0, height)

    # Assert that order of points is equivalent to bounding_box
    # By using distance from edge points of image
    # TODO: I believe this can be simplified but works in an early version
    temp = np.copy(approx_box)
    top_left = -1
    top_right = -1
    bottom_left = -1
    bottom_right = -1
    dist_top_left = 1000000.0
    dist_top_right = 1000000.0
    dist_bottom_left = 1000000.0
    dist_bottom_right = 1000000.0

    idx = 0
    for point in temp:
        x = point[0]
        y = point[1]
            
        # Distance to zero
        dist = np.sqrt((x ** 2) + (y ** 2))
        if dist < dist_top_left:
            top_left = idx
            dist_top_left = dist

        # Distance to top right
        dist = np.sqrt(((x - image.shape[0]) ** 2) + ((y - 0.0) ** 2))
        if dist < dist_top_right:
            top_right = idx
            dist_top_right = dist

        # Distance to bottom right
        dist = np.sqrt(((x - image.shape[0]) ** 2) + ((y - image.shape[1]) ** 2))
        if dist < dist_bottom_right:
            bottom_right = idx
            dist_bottom_right = dist

        # Distance to bottom left
        dist = np.sqrt(((x - 0.0) ** 2) + ((y - image.shape[1]) ** 2))
        if dist < dist_bottom_left:
            bottom_left = idx
            dist_bottom_left = dist

        idx += 1
            
    approx_box[0] = temp[top_left]
    approx_box[1] = temp[top_right]
    approx_box[2] = temp[bottom_right]
    approx_box[3] = temp[bottom_left]

    # Apply transformation (homography)
    transform = cv2.getPerspectiveTransform(approx_box, bounding_box)
    result = cv2.warpPerspective(image, transform, (0, 0))

    if debug:
        cv2.imshow(str(imagepath) + 'result', result)
        print(bounding_box)
        print(bounding_box[2])
    
    # Crop out of original picture
    extracted = result[0:int(bounding_box[2][1]), 0:int(bounding_box[2][0])]
    
    if debug:
        cv2.imshow(str(imagepath) + 'crop', extracted)

    return extracted