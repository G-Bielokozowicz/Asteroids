import pygame
from pygame.mixer import music
from utils import load_sprite, get_random_position, print_text
from button import Button
from models import Spaceship, Asteroid, Shotgun, Shield

import random


class Asteroidy:
    MIN_ASTEROID_DISTANCE = 300

    def __init__(self):
        self._init_pygame()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1600, 900))
        self.background = load_sprite("space", False)
        self.startbg = load_sprite("start", False)
        self.asteroids = []
        self.bullets = []
        self.score = 0
        self.highscore = 0
        self.spaceship = Spaceship((800, 450), self.bullets.append)
        self.count = 1
        self.menu_mode = True
        self.options_mode = False
        self.game_over = False
        self.upgrades = [self._get_random_upgrade()]

        self.music_volume = 0.05
        music.load("assets/sounds/soundtrack.wav")
        music.set_volume(self.music_volume)
        music.play(-1, fade_ms=1000)
        self.is_music_turned_on = True
        self.is_sound_turned_on = True
        self._asteroid_spawn(amount=5)

        self.button_start = Button(self.screen, 700, 300, "button_start")
        self.button_options = Button(self.screen, 700, 380, "button_options")
        self.button_back = Button(self.screen, 700, 600, "button_back")
        self.button_music = Button(self.screen, 700, 300, "button_music_on", "button_music_off")
        self.button_sound = Button(self.screen, 700, 380, "button_sound_on", "button_sound_off")
        self.button_exit = Button(self.screen, 700, 600, "button_exit")

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroidy")

    def _asteroid_spawn(self, amount: int):
        for _ in range(amount):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            ast = Asteroid(position, self.asteroids.append)
            ast.is_sound_turned_on = self.is_sound_turned_on
            self.asteroids.append(ast)

    def _get_random_upgrade(self):
        upgrade_list = {
            1: Shield(get_random_position(self.screen), self.spaceship),
            2: Shotgun(get_random_position(self.screen), self.spaceship)
        }
        return upgrade_list[random.randint(1, 2)]

    # main menu
    def menu(self):
        while self.menu_mode:
            # self.screen.blit(self.startbg, (0, 0))
            self.screen.blit(self.background, (0, 0))
            self.button_options.draw()
            self.button_start.draw()
            self.button_exit.draw()
            pygame.display.flip()
            self._handle_input()

    # options menu
    def _options(self):
        while self.options_mode:
            # self.screen.blit(self.startbg, (0, 0))
            self.screen.blit(self.background, (0, 0))
            self.button_back.draw()
            self.button_music.draw()
            self.button_sound.draw()
            pygame.display.flip()
            self._handle_input()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        self.count += 1
        if self.count > 10000:
            self.count = 1
        if self.count % 500 == 0:
            self._asteroid_spawn(1 + self.score // 500)

        if len(self.asteroids) == 0:
            self._asteroid_spawn(2)
        if len(self.upgrades) == 0:
            if self.count % 3000 == 0:
                self.upgrades.append(self._get_random_upgrade())

        # destroying spaceship when it hits asteroids
        # game over
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    # self.spaceship = None
                    if self.spaceship.destroy(game=self):
                        self._game_loss()
                    self.asteroids.remove(asteroid)
                    break

        # destroying asteroid when it hits bullet
        for bullet in self.bullets[:]:

            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    if asteroid.size == 3:
                        self.score += 10
                    elif asteroid.size == 2:
                        self.score += 20
                    else:
                        self.score += 30
                    asteroid.split()
                    break

        # getting the upgrade
        for bullet in self.bullets[:]:
            for upgrade in self.upgrades[:]:
                if upgrade.collides_with(bullet):
                    upgrade.destroy()
                    self.upgrades.remove(upgrade)
                    self.bullets.remove(bullet)
                    break

        # removing bullets that are outside of the map
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    def _game_loss(self):
        self.game_over = True
        self._record_high_score()
        music.pause()
        self._game_over_loop()

    def _turn_off_sound(self):
        self.is_sound_turned_on = not self.is_sound_turned_on
        for obj in self._get_game_objects():
            obj.is_sound_turned_on = not obj.is_sound_turned_on

    def _game_over_loop(self):
        while True:
            self._draw()
            for event in pygame.event.get():
                # exiting the game
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self._restart()
                    self.main_loop()

    # game restart
    def _restart(self):
        # if self.game_over:
        self.spaceship = Spaceship((800, 450), self.bullets.append)
        self.game_over = False
        self.asteroids.clear()
        self.bullets.clear()
        self.upgrades.clear()
        self.score = 0
        self._asteroid_spawn(amount=5)
        self.upgrades = [self._get_random_upgrade()]
        music.unpause()

    def _handle_input(self):
        for event in pygame.event.get():
            # quitting with escape
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

            # main menu
            if self.menu_mode:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # going to options menu
                    if self.button_options.is_pressed():
                        self.menu_mode = False
                        self.options_mode = True
                        self._options()
                    if self.button_start.is_pressed():
                        self.menu_mode = False
                        self.main_loop()
                    if self.button_exit.is_pressed():
                        quit()
                # starting the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.menu_mode = False
                    self.main_loop()

            # options
            elif self.options_mode:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    # turning music on and off
                    if self.button_music.is_pressed():
                        if self.is_music_turned_on:
                            music.set_volume(0)
                            self.is_music_turned_on = False
                        else:
                            music.set_volume(self.music_volume)
                            self.is_music_turned_on = True
                        self.button_music.change_image()

                    if self.button_sound.is_pressed():
                        self._turn_off_sound()
                        self.button_sound.change_image()
                    # going back to main menu
                    if self.button_back.is_pressed():
                        self.menu_mode = True
                        self.options_mode = False
                        self.menu()
            # game
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()
        # moving the spaceship
        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship and not self.menu_mode:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            else:
                if self.spaceship.isShielded:
                    self.spaceship.sprite = self.spaceship.shielded_sprites[self.spaceship.lives - 1]
                else:
                    self.spaceship.sprite = self.spaceship.unshielded_sprites[self.spaceship.lives - 1]

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        print_text(self.screen, "Score = " + str(self.score), 10, 10, 48, False, (255, 255, 255))
        if self.spaceship:
            temp = "Shotgun = " + str(self.spaceship.shotgunRemaining)
        else:
            temp = "Shotgun = 0 "
        print_text(self.screen, temp, 10, 50, 48, False, (255, 255, 255))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.game_over:
            temp2 = "You lost! Press Enter to restart"
            print_text(self.screen, temp2, 340, 350, 60, False)
            temp3 = "Your current score: " + str(self.score)
            print_text(self.screen, temp3, 500, 410, 60)
            temp4 = "Your highscore: " + str(self.highscore)
            print_text(self.screen, temp4, 560, 470, 60)
        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets, *self.upgrades]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

        # game

    def _record_high_score(self):
        f = open("assets/highscore.txt", "r")
        self.highscore = int(f.read())
        f.close()
        if self.score >= self.highscore:
            f = open("assets/highscore.txt", "w")
            f.write(str(self.score))
            f.close()

    def main_loop(self):
        while True:
            # handle input outside of if, so that it's possible to quit and restart the game
            self._handle_input()
            # if not self.game_over:
            self._process_game_logic()
            self._draw()
