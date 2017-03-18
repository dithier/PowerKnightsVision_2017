#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 19:14:10 2017

@author: christian
"""

import cv2
import numpy as np
import validateTarget as VT
import findTarget as FT
import imageCalculations as IC
from networktables import NetworkTable
import logging
import datetime



def run(table, image_orig, npz_file, validCount, i):
    print "STARTING TO EVALUATE NEW FRAME"
    if i < 4:
        directory = '/home/pi/production/'
        filename = directory + 'original' + str(i) + '.jpg'
        cv2.imwrite(filename, image_orig)    
    npz = np.load(npz_file)
    final_image = np.copy(image_orig)
    
    flag = 0
  
    #try: 
    startMask = datetime.datetime.now()   
    mask = FT.processImage(image_orig, npz)
    endMask = datetime.datetime.now()
    totalMask = endMask - startMask
    print "Time to make mask: " + str(totalMask.microseconds)
    
    if i < 4:
        filename = directory + 'mask' + str(i) + '.jpg'
        cv2.imwrite(filename, mask) 
    #except:
        #print "error processing image"
        #flag = 1
    i += 1
    
    if flag == 0:
        # try:
        startValid = datetime.datetime.now()
        valid, validContours, validRect_coor, BFR_img, validHull = VT.findValidTarget(image_orig, mask)
        endValid = datetime.datetime.now()
        totalValid = endValid - startValid
        print "Time for findValidTarget: " + str(totalValid.microseconds)        
        # except:
            #print "error processing image"
            #flag = 1
            #valid = False
    
    #final_image = MI.drawCrossHairs(final_image)
    startCalc = datetime.datetime.now()
    if valid:
        try:
            cx1, cy1 = IC.findCenter(validContours[0])
            cx2, cy2 = IC.findCenter(validContours[1])
            
            angle = IC.findAnglePeg(final_image, cx1, cx2)
            #distance = IC.findDistancePeg(final_image, validRect_coor)
            validCount += 1
            
            #cv2.drawContours(final_image, validContours, -1, (0, 255, 0), -1)
            #final_image = MI.drawLine2Target(final_image, cx, cy)
        except:
            print "Error with valid target"
            angle = 100
            #distance = 0
    else:
        angle = 100
        #distance = 0
    endCalc = datetime.datetime.now()
    totalCalc = endCalc - startCalc
    print "Time to calculate angle: " + str(totalCalc.microseconds)
        
    startTable = datetime.datetime.now()
    FT.send2Table(table, validCount, angle)
    endTable = datetime.datetime.now()
    totalTable = endTable - startTable
    print "Time sent to table: " + str(totalTable.microseconds)
    
    return image_orig, mask, final_image, validCount, i
    

npz = 'imageValues_WPI_multi.npz'#directory of npz file

#video_input = 'http://127.0.0.1:1180/?action=stream?dummy=param.mjpg'
video_input = '10.5.1.160:1180/?action=stream'
#video_input = 0
video = cv2.VideoCapture(video_input)
#video.set(16,.10) #exposure
#video.set(11,.10) #brightness

try:
    logging.basicConfig(level = logging.DEBUG)
    NetworkTable.setIPAddress('10.5.1.198')
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    
    sd = NetworkTable.getTable("Camera")
except:
    print "error connecting to table"

validCount = 0
i = 0

"""
#directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/Pics Set 3.3/2ft/'
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/WPI/'
pic = '17.jpg'
picture = directory + pic

img = cv2.imread(picture)
"""

#"""
print 1

while 1:
    print 2
    while video.isOpened():
        print 3
        ret, frame = video.read()
        cv2.imshow('Camera Frame', frame)
        cv2.waitKey(0)
                
        #frame = img
        if ret and not (frame == None):
            print 4
            start = datetime.datetime.now()
            image_orig, mask, final_image, validCount, i = run (sd, frame, npz, validCount, i)
            end = datetime.datetime.now()
            total = end - start
            print "Time of total process: " + str(total.microseconds)

"""
start = datetime.datetime.now()
image_orig, mask, final_img, validCount, i = run(sd, img, npz, 0, i)
end = datetime.datetime.now()
totalTime = end - start

print "Total time: " + str(totalTime.microseconds)
cv2.imshow("orig", image_orig)
cv2.imshow("mask", mask)
cv2.imshow("final", final_img)
cv2.waitKey(0)
"""



