from config import *
import pygame
from enemy import Enemy
from wall import Wall
from chest import Chest
import sounds
import random
from powerup import SpeedBoost, Shield, spawn_powerups, handle_powerup_collisions
import random
import game_over


def game_loop(player, player2):
    """
    Main game loop managing the game state.

    Args:
        player (Player): First player object.
        player2 (Player): Second player object.

    Returns:
        None
    """
    # setting the current state of the game
    current_state = "main"

    # endless game loop
    while True:
        if current_state == "main":
            current_state = execute_game(player, player2)
            if current_state == "exit":
                return


def execute_game(player1, player2):
    """
    Main game execution function.

    Args:
        player1 (Player): First player object.
        player2 (Player): Second player object.

    Returns:
        str: "exit" if the game should exit, otherwise None.
    """

    # SETUP

        
    # play the background sound
    sounds.background_sound.play(-1)

    # setting up the background
    background = pygame.image.load("images/background_2.png")
    background = pygame.transform.scale(background, (width, height))  

    # using the clock to control the time frame
    clock = pygame.time.Clock()

    powerups = []

    # screen setup:
    screen = pygame.display.set_mode(resolution)

    # pause button setup and hover effect
    pause = pygame.image.load("ui/pause.png")
    pause_w, pause_h = pause.get_width(), pause.get_height()
    pause_hover_size = (pause_w * 1.2, pause_h * 1.2)
    pause_hover = pygame.transform.scale(pause, pause_hover_size)

    # creating an empty group for the player
    player1_group = pygame.sprite.Group()
    player2_group = pygame.sprite.Group()

    # adding the player to the group
    player1_group.add(player1)
    player2_group.add(player2)

    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets1 = pygame.sprite.Group()
    bullets2 = pygame.sprite.Group()

    # creating an enemy group
    enemies1 = pygame.sprite.Group()
    enemies2 = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown
    enemy_cooldown = 0

    # reading the map file and creating sprite groups of walls
    wall_group = pygame.sprite.Group()
    chest_group = pygame.sprite.Group()
    lines = []
    with open("maps/mapa3.txt", 'r') as file:
        for line in file:
            if line.strip() == "":
                continue
            lines.append(line)

    # adding a position to each tile and adding each tile to the sprite group
    for row, tiles in enumerate(lines):
        for col, tile in enumerate(tiles):
            if tile == "#":
                wall = Wall(col, row)
                wall_group.add(wall)
            if tile == "*":
                chest = Chest(col, row)
                chest_group.add(chest)

    # randomly select a chest(destroyer) to have the key (bomb)
    for chest in chest_group:
        chest.key_available = False
    random_chest = random.choice(chest_group.sprites())
    random_chest.key_available = True


    # MAIN GAME LOOP
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))  

        # Load the destroyer image
        destroyer_image = pygame.image.load("images/boss.png")
        destroyer_image = pygame.transform.scale(destroyer_image, (70, 70))

        # Draw the destroyer image
        screen.blit(destroyer_image, (335, 300))

        # Showing the walls on the screen
        wall_group.draw(screen)
        # Showing the chest (destroyer) on the screen
        chest_group.draw(screen)

        # health bar for players 
        pygame.draw.rect(screen, grey, [50, 0, 100, 20], border_radius=5)
        pygame.draw.rect(screen, dark_red, [50, 0, player1.health, 20], border_radius=5)
        pygame.draw.rect(screen, grey, [720 - 100 - 50, 0, 100, 20], border_radius=5)
        pygame.draw.rect(screen, dark_red, [720 - 50 - player2.health, 0, player2.health, 20], border_radius=5)


        # Draw the powerup icons (for player1 and player2)
        if player1.active_powerup in ['SpeedBoost', 'Shield', 'Despawner', 'Invisible']:
            pygame.draw.circle(screen, yellow, [170, 10], 10)
            powerup_image = pygame.image.load(f'ui/powerups/{player1.active_powerup}.png')
            powerup_image = pygame.transform.scale(powerup_image, (20, 20))
            # Blit the image on top of the circle
            screen.blit(powerup_image, (160, 0))

        if player2.active_powerup in ['SpeedBoost', 'Shield', 'Despawner', 'Invisible']:
            pygame.draw.circle(screen, yellow, [720 - 170, 10], 10)
            powerup_image2 = pygame.image.load(f'ui/powerups/{player2.active_powerup}.png')
            powerup_image2 = pygame.transform.scale(powerup_image2, (20, 20))
            # Blit the image on top of the circle
            screen.blit(powerup_image2, (720 - 180, 0))

        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()
        # getting the keys pressed by the user
        keys = pygame.key.get_pressed()

        # checking if the user is hovering over the pause button
        if 675 <= mouse[0] <= 675 + pause_w and -5 <= mouse[1] <= -5 + pause_h:
            screen.blit(pause_hover, (675 - (pause_hover_size[0] - pause_w) // 2,
                                      -5 - (pause_hover_size[1] - pause_h) // 2))
        else:
            screen.blit(pause, (675, -5))


        # handling events:
        cont = ""
        for event in pygame.event.get():
            # allow the user to quit on (x)
            if event.type == pygame.QUIT:
                player1.save_player_data("save_player_data.json")
                player2.save_player_data( "save_player_2_data.json")
                pygame.quit()

            # checking if the user clicked the back button
            if event.type == pygame.MOUSEBUTTONDOWN or keys[pygame.K_RETURN]:
                if 675 <= mouse[0] <= 675 + pause_w and -5 <= mouse[1] <= -5 + pause_h:
                    cont = pause_(player1, player2)

            # get coordinates in screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse[0], mouse[1])

        # checking if the user wants to exit the game
        if cont == "exit":
            return "exit"

        # Shoot bullets from the players
        player1.shoot(bullets1, 'space')
        player2.shoot(bullets2, 'enter')

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # creating the enemy object
            enemy1 = Enemy('player1')
            enemy2 = Enemy('player2')
            # adding the enemy to the group
            enemies1.add(enemy1)
            enemies2.add(enemy2)

            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            enemy_cooldown = fps * 2

        # updating the enemy cooldown. 
        enemy_cooldown -= 1

        # updating positions and visuals
        player1_group.update(wall_group)
        player2_group.update(wall_group)

        # updating the bullets group
        bullets1.update(wall_group)
        bullets2.update(wall_group)

        # updating the enemies group
        enemies1.update(player1)
        enemies2.update(player2)

        # powerup handling
        spawn_powerups(powerups, 500, 500)
        handle_powerup_collisions([player1, player2], powerups, [enemies1, enemies2])

         # Draw health bar above the chests (destroyers)
        for chest in chest_group:
            health_bar_height = 6
            health_percentage = chest.life / 50
            health_bar_fill = 40 * health_percentage

            health_bar_rect = pygame.Rect(
                chest.rect.x ,
                chest.rect.y - health_bar_height - 2,
                health_bar_fill,
                health_bar_height
            )

            pygame.draw.rect(screen, red, health_bar_rect)

        # Draw the powerups on the screen
        for powerup in powerups:
            powerup.draw(screen)

        # Draw the planets on the screen
        red_planet = pygame.image.load("images/red_planet.png")
        blue_planet = pygame.image.load("images/blue_planet.png")

        # Scale the planet images
        red_planet = pygame.transform.scale(red_planet, (60, 60))
        blue_planet = pygame.transform.scale(blue_planet, (60, 60))

        # Draw the planet images
        screen.blit(red_planet, (width - 200, 200))  # Top right corner with some padding
        screen.blit(blue_planet, (80, height - 200))  # Bottom left corner with some padding

        # Check if players are on the planets for healing
        if red_planet.get_rect(topleft=(width - 200, 200)).colliderect(player1.rect):
            player1.hospital(delta_time=clock.get_time() / 1000)
        if blue_planet.get_rect(topleft=(80, height - 200)).colliderect(player2.rect):
            player2.hospital(delta_time=clock.get_time() / 1000)


        # drawing the player and enemies sprites on the screen
        player1.draw(screen)
        player2.draw(screen)
        enemies1.draw(screen)
        enemies2.draw(screen)

        # drawing the bullet sprites
        for bullet in bullets1:
            bullet.draw(screen)
        for bullet in bullets2:
            bullet.draw(screen)

        # overriding draw cause to make the key
        for chest in chest_group:
            chest.draw(screen)

        # checking for collisions between player bullets (1 and 2) and enemies
        for bullet in bullets1:
            # False means not kill upon impact
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies1, False)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        for bullet in bullets2:
            # False means not kill upon impact
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies2, False)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # checking for collisions between player bullets and chest (destroyer)
        for bullet in bullets1:
            collided_chest = pygame.sprite.spritecollide(bullet, chest_group, False)
            for chest in collided_chest:
                chest.life -= 10
                bullet.kill()
                if chest.life <= 0:
                    chest.dead()

        for bullet in bullets2:
            collided_chest = pygame.sprite.spritecollide(bullet, chest_group, False)
            for chest in collided_chest:
                chest.life -= 10
                bullet.kill()
                if chest.life <= 0:
                    chest.dead()

        for chest in chest_group:
            # updating to check the collision
            chest.update(player1_group)
            chest.update(player2_group)

        destroyer_rect = destroyer_image.get_rect(topleft=(335, 300))

        if destroyer_rect.colliderect(player1.rect) and player1.has_key:
            # if the player collided with the boss, we will return to the game over screen
            player1.coins += 200
            player2.coins += 50
            player1.has_key = False  # Ensure the function is called only once
            cont = game_over.game_over( player1, player2)

        if destroyer_rect.colliderect(player2.rect) and player2.has_key:
            # if the player collided with the boss, we will return to the game over screen
            player2.coins += 200
            player1.coins += 50
            player2.has_key = False
            cont = game_over.game_over(player1, player2)
        if cont == "exit":
            return "exit"
        
        # updates the whole screen since the frame was last drawn
        pygame.display.flip()
    # the main while loop was terminated
    pygame.quit()


def pause_(player, player2):
    """
    Displays a pause menu with options to resume or exit the game.

    Args:
        player: The first player object, which contains methods for respawning and saving player data.
        player2: The second player object, which contains methods for respawning and saving player data.

    Returns:
        None if the game is resumed.
        'exit' if the exit button is clicked, indicating the game should be terminated.
    """
    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # setting up the background
    background = pygame.image.load("ui/background_2.png")
    background = pygame.transform.scale(background, (width, height))

    # loading the pause image
    paused = pygame.image.load("ui/paused.png")

    # loading the resume and exit button with hover effect
    resume = pygame.image.load("ui/resume.png")
    resume_w, resume_h = resume.get_width(), resume.get_height()
    resume_hover = pygame.image.load("ui/resume_hover.png")

    exit_btn = pygame.image.load("ui/exit.png")
    exit_btn_w, exit_btn_h = exit_btn.get_width(), exit_btn.get_height()
    exit_btn_hover = pygame.image.load("ui/exit_hover.png")


    while True:
        # setting up the background
        screen.blit(background, (0,0))
        # setting up the pause image
        screen.blit(paused, (250, 110))
        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        # checking if the user is hovering over the buttonn
        if 270 <= mouse[0] <= 270 + resume_w and 280 <= mouse[1] <= 280 + resume_h:
            screen.blit(resume_hover, (270 - (resume_hover.get_width() - resume_w) // 2,
                                       280 - (resume_hover.get_height() - resume_h) // 2))
        else:
            screen.blit(resume, (270, 280))

        if 270 <= mouse[0] <= 270 + exit_btn_w and 390 <= mouse[1] <= 390 + exit_btn_h:
            screen.blit(exit_btn_hover, (270 - (exit_btn_hover.get_width() - exit_btn_w) // 2,
                                       390 - (exit_btn_hover.get_height() - exit_btn_h) // 2))
        else:
            screen.blit(exit_btn, (270, 390))


        for ev in pygame.event.get():
            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()


            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the user clicked the resume button
                if 270 <= mouse[0] <= 270 + resume_w and 280 <= mouse[1] <= 280 + resume_h:
                    return
                # checking if the user clicked the exit button
                if 270 <= mouse[0] <= 270 + exit_btn_w and 390 <= mouse[1] <= 390 + exit_btn_h:
                    player.respawn()
                    player2.respawn()
                    player.save_player_data("save_player_data.json")
                    player2.save_player_data("save_player_2_data.json")
                    sounds.background_sound.stop()
                    return 'exit'

        # updating the display
        pygame.display.update()

