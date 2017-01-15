# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 12:18:21 2017

@author: Ithier

Takes image and finds contours of both targets and their centers
"""

import cv2
import numpy as np

def processFrame(picture, filename): # picture = dir for img, filename = dir for npz file

    def darkenImage(image, scale):
        darker = (image * scale).astype(np.uint8)
        return darker
        
    def findCenter(cnt, image):
        M = cv2.moments(cnt)
        # FIND CENTROID
        #   Cx = M10/M00, Cy = M01/M00
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/ M['m00'])
        cv2.circle(image, (cx,cy), 8, (0, 255, 140), -1)
        return cx, cy
        
    def bestFitRect(img_orig, cnt):
        # Find convex hull
        hull = cv2.convexHull(cnt)
        box = np.int0(hull)
        
        # Create black image, draw rectangle hull on it, corner detection
        corners_img = np.zeros((img_orig.shape[0],img_orig.shape[1],img_orig.shape[2]), np.uint8)
        cv2.drawContours(corners_img, [box], 0, (255,255,255), -1)
        corners_img = cv2.cvtColor(corners_img, cv2.COLOR_BGR2GRAY) 
        
        #                                 image, number of corners, quality (0-1), min euclidean dist
        corners = cv2.goodFeaturesToTrack(corners_img, 4, 0.2, 10) # Find coordinates for the four corners
        corners = np.int0(corners)
        
        # Load original image and draw BFR and corners
        cv2.drawContours(img_orig, [box], 0, (0,0,255), 2)
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img_orig, (x,y), 5, (255, 0, 255), -1)
        
        return hull, corners, img_orig
    
    # Read in File
    original = cv2.imread(picture, 1)
    
    # Create resizable window for original picture and mask
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
    
    # Load calibration parameters
    # Directory of file containing initial threshold values
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    
    # Threshold Image
    img_darker = darkenImage(original, brightness)
    hsv = cv2.cvtColor(img_darker, cv2.COLOR_BGR2HSV)
    mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)
    mask = np.copy(mask_orig)
    
    # Find Contours and draw them
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt1 = contours[7]
    cnt2 = contours[17]
    cv2.drawContours(original, [cnt1], 0, (255,0,0), 3)
    cv2.drawContours(original, [cnt2], 0, (255,0,0), 3)
    
    # findCenters of targets
    cx1, cy1 = findCenter(cnt1, original)
    cx2, cy2 = findCenter(cnt2, original)
    
    # find and draw BFR
    hull1, corners1, img_orig = bestFitRect(original, cnt1)
    
    # Display images
    cv2.imshow('Original', original)
    cv2.imshow('Mask', mask_orig)
    
    # Destroy windows when done
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        
    return original, mask, cx1, cy1, cx2, cy2, cnt1, cnt2, contours, hull1, corners1