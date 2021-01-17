import sys
import time
import copy
import pygame
import pygame.locals
from typing import Tuple

from grid import Grid


class Game:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, config: dict) -> None:
        self.screen = screen
        self.config = config
        self.font = pygame.font.SysFont(self.config['font'], self.config['font_size'], bold=True)

        self.grid = None
        self.gameLoop('light', 2048)

    def is_win(self, theme: str, text_color: Tuple[int, int, int]) -> str:
        status = self.grid.get_status()

        if status != 'PLAY':
            size = self.config['size']
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            s.fill(self.config['colour'][theme]['over'])
            self.screen.blit(s, (0, 0))

            if status == 'WIN':
                msg = 'YOU WIN!'
            else:
                msg = 'GAME OVER!'

            self.screen.blit(self.font.render(msg, 1, text_color), (140, 180))
            self.screen.blit(self.font.render("Play again y/n", 1, text_color), (80, 255))

            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT or \
                            event.type == pygame.KEYDOWN and event.key == pygame.locals.K_n:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_y:
                        self.start_game()
                        return "PLAY"

        return status

    def start_game(self, theme: str, text_color: Tuple[int, int, int]) -> None:
        self.grid = Grid()
        self.display(theme)

        self.screen.blit(self.font.render("NEW GAME!", 1, text_color), (130, 225))
        pygame.display.update()

        time.sleep(1)

        self.grid.generate_twos(iters=2)
        self.display(theme)

    def restart(self, theme: str, text_color: Tuple[int, int, int]) -> None:
        s = pygame.Surface((self.config['size'], self.config['size']), pygame.SRCALPHA)
        s.fill(self.config['colour'][theme]['over'])
        self.screen.blit(s, (0, 0))

        self.screen.blit(self.font.render('RESTART? y/n', 1, text_color), (85, 225))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.locals.K_n:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_y:
                    self.start_game()

    def display(self, theme: str) -> None:
        self.screen.fill(self.config['colour'][theme]['background'])
        box = self.config['size'] // 4
        padding = self.config['padding']

        for i in range(4):
            for j in range(4):
                colour = self.config['colour'][theme][str(self.grid[i, j])]
                pygame.draw.rect(self.screen, colour,
                                (j * box + padding,
                                 i * box + padding,
                                 box - 2 * padding,
                                 box - 2 * padding), 0)
                if self.grid[i, j] != 0:
                    if self.grid[i, j] in (2, 4):
                        text_colour = self.config['colour'][theme]['dark']
                    else:
                        text_colour = self.config['colour'][theme]['light']

                    self.screen.blit(self.font.render(f"{self.grid[i, j]:>4}", 1, text_colour),
                                     (j * box + 4 * padding, i * box + 7 * padding))

            pygame.display.update()

    def gameLoop(self, theme: str, difficulty: int) -> None:
        status = 'PLAY'

        if theme == "light":
            text_col = self.config['colour'][theme]['dark']
        else:
            text_col = self.config['colour'][theme]['light']

        self.start_game(theme, text_col)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or\
                   event.type == pygame.KEYDOWN and event.key == pygame.locals.K_q:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.restart(theme, text_col)

                    if str(event.key) not in self.config['keys']:
                        continue

                    else:
                        key = self.config['keys'][str(event.key)]

                    current_grid = copy.deepcopy(self.grid.grid)
                    self.grid.move(key)

                    if not (self.grid.grid == current_grid).all():
                        self.grid.generate_twos()
                        self.display(theme)
                        self.is_win(theme, text_col)














