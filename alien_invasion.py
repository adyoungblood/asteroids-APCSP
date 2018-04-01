import pygame

import sys

from pygame.sprite import Group

from pygame import time

from settings import Settings

from game_stats import GameStats

from ship import Ship

from asteroid import Asteroid

import game_functions as gf

def run_game():
    #Initialization of pygame, settings, and screen
    pygame.init()
    as_settings = Settings()
    screen = pygame.display.set_mode((as_settings.screen_width, as_settings.screen_height))
    pygame.display.set_caption("Asteroids")

    stats = GameStats(as_settings)
    

    #Make a group to store bullets in, a ship, and a group to store asteroids in
    ship = Ship(as_settings, screen)
    bullets = Group()
    asteroids = Group()

    #Create the fleet of asteroids
    #gf.create_fleet(as_settings, screen, ship, asteroids)
    
    print("Ships Left: " + str(stats.ships_left))

    ticker = pygame.time.Clock()

    #Main loop
    while True:
        ticker.tick(60)
        gf.check_events(as_settings, screen, ship, bullets)
        gf.check_ship_edges(as_settings, ship)
        
        if stats.game_active:
            ship.update()
            #gf.update_bullets(as_settings, screen, ship, asteroids, bullets)
            #gf.update_asteroids(as_settings, stats, screen, asteroids, ship, bullets)
        else:
            print("Game Over!!!")
            pygame.quit()
            sys.exit()
            break
        
        gf.update_screen(as_settings, screen, ship, asteroids, bullets)

run_game()
