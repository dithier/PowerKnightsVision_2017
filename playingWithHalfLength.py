# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 23:49:40 2017

@author: Ithier
"""
import cv2
import numpy as np
import bounding as B


picture = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/6.jpeg'
filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/FP.npz'
original = cv2.imread(picture)
BFR_img = np.copy(original)

# Load values from program for 6.jpeg
values = np.load(filename)
valid = values['validCnt']
contours = values['cnt']
Rect_coor = values['rectCoor']
#################################################################################
def findLength(h,w):
    H = 5 # height in in of vision target
    W = 2 # width in in of vision target
    distWidth = 10.25 # distance from one edge of vision target to other in in
    conversionFactor = ((h/H) + (w/W))/2
    length = distWidth*conversionFactor
    return length

def avgPxlLengths(Rect_coor):
    w1 = Rect_coor[1][0] - Rect_coor[0][0]
    w2 = Rect_coor[2][0] - Rect_coor[3][0]
    w = (w1 + w2)/2.0 # average width of rectangle based on both sides
    
    h1 = Rect_coor[3][1] - Rect_coor[0][1]
    h2 = Rect_coor[2][1] - Rect_coor[1][1]
    h = (h1 + h2)/2.0 # average height of rectangle based on both sides
    
    aspect_ratio = float(w)/h
    
    return aspect_ratio, h, w
        
##################################################################################
# find if to left or right of valid contour
AR, h, w = avgPxlLengths(Rect_coor)
length = findLength(h,w)

"""
if cx > cxV:
    boundingBox = B.calculateBoundingBox(True, length, thresholdB, Rect_coor, BFR_img) # True means left
    print "Valid target is on left"
else: 
    boundingBox = B.calculateBoundingBox(False, length, thresholdB, Rect_coor, BFR_img)
    print "Valid target is on right"
"""
boundingBox, x, y = B.calculateBoundingBox(False, length, Rect_coor, BFR_img, h)
print "Valid target is on right"
     
cv2.drawContours(original,[np.array(boundingBox)],0,(255,0,255),2)
cv2.circle(original,(x,y), 3, (0,255,0), -1)
cv2.imshow('pic', original)
cv2.waitKey(0)