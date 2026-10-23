class animal:
    def __init__(self,name):
        self.name=name
    def sound(self):
        ...
class dog:
    def __init__(self,name):
        self.name=name
    def sound(self):
        print(self.name ,"Barks")
Doberman=dog("doberman")

Doberman.sound()