from config import *
import math
import pygame

class Bullet(pygame.sprite.Sprite):
    """
    A class to represent a bullet in the game.

    Attributes:
    -----------
    direction (Float) : The direction in which the bullet is moving.
    speed (int) : The speed at which the bullet travels.
    weapon_power (int) : The power level of the bullet, which affects its speed and image.
    image (pygame.Surface) : he image representing the bullet.
    rect (pygame.Rect) :The rectangle representing the bullet's position and size.

    Methods:
    --------
    update_image_skin():
        Updates the bullet's image and speed based on its weapon power.
    update(wall_group):
        Updates the bullet's position and checks for collisions with walls.
    draw(screen):
        Draws the bullet on the given screen.
    """
    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        self.speed = 5
        self.weapon_power = 0
        self.image = pygame.image.load(f"ui/skins/bullet_{self.weapon_power}.png").convert_alpha() #convert_alpha() is used to make the image transparent
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_image_skin(self):
        """
        Updates the image and speed of the bullet based on its weapon power.

        The image is loaded from the file system based on the current weapon power,
        and then scaled to a fixed size. The speed of the bullet is also adjusted
        based on the weapon power.
        """
        self.image = pygame.image.load(f"ui/skins/bullet_{self.weapon_power}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.speed = 5 + self.weapon_power * 2

    def update(self, wall_group):
        """
        Update the bullet's position and handle collisions.

        This method updates the bullet's position based on its speed and direction.
        It also checks if the bullet goes off-screen and removes it if necessary.
        Additionally, it checks for collisions with walls and removes the bullet
        if a collision is detected.

        Args:
            wall_group (pygame.sprite.Group): The group of wall sprites to check for collisions.
        """
        self.update_image_skin()
        # updating the bullets position based in the speed and direction
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

        # killing the bullet if it collides with a wall
        wall_collision= pygame.sprite.spritecollide(self, wall_group, False)
        if wall_collision:
            self.kill()

    def draw(self, screen):
        '''Draws the bullet on the given screen.'''
        screen.blit(self.image, self.rect)
