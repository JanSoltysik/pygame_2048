"""
A file with definitions helpful in creating game's UI.
"""

import copy
from typing import Tuple
from collections import namedtuple

import pygame


ColorVector = Tuple[int, int, int]
ButtonColors = namedtuple("ButtonColors",
                          ["color", "over_color", "text_color"])
BLACK: ColorVector = (0, 0, 0)
WHITE: ColorVector = (255, 255, 255)


class Button:
    """
    Class which represents button in a game ui.

    Attributes
    ----------
    font: pygame.font.Font
        A font of text which will be drawn on the button.
    color: Tuple[int, int, int]
        A tuple of ints which represents current_color of the button.
    current_color: Tuple[int, int, int]
        A tuple of ints which represents color of button when mouse isn't over it..
    over_color: Tuple[int, int, int]
        A tuple of ints which represents color of button when mouse is over it.
    text_color: Tuple[int, int, int]
        A tuple of ints which represents color of the text displayed on the button.
    screen_cords: Tuple[int, int, int, int]
        A tuple of ints representing coordinates on screen
        (x, y, width, height).
    """
    def __init__(self, font: pygame.font.Font,
                 button_color: ButtonColors,
                 screen_cords: Tuple[int, int, int, int]) -> None:
        """
        Parameters
        ----------
        font: pygame.font.Font
            A font of a text which will be displayed on a button.
        button_color: ButtonColor
            A tuple of three element tuples which corresponds to
            standard button's color, color of button when mouse is
            over it and color af a text displayed on a button.
        screen_cords: Tuple[int, int, int, int]
            A tuple of ints representing coordinates on screen
            (x, y, width, height).
        """
        self.font: pygame.font.Font = font
        self.color: ColorVector = button_color.color
        self.current_color: ColorVector = copy.copy(self.color)
        self.over_color: ColorVector = button_color.over_color
        self.text_color: ColorVector = button_color.text_color
        self.screen_cords: Tuple[int, int, int, int] = screen_cords

    def draw(self, screen: pygame.surface.Surface, text_to_display: str, *,
             radius: float = 0.4) -> None:
        """
        Draw a button on a screen with a given attributes.

        Parameters
        ----------
        screen: pygame.surface.Surface
            A screen on which button will be displayed.
        text_to_display: str
            A text displayed on the button.
        radius: float, optional
            The radius of circle used to create round vertices.
        """
        self.draw_round_rectangle(screen, radius)

        text: pygame.surface.Surface = self.font.render(text_to_display,
                                                        True, self.text_color)
        screen.blit(text,
                    (self.screen_cords[0] + (self.screen_cords[2] / 2 - text.get_width() / 2),
                     self.screen_cords[1] + (self.screen_cords[3] / 2 - text.get_height() / 2)))

    def handle_event(self, event: pygame.event.Event, mouse_position: Tuple[int, int]) -> bool:
        """
        Handles pygame event.
        If mouse is over a button it changes color,
        and if mouse is over a button and it is clicked it returns a True.

        Parameters
        ----------
        event: pygame.event.Event
            Captured pygame's event.
        mouse_position: Tuple[int, int]
            Tuple of integers representing mouse position on the pygame's screen.

        Returns
        -------
        bool
            True if mouse is over a button and it is clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(mouse_position):
                self.color = self.current_color
                return True

        if event.type == pygame.MOUSEMOTION:
            if self.is_over(mouse_position):
                self.color = self.over_color
            else:
                self.color = self.current_color

        return False

    def is_over(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if given position is over button.

        Parameters
        ----------
        pos: Tuple[int, int]
            Tuple of integers representing mouse position on the pygame's screen.

        Returns
        -------
        bool
            True if a given position is over a button.
        """
        return all(self.screen_cords[i] < pos[i] < self.screen_cords[i] + self.screen_cords[i + 2]
                   for i in range(2))

    def draw_round_rectangle(self, screen: pygame.surface.Surface, radius: float) -> None:
        """
        Draws a rectangle with a round vertices.

        Parameters
        ----------
        screen: pygame.surface.Surface
            A screen on which button will be displayed.
        radius: float
            The radius of circle used to create round vertices.
        """
        rect: pygame.rect.Rect = pygame.rect.Rect(*self.screen_cords)
        color: pygame.color.Color = pygame.color.Color(*self.color)
        alpha: int = color.a
        pos: Tuple[int, int] = rect.topleft
        color.a = 0
        rect.topleft = 0, 0
        rectangle: pygame.Surface = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle: pygame.surface.Surface =\
            pygame.surface.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, BLACK, circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(
            circle, [int(min(rect.size) * radius)] * 2)

        round_radius: pygame.rect.Rect = rectangle.blit(circle, (0, 0))
        round_radius.bottomright = rect.bottomright
        rectangle.blit(circle, round_radius)
        round_radius.topright = rect.topright
        rectangle.blit(circle, round_radius)
        round_radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, round_radius)

        rectangle.fill(BLACK, rect.inflate(-round_radius.w, 0))
        rectangle.fill(BLACK, rect.inflate(0, -round_radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((*WHITE, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        screen.blit(rectangle, pos)
