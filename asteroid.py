import pygame
from pygame.sprite import Sprite
import random
from vector import Vector

class Asteroid(Sprite):
    """A class to respresent a single asteroid"""

    def __init__(self, as_settings, screen):
        """Initialize the asteroid and its starting position"""
        super(Asteroid, self).__init__()
        self.screen = screen
        self.as_settings = as_settings

        #Load a random asteroid image and set its rect properties
        self.image = pygame.image.load('images/asteroid{0}.png'.format(random.choice(range(1, 4))))
        self.rect = self.image.get_rect()
        #self.mask = pygame.mask.from_surface(self.image)

        #Start each new asteroid near the edges of the screen
        screen_rect = self.screen.get_rect()
        if random.randint(0, 1) == 1:  
            self.rect.x = random.randint(0, int(screen_rect.width / 4))
        else:
            self.rect.x = random.randint(int((3 * screen_rect.width) / 4), screen_rect.width)
        if random.randint(0, 1) == 1:
            self.rect.y = random.randint(0, int(self.rect.height / 4))
        else:
            self.rect.y = random.randint(int((3 * screen_rect.height) / 4), screen_rect.height)
        self.velocity = Vector(self.as_settings.asteroid_speed_factor, random.randint(0, 359))

        #Store the asteroid's exact position
        self.center = [self.rect.centerx, self.rect.centery]

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
        
