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

    # Video code
    videoPath = optcheck.getArguments()[0]

    # Get the dataset from disk
    data_set = dataset.get(resetPersistence = False)
    
    # Video code
    capture = cv2.VideoCapture(videoPath) # Use command line argument as above
    i = 0
    frame_index = 0
    thread_i = 0

    groundPlan = GroundPlan.GroundPlan()

    executor = ThreadPoolExecutor(max_workers=32)
    while (capture.isOpened()):
        ret, frame = capture.read()

        extracted = contour.contour(image = frame, scale = 0.5, imagepath = 'extracted', showExtracted = True)
        if i == 30: # Every 30 frames, a new matching procedure is started, we let the executor handle threading for us
            f = executor.submit(matching.match, np.copy(extracted), data_set, 1, False, frame_index, groundPlan)
        
        i += 1
        frame_index += 1
        frame = contour.drawOnVideoFrame(frame = frame, scale = 0.5)     

        cv2.imshow('movie', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()

    groundPlan.visualize()    

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()