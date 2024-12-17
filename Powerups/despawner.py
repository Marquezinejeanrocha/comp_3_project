from powerup import PowerUp
from config import *

class Despawner(PowerUp):
    def __init__(self, enemies_cooldown):
        super().__init__(name="despawner", image = "despawner.png", duration = 10, cooldown = 15)
        self.cooldown = enemies_cooldown

    def affect_game(self):
        cooldown_time = 30 * fps
        return cooldown_time

    def affect_player(self, player):
        pass