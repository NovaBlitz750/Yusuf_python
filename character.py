class character:
    def __init__(self, health, speed, attack):
        self.health=health
        self.speed=speed
        self.attack=attack
    def showt(self):
        print("Health = ",self.health)
        print("Speed = ",self.speed)
        print("Attacking power = ",self.attack)
class sneakywarrior(character):
    def __init__(self,camouflage,health,speed,attack):
        self.camouflage=camouflage
        super().__init__(health,speed,attack)
    def showt(self):
        print(self.camouflage)
        super().showt()
ninja=sneakywarrior(70,100,80,30)
ninja.showt()