# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:39:21 2016

@author: Ithier
"""

import HSVTrackbarModule as Trackbar
import cv2

# Directory of file containing initial threshold values
directory = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/Calibration Files/' # folder npz file is in
filename = directory + 'imageValues.npz'

# Picture to Calibrate
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Vision Images/Vision Images/LED Peg/'
fileName = '10.jpg'
picture = directory + fileName

img = cv2.imread(picture, 1)

# Calibrate
Trackbar.calibrateCamera(img, filename)