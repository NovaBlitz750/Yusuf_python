"question number 1: Dog"
class animal:
    def sound(self):
        pass
class dog(animal):
    def __init__(self,name):
        self.name=name
    def sound(self,name):
        self.name=name
        print(name, "is barking")
husky=dog("Husky")
husky.sound("Husky")
"Question number 2: Bike"
class vehicle:
    def move(self):
        pass
class bike(vehicle):
    def move(self):
        print("Bike is driving very fast")
bikee=bike()
bikee.move()
"Question 3: Person"
class person:
    def intro(self):
        pass
class teacher:
    def intro(self):
        print("Hello I am ur new teacher :)")
mrs=teacher()
mrs.intro()