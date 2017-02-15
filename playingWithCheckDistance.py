# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 21:35:40 2017

@author: Ithier
"""
import itertools
import math
import cv2
import numpy as np

###############################################################################
rect1 = [[314, 109], [324, 109], [325, 138], [314,140]]
rect2 = [[355,126], [367,126], [366,140], [356, 140]]
rect3 = [[318, 121], [324,124], [323,136], [318,136]]
rect4 = [[354, 112], [365,111], [365,118], [355,119]]

Rect = [rect1, rect2, rect3, rect3]
###############################################################################
overlaps = []

def checkCornerDist(rectCoor):
    threshold = 10
    def distance(a1, b1, a2, b2):
        return math.sqrt((a2 - a1)**2 + (b2 - b1)**2)
        
    def lengths(Rect_coor1, Rect_coor2):
        found = 0
        for i in range(0, len(Rect_coor1)):
            a1 = Rect_coor1[i][0]
            b1 = Rect_coor1[i][1]
            a2 = Rect_coor2[i][0]
            b2 = Rect_coor2[i][1]
            dist = distance(a1, b1, a2, b2)
            if dist < threshold and found == 0:
                overlaps.append([Rect_coor1, Rect_coor2])
                found = 1
    
    # Go through everything in rectCoor and compare distances
    c = itertools.combinations(rectCoor,2)

    for i in c:
        lengths(i[0],i[1])
  
##########################################################################################

checkCornerDist(Rect)

################################################################################
# Find larger contour in overlaps and accept that one
areaOverlap = []
for overlap in overlaps:
    area1 = cv2.contourArea(np.array(overlap[0]))
    area2 = cv2.contourArea(np.array(overlap[1]))
        
        
        
        
        
        