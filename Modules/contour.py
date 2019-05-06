import cv2
import numpy as np

def contour(image):
    i = 0
    image = cv2.resize(src = image, dsize = (0, 0), dst = None, fx = 0.25, fy = 0.25)
    gray = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
    fake = np.zeros(gray.shape)
    thresh1 = 200
    thresh2 = 10
    edges = cv2.Canny(image = gray, threshold1 = thresh1, threshold2 = thresh2)
    #cv2.imshow(str(i) + 'canny', edges)
        
    # Dilate the canny lines so finding contours is easier
    dilated = cv2.dilate(src = edges, kernel = np.array([[1,1,1],[1,1,1],[1,1,1]]))
    cv2.imshow(str(i) + 'dilate', dilated)

    #image, contours, hierarchy = cv2.findContours(image = image, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)
    	#image, contours, hierarchy = cv2.findContours(image = dilated, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE, contours=None)
        #_, contours, _= cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # Find contours in image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #for contour in contours:
        #    for point in contour:
        #        print('a')
                #image = cv2.circle(img = image, center = point, radius = 5, color = (0,255,0), thickness=3)

        #corners = cv2.goodFeaturesToTrack(image, 200, 0.05, 10, None, None, 3, True, 0.04)
        #for corner in corners:
        #    image = cv2.circle(img = image, center = (corner[0][0], corner[0][1]), radius = 5, color = (0,255,0), thickness=3)

        #print(contours)
        #print('\n')
    cv2.drawContours(image, contours, -1, (0, 255, 0), 5)
        #cv2.drawContours(fake, contours, -1, (255, 255, 255), 1)
    cv2.imshow(str(i), image)
        #cv2.imshow(str(i) + 'fake', fake)

    cv2.waitKey()

    # Sort the contours by contour area, as paintings will likely have larger contours
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        #print(contours)
        #cv2.drawContours(image, contours, -1, (0, 255, 0), 5)
    box = None
        # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html #4
        # Approximate the contours into a polygon (starting with the largest contour)
        # This will yield the first polygon with 4 points
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)

            #print(len(approx))
        if len(approx) == 4:
            box = approx
            break
        
        #print(box[0], box[1], box[2], box[3])
    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

    cv2.imshow(str(i), image)
        #cv2.imshow(str(i) + 'fake', fake)
 
        #retval = cv2.boundingRect(fake)
        #print(retval)

        #approxCurve = cv.approx

        # Determine bounding box
    bounding_box = np.zeros((4, 2), dtype = 'float32')
    approx_box = np.zeros((4, 2), dtype = 'float32')
    idx = 0
    smallest_x = 100000.0
    largest_x = -1.0
    smallest_y = 100000.0
    largest_y = -1.0
    for point in box:
        x = point[0][0]
        y = point[0][1]
        approx_box[idx] = (x, y)

        if x < smallest_x:
            smallest_x = x
        if x > largest_x:
            largest_x = x
        if y < smallest_y:
            smallest_y = y
        if y > largest_y:
            largest_y = y
        idx += 1

    width = largest_x - smallest_x
    height = largest_y - smallest_y

    bounding_box[0] = (0.0, 0.0)
    bounding_box[1] = (width, 0.0)
    bounding_box[2] = (width, height)
    bounding_box[3] = (0.0, height)

        # Assert that order of points is equivalent to bounding_box
        # By using distance from edge points of image
        # TODO: I believe this can be simplified but works in an early version
    temp = np.copy(approx_box)
    top_left = -1
    top_right = -1
    bottom_left = -1
    bottom_right = -1
    dist_top_left = 1000000.0
    dist_top_right = 1000000.0
    dist_bottom_left = 1000000.0
    dist_bottom_right = 1000000.0

    idx = 0
    for point in temp:
        x = point[0]
        y = point[1]
            
            # Distance to zero
        dist = np.sqrt((x ** 2) + (y ** 2))
        if dist < dist_top_left:
            top_left = idx
            dist_top_left = dist

            # Distance to top right
        dist = np.sqrt(((x - image.shape[0]) ** 2) + ((y - 0.0) ** 2))
        if dist < dist_top_right:
            top_right = idx
            dist_top_right = dist

            # Distance to bottom right
        dist = np.sqrt(((x - image.shape[0]) ** 2) + ((y - image.shape[1]) ** 2))
        if dist < dist_bottom_right:
            bottom_right = idx
            dist_bottom_right = dist

            # Distance to bottom left
        dist = np.sqrt(((x - 0.0) ** 2) + ((y - image.shape[1]) ** 2))
        if dist < dist_bottom_left:
            bottom_left = idx
            dist_bottom_left = dist

        idx += 1
            
    approx_box[0] = temp[top_left]
    approx_box[1] = temp[top_right]
    approx_box[2] = temp[bottom_right]
    approx_box[3] = temp[bottom_left]

        # Apply transformation (homography)
    transform = cv2.getPerspectiveTransform(approx_box, bounding_box)
    result = cv2.warpPerspective(image, transform, (0, 0))

    cv2.imshow(str(i) + 'result', result)
    print(bounding_box)
    print(bounding_box[2])
        # Crop out of original picture
    cv2.imshow(str(i) + 'crop', result[0:int(bounding_box[2][1]), 0:int(bounding_box[2][0])])