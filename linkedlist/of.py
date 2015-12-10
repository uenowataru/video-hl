import numpy as np
import cv2

cap = cv2.VideoCapture('vid/Bernie Takes on the Media.mp4')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)


count = 0
while(1):
    count+=1
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)

    cv2.imwrite('of/frame' + str(count) + '.jpg',img)
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)



#dense optical flow
cap = cv2.VideoCapture("vid/2015 Integrated Live Fire Exercise-2015.mp4")
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while(1):
   ret, frame2 = cap.read()
   next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

   flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

   mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
   hsv[...,0] = ang*180/np.pi/2
   hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
   bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

   cv2.imshow('frame2',bgr)
   k = cv2.waitKey(30) & 0xff
   if k == 27:
       break
   elif k == ord('s'):
       cv2.imwrite('opticalfb.png',frame2)
       cv2.imwrite('opticalhsv.png',bgr)
   prvs = next
 


cv2.destroyAllWindows()
cap.release()



#1. taking the whole scene, and concatenating the adjacent scenes

#2. have a way to rank the peaks based on the closeness of peaks

#3. look at shape of peaks (kurtosis and skewness)

#4. new sound is introduced to the scene or not


#train deep neural network on flikr photos (https://www.flickr.com/explore/)
#surprise
#intense



# or the absense
# explosions, fire, sparks and noise (ever wondered why these always lead the news bulletins?)
# action and movement: every video must involve someone doing something
# awe-inspiringly big things like landscapes
# amazingly small things that our eyes can’t see – but also anything closeup in general
# human stories and emotion – no matter how complex


#demo.caffe.berkeley for imagenet categorization of images


