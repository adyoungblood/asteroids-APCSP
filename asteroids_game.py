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
    pygame.font.init()
    pygame.mixer.init()
    display_font = pygame.font.SysFont('Comic Sans MS', as_settings.text_size)
    screen = pygame.display.set_mode((as_settings.screen_width, as_settings.screen_height))
    pygame.display.set_caption("Asteroids")

    stats = GameStats(as_settings)

    #Make a group to store bullets in, a ship, and a group to store asteroids in
    ship = Ship(as_settings, screen)
    bullets = Group()
    asteroids = Group()

    #Make sounds
    bulletfire = pygame.mixer.Sound('sounds/firebullet.wav')
    asteroidexplosion = pygame.mixer.Sound('sounds/asteroidexplosion.wav')
    shipexplosion = pygame.mixer.Sound('sounds/shipexplosion.wav')
    sounds = {'asteroid' : asteroidexplosion, 'ship' : shipexplosion, 'bullet' : bulletfire}

    #Create asteroids
    gf.spawn_asteroids(as_settings, stats, screen, ship, asteroids)

    ticker = pygame.time.Clock()

    #Main loop
    while True:
        shipsurface = display_font.render('Ships Left: ' + str(stats.ships_left), False, (0, 0, 0))
        stagesurface = display_font.render('Stage: ' + str(stats.stage), False, (0, 0, 0))
        pointsurface = display_font.render('Points: ' + str(stats.points), False, (0, 0, 0))
        ticker.tick(60)
        gf.check_events(as_settings, screen, ship, bullets, sounds)
        gf.check_ship_edges(as_settings, ship)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(as_settings, stats, screen, ship, asteroids, bullets, sounds)
            gf.update_asteroids(as_settings, stats, screen, asteroids, ship, bullets, sounds)
        else:
            print("Game Over!!!")
            pygame.quit()
            sys.exit()
            break

        gf.update_screen(as_settings, stats, screen, ship, asteroids, bullets, (shipsurface, stagesurface, pointsurface))

run_game()
