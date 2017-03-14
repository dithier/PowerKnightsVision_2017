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



def run(table, image_orig, npz_file, validCount, i):
    if i < 4:
        directory = '/home/pi/production/'
        filename = directory + 'original' + str(i) + '.jpg'
        cv2.imwrite(filename, image_orig)    
    npz = np.load(npz_file)
    final_image = np.copy(image_orig)
    
    flag = 0
  
    #try:    
    mask = FT.processImage(image_orig, npz)
    if i < 4:
        filename = directory + 'mask' + str(i) + '.jpg'
        cv2.imwrite(filename, mask) 
    #except:
        #print "error processing image"
        #flag = 1
    i += 1
    
    if flag == 0:
        # try:
        valid, validContours, validRect_coor, BFR_img, validHull = VT.findValidTarget(image_orig, mask)
        # except:
            #print "error processing image"
            #flag = 1
            #valid = False
    
    #final_image = MI.drawCrossHairs(final_image)
    if valid:
        try:
            cx1, cy1 = IC.findCenter(validContours[0])
            cx2, cy2 = IC.findCenter(validContours[1])
            
            angle = IC.findAnglePeg(final_image, cx1, cx2)
            distance = IC.findDistancePeg(final_image, validRect_coor)
            validCount += 1
            
            #cv2.drawContours(final_image, validContours, -1, (0, 255, 0), -1)
            #final_image = MI.drawLine2Target(final_image, cx, cy)
        except:
            print "Error with valid target"
            angle = 100
            distance = 0
    else:
        angle = 100
        distance = 0
        
    
    FT.send2Table(table, validCount, angle, distance)
    
    return image_orig, mask, final_image, validCount, i
    

npz = 'imageValues_3_3.npz'#directory of npz file

video_input = 'http://127.0.0.1:1180/?action=stream?dummy=param.mjpg'
#video_input = 0

video = cv2.VideoCapture(video_input)

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
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/Pics Set 3.3/2ft/'
pic = '3.jpg'
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
        #frame = img
        if ret and not (frame == None):
            print 4
            image_orig, mask, final_image, validCount, i = run (sd, frame, npz, validCount, i)

"""
image_orig, mask, final_img, validCount, i = run(sd, img, npz, 0, i)
cv2.imshow("orig", image_orig)
cv2.imshow("mask", mask)
cv2.imshow("final", final_img)
cv2.waitKey(0)
#"""



