import random
from powerups_parent import PowerUp
import pygame
import config


class SpeedBoost(PowerUp):
    """
    A class representing a Speed Boost power-up.

    Attributes:
    ----------
    color : tuple - The color representation of the Speed Boost power-up.

    Methods:
    -------
    affect_player(player): Increases the player's speed and sets a timer for the power-up duration.

    """
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/SpeedBoost.png")
        self.color = config.green  # Green for SpeedBoost

    def affect_player(self, player):
        """
        Applies a speed boost power-up to the player if no other power-up is active.
        Args:
            player (Player): The player object to which the power-up will be applied.
        """
        if not player.active_powerup:  # Only apply if no power-up is active
            player.speed += 2 
            player.active_powerup = "SpeedBoost"
            player.powerup_timer = pygame.time.get_ticks() + 3000  # Set a 3-second timer
            print("Speed Boost Activated!")

    def affect_game(self, player, enemy):
        pass


class Shield(PowerUp):
    """
    Shield is a type of PowerUp that restores the player's health to full when activated.

    Attributes:
        color (tuple): The color representation of the shield, default is blue.

    Methods:
        affect_player(player):
            Restores the player's health to 100 and prints "Shield Activated!".
    """
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/Shield.png")
        self.color = config.blue

    def affect_player(self, player):
        """
        Restores the player's health to 100 and prints "Shield Activated!".
        Args:
            player (Player): The player object that will be affected by the power-up.
        """
        player.health = 100
        print("Shield Activated!")

    def affect_game(self, player, enemy):
        pass

class Despawner(PowerUp):
    '''
    A power-up that removes a specified number of enemies from the game when collected by the player.

    Attributes:
        color (tuple): The color representation of the Despawner power-up.

    Methods:
        affect_player(player):
            Placeholder method to define the effect on the player.
        
        affect_game(player, enemy_group):
            Removes enemies from the enemy group targeting the player if no other power-up is active.
            '''
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/Despawner.png")
        self.color = config.red

    def affect_player(self, player):
        pass

    def affect_game(self, player, enemy_group):
        """
        Removes enemies from the enemy group targeting the player if no other power-up is active.
        Args:
            player (Player): The player object that collected the power-up.
            enemy_group (pygame.sprite.Group): The group of enemies targeting the player.
        """
        if not player.active_powerup:  # Only apply if no power-up is active
            for enemy in enemy_group:
                if len(enemy_group) > 1:
                    enemy.kill()

class Invisible(PowerUp):
    """
    A class representing the Invisible power-up in the game.

    Attributes:
    ----------
    color : tuple - The color representation of the power-up (default is blue).

    Methods:
    -------
    affect_player(player):
        Applies the invisible effect to the player if no other power-up is active.
    """
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "ui/powerups/Invisible.png")
        self.color = config.blue

    def affect_player(self, player):
        """
        Applies the invisible power-up effect to the player if no power-up is currently active.

        Args:
            player (Player): The player object to which the power-up effect will be applied.

        """
        if not player.active_powerup:  # Only apply if no power-up is active
            player.invisible = True
            player.active_powerup = "Invisible"
            player.powerup_timer = pygame.time.get_ticks() + 3000  # Set a 3-second timer
            print("invisible Activated!")

    def affect_game(self, player, enemy):
        pass



def spawn_powerups(powerups, screen_width, screen_height):
    """
    Spawns power-ups randomly on the screen with a 2% chance each frame.

    Parameters:
    powerups (list): The list to which new power-ups will be appended.
    screen_width (int): The width of the screen where power-ups can spawn.
    screen_height (int): The height of the screen where power-ups can spawn.
    """
    if random.randint(0, 200) < 1:  # 2% chance to spawn a power-up each frame
        x = random.randint(0, screen_width - 20)
        y = random.randint(0, screen_height - 20)
        powerup_type = random.choice([SpeedBoost, Shield, Despawner, Invisible])
        if len(powerups) < 3:
            powerups.append(powerup_type(x, y))



def handle_powerup_collisions(players, powerups, enemy_groups):
    """
    Handle collisions between players and power-ups, applying the power-up effects
    and removing the power-up from the game once it has been used.

    Args:
        players (list): A list of player objects, each with a 'rect' attribute for collision detection.
        powerups (list): A list of power-up objects, each with 'active' and 'rect' attributes, and
                         'affect_game' or 'affect_player' methods.
        enemy_groups (list): A list of enemy group objects, corresponding to each player.
    """
    # Iterate over a copy of the power-ups list to safely remove power-ups
    for powerup in powerups[:]: 
        if powerup.active:
            # Check for collisions between players and power-ups
            for player, enemy_group in zip(players, enemy_groups):
                if player.rect.colliderect(powerup.rect):  # Ensure the right player gets the effect
                    # Apply the power-up effect and remove the power-up from the game
                    if isinstance(powerup, Despawner):
                        powerup.affect_game(player, enemy_group)
                    else:
                        powerup.affect_player(player)
                    powerup.active = False
                    powerups.remove(powerup)
                    break  # Exit loop once the power-up is handled


