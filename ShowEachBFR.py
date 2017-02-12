# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:25:11 2017

@author: Ithier
"""

import numpy as np
import cv2
import manipulateImage as MI
from heapq import nlargest

############################ LOAD IMAGE ##################################

# directory for img
#directory = 'C:/Users/Ithier/Documents/FIRST/2017/Practice Code/Vision Images/Vision Images/LED Peg/Numbered/'
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/'
fileName = '6.jpeg'
picture = directory + fileName

# directory for npz file
#directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
#filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'
#filename = directory + 'imageValuesMulti.npz'
filename = 'imageValuesMultiAttempt1.npz'

original = cv2.imread(picture)

######################### DO ANALYSIS ####################################

# Make copy of frame/image to work with
img = np.copy(original)

# Load calibration parameters
values = np.load(filename)
brightness = float(values['brightness'])
lower_bound = values['lower']
upper_bound = values['upper']

# Create img with parameters
img_darker = MI.darkenImage(img, brightness)
hsv = cv2.cvtColor(img_darker, cv2.COLOR_BGR2HSV)
mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)

mask= np.copy(mask_orig)

# Clean up mask with dilate and erode and threshold
maskd = MI.dilateAndErode(mask, 5)
maskc = np.copy(maskd)
ret,maskc = cv2.threshold(maskc,127,255,0)
mask = np.copy(maskc)
############################################################################

areas = []
numContours = 20
count = 0
BFR_img = original

 # find contours
_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# take twenty longest contours
biggestContours = nlargest(numContours, contours, key=len) 

# Determine area of each contour and sort by largest to smallest
for i in range(0,len(biggestContours)):
    if len(biggestContours[i]) > 3:
        contourMoment = cv2.moments(biggestContours[i])
        contourArea = contourMoment['m00']
        #if minArea < contourArea < maxArea:
        areas.append(contourArea) 
areas = np.array(areas)
area_indices = np.argsort(areas)


if len(areas) > 0:
    # Check for validity of contours in order of largest area to smallest
    rev_indices = list(reversed(area_indices))
    ind = 0
    i = rev_indices[0]
    for n in range(0, len(rev_indices)):
        if count == 1:
            break
        while count == 0:
            # Find BFR
            box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, biggestContours[i])
            
            MI.drawBFR(BFR_img, box, corners)
            cv2.imshow('pic', BFR_img)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows
                    
            if i == area_indices[0]:
                count = 1
                ind = 0
            
            ind += 1
            i = rev_indices[ind]








