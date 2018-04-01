class Settings():
    """A class for all necessary settings to run the game"""

    def __init__(self):
        """Initialize settings"""
        #Screen settings
        self.screen_width = 1800
        self.screen_height = 975
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_limit = 3
        self.ship_speed_factor = 1
        self.turn_factor = 5
        self.friction_factor = 0.5

        #Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.allowed_bullets = 3
        self.super_bullets = False

        #Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1
