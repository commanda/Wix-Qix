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

# cursor movement rate constants
fast_rate = 8
slow_rate = 4
no_rate = 0

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


class Lines(Layer):
    def __init__(self, start_point):
        super(Lines, self).__init__()
        # Collection of lines we're currently working on drawing
        self.currentFinishedLines = []
        self.color = 255,255,255,255
        self.width = 3
        self.currentLine = Line(start_point, start_point, self.color, self.width)
    
    
    def end_line_at_point(self, point):
        new_start = self.currentLine.end
        self.currentFinishedLines.append(self.currentLine)
        self.currentLine = Line(new_start, point, self.color, self.width)
        
    
    def add_point(self, point):
        self.currentLine.end = point
    
    def draw(self):
        glPushMatrix()
        self.transform()
        
        self.currentLine.draw()
        
        for line in self.currentFinishedLines:
            line.draw()
        
        glPopMatrix()






class Cursor( Sprite ):
    
    def __init__(self, image, boundingRect, lines):
        super(Cursor, self).__init__(image)
        
        
        self.position = boundingRect.rect.midbottom
    
        self.rate = fast_rate
        self.boundingRect = boundingRect
        self.lines = lines
        self.direction = 0
        

        
    def move_up(self):
        new_direction = key.UP
        if self.position[Y] < self.boundingRect.rect.top:
            self.lines.add_point(self.position)
            self.position = self.position[X], self.position[Y]+self.rate
            
        else:
            self.lines.end_line_at_point(self.position)
        if new_direction != self.direction:
            self.lines.end_line_at_point(self.position)
        
        self.direction = new_direction            
            
            
    def move_down(self):
        new_direction = key.DOWN
        if self.position[Y] > self.boundingRect.rect.bottom:
            self.lines.add_point(self.position)
            self.position = self.position[X], self.position[Y]-self.rate 
            
        else:
            self.lines.end_line_at_point(self.position)
        if new_direction != self.direction:
            self.lines.end_line_at_point(self.position)
        
        self.direction = new_direction


    def move_left(self):
        new_direction = key.LEFT
        if self.position[X] > self.boundingRect.rect.left:
            self.lines.add_point(self.position)
            self.position = self.position[X]-self.rate, self.position[Y]
            
        else:
            self.lines.end_line_at_point(self.position)
        if new_direction != self.direction:
            self.lines.end_line_at_point(self.position)
        
        self.direction = new_direction
    
    def move_right(self):
        new_direction = key.RIGHT
        if self.position[X] < self.boundingRect.rect.right:
            self.lines.add_point(self.position)
            self.position = self.position[X]+self.rate, self.position[Y]
                    
        else:
            self.lines.end_line_at_point(self.position)
        
        if new_direction != self.direction:
            self.lines.end_line_at_point(self.position)
        
        self.direction = new_direction
        


class GameControl (Layer):
    
    is_event_handler = True
    
    
    def __init__(self, cursor):
        super(GameControl, self).__init__()
        self.cursor = cursor
        self.held_down_key = 0
        
       
        
    def on_key_press(self, pressed, modifiers):
        if pressed == key.UP:
            self.cursor.move_up()
        elif pressed == key.DOWN:
            self.cursor.move_down()
        elif pressed == key.LEFT:
            self.cursor.move_left()
        elif pressed == key.RIGHT:
            self.cursor.move_right()
            
            
     
    def on_text(self, text):
        if text == 'x':
            print 'x'
            self.cursor.rate = slow_rate
        elif text == 'z':
            self.cursor.rate = fast_rate
        else:
            self.cursor.rate = no_rate
    
    def on_key_release(self, symbol, modifiers):
        if symbol in (key.X, key.Z):
            self.cursor.rate = no_rate
        
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

    start_point = boundingRect.rect.midbottom

    lines = Lines(start_point)
    #lines.end_line_at_point(start_point)
    scene.add(lines, z=0)
    
    image = pyglet.resource.image('cursor.png')
    cursor = Cursor(image, boundingRect, lines)
    scene.add( cursor, z=1)
    scene.add( GameControl(cursor) )
    scene.add(boundingRect, z=1)
    
    director.run(scene)
