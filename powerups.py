import random
from powerups_parent import PowerUp
import pygame


class SpeedBoost(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.color = (0, 255, 0)  # Green for SpeedBoost

    def apply_effect(self, player):
        if not player.active_powerup:  # Only apply if no power-up is active
            player.speed += 2  # Increase player speed
            player.active_powerup = "SpeedBoost"
            player.powerup_timer = pygame.time.get_ticks() + 3000  # Set a 3-second timer
            print("Speed Boost Activated!")


class Shield(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.color = (0, 0, 255)  # Blue for Shield

    def apply_effect(self, player):
        player.shield_active = True  # Activate shield
        print("Shield Activated!")


def spawn_powerups(powerups, screen_width, screen_height):
    if random.randint(0, 200) < 1:  # 2% chance to spawn a power-up each frame
        x = random.randint(0, screen_width - 20)
        y = random.randint(0, screen_height - 20)
        powerup_type = random.choice([SpeedBoost, Shield])
        powerups.append(powerup_type(x, y))


def handle_powerup_collisions(players, powerups):
    for powerup in powerups[:]:  # Iterate over a copy to safely remove power-ups
        if powerup.active:
            if pygame.sprite.spritecollideany(powerup, players):
                # Apply effect and deactivate power-up
                for player in players:
                    if player.rect.colliderect(powerup.rect):  # Ensure the right player gets the effect
                        if not player.active_powerup:  # Only apply if no power-up is active
                            powerup.apply_effect(player)
                            powerup.active = False
                            break  # One player picks up the power-up
                powerups.remove(powerup)  # Remove from the list

