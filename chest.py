import pygame.image
from pygame.sprite import Sprite



class Chest(pygame.sprite.Sprite):
    TILE_SIZE = 32

    def __init__(self, x, y, life=150):
        '''
        Initializes a chest object with specified position and life.

        Attributes:
            image (pygame.Surface): The image representing the chest.
            life (int): The current life of the chest.
            is_exploded (bool): Status indicating if the chest has exploded.
            rect (pygame.Rect): The rectangle representing the chest's position and size.
            key_image (pygame.Surface): The image representing the key.
            key_rect (pygame.Rect): The rectangle representing the key's position and size.
            key_available (bool): Status indicating if the key is available.

        Methods:
            dead(): Changes the chest's image to an explosion and marks it as exploded.
            draw(screen): Draws the chest and the key (if available) on the screen.
            collect_key(player_group): Checks for collision with players and allows key collection.
            update(player_group): Updates the chest's state and checks for key collection.
            '''
        super().__init__()
        self.image  = pygame.image.load("images/destroyer.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.life = life
        self.is_exploded = False
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TILE_SIZE
        self.rect.y = y * self.TILE_SIZE

        # Add a key representation (bomb)
        self.key_image = pygame.image.load("images/bomb.png")
        self.key_image = pygame.transform.scale(self.key_image, (50, 24))
        self.key_rect = self.key_image.get_rect(center=self.rect.center)
        self.key_available = False  # Key is initially unavailable

    def dead(self):
        """
        Handles the death of the object by changing its image to an explosion and setting its exploded status.
        """
        if self.life >=0:
            self.image = pygame.image.load("images/explosion.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.is_exploded = True


    def draw(self, screen):
        '''
        Draws the chest and the key (if available) on the screen.
        Args:
            screen (pygame.Surface): The surface to draw on.
        '''
        # Draw the chest
        screen.blit(self.image, self.rect.topleft)

        # Draw the key if available
        if self.key_available and self.is_exploded:
            #Undraw the chest
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0)) 
            # Draw the key
            screen.blit(self.key_image, self.key_rect.topleft)

    def collect_key(self, player_group):
        """
        Checks if any player in the player_group has collided with the key and collects it.

        Args:
            player_group (iterable): The group of player objects to check for key collection.
        """

        for player in player_group:
            if player.rect.colliderect(self.key_rect) and self.is_exploded:
                print("Key collected by player!")
                self.key_available = False
                player.has_key = True

    def update(self, player_group):
        """
        Update the chest state by checking for collisions with the player group.

        Args:
            player_group (pygame.sprite.Group): The group of player sprites to check for collisions.
        """
        # Check for collision with players if key is available
        if self.key_available and pygame.sprite.spritecollideany(self, player_group):
            self.collect_key(player_group)


