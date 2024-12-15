from config import *
import math
import pygame
 
# everything that moves has to be a child of sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        self.image = pygame.image.load("ui/bullet_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        # getting rectangle for positioning

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7  # todo: change the speed when catching a powerup

    def update(self, wall_group):

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
