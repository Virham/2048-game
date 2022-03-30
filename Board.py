import pygame
import random
pygame.init()


class Board:
    def __init__(self, x, y, size, gridSize):
        self.x = x
        self.y = y
        self.size = size

        self.gridSize = gridSize
        self.pixelSize = int(size / gridSize)
        self.size = self.gridSize * self.pixelSize  # cuts off few overhanging pixels

        self.font = pygame.font.SysFont("Impact", self.pixelSize)
        self.tiles = [0 for i in range(self.gridSize ** 2)]

    def move(self, direction):
        for i in range(self.gridSize):
            x = max(-direction[0], 0) * (self.gridSize - 1) + abs(direction[1]) * i
            y = max(-direction[1], 0) * (self.gridSize - 1) + abs(direction[0]) * i
            start = (x, y)

            self.traversDirection(start, direction, self.gridSize - 1)

    def traversDirection(self, pos, direction, depth):
        index = pos[0] + pos[1] * self.gridSize

        if not depth:
            return int(not self.tiles[index]), False

        canMove, hasMerged = self.traversDirection(pos=(pos[0] + direction[0], pos[1] + direction[1]),
                                        direction=direction, depth=depth - 1)

        if not hasMerged and depth - canMove > 0:
            prevT = (pos[0] + (canMove + 1) * direction[0], pos[1] + (canMove + 1) * direction[1])
            prevTI = prevT[0] + prevT[1] * self.gridSize

            if self.tiles[prevTI] == self.tiles[index]:
                self.tiles[prevTI] *= 2
                self.tiles[index] = 0
                return canMove + 1, True

        if canMove:
            if not self.tiles[index]:
                return canMove + 1, False

            dest = (pos[0] + canMove * direction[0], pos[1] + canMove * direction[1])

            self.tiles[dest[0] + dest[1] * self.gridSize] = self.tiles[index]
            self.tiles[index] = 0
            return canMove, False

        return int(not self.tiles[index]), False

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.size, self.size))

        for i in range(len(self.tiles)):
            if self.tiles[i]:
                self.drawTile(win, i)

    def drawTile(self, win, i):
        x = i % self.gridSize
        y = (i - x) // self.gridSize
        pos = (self.x + x * self.pixelSize, self.y + y * self.pixelSize)

        pygame.draw.rect(win, (0, 0, 0), (pos, (self.pixelSize, self.pixelSize)))
        text = self.font.render(str(self.tiles[i]), False, (255, 255, 255))
        win.blit(text, pos)