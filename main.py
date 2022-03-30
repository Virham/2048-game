import pygame
from Board import Board

class Main:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))

        self.board = Board(100, 110, 500, 4)

    def draw(self):
        self.win.fill((64, 64, 255))
        self.board.draw(self.win)
        pygame.display.update()

    def keyPresses(self):
        keys = pygame.key.get_pressed()
        direction = None

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = (0, -1)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = (-1, 0)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = (0, 1)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = (1, 0)

        if direction:
            self.board.move(direction)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    self.keyPresses()

            self.draw()


Main().loop()
