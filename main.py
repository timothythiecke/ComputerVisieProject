import queue
import threading
import cv2

from Modules.Dataset import getDataSet
from Modules.GroundPlan import GroundPlan, groundPlanMessageConsumer
from Modules.Contour import contour
from Modules.Matching import Matcher
from concurrent.futures import ThreadPoolExecutor

from Modules import optcheck, highgui


def matchCallback(future):
    (matchedPainting, room) = future.result()
    future.groundPlan.markVisited(room)
    highgui.showImagesHorizontally("Matching Result", 3000,
                                   future.extractedPainting, matchedPainting)



def main():
    videoPath = optcheck.getVideoPath()
    dataSet = getDataSet()
    groundPlan = GroundPlan()
    matcher = Matcher(dataSet)
    videoCapture = cv2.VideoCapture(videoPath)
    threadExecutor = ThreadPoolExecutor(max_workers=32)

    frameInterval = 50  # determines the amount of frames before matching
    (frameCount, frameIndex) = (0, 0)
    # waitKey returns ordinal value of the button that is pressed, we indicate 'q' as a button to quit the program
    # run video at 30 FPS ~ One frame per 33.3333333... milliseconds
    while(videoCapture.isOpened() and not cv2.waitKey(33) == ord('q')):
        videoFrame = videoCapture.read()[1]  # discard the 'succeeded variable'
        videoFrame = highgui.resizeImage(videoFrame, dimension=(
                                    int(videoFrame.shape[1] * 0.5),  # width
                                    int(videoFrame.shape[0] * 0.5))  # height
                                    )

        highgui.showImage("Video", videoFrame)

        if frameCount == frameInterval:
            frameCount = 0
            # find painting in video frame
            extractedPainting = contour(videoFrame)
            # match painting in database
            future = threadExecutor.submit(matcher.match, extractedPainting)
            future.extractedPainting = extractedPainting
            future.groundPlan = groundPlan
            future.add_done_callback(matchCallback)

        frameCount += 1
        frameIndex += 1

    videoCapture.release()

    cv2.destroyAllWindows()
    highgui.showImage("Groundplan", groundPlan.visualize())




if __name__ == '__main__':
    main()