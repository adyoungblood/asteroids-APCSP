import ctypes

class Settings():
    """A class for all necessary settings to run the game"""

    def __init__(self):
        """Initialize settings"""

        user32 = ctypes.windll.user32
        
        #Screen settings
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1) - 75
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_limit = 3
        self.ship_speed_factor = 0.5
        self.turn_factor = 5
        self.friction_factor = 0.2
        self.max_speed = 20

        #Bullet settings
        self.bullet_speed_factor = 10
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = 60, 60, 60
        self.bullet_dist = 25
        self.bullet_time = 120

        #Asteroid settings
        self.asteroid_speed_factor = 1
        self.num_splits = 3
        self.fleet_direction = 1
