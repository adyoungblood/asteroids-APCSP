import sys

import pygame

from time import sleep

from bullet import Bullet

from asteroid import Asteroid

import random

clock = pygame.time.Clock()

def ship_hit(as_settings, stats, screen, ship, asteroids, bullets, sounds):
    """Respond to ship being hit by asteroid"""

    if stats.ships_left > 0:
        if ship.invincible_time == 0:

            sounds['ship'].play()
            ship.explode()
    
            #Pause and print ships remaining
            sleep(0.5)
        
            #Decrement ships left
            stats.ships_left -= 1

            #Center ship
            ship.center_ship()

            #Give ship invincibility
            ship.invincible_time = as_settings.ship_invincible_time
    else:
        stats.game_active = False

def check_keydown_events(event, as_settings, screen, ship, bullets, sounds):
    """Respond to key presses"""
    if event.key == pygame.K_w:
        ship.moving_forward = True
    if event.key == pygame.K_d:
        #Enable the ship's movement flag
        ship.turning_right = True
    if event.key == pygame.K_a:
        ship.turning_left = True
    if event.key == pygame.K_SPACE:
        #Create a new bullet and add it to the bullets group
        fire_bullet(as_settings, screen, ship, bullets, sounds)
    if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    #Disable the ship's movement flag
    if event.key == pygame.K_w:
        ship.moving_forward = False
    if event.key == pygame.K_d:
        ship.turning_right = False
    elif event.key == pygame.K_a:
        ship.turning_left = False

def check_events(as_settings, screen, ship, bullets, sounds):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, as_settings, screen, ship, bullets, sounds)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(as_settings, stats, screen, ship, asteroids, bullets, textsurfaces):
    """Update all images on screen and redraw it"""
    #Draw color
    screen.fill(as_settings.bg_color)

    #Redraw all bullets behind ship and asteroids
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #Draw the ship
    ship.blitme()

    #Draw the alien
    asteroids.draw(screen)

    #Draw the score and stage text
    y_diff = 0
    for surface in textsurfaces:
        screen.blit(surface, (as_settings.text_dist_x, y_diff * as_settings.text_dist_y))
        y_diff += 1

    #Draw the screen
    pygame.display.flip()

def update_bullets(as_settings, stats, screen, ship, asteroids, bullets, sounds):
    """Update positions of bullets and remove old ones"""
    #Update bullet positions
    bullets.update()

    #Get rid of old bullets
    for bullet in bullets:#.copy():
        if bullet.time_remaining <= 0:
            bullets.remove(bullet)
        if bullet.rect.x < 0:
            bullet.x = as_settings.screen_width
        if bullet.rect.x > as_settings.screen_width:
            bullet.x = 0
        if bullet.rect.y < 0:
            bullet.y = as_settings.screen_height
        if bullet.rect.y > as_settings.screen_height:
            bullet.y = 0
    check_bullet_asteroid_collisions(as_settings, stats, screen, ship, asteroids, bullets, sounds)


def check_bullet_asteroid_collisions(as_settings, stats, screen, ship, asteroids, bullets, sounds):
    """Respond to bullet-alien collisions"""
    #Remove any bullets that have collided with asteroids and split those asteroids
    for asteroid in asteroids:
        for bullet in bullets:
            if pygame.sprite.collide_mask(asteroid, bullet):
                stats.points += as_settings.asteroid_points
                sounds['asteroid'].play()
                asteroid.split(asteroids)
                bullets.remove(bullet)
                
    if len(asteroids) == 0:
        #Move to next stage
        bullets.empty()
        stats.stage += 1
        print('Stage: ' + str(stats.stage))
        spawn_asteroids(as_settings, stats, screen, ship, asteroids)

def fire_bullet(as_settings, screen, ship, bullets, sounds):
    """Fire a bullet"""
    #Create a new bullet and add it to the bullets group
    sounds['bullet'].play()
    new_bullet = Bullet(as_settings, screen, ship)
    bullets.add(new_bullet)

def spawn_asteroids(as_settings, stats, screen, ship, asteroids):
    """Create a number of asteroids based on stage"""
    screen_rect = screen.get_rect()
    for ast in range(0, random.randint(as_settings.num_asteroids_min, as_settings.num_asteroids_max) * stats.stage):
        ast_x = 0
        ast_y = 0
        if random.randint(0, 1) == 1:  
            ast_x = random.randint(0, int(screen_rect.width / 4))
        else:
            ast_x = random.randint(int((3 * screen_rect.width) / 4), screen_rect.width)
        if random.randint(0, 1) == 1:
            ast_y = random.randint(0, int(screen_rect.height / 4))
        else:
            ast_y = random.randint(int((3 * screen_rect.height) / 4), screen_rect.height)
        new_asteroid = Asteroid(as_settings, screen, as_settings.num_splits, ast_x, ast_y)
        asteroids.add(new_asteroid)

def update_asteroids(as_settings, stats, screen, asteroids, ship, bullets, sounds):
    """Update the position of all asteroids and check for collisions"""
    asteroids.update()

    #Look for alien-ship collisions
    if pygame.sprite.spritecollide(ship, asteroids, False, pygame.sprite.collide_mask):
        ship_hit(as_settings, stats, screen, ship, asteroids, bullets, sounds)

def check_ship_edges(as_settings, ship):
    if ship.center[0] > as_settings.screen_width:
        ship.center[0] = 0
    if ship.center[0] < 0:
        ship.center[0] = as_settings.screen_width
    if ship.center[1] > as_settings.screen_height:
        ship.center[1] = 0
    if ship.center[1] < 0:
        ship.center[1] = as_settings.screen_height
