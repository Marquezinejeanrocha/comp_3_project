from comp_3_project.Powerups.powerup import PowerUp
from comp_3_project.config import *

class Despawner(PowerUp):
    def __init__(self, enemies_cooldown):
        super().__init__(name="despawner", image = "ui/despawner.png", duration = 10, cooldown = 0)
        self.cooldown = enemies_cooldown

    def affect_game(self):
        cooldown_time = 30 * fps
        return cooldown_time

    def affect_player(self, player):
        pass