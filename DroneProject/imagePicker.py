import cv2
import numpy as np
import time
video = cv2.VideoCapture(2)
video.set(4,960)
video.set(3,1280)

i=-5
distance = 8
cv2.waitKey(0)
while i<0:
    ret, image = video.read()
    i+=1

cv2.waitKey(0)
while i<5:
    ret, image = video.read()
    cv2.imshow("Image", image)
    if i>=0:
        cv2.imwrite('calibrate{1}.png'.format(distance,i+35),image)
        print "saved"
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ret, image = video.read()
    ret, image = video.read()
    ret, image = video.read()
    ret, image = video.read()
    time.sleep(0.1)
    i+=1

video.release()
