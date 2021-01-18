from typing import Tuple

import pygame


ColorVector = Tuple[int, int, int]


class Button:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font,
                 color: ColorVector, text_color: ColorVector,
                 x: int, y: int, width: int, height: int, text: str, *,
                 radius: float = 0.4) -> None:
        self.screen = screen
        self.font = font
        self.color: ColorVector = color
        self.text_color: ColorVector = text_color
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.text: str = text
        self.radius: float = radius
        self.BLACK: ColorVector = (0, 0, 0)

    def draw(self) -> None:
        self.draw_round_rectangle()

        text: str = self.font.render(self.text, 1, self.text_color)
        self.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                           self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos: Tuple[int, int]) -> bool:
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def draw_round_rectangle(self) -> None:
        rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        color: pygame.color.Color = pygame.color.Color(*self.color)
        alpha: int = color.a
        color.a: int = 0
        pos: int = rect.topleft
        rect.topleft: Tuple[int, int] = 0, 0
        rectangle: pygame.Surface = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle: pygame.Surface = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, self.BLACK, circle.get_rect(), 0)
        circle: pygame.Surface = pygame.transform.smoothscale(
            circle, [int(min(rect.size) * self.radius)] * 2)

        radius: pygame.Rect = rectangle.blit(circle, (0, 0))
        radius.bottomright: Tuple[int, int] = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright: Tuple[int, int] = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft: Tuple[int, int] = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill(self.BLACK, rect.inflate(-radius.w, 0))
        rectangle.fill(self.BLACK, rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        self.screen.blit(rectangle, pos)
