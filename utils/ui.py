"""
A file with definitions helpful in creating game's UI.
"""

import copy
from typing import Tuple

import pygame


ColorVector = Tuple[int, int, int]


class Button:
    """
    Class which represents button in a game ui.

    Attributes
    ----------
    screen: pygame.surface.Surface
        A pygame screen on which button will be displayed.
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
    x_cord: int
        The x coordinates of button o the pygame's screen.
    y_cord: int
        The y coordinates of button o the pygame's screen.
    width: int
        The width of the button.
    height: int
        The height of the button.
    text: str
        The text displayed on the button.
    radius: float
        The radius of circle used to create round vertices.
    black: Tuple[int, int, int]
        A tuple of ints which represents black color.
    white: Tuple[int, int, int]
        A tuple of ints which represents white color.
    """
    def __init__(self, screen: pygame.surface.Surface, font: pygame.font.Font,
                 color: ColorVector, over_color: ColorVector, text_color: ColorVector,
                 x_cord: int, y_cord: int, width: int, height: int, text: str, *,
                 radius: float = 0.4) -> None:
        """
        Parameters
        ----------
        screen: pygame.surface.Surface
            A screen on which button will be displayed.
        font: pygame.font.Font
            A font of a text which will be displayed on a button.
        color: Tuple[int, int, int]
            Color of a button.
        over_color: Tuple[int, int, int]
            A tuple of ints which represents color of button when mouse is over it.
        text_color: Tuple[int, int, int]
            Color of a button's text.
        x_cord: int
            The x coordinates of button o the pygame's screen.
        y_cord: int
            The y coordinates of button o the pygame's screen.
        width: int
            The width of the button.
        height: int
            The height of the button.
        text: str
            A text displayed on the button.
        radius: float, optional
            Radius used to create round vertices.
        """
        self.screen: pygame.surface.Surface = screen
        self.font: pygame.font.Font = font
        self.color: ColorVector = color
        self.current_color: ColorVector = copy.deepcopy(color)
        self.over_color: ColorVector = over_color
        self.text_color: ColorVector = text_color
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.width: int = width
        self.height: int = height
        self.text: str = text
        self.radius: float = radius
        self.black: ColorVector = (0, 0, 0)
        self.white: ColorVector = (255, 255, 255)

    def draw(self) -> None:
        """
        Draw a button on a screen with a given attributes.
        """
        self.draw_round_rectangle()

        text: pygame.surface.Surface = self.font.render(self.text,
                                                        True, self.text_color)
        self.screen.blit(text,
                         (self.x_cord + (self.width / 2 - text.get_width() / 2),
                          self.y_cord + (self.height / 2 - text.get_height() / 2)))

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
        return self.x_cord < pos[0] < self.x_cord + self.width and\
               self.y_cord < pos[1] < self.y_cord + self.height

    def draw_round_rectangle(self) -> None:
        """
        Draws a rectangle with a round vertices.
        """
        rect: pygame.rect.Rect = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        color: pygame.color.Color = pygame.color.Color(*self.color)
        alpha: int = color.a
        pos: Tuple[int, int] = rect.topleft
        color.a = 0
        rect.topleft = 0, 0
        rectangle: pygame.Surface = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle: pygame.surface.Surface =\
            pygame.surface.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, self.black, circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(
            circle, [int(min(rect.size) * self.radius)] * 2)

        radius: pygame.rect.Rect = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill(self.black, rect.inflate(-radius.w, 0))
        rectangle.fill(self.black, rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((*self.white, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        self.screen.blit(rectangle, pos)
