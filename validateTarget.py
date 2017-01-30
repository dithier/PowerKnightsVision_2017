# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 15:49:26 2017

@author: Ithier

This file sorts 
"""
import cv2
import numpy as np 
from heapq import nlargest
import imageCalculations as IC
import manipulateImage as MI

def isValidShapePeg(Rect_coor):
    #matchThreshold = 0.198
    matchThreshold = 0.25
    '''
    Rectangle.png was created with this code
    cv2.rectangle(rectangle,(20,20),(60,120),(255,255,255),-1)  # coordinates chosen by making sure it has same aspect ratio as real life targe
    cv2.imwrite('rectangle.png', rectangle)
    '''
    # load image to compare 
    rectangle = cv2.imread('rectangle.png', 0)
    
    # Create polygon out of corners
    shape = np.zeros((512,512,3), np.uint8)
    pts = np.array([Rect_coor[3], Rect_coor[0], Rect_coor[1], Rect_coor[2]], np.int32)
    cv2.fillConvexPoly(shape, pts, (255, 255, 255))
    cv2.imwrite('DistortedRectangle.png', shape)
    
    # Threshold and get contours for rectangle
    ret, thresh = cv2.threshold(rectangle, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh,2,1)
    cntR = contours[0]
    
    # Threshold and get contours for polygon
    polygon = cv2.imread('DistortedRectangle.png', 0)
    ret, thresh = cv2.threshold(polygon, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh,2,1)
    cntP = contours[0]
    
    # Compare shapes
    match_quality = cv2.matchShapes(cntR,cntP,1,0.0)
    print "Match: " + str(match_quality)
    
    if match_quality < matchThreshold:
        return True
    else:
        return False
    

def isValidARPeg(Rect_coor):
    #minAR = 0.32
    #maxAR = 0.493
    minAR = .2
    maxAR = .6
    ''' Note on coordinate system: The top left corner of the target is Rect_coor[0], the top right is Rect_coor[1],
    the bottom right is Rect_coor[2], and the bottom left is Rect_coor[3]. The second index determines whether it is an
    x or y coordinate. Ex, Rect_coor[1][0] is the x value of the top right corner of the target while Rect_coor[1][1] is
    the y coordinate for the top right corner.
    '''
    w1 = Rect_coor[1][0] - Rect_coor[0][0]
    w2 = Rect_coor[2][0] - Rect_coor[3][0]
    w = (w1 + w2)/2.0 # average width of rectangle based on both sides
    
    h1 = Rect_coor[3][1] - Rect_coor[0][1]
    h2 = Rect_coor[2][1] - Rect_coor[1][1]
    h = (h1 + h2)/2.0 # average height of rectangle based on both sides
    
    aspect_ratio = float(w)/h
    print "AR: " + str(aspect_ratio)
    
    # Real aspect ratio is 2"/5" = 0.4 (used dimensions from target) 
    if aspect_ratio < minAR or aspect_ratio > maxAR:
        return False
    else:
        return True
        
        

def isValid(hull, Rect_coor):
    valid1 = isValidARPeg(Rect_coor)
    valid2 = isValidShapePeg(hull)
    
    if valid1 == False or valid2 == False:
        return False
    else:
        return True
     

def zeroVariables(image):
    Rect_coor = [0,0]
    BFR_img = image
    return Rect_coor, BFR_img


def findValidTarget(image, mask):
    areas = []
    cnt = []
    Rect_coor = []
    goodTarget = 0
    minArea = 1 # need to calculate good values for min and max area
    maxArea = 100^6 # need to calculate good values for min and max area
    BFR_img = np.copy(image)
    numContours = 5
    count = 0
    ind = 0
    
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
        index = range(0,len(rev_indices))
        for i in rev_indices:
            print i
            if count == 1:
                break
            while goodTarget < 2 and count == 0:
                # Find BFR
                box, corners, BFR_img = MI.bestFitRect(BFR_img, biggestContours[i])
                
                if len(corners) == 4:
                    # Organize corners
                    Rect_coor_indiv = IC.organizeCorners(corners)
                    
                    # Determine if contour meets specs
                    appropriateCnt = isValid(Rect_coor_indiv, Rect_coor_indiv)
                    print appropriateCnt
                    
                    if appropriateCnt:
                        #print "i is Valid: " + str(i)
                        MI.drawBFR(BFR_img, box, corners)
                        cnt.append(biggestContours[i])
                        Rect_coor.append(Rect_coor_indiv)
                        goodTarget += 1
                else: print "Not enough corners"
                        
                if i == area_indices[0] or goodTarget == 2:
                    count = 1
                
                if count != 1:
                    i = rev_indices[index[ind + 1]]
                    ind += 1
                
        
    if len(cnt) == 2:
        valid = True
    elif len(cnt) == 1:
        valid = False
        Rect_coor, BFR_img= zeroVariables(image)
    else:
        valid = False
        Rect_coor, BFR_img = zeroVariables(image)
        cnt = [0,0]
        
    return valid, cnt, Rect_coor, BFR_img
   
        
        
        
        
        
        
        
        
        
        
        