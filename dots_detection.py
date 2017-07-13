import cv2
import numpy as np
import time

# pattern noise filtering


def ok(a,arr):
    for index,i in enumerate(arr):
        if((i[0]-a[0])**2+(i[1]-a[1])**2)<20:
            if(i[2]>a[2]):
                return
            else:
                arr.pop(index)
                arr.append(a)
                return
    arr.append(a)
    return


def marker_points(image,COEF = 0.3):
    # image should be in rgb
    stamp = time.time()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_image)
    bound = maxVal*COEF
    raw_pixels = np.argwhere(gray_image >= bound)
    values = np.reshape(gray_image[gray_image>=bound],(len(raw_pixels),1))
    raw_pixels =  np.concatenate((raw_pixels,values),1)
    median = np.median(raw_pixels, axis=0)
    pixels = []
    # clear from crap pixels
    for i in raw_pixels:
        if((i[0]-median[0])**2+(i[1]-median[1])**2)<600:
            ok(i,pixels)
    # show?
    print 'marker time'
    print time.time()-stamp
    if len(pixels)==6:
            cv2.imshow("IMAGE", image)
            for i in pixels:
                cv2.circle(image, (i[1],i[0]), 3, (0, 255, 0), -1)
                cv2.imshow("IMAGE", image)
#    print pixels
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            #return np.array(pixels,dtype="double")
            return np.array(pixels,dtype="double")[:,:-1]
    elif len(pixels)>6:
        return marker_points(image,COEF+0.05)
    else:
        return marker_points(image,COEF-0.05)


def pose_estimation(image):
    stamp =  time.time()
    model_points = np.array([
                            (0.0, 0.0, 0.0),             
                            (0.0, 120.0, 0.0),       
                            (60.0, 60.0, 0.0),
                            (120.0, 0.0, 0.0),
                            (120.0, 60.0, 0.0), 
                            (120.0, 120.0, 0.0),
                            ])
    size = image.shape
    image_points = marker_points(image)


    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array(
                             [[focal_length, 0, center[0]],
                             [0, focal_length, center[1]],
                             [0, 0, 1]], dtype = "double"
                             )
    camera_matrix = np.array(
                             [[1.10616906e+03*1.08,0.00000000e+00,6.35668602e+02],
                             [0.00000000e+00,1.10819769e+03*1.08,4.96993394e+02],
                             [0, 0, 1]], dtype = "double"
                             )
    
    #print "Camera Matrix :\n {0}".format(camera_matrix)
    image_points = np.array(image_points,dtype = "double")
    #dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
    dist_coeffs = np.array([-0.20523672,0.11735183,-0.00085103,-0.0005939,0.00980464])# need to recalibrate everything
    stamp2 = time.time()
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.CV_ITERATIVE)
    print 'solvePnPtime:'
    print time.time()-stamp2
    print 'time elapsed:'
    print time.time()-stamp
    print 'translation:'
    #x-right y-down
    print translation_vector
    print 'rotation'
    print rotation_vector
    #print rotation_vector

    



paths = ['exposure=10_distance=6m_num0.png','exposure=10_distance=9m_num0.png','exposure=10_distance=9m_num1.png',
         'exposure=10_distance=9m_num2.png','exposure=10_distance=12m_num0.png','exposure=10_distance=12m_num1.png','exposure=10_distance=12m_num2.png']
#paths = ['exposure=10_distance=12m_num4.png']
for path in paths:
    print path
    img = cv2.imread(path,1)
    pose_estimation(img)

    
##(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img)
##bound = maxVal*0.3
##raw_pixels = np.argwhere(img >= bound)
##median = np.median(raw_pixels, axis=0)
##pixels = []
##for i in raw_pixels:
##    if((i[0]-median[0])**2+(i[1]-median[1])**2)<1000 and ok(i,pixels):
##        pixels.append(i)
##
##sec = cv2.imread(path,1)
##cv2.imshow("IMAGE", sec)
##for i in pixels:
##    cv2.circle(sec, (i[1],i[0]), 3, (0, 255, 0), -1)
##    cv2.imshow("IMAGE", sec)
##print pixels
##cv2.waitKey(0)
##cv2.destroyAllWindows()


