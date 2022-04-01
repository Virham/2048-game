import pygame
import math
pygame.init()

COLOR_PALETTES = [
    (43, 35, 24),
    (68, 13, 18)

]



class Tile:
    def __init__(self, num, pos, size):
        self.num = num
        self.pos = pos
        self.size = size

        self.calculateText()
        self.calculateColor()

    def __add__(self, other):
        return self.num - other if type(other) == int else other.num

    def __mul__(self, other):
        self.num *= other
        self.calculateColor()
        self.calculateText()

    def sameNum(self, other):
        return self.num == other.num

    def calculateText(self):
        self.fontSize = int((1.9 * self.size) / len(str(self.num)))
        self.font = pygame.font.SysFont("Impact", min(self.size, self.fontSize) - 10)
        self.render = self.font.render(str(self.num), False, (255, 255, 255))

    def calculateColor(self):
        log = int(math.log2(self.num))
        r = log * COLOR_PALETTES[0][0]
        g = log * COLOR_PALETTES[0][1]
        b = log * COLOR_PALETTES[0][2]

        self.color = (r % 256, g % 256, b % 256)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos, (self.size, self.size)))
        win.blit(self.render, (self.pos[0] + self.fontSize / 10, self.pos[1]))

    def animate(self, newPos):
        pass