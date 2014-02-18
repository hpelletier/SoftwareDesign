# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:33:06 2014

@author: hpelletier
"""

def compare(x,y):
    if x > y:
        return 1
    elif x == y:
        return 0
    elif x < y:       # would have used an else: statement
        return -1
        
print compare(5,6)

'''
Excellent work distinguishing between fruitful vs void functions :-)
'''