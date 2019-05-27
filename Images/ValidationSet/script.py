import cv2
import numpy
import os
from Modules import optcheck, highgui, imgproc
import pickle
from pathlib import Path

#shadow_box.png
imagePath = optcheck.getArguments()[0]
windowName = imagePath
image = highgui.openImage(imagePath)
image = cv2.resize(src = image, dsize = (1000, 1000))
cv2.imshow(windowName, image)

filepath, filename = os.path.split(imagePath)
filename, extension = filename.split(".")

src = numpy.array([[0, 0], [0, 0], [0, 0], [0, 0]], numpy.float32) 
dst = numpy.array([[100, 200], [200, 200], [200, 500], [100, 500]], numpy.float32) # predefined coördinates of the rectangle

def onMouse(event, x, y, flags, userdata):
    global mouseClicks, image, windowName, imagePath
    if(cv2.EVENT_LBUTTONDOWN == event and mouseClicks < 4):  
        src[mouseClicks] = [x, y]
        mouseClicks += 1
    if(mouseClicks == 4):
        mouseClicks += 1 # increase one more time so this function will basically do nothing anymore
        for i in range(0, 3):
            cv2.line(img = image, pt1 = (src[i][0], src[i][1]), pt2 = (src[i + 1][0], src[i + 1][1]), color=(0, 0, 255), thickness= 10)

        cv2.line(img = image, pt1 = (src[3][0], src[3][1]), pt2 = (src[0][0], src[0][1]), color=(0, 0, 255), thickness= 10)
        
        print(filename, end='')
        for point in src:
            print(f" ({point[0]}, {point[1]}) ", end='')
        print("\n")
        cv2.imwrite(highgui.getSavePath(imagePath, 'e'), image)

        out = [imagePath, src[0], src[1], src[2], src[3]]
        config = Path('GT.txt')
        if config.is_file() == False:
            config.touch()
            pickled = []
            pickled.append(out)
            with open('GT.txt', 'wb') as f:
                pickle.dump(pickled, f)
        else:
            pickled = []
            with open('GT.txt', 'rb') as f:   
                pickled = pickle.load(f)
        
            pickled.append(out)

            with open('GT.txt', 'wb') as f:
                pickle.dump(pickled, f)

            #print(pickled)


mouseClicks = 0 
cv2.setMouseCallback(windowName, onMouse, mouseClicks)
cv2.waitKey()

