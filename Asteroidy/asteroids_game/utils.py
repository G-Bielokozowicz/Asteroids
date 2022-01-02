import random

import pygame.font
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.math import Vector2
from pygame import Color, Surface


def load_sprite(name: str, with_alpha=True) -> Surface:
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name: str) -> Sound:
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position: Vector2, surface: Surface) -> Vector2:
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface: Surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )


def get_random_velocity(min_speed: int, max_speed: int):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface: Surface, text: str, locx: int, locy: int, size: int, center=False, color=Color("tomato")):
    font = pygame.font.SysFont('None', size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    if center:
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (locx, locy))
