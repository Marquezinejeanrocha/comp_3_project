from abc import ABC, abstractmethod

import pygame
from pygame.sprite import Sprite

from config import *

class PowerUp(ABC, Sprite):
    @abstractmethod
    def __init__(self, name, image, duration,cooldown):
        super().__init__()
        self.name = name
        self.image= pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(image[0]), int(image[1])))
        self.rect = self.image.get_rect()
        self.duration = duration
        self.cooldown = cooldown



    @abstractmethod
    def affect_game(self):
        pass

    @abstractmethod
    def affect_player(self, player):
        pass
