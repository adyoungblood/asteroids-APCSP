import sys

import pygame

from time import sleep

from bullet import Bullet

from asteroid import Asteroid

clock = pygame.time.Clock()

def ship_hit(as_settings, stats, screen, ship, asteroids, bullets):
    """Respond to ship being hit by alien"""

    if stats.ships_left > 0:
        print("Ship hit!!!")
    
        #Decrement ships left
        stats.ships_left -= 1

        #Empty the list of asteroids and bullets
        bullets.empty()
        asteroids.empty()

        #Create a new fleet and center the ship
        create_fleet(as_settings, screen, ship, asteroids)
        ship.center_ship()

        #Pause and print ships remaining
        sleep(0.5)

        print("Ships Left: " + str(stats.ships_left))

    else:
        stats.game_active = False

def check_keydown_events(event, as_settings, screen, ship, bullets):
    """Respond to key presses"""
    if event.key == pygame.K_w:
        ship.moving_forward = True
    if event.key == pygame.K_d:
        #Enable the ship's movement flag
        ship.turning_right = True
    if event.key == pygame.K_a:
        ship.turning_left = True
    if event.key == pygame.K_SPACE:
        #Create a new bullet and add it to the bullets group if there aren't too many bullets
        fire_bullet(as_settings, screen, ship, bullets)
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

def check_events(as_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, as_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(as_settings, screen, ship, asteroids, bullets):
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

    #Draw the screen
    pygame.display.flip()

def update_bullets(as_settings, screen, ship, asteroids, bullets):
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
    #check_bullet_asteroid_collisions(as_settings, screen, ship, asteroids, bullets)


def check_bullet_asteroid_collisions(as_settings, screen, ship, asteroids, bullets):
    """Respond to bullet-alien collisions"""
    #Remove any bullets and asteroids that have collided
    if as_settings.super_bullets:
        collisions = pygame.sprite.groupcollide(bullets, asteroids, False, True)
    else:
        collisions = pygame.sprite.groupcollide(bullets, asteroids, True, True)

    if len(asteroids) == 0:
        #Destroy existing bullets and create new fleet
        bullets.empty()
        create_fleet(as_settings, screen, ship, asteroids)

def fire_bullet(as_settings, screen, ship, bullets):
    """Fire a bullet"""
    #Create a new bullet and add it to the bullets group
    new_bullet = Bullet(as_settings, screen, ship)
    bullets.add(new_bullet)

def get_number_asteroids_x(as_settings, alien_width):
    """Determine the number of asteroids that fit in a row"""
    available_space_x = as_settings.screen_width - 2 * alien_width
    number_asteroids_x = int(available_space_x / (2 * alien_width))
    return number_asteroids_x

def create_alien(as_settings, screen, asteroids, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(as_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    asteroids.add(alien)
        
def create_fleet(as_settings, screen, ship, asteroids):
    """Create a full fleet of asteroids"""
    #Create an alien and find the number of asteroids in a row
    alien = Alien(as_settings, screen)
    number_asteroids_x = get_number_asteroids_x(as_settings, alien.rect.width)
    number_rows = get_number_rows(as_settings, ship.rect.height, alien.rect.height)
 

    #Create the first row of asteroids
    for row_number in range(number_rows):
        for alien_number in range(number_asteroids_x):
            create_alien(as_settings, screen, asteroids, alien_number, row_number)

def get_number_rows(as_settings, ship_height, alien_height):
    """Determine the number of rows of asteroids that fit on the screen"""
    available_space_y = (as_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_asteroids(as_settings, stats, screen, asteroids, ship, bullets):
    """Check if the fleet is at an edge, then
    update the position of all asteroids in the fleet"""
    check_fleet_edges(as_settings, asteroids)
    asteroids.update()

    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, asteroids):
        ship_hit(as_settings, stats, screen, ship, asteroids, bullets)

    #Look for asteroids hitting the bottom of the screen
    check_asteroids_bottom(as_settings, stats, screen, ship, asteroids, bullets)
        

# TODO: fix all of this jeebus
def check_fleet_edges(as_settings, asteroids):
    """Respond appropriately if any asteroids have reached an edge"""
    for alien in asteroids.sprites():
        if alien.check_edges():
            change_fleet_direction(as_settings, asteroids)
            break

def check_ship_edges(as_settings, ship):
    if ship.center[0] > as_settings.screen_width:
        ship.center[0] = 0
    if ship.center[0] < 0:
        ship.center[0] = as_settings.screen_width
    if ship.center[1] > as_settings.screen_height:
        ship.center[1] = 0
    if ship.center[1] < 0:
        ship.center[1] = as_settings.screen_height

def check_asteroids_bottom(as_settings, stats, screen, ship, asteroids, bullets):
    """Check if any asteroids have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in asteroids.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this like the ship was hit
            ship_hit(as_settings, stats, screen, ship, asteroids, bullets)
            break
