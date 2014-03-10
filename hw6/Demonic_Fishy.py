# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: sgrimshaw, mkeene & hpelletier
"""

import pygame
from pygame.locals import *
from pygame.mixer import *
import random
import math
import time

x_size = 1000   #size of the game window
y_size = 700

class FishyModel:
    """ Encodes the game state """
    
    def __init__(self):        
        self.max_radius = 30   #inital maximum radius of the other fish
        
        self.left_fishies = []   #creates an inital wave of fish that come in from left and stores them in a list
        for y in range(self.max_radius,y_size,(y_size/6)-1):
            left_fishy = LeftFish((random.randint(0,255),random.randint(0,255),random.randint(0,255)),random.randint(2,self.max_radius),1,y)
            self.left_fishies.append(left_fishy)
                
        self.right_fishies = []   #creates an inital wave of fish that come in from right and stores them in a list
        for y in range(30,y_size,(y_size/6)-1):
            right_fishy = RightFish((random.randint(0,255),random.randint(0,255),random.randint(0,255)),random.randint(2,self.max_radius),x_size-1,y)
            self.right_fishies.append(right_fishy)
            
        self.mainFish = MainFish((255,255,255),10,x_size/2,y_size/2)      
          
    def update(self):
        """ Updates the state of the model """
        mainFish = self.mainFish       
        mainFish.update()
        FishyModel.collision(self)
        FishyModel.createFish(self)
        for fish in self.left_fishies:
            fish.update()
        for fish in self.right_fishies:
            fish.update()
            
    def createFish(self):
        """ Generates new random fish """
        
        if self.mainFish.radius < 55:    #stops generating new fish once the main fish reaches its maximum (win state) radius
            create = random.randint(1,10)
            if create == 8:
                fish = RightFish((random.randint(0,255),random.randint(0,255),random.randint(0,255)),random.randint(2,self.max_radius),x_size+self.max_radius,random.randint(self.max_radius,y_size-self.max_radius))
                self.right_fishies.append(fish)
            if create == 9:
                fish = LeftFish((random.randint(0,255),random.randint(0,255),random.randint(0,255)),random.randint(2,self.max_radius),0-self.max_radius,random.randint(self.max_radius,y_size-self.max_radius))
                self.left_fishies.append(fish)
                
        else:  #win state: stops the main fish's movement, pauses the game, and quits once the sound effect has been played
            self.mainFish.vx = 0
            self.mainFish.vy = 0               
            youWin.play()           
            
            
    def collision(self):
        """Detects collisions bewtween the main fish and other fish"""
        mainFish = self.mainFish
        left_fishies = self.left_fishies
        right_fishies = self.right_fishies        
        radMain = mainFish.radius
        
        for fish in self.left_fishies:
            radFish = fish.radius
            dist= math.sqrt((fish.x-mainFish.x)**2+(fish.y-mainFish.y)**2)
            if dist<= (radFish+radMain):
                if radFish > radMain:  #if the other fish is bigger, sound effect plays, game ends
                    ohDear.play()
                    pygame.time.wait(900)
                    pygame.quit()
                elif radFish <= radMain:  #if the main fish is bigger, sound effect plays, smaller fish is eaten (removed from list)
                    self.mainFish.radius += 1
                    nom.play()
                    left_fishies.remove(fish)                    
                    if self.max_radius < 50:
                        self.max_radius += 1
                        
        for fish in self.right_fishies:
            radFish = fish.radius
            dist= math.sqrt((fish.x-mainFish.x)**2+(fish.y-mainFish.y)**2)
            if dist<= (radFish+radMain):
                if radFish > radMain:   #if the other fish is bigger, sound effect plays, game ends
                    ohDear.play()
                    pygame.time.wait(900)
                    pygame.quit()
                elif radFish <= radMain:   #if the main fish is bigger, sound effect plays, smaller fish is eaten (removed from list)
                    self.mainFish.radius += 1
                    nom.play()
                    right_fishies.remove(fish) 
                    if self.max_radius < 50:
                        self.max_radius += 1
        
class LeftFish:
    """ Encodes the state of the fish that swim in from the left in the game """
    def __init__(self,color,radius,x,y):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = random.randint(4,9)
        
    def update(self):
        """ updates the state of the fish """
        self.x += self.vx
        
class RightFish:
    """ Encodes the state of the fish that swim in from the right in the game """
    def __init__(self,color,radius,x,y):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = random.randint(4,9)
        
    def update(self):
        """ updates the state of the fish """
        self.x -= self.vx

class MainFish:
    """ Encodes the state of the main (user controlled) fish in the game """
    def __init__(self,color,radius,x,y):
        self.color = color        
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
    
    def update(self):
        """ updates the state of the fish """
        # limits the movement of the fish to inside the game window and causes it to bounce off the edges
        Right_Limit = x_size -self.radius
        Left_Limit = 0 + self.radius
        Up_Limit = 0 + self.radius
        Down_Limit = y_size - self.radius
        
        moveHorz = True
        moveVert = True
        
        if self.x >= Right_Limit:
            moveHorz = False
            self.x = Right_Limit-1
            self.vx = int(-self.vx/2)
            boop.play()
        if self.x <= Left_Limit:
            moveHorz = False
            self.x = Left_Limit+1
            self.vx =int(-self.vx/2) 
            boop.play()
        if self.y <= Up_Limit:
            moveVert = False
            boop.play()
            self.y = Up_Limit+1
            self.vy = int(-self.vy/2)            
        if self.y >= Down_Limit:
            moveVert = False
            boop.play()
            self.y = Down_Limit-1
            self.vy = int(-self.vy/2)
            
        # normal movement of fish  
        if moveHorz == True:
            self.x += self.vx           
        if moveVert == True:
            self.y += self.vy           
        
class PyGameWindowView:
    """ A view of fishy rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(pygame.Color(0,120,185))
        
        for fishy in self.model.left_fishies:
            pygame.draw.circle(self.screen,pygame.Color(fishy.color[0],fishy.color[1],fishy.color[2]),(fishy.x,fishy.y),fishy.radius)
                            
        for fishy in self.model.right_fishies:
            pygame.draw.circle(self.screen,pygame.Color(fishy.color[0],fishy.color[1],fishy.color[2]),(fishy.x,fishy.y),fishy.radius)
            
        mainFish = self.model.mainFish
        pygame.draw.circle(self.screen,pygame.Color(mainFish.color[0],mainFish.color[1],mainFish.color[2]),(mainFish.x,mainFish.y),mainFish.radius)     
        pygame.display.update()
        
class PyGameKeyboardController:
    """ Handles keyboard input """
    def __init__(self,model):
        self.model = model    
           
    def handle_keyboard_event(self,event):        
        keys = pygame.key.get_pressed()
        if keys[K_UP]:        
            self.model.mainFish.vy += -1      
        if keys[K_LEFT]:
            self.model.mainFish.vx += -1            
        if keys[K_RIGHT]:
            self.model.mainFish.vx += 1
        if keys[K_DOWN]:
            self.model.mainFish.vy += 1

if __name__ == '__main__':
    
    pygame.mixer.pre_init(44100,-16,2,2048) #pre-initializes the mixer
    
    pygame.init()
    
    boop = pygame.mixer.Sound('boop.wav')  #sound effects
    ohDear = pygame.mixer.Sound('ohDear.wav')
    nom = pygame.mixer.Sound('nom.wav')
    youWin = pygame.mixer.Sound('youWin.wav')
        
    size = (x_size,y_size)
    screen = pygame.display.set_mode(size)

    model = FishyModel()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:                
                running = False
         
        controller.handle_keyboard_event(event)            
          
        model.update()
        view.draw()
        time.sleep(.06)
   
    pygame.quit()