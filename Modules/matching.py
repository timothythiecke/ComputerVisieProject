import cv2
import screeninfo
import numpy as np
import os
import random

from Modules  import optcheck, highgui, imgproc




class Matcher(object):
    def __init__(self, dataset):
        self.dataset = dataset

    
    def match(self, image, topMatchesCount=5, frameIndex=-1, groundPlanQueue=None, debug=False):
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

        orb = cv2.ORB_create(200)
        kp_result, desc_result = orb.detectAndCompute(image, None)

        # Create BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        i = 0
        smallest_detected_sum_of_distances = 100000000000.0
        results = []
        for data_set_tuple in self.dataset:
            kp_d = data_set_tuple[2]
            desc_d = data_set_tuple[3]
            matches = bf.match(desc_result, desc_d)
            matches = sorted(matches, key=lambda x: x.distance)

            matches_to_use = 20
            matches = matches[:matches_to_use]        
            distance_sum = sum(match.distance for match in matches)

            if debug:
                print('\tPainting', i, 'Sum of matches:', distance_sum, end = "")

            # Only append to results if the match is likely to be more similar to speed up lookup
            if distance_sum < smallest_detected_sum_of_distances:
                smallest_detected_sum_of_distances = distance_sum
                results.append((i, distance_sum, kp_result, kp_d, matches[:matches_to_use]))    

            i += 1

        if debug:
            print('\nMatching done!', 'Sorting results by smallest sum...')

        # Distance is the notion of similiarity
        # The lower the distance, the more similar detected keypoints are
        # Therefore, the lower the sum of detected mathes, the higher the odds that it is a valid match
        # Sort the results array by the sum associated with the picture
        results = sorted(results, key = lambda x:x[1])
        return results


def match(image, dataSet, topMatchesCount=5, frameIndex=-1, groundPlanQueue=None, debug=False):
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
            The top amount of matches to show. Will default to 1 when dealing with video frames.
        frameIndex
            Current frame being matched with. -1 when dealing with pictures, >-1 when dealing with video frames.
        groundPlanQueue
            Put result of matching on this queue. Another thread will deal with this information. None when dealing with pictures, a queue object when dealing with video frames.
        debug
            If set to true, the program will print additional information and open windows
    """
    if debug:
        print('Starting matching procedure...')

    ### Matching stage ###
    # Initiate SIFT detector
    orb = cv2.ORB_create(200)
    kp_result, desc_result = orb.detectAndCompute(image, None)

    # Create BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    i = 0
    smallest_detected_sum_of_distances = 100000000000.0
    results = []
    for data_set_tuple in dataSet:
        kp_d = data_set_tuple[2]
        desc_d = data_set_tuple[3]
        matches = bf.match(desc_result, desc_d)
        matches = sorted(matches, key=lambda x: x.distance)

        matches_to_use = 20
        matches = matches[:matches_to_use]
        distance_sum = sum(match.distance for match in matches)

        if debug:
            print('\tPainting', i, 'Sum of matches:', distance_sum, end="")

        # Only append to results if the match is likely to be more similar to speed up lookup
        if distance_sum < smallest_detected_sum_of_distances:
            smallest_detected_sum_of_distances = distance_sum
            results.append((i, distance_sum, kp_result, kp_d, matches[:matches_to_use]))    
        
        i += 1

    if debug:
        print('\nMatching done!', 'Sorting results by smallest sum...')

    # Distance is the notion of similiarity
    # The lower the distance, the more similar detected keypoints are
    # Therefore, the lower the sum of detected mathes, the higher the odds that it is a valid match
    # Sort the results array by the sum associated with the picture
    results = sorted(results, key = lambda x:x[1])

    # Show the best results
    # Note: showing the best results does not work well with videoframes/multithreading
    if groundPlanQueue is not None:
        if frameIndex > -1:
            topMatchesCount = 1

    for i in range(topMatchesCount):
        best_frame = 'Best match frame ' + str(frameIndex) + ' top' + str(i)
        image_path = './Images/DataSet/' + dataSet[results[i][0]][0] + '/' + dataSet[results[i][0]][1]
        data_set_image = highgui.loadImage(image_path)
        resized = np.zeros((0, 0))
        scale = 0.125
        resized = cv2.resize(src=data_set_image, dsize=(0, 0), dst=resized, fx=scale, fy=scale)

        # Generate comparison image between extracted and dataset    
        comparison = cv2.drawMatches(img1=image, keypoints1=results[i][2], img2=resized, keypoints2=results[i][3], matches1to2=results[i][4], outImg=None, flags=2)
        cv2.imshow(best_frame, comparison)
        
        # Put the meta data on the queue so the groundPlanConsumer can process it
        print('Painting', image_path, 'with index', results[i][0], 'is estimated to be the painting.', 'You are located in', dataSet[results[i][0]][0])
        if groundPlanQueue is not None:
            zaal = dataSet[results[i][0]][0].split('_')[1]
            groundPlanQueue.put(zaal, block=False)

        # Show the match for a while on screen, then destroy the window
        if frameIndex != -1:
            cv2.waitKey(3000)
            cv2.destroyWindow(best_frame)

# Thread will stop here