import pygame
import math
pygame.init()


class Tile:
    COLOR_PALETTES = [
        (43, 35, 24),
        (68, 13, 18)

    ]

    START_GROW = 0.5

    def __init__(self, num, pos, size):
        self.num = num
        self.visualNum = self.num

        self.pos = pos
        self.startPos = self.pos
        self.endPos = self.pos

        self.maxSize = size
        self.size = size

        self.color = None
        self.fontSize = None
        self.font = None
        self.render = None

        self.calculateColor()

    def __add__(self, other):
        return self.num - other if type(other) == int else other.num

    def merge(self):
        self.num *= 2

    def sameNum(self, other):
        return self.num == other.num

    def calculateText(self):
        self.fontSize = int((1.9 * self.size) / len(str(self.visualNum)))
        self.font = pygame.font.SysFont("Impact", min(self.size, self.fontSize) - 10)
        self.render = self.font.render(str(self.visualNum), False, (255, 255, 255))

    def calculateColor(self):
        log = int(math.log2(self.num))
        r = log * self.COLOR_PALETTES[0][0]
        g = log * self.COLOR_PALETTES[0][1]
        b = log * self.COLOR_PALETTES[0][2]

        self.color = (r % 256, g % 256, b % 256)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos, (self.size, self.size)))
        if self.render:
            win.blit(self.render, (self.pos[0] + self.fontSize / 10, self.pos[1]))

    def spawnTile(self, dt):
        dt = max(0, (dt - self.START_GROW) / self.START_GROW)

        self.size = int(self.maxSize * dt)

        centerX = self.startPos[0] + self.maxSize / 2
        centerY = self.startPos[1] + self.maxSize / 2

        x = centerX - self.size / 2
        y = centerY - self.size / 2
        self.pos = (x, y)

    def increaseTile(self, dt):
        pass

    def moveTile(self, dt):
        sX = self.startPos[0]
        sY = self.startPos[1]

        eX = self.endPos[0]
        eY = self.endPos[1]

        x = sX * (1 - dt) + eX * dt
        y = sY * (1 - dt) + eY * dt

        self.pos = (x, y)

    def animationDone(self):
        self.pos = self.endPos
        self.startPos = self.pos

        self.size = self.maxSize
        self.visualNum = self.num

        self.calculateText()
        self.calculateColor()
