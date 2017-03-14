#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:09:47 2017

@author: christian
"""
import manipulateImage as MI


#def calibrateVision(npzFile)


def processImage(image, npz):
#get all the data findValidTarget needs

#darken
#convert to hsv
#hsv filter
#erode
    minimum = npz['lower']
    maximum = npz['upper']
    #scale = float(npz['brightness'])
    size = 5
    #darker = MI.darkenImage(image, scale)
    mask = MI.HSVFilter(image, minimum, maximum, size)    
    
    return mask
    
    
    
def send2Table(Table, validCount, angle, distance):
    try:
        Table.putNumber('validCount', validCount)
        Table.putNumber('angle', angle)
        Table.putNumber('distance', distance)
    except:
        print "Error sending to table"
    
