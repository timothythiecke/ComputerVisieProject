import queue
import threading
import cv2


from Modules.Dataset import getDataSet
from Modules.GroundPlan import GroundPlan, groundPlanMessageConsumer
from Modules.Contour import contour, PaintingFinder
from concurrent.futures import ThreadPoolExecutor
from Modules import optcheck, highgui, imgproc, Matching


def main():
    videoPath = optcheck.getVideoPath()
    dataSet = getDataSet()
    groundPlan = GroundPlan()
    paintingFinder = PaintingFinder()
    videoCapture = cv2.VideoCapture(videoPath)
    threadExecutor = ThreadPoolExecutor(max_workers=32)

    # Spin up a thread that consumes the results of the matching procedures in different threads
    matchQueue = queue.Queue()
    groundPlanConsumer = threading.Thread(target=groundPlanMessageConsumer,
                                          args=[groundPlan, matchQueue])

    (frameInterval, frameCount, frameIndex) = (30, 0, 0)

    # groundPlan.visualize()

    # waitKey returns ordinal value of the button that is pressed, we indicate 'q' as a button to quit the program
    # run video at 30 FPS
    while(videoCapture.isOpened() and not cv2.waitKey(33) == ord('q')):
        videoFrame = videoCapture.read()[1]  # discard the 'succeeded variable'
        videoFrame = highgui.resizeImage(videoFrame, dimension=(
                                    int(videoFrame.shape[1] * 0.5),  # width
                                    int(videoFrame.shape[0] * 0.5))  # height
                                    )

        highgui.showImage("Video", videoFrame)
        if frameCount == frameInterval:
            # find painting in video frame
            extractedPainting = contour(videoFrame)
            # match painting in database
            highgui.showImage("Extraction", extractedPainting)
            frameCount = 0

        frameCount += 1
        frameIndex += 1

    videoCapture.release()


#    videoPath = optcheck.getVideoPath()
#    dataSet = getDataSet()
#    groundPlan = GroundPlan()
#    groundPlan.visualize()
#    # paintingFinder = PaintingFinder()
#    capture = cv2.VideoCapture(videoPath)
#    executor = ThreadPoolExecutor(max_workers=32)
#
#    frame_interval = 30
#
#    # Spin up a thread that consumes the results of the matching procedures in different threads
#    q = queue.Queue()
#    groundPlanConsumer = threading.Thread(target=groundPlanMessageConsumer,
#                                          args=[groundPlan, q])
#    groundPlanConsumer.start()q
#
#    (frameCount, frameIndex) = [0] * 2  # initialize both values to zero
#
#    while(capture.isOpened()):
#        frame = capture.read()[1]  # discard the 'succeeded' variable
#
#        if frameCount == frame_interval:
#            extracted = contour(image=frame, scale=0.5,
#                                imagepath='extracted', showExtracted=True)
#            executor.submit(Matching.match, np.copy(extracted), dataSet, 5, frameIndex, q, False)
#
#            frameCount = 0
#
#        frameCount += 1
#        frameIndex += 1
#        frame = drawOnVideoFrame(frame=frame, scale=0.5)
#        cv2.imshow("movie", frame)
#        
#        if cv2.waitKey(10) & 0xFF == ord('q'):
#            break
#
#    capture.release()
#    q.put('q')  # in order to stop the groundplan consumer, threads can't be stopped externally
#
#    groundPlan.visualize()
#
#    cv2.waitKey()
#    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()