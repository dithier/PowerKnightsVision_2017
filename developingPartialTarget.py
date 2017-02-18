# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 22:53:27 2017

@author: Ithier
"""
import cv2
import numpy as np
import imageCalculations as IC
import manipulateImage as MI
#Need contours, Rect_coor, valid target

picture = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/12.jpg'
filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/FP.npz'
BFR_img = cv2.imread(picture)

# Load values from program for 6.jpeg
values = np.load(filename)
valid = values['validCnt']
contours = values['cnt']
Rect_coor = values['rectCoor']
#############################################################################
def inside(contour, valid):
     # If False, it finds whether the point is inside or outside or on the contour (it returns +1, -1, 0 respectively).
    for i in range(0, len(contour)):
        x,y = contour[i].ravel()
        bounds = cv2.pointPolygonTest(valid,(x,y),False)
        if bounds == 1 or bounds == 0:
            return False
        else:
            return True # it is outside the valid contour

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
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00']) 
      # make sure contour doesn't share same centroid as valid contour
      if cx != cxV and cy != cyV:
          # make sure contour isn't in valid contour
          if inside(contour, valid):
              revisedContours.append(contour)
###################################################################################   
box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, revisedContours[3])
                
if len(corners) == 4:
    # Organize corners
    Rect_coor_indiv = IC.organizeCorners(corners)
    
cv2.drawContours(BFR_img,[np.array(Rect_coor_indiv)],0,(0,0,255),2)
cv2.imshow('img', BFR_img)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows
########################################################################################
for contour in revisedContours:
    box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, revisedContours[3])
                
    if len(corners) == 4:
        # Organize corners
        Rect_coor_indiv = IC.organizeCorners(corners)
            
"""
for contour in revisedContours:
    cv2.drawContours(BFR_img,[contour],0,(0,0,255),2)
    cv2.namedWindow('img')
    cv2.imshow('img', BFR_img)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows
"""

        

   
