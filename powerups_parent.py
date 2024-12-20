import pygame
from abc import ABC, abstractmethod

class PowerUp(ABC):
    def __init__(self, x, y, width, height, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True
        if image_path:
            self.image = pygame.image.load(image_path)  # Load the image
            self.image = pygame.transform.scale(self.image, (width, height))  # Resize image
        else:
            self.color = (255, 255, 255)  # Default color for debugging

    @abstractmethod
    def affect_player(self, player):
        """Apply the power-up effect to the player."""
        pass

    def affect_game(self, player, enemy):
        pass

    def draw(self, screen):
        if self.active:
            if hasattr(self, 'image'):  # Check if the image exists
                screen.blit(self.image, self.rect)  # Draw the image
            else:
                pygame.draw.rect(screen, self.color, self.rect)  # Default drawing
