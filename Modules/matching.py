import cv2
import screeninfo
import numpy as np
import os

from Modules import optcheck, highgui, imgproc, contour
from Modules import PaintingDetector as pd
from matplotlib import pyplot as plt

def match(image, dataSet, topMatchesCount = 5, debug = False):
    """
    Tries to match the given image with an image in the dataset.
    The function shows the 5 most likely matches.
    Parameters
    ----------
        image 
            Image in standard format to match with dataset
        dataSet
            THE dataset
        topMatchesCount
            The top amount of matches to show
        debug
            If set to true, the program will print additional information and open windows
    """
    
    ### Matching stage ###
    # Initiate SIFT detector
    orb = cv2.ORB_create()
    #sift = cv2.SIFT()
    kp_result, desc_result = orb.detectAndCompute(image, None)

    # Create BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    i = 0
    results = []
    for data_set_tuple in dataSet:
        data_set_image = data_set_tuple[0]
        data_set_meta_data = data_set_tuple[1]
        kp_d, desc_d = orb.detectAndCompute(data_set_image, None)
        matches = bf.match(desc_result, desc_d)
        matches = sorted(matches, key = lambda x:x.distance)

        matches_to_use = 20
        matches = matches[:matches_to_use]        
        distance_sum = sum(match.distance for match in matches)

        if debug:
            print('\tPainting', i, 'Sum of matches:', distance_sum)
            #for m in matches:
            #    print('\t', m.distance)

        comparison = cv2.drawMatches(img1 = image, keypoints1 = kp_result, img2 = data_set_image, keypoints2 = kp_d, matches1to2 = matches[:matches_to_use], outImg = None, flags = 2)
        results.append((i, distance_sum, comparison))    
        i += 1

    # Distance is the notion of similiarity
    # The lower the distance, the mr=ore similar detected keypoints are
    # Therefore, the lower the sum of detected mathes, the higher the odds that it is a valid match
    # Sort the results array by the sum associated with the picture
    results = sorted(results, key = lambda x:x[1])

    # Show the best results
    for i in range(topMatchesCount):
        if i == 0:
            cv2.imshow('Best match ->' + str(results[i][0]), results[i][2])
            print('You are located in', dataSet[results[i][0]][1])
        else:
            cv2.imshow(str(results[i][0]), results[i][2])
        print('Painting', results[i][0], 'Sum: of matches', results[i][1])