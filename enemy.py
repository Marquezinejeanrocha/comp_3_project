
from config import *
import pygame
import random
import math
from player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, animation_idle_frames, animation_death_frames):
        super().__init__()
        self.idle_frames = animation_idle_frames  # List of idle animation frames
        self.death_frames = animation_death_frames  # List of death animation frames
        self.current_frame = 0  # Current frame index
        self.image = self.idle_frames[self.current_frame]  # Set the initial image

        # Positioning and movement
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - enemy_size[0])
        self.rect.y = random.randint(0, height - enemy_size[-1])
        self.speed = random.randint(1, 3)

        # Health and state
        self.health = 10
        self.is_exploding = False
        self.exploding_counter = 3 * fps

    def update(self, player):
        if self.is_exploding:
            self.animate_death()
        else:
            self.animate_idle()
            self.chase_player(player)

    def animate_idle(self):
        # Cycle through idle frames
        self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
        self.image = self.idle_frames[self.current_frame]

    def animate_death(self):
        # Show death animation and remove sprite after it ends
        if self.current_frame < len(self.death_frames):
            self.image = self.death_frames[self.current_frame]
            self.current_frame += 1
        else:
            self.kill()  # Remove sprite when animation finishes

    def chase_player(self, player):
        # Determine movement direction
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        direction = math.atan2(dy, dx)
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2)

        if distance <= 2:
            self.start_explosion()
        else:
            self.move(direction)

    def move(self, direction):
        # Move towards the player
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def start_explosion(self):
        self.is_exploding = True
        self.current_frame = 0  # Reset animation frame to start of death sequence

    def explode(self, player):
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2)
        if distance <= 2:
            player.take_damage(10)
