import pygame
from abc import ABC, abstractmethod

class PowerUp(ABC):
    """
    A base class for power-ups.

    Attributes:
        rect (pygame.Rect): The rectangle representing the power-up's position and size.
        active (bool): A flag indicating whether the power-up is active.
        image (pygame.Surface): The image representing the power-up (optional).
        color (tuple): The color of the power-up for debugging purposes (optional).

    Methods:
        affect_player(self, player):
            Abstract method to apply the power-up effect to the player.
        
        affect_game(self, player, enemy):
            Abstract ethod to apply the power-up effect to the game.

        draw(self, screen):
            Draws the power-up on the screen.
    """
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
    @abstractmethod
    def affect_game(self, player, enemy):
        """Apply the power-up effect to the game."""
        pass

    def draw(self, screen):
        """
        Draws the power-up on the screen.

        Parameters:
        screen (pygame.Surface): The surface on which to draw the power-up.
        """
        if self.active:
            if hasattr(self, 'image'):  # Check if the image exists
                screen.blit(self.image, self.rect)  # Draw the image
            else:
                pygame.draw.rect(screen, self.color, self.rect)  # Default drawing
