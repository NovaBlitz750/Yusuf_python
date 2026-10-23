class IOString:
    def _init__(self):
        self.str=''
    def inp(self):
        self.str=input("Enter a string value ")
    def uc(self):
        print(self.str.upper())
str1=IOString()
str1.inp()
str1.uc()