from abc import ABC, abstractmethod

import pygame
from pygame.sprite import Sprite

from config import *

<<<<<<<< HEAD:Powerups/powerup.py

class PowerUp(ABC, Sprite):
    @abstractmethod
    def __init__(self, name, image, duration,cooldown):
        super().__init__()
        self.name = name
========
class PowerUp(ABC):
    def __init__(self, image, duration):
>>>>>>>> origin/comp_3:powerups/powerup.py
        self.image = pygame.image.load("images/" + image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.rect = self.image.get_rect()
        self.duration = duration * fps

    @abstractmethod
    def affect_game(self):
        pass

    @abstractmethod
    def affect_player(self, player):
        pass
