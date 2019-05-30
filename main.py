import cv2
import screeninfo

from Modules.Dataset import getDataSet
from Modules.GroundPlan import GroundPlan, groundPlanMessageConsumer
from Modules.Contour import contour
from Modules.Matching import Matcher
from concurrent.futures import ThreadPoolExecutor

from Modules import optcheck, highgui


def matchCallback(future):
    (matchedPainting, room) = future.result()
    future.groundPlan.markVisited(room)
    extractedPainting = highgui.resizeImage(image=future.extractedPainting,
                                            dimension=(
                                                int(future.resolution[1]/4),
                                                int(future.resolution[0]/2)
                                            ))
    matchedPainting = highgui.resizeImage(image=matchedPainting,
                                          dimension=(
                                            int(future.resolution[1]/4),
                                            int(future.resolution[0]/2))
                                          )
    highgui.showImage(windowname=f"Extract - {future.matchWindowFlag}",
                      image=extractedPainting,
                      delay=1)
    highgui.showImage(windowname=f"Match - {future.matchWindowFlag}",
                      image=matchedPainting,
                      delay=1)
 


def main():

   
    videoPath = optcheck.getVideoPath()
    dataSet = getDataSet()
    groundPlan = GroundPlan()
    matcher = Matcher(dataSet)
    videoCapture = cv2.VideoCapture(videoPath)
    threadExecutor = ThreadPoolExecutor(max_workers=32)

    frameInterval = 50  # determines the amount of frames before matching
    (frameCount, frameIndex) = (0, 0)

    # initialize windows 
    monitor = screeninfo.get_monitors()[0]
    width, height = (monitor.width, monitor.height)
    highgui.createWindowAtCoordinates("Video", int(width/2), 0)
    highgui.createWindowAtCoordinates("Match - 0", int(width/4), 0) 
    highgui.createWindowAtCoordinates("Match - 1", int(width/4), int(height/2))
    highgui.createWindowAtCoordinates("Extract - 0", 0, 0) 
    highgui.createWindowAtCoordinates("Extract - 1", 0, int(height/2))
    matchWindowFlag = 0 # is used to determine which match window is used.

    # waitKey returns ordinal value of the button that is pressed, we indicate 'q' as a button to quit the program
    # run video at 30 FPS ~ One frame per 33.3333333... milliseconds
    while(videoCapture.isOpened() and not cv2.waitKey(33) == ord('q')):
        videoFrame = videoCapture.read()[1]  # discard the 'succeeded variable'
        videoFrame = highgui.resizeImage(videoFrame, dimension=(
                                    int(width/2),  # width
                                    height)  # height
                                    )


        highgui.showImage("Video", videoFrame, 1)

        if frameCount == frameInterval:
            frameCount = 0
            # find painting in video frame
            extractedPainting = contour(videoFrame)
            # match painting in database
            future = threadExecutor.submit(matcher.match, extractedPainting)
            future.extractedPainting = extractedPainting
            future.groundPlan = groundPlan
            future.matchWindowFlag = matchWindowFlag
            future.resolution = (height, width)
            matchWindowFlag = (matchWindowFlag + 1) % 2
            future.add_done_callback(matchCallback)

        frameCount += 1
        frameIndex += 1

    videoCapture.release()

    cv2.destroyAllWindows()
    #highgui.showImage("Groundplan", groundPlan.visualize())




if __name__ == '__main__':
    main()