# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 00:37:35 2017

@author: Ithier
"""
import cv2

picture = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/6.jpeg'
original = cv2.imread(picture)

cv2.circle(original,(508,609), 3, (0,0,255), -1)
cv2.imshow('pic', original)
cv2.waitKey(0)