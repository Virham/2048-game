import pygame
import random
import math
pygame.init()


class Board:
    def __init__(self, x, y, size, gridSize):
        self.x = x
        self.y = y
        self.size = size

        self.gridSize = gridSize
        self.pixelSize = int(size / gridSize)
        self.size = self.gridSize * self.pixelSize  # cuts off few overhanging pixels

        self.tiles = [0 for i in range(self.gridSize ** 2)]

        for i in range(2):
            self.tiles[self.getRandomEmpty()] = 2

    def move(self, direction):
        startTiles = self.tiles.copy()

        for i in range(self.gridSize):
            x = max(-direction[0], 0) * (self.gridSize - 1) + abs(direction[1]) * i
            y = max(-direction[1], 0) * (self.gridSize - 1) + abs(direction[0]) * i
            start = (x, y)

            self.traversDirection(start, direction, self.gridSize - 1)

        if self.gridHasChanged(startTiles):
            self.addRandomTile()

        return not self.gameOver()

    def traversDirection(self, pos, direction, depth):
        index = pos[0] + pos[1] * self.gridSize

        if not depth:
            return int(not self.tiles[index]), False

        canMove, hasMerged = self.traversDirection(pos=(pos[0] + direction[0], pos[1] + direction[1]),
                                                   direction=direction, depth=depth - 1)

        if not hasMerged and depth - canMove > 0:
            moved = self.mergeTiles(pos, index, direction, canMove)
            if moved:
                return moved

        if canMove:
            return self.moveTile(pos, index, direction, canMove)

        return int(not self.tiles[index]), False

    def mergeTiles(self, pos, index, direction, canMove):
        prevT = (pos[0] + (canMove + 1) * direction[0], pos[1] + (canMove + 1) * direction[1])
        prevTI = prevT[0] + prevT[1] * self.gridSize

        if self.tiles[prevTI] == self.tiles[index]:
            self.tiles[prevTI] *= 2
            self.tiles[index] = 0
            return canMove + 1, True

    def moveTile(self, pos, index, direction, canMove):
        if not self.tiles[index]:
            return canMove + 1, False

        dest = (pos[0] + canMove * direction[0], pos[1] + canMove * direction[1])

        self.tiles[dest[0] + dest[1] * self.gridSize] = self.tiles[index]
        self.tiles[index] = 0
        return canMove, False

    def addRandomTile(self):
        num = 2 if random.random() < 0.9 else 4
        tile = self.getRandomEmpty()
        self.tiles[tile] = num

    def gridHasChanged(self, startTiles):
        for i in range(len(self.tiles)):
            if self.tiles[i] - startTiles[i]:
                return True

        return False

    def gameOver(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                index = i + j * self.gridSize

                if not self.tiles[index]:
                    return False

                # check on the x axis
                if i < self.gridSize - 1:
                    nextIndex = (i + 1) + j * self.gridSize
                    if self.tiles[index] == self.tiles[nextIndex]:
                        return False

                # check on the y axis
                if j < self.gridSize - 1:
                    nextIndex = i + (j + 1) * self.gridSize
                    if self.tiles[index] == self.tiles[nextIndex]:
                        return False

        return True

    def getRandomEmpty(self):
        index = random.randint(0, self.gridSize ** 2 - 1)
        if not self.tiles[index]:
            return index

        return self.getRandomEmpty()

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.size, self.size))

        for i in range(len(self.tiles)):
            if self.tiles[i]:
                self.drawTile(win, i)

    def drawTile(self, win, i):
        x = i % self.gridSize
        y = (i - x) // self.gridSize
        pos = (self.x + x * self.pixelSize, self.y + y * self.pixelSize)
        num = self.tiles[i]

        # arbitrary values for generating nice colors
        log = int(math.log2(num))
        r = log * 68
        g = log * 13
        b = log * 18

        pygame.draw.rect(win, (r % 256, g % 256, b % 256), (pos, (self.pixelSize, self.pixelSize)))

        fontSize = int((1.9 * self.pixelSize) / len(str(num)))
        font = pygame.font.SysFont("Impact", min(self.pixelSize, fontSize) - 10)
        text = font.render(str(num), False, (255, 255, 255))
        win.blit(text, (pos[0] + fontSize / 10, pos[1]))
