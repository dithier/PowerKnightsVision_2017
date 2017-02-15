# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 21:00:16 2017

@author: Ithier
"""
import cv2

# directory for img
directory = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/'
fileName = '10.jpeg'
picture = directory + fileName

img = cv2.imread(picture)

img = cv2.line(img,(314,109), (377,109), (0,255,0), 2)

img = cv2.line(img,(314,140), (377,140), (0,255,0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)