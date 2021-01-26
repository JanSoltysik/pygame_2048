"""
A file implementing main menu of the game as well as game loop.
"""
import time
from typing import Tuple, List, Callable, Dict

import pygame
import numpy as np  # type: ignore

from utils.grid import Grid
from utils.ui import Button, ButtonColors
from mcts_bot.monte_carlo import MonteCarloTreeSearch, get_moves_list


class Game:
    """
    A class implementing main menu and graphics for 2048.
    Attributes
    ---------
    config: dict
        A JSON which contains configuration of the game (colors, sizes, coordinates etc.).
    best_score: int
        Best saved score obtained in 2048.
    grid_size: int
        Size of the game's grid.
    grid: Grid
        Class which implements logic of 2048.
    screen: pygame.surface.Surface:
        Instance of pygame's screen.
    fonts: Dict[str, pygame.font.Font]
        Fonts used by texts displayed during game_loop or
        while in main menu.
    buttons: Dict[str, Button]
        Dict of all required buttons for both game and
        main menu.
    """

    def __init__(self, config: dict) -> None:
        """
        Parameters
        ----------
        config: dict
            A JSON which contains configuration of the game (colors, sizes, coordinates etc.).
        """
        self.config: dict = config
        self.best_score: int = self.config["best_score"]
        self.grid_size: int = self.config['grid_size']
        self.grid: Grid = Grid()

        pygame.init()

        # pygame's attributes
        self.screen: pygame.surface.Surface = \
            pygame.display.set_mode((config['size'],
                                     config['size'] + self.config["header_height"]))

        self.fonts: Dict[str, pygame.font.Font] = {
            "text_font": pygame.font.SysFont(self.config['font'],
                                             self.config['text_font_size'],
                                             bold=True),
            "button_font": pygame.font.SysFont(self.config['font'],
                                               self.config['button_font_size'],
                                               bold=True),
            "title_font": pygame.font.SysFont(self.config['font'],
                                              self.config['title_font_size'],
                                              bold=True)
        }
        self.buttons: Dict[str, Button] = {
            "menu": Button(self.fonts["title_font"],
                           ButtonColors(self.config["color"]["2048"],
                                        self.config["color"]["2048"],
                                        self.config["color"]["white"]),
                           (10, 15, 150, 120)),
            "play": Button(self.fonts["button_font"],
                           ButtonColors(self.config["color"]["play"],
                                        self.config["color"]["64"],
                                        self.config["color"]["black"]),
                           (105, 400, 300, 45)),
            "monte_carlo": Button(self.fonts["button_font"],
                                  ButtonColors(self.config["color"]["play"],
                                               self.config["color"]["64"],
                                               self.config["color"]["black"]),
                                  (105, 500, 300, 45)),
            "reset": Button(self.fonts["button_font"],
                            ButtonColors(self.config["color"]["play"],
                                         self.config["color"]["64"],
                                         self.config["color"]["black"]),
                            (105, 250, 300, 45)),
            "current_score": Button(self.fonts["button_font"],
                                    ButtonColors(self.config['color']['score'],
                                    self.config["color"]["64"],
                                    self.config["color"]["white"]),
                                    (190, 15, 150, 60)),
            "best": Button(self.fonts["button_font"],
                           ButtonColors(self.config['color']['score'],
                                        self.config["color"]["64"],
                                        self.config["color"]["white"]),
                           (345, 15, 150, 60))
        }

        # initialize pygame
        pygame.display.set_caption('2048')
        icon: pygame.surface.Surface = pygame.transform.scale(
            pygame.image.load("images/game_icon.ico"), (32, 32))
        pygame.display.set_icon(icon)

    def check_game_status(self) -> None:
        """
        Check if game is won/lost. If it is true message is
        displayed and return to menu via button is enabled.
        """
        if self.grid.is_win() or self.grid.is_lose():
            size: int = self.config['size']
            screen = pygame.Surface((size, size + self.config["header_height"]), pygame.SRCALPHA)
            screen.fill(self.config['color']['over'])
            self.screen.blit(screen, (0, 0))

            if self.grid.is_win():
                info: str = 'YOU WIN!'
                coords: Tuple[int, int] = (160, 180)
            else:
                info = 'GAME OVER!'
                coords = (140, 180)

            self.screen.blit(self.fonts["text_font"].render(info, True,
                                                            self.config["color"]["dark"]),
                             coords)
            while True:
                self.buttons["reset"].draw(self.screen, "Menu")
                pygame.display.update()

                for event in pygame.event.get():
                    pos: Tuple[int, int] = pygame.mouse.get_pos()
                    if self.buttons["reset"].handle_event(event, pos):
                        self.show_menu()

    def start_game(self) -> None:
        """
        Initialize Grid object and starts game loop.
        """
        self.grid = Grid()
        self.display()
        self.screen.blit(self.fonts["text_font"].render("NEW GAME!", True,
                                                        self.config['color']['dark']),
                         (140, 375))
        pygame.display.update()

        time.sleep(1)
        self.grid.generate_twos(number_of_twos=2)
        self.display()

    def display(self) -> None:
        """
        Generates objects during game loop.
        Created objects:
            - Score's banners.
            - Menu's button.
            - Game's grid.
        """
        self.screen.fill(self.config['color']['background'])
        box: int = self.config['size'] // 4
        padding = self.config['padding']

        self.buttons["menu"].draw(self.screen, "2048")
        self.buttons["current_score"].draw(self.screen,
                                           f"SCORE: {self.grid.score}")
        self.buttons["best"].draw(self.screen,
                                  f"BEST: {self.best_score}")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color: Tuple[int, int, int] =\
                    self.config['color'][str(self.grid[i, j])]
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

                    self.screen.blit(self.fonts["text_font"].render(
                        f"{self.grid[i, j]:>4}", True, text_color),
                        (j * box + 4 * padding,
                         i * box + 7 * padding + self.config["header_height"]))

            pygame.display.update()

    def update_grid(self, current_grid: np.ndarray) -> None:
        """
        If after move grid changed 2/4 is added to a grid, then screen is updated.
        At the end checks for ether win or lose.
        """
        if not np.array_equal(self.grid, current_grid):
            self.grid.generate_twos(number_of_twos=1)
            self.display()
            self.check_game_status()

    def bot_move(self, bot: MonteCarloTreeSearch, all_moves: List[Callable[[], bool]]) -> None:
        """
        Performs a move returned by bot, then checks if grid was updated.

        Parameters
        ----------
        bot: MonteCarloTreeSearch
            Bot object which performs Monte Carlo Search to find best next move.
        all_moves: List[Callable[[], bool]]
            List containing all possible grid's move.
        """
        current_grid: np.ndarray = np.copy(self.grid.grid)
        all_moves[bot(asynchronous=True)]()
        self.update_grid(current_grid)

    def player_move(self, event: pygame.event.Event) -> None:
        """
        Performs move given by a player, then checks if grid was updated.

        Parameters
        ----------
        event: pygame.event.Event
            Event in which method checks if player performed grid's move.
        """
        if str(event.key) in self.config['keys']:
            key = self.config['keys'][str(event.key)]

            current_grid = np.copy(self.grid.grid)
            self.grid.move(key)
            self.best_score = max(self.best_score, self.grid.score)
            self.update_grid(current_grid)

    def game_loop(self, use_bot: bool) -> None:
        """
        Game loop in which either player or bot make
        moves until games is finished. After game is over by clicking
        menu button user can go back to main menu. Loop can be broken
        either by pressing q, exiting created game's window or pressing
        return button.

        Parameters
        ----------
        use_bot: bool
            Boolean which determines if player or bot is playing.
        """
        self.start_game()
        bot: MonteCarloTreeSearch = MonteCarloTreeSearch(self.grid)
        all_moves_list: List[Callable[[], bool]] = get_moves_list(self.grid)

        while True:
            if use_bot:
                self.bot_move(bot, all_moves_list)

            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if Game.check_for_quit(event):
                    break

                if not use_bot and event.type == pygame.KEYDOWN:
                    self.player_move(event)

                if self.buttons["menu"].handle_event(event, pos):
                    self.show_menu()

    def show_menu(self) -> None:
        """
        Generates main menu.
        Player or bot path can be chosen.
        """
        while True:
            self.screen.fill(self.config["color"]["background"])

            self.screen.blit(pygame.transform.scale(
                pygame.image.load("images/game_icon.ico"), (300, 300)), (100, 50))

            self.buttons["play"].draw(self.screen, "Play")
            self.buttons["monte_carlo"].draw(self.screen, "Monte Carlo")
            pygame.display.update()

            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if Game.check_for_quit(event):
                    break

                if self.buttons["play"].handle_event(event, pos):
                    self.game_loop(use_bot=False)
                if self.buttons["monte_carlo"].handle_event(event, pos):
                    self.game_loop(use_bot=True)

    @staticmethod
    def check_for_quit(event: pygame.event.Event) -> bool:
        """
        Checks if game's window was closed or 'q' was pressed if yes game is shut down.

        Parameters
        ----------
        event: pygame.event.Event
            Pygame's event in which method checks if game should shut down.

        Returns
        -------
        bool
            True if player chose to quit.
        """
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            return True

        return False
