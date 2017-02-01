# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 15:12:37 2017

@author: Ithier

This module does picture manipulation like darkening, drawing lines on the img, etc
"""
import cv2
import numpy as np

def darkenImage(image, scale):
    darker = (image * scale).astype(np.uint8)
    return darker
    
def bestFitRect(img_orig, cnt):
    # Find convex hull
    hull = cv2.convexHull(cnt)
    box = np.int0(hull)
    
    # Create black image, draw rectangle hull on it, corner detection
    corners_img = np.zeros((img_orig.shape[0],img_orig.shape[1],img_orig.shape[2]), np.uint8)
    cv2.drawContours(corners_img, [box], 0, (255,255,255), -1)
    corners_img = cv2.cvtColor(corners_img, cv2.COLOR_BGR2GRAY) 

    cv2.imshow('hull', corners_img)   
    #Destroy windows when done
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    
    corners_img = np.float32(corners_img)
    corners = cv2.goodFeaturesToTrack(corners_img,4,0.2,5)
    corners = np.int0(corners)
    
    
    """
    #                                 image, number of corners, quality (0-1), min euclidean dist
    corners = cv2.goodFeaturesToTrack(corners_img, 4, 0.2, 5) # Find coordinates for the four corners
    corners = np.int0(corners)
    
  
    # Load original image and draw BFR and corners
    cv2.drawContours(img_orig, [box], 0, (0,255,255), 2)
    
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img_orig, (x,y), 5, (255, 0, 255), -1)
    """
    return box, hull, corners, img_orig
    
def drawBFR(img_orig, box, corners):
    # Load original image and draw BFR and corners
    cv2.drawContours(img_orig, [box], 0, (0,255,255), 2)
    
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img_orig, (x,y), 5, (255, 0, 255), -1)
    
    
def dilateAndErode(img, size):
    kernel = np.ones((size,size), np.uint8)
    dilation = cv2.dilate(img,kernel,iterations=1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    return erosion 
    
def drawLine2Target(image, cx, cy):
    h, w, c = image.shape # h = height, w = width, c = channel
    cameraX = w / 2
    cameraY = h / 2
    img = cv2.line(image, (cameraX, cameraY), (int(cx),int(cy)), (255, 0, 0), 2)
    img = cv2.circle(img,(int(cx),int(cy)), 5, (0,0,255), -1)
    return img
    
def drawCrossHairs(image):
    h, w, c = image.shape # h = height, w = width, c = channel
    vertMid = w / 2
    vertHorz = h / 2
    image = cv2.line(image, (vertMid, 0), (vertMid, h), (255, 100, 200), 2)
    image = cv2.line(image, (0, vertHorz), (w, vertHorz), (255, 100, 200), 2)
    return image

def rotateImage(frame):
    rows, cols, dim = frame.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1) # image center, angle, scaling  factor 
    Rotated_frame = cv2.warpAffine(frame,M,(cols,rows))
    return Rotated_frame