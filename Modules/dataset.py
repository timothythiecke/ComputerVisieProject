import os
import cv2
from Modules import highgui
from pathlib import Path
import pickle
import numpy as np



"""
Dataset needs to be persistent as creation takes about 2-3 minutes during each build phase
Data set layout
    Array of arrays
    Each array corresponds to information associated with a painting and contains information in the following layout:
    [ room/directory of painting : str, filename : str, array of keypoints, array of descriptors]
    example:
    [
        ['zaal_A', '20190323_111313.jpg', [ keypoint1, keypoint2, ...], [descriptor1, descriptor2, ...]], 
        ['zaal_B', ..., [...], [...]],
        [...]
    ]

We save the keypoints and descriptors here to save time during the matching phase, as matching is a lot faster than
detecting keypoints and are invariant.
Saving painting directory and name takes up a lot less memory as we only need to show an image when a match is
detected
"""

def buildDataSet(debug = False):
    """
    Builds dataset from all the images in the Images/DataSet/ folders.
    Then returns this information. For an explanation of the layout, check the commentary above.
    Currently, metadata is the name of the folder which corresponds to some existing room in the MSK.
    """

    # Load dataset from folders (training)
    data_set = []
    dirs = os.listdir('./Images/DataSet')

    # Initiate SIFT detector
    orb = cv2.ORB_create()  # TODO: FLANN based matching?

    for d in dirs:
        if debug:
            print('Building dataset entries from', './Images/DataSet/' + d + '/')
        directory = os.fsencode('./Images/DataSet/' + d + '/')
        for file in os.listdir(directory):
            filename = os.fsdecode(file)

            rel_path = './Images/DataSet/' + d + '/' + filename
            
            image = highgui.loadImage(rel_path)
            image = cv2.resize(src=image, dsize=(0, 0), dst=None,
                               fx=0.5, fy=0.5)
            
            kp_d, desc_d = orb.detectAndCompute(image, None)
            
            if debug:
                print('\t', rel_path)

            data_set.append((d, filename, kp_d, desc_d))

    if debug:
        print('Dataset building done!')

    return data_set


def getDataSet(resetPersistence=False, debug=False):
    """
    Gets the dataset, either from disk or creates it and then persists it (through lazy init).
    Parameters
    ----------
        resetPersistence
            If set to True, the old dataset is discarded and built anew
        debug
            Prints additional information to the console
    """

    data_set = []

    data_set_path = 'dataset.dat'
    config = Path(data_set_path)

    # Remove dataset if necessary
    if resetPersistence and config.is_file():
        config.unlink()

    if config.is_file() is False:
        if debug:
            print('Persistent dataset not found! Creating and persisting...')
        config.touch()

        # Create dataset, then persist it
        data_set = buildDataSet(debug)
        with open(data_set_path, 'wb') as f:
            # Prepare dataset for pickling, as pickle can't pickle keypoints by itself
            # We need to transform it into something that is more easily accessible
            # https://stackoverflow.com/questions/10045363/pickling-cv2-keypoint-causes-picklingerror
            data_set_pickled = []
            for data_set_entry in data_set:
                pickled_kps = []
                for point, desc in zip(data_set_entry[2], data_set_entry[3]):  # Iterate over keypoints and descriptors at the same time
                    temp = (point.pt, point.size, point.angle, point.response,
                            point.octave, point.class_id, desc)
                    pickled_kps.append(temp)
                data_set_pickled.append((data_set_entry[0], data_set_entry[1],
                                         pickled_kps))

            pickle.dump(data_set_pickled, f)
 
    else:
        if debug:
            print('Loading persistent dataset from file...')
        # Load dataset from file
        with open(data_set_path, 'rb') as f:
            data_set_prep = pickle.load(f)

            # Change pickled version to usable version
            for entry in data_set_prep:
                keypoints = []
                desc = []
                for pickled_kp in entry[2]:
                    temp_feature = cv2.KeyPoint(x=pickled_kp[0][0], y=pickled_kp[0][1], _size=pickled_kp[1], _angle=pickled_kp[2], _response=pickled_kp[3], _octave=pickled_kp[4], _class_id=pickled_kp[5]) 
                    temp_descriptor = pickled_kp[6]
                    keypoints.append(temp_feature)
                    desc.append(temp_descriptor)

                data_set.append((entry[0], entry[1], keypoints, np.array(desc)))
        if debug:
            print('Dataset loaded!')

    #if debug:
    #    print(data_set)
    return data_set