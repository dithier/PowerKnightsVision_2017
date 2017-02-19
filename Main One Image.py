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

directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/'
fileName = '6.jpeg'
picture = directory + fileName

directorysave = 'C:/Users/Ithier/Documents/FIRST/2017/AnalyzedV1/'
picturesave = directorysave + fileName



# directory for npz file
#directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
#filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'
#filename = directory + 'imageValues_1ftH3ftD0Angle0Brightness.npz'

filename = 'imageValues_6jpeg.npz'
#filename = 'imageValues_12jpg.npz'
#dir2 = 'C:/Users/Ithier/Documents/FIRST/2017/Practice Code/Vision Images/Vision Images/LED Peg/Numbered/'
#picture = dir2 + '1.jpg'


original = cv2.imread(picture)


######################### DO ANALYSIS ####################################
angle, distance, validUpdate, BFR_img, mask, cnt = FT.findValids(original, filename)
try:
    cv2.drawContours(original, [cnt[0]], 0, (0,0,255), 2)
except:
    "No valid contours"

try:
    cv2.drawContours(original, [cnt[1]], 0, (255,0,255), 2)
except:
    "No second valid contour"


####################################################################################

cv2.imshow('mask', mask)
cv2.imshow('Analyzed', BFR_img)
cv2.imshow('original', original)
#cv2.imwrite(picturesave, BFR_img)



# Destroy windows when done
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
