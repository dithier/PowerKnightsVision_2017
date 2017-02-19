# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 01:40:59 2017

@author: Ithier
"""
import cv2
def calculateBoundingBox(validLeft, length, thresholdB, Rect_coor, BFR_img):

    if validLeft:
        # calculate length
        newCoorT = int(Rect_coor[0][0] + length)
        newCoorB = int(Rect_coor[3][0] + length)
        # Draw horizontal lines
        BFR_img = cv2.line(BFR_img,(Rect_coor[0][0],Rect_coor[0][1]), (newCoorT,Rect_coor[0][1]), (0,255,0), 2)
        BFR_img = cv2.line(BFR_img,(Rect_coor[3][0],Rect_coor[3][1]), (newCoorB,Rect_coor[3][1]), (0,255,0), 2)
        # Draw vertical lines
        BFR_img = cv2.line(BFR_img,(Rect_coor[0][0],Rect_coor[0][1]), (Rect_coor[3][0],Rect_coor[3][1]), (0,255,0), 2)
        BFR_img = cv2.line(BFR_img,(newCoorT,Rect_coor[0][1]), (newCoorB,Rect_coor[3][1]), (0,255,0), 2)
        boundingBox = [[Rect_coor[0][0], Rect_coor[0][1]], [newCoorT, Rect_coor[0][1]], [newCoorB, Rect_coor[3][1]], [Rect_coor[3][0], Rect_coor[3][1]]]
    else:
        # calculate length
        newCoorT = int(Rect_coor[1][0] - length)
        newCoorB = int(Rect_coor[2][0] - length)
        # Draw horizontal lines
        BFR_img = cv2.line(BFR_img,(Rect_coor[1][0],Rect_coor[1][1]), (newCoorT,Rect_coor[1][1]), (0,255,0), 2)
        BFR_img = cv2.line(BFR_img,(Rect_coor[2][0],Rect_coor[2][1]), (newCoorB,Rect_coor[2][1]), (0,255,0), 2)
        # Draw vertical lines
        BFR_img = cv2.line(BFR_img,(Rect_coor[1][0],Rect_coor[1][1]), (Rect_coor[2][0],Rect_coor[2][1]), (0,255,0), 2)
        BFR_img = cv2.line(BFR_img,(newCoorT,Rect_coor[1][1]), (newCoorB,Rect_coor[2][1]), (0,255,0), 2)
        boundingBox = [[newCoorT, Rect_coor[1][1]], [Rect_coor[1][0], Rect_coor[1][1]], [Rect_coor[2][0], Rect_coor[2][1]], [newCoorB, Rect_coor[2][1]]]
        
    # Make buffered bounding box
    boundingBox[0][0] -= thresholdB
    boundingBox[0][1] -= thresholdB
    boundingBox[1][0] += thresholdB
    boundingBox[1][1] -= thresholdB
    boundingBox[2][0] += thresholdB
    boundingBox[2][1] += thresholdB
    boundingBox[3][0] -= thresholdB
    boundingBox[3][1] += thresholdB
    
    return boundingBox