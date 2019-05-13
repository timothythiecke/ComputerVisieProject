import screeninfo
import numpy
from sklearn.svm import SVC
from Modules import optcheck, highgui, imgproc
from Modules import contour, dataset, matching
from Modules import GroundPlan
from Modules import Validator

def main():
    imagePath = optcheck.getArguments()[0]
    image = highgui.loadImage(imagePath)    
#def match(image, dataSet, topMatchesCount = 5, debug = False):
   # d = dataset.get()
    #matching.match(image = image, dataSet = d)
    validator = Validator.Validator()
    validator.validate()


if __name__ == '__main__':
    main()