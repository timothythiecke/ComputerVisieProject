import screeninfo
import numpy
from sklearn.svm import SVC
from Modules import optcheck, highgui, imgproc
from Modules import contour, GroundPlan

def main():
    groundPlan = GroundPlan.GroundPlan()
    groundPlan.markVisited('1')
    groundPlan.markVisited('2')
    groundPlan.markVisited('4')
    groundPlan.markVisited('5')
    groundPlan.visualize()

if __name__ == '__main__':
    main()