import cv2
import numpy as np
from Modules import colors

def segmentImage(image, debug = False):
    """
    Segments image in three by applying gabor filters
    Parameters
    ----------
        image 
            Grayscale version of source image as this is needed to apply the filter bank, ideally scaled down to fit in the bounds of a monitor
    Returns
    ---------
        output
            Image segmented in three colors
    """
    # Additional info
    # https://www.mathworks.com/help/images/texture-segmentation-using-gabor-filters.html
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html
    # http://www.pami.uwaterloo.ca/pub/hammouda/sd775-paper.pdf # Read this paper

    # Resize image to a smaller format
    # TODO: should be a function argument?
    resized = np.zeros((0, 0))
    resize_scale = 0.25
    resized = cv2.resize(image, (0,0), resized, resize_scale, resize_scale)

    # Convert image to grayscale
    grayscale = np.zeros((0, 0))
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('gabor_grayscale', grayscale)
    
    # Init of filter bank parameters
    # TODO: these values need to be tweaked as they do not yield a perfect result yet
    sigmas =  [ 0.5, 1.5, 2.5]
    thetas = [0.0, 1/6, 1/3, 0.5, 2/3, 5/6]
    lambdas = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    psis = [0.0]
    gamma = 1.0 
    kernel_size = 17

    # Create gabor filter bank
    gabor_iterations = len(sigmas) * len(thetas) * len(lambdas) * len(psis)
    filter_bank = [None] * gabor_iterations
    i = 0

    for sigma in sigmas:
        for theta in thetas:
            for lambd in lambdas:
                for psi in psis:
                    gabor_kernel = np.zeros((0, 0))
                    gabor_kernel = cv2.getGaborKernel(ksize = (kernel_size, kernel_size), sigma = sigma, theta = np.pi * theta, lambd = lambd, gamma = gamma, psi = np.pi * psi)
                    filter_bank[i] = gabor_kernel
                    i += 1

    # Create data set for kmeans
    # Rows determined by amount of pixels in picture
    # Dataset will be Nx(M+O+P) where N is the amount of pixels, M the amount of filters in the bank,
    # O two additional columns for coordinate of pixel and P three additional columns for RGB color value
    # True/False -> Adds/omits X, Y coordinate to feature vector
    # True/False -> Adds/omits RGB color of pixel to feature vector
    use_position = True 
    use_RGB = False 

    data_set_rows = gabor_iterations
    if use_position:
        data_set_rows += 2
    if use_RGB:
        data_set_rows += 3

    data_set = np.zeros((resized.shape[0] * resized.shape[1], data_set_rows))
    if debug:
        print('Dataset shape: ', data_set.shape)

    if use_position or use_RGB:
        for i in range(resized.shape[0]):
            for j in range(resized.shape[1]):
                one_d_index = (i * resized.shape[1]) + j
                col = gabor_iterations
                if use_position: # A possible heuristic might be to have the pixels in the middle have a heavier average
                    data_set[one_d_index, col] = j
                    col += 1
                    data_set[one_d_index, col] = i
                    col += 1

                if use_RGB == 1:
                    data_set[one_d_index, col] = resized[i, j][0]
                    col += 1
                    data_set[one_d_index, col] = resized[i, j][1]
                    col += 1
                    data_set[one_d_index, col] = resized[i, j][2]
                    col += 1

    if debug:
        print('Third row of data set: ', data_set[2])

    # Apply gabor filters and fill up data_set
    for i in range(gabor_iterations):
        # Filter grayscale image with filter banks => responses
        # Sometimes gabor magnitude, gabor energy
        # TODO: sometimes, a small gaussian blur is used to remove noise
        
        gaussian = np.zeros((0, 0))
        #gaussian = filter_bank[i]
        sigma = 0.0
        gaussian = cv2.GaussianBlur(src = filter_bank[i], ksize = (11, 11), sigmaX = sigma, sigmaY = sigma)

        response = np.zeros((0, 0))
        #response = cv2.filter2D(src = grayscale, ddepth = cv2.CV_64F, kernel = np.power(gaussian, 2), dst = response)
        response = cv2.filter2D(src = grayscale, ddepth = cv2.CV_64F, kernel = gaussian, dst = response)

        # Visualize response
        normalized = np.zeros((0,0))
        normalized = cv2.normalize(src = response, dst = normalized, alpha = 255.0, beta = 0.0, norm_type = cv2.NORM_MINMAX)
        #cv2.imshow('normalized' + str(i), normalized.astype(np.uint8)) # A lot of precision is lost, it is only useful for visualization purposes

        # Determine min and max value (currently only debug)
        #minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(src = normalized)
        #print(minVal, maxVal)

        # Then, per pixel, store in dataset
        # Or, per block, store in dataset
        #print(response)
        #print(response.flatten())
        data_set[:, i] = np.array(response.flatten())


    '''# Each pixel now has a feature vector associated with it
    # We could segment the image into smaller blocks (like lab 6) to reduce the amount of feature vectors
    # 16 x 16?, requires image to be scaled into something divisble by 16
    # Append x,y information of block/pixel to feature vector'''

    # Use the magnitude of the feature vectors (responses of gabor filters)
    columns = 1
    if use_position:
        columns += 2
    if use_RGB:
        columns += 3
    data_set_magnitude = np.zeros(((resized.shape[0] * resized.shape[1], columns)))

    # Copy from first dataset to new data set
    # TODO: this part can be reduced to a more simple python numpy assignment
    for i in range(resized.shape[0] * resized.shape[1]):
        #data_set_magnitude[i][0] = np.linalg.norm(data_set[i][0:gabor_iterations])
        v = data_set[i][0:gabor_iterations]
        data_set_magnitude[i][0] = np.sqrt(v.dot(v))
        col = 1
        if use_position:
            data_set_magnitude[i][col] = data_set[i][gabor_iterations + col - 1]
            col += 1
            data_set_magnitude[i][col] = data_set[i][gabor_iterations + col - 1]
            col += 1
        if use_RGB:
            data_set_magnitude[i][col] = data_set[i][gabor_iterations + col - 1]
            col += 1
            data_set_magnitude[i][col] = data_set[i][gabor_iterations + col - 1]
            col += 1
            data_set_magnitude[i][col] = data_set[i][gabor_iterations + col - 1]
            col += 1

    if debug:
        print(data_set_magnitude)

    # Apply kmeans clustering
    # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Set flags
    flags = cv2.KMEANS_PP_CENTERS 

    # Check precision loss
    '''print(data_set[2])
    print(np.float32(data_set)) # A little bit of precision is lost'''

    # Apply KMeans
    clusters = 3
    compactness,labels,centers = cv2.kmeans(np.float32(data_set_magnitude), clusters, None,criteria, 10, flags) #Kmeans expects float32 TODO, does it change the values? see above
    
    if debug:
        print('Labels array: ', labels)

    # The elements of the labels array define which class at a certain element the pixel belongs to
    # Based on this we can draw an image
    output = np.zeros((resized.shape))
    for i in range(resized.shape[0]):
        for j in range(resized.shape[1]):
            one_d_index = (i * resized.shape[1]) + j
            if labels[one_d_index] == 0:
                output[i, j] = colors.GREEN
            if labels[one_d_index] == 1:
                output[i, j] = colors.RED
            if labels[one_d_index] == 2:
                output[i, j] = colors.BLUE
            if labels[one_d_index] == 3:
                output[i, j] = colors.CYAN
            if labels[one_d_index] == 4:
                output[i, j] = colors.ORANGE

    return output