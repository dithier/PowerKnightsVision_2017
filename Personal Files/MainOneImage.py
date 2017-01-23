# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 11:25:28 2017

@author: Ithier

Analyze one image at a time
"""

import cv2 
import findTarget as FT
############################ LOAD IMAGE ##################################

# directory for img
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Vision Images/Vision Images/LED Peg/Numbered/'
fileName = '6.jpg'
picture = directory + fileName

# directory for npz file
directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'

original = cv2.imread(picture)

######################### DO ANALYSIS ####################################
angle, distance, validUpdate, BFR_img, mask = FT.findValids(original, filename)

cv2.imshow('mask', mask)
cv2.imshow('Analyzed', BFR_img)

# Destroy windows when done
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()