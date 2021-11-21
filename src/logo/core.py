import re, math

import pygame
from pygame.locals import *

class Turtle:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y

        self.lastx = x
        self.lasty = y

        self.angle = angle

        self.pen = False
        self.line_weight = 1
        self.line_color = (255, 255, 255)

    def right(self, angle):
        self.angle += angle
    
    def left(self, angle):
        self.angle -= angle

    def forward(self, distance):
        if self.pen:
            self.lastx = self.x
            self.lasty = self.y
            self.x += distance * math.cos(math.radians(self.angle))
            self.y += distance * math.sin(math.radians(self.angle))
        else:
            self.x += distance * math.cos(math.radians(self.angle))
            self.y += distance * math.sin(math.radians(self.angle))
            self.lastx = self.x
            self.lasty = self.y

    def draw(self, screen):
        if self.pen == True:
            pygame.draw.line(screen, self.line_color, (self.lastx, self.lasty), (self.x, self.y), self.line_weight)

    def set_pen(self, value):
        self.pen = value
        #print (f'{self.pen=}')

    def set_line_weight(self, value):
        self.line_weight = value

    def set_line_color(self, value):
        print (value)
        self.line_color = value

    def set_visible(self, value):
        raise NotImplementedError

    def set_x(self, value):
        if self.pen:
            self.lastx = self.x
            self.x = value
        else:
            self.x = value
            self.lastx = value
    
    def set_y(self, value):
        if self.pen:
            self.lasty = self.y
            self.y = value
        else:
            self.y = value
            self.lasty = value


repeat = re.compile('repeat (\d*) \[(.*)\] ')
forever = re.compile('forever \[(.*)\] ')
rt = re.compile('rt (\d*) ')
lt = re.compile('lt (\d*) ')
fd = re.compile('fd (\d*) ')
setpensize = re.compile('setpensize (\d*) ')
setpencolor = re.compile('setpencolor \[(\d*) (\d*) (\d*)\] ')
setx = re.compile('setx (\d*) ')
sety = re.compile('sety (\d*) ')
setxy = re.compile('setxy (\d*) (\d*) ')


comment = re.compile('#(.*)\n')

def run(line, turtle, app):
    token = ''
    for char in line:
        token += char
        #print (token)
        if comment.match(token):
            yield (app.comment, token)
            token = ''
        elif rt.match(token):
            yield (turtle.right, int(rt.match(token).group(1)))
            token = ''
        elif lt.match(token):
            yield (turtle.left, int(lt.match(token).group(1)))
            token = ''
        elif fd.match(token):
            yield (turtle.forward, int(fd.match(token).group(1)))
            token = ''
        elif token == 'cs ':
            yield (app.clearscreen, None)
            token = ''
        elif token == 'pu ':
            yield (turtle.set_pen, False)
            token = ''
        elif token == 'pd ':
            yield (turtle.set_pen, True)
            token = ''
        elif token == 'ht ':
            yield (turtle.set_visible, False)
            token = ''
        elif token == 'st ':
            yield (turtle.set_visible, True)
            token = ''

        elif setx.match(token):
            yield (turtle.set_x, int(setx.match(token).group(1)))
            token = ''
        elif sety.match(token):
            yield (turtle.set_y, int(sety.match(token).group(1)))
            token = ''
        elif setxy.match(token):
            yield (turtle.set_x, int(setxy.match(token).group(1)))
            yield (turtle.set_y, int(setxy.match(token).group(2)))
            token = ''

        elif setpencolor.match(token):
            yield (turtle.set_line_color, (int(setpencolor.match(token).group(1)), int(setpencolor.match(token).group(2)), int(setpencolor.match(token).group(3))))
            token = ''

        elif setpensize.match(token):
            yield (turtle.set_line_weight, int(setpensize.match(token).group(1)))
            token = ''
        
        elif repeat.match(token):
            for i in range(int(repeat.match(token).group(1))):
                for action in run(repeat.match(token).group(2), turtle, app):
                    yield action
            token = ''
        elif forever.match(token):
            raise NotImplementedError
            while True:
                for action in run(forever.match(token).group(1), turtle, app):
                    yield action
        else:
            yield (app.unknown, token)