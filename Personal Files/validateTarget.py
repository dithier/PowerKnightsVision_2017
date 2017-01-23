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

def isValidShapePeg(hull):
    matchThreshold = 0.197
    '''
    Rectangle.png was created with this code
    cv2.rectangle(rectangle,(20,20),(60,120),(255,255,255),-1)  # coordinates chosen by making sure it has same aspect ratio as real life targe
    cv2.imwrite('rectangle.png', rectangle)
    '''
    # load image to compare 
    rectangle = cv2.imread('rectangle.png', 0)
    
    # Threshold and get contours
    ret, thresh = cv2.threshold(rectangle, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh,2,1)
    cnt = contours[0]
    match_quality = cv2.matchShapes(cnt,hull,1,0.0)
    print "Match: " + str(match_quality)
    
    if match_quality < matchThreshold:
        return True
    else:
        return False
    

def isValidARPeg(Rect_coor):
    minAR = 0.1
    maxAR = 0.7
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
    hull = [0,0]
    return Rect_coor, BFR_img, hull


def findValidTarget(image, mask):
    areas = []
    cnt = []
    hull = []
    Rect_coor = []
    goodTarget = 0
    minArea = 1 # need to calculate good values for min and max area
    maxArea = 100^6 # need to calculate good values for min and max area
    BFR_img = np.copy(image)
    numContours = 41
    counter = 0
    
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
    
    while goodTarget < 2 and counter == 0:
        if len(areas) > 0:
            # Check for validity of contours in order of largest area to smallest
            for i in reversed(area_indices):
                # Find BFR
                hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, biggestContours[i])
                
                if len(corners) == 4:
                    # Organize corners
                    Rect_coor_indiv = IC.organizeCorners(corners)
                    
                    # Determine if contour meets specs
                    appropriateCnt = isValid(hull_indiv, Rect_coor_indiv)
                    
                    if appropriateCnt:
                        print "i is Valid: " + str(i)
                        cnt.append(biggestContours[i])
                        hull.append(hull_indiv)
                        Rect_coor.append(Rect_coor_indiv)
                        goodTarget += 1
                    
                # break out of while loop if at end of area
                if i == area_indices[0]:
                    counter = 1
                
        else:
            break 
        
    if len(cnt) == 2:
        valid = True
    elif len(cnt) == 1:
        valid = False
        Rect_coor, BFR_img, hull = zeroVariables(image)
    else:
        valid = False
        Rect_coor, BFR_img, hull = zeroVariables(image)
        cnt = [0,0]
        
    return valid, cnt, Rect_coor, BFR_img, hull
    
        
        
        
        
        
        
        
        
        
        
        