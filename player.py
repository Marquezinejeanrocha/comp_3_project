from utils import *
from config import *
import pygame 
import math
from bullet import Bullet
 
# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self, color, location,  controls):
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

        self.controls = controls  

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0
        self.weapon_power = 1
        self.coins = 100
        self.shield = 0

    def update(self, wall_group):
        # getting the keys input
        keys = pygame.key.get_pressed()
        # Store the original position before movement
        original_x = self.rect.x
        original_y = self.rect.y

        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[self.controls['down']] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[self.controls['left']] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[self.controls['right']] and self.rect.right < width:
            self.rect.x += self.speed

        # Check for wall collisions after movement
        wall_collision = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_collision:
            # If collision detected, revert to the original position
            self.rect.x = original_x
            self.rect.y = original_y

    def shoot(self, bullets):
        """
        bullets --> pygame group where I will add bullets
        """
        # todo: different weapons have different cooldowns
        if self.health <= 0:
            return

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
