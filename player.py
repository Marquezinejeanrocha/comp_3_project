from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from Powerups.powerup import PowerUp
from Powerups.invencibility import Invencibility
import json


# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    pp_list = ["invincebility", "despawner", "gunUpgrade"]

    def __init__(self, color, location, controls):
        # calling the mother classes init aka Sprite
        super().__init__()


        # GAMEPLAY VARIABLES
        self.ship_direction = 'up'
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0
        self.weapon_power = 0
        self.coins = 100
        self.shield = 0
        self.skin = 0
        self.powerup = None

        # VISUAL VARIABLES
        self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_up.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.controls = controls
        self.start_location = location  # Store the initial location for respawn
        self.alive = True
        self.original_color = self.image
        self.respawn_timer = None  # Timer for respawn
        self.has_key = False

    def update_image_based_on_shield(self):
        """Update the player's image dynamically based on the shield state."""
        self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_up.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        if self.skin == 1:
            self.speed = 10

    def update(self, wall_group):

        if not self.alive:
            # Check if it's time to respawn
            if self.respawn_timer and pygame.time.get_ticks() >= self.respawn_timer:
                self.respawn()  # Respawn the player
            return  # Skip further updates if dead

        self.update_image_based_on_shield()


        # getting the keys input
        keys = pygame.key.get_pressed()
        # Store the original position before movement
        original_x = self.rect.x
        original_y = self.rect.y

        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if keys[self.controls['up']] and self.rect.top > 0:
            self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_up.png")  # we use surface to display any image or draw
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.y -= self.speed
        if keys[self.controls['down']] and self.rect.bottom < height:
            self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_down.png")  # we use surface to display any image or draw
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.y += self.speed
        if keys[self.controls['left']] and self.rect.left > 0:

            self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_left.png")  # we use surface to display any image or draw
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.x -= self.speed
        if keys[self.controls['right']] and self.rect.right < width:
            self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_right.png")  # we use surface to display any image or draw
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.x += self.speed

        # Check for wall collisions after movement
        wall_collision = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_collision:
            # If collision detected, revert to the original position
            self.rect.x = original_x
            self.rect.y = original_y

    def shoot(self, bullets, key):
        """
        bullets --> pygame group where I will add bullets
        """
        # todo: different weapons have different cooldowns
        if self.health <= 0:
            return
        # cooldown ==> how many frames I need to wait until I can shoot again
        keys = pygame.key.get_pressed()

        if key == 'space' and keys[pygame.K_SPACE]:
            if self.bullet_cooldown <= 0:
                # these 4 directions, are in order, right, left, up and down
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                    bullet.weapon_power = self.weapon_power
                    #angle_degrees = -math.degrees(angle)  # Convert radians to degrees and invert
                    #bullet.image = pygame.transform.rotate(bullet.image, angle_degrees)
                    bullet.image = pygame.transform.scale(bullet.image, (10,10))
                    bullets.add(bullet)
                # resetting the cooldown
                self.bullet_cooldown = fps * 2

            if self.skin == 1:
                self.bullet_cooldown -= 30
            else:
                self.bullet_cooldown -= 5


        if key == 'enter' and keys[pygame.K_RETURN]:
            if self.bullet_cooldown <= 0:
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                    angle_degrees = -math.degrees(angle)  # Convert radians to degrees and invert
                    bullet.image = pygame.transform.rotate(bullet.image, angle_degrees)
                    bullets.add(bullet)
                # resetting the cooldown
                self.bullet_cooldown = fps * 2
            self.bullet_cooldown -= 5

    def take_damage(self, damage):
        '''if self.powerup is not None and isinstance(self.powerup, Invencibility):
            return
        if self.shield > 0 and damage < self.shield:
            self.shield -= damage
        elif 0 < self.shield < damage:
            damage -= self.shield
            self.shield = 0
            self.health -= damage'''
        if self.health > 0:
            self.health -= damage

        # Check for player death
        elif self.health <= 0:
            self.die()
            
    def hospital(self, delta_time):
        # regains 20% helth per second, without surpassing 100%
        heal_rate = 20  # Porcentagem de cura por segundo
        self.health += heal_rate * delta_time
        if self.health > 100:
            self.health = 100

    def get_powerup(self, pp: PowerUp):
        collided = pygame.sprite.spritecollide(self, pp, False)
        pp.kill()
        if collided:
            self.powerup = pp
            cooldown_reset = pp.cooldown
            while pp.cooldown > 0:
                pp.cooldown -= 1
            pp.cooldown = cooldown_reset
            self.powerup = None

    def die(self):
        self.alive = False
        self.respawn_timer = pygame.time.get_ticks() + 3000
        self.image = pygame.image.load("images/explosion.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
                
    def respawn(self):
        self.alive = True
        self.respawn_timer = None
        self.health = 100
        self.rect.center = self.start_location  # Reset to the start location
        self.image = self.original_color

    def save_player_data(self, filename):
            player_data = {

                'weapon_power': self.weapon_power,
                'coins': self.coins,
                'skin': self.skin
            }
            with open(filename, 'w') as file:
                json.dump(player_data, file)

    def load_player_data(self, filename):
        with open(filename, 'r') as file:
            player_data = json.load(file)
            self.weapon_power = player_data['weapon_power']
            self.coins = player_data['coins']
            self.skin = player_data['skin']

    def reset(self):
        self.health = 100
        self.rect.center = self.start_location  
       
