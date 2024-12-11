from powerup import PowerUp

class Despawner(PowerUp):
    def __init__(self):
        super().__init__(name="despawner", image = "despawner.png", duration = 10, cooldown = 15)

    def affect_game(self):
        pass

    def affect_player(self, player):
        pass