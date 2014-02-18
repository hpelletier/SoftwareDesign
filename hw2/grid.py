# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:00:23 2014

@author: hpelletier
"""
    
def draw_column(col):
    print '+ - - - - +',(' - - - - +')*(col-1)
    print '|         |',('         |')*(col-1)
    print '|         |',('         |')*(col-1)
    print '|         |',('         |')*(col-1)
    print '|         |',('         |')*(col-1)
    print '+ - - - - +',(' - - - - +')*(col-1)
                  
def draw_row(col):
    print '|         |', ('         |')*(col-1)
    print '|         |', ('         |')*(col-1)
    print '|         |', ('         |')*(col-1)
    print '|         |', ('         |')*(col-1)
    print '+ - - - - +', (' - - - - +')*(col-1)
          
def draw_2x2_grid():
    draw_column(2)
    draw_row(2)
    
def draw_4x4_grid():
    draw_column(4)
    draw_row(4)
    draw_row(4)
    draw_row(4)
    
draw_2x2_grid()
draw_4x4_grid()

'''
Love the use of auxiliary functions. Good work!
'''