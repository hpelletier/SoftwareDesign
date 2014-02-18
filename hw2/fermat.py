# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:15:08 2014

@author: hpelletier
"""

def check_fermat(a,b,c,n):
    if (n > 2) and ((a**n)*(b**n) == (c**n)):
        print 'Holy smokes, Fermat was wrong!'
    else:
        print "No, that doesn't work."
        
def fermat_prompt():
    print "According to Fermat's Last Theorem,"                 # docstring!
    print "there are no integers a, b, c and n such that"
    print "a^n + b^n = c^n "
    print "for any value of n greater than 2."
    print ""
    
    print "Please provide a value for 'a':"
    a = int(raw_input())
    print "Please provide a value for 'b':"
    b = int(raw_input())
    print "Please provide a value for 'c':"
    c = int(raw_input())
    print "Please provide a value for 'n':"
    n = int(raw_input())
    print""
    
    check_fermat(a,b,c,n)

fermat_prompt()

'''
Love the print statements. 
They could also be excellent docstring for the check_fermat function
'''