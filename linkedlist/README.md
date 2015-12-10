Key frames by scene recognition
============================

Idea: leverage scene changes in a video to extract relevant key frames
============================
Model video as linked list of n + 1 frames:

0->1->2->3-> .... -> n

Let the weight of a frame f be defined as the sum of squared differences between f and the frame 
preceding it.

The idea is to find a large weight, which indicates a scene change. All frames within a distinct scene can be approximated with a single key frame. Thus, if a video has a long scene of mostly repeating frames, only one frame needs to be used from this long scene as a key frame. Conversely, fast scenes will not go unnoticed when we find the key frames of the video using this scene changing method. 

For example, say 3->4 is a large difference. This means 0,1,2,3 are similar, and can be
approximated with either an average, random selection, or some other method. These nodes become
merged to form a super node, which is represented by one frame.

(0,1,2,3) -> 4 -> 5 -> ... -> n

Do this enough times and the video is succinctly summarized by the super nodes.

Finding the scene changes: what constitutes a weight large enough to be a scene change?
=======================================================================================
If we ordered the differences, they might look something like this
                ..
               ...
               ...
             .....
      ............
  where difference is vertical, order of difference is horizontal.

The transition between large and small weights is where the difference between weights is large.
When the weights are small and ordered, the change is small, and when the weights are large and ordered,
the difference is also small.

We define any weight "large enough" to be a scene change as any weight at a higher index than that of the max differences between weights.


Algorithm
=========
  1.  Compute weights (differences between frames) of the video
  2.  Find number of scene changes by finding the max change in the weights
  3.  Find key frames within each scene change
