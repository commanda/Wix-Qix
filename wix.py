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

from primitives import *

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




class FillRectLayer(Layer):
    def __init__(self, vertices, color):
        super(FillRectLayer, self).__init__()
        self.polygon = Polygon(vertices,color=(.3,0.2,0.5,1.0))

    def draw(self):
        self.polygon.render()







class BoundingRect(Layer):
    def __init__(self, rect):
        super(BoundingRect, self).__init__()
        color = 0,153,204,255
        width = 8
        self.rect = rect
        self.bottom = Line(rect.bottomleft, rect.bottomright, color, width)
        self.right = Line(rect.bottomright, rect.topright, color, width)
        self.top = Line(rect.topright, rect.topleft, color, width)
        self.left = Line(rect.topleft, rect.bottomleft, color, width)
        self.edges = [self.bottom, self.right, self.top, self.left]
        
        
    def draw(self):
        glPushMatrix()
        self.bottom.draw()
        self.top.draw()
        self.left.draw()
        self.right.draw()
        glPopMatrix()


class Lines(Layer):
    def __init__(self, boundingBox, start_point):
        super(Lines, self).__init__()
        self.boundingBox = boundingBox
        # Collection of lines we're currently working on drawing
        self.oldFinishedLines = []
        self.currentFinishedLines = []
        self.color = 255,255,255,255
        self.width = 3
        self.currentLine = Line(start_point, start_point, self.color, self.width)
        self.finishedBoxes = []
        self.last_point_on_wall = start_point
        self.start_wall = self.boundingBox.bottom
        self.box_color = 255,255,0,255
        
    
    def end_line_at_point(self, point):
        print 'end line at: '+str(point)
        if point == self.last_point_on_wall:
            print 'ignoring'
            return
    
        # Add this last point to our current line
        # EDIT: no, don't, that will make this line slanted if we just changed directions
        # self.currentLine.end = point
        
        new_start = self.currentLine.end
        self.currentFinishedLines.append(self.currentLine)
        
        wall_hit = -1
        
        corner_point1 = -1,-1
        corner_point2 = -1,-1
        
        start_wall_index = self.boundingBox.edges.index(self.start_wall)
        for wall_hit_index, wall in enumerate(self.boundingBox.edges):
            if self.is_point_on_line(point, wall):
                wall_hit = wall
                print 'wall hit index: ' + str(wall_hit_index)
                num_vertices_to_add = 0
                # Find out if the start wall is the end wall, 
                # or if they're adjacent, 
                # or if they're opposite
                if self.start_wall == wall_hit:
                    num_vertices_to_add = 1
                
                if ((wall_hit_index -1) % 4 == start_wall_index):
                    # they're adjacent
                    corner_point1 = wall_hit.start
                if ((wall_hit_index +1) % 4 == start_wall_index):
                    corner_point1 = wall_hit.end
            
                    
            
        if wall_hit != -1:
            
            # We did hit a wall. 
            print 'wall hit'
            # Add the current point to our current line
            #self.currentLine.end = point
        
        
            # There will be either 0, 1, or 2 missing corners
            # 0 is when we start and ended on the same wall/line
            # 1 is when we started on one line and ended on another that is perpendicular
            # 2 is when we started and ended on parallel lines
        
            # Find the index         
            
            # Add all our vertices and make a big polygon.
            vertices = []
            for line in self.currentFinishedLines:
                vertices.append(line.start)
                vertices.append(line.end)
                
            
            if corner_point1[X] != -1:
                # Add this corner as a vertex to our polygon
                vertices.append(corner_point1)
                
            print vertices
            # We now need to pretend that the blue bounding box is part of this polygon
            # Find which two or three sides of the bounding box are involved in this rect
            # Take part of the wall we just hit, from the point we hit at until the corner that's
            # closest to the last_point_on_wall, the closing point
            
            
            
            polygon = FillRectLayer(vertices, self.box_color)
            self.finishedBoxes.append(polygon)
            
            # Save this point, because it's now the last time we hit a wall
            self.last_point_on_wall = point
            
            # Save this line because it's now the last wall we hit
            self.start_wall = wall_hit
            
            # Move all our current lines into the old lines collection
            for line in self.currentFinishedLines:
                self.oldFinishedLines.append(line)
            # Delete everything from the currentFinishedLines, we're restarting
            self.currentFinishedLines = []
            
        # Start a new line because we just finished the old line    
        self.currentLine = Line(new_start, point, self.color, self.width)
        
        
    def line_length(self, line):
        if line.start[X] == line.end[X]:
            return math.fabs(line.start[Y] - line.end[Y])
        else:
            return math.fabs(line.start[X] - line.end[X])
            
    
    #def is_parallel(self, line1, line2):
    #    if line1.start[X] 
    
    def is_point_on_line(self, point, line):
        if point[X] == line.start[X]:
            if line.start[Y] <= point[Y] and point[Y] <= line.end[Y]:
                return True
            if line.end[Y] <= point[Y] and point[Y] <= line.start[Y]:
                return True
        if point[Y] == line.start[Y]:
            if line.start[X] <= point[X] and point[X] <= line.end[X]:
                return True
            if line.end[X] <= point[X] and point[X] <= line.start[X]:
                return True
            
        return False
            
    
    def add_point(self, point):
        print 'add point: '+str(point)
        self.currentLine.end = point
        wall_hit = -1
        # if point[X] == self.boundingBox.left or point[X] == self.rect.right or point[Y] == self.rect.top or point[Y] == self.rect.bottom:
        if self.is_point_on_line(point, self.boundingBox.left) or self.is_point_on_line(point, self.boundingBox.right) or self.is_point_on_line(point, self.boundingBox.top) or self.is_point_on_line(point, self.boundingBox.bottom):
            self.end_line_at_point(point)
        
    
    def draw(self):
        glPushMatrix()
        self.transform()
        
        # Tell all our finished boxes to draw
        for box in self.finishedBoxes:
            box.draw()
        
        # Tell all our lines to draw
        self.currentLine.draw()
        
        for line in self.oldFinishedLines:
            line.draw()
        
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
            self.position = self.position[X], self.boundingRect.rect.top
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
            self.position = self.position[X], self.boundingRect.rect.bottom
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
            self.position = self.boundingRect.rect.left, self.position[Y]
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
            self.position = self.boundingRect.rect.right, self.position[Y]
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

    lines = Lines(boundingRect, start_point)
    #lines.end_line_at_point(start_point)
    scene.add(lines, z=0)
    
    image = pyglet.resource.image('cursor.png')
    cursor = Cursor(image, boundingRect, lines)
    scene.add( cursor, z=1)
    scene.add( GameControl(cursor) )
    scene.add(boundingRect, z=1)
    
    
    
    director.run(scene)
