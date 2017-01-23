# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 11:17:57 2017

@author: Ithier

Test BFR and pic 17
"""
import cv2
import manipulateImage as MI
import processFrameforAngle as pf

# directory for img
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Vision Images/Vision Images/LED Peg/Numbered/'
fileName = '12.jpg'
picture = directory + fileName

# directory for npz file
directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'

original = cv2.imread(picture)

mask_orig, contours = pf.processFrame(picture, filename)
cv2.drawContours(original, contours, -1, (0,255,0), 1)

hull, corners, original = MI.bestFitRect(original, contours[3])
hull, corners, original = MI.bestFitRect(original, contours[5])


cv2.imshow('original', original)
cv2.imshow('mast', mask_orig)
# Destroy windows when done
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()


