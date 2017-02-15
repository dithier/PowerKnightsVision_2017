# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 13:49:00 2017

@author: Ithier
"""
import numpy as np
import cv2

###############################################################################
rect1 = [[314, 109], [324, 109], [325, 138], [314,140]]
rect2 = [[355,126], [367,126], [366,140], [356, 140]]
rect3 = [[318, 121], [324,124], [323,136], [318,136]]
rect4 = [[354, 112], [365,111], [365,118], [355,119]]
rect5 = [[400,220], [365,111], [220,100], [320,150]]

Rect = [rect1, rect2, rect3, rect3]

thresholdB = 10
boundingBox = [[314,109], [372,109], [372,140], [314,140]]
# Make buffered bounding box
boundingBox[0][0] -= thresholdB
boundingBox[0][1] -= thresholdB
boundingBox[1][0] += thresholdB
boundingBox[1][1] -= thresholdB
boundingBox[2][0] += thresholdB
boundingBox[2][1] += thresholdB
boundingBox[3][0] -= thresholdB
boundingBox[3][1] += thresholdB
###############################################################################
def testCntLocation(boundingBox, rect):
    # If False, it finds whether the point is inside or outside or on the contour (it returns +1, -1, 0 respectively).
    for i in range(0,len(rect)):
        bounds = cv2.pointPolygonTest(np.array(boundingBox),tuple(rect[i]),False)
        #print bounds
        if bounds == 1 or bounds == 0:
            return True
        else:
            return False

################################################################################
inside = testCntLocation(boundingBox, rect3)
print inside