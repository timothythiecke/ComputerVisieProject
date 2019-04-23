import cv2
import os
from Modules import colors


def openImage(imagePath):
    """
    Opens and returns an image
    Parameters
    ----------
        imagePath : string
            The absolute or relative path pointing to an image.
    Returns
    -------
        The image
    """
    return cv2.imread(imagePath)


def showImage(image, windowname):
    """
    Displays an image in the specified window
    """
    cv2.imshow(windowname, image)
    cv2.waitKey()

<<<<<<< HEAD
=======
def drawLines(image, lines):
    """
    Draws lines which are the result of the HoughLinesP function onto the image.
    """
    if lines is not None:
        for line in lines:
            line = line[0] # a line is a 2D array for compatibility with C++, but will only contain one row, which contains 4 numerical values
            cv2.line(img=image,
                    pt1=(line[0], line[1]), pt2=(line[2], line[3]),
                    color=colors.GREEN, thickness=2, lineType=cv2.LINE_AA)


def drawIntersections(image, lines):
    """
    Draws circles around intersections between lines.
    """
    # based on https://stackoverflow.com/questions/4543506/algorithm-for-intersection-of-2-lines
    if lines is not None:
        for i in range(0, len(lines)):
            # A1 * X + B1 * Y = C1
            (x1, y1, x2, y2) = (lines[i][0][0], lines[i][0][1], lines[i][0][2] ,lines[i][0][3]) 
            A1 = y2 - y1
            B1 = x1 - x2
            C1 = A1 * x1 + B1 * y1
            for j in range(1, len(lines)):   
                # A2 * X + B1 * 2 = C2        
                (x3, y3, x4, y4) = (lines[j][0][0], lines[j][0][1], lines[j][0][2] ,lines[j][0][3]) 
                A2 = y4 - y3
                B2 = x3 - x4
                C2 = A2 * x3 + B2 * y3
                delta = A1 * B2 - A2 * B1
                if delta != 0:
                    x = int((B2 * C1 - B1 * C2) / delta)
                    y = int((A1 * C2 - A2 * C1) / delta)
                    cv2.circle(img = image, center = (x, y), radius = 5, color = colors.RED, thickness=2)

>>>>>>> b35a41e0ac24c253bb580ac94f8487a69d4f1fcd

def showImagesHorizontally(windowname, *images): 
    """
    Shows multiple images horizontally in the specified window
    """
    showImage(windowname, cv2.hconcat((images)))


def saveImage(image, savePath):
    """
    Saves an image to the specified file.
    """
    cv2.imwrite(savePath, image)


def resizeImage(image, dimension):
    """
    Resizes the image to the given dimension
    Parameters
    ----------
        image : numpy.ndarray
            The image to resize
        dimension : tuple
            A tuple (width, height) representing the dimension to resize to
    Returns
    -------
            The resized image
    """
    return cv2.resize(src=image, dsize=dimension)


def getSavePath(defaultPath, extra):
    """
    Gets a new save path which points to the same folder of the original image,
    but allows to add a different name at the end of the original filename, before the extension.
    """
    filepath, filename = os.path.split(defaultPath)
    filename, extension = filename.split(".")
    return f"{filepath}\\{filename}{extra}.{extension}"
