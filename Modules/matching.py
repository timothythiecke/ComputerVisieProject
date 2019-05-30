import cv2
import screeninfo
import numpy as np
import os
import random

from Modules import optcheck, highgui, imgproc


class Matcher(object):
    def __init__(self, dataset):
        self.dataset = dataset

    
    def match(self, image):
        """
        Tries to match the given image with an image in the dataset.
        The function shows the 5 most likely matches.
        Parameters
        ----------
            image 
                Image in standard format to match with dataset
            topMatchesCount
                The top amount of matches to show. Will default to 1 when dealing with video frames.
            frameIndex
                Current frame being matched with. -1 when dealing with pictures, >-1 when dealing with video frames.
            groundPlanQueue
                Put result of matching on this queue. Another thread will deal with this information. None when dealing with pictures, a queue object when  dealing with video frames.
            debug
                If set to true, the program will print additional information and open windows
        """

        orb = cv2.ORB_create(nfeatures=300)
        keypoints, descriptors = orb.detectAndCompute(image, mask=None)

        # Create BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        i = 0
        smallest_detected_sum_of_distances = 100000000000.0
        results = []
        for data_set_tuple in self.dataset:
            kp_d = data_set_tuple[2]
            desc_d = data_set_tuple[3]
            matches = bf.match(descriptors, desc_d)
            matches = sorted(matches, key=lambda x: x.distance)

            matches_to_use = 20
            matches = matches[:matches_to_use]
            distance_sum = sum(match.distance for match in matches)

            # Only append to results if the match is likely to be more similar to speed up lookup
            if distance_sum < smallest_detected_sum_of_distances:
                smallest_detected_sum_of_distances = distance_sum
                results.append((i, distance_sum, keypoints, kp_d, matches[:matches_to_use]))    
            
            i += 1


        # Distance is the notion of similiarity
        # The lower the distance, the more similar detected keypoints are
        # Therefore, the lower the sum of detected mathes, the higher the odds that it is a valid match
        # Sort the results array by the sum associated with the picture
        results = sorted(results, key=lambda x: x[1])
        if(len(results) == 1):  # no match found
            image = highgui.loadImage('./Images/no-image-found.png')
            room = self.dataset[results[0][0]][0].split('_')[1]
        else:
            # return the best result
            predictedPaintingPath = './Images/DataSet/' + self.dataset[results[0][0]][0] + '/' + self.dataset[results[0][0]][1]
            image = highgui.loadImage(predictedPaintingPath)
            room = -1
        
        image = cv2.resize(src=image, dsize=(500, 500))
        
        return (image, room) # return image and room which it resides in