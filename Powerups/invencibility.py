
from comp_3_project.Powerups.powerup import PowerUp


class Invencibility(PowerUp):
    def __init__(self):
        super().__init__(name='invencibility', duration= 5, cooldown= 20, image="ui/invisible.png")

    def affect_game(self,enemies):
        while self.duration >=0 :
            enemies.damage = 0
            self.duration-=1
        return enemies

    def affect_player(self, player):
        if player.health==0:
            player.health = 1
        return player