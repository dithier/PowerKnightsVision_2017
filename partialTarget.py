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

filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/revisedContours12'

def findPartial(cnt, BFR_img, Rect_coor, contours):
    thresholdB = 10
    valid = cnt[0]
################################################################################
    def inside(contour, valid):
         # If False, it finds whether the point is inside or outside or on the contour (it returns +1, -1, 0 respectively).
        for i in range(0, len(contour)):
            x,y = contour[i].ravel()
            bounds = cv2.pointPolygonTest(valid,(x,y),False)
            if bounds == 1 or bounds == 0:
                return False
                print "returned false"
            else:
                return True # it is outside the valid contour
                
    def findLength(h,w):
        H = 5 # height in in of vision target
        W = 2 # width in in of vision target
        distWidth = 10.25 # distance from one edge of vision target to other in in
        conversionFactor = ((h/H) + (w/W))/2
        length = distWidth*conversionFactor
        return length
        
    def testCntLocation(boundingBox, rect):
        # If False, it finds whether the point is inside or outside or on the contour (it returns +1, -1, 0 respectively).
        for i in range(0,len(rect)):
            x,y = rect[i].ravel()
            bounds = cv2.pointPolygonTest(np.array(boundingBox),(x,y),False)
            #print bounds
            if bounds == 1 or bounds == 0:
                return True
            else:
                return False
                
    def avgPxlLengths(Rect_coor):
        w1 = Rect_coor[1][0] - Rect_coor[0][0]
        w2 = Rect_coor[2][0] - Rect_coor[3][0]
        w = (w1 + w2)/2.0 # average width of rectangle based on both sides
        
        h1 = Rect_coor[3][1] - Rect_coor[0][1]
        h2 = Rect_coor[2][1] - Rect_coor[1][1]
        h = (h1 + h2)/2.0 # average height of rectangle based on both sides
        
        aspect_ratio = float(w)/h
        
        return aspect_ratio, h, w
    
    ################################################################################
    numContours = 73
    sortedContours = (sorted(contours, key = lambda contour:cv2.contourArea(contour)))[:numContours]
    sortedContours = list(reversed(sortedContours))
    
    #Inside = inside(sortedContours[0], valid)
    
    # Calculations on Valid Contour
    M = cv2.moments(valid)
    cxV = int(M['m10']/M['m00'])
    cyV = int(M['m01']/M['m00']) 
    
    # Remove contours we don't need to consider
    revisedContours = []
    for contour in sortedContours:
        # need at least length of 4 to have 4 corners 
        if len(contour) > 4:
          M = cv2.moments(contour)
          try:
              cx = int(M['m10']/M['m00'])
              cy = int(M['m01']/M['m00']) 
          except:
              cx = 0
              cy = 0
          # make sure contour doesn't share same centroid as valid contour
          if cx != cxV and cy != cyV:
              # make sure contour isn't in valid contour
              if inside(contour, valid):
                  revisedContours.append(contour)
                  
    #np.savez(filename, validCnt = cnt[0], rectCoor = Rect_coor[0], cnt = contours)
    #np.savez(filename, revised = revisedContours, validCnt = cnt[0])
    #print revisedContours
    ########################################################################################
     
    
    for contour in revisedContours:
        box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, contour)
       
        if len(corners) == 3 or len(corners) == 4:
             M = cv2.moments(contour)
             try:
                 cx = int(M['m10']/M['m00'])
             except:
                 cx = 0
             # find if to left or right of valid contour
             AR, h, w = avgPxlLengths(Rect_coor)
             length = findLength(h,w)
             if cx > cxV:
                 boundingBox = B.calculateBoundingBox(True, length, thresholdB, Rect_coor, BFR_img) # True means left
                 print "Valid target is on left"
             else: 
                 boundingBox = B.calculateBoundingBox(False, length, thresholdB, Rect_coor, BFR_img)
                 print "Valid target is on right"
            
             inside = testCntLocation(boundingBox, contour)
             if inside:
                 print 'Valid second contour found'
                 cnt.append(contour)
                 break
             
    return cnt, Rect_coor