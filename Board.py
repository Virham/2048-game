import pygame
import random
import math
import time

from Tile import Tile
pygame.init()


class Board:
    MOVE = "Move"
    INCREASE = "Increase"
    SPAWN = "Spawn"

    def __init__(self, x, y, size, gridSize):
        self.x = x
        self.y = y
        self.size = size

        self.gridSize = gridSize
        self.pixelSize = int(size / gridSize)
        self.size = self.gridSize * self.pixelSize  # cuts off few overhanging pixels

        self.tiles = [0 for i in range(self.gridSize ** 2)]

        self.animationSpeed = 5
        self.animationTiles = []
        self.animations = {
            self.MOVE: lambda tile, dt: tile.moveTile(dt),
            self.INCREASE: lambda tile, dt: tile.increaseTile(dt),
            self.SPAWN: lambda tile, dt: tile.spawnTile(dt)
        }


        self.GenerateStartingBoard()

    def GenerateStartingBoard(self):
        for i in range(2):
            self.addRandomTile().calculateText()

    def changePos(self, index, newIndex):
        tile = self.tiles[index]
        tile.endPos = self.getPos(newIndex)

        return tile

    def makeTile(self, num, index):
        return Tile(num, self.getPos(index), self.pixelSize)

    def getPos(self, index):
        x = index % self.gridSize
        y = (index - x) // self.gridSize

        return self.x + x * self.pixelSize, self.y + y * self.pixelSize

    def move(self, direction, win):
        self.animationTiles = []
        startTiles = self.tiles.copy()

        for i in range(self.gridSize):
            x = max(-direction[0], 0) * (self.gridSize - 1) + abs(direction[1]) * i
            y = max(-direction[1], 0) * (self.gridSize - 1) + abs(direction[0]) * i
            start = (x, y)

            self.traversDirection(start, direction, self.gridSize - 1)

        if self.gridHasChanged(startTiles):
            self.addRandomTile()

        self.animateChanges(win)

        return not self.gameOver()

    def traversDirection(self, pos, direction, depth):
        index = pos[0] + pos[1] * self.gridSize

        if not depth:
            return int(not self.tiles[index]), False

        canMove, hasMerged = self.traversDirection(pos=(pos[0] + direction[0], pos[1] + direction[1]),
                                                   direction=direction, depth=depth - 1)

        if not hasMerged and depth - canMove > 0:
            moved = self.tryMergeTiles(pos, index, direction, canMove)
            if moved:
                return moved

        if canMove:
            return self.moveTile(pos, index, direction, canMove)

        return int(not self.tiles[index]), False

    def tryMergeTiles(self, pos, index, direction, canMove):
        prevT = (pos[0] + (canMove + 1) * direction[0], pos[1] + (canMove + 1) * direction[1])
        prevI = prevT[0] + prevT[1] * self.gridSize
        tile = self.tiles[index]

        if tile and tile.sameNum(self.tiles[prevI]):
            self.animationTiles.append((self.tiles[prevI], self.INCREASE))
            self.animationTiles.append((self.tiles[index], self.MOVE))

            self.tiles[prevI].merge()
            self.changePos(index, prevI)
            self.tiles[index] = 0

            return canMove + 1, True

    def moveTile(self, pos, index, direction, canMove):
        if not self.tiles[index]:
            return canMove + 1, False

        dest = (pos[0] + canMove * direction[0], pos[1] + canMove * direction[1])
        nextIndex = dest[0] + dest[1] * self.gridSize

        self.tiles[nextIndex] = self.changePos(index, nextIndex)
        self.tiles[index] = 0

        self.animationTiles.append((self.tiles[nextIndex], self.MOVE))

        return canMove, False

    def addRandomTile(self):
        num = 2 if random.random() < 0.9 else 4
        tile = self.getRandomEmpty()
        self.tiles[tile] = self.makeTile(num, tile)

        self.animationTiles.append((self.tiles[tile], self.SPAWN))

        return self.tiles[tile]

    def gridHasChanged(self, startTiles):
        for i in range(len(self.tiles)):
            if self.tiles[i] != startTiles[i]:
                return True

        return False

    def gameOver(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                index = i + j * self.gridSize
                tile = self.tiles[index]

                if not tile:
                    return False

                # check on the x axis
                if i < self.gridSize - 1:
                    nextIndex = (i + 1) + j * self.gridSize
                    if self.canMoveorMerge(index, nextIndex):
                        return False

                # check on the y axis
                if j < self.gridSize - 1:
                    nextIndex = i + (j + 1) * self.gridSize
                    if self.canMoveorMerge(index, nextIndex):
                        return False

        return True

    def canMoveorMerge(self, index, nextIndex):
        tile = self.tiles[index]
        nextTile = self.tiles[nextIndex]

        if not nextTile or tile.sameNum(nextTile):
            return True

    def getRandomEmpty(self):
        index = random.randint(0, self.gridSize ** 2 - 1)
        if not self.tiles[index]:
            return index

        return self.getRandomEmpty()

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.size, self.size))

        for i in range(len(self.tiles)):
            tile = self.tiles[i]

            if tile:
                tile.draw(win)

    def animateChanges(self, win):
        startTime = time.time()

        while self.animationSpeed * (time.time() - startTime) < 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            dt = self.animationSpeed * (time.time() - startTime)
            self.animate(win, dt)

        for animation in self.animationTiles:
            tile = animation[0]
            tile.animationDone()

    def animate(self, win, dt):
        for animations in self.animationTiles:
            tile = animations[0]
            animation = animations[1]
            self.animations[animation](tile, dt)

        self.drawAnimations(win)
        pygame.display.update()

    def drawAnimations(self, win):
        self.draw(win)

        for animation in self.animationTiles:
            tile = animation[0]

            if tile not in self.tiles:
                tile.draw(win)

        pygame.display.update()

