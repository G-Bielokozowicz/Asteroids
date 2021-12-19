from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sprite, load_sound, wrap_position

UP = Vector2(0, -1)  # wektor wskazujacy do gory


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(
            self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3  # turning speed
    ACCELERATION = 0.1  # acceleration speed
    MAX_SPEED = 8  # maximum speed
    BULLET_SPEED = 4  # bullet speed
    STARTING_LIVES = 3  # starting ammount of lives

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.spaceship_hit_asteroid = load_sound("asteroid_hit")
        self.spaceship_destroy_sound = load_sound("spaceship_destroy")
        self.direction = Vector2(UP)
        self.lives = self.STARTING_LIVES
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        if self.velocity.length() > self.MAX_SPEED:
            self.velocity.scale_to_length(self.MAX_SPEED)

    def shoot(self):
        bullet_position = self.position
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(bullet_position, bullet_velocity, 0)
        self.create_bullet_callback(bullet)
        # for i in range(-50, 51, 50):
        #     bullet = Bullet(bullet_position, bullet_velocity, i)
        #     self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def destroy(self, game):
        if self.lives > 1:
            self.lives -= 1
            self.spaceship_hit_asteroid.play()
            return False
        elif self.lives == 1:
            self.lives -= -1
            game.spaceship = None
            self.spaceship_destroy_sound.play()
            return True


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        self.asteroid_destroy_sound = load_sound("asteroid_destroy")
        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        self.asteroid_destroy_sound.play()
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity, rotation):
        super().__init__(position, load_sprite("bullet"), velocity)
        # rotation of bullet when fired
        self.velocity.rotate_ip(rotation)

    def move(self, surface):
        self.position = self.position + self.velocity
