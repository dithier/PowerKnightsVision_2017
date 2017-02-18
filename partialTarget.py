# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 23:23:21 2017

@author: Ithier
"""
import cv2
import numpy as np

def findPartial(BFR_img, Rect_coor, contours):
   """
   cnt[1] = 5
   Rect_coor.append(validContour)
   """
   picture = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/6.jpeg'
   filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/FP'
   original = cv2.imread(picture)
   contours = np.load(filename)
   numContours = 20
   sortedContours = (sorted(contours, key = lambda contour:cv2.contourArea(contour)))[:numContours]
   sortedContours = list(reversed(sortedContours))
   
   for contour in sortedContours:
   cv2.drawContours(original,[contour],0,(0,0,255),2)
   
   cv2.imshow('img', BFR_img)
   cv2.waitKey(0)
    
   #return cnt, Rect_coor
    
findPartial

