# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 13:31:46 2017

@author: Ithier
"""

import cv2

# Directory of file containing initial threshold values
directory = 'C:/Users/Ithier/Documents/OpenCV/FIRST 2016/PowerKnightsVision2016/Calibration Files/' # folder img file is in
pic = directory + "1.jpeg"

img = cv2.imread(pic)

cv2.imshow('img', img)
cv2.waitKey(0)