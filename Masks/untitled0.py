# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 14:37:11 2017

@author: Ithier
"""

import cv2
import numpy as np

img = cv2.imread('5mask.png')

kernel = np.ones((20,20),np.uint8)
dilation = cv2.dilate(img,kernel,iterations = 5)

cv2.imshow('img', img)
cv2.waitKey(0)

