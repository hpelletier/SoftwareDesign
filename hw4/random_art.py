# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo & hpelletier
"""
from random import randint
from math import *
import Image

def build_random_function(min_depth,max_depth):
    """Builds a random generated function consisting of certain building blocks
        Inputs: min_depth: minimum depth (degree of nestedness) of the function
                max_depth: maximum depth (degree of nestedness) of the function
        Output: a randomly generated function of depth between min_depth and max_depth
    """

    if max_depth >= 2 and min_depth >= 2:
        int = randint(0,4)        # be careful not to use one of Python's keywords as a variable
        if int == 0:
            List = ['prod',build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
        elif int == 1:
            List = ['cos_pi',build_random_function(min_depth-1,max_depth-1)]
        elif int == 2:            
            List = ['sin_pi',build_random_function(min_depth-1,max_depth-1)]
        elif int == 3:
            List = ['avg',build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
        elif int == 4:            
            List = ['cube',build_random_function(min_depth-1,max_depth-1)]          
    
    elif max_depth >= 2 and min_depth < 2:
        int = randint(0,6)        
        if int == 0:
            List = ['prod',build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
        elif int == 1:
            List = ['cos_pi',build_random_function(min_depth-1,max_depth-1)]
        elif int == 2:            
            List = ['sin_pi',build_random_function(min_depth-1,max_depth-1)]
        elif int == 3:
            List = ['avg',build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
        elif int == 4:            
            List = ['cube',build_random_function(min_depth-1,max_depth-1)]          
        elif int == 5:            
            List = ['x']            
        elif int == 6:        
            List = ['y']
    
    else:
        int = randint(0,1)
        if int == 0:            
            List = ['x']            # same thing here. "list" is a keyword in Python. Avoid using them as variable names
        elif int == 1:        
            List = ['y']
        
    return List

'''
The logic definitely works, but the way it's written seems rather inefficient. What if you stored the names of your building block functions
as a list? Could you use the fact that randint takes in a minimum and maxmium to make a simpler function?

Also, your "else" block is your base case. It doesn't make a big difference, but you generally want to check for base case before other cases.
'''

#print build_random_function(2,5)

def evaluate_random_function(f, x, y):
    """Evaluates a given random function (of the kind produced by build_random_function)
       for the given x and y values
       Inputs: f: random function
               x: x value
               y: y value
       Output: the value of the evalutated function (single number)
    """
  
    if f[0] == 'avg':
        output = float((evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))/2.0)           
    elif f[0] == 'cube':
        output = float(evaluate_random_function(f[1],x,y)**3.0)
    elif f[0] == 'prod':
        output = float(evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y))
    elif f[0] == 'cos_pi':
        output = float(cos(pi*evaluate_random_function(f[1],x,y)))
    elif f[0] == 'sin_pi':
        output = float(sin(pi*evaluate_random_function(f[1],x,y)))
    elif f[0] == 'x':
        output = float(x)
    elif f[0] == 'y':
        output = float(y)
            
    return output

'''
The 'x' and 'y' are your base cases, so you want to check for those before checking for others.
'''
#print evaluate_random_function(build_random_function(2,5),-0.5,0.7)

def remap_interval(x,a,b,c,d):      # I personally appreciate that you changed the variable names to simpler ones. :-)
    """ Maps the input value in the given input range to an 
        output value in the given output range
        Inputs: x: Input value
                a: Input range start
                b: Input range end
                c: Output range start
                d: Output range end
        Output: Output value (in the output range)
    """
    # your code goes here
    
    x = float(x)
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)

    return float((x-a)/(b-a)*(d-c)+c)
    
#print remap_interval(5.0,0,10,-1,1)

def create_random_art():
    """Creates a 350x350 RBG image using randomly generated functions 
       (via build_random_function) to determine values for the red, blue, 
       and green channels        
    """
        
    red_f = build_random_function(5,15)
    green_f = build_random_function(5,15)
    blue_f = build_random_function(5,15)

    img = Image.new("RGB",(350,350))
    pixel_map = img.load() 
    
    for i in range(0,349):
        
        x = float(remap_interval(float(i),0,349,-1,1))
        
        for j in range(0,349):
            
            y = float(remap_interval(float(j),0,349,-1,1))
            
            # I personally recommending breaking up the following three lines to make them more readable.
            red = remap_interval(float(evaluate_random_function(red_f,x,y)),-1,1,0,255)
            green = remap_interval(float(evaluate_random_function(green_f,x,y)),-1,1,0,255)
            blue = remap_interval(float(evaluate_random_function(blue_f,x,y)),-1,1,0,255)
            
            pixel_map[i,j] = (int(red),int(green),int(blue))            

    img.save('/home/hpelletier/SoftwareDesign/hw4/art100','jpeg') #saves art as a jpeg to hw4 folder
           
#create_random_art()
