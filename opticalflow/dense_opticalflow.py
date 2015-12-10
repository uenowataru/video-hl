import numpy as np
import cv2


def capDenseOF(fileDir):
   cap = cv2.VideoCapture()

   ret, frame1 = cap.read()
   ret, frame2 = cap.read()
   prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
   hsv = np.zeros_like(frame1)
   hsv[...,1] = 255

   height , width , layers =  frame1.shape

   video = cv2.VideoWriter('video', -1 , 30, (width,height), True)
   #video = cv2.VideoWriter('video.mp4', -1,1,(width,height))

   count = 0 

   while(type(frame2) is np.ndarray):
      next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

      flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)

      mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
      hsv[...,0] = ang*180/np.pi/2
      hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
      bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

      # cv2.imshow('frame2',bgr)
      # k = cv2.waitKey(30) & 0xff
      # if k == 27:
      #     break
      # elif k == ord('s'):
      #     cv2.imwrite('opticalfb.png',frame2)
      #     cv2.imwrite('opticalhsv.png',bgr)
      
      cv2.imwrite('of/gray' + str(count) + ' .png', cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY))
      #cv2.imwrite('of/opticalhsv' + str(count) + ' .png',bgr)
      #video.write(bgr)
      
      prvs = next
      ret, frame2 = cap.read()
      count+=1
      

   video.release()
   cv2.destroyAllWindows()
   cap.release()


def framesDenseOF(frame1, frame2):
   prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
   hsv = np.zeros_like(frame1)
   hsv[...,1] = 255

   height , width , layers =  frame1.shape

   video = cv2.VideoWriter('video', -1 , 30, (width,height), True)
   #video = cv2.VideoWriter('video.mp4', -1,1,(width,height))

   count = 0 

   next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

   flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)

   mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
   hsv[...,0] = ang*180/np.pi/2
   hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
   bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

   return bgr

if __name__ == '__main__':
   capDenseOF("../data/videos/100$$uqe na faz neh.mp4")
