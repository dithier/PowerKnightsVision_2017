# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:45:58 2017

@author: Ithier
"""
import numpy as np
import cv2
import manipulateImage as MI

location = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/6.jpeg'
original = cv2.imread(location)

filename = 'imageValues.npz'

# Make copy of frame/image to work with
img = np.copy(original)

# Load calibration parameters
values = np.load(filename)
brightness = float(values['brightness'])
lower_bound = values['lower']
upper_bound = values['upper']

# Create img with parameters
img_darker = MI.darkenImage(img, brightness)
hsv = cv2.cvtColor(img_darker, cv2.COLOR_BGR2HSV)
mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)

mask= np.copy(mask_orig)

# Clean up mask with dilate and erode and threshold
maskd = MI.dilateAndErode(mask, 5)
maskc = np.copy(maskd)
ret,maskc = cv2.threshold(maskc,127,255,0)
mask = np.copy(maskc)
cv2.imshow('mask', mask)
cv2.imshow('pic', original)
cv2.waitKey(0)

