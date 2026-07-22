class dog:
    def __init__(self, speed, life, weight):
        self.speed=speed
        self.life=life
        self.weight=weight
doberman=dog(51,10,34)
husky=dog(46,13,27)
print(f"Doberman can run up to {doberman.speed}km/h, they live for about {doberman.life} years and weigh up to {doberman.weight}kgs")