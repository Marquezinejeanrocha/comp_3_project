import pygame.image
from pygame.sprite import Sprite



class Chest(pygame.sprite.Sprite):
    TILE_SIZE = 32

    def __init__(self, x, y, life=50):
        #change the life later. short life for testing
        super().__init__()
        self.image  = pygame.image.load("images/chestfull.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.life = life
        self.is_exploded = False
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TILE_SIZE
        self.rect.y = y * self.TILE_SIZE

        # Add a key representation
        self.key_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.key_image, (255, 255, 0), (15, 15), 15)  # Yellow circle
        self.key_rect = self.key_image.get_rect(center=self.rect.center)
        self.key_available = False  # Key is initially unavailable

    def dead(self):
        if self.life >=0:
            self.image = pygame.image.load("images/chestbroken.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.is_exploded = True


    def draw(self, screen):
        # Draw the chest
        screen.blit(self.image, self.rect.topleft)

        # Draw the key if available
        if self.key_available and self.is_exploded:
            screen.blit(self.key_image, self.key_rect.topleft)

    def collect_key(self, player_group):

        for player in player_group:
            if player.rect.colliderect(self.key_rect):
                print("Key collected by player!")
                self.key_available = False

                # player has a key with this he will open the door
                player.has_key = True

    def update(self, player_group):
        # Check for collision with players if key is available
        if self.key_available and pygame.sprite.spritecollideany(self, player_group):
            self.collect_key(player_group)


