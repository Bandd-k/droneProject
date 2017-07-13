import cv2
import numpy as np
video = cv2.VideoCapture(2)
video.set(4,960)
video.set(3,1280)
#https://stackoverflow.com/questions/10702105/detecting-led-object-status-from-image
#cv2.namedWindow("Main Frame", cv2.WINDOW_AUTOSIZE)
while True:
    ret, image = video.read()
    #Display Main Frame
    #blurred = cv2.GaussianBlur(image, (25, 25), 0)
    blurred = cv2.GaussianBlur(image, (7, 7), 0)
    cv2.imshow("Image", image)
    #time.sleep(3)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    continue
    #k = cv2.waitKey(1) & 0xFF
    #if k == 27:
    #    break
    #continue
    # find all the 'white' shapes in the image
    lower = np.array([240, 240, 240])
    upper = np.array([255, 255, 255])
    shapeMask = cv2.inRange(blurred, lower, upper)
   
    # find the contours in the mask
    (_,cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print "I found %d white shapes" % (len(cnts))
    #cv2.imshow("Mask", shapeMask)
 
# loop over the contours
    t = 0
    for c in cnts:
        #if t<1:
        #    print [c]
        #t+=1
    # draw the contour and show it
        #if cv2.contourArea(c)<5000:
        M = cv2.moments(c)
        cX = int((M["m10"]+0.001) / (M["m00"]+0.001))
        cY = int((M["m01"]+0.001) / (M["m00"]+0.001))
            
	# draw the contour and center of the shape on the image
        cv2.circle(image, (cX, cY), 7, (0, 255, 0), -1)
            #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.imshow("Image", image)
   
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
video.release()
