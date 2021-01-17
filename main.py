import sys
import json
import pygame
import pygame.locals
from typing import Tuple

from game import Game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



class Button:
    def __init__(self, colour, x, y, width, height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # draw the button on the screen
    def draw(self, win, text_col, font):
        drawRoundRect(win, self.colour, (self.x, self.y,
                                         self.width, self.height))

        if self.text != "":
            text = font.render(self.text, 1, text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    # check if the mouse is positioned over the button
    def is_over(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def drawRoundRect(screen: pygame.Surface, color: Tuple[int, int, int], rect: Tuple[int, int, int, int],
                  radius: float = 0.4) -> None:
    rect = pygame.Rect(rect)
    colour = pygame.color.Color(*color)
    alpha = colour.a
    colour.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill(BLACK, rect.inflate(-radius.w, 0))
    rectangle.fill(BLACK, rect.inflate(0, -radius.h))

    rectangle.fill(colour, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    screen.blit(rectangle, pos)


def showMenu(c: dict, screen):
    # create light theme button
    light_theme = Button(
        tuple(c["colour"]["light"]["2048"]), 200 - 70, 275, 45, 45, "light")
    # create dark theme button
    dark_theme = Button(
        tuple(c["colour"]["dark"]["2048"]), 270 - 70, 275, 45, 45, "dark")

    # initialise theme
    theme = ""
    theme_selected = False

    # create difficulty buttons
    _2048 = Button(tuple(c["colour"]["light"]["64"]),
                   130, 330, 45, 45, "2048")

    # default difficulty
    difficulty = 0
    diff_selected = False

    # create play button
    play = Button(tuple(c["colour"]["light"]["2048"]),
                  235, 400, 45, 45, "play")

    # pygame loop for start screen
    while True:
        screen.fill(BLACK)

        screen.blit(pygame.transform.scale(
            pygame.image.load("images/icon.ico"), (200, 200)), (155, 50))

        font = pygame.font.SysFont(c["font"], 15, bold=True)

        theme_text = font.render("Theme: ", 1, WHITE)
        screen.blit(theme_text, (55, 285))

        diff_text = font.render("Difficulty: ", 1, WHITE)
        screen.blit(diff_text, (40, 345))

        # set fonts for buttons
        font1 = pygame.font.SysFont(c["font"], 15, bold=True)
        font2 = pygame.font.SysFont(c["font"], 14, bold=True)

        # draw all buttons on the screen
        light_theme.draw(screen, BLACK, font1)
        dark_theme.draw(screen, (197, 255, 215), font1)
        _2048.draw(screen, BLACK, font2)
        play.draw(screen, BLACK, font1)

        pygame.display.update()

        for event in pygame.event.get():
            # store mouse position (coordinates)
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                # exit if q is pressed
                pygame.quit()
                sys.exit()

            # check if a button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # select light theme
                if light_theme.is_over(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    light_theme.colour = tuple(c["colour"]["light"]["64"])
                    theme = "light"
                    theme_selected = True

                # select dark theme
                if dark_theme.is_over(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    theme = "dark"
                    theme_selected = True

                if _2048.is_over(pos):
                    _2048.colour = tuple(c["colour"]["light"]["64"])
                    difficulty = 2048
                    diff_selected = True


                # play game with selected theme
                if play.is_over(pos):
                    if theme != "" and difficulty != 0:
                        Game(screen, font, config)

                # reset theme & diff choice if area outside buttons is clicked
                if not play.is_over(pos) and \
                        not dark_theme.is_over(pos) and \
                        not light_theme.is_over(pos) and \
                        not _2048.is_over(pos):
                    theme = ""
                    theme_selected = False
                    diff_selected = False

                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])

            # change colour on hovering over buttons
            if event.type == pygame.MOUSEMOTION:
                if not theme_selected:
                    if light_theme.is_over(pos):
                        light_theme.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        light_theme.colour = tuple(c["colour"]["light"]["2048"])

                    if dark_theme.is_over(pos):
                        dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    else:
                        dark_theme.colour = tuple(c["colour"]["dark"]["2048"])

                if not diff_selected:
                    if _2048.is_over(pos):
                        _2048.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _2048.colour = tuple(c["colour"]["light"]["2048"])

                if play.is_over(pos):
                    play.colour = tuple(c["colour"]["light"]["64"])
                else:
                    play.colour = tuple(c["colour"]["light"]["2048"])


if __name__ == "__main__":
    with open('constants.json', encoding='utf-8') as f:
        config = json.load(f)

    pygame.init()
    screen = pygame.display.set_mode((config['size'], config['size']))
    pygame.display.set_caption('2048')

    icon = pygame.transform.scale(
        pygame.image.load("images/icon.ico"), (32, 32))
    pygame.display.set_icon(icon)

    font = pygame.font.SysFont(config['font'], config['font_size'], bold=True)

    showMenu(config, screen)
