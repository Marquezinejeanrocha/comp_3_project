from config import *
import pygame
import random
import math
from player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, status):
        super().__init__()
        # creating a surface for the enemy
        if status == 'player1':
            self.image = pygame.image.load("ui/enemy_2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))

        if status == 'player2':
            self.image = pygame.image.load("ui/enemy_3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))



        # getting rectangle for positioning
        self.rect = self.image.get_rect()

        # starting the enemy at random valid location on the screen
        self.rect.x = random.randint(0, width - enemy_size[0])  # para o inimigo nao espawnar fora da tela
        self.rect.y = random.randint(0, height - enemy_size[-1])

        # setting a random initial speed for the enemy
        self.speed = random.randint(1, 3)

        # setting the health bar
        self.health = 10

        self.exploding_counter = 3 * fps
        self.damage = 10

    def update(self, player):
        # determining the direction of the movement based on the player location
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # getting the direction in radius
        direction = math.atan2(dy, dx)
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2)

        # if the player is close enough, the enemy will explode
        if distance <= 2:
            if self.exploding_counter == 3*fps:
                self.image = pygame.transform.scale(pygame.image.load("images/explosion.png").convert_alpha(),
                                                    (15, 15))  # change to explosion image
            self.exploding_counter -= fps/2
            if self.exploding_counter == 0:
                self.explode(player)

        else:
            self.move(direction)



    def move(self, direction):
        # moving the enemy towards the player --> like bullet
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def explode(self, player):
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2)
        self.kill()
        if distance <= 2:
            player.take_damage(self.damage)