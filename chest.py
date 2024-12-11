import pygame.image
from pygame.sprite import Sprite


class Chest(pygame.sprite.Sprite):
    TILE_SIZE = 32

    def __init__(self, x, y, life=1000):
        super().__init__()
        self.image  = pygame.image.load("images/chestfull.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.life = life

        self.rect = self.image.get_rect()
        self.rect.x = x * self.TILE_SIZE
        self.rect.y = y * self.TILE_SIZE

    def dead(self):
        if self.life >=0:
            self.image = pygame.image.load("images/chestbroken.png")
            self.image = pygame.transform.scale(self.image, (50, 50))