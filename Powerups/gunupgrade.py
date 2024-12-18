from Powerups.powerup import PowerUp
from player import Player

class GunUpgrade(PowerUp):
    def __init__(self):
        super().__init__(name= "gunUpgrade", image = "ui/gunupgrade.png", duration = 30, cooldown=0)

    def affect_game(self):
        pass

    def affect_player(self, player):
        player.weapon_power *= 2
        player.bullet_cooldown -= 3
        return