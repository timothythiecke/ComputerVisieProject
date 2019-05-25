import screeninfo
import numpy
import cv2
import numpy as np
from Modules.Dataset import DataSet
from Modules.GroundPlan import GroundPlan
from Modules.Contour import contour, drawOnVideoFrame
from concurrent.futures import ThreadPoolExecutor
from Modules import optcheck, highgui, imgproc, matching

def main():
    videoPath = optcheck.getArguments()[0]
    dataSet = DataSet.getDataSet()
    groundPlan = GroundPlan()
    #paintingFinder = PaintingFinder()
    capture = cv2.VideoCapture(videoPath)
    executor = ThreadPoolExecutor(max_workers=32)

    (frameCount, frameIndex) = [0] * 2 # initialize both values to zero
    
    while(capture.isOpened()):
        frame = capture.read()[1] # discard the 'succeeded' variable
        extracted = contour(image = frame, scale = 0.5, imagepath = 'extracted', showExtracted = True)
        if frameCount == 30:
            executor.submit(matching.match, np.copy(extracted), dataSet, 1, False, frameIndex, groundPlan, False)
            frameCount = 0

        frameCount += 1
        frameIndex += 1
        frame = drawOnVideoFrame(frame = frame, scale = 0.5)
        cv2.imshow("movie", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    q.put('q') # in order to stop the groundplan consumer, threads can't be stopped externally

    groundPlan.visualize()    

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()