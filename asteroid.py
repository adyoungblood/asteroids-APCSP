import pygame
from pygame.sprite import Sprite
import random
from vector import Vector

class Asteroid(Sprite):
    """A class to respresent a single asteroid"""

    def __init__(self, as_settings, screen, size, x, y):
        """Initialize the asteroid and its starting position"""
        super(Asteroid, self).__init__()
        self.screen = screen
        self.as_settings = as_settings
        self.size = size

        #Load a random asteroid image and set its rect properties
        self.image = pygame.image.load('images/asteroid{0}.png'.format(random.choice(range(1, 4))))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width * self.size, self.rect.height * self.size))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = Vector(self.as_settings.asteroid_speed_factor, random.randint(0, 359))

        #Store the asteroid's exact position
        self.center = [self.rect.centerx, self.rect.centery]

        if not self.size:
            self.size = self.as_settings.num_splits

    def blitme(self):
        """Draw the asteroid at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """Move the asteroid according to its velocity"""
        vel_components = self.velocity.components()
        self.center = [round(self.center[0] + vel_components[0], 2), round(self.center[1] + vel_components[1], 2)]
        if self.center[0] > self.as_settings.screen_width:
            self.center[0] = 0
        if self.center[0] < 0:
            self.center[0] = self.as_settings.screen_width
        if self.center[1] > self.as_settings.screen_height:
            self.center[1] = 0
        if self.center[1] < 0:
            self.center[1] = self.as_settings.screen_height
        self.rect.center = self.center
        self.mask = pygame.mask.from_surface(self.image, 0)

    def split(self, asteroids):
        if self.size == 1:
            asteroids.remove(self)
        else:
            asteroids.remove(self)
            for i in range(random.randint(2, 4)):
                new_asteroid = Asteroid(self.as_settings, self.screen, self.size - 1, self.center[0], self.center[1])
                asteroids.add(new_asteroid)
        
