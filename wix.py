# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from operator import setslice

from cocos.director import director
from cocos.layer import *
from cocos.scene import Scene
from cocos.scenes.transitions import *
from cocos.actions import *
from cocos.sprite import *
from cocos.menu import *
from cocos.text import *
from cocos.rect import *
from cocos.draw import *

import pyglet
from pyglet import gl, font
from pyglet.window import key

# position coordinate indices (constants)
X = 0
Y = 1

class BackgroundLayer( Layer ):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background.png')
        
    def draw(self):
        glPushMatrix()
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.transform()
        #self.img.blit(0,0)
        glPopMatrix()


class BoundingRect(Layer):
    def __init__(self, rect):
        super(BoundingRect, self).__init__()
        color = 0,153,204,255
        width = 8
        self.rect = rect
        self.bottom = Line(rect.bottomleft, rect.bottomright, color, width)
        self.top = Line(rect.topleft, rect.topright, color, width)
        self.left = Line(rect.bottomleft, rect.topleft, color, width)
        self.right = Line(rect.bottomright, rect.topright, color, width)
        
    def draw(self):
        glPushMatrix()
        self.bottom.draw()
        self.top.draw()
        self.left.draw()
        self.right.draw()
        glPopMatrix()
        

class Cursor( Sprite ):
    
    def __init__(self, image, boundingRect):
        super(Cursor, self).__init__(image)
        
        self.position = 50, 50
        self.rate = 10
        self.boundingRect = boundingRect
        
    def move_up(self):
        print self.position
        if self.position[Y] < self.boundingRect.rect.top:
            self.position = self.position[X], self.position[Y]+self.rate 
    
    def move_down(self):
        print self.position
        if self.position[Y] > self.boundingRect.rect.bottom:
            self.position = self.position[X], self.position[Y]-self.rate 

    def move_left(self):
        print self.position
        if self.position[X] > self.boundingRect.rect.left:
            self.position = self.position[X]-self.rate, self.position[Y]
    
    def move_right(self):
        print self.position
        if self.position[X] < self.boundingRect.rect.right:
            self.position = self.position[X]+self.rate, self.position[Y]
    



class GameControl (Layer):
    
    is_event_handler = True
    
    def __init__(self, cursor):
        super(GameControl, self).__init__()
        self.cursor = cursor
        print 'cursor: ' + str(cursor)
        
    def on_key_press(self, pressed, modifiers):
        if pressed == key.UP:
            self.cursor.move_up()
        elif pressed == key.DOWN:
            self.cursor.move_down()
        elif pressed == key.LEFT:
            self.cursor.move_left()
        elif pressed == key.RIGHT:
            self.cursor.move_right()
        
    def on_text_motion(self, motion):
        if motion == key.MOTION_DOWN:
            self.cursor.move_down()
        elif motion == key.MOTION_UP:
            self.cursor.move_up()            
        elif motion == key.MOTION_LEFT:
            self.cursor.move_left()
        elif motion == key.MOTION_RIGHT:
            self.cursor.move_right()


if __name__ == "__main__":
    print 'main!'
    
    director.init(resizable=True, width=800, height=800)
    scene = Scene()
    scene.add( BackgroundLayer(), z=0)
    
    rect = Rect(50, 50, 700, 700)
    boundingRect = BoundingRect(rect)
    image = pyglet.resource.image('cursor.png')
    cursor = Cursor(image, boundingRect)
    scene.add( cursor, z=1)
    scene.add( GameControl(cursor) )
    scene.add(boundingRect, z=1)
    
    director.run(scene)
        