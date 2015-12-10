import cv2
import numpy as np
import sys

def medianApprox(arr, key):
    sorts = sorted(arr, key=key)
    return arr[len(arr)/2]

class KeyframeExtractor(object):
    """
    KeyframeExtractor extracts keyframes for the given video, a file name.
    """
    def __init__(self, inFile):
        self._buildWeights(inFile)
        self._buildSceneChangeEdges()
        self._scenes = None
        
    def _buildWeights(self, inFile):
        """
        Build a list of edges (the linked list) of weights between
        frames. Weights are calculated by the sum of the squared difference
        between pixels of an image.

        Parameters:
            inFile -- The name of the video file to read.
        """
        self._edges = []
        video_capture = cv2.VideoCapture(inFile)
        prev = None
        read_success, img = video_capture.read()
        i = 0
        while read_success:
            if prev != None:
                diff = img - prev
                weight = np.sum(diff * diff)
                if i % 500 == 0:
                    print "reading img ", i, " weight ", weight
                self._edges.append(Edge(i, i + 1, weight))
            prev = img
            i += 1
            read_success, img = video_capture.read()

        self._numFrames = i
        print "----> Read ", len(self._edges), " images"

    def _buildSceneChangeEdges(self):
        """
        Calculates the edges that are likely to be scene changes. This helps
        to separate the video into chunks to select key frames of the video.

        The number of sceneChangeEdges is guaranteed to be at most 1 / 10 the number
        of frames in the video
        """
        self._keyframes = []
        edgesByWeight = sorted(self._edges, key=lambda e : e.weight())
        diffOfWeights = []
        for idx in range(0, len(edgesByWeight)-1):
            currentVal = edgesByWeight[idx+1].weight() - edgesByWeight[idx].weight()
            diffOfWeights.append((idx, currentVal))
        self._diffOfWeights = diffOfWeights
        diffOfWeights.sort(key=lambda diff : diff[1])
        candidates = sorted(diffOfWeights[-max(len(edgesByWeight)/ 100, 3):], key= lambda el : el[0])
        approxMedian = candidates[len(candidates) / 2]
        bins = len(edgesByWeight) - approxMedian[0]
        print "Using ", bins, " bins.."
        self._sceneChangeEdges = edgesByWeight[-1*bins:]

    def _buildKeyframes(self, inFile):
        """
        Finds the key frames in the given video filename. Uses the previously
        calculated scene change edges to find the key frames.

        Parameters
            inFile -- The video file to read from.
        """
        self._keyFrames = []
        sceneChangesByTime = self.getSceneChangesByTime()
        frameIdx = 0
        sceneIndex = 0
        video_capture = cv2.VideoCapture(inFile)
        read_success, img = video_capture.read()
        while read_success and frameIdx <= sceneChangesByTime[-1].from_i:
            if(frameIdx == sceneChangesByTime[sceneIndex].from_i):
                self._keyFrames.append(img)
                sceneIndex += 1
            frameIdx += 1
            read_success, img = video_capture.read()

    def getKeyframes(self):
        if not self._keyFrames:
            self._buildKeyframes()
        return self._keyFrames

    def getSceneChangeEdges(self):
        return self._sceneChangeEdges

    def getEdges(self):
        return self._edges

    def getDiffOfEdges(self):
        return self._diffOfWeights

    def getSceneChangesByTime(self):
        return sorted(self._sceneChangeEdges, key = lambda e : e.from_i)

    def getScenes(self):
        if not self._scenes:
            self._scenes = []
            lastEnd = 0
            for e in self.getSceneChangesByTime():
                self._scenes.append(Scene(lastEnd, e.from_i + 1))
                lastEnd = e.from_i + 1
            self._scenes.append(Scene(lastEnd, self._numFrames))
        return self._scenes

    def getNumFrames(self):
        return self._numFrames

class Scene:
    def __init__(self, start, end):
        self.startFrame = start
        self.endFrame = end

    def length(self):
        return self.endFrame - self.startFrame

class Edge:
  def __init__(self, from_i, to_i, weight):
    self.from_i = from_i
    self.to_i = to_i
    self._weight = weight

  def weight(self):
    return self._weight

def main():
    """
    Extracts the key frames of sys.argv[1], and shows each for a total of 3 seconds.
    """
    in_file = sys.argv[1]

    extractor = KeyframeExtractor(in_file)

    for e in extractor.getSceneChangeEdges():
        print e.from_i
    for frame in extractor.getKeyframes():
        cv2.imshow('Keyframe', frame)
        user_in = cv2.waitKey(3000)
    cv2.waitKey(3000)

if __name__ == '__main__':
  main()