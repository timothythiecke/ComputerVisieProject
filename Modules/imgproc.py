import cv2


def convertToGrayscale(src):
    """
    Converts the src image to grayscale and returns the result.
    """
<<<<<<< HEAD
    return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


def binaryThreshold(src, ratio):
    """
    Applies a binary threshold on a grayscale src image. The ratio specifies at which grayscale value it should switch from black to white. 
    A ratio of 0.5 makes every pixel with a value < 127 black and every pixel with avalue >= 127 white
    """
    retval, dst = cv2.threshold(src, ratio * 255, 255, cv2.THRESH_BINARY)
    return dst


def unsharpMasking(src, kernelSize):
    """
    Sharpens the given src image and uses a (kernelSize x kernelSize) matrix
    """
    blurredImage = cv2.GaussianBlur(src, (kernelSize, kernelSize), 0) 
    diff = cv2.absdiff(src, blurredImage)
    unsharpImage = cv2.add(diff, src)
    return unsharpImage


def getDoGFilter(size, sigmabig, sigmasmall, angle):
    gaussianColumnMatrix = numpy.array(cv2.getGaussianKernel(ksize = size, sigma = sigmabig))
    gaussianRowMatrix = numpy.transpose(cv2.getGaussianKernel(ksize = size, sigma = sigmasmall))
    squareMatrix = numpy.zeros((size, size))
    for i in range(0, size):
        squareMatrix[i][int((size - 1) / 2)] = gaussianColumnMatrix[i]
    gaussian2D = cv2.filter2D(src = squareMatrix, ddepth = -1, kernel = gaussianRowMatrix)
    gaussian2D = cv2.Sobel(src = gaussian2D, ddepth = -1, dx = 1, dy = 0, ksize = 3)
    rotationMatrix = cv2.getRotationMatrix2D(center = ((int(size / 2), int(size / 2))), angle = angle, scale = 1)
    DogFilter = cv2.warpAffine(src = gaussian2D, M = rotationMatrix, dsize = (size, size))
    return DogFilter


def extractEdges(image, angle):
    result = cv2.convertScaleAbs(cv2.filter2D(convertToGrayscale(image), cv2.CV_32F, getDoGFilter(75, 20, 1, -15)))
    return result


def detectLines(image, threshold1, threshold2, rho, theta):
    result = image.copy()
    image = convertToGrayscale(image)
    edges = cv2.Canny(image = image, threshold1 = threshold1, threshold2 = threshold2, L2gradient = True)
    lines = cv2.HoughLinesP(image = edges, rho = rho, theta = theta, threshold = 30, maxLineGap = 10)
    for line in lines:
        cv2.line(img = result,
                 pt1 = (line[0][0], line[0][1]), pt2 = (line[0][2], line[0][3]), 
                 color = (0,255,0), thickness = 1, lineType = cv2.LINE_AA)    
    return result


def detectCorners(image):
    corners_image = cv2.goodFeaturesToTrack(image = convertToGrayscale(image), maxCorners = 100, qualityLevel = 0.01, minDistance = 2)
    for point in corners_image:
        x = point[0][0]
        y = point[0][1]
        cv2.circle(image, (x, y), 1, (0, 255, 0), 3)


def detectORBFeatures(image, nfeatures):
    keypoints, descriptors = getORBFeatures(image, nfeatures)
    for kp in keypoints:
        x = int(kp.pt[0])
        y = int(kp.pt[1])
        cv2.circle(image, (x, y), 1, (0, 255, 0), 3)


def getORBFeatures(image, nfeatures):
    orb = cv2.ORB_create(nfeatures = nfeatures)
    keypoints, descriptors = orb.detectAndCompute(image = image, mask = None)
    return (keypoints, descriptors)


def matchORBFeatures(image1, image2, nfeatures, nmatches):
    keypoints1, descriptors1 = getORBFeatures(image1, nfeatures)
    keypoints2, descriptors2 = getORBFeatures(image2, nfeatures)
    bf = cv2.BFMatcher_create(normType = cv2.NORM_HAMMING2, crossCheck = True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key = lambda x:x.distance)
    matches = matches[:nmatches]
    result = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches, None, matchColor=(0, 255, 0), flags = 2) 
    return result
=======
    return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
>>>>>>> b35a41e0ac24c253bb580ac94f8487a69d4f1fcd
