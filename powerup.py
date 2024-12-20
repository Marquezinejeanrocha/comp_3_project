import random
from powerups_parent import PowerUp
import pygame


class SpeedBoost(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/SpeedBoost.png")
        self.color = (0, 255, 0)  # Green for SpeedBoost

    def affect_player(self, player):
        if not player.active_powerup:  # Only apply if no power-up is active
            player.speed += 2  # Increase player speed
            player.active_powerup = "SpeedBoost"
            player.powerup_timer = pygame.time.get_ticks() + 3000  # Set a 3-second timer
            print("Speed Boost Activated!")

    def affect_game(self, player, enemy):
        pass


class Shield(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/Shield.png")
        self.color = (0, 0, 255)  # Blue for health

    def affect_player(self, player):
        player.health = 100
        print("Shield Activated!")

    def affect_game(self, player, enemy):
        pass

class Despawner(PowerUp):
    def __init__(self, x, y, despawn_count):
        super().__init__(x, y, 30, 30, "ui/powerups/Despawner.png")
        self.color = (255, 0, 0)  # Red for Despawner
        self.despawn_count = despawn_count

    def affect_player(self, player):
        pass

    def affect_game(self, player, enemy_group):
        """
        Remove a specified number of enemies from the enemy group targeting the player.
        :param player: The player who collected the power-up.
        :param enemy_group: The group of enemies targeting this player.
        """
        # removed_count = 0
        # for enemy in enemy_group:
        #     if removed_count < self.despawn_count:
        #         enemy_group.remove(enemy)
        #         removed_count += 1
        # print(f"Despawner activated! Removed {removed_count} enemies for Player {player.id}.")
        if not player.active_powerup:  # Only apply if no power-up is active
            for enemy in enemy_group:
                if len(enemy_group) > 1:
                    enemy.kill()

class Invisible(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/Invisible.png")
        self.color = (100, 100, 100)  # Blue for health

    def affect_player(self, player):
        if not player.active_powerup:  # Only apply if no power-up is active
            player.invisible = True
            player.active_powerup = "Invisible"
            player.powerup_timer = pygame.time.get_ticks() + 3000  # Set a 3-second timer
            print("invisible Activated!")

    def affect_game(self, player, enemy):
        pass



def spawn_powerups(powerups, screen_width, screen_height):
    if random.randint(0, 200) < 1:  # 2% chance to spawn a power-up each frame
        x = random.randint(0, screen_width - 20)
        y = random.randint(0, screen_height - 20)
        powerup_type = random.choice([SpeedBoost, Shield, Despawner, Invisible])
        if len(powerups) < 3:
            if powerup_type == Despawner:
                powerups.append(Despawner(x, y, despawn_count=random.randint(1, 5)))
            else:
                powerups.append(powerup_type(x, y))



def handle_powerup_collisions(players, powerups, enemy_groups):
    for powerup in powerups[:]:  # Iterate over a copy to safely remove power-ups
        if powerup.active:
            for player, enemy_group in zip(players, enemy_groups):
                if player.rect.colliderect(powerup.rect):  # Ensure the right player gets the effect
                    if isinstance(powerup, Despawner):
                        powerup.affect_game(player, enemy_group)
                    else:
                        powerup.affect_player(player)
                    powerup.active = False
                    powerups.remove(powerup)
                    break  # Exit loop once the power-up is handled


