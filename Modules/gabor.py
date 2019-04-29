import cv2
import numpy as np

def segmentImage(image):
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


######
# 2 DATA met meerdere features
######
# Data in vorige was 50 elementen in z, met elk een array
# Nu 50 elementen met elk array van 2 elementen
# Eerste kolom komt overeen met feature 1
# Eerste kolom komt overeen met feature 2 #in geval van gabor filter komt dit overeen met de response waarde

    
    #cv2.imshow('image', resized)
    #print(resized.shape)
    # https://www.mathworks.com/help/images/texture-segmentation-using-gabor-filters.html
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html
    # http://www.pami.uwaterloo.ca/pub/hammouda/sd775-paper.pdf # Read this paper

    resized = np.zeros((0, 0))
    resize_scale = 0.25
    resized = cv2.resize(image, (0,0), resized, resize_scale, resize_scale)

    # Convert image to grayscale
    grayscale = np.zeros((0, 0))
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('grayscale', grayscale)

    
    # Init
    sigmas =  [ 0.5, 1.5, 2.5]#, 3.5, 4.5, 5.0] #[7.0, 8.0, 9.0, 10.0, 11.0, 12.0] #[ 0.5, 1.5, 2.5, 3.5]
    thetas = [0.0, 1/6, 1/3, 0.5, 2/3, 5/6] #, 1.0]#, 1.25, 1.5, 1.75] # vanaf 1.0 pi is de kernel volledig symmetrisch met 0
    lambdas = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    #lambdas = [3.0]
    psis = [0.0]#, 1/6, 1/3, 0.5, 2/3, 5/6]
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
    # True -> Adds X, Y coordinate to feature vector
    # True -> Adds RGB color of pixel to feature vector
    use_position = True 
    use_RGB = False 

    data_set_rows = gabor_iterations
    if use_position:
        data_set_rows += 2
    if use_RGB:
        data_set_rows += 3

    data_set = np.zeros((resized.shape[0] * resized.shape[1], data_set_rows)) # Rows determined by amount of pixels in picture
    print(data_set.shape)

    if use_position or use_RGB:
        for i in range(resized.shape[0]):
            for j in range(resized.shape[1]):
                one_d_index = (i * resized.shape[1]) + j
                col = gabor_iterations
                if use_position: # A possible heuristic might be to have the pixels in the middle have a heavier average
                    #alpha = j / resized.shape[1]
                    #if alpha < 0.5:
                    #    data_set[one_d_index, col] = alpha
                    #elif alpha > 0.5:
                    #    data_set[one_d_index, col] = 1.0 - alpha
                    #col += 1
                    #alpha = i / resized.shape[0]
                    #if alpha < 0.5:
                    #    data_set[one_d_index, col] = alpha
                    #elif alpha > 0.5:
                    #    data_set[one_d_index, col] = 1.0 - alpha
                    #col += 1
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

    #data_set[2][25] = 1337
    #data_set[2, 25] = 1337
    #print(data_set[2])

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
        response = cv2.filter2D(src = grayscale, ddepth = cv2.CV_64F, kernel = np.power(gaussian, 2), dst = response)
        #cv2.imshow('filtered' + str(i), response)
        #print(response)

        normalized = np.zeros((0,0))
        normalized = cv2.normalize(src = response, dst = normalized, alpha = 255.0, beta = 0.0, norm_type = cv2.NORM_MINMAX)
        #cv2.imshow('normalized' + str(i), normalized.astype(np.uint8)) # Hierbij gaat enorm veel precizie verloren (enkel nuttig om te visualizeren)

        #print(normalized)
        #print(normalized.astype(np.uint8))

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(src = normalized)
        #print(minVal, maxVal)

        # Then, per pixel, store in dataset
        # Or, per block, store in dataset
        #print(response)
        #print(response.flatten())
        data_set[:, i] = np.array(response.flatten())

        #TODO: iterate over pixels, store position and RGB value in data_set as last columns


    '''# Each pixel now has a feature vector associated with it
    # We could segment the image into smaller blocks (like lab 6) to reduce the amount of feature vectors
    # 16 x 16?, requires image to be scaled into something divisble by 16
    # Append x,y information of block/pixel to feature vector'''

    # Use the magnitude of the feature vectors
    #print(np.linalg.norm(data_set[2][0:gabor_iterations]))
    columns = 1
    if use_position:
        columns += 2
    if use_RGB:
        columns += 3
    data_set_magnitude = np.zeros(((resized.shape[0] * resized.shape[1], columns)))

    # Copy from first dataset to new data set
    for i in range(resized.shape[0] * resized.shape[1]):
        data_set_magnitude[i][0] = np.linalg.norm(data_set[i][0:gabor_iterations])
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

    print(data_set_magnitude)

    # Apply kmeans clustering
    # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Set flags (Just to avoid line break in the code)
    flags = cv2.KMEANS_PP_CENTERS 

    '''print(data_set[2])
    print(np.float32(data_set)) # A little bit of precision is lost'''

    # Apply KMeans
    compactness,labels,centers = cv2.kmeans(np.float32(data_set_magnitude), 3, None,criteria, 10, flags) #Kmeans expects float32 TODO, does it change the values?
    #print(labels)

    # The elements of the labels array define which class at a certain element the pixel belongs to
    # Based on this we can draw an image
    output = np.zeros((resized.shape))
    for i in range(resized.shape[0]):
        for j in range(resized.shape[1]):
            one_d_index = (i * resized.shape[1]) + j
            if labels[one_d_index] == 0:
                output[i, j] = (200, 0, 0)
            if labels[one_d_index] == 1:
                output[i, j] = (0, 200, 0)
            if labels[one_d_index] == 2:
                output[i, j] = (0, 0, 200)
            if labels[one_d_index] == 3:
                output[i, j] = (0, 200, 200)
            if labels[one_d_index] == 4:
                output[i, j] = (200, 0, 200)

    return output