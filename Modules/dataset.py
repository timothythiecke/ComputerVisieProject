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


class DataSet():

    
    @staticmethod
    def buildDataSet():
        """
        Builds dataset from all the images in the Images/DataSet/ folders.
        Then returns this information. For an explanation of the layout, check the commentary above.
        Currently, metadata is the name of the folder which corresponds to some existing room in the MSK.
        """
        dataSet = []
        directories = os.listdir('./Images/DataSet')
        orb = cv2.ORB_create() # TODO: FLANN based matching?

        for directory in directories:
            path = './Images/DataSet/' + d + '/'
            for file in os.listdir(os.fsencode(path)):
                filename = os.fsdecode(file)
                image = highgui.loadImage(path + filename)
                image = highgui.resizeImage(image = image, dimension = (1000, 1000))
                keypoints, descriptors = orb.detectAndCompute(image, None)

                dataSet.append((directory, filename, keypoints, descriptors))

        return dataSet


    @staticmethod
    def getDataSet(resetPersistence = False):
        """
        Gets the dataset, either from disk or creates it and then persists it (through lazy init).
        Parameters
        ----------
            resetPersistence
                If set to True, the old dataset is discarded and built anew
        """

        dataSet = []
        dataSetPath = 'dataset.dat'
        config = Path(dataSetPath)
        if resetPersistence == True and dataSetPath.is_file():
            config.unlink()
            
        if config.is_file() == False:
            
            config.touch()
            dataSet = self.buildDataSet()
            with open(dataSetPath, 'wb') as f:
                # Prepare dataset for pickling, as pickle can't pickle keypoints by itself
                # We need to transform it into something that is more easily accessible
                # https://stackoverflow.com/questions/10045363/pickling-cv2-keypoint-causes-picklingerror
                pickleDataSet = []
                for entry in dataSet:
                    pickleKeypoints = []
                    for keypoint, descriptor in zip(entry[2], entry[3]): # Iterate over keypoints and descriptors at the same time
                        pickleKeypoints.append((keypoint.pt, keypoint.size, keypoint.angle, keypoint.response, keypoint.octave, keypoint.class_id, descriptor))
                    pickleDataSet.append((entry[0], entry[1], pickleKeypoints))
                pickle.dump(pickleDataSet, f)

        else:
            with open(dataSetPath, 'rb') as f:
                pickleDataSet = pickle.load(f)
                for entry in pickleDataSet:
                    (keypoints, descriptors) = ([], [])
                    for keypoint in entry[2]:
                        keypoints.append(cv2.KeyPoint(x = keypoint[0][0], y = keypoint[0][1], _size = keypoint[1], _angle = keypoint[2], _response = keypoint[3], _octave = keypoint[4], _class_id = keypoint[5]))
                        descriptors.append(keypoint[6])
                    dataSet.append((entry[0], entry[1], keypoints, descriptors))
        return dataSet
 