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
        #self.mask = pygame.mask.from_surface(self.image)

        # Start each new ship at the center of the screen
        self.rect.center = self.screen_rect.center

        self.center  = [self.rect.centerx, self.rect.centery]

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
        '''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.as_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.as_settings.ship_speed_factor
        self.rect.centerx = self.center
        '''
        #pre-processing
        self.velocity.magnitude = round(self.velocity.magnitude, 2)
        self.velocity.bearing = round((self.velocity.bearing % 360), 2)
        self.direction = round((self.direction % 360), 2)
        
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
        self.velocity.magnitude = min(25, self.velocity.magnitude)
        if self.velocity.magnitude >= 0.5:
            self.velocity.magnitude -= 0.5
        elif self.velocity.magnitude > 0 and self.velocity.magnitude < 0.5:
            self.velocity.magnitude = 0

        #Adjust actual center and rotation without scaling or moving
        orig_rect = self.ori_image.get_rect()
        rot_image = pygame.transform.rotate(self.ori_image, -self.direction - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect.center = self.center
	
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.center
