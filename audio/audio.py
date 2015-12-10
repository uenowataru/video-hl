import numpy as np # for numerical operations
from moviepy.editor import VideoFileClip, concatenate
import cv2

# inDir = "vid/"
# inFile = "ANNOYING 7 HOUR ROADTRIP (TIME LAPSE).mp4"

def getAudioPeaks(fileDir):
	#load the clip
	clip = VideoFileClip(fileDir)
	#lambda function to get a subclip 
	cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=22000) 
	#lambda function to get the volume
	volume = lambda array: np.sqrt(((1.0*array)**2).mean())
	#all the volumes in the clip
	volumes = [volume(cut(i)) for i in range(0,int(clip.audio.duration-2))]
	#find the averaged volume across 10 frames (?)
	frames_perseg = 5

	averaged_volumes = np.array([sum(volumes[i:i+frames_perseg])/frames_perseg 
		for i in range(len(volumes)-frames_perseg)])

	#find if volume is increasing between 2 10f segments
	increases = np.diff(averaged_volumes)[:-1]>=0
	#find if volume is decreasing between 2 10f segments
	decreases = np.diff(averaged_volumes)[1:]<=0
	#find the peaks
	peaks_times = (increases * decreases).nonzero()[0]
	#find the volume of the peaks
	peaks_vols = averaged_volumes[peaks_times]
	#fnid the best peaks
	peaks_times = peaks_times[peaks_vols>np.percentile(peaks_vols,90)]
	#intialize final times with one of the peaks
	final_times=[peaks_times[0]]
	#append the peaks time to final times if it is 30 seconds apart, or is louder than the last 30 seconds
	for t in peaks_times:
		#check if t is 30 seconds apart from the last final time
	    if (t - final_times[-1]) < 30:
	    	#check if t is louder than the last final time
	        if averaged_volumes[t] > averaged_volumes[final_times[-1]]:
	            final_times[-1] = t
	    else:
	        final_times.append(t)

	return final_times

def createVideo(outFile, final_times):
	#concatenate the highlights
	final = concatenate([clip.subclip(max(t-5,0),min(t+5, clip.duration))
	                     for t in final_times])
	#output the videofiles
	final.to_videofile('hl/hl_' + inFile) # low quality is the default


