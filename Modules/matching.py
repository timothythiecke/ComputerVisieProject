import cv2
import screeninfo
import numpy as np
import os

from Modules import optcheck, highgui, imgproc, contour
from Modules import PaintingDetector as pd
from matplotlib import pyplot as plt

def match():
    #TODO: Temp code

    # Load dataset (training)
    data_set = []
    directory = os.fsencode('./Images/DataSet/Zaal_B/')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        image = highgui.openImage('./Images/DataSet/Zaal_B/' + filename)
        image = cv2.resize(src = image, dsize = (0, 0), dst = None, fx = 0.125, fy = 0.125)
        gray = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
        data_set.append(gray)
        
        # TODO: Good features to track veranderen
        #corners = cv2.goodFeaturesToTrack(image = gray, maxCorners = 20, qualityLevel = 0.01, minDistance = 10)
        #for corner in corners:
        #    cv2.circle(image, (corner[0][0], corner[0][1]), 4, (0, 255, 0), 2)    

        #cv2.imshow(filename, image)
        #contour.contour(image, './Images/Zaal_A/' + filename)
    

    # Load query image and contour it
    imagePath = optcheck.getArguments()[0]
    image = highgui.openImage(imagePath)
    result = contour.contour(image, 'imagepath', True)


    ### Matching stage ###
    # Initiate SIFT detector
    orb = cv2.ORB_create()
    #sift = cv2.SIFT()
    kp_result, desc_result = orb.detectAndCompute(result, None)

    # Create BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    i = 0
    for data_set_image in data_set:
        kp_d, desc_d = orb.detectAndCompute(data_set_image, None)
        matches = bf.match(desc_result, desc_d)
        matches = sorted(matches, key = lambda x:x.distance)
        comparison = cv2.drawMatches(img1 = result, keypoints1 = kp_result, img2 = data_set_image, keypoints2 = kp_d, matches1to2 = matches[:20], outImg = None, flags = 2)
        cv2.imshow(str(i), comparison)
        i += 1