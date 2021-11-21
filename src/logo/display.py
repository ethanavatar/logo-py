from core import run

import pygame
from pygame.locals import *

class App:
    def __init__(self, turtle) -> None:
        self.screen = pygame.display.set_mode((600, 600))
        self.turtle = turtle
        self.running = True

    def run(self, program) -> None:
        for line in program:
            for command in run(line, self.turtle, self):
                #print (command)
                command[0](command[1])
                self.turtle.draw(self.screen)

        while self.running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def clearscreen(self, stub) -> None:
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def comment(self, stub) -> None:
        pass

    def unknown(self, stub) -> None:
        pass
        #print ('Unknown command:', stub)