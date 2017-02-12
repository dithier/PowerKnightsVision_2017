# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 21:01:39 2017

@author: Ithier

detecting contours of masks
"""
import cv2 

img = cv2.imread('5mask.png', 0)
# find contours
_, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

for i in range(0, len(contours)):
    cv2.drawContours(img, [contours[i]], -1, (0,255,0), 2)
    cv2.imshow('pic', img)
    cv2.waitKey(0)

