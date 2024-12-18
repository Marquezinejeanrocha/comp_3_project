import pygame


class Wall(pygame.sprite.Sprite):
    TILE_SIZE = 36  # Define the size of each wall tile

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/wallblock_3.png")
        self.image = pygame.transform.scale(self.image, (self.TILE_SIZE, self.TILE_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x = x * self.TILE_SIZE
        self.rect.y = y * self.TILE_SIZE

        