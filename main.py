import pygame
import time
from Board import Board

class Main:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))

        self.board = Board(100, 110, 500, 4)

        self.gameOver = False
        self.gameOverFont = pygame.font.SysFont("Impact", 200)
        self.gameText = self.gameOverFont.render("Game", False, (255, 64, 64))
        self.overText = self.gameOverFont.render("Over!", False, (255, 64, 64))
        self.pressSpaceText = pygame.font.SysFont("Impact", 60).render("Press SPACE to restart!", False, (255, 255, 255))

    def draw(self):
        self.win.fill((131, 131, 131))
        self.board.draw(self.win)

        if self.gameOver:
            self.gameOverScreen()

        pygame.display.update()

    def gameOverScreen(self):
        surf = pygame.Surface((self.width, self.height))
        surf.set_alpha(127)
        surf.fill((0, 0, 0))
        self.win.blit(surf, (0, 0))

        self.win.blit(self.gameText, (720, 80))
        self.win.blit(self.overText, (720, 280))
        self.win.blit(self.pressSpaceText, (670, 600))

    def keyPresses(self):
        keys = pygame.key.get_pressed()
        direction = None

        if self.gameOver:
            if keys[pygame.K_SPACE]:
                return pygame.K_SPACE
            return

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = (0, -1)

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = (-1, 0)

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = (0, 1)

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = (1, 0)

        if direction:
            if not self.board.move(direction, self.win):
                self.gameOver = True

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if self.keyPresses() == pygame.K_SPACE:
                        return

            self.draw()


while True:
    Main().loop()
