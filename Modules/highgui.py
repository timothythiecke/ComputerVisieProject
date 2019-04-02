import cv2
import os


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


def getSavePath(defaultPath, exNumber):
    filepath, filename = os.path.split(defaultPath)
    filename, extension = filename.split(".")
    return f"{filepath}\\{filename}EX{exNumber}.{extension}"
