# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 19:06:57 2017

@author: Ithier

playing with canny edge detection with masks
"""

import cv2
import numpy as np

img = cv2.imread('5mask.png',0)
img2 = np.copy(img)
edges = cv2.Canny(img,100,120)

laplacian = cv2.Laplacian(img2, cv2.CV_64F)
sobelx = cv2.Sobel(img2, cv2.CV_64F,1,0, ksize = 5)
sobely = cv2.Sobel(img2, cv2.CV_64F,0,1, ksize = 5)


cv2.imshow('original', img)
cv2.imshow('canny', edges)
cv2.imshow('Laplaclian', laplacian)
cv2.imshow('sobelx', sobelx)
cv2.imshow('sobely', sobely)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows