import cv2
import os
import colors


def loadImage(imagePath):
    """
    Loads and returns an image
    Parameters
    ----------
        imagePath : string
            The absolute or relative path pointing to an image.
    Returns
    -------
        The image
    """
    return cv2.imread(imagePath)


def showImage(windowname, image):
    """
    Displays an image in the specified window
    """

    cv2.imshow(windowname, image)
    cv2.waitKey()

def drawLines(image, lines):
    """
    Draws lines which are the result of the HoughLinesP function onto the image.
    """
    if lines is not None:
        for line in lines:
            line = line[0] # a line is a 2D array for compatibility with C++, but will only contain one row, which contains 4 numerical values
            
            cv2.line(img=image,
                    pt1=(line[0], line[1]), pt2=(line[2], line[3]),
                    color=colors.GREEN, thickness=5, lineType=cv2.LINE_AA)


def drawPoints(image, points, color):
    """
    Draws circles around intersections.
    """
    for point in points:
        x = point[0]
        y = point[1]
        cv2.circle(img = image, center = (int(x), int(y)), radius = 5, color = color, thickness=5)


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
