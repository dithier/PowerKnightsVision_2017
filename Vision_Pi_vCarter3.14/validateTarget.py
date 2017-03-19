#!/usr/bin/env python2
# -*- coding: utf-8 -*-thresh, cnt
"""
Created on Sat Jan 21 12:19:52 2017

@author: christian
"""

import cv2
import numpy as np
import manipulateImage as MI
import imageCalculations as IC
import math
import datetime

values = np.load('rectangleCNT.npz')
rectangleCNT = values['contour']
def isValidShape(hull, debug):
    #startS = datetime.datetime.now()
    #matchThreshold = .264
    matchThreshold = 0.282
    global rectangleCNT
    
    #check quality of shape match
    match_quality = cv2.matchShapes(rectangleCNT, hull, 1, 0.0)
    if debug >= 1:
        print "match quality " + str(match_quality)
    if debug >= 3:
        endS = datetime.datetime.now()
        totalS = endS - startS
        print "Time to match shape: " + str(totalS.microseconds)
    return (match_quality < matchThreshold)

    
def isValidARPeg(Rect_coor, debug):
#Checks rectangles aspect ratio
    #startAR = datetime.datetime.now()
    #minAR = .32
    minAR = .27
    #maxAR = .493
    maxAR = .609
    
    
    #get AR
    w1 = float(Rect_coor[1][0] - Rect_coor[0][0])
    w2 = float(Rect_coor[2][0] - Rect_coor[3][0])
    h1 = float(Rect_coor[2][1] - Rect_coor[1][1])
    h2 = float(Rect_coor[3][1] - Rect_coor[0][1])
    w = w1 + w2
    h = h1 + h2
    if h == 0:
        h = .001
    AR = float(w)/float(h)
    if debug >= 1:
        print "AR " + str(AR)
    if debug >= 3:
        endAR = datetime.datetime.now()
        totalAR = endAR - startAR
        print "Time to calc AR: " + str(totalAR.microseconds)
    return (minAR < AR < maxAR)
"""    
def isAreaValid(hull, debug):
    area = cv2.contourArea(hull)
    if debug >= 1:
        print "Area: " + str(area)
    if area < 250:
        return False
    else:
        return True
"""
    
    
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

    
def isValid(hull, Rect_coor, debug):
#Checks contour validity
    return isValidShape(hull, debug) and isValidARPeg(Rect_coor, debug) #and isAreaValid(hull, debug)
    
    
def zeroVariables(image):
    Rect_coor = [0,0]
    BFR_img = image
    hull = [0,0]
    return Rect_coor, BFR_img, hull
    

def findValidTarget(image, img_mask, debug):
    if debug >= 2:
        print "started validation"
    
    BFR_img = np.copy(image)
    mask = np.copy(img_mask)
    numContours = 10
    
    #take n largest contours sorted by area
    #startC = datetime.datetime.now()
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sortedContours = (sorted(contours, key = lambda contour:cv2.contourArea(contour), reverse = True))[:numContours]
    if debug >= 3:    
        endC = datetime.datetime.now()
        totalC = endC - startC
        print "Time to find contours and sort: " + str(totalC.microseconds)
    
    #filter invalid contours until 2 valid are found
    validContours = []
    validRect_coor = []
    validHull = []
    valid = False
    for contour in sortedContours:
        #get BFR and corners
        if debug >= 2:
            print "GOT INTO SORTEDCONTOURS"
        
        #startBFR = datetime.datetime.now()
        _, hull, corners, BFR_img = MI.bestFitRect(BFR_img, contour, debug)
        if debug >= 3:
            endBFR = datetime.datetime.now()
            totalBFR = endBFR - startBFR
            print "Time to calc BFR: " + str(totalBFR.microseconds)
        
        if len(corners) == 4:
            try:
                #startR = datetime.datetime.now()
                Rect_coor = IC.organizeCorners(corners)
                if debug >= 3:
                    endR = datetime.datetime.now()
                    totalR = endR - startR
                    print "Time to organize corners: " + str(totalR.microseconds)
            except:
                continue
        else:
            continue
        
        #check validity
        if isValid(hull, Rect_coor, debug):
            if len(validContours) == 1:
                #startCD = datetime.datetime.now()
                CD = checkCornerDist(Rect_coor, validRect_coor[0])
                if debug >= 3:
                    endCD = datetime.datetime.now()
                    totalCD = endCD - startCD
                    print "Time for corner dist check: " + str(totalCD.microseconds)
                if not CD:
                    continue
            if debug >= 2:
                print "1 valid contour found so far"
                
            validContours.append(contour)
            validRect_coor.append(Rect_coor)
            validHull.append(hull) 
            if debug >= 2:
                print "Length of valid contours: " + str(len(validContours))
        else:
            if debug >= 2:
                print "contour was not valid"
        
        if len(validContours) == 2:
            valid = True
            if debug >= 0:
                print "2 VALID CONTOURS, VALID TARGET"
            return valid, validContours, validRect_coor, BFR_img, validHull
            
        """
        if contour == sortedContours[-1] and len(validContours) != 2:
            print "NO VALID TARGET"
        """

    if debug >= 2:    
        print "Num of valid contours: " + str(len(validContours))       
    Rect_coor, BFR_img, hull = zeroVariables(image)
    return valid, validContours, validRect_coor, BFR_img, validHull