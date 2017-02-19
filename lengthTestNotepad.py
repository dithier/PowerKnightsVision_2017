import cv2
import numpy as np 
import bounding as B
import validateTarget as VT

picture = 'C:/Users/Ithier/Documents/FIRST/2017/Pics/6.jpg'
filename = 'C:/Users/Ithier/Documents/FIRST/2017/PowerKnightsVision_2017/FP.npz'
original = cv2.imread(picture)
BFR_img = np.copy(original)
