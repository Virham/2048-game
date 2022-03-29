import pygame
import random


class Board:
    def __init__(self, x, y, size, gridSize):
        self.x = x
        self.y = y
        self.size = size

        self.gridSize = gridSize
        self.pixelSize = int(size / gridSize)

        self.tiles = [0 for i in range(self.gridSize ** 2)]

        for i in range(10):
            self.tiles[random.randint(0, self.gridSize ** 2 - 1)] = 1

    def move(self, direction):
        for i in range(self.gridSize):
            x = max(-direction[0], 0) * (self.gridSize - 1) + abs(direction[1]) * i
            y = max(-direction[1], 0) * (self.gridSize - 1) + abs(direction[0]) * i
            start = (x, y)

            self.traversDirection(start, direction, self.gridSize - 1)

    def traversDirection(self, pos, direction, depth):
        index = pos[0] + pos[1] * self.gridSize

        if not depth:
            return int(not self.tiles[index])

        canMove = self.traversDirection(pos=(pos[0] + direction[0], pos[1] + direction[1]),
                                        direction=direction, depth=depth - 1)
        if canMove:
            if not self.tiles[index]:
                return canMove + 1

            dest = (pos[0] + canMove * direction[0], pos[1] + canMove * direction[1])
            self.tiles[dest[0] + dest[1] * self.gridSize] = self.tiles[index]
            self.tiles[index] = 0
            return canMove

        return int(not self.tiles[index])

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
