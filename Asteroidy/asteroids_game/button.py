from pygame import Surface
import pygame
from utils import load_sprite


class Button:
    def __init__(self, surface:Surface, position_x: int, position_y: int, image: str, image2: str = None,):
        self.position_x = position_x
        self.position_y = position_y
        self.surf = pygame.Surface((200, 50), pygame.SRCALPHA, 32).convert_alpha()
        self.image = load_sprite(image)
        self.surf.blit(self.image, (0, 0))
        self.rect = pygame.Rect(self.position_x, self.position_y, 200, 50)
        self.surface_to_draw=surface
        if image2 is not None:
            self.image2 = load_sprite(image2)
            self.image_number = 1

    def draw(self):
        pygame.draw.rect(self.surface_to_draw, (0, 0, 0), self.rect)
        self.surface_to_draw.blit(self.surf, (self.position_x, self.position_y))

    def is_pressed(self):
        return self.rect.collidepoint((pygame.mouse.get_pos()))

    def change_image(self):
        if self.image_number == 1:
            self.surf.blit(self.image2, (0, 0))
            self.image_number = 2
        else:
            self.surf.blit(self.image, (0, 0))
            self.image_number = 1
        self.draw()