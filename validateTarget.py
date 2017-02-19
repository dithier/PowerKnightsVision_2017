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
import math
import partialTarget as PT

filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/12FP'

def checkCornerDist(Rect_coor1, Rect_coor2):
    threshold = 10
    def distance(a1, a2, b1, b2):
        return math.sqrt((a2 - a1)**2 + (b2 - b1)**2)
    
    for i in range(0,len(Rect_coor1)):
        a1 = Rect_coor1[i][0]
        b1 = Rect_coor1[i][1]
        a2 = Rect_coor2[i][0]
        b2 = Rect_coor2[i][1]
        d = distance(a1, a2, b1, b2)
        if d < threshold:
            return False
    return True
    
def inside(contour, valid):
         # If False, it finds whether the point is inside or outside or on the contour (it returns +1, -1, 0 respectively).
        for i in range(0, len(contour)):
            x = contour[i][0]
            y = contour[i][1]
            bounds = cv2.pointPolygonTest(np.array(valid),(x,y),False)
            if bounds == 1 or bounds == 0:
                print "contour inside"
                return False
            else:
                "contour not inside"
                return True # it is outside the valid contour
                
    
    

def isValidShapePeg(hull):
    matchThreshold = 0.198
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

def avgPxlLengths(Rect_coor):
    w1 = Rect_coor[1][0] - Rect_coor[0][0]
    w2 = Rect_coor[2][0] - Rect_coor[3][0]
    w = (w1 + w2)/2.0 # average width of rectangle based on both sides
    
    h1 = Rect_coor[3][1] - Rect_coor[0][1]
    h2 = Rect_coor[2][1] - Rect_coor[1][1]
    h = (h1 + h2)/2.0 # average height of rectangle based on both sides
    
    aspect_ratio = float(w)/h
    
    return aspect_ratio, h, w

def isValidARPeg(Rect_coor):
    minAR = 0.32
    maxAR = 0.493
    ''' Note on coordinate system: The top left corner of the target is Rect_coor[0], the top right is Rect_coor[1],
    the bottom right is Rect_coor[2], and the bottom left is Rect_coor[3]. The second index determines whether it is an
    x or y coordinate. Ex, Rect_coor[1][0] is the x value of the top right corner of the target while Rect_coor[1][1] is
    the y coordinate for the top right corner.
    '''
    aspect_ratio, h, w = avgPxlLengths(Rect_coor)
    print "AR: " + str(aspect_ratio)
    
    # Real aspect ratio is 2"/5" = 0.4 (used dimensions from target) 
    if aspect_ratio < minAR or aspect_ratio > maxAR:
        return False
    else:
        return True
        

def isValid(hull, Rect_coor):
    valid1 = isValidARPeg(Rect_coor)
    valid2= isValidShapePeg(hull)
    
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
    numContours = 20
    count = 0
    
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
    area_indices = np.argsort(areas) # gives indices of smallest to largest contours in biggestContours
    
    
    if len(areas) > 0:
        # Check for validity of contours in order of largest area to smallest
        rev_indices = list(reversed(area_indices)) #gives indices of largest to smallest contours in biggestContours
        ind = 0 # keeps track of what index we're on within the index list rev_indices
        i = rev_indices[0] # index of biggestContours that we're testing
        for n in range(0, len(rev_indices)):
            if count == 1: # count determines whether we stay in the while loop or not as does whether we've found 2 "good targets"
                break
            while goodTarget < 2 and count == 0:
                # Find BFR
                box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, biggestContours[i])
                
                if len(corners) == 4:
                    # Organize corners
                    Rect_coor_indiv = IC.organizeCorners(corners)
                    
                    # Determine if contour meets specs
                    appropriateCnt = isValid(hull_indiv, Rect_coor_indiv)
                    
                    # If valid already exists check it's not double counting and make sure iti's not in exisiting contour
                    if len(Rect_coor) != 0:
                        appropriateCnt = checkCornerDist(Rect_coor_indiv, Rect_coor[0])
                        isOutside = inside(Rect_coor_indiv, Rect_coor[0])
                    else:
                        isOutside = True
                        
                    
                    if appropriateCnt and isOutside == True:
                        print "i is Valid: " + str(i)
                        MI.drawBFR(BFR_img, box, corners)
                        cnt.append(biggestContours[i])
                        hull.append(hull_indiv)
                        Rect_coor.append(Rect_coor_indiv)
                        goodTarget += 1
                        #np.savez(filename, validCnt = cnt[0], rectCoor = Rect_coor[0], cnt = contours)
                           
                        
                if i == area_indices[0] or goodTarget == 2: # if we've reached the end of our index list or we've found two good targets 
                    count = 1
                    ind = 0
                
                ind += 1
                i = rev_indices[ind]
                print i
                
        
    if len(cnt) == 2:
        valid = True
        print 'Two valid contours'
    elif len(cnt) == 1:
        cnt, Rect_coor = PT.findPartial(cnt, BFR_img, Rect_coor[0], contours)
        if len(cnt) == 1:
            valid = False
            Rect_coor, BFR_img, hull = zeroVariables(image)
            print 'One valid contour'
        else:
            valid = True
        
    else:
        valid = False
        Rect_coor, BFR_img, hull = zeroVariables(image)
        cnt = [0,0]
        
        
    return valid, cnt, Rect_coor, BFR_img, hull
    
        
    
        
        
        
        
        
        
        
        
        