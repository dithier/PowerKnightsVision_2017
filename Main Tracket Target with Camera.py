# -*- coding: utf-8 -*-
"""
Created on Fri May 13 18:10:44 2016

@author: Ithier
"""

import findTarget as FT
import NetworkTableModule as NT
import time
import cv2

directory = 'C:/Users/Ithier/Documents/OpenCV/FIRST 2016/PowerKnightsVision2016/'
#directory = 'C:/Users/Ithier/Documents/!!OpenCV/Mayhem/' # folder npz file is in
frame_0 = directory + 'Raw/'
frame_p = directory + 'Processed/'
filename = directory + 'imageValues.npz'
url = 'http://10.5.1.11/axis-cgi/mjpg/video.cgi?resolution=640x480'   # !!!!!!This needs to change to the new camera url

freqFramesCam = 20 # how often we're sampling the camera to save files 
freqFramesNT = 10 # how often we're sending to network tables

validCount = 0 # initialize how many validUpdates we've had
#############################################################################
from networktables import NetworkTable
import logging

if NetworkTable._staticProvider is None:
    logging.basicConfig(level=logging.DEBUG)
    NetworkTable.setIPAddress('10.5.1.2')
    NetworkTable.setClientMode()
    NetworkTable.initialize()

sd = NetworkTable.getTable("Camera")
##############################################################################

cap = cv2.VideoCapture(url) # capture camera, 0 is laptop cam, numbers after that are cameras attached

 # Check to make sure cap was initialized in capture
if cap.isOpened():
    print 'Cap succesfully opened'
    print cap.grab()
else:
    print 'Cap initialization failed'

    
# Create resizable window for camera 
cv2.namedWindow('Camera Frame', cv2.WINDOW_NORMAL)

c = freqFramesCam
n = freqFramesNT

while(cap.isOpened()):
    # Capture frame-by-frame
    #    ret returns true or false (T if img read correctly); frame is array of img    
    ret, frame = cap.read()
    
    if frame is None:
        print 'Frame is None'
        Processed_frame = cv2.imread('1.png', 1)
        mask = Processed_frame
    else:
        try:
            # Save frame to file
            if c > freqFramesCam:
                # Determine time stamp
                t = time.localtime()
                stamp = str(t[1]) + "_" + str(t[2]) + "_" + str(t[0]) + "time_" + str(t[3]) + "_" + str(t[4]) + "_" + str(t[5]) + "_" + str(n)
                cv2.imwrite(frame_0 + stamp + '.jpg', frame)
                c = 0
            else:
                c = c + 1
        
            # Process image
            Angle, Distance, validUpdate, Processed_frameg, mask = FT.findValids(frame, filename)
            Locked = False 
            
            # Update how many validUpdates we've had so far
            if validUpdate: validCount += 1
            
            # Determine allowable angle offset 
            Error = 3 
            
            # If anle is in acceptable range, write LOCKED on picture
            if -Error <= Angle <= Error:
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(Processed_frame,'LOCKED',(400,85), font, 3.8,(0,255,0),6,cv2.LINE_AA)
                Locked = True
            
            if n > freqFramesNT:
                # Send to NetworkTable
                NT.sendValues(sd, Angle, Distance, validCount, Locked)
                n = 0
            else:
                n = n + 1
            
            # Save processed frame
            cv2.imwrite(frame_p + stamp + '.jpg', Processed_frame)
            
        except:
            print 'There was an error'
    
    # Display the resulting frame
    cv2.imshow('Camera Frame', Processed_frame)
    cv2.imshow('Mask', mask)
   
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
     
    
# When capture done, release it
cap.release() # !! important to do
cv2.destroyAllWindows()


