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
    background = pygame.transform.scale(background, (width, height)) #para que o background ocupe toda a tela

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

    # before starting our main loop, setup the enemy cooldown
    enemy_cooldown = 0

    # MAIN GAME LOOP
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen

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




    #---------------------------------Player---------------------------------

    from utils import *
from config import *
import pygame 
import math
from bullet import Bullet
 
# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self, color, location):
        # calling the mother classes init aka Sprite
        super().__init__()

        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # drawing the image of the player
        self.image.fill(color) 
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # centering the player in its rectangle
        self.rect.center = location   #(width // 2, height // 2) 

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0

    def update(self):
        # getting the keys input
        keys = pygame.key.get_pressed()

        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, bullets):
        """
        bullets --> pygame group where I will add bullets
        """
        # todo: different weapons have different cooldowns
        # cooldown ==> how many frames I need to wait until I can shoot again
        if self.bullet_cooldown <= 0:
            # defining the directions in which the bullets will fly
            # these 4 directions, are in order, right, left, up and down
            for angle in [0, math.pi, math.pi / 2, 3*math.pi / 2]:
                # Creating a bullet for each angle
                # I will use self.rect.centerx to make the x position of the bullet the same as the
                # x position of the player, thus making the bullet come out of them
                # finally, the direction of the bullet is the angle
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1