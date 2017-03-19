#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:09:47 2017

@author: christian
"""
import manipulateImage as MI
import numpy as np


#def calibrateVision(npzFile)


def processImage(image):
#get all the data findValidTarget needs

#darken
#convert to hsv
#hsv filter
#erode
    minimum = np.array([60, 0, 12])
    maximum = np.array([150, 255, 255])
    #scale = float(npz['brightness'])
    size = 5
    #darker = MI.darkenImage(image, scale)
    mask = MI.HSVFilter(image, minimum, maximum, size)    
    
    return mask
    
    
    
def send2Table(Table, validCount, angle):
    try:
        Table.putNumber('validCount', validCount)
        Table.putNumber('angle', angle)
        #Table.putNumber('distance', distance)
    except:
        print "Error sending to table"
    
