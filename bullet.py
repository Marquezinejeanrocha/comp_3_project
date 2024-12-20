from config import *
import math
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        #self.image = pygame.image.load("ui/bullet_1.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (50,50))
        # getting rectangle for positioning

        self.speed = 5
        self.weapon_power = 0
        self.image = pygame.image.load(f"ui/skins/bullet_{self.weapon_power}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_image_skin(self):
        """Update the player's image dynamically based on the shield state."""
        self.image = pygame.image.load(f"ui/skins/bullet_{self.weapon_power}.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        if self.weapon_power == 1:
            self.speed = 7
        elif self.weapon_power == 2:
            self.speed = 10

    def update(self, wall_group):
        self.update_image_skin()
        # updating the bullets position based in the speed and direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

        wall_collision= pygame.sprite.spritecollide(self, wall_group, False)
        if wall_collision:
            self.kill()

    def draw(self, screen):
        # pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        screen.blit(self.image, self.rect)
