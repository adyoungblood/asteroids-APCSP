import pygame

import math

from vector import Vector

class Ship():
    
    def __init__(self, as_settings, screen):
        """Initialization of the ship and setting its starting position"""
        self.screen = screen
        self.as_settings = as_settings

        # load ship image and get its rect and mask
        self.ori_image = pygame.image.load('images/ship.png')
        self.image = self.ori_image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Start each new ship at the center of the screen
        self.rect.center = self.screen_rect.center

        self.center = [self.rect.centerx, self.rect.centery]

        self.invincible_time = 0

        #Movement flags
        self.turning_right = False
        self.turning_left = False
        self.moving_forward = False
		
        #Movement stats
        self.velocity = Vector(0, 0)
        self.direction = 0

    def update(self):
        """Update the ship's position based on vectors"""
        #Update the ship's center value, not the rect
        #pre-processing
        if self.invincible_time > 0:
            self.invincible_time -= 1
        self.velocity.magnitude = round(self.velocity.magnitude, 2)
        self.velocity.bearing = round(bound(self.velocity.bearing, 0, 360), 2)
        self.direction = round(bound(self.direction, 0, 360), 2)
        
        #React to key events
        if self.turning_right:
            self.direction += self.as_settings.turn_factor
        if self.turning_left:
            self.direction -= self.as_settings.turn_factor
        if self.moving_forward:
            self.velocity = self.velocity.resultant_vector(Vector(self.as_settings.ship_speed_factor, self.direction))
            
        #Calculate new velocity and update center value
        vel_components = self.velocity.components()
        self.center = [round(self.center[0] + vel_components[0], 2), round(self.center[1] + vel_components[1], 2)]

        #post-processing
        self.velocity.magnitude = min(self.as_settings.max_speed, self.velocity.magnitude)
        if self.velocity.magnitude > 0:
            self.velocity = self.velocity.resultant_vector(Vector(self.as_settings.friction_factor, self.velocity.bearing - 180))
        else:
            self.velocity.magnitude = 0

        #Adjust actual center and rotation without scaling or moving sprite
        orig_rect = self.ori_image.get_rect()
        rot_image = pygame.transform.rotate(self.ori_image, -(self.direction + 90))
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        
        self.rect.center = self.center

        self.mask = pygame.mask.from_surface(self.image)

    def blitme(self):
        """Draw the ship at its current location"""
        if ((self.invincible_time / self.as_settings.flash_time) - self.invincible_time % self.as_settings.flash_time) % 2 == 0 and self.invincible_time != 0:
            blank_surface = pygame.Surface((100, 100))
            blank_surface.fill(self.as_settings.bg_color)
            self.screen.blit(blank_surface, self.rect)
        else:
            self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.center

    def explode(self):
        """Change the sprite to an explosion"""
        self.direction = 0
        self.velocity = Vector(0, 0)
        self.screen.blit(pygame.image.load('images/shipexplosion.png'), (self.center[0] - 100, self.center[1] - 100))
        pygame.display.flip()


def bound(value, low, high):
    diff = high - low
    return (((value - low) % diff) + low)
