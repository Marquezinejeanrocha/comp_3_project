from abc import ABC, abstractmethod
import pygame
from config import *
from abc import ABC, abstractmethod

class PowerUp(ABC):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # Default color for debugging
        self.active = True

    @abstractmethod
    def apply_effect(self, player):
        """Apply the power-up effect to the player."""
        pass

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
