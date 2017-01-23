# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:43:31 2017

@author: Ithier
"""

import cv2
import numpy as np

# create black img
rectangle = np.zeros((512,512,3), np.uint8)
# draw rectangle with 2/5 AR
cv2.rectangle(rectangle,(20,20),(60,120),(255,255,255),-1)  # coordinates chosen by making sure it has same aspect ratio as real life targe
# write imgage to file
cv2.imwrite('rectangle.png', rectangle)