import time
import pygame
import numpy as np  # type: ignore
from typing import Tuple, List, Callable

from utils.grid import Grid
from utils.ui import Button, ColorVector
from utils.monte_carlo import MonteCarloTreeSearch, get_moves_list


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
    text_color: Tuple[int, int, int]
        Tuple of ints representing color of text used in game.
    use_bot: bool
        Boolean which determines if player or bot is playing.
    text_font: pygame.font.Font:
        Font used in texts displayed on pygame's screeen.
    button_font: pygame.font.Font:
        Font used in button's text.
    title_font: pygame.font.Font:
        Font used in title.
    screen: pygame.surface.Surface:
        Instance of pygame's screen.
    menu: Button
        Button which redirects back to menu.
    play: Button
        Button which starts game in player mode.
    monte_carlo: Button
        Button which starts game in bot mode.
    reset: Button
        Button which brings player back to menu after a win/lose.
    current_score: Button
        A rectangle on which current score is displayed.
    best: Button
        A rectangle on which best score is displayed.
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
        self.text_color: ColorVector = self.config['color']['dark']
        self.use_bot: bool = False

        pygame.init()

        # pygame's attributes
        self.text_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                               self.config['text_font_size'], bold=True)
        self.button_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                                 self.config['button_font_size'], bold=True)
        self.title_font: pygame.font.Font = pygame.font.SysFont(self.config['font'],
                                                                self.config['title_font_size'], bold=True)
        self.screen: pygame.surface.Surface = pygame.display.set_mode((config['size'],
                                                                       config['size'] + self.config["header_height"]))

        # Button's
        self.menu: Button = Button(self.screen, self.title_font,
                                   self.config["color"]["2048"], self.config["color"]["2048"],
                                   self.config["color"]["white"],
                                   10, 15, 150, 120, "2048")

        self.play: Button = Button(self.screen, self.button_font,
                                   self.config["color"]["play"], self.config["color"]["64"],
                                   self.config["color"]["black"],
                                   105, 400, 300, 45, "Play")
        self.monte_carlo: Button = Button(self.screen, self.button_font,
                                          self.config["color"]["play"], self.config["color"]["64"],
                                          self.config["color"]["black"],
                                          105, 500, 300, 45, "Monte Carlo")
        self.reset: Button = Button(self.screen, self.button_font,
                                    self.config["color"]["play"], self.config["color"]["64"],
                                    self.config["color"]["black"],
                                    105, 250, 300, 45, "Menu")
        self.current_score: Button = Button(self.screen, self.button_font,
                                            self.config['color']['score'], self.config["color"]["64"],
                                            self.config["color"]["white"],
                                            190, 15, 150, 60, "SCORE: 0")

        self.best: Button = Button(self.screen, self.button_font,
                                   self.config['color']['score'], self.config["color"]["64"],
                                   self.config["color"]["white"],
                                   345, 15, 150, 60, "BEST: 0")

        # initialize pygame
        pygame.display.set_caption('2048')
        icon: pygame.surface.Surface = pygame.transform.scale(
            pygame.image.load("images/icon.ico"), (32, 32))
        pygame.display.set_icon(icon)

    def check_game_status(self) -> None:
        """
        Check if game is won/lost. If it is true message is displayed and return to menu via button is enabled.
        """
        if self.grid.is_win() or self.grid.is_lose():
            size: int = self.config['size']
            s = pygame.Surface((size, size + self.config["header_height"]), pygame.SRCALPHA)
            s.fill(self.config['color']['over'])
            self.screen.blit(s, (0, 0))

            info: str = 'YOU WIN!' if self.grid.is_win() else 'GAME OVER!'

            self.screen.blit(self.text_font.render(info, True, self.text_color), (140, 180))

            while True:
                self.reset.draw()
                pygame.display.update()

                for event in pygame.event.get():
                    pos: Tuple[int, int] = pygame.mouse.get_pos()
                    if self.reset.handle_event(event, pos):
                        self.show_menu()

    def start_game(self) -> None:
        """
        Initialize Grid object and starts game loop.
        """
        self.grid = Grid()
        self.display()

        self.screen.blit(self.text_font.render("NEW GAME!", True, self.text_color), (130, 225))
        pygame.display.update()

        time.sleep(1)
        self.grid.generate_twos(number_of_twos=2)
        self.display()

    def set_scores(self) -> None:
        """
        Set scores in current/best scores banners.
        """
        self.current_score.text = f"SCORE: {self.grid.score}"
        self.best.text = f"BEST: {self.best_score}"

    def display(self) -> None:
        """
        Generates objects during game loop.
        Created objects:
            - Score's banners.
            - Menu's button.
            - Game's grid.
        """
        self.screen.fill(self.config['color']['background'])
        box = self.config['size'] // 4
        padding = self.config['padding']

        self.set_scores()
        self.menu.draw()
        self.current_score.draw()
        self.best.draw()

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

                    self.screen.blit(self.text_font.render(f"{self.grid[i, j]:>4}", True, text_color),
                                     (j * box + 4 * padding, i * box + 7 * padding + self.config["header_height"]))

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
        all_moves[bot()]()
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

    def gameLoop(self) -> None:
        """
        Game loop in which either player or bot makes moves until games is finished.
        After game is over by clicking menu button user can go back to main menu.
        Loop can be broken either by pressing q, exiting created game's window or pressing return button.
        """
        self.start_game()
        bot: MonteCarloTreeSearch = MonteCarloTreeSearch(self.grid)
        all_moves_list: List[Callable[[], bool]] = get_moves_list(self.grid)

        while True:
            if self.use_bot:
                self.bot_move(bot, all_moves_list)

            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if Game.check_for_quit(event):
                    break

                if not self.use_bot and event.type == pygame.KEYDOWN:
                    self.player_move(event)

                if self.menu.handle_event(event, pos):
                    self.show_menu()

    def show_menu(self) -> None:
        """
        Generates main menu.
        Player or bot path can be chosen.
        """
        while True:
            self.screen.fill(self.config["color"]["background"])

            self.screen.blit(pygame.transform.scale(
                pygame.image.load("images/icon.ico"), (200, 200)), (155, 50))

            self.play.draw()
            self.monte_carlo.draw()
            pygame.display.update()

            for event in pygame.event.get():
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                if Game.check_for_quit(event):
                    break

                if self.play.handle_event(event, pos):
                    self.use_bot = False
                    self.gameLoop()
                if self.monte_carlo.handle_event(event, pos):
                    self.use_bot = True
                    self.gameLoop()

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
