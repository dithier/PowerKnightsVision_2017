# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 23:23:21 2017

@author: Ithier
"""
import cv2
import numpy as np
import manipulateImage as MI
import validateTarget as VT
import bounding as B

def findPartial(cnt, BFR_img, Rect_coor, contours):
    thresholdB = 10
    valid = cnt[0]
################################################################################
    def findLength(h,w):
        H = 5 # height in in of vision target
        W = 2 # width in in of vision target
        distWidth = 10.25 # distance from one edge of vision target to other in in
        conversionFactor = ((h/H) + (w/W))/2
        length = distWidth*conversionFactor
        return length
    
    ################################################################################
    #Inside = inside(sortedContours[0], valid)
    
    # Calculations on Valid Contour
    M = cv2.moments(cnt[0])
    cxV = int(M['m10']/M['m00'])
    cyV = int(M['m01']/M['m00']) 
    
    # Remove contours we don't need to consider
    revisedContours = []
    for contour in sortedContours:
        # need at least length of 4 to have 4 corners 
        if len(contour) > 4:
          M = cv2.moments(contour)
          cx = int(M['m10']/M['m00'])
          cy = int(M['m01']/M['m00']) 
          # make sure contour doesn't share same centroid as valid contour
          if cx != cxV and cy != cyV:
              # make sure contour isn't in valid contour
              if inside(contour, valid):
                  revisedContours.append(contour)
    ########################################################################################
     # find if to left or right of valid contour
     AR, h, w = VT.avgPxlLengths(Rect_coor)
     length = findLength(h,w)
     if cx > cxV:
         boundingBox = B.calculateBoundingBox(True, length, thresholdB, Rect_coor, BFR_img) # True means left
         print "Valid target is on left"
     else: 
         boundingBox = B.calculateBoundingBox(False, length, thresholdB, Rect_coor, BFR_img)
         print "Valid target is on right"
            
             
             
    return cnt, Rect_coor