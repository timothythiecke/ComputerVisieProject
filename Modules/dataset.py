import os
import cv2
from Modules import highgui

def loadImages(debug = False):
    """
    Loads all images of the data set from disk int the Images/DataSet/ folder.
    Then returns an array of tuples containing the image and metadata.
    Currently, metadata is the name of the folder which corresponds to some existing room in the MSK.
    """

    # Load dataset from folders (training)
    data_set = []
    dirs = os.listdir('./Images/DataSet')

    for d in dirs:
        if debug:
            print('Building dataset from', './Images/DataSet/' + d + '/')
        directory = os.fsencode('./Images/DataSet/' + d + '/')
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            image = highgui.openImage('./Images/DataSet/' + d + '/' + filename)
            image = cv2.resize(src = image, dsize = (0, 0), dst = None, fx = 0.125, fy = 0.125) # TODO: parameter?
            data_set.append((image, d)) # Append image and room metadata # TODO: array of tuples or tree like structure?
    
    return data_set