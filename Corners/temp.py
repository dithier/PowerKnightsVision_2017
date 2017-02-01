# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 15:52:51 2017

@author: Ithier
"""
import cv2
import numpy as np
import validateTarget as VT
import processFrameforAngle as pf

# directory for img
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Vision Images/Vision Images/LED Peg/Numbered/'
fileName = '10.jpg'
picture = directory + fileName

# directory for npz file
directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'

original = cv2.imread(picture)

mask_orig, contours = pf.processFrame(picture, filename)
cv2.drawContours(original, contours, -1, (0,255,0), 1) # draw all contours
mask = np.copy(mask_orig)

valid, cnt, Rect_coor, BFR_img, hull = VT.findValidTarget(original, mask)
print valid

#if valid:
    #for i in range(len(contours)):
    #    cv2.drawContours(original, [contours[i]], 0, (255,0,0), 3)

try:
    cv2.drawContours(original, [cnt[0]], 0, (0,0,255), 2)
except:
    "No valid contours"

try:
    cv2.drawContours(original, [cnt[1]], 0, (255,0,255), 2)
except:
    "No second valid contour"

    
cv2.imshow('Image', original)
cv2.imshow('Mask', mask_orig)
    
# Destroy windows when done
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
