class car:
    def __init__(self,speed,mileage):
        self.speed=speed
        self.mileage=mileage
    def show_trait(self):
        print("Speed = ",self.speed)
        print("Mileage = ",self.mileage)
class luxury_car(car):
    def __init__(self,speed,mileage,price,km_used):
        self.price=price
        self.km_used=km_used
        super().__init__(speed,mileage)
    def show_trait(self):
        super().show_trait()
        print("Price = ",self.price)
        print("KM used = ",self.km_used)
lambo=luxury_car(260,16.9,900000,10000)
lambo.show_trait()