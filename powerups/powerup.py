from abc import ABC, abstractmethod
import pygame
from config import *

class PowerUp(ABC):
    def __init__(self, image, duration):
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
