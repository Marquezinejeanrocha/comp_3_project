from config import *
import math
import pygame
from player import Player
from enemy import Enemy
from shed import shed

def game_loop():
    #creatting the player for the game
    player = Player()   

    #by default, I started the player in the main area
    current_state = "main"

    #endless game loop 
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


 
def execute_game(player):

    # SETUP
    # setting up the background
    background = pygame.image.load("images/stardew_valley.jpg")
    background = pygame.transform.scale(background, (width, height))

    # using the clock to control the time frame
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)

    pygame.display.set_caption("Endless Wilderness Explorer")

    # creating an empty group for the player
    player_group = pygame.sprite.Group()

    # adding the player to the group
    player_group.add(player)

    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets = pygame.sprite.Group()

    # creating an enemy group
    enemies = pygame.sprite.Group()

    #reading the map file and creating sprite groups of walls
    wall_group = pygame.sprite.Group()
    lines = []
    with open("maps/mapa.txt", 'r') as file:
        for line in file:
            if line.strip() == "":
                break
            lines.append(line)
    #adding a position to each tile and adding each tile to the sprite group
    for row, tiles in enumerate(lines):
        for col, tile in enumerate(tiles):
            if tile == "#":
                wall = Wall(col, row)
                wall_group.add(wall)

    # before starting our main loop, setup the enemy cooldown
    enemy_cooldown = 0

    # MAIN GAME LOOP
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen

        #showing the walls on the screen
         wall_group.draw(screen)

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # automatically shoot bullets from the player
        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # todo: creating more types of enemies
            enemy = Enemy()

            # adding the enemy to the group
            enemies.add(enemy)

            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            enemy_cooldown = fps * 2 #  o inimigo vai espawnar em 2 seconds

        # updating the enemy cooldown. Isso é para que o inimigo não espawne de forma continua e fique espawnando de 1 em 1 segundo. Ele atualiza em cada interacao do loop, ou seja, a cada frame.
        enemy_cooldown -= 1

        # updating positions and visuals
        player_group.update()

        # updating the bullets group
        bullets.update()
        enemies.update(player)

        #checking if the player moved off-screen from thwe right to the the next area
        if player.rect.right >= width:
            return "shed"

        # drawing the player and enemies sprites on the screen
        player_group.draw(screen)
        enemies.draw(screen)

        # drawing the bullet sprites
        for bullet in bullets:
            bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        for bullet in bullets:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False) # Retorna uma lista com os inimigos que foram intersectados com uma bullet, ou seja, os inimigos que foram atingidos. False means not kill upon impact
            for enemy in collided_enemies:
                enemy.health -= 5

                # removing the bullet from the screen after hitting the player
                bullet.kill()

                if enemy.health <= 0:
                    enemy.kill()

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    pygame.quit()
