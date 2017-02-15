# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 00:13:52 2017

@author: Ithier
"""
import itertools

L = [1,2,3,4,5]
c = itertools.combinations(L,2)
for i in c:
    print i