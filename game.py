from chest import Chest
from config import *
import math
import pygame
from powerups import SpeedBoost, Shield, spawn_powerups, handle_powerup_collisions
from player import *
from enemy import Enemy
from shed import shed
from wall import Wall
from chest import Chest

#creatting the player for the game
def initiate_players():
    controls_player1 = {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d
    }

    controls_player2 = {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT
    }
    player = Player(cute_purple, (110,106), controls_player1)
    player2 = Player(greenish, (612,601), controls_player2)
    return [player, player2]

def game_loop(player, player2):

    current_state = "main"
    initiate = False

    #endless game loop 
    while True:
        if current_state == "main":
            current_state = execute_game(player, player2)
        elif current_state == "exit":
            initiate = True
            return initiate
        elif current_state == "shed":
            current_state = shed(player, player2)


def execute_game(player1, player2):

    # SETUP
    # setting up the background
    background = pygame.image.load("ui/background.png")
    background = pygame.transform.scale(background, (width, height)) #para que o background ocupe toda a tela

    # using the clock to control the time frame
    clock = pygame.time.Clock()
    powerups = []

    # screen setup:
    screen = pygame.display.set_mode(resolution)

    #pause button
    pause = pygame.image.load("ui/pause.png")
    pause_w, pause_h = pause.get_width(), pause.get_height()
    pause_hover_size = (pause_w * 1.2, pause_h * 1.2)
    pause_hover = pygame.transform.scale(pause, pause_hover_size)

    pygame.display.set_caption("Endless Wilderness Explorer")

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
    with open("maps/mapa.txt", 'r') as file:
        for line in file:
            if line.strip() == "":
                break
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

    # MAIN GAME LOOP
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen

        # Showing the walls on the screen
        wall_group.draw(screen)
        # Drawing the chest
        chest_group.draw(screen)
        #health bar for players
        pygame.draw.rect(screen, dark_red, [50, 0, player1.health, 30])
        pygame.draw.rect(screen, dark_red, [720 -50 - player2.health, 0, player2.health, 30])

        mouse= pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if 675 <= mouse[0] <= 675 + pause_w and -5<= mouse[1] <= -5 + pause_h:
            # scaling the original back button
            screen.blit(pause_hover, (675 - (pause_hover_size[0] - pause_w) // 2,
                                     -5 - (pause_hover_size[1] - pause_h) // 2))
        else:
            # if not hovering, then show the original play button

            screen.blit(pause, (675,-5))
        # handling events:
        status = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN or keys[pygame.K_RETURN]:
                if 675 <= mouse[0] <= 675 + pause_w and -5 <= mouse[1] <= -5 + pause_h:
                    status = pause_()

            #get coordinates in screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse[0], mouse[1])

        if status == "exit":
            return "exit"

        # automatically shoot bullets from the player
        player1.shoot(bullets1, 'space')
        player2.shoot(bullets2, 'enter')

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # todo: creating more types of enemies
            enemy1 = Enemy()
            enemy2 = Enemy()
            # adding the enemy to the group
            enemies1.add(enemy1)
            enemies2.add(enemy2)


            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            #  o inimigo vai espawnar em 2 seconds
            enemy_cooldown = fps * 2

        # updating the enemy cooldown. Isso é para que o inimigo não espawne de forma continua e fique espawnando de 1 em 1 segundo.
        # Ele atualiza em cada interacao do loop, ou seja, a cada frame.
        enemy_cooldown -= 1
        # updating positions and visuals
        player1_group.update(wall_group)
        player2_group.update(wall_group)

        # updating the bullets group
        bullets1.update(wall_group)
        bullets2.update(wall_group)

        enemies1.update(player1)
        enemies2.update(player2)

        spawn_powerups(powerups, 500, 500)
        handle_powerup_collisions([player1, player2], powerups)

        for powerup in powerups:
            powerup.draw(screen)

        # Verificando se o jogador está no canto inferior esquerdo da tela
        if (370 <= player1.rect.x <= 430 and 600 <= player1.rect.y <= 660):
            player1.hospital(delta_time = clock.get_time() / 1000)
        if (430 <= player2.rect.x <= 490 and 600 <= player2.rect.y <= 660):
            player2.hospital(delta_time = clock.get_time() / 1000)
        
        # Drawing rectangles to signal the coordinates
        pygame.draw.rect(screen, (255, 0, 0), (370, 600, 60, 60), 2)  # Player 1 hospital area
        pygame.draw.rect(screen, (0, 255, 0), (430, 600, 60, 60), 2)  # Player 2 hospital area

        #checking if the player moved off-screen from thwe right to the next area
        if player1.rect.right >= width and player2.rect.right >= width:
            return "shed"

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


        # checking for collisions between player bullets and enemies
        for bullet in bullets1:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            # Retorna uma lista com os inimigos que foram intersectados com uma bullet, ou seja, os inimigos que foram atingidos.
            # False means not kill upon impact
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies1, False)
            for enemy in collided_enemies:
                enemy.health -= 5

                # removing the bullet from the screen after hitting the player
                bullet.kill()

                if enemy.health <= 0:
                    enemy.kill()
        for bullet in bullets2:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            # Retorna uma lista com os inimigos que foram intersectados com uma bullet, ou seja, os inimigos que foram atingidos.
            # False means not kill upon impact
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies2, False)
            for enemy in collided_enemies:
                enemy.health -= 5

                # removing the bullet from the screen after hitting the player
                bullet.kill()

                if enemy.health <= 0:
                    enemy.kill()

        # checking for collisions between player bullets and chest
        for bullet in bullets1:
            collided_chest= pygame.sprite.spritecollide(bullet, chest_group, False)
            for chest in collided_chest:
                chest.life -= 10
                bullet.kill()
                if chest.life <= 0:
                    #change the image of chest for a broken one
                    chest.dead()
        # updates the whole screen since the frame was last drawn
        # handling events:
        pygame.display.flip()
    # the main while loop was terminated
    pygame.quit()


def pause_():
    screen = pygame.display.set_mode(resolution)

    # in order to print something we need to first create a font, create the text and then blit

    # creating the fonts:
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # creating the rendered texts for the credits
    pause_text = comicsansfont.render("PAUSED", True, white)
    exit_text = comicsansfont.render("exit", True, white)

    # main loop to detect user input and display the credits
    # pause = True
    while True:
        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 500 <= mouse[1] <= 560:
                    return 'exit'

        # display my screen
        # we can fill the screen with an image instead of deep_black
        screen.fill(deep_black)

        # displaying our texts
        screen.blit(pause_text, (720//2,720//2))


        # drawing and displaying the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        pygame.draw.rect(screen, dark_red, [450, 500, 140, 60])


        back_text = corbelfont.render("back", True, white)
        exit_text = corbelfont.render("exit", True, white)

        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        exit_rect = exit_text.get_rect(center = (450 + 140 //2, 500 + 60 // 2))
        screen.blit(back_text, back_rect)
        screen.blit(exit_text, exit_rect)

        # updating the display
        pygame.display.update()
