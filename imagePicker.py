import cv2
import numpy as np
import time
video = cv2.VideoCapture(0)
video.set(4,960)
video.set(3,1280)

i = -3
time.sleep(5)
distance = 1
while i<3:
    ret, image = video.read()
    cv2.imshow("Image", image)
    if i>=0:
        cv2.imwrite('exposure=10_distance={0}m_num{1}.png'.format(distance,i),image)
        print "saved"
    time.sleep(3)
    i+=1
video.release()
