import screeninfo
import numpy as np
import cv2
import threading
import queue
from Modules import optcheck, highgui, imgproc, dataset, matching
from Modules import contour, GroundPlan
from concurrent.futures import ThreadPoolExecutor

def main():
    '''groundPlan = GroundPlan.GroundPlan()
    groundPlan.markVisited('1')
    groundPlan.markVisited('2')
    groundPlan.markVisited('4')
    groundPlan.markVisited('5')
    groundPlan.visualize()'''

    # Video code
    videoPath = optcheck.getArguments()[0]

    # Get the dataset from disk
    data_set = dataset.get(resetPersistence = False)
    
    # Video code
    capture = cv2.VideoCapture(videoPath) # Use command line argument as above
    frame_counter = 0
    frame_index = 0
    frame_interval = 30

    # Spin up a thread that consumes the results of the matching procedures in different threads
    groundPlan = GroundPlan.GroundPlan()
    q = queue.Queue()
    groundPlanConsumer = threading.Thread(target = GroundPlan.groundPlanMessageConsumer, args=[groundPlan, q])
    groundPlanConsumer.start()

    # Spin up an executor to deal with the frame matching procedures
    executor = ThreadPoolExecutor(max_workers=32)
    while (capture.isOpened()):
        ret, frame = capture.read()

        extracted = contour.contour(image = frame, scale = 0.5, imagepath = 'extracted', showExtracted = True)
        if frame_counter == frame_interval: # Every 30 frames, a new matching procedure is started, we let the executor handle threading for us
            frame_counter = 0
            f = executor.submit(matching.match, np.copy(extracted), data_set, 1, frame_index, q, False)
        
        frame_counter += 1
        frame_index += 1
        frame = contour.drawOnVideoFrame(frame = frame, scale = 0.5)     

        cv2.imshow('movie', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    capture.release()
    q.put('q') # in order to stop the groundplan consumer, threads can't be stopped externally

    groundPlan.visualize()    

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()