# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 19:27:27 2017

@author: Ithier

"""
import cv2
import numpy as np

# directory for img
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Practice Code/Vision Images/Vision Images/LED Peg/Numbered/'
fileName = '7.jpg'
picture = directory + fileName

def bestFitRect(img_orig, cnt):
    
    # Create black image, draw rectangle hull on it, corner detection
    corners_img = np.zeros((img_orig.shape[0],img_orig.shape[1],img_orig.shape[2]), np.uint8)
    cv2.drawContours(corners_img, [cnt], 0, (255,255,255), -1)
    corners_img = cv2.cvtColor(corners_img, cv2.COLOR_BGR2GRAY) 

    cv2.imshow('hull', corners_img)   
    #Destroy windows when done
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    
    corners_img = np.float32(corners_img)
    corners = cv2.goodFeaturesToTrack(corners_img,4,0.2,5)
    corners = np.int0(corners)
    
bestFitRect(picture, cnt)