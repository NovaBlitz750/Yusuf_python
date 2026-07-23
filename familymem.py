class familymem:
    def __init__(self,eyec ,height):
        self.eyec=eyec
        self.height=height
    def showt(self):
        print(self.eyec)
class kid(familymem):
    def __init__(self,name, interest, eyec, height):
        self.name=name
        self.interest=interest
        super().__init__(eyec,height)
    def showt(self):
        print(self.name)
        print(self.height)
        print(self.interest)
        super().showt()
Yusuf=kid("Yusuf", "Coding", "Brown", "150 cm")
Yusuf.showt()
print(issubclass(kid,familymem))