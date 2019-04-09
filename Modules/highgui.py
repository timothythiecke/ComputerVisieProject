import cv2
import os
from Modules import colors

def openImage(image):
    return cv2.imread(image)

def showImage(windowname, image):
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
                    color=colors.GREEN, thickness=2, lineType=cv2.LINE_AA)

def drawIntersections(image, lines):
	"""
	Draws circles around intersections between lines.
	"""

	# based on https://stackoverflow.com/questions/4543506/algorithm-for-intersection-of-2-lines
	if lines is not None:
		for i in range(0, len(lines)):
			(x1, y1, x2, y2) = (lines[i][0][0], lines[i][0][1], lines[i][0][2] ,lines[i][0][3]) 
			for j in range(1, len(lines)):			
				(x3, y3, x4, y4) = (lines[j][0][0], lines[j][0][1], lines[j][0][2] ,lines[j][0][3]) 
				delta = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
				if delta != 0:
					x = int(((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / delta)
					y = int(((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / delta)
					cv2.circle(img = image, center = (x, y), radius = 10, color = colors.RED, thickness=2)


def showImagesHorizontally(windowname, *images): 
    showImage(windowname, cv2.hconcat((images)))

def saveImage(image, savePath):
    cv2.imwrite(savePath, image)

def resizeImage(image, dimension):
    return cv2.resize(src = image, dsize = dimension)

def getSavePath(defaultPath, extra):
    """
    Gets a new save path which points to the same folder of the original image,
    but allows to add a different name at the end of the original filename, before the extension.
    """
    filepath, filename = os.path.split(defaultPath)
    filename, extension = filename.split(".")
    return f"{filepath}\\{filename}{extra}.{extension}"
