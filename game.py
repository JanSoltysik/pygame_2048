import time
import copy
import pygame
import pygame.locals
from typing import Tuple

from grid import Grid
from utils.ui import Button, ColorVector


class Game:
    def __init__(self, config: dict) -> None:
        self.config: dict = config
        self.best: int = self.config["best_score"]
        self.grid_size: int = self.config['grid_size']
        self.grid: Grid = Grid
        self.text_color: ColorVector = self.config['color']['dark']

        pygame.init()

        self.text_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                               self.config['text_font_size'], bold=True)
        self.button_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                                 self.config['button_font_size'], bold=True)
        self.title_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                                self.config['title_font_size'], bold=True)
        self.screen: pygame.Surface = pygame.display.set_mode((config['size'],
                                                               config['size'] + self.config["header_height"]))

        self.menu: Button = Button(self.screen, self.title_font,
                                   self.config["color"]["2048"], self.config["color"]["white"],
                                   10, 15, 150, 120, "2048")

        self.play: Button = Button(self.screen, self.button_font,
                                   self.config["color"]["play"], self.config["color"]["black"],
                                   105, 400, 300, 45, "Play")
        self.reset: Button = Button(self.screen, self.button_font,
                                    self.config["color"]["play"], self.config["color"]["black"],
                                    105, 250, 300, 45, "Reset")
        self.current_score: Button = Button(self.screen, self.button_font,
                                            self.config['color']['score'], self.config["color"]["white"],
                                            190, 15, 150, 60, "SCORE: 0")
        self.best_score: Button = Button(self.screen, self.button_font,
                                            self.config['color']['score'], self.config["color"]["white"],
                                            345, 15, 150, 60, "BEST: 0")

        pygame.display.set_caption('2048')
        icon: pygame.Surface = pygame.transform.scale(
            pygame.image.load("images/icon.ico"), (32, 32))
        pygame.display.set_icon(icon)

    def check_game_status(self) -> None:
        if self.grid.is_win() or self.grid.is_lose():
            size:int = self.config['size']
            s = pygame.Surface((size, size + self.config["header_height"]), pygame.SRCALPHA)
            s.fill(self.config['color']['over'])
            self.screen.blit(s, (0, 0))

            if self.grid.is_win():
                msg:str = 'YOU WIN!'
            else:
                msg: str = 'GAME OVER!'

            self.screen.blit(self.text_font.render(msg, 1, self.text_color), (140, 180))

            while True:
                self.reset.draw()
                pygame.display.update()

                for event in pygame.event.get():
                    pos: Tuple[int, int] = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.reset.is_over(pos):
                            self.gameLoop()
                    if event.type == pygame.MOUSEMOTION:
                        if self.reset.is_over(pos):
                            self.reset.color = self.config["color"]["64"]
                        else:
                            self.reset.color = self.config["color"]["play"]

    def start_game(self) -> None:
        self.grid = Grid()
        self.display()

        self.screen.blit(self.text_font.render("NEW GAME!", 1, self.text_color), (130, 225))
        pygame.display.update()

        time.sleep(1)

        self.grid.generate_twos(2)
        self.display()

    def restart(self) -> None:
        s = pygame.Surface((self.config['size'], self.config['size'] + self.config["header_height"]), pygame.SRCALPHA)
        s.fill(self.config['color']['over'])
        self.screen.blit(s, (0, 0))

        self.screen.blit(self.text_font.render('RESTART? y/n', 1, self.text_color), (85, 225))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.locals.K_n:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.locals.K_y:
                    self.start_game()

    def set_scores(self) -> None:
        self.current_score.text = f"SCORE: {self.grid.score}"
        self.best_score.text = f"BEST: {self.best}"

    def display(self) -> None:
        self.screen.fill(self.config['color']['background'])
        box = self.config['size'] // 4
        padding = self.config['padding']

        self.set_scores()
        self.menu.draw()
        self.current_score.draw()
        self.best_score.draw()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = self.config['color'][str(self.grid[i, j])]
                pygame.draw.rect(self.screen, color,
                                (j * box + padding,
                                 i * box + padding + self.config["header_height"],
                                 box - 2 * padding,
                                 box - 2 * padding), 0)
                if self.grid[i, j] != 0:
                    if self.grid[i, j] in (2, 4):
                        text_color = self.config['color']['dark']
                    else:
                        text_color = self.config['color']['light']

                    self.screen.blit(self.text_font.render(f"{self.grid[i, j]:>4}", 1, text_color),
                                     (j * box + 4 * padding, i * box + 7 * padding + self.config["header_height"]))

            pygame.display.update()

    def gameLoop(self) -> None:
        self.start_game()
        while True:
            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if event.type == pygame.locals.QUIT or\
                   event.type == pygame.KEYDOWN and event.key == pygame.locals.K_q:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if str(event.key) not in self.config['keys']:
                        continue

                    else:
                        key = self.config['keys'][str(event.key)]

                    current_grid = copy.deepcopy(self.grid.grid)
                    self.grid.move(key)
                    self.best: int = max(self.best, self.grid.score)

                    if not (self.grid.grid == current_grid).all():
                        self.grid.generate_twos()
                        self.display()
                        self.check_game_status()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.is_over(pos):
                        self.show_menu()

    def show_menu(self) -> None:
        while True:
            self.screen.fill(self.config["color"]["background"])

            self.screen.blit(pygame.transform.scale(
                pygame.image.load("images/icon.ico"), (200, 200)), (155, 50))

            self.play.draw()
            pygame.display.update()

            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play.is_over(pos):
                        self.gameLoop()

                if event.type == pygame.MOUSEMOTION:
                    if self.play.is_over(pos):
                        self.play.color = self.config["color"]["64"]
                    else:
                        self.play.color = self.config["color"]["play"]

