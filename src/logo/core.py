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
            pygame.draw.line(screen, (255, 255, 255), (self.lastx, self.lasty), (self.x, self.y))

    def set_pen(self, value):
        self.pen = value
        #print (f'{self.pen=}')


repeat = re.compile('repeat (\d*) \[(.*)\] ')
forever = re.compile('forever \[(.*)\] ')
rt = re.compile('rt (\d*) ')
lt = re.compile('lt (\d*) ')
fd = re.compile('fd (\d*) ')

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
        elif repeat.match(token):
            for i in range(int(repeat.match(token).group(1))):
                for action in run(repeat.match(token).group(2), turtle, app):
                    yield action
            token = ''
        elif forever.match(token):
            while True:
                for action in run(forever.match(token).group(1), turtle, app):
                    yield action
        else:
            yield (app.unknown, token)