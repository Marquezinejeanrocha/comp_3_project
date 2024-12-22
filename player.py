from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from Powerups.powerup import PowerUp
from Powerups.invencibility import Invencibility
import json


class Player(pygame.sprite.Sprite):  
    """A class to represent the players of the game.

    Attributes
    ----------
    health : int - The health of the player.
    bullet_cooldown : int - The cooldown period between bullets.
    weapon_power : int - The power of the player's weapon.
    coins : int - The number of coins the player has.
    skin : int - The skin type of the player.
    speed : int - The speed of the player.
    powerup : str or None - The current power-up the player has.
    active_powerup : str or None - The currently active power-up.
    powerup_timer : int - The timer to track power-up duration.
    invisible : bool - Whether the player is invisible.
    has_key : bool - Whether the player has a key.
    alive : bool - Whether the player is alive.
    respawn_timer : int or None - The timer for respawn.
    image : pygame.Surface - The image representing the player.
    rect : pygame.Rect - The rectangle representing the player's position.
    controls : dict - The control keys for the player.
    start_location : tuple - The initial location of the player.
    original_image : pygame.Surface - The original image of the player.

    Methods
    -------
    update_image_skin(): Updates the player's image dynamically based on the shield state.
    update(wall_group): Updates the player's state and handles movement and collisions.
    remove_powerup(): Removes the active power-up and reverts its effects.
    shoot(bullets, key): Shoots bullets in four directions if the cooldown allows.
    take_damage(damage): Reduces the player's health by the specified damage amount.
    hospital(delta_time): Regains 20% health per second, without surpassing 100%.
    die(): Handles the player's death and sets a respawn timer.
    respawn(): Respawns the player at the start location with full health.
    save_player_data(filename): Saves the player's data to a file.
    load_player_data(filename): Loads the player's data from a file.
    draw(screen): Draws the player and any active power-up indicators on the screen.
    reset_player(): Resets the player's attributes to their initial values."""

    def __init__(self, color, location, controls):
        # calling the mother classes init aka Sprite
        super().__init__()

        # GAMEPLAY VARIABLES
        self.health = 100
        self.bullet_cooldown = 0
        self.weapon_power = 0
        self.coins = 100
        self.skin = 0
        if self.skin == 1:
            self.speed = 4
        elif self.skin == 2:
            self.speed = 7
        else:
            self.speed = 3
        self.powerup = None
        self.active_powerup = None  # To track the current power-up
        self.powerup_timer = 0  # Timer to track power-up duration
        self.invisible = False
        self.has_key = False
        self.alive = True
        self.respawn_timer = None  # Timer for respawn

        # VISUAL VARIABLES
        self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_up.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.controls = controls
        self.start_location = location  # Store the initial location for respawn
        self.original_image = self.image


    def update_image_skin(self):
        """Update the player's image dynamically based on the shield state."""

        self.image = pygame.image.load(f"ui/skins/skin_{self.skin}_up.png")
        self.image = pygame.transform.scale(self.image, (30, 30))


    def update(self, wall_group):
        """
        Update the player's state, including movement, image update, and collision detection.

        Parameters:
        wall_group (pygame.sprite.Group): Group of wall sprites to check for collisions.
        """

        if not self.alive:
            # Check if it's time to respawn
            if self.respawn_timer and pygame.time.get_ticks() >= self.respawn_timer:
                self.respawn()  
            return  # Skip further updates if dead

        self.update_image_skin()

        # getting the keys input
        keys = pygame.key.get_pressed()
        # Store the original position before movement
        original_x = self.rect.x
        original_y = self.rect.y

        # checking which keys where pressed and moving the player accordingly
        if keys[self.controls['up']] and self.rect.top > 0:
            self.image = pygame.image.load(
                f"ui/skins/skin_{self.skin}_up.png")  # we use surface to display any image or draw
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.y -= self.speed
        if keys[self.controls['down']] and self.rect.bottom < height:
            self.image = pygame.image.load(
                f"ui/skins/skin_{self.skin}_down.png")  
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect.y += self.speed

        if keys[self.controls['left']] and self.rect.left > 0:
            self.image = pygame.image.load(
                f"ui/skins/skin_{self.skin}_left.png")  
            self.image = pygame.transform.scale(self.image, (30, 30))

            self.rect.x -= self.speed
        if keys[self.controls['right']] and self.rect.right < width:
            self.image = pygame.image.load(
                f"ui/skins/skin_{self.skin}_right.png")  
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect.x += self.speed

        # Check for wall collisions after movement
        wall_collision = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_collision:
            # If collision detected, revert to the original position
            self.rect.x = original_x
            self.rect.y = original_y

        if self.active_powerup and pygame.time.get_ticks() > self.powerup_timer:
            self.remove_powerup()

    def remove_powerup(self):
        """
        Removes the currently active power-up from the player.
        """
        # Revert the effects of the speed and invisibility power-ups
        if self.active_powerup == "SpeedBoost":
            self.speed -= 2  # Revert speed boost
        elif self.active_powerup == "Invisible":
            self.invisible = False
        self.active_powerup = None  # Clear the active power-up

    def shoot(self, bullets, key):
        """
        Handles the shooting mechanism for the player.

        Parameters:
        bullets (pygame.sprite.Group): The group to which new bullets will be added.
        key (str): The key that triggers the shooting action ('space' or 'enter').
        """
        # If the player is dead, don't shoot
        if self.health <= 0:
            return
        
        # getting the keys input
        keys = pygame.key.get_pressed()
        if key == 'space' and keys[pygame.K_SPACE]:
            # if the cooldown is 0, we can shoot. Cooldown is how many frames we have to wait to shoot
            if self.bullet_cooldown <= 0:
                # these 4 directions, are in order, right, left, up and down
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                    bullet.weapon_power = self.weapon_power
                    bullet.image = pygame.transform.scale(bullet.image, (10, 10))
                    bullets.add(bullet)

                # resetting the cooldown
                self.bullet_cooldown = fps * 2

            if self.skin == 1:
                self.bullet_cooldown -= 10

            elif self.skin == 2:
                self.bullet_cooldown -= 20

            else:
                self.bullet_cooldown -= 3

        #The same as above, but for the enter key
        if key == 'enter' and keys[pygame.K_RETURN]:
            if self.bullet_cooldown <= 0:
                for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                    bullet.weapon_power = self.weapon_power
                    bullet.image = pygame.transform.scale(bullet.image, (10, 10))
                    bullets.add(bullet)
                self.bullet_cooldown = fps * 2

            if self.skin == 1:
                self.bullet_cooldown -= 10

            elif self.skin == 2:
                self.bullet_cooldown -= 20

            else:
                self.bullet_cooldown -= 3

    def take_damage(self, damage):
        """
        Reduces the player's health by the specified damage amount if the player is not invisible.
        If the player's health drops to 0 or below, triggers the player's death.

        Args:
            damage (int): The amount of damage to inflict on the player.
        """

        if self.health > 0:
            if self.invisible:
                pass
            else:
                self.health -= damage

        # Check for player death
        elif self.health <= 0:
            self.die()

    def hospital(self, delta_time):
        """
        Heals the player over time.
        Args:
            delta_time (float): The time elapsed since the last update, in seconds.
        """
        # regains 20% helth per second, without surpassing 100%
        heal_rate = 20  
        self.health += heal_rate * delta_time
        if self.health > 100:
            self.health = 100

    def die(self):
        """
        Handles the player's death by setting the alive status to False,
        initializing a respawn timer, and updating the player's image to an explosion.
        """
        self.alive = False
        self.respawn_timer = pygame.time.get_ticks() + 3000
        self.image = pygame.image.load("images/explosion.png")
        self.image = pygame.transform.scale(self.image, (30, 30))

    def respawn(self):
        """
        Respawn the player by resetting their status and position.

        This method sets the player's alive status to True, resets the respawn timer,
        restores the player's health to full, and moves the player back to their 
        starting location. It also resets the player's image to the original image.
        """
        self.alive = True
        self.respawn_timer = None
        self.health = 100
        self.rect.center = self.start_location 
        self.image = self.original_image



    def save_player_data(self, filename):
        """
        Save the player's data to a file in JSON format.
        Args:
            filename (str): The name of the file where the player's data will be saved.
        """
        player_data = {

            'weapon_power': self.weapon_power,
            'coins': self.coins,
            'skin': self.skin
        }
        with open(filename, 'w') as file:
            json.dump(player_data, file)

    def load_player_data(self, filename):
        """
        Load player data from a JSON file.

        Parameters:
        filename (str): The path to the JSON file containing player data.
        """
        with open(filename, 'r') as file:
            player_data = json.load(file)
            self.weapon_power = player_data['weapon_power']
            self.coins = player_data['coins']
            self.skin = player_data['skin']

    def draw(self, screen):
        """
        Draws the player and any active power-up indicators on the screen.

        Args:
            screen (pygame.Surface): The surface on which to draw the player and power-up indicators.

        Draws the player's image at the player's rectangle position. If the player has an active power-up,
        it draws a circle around the player to indicate the power-up type:
            - Green circle for "SpeedBoost"
            - Blue circle for "Invisible"
        """
        # Draw the player rectangle
        screen.blit(self.image, self.rect)

        # Draw a circle if SpeedBoost is active
        if self.active_powerup == "SpeedBoost":
            pygame.draw.circle(
                screen,
                (0, 255, 0),  # Green for SpeedBoost
                self.rect.center,  # Center of the player's rectangle
                self.rect.width // 2 + 10,  # Radius slightly larger than the player
                2  # Thickness of the circle outline
            )

        elif self.active_powerup == "Invisible":
            pygame.draw.circle(
                screen,
                (0, 0, 255),  # Green for SpeedBoost
                self.rect.center,  # Center of the player's rectangle
                self.rect.width // 2 + 10,  # Radius slightly larger than the player
                2  # Thickness of the circle outline
            )

    def reset_player(self):
        """
        Resets the player's attributes to their default values.
        """
        self.weapon_power = 0
        self.coins = 0
        self.skin = 0


