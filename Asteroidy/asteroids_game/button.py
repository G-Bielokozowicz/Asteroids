from pygame import Surface
import pygame
from utils import load_sprite


class Button:
    def __init__(self, position_x: int, position_y: int, sprite: str):
        self.position_x = position_x
        self.position_y = position_y
        self.surf = pygame.Surface((200, 50), pygame.SRCALPHA, 32).convert_alpha()
        self.bg = load_sprite(sprite)
        self.surf.blit(self.bg, (0, 0))
        self.rect = pygame.Rect(self.position_x, self.position_y, 200, 50)

    def draw(self, surface: Surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        surface.blit(self.surf, (self.position_x, self.position_y))

    def is_pressed(self):
        return self.rect.collidepoint((pygame.mouse.get_pos()))
