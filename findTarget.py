# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 11:05:43 2017

@author: Ithier

This module is in charge of finding the target
"""

import cv2
import numpy as np
import manipulateImage as MI 
import imageCalculations as IC
import validateTarget as VT


def findValids(img_orig, filename):
    global angle, distance, validUpdate
    angle = 1000
    distance = 0
    validUpdate = False
    
    # Make copy of frame/image to work with
    img = np.copy(img_orig)
    
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
    mask = MI.dilateAndErode(mask, 5)
    maskc = np.copy(mask)
    ret,maskc = cv2.threshold(maskc,127,255,0)
    
    # Determine if there are any valid targets
    valid, cnt, Rect_coor, BFR_img = VT.findValidTarget(img, mask)

    if valid: 
        validUpdate = True
    
        # Find and draw center
        cx1, cy1 = IC.findCenter(cnt[0]) 
        cx2, cy2 = IC.findCenter(cnt[1])
        cx = (cx1 + cx2) / 2
        cy = (cy1 + cy2) / 2
        
        # Calculate angle and distance
        angle = IC.findAnglePeg(BFR_img, cx1, cx2)
        distance = IC.findDistancePeg(BFR_img, Rect_coor)

        # Visualize calculation
        MI.drawLine2Target(BFR_img, cx, cy)  
        MI.drawCrossHairs(BFR_img)          
    else:
        validUpdate = False
        BFR_img = img_orig
        MI.drawCrossHairs(BFR_img)
        print 'No Valid Update'
    
    
    return angle, distance, validUpdate, BFR_img, mask_orig, cnt
