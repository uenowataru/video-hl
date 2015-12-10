import cv2
import keyframe_extractor as kf
import os
import random
from scipy.misc import imsave
import sys
from sets import Set

class TrailerGenerator(object):
    """
    Calculates the video frames for the trailer of a video.

    Parameters:
        inFile -- the video file to create a trailer for
        time -- seconds of video desired
    """
    def __init__(self, inFile, time=5.0, framesPerScene=None):
        ex = kf.KeyframeExtractor(inFile)
        scenesUsed = ex.getScenes()
        if not framesPerScene:
            totalFrames =  time * 20
            framesPerScene = max(1, totalFrames / len(scenesUsed))

        trailer = []
        for scene in scenesUsed:
            framesInScene = range(scene.startFrame, scene.endFrame)
            if len(framesInScene) <= framesPerScene:
                # this is where the method is better than key frame approach
                # here, we've taken spots from similar frames from longer scenes
                # and replaced them with a short scene 
                # (key frames would have kept the longer, redundant scene)
                trailer.append(framesInScene)
            else: # TODO(patrick) pick them smartly, random sample for now
                trailer.append(sorted(random.sample(framesInScene, framesPerScene)))
        trailerFrameNums = [frameNum for frameList in trailer for frameNum in frameList]
        print "using ", len(trailerFrameNums), " frames from ", len(scenesUsed), " scenes"
        self._trailerFrameNums = trailerFrameNums
        if not trailerFrameNums:
            print "No trailer frames wtf"
            sys.exit()
        self._trailerFrames = []
        self.inFile = inFile

    def forEachTrailerFrame(self, func):
        """
        execute a function over each trailer frame.

        """
        frameIdx = 0
        video_capture = cv2.VideoCapture(self.inFile)
        read_success, img = video_capture.read()
        while read_success and frameIdx <= max(self._trailerFrameNums):
            if frameIdx in self._trailerFrameNums:
                func(img)
            frameIdx += 1
            read_success, img = video_capture.read()
        video_capture.release()

    def getTrailerFrames(self):
        if not self._trailerFrames:
            self.forEachTrailerFrame(lambda frame : self._trailerFrames.append(frame))
        return self._trailerFrames

class FrameSaver:
    def __init__(self, baseDir='./'):
        self.i = 0
        self.baseDir = baseDir

    def saveFrame(self, frame):
        name = 'frame%s.png' % ('0' * (8 - len(str(self.i))) + str(self.i) )
        self.i += 1
        if self.i % 50 == 0:
            print "writing frame ", os.path.join(self.baseDir, name)
        cv2.imwrite(os.path.join(self.baseDir, name), frame)


def showFrame(frame):
    cv2.imshow('Trailer', frame)
    user_in = cv2.waitKey(100)

def main():
    """
    Creates a trailer for sys.argv[1] video, based on the scene detection algorithm
    """
    if(len(sys.argv) > 1):
        inFile = sys.argv[1]
        outDir = sys.argv[2]
    else:
        inDir = "vid"
        outDir =  "out"

    for file in os.listdir(inDir):
        if file.endswith(".mp4") and os.stat(inDir + "/" + file).st_size < 20000000:
	   # time = float(sys.argv[3])
  	   trailer = TrailerGenerator(inDir + "/" + file, framesPerScene=3)
	   directory = "out/" + file
	   if not os.path.exists(directory):
            os.makedirs(directory)

  	   trailer.forEachTrailerFrame(FrameSaver(directory).saveFrame)
   	   cv2.waitKey(3000)
    

if __name__ == '__main__':
    main()
