from Powerups.powerup import PowerUp

class Invencibility(PowerUp):
    def __init__(self, name):
        super().__init__(name=name, duration= 5, cooldown= 20, image="invencibility.png")

    def affect_game(self,enemies):
        while self.duration >=0 :
            enemies.damage = 0
            self.duration-=1
        return enemies

    def affect_player(self, player):
        if player.health==0:
            player.health = 1
        return player