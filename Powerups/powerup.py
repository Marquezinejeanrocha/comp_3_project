from abc import ABC, abstractmethod

import pygame
from pygame.sprite import Sprite

class PowerUp(ABC, Sprite):
    @abstractmethod
    def __init__(self, name, image, duration,cooldown):
        super().__init__()
        self.name = name
        self.image= pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.duration = duration
        self.cooldown = cooldown



    @abstractmethod
    def affect_game(self):
        pass

    @abstractmethod
    def affect_player(self, player):
        pass

    def couting(self):
        cooldown = self.cooldown
        self.cooldown -=1
        if self.cooldown == 0:
            self.cooldown = cooldown
        return self.cooldown
