# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:25:11 2017

@author: Ithier
"""

import numpy as np
import cv2
import manipulateImage as MI
import imageCalculations as IC
import validateTarget as VT
from heapq import nlargest
import math

############################ LOAD IMAGE ##################################

validLeft = False # is the valid target on the left or right

# directory for img
#directory = 'C:/Users/Ithier/Documents/FIRST/2017/Practice Code/Vision Images/Vision Images/LED Peg/Numbered/'
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/'
fileName = '10.jpeg'
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
def findLength(h,w):
    H = 5 # height in in of vision target
    W = 2 # width in in of vision target
    distWidth = 10.25 # distance from one edge of vision target to other in in
    conversionFactor = ((h/H) + (w/W))/2
    length = distWidth*conversionFactor
    return length
   
   
def checkCornerDist(rectCoor):
    threshold = 10
    def distance(Rect_coor1, Rect_coor2):
        for i in range(0,len(Rect_coor1)):
            a1 = Rect_coor1[i][0]
            b1 = Rect_coor1[i][1]
            a2 = Rect_coor2[i][0]
            b2 = Rect_coor2[i][1]
        return math.sqrt((a2 - a1)**2 + (b2 - b1)**2)
    
    # Go through everything in rectCoor and compare distances
    for i in range(0, len(rectCoor)):
        dist = distance(rectCoor[0], rectCoor[i + 1])
        if dist < threshold:
            return False
    return True


###################################################################################

areas = []
rectCoor = []
COOR = []
numContours = 5
count = 0
check = 0
BFR_img = original
firstTime = True

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
            if len(corners) == 4:
                    # Organize corners
                    Rect_coor = IC.organizeCorners(corners)
                    rectCoor.append(Rect_coor)
                    
                    if firstTime:
                        AR, h, w = VT.avgPxlLengths(Rect_coor)
                        length = findLength(h,w)
                        
                        if validLeft:
                            # calculate length
                            newCoorT = int(Rect_coor[0][0] + length)
                            newCoorB = int(Rect_coor[3][0] + length)
                            # Draw horizontal lines
                            BFR_img = cv2.line(BFR_img,(Rect_coor[0][0],Rect_coor[0][1]), (newCoorT,Rect_coor[0][1]), (0,255,0), 2)
                            BFR_img = cv2.line(BFR_img,(Rect_coor[3][0],Rect_coor[3][1]), (newCoorB,Rect_coor[3][1]), (0,255,0), 2)
                            # Draw vertical lines
                            BFR_img = cv2.line(BFR_img,(Rect_coor[0][0],Rect_coor[0][1]), (Rect_coor[3][0],Rect_coor[3][1]), (0,255,0), 2)
                            BFR_img = cv2.line(BFR_img,(newCoorT,Rect_coor[0][1]), (newCoorB,Rect_coor[3][1]), (0,255,0), 2)
                        else:
                            # calculate length
                            newCoorT = int(Rect_coor[1][0] - length)
                            newCoorB = int(Rect_coor[2][0] - length)
                            # Draw horizontal lines
                            BFR_img = cv2.line(BFR_img,(Rect_coor[1][0],Rect_coor[1][1]), (newCoorT,Rect_coor[1][1]), (0,255,0), 2)
                            BFR_img = cv2.line(BFR_img,(Rect_coor[2][0],Rect_coor[2][1]), (newCoorB,Rect_coor[2][1]), (0,255,0), 2)
                            # Draw vertical lines
                            BFR_img = cv2.line(BFR_img,(Rect_coor[1][0],Rect_coor[1][1]), (Rect_coor[2][0],Rect_coor[2][1]), (0,255,0), 2)
                            BFR_img = cv2.line(BFR_img,(newCoorT,Rect_coor[1][1]), (newCoorB,Rect_coor[2][1]), (0,255,0), 2)
                        
                        
                        appropriateCnt = True 
                        firstTime = False
                    
                    
                    if len(Rect_coor) == 4 and check == 1:
                        appropriateCnt = checkCornerDist(rectCoor)
                    
                    check = 1 # should from now on check for corner distance
                    
                    if appropriateCnt:
                        print "Rect coor:" + str(Rect_coor)
                        COOR.append(Rect_coor)
                        MI.drawBFR(BFR_img, box, corners)
                        """
                        cv2.namedWindow('pic', cv2.WINDOW_NORMAL)
                        cv2.imshow('pic', BFR_img)
                        if cv2.waitKey(0) & 0xFF == ord('q'):
                            cv2.destroyAllWindows
                        """
                        
                        
                    
            if i == area_indices[0]:
                count = 1
                ind = 0
            
            ind += 1
            i = rev_indices[ind]








