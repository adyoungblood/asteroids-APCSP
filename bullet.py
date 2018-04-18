import pygame
from pygame.sprite import Sprite
import math

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, as_settings, screen, ship):
        #Create a bullet object at the ship's current position
        super(Bullet, self).__init__()
        self.screen = screen

        #Create a bullet rect at (0, 0) and then set correct position
        self.direction = ship.direction
        self.rect = pygame.Rect(0, 0, as_settings.bullet_width, as_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx + (as_settings.bullet_dist * math.cos(math.radians(self.direction)))
        self.rect.centery = ship.rect.centery + (as_settings.bullet_dist * math.sin(math.radians(self.direction)))
        self.mask = pygame.mask.Mask((as_settings.bullet_width, as_settings.bullet_height))
        self.mask.fill()

        #stores the bullet's position as decimal values
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.time_remaining = as_settings.bullet_time

        self.color = as_settings.bullet_color
        self.speed_factor = as_settings.bullet_speed_factor + ship.velocity.magnitude

    def update(self):
        """Move the bullet forwards"""
        #Update the decimal position of the bullet
        self.x += self.speed_factor * math.cos(math.radians(self.direction))
        self.y += self.speed_factor * math.sin(math.radians(self.direction))
        #Update the rect position
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.time_remaining -= 1

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
