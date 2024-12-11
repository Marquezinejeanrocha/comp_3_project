from powerup import PowerUp
from player import Player

class GunUpgrade(PowerUp):
    def __init__(self):
        super().__init__(name= "gunUpgrade", image = "gun_upgrade.png", duration = 30)

    def affect_game(self):
        pass

    def affect_player(self, player: Player):
        player.weapon_power *= 2
        player.bullet_cooldown -= 3
        return