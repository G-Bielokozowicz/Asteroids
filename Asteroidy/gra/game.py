import pygame
import time
from pygame import Color
from utils import load_sprite, get_random_position, print_text

from models import Spaceship, Asteroid


class Asteroidy:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.message = ""
        self.message_color = Color("tomato")
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.count = 0
        self.menu_mode = True
        self.game_over = False

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroidy")

    # menu glowne
    def menu(self):
        while self.menu_mode:
            self.screen.fill((0, 0, 0))
            start_game_text = 'Press Enter to start the game!'
            print_text(self.screen, start_game_text, 50, 50, 64, True, (255, 255, 255))
            pygame.display.flip()
            for event in pygame.event.get():
                # wyjscie z gry
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.menu_mode = False
                    self.main_loop()

    # gra
    def main_loop(self):
        while True:
            # handle input poza game over zeby mozna bylo wyjsc
            self._handle_input()
            if not self.game_over:
                self._process_game_logic()
                self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            # wyjscie z gry
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            # strzelanie
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        # self.count += 1
        # if self.count > 1000:
        #     self.count = 1
        # if self.count % 50 == 0:
        #     if self.spaceship:
        #         while True:
        #             position = get_random_position(self.screen)
        #             if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
        #                 break
        #         self.asteroids.append(Asteroid(position))

        # niszczenie statku kiedy uderzy w asteroide
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    self.game_over = True
                    break
        # kolizja pocisku z asteroida
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        # usuwanie pociskow ktore sa poza mapa
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        # wygrana
        if not self.asteroids and self.spaceship:
            self.message_color = "green"
            self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, 50, 50, 64, True, self.message_color)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
