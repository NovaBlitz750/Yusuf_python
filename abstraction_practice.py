from abc import ABC, abstractmethod

class animal:
    @abstractmethod
    def eat(self):
        ...
class dog(animal):

    def eat(self):
        print("Dog is chewing on a bone")
husky=dog()
husky.eat()
class shape:
    @abstractmethod
    def area(self):
        pass
class square(shape):
    def area(self):
        print("Side*Side")
sq=square()
sq.area()
class vehicle:
    @abstractmethod
    def drive(self):
        pass
class car(vehicle):
    def drive(self):
        print("Car is driving")
